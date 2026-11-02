#!/usr/bin/env python3
"""Read SQLite database header fields directly from assigned database bytes."""
from __future__ import annotations

import struct


HEADER_SIZE = 100
MAGIC = b"SQLite format 3\x00"


def inspect_sqlite(data: bytes) -> dict[str, int]:
    """Return standard SQLite database-header fields with normalized values."""
    if len(data) < HEADER_SIZE or data[:16] != MAGIC:
        raise ValueError("Input is not a complete SQLite 3 database header")

    encoded_page_size = struct.unpack_from(">H", data, 16)[0]
    page_size = 65536 if encoded_page_size == 1 else encoded_page_size
    if page_size < 512 or page_size > 65536 or page_size & (page_size - 1):
        raise ValueError(f"Invalid SQLite page size: {page_size}")

    return {
        "page_size_bytes": page_size,
        "write_version": data[18],
        "read_version": data[19],
        "reserved_bytes_per_page": data[20],
        "max_embedded_payload_fraction": data[21],
        "min_embedded_payload_fraction": data[22],
        "leaf_payload_fraction": data[23],
        "file_change_counter": struct.unpack_from(">I", data, 24)[0],
        "database_size_pages": struct.unpack_from(">I", data, 28)[0],
        "first_freelist_trunk_page": struct.unpack_from(">I", data, 32)[0],
        "total_freelist_pages": struct.unpack_from(">I", data, 36)[0],
        "schema_cookie": struct.unpack_from(">I", data, 40)[0],
        "schema_format": struct.unpack_from(">I", data, 44)[0],
        "default_page_cache_size": struct.unpack_from(">i", data, 48)[0],
        "largest_root_page": struct.unpack_from(">I", data, 52)[0],
        "text_encoding": struct.unpack_from(">I", data, 56)[0],
        "user_version": struct.unpack_from(">I", data, 60)[0],
        "incremental_vacuum_mode": struct.unpack_from(">I", data, 64)[0],
        "application_id": struct.unpack_from(">I", data, 68)[0],
        "version_valid_for": struct.unpack_from(">I", data, 92)[0],
        "sqlite_version_number": struct.unpack_from(">I", data, 96)[0],
    }
