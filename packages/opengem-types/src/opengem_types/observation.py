"""Observation — a single time-series data point."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from opengem_types.series import SeriesId


@dataclass(frozen=True, slots=True)
class Observation:
    """A single (series, reference period, vintage) data point.

    `observed_at` is the reference period (start of quarter / month / day).
    `vintage_at` is the date the source agency published the value.
    `value` may be None if the period exists but no value has been released yet.
    """

    series_id: SeriesId
    observed_at: date
    vintage_at: date
    value: float | None
    source: str
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.vintage_at < self.observed_at:
            # Vintage = release date, must be on or after reference period.
            # An ALFRED-style backfill can have vintage_at == observed_at + 0 if same-day release.
            # But vintage strictly before observation is nonsensical.
            raise ValueError(
                f"vintage_at ({self.vintage_at}) must be >= observed_at ({self.observed_at})"
            )

    @property
    def revision_lag_days(self) -> int:
        """Days between reference period and publication."""
        return (self.vintage_at - self.observed_at).days
