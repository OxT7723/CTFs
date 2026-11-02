#!/usr/bin/env python3
"""Sequentially consume remaining fresh A Little Based timed variants."""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROXY = "http://192.0.2.1/huntress-ctf-proxy"
MODES = (
    ("time_trial", "warmups-day-01/time_trial"),
    ("mastery", "warmups-day-01/mastery"),
)


def request_json(url: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data is not None else {},
        method="POST" if data is not None else "GET",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read())


def get_status(challenge: str) -> dict:
    return request_json(
        PROXY + "?op=status&challenge=" + urllib.parse.quote(challenge, safe="")
    )


def parse_time(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_solver():
    path = ROOT / "warmup-tools" / "run_modes.py"
    spec = importlib.util.spec_from_file_location("run_modes", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load the existing solver")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def offline_answers(solver, record: Path) -> tuple[dict, float]:
    response = json.loads((record / "start-response.json").read_text())
    specs = response.get("artifacts") or [{}]
    blobs = []
    for index, _ in enumerate(specs, 1):
        artifact_dir = record / f"delivery-{index:02d}" if len(specs) > 1 else record
        candidates = sorted(
            path for path in artifact_dir.iterdir()
            if path.is_file() and path.name not in {
                "candidate-answers.json", "start-response.json",
                "status-response.json", "submission-result.json",
                "run-summary.json",
            }
        )
        if len(candidates) != 1:
            raise RuntimeError(f"Expected one raw artifact in {artifact_dir}")
        blobs.append(candidates[0].read_bytes())
    started = time.perf_counter()
    answers, rails = solver.build_answers(response, blobs)
    elapsed_ms = (time.perf_counter() - started) * 1000
    return {"answers": answers, "rails": rails, "elapsed_ms": elapsed_ms}, elapsed_ms


def append_record(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n")
        stream.flush()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python", type=Path, required=True, help="Python with solver dependencies")
    parser.add_argument("--log", type=Path, required=True, help="Append-only JSONL run log")
    parser.add_argument(
        "--max-runs",
        type=int,
        required=True,
        help="Hard cap for this batch; retries stop when the cap or fresh variants run out",
    )
    args = parser.parse_args()
    if args.max_runs < 1:
        parser.error("--max-runs must be positive")
    solver = load_solver()

    statuses = {mode: get_status(challenge) for mode, challenge in MODES}
    remaining = {}
    for mode, challenge in MODES:
        status = statuses[mode]
        count = status.get("unique_attempts_remaining")
        if not isinstance(count, int):
            raise RuntimeError(f"{mode}: status has no unique_attempts_remaining")
        deadline = parse_time(status.get("deadline"))
        if (
            status.get("result") != "CORRECT"
            and deadline is not None
            and deadline > dt.datetime.now(dt.timezone.utc)
        ):
            raise RuntimeError(f"{mode}: an active timed attempt already exists")
        remaining[mode] = count
    print(json.dumps({"preflight_remaining": remaining}), flush=True)

    total = 0
    while any(remaining.values()) and total < args.max_runs:
        for mode, challenge in MODES:
            if remaining[mode] == 0:
                continue
            before_status = get_status(challenge)
            if before_status.get("unique_attempts_remaining") != remaining[mode]:
                raise RuntimeError(
                    f"{mode}: remaining count changed externally; stopping safely"
                )
            deadline = parse_time(before_status.get("deadline"))
            if (
                before_status.get("result") != "CORRECT"
                and deadline is not None
                and deadline > dt.datetime.now(dt.timezone.utc)
            ):
                raise RuntimeError(f"{mode}: active timer detected; stopping safely")

            started = time.perf_counter()
            proc = subprocess.run(
                [
                    str(args.python),
                    str(ROOT / "warmup-tools" / "run_modes.py"),
                    "--retry",
                    challenge,
                ],
                capture_output=True,
                text=True,
                timeout=150,
            )
            client_seconds = time.perf_counter() - started
            if proc.returncode != 0:
                append_record(args.log, {
                    "mode": mode,
                    "stopped": True,
                    "reason": "runner_nonzero_exit",
                    "returncode": proc.returncode,
                    "stdout_tail": proc.stdout[-2000:],
                    "stderr_tail": proc.stderr[-2000:],
                    "client_seconds": client_seconds,
                    "before_remaining": remaining[mode],
                    "recorded_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                })
                print(json.dumps({
                    "stopped": True, "mode": mode,
                    "reason": "runner_nonzero_exit",
                    "returncode": proc.returncode,
                    "stdout_tail": proc.stdout[-1000:],
                    "stderr_tail": proc.stderr[-1000:],
                }), flush=True)
                return 2

            summary = json.loads(proc.stdout)
            record = Path(summary["record"])
            start = json.loads((record / "start-response.json").read_text())
            final = json.loads((record / "status-response.json").read_text())
            candidates = json.loads((record / "candidate-answers.json").read_text())
            offline, _ = offline_answers(solver, record)
            after = final.get("unique_attempts_remaining")
            valid = (
                summary.get("result") == "CORRECT"
                and set(final.get("accepted_ids", [])) == set(start.get("answer_ids", []))
                and candidates == offline["answers"]
                and after == remaining[mode] - 1
                and start.get("hall_of_fame_eligible") is True
            )
            result = {
                "sequence": total + 1,
                "mode": mode,
                "challenge": challenge,
                "attempt_id": summary.get("attempt_id"),
                "started_at": start.get("started_at"),
                "deadline": start.get("deadline"),
                "hall_of_fame_eligible": start.get("hall_of_fame_eligible"),
                "result": summary.get("result"),
                "answer_ids": start.get("answer_ids"),
                "accepted_ids": final.get("accepted_ids"),
                "remaining_before": remaining[mode],
                "remaining_after": after,
                "artifact_sha256": summary.get("artifact_sha256"),
                "artifact_downloads": start.get("downloads"),
                "solver_ms": offline["elapsed_ms"],
                "inferred_rail_fence_rails": offline["rails"],
                "client_seconds": client_seconds,
                "offline_answers_match": candidates == offline["answers"],
                "new_solver_change_needed": not valid,
                "record": str(record),
                "verified": valid,
                "recorded_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
            }
            append_record(args.log, result)
            if not valid:
                print(json.dumps({
                    "stopped": True,
                    "mode": mode,
                    "attempt_id": result["attempt_id"],
                    "result": result["result"],
                    "remaining_before": result["remaining_before"],
                    "remaining_after": result["remaining_after"],
                    "solver_ms": result["solver_ms"],
                    "record": result["record"],
                    "reason": "post-run validation failed; inspect record before continuing",
                }), flush=True)
                return 3

            remaining[mode] = after
            total += 1
            print(json.dumps({
                "sequence": total,
                "mode": mode,
                "attempt_id": result["attempt_id"],
                "result": result["result"],
                "remaining": after,
                "solver_ms": round(result["solver_ms"], 3),
                "client_seconds": round(client_seconds, 3),
                "verified": True,
                "new_solver_change_needed": False,
            }), flush=True)
    print(json.dumps({
        "complete": not any(remaining.values()),
        "batch_limit_reached": total >= args.max_runs and any(remaining.values()),
        "runs": total,
        "remaining": remaining,
    }), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
