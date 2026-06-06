"""POLECAT series catalog — four derived series per country.

POLECAT itself is event-level (one row per event). OPENGEM publishes monthly
country composites, not raw events, per the L021–L030 license-and-parsimony
discipline (CC0 permits republication; editorial discipline keeps it
aggregated unless a specific use case justifies raw event publication).
"""

from __future__ import annotations

from opengem_data_base import SeriesCatalog
from opengem_types import SeriesId

# Country coverage — Tier-V + a wider Tier-T set that POLECAT covers in
# practice. PLOVER's geocoder gives us ~190 countries; OPENGEM publishes
# the ~50 economically-meaningful ones first and expands as the panel demands.
POLECAT_COUNTRIES: tuple[str, ...] = (
    # G20
    "USA", "CHN", "JPN", "DEU", "GBR", "FRA", "IND", "ITA", "BRA", "CAN",
    "RUS", "KOR", "AUS", "MEX", "IDN", "TUR", "SAU", "ARG", "ZAF",
    # Other Tier-V macro economies
    "ESP", "NLD", "CHE", "POL", "SWE", "BEL", "IRL",
    # Other Tier-T economies of interest for OPENGEM geopolitics work
    "UKR", "ISR", "IRN", "EGY", "VNM", "PHL", "PAK", "BGD", "THA", "MYS",
    "SGP", "ARE", "CHL", "COL", "PER", "GRC", "PRT", "CZE", "NGA",
    "VEN", "QAT", "TWN", "HKG", "NOR", "DNK", "FIN", "AUT",
)

# Four derived series per country
_KINDS: tuple[tuple[str, str], ...] = (
    ("event_count", "count"),
    ("goldstein_weighted", "sum"),
    ("material_conflict", "count"),
    ("verbal_conflict", "count"),
)


def _native(iso3: str, kind: str) -> tuple[str, dict[str, str]]:
    return f"polecat_{kind}_{iso3.lower()}", {
        "country": iso3,
        "kind": kind,
    }


POLECAT_CATALOG = SeriesCatalog(
    {
        SeriesId(f"{iso3}.POLECAT.{kind}.country.M"): _native(iso3, kind)
        for iso3 in POLECAT_COUNTRIES
        for kind, _agg in _KINDS
    }
)
