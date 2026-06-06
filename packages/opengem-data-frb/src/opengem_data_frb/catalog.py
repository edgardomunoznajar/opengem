"""FRB Board series catalog."""

from __future__ import annotations

from opengem_types import SeriesId

from opengem_data_base import SeriesCatalog


def _frb(release: str, series: str, freq: str = "D") -> tuple[str, dict[str, str]]:
    return f"{release}/{series}", {"release": release, "series": series, "freq": freq}


FRB_CATALOG = SeriesCatalog(
    {
        # H.15 — Interest rates
        SeriesId("US.FRB.H15.DGS10.D"): _frb("H15", "DGS10"),
        SeriesId("US.FRB.H15.DGS2.D"): _frb("H15", "DGS2"),
        SeriesId("US.FRB.H15.DGS3MO.D"): _frb("H15", "DGS3MO"),
        SeriesId("US.FRB.H15.FEDFUNDS.D"): _frb("H15", "FEDFUNDS"),
        SeriesId("US.FRB.H15.DFEDTARU.D"): _frb("H15", "DFEDTARU"),
        SeriesId("US.FRB.H15.DFEDTARL.D"): _frb("H15", "DFEDTARL"),
        # G.17 — Industrial production / capacity
        SeriesId("US.FRB.G17.INDPRO.M"): _frb("G17", "INDPRO", "M"),
        SeriesId("US.FRB.G17.CAPUTL.M"): _frb("G17", "CAPUTL", "M"),
        # H.6 — Money stock
        SeriesId("US.FRB.H6.M2.M"): _frb("H6", "M2", "M"),
    }
)
