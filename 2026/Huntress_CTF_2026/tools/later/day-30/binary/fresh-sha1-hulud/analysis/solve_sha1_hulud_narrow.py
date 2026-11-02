import ctypes, hashlib, json, os, subprocess, sys, collections
from pathlib import Path
import speakeasy as speakeasy_pkg
from speakeasy import Speakeasy
from speakeasy.winenv.api.usermode.kernel32 import Kernel32
from speakeasy.winenv.api.usermode.ntdll import Ntdll

ROOT=Path(__file__).resolve().parents[4]
path=str(ROOT/'day-30/binary/fresh-sha1-hulud/extracted/sha1-hulud.exe')
INPUT=(sys.argv[1] if len(sys.argv)>1 else 'Wonder Wall')+'\r\n'
outputs=[]; rounds=0; post=[]; snapshots=[]; returns=collections.Counter(); after=False; post_unique=[]; post_seen=set(); post_counts=collections.Counter(); post_snap=[]; read_done=False; input_reads=[]; input_read_keys=set(); sha1_activity={}
comparison_pairs=[]; comparison_triples=[]; comparison_results=[]; success_gate=[]

def rol(x,n): return ((x<<n)|(x>>(32-n)))&0xffffffff

def decompress_lznt1(data):
    pos=0
    output=bytearray()
    while pos<len(data):
        if len(data)-pos<2:
            if not any(data[pos:]): break
            raise ValueError('truncated LZNT1 chunk header')
        header=int.from_bytes(data[pos:pos+2],'little')
        pos+=2
        if header==0 and not any(data[pos:]):
            break
        if header&0x7000!=0x3000:
            raise ValueError(f'invalid LZNT1 chunk signature {header:#x}')
        payload_size=(header&0x0fff)+1
        end=pos+payload_size
        if end>len(data):
            raise ValueError('truncated LZNT1 chunk payload')
        chunk=bytearray()
        if not header&0x8000:
            chunk.extend(data[pos:end])
        else:
            while pos<end:
                flags=data[pos]
                pos+=1
                for bit in range(8):
                    if pos>=end: break
                    if flags&(1<<bit):
                        if pos+2>end:
                            raise ValueError('truncated LZNT1 phrase token')
                        token=int.from_bytes(data[pos:pos+2],'little')
                        pos+=2
                        length_mask=0x0fff
                        displacement_shift=12
                        window=len(chunk)
                        while window>=0x10:
                            length_mask>>=1
                            displacement_shift-=1
                            window>>=1
                        length=(token&length_mask)+3
                        displacement=(token>>displacement_shift)+1
                        if displacement>len(chunk):
                            raise ValueError('invalid LZNT1 back reference')
                        for _ in range(length):
                            chunk.append(chunk[-displacement])
                    else:
                        chunk.append(data[pos])
                        pos+=1
                if len(chunk)>0x1000:
                    raise ValueError('LZNT1 chunk exceeds 4096 bytes')
        output.extend(chunk)
        pos=end
    return bytes(output)

def sha1_round_only(state):
    # sha1-hulud passes {A..E, padding, W0..W15}; the caller applies feed-forward.
    words=[int.from_bytes(state[0x18+i*4:0x1c+i*4],'little') for i in range(16)]
    w=words[:]
    for i in range(16,80): w.append(rol(w[i-3]^w[i-8]^w[i-14]^w[i-16],1))
    a,b,c,d,e=[int.from_bytes(state[i*4:i*4+4],'little') for i in range(5)]
    for i in range(80):
        if i<20: f=(b&c)|((~b)&d); k=0x5a827999
        elif i<40: f=b^c^d; k=0x6ed9eba1
        elif i<60: f=(b&c)|(b&d)|(c&d); k=0x8f1bbcdc
        else: f=b^c^d; k=0xca62c1d6
        t=(rol(a,5)+f+e+k+w[i])&0xffffffff
        e,d,c,b,a=d,c,rol(b,30),a,t
    out=bytearray(state)
    for i,v in enumerate((a,b,c,d,e)): out[i*4:i*4+4]=v.to_bytes(4,'little')
    return bytes(out)

