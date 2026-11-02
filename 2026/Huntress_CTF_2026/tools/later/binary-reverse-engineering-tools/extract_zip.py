#!/usr/bin/env python3
"""Safely extract a ZIP archive, including event-provided AES ZIP files."""

from __future__ import annotations

import argparse
import io
import json
import zipfile
from pathlib import Path, PurePosixPath


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--password", default="infected")
    args = parser.parse_args()

    import pyzipper

    args.destination.mkdir(parents=True, exist_ok=True)
    names = []
    with pyzipper.AESZipFile(args.archive) as archive:
        archive.setpassword(args.password.encode())
        for info in archive.infolist():
            member = PurePosixPath(info.filename)
            if member.is_absolute() or ".." in member.parts:
                raise ValueError(f"Unsafe archive path: {info.filename!r}")
            output = (args.destination / Path(*member.parts)).resolve()
            if args.destination.resolve() not in output.parents and output != args.destination.resolve():
                raise ValueError(f"Archive path escapes destination: {info.filename!r}")
            if info.is_dir():
                output.mkdir(parents=True, exist_ok=True)
            else:
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_bytes(archive.read(info))
                names.append(info.filename)
    (args.destination / ".archive-members.json").write_text(
        json.dumps(names, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
