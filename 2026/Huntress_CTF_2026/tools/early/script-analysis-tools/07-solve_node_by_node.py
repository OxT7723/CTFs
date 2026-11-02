#!/usr/bin/env python3
"""Build Node by Node / Script Triage answer candidates from inert artifacts.

This wraps the general descriptor parser in 09-solve.py and applies the
Day 7 Batch errorlevel/exit label correction. It never executes specimens and
does not contact the Game Master.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
DAY9_SOLVER_PATH = HERE / "09-solve.py"


def load_day9_solver():
    spec = importlib.util.spec_from_file_location("script_analysis_day9_solver", DAY9_SOLVER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load the general Script Triage solver: {DAY9_SOLVER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def select_response(data: dict[str, Any], mode: str) -> dict[str, Any]:
    """Accept a status/start response or a saved challenge_state.json file."""
    if isinstance(data.get("questions"), list):
        return data
    modes = data.get("modes")
    if isinstance(modes, dict):
        try:
            response = modes[mode]["status"]
        except (KeyError, TypeError) as exc:
            raise ValueError(f"No {mode!r} status response exists in the supplied file") from exc
        if isinstance(response, dict) and isinstance(response.get("questions"), list):
            return response
    raise ValueError("Input JSON must contain a questions array or challenge_state.json modes")


def apply_day7_batch_control_correction(
    answers: dict[str, str],
    questions: list[dict[str, Any]],
    artifact_root: Path,
) -> None:
    """Recover the more specific Day 7 `if-errorlevel-exit` label."""
    for question in questions:
        answer_id = question["id"]
        inner_id = answer_id
        artifact_dir = artifact_root
        set_match = re.match(r"set(\d+)\.(.+)", answer_id)
        if set_match:
            artifact_dir = artifact_root / f"set{set_match.group(1)}"
            inner_id = set_match.group(2)

        if not inner_id.startswith("batch-") or not inner_id.endswith("-control"):
            continue

        artifact = question.get("artifact", "")
        filename = artifact.rsplit("->", 1)[-1].strip() if "->" in artifact else artifact
        source_path = artifact_dir / filename
        if source_path.suffix.lower() not in {".cmd", ".bat"} or not source_path.is_file():
            continue
        source = source_path.read_text(errors="replace")
        if re.search(r"(?im)^\s*if\s+errorlevel\b[^\r\n]*\bexit\b", source):
            answers[answer_id] = "if-errorlevel-exit"


def build(questions_response: dict[str, Any], artifact_root: Path) -> dict[str, str]:
    solver = load_day9_solver()
    answers = solver.build_all_answers(questions_response, artifact_root)
    apply_day7_batch_control_correction(
        answers,
        questions_response["questions"],
        artifact_root,
    )

    expected = {question["id"] for question in questions_response["questions"]}
    if set(answers) != expected:
        missing = sorted(expected - set(answers))
        extra = sorted(set(answers) - expected)
        raise ValueError(f"Answer IDs do not match questions (missing={missing}, extra={extra})")
    empty = sorted(answer_id for answer_id, value in answers.items() if not str(value))
    if empty:
        raise ValueError(f"No candidate value was reconstructed for: {', '.join(empty)}")
    return answers


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "answer_response",
        type=Path,
        help="saved Game Master start/status JSON or challenge_state.json",
    )
    parser.add_argument(
        "artifact_directory",
        type=Path,
        help="directory containing the extracted assigned specimen files",
    )
    parser.add_argument(
        "--mode",
        choices=("single_solve", "time_trial", "mastery"),
        default="time_trial",
        help="which status to use when answer_response is challenge_state.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="write answer JSON here; otherwise print it to stdout",
    )
    args = parser.parse_args()

    response_data = json.loads(args.answer_response.read_text())
    response = select_response(response_data, args.mode)
    answers = build(response, args.artifact_directory)
    rendered = json.dumps(answers, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
        print(f"Wrote {len(answers)} answer candidates to {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
