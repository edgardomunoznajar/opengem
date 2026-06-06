"""OPENGEM L3 — DynamicFactorMQ-based forecast backbone.

Public API:
    DFMConfig         — declarative config for a fit
    fit_dfm           — fit a DynamicFactorMQ on a pandas DataFrame and emit forecasts
    fit_us_gdp        — convenience for the L3 v0.1 US GDP backtest entry point
"""

from opengem_l3_dfm.config import DFMConfig
from opengem_l3_dfm.fit import fit_dfm, fit_us_gdp

__all__ = ["DFMConfig", "fit_dfm", "fit_us_gdp"]
__version__ = "0.1.0"
