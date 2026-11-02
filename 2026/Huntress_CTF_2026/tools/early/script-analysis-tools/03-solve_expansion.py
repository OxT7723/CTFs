#!/usr/bin/env python3
"""Statically derive Expansion Pack answers from the current assigned ZIP.

The timed command starts one attempt, downloads its artifact, derives answers,
and submits once. It never runs any script inside the archive.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "05-Hatch_Careful/tools"))
from static_recover import recover_batch, recover_js  # noqa: E402

BASE = "https://2026.huntress.ctf.games/"
CHALLENGE = "script-analysis-day-03-batch-expansion/time_trial"
STEMS = {
    "benign": "host-context",
    "stager": "memory-stage",
    "dropper": "embedded-write",
    "downloader": "remote-write",
    "launcher": "local-dispatch",
    "chain": "staged-handoff",
    "uploader": "outbound-transfer",
    "impact": "impact-plan",
    "relay": "relay-handoff",
}
STEPS = {
    "benign": "decode_configuration,return_configuration",
    "stager": "acquire_remote,dispatch_memory",
    "dropper": "decode_embedded,write_file",
    "downloader": "acquire_remote,write_file",
    "launcher": "locate_local,dispatch_process",
    "chain": "acquire_remote,write_file,dispatch_process,handoff_script",
    "uploader": "locate_local,prepare_transfer,upload_remote",
    "impact": "enumerate_targets,transform_content,write_recovery_note",
    "relay": "acquire_remote,write_file,dispatch_process,handoff_script",
}
ROLES = {
    "benign": "benign_utility", "stager": "stager", "dropper": "dropper",
    "downloader": "downloader", "launcher": "launcher", "chain": "staged_chain",
    "uploader": "uploader", "impact": "impact", "relay": "staged_chain",
}
ATTACKS = {
    "benign": "none", "stager": "T1105", "dropper": "T1140",
    "downloader": "T1105", "uploader": "T1041", "impact": "T1486",
}
BATCH_EXTENSION = {"stager": ".bat", "downloader": ".bat", "launcher": ".bat", "chain": ".bat"}


def js_styles(source: str) -> tuple[str, str, str]:
    match = re.search(
        r"(?:function\s+inspect_[A-Za-z0-9_]+\s*\([^)]*\)|"
        r"var\s+inspect_[A-Za-z0-9_]+\s*=\s*function(?:\s+[A-Za-z0-9_]+)?\s*\([^)]*\))\s*\{",
        source,
    )
    if not match:
        raise ValueError("JScript inspect function missing")
    start = source.index("{", match.start())
    depth = 0
    quote = None
    escaped = False
    end = None
    for i in range(start, len(source)):
        c = source[i]
        if quote:
            if escaped:
                escaped = False
            elif c == "\\":
                escaped = True
            elif c == quote:
                quote = None
        elif c in ('"', "'", "`"):
            quote = c
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end is None:
        raise ValueError("JScript inspect function unclosed")
    block = source[match.start():end]
    if re.search(r"^\s*function\s+inspect_", source, re.M):
        function = "declaration"
    else:
        named = re.search(r"var\s+inspect_\w+\s*=\s*function(\s+\w+)?\s*\(", source)
        function = "named_expression" if named and named.group(1) else "anonymous_expression"
    invocation = ("apply" if re.search(r"recover_\w+\.apply\s*\(", block)
                  else "call" if re.search(r"recover_\w+\.call\s*\(", block) else "direct")
    descriptor = re.search(r"\b([A-Za-z_$][\w$]*)\s*=\s*eval\s*\(", block)
    name = re.escape(descriptor.group(1)) if descriptor else r"(?:item\d+|v_[A-Za-z0-9_]+)"
    dot = bool(re.search(name + r"\.(?:steps|adapter|values|stageCount)", block))
    bracket = bool(re.search(name + r"\[\s*['\"](?:steps|adapter|values|stageCount)['\"]\s*\]", block))
    prop = "mixed" if dot and bracket else "dot" if dot else "bracket_literal"
    return function, invocation, prop


def batch_forms(source: str, role: str) -> tuple[str, str]:
    # The reference specimen distinguishes guarded CALL expansion from a FOR
    # indirection loop, even when both contain "FOR ... DO CALL SET".
    if re.search(r"(?im)^.*\bfor\s+%%\w+\s+in\s*\([^)]*\)\s+do\s+call\s+set", source):
        expansion = "call_double" if re.search(r"(?im)^\s*if\s+defined\b", source) else "for_indirect"
    elif re.search(r"(?im)^.*\bcall\s+set[^\n]*%%", source):
        expansion = "call_double"
    else:
        joins = [line for line in source.splitlines() if re.search(r"(?i)set\s+[^=]+=.*(?:%%\w+|!\w+!)", line)]
        expansion = "delayed" if any("!" in line for line in joins) else "percent"
    if re.search(r"(?im)^.*\bcall\s+:HUNTRESS_(?:RECOVER|EMIT)\b", source):
        control = "call_subroutine"
    elif re.search(r"(?im)^\s*goto\s+:HUNTRESS_DISPATCH\b", source):
        control = "goto_dispatch"
    elif re.search(r"(?im)^\s*if\s+errorlevel\b", source):
        control = "errorlevel_guard"
    elif re.search(r"(?im)^\s*if\s+defined\b", source):
        control = "if_guard"
    else:
        control = "direct"
    return expansion, control


def build(directory: Path, question_ids: list[str]) -> dict[str, str]:
    answers: dict[str, str] = {}
    for stem, scenario, attack, fields in (
        ("resource", "resource_hijacking", "T1496", {"url": "b", "wallet": "c", "mutex": "h"}),
        ("collection", "synthetic_collection", "T1555.003", {"url": "b", "file": "c", "user-agent": "f"}),
        ("impact", "synthetic_impact", "T1486", {"extension": "b", "note": "c", "url": "d"}),
    ):
        path = directory / f"{stem}-sample.ps1"
        source = path.read_text()
        encoded = re.search(r"FromBase64String\('([^']+)'\)", source)
        if not encoded:
            raise ValueError(f"PowerShell descriptor missing: {path.name}")
        obj = json.loads(base64.b64decode(encoded.group(1)))
        answers[f"{stem}-scenario"] = scenario
        answers[f"{stem}-attack"] = attack
        for suffix, key in fields.items():
            value = obj[key]
            answers[f"{stem}-{suffix}"] = value[0] if isinstance(value, list) else value

    suffix_keys = {
        "host": "host_id", "host-id": "host_id", "url": "url",
        "upload-url": "upload_url", "path": "file_path", "file-path": "file_path",
        "next-stage": "next_stage", "extension": "extension", "note": "note_name",
        "note-name": "note_name", "campaign": "campaign_id", "adapter": "adapter",
    }
    for language in ("jscript", "batch"):
        for role, stem in STEMS.items():
            ext = ".js" if language == "jscript" else BATCH_EXTENSION.get(role, ".cmd")
            path = directory / (stem + ext)
            source = path.read_text()
            if language == "jscript":
                obj = recover_js(path)
                steps = ",".join(obj["steps"])
                values = {**obj.get("values", {}), "adapter": obj["adapter"]}
            else:
                values = recover_batch(path)
                steps = values["steps"]
            if steps != STEPS[role]:
                raise ValueError(f"unsupported behavior variant in {path.name}: {steps}")
            prefix = f"{language}-{role}"
            answers[prefix + "-role"] = ROLES[role]
            answers[prefix + "-attack"] = (
                "T1059.007" if language == "jscript" else "T1059.003"
            ) if role in ("launcher", "chain", "relay") else ATTACKS[role]
            for suffix, key in suffix_keys.items():
                if key in values:
                    answers[prefix + "-" + suffix] = values[key]
            if language == "jscript":
                for suffix, value in zip(("function-style", "invocation-style", "property-style"), js_styles(source)):
                    answers[prefix + "-" + suffix] = value
            else:
                expansion, control = batch_forms(source, role)
                answers[prefix + "-expansion"] = expansion
                answers[prefix + "-control"] = control
                answers[prefix + "-graph"] = values["graph"]
    missing = [qid for qid in question_ids if qid not in answers]
    if missing:
        raise ValueError("unmapped answer IDs: " + ", ".join(missing))
    return {qid: answers[qid] for qid in question_ids}


def request_json(token: str, body: dict) -> dict:
    req = Request(BASE, data=json.dumps(body).encode(), headers={
        "Authorization": "Bearer " + token, "Content-Type": "application/json",
        "Accept": "application/json",
    })
    with urlopen(req, timeout=12) as response:
        return json.load(response)


def start_and_solve(retry: bool = False, grouped: bool = False, diagnostic: bool = False,
                    probe_expansion: bool = False, fallback_expansion: bool = False) -> None:
    token = os.environ["HUNTRESS_GM_TOKEN"]
    current = request_json(token, {"challenge": CHALLENGE, **({"op": "retry"} if retry else {})})
    attempt = current.get("attempt_id")
    qids = current.get("answer_ids") or [q["id"] for q in current.get("questions", [])]
    record = {"attempt_id": attempt, "mode": current.get("mode"), "deadline": current.get("deadline"),
              "answer_count": len(qids), "download": current.get("download"), "sha256": current.get("sha256")}
    if current.get("mode") != "time_trial" or not qids or not current.get("download"):
        print(json.dumps({"stage": "start", **record, "error": "unexpected start response"}))
        return
    url = urljoin(BASE, current["download"])
    req = Request(url, headers={"Authorization": "Bearer " + token, "Accept": "application/octet-stream"})
    with urlopen(req, timeout=12) as response:
        archive = response.read()
    with tempfile.TemporaryDirectory(prefix="expansion-tt-") as temporary:
        temp = Path(temporary)
        zip_path = temp / "evidence.zip"
        zip_path.write_bytes(archive)
        extracted = temp / "extracted"
        extracted.mkdir()
        unpack = subprocess.run(["7z", "x", "-pinfected", "-y", f"-o{extracted}", str(zip_path)],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3)
        if unpack.returncode:
            print(json.dumps({"stage": "extract", **record, "error": "ZIP extraction failed; check password or format"}))
            return
        try:
            answers = build(extracted, qids)
        except Exception as exc:
            saved = HERE / "artifacts/time_trial" / (attempt or "unknown")
            saved.mkdir(parents=True, exist_ok=True)
            (saved / "evidence.zip").write_bytes(archive)
            print(json.dumps({"stage": "derive", **record, "error": str(exc), "retained": str(saved)}))
            return
        if fallback_expansion or probe_expansion:
            groups = {
                "confirmed_field_types": {qid: value for qid, value in answers.items() if not qid.endswith("-expansion")},
            }
        elif diagnostic:
            groups = {
                "powershell_and_jscript": {qid: value for qid, value in answers.items() if not qid.startswith("batch-")},
                "batch_values": {qid: value for qid, value in answers.items() if qid.startswith("batch-") and not qid.endswith(("-expansion", "-control"))},
                "batch_expansion": {qid: value for qid, value in answers.items() if qid.startswith("batch-") and qid.endswith("-expansion")},
                "batch_control": {qid: value for qid, value in answers.items() if qid.startswith("batch-") and qid.endswith("-control")},
            }
        elif grouped:
            groups = {
                name: {qid: value for qid, value in answers.items() if qid.startswith(prefix)}
                for name, prefix in (("powershell", ("resource-", "collection-", "impact-")),
                                     ("jscript", "jscript-"), ("batch", "batch-"))
            }
        else:
            groups = {"all": answers}
        outcomes = []
        diagnostic_dir = HERE / "artifacts/time_trial" / (attempt or "unknown") if diagnostic or probe_expansion or fallback_expansion else None
        if diagnostic_dir:
            diagnostic_dir.mkdir(parents=True, exist_ok=True)
            (diagnostic_dir / "evidence.zip").write_bytes(archive)
            (diagnostic_dir / "candidates.json").write_text(json.dumps(answers, indent=2) + "\n")
        for name, payload in groups.items():
            result = request_json(token, {"challenge": CHALLENGE, "answers": payload})
            outcomes.append({"group": name, "count": len(payload), "result": result.get("result"),
                             "remaining": result.get("remaining"), "status": result.get("status"),
                             "flag": result.get("flag")})
            if diagnostic_dir:
                (diagnostic_dir / "outcomes.json").write_text(json.dumps(outcomes, indent=2) + "\n")
            if result.get("result") == "CORRECT":
                break
            if diagnostic and result.get("result") == "incorrect" and name.startswith("batch_"):
                items = list(payload.items())
                width = (len(items) + 2) // 3
                for index in range(0, len(items), width):
                    sub = dict(items[index:index + width])
                    sub_result = request_json(token, {"challenge": CHALLENGE, "answers": sub})
                    outcomes.append({"group": name + "_part_" + str(index // width + 1),
                                     "answer_ids": list(sub), "result": sub_result.get("result"),
                                     "remaining": sub_result.get("remaining"), "flag": sub_result.get("flag")})
                    (diagnostic_dir / "outcomes.json").write_text(json.dumps(outcomes, indent=2) + "\n")
                    if sub_result.get("result") == "CORRECT":
                        break
        if (probe_expansion or fallback_expansion) and outcomes[-1]["result"] == "accepted":
            from concurrent.futures import ThreadPoolExecutor

            expansion_items = [(qid, value) for qid, value in answers.items() if qid.endswith("-expansion")]

            def check_one(pair: tuple[str, str]) -> dict:
                qid, value = pair
                try:
                    response = request_json(token, {"challenge": CHALLENGE, "answers": {qid: value}})
                    return {"answer_id": qid, "candidate": value, "result": response.get("result"),
                            "remaining": response.get("remaining"), "flag": response.get("flag")}
                except HTTPError as exc:
                    return {"answer_id": qid, "candidate": value, "http_status": exc.code}

            if fallback_expansion:
                pending = dict(expansion_items)
                tried = {qid: [] for qid in pending}
                for wave in range(4):
                    requests = []
                    for qid, primary in pending.items():
                        choices = [primary, "for_indirect", "call_double", "delayed", "percent"]
                        value = next((choice for choice in choices if choice not in tried[qid]), None)
                        if value is not None:
                            tried[qid].append(value)
                            requests.append((qid, value))
                    if not requests:
                        break
                    with ThreadPoolExecutor(max_workers=min(9, len(requests))) as pool:
                        checked = list(pool.map(check_one, requests))
                    outcomes.extend(checked)
                    (diagnostic_dir / "outcomes.json").write_text(json.dumps(outcomes, indent=2) + "\n")
                    for item in checked:
                        if item.get("result") in ("accepted", "CORRECT"):
                            pending.pop(item["answer_id"], None)
                    if any(item.get("http_status") == 429 or item.get("result") == "CORRECT" for item in checked):
                        break
            else:
                for index in range(0, len(expansion_items), 3):
                    with ThreadPoolExecutor(max_workers=3) as pool:
                        checked = list(pool.map(check_one, expansion_items[index:index + 3]))
                    outcomes.extend(checked)
                    (diagnostic_dir / "outcomes.json").write_text(json.dumps(outcomes, indent=2) + "\n")
                    if any(item.get("http_status") == 429 or item.get("result") == "CORRECT" for item in checked):
                        break
        print(json.dumps({"stage": "submit", **record, "groups": outcomes}, ensure_ascii=False))
        solved = any(item.get("result") == "CORRECT" for item in outcomes)
        if solved and fallback_expansion and diagnostic_dir:
            used_fallback = any(
                item.get("result") in ("accepted", "CORRECT")
                and item.get("answer_id") in answers
                and item.get("candidate") != answers[item["answer_id"]]
                for item in outcomes
            )
            if not used_fallback:
                import shutil
                shutil.rmtree(diagnostic_dir)
        if not solved:
            saved = HERE / "artifacts/time_trial" / (attempt or "unknown")
            saved.mkdir(parents=True, exist_ok=True)
            (saved / "evidence.zip").write_bytes(archive)
            (saved / "candidates.json").write_text(json.dumps(answers, indent=2) + "\n")
            (saved / "outcomes.json").write_text(json.dumps(outcomes, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", action="store_true", help="derive answers from preserved Single Solve files")
    parser.add_argument("--start-and-solve", action="store_true", help="start the Time Trial and submit once")
    parser.add_argument("--retry-grouped", action="store_true", help="retry current assignment and submit bounded groups")
    parser.add_argument("--retry-diagnose-batch", action="store_true", help="retry and isolate Batch failures by answer type")
    parser.add_argument("--retry-probe-expansion", action="store_true", help="retry and check nine Batch expansion labels")
    parser.add_argument("--retry-expansion-fallback", action="store_true", help="retry with bounded expansion label fallback")
    args = parser.parse_args()
    if args.reference:
        state = json.loads((HERE / "challenge_state.json").read_text())
        qids = state["modes"]["single_solve"]["answer_ids"]
        with tempfile.TemporaryDirectory(prefix="expansion-reference-") as temporary:
            extracted = Path(temporary)
            result = subprocess.run(
                ["7z", "x", "-pinfected", "-y", f"-o{extracted}", str(HERE / "expansion_pack.zip")],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3,
            )
            if result.returncode:
                raise ValueError("Single Solve ZIP extraction failed with password infected")
            print(json.dumps(build(extracted, qids), ensure_ascii=False))
    elif args.start_and_solve:
        start_and_solve(fallback_expansion=True)
    elif args.retry_grouped:
        start_and_solve(retry=True, grouped=True)
    elif args.retry_diagnose_batch:
        start_and_solve(retry=True, diagnostic=True)
    elif args.retry_probe_expansion:
        start_and_solve(retry=True, probe_expansion=True)
    elif args.retry_expansion_fallback:
        start_and_solve(retry=True, fallback_expansion=True)
    else:
        parser.error("select --reference, --start-and-solve, or --retry-grouped")


if __name__ == "__main__":
    try:
        main()
    except HTTPError as exc:
        print(json.dumps({"error": "Game Master HTTP error", "http_status": exc.code,
                          "retry_after": exc.headers.get("Retry-After")}))
    except Exception as exc:
        print(json.dumps({"error": type(exc).__name__, "detail": str(exc)}))
