from __future__ import annotations

import sys

import pytest


@pytest.fixture(autouse=True)
def _no_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    retry_mod = sys.modules.get("opengem_data_base.retry")
    if retry_mod is None:
        import opengem_data_base.retry as retry_mod
    monkeypatch.setattr(retry_mod.time, "sleep", lambda _s: None)
    monkeypatch.setattr(retry_mod.random, "uniform", lambda _a, _b: 0.0)
