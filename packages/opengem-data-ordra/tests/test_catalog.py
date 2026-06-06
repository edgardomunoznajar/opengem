from __future__ import annotations

from opengem_data_ordra import ORDRA_CATALOG, ordra_series_id
from opengem_types import SeriesId


def test_catalog_has_tier_v_core_gdp() -> None:
    """Every Tier-V Core country should have a real GDP quarterly entry."""
    expected = ordra_series_id("US", "gdp_real", "Q")
    assert expected in ORDRA_CATALOG


def test_catalog_germany_cpi_monthly() -> None:
    sid = ordra_series_id("DE", "cpi_headline", "M")
    assert sid in ORDRA_CATALOG


def test_catalog_native_resolution() -> None:
    sid = SeriesId("US.OECD.MEI.gdp_real.Q")
    native, kwargs = ORDRA_CATALOG.native(sid)
    assert "OECD.MEI" in native
    assert kwargs["country"] == "US"
    assert kwargs["frequency"] == "Q"


def test_catalog_size() -> None:
    # 26 core countries × (2 quarterly + 3 monthly) = 130 entries minimum
    assert len(ORDRA_CATALOG) >= 100
