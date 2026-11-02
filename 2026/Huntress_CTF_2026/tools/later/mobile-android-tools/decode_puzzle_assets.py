#!/usr/bin/env python3
"""Decode puzzle assets stored in an APK, including referenced secondary DEX files."""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import re
import struct
import subprocess
import tempfile
import zipfile
import zlib
from posixpath import normpath
from pathlib import Path


def dex_strings(data: bytes, verify_integrity: bool = True) -> list[str]:
    """Read the DEX string table without loading or executing the bytecode."""
    if len(data) < 0x70 or not re.fullmatch(rb"dex\n[0-9]{3}\x00", data[:8]):
        raise ValueError("Dynamic asset is not a supported DEX file")
    if struct.unpack_from("<I", data, 0x20)[0] != len(data):
        raise ValueError("DEX file size does not match its header")
    if verify_integrity:
        if data[0x0C:0x20] != hashlib.sha1(data[0x20:]).digest():
            raise ValueError("DEX SHA-1 integrity check failed")
        checksum = struct.unpack_from("<I", data, 0x08)[0]
        if checksum != (zlib.adler32(data[0x0C:]) & 0xFFFFFFFF):
            raise ValueError("DEX Adler-32 integrity check failed")

    count, offset = struct.unpack_from("<II", data, 0x38)
    if offset < 0x70 or offset + count * 4 > len(data):
        raise ValueError("DEX string table is outside the file")

    values = []
    for index in range(count):
        position = struct.unpack_from("<I", data, offset + index * 4)[0]
        if position >= len(data):
            raise ValueError("DEX string data is outside the file")
        cursor = position
        while cursor < len(data) and data[cursor] & 0x80:
            cursor += 1
        if cursor >= len(data):
            raise ValueError("Invalid DEX string length")
        cursor += 1
        end = data.find(b"\x00", cursor)
        if end < 0:
            raise ValueError("Unterminated DEX string")
        values.append(data[cursor:end].decode("utf-8", errors="replace"))
    return values


def decode_asset(
    payload: dict,
    asset_reader=None,
    verify_dex_integrity: bool = True,
) -> bytes:
    codec = str(payload.get("codec", "")).lower()
    if codec == "plain":
        return str(payload["data"]).encode("utf-8")
    if codec == "reflection":
        return str(payload["data"]).encode("utf-8")
    if codec == "dynamic":
        if asset_reader is None:
            raise ValueError("Dynamic DEX assets require an APK asset reader")
        member = normpath(str(payload["data"]))
        if member.startswith("../") or member.startswith("/"):
            raise ValueError("Dynamic asset path must stay inside the APK")
        return "\n".join(
            dex_strings(
                asset_reader(member), verify_integrity=verify_dex_integrity
            )
        ).encode("utf-8")
    if codec == "split":
        parts = payload["parts"]
        order = payload["order"]
        if (
            not isinstance(parts, list)
            or not isinstance(order, list)
            or len(parts) != len(order)
            or sorted(order) != list(range(len(parts)))
        ):
            raise ValueError("Split asset must provide a permutation matching its parts")
        ordered = [""] * len(parts)
        for part, position in zip(parts, order):
            ordered[position] = str(part)
        return "".join(ordered).encode("utf-8")
    if codec == "indexed":
        data = str(payload["data"])
        order = payload["order"]
        if (
            not isinstance(order, list)
            or len(data) != len(order)
            or sorted(order) != list(range(len(data)))
        ):
            raise ValueError("Indexed asset must provide a permutation matching its data")
        ordered = [""] * len(data)
        for char, position in zip(data, order):
            ordered[position] = char
        return "".join(ordered).encode("utf-8")
    if codec == "hex":
        return bytes.fromhex(payload["data"])
    if codec == "packet":
        packet = bytes.fromhex(payload["data"])
        if len(packet) < 3 or packet[:2] != b"HA":
            raise ValueError("Packet asset must start with the HA framing marker")
        payload_length = packet[2]
        payload_end = 3 + payload_length
        if payload_end > len(packet):
            raise ValueError("Packet payload length exceeds the available bytes")
        return packet[3:payload_end]
    if codec == "caesar":
        key = payload["key"]
        if isinstance(key, str):
            key = int(key, 0)
        if not 0 <= key <= 255:
            raise ValueError("Caesar key must be in the range 0..255")
        return bytes((value - key) % 256 for value in payload["data"].encode("latin-1"))
    if codec == "table":
        encoded = bytes.fromhex(payload["data"])
        key = payload["key"]
        if isinstance(key, str):
            key = int(key, 0)
        if not isinstance(key, int) or not 0 <= key <= 255:
            raise ValueError("Table key must be in the range 0..255")
        step = payload.get("step", 3)
        if isinstance(step, str):
            step = int(step, 0)
        if not isinstance(step, int):
            raise ValueError("Table step must be an integer")
        return bytes(
            (value - key - index * step) % 256
            for index, value in enumerate(encoded)
        )
    if codec == "reverse":
        return str(payload["data"])[::-1].encode("utf-8")
    data = base64.b64decode(payload["data"], validate=True)
    if codec == "base64":
        return data
    if codec == "xor":
        key = payload["key"]
        if isinstance(key, str):
            key = int(key, 0)
        if not 0 <= key <= 255:
            raise ValueError("Single-byte XOR key must be in the range 0..255")
        return bytes(byte ^ key for byte in data)
    if codec == "layered":
        key = payload["key"]
        if isinstance(key, str):
            key = int(key, 0)
        if not isinstance(key, int) or not 0 <= key <= 255:
            raise ValueError("Layered XOR key must be in the range 0..255")
        decoded = bytes(
            byte ^ ((key + index) & 0xFF)
            for index, byte in enumerate(data)
        )
        return decoded[::-1]
    raise ValueError(f"Unsupported puzzle asset codec: {codec!r}")


