"""BIS Data Portal adapter for OPENGEM."""

from opengem_data_bis.adapter import BISAdapter
from opengem_data_bis.catalog import BIS_CATALOG, BIS_CBPOL_COUNTRIES

__all__ = ["BIS_CATALOG", "BIS_CBPOL_COUNTRIES", "BISAdapter"]
__version__ = "0.1.0"
