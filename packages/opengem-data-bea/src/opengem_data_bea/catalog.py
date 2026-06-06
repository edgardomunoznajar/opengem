"""BEA series catalog.

Maps OPENGEM canonical SeriesIds to BEA API parameters.
Each native value is the tuple of (DataSetName, TableName, LineNumber) plus an
optional `Frequency` override.
"""

from __future__ import annotations

from opengem_types import SeriesId

from opengem_data_base import SeriesCatalog


def _bea(dataset: str, table: str, line: int, freq: str = "Q") -> tuple[str, dict[str, str]]:
    """Convenience builder for BEA native identifier tuples."""
    return f"{dataset}/{table}/L{line}", {
        "DataSetName": dataset,
        "TableName": table,
        "LineNumber": str(line),
        "Frequency": freq,
    }


BEA_CATALOG = SeriesCatalog(
    {
        # Real GDP and components (annualized chained dollars, quarterly)
        SeriesId("US.BEA.NIPA.GDP_real.Q"): _bea("NIPA", "T10101", 1, "Q"),
        SeriesId("US.BEA.NIPA.PCE_real.Q"): _bea("NIPA", "T10101", 2, "Q"),
        SeriesId("US.BEA.NIPA.Investment_real.Q"): _bea("NIPA", "T10101", 6, "Q"),
        SeriesId("US.BEA.NIPA.NetExports_real.Q"): _bea("NIPA", "T10101", 14, "Q"),
        SeriesId("US.BEA.NIPA.GovExp_real.Q"): _bea("NIPA", "T10101", 21, "Q"),
        # Nominal GDP and deflator
        SeriesId("US.BEA.NIPA.GDP_nominal.Q"): _bea("NIPA", "T10105", 1, "Q"),
        SeriesId("US.BEA.NIPA.GDP_deflator.Q"): _bea("NIPA", "T10104", 1, "Q"),
        # PCE prices (monthly)
        SeriesId("US.BEA.NIPA.PCE_deflator.M"): _bea("NIPA", "T20804", 1, "M"),
        # GDI
        SeriesId("US.BEA.NIPA.GDI.Q"): _bea("NIPA", "T10703", 1, "Q"),
    }
)
