"""ScenarioPack — a canonical, curated geopolitical-economic scenario template."""

from __future__ import annotations

from dataclasses import dataclass, field

from opengem_types import Country, Identification, ScenarioSpec, Shock, ShockType, Variable


@dataclass(frozen=True, slots=True)
class ScenarioPack:
    """A registered canonical scenario.

    A pack carries:
    - human-readable identity (`pack_id`, `title`, `summary`)
    - geographic and topical tags for discovery
    - canonical `ScenarioSpec` template that can be modulated at invocation
    - identification choices that match the pack's structural narrative
    - reference shock magnitudes that the engine can scale
    """

    pack_id: str
    title: str
    summary: str
    tags: tuple[str, ...]
    regions: tuple[Country | str, ...]
    template: ScenarioSpec
    rationale: str = ""
    references: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.pack_id:
            raise ValueError("pack_id required")
        if not self.title:
            raise ValueError("title required")
        if not self.template.shocks:
            raise ValueError(f"pack {self.pack_id} has empty template.shocks")

    def matches_tag(self, tag: str) -> bool:
        return tag.lower() in (t.lower() for t in self.tags)

    def covers_country(self, country: Country | str) -> bool:
        target = country.value if isinstance(country, Country) else country
        for r in self.regions:
            r_val = r.value if isinstance(r, Country) else r
            if r_val == target or r_val == "ALL":
                return True
        return False
