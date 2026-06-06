"""SeriesId and SeriesMeta.

SeriesId is a hierarchical, canonical identifier:
    <country>.<source>.<release>.<variable>.<frequency>

Examples:
    US.BEA.NIPA.GDP_real.Q
    US.BLS.CPI.CPI_headline_SA.M
    EA.ECB.SDW.HICP_headline.M
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SeriesId:
    """A canonical hierarchical series identifier.

    Validates non-empty, dot-separated, ASCII-only identifier on construction.
    """

    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("SeriesId cannot be empty")
        if not self.value.isascii():
            raise ValueError(f"SeriesId must be ASCII: {self.value!r}")
        parts = self.value.split(".")
        if len(parts) < 3:
            raise ValueError(
                f"SeriesId must have at least 3 dot-separated parts, got {self.value!r}"
            )
        for p in parts:
            if not p:
                raise ValueError(f"SeriesId has empty segment: {self.value!r}")

    @property
    def country(self) -> str:
        return self.value.split(".")[0]

    @property
    def source(self) -> str:
        return self.value.split(".")[1]

    @property
    def variable_kind(self) -> str:
        """The variable component (4th segment if present, else 3rd)."""
        parts = self.value.split(".")
        if len(parts) >= 4:
            return parts[3]
        return parts[2]

    @property
    def frequency_suffix(self) -> str | None:
        """Last segment if it looks like a frequency code (Q, M, D, W, A)."""
        last = self.value.split(".")[-1]
        if last in {"Q", "M", "D", "W", "A"}:
            return last
        return None

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class SeriesMeta:
    """Static metadata describing a series."""

    series_id: SeriesId
    source: str  # 'BEA', 'BLS', etc. — also encoded in series_id but explicit here
    description: str
    unit: str
    frequency: str  # 'Q', 'M', 'D', 'W', 'A'
    country: str  # ISO alpha-2 or canonical region code
    variable_kind: str  # 'gdp_real', 'cpi_headline', etc.
    source_native_id: str | None = None  # the source's own identifier
