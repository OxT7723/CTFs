#!/usr/bin/env python3
"""Run a Script Analysis mode using the live assignment and static solver."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib
import io
import json
import os
import re
import sys
import time
import urllib.parse
from pathlib import Path, PurePosixPath
from typing import Any

import requests


DEFAULT_PROXY = "http://192.0.2.1/huntress-ctf-proxy"
PASSWORD = b"infected"
ROOT = Path(__file__).resolve().parents[1]
MAX_REQUEST_BYTES = 4 * 1024 * 1024


def request_json(
    url: str,
    payload: dict[str, Any] | None = None,
    session: requests.Session | None = None,
) -> dict:
    data = (
        None
        if payload is None
        else json.dumps(payload, separators=(",", ":")).encode()
    )
    client = session or requests
    headers = {"Content-Type": "application/json"} if data is not None else {}
    # A retry request advances to a fresh timed variant. Never replay it
    # automatically after a transport error or transient gateway response.
    max_attempts = 1 if payload and payload.get("op") == "retry" else 5
    for attempt in range(max_attempts):
        try:
            if data is None:
                response = client.get(url, timeout=30)
            else:
                response = client.post(url, data=data, headers=headers, timeout=30)
            if response.status_code in {502, 503, 504} and attempt + 1 < max_attempts:
                response.close()
                time.sleep(min(2**attempt, 8))
                continue
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            status_code = exc.response.status_code if exc.response is not None else None
            if status_code not in {502, 503, 504} and not isinstance(
                exc, requests.ConnectionError
            ):
                raise
            if attempt + 1 == max_attempts:
                raise
            time.sleep(min(2**attempt, 8))
    raise RuntimeError("Game Master request retry loop ended unexpectedly")


def download(
    proxy: str,
    challenge: str,
    delivery: int | None,
    session: requests.Session | None = None,
) -> bytes:
    query = "?op=artifact&challenge=" + urllib.parse.quote(challenge, safe="")
    if delivery is not None:
        query += f"&delivery={delivery}"
    response = (session or requests).get(proxy + query, timeout=60)
    response.raise_for_status()
    return response.content


def download_artifacts(
    proxy: str,
    challenge: str,
    artifact_count: int,
    has_artifact_list: bool,
    session: requests.Session,
) -> list[bytes]:
    """Fetch independent Mastery deliveries concurrently and preserve their order."""
    def fetch(index: int, client: requests.Session) -> bytes:
        delivery = index if has_artifact_list else None
        return download(proxy, challenge, delivery, client)

    if artifact_count <= 1:
        return [fetch(index, session) for index in range(artifact_count)]

    def fetch_concurrent(index: int) -> bytes:
        # Reuse the start request's warm connection for delivery 1. Other
        # concurrent deliveries use their own sessions to avoid sharing one
        # Session across worker threads.
        if index == 0:
            return fetch(index, session)
        with requests.Session() as client:
            return fetch(index, client)

    with ThreadPoolExecutor(max_workers=min(artifact_count, 4)) as pool:
        return list(pool.map(fetch_concurrent, range(artifact_count)))


def load_pyzipper():
    try:
        import pyzipper
    except ModuleNotFoundError:
        # Homebase's shared CTF analysis environment keeps AES ZIP support here.
        site_packages = (
            Path(__file__).resolve().parents[1]
            / "work/day-08/venv/lib/python3.12/site-packages"
        )
        if not site_packages.is_dir():
            raise RuntimeError(
                "pyzipper is required to read AES-encrypted evidence ZIPs"
            )
        sys.path.insert(0, str(site_packages))
        import pyzipper
    return pyzipper


def safe_write(root: Path, name: str, data: bytes) -> None:
    member = PurePosixPath(name)
    if member.is_absolute() or ".." in member.parts:
        raise ValueError(f"Unsafe archive member: {name!r}")
    target = (root / Path(*member.parts)).resolve()
    if root.resolve() not in target.parents:
        raise ValueError(f"Archive member escapes output directory: {name!r}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)


def extract_zip(data: bytes, destination: Path) -> list[str]:
    pyzipper = load_pyzipper()
    destination.mkdir(parents=True, exist_ok=True)
    names = []
    with pyzipper.AESZipFile(io.BytesIO(data)) as archive:
        archive.setpassword(PASSWORD)
        for item in archive.infolist():
            member = PurePosixPath(item.filename)
            if member.is_absolute() or ".." in member.parts:
                raise ValueError(f"Unsafe archive member: {item.filename!r}")
            target = (destination / Path(*member.parts)).resolve()
            if destination.resolve() not in target.parents and target != destination.resolve():
                raise ValueError(f"Archive member escapes output directory: {item.filename!r}")
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            content = archive.read(item)
            safe_write(destination, item.filename, content)
            names.append(item.filename)
    return names


def extract_zip_contents(data: bytes) -> dict[str, bytes]:
    """Read a safe AES ZIP into memory without writing its members to disk."""
    pyzipper = load_pyzipper()
    contents = {}
    with pyzipper.AESZipFile(io.BytesIO(data)) as archive:
        archive.setpassword(PASSWORD)
        for item in archive.infolist():
            member = PurePosixPath(item.filename)
            if member.is_absolute() or ".." in member.parts:
                raise ValueError(f"Unsafe archive member: {item.filename!r}")
            if item.is_dir():
                continue
            contents[item.filename] = archive.read(item)
    return contents


def extract_mastery_contents(
    blobs: list[bytes], sets: list[int]
) -> tuple[dict[str, bytes], dict[str, bytes]] | None:
    """Decode Mastery specimens in memory; return solver and nested ZIP inputs."""
    if not sets:
        return None

    sources: dict[str, bytes] = {}
    nested_archives: dict[str, bytes] = {}

    if len(blobs) == 1:
        outer = extract_zip_contents(blobs[0])
        nested = [
            (name, content)
            for name, content in outer.items()
            if name.lower().endswith(".zip")
        ]
        if not nested:
            return None

        def unpack_nested(item: tuple[str, bytes]):
            name, content = item
            match = re.search(r"(\d+)", PurePosixPath(name).stem)
            if not match:
                return None
            number = int(match.group(1))
            if number not in sets:
                return None
            return number, name, extract_zip_contents(content)

        with ThreadPoolExecutor(max_workers=min(4, len(nested))) as pool:
            unpacked = list(pool.map(unpack_nested, nested))
        for result in unpacked:
            if result is None:
                continue
            number, archive_name, members = result
            nested_archives[archive_name] = outer[archive_name]
            for name, content in members.items():
                sources[f"set{number}/{name}"] = content
        return sources, nested_archives

    if len(blobs) == len(sets):
        def unpack_delivery(item: tuple[int, bytes]):
            number, content = item
            return number, extract_zip_contents(content)

        with ThreadPoolExecutor(max_workers=min(4, len(blobs))) as pool:
            unpacked = list(pool.map(unpack_delivery, zip(sets, blobs)))
        for number, members in unpacked:
            for name, content in members.items():
                sources[f"set{number}/{name}"] = content
        return sources, nested_archives

    return None


def set_numbers(questions: list[dict]) -> list[int]:
    values = set()
    for question in questions:
        match = re.match(r"set(\d+)\.", question.get("id", ""), re.I)
        if match:
            values.add(int(match.group(1)))
        if isinstance(question.get("set"), int):
            values.add(question["set"])
    return sorted(values)


def submit(
    proxy: str,
    challenge: str,
    answers: dict[str, str],
    session: requests.Session,
) -> dict:
    return request_json(
        proxy, {"challenge": challenge, "answers": answers}, session=session
    )


def answer_batches(
    ids: list[str],
    answers: dict[str, str],
    challenge: str,
    batch_size: int | None = None,
) -> list[list[str]]:
    """Keep each submission within the API's answer-count and byte limits."""
    batches: list[list[str]] = []
    current: list[str] = []
    base_size = len(
        json.dumps({"challenge": challenge, "answers": {}}).encode()
    )
    current_answer_bytes = 0
    for answer_id in ids:
        pair_size = len(
            (
                json.dumps(answer_id)
                + ": "
                + json.dumps(answers[answer_id])
            ).encode()
        )
        separator_size = 2 if current else 0
        encoded_size = base_size + current_answer_bytes + separator_size + pair_size
        if current and (
            (batch_size is not None and len(current) + 1 > batch_size)
            or encoded_size > MAX_REQUEST_BYTES
        ):
            batches.append(current)
            current = [answer_id]
            current_answer_bytes = pair_size
            encoded_size = base_size + pair_size
        else:
            current.append(answer_id)
            current_answer_bytes += separator_size + pair_size
        if encoded_size > MAX_REQUEST_BYTES:
            raise ValueError(f"Answer {answer_id!r} exceeds the API request size limit")
    if current:
        batches.append(current)
    return batches


