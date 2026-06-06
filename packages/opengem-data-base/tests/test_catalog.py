from __future__ import annotations

import pytest

from opengem_types import SeriesId

from opengem_data_base import SeriesCatalog


def test_catalog_basic() -> None:
    cat = SeriesCatalog(
        {
            SeriesId("US.BEA.NIPA.GDP_real.Q"): "T10101.L1",
            SeriesId("US.BEA.NIPA.GDP_nominal.Q"): ("T10105.L1", {"freq": "Q"}),
        }
    )
    assert SeriesId("US.BEA.NIPA.GDP_real.Q") in cat
    assert SeriesId("US.BEA.NIPA.GDP_nominal.Q") in cat
    assert len(cat) == 2


def test_catalog_native_lookup() -> None:
    cat = SeriesCatalog(
        {
            SeriesId("US.BEA.NIPA.GDP_real.Q"): "T10101.L1",
            SeriesId("US.BEA.NIPA.GDP_nominal.Q"): ("T10105.L1", {"freq": "Q"}),
        }
    )
    native, kwargs = cat.native(SeriesId("US.BEA.NIPA.GDP_real.Q"))
    assert native == "T10101.L1"
    assert kwargs == {}

    native2, kwargs2 = cat.native(SeriesId("US.BEA.NIPA.GDP_nominal.Q"))
    assert native2 == "T10105.L1"
    assert kwargs2 == {"freq": "Q"}


def test_catalog_missing_key_raises() -> None:
    cat = SeriesCatalog({})
    with pytest.raises(KeyError):
        cat.native(SeriesId("US.NOPE.NA.NA"))


def test_catalog_is_iterable() -> None:
    cat = SeriesCatalog({SeriesId("US.X.Y.Z"): "a", SeriesId("US.X.Y.W"): "b"})
    ids = list(cat)
    assert len(ids) == 2