def decoded_json_assets(
    apk: Path,
    split_assets: dict[str, bytes] | None = None,
    verify_dex_integrity: bool = True,
) -> list[tuple[str, bytes]]:
    decoded_assets = []
    with zipfile.ZipFile(apk) as archive:
        for member in archive.infolist():
            if member.is_dir() or not member.filename.lower().endswith(".json"):
                continue
            try:
                payload = json.loads(archive.read(member))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            if (
                isinstance(payload, dict)
                and "codec" in payload
                and ("data" in payload or str(payload["codec"]).lower() == "analysis")
            ):
                try:
                    if str(payload.get("codec", "")).lower() == "analysis":
                        from solve_analysis_codec import analysis_answer

                        decoded_assets.append(
                            (
                                member.filename,
                                analysis_answer(
                                    apk,
                                    split_assets,
                                    verify_dex_integrity=verify_dex_integrity,
                                ),
                            )
                        )
                        continue
                    decoded_assets.append((
                        member.filename,
                        decode_asset(
                            payload,
                            asset_reader=archive.read,
                            verify_dex_integrity=verify_dex_integrity,
                        ),
                    ))
                except (KeyError, TypeError, ValueError):
                    continue
    return decoded_assets


def decoded_android_assets(
    package: Path, verify_dex_integrity: bool = True
) -> list[tuple[str, bytes]]:
    """Decode a standalone APK or an APK-set bundle, including split fragments."""
    with zipfile.ZipFile(package) as container:
        apk_members = [
            member for member in container.infolist()
            if not member.is_dir() and member.filename.lower().endswith(".apk")
        ]
        if not apk_members:
            return decoded_json_assets(
                package, verify_dex_integrity=verify_dex_integrity
            ) + native_library_strings(package)

        decoded = []
        bases: dict[str, list[bytes]] = {}
        fragments: dict[str, list[tuple[int, bytes]]] = {}
        split_assets = {}
        for member in apk_members:
            with zipfile.ZipFile(io.BytesIO(container.read(member))) as apk:
                for asset in apk.infolist():
                    if not asset.is_dir() and asset.filename.startswith("assets/"):
                        split_assets.setdefault(
                            asset.filename.removeprefix("assets/"), apk.read(asset)
                        )
        with tempfile.TemporaryDirectory() as temp_dir:
            for index, member in enumerate(apk_members):
                apk_path = Path(temp_dir) / f"split-{index}.apk"
                apk_path.write_bytes(container.read(member))
                decoded.extend(
                    (f"{member.filename}:{name}", value)
                    for name, value in decoded_json_assets(
                        apk_path,
                        split_assets,
                        verify_dex_integrity=verify_dex_integrity,
                    )
                )
                decoded.extend(
                    (f"{member.filename}:{name}", value)
                    for name, value in native_library_strings(apk_path)
                )

                with zipfile.ZipFile(apk_path) as apk:
                    for asset in apk.infolist():
                        if asset.is_dir() or not asset.filename.lower().endswith(".json"):
                            continue
                        try:
                            payload = json.loads(apk.read(asset))
                        except (UnicodeDecodeError, json.JSONDecodeError):
                            continue
                        if not isinstance(payload, dict) or str(
                            payload.get("codec", "")
                        ).lower() != "split":
                            continue
                        day = str(payload.get("day", ""))
                        if "parts" in payload and "order" in payload:
                            try:
                                bases.setdefault(day, []).append(
                                    decode_asset(
                                        payload,
                                        asset_reader=apk.read,
                                        verify_dex_integrity=verify_dex_integrity,
                                    )
                                )
                            except (KeyError, TypeError, ValueError):
                                continue
                        elif "part" in payload and isinstance(
                            payload.get("part_index"), int
                        ):
                            fragments.setdefault(day, []).append(
                                (
                                    payload["part_index"],
                                    str(payload["part"]).encode("utf-8"),
                                )
                            )

        for day, base_values in bases.items():
            indexed_fragments = sorted(fragments.get(day, []), key=lambda item: item[0])
            if indexed_fragments:
                for index, base in enumerate(base_values):
                    joined = base + b"".join(value for _, value in indexed_fragments)
                    decoded.append((f"split-bundle:day-{day}:assembled-{index}", joined))
        return decoded


