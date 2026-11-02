#!/usr/bin/env python3
"""Read architecture fields directly from ELF identification and header bytes."""
from __future__ import annotations

import struct


def inspect_elf(data: bytes) -> dict[str, object]:
    if len(data) < 20 or data[:4] != b"\x7fELF":
        raise ValueError("Input is not a complete ELF header")

    elf_class = data[4]
    byte_order = data[5]
    if elf_class not in (1, 2):
        raise ValueError(f"Unsupported ELF class: {elf_class}")
    if byte_order not in (1, 2):
        raise ValueError(f"Unsupported ELF byte order: {byte_order}")
    if data[6] != 1:
        raise ValueError(f"Unsupported ELF identification version: {data[6]}")

    endian = "<" if byte_order == 1 else ">"
    machine = struct.unpack_from(endian + "H", data, 18)[0]
    return {
        "class": "ELF32" if elf_class == 1 else "ELF64",
        "byte_order": "little" if byte_order == 1 else "big",
        "machine": machine,
        "machine_hex": f"0x{machine:04x}",
    }
