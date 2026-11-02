#!/usr/bin/env python3
"""Decode layered Base64, mixed-codec, Morse, hex, and Bacon-nibble blobs."""

from __future__ import annotations

import argparse
import base64
import binascii
import bz2
import codecs
import gzip
import html
import itertools
import lzma
import json
import re
import urllib.parse
import zlib
from pathlib import Path


_WHITESPACE_BYTES = re.compile(rb"\s+")
_WHITESPACE_TEXT = re.compile(r"\s+")
_BASE64_BYTES = re.compile(rb"[A-Za-z0-9_+/=-]+")
_BASE32_BYTES = re.compile(rb"[A-Za-z2-7=]+", re.IGNORECASE)
_ASCII85_BYTES = re.compile(rb"[!-u\s]+")
_HEX_BYTES = re.compile(rb"[0-9a-fA-F]+")
_PERCENT_BYTES = re.compile(rb"%[0-9a-fA-F]{2}")
_HEX_TEXT = re.compile(r"[0-9a-fA-F]+")
_BASE64_TEXT = re.compile(r"[A-Za-z0-9_+/=-]+")
_PERCENT_TEXT = re.compile(r"%[0-9a-fA-F]{2}")
_MIXED_ROW = re.compile(r"\s*(\d{1,2})\t(.*)")
_TERMINAL_SUFFIX = re.compile(rb"[a-z]+-\d{2}$")


MIXED_FRAGMENT_CODECS = {
    1: "base64",
    2: "rot13",
    3: "hex",
    4: "binary",
    5: "decimal",
    6: "octal",
    7: "percent",
    8: "html",
    9: "unicode",
    10: "base32",
    11: "base64url",
    12: "reverse",
    13: "atbash",
    14: "caesar",
    15: "rot47",
    16: "morse",
    17: "bacon",
}

MORSE = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E",
    "..-.": "F", "--.": "G", "....": "H", "..": "I", ".---": "J",
    "-.-": "K", ".-..": "L", "--": "M", "-.": "N", "---": "O",
    ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T",
    "..-": "U", "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y",
    "--..": "Z", "-----": "0", ".----": "1", "..---": "2",
    "...--": "3", "....-": "4", ".....": "5", "-....": "6",
    "--...": "7", "---..": "8", "----.": "9",
}


def decode_layer(data: bytes) -> bytes | None:
    compact = _WHITESPACE_BYTES.sub(b"", data)
    if not compact or _BASE64_BYTES.fullmatch(compact) is None:
        return None
    normalized = compact.replace(b"-", b"+").replace(b"_", b"/")
    normalized += b"=" * (-len(normalized) % 4)
    try:
        decoded = base64.b64decode(normalized, validate=True)
    except binascii.Error:
        return None
    if not decoded or decoded == data:
        return None
    return decoded


def decode_base32(data: bytes) -> bytes | None:
    """Decode a complete Base32 layer when it yields readable text or known binary."""
    compact = _WHITESPACE_BYTES.sub(b"", data)
    if not compact or _BASE32_BYTES.fullmatch(compact) is None:
        return None
    if compact != compact.upper():
        return None
    normalized = compact.upper()
    if b"=" in normalized.rstrip(b"="):
        return None
    unpadded_length = len(normalized.rstrip(b"="))
    if unpadded_length % 8 not in {0, 2, 4, 5, 7}:
        return None
    normalized += b"=" * (-len(normalized) % 8)
    try:
        decoded = base64.b32decode(normalized, casefold=True)
    except (binascii.Error, ValueError):
        return None
    if not decoded or decoded == data:
        return None
    try:
        text = decoded.decode("utf-8")
    except UnicodeDecodeError:
        recognized_binary = decoded.startswith((
            b"\x1f\x8b", b"BZh", b"\xfd7zXZ\x00", b"PK\x03\x04",
            b"\xfe\xff", b"\xff\xfe", b"\x00\x00\xfe\xff",
            b"\xff\xfe\x00\x00",
        )) or (len(decoded) >= 2 and decoded[0] == 0x78)
        if not recognized_binary:
            return None
    else:
        if not text or any(
            not char.isprintable() and char not in "\r\n\t"
            for char in text
        ):
            return None
    return decoded


