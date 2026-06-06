# L191 — Surprise Index per Indicator

**Loop**: 191 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

A *surprise index* compresses, for each indicator × country, the gap between the realised release and the prior consensus expectation. Citigroup popularised the term ("Citi Economic Surprise Index"), but it remains proprietary. This loop specifies OPENGEM's open replication, including methodology, baseline choice, update cadence, and dashboard surfacing.

The surprise index is a *consumer-friendly summary*: one number per country per indicator telling you whether the data have been *beating* or *missing* expectations. It is also a *model input* for the L3 ensemble — surprise is a known predictor of future inflation and growth.

## Methodology

For each `(country, indicator, release_event)`:

```
surprise_z(t) = ( realised(t) - expected(t) ) / σ(t)
```

where:
- `realised(t)` is the first-vintage published value at release.
- `expected(t)` is the pre-release consensus point estimate.
- `σ(t)` is a normalising scale (historical SD of `realised - expected` over a rolling window).

The country-level surprise index `S(t)` is a rolling exponentially-weighted average across the indicator basket:

```
S(t) = Σ_i α_i × EWMA[ surprise_z_i(s) ], s ≤ t
```

with `α_i` the indicator weights (GDP, CPI, payrolls, retail sales, IP, etc.) and EWMA decay half-life of ~3 months. The result is a single zero-mean, unit-variance scalar per country at any moment.

By convention:
- `S(t) > 0` means data have been *beating* expectations.
- `S(t) < 0` means data have been *missing*.
- Magnitude in z-units: ±1 is "noticeable surprise"; ±2 is "regime-shifting".

## Which consensus baseline

Two options for `expected(t)`:

### Option A — A single canonical consensus
Pick one of (Bloomberg, Reuters, MarketEconomics) as the "expectations" baseline. This is what the Citi index does (Bloomberg).

Problem: each of those is paywalled or restricted-license. OPENGEM cannot redistribute them and stay license-clean.

### Option B — OPENGEM's own published nowcast / 1Q forecast
Use OPENGEM's *prior-published* nowcast or 1Q forecast as the expectation, with the realised release as the truth.

```
expected(t) = OPENGEM nowcast for indicator i, vintage just before release t
```

This is what we pick. Reasons:

1. **License-clean.** OPENGEM publishes its forecasts; the comparison is fully open.
2. **Self-consistent.** The surprise index then directly *measures OPENGEM's accuracy* on the latest release — which is also a leaderboard input.
3. **Public.** Anyone can recompute.

This is conceptually similar to *forecast errors* but rolled up into a single z-score per country, suitable for headline display.

### Cross-check option

For Tier-V Core where ECB SPF / WEO / OECD EO publish point forecasts at the right horizon, we also compute a *secondary* surprise index using each as the baseline. This gives the reader the perspective of "vs. consensus" rather than "vs. OPENGEM". The dashboard offers both via a toggle:

- Toggle "OPENGEM expectations" → surprise vs. our nowcast.
- Toggle "WEO expectations" → surprise vs. WEO.
- Toggle "OECD EO expectations" → surprise vs. OECD EO.

## Indicator basket per country

The basket varies by country based on data availability:

| Country | Indicator basket | α weights |
|---|---|---|
| USA | GDP (advance + revised), CPI, core CPI, PCE, payrolls, UR, retail sales, IP, housing starts | 0.20, 0.15, 0.10, 0.10, 0.15, 0.05, 0.10, 0.10, 0.05 |
| Euro area | HICP, GDP (flash + revised), UR, retail sales, IP, PMI | 0.30, 0.25, 0.10, 0.10, 0.15, 0.10 |
| UK | CPI, GDP, UR, retail sales, IP | 0.30, 0.30, 0.10, 0.15, 0.15 |
| Japan | CPI, GDP, machinery orders, retail sales, IP | 0.25, 0.30, 0.15, 0.15, 0.15 |
| BRICS (smaller basket) | CPI, GDP, IP | 0.40, 0.40, 0.20 |

Weights are pinned per epoch and disclosed in the methodology page.

## Update cadence

The surprise index updates **immediately on each indicator release**. Mechanically:

