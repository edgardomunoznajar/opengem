"""ScenarioLibrary — typed registry of canonical packs with discovery API."""

from __future__ import annotations

from collections.abc import Iterator
from typing import overload

from opengem_types import Country

from opengem_scenarios.pack import ScenarioPack


class ScenarioLibrary:
    """Immutable registry of ScenarioPacks.

    Build via constructor (full list) or `.from_iterable`. Discover via
    `iter_all`, `by_tag`, `by_country`, `get`.
    """

    def __init__(self, packs: list[ScenarioPack]) -> None:
        # Reject duplicates
        ids: set[str] = set()
        for p in packs:
            if p.pack_id in ids:
                raise ValueError(f"duplicate pack_id: {p.pack_id}")
            ids.add(p.pack_id)
        self._packs: dict[str, ScenarioPack] = {p.pack_id: p for p in packs}

    def __len__(self) -> int:
        return len(self._packs)

    def __contains__(self, pack_id: str) -> bool:
        return pack_id in self._packs

    def __iter__(self) -> Iterator[ScenarioPack]:
        return iter(self._packs.values())

    @overload
    def get(self, pack_id: str) -> ScenarioPack: ...
    @overload
    def get(self, pack_id: str, default: ScenarioPack) -> ScenarioPack: ...
    def get(self, pack_id: str, default: ScenarioPack | None = None) -> ScenarioPack:
        pack = self._packs.get(pack_id)
        if pack is not None:
            return pack
        if default is not None:
            return default
        raise KeyError(f"pack not found: {pack_id}")

    def by_tag(self, tag: str) -> list[ScenarioPack]:
        return [p for p in self._packs.values() if p.matches_tag(tag)]

    def by_country(self, country: Country | str) -> list[ScenarioPack]:
        return [p for p in self._packs.values() if p.covers_country(country)]


def default_library() -> ScenarioLibrary:
    """The IOC canonical scenario library — 10 packs."""
    from opengem_scenarios.library_packs import build_default_packs

    return ScenarioLibrary(build_default_packs())
