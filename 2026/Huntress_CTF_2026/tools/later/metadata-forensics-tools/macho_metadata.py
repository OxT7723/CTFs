#!/usr/bin/env python3
"""Read CPU types from thin, universal, and ar-archived Mach-O files."""
from __future__ import annotations

import struct


_THIN_MAGICS = {
    b"\xce\xfa\xed\xfe": "<",  # MH_MAGIC, little endian
    b"\xfe\xed\xfa\xce": ">",  # MH_CIGAM, big endian
    b"\xcf\xfa\xed\xfe": "<",  # MH_MAGIC_64, little endian
    b"\xfe\xed\xfa\xcf": ">",  # MH_CIGAM_64, big endian
}
_FAT_MAGICS = {
    b"\xca\xfe\xba\xbe": (">", False),  # FAT_MAGIC
    b"\xbe\xba\xfe\xca": ("<", False),  # FAT_CIGAM
    b"\xca\xfe\xba\xbf": (">", True),  # FAT_MAGIC_64
    b"\xbf\xba\xfe\xca": ("<", True),  # FAT_CIGAM_64
}
def _cpu_name(cpu_type: int) -> str:
    return f"0x{cpu_type:08x}"


def _archive_members(data: bytes) -> list[bytes]:
    """Extract ordinary ar members, including GNU and BSD long names."""
    if not data.startswith(b"!<arch>\n"):
        return []
    members: list[bytes] = []
    cursor = 8
    string_table = b""
    while cursor + 60 <= len(data):
        header = data[cursor:cursor + 60]
        if header[58:60] != b"`\n":
            raise ValueError("Invalid ar member header")
        try:
            size = int(header[48:58].decode("ascii").strip())
        except ValueError as error:
            raise ValueError("Invalid ar member size") from error
        start, end = cursor + 60, cursor + 60 + size
        if end > len(data):
            raise ValueError("Truncated ar member")
        name = header[:16].decode("ascii", errors="replace").strip()
        payload = data[start:end]
        if name == "//":
            string_table = payload
        elif name.startswith("#1/"):
            name_size = int(name[3:])
            if name_size > len(payload):
                raise ValueError("Truncated BSD ar member name")
            payload = payload[name_size:]
            members.append(payload)
        elif name.startswith("/") and name[1:].isdigit() and string_table:
            offset = int(name[1:])
            name_end = string_table.find(b"/\n", offset)
            if name_end < 0:
                name_end = string_table.find(b"\0", offset)
            resolved_name = string_table[offset:name_end].decode(
                "utf-8", errors="replace"
            )
            if resolved_name and not resolved_name.startswith("__.SYMDEF"):
                members.append(payload)
        elif name not in {"/", "/SYM64", "//"} and not name.startswith("__.SYMDEF"):
            members.append(payload)
        cursor = end + (size & 1)
    if cursor != len(data) and data[cursor:].strip(b"\0\n"):
        raise ValueError("Trailing data in ar archive")
    return members


def cpu_types(data: bytes) -> list[str]:
    """Return sorted distinct, zero-padded Mach-O CPU type hex values."""
    found: set[str] = set()

    def visit(blob: bytes) -> None:
        if len(blob) >= 8 and blob[:4] in _THIN_MAGICS:
            endian = _THIN_MAGICS[blob[:4]]
            found.add(_cpu_name(struct.unpack_from(endian + "I", blob, 4)[0]))
            return
        if len(blob) >= 8 and blob[:4] in _FAT_MAGICS:
            endian, is_64 = _FAT_MAGICS[blob[:4]]
            count = struct.unpack_from(endian + "I", blob, 4)[0]
            entry_size = 32 if is_64 else 20
            if count > (len(blob) - 8) // entry_size:
                raise ValueError("Truncated universal Mach-O architecture table")
            for index in range(count):
                entry = 8 + index * entry_size
                cpu_type = struct.unpack_from(endian + "I", blob, entry)[0]
                offset = struct.unpack_from(
                    endian + ("Q" if is_64 else "I"), blob, entry + 8
                )[0]
                size_offset = entry + (16 if is_64 else 12)
                size = struct.unpack_from(
                    endian + ("Q" if is_64 else "I"), blob, size_offset
                )[0]
                if offset + size > len(blob):
                    raise ValueError("Universal Mach-O slice is outside the file")
                # The fat header is authoritative for each slice's CPU type.
                found.add(_cpu_name(cpu_type))
            return
        if blob.startswith(b"!<arch>\n"):
            for member in _archive_members(blob):
                visit(member)

    visit(data)
    return sorted(found)
