"""Abstract VintageStore interface and `VintageView` for as-of queries."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from datetime import date, datetime

from opengem_types import Observation, SeriesId, SeriesMeta, VintageSnapshot


class VintageStore(ABC):
    """Abstract vintage-correct observation store.

    Implementations must guarantee:
    - **No overwrites**: writing (series, observed_at, vintage_at) twice with
      different values is an error (INSERT-only semantics).
    - **Atomic batches**: `write_batch` succeeds entirely or rolls back.
    - **Snapshot determinism**: the `vintage_hash` is reproducible from the
      observation set alone.
    """

    @abstractmethod
    def initialize(self) -> None:
        """Create schema if not present. Idempotent."""

    @abstractmethod
    def register_source(self, source_id: str, name: str, base_url: str | None = None) -> None:
        """Register a source. Idempotent."""

    @abstractmethod
    def register_series(self, meta: SeriesMeta) -> None:
        """Register series metadata. Idempotent on (series_id)."""

    @abstractmethod
    def write_batch(
        self,
        observations: Iterable[Observation],
        source_id: str,
        pulled_at: datetime,
    ) -> VintageSnapshot:
        """Write a batch of observations and the snapshot manifest atomically."""

    @abstractmethod
    def at(self, vintage_at: date) -> VintageView:
        """Return a read-only view of the store as known on `vintage_at`."""

    @abstractmethod
    def close(self) -> None:
        """Release resources. Safe to call multiple times."""


class VintageView(ABC):
    """A read-only snapshot of the store as known on a given date.

    Returns, for each (series, observed_at) pair, the latest vintage <= the view's date.
    """

    @abstractmethod
    def iter_series(self, series_id: str | SeriesId) -> Iterator[Observation]:
        """Iterate observations for one series ordered by observed_at ascending."""

    @abstractmethod
    def latest_value(self, series_id: str | SeriesId, observed_at: date) -> float | None:
        """Latest value as known on the view's date for (series, observed_at)."""
