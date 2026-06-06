"""Canonical typed dataclasses for OPENGEM.

Pure stdlib. The vocabulary every other OPENGEM package speaks.
"""

from opengem_types.conditional import Basis, Conditional, ConfidenceKind
from opengem_types.country import Country
from opengem_types.forecast import DensityForecast, Forecast, ForecastQuantiles
from opengem_types.frequency import Frequency
from opengem_types.observation import Observation
from opengem_types.provenance import RunProvenance
from opengem_types.scenario import Identification, ScenarioSpec, Shock, ShockType
from opengem_types.series import SeriesId, SeriesMeta
from opengem_types.variable import Variable
from opengem_types.vintage import VintageSnapshot

__all__ = [
    "Basis",
    "Conditional",
    "ConfidenceKind",
    "Country",
    "DensityForecast",
    "Forecast",
    "ForecastQuantiles",
    "Frequency",
    "Identification",
    "Observation",
    "RunProvenance",
    "ScenarioSpec",
    "SeriesId",
    "SeriesMeta",
    "Shock",
    "ShockType",
    "Variable",
    "VintageSnapshot",
]

__version__ = "0.2.0"
