"""OECD ORDRA adapter for OPENGEM."""

from opengem_data_ordra.adapter import ORDRAAdapter
from opengem_data_ordra.catalog import ORDRA_CATALOG, ordra_series_id

__all__ = ["ORDRA_CATALOG", "ORDRAAdapter", "ordra_series_id"]
__version__ = "0.1.0"
