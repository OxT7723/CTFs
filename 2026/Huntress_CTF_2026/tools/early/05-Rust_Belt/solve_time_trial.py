#!/usr/bin/env python3
"""Solve the assigned Rust Belt Time Trial from its downloaded bytes."""

import hashlib
import io
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
from urllib.parse import urljoin
import zlib

from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from elftools.elf.elffile import ELFFile
import pefile
import requests


BASE = "https://2026.huntress.ctf.games/"
CID = "binary-reverse-engineering-day-05-rust-runtime-shapes/time_trial"
ROOT = Path(__file__).resolve().parent


def extract_config(data):
    offset = 0
    while (offset := data.find(b"HCFG", offset)) >= 0:
        if offset + 12 <= len(data):
            version, key, size, crc = struct.unpack_from("<BBHI", data, offset + 4)
            if version == 1 and size < 10000 and offset + 12 + size <= len(data):
                decoded = bytes(b ^ key for b in data[offset + 12:offset + 12 + size])
                if zlib.crc32(decoded) == crc:
                    return json.loads(decoded), key, crc
        offset += 4
    raise ValueError("No valid HCFG block")


def elf_details(data):
    elf = ELFFile(io.BytesIO(data))
    names = [section.name for section in elf.iter_sections()]
    symtab = elf.get_section_by_name(".symtab")
    symbols = [symbol.name for symbol in symtab.iter_symbols() if symbol.name] if symtab else []
    disassembly = []
    if symtab:
        for symbol in symtab.iter_symbols():
            if symbol.name != "recover_code" or symbol["st_info"]["type"] != "STT_FUNC":
                continue
            section = elf.get_section(symbol["st_shndx"])
            start = symbol["st_value"] - section["sh_addr"]
            code = section.data()[start:start + symbol["st_size"]]
            disassembly = [
                (ins.mnemonic + (" " + ins.op_str.replace(", ", ",") if ins.op_str else ""))
                for ins in Cs(CS_ARCH_X86, CS_MODE_64).disasm(code, symbol["st_value"])
            ]
            break
    machine = {"EM_X86_64": "x86-64"}.get(elf["e_machine"], elf["e_machine"])
    return {
        "elf_class": "ELF" + str(elf.elfclass),
        "machine": machine,
        "section_names": json.dumps(names, separators=(",", ":")),
        "symbols": json.dumps(symbols, separators=(",", ":")),
        "disassembly": json.dumps(disassembly, separators=(",", ":")),
        "elf_type": elf["e_type"],
        "endianness": "little" if elf.little_endian else "big",
    }


def pe_metadata(data):
    pe = pefile.PE(data=data)
    cli = pe.OPTIONAL_HEADER.DATA_DIRECTORY[14]
    cli_offset = pe.get_offset_from_rva(cli.VirtualAddress)
    metadata_rva = struct.unpack_from("<I", data, cli_offset + 8)[0]
    metadata_offset = pe.get_offset_from_rva(metadata_rva)
    length = struct.unpack_from("<I", data, metadata_offset + 12)[0]
    version = data[metadata_offset + 16:metadata_offset + 16 + length].rstrip(b"\0").decode()
    return "i386" if pe.FILE_HEADER.Machine == 0x14C else hex(pe.FILE_HEADER.Machine), version


def solve(files):
    answers = {}
    for day in range(1, 6):
        prefix = f"d{day:02}"
        extensions = (".dll",) if day == 3 else (".elf", ".exe")
        name = next(name for name in files if name.startswith(prefix + "--") and name.endswith(extensions))
        data = files[name]
        container = "pe" if data[:2] == b"MZ" else "elf"
        answers[f"{prefix}_artifact_sha256_1"] = hashlib.sha256(data).hexdigest()
        if day == 1:
            answers.update({f"{prefix}_analysis_{key}": value for key, value in elf_details(data).items()})
            continue
        config, xor_key, crc = extract_config(data)
        for key in ("campaign", "domain", "mutex", "url"):
            if day != 3 or key != "url":
                answers[f"{prefix}_analysis_config_{key}"] = config[key]
        if day != 3:
            answers[f"{prefix}_analysis_config_crc32_hex"] = hex(crc)
        if day == 2:
            answers[f"{prefix}_analysis_format"] = container
            answers[f"{prefix}_analysis_xor_key_hex"] = hex(xor_key)
        elif day == 3:
            runtime_name = next(name for name in files if name.startswith(prefix + "--") and name.endswith(".runtimeconfig.json"))
            answers[f"{prefix}_artifact_sha256_2"] = hashlib.sha256(files[runtime_name]).hexdigest()
            answers[f"{prefix}_analysis_format"] = "PE_CLI"
            answers[f"{prefix}_analysis_machine"], answers[f"{prefix}_analysis_metadata_version"] = pe_metadata(data)
        else:
            if container == "pe":
                pe = pefile.PE(data=data, fast_load=True)
                architecture = "x86-64" if pe.FILE_HEADER.Machine == 0x8664 else hex(pe.FILE_HEADER.Machine)
            else:
                architecture = "x86-64" if ELFFile(io.BytesIO(data))["e_machine"] == "EM_X86_64" else "unknown"
            answers[f"{prefix}_analysis_architecture"] = architecture
            answers[f"{prefix}_analysis_format"] = container
    return answers


def main():
    token = os.environ.get("HUNTRESS_GM_TOKEN")
    if not token:
        raise SystemExit("HUNTRESS_GM_TOKEN is missing")
    session = requests.Session()
    session.headers.update({"Authorization": "Bearer " + token})
    start = session.post(BASE, json={"challenge": CID}, timeout=10)
    start.raise_for_status()
    assignment = start.json()
    if "download" not in assignment:
        print(json.dumps({"stage": "start", "response": assignment}))
        return
    download = session.get(urljoin(BASE, assignment["download"]), timeout=10)
    download.raise_for_status()
    archive = download.content
    archive_hash = hashlib.sha256(archive).hexdigest()
    if archive_hash != assignment["sha256"]:
        raise ValueError("Assigned ZIP SHA-256 mismatch")
    attempt_id = assignment["attempt_id"]
    output = ROOT / "artifacts" / "time_trial" / ("attempt-" + attempt_id)
    output.mkdir(parents=True, exist_ok=True)
    (output / "evidence.zip").write_bytes(archive)
    with tempfile.TemporaryDirectory(prefix="rust-belt-") as work:
        zip_path = Path(work) / "evidence.zip"
        zip_path.write_bytes(archive)
        extracted = Path(work) / "extracted"
        extracted.mkdir()
        subprocess.run(["7z", "x", "-y", "-pinfected", "-o" + str(extracted), str(zip_path)], check=True, stdout=subprocess.DEVNULL)
        files = {p.name: p.read_bytes() for p in extracted.iterdir() if p.is_file()}
        answers = solve(files)
    expected = set(assignment["answer_ids"])
    if set(answers) != expected:
        print(json.dumps({"stage": "answer_fields", "missing": sorted(expected - set(answers)), "unexpected": sorted(set(answers) - expected), "attempt_id": attempt_id, "deadline": assignment.get("deadline")}))
        return
    response = session.post(BASE, json={"challenge": CID, "answers": answers}, timeout=10)
    response.raise_for_status()
    result = response.json()
    print(json.dumps({"attempt_id": attempt_id, "deadline": assignment.get("deadline"), "download": assignment["download"], "sha256": archive_hash, "result": result.get("result"), "remaining": result.get("remaining"), "status": result.get("status"), "flag": result.get("flag"), "answer_count": len(answers), "artifact_path": str(output / "evidence.zip")}))


if __name__ == "__main__":
    main()
