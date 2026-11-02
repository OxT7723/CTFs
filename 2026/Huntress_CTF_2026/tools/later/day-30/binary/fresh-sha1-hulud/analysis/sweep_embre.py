import pefile
from capstone import *
from capstone.x86 import *
pe=pefile.PE('../extracted/sha1-hulud.exe')
base=pe.OPTIONAL_HEADER.ImageBase
secs=[(s.Name.rstrip(b'\x00').decode(errors='replace'),base+s.VirtualAddress,base+s.VirtualAddress+s.Misc_VirtualSize) for s in pe.sections]
def sec_of(va):
    for n,lo,hi in secs:
        if lo<=va<hi: return n
    return None
for s in pe.sections:
    if s.Name.rstrip(b'\x00')==b'.text': text=s
tva=base+text.VirtualAddress; code=text.get_data()
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
M=(1<<64)-1
C0=0x5d2e9c47a1b386f0; MA=0x41169ddc6c156db1; MB=0xa3d1f5bb9847a411; STRIDE=0x065767ac2ba816c3
def ks(seed,n):
    r8=((((seed<<17)|(seed>>47))&M)^C0)&M; out=bytearray(); r9=0
    for i in range(n):
        x=(r9^r8)&M; z=((x^(x>>29))*MA)&M; z=((z^(z>>27))*MB)&M
        out.append(((z>>55)^((z&0xffffffff)>>24))&0xff); r9=(r9+STRIDE)&M
    return bytes(out)
def rd(va,n):
    try:return pe.get_data(va-base,n)
    except:return b''
pairs=[('rax','eax'),('rbx','ebx'),('rcx','ecx'),('rdx','edx'),('rsi','esi'),('rdi','edi'),
       ('rbp','ebp'),('rsp','esp'),('r8','r8d'),('r9','r9d'),('r10','r10d'),('r11','r11d'),
       ('r12','r12d'),('r13','r13d'),('r14','r14d'),('r15','r15d')]
name2id={}
for rid in range(1,260):
    n=md.reg_name(rid)
    if n:name2id[n]=rid
def parent(rid):
    n=md.reg_name(rid)
    for p64,p32 in pairs:
        if n in(p64,p32):return name2id[p64]
    return rid

seed_secrets=[]; adj_secrets=[]
regimm={}; structs={}; last_push=None
def finalize():
    global structs
    for b,d in list(structs.items()):
        if {'ptr','len','seed'}<=set(d):
            seed_secrets.append((d['ptr'],d['len'],d['seed']&0xffffffff))
        if {'ptr','len','kptr','klen'}<=set(d):
            adj_secrets.append((d['ptr'],d['len'],d['kptr'],d['klen']))
    structs={}
pos=0; N=len(code)
while pos<N:
    progressed=False
    for insn in md.disasm(code[pos:], tva+pos):
        progressed=True
        m=insn.mnemonic; ops=insn.operands
        if m=='lea' and len(ops)==2 and ops[0].type==X86_OP_REG and ops[1].type==X86_OP_MEM and ops[1].mem.base==X86_REG_RIP:
            t=insn.address+insn.size+ops[1].mem.disp
            regimm[parent(ops[0].reg)]=('ptr',t)
        elif m=='mov' and len(ops)==2 and ops[0].type==X86_OP_REG and ops[1].type==X86_OP_IMM:
            regimm[parent(ops[0].reg)]=('imm',ops[1].imm&M)
        elif m=='pop' and len(ops)==1 and ops[0].type==X86_OP_REG and last_push is not None:
            regimm[parent(ops[0].reg)]=('imm',last_push&M); last_push=None
        elif m=='push' and len(ops)==1 and ops[0].type==X86_OP_IMM:
            last_push=ops[0].imm&M
        elif m=='mov' and len(ops)==2 and ops[0].type==X86_OP_MEM and ops[0].mem.base==X86_REG_RBP:
            last_push=None
            disp=ops[0].mem.disp; src=ops[1]; val=None
            if src.type==X86_OP_IMM: val=('imm',src.imm&M)
            elif src.type==X86_OP_REG and parent(src.reg) in regimm: val=regimm[parent(src.reg)]
            if val is not None:
                if val[0]=='ptr' and sec_of(val[1]):
                    # start/continue struct: ptr at some base
                    structs.setdefault(disp,{})['ptr']=val[1]
                    structs[disp]['_ptrsec']=sec_of(val[1])
                else:
                    v=val[1]
                    for b,d in structs.items():
                        if disp==b+8: d['len']=v
                        elif disp==b+0x10:
                            if val[0]=='ptr' and sec_of(v): d['kptr']=v
                            else: d['seed']=v
                        elif disp==b+0x18: d['klen']=v
        else:
            last_push=None
            if m=='call':
                finalize(); regimm={}
        pos=insn.address-tva+insn.size
    if not progressed:
        pos+=1
finalize()
def uniq(lst):
    seen=set(); out=[]
    for x in lst:
        if x in seen:continue
        seen.add(x); out.append(x)
    return out
print('=== SEED-based secrets ===')
for p,l,s in sorted(uniq(seed_secrets)):
    if not sec_of(p): continue
    pt=bytes(a^b for a,b in zip(rd(p,l),ks(s,l)))
    ok=all(9<=c<127 or c in(10,13) for c in pt)
    print('%-8s off=%#06x len=%-3d seed=%#010x %s %r'%(sec_of(p),p-base,l,s,'ok' if ok else 'BAD',pt))
print('=== ADJACENT-KEY secrets ===')
for p,l,kp,kl in sorted(uniq(adj_secrets)):
    if not sec_of(p) or not sec_of(kp): continue
    d=rd(p,l); k=rd(kp,kl); n=min(l,kl)
    pt=bytes(a^b for a,b in zip(d[:n],k[:n]))
    ok=all(9<=c<127 or c in(10,13) for c in pt)
    print('data=%#x len=%d key=%#x klen=%d %s %r'%(p,l,kp,kl,'ok' if ok else 'BAD',pt))
