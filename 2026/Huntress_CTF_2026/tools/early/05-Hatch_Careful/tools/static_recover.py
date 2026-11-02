"""Static-only reconstructor for Hatch Careful Python fixtures; never imports or runs them."""
from __future__ import annotations
import ast, base64, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/'artifacts/single_solve/extracted'

def literal_assignments(tree):
    out={}
    for node in ast.walk(tree):
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            try: out[node.targets[0].id]=ast.literal_eval(node.value)
            except Exception: pass
    return out

def decode_material(material, codec):
    parts=codec.split('|'); form=parts[0]; transform=parts[1]; arg=parts[2] if len(parts)>2 else ''
    if form=='decimal_csv': data=bytes(map(int,material.split(',')))
    elif form=='decimal_dash': data=bytes(map(int,material.split('-')))
    elif form=='decimal_comma': data=bytes(map(int,material.split(',')))
    elif form=='decimal_pipe': data=bytes(map(int,material.split('|')))
    elif form=='decimal_bytes': data=bytes(map(int,material.split('.')))
    elif form=='reversed_decimal': data=bytes(map(int,material.split(',')))[::-1]
    elif form in ('integer_list','integer_tuple'): data=bytes(material)
    elif form=='reversed_integer_list': data=bytes(material)[::-1]
    elif form=='hex_colon': data=bytes.fromhex(material.replace(':',''))
    elif form=='hex_dash': data=bytes.fromhex(material.replace('-',''))
    elif form in ('hex_compact','hex_literal'): data=bytes.fromhex(material)
    elif form=='hex_escape':
        if isinstance(material,bytes): data=material
        else:
            escapes=re.findall(r'\\x([0-9a-fA-F]{2})',material)
            if len(escapes)*4 != len(material): raise ValueError(('unsupported hex_escape literal',codec))
            data=bytes.fromhex(''.join(escapes))
    elif form in ('base64_chunks','base64_literal'): data=base64.b64decode(material)
    elif form=='urlsafe_base64': data=base64.urlsafe_b64decode(material)
    else: raise ValueError((form,codec))
    n=int(arg,16) if arg and transform!='repeating_key_xor' else 0
    if transform=='identity': pass
    elif transform=='reverse_then_xor': data=bytes(x^n for x in data[::-1])
    elif transform=='reverse_bytes' or transform=='reverse': data=data[::-1]
    elif transform=='single_byte_xor': data=bytes(x^n for x in data)
    elif transform=='add_modulo_256': data=bytes((x-n)%256 for x in data)
    elif transform=='subtract_modulo_256': data=bytes((x+n)%256 for x in data)
    elif transform=='repeating_key_xor':
        key=bytes.fromhex(arg.replace(',',''))
        data=bytes(x^key[i%len(key)] for i,x in enumerate(data))
    elif transform=='rolling_xor':
        previous=int(arg,16); out=[]
        for value in data:
            out.append(value^previous); previous=value
        data=bytes(out)
    else: raise ValueError((transform,codec))
    return data.decode('ascii')

def recover_python(path):
    tree=ast.parse(path.read_text())
    vals=literal_assignments(tree)
    material=next(v for k,v in vals.items() if k.startswith('MATERIAL_'))
    codec=next(v for k,v in vals.items() if k.startswith('CODEC_'))
    decoded=decode_material(material,codec)
    fields=dict(item.split('=',1) for item in decoded.split('|') if '=' in item)
    return fields


