"""Baseline forecasters — the bars every real model must clear.

Both return a Normal predictive distribution per horizon as ``(mu, sigma)``:

* **AR(1)** — ``y_t = c + φ·y_{t-1} + ε`` fit by OLS. The h-step mean iterates
  the recursion; the h-step variance is ``σ_ε² · Σ_{k<h} φ^{2k}``.
* **Random walk** (no drift) — h-step mean is the last value; h-step variance is
  ``h · σ_Δ²`` where ``σ_Δ`` is the std of first differences.

These are the canonical CRPS benchmarks in the V&V matrix ("beat AR(1) and RW").
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def _ols_ar1(y: np.ndarray) -> tuple[float, float, float]:
    """OLS fit of an AR(1); returns (intercept, phi, residual_sigma)."""
    y0 = y[:-1]
    y1 = y[1:]
    design = np.column_stack([np.ones_like(y0), y0])
    beta, *_ = np.linalg.lstsq(design, y1, rcond=None)
    c, phi = float(beta[0]), float(beta[1])
    resid = y1 - design @ beta
    dof = max(1, resid.size - 2)
    sigma = float(np.sqrt(np.sum(resid**2) / dof))
    return c, phi, sigma


def ar1_density(history: Sequence[float], horizons: Sequence[int]) -> dict[int, tuple[float, float]]:
    """AR(1) (mu, sigma) per horizon, fit on ``history``."""
    y = np.asarray(history, dtype=float)
    if y.size < 3:
        raise ValueError("AR(1) needs at least 3 observations")
    c, phi, sigma_eps = _ols_ar1(y)
    last = float(y[-1])
    out: dict[int, tuple[float, float]] = {}
    for h in horizons:
        mu = last
        for _ in range(h):
            mu = c + phi * mu
        if abs(phi) < 1.0:
            var = sigma_eps**2 * (1.0 - phi ** (2 * h)) / (1.0 - phi**2)
        else:
            var = sigma_eps**2 * h
        out[h] = (float(mu), float(np.sqrt(max(var, 0.0))))
    return out


def random_walk_density(
    history: Sequence[float], horizons: Sequence[int]
) -> dict[int, tuple[float, float]]:
    """Random-walk (no drift) (mu, sigma) per horizon, fit on ``history``."""
    y = np.asarray(history, dtype=float)
    if y.size < 2:
        raise ValueError("random walk needs at least 2 observations")
    diffs = np.diff(y)
    sigma = float(np.std(diffs, ddof=1)) if diffs.size > 1 else 0.0
    last = float(y[-1])
    return {h: (last, float(np.sqrt(h)) * sigma) for h in horizons}