def decode_ascii85(data: bytes) -> bytes | None:
    """Decode Adobe ASCII85, or an unwrapped ASCII85 payload."""
    candidate = data.strip()
    adobe = candidate.startswith(b"<~") and candidate.endswith(b"~>")
    if not adobe and (
        not candidate
        or len(candidate) % 5 == 1
        or _ASCII85_BYTES.fullmatch(candidate) is None
    ):
        return None
    try:
        decoded = base64.a85decode(candidate, adobe=adobe)
    except (ValueError, OverflowError):
        return None
    if not decoded or decoded == data:
        return None
    if not adobe:
        try:
            text = decoded.decode("utf-8")
        except UnicodeDecodeError:
            recognized_binary = decoded.startswith((
                b"\x1f\x8b", b"BZh", b"\xfd7zXZ\x00", b"PK\x03\x04",
                b"\xfe\xff", b"\xff\xfe", b"\x00\x00\xfe\xff",
                b"\xff\xfe\x00\x00",
            )) or (len(decoded) >= 2 and decoded[0] == 0x78)
            if not recognized_binary:
                return None
        else:
            if not text or any(
                not char.isprintable() and char not in "\r\n\t"
                for char in text
            ):
                return None
    return decoded


def decode_morse(data: bytes) -> bytes | None:
    """Decode whitespace-separated International Morse letters and digits."""
    try:
        symbols = data.decode("ascii").split()
    except UnicodeDecodeError:
        return None
    if not symbols or any(symbol not in MORSE for symbol in symbols):
        return None
    return "".join(MORSE[symbol] for symbol in symbols).encode("ascii")


def decode_hex(data: bytes) -> bytes | None:
    """Decode a complete, whitespace-tolerant hexadecimal byte string."""
    compact = _WHITESPACE_BYTES.sub(b"", data)
    if not compact or len(compact) % 2 or _HEX_BYTES.fullmatch(compact) is None:
        return None
    try:
        return bytes.fromhex(compact.decode("ascii"))
    except ValueError:
        return None


def decode_reversed_hex(data: bytes) -> bytes | None:
    """Reverse a hexadecimal string, then decode its bytes when they are text."""
    compact = _WHITESPACE_BYTES.sub(b"", data)
    if (
        not compact
        or len(compact) % 2
        or _HEX_BYTES.fullmatch(compact) is None
    ):
        return None
    try:
        decoded = bytes.fromhex(compact[::-1].decode("ascii"))
        text = decoded.decode("utf-8")
    except (UnicodeDecodeError, ValueError):
        return None
    if not text or any(
        not char.isprintable() and char not in "\r\n\t"
        for char in text
    ):
        return None
    return decoded


