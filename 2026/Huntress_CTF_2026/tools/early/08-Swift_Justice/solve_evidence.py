import json,hashlib,zipfile,re,base64,sys,zlib
from pathlib import Path
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_MODE_64
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/home/HuntressCTF/swift-tt-current')
def find(day,suffix):
 return next(root.glob(f'd{day:02}--variant-*.{suffix}'))
def anyfile(day, exclude=()):
 return next(p for p in root.glob(f'd{day:02}--variant-*.*') if p.suffix not in exclude and 'runtimeconfig' not in p.name)
def hashf(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def decode_record(c):
 key=c[5];d=bytes(x^key for x in c[12:]);s=d.find(b'{');e=d.find(b'}',s)+1
 if s<0 or e<=s:raise ValueError('HCFG JSON missing')
 crc=int.from_bytes(c[8:12],'little')
 if zlib.crc32(d[s:e])&0xffffffff !=crc:raise ValueError('HCFG CRC mismatch')
 return json.loads(d[s:e]),key,c[4],crc
def hcfg(p,last=False):
 b=p.read_bytes(); pos=b.rfind(b'HCFG') if last else b.find(b'HCFG')
 if pos<0:raise ValueError('HCFG record missing')
 return decode_record(b[pos:])
a={}
for day,suf in [(1,'elf'),(2,None),(3,'dll'),(4,None),(5,'elf'),(6,'jar'),(7,'jar'),(8,'elf')]:a[f'd{day:02}_artifact_sha256_1']=hashf(find(day,suf) if suf else anyfile(day))
a['d03_artifact_sha256_2']=hashf(find(3,'runtimeconfig.json'))
with open(find(1,'elf'),'rb') as f:
 e=ELFFile(f); symtab=e.get_section_by_name('.symtab')
 a['d01_analysis_elf_class']=f'ELF{e.elfclass}'
 a['d01_analysis_machine']={'EM_X86_64':'x86-64','EM_386':'i386','EM_AARCH64':'aarch64'}.get(e['e_machine'],e['e_machine'])
 a['d01_analysis_section_names']=json.dumps([s.name for s in e.iter_sections()],separators=(',',':'))
 a['d01_analysis_symbols']=json.dumps([s.name for s in symtab.iter_symbols() if s.name] if symtab else [],separators=(',',':'))
 recover=next((s for s in symtab.iter_symbols() if s.name=='recover_code' and s['st_info']['type']=='STT_FUNC'),None) if symtab else None
 if recover:
  section=e.get_section(recover['st_shndx']); offset=recover['st_value']-section['sh_addr']; code=section.data()[offset:offset+recover['st_size']]
  decoder=Cs(CS_ARCH_X86,CS_MODE_64 if e.elfclass==64 else CS_MODE_32)
  ins=[]
  for op in decoder.disasm(code,recover['st_value']):
   operand=op.op_str
   if op.mnemonic=='mov' and re.fullmatch(r'eax, 0x[0-9a-f]+',operand): operand='eax, '+str(int(operand.split(', ')[1],16))
   ins.append((op.mnemonic+' '+operand).strip())
  a['d01_analysis_disassembly']=json.dumps(ins,separators=(',',':'))
 else:a['d01_analysis_disassembly']='[]'
 a.update(d01_analysis_elf_type=e['e_type'],d01_analysis_endianness='little' if e.little_endian else 'big',d01_analysis_entry_point=hex(e['e_entry']),d01_analysis_has_symtab=str(symtab is not None).lower())
for day in [2,3,4,5]:
 p=find(day,'dll') if day==3 else (find(day,'elf') if day==5 else anyfile(day)); cfg,key,ver,crc=hcfg(p,last=day==5)
 for k in ['campaign','domain','mutex','url']:a[f'd{day:02}_analysis_config_{k}']=cfg[k]
 a[f'd{day:02}_analysis_config_crc32_hex']=f'0x{crc:08x}'
 if day==2:a.update(d02_analysis_format='pe' if p.suffix=='.exe' else 'elf',d02_analysis_xor_key_hex=f'0x{key:02x}',d02_analysis_has_cpp_typeinfo='true',d02_analysis_has_cpp_vtable='true')
 if day==3:a.update(d03_analysis_format='PE_CLR',d03_analysis_machine='i386',d03_analysis_metadata_version='v4.0.30319')
 if day==4:a.update(d04_analysis_architecture='x86-64',d04_analysis_format='pe' if p.suffix=='.exe' else 'elf',d04_analysis_hcfg_version=str(ver),d04_analysis_xor_key_hex=f'0x{key:02x}')
 if day==5:a.update(d05_analysis_architecture='x86-64',d05_analysis_format='elf',d05_analysis_hcfg_version=str(ver),d05_analysis_xor_key_hex=f'0x{key:02x}')
for day in [6,7]:
 p=find(day,'jar'); found=None
 with zipfile.ZipFile(p) as z:
  for n in z.namelist():
   if n.endswith('.class') and not n.startswith('kotlin/'):
    b=z.read(n)
    for m in re.finditer(rb'SENGRw[A-Za-z0-9+/=]{100,}',b):
     r=base64.b64decode(m.group(0))
     if r.startswith(b'HCFG'):found=r;break
    if found:break
 cfg,key,ver,crc=decode_record(found)
 a.update({f'd{day:02}_analysis_format':'jar',f'd{day:02}_analysis_config_campaign':cfg['campaign'],f'd{day:02}_analysis_config_domain':cfg['domain'],f'd{day:02}_analysis_config_mutex':cfg['mutex'],f'd{day:02}_analysis_config_url':cfg['url'],f'd{day:02}_analysis_config_crc32_hex':f'0x{crc:08x}',f'd{day:02}_analysis_hcfg_version':str(ver),f'd{day:02}_analysis_xor_key_hex':f'0x{key:02x}'})
 with zipfile.ZipFile(p) as z:
  a[f'd{day:02}_analysis_compression_methods']=json.dumps(sorted({i.compress_type for i in z.infolist()}),separators=(',',':'))
# Swift base64-encoded HCFG
p=find(8,'elf');raw=p.read_bytes();record=None
for m in re.finditer(rb'SENGRw[A-Za-z0-9+/=]{100,}',raw):
 try:r=base64.b64decode(m.group(0))
 except Exception:continue
 if r.startswith(b'HCFG'):record=r;break
if record is None: raise RuntimeError('Swift HCFG not found')
cfg,key,ver,crc=decode_record(record)
with open(p,'rb') as f:
 swift=ELFFile(f)
 a.update(d08_analysis_architecture={'EM_X86_64':'x86-64','EM_386':'i386','EM_AARCH64':'aarch64'}.get(swift['e_machine'],swift['e_machine']),d08_analysis_elf_class=str(swift.elfclass),d08_analysis_format='elf',d08_analysis_machine=str({'EM_X86_64':62,'EM_386':3,'EM_AARCH64':183}.get(swift['e_machine'],swift['e_machine'])),d08_analysis_config_campaign=cfg['campaign'],d08_analysis_config_domain=cfg['domain'],d08_analysis_config_mutex=cfg['mutex'],d08_analysis_config_url=cfg['url'],d08_analysis_config_crc32_hex=f'0x{crc:08x}')
print(json.dumps(a,separators=(',',':')))
