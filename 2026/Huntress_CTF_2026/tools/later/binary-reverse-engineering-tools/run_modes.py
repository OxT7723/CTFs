#!/usr/bin/env python3
"""Run a Binary Reverse Engineering mode using the live assignment."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import http.client
import importlib.util
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path, PurePosixPath


DEFAULT_PROXY = "http://192.0.2.1/huntress-ctf-proxy"
ROOT = Path(__file__).resolve().parents[1]
MAX_REQUEST_BYTES = 4 * 1024 * 1024


class GameMasterHTTPError(RuntimeError):
    def __init__(self, status_code: int, detail: object):
        self.status_code = status_code
        self.detail = detail
        if isinstance(detail, dict):
            code = detail.get("error", "")
            message = detail.get("message", "")
            summary = "; ".join(part for part in (str(code), str(message)) if part)
            retry_after = detail.get("retry_after_seconds")
            if retry_after is not None:
                summary += f" (retry after {retry_after}s)"
        else:
            summary = str(detail)[:500]
        super().__init__(f"Game Master HTTP {status_code}: {summary or 'request failed'}")


class PersistentHTTPClient:
    """Reuse one HTTP connection for sequential Game Master requests."""

    def __init__(self, base_url: str, timeout: int = 30):
        parsed = urllib.parse.urlsplit(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError(f"Unsupported Game Master URL: {base_url}")
        self.scheme = parsed.scheme
        self.authority = (parsed.hostname, parsed.port or (443 if parsed.scheme == "https" else 80))
        self.timeout = timeout
        self.connection = self._new_connection()

    def _new_connection(self):
        host, port = self.authority
        if self.scheme == "https":
            return http.client.HTTPSConnection(host, port, timeout=self.timeout)
        return http.client.HTTPConnection(host, port, timeout=self.timeout)

    def reconnect(self) -> None:
        self.connection.close()
        self.connection = self._new_connection()
        self.connection.connect()

    def request_json(self, url: str, payload: dict | None = None) -> dict:
        with self.request_stream(
            url,
            method="POST" if payload is not None else "GET",
            body=None if payload is None else json.dumps(payload).encode(),
            headers=(
                {"Content-Type": "application/json"}
                if payload is not None
                else None
            ),
        ) as response:
            response_body = response.read()
        return json.loads(response_body)

    def request_stream(
        self,
        url: str,
        method: str = "GET",
        body: bytes | None = None,
        headers: dict[str, str] | None = None,
    ):
        parsed = urllib.parse.urlsplit(url)
        authority = (parsed.hostname, parsed.port or (443 if parsed.scheme == "https" else 80))
        if parsed.scheme != self.scheme or authority != self.authority:
            raise ValueError("Persistent Game Master client cannot change origins")
        request_headers = {"Connection": "keep-alive"}
        if headers:
            request_headers.update(headers)
        target = urllib.parse.urlunsplit(("", "", parsed.path or "/", parsed.query, ""))
        try:
            self.connection.request(
                method,
                target,
                body=body,
                headers=request_headers,
            )
        except (BrokenPipeError, ConnectionResetError):
            # The proxy can close an idle keep-alive socket after local
            # analysis. A send failure occurs before getresponse(), so the
            # request body was not accepted as a complete Game Master request.
            self.reconnect()
            self.connection.request(
                method,
                target,
                body=body,
                headers=request_headers,
            )
        response = self.connection.getresponse()
        if response.status >= 400:
            response_body = response.read()
            response.close()
            try:
                detail = json.loads(response_body)
            except (UnicodeDecodeError, json.JSONDecodeError):
                detail = response_body.decode("utf-8", errors="replace")
            raise GameMasterHTTPError(response.status, detail)
        return response


def request_json(
    url: str,
    payload: dict | None = None,
    client: PersistentHTTPClient | None = None,
) -> dict:
    if client is not None:
        return client.request_json(url, payload)
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data is not None else {},
        method="POST" if data is not None else "GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as error:
        body = error.read()
        try:
            detail = json.loads(body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            detail = body.decode("utf-8", errors="replace")
        raise GameMasterHTTPError(error.code, detail) from error


def download_to_file(
    proxy: str,
    challenge: str,
    delivery: int | None,
    destination: Path,
    expected_sha256: str | None,
    verify_sha256: bool = True,
    client: PersistentHTTPClient | None = None,
) -> str | None:
    if verify_sha256 and destination.is_file() and expected_sha256:
        with destination.open("rb") as cached:
            cached_sha256 = hashlib.file_digest(cached, "sha256").hexdigest()
        if cached_sha256 == expected_sha256:
            return cached_sha256

    query = "?op=artifact&challenge=" + urllib.parse.quote(challenge, safe="")
    if delivery is not None:
        query += f"&delivery={delivery}"
    temporary = destination.with_suffix(destination.suffix + ".part")
    digest = hashlib.sha256() if verify_sha256 else None
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        response = (
            client.request_stream(proxy + query)
            if client is not None
            else urllib.request.urlopen(proxy + query, timeout=60)
        )
        with (
            response,
            temporary.open("wb") as output,
        ):
            while chunk := response.read(1024 * 1024):
                if digest is not None:
                    digest.update(chunk)
                output.write(chunk)
        actual_sha256 = digest.hexdigest() if digest is not None else None
        if expected_sha256 and actual_sha256 and actual_sha256 != expected_sha256:
            raise ValueError(f"SHA-256 mismatch for {destination.name}")
        temporary.replace(destination)
        return actual_sha256
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def extract_archive(data: bytes | Path, destination: Path) -> list[str]:
    import pyzipper

    destination.mkdir(parents=True, exist_ok=True)
    names = []
    source = str(data) if isinstance(data, Path) else io.BytesIO(data)
    with pyzipper.AESZipFile(source) as archive:
        archive.setpassword(b"infected")
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
            target.parent.mkdir(parents=True, exist_ok=True)
            content = archive.read(item)
            target.write_bytes(content)
            names.append(item.filename)
    (destination / ".archive-members.json").write_text(
        json.dumps(names, indent=2) + "\n"
    )
    return names


def numbered_sets(questions: list[dict]) -> list[int]:
    result = set()
    for question in questions:
        match = re.match(r"set(\d+)\.", question.get("id", ""), re.I)
        if match:
            result.add(int(match.group(1)))
        if isinstance(question.get("set"), int):
            result.add(question["set"])
    return sorted(result)


def submit(
    proxy: str,
    challenge: str,
    answers: dict[str, str],
    client: PersistentHTTPClient | None = None,
) -> dict:
    return request_json(
        proxy, {"challenge": challenge, "answers": answers}, client=client
    )


def answer_batches(
    challenge: str,
    ids: list[str],
    answers: dict[str, str],
    max_answers: int | None = None,
):
    """Batch within the Game Master's answer-count and JSON-size limits."""
    batch: list[str] = []
    for answer_id in ids:
        candidate = batch + [answer_id]
        payload = {
            "challenge": challenge,
            "answers": {key: answers[key] for key in candidate},
        }
        encoded_size = len(json.dumps(payload).encode())
        if batch and (
            (max_answers is not None and len(candidate) > max_answers)
            or encoded_size > MAX_REQUEST_BYTES
        ):
            yield batch
            batch = [answer_id]
            single_payload = {
                "challenge": challenge,
                "answers": {answer_id: answers[answer_id]},
            }
            if len(json.dumps(single_payload).encode()) > MAX_REQUEST_BYTES:
                raise ValueError(f"Answer {answer_id} exceeds the request size limit")
        else:
            batch = candidate
            if encoded_size > MAX_REQUEST_BYTES:
                raise ValueError(f"Answer {answer_id} exceeds the request size limit")
    if batch:
        yield batch


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
    parser.add_argument("challenge", help="challenge ID from the Game Master")
    parser.add_argument("--retry", action="store_true")
    parser.add_argument("--practice", action="store_true")
    parser.add_argument(
        "--run-for-time",
        action="store_true",
        help="request a fresh timed Hall of Fame attempt on a supported route",
    )
    parser.add_argument(
        "--skip-initial-status",
        action="store_true",
        help="skip the pre-submission status request for a newly started attempt",
    )
    parser.add_argument(
        "--skip-final-status",
        action="store_true",
        help="skip the post-submission status request after submitting answers",
    )
    parser.add_argument(
        "--keep-alive",
        action="store_true",
        help="reuse an HTTP connection for sequential Game Master JSON requests",
    )
    parser.add_argument(
        "--skip-artifact-hash",
        action="store_true",
        help="skip local artifact SHA-256 calculation and verification",
    )
    parser.add_argument(
        "--skip-answer-suffix",
        action="append",
        default=[],
        help="leave matching answer IDs unsubmitted while solving the remaining fields",
    )
    parser.add_argument("--proxy", default=os.environ.get("GAME_MASTER_PROXY_URL", DEFAULT_PROXY))
    parser.add_argument(
        "--batch-size",
        type=int,
        help="optional maximum answers per request; JSON bodies are capped at 4 MiB",
    )
    parser.add_argument(
        "--download-workers",
        type=int,
        choices=range(1, 9),
        default=3,
        metavar="{1..8}",
        help="number of concurrent artifact downloads (default: 3)",
    )
    args = parser.parse_args()
    if args.batch_size is not None and args.batch_size < 1:
        parser.error("--batch-size must be at least 1")
    if args.retry and args.practice:
        parser.error("--retry and --practice cannot be combined")
    if args.practice and args.run_for_time:
        parser.error("--practice cannot be combined with --run-for-time")
    try:
        import pyzipper  # noqa: F401
    except ModuleNotFoundError:
        parser.error(
            "pyzipper is required to read the assigned AES-encrypted evidence "
            "archive; install binary-reverse-engineering-tools/requirements.txt "
            "before starting a timed attempt"
        )

    tool_file = Path(__file__).with_name("analyze_evidence.py")
    module_spec = importlib.util.spec_from_file_location(
        "binary_evidence_solver", tool_file
    )
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError("Could not load the binary evidence analyzer")
    solver = importlib.util.module_from_spec(module_spec)
    sys.modules[module_spec.name] = solver
    module_spec.loader.exec_module(solver)

    client = PersistentHTTPClient(args.proxy) if args.keep_alive else None
    if client is not None:
        client.connection.connect()
    run_started = time.perf_counter()
    start_payload = {"op": "start", "challenge": args.challenge}
    if args.run_for_time:
        start_payload["run_for_time"] = True
    if args.retry:
        start_payload["op"] = "retry"
    elif args.practice:
        start_payload["op"] = "practice"
    start_request_started = time.perf_counter()
    response = request_json(args.proxy, start_payload, client=client)
    start_seconds = time.perf_counter() - start_request_started
    attempt_id = response.get("attempt_id")
    if not attempt_id:
        if response.get("result") == "CORRECT":
            print(
                json.dumps(
                    {
                        "challenge": args.challenge,
                        "submission_result": "CORRECT",
                        "downloaded": False,
                        "message": (
                            "The challenge is already complete; the response "
                            "contains no active attempt assignment."
                        ),
                    },
                    indent=2,
                )
            )
            return 0
        raise ValueError("Game Master response did not include an attempt ID")
    day_match = re.search(r"-day-(\d+)(?:-|/)", args.challenge)
    day_dir = f"day-{int(day_match.group(1)):02d}" if day_match else "other"
    record = ROOT / "work" / day_dir / "binary" / attempt_id
    record.mkdir(parents=True, exist_ok=True)
    (record / "start-response.json").write_text(
        json.dumps(response, indent=2, ensure_ascii=False) + "\n"
    )

    questions = response.get("questions", [])
    sets = numbered_sets(questions)
    specs = response.get("artifacts") or [
        {
            "filename": response.get("filename", "evidence.zip"),
            "sha256": response.get("sha256"),
        }
    ]
    extracted = record / "extracted"
    extracted.mkdir(parents=True, exist_ok=True)
    evidence_paths = [
        record / f"evidence-{index + 1:02d}.zip"
        for index in range(len(specs))
    ]
    hashes: list[str | None] = [""] * len(specs)
    download_started = time.perf_counter()
    if client is not None and len(specs) == 1:
        hashes[0] = download_to_file(
            args.proxy,
            args.challenge,
            0 if response.get("artifacts") else None,
            evidence_paths[0],
            specs[0].get("sha256"),
            not args.skip_artifact_hash,
            client,
        )
        print("Downloaded delivery 1/1", file=sys.stderr)
    else:
        with ThreadPoolExecutor(
            max_workers=min(args.download_workers, len(specs)),
            thread_name_prefix="artifact-download",
        ) as executor:
            futures = {
                executor.submit(
                    download_to_file,
                    args.proxy,
                    args.challenge,
                    index if response.get("artifacts") else None,
                    evidence_paths[index],
                    spec.get("sha256"),
                    not args.skip_artifact_hash,
                ): index
                for index, spec in enumerate(specs)
            }
            completed = 0
            for future in as_completed(futures):
                index = futures[future]
                hashes[index] = future.result()
                completed += 1
                print(
                    f"Verified delivery {index + 1}/{len(specs)} "
                    f"({completed} complete)",
                    file=sys.stderr,
                )
    download_seconds = time.perf_counter() - download_started

    extraction_started = time.perf_counter()
    for index, spec in enumerate(specs):
        target = extracted / f"set{sets[index]}" if len(sets) == len(specs) else extracted
        extract_archive(evidence_paths[index], target)

    if sets and len(specs) == 1:
        for nested in sorted(extracted.glob("*.zip")):
            match = re.search(r"(\d+)", nested.stem)
            if match and int(match.group(1)) in sets:
                extract_archive(nested, extracted / f"set{int(match.group(1))}")
    extraction_seconds = time.perf_counter() - extraction_started

    solver_started = time.perf_counter()
    answers = solver.build_all_answers(
        response,
        extracted,
        tuple(args.skip_answer_suffix),
    )
    solver_seconds = time.perf_counter() - solver_started
    expected = {question["id"] for question in questions}
    skipped = {
        answer_id
        for answer_id in expected
        if any(answer_id.endswith(suffix) for suffix in args.skip_answer_suffix)
    }
    if set(answers) != expected - skipped:
        raise ValueError("Candidate answer IDs do not match the live assignment")
    (record / "candidate-answers.json").write_text(
        json.dumps(answers, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    )

    # Timed analysis can outlast the proxy's keep-alive idle timeout.
    if client is not None:
        client.reconnect()

    status_url = (
        args.proxy + "?op=status&challenge="
        + urllib.parse.quote(args.challenge, safe="")
    )
    status_seconds = 0.0
    initial_status = {}
    if not args.skip_initial_status:
        status_started = time.perf_counter()
        initial_status = request_json(status_url, client=client)
        status_seconds += time.perf_counter() - status_started
    previously_accepted = set(initial_status.get("accepted_ids", []))
    previous_summary_path = record / "run-summary.json"
    if not previously_accepted and previous_summary_path.is_file():
        previous_summary = json.loads(previous_summary_path.read_text())
        if previous_summary.get("attempt_id") == attempt_id:
            previously_accepted = expected - set(
                previous_summary.get("unresolved_ids", [])
            )
    if initial_status.get("result") == "CORRECT":
        previously_accepted = set(expected)
    submit_ids = expected - skipped
    ids = [
        question["id"]
        for question in questions
        if question["id"] in submit_ids
        and question["id"] not in previously_accepted
    ]
    accepted: set[str] = set()
    outcomes = []
    final = initial_status if not ids else None
    stopped = False
    submission_seconds = 0.0
    submission_stop_reason = None

    def submit_group(batch: list[str]) -> None:
        nonlocal final, stopped, submission_seconds, submission_stop_reason
        if stopped or not batch:
            return
        batch = [answer_id for answer_id in batch if answer_id not in accepted]
        if not batch:
            return
        submit_started = time.perf_counter()
        try:
            result = submit(
                args.proxy,
                args.challenge,
                {key: answers[key] for key in batch},
                client=client,
            )
        except GameMasterHTTPError as error:
            submission_seconds += time.perf_counter() - submit_started
            if error.status_code != 429:
                raise
            detail = error.detail if isinstance(error.detail, dict) else {}
            outcomes.append(
                {
                    "ids": batch,
                    "http_status": error.status_code,
                    "error": detail.get("error"),
                    "retry_after_seconds": detail.get("retry_after_seconds"),
                }
            )
            submission_stop_reason = str(error)
            stopped = True
            return
        submission_seconds += time.perf_counter() - submit_started
        outcomes.append({"ids": batch, "result": result.get("result")})
        accepted.update(result.get("accepted_ids", []))
        final = result
        if result.get("result") == "CORRECT":
            stopped = True
        elif result.get("result") in {"accepted", "incorrect"}:
            if result.get("result") == "incorrect" and response.get("deadline"):
                submission_stop_reason = (
                    "Timed answer batch was incorrect; stopped automatic "
                    "bisecting so the artifact can be reviewed offline."
                )
                stopped = True
                return
            for retry_batch in recovery_batches(
                batch, result.get("result", ""), accepted
            ):
                submit_group(retry_batch)
        elif result.get("result") != "incorrect":
            stopped = True

    for batch in answer_batches(args.challenge, ids, answers, args.batch_size):
        submit_group(batch)
        if stopped:
            break

    status = {}
    if not args.skip_final_status:
        status_started = time.perf_counter()
        status = request_json(status_url, client=client)
        status_seconds += time.perf_counter() - status_started
    (record / "submission-outcomes.json").write_text(
        json.dumps(outcomes, indent=2, ensure_ascii=False) + "\n"
    )
    if not args.skip_final_status:
        (record / "status-response.json").write_text(
            json.dumps(status, indent=2, ensure_ascii=False) + "\n"
        )
    accepted_final = (
        set(status.get("accepted_ids", []))
        | set((final or {}).get("accepted_ids", []))
        | previously_accepted
        | accepted
    )
    if (final or {}).get("result") == "CORRECT":
        accepted_final |= expected
    summary = {
        "challenge": args.challenge,
        "mode": status.get("mode", response.get("mode")),
        "attempt_id": attempt_id,
        "deadline": status.get("deadline") or response.get("deadline"),
        "hall_of_fame_eligible": status.get(
            "hall_of_fame_eligible", response.get("hall_of_fame_eligible")
        ),
        "unique_attempts_remaining": status.get(
            "unique_attempts_remaining", response.get("unique_attempts_remaining")
        ),
        "variant_fresh": status.get("variant_fresh", response.get("variant_fresh")),
        "question_count": len(questions),
        "artifact_sha256": hashes,
        "download_workers": min(args.download_workers, len(specs)),
        "start_seconds": round(start_seconds, 4),
        "download_seconds": round(download_seconds, 3),
        "extraction_seconds": round(extraction_seconds, 4),
        "solver_seconds": round(solver_seconds, 4),
        "status_seconds": round(status_seconds, 4),
        "submission_seconds": round(submission_seconds, 4),
        "total_seconds": round(time.perf_counter() - run_started, 4),
        "submission_stop_reason": submission_stop_reason,
        "submission_result": (
            status.get("result")
            if status.get("result") == "CORRECT"
            else (final or {}).get("result")
        ),
        "accepted_id_count": len(accepted_final),
        "unresolved_ids": sorted(expected - accepted_final),
        "skipped_ids": sorted(skipped),
        "flag": status.get("flag") or (final or {}).get("flag"),
        "record": str(record),
    }
    (record / "run-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["submission_result"] in {"accepted", "CORRECT"} else 3


if __name__ == "__main__":
    raise SystemExit(main())
