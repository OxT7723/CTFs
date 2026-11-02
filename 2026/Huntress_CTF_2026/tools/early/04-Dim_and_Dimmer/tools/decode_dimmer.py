import re,base64,json,pathlib,urllib.parse
root=pathlib.Path('/tmp/huntress-d4-dim-tt')

def decode_cmd(p,s):
 enc=re.search(r'(?im)^\s*rem HUNTRESS-MATERIAL:(\S+)',s).group(1)
 codec=re.search(r'(?im)^\s*rem HUNTRESS-CODEC:(\S+)',s).group(1)
 fmt,op=codec.split('|')
 if fmt in ('plain_fragments','split_fragments','base64_literal'):
  b=base64.b64decode(enc)
 elif fmt=='hex_pairs': b=bytes.fromhex(enc)
 elif fmt=='decimal_bytes': b=bytes(map(int,enc.split('.')))
 elif fmt=='reversed_text': b=base64.b64decode(enc[::-1])
 else: raise ValueError(codec)
 if op=='identity': pass
 elif op=='reverse': b=b[::-1]
 elif op=='xor_5a': b=bytes(x^0x5a for x in b)
 elif op=='reverse_xor':
  b=b[::-1]; key=b[0]^ord('v'); b=bytes(x^key for x in b)
 elif op=='add_7': b=bytes((x-7)%256 for x in b)
 elif op=='rotate_left': b=bytes(((x>>1)|(x<<7))&255 for x in b)
 else: raise ValueError(codec)
 return b.decode(errors='strict')

def decode_vbs(p,s):
 mat=re.search(r'Const Material_\w+ = "([^"]+)"',s).group(1)
 codec=re.search(r'Const Codec_\w+ = "([^"]+)"',s).group(1)
 parts=codec.split('|'); fmt,op=parts[:2]
 if fmt in ('hex_dash','hex_colon'):
  sep='-' if fmt=='hex_dash' else ':'; b=bytes.fromhex(mat.replace(sep,''))
 elif fmt=='hex_compact': b=bytes.fromhex(mat)
 elif fmt=='reversed_hex':
  b=bytes.fromhex(mat.replace(':','')); b=b[::-1]
 elif fmt in ('decimal_dash','decimal_pipe','decimal_comma','reversed_decimal'):
  sep='-' if fmt=='decimal_dash' else '|' if fmt=='decimal_pipe' else ','
  b=bytes(map(int,mat.split(sep)))
 elif fmt=='base64_literal': b=base64.b64decode(mat)
 elif fmt=='base64_chunks':
  w=(len(mat)+3)//4
  packed=''.join(mat[i*w:min((i+1)*w,len(mat))] for i in range(4))
  b=base64.b64decode(packed)
 else: raise ValueError(codec)
 if fmt=='reversed_decimal': b=b[::-1]
 if op=='identity': pass
 elif op=='reverse_bytes': b=b[::-1]
 elif op=='reverse_then_xor': b=bytes(x^int(parts[2],16) for x in b[::-1])
 elif op=='single_byte_xor': b=bytes(x^int(parts[2],16) for x in b)
 elif op=='subtract_modulo_256': b=bytes((x+int(parts[2],16))%256 for x in b)
 elif op=='add_modulo_256': b=bytes((x-int(parts[2],16))%256 for x in b)
 elif op=='repeating_key_xor':
  key=bytes(int(x,16) for x in parts[2].split(',')); b=bytes(x^key[i%len(key)] for i,x in enumerate(b))
 elif op=='rolling_xor':
  prev=int(parts[2],16); out=[]
  for x in b: out.append(x^prev); prev=x
  b=bytes(out)
 elif op=='repeating_key_xor':
  key=bytes(int(x,16) for x in parts[2].split(',')); b=bytes(x^key[i%len(key)] for i,x in enumerate(b))
 else: raise ValueError(codec)
 return b.decode(errors='strict')

def decode_js(p,s):
 # encoded text or array
 m=re.search(r'var packedText = (.*?);',s,re.S)
 if m:
  text=''.join(re.findall(r'"([^"]*)"',m.group(1)))
  if re.search(r'%[0-9a-fA-F]{2}',text): b=bytes(int(x,16) for x in re.findall(r'%([0-9a-fA-F]{2})',text))
  elif re.fullmatch(r'[0-9]+(?:-[0-9]+)+',text): b=bytes(map(int,text.split('-')))
  elif ':' in text: b=bytes.fromhex(text.replace(':',''))
  else: b=base64.b64decode(text + '='*((-len(text))%4))
 else:
  arrs=re.findall(r'\b(?:var|let|const)\s+\w+\s*=\s*\[([0-9a-fA-FxX,\s]+)\]',s)
  arrays=[]
  for a in arrs:
   if re.fullmatch(r'[\s0-9a-fA-FxX,]+',a):
    try: arrays.append([int(x.strip(),0) if x.strip().lower().startswith('0x') else int(x.strip()) for x in a.split(',') if x.strip()])
    except: pass
  arrays=[arr for arr in arrays if len(arr)>10]
  if not arrays: raise ValueError('no byte array')
  b=bytes(x for arr in arrays for x in arr)
 # decoder body
 m=re.search(r'(?:function\s+decode_[\w]+\s*\([^)]*\)\s*\{|var\s+decode_[\w]+\s*=\s*function[^\{]*\{)(.*?)(?:\n\};|\n\})',s,re.S)
 body=m.group(1) if m else ''
 # transform encoded bytes, including explicit array reverse before decoder
 if len(re.findall(r'\.reverse\(\)',s)) % 2: b=b[::-1]
 km=re.search(r'keyBytes\s*=\s*\[([^]]+)\]',body)
 if km:
  key=[int(x.strip()) for x in km.group(1).split(',') if x.strip()]
  b=bytes(x^key[i%len(key)] for i,x in enumerate(b))
 elif re.search(r'previous\s*=\s*(\d+)',body) and re.search(r'\^\s*previous',body):
  pm=re.search(r'previous\s*=\s*(\d+)',body); prev=int(pm.group(1)); out=[]
  for i,x in enumerate(b):
   out.append(x^prev); prev=x
  b=bytes(out)
 else:
  xm=re.search(r'\^\s*(\d+)',body)
  if xm: b=bytes(x^int(xm.group(1)) for x in b)
  else:
   sm=re.search(r'\-\s*(\d+)\s*\+\s*256',body)
   if sm: b=bytes((x-int(sm.group(1)))%256 for x in b)
   else:
    am=re.search(r'\+\s*(\d+)\s*\)\s*%\s*256',body)
    if am: b=bytes((x+int(am.group(1)))%256 for x in b)
 return b.decode()

for p in sorted(root.iterdir()):
 if p.suffix not in ('.cmd','.bat','.js','.vbs'): continue
 s=p.read_text(errors='replace')
 try:
  out=decode_cmd(p,s) if p.suffix in ('.cmd','.bat') else decode_vbs(p,s) if p.suffix=='.vbs' else decode_js(p,s)
  if out.startswith('{'): out=json.dumps(json.loads(out),ensure_ascii=False)
  print(p.name,'=>',out)
 except Exception as e: print(p.name,'ERROR',e)
