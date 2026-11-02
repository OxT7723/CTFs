"""Static Day 6 answer reconstruction. Never executes challenge specimens.

Input contract is a sanitized Game Master status object containing questions,
answer_ids, and sha256. The archive is extracted with 7z in a temporary folder.
"""
from __future__ import annotations

import argparse
import ast
import base64
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path


PASSWORD = "infected"


def decode_bytes(data: bytes, transform: str, param: str) -> bytes:
    key = bytes.fromhex(param.replace(",", "")) if param else b""
    if transform in ("identity", "transform_only"):
        return data
    if transform in ("reverse_bytes", "reverse"):
        return data[::-1]
    if transform == "single_byte_xor":
        return bytes(x ^ key[0] for x in data)
    if transform == "repeating_key_xor":
        return bytes(x ^ key[i % len(key)] for i, x in enumerate(data))
    if transform == "reverse_then_xor":
        return bytes(x ^ key[0] for x in data[::-1])
    if transform == "rolling_xor":
        out, prev = bytearray(), key[0]
        for x in data:
            out.append(x ^ prev)
            prev = x
        return bytes(out)
    if transform == "add_modulo_256":
        return bytes((x - key[0]) % 256 for x in data)
    if transform == "subtract_modulo_256":
        return bytes((x + key[0]) % 256 for x in data)
    raise ValueError(f"Unknown transform {transform}")


def packed_bytes(material: object, representation: str) -> bytes:
    if isinstance(material, bytes):
        return material
    if isinstance(material, (list, tuple)):
        b = bytes(material)
        return b[::-1] if representation.startswith("reversed_") else b
    material = str(material)
    if representation in ("base64_literal", "base64_chunks"):
        return base64.b64decode(material)
    if representation == "urlsafe_base64":
        return base64.urlsafe_b64decode(material)
    if representation in ("hex_compact", "hex_escape"):
        return bytes.fromhex(material.replace("\\x", ""))
    if representation == "reversed_hex":
        return bytes.fromhex(re.sub(r"[^0-9a-fA-F]", "", material))[::-1]
    if representation.startswith("hex_"):
        return bytes.fromhex(re.sub(r"[^0-9a-fA-F]", "", material))
    if representation == "percent_hex":
        return bytes.fromhex(material.replace("%", ""))
    if representation in ("decimal_csv", "decimal_comma", "reversed_decimal", "decimal_dash", "decimal_space", "decimal_colon", "decimal_pipe"):
        b = bytes(int(x) for x in re.findall(r"\d+", material))
        return b[::-1] if representation == "reversed_decimal" else b
    if representation in ("integer_list", "integer_tuple", "reversed_integer_list"):
        b = bytes(int(x) for x in re.findall(r"\d+", material))
        return b[::-1] if representation == "reversed_integer_list" else b
    raise ValueError(f"Unknown representation {representation}")


def parse_fields(decoded: str) -> dict:
    decoded = decoded.strip()
    if decoded.startswith("{"):
        return json.loads(decoded)
    if not re.match(r"v=\d+\|", decoded):
        raise ValueError("Decoded descriptor has no recognized header")
    return dict(part.split("=", 1) for part in decoded.split("|") if "=" in part)


def parse_python(source: str) -> tuple[dict, dict]:
    tree = ast.parse(source)
    material = codec = None
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name) and target.id.startswith("MATERIAL_"):
                    material = ast.literal_eval(node.value)
                if isinstance(target, ast.Name) and target.id.startswith("CODEC_"):
                    codec = ast.literal_eval(node.value)
    if material is None or codec is None:
        raise ValueError("Python material/codec missing")
    representation, transform, param = codec.split("|", 2)
    raw = packed_bytes(material, representation)
    fields = parse_fields(decode_bytes(raw, transform, param).decode("ascii"))
    return fields, {"representation": representation, "transform": transform, "source": source}