def native_library_strings(apk: Path) -> list[tuple[str, bytes]]:
    """Collect printable strings from shared libraries exporting a secret getter.

    APK libraries are inspected as data; they are never loaded or executed.
    The mode runner applies the live question's answer format to these strings.
    """
    results = []
    with zipfile.ZipFile(apk) as archive, tempfile.TemporaryDirectory() as temp_dir:
        for index, member in enumerate(archive.infolist()):
            if member.is_dir() or not member.filename.lower().endswith(".so"):
                continue
            library_path = Path(temp_dir) / f"library-{index}.so"
            library_path.write_bytes(archive.read(member))
            try:
                symbols = subprocess.run(
                    ["nm", "-D", "--defined-only", str(library_path)],
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
            except (OSError, subprocess.TimeoutExpired):
                continue
            if symbols.returncode:
                continue
            exported_names = [
                fields[-1]
                for line in symbols.stdout.splitlines()
                if (fields := line.split())
            ]
            if not any(re.search(r"(?:secret|proof)$", name, re.I) for name in exported_names):
                continue
            raw = library_path.read_bytes()
            for match in re.finditer(rb"[ -~]{4,}", raw):
                results.append((member.filename, match.group(0)))
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("apk", type=Path)
    args = parser.parse_args()

    decoded_assets = decoded_json_assets(args.apk)
    native_strings = native_library_strings(args.apk)
    for name, decoded in decoded_assets:
        print(f"--- {name} ---")
        try:
            print(decoded.decode("utf-8"))
        except UnicodeDecodeError:
            print(decoded.hex())
    for name, value in native_strings:
        print(f"--- {name} (static strings) ---")
        print(value.decode("ascii", errors="replace"))
    if not decoded_assets and not native_strings:
        raise SystemExit("No supported encoded assets or native secret libraries found")


if __name__ == "__main__":
    main()
