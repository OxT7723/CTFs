#!/usr/bin/env python3
"""Build binary challenge answers from a start response and extracted files."""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import re
import subprocess
import zipfile
import zlib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass
class Hcfg:
    source_offset: int | None
    record_offset: int
    version: int
    xor_key: int
    crc32: int
    payload: bytes
    values: dict


def valid_hcfg_records(
    data: bytes, source_offset: int | None = None, limit: int | None = None
) -> list[Hcfg]:
    """Return every bounded, CRC-valid HCFG JSON object in the supplied bytes."""
    records: list[Hcfg] = []
    offset = 0
    while True:
        offset = data.find(b"HCFG", offset)
        if offset < 0:
            return records
        if offset + 12 <= len(data):
            version, key = data[offset + 4], data[offset + 5]
            length = int.from_bytes(data[offset + 6:offset + 8], "little")
            expected_crc = int.from_bytes(data[offset + 8:offset + 12], "little")
            payload_end = offset + 12 + length
            if payload_end <= len(data):
                cipher = data[offset + 12:payload_end]
                plain = bytes(byte ^ key for byte in cipher)
                if zlib.crc32(plain) == expected_crc:
                    try:
                        values = json.loads(plain)
                    except (UnicodeDecodeError, json.JSONDecodeError):
                        pass
                    else:
                        if isinstance(values, dict):
                            records.append(
                                Hcfg(
                                    source_offset,
                                    offset,
                                    version,
                                    key,
                                    expected_crc,
                                    plain,
                                    values,
                                )
                            )
                            if limit is not None and len(records) >= limit:
                                return records
        offset += 1


def valid_hcfg(data: bytes, source_offset: int | None = None) -> Hcfg | None:
    records = valid_hcfg_records(data, source_offset, limit=1)
    return records[0] if records else None


def find_unique_raw_hcfg(path: Path) -> Hcfg:
    """Find the sole valid raw HCFG record in the delivered file bytes."""
    records = valid_hcfg_records(path.read_bytes())
    if len(records) != 1:
        raise ValueError(
            f"Expected one CRC32-valid raw HCFG record in {path}, found {len(records)}"
        )
    return records[0]


def embedded_blobs(path: Path):
    raw = path.read_bytes()
    yield raw, 0
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            for member in archive.infolist():
                if not member.is_dir():
                    yield archive.read(member), 0


def find_hcfg(path: Path) -> Hcfg:
    for blob, _ in embedded_blobs(path):
        found = valid_hcfg(blob)
        if found:
            return found
        for match in re.finditer(rb"[A-Za-z0-9+/]{80,}={0,2}", blob):
            try:
                decoded = base64.b64decode(match.group(), validate=True)
            except (ValueError, binascii.Error):
                continue
            found = valid_hcfg(decoded, match.start())
            if found:
                return found
    raise ValueError(f"No valid HCFG record found in {path}")


def find_hcfg_backward(path: Path) -> Hcfg:
    """Find the last CRC32-valid raw HCFG record in a specimen."""
    data = path.read_bytes()
    end = len(data)
    while True:
        offset = data.rfind(b"HCFG", 0, end)
        if offset < 0:
            break
        end = offset
        if offset + 12 > len(data):
            continue
        version, key = data[offset + 4], data[offset + 5]
        length = int.from_bytes(data[offset + 6:offset + 8], "little")
        expected_crc = int.from_bytes(data[offset + 8:offset + 12], "little")
        cipher = data[offset + 12:offset + 12 + length]
        if len(cipher) != length:
            continue
        plain = bytes(byte ^ key for byte in cipher)
        if zlib.crc32(plain) != expected_crc:
            continue
        try:
            values = json.loads(plain)
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        return Hcfg(None, offset, version, key, expected_crc, plain, values)
    raise ValueError(f"No valid raw HCFG record found in {path}")


def find_hgrf_backward(path: Path) -> Hcfg:
    """Find the last CRC32-valid raw HGRF record in a specimen."""
    data = path.read_bytes()
    end = len(data)
    while True:
        offset = data.rfind(b"HGRF", 0, end)
        if offset < 0:
            break
        end = offset
        if offset + 12 > len(data):
            continue
        version, key = data[offset + 4], data[offset + 5]
        length = int.from_bytes(data[offset + 6:offset + 8], "little")
        expected_crc = int.from_bytes(data[offset + 8:offset + 12], "little")
        cipher = data[offset + 12:offset + 12 + length]
        if len(cipher) != length:
            continue
        plain = bytes(byte ^ key for byte in cipher)
        if zlib.crc32(plain) != expected_crc:
            continue
        try:
            values = json.loads(plain)
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if isinstance(values, dict):
            return Hcfg(None, offset, version, key, expected_crc, plain, values)
    raise ValueError(f"No valid raw HGRF record found in {path}")


def find_hgau_backward(path: Path) -> Hcfg:
    """Find the last CRC32-valid raw HGAU record in a specimen."""
    data = path.read_bytes()
    end = len(data)
    while True:
        offset = data.rfind(b"HGAU", 0, end)
        if offset < 0:
            break
        end = offset
        if offset + 12 > len(data):
            continue
        version, key = data[offset + 4], data[offset + 5]
        length = int.from_bytes(data[offset + 6:offset + 8], "little")
        expected_crc = int.from_bytes(data[offset + 8:offset + 12], "little")
        cipher = data[offset + 12:offset + 12 + length]
        if len(cipher) != length:
            continue
        plain = bytes(byte ^ key for byte in cipher)
        if zlib.crc32(plain) != expected_crc:
            continue
        try:
            values = json.loads(plain)
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if isinstance(values, dict):
            return Hcfg(None, offset, version, key, expected_crc, plain, values)
    raise ValueError(f"No valid raw HGAU record found in {path}")


def decode_packed_overlay(path: Path) -> tuple[bytes, int, int]:
    """Decode the final PK19/RS20 overlay appended to a delivered specimen."""
    data = path.read_bytes()
    candidates = [
        (data.rfind(magic), magic)
        for magic in (b"PK19", b"RS20")
    ]
    offset, magic = max(candidates, key=lambda item: item[0])
    if offset < 0:
        raise ValueError(f"No supported packed overlay found in {path}")
    if magic == b"RS20":
        header_end = offset + 48
        if header_end > len(data):
            raise ValueError(f"Truncated RS20 resource header in {path}")
        resource_length = int.from_bytes(data[offset + 8:offset + 12], "little")
        scratch_length = int.from_bytes(data[offset + 12:offset + 14], "little")
        expected_scratch_sha256 = data[offset + 16:offset + 48]
        resource_end = header_end + resource_length
        overlay_end = resource_end + scratch_length
        if overlay_end != len(data):
            raise ValueError(f"RS20 resource and scratch bounds do not match {path}")
        resource = data[header_end:resource_end]
        scratch = data[resource_end:overlay_end]
        if hashlib.sha256(scratch).digest() != expected_scratch_sha256:
            raise ValueError(f"RS20 scratch SHA-256 mismatch in {path}")
        return resource, offset, len(data) - offset
    header_end = offset + 44
    if header_end > len(data):
        raise ValueError(f"Truncated packed overlay header in {path}")
    key1, key2 = data[offset + 5], data[offset + 6]
    packed_length = int.from_bytes(data[offset + 8:offset + 12], "little")
    expected_sha256 = data[offset + 12:offset + 44]
    packed = data[header_end:header_end + packed_length]
    if len(packed) != packed_length:
        raise ValueError(f"Truncated packed overlay payload in {path}")

    def ror8(value: int, count: int) -> int:
        return ((value >> count) | (value << (8 - count))) & 0xFF

    unpacked = bytes(ror8(byte ^ key2, 3) ^ key1 for byte in packed)
    if hashlib.sha256(unpacked).digest() != expected_sha256:
        raise ValueError(f"Packed overlay SHA-256 mismatch in {path}")
    return unpacked, offset, len(data) - offset


