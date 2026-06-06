# L208 — Tail Forecasts: Left-Tail GDP, Fan Charts

**Loop**: 208 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

Macroeconomic outcomes have asymmetric tails. The left tail of GDP (deep recessions) carries far more economic and policy weight than the right tail (slightly-above-trend growth). The same asymmetry applies to inflation (the right tail of CPI), to unemployment (the right tail), and to fiscal balances (the left tail).

Standard 80% bands (L188) under-communicate tail risk. This loop pins how OPENGEM publishes *tail-focused* forecasts: explicit P5 and P95 tail quantiles, Growth-at-Risk style left-tail metrics, fan-chart visualisation, and downside skew indicators.

## The Growth-at-Risk metric (GaR)

Adrian-Boyarchenko-Giannone (2019) introduced "Growth-at-Risk" — the conditional 5th percentile of the GDP density. Direct analogue of Value-at-Risk in finance, but for macroeconomic outcomes.

```
GaR_5%_{t+h} = inf { y : P(y_{t+h} ≤ y | I_t) ≥ 0.05 }
```

i.e. the level of growth such that there is a 5% chance of being below.

For USA GDP YoY at 4Q-ahead, a typical reading might be:

```
GaR 5%: -0.4%
P50: 2.18%
GaR 95% (upside-at-risk): 4.0%
Left-tail skew: -0.7 (left tail wider than right)
```

The reader sees: "with 5% probability, growth is below -0.4% next year." That is a much sharper communication than "the band is 1.04% to 3.28%."

## What we publish at the tail

For every cell `(country, indicator, horizon)`:

| Field | Source |
|---|---|
| `gar_5_pct` | P5 of the density |
| `gar_95_pct` | P95 of the density |
| `expected_shortfall_5_pct` | Mean of the density below P5 |
| `expected_shortfall_95_pct` | Mean of the density above P95 |
| `left_tail_skewness` | Quantile-based skewness using P5/P50/P95 |
| `right_tail_skewness` | Same |
| `tail_calibration_status` | PIT-KS at tail-only segment (P5 + P95 bins) |

These are exposed in the `forecast.v1` JSON under an optional `tails` block:

```json
{
  "forecast_id": "fcst_2026-06-06_USA_GDP_4Q_...",
  "point": 2.18,
  "bands": {"p10": 1.04, "p25": 1.49, "p50": 2.18, "p75": 2.83, "p90": 3.28},
  "tails": {
    "p5": 0.62,
    "p95": 3.74,
    "expected_shortfall_5_pct": -0.18,
    "expected_shortfall_95_pct": 4.12,
    "kelly_skew_quantile_based": -0.34,
    "tail_calibration_kspvalue": 0.41,
    "gar_methodology": "https://opengem.org/methodology/gar"
  }
}
```

## The fan-chart visualization

The default chart shows the 80% band. The "tail view" toggle expands to a five-band fan chart in the Bank of England tradition:

```
   horizon  P5      P25     P50     P75    P95
   nowcast  outer ──inner──●──inner── outer
   1Q       outer ──inner──●──inner── outer
   4Q       outer ──inner──●──inner── outer
   2Y       outer ──inner──●──inner── outer
   5Y       outer ──inner──●──inner── outer
```

The outer band is P5-P95 (90%); the inner band is P25-P75 (50%). The widening from inner to outer is the *tail thickness*. Asymmetric tails show as a visibly off-centred P50 within the fan.

Bank of England fan-chart colour convention (mute red gradient from inner light to outer dark) is industry-recognised; we follow it for the tail-view to leverage familiarity.

## Asymmetric densities

GDP densities under stress are *left-skewed*: P50 to P5 is a longer distance than P95 to P50. Standard Gaussian variants impose symmetry. To preserve skew, we either:

1. Use a non-Gaussian variant (skew-normal, mixture-of-two-Gaussians, t-with-skew-Student).
2. Use *quantile regression* directly — the Adrian-Boyarchenko-Giannone approach — to estimate P5 and P95 independently of P50.

OPENGEM ships a *quantile regression variant* (`L3-QR`) specifically for tail-focused cells, alongside the Gaussian variants. The combiner (L189) gives QR substantial weight on the GaR cells:

```
For tail-focused cells, the BMA mix is:
  L3-DFM (Gaussian-symmetric)        0.20
  L3-ML-RIDGE                         0.25
  L3-BVAR-LARGE                       0.25
  L3-QR (asymmetric, tail-focused)    0.30
```