NATIVE_SOURCE = r"""
#include <stdint.h>
#include <string.h>

uint64_t hulud_fast_mix(uint64_t x, uint64_t scale, uint64_t length,
                        const uint8_t *data) {
    const uint64_t rounds = 0x2aea540;
    const uint64_t multiplier = 0xf8714df9dba9a23dULL;
    for (uint64_t i = 0; i < rounds; ++i) {
        uint64_t offset = (((uint64_t)(uint32_t)(x >> 32)) * scale) >> 32;
        uint64_t word = 0;
        if (offset + 8 <= length) {
            memcpy(&word, data + offset, 8);
        } else {
            for (unsigned j = 0; j < 8; ++j)
                word |= (uint64_t)data[(offset + j) % length] << (j * 8);
        }
        x ^= word;
        x *= multiplier;
        x ^= x >> 29;
    }
    return x;
}

static uint32_t rol32(uint32_t x, unsigned n) {
    return (x << n) | (x >> (32 - n));
}

void hulud_sha1_round(uint8_t *state) {
    uint32_t w[80], a, b, c, d, e;
    for (unsigned i = 0; i < 16; ++i)
        memcpy(&w[i], state + 0x18 + i * 4, 4);
    for (unsigned i = 16; i < 80; ++i)
        w[i] = rol32(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1);
    memcpy(&a, state + 0, 4); memcpy(&b, state + 4, 4);
    memcpy(&c, state + 8, 4); memcpy(&d, state + 12, 4);
    memcpy(&e, state + 16, 4);
    for (unsigned i = 0; i < 80; ++i) {
        uint32_t f, k;
        if (i < 20) { f = (b & c) | (~b & d); k = 0x5a827999; }
        else if (i < 40) { f = b ^ c ^ d; k = 0x6ed9eba1; }
        else if (i < 60) { f = (b & c) | (b & d) | (c & d); k = 0x8f1bbcdc; }
        else { f = b ^ c ^ d; k = 0xca62c1d6; }
        uint32_t t = rol32(a, 5) + f + e + k + w[i];
        e = d; d = c; c = rol32(b, 30); b = a; a = t;
    }
    memcpy(state + 0, &a, 4); memcpy(state + 4, &b, 4);
    memcpy(state + 8, &c, 4); memcpy(state + 12, &d, 4);
    memcpy(state + 16, &e, 4);
}
"""
NATIVE_PATH = '/tmp/libsha1_hulud_narrow.so'
if not os.path.exists(NATIVE_PATH):
    subprocess.run(
        ['gcc', '-shared', '-fPIC', '-O3', '-x', 'c', '-o', NATIVE_PATH, '-'],
        input=NATIVE_SOURCE.encode(), check=True,
    )
mixer=ctypes.CDLL(NATIVE_PATH)
mixer.hulud_fast_mix.argtypes=[
    ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64,
    ctypes.POINTER(ctypes.c_ubyte),
]
mixer.hulud_fast_mix.restype=ctypes.c_uint64
mixer.hulud_sha1_round.argtypes=[ctypes.POINTER(ctypes.c_ubyte)]
mixer.hulud_sha1_round.restype=None
fast_mix_records=[]
veh_interrupt_records=[]
veh_access_records=[]

def code_hook(emu,addr,size,ctx):
    global rounds, after
    if addr==0x14003cee4: after=True
    if 0x14003cee4 <= addr <= 0x14003d450:
        post.append(addr)
        if addr in (0x14003cee4,0x14003cf93,0x14003d0b8,0x14003d0dd,0x14003d106,0x14003d11b,0x14003d137,0x14003d1b8,0x14003d1d0,0x14003d307,0x14003d310,0x14003d412,0x14003d420,0x14003d408):
            rbp=emu.reg_read('rbp')
            try: raw=emu.mem_read(rbp+0x7b8,0x74)
            except Exception: raw=b''
            snapshots.append({'pc':hex(addr),'rbp':hex(rbp),'rax':hex(emu.reg_read('rax')),'rdi':hex(emu.reg_read('rdi')),'rsi':hex(emu.reg_read('rsi')),'r14':hex(emu.reg_read('r14')),'r15':hex(emu.reg_read('r15')),'globals':emu.mem_read(0x140098a8c,0x2d).hex(),'local':raw.hex()})
    if addr not in (0x140001080,0x140010840,0x14001dfc0): return
    rcx=emu.reg_read('rcx'); rsp=emu.reg_read('rsp')
    returns[int.from_bytes(emu.mem_read(rsp,8),'little')]+=1
    state=emu.mem_read(rcx,0x58)
    native_state=(ctypes.c_ubyte*len(state)).from_buffer_copy(state)
    mixer.hulud_sha1_round(native_state)
    out=bytes(native_state)
    ret=int.from_bytes(emu.mem_read(rsp,8),'little')
    activity=sha1_activity.setdefault(ret,{'count':0})
    if activity['count']==0:
        activity['first_state_in']=state.hex()
        activity['first_state_out']=out.hex()
    activity['count']+=1
    activity['last_state_in']=state.hex()
    activity['last_state_out']=out.hex()
    if ret in (0x14003d168,0x14004184d):
        obj={'state_in':state.hex(),'state_out':out.hex(),'regs':{r:hex(emu.reg_read(r)) for r in ['rax','rbx','rcx','rdx','rsi','rdi','r8','r9','r10','r11','r12','r13','r14','r15','rbp','rsp']}}
        open('/tmp/sha1-obfuscated-block.json' if ret==0x14004184d else '/tmp/sha1-second-block.json','w').write(json.dumps(obj))
    emu.mem_write(rcx,out)
    if rounds==0:
        open('/tmp/sha1-first-block.json','w').write(json.dumps({'state_in':state.hex(),'state_out':out.hex(),'input':INPUT}))
    rounds+=1
    emu.reg_write('rax',0)
    emu.reg_write('rsp',rsp+8)
    emu.reg_write('rip',ret)

