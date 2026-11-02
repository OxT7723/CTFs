#!/usr/bin/env python3
"""Run the current Go Fish Time Trial from its assigned ZIP in one pass."""

import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.parse import urljoin

from elftools.elf.elffile import ELFFile
import pefile
import requests

_shared_path = Path(__file__).resolve().parents[1] / "05-Rust_Belt" / "solve_time_trial.py"
_shared_spec = importlib.util.spec_from_file_location("rust_belt_solver", _shared_path)
_shared = importlib.util.module_from_spec(_shared_spec)
_shared_spec.loader.exec_module(_shared)
elf_details = _shared.elf_details
extract_config = _shared.extract_config
pe_metadata = _shared.pe_metadata


BASE = "https://2026.huntress.ctf.games/"
CID = "binary-reverse-engineering-day-04-go-runtime-fingerprints/time_trial"
ROOT = Path(__file__).resolve().parent


def solve(files):
    answers = {}
    for day in range(1, 5):
        prefix = f"d{day:02}"
        suffixes = (".dll",) if day == 3 else (".elf", ".exe")
        name = next(name for name in files if name.startswith(prefix + "--") and name.endswith(suffixes))
        data = files[name]
        container = "pe" if data.startswith(b"MZ") else "elf"
        answers[f"{prefix}_artifact_sha256_1"] = hashlib.sha256(data).hexdigest()
        if day == 1:
            answers.update({f"{prefix}_analysis_{key}": value for key, value in elf_details(data).items()})
            continue
        config, xor_key, crc = extract_config(data)
        for key in ("campaign", "domain", "mutex", "url"):
            if day != 3 or key != "url":
                answers[f"{prefix}_analysis_config_{key}"] = config[key]
        if day != 3:
            answers[f"{prefix}_analysis_config_crc32_hex"] = hex(crc)
        if day == 2:
            answers[f"{prefix}_analysis_format"] = container
            answers[f"{prefix}_analysis_xor_key_hex"] = hex(xor_key)
        elif day == 3:
            runtime = next(name for name in files if name.startswith(prefix + "--") and name.endswith(".runtimeconfig.json"))
            answers[f"{prefix}_artifact_sha256_2"] = hashlib.sha256(files[runtime]).hexdigest()
            answers[f"{prefix}_analysis_format"] = "PE_CLI"
            answers[f"{prefix}_analysis_machine"], answers[f"{prefix}_analysis_metadata_version"] = pe_metadata(data)
        else:
            if container == "pe":
                pe = pefile.PE(data=data, fast_load=True)
                architecture = "x86-64" if pe.FILE_HEADER.Machine == 0x8664 else hex(pe.FILE_HEADER.Machine)
            else:
                architecture = "x86-64" if ELFFile(io.BytesIO(data))["e_machine"] == "EM_X86_64" else "unknown"
            answers[f"{prefix}_analysis_architecture"] = architecture
            answers[f"{prefix}_analysis_format"] = container
    return answers


def main():
    token = os.environ.get("HUNTRESS_GM_TOKEN")
    if not token:
        raise SystemExit("HUNTRESS_GM_TOKEN is missing")
    session = requests.Session()
    session.headers.update({"Authorization": "Bearer " + token})
    retry = "--retry" in sys.argv[1:]
    assignment_response = session.post(BASE, json={"challenge": CID, **({"op": "retry"} if retry else {})}, timeout=10)
    assignment_response.raise_for_status()
    assignment = assignment_response.json()
    if "download" not in assignment:
        print(json.dumps({"stage": "start", "response": assignment}))
        return
    attempt_id = assignment["attempt_id"]
    record = {"attempt_id": attempt_id, "deadline": assignment.get("deadline"),
              "download": assignment["download"], "sha256": assignment.get("sha256"),
              "answer_ids": assignment["answer_ids"]}
    record_path = Path(tempfile.gettempdir()) / f"gofish-time-trial-{attempt_id}.json"
    record_path.write_text(json.dumps(record, indent=2) + "\n")
    archive_response = session.get(urljoin(BASE, assignment["download"]), timeout=10)
    archive_response.raise_for_status()
    archive = archive_response.content
    with tempfile.TemporaryDirectory(prefix="gofish-time-trial-") as work:
        zip_path = Path(work) / "evidence.zip"
        zip_path.write_bytes(archive)
        extracted = Path(work) / "extracted"
        extracted.mkdir()
        subprocess.run(["7z", "x", "-y", "-pinfected", "-o" + str(extracted), str(zip_path)],
                       check=True, stdout=subprocess.DEVNULL)
        files = {path.name: path.read_bytes() for path in extracted.rglob("*") if path.is_file()}
        answers = solve(files)
        expected = set(assignment["answer_ids"])
        if set(answers) != expected:
            record.update({"stage": "answer_fields", "missing": sorted(expected - set(answers)),
                           "unexpected": sorted(set(answers) - expected)})
            (ROOT / "artifacts" / "time_trial").mkdir(parents=True, exist_ok=True)
            (ROOT / "artifacts" / "time_trial" / f"attempt-{attempt_id}.zip").write_bytes(archive)
            record_path.write_text(json.dumps(record, indent=2) + "\n")
            print(json.dumps(record))
            return
        result_response = session.post(BASE, json={"challenge": CID, "answers": answers}, timeout=10)
        result_response.raise_for_status()
        result = result_response.json()
        record.update({"result": result.get("result"), "remaining": result.get("remaining"),
                       "status": result.get("status"), "flag": result.get("flag"),
                       "accepted_ids": result.get("accepted_ids"), "answers": answers})
        if result.get("result") != "CORRECT":
            (ROOT / "artifacts" / "time_trial").mkdir(parents=True, exist_ok=True)
            (ROOT / "artifacts" / "time_trial" / f"attempt-{attempt_id}.zip").write_bytes(archive)
        record_path.write_text(json.dumps(record, indent=2) + "\n")
        print(json.dumps({k: v for k, v in record.items() if k not in ("answers", "answer_ids", "accepted_ids")}))


if __name__ == "__main__":
    main()
