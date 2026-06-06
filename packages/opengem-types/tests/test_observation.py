from __future__ import annotations

from datetime import date

import pytest

from opengem_types import Observation, SeriesId


def _sid() -> SeriesId:
    return SeriesId("US.BEA.NIPA.GDP_real.Q")


def test_observation_construction() -> None:
    obs = Observation(
        series_id=_sid(),
        observed_at=date(2026, 1, 1),
        vintage_at=date(2026, 4, 28),
        value=23500.123,
        source="BEA",
    )
    assert obs.value == 23500.123
    assert obs.revision_lag_days == (date(2026, 4, 28) - date(2026, 1, 1)).days


def test_observation_value_none_allowed() -> None:
    obs = Observation(
        series_id=_sid(),
        observed_at=date(2026, 4, 1),
        vintage_at=date(2026, 4, 28),
        value=None,
        source="BEA",
    )
    assert obs.value is None


def test_observation_vintage_before_observed_rejected() -> None:
    with pytest.raises(ValueError, match="vintage_at .* must be >= observed_at"):
        Observation(
            series_id=_sid(),
            observed_at=date(2026, 5, 1),
            vintage_at=date(2026, 4, 28),
            value=1.0,
            source="BEA",
        )


def test_observation_is_frozen() -> None:
    obs = Observation(
        series_id=_sid(),
        observed_at=date(2026, 1, 1),
        vintage_at=date(2026, 4, 28),
        value=1.0,
        source="BEA",
    )
    with pytest.raises(Exception):  # FrozenInstanceError
        obs.value = 2.0  # type: ignore[misc]