def api_hook(emu,imp,orig,argv):
    name=imp.rsplit('.',1)[-1].lower()
    if name=='getfileinformationbyhandle':
        hfile,info=argv
        f=emu.file_get(hfile)
        if not f or not info:
            emu.set_last_error(6)
            return 0
        size=f.get_size()
        record=bytearray(52)
        record[0:4]=(0x80).to_bytes(4,'little')  # FILE_ATTRIBUTE_NORMAL
        record[32:36]=(size>>32).to_bytes(4,'little')
        record[36:40]=(size&0xffffffff).to_bytes(4,'little')
        record[40:44]=(1).to_bytes(4,'little')   # one hard link
        emu.mem_write(info,bytes(record))
        emu.set_last_error(0)
        print('FILE_INFORMATION',hex(hfile),f.get_path(),size)
        return 1
    if name=='writeconsolew':
        h,buf,n,written=argv
        txt=emu.mem_read(buf,min(n,0x1000)*2).decode('utf-16le','replace')
        outputs.append(txt); emu.mem_write(written,len(txt).to_bytes(4,'little'))
        print('OUTPUT',repr(txt))
        return 1
    if name=='readconsolew':
        global read_done
        h,buf,n,readp,*rest=argv
        txt=INPUT[:n]
        emu.mem_write(buf,txt.encode('utf-16le'))
        emu.mem_write(readp,len(txt).to_bytes(4,'little'))
        read_done=True
        print('INPUT',repr(txt))
        return 1
    if name=='ntwritefile':
        h,event,apc,apcctx,ios,buf,n,offset,key=argv
        raw=emu.mem_read(buf,min(n,0x10000))
        try: txt=raw.decode('utf-8','replace')
        except Exception: txt=repr(raw)
        outputs.append(txt); print('OUTPUT',repr(txt))
        emu.mem_write(ios,b'\0'*8+min(n,0x10000).to_bytes(8,'little'))
        return 0
    if name=='ntreadfile':
        h,event,apc,apcctx,ios,buf,n,offset,key=argv
        f=emu.file_get(h)
        if not f or not ios or not buf:
            return 0xc0000008  # STATUS_INVALID_HANDLE
        length=n&0xffffffff
        if offset:
            file_offset=int.from_bytes(emu.mem_read(offset,8),'little')
            f.seek(file_offset,0)
        raw=f.get_data(length)
        if raw:
            emu.mem_write(buf,raw)
        emu.mem_write(ios,b'\0'*8+len(raw).to_bytes(8,'little'))
        print('NT_READ_FILE',f.get_path(),'requested',length,'read',len(raw),
              'offset',f.tell())
        return 0 if raw else 0xc0000011  # STATUS_END_OF_FILE
    if name=='rtldecompressbuffer':
        compression_format,outbuf,out_capacity,inbuf,in_size,final_size=argv
        if compression_format&0xf!=2:  # COMPRESSION_FORMAT_LZNT1
            return orig(argv) if orig else 0xc0000002
        try:
            compressed=emu.mem_read(inbuf,in_size&0xffffffff)
            decompressed=decompress_lznt1(compressed)
        except Exception as exc:
            print('RTL_DECOMPRESS_BUFFER_ERROR',hex(inbuf),hex(in_size),repr(exc))
            return 0xc0000242  # STATUS_BAD_COMPRESSION_BUFFER
        if len(decompressed)>out_capacity&0xffffffff:
            return 0xc0000023  # STATUS_BUFFER_TOO_SMALL
        emu.mem_write(outbuf,decompressed)
        if final_size:
            emu.mem_write(final_size,len(decompressed).to_bytes(4,'little'))
        print('RTL_DECOMPRESS_BUFFER',hex(inbuf),len(compressed),
              hex(outbuf),len(decompressed),
              'sha1',hashlib.sha1(decompressed).hexdigest())
        return 0
    if name=='widechartomultibyte':
        cp,flags,wide,n,outbuf,cap,defaultchar,useddefault=argv
        if n==-1:
            raw=bytearray()
            for i in range(0,0x1000,2):
                ch=emu.mem_read(wide+i,2)
                if ch==b'\0\0': break
                raw+=ch
        else: raw=emu.mem_read(wide,max(0,n)*2)
        txt=raw.decode('utf-16le','replace')
        enc=txt.encode('utf-8') if cp==65001 else txt.encode('cp1252','replace')
        if outbuf and cap: emu.mem_write(outbuf,enc[:cap])
        if useddefault: emu.mem_write(useddefault,b'\0')
        return len(enc)
    if name=='getthreadcontext':
        h,context=argv
        raw=bytearray(emu.mem_read(context,0x4d0))
        for off in (0x48,0x50,0x58,0x60,0x68,0x70): raw[off:off+8]=b'\0'*8
        emu.mem_write(context,bytes(raw))
        return 1
    if name=='checkremotedebuggerpresent':
        h,out=argv; emu.mem_write(out,b'\0'*4); return 1
    if name=='isdebuggerpresent': return 0
    if name=='getmodulehandleexw':
        flags,module,out=argv
        if flags & 2: emu.mem_write(out,(0x140000000).to_bytes(8,'little')); return 1
        return 0
    if name=='setthreadstackguarantee': return 1
    if name=='setthreaddescription': return 0
    if name=='getconsoleoutputcp' or name=='getconsolecp': return 65001
    return orig(argv) if orig else 1

