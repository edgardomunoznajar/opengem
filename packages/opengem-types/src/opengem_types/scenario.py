"""ScenarioSpec — structured shock specification for the Scenario Subsystem."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum

from opengem_types.country import Country
from opengem_types.variable import Variable


class ShockType(StrEnum):
    LEVEL_SHOCK = "level_shock"  # one-time adjustment to level
    PATH_SHOCK = "path_shock"  # specified trajectory
    STRUCTURAL_SHOCK = "structural_shock"  # identified shock via L1


class Identification(StrEnum):
    CHOLESKY = "cholesky"
    SIGN_RESTRICTION = "sign_restriction"
    STRUCTURAL = "structural"
    NARRATIVE = "narrative"


@dataclass(frozen=True, slots=True)
class Shock:
    """A single shock element of a scenario."""

    country: Country
    variable: Variable
    magnitude: float
    unit: str  # 'pp' (percentage points), 'pct' (percent), 'level', 'sigma'
    start_period: date
    length_quarters: int = 1


@dataclass(frozen=True, slots=True)
class ScenarioSpec:
    """A scenario request: one or more shocks + identification + target scope.

    Multiple shocks compose; the propagator applies them jointly.
    """

    scenario_id: str  # human-friendly name like 'russia-ukraine-energy-2026Q3'
    shocks: tuple[Shock, ...]
    shock_type: ShockType
    identification: Identification
    target_countries: tuple[Country, ...]
    target_variables: tuple[Variable, ...]
    target_horizons_q: tuple[int, ...] = (1, 4, 8)
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.shocks:
            raise ValueError("ScenarioSpec must have at least one shock")
        if not self.target_countries:
            raise ValueError("ScenarioSpec must target at least one country")
        if not self.target_variables:
            raise ValueError("ScenarioSpec must target at least one variable")
