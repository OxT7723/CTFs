import pefile
from capstone import *
from capstone.x86 import X86_OP_MEM, X86_REG_RIP, X86_OP_IMM, X86_OP_REG
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
        kb=((z>>55) ^ ((z & 0xffffffff)>>24))&0xff
        out.append(kb)
        r9=(r9+STRIDE)&M
    return bytes(out)
def rddata(va,n):
    return pe.get_data(va-base,n)
def dec(ptr,n,seed):
    ct=rddata(ptr,n)
    k=ks(seed,n)
    return bytes(a^b for a,b in zip(ct,k))

# Parse: for each lea reg,[xsobf], decode forward ~10 insns to grab len (mov qword[mem],imm or push imm/pop) & seed (mov r32,imm32)
results=[]
seen=set()
for off in range(len(code)-4):
    insn=next(md.disasm(code[off:off+15], text_va+off, count=1), None)
    if insn is None or insn.mnemonic!='lea': continue
    tgt=None
    for op in insn.operands:
        if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP:
            t=insn.address+insn.size+op.mem.disp
            if xlo<=t<xhi: tgt=t
    if tgt is None: continue
    # decode forward
    ln=None; seed=None
    a=insn.address+insn.size
    foff=a-text_va
    cnt=0
    for ins2 in md.disasm(code[foff:foff+120], a):
        cnt+=1
        if cnt>12: break
        # length: mov qword ptr [..], imm   OR  push imm ; pop r  pattern -> capture small imm store after
        if ins2.mnemonic=='mov' and len(ins2.operands)==2:
            d,sop=ins2.operands
            if d.type==X86_OP_MEM and sop.type==X86_OP_IMM:
                v=sop.imm & M
                if ln is None and 0<v<0x100:
                    ln=v
                elif v>0x1000 and seed is None:
                    seed=v & 0xffffffff
            if d.type==X86_OP_REG and sop.type==X86_OP_IMM:
                v=sop.imm & 0xffffffff
                if v>0x10000000 and seed is None:
                    seed=v
        if ins2.mnemonic=='pop' and ln is None:
            pass
    key=(tgt,)
    if ln and seed and tgt not in seen:
        seen.add(tgt)
        results.append((tgt,ln,seed))
# Also handle push imm/pop for length (len=8 case used push 8;pop r15)
results.sort()
for tgt,ln,seed in results:
    pt=dec(tgt,ln,seed)
    printable=all(9<=c<127 or c in (10,13) for c in pt)
    print('ptr=%#x len=%-3d seed=%#010x  %s  %r'%(tgt,ln,seed,'OK ' if printable else 'BAD', pt))
print('\ntotal parsed:',len(results))
