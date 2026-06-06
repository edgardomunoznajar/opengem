from __future__ import annotations

from collections.abc import Iterator
from datetime import date

import pytest

from opengem_types import Observation, SeriesId

from opengem_data_base import Adapter, SeriesCatalog


class _FakeAdapter(Adapter):
    source_id = "FAKE"
    catalog = SeriesCatalog(
        {
            SeriesId("US.FAKE.X.Q"): "src-x",
            SeriesId("US.FAKE.Y.Q"): "src-y",
        }
    )

    def pull_series(self, opengem_series_id: SeriesId) -> Iterator[Observation]:
        yield Observation(
            series_id=opengem_series_id,
            observed_at=date(2026, 1, 1),
            vintage_at=date(2026, 4, 28),
            value=42.0,
            source=self.source_id,
        )


def test_concrete_adapter_pull_series() -> None:
    a = _FakeAdapter()
    obs = list(a.pull_series(SeriesId("US.FAKE.X.Q")))
    assert len(obs) == 1
    assert obs[0].value == 42.0


def test_concrete_adapter_pull_release_iterates_catalog() -> None:
    a = _FakeAdapter()
    obs = list(a.pull_release())
    assert len(obs) == 2
    series_ids = {str(o.series_id) for o in obs}
    assert series_ids == {"US.FAKE.X.Q", "US.FAKE.Y.Q"}


def test_instantiation_without_source_id_rejected() -> None:
    class _NoSource(Adapter):
        def pull_series(self, opengem_series_id: SeriesId) -> Iterator[Observation]:
            yield from ()

    with pytest.raises(TypeError, match="source_id"):
        _NoSource()


def test_health_check_default_true() -> None:
    assert _FakeAdapter().health_check() is True
