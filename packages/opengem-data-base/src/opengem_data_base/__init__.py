"""Adapter base class + common patterns for OPENGEM data adapters."""

from opengem_data_base.adapter import Adapter, PullManifest
from opengem_data_base.catalog import SeriesCatalog
from opengem_data_base.errors import (
    AdapterError,
    AuthError,
    OutageError,
    RateLimitError,
    SchemaError,
)
from opengem_data_base.retry import retry

__all__ = [
    "Adapter",
    "AdapterError",
    "AuthError",
    "OutageError",
    "PullManifest",
    "RateLimitError",
    "SchemaError",
    "SeriesCatalog",
    "retry",
]
__version__ = "0.1.0"
