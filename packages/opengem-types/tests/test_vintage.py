from __future__ import annotations

from datetime import date, datetime

from opengem_types import Observation, SeriesId, VintageSnapshot


def _obs(sid: str, observed: date, vintage: date, value: float | None) -> Observation:
    return Observation(
        series_id=SeriesId(sid),
        observed_at=observed,
        vintage_at=vintage,
        value=value,
        source="BEA",
    )


def test_vintage_hash_deterministic() -> None:
    obs = [
        _obs("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1), date(2026, 4, 28), 23500.123),
        _obs("US.BEA.NIPA.GDP_real.Q", date(2025, 10, 1), date(2026, 1, 30), 23200.5),
    ]
    snap1 = VintageSnapshot.from_observations(obs, "BEA", datetime(2026, 4, 28, 14, 0, 0))
    snap2 = VintageSnapshot.from_observations(
        list(reversed(obs)), "BEA", datetime(2026, 4, 28, 14, 0, 0)
    )
    assert snap1.vintage_hash == snap2.vintage_hash
    assert snap1.observation_count == 2
    assert snap1.series_count == 1


def test_vintage_hash_changes_on_value_change() -> None:
    obs_a = [_obs("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1), date(2026, 4, 28), 100.0)]
    obs_b = [_obs("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1), date(2026, 4, 28), 100.0001)]
    h_a = VintageSnapshot.from_observations(obs_a, "BEA", datetime(2026, 4, 28)).vintage_hash
    h_b = VintageSnapshot.from_observations(obs_b, "BEA", datetime(2026, 4, 28)).vintage_hash
    assert h_a != h_b


def test_vintage_hash_handles_none() -> None:
    obs = [_obs("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1), date(2026, 4, 28), None)]
    snap = VintageSnapshot.from_observations(obs, "BEA", datetime(2026, 4, 28))
    assert snap.vintage_hash.startswith("sha256:")
    assert snap.observation_count == 1


def test_vintage_manifest_counts_per_series() -> None:
    obs = [
        _obs("US.BEA.NIPA.GDP_real.Q", date(2026, 1, 1), date(2026, 4, 28), 100.0),
        _obs("US.BEA.NIPA.GDP_real.Q", date(2025, 10, 1), date(2026, 1, 30), 99.0),
        _obs("US.BLS.CPI.headline.M", date(2026, 4, 1), date(2026, 5, 12), 305.7),
    ]
    snap = VintageSnapshot.from_observations(obs, "MIXED", datetime(2026, 5, 13))
    assert snap.manifest["US.BEA.NIPA.GDP_real.Q"] == 2
    assert snap.manifest["US.BLS.CPI.headline.M"] == 1
    assert snap.series_count == 2
