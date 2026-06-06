"""Tests for CRPS / PIT / MAE / RMSE."""

from __future__ import annotations

import math

import pytest
from opengem_backtest.metrics import (
    QUANTILE_LEVELS,
    crps_from_quantiles,
    crps_gaussian,
    gaussian_quantiles,
    mae,
    pit_value,
    rmse,
)
from scipy.stats import norm

# Closed-form CRPS of N(0,1) at 0: 2*phi(0) - 1/sqrt(pi)
CRPS_STD_NORMAL_AT_0 = 2.0 * norm.pdf(0.0) - 1.0 / math.sqrt(math.pi)  # ~0.233695


def test_crps_gaussian_known_value():
    assert crps_gaussian(0.0, 1.0, 0.0) == pytest.approx(CRPS_STD_NORMAL_AT_0, abs=1e-9)


def test_crps_gaussian_degenerate_is_abs_error():
    assert crps_gaussian(2.0, 0.0, 5.0) == pytest.approx(3.0)


def test_crps_from_quantiles_converges_to_gaussian():
    # 99 quantiles of N(0,1) -> quantile-integral CRPS approaches the closed form
    levels = [i / 100 for i in range(1, 100)]
    q = {lv: float(norm.ppf(lv)) for lv in levels}
    assert crps_from_quantiles(q, 0.0) == pytest.approx(CRPS_STD_NORMAL_AT_0, abs=1e-2)


def test_crps_from_five_quantiles_is_reasonable():
    q = gaussian_quantiles(0.0, 1.0)
    val = crps_from_quantiles(q, 0.0)
    # coarse 5-point reconstruction: within ~25% of the truth, and positive
    assert val > 0
    assert abs(val - CRPS_STD_NORMAL_AT_0) < 0.25 * CRPS_STD_NORMAL_AT_0


def test_crps_perfect_forecast_is_zero():
    q = {0.1: 4.0, 0.25: 4.0, 0.5: 4.0, 0.75: 4.0, 0.9: 4.0}
    assert crps_from_quantiles(q, 4.0) == pytest.approx(0.0, abs=1e-9)


def test_crps_lower_when_centered_on_actual():
    centered = crps_from_quantiles(gaussian_quantiles(2.0, 1.0), 2.0)
    off = crps_from_quantiles(gaussian_quantiles(2.0, 1.0), 6.0)
    assert centered < off


def test_gaussian_quantiles_monotone_and_centered():
    q = gaussian_quantiles(3.0, 2.0)
    assert q[0.5] == pytest.approx(3.0)
    vals = [q[lv] for lv in QUANTILE_LEVELS]
    assert vals == sorted(vals)


def test_pit_value_at_median_is_half():
    q = gaussian_quantiles(0.0, 1.0)
    assert pit_value(q, 0.0) == pytest.approx(0.5, abs=1e-6)


def test_pit_value_below_p10_is_small():
    q = gaussian_quantiles(0.0, 1.0)
    assert pit_value(q, -5.0) < 0.10


def test_mae_rmse_basic():
    assert mae([1.0, 2.0, 3.0], [1.0, 2.0, 0.0]) == pytest.approx(1.0)
    assert rmse([0.0, 0.0], [3.0, 4.0]) == pytest.approx(math.sqrt((9 + 16) / 2))