cfg_path=Path(speakeasy_pkg.__file__).parent/'configs'/'default.json'
cfg=json.loads(cfg_path.read_text())
cfg['timeout']=int(os.environ.get('SHA1_HULUD_TIMEOUT','600'))
cfg['max_api_count']=1000000
kernel32_placeholder='/tmp/sha1-hulud-kernel32-placeholder.dll'
if not os.path.exists(kernel32_placeholder):
    placeholder=bytearray(open(
        str(Path(speakeasy_pkg.__file__).parent/'winenv/decoys/amd64/default_exe.exe'),
        'rb').read())
    peoff=int.from_bytes(placeholder[0x3c:0x40],'little')
    coff_characteristics=peoff+4+18
    characteristics=int.from_bytes(
        placeholder[coff_characteristics:coff_characteristics+2],'little')
    placeholder[coff_characteristics:coff_characteristics+2]=(
        characteristics|0x2000).to_bytes(2,'little')
    open(kernel32_placeholder,'wb').write(placeholder)
cfg['filesystem']['files'].append({
    'mode':'full_path',
    'emu_path':'C:\\Windows\\system32\\kernel32.dll',
    'path':kernel32_placeholder,
})
cfg['filesystem']['files'].append({
    'mode':'full_path',
    'emu_path':'C:\\Windows\\system32\\ntdll.dll',
    'path':kernel32_placeholder,
})
cfg['filesystem']['files'].append({
    'mode':'by_ext',
    'ext':'dll',
    'path':kernel32_placeholder,
})
se=Speakeasy(config=cfg)
mod=se.load_module(path)
def preserve_import_owner(emu,addr,size,ctx):
    # Speakeasy resolves invalid import stubs through the PE that owns the
    # current instruction. Keep that context anchored to this main image.
    if addr==0x1400653ac:
        owner=emu.get_module_from_addr(addr)
        print('FILEINFO_CALL',type(emu.curr_mod).__name__,
              hex(owner.get_base()) if owner else None)
        if owner:
            emu.curr_mod=owner
        hfile=emu.reg_read('rcx')
        out=emu.reg_read('rdx')
        f=emu.file_get(hfile)
        if f and out:
            file_size=f.get_size()
            record=bytearray(52)
            record[0:4]=(0x80).to_bytes(4,'little')
            record[32:36]=(file_size>>32).to_bytes(4,'little')
            record[36:40]=(file_size&0xffffffff).to_bytes(4,'little')
            record[40:44]=(1).to_bytes(4,'little')
            emu.mem_write(out,bytes(record))
            emu.set_last_error(0)
            emu.reg_write('rax',1)
            emu.reg_write('rip',addr+6)
            print('FILE_INFORMATION',hex(hfile),f.get_path(),file_size)
se.add_code_hook(preserve_import_owner,begin=0x1400653ac,end=0x1400653ac)

def emulate_native_file_read_call(emu,addr,size,ctx):
    if addr not in (0x14006e017,0x140065571):
        return
    hfile=emu.reg_read('rcx')
    rsp=emu.reg_read('rsp')
    ios=int.from_bytes(emu.mem_read(rsp+0x20,8),'little')
    buf=int.from_bytes(emu.mem_read(rsp+0x28,8),'little')
    length=int.from_bytes(emu.mem_read(rsp+0x30,8),'little')&0xffffffff
    offset_ptr=int.from_bytes(emu.mem_read(rsp+0x38,8),'little')
    f=emu.file_get(hfile)
    if not f or not ios or not buf:
        emu.reg_write('rax',0xc0000008)
    else:
        if offset_ptr:
            file_offset=int.from_bytes(emu.mem_read(offset_ptr,8),'little')
            f.seek(file_offset,0)
        raw=f.get_data(length)
        if raw:
            emu.mem_write(buf,raw)
        status=0 if raw else 0xc0000011
        emu.mem_write(ios,status.to_bytes(8,'little')+len(raw).to_bytes(8,'little'))
        emu.reg_write('rax',status)
        print('NT_READ_FILE',hex(addr),f.get_path(),'requested',length,
              'read',len(raw),'offset',f.tell())
    emu.reg_write('rip',addr+6)
se.add_code_hook(emulate_native_file_read_call,
                 begin=0x14006e017,end=0x14006e017)
