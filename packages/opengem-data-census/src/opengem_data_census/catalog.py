"""Census Bureau series catalog."""

from __future__ import annotations

from opengem_types import SeriesId

from opengem_data_base import SeriesCatalog


def _m3(data_type: str) -> tuple[str, dict[str, str]]:
    """M3 = Manufacturers' Shipments, Inventories, Orders."""
    return f"M3/{data_type}", {
        "dataset": "timeseries/eits/advm3",
        "data_type_code": data_type,
        "category_code": "0",  # total
        "seasonally_adj": "yes",
    }


def _mrts(data_type: str) -> tuple[str, dict[str, str]]:
    return f"MRTS/{data_type}", {
        "dataset": "timeseries/eits/marts",
        "data_type_code": data_type,
        "category_code": "44X72",  # total retail and food services
        "seasonally_adj": "yes",
    }


CENSUS_CATALOG = SeriesCatalog(
    {
        SeriesId("US.CENSUS.M3.inventories_total.M"): _m3("TI"),  # total inventories
        SeriesId("US.CENSUS.M3.shipments_total.M"): _m3("VS"),  # value of shipments
        SeriesId("US.CENSUS.M3.new_orders_total.M"): _m3("NO"),  # new orders
        SeriesId("US.CENSUS.MRTS.retail_sales.M"): _mrts("SM"),  # sales
    }
)
