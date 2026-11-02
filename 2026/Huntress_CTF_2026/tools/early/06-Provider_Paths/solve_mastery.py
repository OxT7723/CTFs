#!/usr/bin/env python3
"""Solve the current Provider Paths Mastery assignment from its APK bytes."""

import io
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import urljoin
import zipfile

import requests


BASE = "https://2026.huntress.ctf.games/"
CHALLENGE = "mobile-android-day-06-provider-paths/mastery"


def decode(apk: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(apk)) as archive:
        puzzle = json.loads(archive.read("assets/huntress_puzzle.json"))
    if puzzle.get("codec") != "hex":
        raise ValueError("unsupported puzzle codec")
    answer = bytes.fromhex(puzzle["data"]).decode("ascii")
    if not re.fullmatch(r"ANS-[0-9A-F]{16}", answer):
        raise ValueError("decoded answer has unexpected format")
    return answer


def main() -> None:
    token = os.environ["HUNTRESS_GM_TOKEN"]
    session = requests.Session()
    session.headers.update({"Authorization": "Bearer " + token})
    retry = "--retry" in sys.argv[1:]
    response = session.post(BASE, json={"challenge": CHALLENGE, **({"op": "retry"} if retry else {})}, timeout=10)
    response.raise_for_status()
    assignment = response.json()
    print(json.dumps({k: assignment.get(k) for k in ("attempt_id", "deadline", "answer_ids")}), flush=True)
    deliveries = assignment.get("artifacts") or assignment.get("downloads")
    if not deliveries:
        raise ValueError("Mastery assignment has no deliveries")
    answer_ids = assignment["answer_ids"]
    if len(deliveries) != len(answer_ids):
        raise ValueError("delivery and answer counts differ")
    answers = {}
    downloaded = []
    try:
        for item, answer_id in zip(deliveries, answer_ids):
            link = item if isinstance(item, str) else item["download"]
            artifact = session.get(urljoin(BASE, link), timeout=10)
            artifact.raise_for_status()
            downloaded.append(artifact.content)
            answers[answer_id] = decode(artifact.content)
        verdict = session.post(BASE, json={"challenge": CHALLENGE, "answers": answers}, timeout=10)
        verdict.raise_for_status()
        result = verdict.json()
        print(json.dumps({"answers": answers, "result": result.get("result"), "flag": result.get("flag"), "remaining": result.get("remaining"), "status": result.get("status")}), flush=True)
        if result.get("result") != "CORRECT":
            raise ValueError("Mastery was not completed")
    except Exception:
        attempt = assignment.get("attempt_id", "unknown")
        for index, artifact in enumerate(downloaded, 1):
            Path(__file__).with_name(f"provider_paths_mastery_debug_{attempt}_{index}.apk").write_bytes(artifact)
        raise


if __name__ == "__main__":
    main()
