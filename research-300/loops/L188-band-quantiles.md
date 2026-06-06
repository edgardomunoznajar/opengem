# L188 — Bands: P10/P50/P90 vs P5/P25/P50/P75/P95

**Loop**: 188 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

Two band schemes are mainstream in macro forecasting:

- **80% band** = P10 / P50 / P90 (three quantiles, two shaded regions on a chart, or one fan)
- **90% + 50% nested fan** = P5 / P25 / P50 / P75 / P95 (five quantiles, two nested shaded regions, the classic Bank of England fan chart)

Pick one as the canonical chart default. Expose both via API. Defend the choice with a concrete reading-time argument.

**Decision: canonical chart default is the 80% band (P10 / P50 / P90). The API always returns all five quantiles (P10 / P25 / P50 / P75 / P90); the BoE-style five-quantile (P5 / P25 / P50 / P75 / P95) is available via a query parameter and a toggle on the chart UI.**

## Why the 80% band as default

Three reasons, each load-bearing:

### 1. The 80% interval matches the operational language

When CFOs and analysts say "the 80% confidence range for next year's growth is 1.5% to 3.2%", they mean P10-P90. Central banks talk in 70% (Bank of England), 80% (Riksbank, ECB), or 90% (Federal Reserve SEP) bands; the *plurality* of major institutions uses 80%. Choosing 80% maximises cross-comparability with peer publications.

### 2. The default chart has to be readable at 320 px

The dashboard is responsive and renders on phones. A fan chart with five nested bands is unreadable below ~500 px; a single 80% band is readable at 320 px. The default has to work for the median visitor, who is mobile.

### 3. P5 and P95 are statistically frail at our sample sizes

Our V&V matrix evaluation windows are 40-150 OOS observations per cell. P5/P95 quantile calibration requires more data than P10/P90 to be tight. We can compute P5 and P95 internally (from the density), but our *honest* calibration statement is the 80% band. PIT-KS tests pass more reliably on the 80% interval than on the 95% interval in our regime.

## Why the API exposes both

The API surface is a JSON contract — readers do not all want the same quantile cut. Three audiences:

- **Dashboard chart**: P10/P50/P90 (the 80% band) by default; user toggle expands to the 90% fan with P25/P75 nested.
- **Spreadsheet user pasting into Excel**: probably wants P50 as the point and P10/P90 as the bracket.
- **Quant researcher**: wants the full sample density (Parquet of N=10,000 draws), can compute arbitrary quantiles themselves.

The `forecast.v1` JSON `bands` block carries five quantiles (P10/P25/P50/P75/P90); the `density.samples_url` Parquet carries the full 10,000-draw sample. Researchers compute their own P5/P95 from the sample.

## The chart's quantile rendering

Default mode:

```
   2026-Q1 ───────●───────  P50 = 2.18
                  │
   P90 ──────────────       P10 ────
   shaded 1.04 ────── 3.28  (80% band)
```

Expanded mode (user clicks "fan view"):

```
   2026-Q1 ───────●───────  P50 = 2.18
                  │
   P75 ─────●─────             P25 ─────
   inner shaded 1.49 ── 2.83  (50% band)
   outer shaded 1.04 ── 3.28  (80% band)
```

The BoE-style P5/P95 cut is available as a third toggle ("90% fan"). We compute these from the density samples on demand. Three modes, one canonical default.

## Why not just P50 (the point)

A dashboard that only shows the central forecast is a dashboard that hides its uncertainty. That is exactly what L001 (OPENGEM publishes its mistakes) is against. The default cannot be P50-only.

## Why not P25/P75 only (the 50% band)

The 50% band is too narrow to communicate uncertainty honestly. A median user looking at a 50% band reads it as "the forecast" and ignores tail risk. The 80% band is wide enough to force the reader to register that the central number is one possibility among many.

## Numerical examples for context

For the USA GDP-4Q forecast from L181:

| Quantile cut | Band on the chart | Width |
|---|---|---|
| 50% (P25-P75) | 1.49% to 2.83% | 1.34 pp |
| 80% (P10-P90) | 1.04% to 3.28% | 2.24 pp |
| 90% (P5-P95)  | 0.62% to 3.74% | 3.12 pp |
| 95% (P2.5-P97.5) | 0.18% to 4.18% | 4.00 pp |

Width grows roughly as expected for a near-Gaussian density. The 80% band of 2.24 pp width is wide enough to register as uncertain but not so wide that the central tendency is invisible.

## Color and accessibility

The chart's band colour is a single hue with two opacity levels (only one used in default mode):

- P10-P90 shaded region: 30% opacity teal (matches the OPENGEM brand colour palette from L131).
- P25-P75 (when expanded): 60% opacity teal stacked on top.
- P50 line: solid teal, 2 px stroke.

Colour is *not* the only encoding — width is the dominant cue. Colourblind-safe by design. The legend explicitly labels "80% band" so no inference is needed about what the shaded region means.

## Cross-quantile coherence

A forecast's density must satisfy `P10 ≤ P25 ≤ P50 ≤ P75 ≤ P90`. The BMA combiner (L189) produces mixtures whose quantiles are extracted by numerical inversion; we validate monotonicity at write time and reject any forecast that violates it. This catches numerical instability before publication.

## When to deviate from the default

Some indicators have a natural single-sided uncertainty:

- **Recession probability**: 0-1, displayed as a thick line with a calibration band, not P10/P90.
- **Unemployment near a floor**: bounded below by ~3%, so density is asymmetric; we still publish P10/P90 but the chart shows the asymmetry clearly.
- **Categorical forecasts** (regime classifiers): no bands; display each class probability as a stacked area instead.

These deviations are encoded in the indicator's `display_hint` field in the schema metadata, and the chart renderer picks the appropriate primitive.

## What this loop produced

- Decision: canonical default is P10/P50/P90; API serves five quantiles plus full samples.
- Three-way defence: institutional alignment, mobile readability, statistical reliability.
- Chart-rendering spec for default + expanded modes.
- Colour + accessibility constraints.
- Cross-quantile coherence validation rule.

## What comes next

- **L195** — chart UI consuming this band convention.
- **L189** — combiner producing the mixture density these quantiles come from.
- **L208** — tail forecasts (left-tail GDP) that extend this with fan-chart treatment.

## Related

- [[L181-forecast-object-schema]] — `bands` block carrying these quantiles.
- [[L195-forecast-ui-spec]] — chart UI.
- [[L208-tail-forecasts]] — fan-chart extensions for catastrophic tails.
- [[L189-bma-combiner]] — density source.
- [[R08-vv-matrix-detail]] — calibration tests at the 80% level.
