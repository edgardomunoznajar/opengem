from __future__ import annotations

from datetime import date

import pytest

from opengem_types import (
    Country,
    Identification,
    ScenarioSpec,
    Shock,
    ShockType,
    Variable,
)


def _shock() -> Shock:
    return Shock(
        country=Country.US,
        variable=Variable.POLICY_RATE,
        magnitude=1.0,
        unit="pp",
        start_period=date(2026, 7, 1),
        length_quarters=4,
    )


def test_scenario_spec_construction() -> None:
    spec = ScenarioSpec(
        scenario_id="fed-plus-100bp-2026Q3",
        shocks=(_shock(),),
        shock_type=ShockType.LEVEL_SHOCK,
        identification=Identification.CHOLESKY,
        target_countries=(Country.US, Country.EA, Country.JP),
        target_variables=(Variable.GDP_REAL, Variable.CPI_HEADLINE),
    )
    assert spec.target_horizons_q == (1, 4, 8)
    assert spec.shock_type == ShockType.LEVEL_SHOCK


def test_scenario_spec_empty_shocks_rejected() -> None:
    with pytest.raises(ValueError, match="at least one shock"):
        ScenarioSpec(
            scenario_id="empty",
            shocks=(),
            shock_type=ShockType.LEVEL_SHOCK,
            identification=Identification.CHOLESKY,
            target_countries=(Country.US,),
            target_variables=(Variable.GDP_REAL,),
        )


def test_scenario_spec_empty_targets_rejected() -> None:
    with pytest.raises(ValueError, match="at least one country"):
        ScenarioSpec(
            scenario_id="no-country",
            shocks=(_shock(),),
            shock_type=ShockType.LEVEL_SHOCK,
            identification=Identification.CHOLESKY,
            target_countries=(),
            target_variables=(Variable.GDP_REAL,),
        )

    with pytest.raises(ValueError, match="at least one variable"):
        ScenarioSpec(
            scenario_id="no-var",
            shocks=(_shock(),),
            shock_type=ShockType.LEVEL_SHOCK,
            identification=Identification.CHOLESKY,
            target_countries=(Country.US,),
            target_variables=(),
        )
