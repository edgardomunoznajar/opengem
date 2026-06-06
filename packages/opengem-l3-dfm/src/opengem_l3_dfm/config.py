"""DFMConfig — declarative config for a DynamicFactorMQ fit."""

from __future__ import annotations

from dataclasses import dataclass

from opengem_types import Country


@dataclass(frozen=True, slots=True)
class DFMConfig:
    """Configuration for one DFM fit.

    Attributes
    ----------
    country : str
        Canonical OPENGEM country code — ISO 3166-1 alpha-2, validated against
        ``opengem_types.Country`` (e.g. "US"). ISO-3 codes like "USA" are rejected;
        ``DensityForecast.country`` is typed as ``Country`` so the whole pipeline
        must use the alpha-2 roster.
    target : str
        Target variable code, OPENGEM-canonical (e.g. "gdp_yoy", "cpi_yoy").
    factors : int
        Number of latent factors. Default 2 — matches NY Fed Nowcast in
        the original Bok et al. spec.
    factor_order : int
        VAR order for the latent factors. Default 1.
    horizons_q : tuple[int, ...]
        Forecast horizons in quarters. Default (1, 4, 8, 20).
    series_codes : tuple[str, ...]
        OPENGEM series codes to use as model inputs. The target series is
        expected to be one of them.
    include_constant : bool
        Whether to fit an intercept on the observations. Default True.
    """

    country: str
    target: str
    factors: int = 2
    factor_order: int = 1
    horizons_q: tuple[int, ...] = (1, 4, 8, 20)
    series_codes: tuple[str, ...] = ()
    include_constant: bool = True

    def __post_init__(self) -> None:
        if self.factors < 1:
            raise ValueError("factors must be >= 1")
        if self.factor_order < 0:
            raise ValueError("factor_order must be >= 0")
        if not self.horizons_q or any(h < 1 for h in self.horizons_q):
            raise ValueError("horizons_q must be a non-empty tuple of positive ints")
        try:
            Country(self.country)
        except ValueError as exc:
            raise ValueError(
                f"country must be a canonical opengem_types.Country (ISO-2), "
                f"got {self.country!r}"
            ) from exc
