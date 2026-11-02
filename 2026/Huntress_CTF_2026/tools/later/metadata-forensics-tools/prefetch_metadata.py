#!/usr/bin/env python3
"""Read the executable identity from compressed or uncompressed Windows Prefetch data."""
from __future__ import annotations

import struct


def decompress_prefetch(data: bytes) -> bytes:
    """Unwrap a Windows MAM XPRESS-Huffman compressed Prefetch file when needed."""
    if not data.startswith(b"MAM"):
        return data
    if len(data) < 8 or data[3] != 4:
        raise ValueError("Unsupported or truncated Windows MAM compression header")

    expected_size = struct.unpack_from("<I", data, 4)[0]
    try:
        from dissect.util.compression.lzxpress_huffman import decompress
    except ImportError as error:
        raise RuntimeError(
            "Compressed Prefetch parsing requires dissect.util; install "
            "metadata-forensics-tools/requirements.txt"
        ) from error

    result = decompress(data[8:])
    if len(result) < expected_size:
        raise ValueError(
            f"Prefetch decompressed to {len(result)} bytes; expected {expected_size}"
        )
    # The XPRESS-Huffman decoder can emit a few bytes from the final padded
    # match. The MAM header gives the authoritative uncompressed byte length.
    return result[:expected_size]


def executable_name(data: bytes) -> str:
    """Return the executable name stored in the Prefetch file header."""
    data = decompress_prefetch(data)
    if len(data) < 0x88 or data[4:8] != b"SCCA":
        raise ValueError("Input is not a complete Windows Prefetch file")

    # Windows Prefetch versions store a fixed 60-character UTF-16LE name at
    # offset 0x10. Strip the terminating NUL and any trailing padding.
    raw_name = data[0x10:0x88]
    terminator = next(
        (
            offset
            for offset in range(0, len(raw_name) - 1, 2)
            if raw_name[offset:offset + 2] == b"\x00\x00"
        ),
        len(raw_name),
    )
    name = raw_name[:terminator].decode("utf-16le", errors="strict")
    if not name:
        raise ValueError("Prefetch executable name is empty")
    return name
