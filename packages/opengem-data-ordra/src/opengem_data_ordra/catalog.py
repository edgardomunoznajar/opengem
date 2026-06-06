"""ORDRA series catalog builder.

ORDRA covers many countries × variables × frequencies. We build catalog entries
programmatically from a Tier-V country roster × MEI subject codes.
"""

from __future__ import annotations

from opengem_data_base import SeriesCatalog
from opengem_types import Country, SeriesId

# ORDRA MEI subject codes per OECD documentation
MEI_SUBJECTS: dict[str, tuple[str, str]] = {
    # opengem variable kind → (mei_subject, mei_measure)
    "gdp_real": ("LORSGPRT", "IXOBSA"),       # real GDP, index, SA
    "gdp_nominal": ("LORSGPCD", "IXOBSA"),    # nominal GDP, index, SA
    "cpi_headline": ("CPALTT01", "IXOBSA"),   # CPI all items, SA
    "cpi_core": ("CPALCY01", "IXOBSA"),       # CPI core
    "unemployment_rate": ("LRUNTTTT", "STSA"),  # Unemp rate, SA, % of LF
    "industrial_production": ("PRINTO01", "IXOBSA"),
    "leading_indicator": ("LOLITOAA", "STSA"),
}


def ordra_series_id(country: str, variable_kind: str, frequency: str = "Q") -> SeriesId:
    """Construct an OPENGEM SeriesId for an ORDRA series."""
    return SeriesId(f"{country}.OECD.MEI.{variable_kind}.{frequency}")


def _ordra(country: str, variable_kind: str, frequency: str) -> tuple[str, dict[str, str]]:
    subj, meas = MEI_SUBJECTS[variable_kind]
    return f"OECD.MEI/{country}.{subj}.{meas}.{frequency}", {
        "subject": subj,
        "measure": meas,
        "country": country,
        "frequency": frequency,
    }


def _build_catalog() -> SeriesCatalog:
    """Build the default Tier-V catalog: tier_v_core × core variables × Q/M."""
    entries: dict[SeriesId, tuple[str, dict[str, str]]] = {}
    core_countries = sorted(Country.tier_v_core())
    # GDP quarterly
    for c in core_countries:
        country_iso = c.value
        for var in ("gdp_real", "gdp_nominal"):
            sid = ordra_series_id(country_iso, var, "Q")
            entries[sid] = _ordra(country_iso, var, "Q")
        for var in ("cpi_headline", "unemployment_rate", "industrial_production"):
            sid = ordra_series_id(country_iso, var, "M")
            entries[sid] = _ordra(country_iso, var, "M")
    return SeriesCatalog(entries)


ORDRA_CATALOG = _build_catalog()
