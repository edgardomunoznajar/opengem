from __future__ import annotations

from datetime import date

from opengem_types import Country, Variable

from opengem_scenarios import ScenarioInvocation, default_library


def test_invocation_resolves_to_concrete_spec() -> None:
    lib = default_library()
    pack = lib.get("fed-plus-100bp")
    inv = ScenarioInvocation(pack=pack, invoked_at=date(2026, 5, 25))
    spec = inv.resolve()
    assert "fed-plus-100bp" in spec.scenario_id
    assert "2026-05-25" in spec.scenario_id
    assert spec.shocks[0].magnitude == 1.0
    assert spec.metadata["pack_id"] == "fed-plus-100bp"


def test_invocation_magnitude_scaling() -> None:
    lib = default_library()
    pack = lib.get("fed-plus-100bp")
    inv = ScenarioInvocation(pack=pack, invoked_at=date(2026, 5, 25), magnitude_scale=2.5)
    spec = inv.resolve()
    assert spec.shocks[0].magnitude == 1.0 * 2.5  # +250bp instead of +100bp


def test_invocation_start_override() -> None:
    lib = default_library()
    pack = lib.get("fed-plus-100bp")
    inv = ScenarioInvocation(
        pack=pack,
        invoked_at=date(2026, 5, 25),
        start_period_override=date(2026, 10, 1),
    )
    spec = inv.resolve()
    assert spec.shocks[0].start_period == date(2026, 10, 1)


def test_invocation_additional_countries() -> None:
    lib = default_library()
    pack = lib.get("fed-plus-100bp")
    inv = ScenarioInvocation(
        pack=pack,
        invoked_at=date(2026, 5, 25),
        additional_countries=(Country.IN, Country.ZA),
    )
    spec = inv.resolve()
    assert Country.IN in spec.target_countries
    assert Country.ZA in spec.target_countries
    # Original countries preserved
    assert Country.US in spec.target_countries


def test_invocation_no_duplicate_country_added() -> None:
    lib = default_library()
    pack = lib.get("fed-plus-100bp")  # already has US
    inv = ScenarioInvocation(
        pack=pack,
        invoked_at=date(2026, 5, 25),
        additional_countries=(Country.US,),  # duplicate
    )
    spec = inv.resolve()
    us_count = sum(1 for c in spec.target_countries if c == Country.US)
    assert us_count == 1
