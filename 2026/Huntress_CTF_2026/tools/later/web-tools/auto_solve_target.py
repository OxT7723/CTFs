#!/usr/bin/env python3
"""Choose a known bounded web solver from one assigned target's own clues."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from threading import Lock
from time import perf_counter
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPCookieProcessor, Request, build_opener
from http.cookiejar import CookieJar

from inspect_target import normalize_url, origin


MAX_BODY_BYTES = 2 * 1024 * 1024
USER_AGENT = "HuntressCTF-Web-Inspector/1.0"


class PageFacts(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.forms: list[dict[str, str]] = []
        self._form: dict[str, str] | None = None
        self.text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "a" and values.get("href"):
            self.links.append(str(values["href"]))
        elif tag == "form":
            self._form = {
                "action": str(values.get("action", "")),
                "method": str(values.get("method", "get")).lower(),
            }
        elif tag in {"input", "button", "textarea", "select"} and self._form is not None:
            name = str(values.get("name", ""))
            if name:
                self._form["field:" + name] = str(values.get("type", tag)).lower()

    def handle_endtag(self, tag: str) -> None:
        if tag == "form" and self._form is not None:
            self.forms.append(self._form)
            self._form = None

    def handle_data(self, data: str) -> None:
        self.text.append(data)


class Probe:
    def __init__(self, target: str):
        self.target = normalize_url(target)
        self.allowed_origin = origin(self.target)
        self.opener = build_opener(HTTPCookieProcessor(CookieJar()))
        self.timings: list[dict[str, object]] = []
        self._timing_lock = Lock()

    def get(self, route: str) -> tuple[int, bytes]:
        url = normalize_url(urljoin(self.target, route))
        if origin(url) != self.allowed_origin:
            raise ValueError(f"refusing off-origin route: {route}")
        request = Request(
            url,
            headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
            method="GET",
        )
        started = perf_counter()
        try:
            response = self.opener.open(request, timeout=12)
        except HTTPError as exc:
            response = exc
        except URLError as exc:
            raise RuntimeError(f"request failed for {route}: {exc.reason}") from exc
        body = response.read(MAX_BODY_BYTES + 1)
        elapsed_ms = round((perf_counter() - started) * 1000, 1)
        if len(body) > MAX_BODY_BYTES:
            raise RuntimeError(f"{route} exceeded the 2 MiB response limit")
        with self._timing_lock:
            self.timings.append(
                {
                    "route": route,
                    "status": int(getattr(response, "status", response.code)),
                    "elapsed_ms": elapsed_ms,
                }
            )
        return int(getattr(response, "status", response.code)), body


def dispatch_from_clues(
    clues: dict,
    page_text: str,
    secondary_document: dict | None = None,
) -> tuple[str, list[str]] | None:
    if (
        clues.get("framework") == "ASP.NET Core Blazor Server"
        and clues.get("component_route")
        and clues.get("feature_route")
    ):
        return "framework-roulette-blazor", ["solve_framework_roulette.py"]
    if (
        clues.get("request_log_route")
        and clues.get("event_json_field")
        and clues.get("worker_query_field")
        and clues.get("response_route")
    ):
        return "day31-full-stack-incident", ["solve_full_stack_incident.py"]
    if (
        clues.get("owner_directory_route")
        and clues.get("feature_route")
        and clues.get("secondary_route")
    ):
        return "day30-queue-confusion", ["solve_queue_confusion.py"]
    if (
        clues.get("current_role")
        and clues.get("identity_directory_route")
        and clues.get("feature_route")
    ):
        return "day30-pass-identity", ["solve_pass_identity.py"]
    if clues.get("current_role") and clues.get("records_owner") and clues.get("feature_route"):
        return "day30-pass-identity", ["solve_pass_identity.py"]
    if clues.get("update_feed") and clues.get("update_policy"):
        return "day29-trust-the-build", ["solve_trust_the_build.py"]
    if clues.get("topology_route") and clues.get("case_directory_route"):
        return "day29-internal-affairs", ["solve_internal_fetch.py"]
    if clues.get("policy_format_route") and clues.get("feature_route"):
        return "day28-fail-open", ["solve_day28.py", "fail-open"]
    report = secondary_document.get("report") if isinstance(secondary_document, dict) else None
    report_fields = report.get("fields") if isinstance(report, dict) else None
    if (
        isinstance(report_fields, list)
        and {"export_id", "missing_event", "observed_event"}.issubset(report_fields)
    ):
        return "day28-missing-log", ["solve_day28.py", "missing-log"]
    if clues.get("stream_reference") is not None:
        return "day27-websocket", ["solve_day27.py", "socket"]
    if clues.get("deployment") == "trusted_reverse_proxy":
        return "day27-forwarded-header", ["solve_day27.py", "forwarded"]
    if clues.get("event_type") and clues.get("owner_scope"):
        return "day26-webhook", ["solve_day26.py", "webhook"]
    if clues.get("state_format_route"):
        return "day26-serialized", ["solve_day26.py", "serialized"]
    if clues.get("recovery_guide_route"):
        return "day25-reset", ["solve_day25.py", "reset"]
    if clues.get("input_parameter") and clues.get("feature_route"):
        return "day25-shell", ["solve_day25.py", "shell"]
    if clues.get("inventory_route") and clues.get("protected_reference"):
        return "api-field-action", ["solve_api_field_action.py"]
    if clues.get("protected_reference") and clues.get("feature_route"):
        return "day25-resolver", ["solve_day25.py", "resolver"]
    if clues.get("moderator_data_route"):
        return "stored-xss", ["solve_stored_xss.py"]
    if clues.get("preview_guide") and clues.get("render_route"):
        return "upload-preview", ["solve_upload_preview.py"]
    if clues.get("preferences_route"):
        return "csrf-preferences", ["solve_csrf_preferences.py"]
    if clues.get("callback_nonce"):
        return "reflected-callback", ["solve_reflect_callback.py"]
    if clues.get("session_hint"):
        return "session-impression", ["solve_session_impression.py"]

    lowered = page_text.lower()
    if clues.get("secondary_route") and any(
        word in lowered for word in ("credit", "purchase", "spend", "spent", "ledger")
    ):
        return "day27-race-condition", ["solve_day27.py", "double-spent"]
    if clues.get("feature_route") and clues.get("secondary_route"):
        if "internal" in lowered and "fetch" in lowered:
            return "internal-fetch", ["solve_internal_fetch.py"]
        if "profile" in lowered and ("audit" in lowered or "extra field" in lowered):
            return "mass-assignment", ["solve_mass_assignment.py"]
        if "delayed" in lowered or ("query" in lowered and "later" in lowered):
            return "delayed-query", ["solve_delayed_query.py"]
    if clues.get("feature_route") and "template" in lowered:
        return "template-expression", ["solve_template_expression.py"]
    if clues.get("feature_route") and page_text:
        return "clued-route", ["solve_clued_route.py"]
    return None


def classify_unclued(root_body: bytes, robots_body: bytes) -> tuple[str, list[str]] | None:
    facts = PageFacts()
    facts.feed(root_body.decode("utf-8", errors="replace"))
    text = " ".join(facts.text).lower()
    robots = robots_body.decode("utf-8", errors="replace").lower()
    if re.search(
        r"disallow:\s*/(?:archives?|snapshots?|backups?|deploy(?:ments?)?|releases?)[^\s]*",
        robots,
    ):
        return "backup-exposure", ["solve_backup_exposure.py"]
    if (
        any(re.search(r"/api/(?:history|timeline|events?|activity)", href, re.I) for href in facts.links)
        and any(
            re.search(r"/(?:cases?|tickets?|incidents?|briefs)/\d+", href, re.I)
            for href in facts.links
        )
    ):
        return "idor", ["solve_idor.py"]
    if (
        any(re.search(r"\.php\?[^#]*\bdoc=", href, re.I) for href in facts.links)
        and ("document viewer" in text or "runbook" in text)
    ):
        return "path-traversal", ["solve_path_traversal.py"]
    if "search" in text and any(
        form["method"] == "get" and any(key.startswith("field:") for key in form)
        for form in facts.forms
    ):
        return "sqli", ["solve_sqli.py"]
    return None


def proof_from_output(stdout: str) -> str | None:
    try:
        result = json.loads(stdout)
    except json.JSONDecodeError:
        return None
    proof = result.get("proof")
    if isinstance(proof, str):
        return proof
    for item in result.get("proofs", []):
        if isinstance(item, dict) and isinstance(item.get("answer"), str):
            return item["answer"]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="exact target URL returned by the current attempt")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    try:
        target = normalize_url(args.target)
        host = urlsplit(target).hostname or "target"
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_dir = args.output_dir or (
            Path("web-tools/evidence") / f"{host}-auto-{timestamp}"
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        total_started = perf_counter()
        probe = Probe(target)

        clues_status, clues_body = probe.get("/api/clues")
        clues: dict = {}
        secondary_document: dict | None = None
        root_body = b""
        page_text = ""
        if clues_status == 200:
            try:
                value = json.loads(clues_body.decode("utf-8"))
                if isinstance(value, dict):
                    clues = value
            except (UnicodeDecodeError, json.JSONDecodeError):
                pass

        if clues.get("error") == "session_required":
            _, root_body = probe.get("/")
            clues_status, clues_body = probe.get("/api/clues")
            try:
                value = json.loads(clues_body.decode("utf-8"))
                if isinstance(value, dict):
                    clues = value
            except (UnicodeDecodeError, json.JSONDecodeError):
                clues = {}

        secondary_route = clues.get("secondary_route")
        if isinstance(secondary_route, str):
            try:
                secondary_status, secondary_body = probe.get(secondary_route)
                if secondary_status == 200:
                    value = json.loads(secondary_body.decode("utf-8"))
                    if isinstance(value, dict):
                        secondary_document = value
            except (RuntimeError, UnicodeDecodeError, json.JSONDecodeError):
                secondary_document = None

        if clues:
            selected = dispatch_from_clues(clues, page_text, secondary_document)
            if selected is None and (
                clues.get("secondary_route")
                or (clues.get("feature_route") and not clues.get("callback_nonce"))
            ):
                if not root_body:
                    _, root_body = probe.get("/")
                facts = PageFacts()
                facts.feed(root_body.decode("utf-8", errors="replace"))
                page_text = " ".join(facts.text)
                selected = dispatch_from_clues(clues, page_text, secondary_document)
        else:
            selected = None

        if selected is None:
            if not root_body:
                with ThreadPoolExecutor(max_workers=2) as pool:
                    root_future = pool.submit(probe.get, "/")
                    robots_future = pool.submit(probe.get, "/robots.txt")
                    _, root_body = root_future.result()
                    _, robots_body = robots_future.result()
            else:
                _, robots_body = probe.get("/robots.txt")
            selected = classify_unclued(root_body, robots_body)

        discovery_elapsed_ms = round((perf_counter() - total_started) * 1000, 1)
        if selected is None:
            print(
                json.dumps(
                    {
                        "error": "no known solver matched this target",
                        "clues_status": clues_status,
                        "clues": clues,
                        "next_step": "inspect the assigned target and extend the dispatcher",
                    },
                    indent=2,
                ),
                file=sys.stderr,
            )
            return 2

        technique, command = selected
        solver_path = Path(__file__).resolve().parent / command[0]
        child_args = [sys.executable, str(solver_path), *command[1:], target]
        if technique == "framework-roulette-blazor":
            child_args.extend(["--clues-json", json.dumps(clues)])
        if technique in {
            "backup-exposure",
            "idor",
            "sqli",
            "api-field-action",
            "upload-preview",
            "csrf-preferences",
            "day27-websocket",
            "day27-forwarded-header",
            "day27-race-condition",
            "day28-fail-open",
            "day28-missing-log",
            "day29-trust-the-build",
            "day29-internal-affairs",
            "day30-pass-identity",
            "day30-queue-confusion",
            "framework-roulette-blazor",
            "day31-full-stack-incident",
            "path-traversal",
        }:
            child_args.extend(["--output-dir", str(output_dir / technique)])
        solver_started = perf_counter()
        completed = subprocess.run(
            child_args,
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if completed.returncode != 0:
            if completed.stdout:
                print(completed.stdout, end="")
            if completed.stderr:
                print(completed.stderr, end="", file=sys.stderr)
            return completed.returncode
        proof = proof_from_output(completed.stdout)
        if proof is None:
            print(completed.stdout, end="")
            print(
                json.dumps({"error": "selected solver returned no proof", "technique": technique}),
                file=sys.stderr,
            )
            return 1
        solver_elapsed_ms = round((perf_counter() - solver_started) * 1000, 1)
        print(
            json.dumps(
                {
                    "proof": proof,
                    "technique": technique,
                    "solver_output": json.loads(completed.stdout),
                    "discovery_elapsed_ms": discovery_elapsed_ms,
                    "solver_elapsed_ms": solver_elapsed_ms,
                    "elapsed_ms": round((perf_counter() - total_started) * 1000, 1),
                    "discovery_requests": probe.timings,
                },
                indent=2,
            )
        )
        return 0
    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
