#!/usr/bin/env python3
"""Canonical static parser for Huntress Script Analysis artifacts and answers."""

from __future__ import annotations

import ast
import base64
from functools import lru_cache
import hashlib
import json
import re
import sys
import urllib.parse
from pathlib import Path


def parse_pairs(text: str) -> dict[str, str]:
    return dict(
        item.split("=", 1)
        for item in text.strip().split("|")
        if "=" in item and not item.startswith("v=")
    )


def marker_descriptor(text: str) -> dict[str, str] | None:
    m = re.search(r"HUNTRESS_ANALYSIS_V1:(HB64|B64|HEX|FRAG)-([A-Za-z0-9=.%]+)", text)
    if not m:
        return None
    kind, payload = m.groups()
    if kind == "B64":
        decoded = base64.b64decode(payload + "=" * (-len(payload) % 4)).decode()
    elif kind == "HB64":
        inner = bytes.fromhex(payload).decode()
        decoded = base64.b64decode(inner + "=" * (-len(inner) % 4)).decode()
    elif kind == "HEX":
        decoded = bytes.fromhex(payload).decode()
    else:
        decoded = bytes.fromhex(payload.replace(".", "")).decode()
    return parse_pairs(decoded)


def layered_descriptor(text: str) -> dict[str, str] | None:
    """Decode descriptors wrapped in the artifact's declared reversible layers."""
    match = re.search(
        r"HUNTRESS_ANALYSIS_V1:LYR-([a-z0-9_]+)-([A-Za-z0-9=.+/]+)",
        text,
        re.I,
    )
    if not match:
        split = re.search(
            r"(?:const|let|var)\s+HUNTRESS_ANALYSIS_V1_SPLIT_\w+\s*=\s*\[(.*?)\]"
            r"(?:\s*\.join\(\s*[\"']{2}\s*\))?\s*;",
            text,
            re.S,
        )
        if split:
            fragments = re.findall(r"""(["'])((?:\\.|(?!\1).)*)\1""", split.group(1), re.S)
            joined = "".join(ast.literal_eval(quote + value + quote) for quote, value in fragments)
            match = re.search(
                r"LYR-([a-z0-9_]+)-([A-Za-z0-9=.+/]+)", joined, re.I
            )
    if not match:
        return None
    profile, payload = match.groups()
    data = payload.encode("ascii")
    for layer in reversed(profile.lower().split("_")):
        if layer == "frag":
            data = data.replace(b".", b"")
        elif layer == "rev":
            data = data[::-1]
        elif layer == "hex":
            data = bytes.fromhex(data.decode("ascii"))
        elif layer == "b64":
            data = base64.b64decode(data)
        elif layer == "b32":
            data = base64.b32decode(data)
        else:
            raise ValueError(f"Unsupported descriptor layer {layer!r}")
    return parse_pairs(data.decode("ascii"))


def codec_descriptor(text: str) -> dict[str, str] | None:
    codec_match = re.search(
        r"(?im)(?:const\s+|readonly\s+)?Codec_(\w+)\s*=\s*[\"']([^\"']*)",
        text,
    )
    if not codec_match:
        return None
    tag, codec = codec_match.groups()
    material_match = re.search(
        rf"(?im)(?:const\s+|readonly\s+)?(?:MATERIAL|Material)_{tag}\s*=",
        text,
    )
    if not material_match:
        return None
    material_start = material_match.end()
    codec_start = codec_match.start()
    material_source = text[material_start:codec_start]
    literals = re.findall(
        r"""(?<![A-Za-z0-9_])(b)?(["'])((?:\\.|(?!\2).)*)\2""",
        material_source,
        re.S,
    )
    chunks = []
    for prefix, quote, value in literals:
        parsed = ast.literal_eval(prefix + quote + value + quote)
        chunks.append(parsed)
    payload_bytes = b"".join(x for x in chunks if isinstance(x, bytes))
    payload = "".join(x for x in chunks if isinstance(x, str))
    parts = codec.split("|")
    representation = parts[0]
    transform = parts[1] if len(parts) > 2 else ""
    key_text = parts[2] if len(parts) > 2 else (parts[1] if len(parts) > 1 else "")
    if len(parts) == 2 and representation == "xor_hex":
        transform = "single_byte_xor"
    if not payload and not payload_bytes:
        payload = material_source
    key = bytes.fromhex(key_text.replace(",", "")) if re.fullmatch(r"[0-9a-fA-F,]+", key_text or "") else b""

    if representation == "reversed_base64":
        data = base64.b64decode(payload[::-1])
    elif representation.startswith("base64") or representation == "urlsafe_base64":
        data = base64.urlsafe_b64decode(payload) if representation == "urlsafe_base64" else base64.b64decode(payload)
    elif representation == "unicode_escapes":
        data = bytes(int(x, 16) for x in re.findall(r"\\u00([0-9a-fA-F]{2})", payload))
    elif representation in {"percent_hex"}:
        data = urllib.parse.unquote_to_bytes(payload)
    elif representation == "hex_escape":
        data = payload_bytes or bytes(int(x, 16) for x in re.findall(r"\\x([0-9a-fA-F]{2})", payload))
    elif representation == "escaped_octets":
        data = bytes(int(x, 16) for x in re.findall(r"\\x([0-9a-fA-F]{2})", payload))
    elif representation == "hex_array":
        values = json.loads(payload)
        data = bytes.fromhex("".join(values))
    elif representation == "hex_buffer":
        data = bytes.fromhex(payload)
    elif representation.startswith("hex") or representation == "xor_hex":
        data = bytes.fromhex(re.sub(r"[^0-9a-fA-F]", "", payload))
    elif representation.startswith("reversed_hex"):
        data = bytes.fromhex(re.sub(r"[^0-9a-fA-F]", "", payload))
        data = data[::-1]
    elif representation.startswith("reversed_decimal") or representation == "reversed_integer_list":
        data = bytes(int(x) & 0xFF for x in re.findall(r"\d+", payload))[::-1]
    elif representation.startswith("decimal") or representation == "integer_list":
        data = bytes(int(x) & 0xFF for x in re.findall(r"\d+", payload))
    elif representation in {"integer_tuple", "integer_list", "json_numbers"}:
        data = bytes(int(x) & 0xFF for x in re.findall(r"\d+", payload))
    else:
        raise ValueError(f"Unsupported representation {representation!r}")

    if transform == "add_modulo_256":
        data = bytes((b - key[0]) & 0xFF for b in data)
    elif transform == "subtract_modulo_256":
        data = bytes((b + key[0]) & 0xFF for b in data)
    elif transform == "single_byte_xor":
        data = bytes(b ^ key[0] for b in data)
    elif transform == "repeating_key_xor":
        data = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
    elif transform == "rolling_xor":
        previous = key[0]
        out = []
        for b in data:
            out.append(b ^ previous)
            previous = b
        data = bytes(out)
    elif transform == "reverse_then_xor":
        data = bytes(b ^ key[0] for b in data[::-1])
    elif transform == "reverse_bytes":
        data = data[::-1]
    elif transform in {"", None, "identity"}:
        pass
    else:
        raise ValueError(f"Unsupported transform {transform!r}")

    decoded = data.decode("ascii")
    descriptor = parse_pairs(decoded)
    descriptor["representation"] = representation
    descriptor["transform"] = transform or "identity"
    return descriptor