def decode_reversed_text(data: bytes) -> bytes | None:
    """Reverse readable text only when it improves the English interpretation."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None
    reversed_text = text[::-1].encode("utf-8")
    if readable_english_score(reversed_text) <= readable_english_score(data):
        return None
    return reversed_text


def decode_percent_bytes(data: bytes) -> bytes | None:
    """Decode percent-escaped bytes without treating plus signs as spaces."""
    if _PERCENT_BYTES.search(data) is None:
        return None
    decoded = urllib.parse.unquote_to_bytes(data)
    return decoded if decoded != data else None


def decode_binary_bytes(data: bytes) -> bytes | None:
    """Decode whitespace-separated eight-bit binary byte values."""
    try:
        values = data.decode("ascii").split()
    except UnicodeDecodeError:
        return None
    if not values or any(not re.fullmatch(r"[01]{8}", value) for value in values):
        return None
    return bytes(int(value, 2) for value in values)


def decode_decimal_bytes(data: bytes) -> bytes | None:
    """Decode whitespace-separated decimal byte values without hex ambiguity."""
    try:
        values = data.decode("ascii").split()
    except UnicodeDecodeError:
        return None
    if (
        len(values) < 2
        or any(not re.fullmatch(r"\d{1,3}", value) for value in values)
        or not any(len(value) == 3 for value in values)
    ):
        return None
    numbers = [int(value) for value in values]
    if any(value > 255 for value in numbers):
        return None
    return bytes(numbers)


def decode_unicode_bom(data: bytes) -> bytes | None:
    """Decode BOM-marked UTF-16/32 text and return it as UTF-8."""
    for encoding, bom in (
        ("utf-32", (b"\x00\x00\xfe\xff", b"\xff\xfe\x00\x00")),
        ("utf-16", (b"\xfe\xff", b"\xff\xfe")),
    ):
        if data.startswith(bom):
            try:
                return data.decode(encoding).encode("utf-8")
            except UnicodeDecodeError:
                return None
    return None


def decode_unicode_codepoints(data: bytes) -> bytes | None:
    """Decode whitespace-separated U+ hexadecimal Unicode code points."""
    try:
        tokens = data.decode("ascii").split()
    except UnicodeDecodeError:
        return None
    if not tokens or any(
        re.fullmatch(r"U\+[0-9a-fA-F]{4,6}", token) is None
        for token in tokens
    ):
        return None
    values = [int(token[2:], 16) for token in tokens]
    if any(value > 0x10FFFF or 0xD800 <= value <= 0xDFFF for value in values):
        return None
    return "".join(chr(value) for value in values).encode("utf-8")


def decode_brainfuck(data: bytes, step_limit: int = 10_000_000) -> bytes | None:
    """Run a plain Brainfuck program and return its output bytes."""
    if b"." not in data:
        return None
    commands = b"><+-.,[]"
    if not data or any(byte not in commands + b" \t\r\n" for byte in data):
        return None
    program = bytes(byte for byte in data if byte in commands)
    if not program:
        return None

    jumps: dict[int, int] = {}
    stack = []
    for index, command in enumerate(program):
        if command == ord("["):
            stack.append(index)
        elif command == ord("]"):
            if not stack:
                return None
            opening = stack.pop()
            jumps[opening] = index
            jumps[index] = opening
    if stack:
        return None

    tape: dict[int, int] = {}
    pointer = 0
    pc = 0
    output = bytearray()
    steps = 0
    while pc < len(program):
        steps += 1
        if steps > step_limit:
            return None
        command = program[pc]
        value = tape.get(pointer, 0)
        if command == ord(">"):
            pointer += 1
        elif command == ord("<"):
            pointer -= 1
        elif command == ord("+"):
            tape[pointer] = (value + 1) & 0xFF
        elif command == ord("-"):
            tape[pointer] = (value - 1) & 0xFF
        elif command == ord("."):
            output.append(value)
        elif command == ord(","):
            tape[pointer] = 0
        elif command == ord("[") and value == 0:
            pc = jumps[pc]
        elif command == ord("]") and value != 0:
            pc = jumps[pc]
        pc += 1
    return bytes(output) if output else None


def decode_ook(data: bytes) -> bytes | None:
    """Translate standard Ook! instruction pairs and run the Brainfuck program."""
    if b"Ook" not in data:
        return None
    if re.fullmatch(rb"\s*(?:Ook[.!?]\s*)+", data) is None:
        return None
    tokens = re.findall(rb"Ook([.!?])", data)
    if len(tokens) % 2:
        return None
    commands = {
        (b".", b"."): b"+",
        (b".", b"?"): b">",
        (b"?", b"."): b"<",
        (b"!", b"."): b".",
        (b".", b"!"): b",",
        (b"?", b"?"): b"[",
        (b"?", b"!"): b"]",
        (b"!", b"!"): b"-",
    }
    try:
        program = b"".join(
            commands[(tokens[index], tokens[index + 1])]
            for index in range(0, len(tokens), 2)
        )
    except KeyError:
        return None
    return decode_brainfuck(program)


def decode_compressed(data: bytes) -> bytes | None:
    """Decompress common self-identifying compression wrappers."""
    decompressors = (
        (data.startswith(b"\x1f\x8b"), gzip.decompress),
        (data.startswith(b"BZh"), bz2.decompress),
        (data.startswith(b"\xfd7zXZ\x00"), lzma.decompress),
        (len(data) >= 2 and data[0] == 0x78, zlib.decompress),
    )
    for matches, decompress in decompressors:
        if not matches:
            continue
        try:
            decoded = decompress(data)
        except (OSError, EOFError, lzma.LZMAError, zlib.error):
            continue
        if decoded and decoded != data:
            return decoded
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        try:
            decoded = zlib.decompress(data, -zlib.MAX_WBITS)
        except zlib.error:
            return None
        if decoded and decoded != data:
            return decoded
    return None


def decode_wrapped_layers(data: bytes, limit: int = 8) -> bytes:
    """Decode common complete layers such as Base64, hex, BOM text, and DEFLATE."""
    def is_terminal_text(value: bytes) -> bool:
        try:
            text = value.decode("utf-8")
        except UnicodeDecodeError:
            return False
        compact = _WHITESPACE_TEXT.sub("", text)
        looks_encoded = (
            (compact.startswith("<~") and compact.endswith("~>"))
            or _PERCENT_TEXT.search(compact) is not None
            or (
                len(compact) >= 8
                and len(compact) % 2 == 0
                and _HEX_TEXT.fullmatch(compact) is not None
            )
            or (
                len(compact) >= 8
                and _BASE64_TEXT.fullmatch(compact) is not None
                and ("=" in compact or len(compact) % 4 == 0)
            )
        )
        return (
            bool(text)
            and all(char.isprintable() or char in "\r\n\t" for char in text)
            and not looks_encoded
        )

    decoded = data
    for _ in range(limit):
        if re.fullmatch(rb"\s*[a-z]+(?:[- ][a-z]+)*\s*", decoded):
            break
        compressed = decode_compressed(decoded)
        if compressed is not None:
            decoded = compressed
            if is_terminal_text(decoded):
                break
            continue
        next_layer = (
            decode_percent_bytes(decoded)
            or decode_reversed_hex(decoded)
            or decode_hex(decoded)
            or decode_unicode_bom(decoded)
            or decode_unicode_codepoints(decoded)
            or decode_base32(decoded)
            or decode_layer(decoded)
            or decode_ascii85(decoded)
            or decode_reversed_text(decoded)
        )
        if next_layer is None or next_layer == decoded:
            break
        decoded = next_layer
        if is_terminal_text(decoded):
            break
    try:
        decoded.decode("utf-8")
    except UnicodeDecodeError:
        return data
    return decoded


def decode_bacon_nibbles(data: bytes) -> bytes | None:
    """Map five-character a/b groups with values 0–15 to hexadecimal digits."""
    try:
        groups = data.decode("ascii").split()
    except UnicodeDecodeError:
        return None
    if not groups or any(not re.fullmatch(r"[ab]{5}", group) for group in groups):
        return None
    values = [
        int(group.translate(str.maketrans({"a": "0", "b": "1"})), 2)
        for group in groups
    ]
    if any(value > 15 for value in values):
        return None
    return "".join(format(value, "x") for value in values).encode("ascii")


def decode_layers(data: bytes, limit: int = 32) -> list[bytes]:
    layers = [data]
    for _ in range(limit):
        decoded = decode_ascii85(layers[-1]) or decode_layer(layers[-1])
        if decoded is None:
            break
        layers.append(decoded)
    return layers


def _decode_numbered_fragments_impl(
    data: bytes,
    rail_fence_rails: int | None = None,
    *,
    allow_recursive: bool = True,
    fast_instruction_slug: bool = False,
) -> bytes | None:
    """Decode numbered fragments whose codec is selected by row number."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None
    rows = []
    for line in text.splitlines():
        match = _MIXED_ROW.fullmatch(line)
        if not match:
            return None
        rows.append((int(match.group(1)), match.group(2)))
    row_numbers = [number for number, _ in rows]
    if row_numbers != list(range(1, len(rows) + 1)):
        return None
    if not rows:
        return None

    unknown_interior = any(
        number not in MIXED_FRAGMENT_CODECS for number, _ in rows[:-1]
    )
    if unknown_interior and rows[-1][0] not in MIXED_FRAGMENT_CODECS:
        known_rows = [
            (number, payload)
            for number, payload in rows
            if number in MIXED_FRAGMENT_CODECS
        ]
        if not known_rows:
            return None
        prefix = decode_numbered_fragments(
            "\n".join(f"{number}\t{payload}" for number, payload in known_rows).encode()
        )
        if prefix is None:
            return None

        # Some assignments append independently encoded pieces after the
        # numbered codec rows. A hex span can begin immediately after a
        # plaintext character that is also a valid hex digit, so keep every
        # valid UTF-8 suffix boundary until the complete answer is assembled.
        prefix_candidates = [prefix]
        terminal_hex = re.search(rb"([0-9a-fA-F]+)$", prefix)
        if terminal_hex:
            encoded_suffix = terminal_hex.group(1)
            for offset in range(len(encoded_suffix)):
                candidate_hex = encoded_suffix[offset:]
                if len(candidate_hex) % 2:
                    continue
                try:
                    decoded_suffix = bytes.fromhex(
                        candidate_hex.decode("ascii")
                    ).decode("utf-8")
                except (ValueError, UnicodeDecodeError):
                    continue
                prefix_candidates.append(
                    prefix[:terminal_hex.start(1) + offset]
                    + decoded_suffix.encode("utf-8")
                )

        extra_rows = [
            payload
            for number, payload in rows
            if number not in MIXED_FRAGMENT_CODECS
        ]
        terminal_program = None
        if extra_rows:
            payload = extra_rows[-1].encode("utf-8")
            candidate = decode_ook(payload) or decode_brainfuck(payload)
            if candidate and _TERMINAL_SUFFIX.search(candidate):
                terminal_program = candidate
        candidates = []
        for index, payload in enumerate(extra_rows):
            payload_bytes = payload.encode("utf-8")
            layered = decode_wrapped_layers(payload_bytes)
            hex_bytes = decode_hex(payload_bytes)
            options = [payload_bytes]
            try:
                rot13_payload = codecs.decode(
                    payload_bytes.decode("ascii"), "rot_13"
                ).encode("ascii")
            except (UnicodeDecodeError, UnicodeEncodeError):
                rot13_payload = payload_bytes
            if rot13_payload != payload_bytes:
                rotated_layer = decode_wrapped_layers(rot13_payload)
                if rotated_layer != rot13_payload:
                    options.append(rotated_layer)
                # A short ROT13-wrapped Base64 fragment can also look like
                # reversed hex. Preserve the direct Base64 reading as another
                # candidate so the assembled slug can disambiguate it.
                rotated_base64 = decode_layer(rot13_payload)
                if rotated_base64 is not None:
                    alternate_layer = decode_wrapped_layers(rotated_base64)
                    if alternate_layer != rot13_payload:
                        options.append(alternate_layer)
            program_output = (
                decode_ook(payload_bytes) or decode_brainfuck(payload_bytes)
            )
            if program_output:
                options.append(program_output)
            # A terminal comma can separate the final value from nothing,
            # while doubled commas still preserve a literal comma value.
            counted_payload = payload[:-1] if payload.endswith(",") else payload
            counted = list(
                re.finditer(r"(\d+):(.*?)(?=,\d+:|$)", counted_payload)
            )
            if counted and all(
                counted_payload[previous.end():current.start()] == ","
                for previous, current in zip(counted, counted[1:])
            ) and counted[0].start() == 0 and counted[-1].end() == len(counted_payload):
                options.append(
                    "".join(
                        match.group(2) * int(match.group(1))
                        for match in counted
                    ).encode("utf-8")
                )
            if layered != payload_bytes:
                options.append(layered)
            if layered == payload_bytes and hex_bytes is not None:
                options.append(hex_bytes)
            elif (
                layered == payload_bytes
                and hex_bytes is None
                and not any(option != payload_bytes for option in options)
            ):
                rails_to_try = list(range(2, min(11, len(payload_bytes))))
                if rail_fence_rails in rails_to_try:
                    rails_to_try.remove(rail_fence_rails)
                    rails_to_try.insert(0, rail_fence_rails)
                options.extend(
                    candidate
                    for rails in rails_to_try
                    if (candidate := rail_fence_decode(payload_bytes, rails))
                    is not None
                )
            if hex_bytes is not None:
                if (text_bytes := decode_unicode_bom(hex_bytes)) is not None:
                    options.append(text_bytes)
            elif (
                allow_recursive
                and layered == payload_bytes
                and terminal_program is None
                and not re.fullmatch(
                    rb"\s*[a-z]+(?:[- ][a-z]+)*\s*", payload_bytes
                )
            ):
                nested = decode_assignment(payload_bytes, rail_fence_rails)
                options.append(nested)
            if terminal_program is not None and index == len(extra_rows) - 1:
                options = [terminal_program]

            # Suffix pieces are text. Discard arbitrary binary decoder outputs
            # before combining them so an ambiguous ASCII85-looking fragment
            # cannot multiply the search space or outrank a real text decode.
            usable = []
            for option in options:
                try:
                    text_option = option.decode("utf-8")
                except UnicodeDecodeError:
                    continue
                if text_option and all(
                    char.isprintable() or char in "\r\n\t"
                    for char in text_option
                ):
                    usable.append(option)
            decoded_options = [
                option for option in usable if option != payload_bytes
            ]
            if decoded_options:
                usable = decoded_options
            if not usable:
                return None
            candidates.append(list(dict.fromkeys(usable)))

        slug_pattern = re.compile(
            rb"\b[a-z]+(?:-[a-z]+){2}-\d{2}\b"
        )
        full_candidates = candidates
        def fragment_score(value: bytes) -> tuple[float, int, int]:
            text = value.decode("utf-8")
            readable = sum(
                char.isascii()
                and (char.isalpha() or char.isspace() or char in "-:.,!?;'")
                for char in text
            )
            normalized = text.lower()
            common_bigrams = sum(
                normalized[index:index + 2] in COMMON_ENGLISH_BIGRAMS
                for index in range(len(normalized) - 1)
            )
            return (
                readable / max(1, len(text)),
                common_bigrams,
                -len(text),
            )

        # Keep the strongest text interpretations of each independently
        # encoded fragment so large bundles do not require an exhaustive
        # cross-product.
        candidates = [
            sorted(options, key=fragment_score, reverse=True)[:2]
            for options in candidates
        ]
        if fast_instruction_slug and candidates:
            for candidate_prefix in prefix_candidates:
                combined = candidate_prefix + b"".join(
                    options[0] for options in candidates
                )
                match = next(
                    (
                        candidate
                        for candidate in slug_pattern.finditer(combined)
                        if combined[
                            max(
                                0,
                                candidate.start() - len(b"Game Master: "),
                            ):candidate.start()
                        ] == b"Game Master: "
                    ),
                    None,
                )
                if match:
                    return combined

        def best_slug_combination(
            fragment_options: list[list[bytes]],
        ) -> bytes | None:
            best_combined = None
            best_score = None
            for candidate_prefix, pieces in itertools.product(
                prefix_candidates, itertools.product(*fragment_options)
            ):
                combined = candidate_prefix + b"".join(pieces)
                try:
                    combined.decode("utf-8")
                except UnicodeDecodeError:
                    continue
                matches = list(slug_pattern.finditer(combined))
                if not matches:
                    continue
                match = matches[-1]
                slug = match.group()
                words = slug.decode("ascii").split("-")[:-1]
                instruction_context = combined[
                    max(0, match.start() - len(b"Game Master: ")):match.start()
                ]
                score = (
                    int(instruction_context == b"Game Master: "),
                    int(combined[max(0, match.start() - 2):match.start()] == b": "),
                    len(words[0]),
                    slug_readability_score(slug),
                    sum(map(len, words)),
                )
                if best_score is None or score > best_score:
                    best_combined = combined
                    best_score = score
            if best_combined is None:
                # Some bundles percent-encode the completed instruction in
                # multiple layers. Decode only after joining the numbered
                # fragments, since an escape can cross fragment boundaries.
                for candidate_prefix in prefix_candidates:
                    combined = candidate_prefix + b"".join(
                        options[0] for options in fragment_options
                    )
                    decoded = decode_assignment(combined, rail_fence_rails)
                    if slug_pattern.search(decoded):
                        return decoded
            return best_combined

        best_combined = best_slug_combination(candidates)
        if best_combined is None and terminal_program is not None:
            best_combined = best_slug_combination(full_candidates)
        return best_combined

    decoded = []
    for number, payload in rows[:-1] if rows[-1][0] not in MIXED_FRAGMENT_CODECS else rows:
        if number not in MIXED_FRAGMENT_CODECS:
            return None
        codec = MIXED_FRAGMENT_CODECS[number]
        if codec == "base64":
            value = base64.b64decode(payload + "=" * (-len(payload) % 4))
        elif codec == "rot13":
            value = codecs.encode(payload, "rot_13").encode("utf-8")
        elif codec == "hex":
            value = bytes.fromhex(payload)
        elif codec == "binary":
            value = bytes(int(part, 2) for part in payload.split())
        elif codec == "decimal":
            value = bytes(int(part, 10) for part in payload.split())
        elif codec == "octal":
            value = bytes(int(part, 8) for part in payload.split())
        elif codec == "percent":
            value = urllib.parse.unquote_to_bytes(payload)
        elif codec == "html":
            value = html.unescape(payload).encode("utf-8")
        elif codec == "unicode":
            value = json.loads(payload).encode("utf-8")
        elif codec == "base32":
            value = base64.b32decode(payload + "=" * (-len(payload) % 8))
        elif codec == "rot47":
            value = rot47(payload.encode("utf-8"))
            if value is None:
                return None
        elif codec == "morse":
            value = decode_morse(payload.encode("ascii"))
            if value is None:
                return None
        elif codec == "bacon":
            value = decode_bacon_nibbles(payload.encode("ascii"))
            if value is None:
                return None
        else:
            if codec == "reverse":
                value = payload[::-1].encode("utf-8")
            elif codec == "atbash":
                value = atbash(payload.encode("utf-8"))
                if value is None:
                    return None
            elif codec == "caesar":
                value = caesar_shift(payload.encode("utf-8"), -7)
                if value is None:
                    return None
            else:
                normalized = payload.replace("-", "+").replace("_", "/")
                normalized += "=" * (-len(normalized) % 4)
                value = base64.b64decode(normalized, validate=True)
        decoded.append(value)

    if rows[-1][0] not in MIXED_FRAGMENT_CODECS:
        # Some assignments append a short Rail Fence encoded slug suffix
        # after the numbered mixed-codec rows.
        payload = rows[-1][1].encode("utf-8")
        suffix = next(
            (
                candidate
                for rails in range(2, min(11, len(payload)))
                if (candidate := rail_fence_decode(payload, rails)) is not None
                and re.fullmatch(rb"[a-z]+-\d{2}", candidate)
            ),
            None,
        )
        if suffix is None:
            return None
        decoded.append(suffix)
    return b"".join(decoded)


