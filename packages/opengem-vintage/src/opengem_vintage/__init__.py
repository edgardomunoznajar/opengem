"""Vintage-correct storage primitives for OPENGEM."""

from opengem_vintage.store import VintageStore, VintageView
from opengem_vintage.sqlite_store import SQLiteVintageStore

__all__ = ["SQLiteVintageStore", "VintageStore", "VintageView"]
__version__ = "0.1.0"