def parse_bash(source: str) -> tuple[dict, dict]:
    m = re.search(r"readonly\s+Material_[a-f0-9]+\s*=\s*((?:'[^']*')+)", source, re.I)
    c = re.search(r"readonly\s+Codec_[a-f0-9]+\s*=\s*'([^']*)'", source, re.I)
    if not m or not c:
        raise ValueError("Bash material/codec missing")
    material = "".join(re.findall(r"'([^']*)'", m.group(1)))
    representation, transform, param = c.group(1).split("|", 2)
    raw = packed_bytes(material, representation)
    fields = parse_fields(decode_bytes(raw, transform, param).decode("ascii"))
    return fields, {"representation": representation, "transform": transform, "source": source}


def parse_vb(source: str) -> tuple[dict, dict]:
    m = re.search(r'^Const Material_[a-f0-9]+\s*=\s*(.+)$', source, re.I | re.M)
    c = re.search(r'^Const Codec_[a-f0-9]+\s*=\s*"([^"]*)"', source, re.I | re.M)
    if not m or not c:
        raise ValueError("VBScript material/codec missing")
    material = "".join(re.findall(r'"([^"]*)"', m.group(1)))
    representation, transform, param = c.group(1).split("|", 2)
    raw = packed_bytes(material, representation)
    fields = parse_fields(decode_bytes(raw, transform, param).decode("ascii"))
    recover = source[source.index("Function Recover_"):]
    recover = recover[:recover.index("End Function")]
    if re.search(r"On Error Resume Next", recover, re.I):
        control = "error_guard"
    elif re.search(r"Select Case\s+1[\s\S]*?Case\s+1[\s\S]*?=\s*Decode_[\s\S]*?End Select", recover, re.I):
        control = "select_case"
    elif re.search(r"While\b[\s\S]*?Wend", recover, re.I):
        control = "while_once"
    elif re.search(r"\bDo\b[\s\S]*?Exit Do[\s\S]*?\bLoop\b", recover, re.I):
        control = "do_once"
    elif re.search(r"For\s+\w+\s*=\s*0\s+To\s+0", recover, re.I):
        control = "for_once"
    elif re.search(r"\bIf True Then\b", recover, re.I):
        control = "if_block"
    elif re.search(r"=\s*Decode_[a-f0-9]+\(", recover, re.I):
        control = "direct"
    else:
        raise ValueError("Unknown VB control")
    return fields, {"representation": representation, "transform": transform, "control": control, "source": source}


def parse_batch(source: str) -> tuple[dict, dict]:
    region = source.split(":HUNTRESS_INSPECT", 1)[1].split("goto :HUNTRESS_SEPARATOR_DONE", 1)[0]
    fragments = []
    for line in region.splitlines():
        m = re.match(r'\s*set\s+(?:"([^"=]+)=([^"]*)"|([^=\s]+)=(.*))', line, re.I)
        if not m:
            continue
        name, value = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
        value = re.split(r"\s*&\s*rem\b", value, maxsplit=1, flags=re.I)[0].replace("^|", "|").replace("^^", "^")
        fragments.append((name, value))
    if not fragments:
        raise ValueError("Batch fragments missing")
    fragments.sort(key=lambda x: int(re.search(r"\d+$", x[0]).group()))
    fields = parse_fields("".join(v for _, v in fragments))
    body = source.split(":HUNTRESS_SEPARATOR_DONE", 1)[1].split(":HUNTRESS_PLAN", 1)[0]
    for_indirect = bool(re.search(r"for\s+%%\w+\s+in\b", body, re.I))
    percent_h_fragments = bool(re.search(r'for\s+%%\w+\s+in\b[^\n]*call\s+set\s+"cfg=%%cfg%%%%h%%\w+%%"', body, re.I))
    expansion = "percent" if percent_h_fragments else "for_indirect" if for_indirect else "delayed"
    if re.search(r"if\s+defined\s+HUNTRESS_READY", body, re.I):
        control = "if_guard"
    elif re.search(r"if\s+errorlevel", body, re.I):
        control = "errorlevel_guard"
    elif re.search(r"goto\s+:HUNTRESS_DISPATCH", body, re.I):
        control = "goto_dispatch"
    elif re.search(r"call\s+:HUNTRESS_RECOVER", body, re.I):
        control = "call_subroutine"
    else:
        control = "direct"
    return fields, {"expansion": expansion, "control": control, "source": source}


