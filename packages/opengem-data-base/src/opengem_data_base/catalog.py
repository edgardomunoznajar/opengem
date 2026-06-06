"""SeriesCatalog — typed mapping from OPENGEM canonical SeriesIds to source-native identifiers."""

from __future__ import annotations

from collections.abc import Iterator, Mapping

from opengem_types import SeriesId


class SeriesCatalog:
    """Immutable mapping: OPENGEM SeriesId → source-native id (and optional kwargs).

    The native identifier can be a simple string or a (id, kwargs) tuple to
    carry source-specific endpoint parameters.
    """

    def __init__(self, mapping: Mapping[SeriesId, str | tuple[str, dict[str, str]]]) -> None:
        self._map: dict[SeriesId, tuple[str, dict[str, str]]] = {}
        for k, v in mapping.items():
            if isinstance(v, str):
                self._map[k] = (v, {})
            else:
                native_id, kwargs = v
                self._map[k] = (native_id, dict(kwargs))

    def __contains__(self, key: SeriesId) -> bool:
        return key in self._map

    def __iter__(self) -> Iterator[SeriesId]:
        return iter(self._map)

    def __len__(self) -> int:
        return len(self._map)

    def native(self, series_id: SeriesId) -> tuple[str, dict[str, str]]:
        if series_id not in self._map:
            raise KeyError(f"SeriesId not in catalog: {series_id}")
        return self._map[series_id]

    def items(self) -> Iterator[tuple[SeriesId, tuple[str, dict[str, str]]]]:
        return iter(self._map.items())