def run_tool(*args: str) -> str:
    return subprocess.check_output(args, text=True, errors="replace")


@lru_cache(maxsize=512)
def elf_header(path: Path) -> str:
    return run_tool("readelf", "-h", str(path))


@lru_cache(maxsize=512)
def elf_sections(path: Path) -> str:
    return run_tool("readelf", "-SW", str(path))


@lru_cache(maxsize=512)
def pe_section_names(path: Path) -> list[str]:
    data = path.read_bytes()
    if data[:2] != b"MZ" or len(data) < 0x40:
        raise ValueError(f"Not a valid PE image: {path}")
    pe_offset = int.from_bytes(data[0x3C:0x40], "little")
    if pe_offset + 24 > len(data) or data[pe_offset:pe_offset + 4] != b"PE\0\0":
        raise ValueError(f"Invalid PE signature in {path}")
    section_count = int.from_bytes(data[pe_offset + 6:pe_offset + 8], "little")
    optional_size = int.from_bytes(data[pe_offset + 20:pe_offset + 22], "little")
    section_table = pe_offset + 24 + optional_size
    if section_table + section_count * 40 > len(data):
        raise ValueError(f"Truncated PE section table in {path}")
    return [
        data[section_table + index * 40:section_table + index * 40 + 8]
        .split(b"\0", 1)[0]
        .decode("ascii", errors="replace")
        for index in range(section_count)
    ]


def elf_symbols(path: Path) -> str:
    return run_tool("readelf", "-sW", str(path))


@lru_cache(maxsize=512)
def section_names(path: Path) -> list[str]:
    if path.read_bytes().startswith(b"MZ"):
        return pe_section_names(path)
    names = [""]
    for line in elf_sections(path).splitlines():
        match = re.match(r"\s*\[\s*(\d+)\]\s+(\S+)", line)
        if match and match.group(1) != "0":
            names.append(match.group(2))
    return names


def symbol_names(path: Path) -> list[str]:
    if path.read_bytes().startswith(b"MZ"):
        names = []
        for line in run_tool("nm", "-a", str(path)).splitlines():
            fields = line.split()
            if len(fields) >= 3 and len(fields[-2]) == 1 and not fields[-1].startswith("."):
                names.append(fields[-1])
        return names
    output = elf_symbols(path)
    table_match = re.search(
        r"Symbol table '\.symtab' contains.*?(?=\nSymbol table |\Z)",
        output,
        re.S,
    )
    if not table_match:
        return []
    names = []
    for line in table_match.group().splitlines():
        match = re.match(
            r"\s*\d+:\s+\S+\s+\d+\s+\S+\s+\S+\s+\S+\s+\S+\s*(.*)$", line
        )
        if match and match.group(1).strip():
            names.append(match.group(1).rstrip())
    return names


def exported_function_names(path: Path) -> list[str]:
    """Return defined global ELF functions from the static symbol table."""
    if not path.read_bytes().startswith(b"\x7fELF"):
        return []
    names = []
    for line in elf_symbols(path).splitlines():
        match = re.match(
            r"\s*\d+:\s+[0-9a-fA-F]+\s+\d+\s+FUNC\s+GLOBAL\s+\S+\s+(\S+)\s+(\S+)",
            line,
        )
        if match and match.group(1) != "UND":
            names.append(match.group(2))
    return names


def designated_exported_symbol(path: Path, questions: list[dict]) -> str:
    """Resolve a single referenced exported function without guessing on ambiguity."""
    names = exported_function_names(path)
    if not names:
        return "none"
    context = "\n".join(
        f"{question.get('id', '')} {question.get('question', '')}"
        for question in questions
    )
    referenced = [
        name for name in names
        if re.search(rf"(?<![\w]){re.escape(name)}(?![\w])", context)
    ]
    if len(referenced) == 1:
        return referenced[0]

    analysis_names = [
        name for name in names
        if name.casefold() != "main"
        and re.search(r"analysis|recover|decode|inspect", name, re.I)
    ]
    if len(analysis_names) == 1:
        return analysis_names[0]
    if not analysis_names:
        return "none"
    raise ValueError(
        "Could not identify one designated exported function from the ELF questions"
    )


def pe_section_symbol(path: Path, section: str, symbol: str) -> str | None:
    prefix = section + "$"
    for line in run_tool("nm", "-a", str(path)).splitlines():
        fields = line.split()
        if len(fields) >= 3 and fields[-1].startswith(prefix):
            if fields[-1].endswith(symbol):
                return fields[-1]
    return None


def elf_symbol_bytes(path: Path, name: str) -> bytes | None:
    output = elf_symbols(path)
    symbol = None
    for line in output.splitlines():
        match = re.match(
            r"\s*\d+:\s+([0-9a-fA-F]+)\s+(\d+)\s+\S+\s+\S+\s+\S+\s+(\d+)\s+(\S+)",
            line,
        )
        if match and match.group(4) == name:
            symbol = (
                int(match.group(1), 16),
                int(match.group(2)),
                int(match.group(3)),
            )
            break
    if symbol is None:
        return None
    address, size, section_index = symbol

    section = None
    for line in elf_sections(path).splitlines():
        match = re.match(
            r"\s*\[\s*(\d+)\]\s+(\S+)\s+\S+\s+([0-9a-fA-F]+)\s+"
            r"([0-9a-fA-F]+)\s+([0-9a-fA-F]+)",
            line,
        )
        if match and int(match.group(1)) == section_index:
            section = (
                int(match.group(3), 16),
                int(match.group(4), 16),
                int(match.group(5), 16),
            )
            break
    if section is None:
        raise ValueError(f"Could not locate ELF section #{section_index} in {path}")
    section_address, file_offset, section_size = section
    if not section_address <= address < section_address + section_size:
        raise ValueError(f"ELF symbol {name!r} falls outside its section")
    start = file_offset + address - section_address
    data = path.read_bytes()
    end = start + size if size else data.find(b"\0", start)
    if end < start:
        end = len(data)
    return data[start:end].split(b"\0", 1)[0]


def elf_section_bytes(path: Path, name: str) -> bytes | None:
    data = path.read_bytes()
    for line in elf_sections(path).splitlines():
        match = re.match(
            r"\s*\[\s*(\d+)\]\s+(\S+)\s+\S+\s+([0-9a-fA-F]+)\s+"
            r"([0-9a-fA-F]+)\s+([0-9a-fA-F]+)",
            line,
        )
        if match and match.group(2) == name:
            offset = int(match.group(4), 16)
            size = int(match.group(5), 16)
            return data[offset:offset + size].split(b"\0", 1)[0]
    return None


def elf_section_data(path: Path, name: str) -> bytes | None:
    """Return the exact file-backed bytes of an ELF section."""
    data = path.read_bytes()
    for line in elf_sections(path).splitlines():
        match = re.match(
            r"\s*\[\s*(\d+)\]\s+(\S+)\s+\S+\s+([0-9a-fA-F]+)\s+"
            r"([0-9a-fA-F]+)\s+([0-9a-fA-F]+)",
            line,
        )
        if match and match.group(2) == name:
            offset = int(match.group(4), 16)
            size = int(match.group(5), 16)
            return data[offset:offset + size]
    return None


def disassemble_recover_code(path: Path) -> list[str]:
    output = run_tool(
        "objdump", "-d", "-M", "intel", "--disassemble=recover_code", str(path)
    )
    instructions = []
    for line in output.splitlines():
        match = re.match(
            r"\s*[0-9a-f]+:\s+(?:[0-9a-f]{2}\s+)+\s*"
            r"([a-z][a-z0-9.]*)\s*(.*?)\s*$",
            line,
            re.I,
        )
        if match:
            instruction, operands = match.groups()
            instructions.append(
                instruction.lower() + (" " + operands.strip() if operands.strip() else "")
            )
    return instructions


