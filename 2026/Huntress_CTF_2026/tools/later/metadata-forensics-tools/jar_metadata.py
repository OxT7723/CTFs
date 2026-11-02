#!/usr/bin/env python3
"""Read Java archive manifest metadata from JAR bytes."""
from __future__ import annotations

import io
from zipfile import BadZipFile, ZipFile


def manifest_attributes(data: bytes) -> dict[str, str]:
    """Return the main-section manifest attributes, with continuation lines joined."""
    try:
        with ZipFile(io.BytesIO(data)) as archive:
            manifest = archive.read("META-INF/MANIFEST.MF")
    except (BadZipFile, KeyError) as error:
        raise ValueError("JAR has no readable META-INF/MANIFEST.MF") from error

    text = manifest.decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
    main_section = text.split("\n\n", 1)[0]
    unfolded: list[str] = []
    for line in main_section.split("\n"):
        if line.startswith(" ") and unfolded:
            unfolded[-1] += line[1:]
        else:
            unfolded.append(line)

    attributes: dict[str, str] = {}
    for line in unfolded:
        if ": " not in line:
            continue
        name, value = line.split(": ", 1)
        attributes[name.casefold()] = value
    return attributes


def main_class(data: bytes) -> str:
    """Return the manifest Main-Class value, or 'none' when it is absent."""
    return manifest_attributes(data).get("main-class", "none")