se.add_code_hook(emulate_native_file_read_call,
                 begin=0x140065571,end=0x140065571)
# The binary reads KUSER_SHARED_DATA.InterruptTime directly. Speakeasy leaves
# the native 0x7ffe0000 user-data page unmapped, so provide a stable KSYSTEM_TIME
# snapshot (High1Time, LowPart, High2Time) for its seqlock reads.
se.emu.mem_map(0x1000,base=0x7ffe0000,tag='emu.KUSER_SHARED_DATA')
se.mem_write(0x7ffe0008,b'\0'*12)
se.add_code_hook(code_hook,begin=0x140001080,end=0x140001080)
se.add_code_hook(code_hook,begin=0x140010840,end=0x140010840)
se.add_code_hook(code_hook,begin=0x14001dfc0,end=0x14001dfc0)
for name,argc in [('WriteConsoleW',4),('ReadConsoleW',5),('SetThreadStackGuarantee',1),('SetThreadDescription',2),('CheckRemoteDebuggerPresent',2),('IsDebuggerPresent',0),('GetThreadContext',2),('GetModuleHandleExW',3),('WideCharToMultiByte',8),('GetConsoleOutputCP',1),('GetConsoleCP',0),('GetFileInformationByHandle',2)]:
    se.add_api_hook(api_hook,'KERNEL32',name,argc)
se.add_code_hook(code_hook,begin=0x14003cee4,end=0x14003d450)
def observe_after(emu,addr,size,ctx):
    global after
    if addr==0x14003cee4: after=True
    if not after: return
    post_counts[addr]+=1
    if addr not in post_seen and len(post_unique)<12000:
        post_seen.add(addr); post_unique.append(addr)
    if addr in (0x14003d42b,0x14003d5aa,0x14003d5b1,0x14003d5e0,0x14003e1fd,0x14003e002,0x1400416eb,0x1400418cd,0x1400412db,0x140041234,0x1400412cc,0x14003d408,0x14003d412,0x14003d420):
        rbp=emu.reg_read('rbp')
        try: local=emu.mem_read(rbp+0x6a0,0x90).hex()
        except Exception: local='readfail'
        post_snap.append({'pc':hex(addr),'regs':{r:hex(emu.reg_read(r)) for r in ['rax','rbx','rcx','rdx','rsi','rdi','r8','r9','r10','r11','r12','r13','r14','r15','rbp','rsp']},'local':local})
trace_path=[]
trace_snaps=[]
def trace_path_hook(emu,addr,size,ctx):
    if not after: return
    if len(trace_path)<20000: trace_path.append(addr)
    if addr in (0x14003c673,0x14003c679,0x14003c68a,0x14003c6c8,0x14003c6da,0x14003c6ed,0x14003cad1,0x14003d1b8,0x14003d1d0,0x14003d24c,0x14003d307,0x14003d30a,0x14003d310,0x14003d408,0x14003d42b):
        try: glob=emu.mem_read(0x140098070,4).hex()
        except Exception: glob='?'
        trace_snaps.append({'pc':hex(addr),'rax':hex(emu.reg_read('rax')),'rcx':hex(emu.reg_read('rcx')),'rdx':hex(emu.reg_read('rdx')),'rsi':hex(emu.reg_read('rsi')),'rdi':hex(emu.reg_read('rdi')),'rbp':hex(emu.reg_read('rbp')),'rsp':hex(emu.reg_read('rsp')),'panic':glob})
se.add_code_hook(trace_path_hook,begin=0x14003c650,end=0x14003d450)
def emulate_registered_access_veh(emu,addr,size,ctx):
    marker=int.from_bytes(emu.mem_read(0x140098ae0,4),'little')
    if (marker==0x0c883a7e and
            emu.reg_read('rsi')==addr and
            emu.reg_read('rdi')==addr+4):
        # The handler validates a write AV, derives R13 from ExceptionInfo,
        # and resumes at CONTEXT.Rdi, skipping the faulting write.
        target=emu.reg_read('r9')
        info_value=((1<<48)^target)
        emu.reg_write('r13',info_value)
        emu.reg_write('rip',emu.reg_read('rdi'))
        veh_access_records.append({
            'pc':hex(addr),'fault_address':hex(target),
            'marker':hex(marker),'r13':hex(info_value),
            'resume':hex(emu.reg_read('rip')),
        })
se.add_code_hook(emulate_registered_access_veh,
                 begin=0x14003fad1,end=0x14003fad1)
se.add_code_hook(emulate_registered_access_veh,
                 begin=0x1400462e4,end=0x1400462e4)
def sync_thread_id(emu,addr,size,ctx):
    emu.mem_write(emu.gs_addr+0x48,(0x434).to_bytes(4,'little'))
