#!/usr/bin/env python3
"""Solve both current Go Fish Mastery deliveries under their shared timer."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.parse import urljoin

import requests

from solve_time_trial import BASE, ROOT, solve


CID = "binary-reverse-engineering-day-04-go-runtime-fingerprints/mastery"


def main():
    token = os.environ.get("HUNTRESS_GM_TOKEN")
    if not token:
        raise SystemExit("HUNTRESS_GM_TOKEN is missing")
    session = requests.Session()
    session.headers.update({"Authorization": "Bearer " + token})
    retry = "--retry" in sys.argv[1:]
    start_response = session.post(BASE, json={"challenge": CID, **({"op": "retry"} if retry else {})}, timeout=10)
    start_response.raise_for_status()
    assignment = start_response.json()
    deliveries = assignment.get("artifacts") or assignment.get("downloads")
    if not deliveries and assignment.get("download"):
        deliveries = [{"download": assignment["download"], "sha256": assignment.get("sha256")}]
    if not deliveries:
        print(json.dumps({"stage": "start", "response": assignment}))
        return
    attempt_id = assignment["attempt_id"]
    record = {"attempt_id": attempt_id, "deadline": assignment.get("deadline"),
              "answer_ids": assignment["answer_ids"], "deliveries": []}
    record_path = Path(tempfile.gettempdir()) / f"gofish-mastery-{attempt_id}.json"
    record_path.write_text(json.dumps(record, indent=2) + "\n")
    answers = {}
    archives = []
    try:
        for index, item in enumerate(deliveries, 1):
            link = item if isinstance(item, str) else item["download"]
            response = session.get(urljoin(BASE, link), timeout=10)
            response.raise_for_status()
            archive = response.content
            archives.append(archive)
            record["deliveries"].append({"set": index, "download": link,
                                         "sha256": item.get("sha256") if isinstance(item, dict) else None})
            with tempfile.TemporaryDirectory(prefix=f"gofish-mastery-{index}-") as work:
                zip_path = Path(work) / "evidence.zip"
                zip_path.write_bytes(archive)
                extracted = Path(work) / "extracted"
                extracted.mkdir()
                subprocess.run(["7z", "x", "-y", "-pinfected", "-o" + str(extracted), str(zip_path)],
                               check=True, stdout=subprocess.DEVNULL)
                files = {path.name: path.read_bytes() for path in extracted.rglob("*") if path.is_file()}
                answers.update({f"set{index}.{key}": value for key, value in solve(files).items()})
        expected = set(assignment["answer_ids"])
        if set(answers) != expected:
            record.update({"stage": "answer_fields", "missing": sorted(expected - set(answers)),
                           "unexpected": sorted(set(answers) - expected)})
            print(json.dumps(record))
            return
        result_response = session.post(BASE, json={"challenge": CID, "answers": answers}, timeout=10)
        result_response.raise_for_status()
        result = result_response.json()
        record.update({"result": result.get("result"), "remaining": result.get("remaining"),
                       "status": result.get("status"), "flag": result.get("flag"),
                       "accepted_ids": result.get("accepted_ids"), "answers": answers})
        print(json.dumps({k: v for k, v in record.items() if k not in ("answers", "answer_ids", "accepted_ids")}))
    finally:
        if record.get("result") != "CORRECT":
            output = ROOT / "artifacts" / "mastery" / ("attempt-" + attempt_id)
            output.mkdir(parents=True, exist_ok=True)
            for index, archive in enumerate(archives, 1):
                (output / f"set{index}-evidence.zip").write_bytes(archive)
        record_path.write_text(json.dumps(record, indent=2) + "\n")


if __name__ == "__main__":
    main()
