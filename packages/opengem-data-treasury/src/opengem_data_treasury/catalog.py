"""US Treasury FiscalData series catalog."""

from __future__ import annotations

from opengem_types import SeriesId

from opengem_data_base import SeriesCatalog


def _yields(maturity: str) -> tuple[str, dict[str, str]]:
    return f"YIELDS/{maturity}", {
        "endpoint": "/v2/accounting/od/daily_treasury_yield_curve_rates",
        "value_field": "avg_interest_rate_amt",
        "date_field": "record_date",
        "filter": f"security_desc:eq:{maturity}",
    }


TREASURY_CATALOG = SeriesCatalog(
    {
        # daily_treasury_yield_curve_rates endpoint filters by security_desc
        SeriesId("US.TREAS.YIELDS.10Y.D"): _yields("10-Year"),
        SeriesId("US.TREAS.YIELDS.2Y.D"): _yields("2-Year"),
        SeriesId("US.TREAS.YIELDS.3M.D"): _yields("3-Month"),
        # debt_to_penny
        SeriesId("US.TREAS.DEBT.public.D"): (
            "DEBT/public",
            {
                "endpoint": "/v2/accounting/od/debt_to_penny",
                "value_field": "tot_pub_debt_out_amt",
                "date_field": "record_date",
                "filter": "",
            },
        ),
    }
)
