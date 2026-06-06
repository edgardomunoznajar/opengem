# L205 — Mixed-Frequency Models (MIDAS, MF-DFM)

**Loop**: 205 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

Macroeconomic data is published at mixed frequencies: GDP is quarterly, CPI / payrolls / IP are monthly, term spreads / commodity prices / sentiment surveys are daily. The naive solution — aggregate everything to the lowest frequency (quarterly) and lose information — is what GMT-style econometrics did for decades. Modern macro nowcasting handles mixed frequencies natively.

Two main approaches: **MIDAS regression** (Mixed-Data Sampling, Ghysels-Santa-Clara-Valkanov 2004) and **MF-DFM** (Mixed-Frequency Dynamic Factor Model, Mariano-Murasawa 2003, Banbura-Modugno 2014). This loop picks which we ship at IOC, when each shines, and how mixed-frequency machinery feeds the nowcast horizon.

## The problem

The forecaster wants to nowcast 2026-Q1 USA GDP at the end of February 2026. Available:

- 2025-Q4 GDP (advance estimate, released Jan 30 2026).
- January 2026 monthly indicators (payrolls Feb 7; CPI Feb 13; IP Feb 18; retail sales Feb 16).
- Daily series through Feb 28 2026 (yields, oil, VIX, etc.).

A pure quarterly model wastes the January monthly information. A pure monthly model can't aggregate to GDP. Mixed-frequency models bridge this.

## MIDAS regression

```
y_t (quarterly) = α + β_0 × Σ_{j=0}^{J} w_j(θ) × x_{m(t,j)} + ε_t
```

Where `x_{m(t,j)}` is the monthly series at sub-period j of quarter t, and `w_j(θ)` is a parsimonious weighting function (Almon polynomial, exponential, beta) controlled by a small parameter vector θ.

The weight function shape: typically downward-sloping over months (more recent months matter more) or hump-shaped (recent + 2-3 months back equally informative).

**Strengths**: Simple. Few parameters (typically 3-5 per indicator). Robust to noise. Works well when nowcasting a single target.

**Weaknesses**: Hand-crafted weight function shapes. Limited multivariate generality.

## MF-DFM

The mixed-frequency dynamic factor model treats the lowest-frequency target (GDP) as observable at the quarterly grid but missing at the in-between months. The factor structure runs on the highest frequency (monthly or weekly), with the observation equation linking factors to GDP via a (typically Mariano-Murasawa) 3-month average aggregation rule:

```
factor f_t evolves at monthly frequency.
y_quarterly = f_{t} + f_{t-1} + f_{t-2}    (Mariano-Murasawa aggregation)
y_monthly_indicator_i = λ_i × f_t + idiosyncratic_i
```

Kalman filter handles missing observations naturally. The factor at the end of each month gives a continuously-updating nowcast.

**Strengths**: Multivariate, theory-grounded, handles arbitrary missing patterns. Industry standard (NY Fed Nowcasting, Atlanta Fed GDPNow).

**Weaknesses**: Requires state-space estimation (Kalman + EM); more compute than MIDAS.

## The choice for IOC

**Ship MF-DFM as the primary nowcast variant. Ship MIDAS as a supplementary variant in the BMA mix on the nowcast horizon only.**

Reasoning:

1. **MF-DFM dominates in cross-indicator settings.** OPENGEM's USA panel has ~14 informative monthly indicators per indicator family. Multivariate MF-DFM exploits this; univariate MIDAS does not.
2. **NY Fed Nowcasting open-sources a working implementation.** We can port from `statsmodels` + the NY Fed code release (L032) without inventing. Maintenance burden is low.
3. **MIDAS still earns a seat at the table** because it is robust in low-data regimes (Tier-T countries, fresh indicators). MIDAS-Almon on a single indicator is easier to validate than a full MF-DFM.

The BMA combiner at nowcast horizon weights MF-DFM, MIDAS, DFM-quarterly, and ML-ridge. Empirically MF-DFM ends up ~50-65% of the BMA weight on USA nowcast cells; the rest spreads across the others.

## Implementation

The package `opengem-l3-mfdfm`:

