#!/usr/bin/env python3
"""Build Node by Node / Script Triage answer candidates from inert artifacts.

This wraps the canonical descriptor parser in script_analysis_solver.py. It never executes
specimens and does not contact the Game Master.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import script_analysis_solver


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


def build(questions_response: dict[str, Any], artifact_root: Path) -> dict[str, str]:
    answers = script_analysis_solver.build_all_answers(questions_response, artifact_root)
    script_analysis_solver.validate_answers(questions_response, answers)
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
