#!/usr/bin/env python3
"""Run a Warmups mode using the current assignment and mixed-codec decoder."""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import http.client
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path


DEFAULT_PROXY = "http://192.0.2.1/huntress-ctf-proxy"
ROOT = Path(__file__).resolve().parents[1]
ZIP_PASSWORD = b"infected"


class GameMasterHTTPError(RuntimeError):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        super().__init__(f"Game Master HTTP {status_code}: {detail[:500]}")


class PersistentHTTPClient:
    """Reuse one Game Master proxy connection across sequential requests."""

    def __init__(self, base_url: str, timeout: int = 60):
        parsed = urllib.parse.urlsplit(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError(f"Unsupported Game Master URL: {base_url}")
        self.scheme = parsed.scheme
        self.authority = (
            parsed.hostname,
            parsed.port or (443 if parsed.scheme == "https" else 80),
        )
        self.timeout = timeout
        if self.scheme == "https":
            self.connection = http.client.HTTPSConnection(
                *self.authority, timeout=timeout
            )
        else:
            self.connection = http.client.HTTPConnection(
                *self.authority, timeout=timeout
            )

    def _request(
        self, url: str, payload: dict | None = None
    ) -> tuple[http.client.HTTPResponse, bytes]:
        parsed = urllib.parse.urlsplit(url)
        authority = (
            parsed.hostname,
            parsed.port or (443 if parsed.scheme == "https" else 80),
        )
        if parsed.scheme != self.scheme or authority != self.authority:
            raise ValueError("Persistent Game Master client cannot change origins")
        body = None if payload is None else json.dumps(payload).encode()
        headers = {"Connection": "keep-alive"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        target = urllib.parse.urlunsplit(
            ("", "", parsed.path or "/", parsed.query, "")
        )
        self.connection.request(
            "POST" if body is not None else "GET",
            target,
            body=body,
            headers=headers,
        )
        response = self.connection.getresponse()
        response_body = response.read()
        if response.status >= 400:
            detail = response_body.decode("utf-8", errors="replace")[:500]
            raise GameMasterHTTPError(
                response.status, detail or "request failed"
            )
        return response, response_body

    def request_json(self, url: str, payload: dict | None = None) -> dict:
        _, body = self._request(url, payload)
        return json.loads(body)

    def request_bytes(self, url: str) -> tuple[object, bytes]:
        response, body = self._request(url)
        return response.headers, body

    def close(self) -> None:
        self.connection.close()

    def reconnect(self) -> None:
        """Replace a keep-alive connection that may have expired while idle."""
        self.connection.close()
        if self.scheme == "https":
            self.connection = http.client.HTTPSConnection(
                *self.authority, timeout=self.timeout
            )
        else:
            self.connection = http.client.HTTPConnection(
                *self.authority, timeout=self.timeout
            )


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
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read())


def archive_files(data: bytes) -> dict[str, bytes]:
    if not zipfile.is_zipfile(io.BytesIO(data)):
        return {}
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            if any(item.flag_bits & 1 for item in archive.infolist()):
                raise zipfile.BadZipFile("encrypted")
            return {
                Path(item.filename).name: archive.read(item)
                for item in archive.infolist()
                if not item.is_dir()
            }
    except zipfile.BadZipFile:
        try:
            import pyzipper
        except ModuleNotFoundError as error:
            raise RuntimeError(
                "pyzipper is required to read encrypted ZIP artifacts"
            ) from error

        with pyzipper.AESZipFile(io.BytesIO(data)) as archive:
            archive.setpassword(ZIP_PASSWORD)
            return {
                Path(item.filename).name: archive.read(item)
                for item in archive.infolist()
                if not item.is_dir()
            }


def download_artifact(
    proxy: str,
    challenge: str,
    index: int,
    spec: dict,
    has_artifact_specs: bool,
    verify_sha256: bool = True,
    client: PersistentHTTPClient | None = None,
) -> tuple[str, bytes, str | None]:
    capability_path = spec.get("download", "")
    capability = capability_path.rsplit("/", 1)[-1]
    if re.fullmatch(r"[0-9a-f]{64}", capability):
        download_url = proxy + "?op=download&capability=" + capability
    else:
        download_url = ""
    artifact_query = (
        "?op=artifact&challenge=" + urllib.parse.quote(challenge, safe="")
    )
    if has_artifact_specs:
        artifact_query += f"&delivery={index}"
    artifact_url = proxy + artifact_query

    def fetch(url: str) -> tuple[object, bytes]:
        if client is not None:
            return client.request_bytes(url)
        with urllib.request.urlopen(url, timeout=60) as response:
            return response.headers, response.read()

    if download_url:
        try:
            headers, data = fetch(download_url)
        except (GameMasterHTTPError, urllib.error.HTTPError) as error:
            status_code = getattr(
                error, "status_code", getattr(error, "code", None)
            )
            if status_code != 404:
                raise
            headers, data = fetch(artifact_url)
    else:
        headers, data = fetch(artifact_url)

    disposition = headers.get("Content-Disposition", "")
    match = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)', disposition, re.I)
    filename = Path(spec.get("filename") or (
        urllib.parse.unquote(match.group(1)) if match else "blob.txt"
    )).name
    digest = hashlib.sha256(data).hexdigest() if verify_sha256 else None
    expected = spec.get("sha256")
    if expected and digest and expected != digest:
        raise ValueError(f"Assigned artifact SHA-256 does not match {filename}")
    return filename, data, digest


