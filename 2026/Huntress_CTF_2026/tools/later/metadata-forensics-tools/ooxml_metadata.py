"""Readers for Open Packaging Convention and OOXML metadata."""
from __future__ import annotations

import io
import xml.etree.ElementTree as ET
from zipfile import BadZipFile, ZipFile


def external_relationship_targets(data: bytes) -> list[str]:
    """Return sorted external relationship targets from a DOCX package."""
    try:
        package = ZipFile(io.BytesIO(data))
    except BadZipFile as exc:
        raise ValueError("Input is not a valid OOXML ZIP package") from exc

    targets: list[str] = []
    with package:
        for item in package.infolist():
            if item.is_dir() or not item.filename.lower().endswith(".rels"):
                continue
            try:
                root = ET.fromstring(package.read(item))
            except ET.ParseError as exc:
                raise ValueError(f"Invalid relationship XML: {item.filename}") from exc

            for relationship in root.iter():
                if relationship.tag.rsplit("}", 1)[-1] != "Relationship":
                    continue
                if relationship.attrib.get("TargetMode", "").casefold() != "external":
                    continue
                target = relationship.attrib.get("Target")
                if target is not None:
                    targets.append(target)
    return sorted(targets)
