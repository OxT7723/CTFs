#!/usr/bin/env python3
"""Follow an assigned app's route inventory and extract its response proof."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urljoin, urlsplit

from inspect_target import fetch, normalize_url, origin, safe_filename


PROOF_RE = re.compile(r"\bproof[_-][A-Za-z0-9_-]{12,}\b")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read a same-origin clue endpoint and follow its feature route."
    )
    parser.add_argument("target", help="absolute target URL assigned by the Game Master")
    parser.add_argument("--clues", default="/api/clues", help="same-origin clue endpoint")
    parser.add_argument("--route-key", default="feature_route", help="route field in clue JSON")
    parser.add_argument("--output-dir", type=Path, help="directory for response evidence")
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")

    try:
        target = normalize_url(args.target)
        allowed_origin = origin(target)
        clues_url = normalize_url(urljoin(target, args.clues))
        if origin(clues_url) != allowed_origin:
            raise ValueError("clue endpoint must stay on the assigned target origin")
    except ValueError as exc:
        parser.error(str(exc))

    host = urlsplit(target).hostname or "target"
    output_dir = args.output_dir or Path("web-tools/evidence") / f"{host}-clued-route"
    output_dir.mkdir(parents=True, exist_ok=True)
    clues_result = fetch(clues_url, allowed_origin, args.timeout)
    clues_body = clues_result.pop("_body", None)
    if clues_result.get("status") != 200 or not isinstance(clues_body, bytes):
        print(json.dumps({"error": "clue endpoint could not be read"}, indent=2))
        return 1
    clues_path = output_dir / safe_filename(1, clues_url)
    clues_path.write_bytes(clues_body)
    try:
        clues = json.loads(clues_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        print(json.dumps({"error": "clue endpoint did not return valid JSON"}, indent=2))
        return 1

    route = clues.get(args.route_key) if isinstance(clues, dict) else None
    if not isinstance(route, str) or not route:
        print(json.dumps({"error": f"clue field {args.route_key!r} is missing"}, indent=2))
        return 1
    feature_url = normalize_url(urljoin(target, route))
    if origin(feature_url) != allowed_origin:
        print(json.dumps({"error": "feature route leaves the assigned target origin"}, indent=2))
        return 1
    feature_result = fetch(feature_url, allowed_origin, args.timeout)
    feature_body = feature_result.pop("_body", None)
    proof: str | None = None
    feature_record: dict[str, object] = {
        "url": feature_url,
        "status": feature_result.get("status"),
    }
    if isinstance(feature_body, bytes):
        feature_path = output_dir / safe_filename(2, feature_url)
        feature_path.write_bytes(feature_body)
        feature_record.update(
            {
                "sha256": hashlib.sha256(feature_body).hexdigest(),
                "body_file": feature_path.name,
            }
        )
        matches = list(
            dict.fromkeys(PROOF_RE.findall(feature_body.decode("utf-8", errors="replace")))
        )
        if matches:
            proof = matches[0]

    report = {
        "target": target,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "clues": clues,
        "clues_sha256": hashlib.sha256(clues_body).hexdigest(),
        "clues_file": clues_path.name,
        "feature": feature_record,
        "proof": proof,
        "request_policy": {"method": "GET", "same_origin_only": True},
    }
    report_path = output_dir / "report.json"
    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "report": str(report_path),
                "feature_url": feature_url,
                "proof": proof,
            },
            indent=2,
        )
    )
    return 0 if proof else 1


if __name__ == "__main__":
    sys.exit(main())