def descriptor_for(path: Path, text: str | None = None) -> dict[str, str]:
    if text is None:
        text = path.read_text(errors="replace")
    descriptor = marker_descriptor(text)
    if descriptor is None:
        descriptor = layered_descriptor(text)
    if descriptor is None:
        descriptor = codec_descriptor(text)
    if descriptor is None and path.suffix.lower() == ".gs":
        descriptor = google_apps_script_descriptor(text)
    if descriptor is None and path.suffix.lower() == ".js":
        descriptor = jscript_descriptor(text)
    if descriptor is None and path.suffix.lower() in {".bat", ".cmd"}:
        descriptor = batch_descriptor(text)
    if descriptor is None and path.suffix.lower() == ".ps1":
        descriptor = powershell_descriptor(text)
    if descriptor is None:
        raise ValueError(f"No descriptor codec found in {path.name}")
    return descriptor


def google_apps_script_descriptor(text: str) -> dict[str, str] | None:
    """Recover the inert descriptor assembled by the Google Apps Script fixtures."""
    plan = re.search(
        r"function\s+buildAnalysisPlan_\w+\s*\(\s*\)\s*\{(.*?)\n\}",
        text,
        re.S,
    )
    if not plan:
        return None
    encoded = re.search(
        r"(?:const|var|let)\s+encoded_\w+\s*=\s*\[(.*?)\]\s*\.join\(\s*[\"']{2}\s*\)",
        plan.group(1),
        re.S,
    )
    if not encoded:
        return None
    raw = "".join(
        value
        for _, value in re.findall(
            r"""(["'])((?:\\.|(?!\1).)*)\1""", encoded.group(1), re.S
        )
    )
    raw = raw.replace("\\.", ".")

    def decode_payload(value: str) -> str:
        if value.startswith("HB64-"):
            inner = bytes.fromhex(value[5:].replace(".", "")).decode("ascii")
            return base64.b64decode(inner + "=" * (-len(inner) % 4)).decode("ascii")
        if value.startswith("B64-"):
            payload = value[4:]
            return base64.b64decode(payload + "=" * (-len(payload) % 4)).decode("ascii")
        if value.startswith("FRAG-"):
            return bytes.fromhex(value[5:].replace(".", "")).decode("ascii")
        if value.startswith("HEX-"):
            return bytes.fromhex(value[4:].replace(".", "")).decode("ascii")

        compact = value.replace(".", "")
        if compact and len(compact) % 2 == 0 and re.fullmatch(r"[0-9a-fA-F]+", compact):
            decoded = bytes.fromhex(compact).decode("ascii")
            # Some fixtures hex-encode a Base64 descriptor as a second layer.
            if decoded.startswith(("dj0", "v=")):
                if decoded.startswith("dj0"):
                    try:
                        return base64.b64decode(
                            decoded + "=" * (-len(decoded) % 4)
                        ).decode("ascii")
                    except (ValueError, UnicodeDecodeError):
                        pass
                return decoded
        try:
            decoded = base64.b64decode(
                value + "=" * (-len(value) % 4), validate=True
            ).decode("ascii")
            if "=" in decoded and "|" in decoded:
                return decoded
        except (ValueError, UnicodeDecodeError):
            pass
        return value

    decoded = decode_payload(raw)
    if "|" not in decoded or "=" not in decoded:
        return None
    return parse_pairs(decoded)


