from __future__ import annotations

from datetime import date, datetime

import pytest
from opengem_types import (
    Country,
    DensityForecast,
    Forecast,
    ForecastQuantiles,
    RunProvenance,
    Variable,
)


def test_forecast_quantiles_monotone() -> None:
    q = ForecastQuantiles(p10=0.1, p25=0.15, p50=0.2, p75=0.25, p90=0.3)
    assert q.p50 == 0.2


def test_forecast_quantiles_non_monotone_rejected() -> None:
    with pytest.raises(ValueError, match="monotone"):
        ForecastQuantiles(p10=0.3, p25=0.2, p50=0.1, p75=0.05, p90=0.0)


def test_density_forecast_construction() -> None:
    df = DensityForecast(
        run_id="20260524-abc123",
        country=Country.US,
        variable=Variable.GDP_REAL,
        horizon_q=4,
        forecast_for_period=date(2027, 7, 1),
        quantiles=ForecastQuantiles(p10=0.012, p25=0.018, p50=0.024, p75=0.030, p90=0.038),
        variant_weights={"v1_dfm": 0.42, "v2_ml": 0.35, "v3_bvar": 0.23},
    )
    assert df.density_type == "mixture"
    assert sum(df.variant_weights.values()) == pytest.approx(1.0)


def test_run_provenance_validates_hashes() -> None:
    p = RunProvenance(
        run_id="20260524-abc123",
        code_sha="git:abc123" + "0" * 32,
        vintage_hash="sha256:" + "0" * 64,
        prior_hash="sha256:" + "1" * 64,
        posterior_hash="sha256:" + "2" * 64,
        started_at=datetime(2026, 5, 24, 6, 0, 0),
        completed_at=datetime(2026, 5, 24, 6, 30, 0),
    )
    assert p.superseded_by is None


def test_run_provenance_rejects_unprefixed_hash() -> None:
    with pytest.raises(ValueError, match="sha256"):
        RunProvenance(
            run_id="r",
            code_sha="x",
            vintage_hash="abc",  # missing prefix
            prior_hash="sha256:" + "1" * 64,
            posterior_hash="sha256:" + "2" * 64,
            started_at=datetime(2026, 5, 24),
            completed_at=datetime(2026, 5, 24),
        )


def test_forecast_basic() -> None:
    f = Forecast(
        run_id="r1",
        country=Country.US,
        variable=Variable.GDP_REAL,
        horizon_q=1,
        forecast_for_period=date(2026, 7, 1),
        value=0.022,
    )
    assert f.horizon_q == 1
