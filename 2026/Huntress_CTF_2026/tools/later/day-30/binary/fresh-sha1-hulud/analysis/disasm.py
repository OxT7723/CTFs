import pefile,sys
from capstone import *
from capstone.x86 import X86_OP_MEM, X86_REG_RIP, X86_OP_IMM
pe=pefile.PE('../extracted/sha1-hulud.exe')
base=pe.OPTIONAL_HEADER.ImageBase
secs=[(s.Name.rstrip(b'\x00').decode(errors='replace'),base+s.VirtualAddress,base+s.VirtualAddress+s.Misc_VirtualSize) for s in pe.sections]
def sec_of(va):
    for n,lo,hi in secs:
        if lo<=va<hi: return n
    return '?'
def rd(va,n):
    try: return pe.get_data(va-base,n)
    except: return b''
for s in pe.sections:
    if s.Name.rstrip(b'\x00')==b'.text': text=s
text_va=base+text.VirtualAddress; code=text.get_data()
md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=True
start=int(sys.argv[1],16); end=int(sys.argv[2],16)
off=start-text_va
for insn in md.disasm(code[off:end-text_va],start):
    extra=''
    for op in insn.operands:
        if op.type==X86_OP_MEM and op.mem.base==X86_REG_RIP:
            tgt=insn.address+insn.size+op.mem.disp
            sx=''
            if sec_of(tgt) in ('.rdata','.data'):
                raw=rd(tgt,24)
                printable=''.join(chr(c) if 32<=c<127 else '.' for c in raw)
                sx=' "%s"'%printable
            extra=' ; -> %#x [%s]%s'%(tgt,sec_of(tgt),sx)
        if op.type==X86_OP_IMM and insn.mnemonic in ('call','jmp') and (0x140000000<=op.imm<0x140100000):
            extra=' ; [%s]'%sec_of(op.imm)
    print('%#x: %-10s %s%s'%(insn.address,insn.mnemonic,insn.op_str,extra))
