# L166 — Recession-Probability Tile

**Loop**: 166 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

The recession-probability tile is the single most demanded artifact in macro. Every research desk produces one. OPENGEM's version is publicly cited per country, vintaged, and methodology-open.

We adopt the Bauer-Mertens (FRBSF) framework as our default, blend with a yield-curve baseline (Estrella-Mishkin) and a regime-classifier (HMM on growth + inflation), and surface as a tile per Tier-V country.

## The tile (atom)

```
   ┌─────────────────────────────────────────────┐
   │ 🇺🇸 USA  Recession probability, 12mo ahead  │
   │ ─────────────────────────────────────────── │
   │                                               │
   │           38%                                 │
   │       elevated                                │
   │                                               │
   │  ▣▣▣▣▣▣▣░░░░░░░░░░░░░░░░  0–100%             │
   │                                               │
   │  ─╱╲╱──╲╱──╱──╲                              │
   │  12mo history                                 │
   │                                               │
   │  Drivers: term spread (-0.42)                 │
   │           credit spreads (+58bp)              │
   │           manufacturing PMI (47.2)            │
   │                                               │
   │  Methodology: Bauer-Mertens blend             │
   │  Vintage: 2026-06-04                          │
   │  [ open the recession page → ]                │
   └─────────────────────────────────────────────┘
   width: ~360px, height: ~260px
```

## The hero number

The hero number is the model-blended probability of recession within 12 months. Bands:

- 0–10%: `calm` — green badge
- 10–25%: `monitor` — yellow badge
- 25–50%: `elevated` — orange badge
- 50–75%: `likely` — red badge
- 75%+: `imminent` — dark-red badge with siren icon

We never display "definite" — even at 95% there's uncertainty.

## The methodology blend

OPENGEM's tile is a weighted blend of:

| Model | Weight | Reference |
|---|---|---|
| Bauer-Mertens (yield curve, probit) | 40% | FRBSF |
| Estrella-Mishkin classical (term spread) | 20% | NY Fed |
| Regime classifier (HMM on GDP + inflation) | 25% | OPENGEM L214 |
| Credit-spread surge classifier | 15% | OPENGEM custom |

The weights are calibrated against historical recession outcomes via Brier scoring. They're public, vintaged, and changeable — when changed, the prior version stays cited.

## The drivers

The tile lists the top 3 drivers contributing to the current probability. These come from the model's marginal contributions (similar to SHAP for the probit / HMM ensemble).

```
   Drivers:
    • Term spread: -0.42 (contributes +18pp to base rate)
    • Credit spreads: +58bp (contributes +8pp)
    • Manufacturing PMI: 47.2 (contributes +5pp)
   Base rate (unconditional): 7%
```

Hover each driver: tooltip with the indicator's series link and a mini-spark.

## The history sparkline

12-month history of the probability itself. Helps the user see "is it rising or falling."

## The recession page (drilldown)

Click "open recession page" → routes to `/recession?country=usa`:

```
   USA recession probability — full view
   ────────────────────────────────────────
   [ Full chart with bands ]
   - Current model probability (blended)
   - Each model's probability separately
   - Historical actual recessions shaded (NBER + OPENGEM-curated)
   - Calibration plot (predicted vs actual)
   - Brier score and log-loss history
   - Methodology cards (each model)
```

This is the canonical recession page per country.

## Cross-country recession grid

The world page (L161) has a "recession-prob heatmap" tab:

```
   Recession probability heatmap (12mo)
   ────────────────────────────────────
   USA   38%   ▣▣▣▣▣▣▣░░░░░
   GBR   42%   ▣▣▣▣▣▣▣▣░░░░
   DEU   31%   ▣▣▣▣▣▣░░░░░░
   FRA   28%   ▣▣▣▣▣░░░░░░░
   ITA   45%   ▣▣▣▣▣▣▣▣▣░░░
   JPN   12%   ▣▣░░░░░░░░░░
   CAN   34%   ▣▣▣▣▣▣▣░░░░░
   ...
```

Sorted by probability. Hover any row → its tile. Click → recession page.

## "Recession nowcast" vs "12mo ahead"

The tile defaults to 12-month-ahead. Toggle to:
- "Nowcast" (am I in one right now)
- "6mo ahead"
- "12mo ahead" (default)
- "24mo ahead"