se.add_code_hook(sync_thread_id,begin=0x14002b872,end=0x14002b872)
def capture_comparison(emu,addr,size,ctx):
    rbp=emu.reg_read('rbp')
    bl=emu.reg_read('rbx')&0xff
    sil=emu.reg_read('rsi')&0xff
    dl=emu.reg_read('rdx')&0xff
    comparison_pairs.append((sil,dl))
    comparison_triples.append({
        'bl':bl,
        'sil':sil,
        'dl':dl,
        'rbx':hex(emu.reg_read('rbx')),
        'rsi':hex(emu.reg_read('rsi')),
        'rdx':hex(emu.reg_read('rdx')),
        'rbp':hex(rbp),
        'iterator':int.from_bytes(emu.mem_read(rbp+0x1118,8),'little'),
    })
se.add_code_hook(capture_comparison,begin=0x140059cd9,end=0x140059cd9)
def capture_comparison_result(emu,addr,size,ctx):
    rbp=emu.reg_read('rbp')
    frame={}
    for disp in (0x1100,0x1108,0x1110,0x1118,0x1120,0x1128,
                 0x1130,0x1138,0x1140,0x1148,0x1150,0x1168,
                 0x1170,0x1178,0x1180,0x1188):
        frame[hex(disp)]=hex(int.from_bytes(emu.mem_read(rbp+disp,8),'little'))
    comparison_results.append({
        'pair_end':len(comparison_pairs),
        'mismatch':int.from_bytes(emu.mem_read(rbp+0xca8,1),'little'),
        'iterator':int.from_bytes(emu.mem_read(rbp+0x1118,8),'little'),
        'gate_before':int.from_bytes(emu.mem_read(rbp+0x5f8,8),'little'),
        'rbp':hex(rbp),
        'frame':frame,
    })
    print('COMPARE_RESULT',comparison_results[-1])
se.add_code_hook(capture_comparison_result,begin=0x140059ce9,end=0x140059ce9)
def capture_equal_bit(emu,addr,size,ctx):
    if comparison_results:
        comparison_results[-1]['equal_bit']=emu.reg_read('rax')&0xff
se.add_code_hook(capture_equal_bit,begin=0x140059cf3,end=0x140059cf3)
def capture_success_gate(emu,addr,size,ctx):
    rbp=emu.reg_read('rbp')
    item={
        'pc':hex(addr),
        'gate':int.from_bytes(emu.mem_read(rbp+0x5f8,8),'little'),
    }
    success_gate.append(item)
    print('SUCCESS_GATE',item)
se.add_code_hook(capture_success_gate,begin=0x14005a019,end=0x14005a019)
watch_writes=[]
def watch_global_write(emu,access,address,size,value,ctx):
    if address in (0x140098070,0x140098a8c,0x140098a8d,0x140098bb8,0x140098ae0):
        watch_writes.append((emu.reg_read('rip'),address,size,value))
se.add_mem_write_hook(watch_global_write,begin=0x140098070,end=0x140098070)
def input_read_hook(emu,access,address,size,value,ctx):
    if not read_done: return
    pc=emu.reg_read('rip')
    key=(pc,address,size)
    if key in input_read_keys or len(input_reads)>=5000: return
    input_read_keys.add(key)
    try: data=emu.mem_read(address,min(size,64)).hex()
    except Exception: data='?'
    input_reads.append((pc,address,size,data))
se.add_mem_read_hook(input_read_hook,begin=0xd000,end=0x10000)
se.add_mem_read_hook(input_read_hook,begin=0x3f2600,end=0x3f3000)
def fast_mix_hook(emu,addr,size,ctx):
    x=emu.reg_read('rcx')
    scale=emu.reg_read('r8')
    length=emu.reg_read('rsi')
    base=emu.reg_read('rdi')
    if not length:
        raise ValueError('slow mixer received a zero-length source')
    data=emu.mem_read(base,length)
    buf=(ctypes.c_ubyte*len(data)).from_buffer_copy(data)
    mixed=mixer.hulud_fast_mix(x,scale,length,buf)
    fast_mix_records.append({
        'pc':hex(addr),'seed':hex(x),'scale':hex(scale),'length':hex(length),
        'data_address':hex(base),'data_sha1':hashlib.sha1(data).hexdigest(),
        'result':hex(mixed),
    })
    print('IMAGE_MIX',fast_mix_records[-1])
    sys.stdout.flush()
    emu.reg_write('rcx',mixed)
    emu.reg_write('rip',0x1400419c5)

def fast_second_image_mix_hook(emu,addr,size,ctx):
    rbp=emu.reg_read('rbp')
    x=emu.reg_read('rcx')
    scale=emu.reg_read('r8')
    length=int.from_bytes(emu.mem_read(rbp+0x798,8),'little')
    base=int.from_bytes(emu.mem_read(rbp+0xd08,8),'little')
    if not length:
        raise ValueError('second image mixer received a zero-length source')
    data=emu.mem_read(base,length)
    buf=(ctypes.c_ubyte*len(data)).from_buffer_copy(data)
    mixed=mixer.hulud_fast_mix(x,scale,length,buf)
    fast_mix_records.append({
        'pc':hex(addr),'seed':hex(x),'scale':hex(scale),'length':hex(length),
        'data_address':hex(base),'data_sha1':hashlib.sha1(data).hexdigest(),
        'result':hex(mixed),
    })
    emu.reg_write('rcx',mixed)
    emu.reg_write('r9',0x2aea540)
    emu.reg_write('rip',0x140048277)