def recover_vbscript(path):
    """Statically recover declared VBScript fixture metadata; never executes it."""
    text=path.read_text()
    material=re.search(r'Const\s+Material_\w+\s*=\s*"([^"]*)"',text,re.I).group(1)
    codec=re.search(r'Const\s+Codec_\w+\s*=\s*"([^"]*)"',text,re.I).group(1)
    parts=codec.split('|'); form,transform=parts[:2]; arg=parts[2] if len(parts)>2 else ''
    if form=='base64_chunks':
        width=(len(material)+3)//4
        packed=material[:width]+material[width:2*width]+material[2*width:3*width]+material[3*width:]
        data=base64.b64decode(packed)
    elif form=='base64_literal': data=base64.b64decode(material)
    elif form=='reversed_hex': data=bytes.fromhex(material.replace(':',''))[::-1]
    elif form=='reversed_decimal': data=bytes(map(int,material.split(',')))[::-1]
    elif form=='decimal_dash': data=bytes(map(int,material.split('-')))
    elif form=='decimal_comma': data=bytes(map(int,material.split(',')))
    elif form=='decimal_pipe': data=bytes(map(int,material.split('|')))
    elif form=='hex_dash': data=bytes.fromhex(material.replace('-',''))
    elif form=='hex_colon': data=bytes.fromhex(material.replace(':',''))
    elif form=='hex_compact': data=bytes.fromhex(material)
    else: raise ValueError(('unsupported VBScript representation',form,path.name))
    if transform=='identity': pass
    elif transform in ('reverse_bytes','reverse'): data=data[::-1]
    elif transform=='reverse_then_xor':
        n=int(arg,16); data=bytes(x^n for x in data[::-1])
    elif transform=='add_modulo_256':
        n=int(arg,16); data=bytes((x-n)%256 for x in data)
    elif transform=='subtract_modulo_256':
        n=int(arg,16); data=bytes((x+n)%256 for x in data)
    elif transform=='single_byte_xor':
        n=int(arg,16); data=bytes(x^n for x in data)
    elif transform=='repeating_key_xor':
        key=bytes.fromhex(arg.replace(',','')); data=bytes(x^key[i%len(key)] for i,x in enumerate(data))
    elif transform=='rolling_xor':
        previous=int(arg,16); out=[]
        for value in data:
            out.append(value^previous); previous=value
        data=bytes(out)
    else: raise ValueError(('unsupported VBScript transform',transform,path.name))
    fields=dict(item.split('=',1) for item in data.decode('ascii').split('|') if '=' in item)
    fields['representation']=form; fields['transform']=transform
    return fields


