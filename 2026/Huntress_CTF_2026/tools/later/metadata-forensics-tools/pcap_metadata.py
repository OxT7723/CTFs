#!/usr/bin/env python3
"""Read packet-record counts from classic PCAP captures."""
from __future__ import annotations

import struct


MAGIC = {
    b"\xd4\xc3\xb2\xa1": "<",  # little-endian, microsecond timestamps
    b"\xa1\xb2\xc3\xd4": ">",  # big-endian, microsecond timestamps
    b"\x4d\x3c\xb2\xa1": "<",  # little-endian, nanosecond timestamps
    b"\xa1\xb2\x3c\x4d": ">",  # big-endian, nanosecond timestamps
}


def packet_count(data: bytes) -> int:
    """Count complete PCAP record headers and payloads.

    A record with ``captured_length < original_length`` is still a packet:
    snap-length truncation is valid PCAP data. Structurally malformed or
    truncated records are rejected instead of silently counted.
    """
    if len(data) < 24:
        raise ValueError("PCAP global header is truncated")
    endian = MAGIC.get(data[:4])
    if endian is None:
        raise ValueError("Input does not have a supported classic PCAP magic value")

    major, minor, _zone, _accuracy, snap_length, _network = struct.unpack_from(
        endian + "HHIIII", data, 4
    )
    if major != 2 or minor not in (2, 3, 4):
        raise ValueError(f"Unsupported PCAP version {major}.{minor}")

    offset = 24
    count = 0
    while offset < len(data):
        if len(data) - offset < 16:
            raise ValueError(f"Truncated PCAP record header at offset {offset}")
        _seconds, _fraction, captured_length, original_length = struct.unpack_from(
            endian + "IIII", data, offset
        )
        if captured_length > original_length:
            raise ValueError(
                f"PCAP captured length exceeds original length at offset {offset}"
            )
        if snap_length and captured_length > snap_length:
            raise ValueError(
                f"PCAP captured length exceeds snap length at offset {offset}"
            )
        offset += 16
        if captured_length > len(data) - offset:
            raise ValueError(f"Truncated PCAP packet data at offset {offset}")
        offset += captured_length
        count += 1
    return count
