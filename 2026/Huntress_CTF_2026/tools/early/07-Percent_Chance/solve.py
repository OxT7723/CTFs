"""Decode the current Percent Chance artifact; optionally run a timed attempt."""
import json
import io
import base64
import codecs
import os
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote_to_bytes
from urllib.request import Request, urlopen

BASE = "https://2026.huntress.ctf.games/"
CHALLENGES = {"time_trial": "warmups-day-07/time_trial", "mastery": "warmups-day-07/mastery"}


def decode(blob: bytes) -> str:
    if blob.startswith(b"01\t"):
        parts = [line.split("\t", 1) for line in blob.decode("utf-8").splitlines() if line.strip()]
        if [int(number) for number, _ in parts] != list(range(1, 8)):
            raise ValueError("Unexpected numbered-line structure")
        values = [value for _, value in parts]
        decoded = [
            base64.b64decode(values[0]).decode("utf-8"),
            codecs.decode(values[1], "rot_13"),
            bytes.fromhex(values[2]).decode("utf-8"),
            bytes(int(n, 2) for n in values[3].split()).decode("utf-8"),
            bytes(int(n) for n in values[4].split()).decode("utf-8"),
            bytes(int(n, 8) for n in values[5].split()).decode("utf-8"),
            unquote_to_bytes(values[6]).decode("utf-8"),
        ]
        sentence = "".join(decoded)
        matches = re.findall(r"\b[a-z]+-[a-z]+-[a-z]+-\d{2}\b", sentence)
        if len(matches) != 1:
            raise ValueError(f"Decoded sentence has {len(matches)} slugs: {sentence!r}")
        return matches[0]
    for _ in range(20):
        text = blob.decode("utf-8")
        next_blob = unquote_to_bytes(text)
        if next_blob == blob:
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            if not lines:
                raise ValueError("No decoded lines")
            matches = re.findall(r"\b[a-z]+-[a-z]+-[a-z]+-\d{2}\b", lines[-1])
            if len(matches) != 1:
                raise ValueError("Final line does not contain exactly one slug")
            return matches[0]
        blob = next_blob
    raise ValueError("Percent encoding did not converge")


def request(token, payload=None, url=BASE):
    headers = {"Authorization": "Bearer " + token}
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    return urlopen(Request(url, data=data, headers=headers), timeout=15).read()


def answers_from_artifact(blob: bytes, start: dict) -> dict[str, str]:
    questions = start["questions"]
    answer_ids = start["answer_ids"]
    if len(questions) != len(answer_ids):
        raise ValueError("Question and answer ID counts differ")
    if len(questions) == 1 and not zipfile.is_zipfile(io.BytesIO(blob)):
        return {answer_ids[0]: decode(blob)}
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        files = {name.rsplit("/", 1)[-1]: name for name in archive.namelist() if not name.endswith("/")}
        answers = {}
        for question, answer_id in zip(questions, answer_ids):
            filename = question["artifact"]
            if filename not in files:
                raise ValueError(f"Missing artifact: {filename}")
            try:
                data = archive.read(files[filename], pwd=b"infected")
            except RuntimeError as exc:
                raise ValueError("ZIP could not be opened with password 'infected'; ask user for guidance") from exc
            answers[answer_id] = decode(data)
        return answers


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] not in CHALLENGES:
        print(decode(Path(sys.argv[1]).read_bytes()))
    elif len(sys.argv) in (2, 3) and sys.argv[1] in CHALLENGES:
        if len(sys.argv) == 3 and sys.argv[2] != "--retry":
            raise SystemExit("Only --retry is supported as a third argument")
        challenge = CHALLENGES[sys.argv[1]]
        token = os.environ["HUNTRESS_GM_TOKEN"]
        payload = {"challenge": challenge}
        if len(sys.argv) == 3:
            payload["op"] = "retry"
        start = json.loads(request(token, payload))
        print("started", start.get("attempt_id"), "deadline", start.get("deadline"), flush=True)
        url = "https://2026.huntress.ctf.games" + start["download"]
        blob = request(token, url=url)
        answers = answers_from_artifact(blob, start)
        print("decoded", len(answers), "answers", flush=True)
        result = json.loads(request(token, {"challenge": challenge, "answers": answers}))
        print("result", result.get("result"), "remaining", result.get("remaining"), "flag", result.get("flag"), flush=True)
    else:
        raise SystemExit("usage: solve.py <time_trial|mastery|artifact> [--retry]")