The full recession page shows all horizons stacked.

## The probability over horizon chart

The drilldown has a "term-structure of recession probability":

```
       %
        │
    50%─│      ──────
        │  ────
    40%─│──
        │
    30%─│
        │
   ─────┴──────────────────
       Now   6mo  12mo  24mo
```

Bauer-Mertens framework gives this naturally. Useful for "is it imminent or just rising."

## Calibration plot (for the curious)

The drilldown shows the model's calibration:

```
   Predicted prob vs actual recession frequency
   (1990–2025 historical bins)

       Actual
   1.0 │     ●
       │  ●
   0.5 │● ●
       │●
   0.0 │─────────────
       0.0    1.0  Predicted
```

A well-calibrated model has dots on the diagonal. We show whether OPENGEM-blend is over or under-confident.

## Coverage

Tier-V countries (full recession-prob): USA, EU-block (DEU, FRA, ITA, ESP, NLD), GBR, JPN, CAN, AUS, KOR, CHN. ~12 countries.

Tier-IV (yield-curve-based only): another 15 countries with sufficient yield curve data.

Tier-III (regime-based only): more countries with GDP + inflation but no usable yield curve.

Below Tier-III: "insufficient data" with a coverage-gap badge.

## URL contract

```
/recession?country=usa
/recession?country=usa&horizon=24mo
/recession?country=usa&vintage=2024-09-15
/recession?compare=usa,gbr,deu
```

## Editorial: the "watch list"

A curated list of countries OPENGEM editorial flags as "on watch" — based on probability crossing a threshold (>50%) or a sharp acceleration (>15pp in 4 weeks).

The accountability page (L175) tracks how many on-watch countries actually entered recession.

## Methodology disclosure

Every probability comes with the methodology pop-up (L172):

```
   ┌────────────────────────────────────────┐
   │  Methodology: Bauer-Mertens blend       │
   │  ──────────────────────────────────    │
   │  This recession probability blends      │
   │  four models calibrated against         │
   │  historical NBER recessions.            │
   │                                          │
   │  Each model and its weight is open:     │
   │   • Bauer-Mertens (40%)                  │
   │   • Estrella-Mishkin (20%)               │
   │   • Regime HMM (25%)                     │
   │   • Credit spread classifier (15%)      │
   │                                          │
   │  Weights calibrated 2025-12 via Brier    │
   │  scoring on 1990–2025 history.          │
   │                                          │
   │  [Full methodology →]                   │
   └────────────────────────────────────────┘
```

## The accountability arc

When the time horizon passes, every recession-probability vintage is scored:

```
   Forecast made 2024-Q3, 12mo horizon
   Probability: 24%
   Actual: no recession (yet, as of 2025-Q3)
   Brier: 0.058  (well-calibrated)
   Was OPENGEM in the bottom half of forecasters? No, top quartile.
```

Lives on the accountability page (L175). The track record is public.

## Cross-cohort tile

A "world recession-prob composite" — the population-weighted average across Tier-V countries. Shown on the home page:

```
   World recession prob (12mo, population-weighted): 33%
   ─╱╲╱──╲╱──╱──╲
```

Click → routes to a cross-country comparison view.

## What the tile is NOT

- Not a binary "recession yes/no" toggle. Probability with bands.
- Not just one model. The blend is the point.
- Not Goldman Sachs's number. It's open, vintaged, and we publish when wrong.

## Implementation

- Tile component: server-rendered, hydrated for the sparkline
- Drivers: computed server-side from model marginals
- Calibration plot: D3
- Endpoint: `/api/recession?country=usa&horizon=12mo&vintage=latest`
- Cache: weekly TTL (recession-prob doesn't change daily; we refresh on data updates)

## Empty / degraded states

If insufficient data:

```
   ┌─────────────────────────────────────────────┐
   │ 🇲🇲 MMR  Recession probability — unavailable │
   │                                               │
   │  Insufficient time series for a calibrated    │
   │  recession-probability model.                  │
   │  We track: GDP, CPI, USD                       │
   │  Missing: yield curve, credit spreads          │
   │                                               │
   │  [ Request coverage ] [ Use regime classifier ]│
   └─────────────────────────────────────────────┘
```

The "Use regime classifier" link runs the HMM-only path (Tier-III). Lower confidence but available.
