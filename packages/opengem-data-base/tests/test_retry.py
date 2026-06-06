from __future__ import annotations

import pytest
from opengem_data_base import OutageError, RateLimitError, retry


def test_retry_passes_through_on_success() -> None:
    calls = []

    @retry(max_attempts=3, base_delay=0.0, jitter=0.0)
    def fn() -> int:
        calls.append(1)
        return 42

    assert fn() == 42
    assert len(calls) == 1


def test_retry_succeeds_after_one_outage() -> None:
    calls = []

    @retry(max_attempts=3, base_delay=0.0, jitter=0.0)
    def fn() -> int:
        calls.append(1)
        if len(calls) == 1:
            raise OutageError("transient", source_id="TEST")
        return 42

    assert fn() == 42
    assert len(calls) == 2


def test_retry_raises_after_max_attempts() -> None:
    calls = []

    @retry(max_attempts=2, base_delay=0.0, jitter=0.0)
    def fn() -> int:
        calls.append(1)
        raise OutageError("always", source_id="TEST")

    with pytest.raises(OutageError):
        fn()
    assert len(calls) == 2


def test_retry_does_not_retry_non_listed_exception() -> None:
    calls = []

    @retry(max_attempts=3, base_delay=0.0, jitter=0.0)
    def fn() -> int:
        calls.append(1)
        raise ValueError("boom")

    with pytest.raises(ValueError):
        fn()
    assert len(calls) == 1


def test_retry_respects_rate_limit_retry_after(monkeypatch: pytest.MonkeyPatch) -> None:
    """If RateLimitError carries retry_after_seconds, use it (capped at max_delay)."""
    sleeps: list[float] = []

    def fake_sleep(s: float) -> None:
        sleeps.append(s)

    import sys

    retry_mod = sys.modules["opengem_data_base.retry"]

    monkeypatch.setattr(retry_mod.time, "sleep", fake_sleep)
    monkeypatch.setattr(retry_mod.random, "uniform", lambda a, b: 0.0)

    calls = []

    @retry(max_attempts=2, base_delay=10.0, max_delay=100.0, jitter=0.0)
    def fn() -> int:
        calls.append(1)
        if len(calls) == 1:
            raise RateLimitError("slow down", source_id="TEST", retry_after_seconds=2.5)
        return 7

    assert fn() == 7
    # First attempt failed, then we slept 2.5s (retry_after), not 10s base
    assert sleeps == [2.5]
