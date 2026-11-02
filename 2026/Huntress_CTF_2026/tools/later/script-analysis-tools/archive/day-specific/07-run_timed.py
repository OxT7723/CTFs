#!/usr/bin/env python3
"""Fetch, statically solve, submit, and reconcile a timed Script Analysis attempt."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import io
import json
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


PROXY = "http://192.0.2.1/huntress-ctf-proxy"
CHALLENGE_PREFIX = "script-analysis-day-07-node-operation-graphs"
ZIP_PASSWORD = b"infected"


def gm_request(url: str, payload: dict[str, Any] | None = None) -> Any:
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data is not None else {},
        method="POST" if data is not None else "GET",
    )
    with urllib.request.urlopen(request, timeout=8) as response:
        raw = response.read()
    try:
        return json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return raw


def load_pyzipper():
    try:
        return importlib.import_module("pyzipper")
    except ModuleNotFoundError:
        # Homebase's shared CTF analysis environment keeps AES ZIP support here.
        site_packages = (
            Path(__file__).resolve().parents[1]
            / "work/day-08/venv/lib/python3.12/site-packages"
        )
        if site_packages.is_dir():
            sys.path.insert(0, str(site_packages))
            return importlib.import_module("pyzipper")
        raise RuntimeError("pyzipper is required to read AES-encrypted evidence ZIPs")


def archive_entries(data: bytes) -> list[tuple[str, bytes]]:
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            infos = [info for info in archive.infolist() if not info.is_dir()]
            if any(info.flag_bits & 0x1 for info in infos):
                raise RuntimeError("AES-encrypted ZIP")
            return [(info.filename, archive.read(info)) for info in infos]
    except (zipfile.BadZipFile, RuntimeError):
        pyzipper = load_pyzipper()
        with pyzipper.AESZipFile(io.BytesIO(data)) as archive:
            archive.pwd = ZIP_PASSWORD
            return [
                (info.filename, archive.read(info))
                for info in archive.infolist()
                if not info.is_dir()
            ]


def safe_write(root: Path, name: str, data: bytes) -> Path:
    relative = PurePosixPath(name)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"Unsafe archive path: {name!r}")
    target = (root / Path(*relative.parts)).resolve()
    if root.resolve() not in target.parents:
        raise ValueError(f"Archive path escapes extraction directory: {name!r}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return target


def extract_assignment(archive_data: bytes, destination: Path, response: dict[str, Any]) -> None:
    outer_entries = archive_entries(archive_data)
    set_numbers = sorted(
        {
            int(match.group(1))
            for question in response.get("questions", [])
            if (match := re.match(r"set(\d+)\.", question.get("id", "")))
        }
    )
    nested = [(name, data) for name, data in outer_entries if name.lower().endswith(".zip")]

    if set_numbers and nested:
        for index, (name, data) in enumerate(nested):
            set_number = set_numbers[index] if index < len(set_numbers) else index + 1
            root = destination / f"set{set_number}"
            root.mkdir(parents=True, exist_ok=True)
            for inner_name, inner_data in archive_entries(data):
                safe_write(root, inner_name, inner_data)
        return

    if len(outer_entries) == 1 and outer_entries[0][0].lower().endswith(".zip"):
        destination.mkdir(parents=True, exist_ok=True)
        for name, data in archive_entries(outer_entries[0][1]):
            safe_write(destination, name, data)
        return

    for name, data in outer_entries:
        if name.lower().endswith(".zip"):
            inner_root = destination / Path(name).stem
            inner_root.mkdir(parents=True, exist_ok=True)
            for inner_name, inner_data in archive_entries(data):
                safe_write(inner_root, inner_name, inner_data)
        else:
            safe_write(destination, name, data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("time_trial", "mastery"), required=True)
    parser.add_argument("--retry", action="store_true", help="request a fresh timed variant")
    parser.add_argument(
        "--training",
        action="store_true",
        help="request an untimed practice variant instead of a timed run",
    )
    parser.add_argument(
        "--challenge",
        help="full challenge ID; defaults to the Day 7 Node by Node challenge in the selected mode",
    )
    args = parser.parse_args()

    challenge = args.challenge or f"{CHALLENGE_PREFIX}/{args.mode}"
    timed = not args.training
    start_payload = (
        {"op": "retry", "challenge": challenge, "run_for_time": timed}
        if args.retry
        else {"challenge": challenge, "run_for_time": timed}
    )
    response = gm_request(PROXY, start_payload)
    if not isinstance(response, dict) or not isinstance(response.get("questions"), list):
        raise RuntimeError(f"Unexpected start response: {response!r}")
    if response.get("mode") != args.mode:
        raise RuntimeError(f"Requested {args.mode}, received {response.get('mode')!r}")
    if timed and response.get("run_for_time") is False:
        raise RuntimeError(
            "The server resumed an untimed attempt. Finish it, then run with --retry."
        )

    download_url = PROXY + "?op=artifact&challenge=" + urllib.parse.quote(challenge, safe="/")
    archive_data = gm_request(download_url)
    if not isinstance(archive_data, bytes):
        raise RuntimeError("The artifact operation did not return archive bytes")
    actual_hash = hashlib.sha256(archive_data).hexdigest()
    if actual_hash != response.get("sha256"):
        raise RuntimeError(
            f"Artifact SHA-256 mismatch: expected {response.get('sha256')}, got {actual_hash}"
        )

    helper = Path(__file__).with_name("07-solve_node_by_node.py")
    day_match = re.search(r"script-analysis-day-(\d+)", challenge)
    day_folder = f"day-{int(day_match.group(1)):02d}" if day_match else "day-unknown"
    record_dir = (
        Path(__file__).resolve().parents[1]
        / "work"
        / day_folder
        / "attempt-records"
        / response.get("attempt_id", "unknown-attempt")
    )
    record_dir.mkdir(parents=True, exist_ok=True)
    (record_dir / "start-response.json").write_text(
        json.dumps(response, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (record_dir / "evidence.zip").write_bytes(archive_data)
    with tempfile.TemporaryDirectory(prefix="huntress-day07-") as temporary:
        root = Path(temporary)
        start_file = record_dir / "start-response.json"
        artifact_root = root / "artifacts"
        answers_file = record_dir / "candidate-answers.json"
        extract_assignment(archive_data, artifact_root, response)
        command = [
            sys.executable,
            str(helper),
            str(start_file),
            str(artifact_root),
            "--mode",
            args.mode,
            "--output",
            str(answers_file),
        ]
        completed = subprocess.run(command, capture_output=True, text=True, timeout=5)
        if completed.returncode:
            raise RuntimeError(completed.stderr or completed.stdout)
        answers = json.loads(answers_file.read_text(encoding="utf-8"))
        expected_ids = {question["id"] for question in response["questions"]}
        if set(answers) != expected_ids or any(not str(value).strip() for value in answers.values()):
            raise RuntimeError("Candidate answer IDs or values do not match the assignment")
        invalid_enums = [
            question["id"]
            for question in response["questions"]
            if question.get("answer_format", {}).get("accepted_values")
            and answers[question["id"]]
            not in question["answer_format"]["accepted_values"]
        ]
        if invalid_enums:
            raise RuntimeError(f"Enum candidates outside the API formats: {invalid_enums}")

        result = gm_request(PROXY, {"challenge": challenge, "answers": answers})
        if not isinstance(result, dict):
            raise RuntimeError(f"Unexpected submission response: {result!r}")
        (record_dir / "submission-result.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        # A grouped submission's aggregate result is not an answer-by-answer
        # verdict. Preserve the server's authoritative accepted IDs separately.
        status_url = PROXY + "?op=status&challenge=" + urllib.parse.quote(challenge, safe="/")
        try:
            current_status = gm_request(status_url)
        except Exception as exc:
            current_status = {"status_fetch_error": str(exc)}
        if isinstance(current_status, dict):
            (record_dir / "status-after-submit.json").write_text(
                json.dumps(current_status, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        accepted_ids = set(current_status.get("accepted_ids", [])) if isinstance(current_status, dict) else set()
        debug_dir = None
        if result.get("result") != "CORRECT":
            debug_dir = record_dir
        print(
            json.dumps(
                {
                    "challenge": challenge,
                    "mode": response["mode"],
                    "attempt_id": response.get("attempt_id"),
                    "deadline": response.get("deadline"),
                    "question_count": len(response["questions"]),
                    "accepted_count": len(accepted_ids),
                    "unaccepted_count": len(expected_ids - accepted_ids) if accepted_ids else None,
                    "artifact_sha256": actual_hash,
                    "result": result.get("result"),
                    "remaining": result.get("remaining"),
                    "flag": result.get("flag"),
                    "download": response.get("download"),
                    "debug_dir": str(debug_dir) if debug_dir else None,
                },
                ensure_ascii=False,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
