from __future__ import annotations

import pytest

from opengem_types import Country

from opengem_scenarios import ScenarioLibrary, default_library
from opengem_scenarios.library_packs import build_default_packs


def test_default_library_has_ten_packs() -> None:
    lib = default_library()
    assert len(lib) == 10
    expected_ids = {
        "russia-ukraine-energy",
        "china-taiwan-disruption",
        "iran-israel-escalation",
        "fed-plus-100bp",
        "opec-supply-cut",
        "eu-energy-shock",
        "us-election-fiscal-regime",
        "china-stimulus",
        "global-recession-trigger",
        "sanctions-on-tech",
    }
    actual = {p.pack_id for p in lib}
    assert actual == expected_ids


def test_library_get() -> None:
    lib = default_library()
    pack = lib.get("fed-plus-100bp")
    assert pack.title.startswith("Fed surprise")


def test_library_get_missing() -> None:
    lib = default_library()
    with pytest.raises(KeyError):
        lib.get("nonexistent-pack")


def test_library_by_tag() -> None:
    lib = default_library()
    energy_packs = lib.by_tag("energy")
    energy_ids = {p.pack_id for p in energy_packs}
    assert "russia-ukraine-energy" in energy_ids
    assert "eu-energy-shock" in energy_ids
    assert "opec-supply-cut" in energy_ids


def test_library_by_country() -> None:
    lib = default_library()
    us_packs = lib.by_country(Country.US)
    assert len(us_packs) >= 3


def test_library_duplicate_id_rejected() -> None:
    packs = build_default_packs()
    duped = packs + [packs[0]]
    with pytest.raises(ValueError, match="duplicate pack_id"):
        ScenarioLibrary(duped)


def test_all_packs_have_nonempty_template() -> None:
    lib = default_library()
    for pack in lib:
        assert pack.template.shocks, f"{pack.pack_id} has empty shocks"
        assert pack.template.target_countries, f"{pack.pack_id} has empty target_countries"


def test_all_packs_have_rationale_and_references() -> None:
    lib = default_library()
    for pack in lib:
        assert pack.rationale, f"{pack.pack_id} lacks rationale"
        assert pack.references, f"{pack.pack_id} lacks references"