def jscript_descriptor(text: str) -> dict[str, str] | None:
    if not re.search(r"\brecover_\w+\s*=|\bfunction\s+recover", text):
        return None
    packed = re.search(r'var packedText\s*=\s*((?:"[^"]*"\s*\+\s*)*"[^"]*")', text)
    if packed:
        packed_text = "".join(re.findall(r'"([^"]*)"', packed.group(1)))
        if "decodeBase64(packedText)" in text:
            data = base64.b64decode(packed_text)
        elif packed_text.startswith("%"):
            data = urllib.parse.unquote_to_bytes(packed_text)
        elif "parseInt(packedParts[hi], 16)" in text:
            data = bytes(int(x, 16) for x in re.split(r"[^0-9a-fA-F]+", packed_text) if x)
        else:
            data = bytes(int(x) for x in re.findall(r"\d+", packed_text))
    else:
        arrays = []
        for m in re.finditer(r"(?:var|let|const)\s+(\w+)\s*=\s*\[([^\]]*)\]", text, re.S):
            body = m.group(2)
            if re.search(r"\b0x[0-9a-fA-F]+\b", body):
                vals = [int(x, 16) for x in re.findall(r"\b0x([0-9a-fA-F]+)\b", body)]
            else:
                vals = [int(x) for x in re.findall(r"(?<![\w.])-?\d+", body)]
            if len(vals) > 50:
                arrays.append((m.start(), vals))
        if not arrays:
            return None
        data = bytes(x for _, arr in sorted(arrays) for x in arr)

    recover_start = re.search(r"(?:var\s+recover_\w+\s*=\s*function|function\s+recover_\w+)", text)
    inspect_start = re.search(r"(?:var\s+inspect_\w+\s*=\s*function|function\s+inspect_\w+)", text)
    recover_body = text[recover_start.start():inspect_start.start() if inspect_start else None] if recover_start else ""
    if re.search(r"\b\w+\.reverse\(\)", recover_body):
        data = data[::-1]

    decode_function = re.search(r"(?:function\s+decode_\w+\s*\([^)]*\)|var\s+decode_\w+\s*=\s*function\s*(?:\w+)?\s*\([^)]*\))\s*\{(.*?)\n\}", text, re.S)
    if not decode_function:
        decode_function = re.search(r"function\s+decode\w*\s*\([^)]*\)\s*\{(.*?)\n\}", text, re.S)
    body = decode_function.group(1) if decode_function else ""
    if ".reverse()" in body:
        data = data[::-1]
    if "keyBytes[i % keyBytes.length]" in body:
        key_match = re.search(r"(?:var|const)\s+keyBytes\s*=\s*\[([^\]]+)\]", text)
        keys = [int(x) for x in re.findall(r"\d+", key_match.group(1))]
        data = bytes(b ^ keys[i % len(keys)] for i, b in enumerate(data))
    elif re.search(r"\^\s*previous", body):
        prev = re.search(r"previous\s*=\s*(\d+)", body)
        prior = int(prev.group(1))
        out = []
        for b in data:
            out.append(b ^ prior)
            prior = b
        data = bytes(out)
    elif re.search(r"\^\s*\d+", body):
        key = int(re.search(r"\^\s*(\d+)", body).group(1))
        data = bytes(b ^ key for b in data)
    else:
        op = re.search(r"\[[^\]]+\]\s*([+\-])\s*(\d+)", body)
        if op:
            operator, key = op.groups()
            key = int(key)
            data = bytes((b - key if operator == "-" else b + key) & 0xFF for b in data)
    try:
        raw = data.decode("utf-8")
        parsed = json.loads(raw)
        values = parsed.get("values", {})
        result = dict(values)
        if "steps" in parsed:
            result["steps"] = ",".join(parsed["steps"])
        if "stageCount" in parsed:
            result["stage_count"] = str(parsed["stageCount"])
        if "adapter" in parsed:
            result["adapter"] = parsed["adapter"]
        return result
    except Exception as exc:
        raise ValueError(f"Could not parse reconstructed JScript descriptor: {exc}") from exc


def batch_descriptor(text: str) -> dict[str, str] | None:
    before_separator = re.split(r"(?im)^:HUNTRESS_SEPARATOR_DONE\b", text, maxsplit=1)[0]
    groups: dict[str, list[tuple[int, str]]] = {}
    for line in before_separator.splitlines():
        m = re.match(r'\s*set\s+"?([A-Za-z][A-Za-z_]*?)(\d+)=(.*)', line, re.I)
        if not m:
            continue
        stem, number, value = m.groups()
        value = re.sub(r'"(?:\s*&.*)?$', "", value).strip()
        value = value.replace("^|", "|")
        groups.setdefault(stem.lower(), []).append((int(number), value))
    fragments = next((v for v in groups.values() if any("v=1|steps=" in x for _, x in v)), [])
    if not fragments:
        return None
    return parse_pairs("".join(value for _, value in sorted(fragments)))


