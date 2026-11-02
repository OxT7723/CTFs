#!/usr/bin/env python3
"""Solve Day 06 Mastery from assigned archives and reconcile each answer set."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


PROXY = "http://192.0.2.1/huntress-ctf-proxy"
CHALLENGE = "script-analysis-day-06-bash-behavior-graphs/mastery"
ROOT = Path(__file__).resolve().parents[1]
ZIP_PASSWORD = b"infected"


def request(url: str, payload: dict[str, Any] | None = None) -> tuple[Any, int]:
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data is not None else {},
        method="POST" if data is not None else "GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            raw, code = response.read(), response.status
    except urllib.error.HTTPError as exc:
        raw, code = exc.read(), exc.code
    try:
        return json.loads(raw), code
    except (UnicodeDecodeError, json.JSONDecodeError):
        return raw, code


def archive_members(data: bytes) -> list[tuple[str, bytes]]:
    try:
        with zipfile.ZipFile(__import__("io").BytesIO(data)) as archive:
            if any(info.flag_bits & 1 for info in archive.infolist()):
                raise zipfile.BadZipFile("AES encrypted")
            return [
                (info.filename, archive.read(info))
                for info in archive.infolist()
                if not info.is_dir()
            ]
    except zipfile.BadZipFile:
        try:
            import pyzipper
        except ModuleNotFoundError:
            site_packages = ROOT / "work/day-08/venv/lib/python3.12/site-packages"
            sys.path.insert(0, str(site_packages))
            import pyzipper
        with pyzipper.AESZipFile(__import__("io").BytesIO(data)) as archive:
            return [
                (info.filename, archive.read(info, pwd=ZIP_PASSWORD))
                for info in archive.infolist()
                if not info.is_dir()
            ]


def write_member(root: Path, name: str, data: bytes) -> None:
    member = PurePosixPath(name)
    if member.is_absolute() or ".." in member.parts:
        raise ValueError(f"Unsafe archive path: {name!r}")
    target = (root / Path(*member.parts)).resolve()
    if root.resolve() not in target.parents:
        raise ValueError(f"Archive path escapes output directory: {name!r}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)


def write_challenge_report(response: dict[str, Any], destination: Path) -> None:
    lines = [
        "# Day 06 Mastery — Shell We Begin",
        "",
        "## Challenge",
        "",
        f"- **Name:** {response.get('name')}",
        f"- **ID:** `{CHALLENGE}`",
        f"- **Description:** {response.get('prompt')}",
        f"- **Mode:** `{response.get('mode')}`",
        f"- **Attempt:** `{response.get('attempt_id')}`",
        f"- **Started:** `{response.get('started_at')}`",
        f"- **Deadline:** `{response.get('deadline')}`",
        "",
        "## Instructions",
        "",
        response.get("guidance", ""),
        "",
        "## Files",
        "",
    ]
    for index, artifact in enumerate(response.get("artifacts", []), 1):
        lines.extend(
            [
                f"- **Delivery {index}: {artifact.get('filename')}**",
                f"  Download: [{artifact.get('filename')} {index}]({artifact.get('download')})",
                f"  SHA-256: `{artifact.get('sha256')}`",
            ]
        )
    questions = response.get("questions", [])
    lines.extend(
        [
            "",
            "## Questions and answer formats",
            "",
            f"The API returned {len(questions)} questions. Submit each under its exact ID.",
            "",
        ]
    )
    for question in questions:
        lines.extend([f"### `{question['id']}`", "", question.get("question", "")])
        for key in ("artifact", "answer_format", "normalization", "set"):
            if key not in question:
                continue
            value = question[key]
            if isinstance(value, dict):
                value = json.dumps(value, ensure_ascii=False, sort_keys=True)
            lines.append(f"- **{key}:** `{value}`")
        lines.append("")
    lines.extend(
        [
            "## How to submit",
            "",
            f"Done means all {len(questions)} answer IDs are accepted and the Game Master returns `CORRECT`.",
        ]
    )
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--retry",
        action="store_true",
        help="renew the expired attempt; otherwise reconnect to the current attempt",
    )
    parser.add_argument(
        "--practice",
        action="store_true",
        help="continue the last Mastery assignment in untimed practice after retries are exhausted",
    )
    parser.add_argument(
        "--family-groups",
        action="store_true",
        help="submit set 1 together and split set 2 into artifact families for diagnosis",
    )
    parser.add_argument(
        "--only-set",
        type=int,
        choices=(1, 2),
        help="submit one set only when continuing a partially accepted Mastery attempt",
    )
    parser.add_argument(
        "--specimen-groups",
        action="store_true",
        help="split set 2's VBScript answers by API artifact for narrower diagnosis",
    )
    parser.add_argument(
        "--batch-specimen-groups",
        action="store_true",
        help="split set 2's Batch answers by API artifact for narrower diagnosis",
    )
    parser.add_argument(
        "--batch-expansion-groups",
        action="store_true",
        help="submit Batch expansion fields one at a time for one selected set",
    )
    parser.add_argument(
        "--batch-expansion-probes",
        action="store_true",
        help="probe the exact expansion labels for each Batch expansion field",
    )
    parser.add_argument(
        "--single-answer-groups",
        action="store_true",
        help="submit set2.vbscript-benign answers one ID at a time",
    )
    parser.add_argument(
        "--single-specimen-fields",
        help="submit one answer ID at a time for the named API artifact (for example local-dispatch.vbs)",
    )
    parser.add_argument(
        "--compare-vb-pairs",
        action="store_true",
        help="compare set2 VBScript memory-stage and relay-handoff answers by field",
    )
    parser.add_argument(
        "--control-probes",
        nargs="?",
        const="*",
        metavar="ARTIFACT",
        help="probe control labels for a VBScript answer, optionally selected by artifact filename",
    )
    parser.add_argument(
        "--full-submit",
        action="store_true",
        help="submit the complete answer map in one request",
    )
    args = parser.parse_args()

    if args.retry and args.practice:
        parser.error("--retry and --practice are mutually exclusive")
    operation = "retry" if args.retry else "practice" if args.practice else "start"
    payload = {"op": operation, "challenge": CHALLENGE}
    response, code = request(PROXY, payload)
    if code != 200 or not isinstance(response, dict) or not isinstance(response.get("questions"), list):
        raise RuntimeError(f"Start/retry failed (HTTP {code}): {response!r}")
    if response.get("mode") != "mastery":
        raise RuntimeError(f"Expected mastery mode, received {response.get('mode')!r}")

    attempt_id = response.get("attempt_id", "unknown-attempt")
    record = ROOT / "work/day06/mastery/attempt-records" / attempt_id
    record.mkdir(parents=True, exist_ok=True)
    (record / "start-response.json").write_text(
        json.dumps(response, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    sets = sorted(
        {q.get("set") for q in response["questions"] if isinstance(q.get("set"), int)}
    )
    artifacts = response.get("artifacts", [])
    if len(sets) != len(artifacts):
        raise RuntimeError(f"Expected one archive per set; got {len(sets)} sets and {len(artifacts)} archives")

    extracted = record / "artifacts"
    extracted.mkdir(exist_ok=True)
    for index, (set_number, artifact) in enumerate(zip(sets, artifacts)):
        url = (
            PROXY
            + "?op=artifact&challenge="
            + urllib.parse.quote(CHALLENGE, safe="")
            + f"&delivery={index}"
        )
        data, artifact_code = request(url)
        if artifact_code != 200 or not isinstance(data, bytes):
            raise RuntimeError(f"Artifact delivery {index + 1} failed (HTTP {artifact_code})")
        digest = hashlib.sha256(data).hexdigest()
        if digest != artifact.get("sha256"):
            raise RuntimeError(f"Delivery {index + 1} SHA-256 mismatch")
        (record / f"evidence-delivery-{index + 1:02d}.zip").write_bytes(data)
        set_root = extracted / f"set{set_number}"
        set_root.mkdir(parents=True, exist_ok=True)
        for name, member_data in archive_members(data):
            write_member(set_root, name, member_data)

    tools = Path(__file__).resolve().parent
    sys.path.insert(0, str(tools))
    import script_analysis_solver

    answers = script_analysis_solver.build_all_answers(response, extracted)
    script_analysis_solver.validate_answers(response, answers)
    (record / "candidate-answers.json").write_text(
        json.dumps(answers, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    groups: list[tuple[str, dict[str, str]]] = []
    group_results = []
    final_result: dict[str, Any] = {}
    if args.full_submit:
        groups.append(("all", answers))
    elif args.batch_expansion_probes:
        pass
    elif args.batch_expansion_groups:
        for key, value in sorted(answers.items()):
            if not key.endswith("-expansion") or not key.startswith("set"):
                continue
            set_number = int(key.split(".", 1)[0][3:])
            if args.only_set is not None and set_number != args.only_set:
                continue
            if key.split(".", 1)[1].startswith("batch-"):
                groups.append((key, {key: value}))
    elif args.compare_vb_pairs:
        question_by_id = {q["id"]: q for q in response["questions"]}
        by_field: dict[str, dict[str, str]] = {}
        targets = ("set2.vbscript-stager-", "set2.vbscript-relay-")
        for key, value in answers.items():
            if not key.startswith(targets):
                continue
            question = question_by_id[key]
            artifact_name = question.get("artifact", "").rsplit("->", 1)[-1].strip()
            if key.startswith("set2.vbscript-stager-"):
                field = key.rsplit("-", 1)[-1]
                if field == "url":
                    field = "indicator"
            else:
                field = key.rsplit("-", 1)[-1]
                if field == "next-stage":
                    field = "indicator"
            by_field.setdefault(field, {})[key] = value
        groups.extend((f"set2-vbscript-pair-{field}", by_field[field]) for field in sorted(by_field))
    elif args.control_probes:
        pass
    elif args.single_answer_groups:
        set_number = args.only_set or 2
        groups.extend(
            (key, {key: value})
            for key, value in sorted(answers.items())
            if key.startswith(f"set{set_number}.vbscript-benign-")
            and not key.endswith("-host-id")
        )
    elif args.single_specimen_fields:
        question_by_id = {q["id"]: q for q in response["questions"]}
        set_number = args.only_set or 2
        for key, value in sorted(answers.items()):
            artifact = question_by_id[key].get("artifact", "")
            if (
                key.startswith(f"set{set_number}.")
                and args.single_specimen_fields.lower() in artifact.lower()
            ):
                groups.append((key, {key: value}))
    elif args.specimen_groups:
        question_by_id = {q["id"]: q for q in response["questions"]}
        by_artifact: dict[str, dict[str, str]] = {}
        for key, value in answers.items():
            question = question_by_id[key]
            set_number = args.only_set or 2
            if not key.startswith(f"set{set_number}.vbscript-"):
                continue
            artifact = question.get("artifact", "")
            label = f"set{set_number}-vbscript-" + artifact.rsplit("->", 1)[-1].strip()
            by_artifact.setdefault(label, {})[key] = value
        groups.extend((label, by_artifact[label]) for label in sorted(by_artifact))
    elif args.batch_specimen_groups:
        question_by_id = {q["id"]: q for q in response["questions"]}
        by_artifact: dict[str, dict[str, str]] = {}
        for key, value in answers.items():
            if not key.startswith("set2.batch-"):
                continue
            artifact = question_by_id[key].get("artifact", "")
            label = "set2-batch-" + artifact.rsplit("->", 1)[-1].strip()
            by_artifact.setdefault(label, {})[key] = value
        groups.extend((label, by_artifact[label]) for label in sorted(by_artifact))
    elif args.family_groups and len(sets) == 2:
        selected_sets = [
            set_number
            for set_number in sets
            if args.only_set is None or set_number == args.only_set
        ]
        for set_number in selected_sets:
            set_prefix = f"set{set_number}."
            family_prefixes = sorted(
                {
                    key[len(set_prefix) :].split("-", 1)[0]
                    for key in answers
                    if key.startswith(set_prefix)
                }
            )
            for family in family_prefixes:
                prefix = f"{set_prefix}{family}-"
                groups.append(
                    (
                        f"set{set_number}-{family}",
                        {key: value for key, value in answers.items() if key.startswith(prefix)},
                    )
                )
    else:
        for set_number in sets:
            if args.only_set is not None and set_number != args.only_set:
                continue
            prefix = f"set{set_number}."
            groups.append(
                (f"set{set_number}", {key: value for key, value in answers.items() if key.startswith(prefix)})
            )
    if args.control_probes is None and not args.batch_expansion_probes and not groups:
        raise ValueError("No answer groups selected")

    if args.batch_expansion_probes:
        probe_values = (
            "CALL-double",
            "FOR-indirect",
            "delayed",
            "percent",
            "call_double",
            "for_indirect",
            "call-double",
            "for-indirect",
        )
        question_by_id = {q["id"]: q for q in response["questions"]}
        probe_ids = [
            key
            for key in sorted(answers)
            if key.endswith("-expansion")
            and key.startswith("set")
            and key.split(".", 1)[1].startswith("batch-")
            and (args.only_set is None or int(key.split(".", 1)[0][3:]) == args.only_set)
        ]
        stop_probing = False
        for answer_id in probe_ids:
            for index, value in enumerate(probe_values, 1):
                result, submit_code = request(
                    PROXY, {"challenge": CHALLENGE, "answers": {answer_id: value}}
                )
                (record / f"expansion-probe-{answer_id}-{index}.json").write_text(
                    json.dumps(
                        {
                            "answer_id": answer_id,
                            "question": question_by_id[answer_id].get("question"),
                            "value": value,
                            "http_status": submit_code,
                            "response": result,
                        },
                        ensure_ascii=False,
                        indent=2,
                    )
                    + "\n",
                    encoding="utf-8",
                )
                accepted = isinstance(result, dict) and result.get("result") in (
                    "accepted",
                    "CORRECT",
                )
                if accepted:
                    answers[answer_id] = value
                group_results.append(
                    {
                        "group": f"probe-{answer_id}",
                        "answer_count": 1,
                        "value": value,
                        "http_status": submit_code,
                        "result": result.get("result") if isinstance(result, dict) else None,
                    }
                )
                final_result = result if isinstance(result, dict) else {}
                if accepted or final_result.get("result") in (
                    "expired",
                    "already_solved",
                ):
                    break
                if final_result.get("result") not in ("incorrect",):
                    stop_probing = True
                    break
            if stop_probing:
                break
    elif args.control_probes is not None:
        set_number = args.only_set or 2
        question_by_id = {q["id"]: q for q in response["questions"]}
        controls = sorted(
            key
            for key, value in answers.items()
            if key.startswith(f"set{set_number}.vbscript-")
            and key.endswith("-control")
            and value == "if_block"
            and (
                args.control_probes == "*"
                or args.control_probes.lower()
                in question_by_id[key].get("artifact", "").lower()
            )
        )
        if not controls:
            raise RuntimeError("This assignment has no matching VBScript if_block control to probe")
        answer_id = controls[0]
        probe_values = (
            "if_block",
            "if_then_else",
            "if_else",
            "if_guard",
            "if_then",
            "if_true_guard",
            "direct",
        )
        for index, value in enumerate(probe_values, 1):
            result, submit_code = request(
                PROXY, {"challenge": CHALLENGE, "answers": {answer_id: value}}
            )
            (record / f"control-probe-{index}.json").write_text(
                json.dumps(
                    {"answer_id": answer_id, "value": value, "http_status": submit_code, "response": result},
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            group_results.append(
                {
                    "group": f"probe-{answer_id}",
                    "answer_count": 1,
                    "value": value,
                    "http_status": submit_code,
                    "result": result.get("result") if isinstance(result, dict) else None,
                }
            )
            final_result = result if isinstance(result, dict) else {}
            if final_result.get("result") in ("accepted", "CORRECT"):
                answers[answer_id] = value
            if final_result.get("result") in ("accepted", "CORRECT", "expired", "already_solved"):
                break
    elif args.control_probes is None and not args.batch_expansion_probes:
        for label, group in groups:
            result, submit_code = request(
                PROXY, {"challenge": CHALLENGE, "answers": group}
            )
            (record / f"submission-{label}.json").write_text(
                json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            group_results.append(
                {
                    "group": label,
                    "answer_count": len(group),
                    "http_status": submit_code,
                    "result": result.get("result") if isinstance(result, dict) else None,
                }
            )
            final_result = result if isinstance(result, dict) else {}
            if final_result.get("result") in ("CORRECT", "expired", "already_solved"):
                break

    status_url = PROXY + "?op=status&challenge=" + urllib.parse.quote(CHALLENGE, safe="")
    status, status_code = request(status_url)
    if status_code == 200 and isinstance(status, dict):
        (record / "status-after-submissions.json").write_text(
            json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    accepted_ids = set(status.get("accepted_ids", [])) if isinstance(status, dict) else set()
    write_challenge_report(response, record / "CHALLENGE.md")
    if final_result.get("result") == "CORRECT":
        (record / "accepted-answers.json").write_text(
            json.dumps(answers, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    summary = {
        "challenge": CHALLENGE,
        "attempt_id": attempt_id,
        "deadline": response.get("deadline"),
        "question_count": len(response["questions"]),
        "artifact_sha256": [a.get("sha256") for a in artifacts],
        "groups": group_results,
        "status_http": status_code,
        "accepted_id_count_from_status": len(accepted_ids),
        "final_result": final_result.get("result"),
        "flag": final_result.get("flag"),
        "record": str(record),
    }
    (record / "run-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if final_result.get("result") == "CORRECT" else 3


if __name__ == "__main__":
    raise SystemExit(main())
