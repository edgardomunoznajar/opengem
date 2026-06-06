"""POLECAT adapter tests — fixture-driven, no network."""

from __future__ import annotations

from datetime import date

import httpx
import pytest

from opengem_types import SeriesId

from opengem_data_polecat import POLECATAdapter, POLECAT_CATALOG, POLECAT_COUNTRIES
from opengem_data_polecat.adapter import _aggregate, _normalize_iso


# A minimal POLECAT-shaped TSV fixture.
_FIXTURE_TSV = """\
event_id\tevent_date\tcountry_iso3\tquad_class\tgoldstein
1\t2024-01-15\tUSA\t1\t3.4
2\t2024-01-22\tUSA\t3\t-5.0
3\t2024-02-03\tUSA\t4\t-9.0
4\t2024-01-10\tCHN\t2\t6.0
5\t2024-01-11\tCHN\t4\t-8.5
6\t2024-03-05\tDEU\t1\t2.0
7\tbroken-date\tDEU\t1\t1.0
8\t2024-02-15\t\t1\t1.0
9\t2024-02-15\txx\t1\t1.0
"""


def test_aggregate_event_count():
    agg = _aggregate(_FIXTURE_TSV)
    assert agg["USA|event_count"] == {date(2024, 1, 1): 2.0, date(2024, 2, 1): 1.0}
    assert agg["CHN|event_count"] == {date(2024, 1, 1): 2.0}
    assert agg["DEU|event_count"] == {date(2024, 3, 1): 1.0}


def test_aggregate_goldstein_weighted():
    agg = _aggregate(_FIXTURE_TSV)
    assert abs(agg["USA|goldstein_weighted"][date(2024, 1, 1)] - (3.4 + -5.0)) < 1e-9
    assert agg["USA|goldstein_weighted"][date(2024, 2, 1)] == -9.0
    assert abs(agg["CHN|goldstein_weighted"][date(2024, 1, 1)] - (6.0 + -8.5)) < 1e-9


def test_aggregate_quad_class_decomposition():
    agg = _aggregate(_FIXTURE_TSV)
    assert agg["USA|material_conflict"] == {date(2024, 2, 1): 1.0}
    assert agg["USA|verbal_conflict"] == {date(2024, 1, 1): 1.0}
    assert agg["CHN|material_conflict"] == {date(2024, 1, 1): 1.0}
    assert "DEU|material_conflict" not in agg or agg["DEU|material_conflict"] == {}


def test_aggregate_ignores_broken_rows():
    agg = _aggregate(_FIXTURE_TSV)
    assert "DEU|event_count" in agg
    # The broken-date row for DEU is dropped — only the 2024-03-05 row counts
    assert agg["DEU|event_count"] == {date(2024, 3, 1): 1.0}
    # Empty / unknown ISOs are dropped entirely
    assert "" not in {k.split("|")[0] for k in agg}


def test_normalize_iso():
    assert _normalize_iso("usa") == "USA"
    assert _normalize_iso("USA") == "USA"
    assert _normalize_iso("us") == ""
    assert _normalize_iso("") == ""
    assert _normalize_iso("abcd") == ""


def test_catalog_coverage():
    # Tier-V economies must be in the catalog
    for iso3 in ("USA", "CHN", "JPN", "DEU", "GBR", "FRA", "IND"):
        assert SeriesId(f"{iso3}.POLECAT.event_count.country.M") in POLECAT_CATALOG
        assert SeriesId(f"{iso3}.POLECAT.goldstein_weighted.country.M") in POLECAT_CATALOG
    # Four kinds per country
    assert len(POLECAT_CATALOG) == 4 * len(POLECAT_COUNTRIES)


def test_adapter_emits_observations_from_fixture(monkeypatch):
    """End-to-end: install a fixture archive, pull a series, verify Observations."""
    import opengem_data_polecat.adapter as mod

    fixture_bytes = _FIXTURE_TSV.encode("utf-8")
    adapter = POLECATAdapter()

    def fake_get(self, _url, **_kw):
        return httpx.Response(200, content=fixture_bytes)

    monkeypatch.setattr(httpx.Client, "get", fake_get)

    sid = SeriesId("USA.POLECAT.event_count.country.M")
    obs = list(adapter.pull_series(sid))

    assert len(obs) == 2
    months = sorted(o.observed_at for o in obs)
    assert months == [date(2024, 1, 1), date(2024, 2, 1)]
    values_by_month = {o.observed_at: o.value for o in obs}
    assert values_by_month[date(2024, 1, 1)] == 2.0
    assert values_by_month[date(2024, 2, 1)] == 1.0

    # Provenance fields
    for o in obs:
        assert o.source == "POLECAT"
        assert o.series_id == sid
        assert o.metadata["country"] == "USA"
        assert "Cline Center" in o.metadata["source_attribution"]


def test_unknown_series_id_raises():
    adapter = POLECATAdapter()
    with pytest.raises(KeyError):
        list(adapter.pull_series(SeriesId("NOT.A.REAL.SERIES.M")))