1. The release lands (CPI at 12:30 UTC, payrolls at 13:30 UTC second Friday, etc.).
2. The vintage store records the new value.
3. The surprise component for that indicator is recomputed.
4. The aggregate `S(t)` is recomputed.
5. The dashboard updates and pushes to subscribers.

The dashboard chart shows `S(t)` as a continuous line with each release marked as an event arrow (+0.7 z on payrolls 2026-06-04, etc.). Hover for the event detail.

## API contract

```
GET /v1/surprise?country=USA
→ {
    "schema": "opengem.surprise.v1",
    "country": "USA",
    "computed_at": "2026-06-06T13:35:00Z",
    "current_value": 0.42,
    "current_band": [-1.96, 1.96],
    "interpretation": "USA macro data running slightly above OPENGEM expectations",
    "recent_events": [
      {"date": "2026-06-04T13:30:00Z", "indicator": "payrolls", "realised": 230000, "expected": 195000, "z": 1.1, "delta_S": 0.18},
      {"date": "2026-06-05T12:30:00Z", "indicator": "cpi_yoy", "realised": 2.6, "expected": 2.8, "z": -0.4, "delta_S": -0.07}
    ],
    "history_30d_url": "/v1/surprise/USA/history?days=30",
    "history_3y_url": "/v1/surprise/USA/history?days=1095",
    "model_card_url": "https://opengem.org/methodology/surprise-index"
  }
```

## Dashboard surfacing

Three places the surprise index appears:

1. **Country page header**: large numeral with sign-tinted colour (green > 0, red < 0). "USA Macro Surprise: +0.42" with a sparkline of the last 30 days.
2. **Cross-country heatmap**: every country's current `S(t)` rendered as a coloured tile. Default sort by descending value; click a tile to drill into the country page.
3. **Event ticker**: every fresh release fires a one-line ticker entry: "USA payrolls +230k vs +195k expected (z=+1.1, surprise=+0.18)".

## Use as L3 input

The surprise index per country is also a feature in the L3-ML-RIDGE variant: lagged `S` predicts next-quarter CPI revisions, term-spread shifts, etc. Empirically (Coulombe 2022; Bybee-Kelly-Manela-Xiu) news-and-surprise factors carry forecast skill. We include `S` as a regressor.

## Pitfalls and explicit limitations

1. **Reflexivity.** Using OPENGEM's own nowcast as the baseline means the surprise index measures *OPENGEM's nowcast error*. A persistently-biased nowcast produces a persistently-non-zero surprise index that is *not* about the underlying economy — it is about the model.
   *Mitigation*: dashboard footer always shows the alternative baseline (WEO / OECD EO surprise) for cross-check.

2. **Indicator basket weighting is subjective.** Different weights produce different surprise indices.
   *Mitigation*: publish sensitivity analysis (±0.1 on each weight); show robust trend.

3. **First-vintage vs. final.** A release that is heavily revised later changes the "true" value. We deliberately use the *first-vintage* in the surprise calculation, because that is what was actionable at release time.
   *Mitigation*: footer note that surprise is "vintage 0" not "final".

4. **Holiday + revision events.** Sometimes a single release rewrites months of history. We treat this as a single surprise event keyed to the release date; the magnitude reflects the new vintage vs. prior nowcast at the surface.

## Methodology page commitment

The methodology page at `opengem.org/methodology/surprise-index` exposes the full formula, weights, code, and historical time series, and links to the open-source replication notebook (`prototypes/surprise-index/`).

## What this loop produced

- Formal surprise index formula (z-score + EWMA aggregation).
- Baseline: OPENGEM nowcast (license-clean primary); WEO/OECD EO as secondary toggles.
- Country-specific indicator baskets + weights.
- Immediate update cadence on each release.
- API contract.
- Dashboard surfacing in three places.
- Pitfalls + mitigations.

## What comes next

- **L196** — scenario triggers reference surprise index thresholds.
- **L200** — failure log captures persistently-biased surprise (signal of model rot).

## Related

- [[L181-forecast-object-schema]] — nowcast forecast that serves as the baseline.
- [[L190-consensus-comparison]] — alternative baselines (WEO, OECD EO).
- [[L196-scenario-triggers]] — surprise as trigger input.
- [[L200-failure-log]] — persistent-bias detection.
- [[R06-wider-information-surface]] — news-and-surprise as L3 covariate.
