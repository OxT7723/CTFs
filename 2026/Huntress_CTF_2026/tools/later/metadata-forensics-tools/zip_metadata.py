#!/usr/bin/env python3
"""Read ZIP directory metadata from the raw archive bytes."""
from __future__ import annotations

import io
import struct
from zipfile import ZipFile


EOCD_SIGNATURE = b"PK\x05\x06"
ZIP64_LOCATOR_SIGNATURE = b"PK\x06\x07"
ZIP64_EOCD_SIGNATURE = b"PK\x06\x06"


def inspect_zip(data: bytes) -> dict[str, object]:
    """Return the EOCD fields and central-directory names for a ZIP archive."""
    eocd_offset = data.rfind(EOCD_SIGNATURE)
    if eocd_offset < 0 or eocd_offset + 22 > len(data):
        raise ValueError("ZIP End of Central Directory record is missing or truncated")

    (
        disk_number,
        central_directory_disk,
        entries_on_disk,
        total_entries,
        central_directory_size,
        central_directory_offset,
        comment_length,
    ) = struct.unpack_from("<HHHHIIH", data, eocd_offset + 4)
    comment_start = eocd_offset + 22
    if comment_start + comment_length > len(data):
        raise ValueError("ZIP End of Central Directory comment is truncated")

    values: dict[str, object] = {
        "eocd_offset": eocd_offset,
        "eocd_disk_number": disk_number,
        "eocd_central_directory_disk": central_directory_disk,
        "eocd_entries_on_disk": entries_on_disk,
        "eocd_total_entries": total_entries,
        "eocd_central_directory_size": central_directory_size,
        "eocd_central_directory_offset": central_directory_offset,
        "eocd_comment_length": comment_length,
        "central_directory_member_names": [],
    }

    # The classic EOCD saturates fields at their maximum when ZIP64 is used.
    locator_offset = eocd_offset - 20
    if (
        total_entries == 0xFFFF
        or entries_on_disk == 0xFFFF
        or central_directory_size == 0xFFFFFFFF
        or central_directory_offset == 0xFFFFFFFF
    ) and data[locator_offset:locator_offset + 4] == ZIP64_LOCATOR_SIGNATURE:
        _, zip64_disk, zip64_offset, _ = struct.unpack_from(
            "<I IQI".replace(" ", ""), data, locator_offset
        )
        if data[zip64_offset:zip64_offset + 4] != ZIP64_EOCD_SIGNATURE:
            raise ValueError("ZIP64 End of Central Directory record is missing")
        (
            _record_size,
            _made_by,
            _needed,
            _disk,
            _cd_disk,
            zip64_entries_on_disk,
            zip64_total_entries,
            zip64_cd_size,
            zip64_cd_offset,
        ) = struct.unpack_from("<QHHIIQQQQ", data, zip64_offset + 4)
        values.update({
            "zip64_eocd_entries_on_disk": zip64_entries_on_disk,
            "zip64_eocd_total_entries": zip64_total_entries,
            "zip64_eocd_central_directory_size": zip64_cd_size,
            "zip64_eocd_central_directory_offset": zip64_cd_offset,
        })
        if entries_on_disk == 0xFFFF:
            values["eocd_entries_on_disk"] = zip64_entries_on_disk
        if total_entries == 0xFFFF:
            values["eocd_total_entries"] = zip64_total_entries
        if central_directory_size == 0xFFFFFFFF:
            values["eocd_central_directory_size"] = zip64_cd_size
        if central_directory_offset == 0xFFFFFFFF:
            values["eocd_central_directory_offset"] = zip64_cd_offset

    try:
        with ZipFile(io.BytesIO(data)) as archive:
            values["central_directory_member_names"] = sorted(archive.namelist())
            values["central_directory_member_count"] = len(archive.infolist())
    except Exception as error:
        values["central_directory_error"] = str(error)
    return values
