"""Solve the current two-archive Mastery assignment with bounded answer checks."""
import concurrent.futures
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import time
from urllib.parse import urljoin

import requests

BASE = "https://2026.huntress.ctf.games/"
CID = "script-analysis-day-04-shell-contrast/mastery"
HERE = pathlib.Path(__file__).resolve().parent
CHALLENGE = HERE.parent
STATE_PATH = CHALLENGE / "challenge_state.json"
TOKEN = os.environ.get("HUNTRESS_GM_TOKEN")
if not TOKEN:
    raise SystemExit("HUNTRESS_GM_TOKEN missing")
HEADERS = {"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"}


def post(body):
    response = requests.post(BASE, headers=HEADERS, json=body, timeout=5)
    if response.status_code == 429:
        raise RuntimeError("Game Master rate limit (429)")
    response.raise_for_status()
    return response.json()


def download(item):
    url = urljoin(BASE, item["download"])
    response = requests.get(url, headers=HEADERS, timeout=5)
    response.raise_for_status()
    return item, response.content


def solve_one(item_and_bytes):
    item, archive = item_and_bytes
    filename = item["filename"]
    with tempfile.TemporaryDirectory(prefix="dimmer-mastery-") as td:
        root = pathlib.Path(td)
        zip_path = root / filename
        extracted = root / "extracted"
        extracted.mkdir()
        zip_path.write_bytes(archive)
        process = subprocess.run(
            ["7z", "x", "-y", "-pinfected", "-o" + str(extracted), str(zip_path)],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE, timeout=5,
        )
        if process.returncode not in (0, 1):
            raise RuntimeError("Archive extraction failed with password infected")
        answers_path = root / "answers.json"
        env = dict(os.environ, DIMMER_ARTIFACT_DIR=str(extracted),
                   DIMMER_CANDIDATES_PATH=str(answers_path))
        process = subprocess.run(
            [sys.executable, str(HERE / "build_dimmer_answers.py")],
            env=env, stdin=subprocess.DEVNULL, capture_output=True,
            text=True, timeout=5,
        )
        if process.returncode:
            raise RuntimeError("Solver failed: " + process.stderr[:250])
        return item, json.loads(answers_path.read_text())


state = json.loads(STATE_PATH.read_text())
expected_ids = set(state["modes"]["mastery"]["answer_ids"])
retry_requested = "--retry" in sys.argv[1:]
started = post({"challenge": CID, **({"op": "retry"} if retry_requested else {})})
if started.get("result") == "CORRECT" and not retry_requested:
    raise SystemExit("Mastery is solved; pass --retry to request a new timed attempt")
if not started.get("deadline"):
    started = post({"op": "retry", "challenge": CID})
if not started.get("deadline"):
    raise SystemExit("START_FAILED " + str(started.get("result", started.get("error"))))
began = time.monotonic()
answer_ids = set(started.get("answer_ids", []))
if answer_ids != expected_ids:
    raise SystemExit("Current answer IDs differ from the prepared Mastery contract")
artifact_items = started.get("artifacts", [])
if not artifact_items and started.get("downloads"):
    artifact_items = [
        {"download": path, "filename": "evidence.zip"}
        for path in started["downloads"]
    ]
if len(artifact_items) != 2 or any("download" not in item for item in artifact_items):
    raise SystemExit("Unexpected Mastery artifact assignment")

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    archive_pairs = list(pool.map(download, artifact_items))
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    solved_pairs = list(pool.map(solve_one, archive_pairs))
candidates = {}
for index, (_, answers) in enumerate(solved_pairs, 1):
    candidates.update({f"set{index}.{key}": value for key, value in answers.items()})
if set(candidates) != answer_ids:
    raise SystemExit("Solver did not cover all current Mastery answer IDs")

accepted = {}
rejected = {}
events = []
stopped = False


def record(answer_id, value, result):
    global stopped
    status = result.get("result")
    events.append((answer_id, value, status, result.get("remaining")))
    if status in ("accepted", "CORRECT"):
        accepted[answer_id] = value
    elif status == "incorrect":
        rejected.setdefault(answer_id, []).append(value)
    elif status in ("expired", "rate_limited"):
        stopped = True
    if status == "CORRECT":
        stopped = True


def submit_one(item):
    answer_id, value = item
    return answer_id, value, post({"challenge": CID, "answers": {answer_id: value}})


def submit_round(items):
    global stopped
    if stopped or not items:
        return
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
        futures = [pool.submit(submit_one, item) for item in items]
        for future in concurrent.futures.as_completed(futures):
            try:
                answer_id, value, result = future.result()
                record(answer_id, value, result)
            except RuntimeError as error:
                if "429" in str(error):
                    stopped = True
                events.append(("request", "", type(error).__name__, None))
            except requests.RequestException as error:
                events.append(("request", "", type(error).__name__, None))


uncertain = {key for key in answer_ids if key.endswith(("-control", "-expansion"))}
full_result = post({"challenge": CID, "answers": candidates})
record("full_462", "", full_result)
if full_result.get("result") == "CORRECT":
    accepted.pop("full_462", None)
    accepted.update(candidates)