def decode_numbered_fragments(
    data: bytes,
    rail_fence_rails: int | None = None,
    *,
    allow_recursive: bool = True,
    fast_instruction_slug: bool = False,
) -> bytes | None:
    """Ignore malformed codec-shaped text instead of aborting other decoders."""
    try:
        return _decode_numbered_fragments_impl(
            data,
            rail_fence_rails,
            allow_recursive=allow_recursive,
            fast_instruction_slug=fast_instruction_slug,
        )
    except (
        ValueError,
        binascii.Error,
        UnicodeError,
        OverflowError,
        json.JSONDecodeError,
        TypeError,
    ):
        return None


SLUG_PATTERN = re.compile(rb"\b[a-z]+(?:-[a-z]+){2}-\d{2}\b")
COMMON_ENGLISH_BIGRAMS = set(
    "th he in er an re on at en nd ti es or te of ed is it al ar st to nt "
    "ng se ha as ou io le ve co me de hi ri ro ic ne ea ra ce li ch ll be "
    "ma si om ur".split()
)


def slug_readability_score(data: bytes) -> int | None:
    """Score answer slugs by common English letter pairs and word shapes."""
    matches = SLUG_PATTERN.findall(data)
    if not matches:
        return None
    words = matches[-1].decode("ascii").split("-")[:-1]
    common_pairs = sum(
        word[index:index + 2] in COMMON_ENGLISH_BIGRAMS
        for word in words
        for index in range(len(word) - 1)
    )
    consonant_pairs = sum(
        word[index] not in "aeiouy" and word[index + 1] not in "aeiouy"
        for word in words
        for index in range(len(word) - 1)
    )
    return common_pairs - consonant_pairs