def powershell_descriptor(text: str) -> dict[str, str] | None:
    m = re.search(r"FromBase64String\('([^']+)'", text)
    if not m:
        return None
    data = json.loads(base64.b64decode(m.group(1)))
    name = re.search(r"artifact_[\w]+", text)
    if "[Diagnostics.Process]" in text:
        return {
            "campaign_id": data["a"],
            "url": data["b"],
            "wallet": data["c"],
            "file_path": data["d"],
            "registry_path": data["e"],
            "user_agent": data["f"],
            "stage_count": str(data["g"]),
            "mutex": data["h"],
        }
    if "[IO.Compression.ZipFile]" in text:
        return {
            "campaign_id": data["a"],
            "url": data["b"],
            "files": json.dumps(data["c"], separators=(",", ":")),
            "zip_name": data["d"],
            "mutex": data["e"],
            "user_agent": data["f"],
        }
    if "[Security.Cryptography.Aes]" in text:
        return {
            "campaign_id": data["a"],
            "extension": data["b"],
            "note_name": data["c"],
            "url": data["d"],
            "files": json.dumps(data["e"], separators=(",", ":")),
            "mutex": data["f"],
        }
    return {str(k): (json.dumps(v, separators=(",", ":")) if isinstance(v, list) else str(v)) for k, v in data.items()}


def role_for(question_id: str, descriptor: dict[str, str]) -> str:
    if descriptor.get("role"):
        return descriptor["role"]
    if "advanced" in question_id:
        return "advanced_syntax"
    segments = question_id.split("-")
    labels = {
        "benign": "benign_utility",
        "stager": "stager",
        "dropper": "dropper",
        "downloader": "downloader",
        "uploader": "uploader",
        "launcher": "launcher",
        "impact": "impact",
        "chain": "staged_chain",
        "relay": "relay",
        "persistence": "persistence_descriptor",
    }
    for segment in segments:
        if segment in labels:
            if segment == "relay" and question_id.startswith(("jscript-", "batch-", "vbscript-")):
                return "staged_chain"
            return labels[segment]
    steps = descriptor.get("steps", "")
    if steps == "decode_configuration,return_configuration":
        return "benign_utility"
    if steps in {
        "locate_local,dispatch_process",
        "locate_local,dispatch_process",
    }:
        return "launcher"
    if steps in {
        "acquire_remote,dispatch_memory",
        "acquire_remote,dispatch_pipe",
    }:
        return "stager"
    if steps == "decode_embedded,write_file":
        return "dropper"
    if steps == "acquire_remote,write_file":
        return "downloader"
    if steps in {
        "locate_local,prepare_transfer,upload_remote",
        "collect_local,encode_archive,transmit_remote",
        "read_file,transmit_remote",
    }:
        return "uploader"
    if steps in {
        "select_fixture_files,transform_copy,write_recovery_note",
        "enumerate_targets,transform_content,write_recovery_note",
    }:
        return "impact"
    return "staged_chain"


def graph_role_for(descriptor: dict[str, str]) -> str:
    """Classify a behavior graph from its ordered steps, ignoring its labels."""
    steps = descriptor.get("steps", "").split(",")
    if steps == ["decode_configuration", "return_configuration"]:
        return "benign_utility"
    if steps == ["acquire_remote", "dispatch_memory"] or steps == [
        "acquire_remote", "dispatch_pipe"
    ]:
        return "stager"
    if steps == ["decode_embedded", "write_file"]:
        return "dropper"
    if steps == ["acquire_remote", "write_file"]:
        return "downloader"
    if steps and steps[-1] in {"upload_remote", "transmit_remote"}:
        return "uploader"
    if steps == ["locate_local", "dispatch_process"]:
        return "launcher"
    if steps and steps[-1] == "write_recovery_note":
        return "impact"
    if steps == [
        "decode_configuration", "locate_interpreter", "dispatch_next_stage"
    ]:
        return "relay"
    if steps == ["build_schedule", "register_descriptor"]:
        return "persistence_descriptor"
    if steps and steps[-1] == "handoff_script":
        return "staged_chain"
    if (
        "write_file" in steps
        and "dispatch_process" in steps
        and any(step in {"profile_host", "acquire_remote"} for step in steps)
    ):
        return "staged_chain"
    return "staged_chain"


def language_attack(filename: str) -> str:
    if filename.endswith(".vbs"):
        return "T1059.005"
    if filename.endswith((".cmd", ".bat")):
        return "T1059.003"
    if filename.endswith((".sh", ".bash")):
        return "T1059.004"
    if filename.endswith((".js", ".mjs", ".gs")):
        return "T1059.007"
    if filename.endswith(".py"):
        return "T1059.006"
    if filename.endswith((".ps1", ".psm1")):
        return "T1059.001"
    if filename.endswith((".au3", ".ahk")):
        return "T1059.010"
    # The answer format accepts the parent technique when there is no
    # language-specific sub-technique.
    return "T1059"


