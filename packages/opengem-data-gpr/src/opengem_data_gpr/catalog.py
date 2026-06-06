"""GPR series catalog — global + 44 country-specific indexes."""

from __future__ import annotations

from opengem_data_base import SeriesCatalog
from opengem_types import SeriesId

# Country-specific GPR coverage per Caldara-Iacoviello (44 countries)
GPR_COUNTRIES: tuple[str, ...] = (
    "AR", "BR", "CL", "CO", "MX", "PE", "VE",
    "CA", "US",
    "AU", "CN", "HK", "IN", "ID", "JP", "KR", "MY", "PH", "SG", "TH", "TW", "VN",
    "AT", "BE", "DK", "FI", "FR", "DE", "GR", "IE", "IT", "NL", "NO", "PL", "PT", "RU", "ES", "SE", "CH", "TR", "UA", "UK",
    "EG", "IL", "SA", "ZA",
)


def _gpr_global() -> tuple[str, dict[str, str]]:
    return "gpr_global", {"kind": "global", "country": "WORLD"}


def _gpr_country(country: str) -> tuple[str, dict[str, str]]:
    return f"gpr_{country}", {"kind": "country", "country": country}


GPR_CATALOG = SeriesCatalog(
    {
        SeriesId("WORLD.GPR.GPR.global.M"): _gpr_global(),
        **{SeriesId(f"{c}.GPR.GPR.country.M"): _gpr_country(c) for c in GPR_COUNTRIES},
    }
)
