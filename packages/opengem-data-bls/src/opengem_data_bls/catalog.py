"""BLS series catalog."""

from __future__ import annotations

from opengem_types import SeriesId

from opengem_data_base import SeriesCatalog

BLS_CATALOG = SeriesCatalog(
    {
        SeriesId("US.BLS.CPI.headline_NSA.M"): "CUUR0000SA0",
        SeriesId("US.BLS.CPI.headline_SA.M"): "CUSR0000SA0",
        SeriesId("US.BLS.CPI.core_SA.M"): "CUSR0000SA0L1E",
        SeriesId("US.BLS.LNS.unemp_rate.M"): "LNS14000000",
        SeriesId("US.BLS.CES.nonfarm_payrolls.M"): "CES0000000001",
        SeriesId("US.BLS.CES.avg_hourly_earnings.M"): "CES0500000003",
        SeriesId("US.BLS.PPI.final_demand.M"): "WPUFD4",
    }
)
