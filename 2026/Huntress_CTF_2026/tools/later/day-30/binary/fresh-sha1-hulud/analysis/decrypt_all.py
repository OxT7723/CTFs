import pefile
from capstone import *
from capstone.x86 import *
pe=pefile.PE('../extracted/sha1-hulud.exe')
base=pe.OPTIONAL_HEADER.ImageBase
for s in pe.sections:
    if s.Name.rstrip(b'\x00')==b'.text': text=s
text_va=base+text.VirtualAddress; code=text.get_data()
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
xlo,xhi=base+0x9e000, base+0x9e000+0x1ad
M=(1<<64)-1
C0=0x5d2e9c47a1b386f0; MA=0x41169ddc6c156db1; MB=0xa3d1f5bb9847a411; STRIDE=0x065767ac2ba816c3
def ks(seed,n):
    r8=((((seed<<17)|(seed>>47))&M) ^ C0)&M
    out=bytearray(); r9=0
    for i in range(n):
        x=(r9 ^ r8)&M
        z=((x ^ (x>>29))*MA)&M
        z=((z ^ (z>>27))*MB)&M
        out.append(((z>>55) ^ ((z & 0xffffffff)>>24))&0xff)
        r9=(r9+STRIDE)&M
    return bytes(out)
def dec(ptr,n,seed):
    ct=pe.get_data(ptr-base,n); k=ks(seed,n)
    return bytes(a^b for a,b in zip(ct,k))
# build 32->64 parent map by name
P={}
pairs=[('rax','eax'),('rbx','ebx'),('rcx','ecx'),('rdx','edx'),('rsi','esi'),('rdi','edi'),
       ('rbp','ebp'),('rsp','esp'),('r8','r8d'),('r9','r9d'),('r10','r10d'),('r11','r11d'),
       ('r12','r12d'),('r13','r13d'),('r14','r14d'),('r15','r15d')]
name2id={}
# capstone reg ids via md
import capstone
for rid in range(1,250):
    n=md.reg_name(rid)
    if n: name2id[n]=rid
def parent(rid):
    n=md.reg_name(rid)
    for p64,p32 in pairs:
        if n in (p64,p32): return name2id[p64]
    return rid
regimm={}; structs={}; results=[]; last_push=None
RS=0x14003e400; RE=0x14003fe00
for insn in md.disasm(code[RS-text_va:RE-text_va], RS):
    m=insn.mnemonic; ops=insn.operands
    if m=='lea' and len(ops)==2 and ops[0].type==X86_OP_REG and ops[1].type==X86_OP_MEM and ops[1].mem.base==X86_REG_RIP:
        t=insn.address+insn.size+ops[1].mem.disp
        regimm[parent(ops[0].reg)]=('xs',t) if xlo<=t<xhi else ('imm',t); continue
    if m=='mov' and len(ops)==2 and ops[0].type==X86_OP_REG and ops[1].type==X86_OP_IMM:
        regimm[parent(ops[0].reg)]=('imm',ops[1].imm & M); continue
    if m=='pop' and len(ops)==1 and ops[0].type==X86_OP_REG and last_push is not None:
        regimm[parent(ops[0].reg)]=('imm',last_push & M); last_push=None; continue
    if m=='push' and len(ops)==1 and ops[0].type==X86_OP_IMM:
        last_push=ops[0].imm & M; continue
    last_push=None
    if m=='mov' and len(ops)==2 and ops[0].type==X86_OP_MEM and ops[0].mem.base==X86_REG_RBP:
        disp=ops[0].mem.disp; src=ops[1]; val=None
        if src.type==X86_OP_IMM: val=('imm',src.imm & M)
        elif src.type==X86_OP_REG and parent(src.reg) in regimm: val=regimm[parent(src.reg)]
        if val is None: continue
        if val[0]=='xs': structs[disp]={'ptr':val[1]}
        else:
            for b,d in structs.items():
                if disp==b+8: d['len']=val[1]
                elif disp==b+0x10: d['seed']=val[1]
        continue
    if m=='call':
        for b,d in list(structs.items()):
            if {'ptr','len','seed'}<=set(d): results.append((d['ptr'],d['len'],d['seed']&0xffffffff))
        structs={}; regimm={}
seen=set(); uniq=[]
for t in results:
    if t in seen: continue
    seen.add(t); uniq.append(t)
uniq.sort()
for p,l,s in uniq:
    pt=dec(p,l,s); ok=all(9<=c<127 or c in(10,13) for c in pt)
    print('off=%#06x len=%-3d seed=%#010x %s %r'%(p-base,l,s,'ok ' if ok else 'BAD',pt))
print('total',len(uniq))
