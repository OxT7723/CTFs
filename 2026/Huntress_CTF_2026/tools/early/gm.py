"""Small read-only client for the public Huntress Game Master API.

Gameplay mutations are intentionally not exposed here. Sync only needs GET
operations, so it cannot accidentally start, retry, or submit an attempt.
"""
from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


DEFAULT_BASE_URL = "https://2026.huntress.ctf.games/"


class GameMasterError(RuntimeError):
    """A request failed without including credentials in its message."""


class GameMasterClient:
    def __init__(self, base_url: str = DEFAULT_BASE_URL, timeout: float = 20.0):
        self.base_url = base_url
        self.timeout = timeout
        self.token = os.environ.get("HUNTRESS_GM_TOKEN")
        if not self.token:
            raise GameMasterError("HUNTRESS_GM_TOKEN is missing or empty.")

    def _get(self, params: dict[str, Any]) -> tuple[Any, int]:
        url = self.base_url + "?" + urlencode(params)
        request = Request(url, headers={
            "Authorization": "Bearer " + self.token,
            "Accept": "application/json",
        })
        try:
            with urlopen(request, timeout=self.timeout) as response:
                status = response.status
                body = response.read()
        except HTTPError as exc:
            status = exc.code
            body = exc.read()
        except (URLError, TimeoutError, OSError) as exc:
            raise GameMasterError(f"Game Master GET failed: {type(exc).__name__}.") from None
        try:
            data = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise GameMasterError(f"Game Master returned non-JSON data (HTTP {status}).") from None
        if status >= 400 and status != 409:
            # Never echo server-supplied strings that might contain request data.
            raise GameMasterError(f"Game Master request failed (HTTP {status}).")
        return data, status

    def openapi(self) -> dict[str, Any]:
        data, _ = self._get({"op": "openapi"})
        return data

    def list_challenges(self, *, day: int | None = None, lane: str | None = None,
                        all_released: bool = True) -> dict[str, Any]:
        params: dict[str, Any] = {"op": "list"}
        if day is not None:
            params["day"] = day
        if lane is not None:
            params["lane"] = lane
        if all_released and day is None:
            params["all"] = "true"
        data, _ = self._get(params)
        if not isinstance(data, dict) or not isinstance(data.get("challenges"), list):
            raise GameMasterError("Game Master list response has no challenges array.")
        return data

    def status(self, challenge_id: str) -> tuple[dict[str, Any], int]:
        """Read existing attempt status; HTTP 409 is returned as data/status."""
        data, status = self._get({"op": "status", "challenge": challenge_id})
        if not isinstance(data, dict):
            raise GameMasterError("Game Master status response is not a JSON object.")
        return data, status
