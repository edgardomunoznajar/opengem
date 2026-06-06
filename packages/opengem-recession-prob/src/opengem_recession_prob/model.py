"""TermSpreadModel — probit fit of recession indicator on lagged term spread.

Mathematical model:
    P(recession_{t+h} = 1 | spread_t) = Phi(alpha + beta * spread_t_bp)

where Phi is the standard normal CDF, spread_t_bp is the 10y-3m spread in basis
points (10y minus 3m, both in percent times 100), and h is the horizon
(typically 12 months).

We provide a closed-form Phi (via erf from math), pre-fitted Bauer-Mertens-style
coefficients for the US 12-month horizon, and a simple IRLS estimator if you
want to refit. No numpy/scipy dependency for IOC.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date

from opengem_types import Basis, Conditional, ConfidenceKind, Country


def _phi(x: float) -> float:
    """Standard normal CDF via math.erf."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


@dataclass(frozen=True, slots=True)
class TermSpreadModel:
    """Calibrated probit model parameters.

    Convention: `spread_bp` is (10y - 3m) in basis points. Positive = steeper.
    Negative = inverted = recession signal.
    """

    country: Country
    horizon_months: int
    alpha: float  # intercept
    beta: float  # coefficient on spread_bp
    auc: float | None = None  # in-sample AUC (calibration reference)
    sample_start: date | None = None
    sample_end: date | None = None
    fit_method: str = "bauer_mertens_replication"

    def predict(self, spread_bp: float) -> float:
        """Return P(recession in next horizon_months months)."""
        z = self.alpha + self.beta * spread_bp
        return _phi(z)


# Bauer-Mertens (FRBSF 2018-07) US 12m parameters, approximated from their probit
# coefficients on monthly data 1972-01..2018-07 with spread = DGS10 - DGS3M.
# The coefficients here are within the published confidence bands; users should
# refit on current data via fit_probit() if exact replication is required.
BAUER_MERTENS_US_PARAMS = TermSpreadModel(
    country=Country.US,
    horizon_months=12,
    alpha=-0.55,
    beta=-0.014,
    auc=0.89,
    sample_start=date(1972, 1, 1),
    sample_end=date(2018, 7, 31),
)


@dataclass(frozen=True, slots=True)
class RecessionProbabilityResult:
    """Typed result of a recession-probability query."""

    country: Country
    as_of: date
    horizon_months: int
    probability: float
    term_spread_bp: float
    model_id: str  # e.g., 'bauer_mertens_us_12m_v1'
    auc: float | None = None
    notes: str = ""
    inputs_hash: str | None = None

    def to_conditional(self) -> Conditional[float]:
        """Wrap as a Conditional[float] for the OPENGEM epistemic contract."""
        caveats: list[str] = [
            "Term-spread signal is US-strongest; non-US calibrations have lower AUC",
            "Probit assumes the historical regime; structural breaks degrade signal",
        ]
        framing = (
            f"Recession probability {self.probability:.0%} over next "
            f"{self.horizon_months} months — this could happen based on the "
            f"term-spread signal (spread {self.term_spread_bp:.0f}bp), "
            f"per {self.model_id}"
        )
        return Conditional(
            value=self.probability,
            basis=Basis(
                model_or_method=self.model_id,
                inputs_description=(
                    f"10y-3m term spread = {self.term_spread_bp:.1f}bp, "
                    f"as of {self.as_of.isoformat()}"
                ),
                as_of=self.as_of,
                citations=("Bauer & Mertens (2018) FRBSF Economic Letter 2018-07",),
                caveats=tuple(caveats),
            ),
            confidence=ConfidenceKind.POINT,
            framed_as=framing,
            conditional_on=(
                f"current term spread = {self.term_spread_bp:.0f}bp",
                "the historical signal-to-recession mapping continues to hold",
            ),
        )


def recession_probability(
    spread_bp: float,
    *,
    as_of: date,
    model: TermSpreadModel = BAUER_MERTENS_US_PARAMS,
    model_id: str | None = None,
    notes: str = "",
) -> RecessionProbabilityResult:
    """Compute recession probability for a country given current term spread."""
    if model_id is None:
        model_id = f"{model.country.value.lower()}_{model.horizon_months}m_{model.fit_method}"
    return RecessionProbabilityResult(
        country=model.country,
        as_of=as_of,
        horizon_months=model.horizon_months,
        probability=model.predict(spread_bp),
        term_spread_bp=spread_bp,
        model_id=model_id,
        auc=model.auc,
        notes=notes,
    )


# Optional re-fitting via IRLS (no scipy dependency)
def fit_probit_irls(
    spreads_bp: list[float],
    recession: list[int],
    *,
    max_iter: int = 50,
    tol: float = 1e-6,
) -> tuple[float, float]:
    """Newton-Raphson IRLS fit of probit on (spread_bp, recession_indicator) data.

    Returns (alpha, beta). Simple, no autograd. Stable for the kind of data
    here. If non-convergent, returns last iterate.
    """
    if len(spreads_bp) != len(recession):
        raise ValueError("spreads_bp and recession must be same length")
    n = len(spreads_bp)
    if n < 10:
        raise ValueError("need at least 10 observations")

    # Map y in {0,1}; ensure dtype
    y = [float(v) for v in recession]
    x = [float(v) for v in spreads_bp]

    alpha, beta = 0.0, 0.0

    for _ in range(max_iter):
        # Linear predictor
        eta = [alpha + beta * x_i for x_i in x]
        # Probit link
        p = [max(min(_phi(z), 1.0 - 1e-9), 1e-9) for z in eta]
        # Derivatives
        phi_z = [_normal_pdf(z) for z in eta]
        # Working response
        w = [(phi_z[i] ** 2) / (p[i] * (1.0 - p[i])) for i in range(n)]
        z_star = [
            eta[i] + (y[i] - p[i]) / phi_z[i] if phi_z[i] > 1e-9 else eta[i]
            for i in range(n)
        ]

        # Weighted least squares for (alpha, beta)
        sw = sum(w)
        swx = sum(w[i] * x[i] for i in range(n))
        swxx = sum(w[i] * x[i] * x[i] for i in range(n))
        swz = sum(w[i] * z_star[i] for i in range(n))
        swxz = sum(w[i] * x[i] * z_star[i] for i in range(n))

        det = sw * swxx - swx * swx
        if abs(det) < 1e-12:
            break
        new_alpha = (swxx * swz - swx * swxz) / det
        new_beta = (sw * swxz - swx * swz) / det

        if abs(new_alpha - alpha) + abs(new_beta - beta) < tol:
            alpha, beta = new_alpha, new_beta
            break
        alpha, beta = new_alpha, new_beta

    return alpha, beta


def _normal_pdf(z: float) -> float:
    """Standard normal density."""
    return math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
