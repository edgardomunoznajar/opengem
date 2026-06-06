"""ScenarioInvocation — a bound pack + runtime parameters ready for execution."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date

from opengem_types import Country, ScenarioSpec, Variable

from opengem_scenarios.pack import ScenarioPack


@dataclass(frozen=True, slots=True)
class ScenarioInvocation:
    """A pack bound to runtime parameters.

    Pack templates carry default shock magnitudes and start dates. At invocation
    time the user (or the event-trigger engine) can scale magnitude, retarget
    countries/variables/horizons, and shift start period. The result is a fully
    resolved ScenarioSpec ready for the execution engine.
    """

    pack: ScenarioPack
    invoked_at: date
    magnitude_scale: float = 1.0
    start_period_override: date | None = None
    additional_countries: tuple[Country, ...] = field(default_factory=tuple)
    additional_variables: tuple[Variable, ...] = field(default_factory=tuple)
    notes: str = ""

    def resolve(self) -> ScenarioSpec:
        """Resolve to a concrete ScenarioSpec for the execution engine."""
        spec = self.pack.template

        # Apply magnitude scaling and optional start-period override
        new_shocks = tuple(
            replace(
                s,
                magnitude=s.magnitude * self.magnitude_scale,
                start_period=self.start_period_override or s.start_period,
            )
            for s in spec.shocks
        )

        target_countries = spec.target_countries + tuple(
            c for c in self.additional_countries if c not in spec.target_countries
        )
        target_variables = spec.target_variables + tuple(
            v for v in self.additional_variables if v not in spec.target_variables
        )

        scenario_id = f"{spec.scenario_id}@{self.invoked_at.isoformat()}"

        return ScenarioSpec(
            scenario_id=scenario_id,
            shocks=new_shocks,
            shock_type=spec.shock_type,
            identification=spec.identification,
            target_countries=target_countries,
            target_variables=target_variables,
            target_horizons_q=spec.target_horizons_q,
            metadata={
                **spec.metadata,
                "pack_id": self.pack.pack_id,
                "magnitude_scale": str(self.magnitude_scale),
                "invoked_at": self.invoked_at.isoformat(),
                **({"notes": self.notes} if self.notes else {}),
            },
        )
