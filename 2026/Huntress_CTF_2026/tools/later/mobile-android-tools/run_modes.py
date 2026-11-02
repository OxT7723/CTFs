#!/usr/bin/env python3
"""Solve a Mobile Android attempt, or run the solver offline on saved APKs."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import http.client
import io
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
from pathlib import Path


DEFAULT_PROXY = "http://192.0.2.1/huntress-ctf-proxy"
TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
from decode_puzzle_assets import decoded_android_assets


class KeepAliveHTTPClient:
    """Reuse one HTTP/1.1 connection per thread and endpoint."""

    def __init__(self) -> None:
        self._local = threading.local()

    def close_current_thread_connections(self) -> None:
        """Drop idle sockets before a delayed state-changing request."""
        connections = getattr(self._local, "connections", {})
        self._local.connections = {}
        for connection in connections.values():
            connection.close()

    def request(
        self, url: str, payload: dict | None = None, timeout: int = 30
    ) -> tuple[bytes, http.client.HTTPMessage]:
        parts = urllib.parse.urlsplit(url)
        if parts.scheme not in {"http", "https"} or not parts.hostname:
            raise ValueError(f"Unsupported Game Master URL: {url}")

        port = parts.port or (443 if parts.scheme == "https" else 80)
        endpoint = (parts.scheme, parts.hostname, port)
        connections = getattr(self._local, "connections", None)
        if connections is None:
            connections = self._local.connections = {}

        connection = connections.get(endpoint)
        if connection is None:
            connection_type = (
                http.client.HTTPSConnection
                if parts.scheme == "https"
                else http.client.HTTPConnection
            )
            connection = connection_type(
                parts.hostname, port=port, timeout=timeout
            )
            connections[endpoint] = connection

        target = parts.path or "/"
        if parts.query:
            target += "?" + parts.query
        data = None if payload is None else json.dumps(payload).encode()
        headers = {"Connection": "keep-alive"}
        if data is not None:
            headers["Content-Type"] = "application/json"

        try:
            connection.request(
                "POST" if data is not None else "GET",
                target,
                body=data,
                headers=headers,
            )
            response = connection.getresponse()
            body = response.read()
            response_headers = response.headers
            status = response.status
            reason = response.reason
            will_close = response.will_close
        except Exception:
            connections.pop(endpoint, None)
            connection.close()
            raise

        if will_close:
            connections.pop(endpoint, None)
            connection.close()
        if status < 200 or status >= 300:
            raise urllib.error.HTTPError(
                url,
                status,
                reason,
                response_headers,
                io.BytesIO(body),
            )
        return body, response_headers


HTTP = KeepAliveHTTPClient()


def request_json(url: str, payload: dict | None = None) -> dict:
    body, _ = HTTP.request(url, payload, timeout=30)
    return json.loads(body)


def fetch_artifact(
    proxy: str,
    challenge: str,
    delivery: int | None,
    download_path: str | None = None,
) -> tuple[bytes, str]:
    capability_match = re.fullmatch(
        r"/api/huntress/game-master/download/([0-9a-f]{64})",
        urllib.parse.urlsplit(download_path or "").path,
    )
    if capability_match:
        query = {"op": "download", "capability": capability_match.group(1)}
    else:
        query = {"op": "artifact", "challenge": challenge}
        if delivery is not None:
            query["delivery"] = str(delivery)
    data, headers = HTTP.request(
        proxy + "?" + urllib.parse.urlencode(query), timeout=60
    )
    disposition = headers.get("Content-Disposition", "")
    match = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)', disposition, re.I)
    filename = urllib.parse.unquote(match.group(1)) if match else "assigned.apk"
    return data, Path(filename).name


def candidate_from_asset(syntax: str, decoded: bytes) -> str:
    text = decoded.decode("utf-8").strip()
    pattern = re.search(
        r"([A-Z][A-Z0-9_-]*-)\s*followed by exactly\s+(\d+)\s+"
        r"uppercase hexadecimal characters?",
        syntax,
        re.I,
    )
    if pattern:
        token = re.search(
            re.escape(pattern.group(1))
            + rf"[A-Fa-f0-9]{{{int(pattern.group(2))}}}",
            text,
        )
        if not token:
            raise ValueError(
                "Decoded asset does not contain a token matching the API format"
            )
        return token.group(0)
    return text


def delivery_index_for_question(question: dict) -> int | None:
    delivery_match = re.search(
        r"delivery\s+(\d+)", question.get("artifact", ""), re.I
    )
    delivery_number = question.get("set")
    if not isinstance(delivery_number, int) and delivery_match:
        delivery_number = int(delivery_match.group(1))
    if isinstance(delivery_number, int):
        if delivery_number < 1:
            raise ValueError(
                f"Question {question.get('id')} refers to invalid delivery "
                f"{delivery_number}"
            )
        return delivery_number - 1
    return None


def delivery_for_question(question: dict, count: int) -> int:
    delivery_index = delivery_index_for_question(question)
    if delivery_index is not None:
        if delivery_index >= count:
            raise ValueError(
                f"Question {question.get('id')} refers to missing delivery "
                f"{delivery_index + 1} (received {count} artifacts)"
            )
        return delivery_index
    if count == 1:
        return 0
    raise ValueError(
        f"Cannot associate question {question.get('id')} with one of "
        f"{count} artifacts"
    )


def answer_ids_for_response(response: dict) -> list[str]:
    return response.get("answer_ids") or [
        question["id"] for question in response.get("questions", [])
    ]


def solve_response(
    response: dict,
    apk_paths: list[Path],
    verify_dex_integrity: bool = True,
) -> tuple[dict[str, str], float]:
    started = time.perf_counter()
    decoded_by_delivery = [
        decoded_android_assets(path, verify_dex_integrity=verify_dex_integrity)
        for path in apk_paths
    ]
    answers: dict[str, str] = {}
    for question in response.get("questions", []):
        answer_id = question["id"]
        delivery = delivery_for_question(question, len(decoded_by_delivery))
        syntax = question.get("answer_format", {}).get("syntax", "")
        matches = []
        for _, value in decoded_by_delivery[delivery]:
            try:
                matches.append(candidate_from_asset(syntax, value))
            except (UnicodeDecodeError, ValueError):
                continue
        if not matches:
            raise ValueError(f"No decoded answer candidate for {answer_id}")
        if len(set(matches)) != 1:
            raise ValueError(f"Ambiguous decoded answers for {answer_id}")
        answers[answer_id] = matches[0]

    if not answers:
        raise ValueError("The Game Master response contained no questions")
    expected_answer_ids = answer_ids_for_response(response)
    if set(answers) != set(expected_answer_ids):
        raise ValueError(
            "Candidate answer IDs do not match the live response: "
            f"{sorted(answers)} != {sorted(expected_answer_ids)}"
        )
    return answers, (time.perf_counter() - started) * 1000


def offline_main(args: argparse.Namespace) -> int:
    response = json.loads(args.offline_response.read_text())
    apk_paths = args.offline_artifact
    expected_count = len(response.get("artifacts", []))
    if expected_count and len(apk_paths) != expected_count:
        raise ValueError(
            f"Response describes {expected_count} artifacts; received "
            f"{len(apk_paths)} --offline-artifact arguments"
        )
    if not expected_count and not apk_paths:
        raise ValueError("Supply at least one --offline-artifact")
    answers, solver_ms = solve_response(
        response, apk_paths, verify_dex_integrity=not args.fast
    )
    print(
        json.dumps(
            {
                "mode": response.get("mode"),
                "question_count": len(answers),
                "answers": answers,
                "solver_execution_ms": round(solver_ms, 3),
                "submitted": False,
                "offline": True,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "challenge", nargs="?", help="challenge ID from the Game Master"
    )
    parser.add_argument(
        "--offline-response",
        type=Path,
        help="response JSON saved from the Game Master; use with saved APKs",
    )
    parser.add_argument(
        "--offline-artifact",
        type=Path,
        action="append",
        default=[],
        help="APK path in the same order as response.artifacts; repeat for Mastery",
    )
    parser.add_argument(
        "--retry",
        action="store_true",
        help="advance to a new attempt; for timed modes, combine with --ranked",
    )
    parser.add_argument(
        "--ranked",
        action="store_true",
        help="explicitly authorize a possibly timed Time Trial or Mastery request",
    )
    parser.add_argument(
        "--regular-untimed",
        action="store_true",
        help="select the regular pool after confirming the route supports untimed play",
    )
    parser.add_argument(
        "--practice-untimed",
        action="store_true",
        help="continue an exhausted legacy mode through its untimed practice route",
    )
    parser.add_argument(
        "--run-for-time",
        action="store_true",
        help="request a timed attempt on routes that support the opt-in flag",
    )
    parser.add_argument(
        "--legacy-timed-default",
        action="store_true",
        help="explicitly select a legacy timed-by-default route (omit run_for_time)",
    )
    parser.add_argument(
        "--verify-sha256",
        action="store_true",
        help="verify downloaded APKs against API hashes (adds work on timed path)",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="skip APK SHA-256 and embedded DEX integrity verification",
    )
    parser.add_argument(
        "--proxy",
        default=os.environ.get("GAME_MASTER_PROXY_URL", DEFAULT_PROXY),
    )
    args = parser.parse_args()

    if args.fast and args.verify_sha256:
        parser.error("--fast cannot be combined with --verify-sha256")

    if args.offline_response:
        if (
            args.challenge
            or args.retry
            or args.ranked
            or args.regular_untimed
            or args.practice_untimed
            or args.run_for_time
            or args.legacy_timed_default
        ):
            parser.error(
                "offline mode takes its challenge and questions from "
                "--offline-response; it cannot start or submit attempts"
            )
        try:
            return offline_main(args)
        except Exception as exc:
            parser.error(str(exc))
    if not args.challenge:
        parser.error("challenge ID is required unless --offline-response is used")

    timed_mode = args.challenge.endswith(("/time_trial", "/mastery"))
    selected_routes = sum(
        (
            args.regular_untimed,
            args.practice_untimed,
            args.run_for_time,
            args.legacy_timed_default,
        )
    )
    if timed_mode and selected_routes != 1:
        parser.error(
            "select exactly one route: --regular-untimed, --run-for-time, or "
            "--legacy-timed-default, or --practice-untimed"
        )
    if args.practice_untimed and (
        args.retry
        or args.ranked
        or args.regular_untimed
        or args.run_for_time
        or args.legacy_timed_default
    ):
        parser.error(
            "--practice-untimed selects op=practice and cannot be combined "
            "with another attempt route"
        )
    if timed_mode and args.regular_untimed and args.ranked:
        parser.error("--regular-untimed cannot be combined with --ranked")
    if timed_mode and (args.run_for_time or args.legacy_timed_default) and not args.ranked:
        parser.error(
            "timed routes require --ranked after the required preflight"
        )
    if not timed_mode and (
        args.ranked
        or args.regular_untimed
        or args.practice_untimed
        or args.legacy_timed_default
        or args.run_for_time
    ):
        parser.error("timing-route options are only for Time Trial or Mastery")
    if args.retry and timed_mode and not args.ranked:
        if not args.regular_untimed:
            parser.error("a legacy timed-mode retry requires explicit --ranked")

    start_time = time.perf_counter()
    payload: dict = {"challenge": args.challenge}
    if args.practice_untimed:
        payload["op"] = "practice"
    elif args.retry:
        payload["op"] = "retry"
    else:
        payload["op"] = "start"
    if args.run_for_time:
        payload["run_for_time"] = True
    response = request_json(args.proxy, payload)
    start_elapsed_ms = (time.perf_counter() - start_time) * 1000
    attempt_id = response.get("attempt_id", "unknown-attempt")
    mode = response.get("mode") or args.challenge.rsplit("/", 1)[-1]
    if args.practice_untimed and attempt_id == "unknown-attempt":
        attempt_id = "practice"
    day_match = re.search(r"-day-(\d+)(?:-|/)", args.challenge)
    day_dir = f"day-{int(day_match.group(1)):02d}" if day_match else "other"
    record = ROOT / "work" / day_dir / "mobile-android" / attempt_id
    record.mkdir(parents=True, exist_ok=True)
    (record / "start-response.json").write_text(
        json.dumps(response, indent=2, ensure_ascii=False) + "\n"
    )
    print(
        json.dumps(
            {
                "attempt_id": attempt_id,
                "mode": mode,
                "deadline": response.get("deadline"),
                "hall_of_fame_eligible": response.get("hall_of_fame_eligible"),
                "answer_ids": answer_ids_for_response(response),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )

    specs = response.get("artifacts") or []
    if specs:
        delivery_indexes = list(range(len(specs)))
    else:
        deliveries = {}
        for question in response.get("questions", []):
            delivery_index = delivery_index_for_question(question)
            if delivery_index is None:
                continue
            deliveries.setdefault(delivery_index, question)
        if deliveries:
            delivery_indexes = sorted(deliveries)
            if delivery_indexes != list(range(len(delivery_indexes))):
                raise ValueError(
                    "Practice questions reference non-contiguous deliveries: "
                    f"{delivery_indexes}"
                )
            specs = []
            for index in delivery_indexes:
                reference = str(deliveries[index].get("artifact", ""))
                filename_match = re.search(
                    r"delivery\s+\d+\s*:\s*([^,;]+)", reference, re.I
                )
                filename = (
                    Path(filename_match.group(1).strip()).name
                    if filename_match
                    else f"delivery_{index + 1}.apk"
                )
                specs.append({"filename": filename})
        else:
            specs = [
                {
                    "filename": response.get("filename", "assigned.apk"),
                    "sha256": response.get("sha256"),
                    "download": response.get("download"),
                }
            ]
            delivery_indexes = [None]
    download_started = time.perf_counter()
    if len(specs) == 1:
        downloads = [
            fetch_artifact(
                args.proxy,
                args.challenge,
                delivery_indexes[0],
                specs[0].get("download"),
            )
        ]
    else:
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=min(8, len(specs))
        ) as executor:
            futures = [
                executor.submit(
                    fetch_artifact,
                    args.proxy,
                    args.challenge,
                    delivery_indexes[index],
                    spec.get("download"),
                )
                for index, spec in enumerate(specs)
            ]
            downloads = [future.result() for future in futures]
    download_elapsed_ms = (time.perf_counter() - download_started) * 1000

    apk_paths = []
    artifact_hashes = []
    for index, (spec, (data, filename)) in enumerate(zip(specs, downloads)):
        digest = hashlib.sha256(data).hexdigest() if args.verify_sha256 else None
        if (
            args.verify_sha256
            and spec.get("sha256")
            and digest != spec["sha256"]
        ):
            raise ValueError(f"SHA-256 mismatch for delivery {index + 1}")
        artifact_hashes.append(digest)
        apk_path = record / Path(spec.get("filename") or filename).name
        apk_path.write_bytes(data)
        apk_paths.append(apk_path)

    answers, solver_ms = solve_response(
        response, apk_paths, verify_dex_integrity=not args.fast
    )
    (record / "candidate-answers.json").write_text(
        json.dumps(answers, indent=2, ensure_ascii=False) + "\n"
    )

    accepted = set(response.get("accepted_ids", []))
    pending_answers = {
        answer_id: answer
        for answer_id, answer in answers.items()
        if answer_id not in accepted
    }
    submission = None
    submission_elapsed_ms = 0.0
    if pending_answers:
        submission_started = time.perf_counter()
        HTTP.close_current_thread_connections()
        submission = request_json(
            args.proxy,
            {"challenge": args.challenge, "answers": pending_answers},
        )
        submission_elapsed_ms = (time.perf_counter() - submission_started) * 1000
        (record / "submission-result.json").write_text(
            json.dumps(submission, indent=2, ensure_ascii=False) + "\n"
        )
    confirmed_by_submit = bool(
        submission
        and submission.get("result") == "CORRECT"
        and submission.get("status") != "pending"
    )
    status_elapsed_ms = 0.0
    if confirmed_by_submit:
        status = submission
    else:
        status_url = (
            args.proxy
            + "?op=status&challenge="
            + urllib.parse.quote(args.challenge, safe="")
        )
        status_started = time.perf_counter()
        status = request_json(status_url)
        status_elapsed_ms = (time.perf_counter() - status_started) * 1000
        (record / "status-response.json").write_text(
            json.dumps(status, indent=2, ensure_ascii=False) + "\n"
        )
    result = submission or status
    summary = {
        "challenge": args.challenge,
        "mode": mode,
        "practice": bool(args.practice_untimed),
        "attempt_id": attempt_id,
        "deadline": response.get("deadline"),
        "hall_of_fame_eligible": response.get("hall_of_fame_eligible"),
        "question_count": len(response.get("questions", [])),
        "submitted_answer_ids": sorted(pending_answers),
        "accepted_ids": (
            answer_ids_for_response(response)
            if confirmed_by_submit
            else status.get("accepted_ids", [])
        ),
        "status_checked": not confirmed_by_submit,
        "result": result.get("result"),
        "scoring_status": status.get("status"),
        "solver_execution_ms": round(solver_ms, 3),
        "artifact_download_ms": round(download_elapsed_ms, 3),
        "start_request_ms": round(start_elapsed_ms, 3),
        "submission_request_ms": round(submission_elapsed_ms, 3),
        "status_request_ms": round(status_elapsed_ms, 3),
        "client_end_to_end_ms": round((time.perf_counter() - start_time) * 1000, 3),
        "record": str(record),
    }
    if args.verify_sha256:
        summary["artifact_sha256"] = artifact_hashes
    (record / "run-summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if status.get("result") == "CORRECT" or result.get("result") == "CORRECT" else 3


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        raise SystemExit(f"Error: {exc}")