def recover_code_value(path: Path) -> int | None:
    """Evaluate the common immediate-return form without executing the sample."""
    value = None
    instructions = disassemble_recover_code(path)
    if not instructions:
        return None
    for instruction in instructions:
        match = re.fullmatch(
            r"(mov|movabs)\s+(eax|rax),\s*(0x[0-9a-f]+|\d+)",
            instruction,
        )
        if match:
            value = int(match.group(3), 0)
            continue
        match = re.fullmatch(
            r"(xor|add|sub|or|and)\s+(eax|rax),\s*(eax|rax|0x[0-9a-f]+|\d+)",
            instruction,
        )
        if match:
            operation, _, operand = match.groups()
            if operand in {"eax", "rax"}:
                other = value
            else:
                other = int(operand, 0)
            if value is None:
                if operation == "xor" and operand in {"eax", "rax"}:
                    value = 0
                    continue
                raise ValueError(f"Cannot evaluate recover_code instruction: {instruction}")
            if operation == "xor":
                value ^= other
            elif operation == "add":
                value += other
            elif operation == "sub":
                value -= other
            elif operation == "or":
                value |= other
            elif operation == "and":
                value &= other
            if instruction.split()[1].startswith("eax"):
                value &= 0xFFFFFFFF
            continue
        if instruction.startswith(("ret", "nop", "endbr64", "push ", "pop ")):
            continue
        if instruction in {"leave"}:
            continue
        raise ValueError(f"Cannot evaluate recover_code instruction: {instruction}")
    if value is None:
        raise ValueError(f"Could not recover an immediate return value from {path}")
    return value


def java_class_info(data: bytes) -> dict:
    """Read a class file's header and member names without a JDK dependency."""
    if data[:4] != b"\xca\xfe\xba\xbe":
        raise ValueError("Invalid Java class file")
    offset = 8

    def read_u1() -> int:
        nonlocal offset
        value = data[offset]
        offset += 1
        return value

    def read_u2() -> int:
        nonlocal offset
        value = int.from_bytes(data[offset:offset + 2], "big")
        offset += 2
        return value

    def read_u4() -> int:
        nonlocal offset
        value = int.from_bytes(data[offset:offset + 4], "big")
        offset += 4
        return value

    def skip_attributes(count: int) -> None:
        nonlocal offset
        for _ in range(count):
            read_u2()
            length = read_u4()
            offset += length

    constant_pool: list[object | None] = [None] * read_u2()
    index = 1
    while index < len(constant_pool):
        tag = read_u1()
        if tag == 1:
            length = read_u2()
            constant_pool[index] = data[offset:offset + length].decode(
                "utf-8", errors="replace"
            )
            offset += length
        elif tag in {3, 4}:
            offset += 4
        elif tag in {5, 6}:
            offset += 8
            index += 1
        elif tag in {7, 8, 16, 19, 20}:
            constant_pool[index] = read_u2()
        elif tag in {9, 10, 11, 12, 17, 18}:
            offset += 4
        elif tag == 15:
            offset += 3
        else:
            raise ValueError(f"Unsupported Java constant-pool tag {tag}")
        index += 1

    access_flags = read_u2()
    this_class = read_u2()
    read_u2()  # superclass
    class_name_index = constant_pool[this_class]
    class_name = constant_pool[class_name_index] if isinstance(class_name_index, int) else ""
    for _ in range(read_u2()):
        read_u2()

    for _ in range(read_u2()):
        read_u2()
        read_u2()
        read_u2()
        skip_attributes(read_u2())

    methods = []
    for _ in range(read_u2()):
        flags = read_u2()
        name_index = read_u2()
        descriptor_index = read_u2()
        methods.append(
            {
                "access_flags": flags,
                "name": constant_pool[name_index],
                "descriptor": constant_pool[descriptor_index],
            }
        )
        skip_attributes(read_u2())
    skip_attributes(read_u2())
    return {
        "name": class_name.replace("/", "."),
        "internal_name": class_name,
        "access_flags": access_flags,
        "methods": methods,
        "constant_pool": constant_pool,
    }