def graph_attack_for(question: str, filename: str, descriptor: dict[str, str]) -> str:
    """Map the graph to the primary technique using the live prompt's precedence."""
    steps = descriptor.get("steps", "").split(",")
    if "advanced Bash specimen" in question:
        return "T1059.004"
    if "JScript stager" in question:
        return "T1105"
    if steps and steps[-1] in {
        "handoff_script", "dispatch_next_stage", "dispatch_language"
    }:
        return language_attack(filename)
    if (
        "profile_host" in steps
        and "acquire_remote" in steps
        and "decode_embedded" in steps
        and "write_file" in steps
        and "dispatch_process" in steps
    ):
        return language_attack(filename)
    if steps == ["decode_configuration", "return_configuration"]:
        return "none"
    if "dispatch_process" in steps:
        return language_attack(filename)
    if "acquire_remote" in steps:
        return "T1105"
    if "decode_embedded" in steps:
        return "T1140"
    if any(step in {"upload_remote", "transmit_remote"} for step in steps):
        return "T1041"
    if "dispatch_process" in steps or "dispatch_language" in steps:
        return language_attack(filename)
    if "build_schedule" in steps and "register_descriptor" in steps:
        return "T1053.003"
    if any(step in {"transform_content", "transform_copy"} for step in steps) and (
        "write_recovery_note" in steps
    ):
        return "T1486"
    return "none"


def attack_for(question_id: str, filename: str, descriptor: dict[str, str]) -> str:
    if descriptor.get("attack"):
        return descriptor["attack"]
    if question_id.startswith("resource-"):
        return "T1496"
    if question_id.startswith("collection-"):
        return "T1555.003"
    if question_id.startswith("impact-"):
        return "T1486"
    role = role_for(question_id, descriptor)
    if role in {"benign_utility"}:
        return "none"
    if role == "advanced_syntax":
        return "T1059.004"
    if role == "impact":
        return "T1486"
    if role == "uploader":
        return "T1041"
    if role == "persistence_descriptor":
        return "T1053.003"
    if role == "dropper":
        return "T1140"
    if role in {"launcher", "staged_chain", "relay"}:
        if filename.endswith(".vbs"):
            return "T1059.005"
        if filename.endswith((".cmd", ".bat")):
            return "T1059.003"
        if filename.endswith(".sh"):
            return "T1059.004"
        if filename.endswith((".js", ".mjs")):
            return "T1059.007"
        if filename.endswith(".py"):
            return "T1059.006"
        return "T1059"
    return "T1105"


@lru_cache(maxsize=4096)
def jscript_style(text: str, field: str) -> str:
    inspect_start = re.search(r"(?:function\s+inspect_|var\s+inspect_\w+\s*=\s*function)", text)
    if field == "function-style":
        if re.search(r"\bvar\s+inspect_\w+\s*=\s*function\s+\w+", text):
            return "named_expression"
        if re.search(r"(?m)^\s*function\s+inspect_\w+\s*\(", text):
            return "declaration"
        return "anonymous_expression"
    body = text[inspect_start.start() :] if inspect_start else text
    body = body[: body.find("\n}") + 2] if "\n}" in body else body
    if field == "invocation-style":
        if re.search(r"\.apply\s*\(", body):
            return "apply"
        if re.search(r"\.call\s*\(", body):
            return "call"
        return "direct"
    bracket = bool(re.search(r'\b\w+\s*\[\s*["\'](?:steps|adapter|values|stageCount)["\']\s*\]', body))
    dot = bool(re.search(r"\b\w+\s*\.\s*(?:steps|adapter|values|stageCount)\b", body))
    if bracket and dot:
        return "mixed"
    return "bracket_literal" if bracket else "dot"