def recovery_batches(
    ids: list[str], result: str, accepted: set[str]
) -> list[list[str]]:
    """Return only unresolved IDs, splitting when a partial result makes no progress."""
    if result not in {"accepted", "incorrect"}:
        return []
    unresolved = [answer_id for answer_id in ids if answer_id not in accepted]
    if not unresolved:
        return []
    if result == "accepted" and len(unresolved) < len(ids):
        return [unresolved]
    if len(unresolved) == 1:
        return []
    middle = len(unresolved) // 2
    return [unresolved[:middle], unresolved[middle:]]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("challenge", help="challenge ID from the Game Master list")
    parser.add_argument("--retry", action="store_true")
    parser.add_argument(
        "--run-for-time",
        action="store_true",
        help="request a fresh timed Hall of Fame attempt",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="skip optional artifact hashing during a timed run",
    )
    parser.add_argument("--proxy", default=os.environ.get("GAME_MASTER_PROXY_URL", DEFAULT_PROXY))
    parser.add_argument(
        "--batch-size",
        type=int,
        help="optional maximum answers per request; JSON bodies are capped at 4 MiB",
    )
    args = parser.parse_args()
    if args.batch_size is not None and args.batch_size < 1:
        parser.error("--batch-size must be at least 1")

    # Load Python modules before requesting the assignment so their import cost
    # does not fall inside a server-timed attempt.
    tools = Path(__file__).resolve().parent
    sys.path.insert(0, str(tools))
    solver = importlib.import_module("script_analysis_solver")
    load_pyzipper()

    client_started = time.perf_counter()
    session = requests.Session()
    start_payload = {"challenge": args.challenge}
    if args.retry:
        start_payload["op"] = "retry"
    if args.run_for_time:
        start_payload["run_for_time"] = True
    response = request_json(args.proxy, start_payload, session=session)
    attempt_id = response.get("attempt_id", "unknown-attempt")
    day_match = re.search(r"-day-(\d+)(?:-|/)", args.challenge)
    day_dir = f"day-{int(day_match.group(1)):02d}" if day_match else "other"
    record = ROOT / "work" / day_dir / "script-analysis" / attempt_id
    record.mkdir(parents=True, exist_ok=True)
    (record / "start-response.json").write_text(
        json.dumps(response, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "stage": "attempt_started",
                "challenge": args.challenge,
                "mode": response.get("mode"),
                "attempt_id": attempt_id,
                "deadline": response.get("deadline"),
                "run_for_time": response.get("run_for_time"),
                "hall_of_fame_eligible": response.get("hall_of_fame_eligible"),
                "unique_attempts_remaining": response.get(
                    "unique_attempts_remaining"
                ),
                "answer_count": len(response.get("answer_ids", [])),
                "artifact_count": len(response.get("artifacts", [])),
            },
            separators=(",", ":"),
        ),
        flush=True,
    )

    questions = response.get("questions", [])
    sets = set_numbers(questions)
    artifact_specs = response.get("artifacts") or [
        {
            "filename": response.get("filename", "evidence.zip"),
            "sha256": response.get("sha256"),
        }
    ]
    extracted = record / "extracted"
    extracted.mkdir(parents=True, exist_ok=True)
    extracted_names: list[str] = []
    artifact_sources: dict[str, bytes] | None = None
    nested_archives: dict[str, bytes] = {}
    download_started = time.perf_counter()
    blobs = download_artifacts(
        args.proxy,
        args.challenge,
        len(artifact_specs),
        bool(response.get("artifacts")),
        session,
    )
    artifact_download_ms = (time.perf_counter() - download_started) * 1000

    processing_started = time.perf_counter()
    for index, (spec, blob) in enumerate(zip(artifact_specs, blobs)):
        if not args.fast:
            digest = hashlib.sha256(blob).hexdigest()
            if spec.get("sha256") and digest != spec["sha256"]:
                raise ValueError(f"SHA-256 mismatch for delivery {index + 1}")
        (record / f"evidence-{index + 1:02d}.zip").write_bytes(blob)
    mastery_contents = extract_mastery_contents(blobs, sets)
    if mastery_contents is not None:
        artifact_sources, nested_archives = mastery_contents
    else:
        for index, blob in enumerate(blobs):
            target = (
                extracted / f"set{sets[index]}"
                if len(sets) == len(artifact_specs)
                else extracted
            )
            extracted_names.extend(extract_zip(blob, target))
        if sets and len(artifact_specs) == 1:
            for nested in sorted(extracted.glob("*.zip")):
                match = re.search(r"(\d+)", nested.stem)
                if not match:
                    continue
                number = int(match.group(1))
                if number not in sets:
                    continue
                nested_dir = extracted / f"set{number}"
                extracted_names.extend(extract_zip(nested.read_bytes(), nested_dir))

    answers = solver.build_all_answers(
        response, extracted, artifact_sources=artifact_sources
    )
    solver.validate_answers(response, answers)
    candidate_json = (
        json.dumps(answers, ensure_ascii=False, separators=(",", ":"))
        if args.fast
        else json.dumps(answers, indent=2, ensure_ascii=False, sort_keys=True)
    )
    (record / "candidate-answers.json").write_text(candidate_json + "\n")
    processing_ms = (time.perf_counter() - processing_started) * 1000

    ids = [question["id"] for question in questions]
    accepted_file = record / "accepted-ids.json"
    accepted: set[str] = (
        set(json.loads(accepted_file.read_text())) if accepted_file.exists() else set()
    )
    accepted.intersection_update(ids)
    outcomes = []
    final = None
    stopped = False
    submission_ms = 0.0

    def submit_group(batch: list[str]) -> None:
        nonlocal final, stopped, submission_ms
        if stopped or not batch:
            return
        submit_started = time.perf_counter()
        result = submit(
            args.proxy,
            args.challenge,
            {key: answers[key] for key in batch},
            session,
        )
        submission_ms += (time.perf_counter() - submit_started) * 1000
        accepted.update(result.get("accepted_ids", []))
        compact_result = {
            key: result[key]
            for key in (
                "result",
                "flag",
                "remaining",
                "status",
                "solved",
                "message",
            )
            if key in result
        }
        outcomes.append(
            {
                "ids": batch,
                "response": compact_result,
                "accepted_ids_count": len(result.get("accepted_ids", [])),
            }
        )
        (record / "submission-outcomes.json").write_text(
            json.dumps(outcomes, indent=2, ensure_ascii=False) + "\n"
        )
        (record / "accepted-ids.json").write_text(
            json.dumps(sorted(accepted), indent=2) + "\n"
        )
        final = result
        if result.get("result") == "CORRECT":
            stopped = True
            return
        if result.get("result") in {"accepted", "incorrect"}:
            for retry_batch in recovery_batches(
                batch, result.get("result", ""), accepted
            ):
                submit_group(retry_batch)
            return
        stopped = True

    pending_ids = [answer_id for answer_id in ids if answer_id not in accepted]
    for batch in answer_batches(
        pending_ids, answers, args.challenge, args.batch_size
    ):
        submit_group(batch)
        if stopped:
            break

    # Keep the extracted evidence in the attempt record, but write Mastery's
    # thousands of small specimen files after the timed submission completes.
    for name, content in nested_archives.items():
        safe_write(extracted, name, content)
    if artifact_sources is not None:
        for name, content in artifact_sources.items():
            safe_write(extracted, name, content)

    status_url = (
        args.proxy + "?op=status&challenge="
        + urllib.parse.quote(args.challenge, safe="")
    )
    status_started = time.perf_counter()
    status = request_json(status_url, session=session)
    status_request_ms = (time.perf_counter() - status_started) * 1000
    (record / "submission-outcomes.json").write_text(
        json.dumps(outcomes, indent=2, ensure_ascii=False) + "\n"
    )
    (record / "status-response.json").write_text(
        json.dumps(status, indent=2, ensure_ascii=False) + "\n"
    )
    unresolved = sorted(set(ids) - set(status.get("accepted_ids", accepted)))
    (record / "unresolved-ids.json").write_text(
        json.dumps(unresolved, indent=2) + "\n"
    )
    summary = {
        "challenge": args.challenge,
        "mode": response.get("mode"),
        "attempt_id": attempt_id,
        "deadline": response.get("deadline"),
        "run_for_time": response.get("run_for_time"),
        "hall_of_fame_eligible": response.get("hall_of_fame_eligible"),
        "ranked_attempts_remaining": response.get("ranked_attempts_remaining"),
        "question_count": len(questions),
        "artifact_sha256": (
            []
            if args.fast
            else [
                hashlib.sha256(
                    (record / f"evidence-{index + 1:02d}.zip").read_bytes()
                ).hexdigest()
                for index in range(len(artifact_specs))
            ]
        ),
        "submission_result": (final or {}).get("result"),
        "accepted_id_count": len(status.get("accepted_ids", accepted)),
        "unresolved_count": len(unresolved),
        "flag": status.get("flag") or (final or {}).get("flag"),
        "scoring_status": (final or {}).get("status"),
        "artifact_download_ms": round(artifact_download_ms, 2),
        "processing_ms": round(processing_ms, 2),
        "submission_ms": round(submission_ms, 2),
        "status_request_ms": round(status_request_ms, 2),
        "client_total_ms": round((time.perf_counter() - client_started) * 1000, 2),
        "record": str(record),
    }
    (record / "final-submission-response.json").write_text(
        json.dumps(final or {}, indent=2, ensure_ascii=False) + "\n"
    )
    (record / "run-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["submission_result"] in {"accepted", "CORRECT"} else 3


if __name__ == "__main__":
    raise SystemExit(main())