def milestone_hook(emu,addr,size,ctx):
    snapshots.append({
        'pc':hex(addr),
        'regs':{r:hex(emu.reg_read(r)) for r in
                ('rax','rbx','rcx','rdx','rsi','rdi','r8','r9','r13','rbp','rsp')},
    })

for watched in (0x1400418cd,0x14004194d,0x1400419c5,0x1400419df,
                0x140041a48,0x140041aa2,0x140041b4a):
    callback=fast_mix_hook if watched==0x14004194d else milestone_hook
    se.add_code_hook(callback,begin=watched,end=watched)
se.add_code_hook(fast_second_image_mix_hook,
                 begin=0x1400481db,end=0x1400481db)
deep_snapshots=[]
deep_counts=collections.Counter()
def deep_frame_hook(emu,addr,size,ctx):
    key=hex(addr)
    deep_counts[key]+=1
    if deep_counts[key]>4:
        return
    rbp=emu.reg_read('rbp')
    try:
        frame=emu.mem_read(rbp+0x200,0x1200).hex()
    except Exception:
        frame='readfail'
    deep_snapshots.append({
        'pc':key,
        'occurrence':deep_counts[key],
        'regs':{r:hex(emu.reg_read(r)) for r in
                ('rax','rbx','rcx','rdx','rsi','rdi','r8','r9','r10','r11',
                 'r12','r13','r14','r15','rbp','rsp')},
        'frame':frame,
    })
for watched in (0x140041cbb,0x140041e07,0x140042419,0x140042b78,
                0x1400431da):
    se.add_code_hook(deep_frame_hook,begin=watched,end=watched)
# Keep OS information queries deterministic and debugger-free.
def query_process(self,emu,argv,ctx={}):
    h,cls,info,size,returned=argv
    if cls==7:
        if info:self.mem_write(info,b'\0'*min(size,8))
        return 0
    if cls==30:return 0xc0000353
    if cls==31:
        if info:self.mem_write(info,(1).to_bytes(4,'little'))
        return 0
    return 0xc0000003

def query_system(self,emu,argv,ctx={}):
    cls,info,size,returned=argv
    if cls==0x23:
        if info:self.mem_write(info,b'\0\1')
        return 0
    return 0xc0000003
Ntdll.NtQueryInformationProcess=Ntdll.apihook('NtQueryInformationProcess',argc=5)(query_process)
Ntdll.NtQuerySystemInformation=Ntdll.apihook('NtQuerySystemInformation',argc=4)(query_system)
se.add_api_hook(api_hook,'ntdll','NtWriteFile',9)
se.add_api_hook(api_hook,'ntdll','NtReadFile',9)
se.add_api_hook(api_hook,'ntdll','RtlDecompressBuffer',6)
original_interrupt_handler=se.emu._hook_interrupt
def emulate_registered_veh(emu,intnum,ctx):
    pc=emu.reg_read('rip')
    marker=int.from_bytes(emu.mem_read(0x140098ae0,4),'little')
    if intnum==3 and marker==0x80000003:
        emu.mem_write(0x140098ba8,b'\x01')
        veh_interrupt_records.append({
            'interrupt':intnum,'pc':hex(pc),'marker':hex(marker),
            'action':'continue_after_breakpoint',
        })
        return True
    if intnum==1 and marker==0x80000004:
        emu.mem_write(0x140098baa,b'\x01')
        emu.reg_write('eflags',emu.reg_read('eflags') & ~0x100)
        veh_interrupt_records.append({
            'interrupt':intnum,'pc':hex(pc),'marker':hex(marker),
            'action':'mark_single_step_and_clear_tf',
        })
        return True
    if intnum==1 and marker==0x5b3ea749:
        rsi=emu.reg_read('rsi')
        rdi=emu.reg_read('rdi')
        cur=(pc-rsi)&0xffffffffffffffff
        limit=(rdi-rsi)&0xffffffffffffffff
        if cur<=limit:
            emu.reg_write('r13',pc)
        flags=emu.reg_read('eflags') & ~0x100
        if cur<limit:
            flags|=0x100
        emu.reg_write('eflags',flags)
        veh_interrupt_records.append({
            'interrupt':intnum,'pc':hex(pc),'marker':hex(marker),
            'rsi':hex(rsi),'rdi':hex(rdi),'r13':hex(emu.reg_read('r13')),
            'tf_rearmed':cur<limit,
        })
        return True
    if intnum==3 and marker==0xc8c291de:
        # This breakpoint is the payload's context-derived key step:
        # VEH copies the INT3 address into R15, then resumes after INT3.
        exception_address=(pc-1)&0xffffffffffffffff
        emu.reg_write('r15',exception_address)
        emu.reg_write('rip',pc)
        veh_interrupt_records.append({
            'interrupt':intnum,'pc':hex(pc),'marker':hex(marker),
            'exception_address':hex(exception_address),
            'action':'set_r15_to_exception_address_and_continue',
        })
        return True
    return original_interrupt_handler(emu,intnum,ctx)