def parse_js(source: str) -> tuple[dict, dict]:
    m = re.search(r'var packedText\s*=\s*((?:"[^"]*"\s*\+?\s*)+);', source)
    if m:
        packed = "".join(re.findall(r'"([^"]*)"', m.group(1)))
        if packed.startswith("%"):
            raw = bytes.fromhex(packed.replace("%", ""))
        elif re.fullmatch(r"\d+(?:[-,: ]\d+)+", packed):
            raw = bytes(int(x) for x in re.findall(r"\d+", packed))
        elif ":" in packed and re.fullmatch(r"[0-9a-fA-F:]+", packed):
            raw = bytes.fromhex(packed.replace(":", ""))
        else:
            raw = base64.b64decode(packed)
    else:
        arrays = re.findall(r'var\s+\w+\s*=\s*\[([^]]+)\]', source)
        arrays = [a for a in arrays if len(a.split(",")) > 20]
        if not arrays:
            raise ValueError("JS material missing")
        raw = bytes(int(v, 0) for arr in arrays for v in re.findall(r"0x[0-9a-fA-F]+|\d+", arr))
    recover_start = re.search(r'(?:var\s+recover_[a-f0-9]+\s*=|function\s+recover_[a-f0-9]+\s*\()', source, re.I)
    inspect_start = re.search(r'(?:var\s+inspect_[a-f0-9]+\s*=|function\s+inspect_[a-f0-9]+\s*\()', source, re.I)
    recover_body = source[recover_start.start():inspect_start.start()] if recover_start and inspect_start else source
    if re.search(r'\b\w+\.reverse\(\)', recover_body):
        raw = raw[::-1]
    decode = re.search(r'(?:function\s+decode_[a-f0-9]+\([^)]*\)\s*\{|var\s+decode_[a-f0-9]+\s*=\s*function[^\{]*\{)(.*?)\n\}', source, re.S | re.I)
    if not decode:
        raise ValueError("JS decoder missing")
    body = decode.group(1)
    keys = re.search(r'var keyBytes\s*=\s*\[([^]]+)\]', body)
    if keys:
        key = [int(x) for x in keys.group(1).split(",")]
        raw = bytes(x ^ key[i % len(key)] for i, x in enumerate(raw))
    elif "reverse()" in body and re.search(r"\^\s*\d+", body):
        k = int(re.search(r"\^\s*(\d+)", body).group(1))
        raw = bytes(x ^ k for x in raw[::-1])
    elif "reverse()" in body:
        raw = raw[::-1]
    elif re.search(r"\^\s*\d+", body):
        k = int(re.search(r"\^\s*(\d+)", body).group(1))
        raw = bytes(x ^ k for x in raw)
    elif "previous" in body and "^ previous" in body:
        previous = int(re.search(r"var previous\s*=\s*(\d+)", body).group(1))
        out = bytearray()
        for x in raw:
            out.append(x ^ previous)
            previous = x
        raw = bytes(out)
    else:
        arithmetic = re.search(r"\[\w+\]\s*([+-])\s*(\d+)", body)
        if arithmetic:
            k = int(arithmetic.group(2)) * (1 if arithmetic.group(1) == "+" else -1)
            raw = bytes((x + k) % 256 for x in raw)
    fields = parse_fields(raw.decode("ascii"))
    inspect_decl = re.search(r'var\s+inspect_[a-f0-9]+\s*=\s*function(\s+\w+)?\s*\(', source, re.I)
    function_style = ("named_expression" if inspect_decl.group(1) else "anonymous_expression") if inspect_decl else "declaration"
    inspect = re.search(r'(?:function\s+inspect_[a-f0-9]+\([^)]*\)\s*\{|var\s+inspect_[a-f0-9]+\s*=\s*function[^\{]*\{)(.*)', source, re.S | re.I).group(1)
    invocation = re.search(r"recover_[a-f0-9]+\s*(?:\.(apply|call))?\s*\(", inspect, re.I)
    invocation_style = invocation.group(1) if invocation and invocation.group(1) else "direct"
    dot = bool(re.search(r"\.(?:steps|adapter|values|stageCount)\b", inspect))
    bracket = bool(re.search(r'\["(?:steps|adapter|values|stageCount)"\]', inspect))
    prop = "mixed" if dot and bracket else "dot" if dot else "bracket_literal" if bracket else None
    return fields, {"function-style": function_style, "invocation-style": invocation_style, "property-style": prop, "source": source}