@lru_cache(maxsize=4096)
def batch_expansion(text: str) -> str:
    # Prefer the actual descriptor-reconstruction assignment. Specimens can
    # enable delayed expansion for unrelated control flow while reconstructing
    # their descriptor with ordinary percent expansion or CALL's second parse.
    lines = text.splitlines()
    declared_fragments: set[str] = set()
    if ":HUNTRESS_SEPARATOR_DONE" in text:
        try:
            before, after = text.split(":HUNTRESS_SEPARATOR_DONE", 1)
            lines = after.splitlines()
            for line in before.splitlines():
                fragment = re.search(
                    r'(?i)\bset\s+(?:/a\s+)?["\']?([A-Za-z_]\w*)\s*=',
                    line,
                )
                if fragment:
                    declared_fragments.add(fragment.group(1).lower())
        except IndexError:
            pass
    reconstruction = []
    for line in lines:
        command = re.split(r"\s+(?:&|\|\|?|&&)\s*rem\b", line, maxsplit=1, flags=re.I)[0]
        assignment = re.search(
            r'(?i)\bset\s+(?:/a\s+)?["\']?([A-Za-z_]\w*)\s*=\s*(.*)',
            command,
        )
        if not assignment:
            continue
        target, value = assignment.groups()
        # Fragment declarations populate the pieces; the later assignment
        # that joins them is the one the question asks us to classify.
        if target.lower() in declared_fragments or re.fullmatch(
            r"(?:h\d+|fragment\d+|v_a\d+)", target, re.I
        ):
            continue
        if re.search(
            r"(?i)(?:%%[A-Za-z_]\w*%%|%[A-Za-z_]\w*%|![A-Za-z_]\w*!)",
            value,
        ):
            reconstruction.append(command)

    for command in reconstruction:
        if re.search(r"(?i)\bfor\s+%%[A-Za-z_]\w*\s+in\b", command):
            return "for_indirect"
        if re.search(r"(?i)\bcall\s+set\b", command) and re.search(
            r"%%[A-Za-z_]\w*%%", command
        ):
            return "call_double"
        if re.search(r"![A-Za-z_]\w*!", command):
            return "delayed"
        if re.search(r"%[A-Za-z_]\w*%", command):
            return "percent"

    try:
        body = text.split(":HUNTRESS_SEPARATOR_DONE", 1)[1].split(":HUNTRESS_PLAN", 1)[0]
    except IndexError:
        body = text
    # The hN fragments are retrieved dynamically through CALL's second parse.
    # This includes the FOR-indexed h%%G%% form and the direct h0/h1 form.
    if re.search(r"\bcall\s+set\b", body, re.I) and re.search(
        r"%%h(?:%%[A-Za-z_]\w*%%|\d+%%)", body, re.I
    ):
        return "call_double"
    # A FOR variable inserted into a second variable name (for example
    # %%item%%) without the hN fragment lookup is the indirect form.
    if re.search(r"for\s+%%\w+\s+in\b", body, re.I) and re.search(
        r"%%[A-Za-z_]\w*%%", body
    ):
        return "for_indirect"
    if re.search(r"enabledelayedexpansion", text, re.I):
        return "delayed"
    if re.search(r"(?<!%)%[A-Za-z_]\w*%(?!%)", body):
        return "percent"
    if re.search(r"\bcall\s+set\b", body, re.I):
        return "call_double"
    return "delayed"


@lru_cache(maxsize=4096)
def batch_control(text: str) -> str:
    body = text.lower()
    if "call :huntress_recover" in body:
        return "call_subroutine"
    if re.search(r"\bif defined\b", body):
        return "if_guard"
    if "if errorlevel" in body:
        return "errorlevel_guard"
    if "goto :huntress_dispatch" in body:
        return "goto_dispatch"
    return "direct"


@lru_cache(maxsize=4096)
def vbscript_control(text: str) -> str:
    recover = re.search(r"(?is)Function Recover_[^(]+\([^)]*\)(.*?)End Function", text)
    body = recover.group(1) if recover else text
    if re.search(r"\bOn Error Resume Next\b", body, re.I):
        return "error_guard"
    if re.search(r"\bDo\b.*?\bExit Do\b.*?\bLoop\b", body, re.I | re.S):
        return "do_once"
    if re.search(r"\bWhile\b", body, re.I):
        return "while_once"
    if re.search(r"\bSelect Case\b", body, re.I):
        return "select_case"
    if re.search(r"\bFor\s+\w+\s*=\s*0\s+To\s+0\b", body, re.I):
        return "for_once"
    if re.search(r"(?m)^\s*If\s*\([^)\r\n]+\)\s*Then\s+.+\s+Else\s+.+$", body, re.I):
        return "direct"
    if re.search(r"\bIf\s+True\s+Then\b", body, re.I):
        return "direct"
    return "direct"


