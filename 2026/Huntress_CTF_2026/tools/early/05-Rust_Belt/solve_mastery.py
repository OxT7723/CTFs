#!/usr/bin/env python3
"""Solve both assigned Rust Belt Mastery deliveries before the shared deadline."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.parse import urljoin

import requests

from solve_time_trial import BASE, ROOT, solve


CID = "binary-reverse-engineering-day-05-rust-runtime-shapes/mastery"


def main():
    token = os.environ.get("HUNTRESS_GM_TOKEN")
    if not token:
        raise SystemExit("HUNTRESS_GM_TOKEN is missing")
    session = requests.Session()
    session.headers.update({"Authorization": "Bearer " + token})
    request = {"challenge": CID}
    if "--retry" in sys.argv:
        request["op"] = "retry"
    start = session.post(BASE, json=request, timeout=10)
    start.raise_for_status()
    assignment = start.json()
    deliveries = assignment.get("artifacts")
    if not deliveries and assignment.get("downloads"):
        deliveries = assignment["downloads"]
    if not deliveries and assignment.get("download"):
        deliveries = [{"download": assignment["download"], "sha256": assignment.get("sha256")}]
    if not deliveries:
        print(json.dumps({"stage": "start", "keys": list(assignment), "result": assignment.get("result"), "deadline": assignment.get("deadline")}))
        return

    attempt_id = assignment["attempt_id"]
    output = ROOT / "artifacts" / "mastery" / ("attempt-" + attempt_id)
    output.mkdir(parents=True, exist_ok=True)
    answers = {}
    evidence = []
    for index, item in enumerate(deliveries, 1):
        download_path = item if isinstance(item, str) else item["download"]
        response = session.get(urljoin(BASE, download_path), timeout=10)
        response.raise_for_status()
        archive = response.content
        digest = hashlib.sha256(archive).hexdigest()
        expected_hash = item.get("sha256") if isinstance(item, dict) else None
        if expected_hash and digest != expected_hash:
            raise ValueError(f"Delivery {index} SHA-256 mismatch")
        destination = output / f"set{index}-evidence.zip"
        destination.write_bytes(archive)
        with tempfile.TemporaryDirectory(prefix=f"rust-belt-mastery-{index}-") as work:
            zip_path = Path(work) / "evidence.zip"
            zip_path.write_bytes(archive)
            extracted = Path(work) / "extracted"
            extracted.mkdir()
            subprocess.run(["7z", "x", "-y", "-pinfected", "-o" + str(extracted), str(zip_path)], check=True, stdout=subprocess.DEVNULL)
            files = {path.name: path.read_bytes() for path in extracted.rglob("*") if path.is_file()}
            answers.update({f"set{index}.{key}": value for key, value in solve(files).items()})
        evidence.append({"set": index, "download": download_path, "sha256": digest, "path": str(destination)})

    expected_ids = set(assignment["answer_ids"])
    if set(answers) != expected_ids:
        print(json.dumps({"stage": "answer_fields", "missing": sorted(expected_ids - set(answers)), "unexpected": sorted(set(answers) - expected_ids), "attempt_id": attempt_id, "deadline": assignment.get("deadline"), "evidence": evidence}))
        return
    response = session.post(BASE, json={"challenge": CID, "answers": answers}, timeout=10)
    response.raise_for_status()
    result = response.json()
    print(json.dumps({"attempt_id": attempt_id, "deadline": assignment.get("deadline"), "result": result.get("result"), "remaining": result.get("remaining"), "status": result.get("status"), "flag": result.get("flag"), "answer_count": len(answers), "evidence": evidence}))


if __name__ == "__main__":
    main()