def infer_rail_fence_rails(blobs: list[bytes]) -> int | None:
    """Infer a shared Rail Fence rail count from a bundle of assigned blobs."""
    scores: dict[int, int] = {}
    for rails in range(2, 11):
        score = 0
        count = 0
        for blob in blobs:
            decoded = decode_numbered_fragments(blob, rail_fence_rails=rails)
            if decoded is None:
                continue
            candidate_score = slug_readability_score(decoded)
            if candidate_score is not None:
                score += candidate_score
                count += 1
        if count:
            scores[rails] = score
    if not scores:
        return None
    best_score = max(scores.values())
    best_rails = [rails for rails, score in scores.items() if score == best_score]
    return best_rails[0] if len(best_rails) == 1 else None


def atbash(data: bytes) -> bytes | None:
    """Apply the Latin alphabet Atbash substitution to UTF-8 text."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None
    if not text or not any(char.isalpha() for char in text):
        return None
    translated = []
    for char in text:
        if "a" <= char <= "z":
            translated.append(chr(ord("z") - (ord(char) - ord("a"))))
        elif "A" <= char <= "Z":
            translated.append(chr(ord("Z") - (ord(char) - ord("A"))))
        else:
            translated.append(char)
    return "".join(translated).encode("utf-8")


def caesar_shift(data: bytes, shift: int) -> bytes | None:
    """Shift ASCII letters by ``shift`` places, preserving other bytes."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None
    translated = []
    for char in text:
        if "a" <= char <= "z":
            translated.append(chr((ord(char) - ord("a") + shift) % 26 + ord("a")))
        elif "A" <= char <= "Z":
            translated.append(chr((ord(char) - ord("A") + shift) % 26 + ord("A")))
        else:
            translated.append(char)
    return "".join(translated).encode("utf-8")