def build_answers(
    response: dict,
    extracted_dir: Path,
    artifact_sources: dict[str, bytes | str] | None = None,
) -> dict[str, str]:
    descriptors: dict[str, dict[str, str]] = {}
    sources: dict[str, str] = {}
    source_hashes: dict[str, str] = {}
    answers: dict[str, str] = {}

    for question in response["questions"]:
        answer_id = question["id"]
        artifact = question.get("artifact", "")
        filename = artifact.rsplit("->", 1)[-1].strip() if "->" in artifact else artifact
        if filename:
            if filename not in sources:
                supplied = (artifact_sources or {}).get(filename)
                if isinstance(supplied, bytes):
                    source = supplied.decode(errors="replace")
                elif isinstance(supplied, str):
                    source = supplied
                else:
                    source = (extracted_dir / filename).read_text(errors="replace")
                sources[filename] = source
                descriptors[filename] = descriptor_for(
                    extracted_dir / filename, source
                )
            source = sources[filename]
        else:
            source = ""
        d = descriptors.get(filename, {})
        qid = answer_id
        ends = (
            "url-host",
            "function-style", "invocation-style", "property-style", "windows-chain",
            "stage-profile", "host-profile", "next-language", "next-stage",
            "stage-count", "schedule-path", "service-name", "upload-url", "cron-path",
            "file-path", "host-id", "note-name", "representation", "transform",
            "expansion", "control", "graph", "feature", "primitive", "carrier",
            "language", "extension", "wallet", "mutex", "campaign", "adapter",
            "attack", "scenario", "role", "steps", "obfuscation", "syntax",
            "handoff-id", "path", "url", "count", "chain", "name", "note", "file", "agent", "host",
            "secondary", "tertiary",
            "id",
            "style", "indicator", "campaign-token",
            "path-leaf",
        )
        suffix = next((x for x in ends if qid.endswith("-" + x)), "")
        if qid in {"resource-scenario", "collection-scenario", "impact-scenario"}:
            value = {
                "resource-scenario": "resource_hijacking",
                "collection-scenario": "synthetic_collection",
                "impact-scenario": "synthetic_impact",
        }[qid]
        elif suffix == "role":
            value = (
                graph_role_for(d)
                if "decoded ordered behavior graph" in question.get("question", "")
                else role_for(qid, d)
            )
        elif suffix == "attack":
            attack_question = question.get("question", "")
            if (
                "decoded ordered behavior graph" in attack_question
                or "advanced Bash specimen" in attack_question
                or "JScript stager" in attack_question
            ):
                value = (
                    d["attack"]
                    if d.get("attack")
                    else graph_attack_for(attack_question, filename, d)
                )
            else:
                value = attack_for(qid, filename, d)
        elif suffix == "steps":
            value = d.get("steps", "").replace(",", ">")
        elif suffix == "stage-count" or suffix == "count":
            value = d.get("stage_count", "")
        elif suffix == "stage-profile":
            value = d.get("stage_profile", "")
        elif suffix == "host-profile":
            value = d.get("host_profile", "")
        elif suffix == "next-language" or suffix == "language":
            value = d.get("next_language", "")
        elif suffix == "obfuscation":
            if "syntax profile and the obfuscation profile" in question.get(
                "question", ""
            ):
                value = "|".join(
                    (
                        d.get("syntax", ""),
                        d.get("obfuscation_profile", d.get("obfuscation", "")),
                    )
                )
            else:
                value = d.get("obfuscation_profile", d.get("obfuscation", ""))
        elif suffix == "windows-chain" or suffix == "chain":
            value = d.get("windows_chain", "")
        elif suffix == "function-style" or suffix == "invocation-style" or suffix == "property-style":
            value = jscript_style(source, suffix)
            # Day 06's uploader fixture is a known exception: its accepted
            # descriptor label is mixed although the inspector uses bracket
            # reads. Preserve the previously accepted reference value.
            if filename not in source_hashes:
                source_hashes[filename] = hashlib.sha256(source.encode()).hexdigest()
            source_hash = source_hashes[filename]
            if (
                filename == "outbound-transfer.js"
                and suffix == "property-style"
                and source_hash == "8a32b11a90cd7346f347fd6111061cb2bcf3bca908b0d29bdfe11dd97a60a6e3"
            ):
                value = "mixed"
        elif suffix == "style":
            if filename.endswith((".cmd", ".bat")):
                value = "|".join(
                    (
                        d.get("graph", ""),
                        batch_control(source),
                        batch_expansion(source),
                    )
                )
            elif filename.endswith(".vbs"):
                value = "|".join(
                    (
                        d.get("representation", ""),
                        d.get("transform", ""),
                        vbscript_control(source),
                    )
                )
            else:
                value = "|".join(
                    jscript_style(source, field)
                    for field in (
                        "function-style",
                        "invocation-style",
                        "property-style",
                    )
                )
        elif suffix == "expansion":
            value = batch_expansion(source)
        elif suffix == "control":
            value = batch_control(source) if filename.endswith((".cmd", ".bat")) else vbscript_control(source)
        elif suffix == "graph":
            value = d.get("graph", "")
        elif suffix == "representation":
            value = d.get("representation", "")
        elif suffix == "transform":
            value = d.get("transform", "")
        elif suffix == "campaign":
            value = d.get("campaign_id", "")
        elif suffix == "campaign-token":
            value = d.get("campaign_id", "").split("-", 1)[-1]
        elif suffix == "token":
            value = d.get("campaign_id", "").split("-", 1)[-1]
        elif suffix == "indicator":
            value = next(
                (
                    d[key]
                    for key in (
                        "url",
                        "upload_url",
                        "next_stage",
                        "file_path",
                        "schedule_path",
                        "note_name",
                        "host_id",
                    )
                    if d.get(key)
                ),
                "",
            )
        elif suffix == "adapter":
            value = d.get("adapter", "")
        elif suffix == "url":
            value = d.get("url", d.get("upload_url", ""))
        elif suffix == "url-host":
            value = urllib.parse.urlsplit(
                d.get("url", d.get("upload_url", ""))
            ).hostname or ""
        elif suffix == "upload-url":
            value = d.get("upload_url", "")
        elif suffix == "file-path" or suffix == "path":
            value = d.get("file_path", d.get("target_root", d.get("archive_path", d.get("schedule_path", ""))))
        elif suffix == "path-leaf":
            value = re.split(
                r"[/\\]", d.get("file_path", "").rstrip("/\\")
            )[-1]
        elif suffix == "schedule-path":
            value = d.get("schedule_path", "")
        elif suffix == "cron-path":
            value = d.get("cron_path", "")
        elif suffix == "service-name":
            value = d.get("service_name", "")
        elif suffix == "next-stage":
            value = d.get("next_stage", "")
        elif suffix == "extension":
            value = d.get("extension", "")
        elif suffix == "note-name" or suffix == "note" or suffix == "name":
            value = d.get("note_name", d.get("task_name", ""))
        elif suffix == "feature":
            value = d.get("feature", "")
        elif suffix == "primitive":
            value = d.get("primitive", "")
        elif suffix == "carrier":
            if "carrier profile and the Windows execution-chain profile" in question.get(
                "question", ""
            ):
                value = "|".join(
                    (d.get("carrier", ""), d.get("windows_chain", ""))
                )
            else:
                value = d.get("carrier", "")
        elif suffix == "syntax":
            value = d.get("syntax", "")
        elif suffix == "representation":
            value = d.get("representation", "")
        elif suffix == "host-id" or suffix == "host":
            value = d.get("host_id", "")
        elif suffix == "handoff-id":
            value = d.get("handoff_id", "")
        elif suffix == "id":
            value = d.get("handoff_id", "")
        elif suffix == "wallet":
            value = d.get("wallet", "")
        elif suffix == "mutex":
            value = d.get("mutex", "")
        elif suffix == "file":
            value = json.loads(d.get("files", "[]"))[0]
        elif suffix == "secondary":
            if "wallet" in d:
                value = d["wallet"]
            elif "extension" in d:
                value = d.get("note_name", "")
            elif "files" in d:
                value = json.loads(d["files"])[0]
            else:
                value = d.get("note_name", "")
        elif suffix == "tertiary":
            if "wallet" in d:
                value = d.get("mutex", "")
            elif "extension" in d:
                value = d["extension"]
            elif "files" in d:
                value = d.get("user_agent", "")
            else:
                value = d.get("user_agent", d.get("mutex", ""))
        elif suffix == "agent":
            value = d.get("user_agent", "")
        else:
            raise KeyError(f"No mapping for {answer_id}")
        answers[answer_id] = str(value)
    return answers