@lru_cache(maxsize=256)
def jar_main_class_info(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        manifest = archive.read("META-INF/MANIFEST.MF").decode("utf-8", errors="replace")
        manifest = re.sub(r"\r?\n ", "", manifest)
        main_match = re.search(r"(?im)^Main-Class:\s*(\S+)", manifest)
        if main_match:
            entry = main_match.group(1).replace(".", "/") + ".class"
        else:
            candidates = [
                name for name in archive.namelist()
                if name.endswith(".class") and "$" not in Path(name).stem
            ]
            if not candidates:
                raise ValueError(f"No main class found in {path}")
            entry = candidates[0]
        return java_class_info(archive.read(entry))


def jar_has_coroutine_runtime(path: Path) -> bool:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if any(name.startswith("kotlinx/coroutines/") for name in names):
            return True
        return any(
            name.startswith("kotlin/coroutines/jvm/internal/")
            and name.endswith(".class")
            for name in names
        )


def jar_json_member(path: Path, member: str) -> dict:
    """Read a JSON evidence member embedded in a JAR."""
    with zipfile.ZipFile(path) as archive:
        try:
            content = archive.read(member)
        except KeyError as exc:
            raise ValueError(f"JAR {path} has no {member!r} member") from exc
    value = json.loads(content)
    if not isinstance(value, dict):
        raise ValueError(f"JAR member {member!r} is not a JSON object")
    return value


def binary_container(path: Path) -> str:
    """Classify a specimen by its parsed final container, including valid JARs."""
    data = path.read_bytes()
    if data.startswith(b"\x7fELF"):
        return "elf"
    if data.startswith(b"MZ"):
        return "pe_cli" if metadata_version(path) != "none" else "pe"
    if data.startswith(b"\x00asm"):
        return "wasm"
    if data.startswith(b"PK"):
        try:
            with zipfile.ZipFile(path) as archive:
                if any(
                    name.endswith(".class")
                    and archive.read(name).startswith(b"\xca\xfe\xba\xbe")
                    for name in archive.namelist()
                    if not name.endswith("/")
                ):
                    return "jar"
        except (OSError, zipfile.BadZipFile):
            pass
    if data.startswith(b"NEKO"):
        return "neko_bytecode"
    return "none"


def elf_section_for_file_offset(path: Path, offset: int) -> str:
    for line in elf_sections(path).splitlines():
        match = re.match(
            r"\s*\[\s*(\d+)\]\s+(\S+)\s+\S+\s+([0-9a-fA-F]+)\s+"
            r"([0-9a-fA-F]+)\s+([0-9a-fA-F]+)",
            line,
        )
        if match:
            file_offset = int(match.group(4), 16)
            size = int(match.group(5), 16)
            if file_offset <= offset < file_offset + size:
                return match.group(2)
    return "none"


def hcfg_storage(path: Path) -> str:
    found = find_hcfg(path)
    offset = found.source_offset if found.source_offset is not None else found.record_offset
    data = path.read_bytes()
    if found.source_offset is not None:
        return "base64"
    if data.startswith(b"\x00asm"):
        return "wasm_data_segment"
    if data.startswith(b"\x7fELF"):
        section = elf_section_for_file_offset(path, offset)
        if section == ".hcfg":
            return "raw_hcfg_section"
        if section == ".relro_padding":
            return "raw"
        if section in {".data", ".rodata", ".noptrdata"}:
            return "raw_const_array"
        return "raw"
    if data.startswith(b"MZ"):
        return "raw"
    raise ValueError(f"HCFG storage label is unresolved for {path}")


def elf_class(path: Path) -> int:
    match = re.search(r"Class:\s+ELF(\d+)", elf_header(path))
    if not match:
        raise ValueError(f"Could not read ELF class from {path}")
    return int(match.group(1))


def elf_machine(path: Path) -> str:
    match = re.search(r"Machine:\s*(.+)", elf_header(path))
    if not match:
        raise ValueError(f"Could not read ELF machine from {path}")
    label = match.group(1).strip()
    if "X86-64" in label:
        return "x86-64"
    if "Intel 80386" in label:
        return "i386"
    return label


def elf_machine_code(path: Path) -> int:
    data = path.read_bytes()
    if data[:4] != b"\x7fELF" or len(data) < 20:
        raise ValueError(f"Not a valid ELF header: {path}")
    byte_order = {1: "little", 2: "big"}.get(data[5])
    if byte_order is None:
        raise ValueError(f"Invalid ELF byte order in {path}")
    return int.from_bytes(data[18:20], byte_order)


def elf_entry(path: Path) -> str:
    match = re.search(r"Entry point address:\s*(0x[0-9a-f]+)", elf_header(path), re.I)
    if not match:
        raise ValueError(f"Could not read ELF entry point from {path}")
    return match.group(1).lower()


def pe_machine(path: Path) -> int:
    data = path.read_bytes()
    pe_offset = int.from_bytes(data[0x3C:0x40], "little")
    return int.from_bytes(data[pe_offset + 4:pe_offset + 6], "little")


def pe_machine_label(path: Path) -> str:
    output = run_tool("objdump", "-f", str(path))
    match = re.search(r"^\s*architecture:\s*([^,\s]+)", output, re.M)
    if not match:
        raise ValueError(f"Could not read PE machine label from {path}")
    return match.group(1)


@lru_cache(maxsize=512)
def metadata_version(path: Path) -> str:
    data = path.read_bytes()
    if len(data) < 0x40 or data[:2] != b"MZ":
        return "none"
    pe_offset = int.from_bytes(data[0x3C:0x40], "little")
    if pe_offset + 24 > len(data) or data[pe_offset:pe_offset + 4] != b"PE\0\0":
        return "none"
    section_count = int.from_bytes(data[pe_offset + 6:pe_offset + 8], "little")
    optional_size = int.from_bytes(data[pe_offset + 20:pe_offset + 22], "little")
    optional = pe_offset + 24
    if optional_size < 2 or optional + optional_size > len(data):
        return "none"
    magic = int.from_bytes(data[optional:optional + 2], "little")
    if magic == 0x10B:
        directory_offset = optional + 96
    elif magic == 0x20B:
        directory_offset = optional + 112
    else:
        return "none"
    if directory_offset + 15 * 8 > optional + optional_size:
        return "none"
    cli_rva = int.from_bytes(
        data[directory_offset + 14 * 8:directory_offset + 14 * 8 + 4], "little"
    )
    if cli_rva == 0:
        return "none"
    section_table = optional + optional_size

    def rva_to_offset(rva: int, size: int) -> int | None:
        for index in range(section_count):
            entry = section_table + 40 * index
            if entry + 40 > len(data):
                return None
            virtual_address = int.from_bytes(data[entry + 12:entry + 16], "little")
            raw_size = int.from_bytes(data[entry + 16:entry + 20], "little")
            raw_pointer = int.from_bytes(data[entry + 20:entry + 24], "little")
            delta = rva - virtual_address
            if delta >= 0 and delta + size <= raw_size:
                file_offset = raw_pointer + delta
                if file_offset + size <= len(data):
                    return file_offset
        return None

    cli_offset = rva_to_offset(cli_rva, 16)
    if cli_offset is None:
        return "none"
    metadata_rva = int.from_bytes(data[cli_offset + 8:cli_offset + 12], "little")
    if metadata_rva == 0:
        return "none"
    root = rva_to_offset(metadata_rva, 16)
    if root is None or data[root:root + 4] != b"BSJB":
        return "none"
    version_length = int.from_bytes(data[root + 12:root + 16], "little")
    version_end = root + 16 + version_length
    if version_end > len(data):
        return "none"
    version = data[root + 16:version_end].rstrip(b"\0")
    return version.decode("ascii", errors="replace")


def cli_runtime_version(path: Path) -> str:
    """Read the CLR runtime major.minor pair from a managed PE image."""
    data = path.read_bytes()
    if data[:2] != b"MZ" or len(data) < 0x40:
        raise ValueError(f"Not a managed PE image: {path}")
    pe_offset = int.from_bytes(data[0x3C:0x40], "little")
    section_count = int.from_bytes(data[pe_offset + 6:pe_offset + 8], "little")
    optional_size = int.from_bytes(data[pe_offset + 20:pe_offset + 22], "little")
    optional = pe_offset + 24
    magic = int.from_bytes(data[optional:optional + 2], "little")
    directory_offset = optional + (96 if magic == 0x10B else 112)
    cli_rva = int.from_bytes(data[directory_offset + 14 * 8:
                                  directory_offset + 14 * 8 + 4], "little")
    section_table = optional + optional_size
    for index in range(section_count):
        entry = section_table + index * 40
        virtual_size = int.from_bytes(data[entry + 8:entry + 12], "little")
        virtual_address = int.from_bytes(data[entry + 12:entry + 16], "little")
        raw_size = int.from_bytes(data[entry + 16:entry + 20], "little")
        raw_pointer = int.from_bytes(data[entry + 20:entry + 24], "little")
        if virtual_address <= cli_rva < virtual_address + max(virtual_size, raw_size):
            cli_offset = raw_pointer + cli_rva - virtual_address
            if cli_offset + 8 > len(data):
                break
            major = int.from_bytes(data[cli_offset + 4:cli_offset + 6], "little")
            minor = int.from_bytes(data[cli_offset + 6:cli_offset + 8], "little")
            return f"{major}.{minor}"
    raise ValueError(f"Could not locate a valid CLR header in {path}")


def artifact_index(extracted: Path) -> dict[str, list[Path]]:
    result: dict[str, list[Path]] = {}
    order_file = extracted / ".archive-members.json"
    if order_file.is_file():
        ordered_paths = [
            extracted / name for name in json.loads(order_file.read_text())
        ]
    else:
        ordered_paths = sorted(extracted.iterdir())
    for path in ordered_paths:
        match = re.match(r"(d\d+)--", path.name, re.I)
        if match and path.is_file():
            result.setdefault(match.group(1).lower(), []).append(path)
    return result


def primary_binary(paths: list[Path]) -> Path:
    candidates = [
        path for path in paths
        if path.suffix.lower() in {
            ".elf", ".dll", ".exe", ".jar", ".wasm", ".cmxs", ".n"
        }
    ]
    if not candidates:
        raise ValueError(f"No binary specimen found among: {paths}")
    return candidates[0]


def managed_assembly(paths: list[Path]) -> Path:
    """Resolve the Day 03 primary assembly without relying on archive ordering."""
    candidates = [
        path
        for path in paths
        if path.suffix.lower() == ".dll" and metadata_version(path) != "none"
    ]
    if len(candidates) == 1:
        return candidates[0]
    configured = [
        path
        for path in candidates
        if len(valid_hcfg_records(path.read_bytes())) == 1
    ]
    if len(configured) == 1:
        return configured[0]
    raise ValueError(
        "Could not uniquely identify the Day 03 managed assembly; "
        f"managed candidates: {candidates}, configured candidates: {configured}"
    )


def role_binary(paths: list[Path], role: str) -> Path:
    candidates = [
        path for path in paths
        if path.suffix.lower() in {
            ".elf", ".dll", ".exe", ".jar", ".wasm", ".cmxs", ".n"
        }
        and role.lower() in path.stem.lower()
    ]
    if len(candidates) != 1:
        raise ValueError(
            f"Expected one binary with role {role!r}, found: {candidates}"
        )
    return candidates[0]


def optimization_binary(paths: list[Path], optimized: bool) -> Path:
    """Select a Day 29 optimization variant by its delivered O3/O0 suffix."""
    suffix = "O3.elf" if optimized else "O0.elf"
    candidates = [
        path for path in paths
        if path.name.lower().endswith(suffix.lower())
    ]
    if len(candidates) != 1:
        raise ValueError(
            f"Expected one Day 29 {'optimized' if optimized else 'unoptimized'} "
            f"binary ending in {suffix!r}, found: {candidates}"
        )
    return candidates[0]


def labeled_role_binary(paths: list[Path], role: str) -> Path:
    """Select a specimen by an exact filename token such as ``c`` or ``cpp``."""
    wanted = role.lower()
    candidates = [
        path for path in paths
        if path.suffix.lower() in {".elf", ".dll", ".exe", ".jar", ".wasm", ".cmxs"}
        and wanted in re.findall(r"[a-z0-9]+", path.stem.lower())
    ]
    if len(candidates) != 1:
        raise ValueError(
            f"Expected one binary labeled {role!r}, found: {candidates}"
        )
    return candidates[0]


def slot_binary(paths: list[Path], slot: int) -> Path:
    """Select a delivered binary whose filename identifies its slot."""
    pattern = re.compile(rf"(?:^|[-_])slot[-_]?{slot}(?:[-_]|$)", re.I)
    candidates = [
        path for path in paths
        if path.suffix.lower() in {".elf", ".dll", ".exe", ".jar", ".wasm", ".cmxs"}
        and pattern.search(path.stem)
    ]
    if len(candidates) != 1:
        raise ValueError(
            f"Expected one binary for slot {slot}, found: {candidates}"
        )
    return candidates[0]


def build_answers(
    response: dict,
    extracted: Path,
    skip_suffixes: tuple[str, ...] = (),
) -> dict[str, str]:
    indexed = artifact_index(extracted)
    hcfg_cache: dict[str, Hcfg] = {}
    hgrf_cache: dict[str, Hcfg] = {}
    hgau_cache: dict[str, Hcfg] = {}
    symbols_cache: dict[str, list[str]] = {}
    overlay_cache: dict[str, tuple[bytes, int, int]] = {}
    paired_config_verified: set[str] = set()
    answers: dict[str, str] = {}

    def cached_symbols(path: Path) -> list[str]:
        cache_key = str(path)
        if cache_key not in symbols_cache:
            symbols_cache[cache_key] = symbol_names(path)
        return symbols_cache[cache_key]

    direct_field_aliases = {
        "sha256": "_artifact_sha256_binary",
        "elf_class": "_analysis_elf_class",
        "endianness": "_analysis_endianness",
        "machine": "_analysis_machine",
        "format": "_analysis_format",
        "elf_type": "_analysis_elf_type",
        "marker": "_analysis_marker",
        "has_symtab": "_analysis_has_symtab",
        "exported_symbol": "_analysis_exported_symbol",
        "recover_code": "_analysis_recover_code",
        "entry_point": "_analysis_entry_point",
        "xor_key": "_analysis_xor_key_hex",
        "config_crc32": "_config_crc32_hex",
        "campaign": "_config_campaign",
        "domain": "_config_domain",
        "url": "_config_url",
        "mutex": "_config_mutex",
        "has_cpp_vtable": "_analysis_has_cpp_vtable",
        "has_cpp_typeinfo": "_analysis_has_cpp_typeinfo",
        "mangled_score_symbol": "_analysis_mangled_score_symbol",
        "vtable_symbol": "_analysis_vtable_symbol",
    }

    for question in response["questions"]:
        answer_id = question["id"]
        if any(answer_id.lower().endswith(suffix.lower()) for suffix in skip_suffixes):
            continue
        labeled_role = None
        labeled_field = re.fullmatch(r"(c|cpp)_(.+)", answer_id, re.I)
        if labeled_field:
            labeled_role = labeled_field.group(1).lower()
            base_field = labeled_field.group(2).lower()
        else:
            base_field = answer_id.lower()
        day_match = re.match(r"(d\d+)_", answer_id, re.I)
        slot_match = re.fullmatch(
            r"(?:d\d+_)?slot(\d+)_(.+)", answer_id, re.I
        )
        if slot_match:
            base_field = slot_match.group(2).lower()
        field = direct_field_aliases.get(base_field, base_field)
        if field.startswith("analysis_"):
            field = "_" + field
        day = day_match.group(1).lower() if day_match else "standalone"
        paths = indexed.get(day, [])
        if not paths and (not day_match or slot_match):
            standalone = sorted(
                path for path in extracted.iterdir()
                if path.is_file()
                and path.suffix.lower() in {".elf", ".dll", ".exe", ".jar", ".wasm", ".cmxs"}
            )
            needs_named_specimen = (
                "_config_" in field
                or field.endswith(("_analysis_xor_key_hex",
                                   "_analysis_has_cpp_typeinfo",
                                   "_analysis_has_cpp_vtable",
                                   "_analysis_mangled_score_symbol",
                                   "_analysis_vtable_symbol"))
            )
            if slot_match or labeled_role or needs_named_specimen or len(standalone) == 1:
                paths = standalone
        if not paths:
            if not day_match and not slot_match and answer_id.lower() not in direct_field_aliases:
                raise ValueError(f"Cannot derive specimen from answer ID {answer_id}")
            raise ValueError(f"No extracted files for {day}")
        binary = (
            slot_binary(paths, int(slot_match.group(1)))
            if slot_match
            else labeled_role_binary(paths, labeled_role)
            if labeled_role
            else managed_assembly(paths)
            if day == "d03"
            else primary_binary(paths)
        )
        if day == "d30":
            if field.startswith("d30_analysis_config_capsule_"):
                binary = role_binary(paths, "config")
            elif field.startswith("d30_analysis_loader_"):
                binary = role_binary(paths, "loader")
            elif field.startswith("d30_analysis_library_"):
                binary = role_binary(paths, "library")
            elif field.startswith("d30_analysis_config_"):
                binary = role_binary(paths, "loader")

        def cached_hgrf() -> Hcfg:
            cache_key = str(binary)
            if cache_key not in hgrf_cache:
                hgrf_cache[cache_key] = find_hgrf_backward(binary)
            return hgrf_cache[cache_key]

        def cached_hgau() -> Hcfg:
            cache_key = str(binary)
            if cache_key not in hgau_cache:
                hgau_cache[cache_key] = find_hgau_backward(binary)
            return hgau_cache[cache_key]

        def campaign_graph_config() -> dict:
            if day not in paired_config_verified:
                canonical_graphs = []
                for role in ("loader", "library", "config"):
                    graph = find_hgrf_backward(role_binary(paths, role)).values
                    normalized = dict(graph)
                    normalized.pop("this_role", None)
                    canonical_graphs.append(normalized)
                if any(
                    graph != canonical_graphs[0]
                    for graph in canonical_graphs[1:]
                ):
                    raise ValueError(
                        "D30 campaign graphs differ after removing this_role"
                    )
                paired_config_verified.add(day)
            graph = cached_hgrf().values
            graph = graph.get("graph", graph)
            config = graph.get("config")
            if not isinstance(config, dict):
                raise ValueError(f"HGRF graph in {binary} has no config object")
            return config

        if (
            not labeled_role
            and len(paths) > 1
            and (
                field.endswith(("_analysis_has_cpp_typeinfo", "_analysis_has_cpp_vtable",
                                "_analysis_mangled_score_symbol", "_analysis_vtable_symbol"))
                or "_config_" in field
                or field.endswith(("_analysis_xor_key_hex",))
            )
        ):
            configured = []
            for candidate in paths:
                try:
                    find_hcfg(candidate)
                except ValueError:
                    continue
                configured.append(candidate)
            if "_config_" in field or field.endswith("_analysis_xor_key_hex"):
                if len(configured) == 1:
                    binary = configured[0]
            else:
                cpp_candidates = []
                for candidate in paths:
                    names = cached_symbols(candidate)
                    data = candidate.read_bytes()
                    if (
                        any(name.startswith(("_ZTV", "_ZTI")) for name in names)
                        or b"_ZTV" in data
                        or b"_ZTI" in data
                    ):
                        cpp_candidates.append(candidate)
                if len(cpp_candidates) == 1:
                    binary = cpp_candidates[0]
        role_match = re.match(
            r"d\d+_analysis_(stripped|symbolized|compact|direct|loader|plugin|corrected|vulnerable|gcc|tcc|false_friend|family_a|family_b|optimized|unoptimized)_",
            field,
        )
        if role_match:
            if day == "d29":
                binary = optimization_binary(
                    paths, optimized=role_match.group(1) == "optimized"
                )
            else:
                binary = role_binary(paths, role_match.group(1).replace("_", "-"))
        elif day == "d21" and "_config_" in field:
            binary = role_binary(paths, "plugin")
        elif day == "d28" and "_config_" in field:
            binary = role_binary(paths, "family-a")
        elif day == "d29" and "_config_" in field:
            binary = optimization_binary(paths, optimized=True)

        def cached_overlay() -> tuple[bytes, int, int]:
            cache_key = str(binary)
            if cache_key not in overlay_cache:
                overlay_cache[cache_key] = decode_packed_overlay(binary)
            return overlay_cache[cache_key]

        def cached_hcfg() -> Hcfg:
            cache_key = str(binary)
            if cache_key not in hcfg_cache:
                if day == "d03":
                    hcfg_cache[cache_key] = find_unique_raw_hcfg(binary)
                elif day in {"d27", "d28", "d29"}:
                    hcfg_cache[cache_key] = find_hcfg_backward(binary)
                elif binary.read_bytes().rfind(b"RS20") >= 0:
                    unpacked, _, _ = cached_overlay()
                    found = valid_hcfg(unpacked)
                    if found is None:
                        raise ValueError(
                            f"No valid HCFG record in RS20 resource for {binary}"
                        )
                    hcfg_cache[cache_key] = found
                else:
                    try:
                        hcfg_cache[cache_key] = find_hcfg(binary)
                    except ValueError:
                        unpacked, _, _ = cached_overlay()
                        found = valid_hcfg(unpacked)
                        if found is None:
                            raise ValueError(
                                f"No valid HCFG record in decoded overlay for {binary}"
                            )
                        hcfg_cache[cache_key] = found
            return hcfg_cache[cache_key]

        if (
            day in {"d24", "d25"}
            and "_config_" in field
            and not field.startswith(
                (
                    f"{day}_analysis_corrected_config_",
                    f"{day}_analysis_vulnerable_config_",
                )
            )
            and day not in paired_config_verified
        ):
            vulnerable = role_binary(paths, "vulnerable")
            corrected = role_binary(paths, "corrected")
            if find_hcfg(vulnerable).payload != find_hcfg(corrected).payload:
                raise ValueError(
                    f"{day.upper()} vulnerable and corrected HCFG payloads differ"
                )
            paired_config_verified.add(day)
        if (
            day == "d27"
            and "_config_" in field
            and not field.startswith(
                ("d27_analysis_gcc_config_", "d27_analysis_tcc_config_")
            )
            and day not in paired_config_verified
        ):
            gcc_config = find_hcfg_backward(role_binary(paths, "gcc"))
            tcc_config = find_hcfg_backward(role_binary(paths, "tcc"))
            if gcc_config.payload != tcc_config.payload:
                raise ValueError("D27 GCC and TCC HCFG payloads differ")
            paired_config_verified.add(day)
        if (
            day == "d28"
            and "_config_" in field
            and not field.startswith("d28_analysis_false_friend_config_")
            and day not in paired_config_verified
        ):
            family_a_config = find_hcfg_backward(role_binary(paths, "family-a"))
            family_b_config = find_hcfg_backward(role_binary(paths, "family-b"))
            if family_a_config.payload != family_b_config.payload:
                raise ValueError("D28 family A and family B HCFG payloads differ")
            paired_config_verified.add(day)
        if (
            day == "d29"
            and "_config_" in field
            and not field.startswith(
                (
                    "d29_analysis_optimized_config_",
                    "d29_analysis_unoptimized_config_",
                )
            )
            and day not in paired_config_verified
        ):
            optimized_config = find_hcfg_backward(
                optimization_binary(paths, optimized=True)
            )
            unoptimized_config = find_hcfg_backward(
                optimization_binary(paths, optimized=False)
            )
            if optimized_config.payload != unoptimized_config.payload:
                raise ValueError(
                    "D29 optimized and unoptimized HCFG payloads differ"
                )
            binary = optimization_binary(paths, optimized=True)
            paired_config_verified.add(day)

        if field.endswith("_structural_artifact_count"):
            value = str(len(paths))
        elif field.endswith("_structural_ordered_set_sha256"):
            joined_hashes = ":".join(
                hashlib.sha256(path.read_bytes()).hexdigest() for path in paths
            )
            value = hashlib.sha256(joined_hashes.encode("utf-8")).hexdigest()
        elif field.endswith("_analysis_section_count"):
            value = str(len(section_names(binary)))
        elif field.endswith("_analysis_symbol_count"):
            value = str(len(cached_symbols(binary)))
        elif field.endswith("_analysis_d_symbol_count"):
            value = str(sum(
                bool(re.search(r"^_D|\b_d_", name))
                for name in cached_symbols(binary)
            ))
        elif field.endswith("_analysis_crystal_symbol_count"):
            names = [
                line for line in run_tool("objdump", "-t", str(binary)).splitlines()
                if re.match(r"\s*[0-9a-fA-F]+\s", line)
            ]
            value = str(sum(
                bool(re.search(r"Crystal|crystal|__crystal|GC_", line))
                for line in names
            ))
        elif field.endswith("_analysis_handler_symbol_count"):
            value = str(sum(
                bool(re.search(r"event_(success|decoy|failure)", name))
                for name in cached_symbols(binary)
            ))
        elif field.endswith("_analysis_handler_symbols_sha256"):
            names = sorted(
                name for name in cached_symbols(binary)
                if re.search(r"event_(success|decoy|failure)", name)
            )
            value = hashlib.sha256("\n".join(names).encode("utf-8")).hexdigest()
        elif field.endswith("_analysis_overlay_offset"):
            _, offset, _ = cached_overlay()
            value = str(offset)
        elif field.endswith("_analysis_overlay_size"):
            _, _, size = cached_overlay()
            value = str(size)
        elif field.endswith("_analysis_packing_key_1_hex"):
            data = binary.read_bytes()
            offset = data.rfind(b"PK19")
            if offset < 0 or offset + 7 > len(data):
                raise ValueError(f"No complete PK19 overlay header in {binary}")
            value = f"0x{data[offset + 5]:02x}"
        elif field.endswith("_analysis_packing_key_2_hex"):
            data = binary.read_bytes()
            offset = data.rfind(b"PK19")
            if offset < 0 or offset + 7 > len(data):
                raise ValueError(f"No complete PK19 overlay header in {binary}")
            value = f"0x{data[offset + 6]:02x}"
        elif field.endswith("_analysis_hcfg_resource_size"):
            data = binary.read_bytes()
            offset = data.rfind(b"RS20")
            if offset < 0 or offset + 12 > len(data):
                raise ValueError(f"No complete RS20 resource header in {binary}")
            value = str(int.from_bytes(data[offset + 8:offset + 12], "little"))
        elif field == "_artifact_sha256_binary":
            value = hashlib.sha256(binary.read_bytes()).hexdigest()
        elif "_artifact_sha256_" in field:
            ordinal = int(field.rsplit("_", 1)[1]) - 1
            if ordinal < 0 or ordinal >= len(paths):
                raise ValueError(f"No artifact #{ordinal + 1} for {day}")
            value = hashlib.sha256(paths[ordinal].read_bytes()).hexdigest()
        elif field.endswith("_analysis_marker"):
            marker = elf_symbol_bytes(binary, "marker")
            if marker is None:
                marker = elf_section_bytes(binary, ".huntress")
            value = (
                marker.decode("utf-8", errors="replace")
                if marker is not None
                else "none"
            )
        elif field.endswith("_analysis_exported_symbol"):
            value = designated_exported_symbol(binary, response["questions"])
        elif field.endswith("_analysis_recover_code"):
            recovered = recover_code_value(binary)
            value = str(recovered) if recovered is not None else "none"
        elif "_config_" in field and not (
            day == "d30" and field.endswith("_format")
        ):
            if day == "d31":
                config_field = field.split("_config_", 1)[1]
                gauntlet = cached_hgau().values
                config = gauntlet.get("config")
                if not isinstance(config, dict):
                    raise ValueError(f"HGAU record in {binary} has no config object")
                if config_field in config:
                    value = str(config[config_field])
                else:
                    raise ValueError(f"HGAU config has no field {config_field!r}")
            elif day == "d30" and (
                field.startswith("d30_analysis_config_capsule_graph_config_")
                or field in {
                    "d30_analysis_config_campaign",
                    "d30_analysis_config_domain",
                    "d30_analysis_config_mutex",
                    "d30_analysis_config_url",
                }
            ):
                if field.startswith("d30_analysis_config_capsule_graph_config_"):
                    config_field = field.rsplit("_", 1)[1]
                else:
                    config_field = field.removeprefix("d30_analysis_config_")
                config = campaign_graph_config()
                if config_field in config:
                    value = str(config[config_field])
                else:
                    raise ValueError(
                        f"HGRF config has no field {config_field!r} in {day}"
                    )
            else:
                config_field = field.split("_config_", 1)[1]
                config = cached_hcfg()
                if config_field == "crc32_hex":
                    value = f"0x{config.crc32:08x}"
                elif config_field in config.values:
                    value = str(config.values[config_field])
                else:
                    raise ValueError(f"HCFG has no field {config_field!r} in {day}")
        elif field.endswith("_analysis_hcfg_version"):
            value = str(cached_hcfg().version)
        elif field.endswith("_analysis_xor_key_hex"):
            xor_key = cached_hgau().xor_key if day == "d31" else cached_hcfg().xor_key
            value = f"0x{xor_key:02x}"
        elif field.endswith("_analysis_gauntlet_crc32_hex"):
            value = f"0x{cached_hgau().crc32:08x}"
        elif field.endswith("_analysis_gauntlet_trace_branch"):
            trace = cached_hgau().values.get("trace")
            if not isinstance(trace, dict) or "branch" not in trace:
                raise ValueError(f"HGAU record in {binary} has no trace branch")
            value = str(trace["branch"])
        elif field.endswith(("_analysis_hcfg_offset", "_analysis_plugin_hcfg_offset")):
            found = cached_hcfg()
            value = str(
                found.source_offset
                if found.source_offset is not None
                else found.record_offset
            )
        elif field.endswith("_analysis_has_hcfg_section"):
            data = binary.read_bytes()
            if data.startswith(b"\x7fELF"):
                names = elf_sections(binary)
                present = ".hcfg" in names
            elif data.startswith(b"MZ"):
                names = pe_section_names(binary)
                present = any(name.lower() == ".hcfg" for name in names)
            else:
                present = False
            value = str(present).lower()
        elif field.endswith("_analysis_hcfg_storage"):
            value = hcfg_storage(binary)
        elif field.endswith("_analysis_cli_runtime"):
            value = cli_runtime_version(binary)
        elif field.endswith("_analysis_has_decoy_branch"):
            data = binary.read_bytes()
            present = (
                b"decoy" in data
                or "decoy".encode("utf-16le") in data
                or "decoy" in data.decode("utf-16le", errors="ignore")
            )
            value = str(present).lower()
        elif field.endswith("_analysis_has_nim_runtime"):
            data = binary.read_bytes()
            value = str(b"NimString" in data or b"NimMain" in data).lower()
        elif field.endswith("_analysis_has_fpc_runtime"):
            data = binary.read_bytes()
            present = b"FPC" in data or any(
                "FPC_" in name for name in cached_symbols(binary)
            )
            value = str(present).lower()
        elif field.endswith("_analysis_has_gnat_runtime"):
            data = binary.read_bytes()
            present = b"__gnat" in data or any(
                "gnat" in name for name in cached_symbols(binary)
            )
            value = str(present).lower()
        elif field.endswith("_analysis_conditional_branch_opcode_count"):
            text = elf_section_data(binary, ".text")
            if text is None:
                raise ValueError(f"No .text section found in {binary}")
            count = sum(0x70 <= byte <= 0x7F for byte in text)
            count += sum(
                text[index] == 0x0F and 0x80 <= text[index + 1] <= 0x8F
                for index in range(len(text) - 1)
            )
            value = str(count)
        elif field.endswith("_analysis_compression_methods"):
            with zipfile.ZipFile(binary) as archive:
                methods = sorted({item.compress_type for item in archive.infolist()})
            value = json.dumps(methods, separators=(",", ":"))
        elif field.endswith("_analysis_crash_fault_method"):
            trace = jar_json_member(binary, "crash/trace.json")
            frames = trace.get("frames")
            if (
                not isinstance(frames, list)
                or not frames
                or not isinstance(frames[0], str)
            ):
                raise ValueError(f"JAR {binary} has no first crash frame")
            value = frames[0]
        elif field.endswith("_analysis_crash_frames_match_methods"):
            trace = jar_json_member(binary, "crash/trace.json")
            frames = trace.get("frames")
            if not isinstance(frames, list) or not all(
                isinstance(frame, str) for frame in frames
            ):
                raise ValueError(f"JAR {binary} has an invalid crash frame list")
            method_names = {
                method["name"] for method in jar_main_class_info(binary)["methods"]
            }
            value = str(all(frame in method_names for frame in frames)).lower()
        elif field.endswith("_analysis_methods"):
            info = jar_main_class_info(binary)
            value = json.dumps(
                [method["name"] for method in info["methods"]],
                separators=(",", ":"),
            )
        elif field.endswith("_analysis_class_name"):
            value = jar_main_class_info(binary)["internal_name"]
        elif field.endswith("_analysis_class_count"):
            with zipfile.ZipFile(binary) as archive:
                value = str(sum(
                    name.endswith(".class") for name in archive.namelist()
                ))
        elif field.endswith("_analysis_method_names_sha256"):
            names = sorted({
                method["name"] for method in jar_main_class_info(binary)["methods"]
            })
            value = hashlib.sha256("\n".join(names).encode("utf-8")).hexdigest()
        elif field.endswith("_analysis_access_flags"):
            value = str(jar_main_class_info(binary)["access_flags"])
        elif field.endswith("_analysis_method_count"):
            value = str(len(jar_main_class_info(binary)["methods"]))
        elif field.endswith("_analysis_has_coroutine_runtime"):
            value = str(jar_has_coroutine_runtime(binary)).lower()
        elif field.endswith("_analysis_section_names"):
            value = json.dumps(section_names(binary), separators=(",", ":"))
        elif field.endswith("_analysis_symbols"):
            value = json.dumps(cached_symbols(binary), separators=(",", ":"))
        elif field.endswith("_analysis_disassembly"):
            value = json.dumps(disassemble_recover_code(binary), separators=(",", ":"))
        elif field.endswith("_analysis_elf_class"):
            cls = elf_class(binary)
            answer_format = question.get("answer_format", {})
            accepted_values = answer_format.get("accepted_values", [])
            if f"ELF{cls}" in accepted_values or answer_format.get("kind") == "exact_text":
                value = f"ELF{cls}"
            else:
                value = str(cls)
        elif field.endswith("_analysis_elf_type"):
            header = elf_header(binary)
            match = re.search(r"Type:\s*(\S+)", header)
            elf_type = match.group(1).upper() if match else None
            value = {
                "NONE": "ET_NONE",
                "REL": "ET_REL",
                "EXEC": "ET_EXEC",
                "DYN": "ET_DYN",
                "CORE": "ET_CORE",
            }.get(elf_type, elf_type or "none")
        elif field.endswith("_analysis_endianness"):
            header = elf_header(binary)
            value = "little" if "little endian" in header.lower() else "big"
        elif field.endswith("_analysis_entry_point"):
            value = elf_entry(binary)
        elif re.search(
            r"_analysis_(?:(?:stripped|symbolized|compact|direct|loader|plugin|gcc|tcc|false_friend|family_a|family_b|optimized|unoptimized)_)?"
            r"(?:machine|architecture)$",
            field,
        ):
            data = binary.read_bytes()
            if field.endswith(("_loader_machine", "_plugin_machine")):
                value = str(elf_machine_code(binary))
            elif data.startswith(b"\x00asm"):
                value = "wasm32"
            elif question.get("answer_format", {}).get("kind") == "integer":
                value = str(
                    pe_machine(binary)
                    if data.startswith(b"MZ")
                    else elf_machine_code(binary)
                )
            elif field.endswith(("_stripped_machine", "_symbolized_machine")):
                value = str(pe_machine(binary)) if data[:2] == b"MZ" else str(
                    elf_machine_code(binary)
                )
            else:
                value = (
                    pe_machine_label(binary)
                    if data[:2] == b"MZ"
                    else elf_machine(binary)
                )
        elif day in {"d24", "d25"} and field.endswith(
            ("_analysis_corrected_format", "_analysis_vulnerable_format")
        ):
            value = binary_container(binary)
        elif re.search(
            r"_analysis_(?:(?:stripped|symbolized|compact|direct|loader|library|config_capsule|gcc|tcc|false_friend|family_a|family_b|optimized|unoptimized)_)?format$",
            field,
        ):
            if day in {"d27", "d28", "d29", "d30"}:
                value = binary_container(binary)
            else:
                data = binary.read_bytes()
                if data.startswith(b"\x00asm"):
                    value = "WASM"
                elif data.startswith(b"\x7fELF"):
                    value = "ELF"
                elif data.startswith(b"PK"):
                    value = "JAR"
                elif data.startswith(b"MZ"):
                    value = "PE_CLI" if metadata_version(binary) != "none" else "PE"
                else:
                    value = "none"
            answer_format = question.get("answer_format", {})
            accepted_values = answer_format.get("accepted_values", [])
            if value.lower() in accepted_values:
                value = value.lower()
            elif answer_format.get("kind") == "exact_text":
                value = value.lower()
            elif field.startswith("d19_"):
                value = value.lower()
        elif field.endswith("_analysis_metadata_version"):
            value = metadata_version(binary)
        elif field.endswith("_analysis_has_symtab"):
            value = str(".symtab" in elf_sections(binary)).lower()
        elif field.endswith("_analysis_has_cpp_typeinfo"):
            data = binary.read_bytes()
            if data.startswith(b"MZ"):
                present = b"_ZTI" in data or b"typeinfo for" in data
            else:
                present = any(
                    name.startswith("_ZTI") or "typeinfo for" in name
                    for name in cached_symbols(binary)
                )
            value = str(present).lower()
        elif field.endswith("_analysis_has_cpp_vtable"):
            data = binary.read_bytes()
            if data.startswith(b"MZ"):
                present = b"_ZTV" in data or b"vtable for" in data
            else:
                present = any(
                    name.startswith("_ZTV") or "vtable for" in name
                    for name in cached_symbols(binary)
                )
            value = str(present).lower()
        elif field.endswith("_analysis_mangled_score_symbol"):
            candidates = [
                name for name in cached_symbols(binary)
                if "score" in name.lower()
            ]
            value = candidates[0] if candidates else "none"
            if candidates and binary.read_bytes().startswith(b"MZ"):
                value = (
                    pe_section_symbol(binary, ".text", candidates[0])
                    or value
                )
        elif field.endswith("_analysis_vtable_symbol"):
            names = cached_symbols(binary)
            candidates = [
                name for name in names
                if name.startswith("_ZTV") or "vtable for" in name
            ]
            class_candidates = [
                name for name in candidates if "__cxxabiv1" not in name
            ]
            if class_candidates:
                candidates = class_candidates
            value = candidates[0] if candidates else "none"
            if candidates and binary.read_bytes().startswith(b"MZ"):
                value = (
                    pe_section_symbol(binary, ".rdata", candidates[0])
                    or value
                )
        elif field.endswith("_analysis_typeinfo_symbol"):
            names = cached_symbols(binary)
            score = next((name for name in names if "score" in name.lower()), "")
            class_match = re.match(r"_ZNK?(\d+)", score)
            if class_match:
                class_length = int(class_match.group(1))
                class_start = class_match.end()
                class_name = score[class_start:class_start + class_length]
            else:
                class_name = ""
            expected = f"_ZTI{len(class_name)}{class_name}" if class_name else ""
            if expected in names:
                value = expected
                if binary.read_bytes().startswith(b"MZ"):
                    value = pe_section_symbol(binary, ".rdata", expected) or value
            else:
                candidates = [
                    name for name in names
                    if re.match(r"_ZTI\d+", name)
                    and (not class_name or class_name in name)
                ]
                if not candidates:
                    candidates = [
                        name for name in names if re.match(r"_ZTI\d+", name)
                    ]
                value = candidates[0] if candidates else "none"
        elif field.endswith("_analysis_has_go_runtime"):
            data = binary.read_bytes()
            if day == "d04":
                present = b"runtime.main" in data
            else:
                sections = (
                    " ".join(pe_section_names(binary)).lower()
                    if data.startswith(b"MZ")
                    else elf_sections(binary).lower()
                )
                names = cached_symbols(binary)
                present = (
                    ".gopclntab" in sections
                    or ".go.buildinfo" in sections
                    or b"Go build ID:" in data
                    or b"runtime." in data
                    or any(name.startswith("runtime.") for name in names)
                )
            value = str(present).lower()
        elif field.endswith("_analysis_has_rust_mangled_symbol"):
            names = cached_symbols(binary)
            present = any(
                name.startswith("_R")
                or (
                    name.startswith("_ZN")
                    and re.search(r"\d+h[0-9a-fA-F]{8,}E?$", name)
                )
                for name in names
            )
            value = str(present).lower()
        else:
            raise ValueError(f"No answer handler for {answer_id}")
        answers[answer_id] = value
    return answers


def build_all_answers(
    response: dict,
    extracted: Path,
    skip_suffixes: tuple[str, ...] = (),
) -> dict[str, str]:
    """Handle either a single evidence set or numbered Mastery sets."""
    questions = [
        question for question in response["questions"]
        if not any(
            question["id"].lower().endswith(suffix.lower())
            for suffix in skip_suffixes
        )
    ]
    sets = sorted(
        {
            int(match.group(1))
            for question in questions
            if (match := re.match(r"set(\d+)\.", question["id"], re.I))
        }
    )
    if not sets:
        return build_answers(
            {"questions": questions},
            extracted,
            skip_suffixes,
        )

    answers: dict[str, str] = {}
    for number in sets:
        prefix = f"set{number}."
        subset = [
            {**question, "id": question["id"][len(prefix):]}
            for question in questions
            if question["id"].startswith(prefix)
        ]
        set_dir = extracted / f"set{number}"
        if not set_dir.is_dir():
            set_dir = extracted
        candidates = build_answers(
            {"questions": subset},
            set_dir,
            skip_suffixes,
        )
        answers.update({prefix + key: value for key, value in candidates.items()})
    if len(answers) != len(questions):
        raise ValueError("Some current answer IDs were not mapped")
    return answers


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("extracted_dir", type=Path)
    parser.add_argument("--answer-map", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    response = json.loads(args.answer_map.read_text())
    answers = build_all_answers(response, args.extracted_dir)
    expected = set(response.get("answer_ids", []))
    if expected and set(answers) != expected:
        raise ValueError("Candidate answer IDs do not match the live response")
    rendered = json.dumps(answers, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered)
        print(f"Wrote {len(answers)} candidates to {args.output}")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
