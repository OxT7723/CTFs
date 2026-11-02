#!/usr/bin/env python3
"""Read selected portable executable fields directly from PE bytes."""
from __future__ import annotations

import argparse
import json
import struct
import uuid
from pathlib import Path


def inspect_version_info(data: bytes) -> dict[str, str]:
    """Read string values from a PE VERSIONINFO resource."""
    try:
        import pefile
    except ImportError as error:
        raise RuntimeError(
            "PE VERSIONINFO parsing requires pefile; install "
            "metadata-forensics-tools/requirements.txt"
        ) from error

    image = pefile.PE(data=data, fast_load=True)
    image.parse_data_directories(
        directories=[pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_RESOURCE"]]
    )
    result: dict[str, str] = {}
    for group in image.FileInfo or []:
        for entry in group:
            for table in getattr(entry, "StringTable", []) or []:
                for raw_key, raw_value in table.entries.items():
                    key = raw_key.decode("utf-8", errors="replace")
                    value = raw_value.decode("utf-8", errors="replace")
                    result.setdefault(key, value)
    return result


def inspect_pe(data: bytes) -> dict[str, object]:
    if len(data) < 0x40 or data[:2] != b"MZ":
        raise ValueError("Input is not a PE image")
    pe_offset = struct.unpack_from("<I", data, 0x3C)[0]
    if pe_offset + 24 > len(data) or data[pe_offset:pe_offset + 4] != b"PE\0\0":
        raise ValueError("PE signature is missing or truncated")
    machine, section_count = struct.unpack_from("<HH", data, pe_offset + 4)
    optional_offset = pe_offset + 24
    optional_magic = struct.unpack_from("<H", data, optional_offset)[0]
    if optional_magic not in (0x10B, 0x20B):
        raise ValueError(f"Unsupported PE optional header: 0x{optional_magic:04x}")
    if optional_offset + 20 > len(data):
        raise ValueError("PE optional header is truncated")
    entry_rva = struct.unpack_from("<I", data, optional_offset + 16)[0]
    image_base_offset = optional_offset + (28 if optional_magic == 0x10B else 24)
    image_base_format = "<I" if optional_magic == 0x10B else "<Q"
    image_base = struct.unpack_from(image_base_format, data, image_base_offset)[0]
    return {
        "machine": machine,
        "section_count": section_count,
        "optional_header": "PE32" if optional_magic == 0x10B else "PE32+",
        "address_of_entry_point_rva_hex": f"0x{entry_rva:08x}",
        "image_base_hex": hex(image_base),
    }


def inspect_dotnet_mvid(data: bytes) -> str:
    """Read the Module table MVID from a managed PE image."""
    if len(data) < 0x40 or data[:2] != b"MZ":
        raise ValueError("Input is not a PE image")
    pe_offset = struct.unpack_from("<I", data, 0x3C)[0]
    if pe_offset + 24 > len(data) or data[pe_offset:pe_offset + 4] != b"PE\0\0":
        raise ValueError("PE signature is missing or truncated")

    section_count = struct.unpack_from("<H", data, pe_offset + 6)[0]
    optional_size = struct.unpack_from("<H", data, pe_offset + 20)[0]
    optional = pe_offset + 24
    magic = struct.unpack_from("<H", data, optional)[0]
    if magic not in (0x10B, 0x20B):
        raise ValueError(f"Unsupported PE optional header: 0x{magic:04x}")
    directories = optional + (96 if magic == 0x10B else 112)
    cli_rva = struct.unpack_from("<I", data, directories + 14 * 8)[0]
    if not cli_rva:
        raise ValueError("PE image has no CLR header")

    section_table = optional + optional_size
    sections = []
    for index in range(section_count):
        entry = section_table + 40 * index
        virtual_size, virtual_address, raw_size, raw_offset = struct.unpack_from(
            "<IIII", data, entry + 8
        )
        sections.append((virtual_address, max(virtual_size, raw_size), raw_offset))

    def rva_to_offset(rva: int) -> int:
        for virtual_address, size, raw_offset in sections:
            if virtual_address <= rva < virtual_address + size:
                return raw_offset + rva - virtual_address
        if rva < section_table:
            return rva
        raise ValueError(f"Could not map PE RVA 0x{rva:x}")

    cli_offset = rva_to_offset(cli_rva)
    metadata_rva = struct.unpack_from("<I", data, cli_offset + 8)[0]
    root = rva_to_offset(metadata_rva)
    if data[root:root + 4] != b"BSJB":
        raise ValueError("CLR metadata signature is missing")

    version_length = struct.unpack_from("<I", data, root + 12)[0]
    cursor = root + 16 + ((version_length + 3) & ~3)
    _, stream_count = struct.unpack_from("<HH", data, cursor)
    cursor += 4
    streams: dict[str, tuple[int, int]] = {}
    for _ in range(stream_count):
        relative_offset, size = struct.unpack_from("<II", data, cursor)
        cursor += 8
        end = data.index(b"\0", cursor)
        name = data[cursor:end].decode("ascii")
        cursor = (end + 4) & ~3
        streams[name] = (relative_offset, size)

    table_info = streams.get("#~") or streams.get("#-")
    guid_info = streams.get("#GUID")
    if not table_info or not guid_info:
        raise ValueError("CLR metadata is missing its tables or GUID heap")
    tables = root + table_info[0]
    heap_sizes = data[tables + 6]
    valid_tables = struct.unpack_from("<Q", data, tables + 8)[0]
    if not valid_tables & 1:
        raise ValueError("CLR metadata has no Module table")
    cursor = tables + 24
    for table_index in range(64):
        if valid_tables & (1 << table_index):
            cursor += 4
    string_index_size = 4 if heap_sizes & 0x01 else 2
    guid_index_size = 4 if heap_sizes & 0x02 else 2
    mvid_index_offset = cursor + 2 + string_index_size
    mvid_index = int.from_bytes(
        data[mvid_index_offset:mvid_index_offset + guid_index_size], "little"
    )
    if not mvid_index:
        raise ValueError("Module table has an empty MVID index")
    guid_offset = root + guid_info[0] + (mvid_index - 1) * 16
    if guid_offset + 16 > len(data):
        raise ValueError("Module MVID lies outside the GUID heap")
    return str(uuid.UUID(bytes_le=data[guid_offset:guid_offset + 16]))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pe_file", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--version-info",
        action="store_true",
        help="include string values from the PE VERSIONINFO resource",
    )
    args = parser.parse_args()
    result = inspect_pe(args.pe_file.read_bytes())
    if args.version_info:
        result["version_info"] = inspect_version_info(args.pe_file.read_bytes())
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