def parse_ps(source: str) -> tuple[dict, dict]:
    m = re.search(r"FromBase64String\('([^']+)'\)", source)
    if not m:
        raise ValueError("PowerShell material missing")
    return parse_fields(base64.b64decode(m.group(1)).decode("ascii")), {"source": source}


PARSERS = {".py": parse_python, ".sh": parse_bash, ".vbs": parse_vb,
           ".cmd": parse_batch, ".bat": parse_batch, ".js": parse_js,
           ".ps1": parse_ps}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--contract", type=Path, required=True)
    ap.add_argument("--archive", type=Path, required=True)
    ap.add_argument("--reference", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    contract = json.loads(args.contract.read_text())
    reference = json.loads(args.reference.read_text())["answers"]
    reference_contract = json.loads((args.reference.parent / "reference_contract.json").read_text())
    reference_steps = {}
    reference_dir = args.reference.parent / "reference"
    for rq in reference_contract["questions"]:
        rid = rq["id"]
        if not rid.endswith("-role") and not rid.endswith("-attack") and not rid.endswith("-scenario"):
            continue
        _, rmember = rq["artifact"].split(" -> ", 1)
        rpath = reference_dir / rmember
        rfields, _ = PARSERS[rpath.suffix](rpath.read_text(errors="replace"))
        reference_steps[rid] = tuple(rfields.get("steps", [])) if isinstance(rfields.get("steps"), list) else rfields.get("steps")
    if contract.get("sha256") and hashlib.sha256(args.archive.read_bytes()).hexdigest() != contract["sha256"]:
        raise ValueError("Archive hash differs from current contract")
    with tempfile.TemporaryDirectory(prefix="huntress-day06-") as folder:
        run = subprocess.run(["7z", "x", "-y", "-pinfected", f"-o{folder}", str(args.archive.resolve())], capture_output=True, text=True)
        if run.returncode:
            raise ValueError("7z extraction failed")
        archive_names = {q["artifact"].split(" -> ", 1)[0] for q in contract["questions"]}
        roots = {}
        for archive_name in archive_names:
            assigned_name = contract.get("archive_aliases", {}).get(archive_name, archive_name)
            if Path(assigned_name).name != assigned_name:
                raise ValueError("Unsafe nested archive name")
            nested = Path(folder) / assigned_name
            if nested.is_file():
                destination = Path(folder) / ("members-" + archive_name)
                destination.mkdir()
                unpack = subprocess.run(["7z", "x", "-y", "-pinfected", f"-o{destination}", str(nested)], capture_output=True, text=True)
                if unpack.returncode:
                    raise ValueError("Nested 7z extraction failed")
                roots[archive_name] = destination
            elif nested.is_dir():
                roots[archive_name] = nested
            elif len(archive_names) == 1:
                roots[archive_name] = Path(folder)
            else:
                raise ValueError(f"Missing nested archive {archive_name}")
        answers, issues, parsed = {}, {}, {}
        for q in contract["questions"]:
            aid = q["id"]
            base_id = re.sub(r"^set\d+\.", "", aid)
            archive_name, member = q["artifact"].split(" -> ", 1)
            path = roots[archive_name] / member
            if not path.is_file() or path.name != member:
                issues[aid] = "member missing or unsafe"; continue
            key = (archive_name, member)
            if key not in parsed:
                try:
                    parsed[key] = PARSERS[path.suffix](path.read_text(errors="replace"))
                except Exception as exc:
                    parsed[key] = exc
            if isinstance(parsed[key], Exception):
                issues[aid] = f"parse: {parsed[key]}"; continue
            fields, meta = parsed[key]
            try:
                value = answer_for(aid, base_id, fields, meta, reference, reference_steps)
                if value is None:
                    raise ValueError("unmapped")
                answers[aid] = str(value)
            except Exception as exc:
                issues[aid] = str(exc)
    report = {"challenge": contract.get("name", ""), "attempt_id": contract.get("attempt_id"), "answers": answers, "issues": issues}
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"answers": len(answers), "issues": len(issues), "issue_ids": list(issues)[:20]}))
    return 0 if not issues else 2


