#!/usr/bin/env python3
import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path


def run_ssh(host: str, remote_command: str) -> str:
    proc = subprocess.run(
        ["ssh", host, remote_command],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"SSH command failed ({proc.returncode}):\n"
            f"{proc.stderr.strip() or proc.stdout.strip()}"
        )
    return proc.stdout


def parse_json_output(text: str):
    text = text.strip()
    if not text:
        raise ValueError("Game Master returned no output.")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        starts = [i for i in (text.find("{"), text.find("[")) if i >= 0]
        if not starts:
            raise
        return json.loads(text[min(starts):])


def safe_name(value: str) -> str:
    value = re.sub(r"[^a-z0-9._-]+", "_", value.strip().lower())
    return value.strip("_") or "challenge"


def collect_challenge_records(obj):
    found = []

    def walk(x):
        if isinstance(x, dict):
            cid = x.get("id")
            if isinstance(cid, str) and (
                "day" in x or "mode" in x or "lane" in x or "name" in x or "title" in x
            ):
                found.append(x)
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(obj)
    return found


def challenge_day(record):
    day = record.get("day")
    if isinstance(day, int):
        return day
    if isinstance(day, str) and day.isdigit():
        return int(day)

    cid = str(record.get("id", ""))
    m = re.search(r"(?:^|-)day[-_]?0*(\d+)(?:-|$)", cid, re.I)
    return int(m.group(1)) if m else None


def base_challenge_id(record):
    return str(record.get("id", "")).split("/", 1)[0]


def markdown_escape(text):
    return str(text).replace("|", r"\|").replace("\n", " ")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Huntress CTF list and full Game Master details for one day."
    )
    parser.add_argument("day", type=int, help="CTF day number, e.g. 3")
    parser.add_argument("--host", default="huntress", help="SSH host/alias (default: huntress)")
    parser.add_argument(
        "--out",
        default="game_master",
        help="Local output directory (default: ./game_master)",
    )
    parser.add_argument(
        "--all-modes",
        action="store_true",
        help="Include time_trial/mastery. Default: single_solve only.",
    )
    args = parser.parse_args()

    if not 1 <= args.day <= 31:
        parser.error("day must be between 1 and 31")

    root = Path(args.out).expanduser()
    day_dir = root / f"day_{args.day:02d}"
    details_dir = day_dir / "details"
    details_dir.mkdir(parents=True, exist_ok=True)

    # list_cmd = f'curl -fsS "$HUNTRESS_GAME_MASTER_URL?op=list&day={args.day}"'

    list_cmd = (
    'source /etc/profile.d/huntress-game-master.sh && '
    f'curl -fsS "$HUNTRESS_GAME_MASTER_URL?op=list&day={args.day}"'
    )
    
    print(f"[+] Fetching Day {args.day} challenge list via ssh {args.host} ...")
    list_data = parse_json_output(run_ssh(args.host, list_cmd))

    (day_dir / "challenges.json").write_text(
        json.dumps(list_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    selected = {}
    for rec in collect_challenge_records(list_data):
        cid = rec.get("id")
        if not isinstance(cid, str) or challenge_day(rec) != args.day:
            continue
        if not args.all_modes:
            if "/" in cid or rec.get("mode") not in (None, "single_solve"):
                continue
        selected[cid] = rec

    if not selected:
        print(f"[!] No Day {args.day} challenge records detected.")
        print(f"[i] Raw list saved to {day_dir / 'challenges.json'}")
        return 2

    print(f"[+] Found {len(selected)} challenge(s). Fetching full details...")
    results = []

    for cid, rec in sorted(
        selected.items(),
        key=lambda kv: (str(kv[1].get("lane", "")), str(kv[1].get("name", kv[1].get("title", "")))),
    ):
        base_id = base_challenge_id(rec)
        payload = json.dumps({"challenge": base_id})
        remote = (
            "source /etc/profile.d/huntress-game-master.sh && "
            "curl -fsS -X POST "
            "-H 'Content-Type: application/json' "
            f"-d {shlex.quote(payload)} "
            '"$HUNTRESS_GAME_MASTER_URL"'
        )
        
        label = rec.get("name") or rec.get("title") or cid
        print(f"    - {label} [{base_id}]")

        try:
            detail = parse_json_output(run_ssh(args.host, remote))
        except Exception as exc:
            detail = {"challenge": base_id, "_sync_error": str(exc)}

        detail_path = details_dir / f"{safe_name(base_id)}.json"
        detail_path.write_text(
            json.dumps(detail, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        results.append((rec, detail, detail_path))

    summary = [
        f"# Huntress CTF 2026 - Day {args.day}",
        "",
        "Generated from the Game Master through the Homebase SSH connection.",
        "",
        "## Challenges",
        "",
        "| Lane | Challenge | ID | Questions | Detail file |",
        "|---|---|---|---:|---|",
    ]

    for rec, detail, detail_path in results:
        lane = rec.get("lane", "")
        name = rec.get("name") or rec.get("title") or rec.get("id", "")
        cid = base_challenge_id(rec)
        questions = detail.get("questions", [])
        qcount = len(questions) if isinstance(questions, list) else 0
        rel = detail_path.relative_to(day_dir)
        summary.append(
            f"| {markdown_escape(lane)} | {markdown_escape(name)} | "
            f"`{markdown_escape(cid)}` | {qcount} | [{rel.name}]({rel.as_posix()}) |"
        )

    for rec, detail, _ in results:
        name = rec.get("name") or rec.get("title") or rec.get("id", "")
        cid = base_challenge_id(rec)
        summary += ["", f"## {name}", "", f"- **ID:** `{cid}`", f"- **Lane:** `{rec.get('lane', '')}`"]

        if detail.get("_sync_error"):
            summary.append(f"- **Error:** `{detail['_sync_error']}`")
            continue

        if detail.get("prompt"):
            summary += ["", "### Prompt", "", str(detail["prompt"])]

        if detail.get("sha256") or detail.get("download"):
            summary += ["", "### Artifact", ""]
            if detail.get("sha256"):
                summary.append(f"- **SHA-256:** `{detail['sha256']}`")
            if detail.get("download"):
                summary.append(f"- **Download:** `{detail['download']}`")

        questions = detail.get("questions", [])
        if isinstance(questions, list) and questions:
            summary += ["", "### Questions", ""]
            for i, q in enumerate(questions, 1):
                qid = q.get("id", "")
                text = q.get("question", "")
                summary.append(f"{i}. **`{qid}`** - {text}")
                if q.get("artifact"):
                    summary.append(f"   - Artifact: `{q['artifact']}`")
                fmt = q.get("answer_format", {})
                if isinstance(fmt, dict):
                    if fmt.get("kind"):
                        summary.append(f"   - Format: `{fmt['kind']}`")
                    if fmt.get("accepted_values"):
                        vals = ", ".join(f"`{v}`" for v in fmt["accepted_values"])
                        summary.append(f"   - Accepted values: {vals}")

        answer_ids = detail.get("answer_ids")
        if isinstance(answer_ids, list):
            summary += ["", "### Answer IDs", "", "```text", *map(str, answer_ids), "```"]

    summary_path = day_dir / f"day_{args.day:02d}_summary.md"
    summary_path.write_text("\n".join(summary) + "\n", encoding="utf-8")

    print()
    print("[+] Done.")
    print(f"    Raw list: {day_dir / 'challenges.json'}")
    print(f"    Details:  {details_dir}")
    print(f"    Summary:  {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
