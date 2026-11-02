"""Read partition start LBAs from raw MBR and GPT disk images."""
from __future__ import annotations

import struct


SECTOR_SIZE = 512
GPT_SIGNATURE = b"EFI PART"
EXTENDED_PARTITION_TYPES = {0x05, 0x0F, 0x85}


def partition_start_lba_sequence(data: bytes) -> list[int]:
    """Return allocated partition starts in table order, excluding containers."""
    if len(data) < SECTOR_SIZE:
        raise ValueError("Disk image is shorter than one sector")

    if len(data) >= 2 * SECTOR_SIZE and data[SECTOR_SIZE:SECTOR_SIZE + 8] == GPT_SIGNATURE:
        return _gpt_partition_starts(data)
    return _mbr_partition_starts(data)


def _gpt_partition_starts(data: bytes) -> list[int]:
    header = data[SECTOR_SIZE:2 * SECTOR_SIZE]
    if len(header) < 92:
        raise ValueError("Truncated GPT header")

    entry_lba = struct.unpack_from("<Q", header, 72)[0]
    entry_count = struct.unpack_from("<I", header, 80)[0]
    entry_size = struct.unpack_from("<I", header, 84)[0]
    if entry_size < 48:
        raise ValueError(f"Invalid GPT partition entry size: {entry_size}")

    table_start = entry_lba * SECTOR_SIZE
    table_end = table_start + entry_count * entry_size
    if table_start > len(data) or table_end > len(data):
        raise ValueError("GPT partition table extends beyond the disk image")

    starts: list[int] = []
    for index in range(entry_count):
        offset = table_start + index * entry_size
        entry = data[offset:offset + entry_size]
        if entry[:16] != bytes(16):
            starts.append(struct.unpack_from("<Q", entry, 32)[0])
    return starts


def _mbr_partition_starts(data: bytes) -> list[int]:
    if len(data) < 512 or data[510:512] != b"\x55\xaa":
        raise ValueError("Disk image has neither a GPT header nor a valid MBR")

    entries = [data[446 + index * 16:462 + index * 16] for index in range(4)]
    if any(entry[4] == 0xEE for entry in entries):
        raise ValueError("Protective MBR found without a readable GPT header")

    starts: list[int] = []
    extended_bases: list[int] = []
    for entry in entries:
        partition_type = entry[4]
        start_lba = struct.unpack_from("<I", entry, 8)[0]
        if not partition_type or not start_lba:
            continue
        if partition_type in EXTENDED_PARTITION_TYPES:
            extended_bases.append(start_lba)
        else:
            starts.append(start_lba)

    for base_lba in extended_bases:
        ebr_lba = base_lba
        visited: set[int] = set()
        while ebr_lba and ebr_lba not in visited:
            visited.add(ebr_lba)
            offset = ebr_lba * SECTOR_SIZE
            ebr = data[offset:offset + SECTOR_SIZE]
            if len(ebr) != SECTOR_SIZE or ebr[510:512] != b"\x55\xaa":
                break
            first = ebr[446:462]
            first_type = first[4]
            relative_start = struct.unpack_from("<I", first, 8)[0]
            if first_type and relative_start:
                starts.append(ebr_lba + relative_start)

            link = ebr[462:478]
            link_type = link[4]
            link_start = struct.unpack_from("<I", link, 8)[0]
            if link_type not in EXTENDED_PARTITION_TYPES or not link_start:
                break
            ebr_lba = base_lba + link_start

    return starts
