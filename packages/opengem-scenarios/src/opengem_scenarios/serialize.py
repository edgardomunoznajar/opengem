"""JSON serialization for ScenarioPack — for disk persistence and API surface."""

from __future__ import annotations

from datetime import date
from typing import Any

from opengem_types import Country, Identification, ScenarioSpec, Shock, ShockType, Variable

from opengem_scenarios.pack import ScenarioPack


def pack_to_dict(pack: ScenarioPack) -> dict[str, Any]:
    """Serialize a ScenarioPack to a JSON-safe dict."""
    return {
        "pack_id": pack.pack_id,
        "title": pack.title,
        "summary": pack.summary,
        "tags": list(pack.tags),
        "regions": [r.value if isinstance(r, Country) else r for r in pack.regions],
        "rationale": pack.rationale,
        "references": list(pack.references),
        "template": _spec_to_dict(pack.template),
    }


def pack_from_dict(d: dict[str, Any]) -> ScenarioPack:
    """Inverse of pack_to_dict."""
    regions = tuple(_resolve_country(r) for r in d.get("regions", []))
    return ScenarioPack(
        pack_id=d["pack_id"],
        title=d["title"],
        summary=d["summary"],
        tags=tuple(d.get("tags", [])),
        regions=regions,
        rationale=d.get("rationale", ""),
        references=tuple(d.get("references", [])),
        template=_spec_from_dict(d["template"]),
    )


def _spec_to_dict(spec: ScenarioSpec) -> dict[str, Any]:
    return {
        "scenario_id": spec.scenario_id,
        "shocks": [_shock_to_dict(s) for s in spec.shocks],
        "shock_type": spec.shock_type.value,
        "identification": spec.identification.value,
        "target_countries": [c.value for c in spec.target_countries],
        "target_variables": [v.value for v in spec.target_variables],
        "target_horizons_q": list(spec.target_horizons_q),
        "metadata": dict(spec.metadata),
    }


def _spec_from_dict(d: dict[str, Any]) -> ScenarioSpec:
    return ScenarioSpec(
        scenario_id=d["scenario_id"],
        shocks=tuple(_shock_from_dict(s) for s in d["shocks"]),
        shock_type=ShockType(d["shock_type"]),
        identification=Identification(d["identification"]),
        target_countries=tuple(Country(c) for c in d["target_countries"]),
        target_variables=tuple(Variable(v) for v in d["target_variables"]),
        target_horizons_q=tuple(d.get("target_horizons_q", (1, 4, 8))),
        metadata=dict(d.get("metadata", {})),
    )


def _shock_to_dict(s: Shock) -> dict[str, Any]:
    return {
        "country": s.country.value,
        "variable": s.variable.value,
        "magnitude": s.magnitude,
        "unit": s.unit,
        "start_period": s.start_period.isoformat(),
        "length_quarters": s.length_quarters,
    }


def _shock_from_dict(d: dict[str, Any]) -> Shock:
    return Shock(
        country=Country(d["country"]),
        variable=Variable(d["variable"]),
        magnitude=float(d["magnitude"]),
        unit=d["unit"],
        start_period=date.fromisoformat(d["start_period"]),
        length_quarters=int(d.get("length_quarters", 1)),
    )


def _resolve_country(r: Country | str) -> Country | str:
    if isinstance(r, Country):
        return r
    try:
        return Country(r)
    except ValueError:
        return r
