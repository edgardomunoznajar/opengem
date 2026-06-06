"""Exponential-backoff retry decorator with jitter."""

from __future__ import annotations

import logging
import random
import time
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

from opengem_data_base.errors import OutageError, RateLimitError

P = ParamSpec("P")
T = TypeVar("T")

_log = logging.getLogger(__name__)


def retry(
    *,
    max_attempts: int = 4,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    jitter: float = 0.5,
    retry_on: tuple[type[BaseException], ...] = (OutageError, RateLimitError),
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator that retries a function on transient errors with exponential backoff.

    Uses `retry_after_seconds` from `RateLimitError` when present.
    """

    def decorator(fn: Callable[P, T]) -> Callable[P, T]:
        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            last_exc: BaseException | None = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except retry_on as e:
                    last_exc = e
                    if attempt == max_attempts:
                        break
                    if isinstance(e, RateLimitError) and e.retry_after_seconds is not None:
                        delay = min(e.retry_after_seconds, max_delay)
                    else:
                        delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                    delay = delay + random.uniform(0, jitter)
                    _log.warning(
                        "retry: %s attempt %d/%d after %.2fs (%s)",
                        fn.__name__,
                        attempt,
                        max_attempts,
                        delay,
                        type(e).__name__,
                    )
                    time.sleep(delay)
            assert last_exc is not None
            raise last_exc

        return wrapper

    return decorator
