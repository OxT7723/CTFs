#!/usr/bin/env python3
"""Find exposed backup proofs using bounded, same-origin GET requests."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from threading import Lock
from urllib.parse import urljoin, urlsplit

from inspect_target import (
    MAX_BODY_BYTES,
    PageExtractor,
    fetch,
    normalize_url,
    origin,
    safe_filename,
)


PROOF_RE = re.compile(r"\bproof[_-][A-Za-z0-9_-]{12,}\b")
BACKUP_RE = re.compile(r"(?:\.bak|\.backup|\.old|\.zip|\.tar(?:\.gz)?)$", re.IGNORECASE)
MAX_REQUESTS = 12


def body_text(result: dict[str, object]) -> str:
    body = result.get("_body")
    if not isinstance(body, bytes):
        return ""
    charset = "utf-8"
    headers = result.get("headers")
    if isinstance(headers, dict):
        content_type = str(headers.get("content-type", ""))
        match = re.search(r"charset\s*=\s*['\"]?([^;'\"]+)", content_type, re.IGNORECASE)
        if match:
            charset = match.group(1).strip()
    try:
        return body.decode(charset, errors="replace")
    except LookupError:
        return body.decode("utf-8", errors="replace")


def hrefs(text: str) -> list[str]:
    parser = PageExtractor()
    parser.feed(text)
    return [item["href"] for item in parser.links if item.get("href")]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Passively find proof text in backup files linked by an assigned target."
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
    output_dir = args.output_dir or Path("web-evidence") / f"{host}-backup"
    output_dir.mkdir(parents=True, exist_ok=True)

    requested: list[str] = []
    results: list[dict[str, object]] = []
    reservation_lock = Lock()

    def get(url: str) -> dict[str, object] | None:
        normalized = normalize_url(url)
        if origin(normalized) != target_origin:
            return None
        with reservation_lock:
            if normalized in requested:
                return next(
                    (item for item in results if item.get("requested_url") == normalized),
                    None,
                )
            if len(requested) >= MAX_REQUESTS:
                return None
            requested.append(normalized)
            request_number = len(requested)
        result = fetch(normalized, target_origin, args.timeout)
        body = result.pop("_body", None)
        if isinstance(body, bytes):
            body_path = output_dir / safe_filename(request_number, normalized)
            body_path.write_bytes(body)
            result["body_file"] = body_path.name
            result["body_sha256"] = hashlib.sha256(body).hexdigest()
            result["body_bytes"] = len(body)
            result["_body"] = body
        with reservation_lock:
            results.append(result)
        return result

    robots_url = urljoin(target, "/robots.txt")
    # These are independent discovery sources, so overlap their network wait.
    with ThreadPoolExecutor(max_workers=2) as pool:
        root_future = pool.submit(get, target)
        robots_future = pool.submit(get, robots_url)
        root = root_future.result()
        robots = robots_future.result()
    backup_pages: list[str] = []

    # Robots paths and explicit links on the target page are the only
    # discovery sources; the solver does not guess paths or crawl the host.
    discovery_results = [item for item in (root, robots) if item is not None]
    for result in discovery_results:
        text = body_text(result)
        if result is robots:
            for line in text.splitlines():
                match = re.match(r"\s*Disallow\s*:\s*(\S+)", line, re.IGNORECASE)
                if match:
                    backup_pages.append(urljoin(target, match.group(1)))
        for link in hrefs(text):
            linked = urljoin(str(result.get("final_url", target)), link)
            try:
                if origin(normalize_url(linked)) != target_origin:
                    continue
            except ValueError:
                continue
            path = urlsplit(linked).path
            if BACKUP_RE.search(path):
                backup_pages.append(linked)

    proof_sources: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for page_url in dict.fromkeys(backup_pages):
        page = get(page_url)
        if page is None:
            continue
        text = body_text(page)
        found = hrefs(text)
        for link in found:
            linked = urljoin(str(page.get("final_url", page_url)), link)
            try:
                normalized = normalize_url(linked)
                if origin(normalized) != target_origin:
                    continue
            except ValueError:
                continue
            if BACKUP_RE.search(urlsplit(normalized).path):
                found_page = get(normalized)
                if found_page is not None:
                    candidate = body_text(found_page)
                    for proof in PROOF_RE.findall(candidate):
                        key = (proof, str(found_page.get("final_url", normalized)))
                        if key not in seen:
                            seen.add(key)
                            proof_sources.append(
                                {
                                    "answer": proof,
                                    "url": key[1],
                                    "sha256": str(found_page.get("body_sha256", "")),
                                    "body_file": str(found_page.get("body_file", "")),
                                }
                            )
        for proof in PROOF_RE.findall(text):
            key = (proof, str(page.get("final_url", page_url)))
            if key not in seen:
                seen.add(key)
                proof_sources.append(
                    {
                        "answer": proof,
                        "url": key[1],
                        "sha256": str(page.get("body_sha256", "")),
                        "body_file": str(page.get("body_file", "")),
                    }
                )

    report_results = [
        {key: value for key, value in result.items() if key != "_body"}
        for result in results
    ]
    report_path = output_dir / "report.json"
    report_path.write_text(
        json.dumps(
            {
                "target": target,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "request_policy": {
                    "method": "GET",
                    "max_response_bytes": MAX_BODY_BYTES,
                    "same_origin_only": True,
                    "max_requests": MAX_REQUESTS,
                },
                "results": report_results,
                "proofs": proof_sources,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"report": str(report_path), "proofs": proof_sources}, indent=2))
    return 0 if proof_sources else 1


if __name__ == "__main__":
    sys.exit(main())
