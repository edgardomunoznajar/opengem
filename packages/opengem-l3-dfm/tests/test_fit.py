"""Tests for opengem-l3-dfm.

We test the boundary code (config validation, quantile derivation, horizon
arithmetic) deterministically. The integration test fits an actual DFM on a
small synthetic panel; it's slow but proves the wrapper works against the real
statsmodels implementation.
"""

from __future__ import annotations

import math
from datetime import date

import pytest
from opengem_l3_dfm import DFMConfig
from opengem_l3_dfm.fit import (
    _add_quarters,
    _normal_quantiles,
    _run_id,
)

# ----------------- DFMConfig validation ---------------------------------


def test_dfmconfig_defaults_validate():
    cfg = DFMConfig(country="US", target="gdp_yoy")
    assert cfg.factors == 2
    assert cfg.horizons_q == (1, 4, 8, 20)


def test_dfmconfig_rejects_bad_country():
    # Country is the canonical opengem_types.Country (ISO-2). The ISO-3 "USA"
    # is NOT a valid member and must be rejected — DensityForecast.country is
    # typed as Country, so the whole pipeline uses the alpha-2 roster.
    with pytest.raises(ValueError):
        DFMConfig(country="USA", target="gdp_yoy")


def test_dfmconfig_rejects_bad_factors():
    with pytest.raises(ValueError):
        DFMConfig(country="US", target="gdp_yoy", factors=0)


def test_dfmconfig_rejects_empty_horizons():
    with pytest.raises(ValueError):
        DFMConfig(country="US", target="gdp_yoy", horizons_q=())


def test_dfmconfig_rejects_negative_horizons():
    with pytest.raises(ValueError):
        DFMConfig(country="US", target="gdp_yoy", horizons_q=(1, -1))


# ----------------- _normal_quantiles -----------------------------------


def test_normal_quantiles_basic():
    q = _normal_quantiles(mu=2.0, se=1.0)
    assert q.p50 == 2.0
    # P10 < P25 < P50 < P75 < P90, ~1.28 SE apart at tails
    assert q.p10 < q.p25 < q.p50 < q.p75 < q.p90
    assert abs((q.p90 - q.p10) - 2 * 1.2816) < 1e-6


def test_normal_quantiles_zero_se_degenerate():
    q = _normal_quantiles(mu=3.14, se=0.0)
    assert q.p10 == q.p25 == q.p50 == q.p75 == q.p90 == 3.14


def test_normal_quantiles_nan_se_degenerate():
    q = _normal_quantiles(mu=1.0, se=math.nan)
    assert q.p50 == 1.0


# ----------------- _add_quarters ---------------------------------------


def test_add_quarters_within_year():
    assert _add_quarters(date(2026, 3, 28), 1).month == 6
    assert _add_quarters(date(2026, 3, 28), 1).year == 2026


def test_add_quarters_across_year():
    d = _add_quarters(date(2026, 12, 28), 1)
    assert (d.year, d.month) == (2027, 3)


def test_add_quarters_multi_year():
    d = _add_quarters(date(2026, 3, 28), 8)  # +2 years
    assert (d.year, d.month) == (2028, 3)


# ----------------- _run_id stability -----------------------------------


def test_run_id_stable():
    cfg = DFMConfig(country="US", target="gdp_yoy")
    a = _run_id(cfg, (100, 5), "0.14.4")
    b = _run_id(cfg, (100, 5), "0.14.4")
    assert a == b


def test_run_id_changes_with_shape():
    cfg = DFMConfig(country="US", target="gdp_yoy")
    assert _run_id(cfg, (100, 5), "0.14.4") != _run_id(cfg, (101, 5), "0.14.4")


def test_run_id_changes_with_version():
    cfg = DFMConfig(country="US", target="gdp_yoy")
    assert _run_id(cfg, (100, 5), "0.14.4") != _run_id(cfg, (100, 5), "0.15.0")


def test_run_id_changes_with_config():
    cfg_a = DFMConfig(country="US", target="gdp_yoy")
    cfg_b = DFMConfig(country="US", target="gdp_yoy", factors=3)
    assert _run_id(cfg_a, (100, 5), "0.14.4") != _run_id(cfg_b, (100, 5), "0.14.4")


# ----------------- Integration test ------------------------------------


@pytest.mark.integration
def test_fit_dfm_on_synthetic_panel():
    """End-to-end: fit a real DFM on a small synthetic panel.

    Slow because it imports + fits statsmodels DynamicFactorMQ. Skipped by
    default; run with `pytest -m integration`.
    """
    np = pytest.importorskip("numpy")
    pd = pytest.importorskip("pandas")
    pytest.importorskip("statsmodels")

    from opengem_l3_dfm.fit import fit_dfm

    # 80 quarterly observations of two correlated series.
    rng = np.random.default_rng(42)
    n = 80
    factor = np.cumsum(rng.normal(0, 0.3, n))
    y = factor + rng.normal(0, 0.5, n)
    x = 0.7 * factor + rng.normal(0, 0.5, n)
    idx = pd.period_range("2005Q1", periods=n, freq="Q")
    panel = pd.DataFrame({"gdp_yoy": y, "cpi_yoy": x}, index=idx)

    cfg = DFMConfig(country="US", target="gdp_yoy", factors=1, horizons_q=(1, 4))
    out = fit_dfm(panel, cfg, base_period=date(2024, 12, 31))

    assert len(out) == 2
    assert {f.horizon_q for f in out} == {1, 4}
    for f in out:
        assert f.country == "US"
        assert f.variable == "gdp_yoy"
        assert math.isfinite(f.quantiles.p50)
        assert f.quantiles.p10 < f.quantiles.p90
