"""Forecast scoring metrics.

CRPS (Continuous Ranked Probability Score) is the primary metric for density
forecasts — lower is better. We provide two forms:

* ``crps_gaussian`` — exact closed form for a Normal predictive distribution.
* ``crps_from_quantiles`` — the model-agnostic V&V form: the quantile
  decomposition ``CRPS = 2 ∫_0^1 QL_τ(y, q_τ) dτ`` evaluated numerically over a
  fine τ-grid, with the predictive quantile function reconstructed by
  piecewise-linear interpolation (and linear tail extrapolation) of the five
  reported quantiles. On a dense quantile set this converges to the closed form.

MAE/RMSE are point metrics; PIT (probability integral transform) is the
calibration input — under a well-calibrated density the PIT values are U[0, 1].
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence

import numpy as np
from scipy.stats import norm

# The five canonical quantile levels OPENGEM reports.
QUANTILE_LEVELS: tuple[float, ...] = (0.10, 0.25, 0.50, 0.75, 0.90)


def crps_gaussian(mu: float, sigma: float, actual: float) -> float:
    """Exact CRPS of N(mu, sigma^2) evaluated at ``actual``.

    Degenerates to absolute error when sigma <= 0 (a point forecast).
    """
    if not math.isfinite(sigma) or sigma <= 0:
        return abs(actual - mu)
    omega = (actual - mu) / sigma
    return float(sigma * (omega * (2.0 * norm.cdf(omega) - 1.0) + 2.0 * norm.pdf(omega) - 1.0 / math.sqrt(math.pi)))


def _quantile_function(
    levels: Sequence[float], values: Sequence[float], grid: np.ndarray
) -> np.ndarray:
    """Reconstruct Q(τ) on ``grid`` by linear interp + linear tail extrapolation."""
    lv = np.asarray(levels, dtype=float)
    qv = np.asarray(values, dtype=float)
    # Extrapolate to τ=0 and τ=1 using the end slopes so tails aren't clamped flat.
    slope_lo = (qv[1] - qv[0]) / (lv[1] - lv[0])
    slope_hi = (qv[-1] - qv[-2]) / (lv[-1] - lv[-2])
    q_at_0 = qv[0] - slope_lo * lv[0]
    q_at_1 = qv[-1] + slope_hi * (1.0 - lv[-1])
    full_lv = np.concatenate(([0.0], lv, [1.0]))
    full_qv = np.concatenate(([q_at_0], qv, [q_at_1]))
    return np.interp(grid, full_lv, full_qv)


def crps_from_quantiles(
    quantiles: Mapping[float, float], actual: float, n_grid: int = 1000
) -> float:
    """CRPS via the quantile-loss integral, from a sparse set of reported quantiles.

    ``quantiles`` maps level (e.g. 0.1) to predicted value. Uses
    ``CRPS = 2 ∫_0^1 QL_τ dτ`` with QL the pinball loss.
    """
    levels = sorted(quantiles)
    values = [quantiles[lv] for lv in levels]
    if len(levels) < 2:
        raise ValueError("need at least two quantiles")
    # midpoint grid over (0, 1) avoids the degenerate τ=0,1 endpoints
    grid = (np.arange(n_grid) + 0.5) / n_grid
    q = _quantile_function(levels, values, grid)
    diff = actual - q
    # pinball loss: τ*diff if diff>=0 else (τ-1)*diff
    pinball = np.where(diff >= 0, grid * diff, (grid - 1.0) * diff)
    return float(2.0 * pinball.mean())


def gaussian_quantiles(
    mu: float, sigma: float, levels: Sequence[float] = QUANTILE_LEVELS
) -> dict[float, float]:
    """The five reported quantiles of N(mu, sigma^2). Degenerate if sigma <= 0."""
    if not math.isfinite(sigma) or sigma <= 0:
        return {float(lv): float(mu) for lv in levels}
    return {float(lv): float(mu + sigma * norm.ppf(lv)) for lv in levels}


def pit_value(quantiles: Mapping[float, float], actual: float) -> float:
    """Probability integral transform: the predictive CDF evaluated at ``actual``.

    Inverts the quantile function by linear interpolation. Clamped to [0, 1].
    """
    levels = sorted(quantiles)
    values = [quantiles[lv] for lv in levels]
    lv = np.asarray(levels, dtype=float)
    qv = np.asarray(values, dtype=float)
    slope_lo = (qv[1] - qv[0]) / (lv[1] - lv[0])
    slope_hi = (qv[-1] - qv[-2]) / (lv[-1] - lv[-2])
    q_at_0 = qv[0] - slope_lo * lv[0]
    q_at_1 = qv[-1] + slope_hi * (1.0 - lv[-1])
    full_lv = np.concatenate(([0.0], lv, [1.0]))
    full_qv = np.concatenate(([q_at_0], qv, [q_at_1]))
    # invert: find τ such that Q(τ) = actual
    pit = float(np.interp(actual, full_qv, full_lv))
    return min(1.0, max(0.0, pit))


def mae(points: Sequence[float], actuals: Sequence[float]) -> float:
    """Mean absolute error."""
    p = np.asarray(points, dtype=float)
    a = np.asarray(actuals, dtype=float)
    if p.size == 0:
        raise ValueError("empty input")
    return float(np.mean(np.abs(p - a)))


def rmse(points: Sequence[float], actuals: Sequence[float]) -> float:
    """Root mean squared error."""
    p = np.asarray(points, dtype=float)
    a = np.asarray(actuals, dtype=float)
    if p.size == 0:
        raise ValueError("empty input")
    return float(np.sqrt(np.mean((p - a) ** 2)))