def token_from_text(syntax: str, decoded: bytes) -> str:
    text = decoded.decode("utf-8")
    number_words = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    }

    def count_from(match: re.Match | None, fallback: int) -> int:
        if not match:
            return fallback
        value = match.group(1).lower()
        return int(value) if value.isdigit() else number_words.get(value, fallback)

    words = count_from(
        re.search(r"(\d+|[a-z]+)\s+lowercase words", syntax, re.I), 0
    )
    digits = count_from(re.search(r"(\d+|[a-z]+)-digit", syntax, re.I), 2)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    final_line = lines[-1] if lines else text.strip()
    if words:
        master_instruction = re.search(
            r"\bGame Master:\s*([a-z0-9]+(?:-[a-z0-9]+)+)",
            final_line,
            re.I,
        )
        if master_instruction:
            return master_instruction.group(1).strip(".,;:!\"'")
        exact_instruction = re.search(
            r"\bsubmit this exact answer to the Game Master:\s*(\S+)",
            final_line,
            re.I,
        )
        if exact_instruction:
            instructed = exact_instruction.group(1).strip(".,;:!\"'")
            if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)+", instructed):
                return instructed
        pattern = re.compile(
            rf"\b[a-z]+(?:-[a-z]+){{{words - 1}}}-\d{{{digits}}}\b"
        )
        matches = pattern.findall(final_line)
        if matches:
            return matches[-1]
        # Some assignments serialize a character stream as comma-delimited
        # count:value entries. The value itself may be a comma, so split-based
        # parsing loses it; use the next count prefix as the delimiter.
        counted_chars = list(
            re.finditer(r"(?:^|,)(\d+):(.*?)(?=,\d+:|$)", final_line)
        )
        if len(counted_chars) > 1:
            expanded = "".join(
                match.group(2) * int(match.group(1))
                for match in counted_chars
            )
            matches = pattern.findall(expanded)
            if matches:
                return matches[-1]
        # Mixed-codec assignments can leave a slug fragment hex-encoded
        # between readable fragments. Decode only spans that produce the
        # exact requested slug shape.
        partial = final_line.rsplit(None, 1)[-1].strip(".,;:!\"'")
        for start in range(len(partial)):
            for end in range(len(partial), start + 1, -1):
                encoded = partial[start:end]
                if len(encoded) % 2 or not re.fullmatch(r"[0-9a-fA-F]+", encoded):
                    continue
                try:
                    decoded_hex = bytes.fromhex(encoded).decode("ascii")
                except (ValueError, UnicodeDecodeError):
                    continue
                candidate = f"{partial[:start]}{decoded_hex}{partial[end:]}"
                if pattern.fullmatch(candidate):
                    return candidate
        raise ValueError("Decoded artifact does not match the requested answer format")
    if not lines:
        raise ValueError("Decoded artifact has no non-empty text")
    return final_line


