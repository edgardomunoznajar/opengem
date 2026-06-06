"""opengem-panel — vintage observations -> model-ready quarterly panel.

Public API:
    ColumnSpec   — declarative (column, series_id, transform) triple
    build_panel  — assemble a quarterly pandas DataFrame from a VintageView
    US_GDP_CPI_SPEC — the canonical 2-column US panel (gdp_yoy + cpi_yoy)
"""

from opengem_panel.builder import US_GDP_CPI_SPEC, ColumnSpec, build_panel

__all__ = ["US_GDP_CPI_SPEC", "ColumnSpec", "build_panel"]
__version__ = "0.1.0"