if not stopped:
    base_answers = {key: candidates[key] for key in sorted(answer_ids - uncertain)}
    base_result = post({"challenge": CID, "answers": base_answers})
    record("base_408", "", base_result)
    if base_result.get("result") in ("accepted", "CORRECT"):
        accepted.pop("base_408", None)
        accepted.update(base_answers)
if not stopped:
    groups = [
        ("vbscript_controls", sorted(key for key in uncertain if ".vbscript-" in key)),
    ]
    for set_number in (1, 2):
        groups.extend([
            (f"set{set_number}_batch_controls", sorted(
                key for key in uncertain
                if key.startswith(f"set{set_number}.batch-") and key.endswith("-control")
            )),
            (f"set{set_number}_batch_expansions", sorted(
                key for key in uncertain
                if key.startswith(f"set{set_number}.batch-") and key.endswith("-expansion")
            )),
        ])
    singles = []
    for label, keys in groups:
        if stopped:
            break
        result = post({"challenge": CID, "answers": {key: candidates[key] for key in keys}})
        record(label, "", result)
        if result.get("result") in ("accepted", "CORRECT"):
            accepted.pop(label, None)
            accepted.update({key: candidates[key] for key in keys})
        elif result.get("result") == "incorrect":
            singles.extend(keys)
    submit_round([(key, candidates[key]) for key in singles if key not in accepted])

alternatives = {
    "for_loop": ["for_once", "call_subroutine"],
    "if_guard": ["direct", "if_defined"],
    "if_defined": ["if_guard", "direct"],
    "if_true_guard": ["direct", "error_guard"],
    "if_then_else": ["direct", "if_guard"],
    "if_then": ["direct", "if_guard"],
    "error_resume_next": ["error_guard", "direct"],
    "percent": ["delayed", "call_double"],
    "call_double": ["delayed", "for_indirect"],
    "delayed": ["call_double", "for_indirect"],
    "for_indirect": ["call_double", "delayed"],
}
for round_number in range(2):
    pending = []
    for key in sorted(uncertain - accepted.keys()):
        choices = alternatives.get(candidates[key], [])
        if round_number < len(choices) and choices[round_number] not in rejected.get(key, []):
            pending.append((key, choices[round_number]))
    submit_round(pending)
    if stopped:
        break

remaining = next((row[3] for row in reversed(events) if row[3] is not None), None)
success = any(row[2] == "CORRECT" for row in events) or remaining == 0
if success:
    remaining = 0
confirmed_count = len(answer_ids) if success else len(accepted)
attempt_id = str(started.get("attempt_id") or "unidentified")
stored = []
if not success:
    root = CHALLENGE / "artifacts" / "mastery" / ("attempt-" + attempt_id)
    root.mkdir(parents=True, exist_ok=True)
    for index, (item, archive) in enumerate(archive_pairs, 1):
        path = root / f"evidence-{index:02d}.zip"
        path.write_bytes(archive)
        stored.append(str(path.relative_to(CHALLENGE.parent)))
mode = state["modes"]["mastery"]
record_for_state = {
    "attempt_id": attempt_id, "mode": "mastery",
    "deadline": started.get("deadline"),
    "result": "CORRECT" if success else "expired",
    "confirmed_answers": confirmed_count, "remaining": remaining,
    "artifacts": [
        {"set": index + 1, "filename": item["filename"], "sha256": item.get("sha256"),
         "path": None if success else stored[index]}
        for index, item in enumerate(artifact_items)
    ],
    "submission_summary": {
        "accepted_responses": sum(row[2] == "accepted" for row in events),
        "incorrect_responses": sum(row[2] == "incorrect" for row in events),
        "correct_responses": sum(row[2] == "CORRECT" for row in events),
    },
}
if not success:
    record_for_state["accepted_syntax_values"] = {
        key: value for key, value in accepted.items()
        if key.endswith(("-control", "-expansion"))
    }
    record_for_state["rejected_syntax_candidates"] = rejected
    record_for_state["submission_groups"] = [
        {"group": key, "candidate": value, "result": result, "remaining": left}
        for key, value, result, left in events
    ]
mode.setdefault("attempts", []).append(record_for_state)
mode["status"] = {
    **mode.get("status", {}), "http_status": 200,
    "result": "CORRECT" if success else "expired",
    "attempt_id": attempt_id,
}
mode["status"].pop("status", None)
mode["status"].pop("error", None)
mode["progress_summary"] = (
    f"Latest Mastery attempt confirmed {confirmed_count} of {len(answer_ids)} fields; "
    f"{remaining if remaining is not None else 'unknown'} remain."
)
STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "attempt_id": attempt_id, "elapsed_seconds": round(time.monotonic() - began, 3),
    "accepted": confirmed_count, "remaining": remaining, "success": success,
    "artifacts": [{"set": index + 1, "filename": item["filename"], "sha256": item.get("sha256")} for index, item in enumerate(artifact_items)],
    "events": events,
}))
