"""Thin HTTP client used by tool implementations.

In production this points at https://api.opengem.org. In tests it points at a
local FastAPI stub or returns canned fixtures via ``FixtureClient``.
"""

from __future__ import annotations

import os
from typing import Any, Protocol

import httpx


class APIClient(Protocol):
    """Minimal client surface used by tools."""

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]: ...


class HttpAPIClient:
    """Real HTTP client. Talks to OPENGEM_API_URL."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 15.0,
    ) -> None:
        self._base = (base_url or os.environ.get("OPENGEM_API_URL", "https://api.opengem.org")).rstrip("/")
        self._key = api_key or os.environ.get("OPENGEM_API_KEY")
        self._timeout = timeout
        self._client = httpx.Client(timeout=timeout)

    def __enter__(self) -> HttpAPIClient:
        return self

    def __exit__(self, *_: object) -> None:
        self._client.close()

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        headers = {}
        if self._key:
            headers["Authorization"] = f"Bearer {self._key}"
        resp = self._client.get(f"{self._base}{path}", params=params, headers=headers)
        resp.raise_for_status()
        body = resp.json()
        if not isinstance(body, dict):
            return {"items": body}
        return body


class FixtureClient:
    """In-memory client backed by a routes → response mapping. Used in tests."""

    def __init__(self, routes: dict[str, Any]) -> None:
        # Keys are "GET /path" or just "/path"; values are dict or list.
        self._routes = {self._norm(k): v for k, v in routes.items()}
        self.calls: list[tuple[str, dict[str, Any] | None]] = []

    @staticmethod
    def _norm(k: str) -> str:
        if k.startswith("GET "):
            k = k[4:]
        return k

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        self.calls.append((path, params))
        if path not in self._routes:
            raise KeyError(f"FixtureClient: no route configured for {path!r}")
        body = self._routes[path]
        if not isinstance(body, dict):
            return {"items": body}
        return body
