#!/usr/bin/env python3
"""Collect a small, passive HTTP snapshot from a supplied CTF target."""

from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


MAX_BODY_BYTES = 2 * 1024 * 1024
MAX_REDIRECTS = 5
MAX_REQUESTS = 16
DEFAULT_PATHS = ["/", "/robots.txt", "/sitemap.xml", "/.well-known/security.txt"]


class PageExtractor(HTMLParser):
    """Extract useful page structure without executing or rendering the HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.in_title = False
        self.links: list[dict[str, str]] = []
        self.scripts: list[str] = []
        self.forms: list[dict[str, object]] = []
        self._form: dict[str, object] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if tag == "title":
            self.in_title = True
        elif tag in {"a", "link"} and values.get("href"):
            self.links.append({"tag": tag, "href": values["href"]})
        elif tag == "script" and values.get("src"):
            self.scripts.append(values["src"])
        elif tag == "form":
            self._form = {
                "action": values.get("action", ""),
                "method": values.get("method", "get").upper(),
                "controls": [],
            }
            self.forms.append(self._form)
        elif tag in {"input", "button", "select", "textarea"} and self._form is not None:
            controls = self._form["controls"]
            assert isinstance(controls, list)
            controls.append(
                {
                    "tag": tag,
                    "type": values.get("type", ""),
                    "name": values.get("name", ""),
                    "value": values.get("value", ""),
                }
            )

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        elif tag == "form":
            self._form = None

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data.strip())


class NoAutomaticRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        return None


def origin(url: str) -> tuple[str, str, int]:
    parts = urlsplit(url)
    if parts.scheme not in {"http", "https"} or not parts.hostname:
        raise ValueError("target must be an absolute http:// or https:// URL")
    if parts.username is not None or parts.password is not None:
        raise ValueError("do not put credentials in the target URL")
    port = parts.port or (443 if parts.scheme == "https" else 80)
    return parts.scheme.lower(), parts.hostname.lower(), port


def normalize_url(url: str) -> str:
    parts = urlsplit(url)
    if parts.scheme not in {"http", "https"} or not parts.hostname:
        raise ValueError(f"not an HTTP(S) URL: {url}")
    if parts.username is not None or parts.password is not None:
        raise ValueError("URLs containing credentials are not allowed")
    return urlunsplit((parts.scheme, parts.netloc, parts.path or "/", parts.query, ""))


def content_charset(content_type: str) -> str:
    match = re.search(r"charset\s*=\s*['\"]?([^;'\"]+)", content_type, re.IGNORECASE)
    return match.group(1).strip() if match else "utf-8"


def request_once(url: str, timeout: float):
    request = Request(
        url,
        headers={
            "User-Agent": "HuntressCTF-Web-Inspector/1.0",
            "Accept": "*/*",
        },
        method="GET",
    )
    opener = build_opener(NoAutomaticRedirects)
    try:
        response = opener.open(request, timeout=timeout)
    except HTTPError as exc:
        response = exc
    status = getattr(response, "status", response.code)
    headers = {key.lower(): value for key, value in response.headers.items()}
    body = response.read(MAX_BODY_BYTES + 1)
    truncated = len(body) > MAX_BODY_BYTES
    if truncated:
        body = body[:MAX_BODY_BYTES]
    return status, headers, body, truncated


def fetch(url: str, target_origin: tuple[str, str, int], timeout: float) -> dict[str, object]:
    current = normalize_url(url)
    redirects: list[dict[str, object]] = []
    for _ in range(MAX_REDIRECTS + 1):
        if origin(current) != target_origin:
            raise ValueError(f"refusing off-origin URL: {current}")
        try:
            status, headers, body, truncated = request_once(current, timeout)
        except HTTPError as exc:
            status = exc.code
            headers = {key.lower(): value for key, value in exc.headers.items()}
            body = exc.read(MAX_BODY_BYTES + 1)
            truncated = len(body) > MAX_BODY_BYTES
            body = body[:MAX_BODY_BYTES]
        except URLError as exc:
            return {
                "requested_url": current,
                "error": str(exc.reason),
                "redirects": redirects,
            }

        location = headers.get("location")
        if status in {301, 302, 303, 307, 308} and location:
            try:
                destination = normalize_url(urljoin(current, location))
                destination_origin = origin(destination)
            except ValueError:
                return {
                    "requested_url": current,
                    "status": status,
                    "headers": headers,
                    "redirects": redirects,
                    "error": "redirect is not a valid HTTP(S) URL; not followed",
                }
            redirects.append({"status": status, "from": current, "to": destination})
            if destination_origin != target_origin:
                return {
                    "requested_url": current,
                    "status": status,
                    "headers": headers,
                    "redirects": redirects,
                    "error": "redirect leaves the supplied origin; not followed",
                }
            current = destination
            continue

        digest = hashlib.sha256(body).hexdigest()
        content_type = headers.get("content-type", "")
        is_html = "html" in content_type.lower() or body.lstrip().lower().startswith(
            (b"<!doctype html", b"<html")
        )
        extracted: dict[str, object] = {}
        if is_html:
            try:
                text = body.decode(content_charset(content_type), errors="replace")
            except LookupError:
                text = body.decode("utf-8", errors="replace")
            parser = PageExtractor()
            parser.feed(text)
            extracted = {
                "title": " ".join(part for part in parser.title_parts if part),
                "links": parser.links,
                "scripts": parser.scripts,
                "forms": parser.forms,
            }
        return {
            "requested_url": url,
            "final_url": current,
            "status": status,
            "headers": headers,
            "body_sha256": digest,
            "body_bytes": len(body),
            "body_truncated": truncated,
            "is_html": is_html,
            "extracted": extracted,
            "redirects": redirects,
            "_body": body,
        }
    return {
        "requested_url": url,
        "redirects": redirects,
        "error": f"redirect limit ({MAX_REDIRECTS}) reached",
    }


def safe_filename(index: int, url: str) -> str:
    parts = urlsplit(url)
    label = re.sub(r"[^A-Za-z0-9._-]+", "_", parts.path.strip("/"))[:48] or "root"
    suffix = hashlib.sha256(url.encode("utf-8")).hexdigest()[:10]
    return f"{index:02d}-{label}-{suffix}.body"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Save a bounded, GET-only snapshot of a supplied CTF web target."
    )
    parser.add_argument("target", help="absolute URL supplied by the challenge")
    parser.add_argument(
        "--path",
        action="append",
        dest="paths",
        help="additional same-origin path to GET (repeatable; defaults include common discovery files)",
    )
    parser.add_argument("--output-dir", type=Path, help="evidence directory (default: web-evidence/<host>-<time>)")
    parser.add_argument("--timeout", type=float, default=10.0, help="per-request timeout in seconds (default: 10)")
    args = parser.parse_args()

    try:
        target = normalize_url(args.target)
        target_origin = origin(target)
    except ValueError as exc:
        parser.error(str(exc))
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")

    paths = DEFAULT_PATHS + (args.paths or [])
    if len(paths) > MAX_REQUESTS:
        parser.error(f"at most {MAX_REQUESTS} paths may be requested per run")

    urls: list[str] = []
    for path in paths:
        candidate = normalize_url(urljoin(target, path))
        if origin(candidate) != target_origin:
            parser.error(f"path resolves outside the target origin: {path}")
        if candidate not in urls:
            urls.append(candidate)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    output_dir = args.output_dir or Path("web-evidence") / f"{target_origin[1]}-{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    results: list[dict[str, object]] = []
    for index, url in enumerate(urls, start=1):
        result = fetch(url, target_origin, args.timeout)
        body = result.pop("_body", None)
        if isinstance(body, bytes):
            body_path = output_dir / safe_filename(index, url)
            body_path.write_bytes(body)
            result["body_file"] = body_path.name
        results.append(result)

    report = {
        "target": target,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "request_policy": {
            "method": "GET",
            "max_response_bytes": MAX_BODY_BYTES,
            "max_redirects": MAX_REDIRECTS,
            "same_origin_only": True,
            "forms_submitted": False,
        },
        "results": results,
    }
    report_path = output_dir / "report.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Saved {len(results)} response records to {report_path}")
    for result in results:
        print(
            f"{result.get('status', 'ERR'):>3} "
            f"{result.get('final_url', result.get('requested_url', ''))} "
            f"{result.get('body_sha256', '')}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