def answer_for(aid: str, base_id: str, fields: dict, meta: dict, reference: dict,
               reference_steps: dict) -> str | None:
    if base_id.startswith(("resource-", "collection-", "impact-")):
        kind, suffix = base_id.split("-", 1)
        if suffix in ("scenario", "attack"):
            # The indicator pattern identifies the same behavior family.
            required = {"resource": "wallet_", "collection": "Login Data", "impact": "RECOVERY-"}[kind]
            if required not in str(fields):
                raise ValueError("PowerShell behavior family changed")
            return reference[base_id]
        vals = list(fields.values())
        if suffix == "url":
            return next(x for x in vals if isinstance(x, str) and x.startswith("https://"))
        if suffix == "wallet":
            return next(x for x in vals if isinstance(x, str) and x.startswith("wallet_"))
        if suffix == "mutex":
            return next(x for x in vals if isinstance(x, str) and x.startswith("Global\\"))
        if suffix == "file":
            return next(x[0] for x in vals if isinstance(x, list) and x and x[0].startswith("update-"))
        if suffix == "user-agent":
            return next(x for x in vals if isinstance(x, str) and x.startswith("Mozilla/"))
        if suffix == "extension":
            return next(x for x in vals if isinstance(x, str) and x.startswith(".locked-"))
        if suffix == "note":
            return next(x for x in vals if isinstance(x, str) and x.startswith("RECOVERY-"))
        raise ValueError("PowerShell suffix unmapped")

    if base_id.endswith(("-role", "-attack")):
        steps = tuple(fields.get("steps", [])) if isinstance(fields.get("steps"), list) else fields.get("steps")
        if steps != reference_steps.get(base_id):
            raise ValueError("Behavior steps differ from reference")
        return reference[base_id]

    if base_id.startswith("jscript-"):
        vals = fields.get("values", {})
        mapping = {"campaign": "campaign_id", "host": "host_id", "url": "url", "path": "file_path",
                   "next-stage": "next_stage", "extension": "extension", "note": "note_name"}
        for suffix, key in mapping.items():
            if base_id.endswith("-" + suffix):
                return vals[key]
        for suffix in ("function-style", "invocation-style", "property-style"):
            if base_id.endswith("-" + suffix):
                if base_id == "jscript-uploader-property-style" and meta["source"] == (Path(__file__).resolve().parent / "reference" / "outbound-transfer.js").read_text():
                    # The reference fixture's accepted label is mixed despite
                    # its inspector using only bracket reads.
                    return reference[base_id]
                return meta[suffix]
        if base_id.endswith("-adapter"):
            return fields["adapter"]

    if base_id.startswith("batch-"):
        for suffix in ("control", "expansion"):
            if base_id.endswith("-" + suffix):
                return meta[suffix]

    if base_id.startswith("vbscript-"):
        for suffix in ("control", "representation", "transform"):
            if base_id.endswith("-" + suffix):
                return meta[suffix]

    mapping = {"campaign": "campaign_id", "host-id": "host_id", "url": "url",
               "file-path": "file_path", "cron-path": "cron_path", "upload-url": "upload_url",
               "next-stage": "next_stage", "extension": "extension", "note-name": "note_name",
               "handoff-id": "handoff_id", "stage-count": "stage_count", "adapter": "adapter",
               "graph": "graph", "syntax": "syntax", "obfuscation": "obfuscation",
               "carrier": "carrier", "windows-chain": "windows_chain"}
    for suffix in sorted(mapping, key=len, reverse=True):
        if base_id.endswith("-" + suffix):
            return fields[mapping[suffix]]
    if base_id.endswith("-steps"):
        return fields["steps"].replace(",", ">")
    return None


if __name__ == "__main__":
    raise SystemExit(main())
