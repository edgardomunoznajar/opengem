from __future__ import annotations

import pytest
from opengem_types import SeriesId


def test_series_id_parses_segments() -> None:
    sid = SeriesId("US.BEA.NIPA.GDP_real.Q")
    assert sid.country == "US"
    assert sid.source == "BEA"
    assert sid.variable_kind == "GDP_real"
    assert sid.frequency_suffix == "Q"


def test_series_id_three_segments_no_freq() -> None:
    sid = SeriesId("US.FRB.M2")
    assert sid.country == "US"
    assert sid.source == "FRB"
    assert sid.variable_kind == "M2"
    assert sid.frequency_suffix is None


def test_series_id_str() -> None:
    s = "EA.ECB.SDW.HICP.M"
    assert str(SeriesId(s)) == s


@pytest.mark.parametrize(
    "bad",
    [
        "",
        "single",
        "two.parts",
        "trailing.dot.",
        ".leading",
        "two..dots",
    ],
)
def test_series_id_invalid(bad: str) -> None:
    with pytest.raises(ValueError):
        SeriesId(bad)


def test_series_id_non_ascii_rejected() -> None:
    with pytest.raises(ValueError):
        SeriesId("ÜS.BEA.NIPA")


def test_series_id_is_hashable_and_frozen() -> None:
    a = SeriesId("US.BEA.NIPA.GDP_real.Q")
    b = SeriesId("US.BEA.NIPA.GDP_real.Q")
    assert a == b
    assert hash(a) == hash(b)
    {a, b}  # works in a set