QR specialises in the tails; the others handle the central density.

## The Growth-at-Risk page

A dedicated cross-country page (`opengem.org/gar`) shows:

- Bar chart: each country's current GaR 5% at 4Q-ahead.
- Time series: each country's GaR evolution over the past 5 years.
- Cross-section heatmap: GaR 5% × horizon (1Q / 4Q / 2Y / 5Y) × country.

```
Growth-at-Risk (5%) — 4Q-ahead — as of 2026-06-06
─────────────────────────────────────────────────────
USA       -0.4%   ────●─────  (P50: 2.18%)
GBR       -0.8%   ──●───────  (P50: 1.85%)
DEU       -1.2%   ●─────────  (P50: 0.92%)  ← deepest left-tail
FRA       -0.6%   ───●──────  (P50: 1.45%)
JPN        0.2%   ──────●───  (P50: 1.10%)
...
EA       -0.8%   ──●───────  (P50: 1.32%)
```

This is the "where is the next recession risk concentrated" view at a glance.

## Tail calibration

A correctly-calibrated tail forecast hits the realised value below the P5 *exactly* 5% of the time across the OOS window. We test this with a binomial test:

- Expected exceedances: `n × 0.05` (e.g. for n=168 OOS observations, 8.4 exceedances expected).
- Observed exceedances: count of times realised < P5.
- Test: binomial CI; the tail is calibrated if observed lies within the 90% CI.

For the right tail, same test against P95.

If a tail is consistently under-exceeded (fewer than 5% misses below P5), the model is *overstating* tail risk; if consistently over-exceeded, *understating*. Both are calibration failures and trigger PIT-KS warning + remedial review.

## The "GaR moved by X" event

When GaR moves by >0.5 pp from one vintage to the next, the dashboard fires an event ticker:

```
2026-06-06 08:00 UTC — USA GDP 4Q GaR(5%) moved from -0.2% to -0.4%
                       Drivers: long-yield path -0.1, term-spread invert -0.1
```

This is the analogue of the surprise index (L191) but for tail risk. It feeds the scenario engine (L196): a sustained GaR-5% drop is a trigger atom for "deepening downside risk" packs.

## Cross-country tail comovement

The cross-country aggregate left-tail uses the L207 sample-level machinery: world GDP P5 is computed from joint samples across countries. When countries co-move, the world P5 is less extreme than each country's individual P5 (diversification); when countries decouple in crisis, the world P5 reflects the average miss.

## Empirical caveat: tails are harder to calibrate

The left tail of GDP at long horizons (4Q-5Y) is empirically the hardest cell to calibrate in macro forecasting. Historical recessions are sparse; the OOS sample includes few left-tail events; estimation variance is high.

OPENGEM's posture: publish tails *transparently* with PIT testing; flag calibration failure; do not pretend to have tight tails when we don't. The honest tail-publication discipline is itself a competitive differentiator — Bloomberg and Stratfor systematically over-promise on tail risk.

## Counterfactual-tail link

Tail forecasts are descriptive. When we describe the tail, we are saying "5% probability of <-0.4%". The counterfactual scenarios (L210) build on this by saying "*if* shock X occurs, *then* the conditional density shifts to ...". The two are complementary; tail forecasts describe the marginal density; counterfactuals describe conditional ones.

## What this loop produced

- Growth-at-Risk metric definition.
- `tails` block in forecast.v1 schema.
- Five-band fan-chart UX.
- L3-QR variant added for tail-focused cells.
- Cross-country GaR page.
- Tail calibration test (binomial exceedance).
- GaR-moved-by-X event ticker.
- Caveat on calibration difficulty.

## What comes next

- **L210** — counterfactual scenarios complement marginal tail descriptions.
- **L196/L197** — scenario triggers can include GaR thresholds.

## Related

- [[L188-band-quantiles]] — extends the band scheme.
- [[L189-bma-combiner]] — combiner mix with L3-QR.
- [[L193-calibration-plots]] — tail-specific PIT test.
- [[L207-density-aggregation]] — joint samples for world-tail aggregates.
- [[L210-counterfactual-scenarios]] — conditional companions to marginal tails.
- [[L195-forecast-ui-spec]] — fan-chart toggle.
