"""Run one bounded Time Trial attempt from the current assigned archive."""
import concurrent.futures
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import time

import requests

BASE = "https://2026.huntress.ctf.games/"
CID = "script-analysis-day-04-shell-contrast/time_trial"
HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent
TOKEN = os.environ.get("HUNTRESS_GM_TOKEN")
if not TOKEN:
    raise SystemExit("HUNTRESS_GM_TOKEN missing")
HEADERS = {"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"}


def post(body):
    response = requests.post(BASE, headers=HEADERS, json=body, timeout=3)
    if response.status_code == 429:
        raise RuntimeError("Game Master rate limit (429)")
    response.raise_for_status()
    return response.json()


retry_requested = "--retry" in sys.argv[1:]
started = post({"challenge": CID, **({"op": "retry"} if retry_requested else {})})
if started.get("result") == "CORRECT" and not retry_requested:
    raise SystemExit("Time Trial is solved; pass --retry to request a new timed attempt")
if not started.get("deadline"):
    started = post({"op": "retry", "challenge": CID})
if not started.get("deadline"):
    raise SystemExit("START_FAILED " + str(started.get("result", started.get("error"))))

began = time.monotonic()
assigned_ids = set(started.get("answer_ids", []))
state_path = CHALLENGE / "challenge_state.json"
state = json.loads(state_path.read_text())
reference_ids = set(state["modes"]["time_trial"]["answer_ids"])
if assigned_ids and assigned_ids != reference_ids:
    raise SystemExit("Current answer IDs changed; update the solver before submitting")
assigned_ids = assigned_ids or reference_ids

response = requests.get(
    BASE, params={"op": "artifact", "challenge": CID},
    headers=HEADERS, timeout=4
)
response.raise_for_status()
archive = response.content
sha = hashlib.sha256(archive).hexdigest()
attempt_id = str(started.get("attempt_id") or "unidentified")

with tempfile.TemporaryDirectory(prefix="dimmer-current-") as tmp:
    tmp = pathlib.Path(tmp)
    zip_path = tmp / "evidence.zip"
    extracted = tmp / "extracted"
    extracted.mkdir()
    zip_path.write_bytes(archive)
    process = subprocess.run(
        ["7z", "x", "-y", "-pinfected", "-o" + str(extracted), str(zip_path)],
        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE, timeout=4
    )
    if process.returncode not in (0, 1):
        raise SystemExit("Archive extraction failed; password infected did not work")
    answers_path = tmp / "answers.json"
    env = dict(os.environ, DIMMER_ARTIFACT_DIR=str(extracted),
               DIMMER_CANDIDATES_PATH=str(answers_path))
    process = subprocess.run(
        [sys.executable, str(HERE / "build_dimmer_answers.py")],
        env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=4
    )
    if process.returncode:
        raise SystemExit("Solver failed: " + process.stderr[:300])
    candidates = json.loads(answers_path.read_text())

if set(candidates) != assigned_ids:
    raise SystemExit("Solver did not cover the current answer IDs")

accepted = {}
rejected = {}
events = []
stopped = False


def record(answer_id, candidate, result):
    global stopped
    status = result.get("result")
    events.append((answer_id, candidate, status, result.get("remaining")))
    if status in ("accepted", "CORRECT"):
        accepted[answer_id] = candidate
    elif status == "incorrect":
        rejected.setdefault(answer_id, []).append(candidate)
    elif status in ("expired", "rate_limited"):
        stopped = True
    if status == "CORRECT":
        stopped = True


def submit_one(item):
    answer_id, candidate = item
    return answer_id, candidate, post({"challenge": CID, "answers": {answer_id: candidate}})


def submit_round(items):
    global stopped
    if stopped or not items:
        return
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        futures = [pool.submit(submit_one, item) for item in items]
        for future in concurrent.futures.as_completed(futures):
            try:
                answer_id, candidate, result = future.result()
                record(answer_id, candidate, result)
            except RuntimeError as error:
                if "429" in str(error):
                    stopped = True
                events.append(("request", "", type(error).__name__, None))
            except requests.RequestException as error:
                events.append(("request", "", type(error).__name__, None))


uncertain = {k for k in assigned_ids if k.endswith(("-control", "-expansion"))}
first = {k: candidates[k] for k in sorted(assigned_ids - uncertain)}
record("base_204", "", post({"challenge": CID, "answers": first}))
if events[-1][2] in ("accepted", "CORRECT"):
    accepted.pop("base_204", None)
    accepted.update(first)
submit_round([(k, candidates[k]) for k in sorted(uncertain)])

# Fallbacks are bounded. A new specimen may have a different syntax form.
alternatives = {
    "for_loop": ["for_once", "call_subroutine"],
    "if_defined": ["direct", "if_guard"],
    "if_true_guard": ["error_guard", "direct"],
    "if_then_else": ["direct", "if_guard"],
    "percent": ["delayed", "call_double"],
    "call_double": ["delayed", "for_indirect"],
    "delayed": ["call_double", "for_indirect"],
    "for_indirect": ["call_double", "delayed"],
}
for round_number in range(2):
    pending = []
    for answer_id in sorted(uncertain - accepted.keys()):
        choices = alternatives.get(candidates[answer_id], [])
        if round_number < len(choices):
            value = choices[round_number]
            if value not in rejected.get(answer_id, []):
                pending.append((answer_id, value))
    submit_round(pending)
    if stopped:
        break

remaining = next((event[3] for event in reversed(events) if event[3] is not None), None)
success = any(event[2] == "CORRECT" for event in events) or remaining == 0
if success:
    remaining = 0
artifact_path = None
if not success:
    artifact_dir = CHALLENGE / "artifacts" / "time_trial" / ("attempt-" + attempt_id)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    artifact_file = artifact_dir / "evidence.zip"
    artifact_file.write_bytes(archive)
    artifact_path = str(artifact_file.relative_to(CHALLENGE.parent))

state = json.loads(state_path.read_text())
mode = state["modes"]["time_trial"]
attempt_record = {
    "attempt_id": attempt_id, "mode": "time_trial",
    "deadline": started.get("deadline"), "artifact_sha256": sha,
    "artifact_path": artifact_path, "result": "CORRECT" if success else "expired",
    "confirmed_answers": len(accepted), "remaining": remaining,
    "submission_summary": {
        "accepted_responses": sum(event[2] == "accepted" for event in events),
        "incorrect_responses": sum(event[2] == "incorrect" for event in events),
        "correct_responses": sum(event[2] == "CORRECT" for event in events),
    },
}
if not success:
    attempt_record["accepted_syntax_values"] = {
        key: value for key, value in accepted.items()
        if key.endswith(("-control", "-expansion"))
    }
    attempt_record["rejected_syntax_candidates"] = rejected
    attempt_record["submission_groups"] = [
        {"group": answer_id, "candidate": candidate, "result": result, "remaining": left}
        for answer_id, candidate, result, left in events
    ]
mode.setdefault("attempts", []).append(attempt_record)
mode["status"] = {
    **mode.get("status", {}),
    "result": "CORRECT" if success else "expired",
    "attempt_id": attempt_id,
}
mode["progress_summary"] = (
    f"Latest Time Trial attempt confirmed {len(accepted)} of {len(assigned_ids)} fields; "
    f"{remaining if remaining is not None else 'unknown'} remain."
)
state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "attempt_id": attempt_id, "sha256": sha, "elapsed_seconds": round(time.monotonic() - began, 3),
    "accepted": len(accepted), "remaining": remaining, "success": success,
    "events": events,
}))