se.emu._hook_interrupt=emulate_registered_veh
se.run_module(mod,all_entrypoints=True)
pair_record={
    'input':INPUT.rstrip('\r\n'),
    'pair_count':len(comparison_pairs),
    'left':bytes(x for x,_ in comparison_pairs).hex(),
    'right':bytes(y for _,y in comparison_pairs).hex(),
    'pairs':[[x,y] for x,y in comparison_pairs],
    'triples':comparison_triples,
    'results':comparison_results,
    'success_gate':success_gate,
}
(Path(__file__).parent/'local-comparison-capture.json').write_text(
    json.dumps(pair_record,indent=2)+'\n')
print('COMPARISON_CAPTURE',json.dumps(pair_record))
report=se.get_json_report()
if isinstance(report,str): report=json.loads(report)
open('/tmp/sha1-hulud-replacement-report.json','w').write(json.dumps(report))
open('/tmp/sha1-hulud-deep-snapshots.json','w').write(json.dumps(deep_snapshots))
open('/tmp/sha1-hulud-sha1-activity.json','w').write(json.dumps(
    {hex(k):v for k,v in sha1_activity.items()}))
memory_summary=[]
memory_hits=[]
dump_dir='/tmp/sha1-hulud-final-memory'
os.makedirs(dump_dir,exist_ok=True)
for tag,base,size,is_free,proc,data in se.get_memory_dumps():
 memory_summary.append({'tag':tag,'base':hex(base),'size':size,'free':is_free,'process':str(proc)})
 if size<=0x2000000 and any(key in str(tag).lower() for key in ('module.sha1-hulud','stack','heap')):
  safe=''.join(c if c.isalnum() or c in '._-' else '_' for c in str(tag))
  open(os.path.join(dump_dir,f'{safe}-{base:x}.bin'),'wb').write(data)
 for needle in (b'flag{',b'huntress{',b'FLAG{',b'Wonder',b'WONDER',b'SHA1-Hulud'):
  pos=0
  while True:
   pos=data.find(needle,pos)
   if pos<0: break
   memory_hits.append({'tag':tag,'base':hex(base),'offset':hex(pos),'needle':needle.decode('ascii')})
   pos+=1
open('/tmp/sha1-hulud-memory-summary.json','w').write(json.dumps(memory_summary))
open('/tmp/sha1-hulud-memory-hits.json','w').write(json.dumps(memory_hits))
print('MEMORY_MAPS',memory_summary)
print('MEMORY_HITS',memory_hits)
print('DEEP_SNAPSHOT_COUNT',len(deep_snapshots))
print('SHA1_ACTIVITY', {hex(k):v for k,v in sha1_activity.items()})
print('SHA1_BLOCK_CALLS',rounds)
print('INPUT_READS',len(input_reads),[(hex(pc),hex(a),n,d) for pc,a,n,d in input_reads[:400]])
print('CALL_RETURNS',[(hex(k),v) for k,v in returns.most_common()])
print('VEH_EVENTS',veh_interrupt_records)
print('VEH_ACCESS_EVENTS',veh_access_records)
print('SECOND_BLOCK',open('/tmp/sha1-second-block.json').read() if __import__('os').path.exists('/tmp/sha1-second-block.json') else 'missing')
print('POST_UNIQUE_N',len(post_unique),'POST_UNIQUE_TAIL',[hex(x) for x in post_unique[-120:]])
print('POST_COUNTS_TOP',[(hex(k),v) for k,v in post_counts.most_common(40)])
print('FAST_MIX',fast_mix_records)
for x in post_snap[-20:]:print('POST_SNAP',x)
print('POST_TRACE',len(post),[hex(x) for x in post if x in (0x14003d0b8,0x14003d106,0x14003d11b,0x14003d137,0x14003d1b8,0x14003d307,0x14003d310,0x14003d412,0x14003d420,0x14003d408)])
print('TRACE_PATH_N',len(trace_path),'TAIL',[hex(x) for x in trace_path[-200:]])
for x in trace_snaps: print('TRACE_SNAP',x)
print('WATCH_WRITES',[(hex(pc),hex(a),n,hex(v)) for pc,a,n,v in watch_writes])
for x in snapshots:print('SNAP',x)
for ep in report.get('entry_points',[]):
 print('ENTRY',ep.get('ep_type'),'RET',ep.get('ret_val'),'ERR',ep.get('error'),'APIS',len(ep.get('apis',[])))
 for a in ep.get('apis',[]):
  if any(k in a.get('api_name','').lower() for k in ('console','exit','unhandled')):print('API',a)
