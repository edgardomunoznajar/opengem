"""Adapter — abstract base class for OPENGEM data adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import date, datetime

from opengem_types import Observation, SeriesId

from opengem_data_base.catalog import SeriesCatalog


@dataclass(frozen=True, slots=True)
class PullManifest:
    """Summary of one adapter pull invocation."""

    source_id: str
    pulled_at: datetime
    series_pulled: tuple[str, ...]
    observation_count: int
    errors: tuple[str, ...] = field(default_factory=tuple)


class Adapter(ABC):
    """Abstract base for all OPENGEM data adapters.

    Concrete adapters must:
    - declare `source_id` (e.g., 'BEA', 'BLS', 'ECB')
    - declare `catalog` mapping OPENGEM SeriesIds to source-native identifiers
    - implement `pull_series(opengem_series_id)` returning an iterator of Observations
    - optionally override `pull_release(as_of=...)` if the source has a release-level
      bulk endpoint; default implementation iterates the catalog
    """

    source_id: str = ""
    catalog: SeriesCatalog = SeriesCatalog({})

    def __init__(self) -> None:
        if not self.__class__.source_id:
            raise TypeError(
                f"{self.__class__.__name__} must declare a non-empty source_id class attribute"
            )

    @abstractmethod
    def pull_series(self, opengem_series_id: SeriesId) -> Iterator[Observation]:
        """Pull all historical observations for one series."""
        ...

    def pull_release(self, as_of: date | None = None) -> Iterator[Observation]:
        """Pull the latest release values for all series in catalog.

        Default: iterate the catalog and yield from `pull_series` for each.
        Subclasses can override with a more efficient bulk endpoint.
        """
        del as_of  # not used by default impl; subclasses may use it
        for sid in self.catalog:
            yield from self.pull_series(sid)

    def health_check(self) -> bool:
        """Cheap call to verify the source is reachable. Default: True (override)."""
        return True