def rot47(data: bytes) -> bytes | None:
    """Rotate printable ASCII characters by 47 places."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None
    return "".join(
        chr(33 + ((ord(char) - 33 + 47) % 94))
        if 33 <= ord(char) <= 126
        else char
        for char in text
    ).encode("utf-8")


def readable_english_score(data: bytes) -> int:
    """Score common instruction words to distinguish an Atbash layer."""
    try:
        words = set(re.findall(r"[a-z]+", data.decode("utf-8").lower()))
    except UnicodeDecodeError:
        return 0
    markers = {
        "answer", "decode", "decoding", "exact", "game", "master",
        "message", "submit", "this", "to", "warmup", "work",
    }
    return len(words & markers)


def rail_fence_decode(data: bytes, rails: int) -> bytes | None:
    """Decode a Rail Fence transposition with the given number of rails."""
    if rails < 2 or rails >= len(data):
        return None
    cycle = list(range(rails)) + list(range(rails - 2, 0, -1))
    rail_counts = [0] * rails
    for index in range(len(data)):
        rail_counts[cycle[index % len(cycle)]] += 1

    rail_data = []
    offset = 0
    for count in rail_counts:
        rail_data.append(data[offset:offset + count])
        offset += count

    rail_offsets = [0] * rails
    decoded = bytearray()
    for index in range(len(data)):
        rail = cycle[index % len(cycle)]
        decoded.append(rail_data[rail][rail_offsets[rail]])
        rail_offsets[rail] += 1
    return bytes(decoded)


def _decode_assignment_layers(
    data: bytes, rail_fence_rails: int | None = None
) -> bytes:
    """Decode the assigned blob format, including its numbered text fragments."""
    decoded = data
    for _ in range(32):
        next_layer = (
            decode_numbered_fragments(decoded, rail_fence_rails)
            or decode_ook(decoded)
            or decode_brainfuck(decoded)
            or decode_bacon_nibbles(decoded)
            or decode_morse(decoded)
            or decode_percent_bytes(decoded)
            or decode_decimal_bytes(decoded)
            or decode_binary_bytes(decoded)
            or decode_reversed_text(decoded)
            or decode_reversed_hex(decoded)
            or decode_hex(decoded)
            or decode_unicode_bom(decoded)
            or decode_unicode_codepoints(decoded)
            or decode_compressed(decoded)
            or decode_base32(decoded)
            or decode_layer(decoded)
            or decode_ascii85(decoded)
        )
        if next_layer is None or next_layer == decoded:
            break
        decoded = next_layer
    candidates = [decoded]
    candidates.extend(
        candidate
        for shift in range(1, 26)
        if (candidate := caesar_shift(decoded, shift)) is not None
    )
    rotated = rot47(decoded)
    if rotated is not None:
        candidates.append(rotated)
    opposite = atbash(decoded)
    if opposite is not None:
        candidates.append(opposite)
    candidates.extend(
        candidate
        for rails in range(2, min(11, len(decoded)))
        if (candidate := rail_fence_decode(decoded, rails)) is not None
    )
    return max(candidates, key=readable_english_score)


def decode_assignment(data: bytes, rail_fence_rails: int | None = None) -> bytes:
    """Decode assigned layers, including ROT13 applied before Base64."""
    numbered = decode_numbered_fragments(
        data,
        rail_fence_rails,
        allow_recursive=False,
        fast_instruction_slug=True,
    )
    if (
        numbered is not None
        and re.search(
            rb"Game Master:\s*[a-z0-9]+(?:-[a-z0-9]+)+",
            numbered,
            re.I,
        )
    ):
        return numbered
    candidates = [_decode_assignment_layers(data, rail_fence_rails)]
    try:
        rot13_input = codecs.decode(data.decode("ascii"), "rot_13").encode("ascii")
    except (UnicodeDecodeError, UnicodeEncodeError):
        pass
    else:
        if rot13_input != data:
            candidates.append(
                _decode_assignment_layers(rot13_input, rail_fence_rails)
            )
    return max(candidates, key=readable_english_score)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument(
        "--final-only",
        action="store_true",
        help="print only the final decoded layer",
    )
    args = parser.parse_args()

    data = args.input.read_bytes()
    rail_fence_rails = None
    if args.final_only:
        selected = [decode_assignment(data)]
    else:
        layers = [data]
        for _ in range(32):
            current = layers[-1]
            decoded = (
                decode_numbered_fragments(current, rail_fence_rails)
                or decode_bacon_nibbles(current)
                or decode_morse(current)
                or decode_percent_bytes(current)
                or decode_decimal_bytes(current)
                or decode_binary_bytes(current)
                or decode_hex(current)
                or decode_unicode_bom(current)
                or decode_unicode_codepoints(current)
                or decode_base32(current)
                or decode_layer(current)
                or decode_ascii85(current)
            )
            if decoded is None or decoded == current:
                break
            layers.append(decoded)
        final = decode_assignment(data)
        if final != layers[-1]:
            layers.append(final)
        selected = layers
    for index, layer in enumerate(selected):
        label = "final" if args.final_only else f"layer {index}"
        print(f"--- {label} ---")
        try:
            print(layer.decode("utf-8"))
        except UnicodeDecodeError:
            print(layer.hex())


if __name__ == "__main__":
    main()
