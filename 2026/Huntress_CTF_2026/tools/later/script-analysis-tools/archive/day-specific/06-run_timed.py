"""Run a prepared Day 6 timed attempt; never prints or stores GM credentials."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


BASE = "https://2026.huntress.ctf.games/"
CHALLENGE = "script-analysis-day-06-bash-behavior-graphs"
ROOT = Path(__file__).resolve().parents[1]
SOLVE = Path(__file__).resolve().parent


def get_token() -> str:
    token = os.environ.get("HUNTRESS_GM_TOKEN")
    if not token:
        raise RuntimeError("Game Master token missing")
    return token


def post(op: str, challenge: str, token: str, answers: dict | None = None) -> tuple[dict, int]:
    body = {"op": op, "challenge": challenge}
    if answers is not None:
        body["answers"] = answers
    req = Request(BASE, data=json.dumps(body).encode(), headers={"Authorization": "Bearer " + token,
                                                             "Content-Type": "application/json"})
    try:
        with urlopen(req, timeout=30) as response:
            return json.load(response), response.status
    except HTTPError as exc:
        return json.load(exc), exc.code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["time_trial", "mastery"])
    parser.add_argument("--retry", action="store_true", help="Request a fresh timed variant")
    parser.add_argument("--diagnose", action="store_true", help="Submit three evidence-based answer groups")
    parser.add_argument("--diagnose-on-incorrect", action="store_true", help="Check answer families immediately after an incorrect full batch")
    parser.add_argument("--verify-forms", action="store_true", help="Verify one current answer for each high-risk syntax form after an incorrect batch")
    parser.add_argument("--probe-semantics", action="store_true", help="Check repeated submission result for one known scenario answer")
    parser.add_argument("--probe-risk", action="store_true", help="Validate unresolved syntax labels before the full batch")
    args = parser.parse_args()
    token = get_token()
    challenge = CHALLENGE + "/" + args.mode
    result, http = post("retry" if args.retry else "start", challenge, token)
    if http != 200:
        raise RuntimeError(f"Start failed, HTTP {http}, status {result.get('error') or result.get('result')}")
    required = ("attempt_id", "questions", "answer_ids")
    missing = [key for key in required if key not in result]
    if missing:
        raise RuntimeError(f"Start contract missing {missing}; response keys {list(result)}")
    if not (("download" in result and "sha256" in result) or isinstance(result.get("artifacts"), list)):
        raise RuntimeError(f"No supported artifact assignment; response keys {list(result)}")
    work = SOLVE / args.mode / result["attempt_id"]
    work.mkdir(parents=True, exist_ok=False)
    archive = ROOT / "artifacts" / (args.mode + "-" + result["attempt_id"] + ".zip")
    contract = {key: result[key] for key in ("name", "attempt_id", "mode", "deadline", "questions", "answer_ids") if key in result}
    if "download" in result and "sha256" in result:
        download = urljoin(BASE, result["download"])
        req = Request(download, headers={"Authorization": "Bearer " + token})
        with urlopen(req, timeout=30) as response:
            artifact = response.read()
        if hashlib.sha256(artifact).hexdigest() != result["sha256"]:
            raise RuntimeError("Assigned artifact hash mismatch")
        archive.write_bytes(artifact)
        contract["sha256"] = result["sha256"]
    else:
        items = []
        prefixes = list(dict.fromkeys(q["artifact"].split(" -> ", 1)[0] for q in result["questions"]))
        assigned = result["artifacts"]
        listed_downloads = result.get("downloads")
        if isinstance(listed_downloads, list) and len(listed_downloads) == len(assigned):
            by_url = {item["download"]: item for item in assigned}
            if all(url in by_url for url in listed_downloads):
                assigned = [by_url[url] for url in listed_downloads]
        if len(prefixes) != len(assigned):
            raise RuntimeError("Artifact count differs from question deliveries")
        aliases = {}
        for index, item in enumerate(assigned, 1):
            original_name = item["filename"]
            if Path(original_name).name != original_name or not original_name.endswith(".zip"):
                raise RuntimeError("Unsafe assigned filename")
            name = f"assigned-{index:02}.zip"
            aliases[prefixes[index - 1]] = name
            req = Request(urljoin(BASE, item["download"]), headers={"Authorization": "Bearer " + token})
            with urlopen(req, timeout=30) as response:
                data = response.read()
            if hashlib.sha256(data).hexdigest() != item["sha256"]:
                raise RuntimeError("Assigned nested artifact hash mismatch")
            (work / name).write_bytes(data)
            items.append((name, data))
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as bundle:
            for name, data in items:
                bundle.writestr(name, data)
        contract["sha256"] = hashlib.sha256(archive.read_bytes()).hexdigest()
        contract["archive_aliases"] = aliases
    (work / "contract.json").write_text(json.dumps(contract, indent=2) + "\n")
    output = work / "solver_output.json"
    command = [sys.executable, str(SOLVE / "timed_solver.py"),
               "--contract", str(work / "contract.json"), "--archive", str(archive),
               "--reference", str(SOLVE / "single_solve_answers.json"), "--output", str(output)]
    proc = subprocess.run(command, capture_output=True, text=True)
    print("solver:", proc.stdout.strip()[:500])
    if proc.returncode:
        print("solver exit:", proc.returncode, proc.stderr[-500:])
        return 2
    answers = json.loads(output.read_text())["answers"]
    if set(answers) != set(result["answer_ids"]):
        raise RuntimeError("Solver answers do not match current answer IDs")
    if args.probe_semantics:
        probe_id = "set1.resource-scenario" if args.mode == "mastery" else "resource-scenario"
        probe_results = []
        for _ in range(2):
            outcome, status = post("submit", challenge, token, {probe_id: answers[probe_id]})
            probe_results.append({"http": status, "result": outcome.get("result")})
            if status == 429 or outcome.get("result") == "expired":
                break
        print("repeat semantics:", json.dumps(probe_results))
    if args.probe_risk:
        checked = {}
        for value in ("percent", "if_block"):
            found = next(((k, v) for k, v in answers.items() if v == value and k.endswith(("-expansion", "-control"))), None)
            if not found:
                continue
            outcome, status = post("submit", challenge, token, {found[0]: found[1]})
            checked[found[0]] = {"value": value, "result": outcome.get("result"), "http": status}
            if status == 429 or outcome.get("result") in ("incorrect", "expired"):
                break
        print("risk checks:", json.dumps(checked))
        (work / "risk_checks.json").write_text(json.dumps(checked, indent=2) + "\n")
        if any(item["result"] != "accepted" for item in checked.values()):
            return 4
    graded, submit_http = (None, None)
    if not args.diagnose:
        graded, submit_http = post("submit", challenge, token, answers)
        print("full submission:", graded.get("result"))
    full_result = graded.get("result") if graded else None
    if args.diagnose or (args.diagnose_on_incorrect and graded.get("result") == "incorrect"):
        rules = {
            "js_function": lambda k: k.startswith("jscript-") and k.endswith("-function-style"),
            "js_invocation": lambda k: k.startswith("jscript-") and k.endswith("-invocation-style"),
            "js_property": lambda k: k.startswith("jscript-") and k.endswith("-property-style"),
            "batch_control": lambda k: k.startswith("batch-") and k.endswith("-control"),
            "vb_control": lambda k: k.startswith("vbscript-") and k.endswith("-control"),
        }
        groups = {}
        for prefix in (["set1.", "set2."] if args.mode == "mastery" else [""]):
            scoped = {k: v for k, v in answers.items() if k.startswith(prefix)}
            groups[prefix + "batch_expansion_for"] = {k: v for k, v in scoped.items() if k[len(prefix):].startswith("batch-") and k.endswith("-expansion") and v == "for_indirect"}
            groups[prefix + "batch_expansion_other"] = {k: v for k, v in scoped.items() if k[len(prefix):].startswith("batch-") and k.endswith("-expansion") and v != "for_indirect"}
            for name, predicate in rules.items():
                groups[prefix + name] = {k: v for k, v in scoped.items() if predicate(k[len(prefix):])}
            classified = {key for name, group in groups.items() if name.startswith(prefix) for key in group}
            groups[prefix + "other_answers"] = {k: v for k, v in scoped.items() if k not in classified}
        outcomes = {}
        for label, group in groups.items():
            if not group:
                continue
            graded, submit_http = post("submit", challenge, token, group)
            outcomes[label] = {"count": len(group), "http": submit_http, "result": graded.get("result")}
            if submit_http == 429 or graded.get("result") in ("CORRECT", "already_solved", "expired"):
                break
        graded = {"result": list(outcomes.values())[-1]["result"]}
        submit_http = list(outcomes.values())[-1]["http"]
        print("groups:", json.dumps(outcomes))
    if args.verify_forms and full_result == "incorrect":
        checks = {}
        for prefix in (["set1.", "set2."] if args.mode == "mastery" else [""]):
            for indicator in ("batch-benign-campaign", "resource-url"):
                key = prefix + indicator
                if key in answers:
                    checks[key] = answers[key]
            for value in ("for_indirect", "delayed", "percent", "call_double"):
                found = next(((k, v) for k, v in answers.items() if k.startswith(prefix + "batch-") and k.endswith("-expansion") and v == value), None)
                if found:
                    checks[found[0]] = found[1]
            chain_key = prefix + "batch-chain-expansion"
            if chain_key in answers:
                checks[chain_key] = answers[chain_key]
            for value in ("if_block", "select_case"):
                found = next(((k, v) for k, v in answers.items() if k.startswith(prefix + "vbscript-") and k.endswith("-control") and v == value), None)
                if found:
                    checks[found[0]] = found[1]
        verified = {}
        for answer_id, value in checks.items():
            outcome, status = post("submit", challenge, token, {answer_id: value})
            verified[answer_id] = {"value": value, "result": outcome.get("result"), "http": status}
            if status == 429 or outcome.get("result") in ("CORRECT", "already_solved", "expired"):
                break
        (work / "form_verification.json").write_text(json.dumps(verified, indent=2) + "\n")
        print("form verification:", json.dumps(verified))
    summary = {"attempt_id": result["attempt_id"], "mode": args.mode, "deadline": result.get("deadline"),
               "answer_count": len(answers), "http_status": submit_http, "result": graded.get("result")}
    (work / "submission_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print("submission:", json.dumps(summary))
    return 0 if graded.get("result") in ("CORRECT", "already_solved") else 3


if __name__ == "__main__":
    raise SystemExit(main())
