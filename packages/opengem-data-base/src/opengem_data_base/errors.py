"""Adapter error taxonomy.

All adapters raise from this hierarchy so callers can handle uniformly.
"""

from __future__ import annotations


class AdapterError(Exception):
    """Base class for all adapter errors."""

    def __init__(self, message: str, *, source_id: str | None = None) -> None:
        super().__init__(message)
        self.source_id = source_id


class AuthError(AdapterError):
    """Authentication failed: missing or invalid API key, expired token, etc."""


class RateLimitError(AdapterError):
    """Source rate-limit exceeded. Caller should back off."""

    def __init__(
        self,
        message: str,
        *,
        source_id: str | None = None,
        retry_after_seconds: float | None = None,
    ) -> None:
        super().__init__(message, source_id=source_id)
        self.retry_after_seconds = retry_after_seconds


class OutageError(AdapterError):
    """Source returned 5xx or is otherwise unavailable."""


class SchemaError(AdapterError):
    """Source response did not match expected schema. Indicates source-side change."""


class NotFoundError(AdapterError):
    """Requested series or resource not found at source."""
