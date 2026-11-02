"""Static parser for Pool Party evidence ZIP. Never executes delivered binaries."""
import argparse
import base64
import hashlib
import io
import json
import re
import struct
import subprocess
import tempfile
import zipfile
import zlib
from pathlib import Path

import pefile
import pyzipper
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from elftools.elf.elffile import ELFFile


def config(blob):
    for m in re.finditer(b'HCFG', blob):
        o = m.start()
        if o + 12 > len(blob):
            continue
        ver, key = blob[o + 4], blob[o + 5]
        n = struct.unpack_from('<H', blob, o + 6)[0]
        crc = struct.unpack_from('<I', blob, o + 8)[0]
        raw = bytes(x ^ key for x in blob[o + 12:o + 12 + n])
        if len(raw) != n or zlib.crc32(raw) != crc:
            continue
        try:
            return ver, key, crc, json.loads(raw)
        except (ValueError, UnicodeDecodeError):
            pass
    raise ValueError('no valid HCFG record')


def solve(path):
    out = {}
    blob = path.read_bytes() if isinstance(path, Path) else path
    with pyzipper.AESZipFile(io.BytesIO(blob)) as archive:
        data = {n: archive.read(n, pwd=b'infected') for n in archive.namelist() if not n.endswith('/')}
    byday = {}
    for name, blob in sorted(data.items()):
        day = name[:3]
        byday.setdefault(day, []).append((name, blob))
    for day, entries in byday.items():
        for index, (_, blob) in enumerate(entries, 1):
            out[f'{day}_artifact_sha256_{index}'] = hashlib.sha256(blob).hexdigest()
    with tempfile.TemporaryDirectory() as td:
        name, blob = byday['d01'][0]
        p = Path(td) / name
        p.write_bytes(blob)
        with p.open('rb') as f:
            elf = ELFFile(f)
            out['d01_analysis_elf_class'] = f'ELF{elf.elfclass}'
            out['d01_analysis_machine'] = 'x86-64' if elf.header.e_machine == 'EM_X86_64' else elf.header.e_machine
            out['d01_analysis_elf_type'] = elf.header.e_type
            out['d01_analysis_endianness'] = 'little' if elf.little_endian else 'big'
            out['d01_analysis_section_names'] = json.dumps([s.name for s in elf.iter_sections()], separators=(',', ':'))
            syms = list(elf.get_section_by_name('.symtab').iter_symbols())
            out['d01_analysis_symbols'] = json.dumps([s.name for s in syms if s.name], separators=(',', ':'))
            recover = next((s for s in syms if s.name == 'recover_code' and s.entry.st_info.type == 'STT_FUNC'), None)
            if recover:
                sec = elf.get_section(recover.entry.st_shndx)
                offset = recover.entry.st_value - sec.header.sh_addr
                code = sec.data()[offset:offset + recover.entry.st_size]
                ins = [f'{i.mnemonic} {i.op_str}'.strip() for i in Cs(CS_ARCH_X86, CS_MODE_64).disasm(code, recover.entry.st_value)]
            else:
                ins = []
            out['d01_analysis_disassembly'] = json.dumps(ins, separators=(',', ':'))
        for day in ('d02', 'd03', 'd04', 'd05'):
            exe_name, exe = next((n,b) for n,b in byday[day] if n.endswith(('.elf','.dll','.exe')))
            ver,key,crc,cfg = config(exe)
            for field in ('campaign','domain','mutex','url'):
                if f'{day}_analysis_config_{field}' in QUESTION_IDS:
                    out[f'{day}_analysis_config_{field}'] = cfg[field]
            if f'{day}_analysis_config_crc32_hex' in QUESTION_IDS:
                out[f'{day}_analysis_config_crc32_hex'] = f'0x{crc:08x}'
            if day == 'd02':
                out['d02_analysis_xor_key_hex'] = f'0x{key:02x}'
                out['d02_analysis_format'] = 'pe' if exe_name.endswith('.exe') else 'elf'
            elif day == 'd03':
                out['d03_analysis_format'] = 'PE_CLI'
                out['d03_analysis_machine'] = 'i386'
                pe = pefile.PE(data=exe, fast_load=False)
                com = pe.OPTIONAL_HEADER.DATA_DIRECTORY[14]
                cli_offset = pe.get_offset_from_rva(com.VirtualAddress)
                md_rva = struct.unpack_from('<I', exe, cli_offset + 8)[0]
                md_offset = pe.get_offset_from_rva(md_rva)
                version_len = struct.unpack_from('<I', exe, md_offset + 12)[0]
                out['d03_analysis_metadata_version'] = exe[md_offset + 16:md_offset + 16 + version_len].rstrip(b'\0').decode()
            elif day in ('d04','d05'):
                out[f'{day}_analysis_architecture'] = 'x86-64'
                out[f'{day}_analysis_format'] = 'pe' if exe_name.endswith('.exe') else 'elf'
        jar = next(b for n,b in byday['d06'] if n.endswith('.jar'))
        with zipfile.ZipFile(__import__('io').BytesIO(jar)) as j:
            classes = [j.read(n) for n in j.namelist() if n.endswith('.class')]
        records = []
        for cls in classes:
            for candidate in re.findall(rb'[A-Za-z0-9+/]{80,}={0,2}', cls):
                try:
                    records.append(config(base64.b64decode(candidate, validate=True)))
                except (ValueError, base64.binascii.Error):
                    pass
        if len(records) != 1:
            raise ValueError(f'expected one Java config, got {len(records)}')
        ver,key,crc,cfg = records[0]
        out['d06_analysis_format'] = 'jar'
        for field in ('campaign','domain','mutex','url'):
            out[f'd06_analysis_config_{field}'] = cfg[field]
        out['d06_analysis_config_crc32_hex'] = f'0x{crc:08x}'
        out['d06_analysis_hcfg_version'] = str(ver)
    return out


QUESTION_IDS = set()

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('archive', type=Path)
    ap.add_argument('--ids', type=Path, help='JSON array of current answer IDs')
    args = ap.parse_args()
    if args.ids:
        QUESTION_IDS.update(json.loads(args.ids.read_text()))
    else:
        QUESTION_IDS.update(json.loads((Path(__file__).parent / 'challenge_state.json').read_text())['modes']['single_solve']['status']['answer_ids'])
    print(json.dumps(solve(args.archive), indent=2))
