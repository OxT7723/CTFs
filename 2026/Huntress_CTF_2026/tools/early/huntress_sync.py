#!/usr/bin/env python3
"""Read-only synchronization of the public Game Master inventory to this repo."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import quote

import gm
import coursestack_sync as common


VERSION = 1
README_START = '<!-- huntress:metadata:start -->'
README_END = '<!-- huntress:metadata:end -->'
INDEX_START = '<!-- huntress:index:start -->'
INDEX_END = '<!-- huntress:index:end -->'
LEGACY_COURSE_INDEX_START = '<!-- coursestack:index:start -->'
LEGACY_COURSE_INDEX_END = '<!-- coursestack:index:end -->'
MODES = ("single_solve", "time_trial", "mastery")
MODE_LABELS = {"single_solve": "Single Solve", "time_trial": "Time Trial", "mastery": "Mastery"}


def family_id(challenge_id: str) -> str:
    return re.sub(r"/(?:time_trial|mastery)$", "", challenge_id)


def safe_public_record(record: dict) -> dict:
    """Allowlist public list fields; notably the live list also has `flag`."""
    return {k: record[k] for k in ("id", "name", "title", "day", "lane", "mode", "prompt", "guidance", "solved") if k in record}


def safe_questions(status: dict) -> list[dict]:
    questions = status.get("questions")
    if not isinstance(questions, list):
        return []
    allowed = ("id", "answer_id", "question", "prompt", "artifact", "answer_format", "normalization")
    return [{k: q[k] for k in allowed if k in q} for q in questions if isinstance(q, dict)]


def safe_status(status: dict, http_status: int) -> dict:
    """Persist useful status/question metadata, never answer values or flags."""
    out: dict = {"http_status": http_status}
    for key in ("status", "result", "solved", "remaining", "deadline", "attempt_id", "mode", "challenge"):
        value = status.get(key)
        if isinstance(value, (str, int, float, bool)) or value is None:
            if key in status:
                out[key] = value
    if "status" not in out and isinstance(status.get("error"), str):
        out["status"] = status["error"]
    if isinstance(status.get("answer_ids"), list):
        out["answer_ids"] = [x for x in status["answer_ids"] if isinstance(x, str)]
    questions = safe_questions(status)
    if questions:
        out["questions"] = questions
        out.setdefault("answer_ids", [q.get("answer_id") or q.get("id") for q in questions if q.get("answer_id") or q.get("id")])
    # Some status responses report answer results as a mapping/list. Keep only
    # identifiers and result states; submitted candidates remain local state.
    answers = status.get("answers")
    if isinstance(answers, dict):
        out["answer_results"] = {
            str(k): {field: v[field] for field in ("status", "result", "correct") if field in v}
            for k, v in answers.items() if isinstance(v, dict)
        }
    elif isinstance(answers, list):
        out["answer_results"] = [
            {field: v[field] for field in ("answer_id", "id", "status", "result", "correct") if field in v}
            for v in answers if isinstance(v, dict)
        ]
    return out


def slug(value: str) -> str:
    return common.folder_name(value)


def local_challenge_dirs(root: Path) -> dict[tuple[int, str], Path]:
    found = {}
    for path in root.glob("[0-9][0-9]-*"):
        if not path.is_dir():
            continue
        m = re.match(r"(\d+)-(.+)$", path.name)
        if not m:
            continue
        normalized = re.sub(r"[^a-z0-9]", "", m.group(2).casefold())
        found[(int(m.group(1)), normalized)] = path
    return found


def locate_folder(root: Path, local: dict, group: dict, known_gm_paths: dict[str, Path]) -> Path:
    day = group.get("day")
    title = group.get("title") or group.get("name") or group["id"]
    if group["id"] in known_gm_paths:
        return known_gm_paths[group["id"]]
    norm = re.sub(r"[^a-z0-9]", "", common.clean(title).casefold())
    existing = local.get((day, norm))
    # A matching name is only a candidate. Adopt it only when prior machine
    # state or the explicit CourseStack folder record confirms the association.
    if existing and (existing / "challenge_state.json").exists():
        previous = read_json(existing / "challenge_state.json", {})
        if previous.get("challenge_id") == group["id"]:
            return existing
    folder = root / f"{int(day):02d}-{slug(title)}"
    # Never infer cross-system identity from title alone.
    if folder.exists():
        folder = root / f"{int(day):02d}-{slug(title)}-{re.sub(r'[^a-zA-Z0-9]', '', group['id'])[-8:]}"
    return folder


def read_json(path: Path, default):
    if not path.exists() or not path.stat().st_size:
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def migrated_answers(folder: Path) -> list[dict]:
    migrated = []
    for path in sorted(folder.glob("*answer*status*.json")):
        data = read_json(path, None)
        if not isinstance(data, dict) or not isinstance(data.get("answers"), list):
            continue
        answers = {}
        for item in data["answers"]:
            if not isinstance(item, dict) or not item.get("answer_id"):
                continue
            answer_id = str(item["answer_id"])
            status = item.get("status")
            entry = {"confirmed": status == "accepted", "scope": "instance", "evidence": f"migrated from {path.name}", "incorrect_candidates": []}
            if status == "accepted" and "answer" in item:
                entry["confirmed_candidate"] = item["answer"]
            if item.get("last_candidate_result") == "incorrect" and item.get("last_submitted_candidate") is not None:
                entry["incorrect_candidates"].append(item["last_submitted_candidate"])
            if item.get("unaccepted_saved_guess") is not None:
                entry["candidate"] = item["unaccepted_saved_guess"]
            entry["last_submission_result"] = item.get("last_candidate_result", status)
            answers[answer_id] = entry
        migrated.append({"mode": data.get("mode", "single_solve"), "source": path.name, "instance_key": "legacy-import", "answers": answers, "accepted_count": data.get("accepted_count"), "pending_count": data.get("pending_count")})
    return migrated


def ensure_state(folder: Path, group: dict, course_record: dict | None = None) -> dict:
    path = folder / "challenge_state.json"
    state = read_json(path, {})
    if not isinstance(state, dict):
        state = {}
    state.setdefault("version", VERSION)
    state.setdefault("challenge_id", group["id"])
    state.setdefault("day", group.get("day"))
    state.setdefault("lane", group.get("lane"))
    state.setdefault("knowledge", {})
    if course_record:
        state["coursestack"] = {
            "key": course_record.get("key"),
            "identity": course_record.get("identity"),
            "course_id": course_record.get("course_id"),
        }
    state.setdefault("modes", {})
    for mode in MODES:
        state["modes"].setdefault(mode, {"challenge_id": None, "listed_solved": None, "status": None, "answer_ids": [], "attempts": []})
    if not state.get("modes", {}).get("single_solve", {}).get("attempts"):
        state["modes"]["single_solve"]["attempts"].extend(migrated_answers(folder))
    return state


def ensure_legacy_state(folder: Path, root: Path, legacy_index: dict) -> dict:
    """Give historical local folders standard state without dropping old files."""
    sources = []
    for p in sorted(folder.glob("*answer*status*.json")):
        data = read_json(p, None)
        if isinstance(data, dict) and isinstance(data.get("answers"), list):
            sources.append(data)
    data = sources[0] if sources else {}
    relative = (folder / "readme.md").relative_to(root).as_posix()
    course_record = next((r for r in legacy_index.get("records", {}).values()
                          if isinstance(r, dict) and r.get("path") == relative), {})
    state = read_json(folder / "challenge_state.json", {})
    state.setdefault("version", VERSION)
    state.setdefault("challenge_id", data.get("challenge_id", "local:" + folder.name))
    if not data and course_record:
        state.setdefault("source_system", "coursestack")
        state.setdefault("source_record_id", course_record.get("identity"))
    if course_record:
        state["coursestack"] = {
            "key": course_record.get("key"),
            "identity": course_record.get("identity"),
            "course_id": legacy_index.get("course_id"),
        }
    state.setdefault("day", int(folder.name[:2]) if folder.name[:2].isdigit() else None)
    state.setdefault("lane", course_record.get("category", "unknown"))
    if state.get("lane") == "unknown" and course_record.get("category"):
        state["lane"] = course_record["category"]
    state.setdefault("title", data.get("challenge", course_record.get("title", folder.name)))
    state.setdefault("knowledge", {})
    state.setdefault("modes", {})
    for mode in MODES:
        state["modes"].setdefault(mode, {"challenge_id": None, "listed_solved": None, "status": None, "answer_ids": [], "attempts": []})
    mode = data.get("mode", "single_solve")
    if mode not in MODES:
        mode = "single_solve"
    if not state["modes"][mode]["attempts"]:
        state["modes"][mode]["attempts"].extend(migrated_answers(folder))
    return state


def render_metadata(group: dict) -> str:
    lines = ["## Game Master metadata", "", f"- **Challenge ID:** `{group['id']}`", f"- **Day:** {group.get('day')}", f"- **Lane:** {group.get('lane')}", "", "### Modes", "", "| Mode | Challenge ID | Listed status |", "| --- | --- | --- |"]
    for mode in MODES:
        record = group["modes"].get(mode)
        if record:
            solved = record.get("solved")
            label = "Solved" if solved is True else "Unsolved" if solved is False else "Not reported"
            lines.append(f"| {MODE_LABELS[mode]} | `{record['id']}` | {label} |")
        else:
            lines.append(f"| {MODE_LABELS[mode]} | — | Not offered in current list |")
    if group.get("prompt"):
        lines += ["", "### Current prompt", "", str(group["prompt"])]
    if group.get("guidance"):
        lines += ["", "### Game Master guidance", "", str(group["guidance"])]
    qset = []
    for mode in MODES:
        status = group["modes"].get(mode, {}).get("status_detail", {})
        for q in status.get("questions", []):
            if q not in qset:
                qset.append(q)
    if qset:
        lines += ["", "### Questions and answer formats", ""]
        for q in qset:
            qid = q.get("answer_id") or q.get("id", "")
            lines.append(f"- **`{qid}`**: {q.get('question') or q.get('prompt', '')}")
            if q.get("artifact"):
                lines.append(f"  - Artifact: `{q['artifact']}`")
            if q.get("answer_format"):
                lines.append(f"  - Format: `{json.dumps(q['answer_format'], ensure_ascii=False)}`")
            if q.get("normalization"):
                lines.append(f"  - Normalization: `{q['normalization']}`")
    return "\n".join(lines)


def make_readme(folder: Path, group: dict) -> str:
    path = folder / "readme.md"
    old = common.read_text(path)
    if not old:
        old = f"# {group.get('title') or group.get('name') or group['id']}\n\n"
    elif README_START in old and not re.search(r"^#\s+", old, re.M):
        old = f"# {group.get('title') or group.get('name') or group['id']}\n\n" + old.lstrip()
    content = common.replace_block(old, render_metadata(group), README_START, README_END)
    if old.startswith(f"# {group.get('title') or group.get('name') or group['id']}\n") and "## My Notes" not in old:
        content += "\n\n---\n\n## My Notes\n\n### Initial Thoughts\n\n### Analysis\n\n### Commands Used\n\n```text\n\n```\n\n### Solution\n\n### Lessons Learned\n"
    return content


def replace_primary_index(text: str, rows: str) -> str:
    """Own a distinct Huntress region, migrating the prior shared region once."""
    huntress = common.block(text, INDEX_START, INDEX_END)
    managed = INDEX_START + "\n" + rows.rstrip() + "\n" + INDEX_END
    if huntress is not None:
        a, b = huntress
        return text[:a] + managed + text[b:]
    old_course = common.block(text, LEGACY_COURSE_INDEX_START, LEGACY_COURSE_INDEX_END)
    if old_course is not None:
        a, b = old_course
        return text[:a] + managed + text[b:]
    return text.rstrip() + "\n\n" + managed + "\n"


def build_groups(challenges: list[dict]) -> dict[str, dict]:
    groups: dict[str, dict] = {}
    for raw in challenges:
        if not isinstance(raw, dict) or not isinstance(raw.get("id"), str):
            continue
        record = safe_public_record(raw)
        fid = family_id(record["id"])
        group = groups.setdefault(fid, {"id": fid, "modes": {}})
        for key in ("day", "lane", "title", "name", "prompt", "guidance"):
            if key in record and record[key] is not None:
                group[key] = record[key]
        mode = record.get("mode")
        if mode in MODES:
            group["modes"][mode] = record
    return groups


def sync_data(root: Path, listing: dict, status_by_id: dict[str, tuple[dict, int]] | None = None, dry_run: bool = False) -> tuple[int, int]:
    groups = build_groups(listing.get("challenges", []))
    local = local_challenge_dirs(root)
    planned: list[tuple[Path, str]] = []
    rows = ["## Challenges", "", "| Day | Lane | Challenge | Single Solve | Time Trial | Mastery | Writeup |", "| --- | --- | --- | --- | --- | --- | --- |"]
    live_paths = set()
    writeup_by_path = {}
    course_by_path = {}
    course_by_key = {}
    legacy_state = read_json(root / ".coursestack-sync.json", {})
    if isinstance(legacy_state, dict):
        for record in legacy_state.get("records", {}).values():
            if isinstance(record, dict) and record.get("path"):
                relative = str(record["path"])
                record = dict(record)
                record["course_id"] = legacy_state.get("course_id")
                course_by_path[relative] = record
                course_by_key[record.get("key")] = record
                writeup_by_path[relative] = record.get("writeup", "")

    index_path = root / "README.md"
    index_text = common.read_text(index_path)
    for key, value in common.writeups(index_text).items():
        record = course_by_key.get(key)
        if record and value:
            writeup_by_path[record["path"]] = value

    known_gm_paths = {}
    for state_path in root.glob("[0-9][0-9]-*/challenge_state.json"):
        saved = read_json(state_path, {})
        family = saved.get("challenge_id")
        if isinstance(family, str) and not family.startswith("local:"):
            known_gm_paths[family] = state_path.parent

    for group in sorted(groups.values(), key=lambda g: (g.get("day", 0), str(g.get("title", "")).casefold(), g["id"])):
        folder = locate_folder(root, local, group, known_gm_paths)
        folder.mkdir(parents=True, exist_ok=True) if not dry_run else None
        live_paths.add(folder.resolve())
        relative_readme = (folder / "readme.md").relative_to(root).as_posix()
        course_record = course_by_path.get(relative_readme)
        state = ensure_state(folder, group, course_record)
        state["challenge_id"] = group["id"]
        state["day"] = group.get("day")
        state["lane"] = group.get("lane")
        state["title"] = group.get("title") or group.get("name")
        for mode in MODES:
            entry = state["modes"][mode]
            current = group["modes"].get(mode)
            if current:
                entry["challenge_id"] = current["id"]
                entry["listed_solved"] = current.get("solved")
                status_pair = (status_by_id or {}).get(current["id"])
                if status_pair:
                    detail, http_status = status_pair
                    normalized = safe_status(detail, http_status)
                    entry["status"] = normalized
                    entry["answer_ids"] = normalized.get("answer_ids", entry.get("answer_ids", []))
                    current["status_detail"] = normalized
                    attempt_id = normalized.get("attempt_id")
                    if not attempt_id and isinstance(detail.get("attempt"), dict):
                        attempt_id = detail["attempt"].get("id")
                    if attempt_id or normalized.get("deadline"):
                        attempt_key = str(attempt_id or normalized["deadline"])
                        history = entry.setdefault("attempts", [])
                        previous = next((a for a in history if str(a.get("attempt_id") or a.get("deadline")) == attempt_key), None)
                        snapshot = {"mode": mode, "attempt_id": attempt_id, "deadline": normalized.get("deadline"),
                                    "status": normalized.get("status"), "result": normalized.get("result"),
                                    "remaining": normalized.get("remaining"), "answer_ids": normalized.get("answer_ids", [])}
                        if previous is None:
                            history.append(snapshot)
                        else:
                            previous.update(snapshot)
            # A mode absent from today's list is retained and marked not-listed;
            # previous attempts and state are never removed.
        planned.append((folder / "challenge_state.json", json.dumps(state, ensure_ascii=False, indent=2) + "\n"))
        planned.append((folder / "readme.md", make_readme(folder, group)))
        cells = []
        for mode in MODES:
            current = group["modes"].get(mode)
            if current is None:
                cells.append("—")
            else:
                cells.append("✅" if current.get("solved") is True else "⬜" if current.get("solved") is False else "?")
        link = "/".join(quote(part) for part in folder.relative_to(root).parts) + "/readme.md"
        writeup = writeup_by_path.get((folder / "readme.md").relative_to(root).as_posix(), "")
        cs = f" <!-- cs:{course_record['key']} -->" if course_record and course_record.get("key") else ""
        rows.append(f"| Day {int(group['day']):02d}{cs} | {common.cell(group.get('lane', ''))} | [{common.cell(group.get('title') or group.get('name', group['id']))}]({link}) | {cells[0]} | {cells[1]} | {cells[2]} | {writeup} |")

    # Retain local-only and historical directories in the index; never delete them.
    for folder in sorted(root.glob("[0-9][0-9]-*")):
        if not folder.is_dir() or folder.resolve() in live_paths:
            continue
        readme = folder / "readme.md"
        if not readme.exists():
            continue
        match = re.match(r"(\d+)-(.+)$", folder.name)
        day = f"Day {int(match.group(1)):02d}" if match else "Local"
        label = re.sub(r"_+", " ", match.group(2)) if match else folder.name
        link = "/".join(quote(part) for part in folder.relative_to(root).parts) + "/readme.md"
        legacy = ensure_legacy_state(folder, root, legacy_state)
        planned.append((folder / "challenge_state.json", json.dumps(legacy, ensure_ascii=False, indent=2) + "\n"))
        relative_readme = (folder / "readme.md").relative_to(root).as_posix()
        course_record = course_by_path.get(relative_readme)
        writeup = writeup_by_path.get(relative_readme, "")
        cs = f" <!-- cs:{course_record['key']} -->" if course_record and course_record.get("key") else ""
        rows.append(f"| {day}{cs} | Local history | [{common.cell(label)}]({link}) | Historical | Historical | Historical | {writeup} |")

    if not index_text:
        index_text = "# Huntress CTF 2026: AI Arena\n\nNotes and writeups for this CTF.\n\n"
    planned.append((index_path, replace_primary_index(index_text, "\n".join(rows))))

    mapping = {"version": 1, "course_id": legacy_state.get("course_id") if isinstance(legacy_state, dict) else None, "mappings": {}}
    for relative, record in sorted(course_by_path.items()):
        folder = root / Path(relative).parent
        challenge_state = read_json(folder / "challenge_state.json", {})
        family = challenge_state.get("challenge_id")
        modes = challenge_state.get("modes", {})
        mapping["mappings"][record["key"]] = {
            "coursestack_identity": record.get("identity"),
            "folder": Path(relative).parent.as_posix(),
            "game_master_family_id": family if isinstance(family, str) and not family.startswith("local:") else None,
            "currently_listed_in_game_master": family in groups,
            "game_master_mode_ids": {name: modes.get(name, {}).get("challenge_id") for name in MODES if modes.get(name, {}).get("challenge_id")},
        }
    planned.append((root / ".coursestack-gm-map.json", json.dumps(mapping, ensure_ascii=False, indent=2) + "\n"))

    changed = 0
    for path, text in planned:
        if common.read_text(path) == text:
            continue
        changed += 1
        if not dry_run:
            common.atomic_write(path, text)
    return len(groups), changed


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--from-snapshot", type=Path, help="Use a saved list JSON instead of making network calls.")
    parser.add_argument("--no-status", action="store_true", help="Do not make read-only status GET requests.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    lock = None
    try:
        root = args.root.resolve()
        if not args.dry_run:
            lock_path = root / ".huntress-gm-sync.lock"
            fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.close(fd)
            lock = lock_path
        if args.from_snapshot:
            listing = json.loads(args.from_snapshot.read_text(encoding="utf-8"))
        else:
            client = gm.GameMasterClient()
            listing = client.list_challenges(all_released=True)
        statuses = {}
        if not args.no_status and not args.from_snapshot:
            client = client  # make the selected authenticated client explicit
            for raw in listing.get("challenges", []):
                cid = raw.get("id") if isinstance(raw, dict) else None
                if not isinstance(cid, str):
                    continue
                try:
                    statuses[cid] = client.status(cid)
                except gm.GameMasterError as exc:
                    print(f"Warning: status unavailable for {cid}: {exc}", file=sys.stderr)
        count, changed = sync_data(root, listing, statuses, args.dry_run)
        print(f"{'Preview' if args.dry_run else 'Synced'} {count} challenge families; {changed} files {'would change' if args.dry_run else 'changed'}.")
        return 0
    except (OSError, ValueError, TypeError, KeyError, gm.GameMasterError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    finally:
        if lock is not None:
            lock.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
