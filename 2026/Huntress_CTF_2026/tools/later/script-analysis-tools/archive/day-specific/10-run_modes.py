#!/usr/bin/env python3
"""Run and solve Day 10 Bind Over Matter timed modes."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import sys
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


PROXY = "http://192.0.2.1/huntress-ctf-proxy"
CHALLENGES = {
    "time_trial": "script-analysis-day-10-wmi-persistence-reconstruction/time_trial",
    "mastery": "script-analysis-day-10-wmi-persistence-reconstruction/mastery",
}
ROOT = Path(__file__).resolve().parents[1]
ZIP_PASSWORD = b"infected"


def request_json(url: str, payload: dict[str, Any] | None = None) -> tuple[Any, int]:
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data is not None else {},
        method="POST" if data is not None else "GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            return json.loads(response.read()), response.status
    except urllib.error.HTTPError as error:
        try:
            return json.loads(error.read()), error.code
        except json.JSONDecodeError:
            raise RuntimeError(f"Game Master returned HTTP {error.code}") from error


def download_artifact(challenge: str, delivery: int | None) -> bytes:
    query = (
        "?op=artifact&challenge="
        + urllib.parse.quote(challenge, safe="")
    )
    if delivery is not None:
        query += f"&delivery={delivery}"
    request = urllib.request.Request(PROXY + query)
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()


def archive_members(data: bytes) -> list[tuple[str, bytes]]:
    import io

    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            if any(info.flag_bits & 1 for info in archive.infolist()):
                raise zipfile.BadZipFile("encrypted ZIP")
            return [
                (info.filename, archive.read(info))
                for info in archive.infolist()
                if not info.is_dir()
            ]
    except zipfile.BadZipFile:
        try:
            import pyzipper
        except ModuleNotFoundError:
            venv_site = ROOT / "work/day-08/venv/lib/python3.12/site-packages"
            if venv_site.exists():
                sys.path.insert(0, str(venv_site))
            import pyzipper
        with pyzipper.AESZipFile(io.BytesIO(data)) as archive:
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


def write_challenge_report(response: dict[str, Any], challenge: str, path: Path) -> None:
    lines = [
        "# Day 10 — Bind Over Matter",
        "",
        "## Challenge",
        "",
        f"- **Name:** {response.get('name')}",
        f"- **ID:** `{challenge}`",
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
    artifacts = response.get("artifacts")
    if artifacts:
        for index, artifact in enumerate(artifacts):
            filename = artifact.get("filename", f"evidence-{index + 1}.zip")
            lines.extend(
                [
                    f"- **{filename}:** [{filename} {index + 1}]({artifact.get('download')})",
                    f"  SHA-256: `{artifact.get('sha256')}`",
                ]
            )
    elif response.get("download"):
        filename = response.get("filename", "evidence.zip")
        lines.extend(
            [
                f"- **{filename}:** [Download {filename}]({response['download']})",
                f"  SHA-256: `{response.get('sha256')}`",
                "- **Archive password:** `infected`",
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
        lines.extend(
            [
                f"### `{question['id']}`",
                "",
                question.get("question", ""),
            ]
        )
        for key, value in question.items():
            if key in ("id", "question"):
                continue
            shown = (
                json.dumps(value, ensure_ascii=False, sort_keys=True)
                if isinstance(value, (dict, list))
                else value
            )
            lines.append(f"- **{key}:** `{shown}`")
        lines.append("")
    lines.extend(
        [
            "## How to submit",
            "",
            f"Done means all {len(questions)} answer IDs are accepted and the Game Master returns `CORRECT`.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=tuple(CHALLENGES))
    parser.add_argument(
        "--retry",
        action="store_true",
        help="request a fresh timed variant instead of starting or resuming",
    )
    args = parser.parse_args()

    challenge = CHALLENGES[args.mode]
    payload = (
        {"op": "retry", "challenge": challenge}
        if args.retry
        else {"challenge": challenge}
    )
    response, status_code = request_json(PROXY, payload)
    if status_code != 200 or not isinstance(response, dict):
        raise RuntimeError(f"Could not start {args.mode} (HTTP {status_code}): {response!r}")
    if response.get("mode") != args.mode:
        raise RuntimeError(
            f"Expected mode {args.mode!r}, received {response.get('mode')!r}"
        )

    attempt_id = response.get("attempt_id", "unknown-attempt")
    record = ROOT / f"work/day10/{args.mode}/attempt-records" / attempt_id
    record.mkdir(parents=True, exist_ok=True)
    (record / "start-response.json").write_text(
        json.dumps(response, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    questions = response.get("questions", [])
    sets = sorted(
        {q.get("set") for q in questions if isinstance(q.get("set"), int)}
    )
    artifacts = response.get("artifacts")
    if isinstance(artifacts, list) and artifacts:
        deliveries = artifacts
        if sets and len(sets) != len(deliveries):
            raise RuntimeError(
                f"Received {len(deliveries)} archives for {len(sets)} answer sets"
            )
    else:
        deliveries = [
            {
                "filename": response.get("filename", "evidence.zip"),
                "sha256": response.get("sha256"),
            }
        ]

    extracted = record / "artifacts"
    extracted.mkdir(parents=True, exist_ok=True)
    for index, artifact in enumerate(deliveries):
        delivery_index = index if len(deliveries) > 1 or artifacts else None
        data = download_artifact(challenge, delivery_index)
        digest = hashlib.sha256(data).hexdigest()
        expected = artifact.get("sha256")
        if expected and digest != expected:
            raise RuntimeError(
                f"Delivery {index + 1} SHA-256 mismatch: expected {expected}, got {digest}"
            )
        (record / f"evidence-delivery-{index + 1:02d}.zip").write_bytes(data)
        if len(deliveries) == len(sets) and sets:
            destination = extracted / f"set{sets[index]}"
        else:
            destination = extracted
        destination.mkdir(parents=True, exist_ok=True)
        for name, member_data in archive_members(data):
            write_member(destination, name, member_data)

    if len(deliveries) == 1 and len(sets) > 1:
        nested_archives = [
            extracted / f"evidence-{index + 1:02d}.zip"
            for index in range(len(sets))
        ]
        if all(path.is_file() for path in nested_archives):
            for set_number, nested_path in zip(sets, nested_archives):
                nested_data = nested_path.read_bytes()
                (record / f"evidence-set{set_number:02d}.zip").write_bytes(
                    nested_data
                )
                set_root = extracted / f"set{set_number}"
                set_root.mkdir(parents=True, exist_ok=True)
                for name, member_data in archive_members(nested_data):
                    write_member(set_root, name, member_data)

    tools = Path(__file__).resolve().parent
    sys.path.insert(0, str(tools))
    solver = importlib.import_module("script_analysis_solver")
    answers = solver.build_all_answers(response, extracted)
    solver.validate_answers(response, answers)
    (record / "candidate-answers.json").write_text(
        json.dumps(answers, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    result, submit_code = request_json(
        PROXY, {"challenge": challenge, "answers": answers}
    )
    (record / "submission-all.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    status_url = (
        PROXY
        + "?op=status&challenge="
        + urllib.parse.quote(challenge, safe="")
    )
    status, status_http = request_json(status_url)
    if isinstance(status, dict):
        (record / "status-after-submission.json").write_text(
            json.dumps(status, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    write_challenge_report(response, challenge, record / "CHALLENGE.md")

    final_result = result.get("result") if isinstance(result, dict) else None
    if final_result == "CORRECT":
        (record / "accepted-answers.json").write_text(
            json.dumps(answers, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    summary = {
        "challenge": challenge,
        "mode": args.mode,
        "attempt_id": attempt_id,
        "deadline": response.get("deadline"),
        "question_count": len(questions),
        "artifact_sha256": [artifact.get("sha256") for artifact in deliveries],
        "submission_http": submit_code,
        "submission_result": final_result,
        "remaining": result.get("remaining") if isinstance(result, dict) else None,
        "status_http": status_http,
        "status_result": status.get("result") if isinstance(status, dict) else None,
        "accepted_id_count": len(status.get("accepted_ids", []))
        if isinstance(status, dict)
        else None,
        "flag": result.get("flag") if isinstance(result, dict) else None,
        "record": str(record),
    }
    (record / "run-summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if final_result == "CORRECT" else 3


if __name__ == "__main__":
    raise SystemExit(main())
