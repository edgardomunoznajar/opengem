"""Tests for AR(1) and random-walk baseline density forecasts."""

from __future__ import annotations

import math

import pytest
from opengem_backtest.baselines import ar1_density, random_walk_density


def test_random_walk_mean_is_last_value():
    hist = [1.0, 1.5, 0.5, 2.0, 1.0]
    out = random_walk_density(hist, [1, 4])
    assert out[1][0] == pytest.approx(1.0)  # mu = last
    assert out[4][0] == pytest.approx(1.0)


def test_random_walk_variance_grows_with_sqrt_h():
    hist = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0]  # diffs alternate +-1
    out = random_walk_density(hist, [1, 4])
    s1 = out[1][1]
    s4 = out[4][1]
    assert s4 == pytest.approx(s1 * math.sqrt(4), rel=1e-9)


def test_random_walk_constant_drift_zero_sigma():
    out = random_walk_density([0.0, 1.0, 2.0, 3.0, 4.0], [1])  # constant diff -> zero variance
    assert out[1][1] == pytest.approx(0.0)


def test_ar1_mean_reverts_toward_unconditional_mean():
    # mean-reverting series around 5.0
    hist = [5.0 + (-1) ** i * 1.0 for i in range(30)]
    out = ar1_density(hist, [1, 8])
    mu1, sig1 = out[1]
    mu8, _sig8 = out[8]
    assert math.isfinite(mu1) and sig1 > 0
    # longer horizon collapses toward the unconditional mean (~5.0)
    assert abs(mu8 - 5.0) <= abs(mu1 - 5.0) + 1e-9


def test_ar1_requires_min_observations():
    with pytest.raises(ValueError):
        ar1_density([1.0, 2.0], [1])
