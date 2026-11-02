#!/usr/bin/env python3
"""Read root-key metadata from a Windows Registry hive."""
from __future__ import annotations

import struct


BASE_BLOCK_SIZE = 0x1000
ROOT_CELL_OFFSET = 0x24
NK_NAME_LENGTH_OFFSET = 0x48
NK_NAME_OFFSET = 0x4C
KEY_COMP_NAME = 0x20


def hive_root_name(data: bytes) -> str:
    """Return the name of the root NK cell in a REGF hive."""
    if len(data) < BASE_BLOCK_SIZE + 8 or data[:4] != b"regf":
        raise ValueError("Input is not a complete Windows Registry hive")

    root_relative_offset = struct.unpack_from("<I", data, ROOT_CELL_OFFSET)[0]
    cell_offset = BASE_BLOCK_SIZE + root_relative_offset
    nk_offset = cell_offset + 4  # Skip the signed cell-size field.
    if nk_offset + NK_NAME_OFFSET > len(data):
        raise ValueError("Registry root cell is outside the hive")
    if data[nk_offset:nk_offset + 2] != b"nk":
        raise ValueError("Registry root cell is not a key node")

    flags = struct.unpack_from("<H", data, nk_offset + 2)[0]
    name_length = struct.unpack_from("<H", data, nk_offset + NK_NAME_LENGTH_OFFSET)[0]
    name_start = nk_offset + NK_NAME_OFFSET
    name_end = name_start + name_length
    if name_end > len(data):
        raise ValueError("Registry root key name is truncated")
    encoding = "latin-1" if flags & KEY_COMP_NAME else "utf-16le"
    return data[name_start:name_end].decode(encoding)