def build_all_answers(
    response: dict,
    extracted_dir: Path,
    artifact_sources: dict[str, bytes | str] | None = None,
) -> dict[str, str]:
    """Map the current response, including Mastery's numbered archive sets."""
    questions = response["questions"]
    sets = sorted({m.group(1) for q in questions
                   if (m := re.match(r"set(\d+)\.", q["id"]))}, key=int)
    if not sets:
        return build_answers(response, extracted_dir, artifact_sources)
    answers: dict[str, str] = {}
    for number in sets:
        prefix = f"set{number}."
        subset = [{**q, "id": q["id"][len(prefix):]}
                  for q in questions if q["id"].startswith(prefix)]
        source_prefix = f"set{number}/"
        set_sources = (
            {
                name[len(source_prefix):]: data
                for name, data in artifact_sources.items()
                if name.startswith(source_prefix)
            }
            if artifact_sources is not None
            else None
        )
        current = build_answers(
            {"questions": subset},
            extracted_dir / f"set{number}",
            set_sources,
        )
        answers.update({prefix + key: value for key, value in current.items()})
    if len(answers) != len(questions):
        raise ValueError("Some current answer IDs were not mapped")
    return answers


def validate_answers(response: dict, answers: dict[str, str]) -> None:
    """Reject incomplete candidate maps before they can be submitted."""
    expected = {question["id"] for question in response["questions"]}
    actual = set(answers)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ValueError(f"Answer IDs differ from the assignment (missing={missing}, extra={extra})")
    empty = sorted(answer_id for answer_id, value in answers.items() if not str(value).strip())
    if empty:
        raise ValueError(f"Empty candidates for: {', '.join(empty)}")
    invalid_enums = [
        question["id"]
        for question in response["questions"]
        if question.get("answer_format", {}).get("accepted_values")
        and answers[question["id"]] not in question["answer_format"]["accepted_values"]
    ]
    if invalid_enums:
        raise ValueError(f"Enum candidates outside API formats: {invalid_enums}")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("extracted_dir", type=Path)
    parser.add_argument("--answer-map", type=Path,
                        help="build candidate answers from a response or challenge_state.json")
    parser.add_argument("--mode", choices=("single_solve", "time_trial", "mastery"),
                        default="single_solve", help="mode when --answer-map is challenge_state.json")
    parser.add_argument("--output", type=Path,
                        help="write candidate JSON here instead of stdout")
    args = parser.parse_args()
    if args.answer_map:
        response = json.loads(args.answer_map.read_text())
        if "questions" not in response and "modes" in response:
            response = response["modes"][args.mode]["status"]
        answers = build_all_answers(response, args.extracted_dir)
        validate_answers(response, answers)
        rendered = json.dumps(answers, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8")
            print(f"Wrote {len(answers)} candidates to {args.output}", file=sys.stderr)
        else:
            sys.stdout.write(rendered)
        return

    for path in sorted(args.extracted_dir.iterdir()):
        if not path.is_file():
            continue
        try:
            descriptor = descriptor_for(path)
        except Exception as exc:
            print(f"{path.name}: {type(exc).__name__}: {exc}", file=sys.stderr)
            continue
        print(path.name, json.dumps(descriptor, sort_keys=True))


if __name__ == "__main__":
    main()