def recover_js(path):
    import json, re
    text=path.read_text()
    pm=re.search(r'packedText\s*=\s*([\s\S]*?);',text)
    m=None
    if pm:
        literals=re.findall(r'"((?:\\.|[^"\\])*)"',pm.group(1))
        if literals: m=(''.join(literals),)
    if m:
        raw=m[0]
        if re.fullmatch(r'\d+(?:-\d+)+',raw): data=bytes(int(x) for x in raw.split('-'))
        elif re.search(r'%[0-9a-fA-F]{2}',raw): data=bytes.fromhex(''.join(re.findall(r'%([0-9a-fA-F]{2})',raw)))
        elif ':' in raw and re.fullmatch(r'[0-9a-fA-F:]+',raw): data=bytes.fromhex(raw.replace(':',''))
        else: data=base64.b64decode(raw)
    else:
        arrays={}
        for am in re.finditer(r'(?:var|let|const)\s+([A-Za-z_$][\w$]*)\s*=\s*\[([\s\S]*?)\]\s*;',text):
            arrays[am.group(1)]=bytes(int(x,0) for x in re.findall(r'0x[0-9a-fA-F]+|\b\d+\b',am.group(2)))
        cm=re.search(r'([A-Za-z_$][\w$]*)\s*=\s*([A-Za-z_$][\w$]*)\.concat\(([^)]+)\)',text)
        if cm and cm.group(2) in arrays:
            names=[cm.group(2),*re.findall(r'[A-Za-z_$][\w$]*',cm.group(3))]
            if all(name in arrays for name in names): data=b''.join(arrays[name] for name in names)
            else: raise ValueError('unknown concatenated JS arrays '+path.name)
        elif arrays:
            payloads=[(name,value) for name,value in arrays.items() if name.lower() not in ('keybytes','recoveredmaterial','decodedbytes','decryptedbytes','d') and value]
            preferred=next((name for name in ('characters','item1','v_a19c','s','storedmaterial') if name in arrays and arrays[name]),None)
            if preferred: data=arrays[preferred]
            elif payloads: data=max(payloads,key=lambda item:len(item[1]))[1]
            else: raise ValueError('no literal material '+path.name)
        else: raise ValueError('no literal material '+path.name)
    dm=re.search(r'(?:function\s+decode_[A-Za-z0-9_]+\s*\([^)]*\)|decode_[A-Za-z0-9_]+\s*=\s*function[^\{]*\{)([\s\S]*?)return\s+[^;]+;',text)
    body=dm.group(1) if dm else ''
    recover_match=re.search(r'(?:function\s+recover_|(?:var|let|const)\s+recover_)',text)
    recover_start=recover_match.start() if recover_match else -1
    inspect_start=text.find('var inspect_',recover_start if recover_start>=0 else 0)
    recover_body=text[recover_start:inspect_start if inspect_start>=0 else len(text)] if recover_start>=0 else ''
    if re.search(r'\b[A-Za-z_$][\w$]*\.reverse\s*\(\)',recover_body): data=data[::-1]
    if '.reverse()' in body:
        data=data[::-1]
        key=re.search(r'\^\s*(\d+)',body)
        if key: data=bytes(x^int(key.group(1)) for x in data)
    elif 'keyBytes' in body:
        km=re.search(r'keyBytes\s*=\s*\[([^\]]+)\]',body); key=[int(x.strip(),0) for x in km.group(1).split(',')]
        data=bytes(x^key[i%len(key)] for i,x in enumerate(data))
    elif 'previous' in body and '^' in body:
        prevm=re.search(r'previous\s*=\s*(\d+)',body); prev=int(prevm.group(1)); out=[]
        for x in data: out.append(x^prev); prev=x
        data=bytes(out)
    elif re.search(r'\^\s*\d+',body):
        k=int(re.search(r'\^\s*(\d+)',body).group(1)); data=bytes(x^k for x in data)
    elif re.search(r'\w+\[i\]\s*-\s*\d+',body) and '% 256' in body:
        k=int(re.search(r'\w+\[i\]\s*-\s*(\d+)',body).group(1)); data=bytes((x-k)%256 for x in data)
    elif re.search(r'\w+\[i\]\s*\+\s*\d+',body) and '% 256' in body:
        k=int(re.search(r'\w+\[i\]\s*\+\s*(\d+)',body).group(1)); data=bytes((x+k)%256 for x in data)
    elif re.search(r'\w+\s*=\s*\w+\.slice\(0\)',body) or re.search(r'return\s+\w+\s*;',body): pass
    else: raise ValueError('unknown JS decoder '+path.name+' '+body[:160])
    return json.loads(data.decode('ascii'))


def recover_batch(path):
    """Reassemble inert HUNTRESS_INSPECT Batch assignments without running the file."""
    text=path.read_text()
    block=re.search(r'^:HUNTRESS_INSPECT\s*\r?\n([\s\S]*?)^:HUNTRESS_SEPARATOR_DONE\s*$',text,re.I|re.M)
    if not block: raise ValueError('inspect block missing '+path.name)
    values=[]
    for line in block.group(1).splitlines():
        m=re.match(r'\s*(?:set\s+)?"?((?:item|fragment|FrAg|h|v_a)\d+)=(.*)',line,re.I)
        if not m: continue
        value=m.group(2)
        if '"' in value: value=value.split('"',1)[0]
        value=re.sub(r'\^([|&<>])',r'\1',value)
        values.append(value)
    if not values: raise ValueError('inspect fragment assignments missing '+path.name)
    decoded=''.join(values)
    return dict(item.split('=',1) for item in decoded.split('|') if '=' in item)
