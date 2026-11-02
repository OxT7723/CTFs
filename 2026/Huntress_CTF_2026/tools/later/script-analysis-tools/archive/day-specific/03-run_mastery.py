#!/usr/bin/env python3
"""Solve a fresh two-set Expansion Pack Mastery attempt from assigned bytes."""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urljoin

import httpx

from solve_expansion import BASE, HERE, build

CHALLENGE = "script-analysis-day-03-batch-expansion/mastery"
LABELS = ("percent", "delayed", "call_double", "for_indirect")


def unpack_zip(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ["7z", "x", "-pinfected", "-y", f"-o{destination}", str(archive)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3,
    )
    if result.returncode:
        raise ValueError("ZIP extraction failed with the documented password infected")


def derive(bundle: Path, qids: list[str]) -> dict[str, str]:
    answers: dict[str, str] = {}
    for index in (1, 2):
        prefix = f"set{index}."
        subset = [qid[len(prefix):] for qid in qids if qid.startswith(prefix)]
        if len(subset) != 159:
            raise ValueError(f"unexpected answer ID set for {prefix}: {len(subset)}")
        extracted = bundle / f"extracted-{index}"
        unpack_zip(bundle / f"evidence-{index:02d}.zip", extracted)
        answers.update({prefix + qid: value for qid, value in build(extracted, subset).items()})
    if set(answers) != set(qids):
        raise ValueError("derived answer IDs differ from current Game Master IDs")
    return answers


async def run(retry: bool) -> None:
    token = os.environ["HUNTRESS_GM_TOKEN"]
    headers = {"Authorization": "Bearer " + token}
    limits = httpx.Limits(max_connections=20, max_keepalive_connections=20)
    async with httpx.AsyncClient(http2=True, headers=headers, timeout=5, limits=limits) as client:
        response = await client.post(BASE, json={"challenge": CHALLENGE, **({"op": "retry"} if retry else {})})
        response.raise_for_status()
        current = response.json()
        attempt = current.get("attempt_id") or "unknown-attempt"
        qids = current.get("answer_ids") or [question["id"] for question in current.get("questions", [])]
        record = {"attempt_id": attempt, "mode": current.get("mode"), "deadline": current.get("deadline"),
                  "answer_count": len(qids), "artifacts": current.get("artifacts"), "download": current.get("download")}
        if current.get("mode") != "mastery" or len(qids) != 318:
            print(json.dumps({"stage": "start", **record, "error": "unexpected start response"}))
            return
        with tempfile.TemporaryDirectory(prefix="expansion-mastery-") as temporary:
            bundle = Path(temporary)
            retained = HERE / "artifacts/mastery" / attempt

            async def fetch(download: str) -> bytes:
                reply = await client.get(urljoin(BASE, download))
                reply.raise_for_status()
                return reply.content

            try:
                artifacts = current.get("artifacts")
                if artifacts:
                    if len(artifacts) != 2:
                        raise ValueError(f"expected two ZIP artifacts, got {len(artifacts)}")
                    contents = await asyncio.gather(*(fetch(item["download"]) for item in artifacts))
                    for index, (item, content) in enumerate(zip(artifacts, contents), 1):
                        filename = item.get("filename") or item.get("name") or f"evidence-{index:02d}.zip"
                        if filename not in ("evidence-01.zip", "evidence-02.zip"):
                            raise ValueError(f"unexpected Mastery artifact name: {filename}")
                        (bundle / filename).write_bytes(content)
                elif current.get("download"):
                    outer = bundle / "mastery.zip"
                    outer.write_bytes(await fetch(current["download"]))
                    unpack_zip(outer, bundle)
                    for index in (1, 2):
                        filename = f"evidence-{index:02d}.zip"
                        if not (bundle / filename).exists():
                            matches = list(bundle.rglob(filename))
                            if len(matches) != 1:
                                raise ValueError(f"outer ZIP did not contain one {filename}")
                            shutil.copy2(matches[0], bundle / filename)
                else:
                    raise ValueError("Mastery response has no artifact download")
                answers = derive(bundle, qids)
            except Exception as exc:
                retained.mkdir(parents=True, exist_ok=True)
                for archive in bundle.glob("*.zip"):
                    shutil.copy2(archive, retained / archive.name)
                (retained / "start.json").write_text(json.dumps(current, indent=2) + "\n")
                print(json.dumps({"stage": "derive", **record, "error": str(exc), "retained": str(retained)}))
                return

            async def submit(payload: dict[str, str]) -> dict:
                try:
                    reply = await client.post(BASE, json={"challenge": CHALLENGE, "answers": payload})
                    if reply.status_code >= 400:
                        return {"http_status": reply.status_code}
                    data = reply.json()
                    return {"result": data.get("result"), "remaining": data.get("remaining"),
                            "flag": data.get("flag"), "status": data.get("status")}
                except Exception as exc:
                    return {"error": type(exc).__name__}

            stable = {qid: value for qid, value in answers.items() if not qid.endswith("-expansion")}
            outcome = await submit(stable)
            results = [{"group": "non_expansion", "count": len(stable), **outcome}]
            if outcome.get("result") != "accepted":
                retained.mkdir(parents=True, exist_ok=True)
                for archive in bundle.glob("*.zip"):
                    shutil.copy2(archive, retained / archive.name)
                (retained / "candidates.json").write_text(json.dumps(answers, indent=2) + "\n")
                (retained / "outcomes.json").write_text(json.dumps(results, indent=2) + "\n")
                print(json.dumps({"stage": "stable_submission", **record, "outcomes": results,
                                  "retained": str(retained)}))
                return

            pending = {qid: value for qid, value in answers.items() if qid.endswith("-expansion")}
            tried = {qid: [] for qid in pending}
            semaphore = asyncio.Semaphore(12)

            async def check(qid: str, value: str) -> dict:
                async with semaphore:
                    result = await submit({qid: value})
                    return {"answer_id": qid, "candidate": value, **result}

            for wave in range(4):
                requests = []
                for qid, primary in pending.items():
                    candidate = next((value for value in (primary, *LABELS) if value not in tried[qid]), None)
                    if candidate is not None:
                        tried[qid].append(candidate)
                        requests.append((qid, candidate))
                if not requests:
                    break
                checked = await asyncio.gather(*(check(qid, value) for qid, value in requests))
                results.extend(checked)
                for item in checked:
                    if item.get("result") in ("accepted", "CORRECT"):
                        pending.pop(item["answer_id"], None)
                if any(item.get("http_status") == 429 for item in checked):
                    break
                if any(item.get("result") == "CORRECT" for item in checked):
                    break

            correct = next((item for item in results if item.get("result") == "CORRECT"), None)
            summary = {"stage": "submit", "attempt_id": attempt, "deadline": current.get("deadline"),
                       "answer_count": len(answers), "stable_result": outcome.get("result"),
                       "accepted_expansion_count": 18 - len(pending), "unresolved_expansion": sorted(pending),
                       "result": "CORRECT" if correct else "incomplete", "flag": correct.get("flag") if correct else None,
                       "request_count": len(results), "http_429": any(item.get("http_status") == 429 for item in results)}
            if not correct:
                retained.mkdir(parents=True, exist_ok=True)
                for archive in bundle.glob("*.zip"):
                    shutil.copy2(archive, retained / archive.name)
                (retained / "candidates.json").write_text(json.dumps(answers, indent=2) + "\n")
                (retained / "outcomes.json").write_text(json.dumps(results, indent=2) + "\n")
                summary["retained"] = str(retained)
            print(json.dumps(summary))


def dry_run() -> None:
    state = json.loads((HERE / "challenge_state.json").read_text())
    ids = state["modes"]["mastery"]["answer_ids"]
    with tempfile.TemporaryDirectory(prefix="expansion-mastery-test-") as temporary:
        bundle = Path(temporary)
        for index in (1, 2):
            shutil.copy2(HERE / "expansion_pack.zip", bundle / f"evidence-{index:02d}.zip")
        answers = derive(bundle, ids)
        print(json.dumps({"dry_run": True, "answer_count": len(answers), "answer_ids_match": set(answers) == set(ids)}))


def main() -> None:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--dry-run", action="store_true")
    action.add_argument("--start", action="store_true")
    action.add_argument("--retry", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        dry_run()
    else:
        asyncio.run(run(retry=args.retry))


if __name__ == "__main__":
    main()