def build_answers(response: dict, delivery_blobs: list[bytes]) -> tuple[dict[str, str], int | None]:
    """Decode each question from its assigned artifact delivery."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from decode_base64_layers import decode_assignment, infer_rail_fence_rails

    if not delivery_blobs:
        raise ValueError("The assignment has no downloaded artifacts")
    extracted_by_delivery = [archive_files(blob) for blob in delivery_blobs]
    assigned_blobs: list[bytes] = []
    for question in response.get("questions", []):
        set_match = re.match(r"set(\d+)\.", question.get("id", ""), re.I)
        delivery_match = re.search(
            r"\bdelivery\s+(\d+)\b", question.get("artifact", ""), re.I
        )
        set_number = int(set_match.group(1)) if set_match else None
        delivery_number = int(delivery_match.group(1)) if delivery_match else None
        if (
            len(delivery_blobs) > 1
            and set_number is not None
            and delivery_number is not None
            and set_number != delivery_number
        ):
            raise ValueError(f"Conflicting delivery information for {question['id']}")
        selected = (
            (delivery_number or set_number) if len(delivery_blobs) > 1 else 1
        )
        if selected is None or not 1 <= selected <= len(delivery_blobs):
            raise ValueError(f"Cannot identify artifact delivery for {question['id']}")
        index = selected - 1
        descriptor_text = question.get("artifact", "").split("->")[-1].strip()
        descriptor_text = re.sub(r"^delivery\s+\d+\s*:\s*", "", descriptor_text, flags=re.I)
        descriptor = Path(descriptor_text).name
        assigned_blobs.append(
            extracted_by_delivery[index].get(descriptor, delivery_blobs[index])
        )

    # Rail inference compares each rail count across every assigned blob. On
    # large bundles, decoding each answer already tries all rail counts and
    # uses the final answer pattern to choose the valid reconstruction, so
    # skip the expensive global comparison.
    rail_fence_rails = (
        infer_rail_fence_rails(assigned_blobs)
        if 1 < len(assigned_blobs) <= 16
        else None
    )
    answers = {}
    for question, assigned in zip(response.get("questions", []), assigned_blobs):
        decoded = decode_assignment(assigned, rail_fence_rails=rail_fence_rails)
        syntax = question.get("answer_format", {}).get("syntax", "")
        try:
            answers[question["id"]] = token_from_text(syntax, decoded)
        except ValueError as error:
            raise ValueError(f"{question['id']}: {error}") from error
    if set(answers) != set(response.get("answer_ids", [])):
        raise ValueError("Candidate answer IDs do not match the live response")
    return answers, rail_fence_rails


def outstanding_answers(
    answers: dict[str, str], accepted_ids: list[str] | set[str]
) -> dict[str, str]:
    """Keep reconnect submissions limited to answer IDs still outstanding."""
    accepted = set(accepted_ids)
    return {
        answer_id: answer
        for answer_id, answer in answers.items()
        if answer_id not in accepted
    }


def main() -> int:
    run_started = time.perf_counter()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("challenge", help="challenge ID from the Game Master")
    parser.add_argument("--retry", action="store_true")
    parser.add_argument("--practice", action="store_true")
    parser.add_argument(
        "--run-for-time",
        action="store_true",
        help="request a fresh ranked timed attempt on a dual-pool route",
    )
    parser.add_argument(
        "--skip-artifact-hash",
        action="store_true",
        help="skip optional artifact SHA-256 verification to save timed processing",
    )
    parser.add_argument(
        "--keep-alive",
        action="store_true",
        help="warm and reuse one proxy connection for a legacy timed retry",
    )
    parser.add_argument("--proxy", default=os.environ.get("GAME_MASTER_PROXY_URL", DEFAULT_PROXY))
    args = parser.parse_args()
    if args.retry and args.practice:
        parser.error("--retry and --practice cannot be combined")
    if args.run_for_time and args.practice:
        parser.error("--run-for-time and --practice cannot be combined")
    if args.keep_alive and not args.retry:
        parser.error("--keep-alive requires --retry")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import decode_base64_layers  # noqa: F401

    status_url = (
        args.proxy + "?op=status&challenge="
        + urllib.parse.quote(args.challenge, safe="")
    )
    client = (
        PersistentHTTPClient(args.proxy)
        if args.keep_alive or args.run_for_time
        else None
    )
    preflight = None
    timings: dict[str, float] = {}
    if client is not None:
        stage_started = time.perf_counter()
        preflight = request_json(status_url, client=client)
        timings["preflight_ms"] = (time.perf_counter() - stage_started) * 1000
    if args.retry and preflight is not None:
        result = preflight.get("result")
        deadline = preflight.get("deadline")
        if result not in {"CORRECT", "expired"}:
            if deadline is None:
                client.close()
                raise RuntimeError(
                    "Cannot safely retry: the current attempt has no ended deadline"
                )
            parsed_deadline = dt.datetime.fromisoformat(
                deadline.replace("Z", "+00:00")
            )
            if parsed_deadline > dt.datetime.now(dt.timezone.utc):
                client.close()
                raise RuntimeError(
                    "Cannot safely retry: a timed attempt is still active"
                )

    payload = {"challenge": args.challenge}
    if args.retry:
        payload["op"] = "retry"
    elif args.practice:
        payload["op"] = "practice"
    elif args.run_for_time:
        result = preflight.get("result") if preflight is not None else None
        deadline = preflight.get("deadline") if preflight is not None else None
        active_deadline = (
            dt.datetime.fromisoformat(deadline.replace("Z", "+00:00"))
            if deadline
            else None
        )
        if (
            preflight is None
            or not preflight.get("attempt_id")
        ):
            payload["op"] = "start"
        elif (
            result not in {"CORRECT", "expired"}
            and active_deadline is not None
            and active_deadline > dt.datetime.now(dt.timezone.utc)
        ):
            if preflight.get("run_for_time") is not True:
                client.close()
                raise RuntimeError(
                    "A regular attempt is still active; finish it before "
                    "starting a ranked timed attempt"
                )
            payload["op"] = "start"
        elif result in {"CORRECT", "expired"}:
            payload["op"] = "retry"
        else:
            client.close()
            raise RuntimeError(
                "The current attempt is not complete; refusing to advance "
                "to another ranked variant"
            )
    if args.run_for_time:
        payload["run_for_time"] = True
    start_request_started = time.perf_counter()
    response = request_json(args.proxy, payload, client=client)
    timings["start_request_ms"] = (
        time.perf_counter() - start_request_started
    ) * 1000
    attempt_started = start_request_started
    if args.run_for_time and (
        response.get("run_for_time") is not True
        or response.get("hall_of_fame_eligible") is not True
        or not response.get("deadline")
    ):
        if client is not None:
            client.close()
        raise RuntimeError(
            "Game Master did not confirm a ranked timed attempt; "
            "stopping before artifact processing"
        )
    attempt_id = response.get("attempt_id", "unknown-attempt")
    day_match = re.search(r"-day-(\d+)(?:-|/|$)", args.challenge)
    day_dir = f"day-{int(day_match.group(1)):02d}" if day_match else "other"
    record = ROOT / "work" / day_dir / "warmups" / attempt_id
    record.mkdir(parents=True, exist_ok=True)
    (record / "start-response.json").write_text(
        json.dumps(response, indent=2, ensure_ascii=False) + "\n"
    )

    specs = response.get("artifacts") or [
        {
            "filename": response.get("filename", "blob.txt"),
            "sha256": response.get("sha256"),
        }
    ]
    download_args = [
        (
            args.proxy,
            args.challenge,
            index,
            spec,
            bool(response.get("artifacts")),
            not args.skip_artifact_hash,
            client if client is not None and index == 0 else None,
        )
        for index, spec in enumerate(specs)
    ]
    stage_started = time.perf_counter()
    if len(download_args) == 1:
        downloads = [download_artifact(*download_args[0])]
    else:
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=min(len(download_args), 8)
        ) as pool:
            downloads = list(pool.map(
                lambda values: download_artifact(*values), download_args
            ))
    timings["download_ms"] = (time.perf_counter() - stage_started) * 1000

    blobs = []
    hashes = []
    artifact_write_started = time.perf_counter()
    for index, (filename, data, digest) in enumerate(downloads):
        spec = specs[index]
        expected = spec.get("sha256") or (
            response.get("sha256") if not response.get("artifacts") else None
        )
        if expected and digest and expected != digest:
            raise ValueError(f"Assigned artifact SHA-256 does not match {filename}")
        blobs.append(data)
        hashes.append(digest)
        artifact_dir = record / f"delivery-{index + 1:02d}" if len(specs) > 1 else record
        artifact_dir.mkdir(parents=True, exist_ok=True)
        (artifact_dir / filename).write_bytes(data)
        extracted_files = [] if args.run_for_time else archive_files(data)
        if extracted_files:
            extracted = artifact_dir / "extracted"
            extracted.mkdir(exist_ok=True)
            for member, member_data in extracted_files.items():
                (extracted / member).write_bytes(member_data)
    timings["artifact_write_ms"] = (
        time.perf_counter() - artifact_write_started
    ) * 1000

    decode_started = time.perf_counter()
    answers, rail_fence_rails = build_answers(response, blobs)
    decode_seconds = time.perf_counter() - decode_started
    timings["decode_ms"] = decode_seconds * 1000
    (record / "candidate-answers.json").write_text(
        json.dumps(answers, indent=2, ensure_ascii=False) + "\n"
    )
    if client is not None and decode_seconds >= 2:
        client.reconnect()
    accepted_before = set(response.get("accepted_ids", []))
    outstanding = outstanding_answers(answers, accepted_before)
    submit_started = time.perf_counter()
    if outstanding:
        try:
            result = request_json(
                args.proxy,
                {"challenge": args.challenge, "answers": outstanding},
                client=client,
            )
        except (
            http.client.RemoteDisconnected,
            ConnectionError,
            TimeoutError,
            urllib.error.URLError,
        ):
            # The submit may have reached the Game Master even if its response
            # was lost. Reconcile this exact attempt before resending anything.
            progress = request_json(status_url)
            if progress.get("attempt_id") != attempt_id:
                raise RuntimeError(
                    "Submission response was lost and status returned a "
                    "different attempt; refusing to resubmit"
                )
            remaining = outstanding_answers(
                answers, progress.get("accepted_ids", [])
            )
            if progress.get("result") == "CORRECT" or not remaining:
                result = progress
            elif remaining:
                result = request_json(
                    args.proxy,
                    {"challenge": args.challenge, "answers": remaining},
                )
            else:
                result = progress
    else:
        result = {
            "result": response.get("result") or "CORRECT",
            "accepted_ids": sorted(accepted_before),
            "already_accepted": True,
        }
    batch_result = result
    individual_results = []
    if result.get("result") == "incorrect" and len(outstanding) > 1:
        (record / "batch-submission-result.json").write_text(
            json.dumps(batch_result, indent=2, ensure_ascii=False) + "\n"
        )
        progress = request_json(status_url, client=client)
        accepted_after_batch = set(progress.get("accepted_ids", []))
        for answer_id, answer in outstanding.items():
            if answer_id in accepted_after_batch:
                continue
            result = request_json(
                args.proxy,
                {"challenge": args.challenge, "answers": {answer_id: answer}},
                client=client,
            )
            accepted_after_batch.update(result.get("accepted_ids", []))
            individual_results.append(
                {"answer_id": answer_id, "result": result.get("result")}
            )
            if result.get("result") == "CORRECT":
                break
        (record / "individual-submission-results.json").write_text(
            json.dumps(individual_results, indent=2, ensure_ascii=False) + "\n"
        )
    timings["submit_ms"] = (time.perf_counter() - submit_started) * 1000
    if result.get("result") == "CORRECT":
        timings["client_elapsed_from_start_request_to_correct_ms"] = (
            time.perf_counter() - attempt_started
        ) * 1000
    stage_started = time.perf_counter()
    status = request_json(status_url, client=client)
    timings["final_status_ms"] = (time.perf_counter() - stage_started) * 1000
    timings["total_elapsed_ms"] = (time.perf_counter() - run_started) * 1000
    final_result = status.get("result") or result.get("result")
    (record / "submission-result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    )
    (record / "status-response.json").write_text(
        json.dumps(status, indent=2, ensure_ascii=False) + "\n"
    )
    summary = {
        "challenge": args.challenge,
        "mode": response.get("mode"),
        "attempt_id": attempt_id,
        "started_at": response.get("started_at"),
        "deadline": response.get("deadline"),
        "run_for_time": response.get("run_for_time", False),
        "hall_of_fame_eligible": response.get("hall_of_fame_eligible", False),
        "artifact_sha256": hashes[0] if len(hashes) == 1 else hashes,
        "inferred_rail_fence_rails": rail_fence_rails,
        "decode_ms": round(decode_seconds * 1000, 3),
        "timings": {key: round(value, 3) for key, value in timings.items()},
        "result": final_result,
        "batch_result": batch_result.get("result"),
        "flag": status.get("flag") or result.get("flag"),
        "record": str(record),
    }
    (record / "run-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if client is not None:
        client.close()
    return 0 if summary["result"] == "CORRECT" else 3


if __name__ == "__main__":
    raise SystemExit(main())
