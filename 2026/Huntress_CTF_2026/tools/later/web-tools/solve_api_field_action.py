#!/usr/bin/env python3
"""Use an assigned API inventory to test its disclosed field/action pairs."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlencode, urljoin, urlsplit
from urllib.request import Request, urlopen
from urllib.error import HTTPError

from inspect_target import normalize_url, origin


MAX_BODY_BYTES = 2 * 1024 * 1024
MAX_VALUES = 32
PROOF_RE = re.compile(rb"\bproof[_-][A-Za-z0-9_-]{12,}\b")


def get(url: str, allowed_origin: tuple[str, str, int]) -> tuple[int, bytes]:
    normalized = normalize_url(url)
    if origin(normalized) != allowed_origin:
        raise ValueError(f"refusing off-origin URL: {normalized}")
    request = Request(
        normalized,
        headers={"User-Agent": "HuntressCTF-Web-Inspector/1.0", "Accept": "*/*"},
        method="GET",
    )
    try:
        with urlopen(request, timeout=12) as response:
            return response.status, response.read(MAX_BODY_BYTES + 1)
    except HTTPError as exc:
        return exc.code, exc.read(MAX_BODY_BYTES + 1)


def save_body(output_dir: Path, name: str, body: bytes) -> dict[str, object]:
    body = body[:MAX_BODY_BYTES]
    path = output_dir / name
    path.write_bytes(body)
    return {
        "file": path.name,
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read a target's route inventory and try its advertised fields/actions."
    )
    parser.add_argument("target", help="absolute target URL returned by the current attempt")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    try:
        target = normalize_url(args.target)
        allowed_origin = origin(target)
        host = urlsplit(target).hostname or "target"
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_dir = args.output_dir or (
            Path("web-tools/evidence") / f"{host}-api-field-action-{timestamp}"
        )
        output_dir.mkdir(parents=True, exist_ok=True)

        clues_url = normalize_url(urljoin(target, "/api/clues"))
        clues_status, clues_body = get(clues_url, allowed_origin)
        if clues_status != 200:
            raise RuntimeError(f"route clues returned HTTP {clues_status}")
        clues = json.loads(clues_body.decode("utf-8"))
        if not isinstance(clues, dict):
            raise ValueError("route clues are not a JSON object")
        inventory_route = clues.get("inventory_route")
        feature_route = clues.get("feature_route")
        reference = clues.get("protected_reference")
        if not all(isinstance(value, str) and value for value in (inventory_route, feature_route)):
            raise ValueError("route clues lack inventory_route or feature_route")
        if not isinstance(reference, (str, int)):
            raise ValueError("route clues lack a protected_reference")

        inventory_url = normalize_url(urljoin(target, inventory_route))
        if origin(inventory_url) != allowed_origin:
            raise ValueError("inventory route leaves the assigned target")
        inventory_status, inventory_body = get(inventory_url, allowed_origin)
        if inventory_status != 200:
            raise RuntimeError(f"API inventory returned HTTP {inventory_status}")
        inventory = json.loads(inventory_body.decode("utf-8"))
        if not isinstance(inventory, dict):
            raise ValueError("API inventory is not a JSON object")
        fields = inventory.get("fields")
        actions = inventory.get("actions")
        if (
            not isinstance(fields, list)
            or not isinstance(actions, list)
            or not fields
            or not actions
            or len(fields) > MAX_VALUES
            or len(actions) > MAX_VALUES
            or any(not isinstance(value, str) or not value for value in fields + actions)
        ):
            raise ValueError("inventory fields/actions are missing or outside the bounded format")

        feature_url = normalize_url(urljoin(target, feature_route))
        if origin(feature_url) != allowed_origin:
            raise ValueError("feature route leaves the assigned target")
        attempts: list[dict[str, object]] = []
        proof: str | None = None
        for field in fields:
            for action in actions:
                query = urlencode({"id": str(reference), "fields": field, "action": action})
                response_url = f"{feature_url}?{query}"
                status, body = get(response_url, allowed_origin)
                body = body[:MAX_BODY_BYTES]
                record = {
                    "field": field,
                    "action": action,
                    "status": status,
                    **save_body(output_dir, f"response-{len(attempts) + 1:02d}.body", body),
                }
                attempts.append(record)
                match = PROOF_RE.search(body)
                if match:
                    proof = match.group(0).decode("ascii")
                    break
            if proof:
                break

        save_body(output_dir, "clues.body", clues_body)
        save_body(output_dir, "inventory.body", inventory_body)
        report = {
            "target": target,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "protected_reference": reference,
            "inventory": inventory,
            "attempts": attempts,
            "proof": proof,
            "request_policy": {
                "method": "GET",
                "same_origin_only": True,
                "max_field_values": MAX_VALUES,
                "max_action_values": MAX_VALUES,
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