```python
# packages/opengem-l3-mfdfm/src/opengem_l3_mfdfm/model.py

@dataclass
class MFDFMSpec:
    n_factors: int           # typically 1-3
    factor_lag_order: int    # AR(p) on the factor; typically 2
    monthly_indicators: list[str]
    quarterly_indicators: list[str]
    daily_indicators: list[str] | None   # optional; aggregated within-month first
    rng_seed: int

def fit_mfdfm(spec: MFDFMSpec, data: MixedFrequencyData) -> MFDFMPosterior:
    """Kalman filter + EM. Returns factor posterior and loadings."""
    ...

def nowcast(posterior: MFDFMPosterior, as_of: date) -> ForecastDensity:
    """Conditional density of the quarterly target given monthly data through as_of."""
    ...
```

A daily-frequency wrapper aggregates daily series to monthly (mean, last value, or beta-weighted) before feeding the MF-DFM. The aggregation function per daily series is in the model card.

## The "nowcast diary"

A useful side-product of MF-DFM nowcasting is the contribution decomposition: how does each new monthly release move the nowcast?

```
GDP nowcast 2026-Q1:
- 2026-01-30: 2.45% (after 2025-Q4 advance estimate)
- 2026-02-07: 2.48% (+0.03 from payrolls upside, +0.05 from PCE, -0.05 ISM disappointment)
- 2026-02-13: 2.41% (-0.07 from CPI surprise)
- 2026-02-16: 2.43% (+0.02 from retail sales)
- 2026-02-18: 2.39% (-0.04 from IP)
- 2026-02-28: 2.40% (housing starts neutral)
```

Each row decomposes into per-release contributions. The dashboard publishes this nowcast diary as a sidebar panel on the USA GDP page.

The contribution decomposition follows Banbura-Modugno's news decomposition: each new release's contribution = (filtered factor revision × loading on GDP) × Mariano-Murasawa weight.

## Cadence

- MF-DFM is re-fit **monthly** when new releases land for high-information indicators (payrolls, CPI).
- The Kalman filter updates the nowcast on every new release (event-driven).
- Re-estimation of factor loadings is monthly; the Kalman runs continuously.

This is materially different from the quarterly cadence for 4Q+ forecasts. Nowcast wants the fastest cadence; longer horizons want slower, more deliberate re-fits.

## Daily-frequency information

Selected daily series enter via prior aggregation:

| Daily series | Aggregation to monthly | Role |
|---|---|---|
| 10y-3m term spread | Month-end value | Leading indicator for recession-prob nowcast |
| WTI / Brent oil | Monthly average | Inflation nowcast |
| VIX | Monthly average | Financial conditions nowcast |
| TWI USD | Monthly average | Trade balance, inflation nowcast |
| Manufacturing PMI (when monthly) | First-of-month value | Activity nowcast |

The aggregation rule is documented per indicator in the model card.

## Pitfalls and how we handle them

1. **Vintage misalignment.** A monthly release at 12:30 UTC on day X is in the public vintage at 12:30 UTC. A backtest that "uses" the release "at the start of day X" leaks future information. *Mitigation*: every Kalman update timestamps itself, and the backtest engine (R24) respects the exact release timestamps when replaying.

2. **Same-day-release ordering.** When CPI and IP release at the same time, the order of updates does not affect the *final* nowcast at end of day but does affect the decomposition. *Mitigation*: aggregate same-day releases into one update with joint decomposition.

3. **Daily-series drift.** Daily series accumulate noise. *Mitigation*: shrinkage on daily-series loadings; small weights.

4. **Calendar effects.** Releases on holidays / weekends delay. *Mitigation*: hold the prior factor estimate until the next business-day release.

## Methodology page

The nowcast methodology page exposes:

- The factor-extraction equations.
- Indicator list with loadings.
- The Mariano-Murasawa aggregation function.
- The contribution decomposition formula.
- A live "what would move the nowcast" calculator (sensitivity to each upcoming release).

## What this loop produced

- Two-paragraph statement of MIDAS vs MF-DFM.
- Pick: MF-DFM primary, MIDAS supplementary.
- Implementation footprint sketch.
- Nowcast diary (per-release contribution decomposition).
- Cadence: event-driven + monthly re-fit.
- Daily-series aggregation table.
- Pitfalls + mitigations.

## What comes next

- **L206** — real-time vs final estimates question this naturally bridges.
- **L189** — BMA combiner uses the MF-DFM as a nowcast-horizon variant.

## Related

- [[L011-openbb-terminal]] — NY Fed Nowcasting code reference checked.
- [[R14-l3-architecture]] — variants.
- [[L187-forecast-horizons]] — nowcast is first-class.
- [[L189-bma-combiner]] — combiner mix on nowcast cell.
- [[L191-surprise-index]] — built on nowcast-as-baseline.
- [[L206-real-time-vs-final]] — companion.
