"""BIS CBPOL series catalog."""

from __future__ import annotations

from opengem_data_base import SeriesCatalog
from opengem_types import SeriesId

# BIS Central Bank Policy Rates — coverage per R07 §2.3
BIS_CBPOL_COUNTRIES: tuple[str, ...] = (
    "AR", "AU", "BR", "CA", "CN", "HR", "CZ", "DK", "GR", "HK",
    "HU", "IS", "IN", "ID", "IL", "JP", "KR", "MX", "MY", "NO",
    "NZ", "PE", "PH", "PL", "RO", "RU", "SA", "SE", "CH", "TH",
    "TR", "UK", "US", "ZA",
    # Euro-area members (post-2024 dissemination)
    "AT", "BE", "DE", "ES", "FI", "FR", "IE", "IT", "LU", "NL", "PT",
)


def _bis(country: str) -> tuple[str, dict[str, str]]:
    return f"BIS.CBPOL/{country}", {
        "country": country,
        "frequency": "D",
        "key": f"D.{country}",
    }


BIS_CATALOG = SeriesCatalog(
    {
        SeriesId(f"{c}.BIS.CBPOL.policy_rate.D"): _bis(c)
        for c in BIS_CBPOL_COUNTRIES
    }
)
