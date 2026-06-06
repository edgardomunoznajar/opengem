# L219 — Labor Market Page

**Loop**: 219 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

Labor is the macro indicator with the **highest information density per data release**. The US BLS Employment Situation report (NFP, unemployment, average hourly earnings, participation, all the cuts) moves markets twice a month and is read by every central banker. Cross-country, the OECD LFS (Labour Force Survey) harmonizes unemployment + participation + wage growth + hours for ~40 countries. **And yet the BLS report, the OECD LFS, and the central-bank wage-tracker data live in three separate, ugly silos.** Bloomberg ECST gets you the headline; nothing public makes it digestible.

OPENGEM's labor market page is the page that beats Bloomberg's ECST function for non-pros. Damian (the YouTuber) screenshots its monthly NFP card, Marcus (the FT journalist) embeds its real-wage chart, Nadia (the SWF analyst) cites its cross-country participation-gap matrix. It is the page that, on the first Friday of every month at 8:30am ET, becomes the *receipt* for the NFP narrative.

This loop **decides** the structure (US-deep + cross-country shallow), the visualizations (release card + Phillips curve + Beveridge curve + cross-country grid), and the wage-data integration.

## The structure: US-deep + cross-country shallow

OPENGEM acknowledges what every macro shop knows but rarely says out loud: **the US labor market is 4x more granular than any other country's** because BLS publishes JOLTS, ECI, Employment Cost Index, demographic cuts, industry cuts, and the Establishment Survey + Household Survey distinction. So we build a **US-deep** view (matching Bloomberg ECST depth) and a **cross-country shallow** view (OECD LFS-equivalent for ~40 countries). Both are first-class.

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ LABOR MARKET                                                         │
│ US deep (BLS) + cross-country (OECD LFS). Vintaged, real-time-aware. │
└──────────────────────────────────────────────────────────────────────┘

[Major view tabs]
 [US deep]   [Cross-country grid]   [Real wages]   [Beveridge curve]   [Phillips curve]

[Selectors — vary by view]
 [Frequency: M / Q]   [Real / Nominal wages]   [Country group: G20 ▼]   [Vintage ▼]

╔══════════════════════════════════════════════════════════════════════╗
║ US DEEP VIEW                                                          ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Release card (after each NFP Friday) ─────────────────────────────┐
│ ╔════════════════════════════════════════════════════════════════╗ │
│ ║ MAY 2026 EMPLOYMENT SITUATION (released 2026-06-05 8:30am ET)   ║ │
│ ║                                                                 ║ │
│ ║ Nonfarm payrolls: +218k    consensus +180k     SURPRISE +38k 📈 ║ │
│ ║ Unemployment rate: 3.9%    consensus 4.0%      SURPRISE -0.1pp  ║ │
│ ║ AHE m/m: +0.3%             consensus +0.3%     IN LINE          ║ │
│ ║ AHE y/y: +4.0%             consensus +4.0%     IN LINE          ║ │
│ ║ Participation: 62.6%       consensus 62.6%     IN LINE          ║ │
│ ║                                                                 ║ │
│ ║ Revisions:  Apr +185k → +175k  ▼ -10k                            ║ │
│ ║             Mar +245k → +258k  ▲ +13k                            ║ │
│ ║                                                                 ║ │
│ ║ OPENGEM nowcast (issued 2026-06-03): +198k  ERROR: -20k          ║ │
│ ║ Bloomberg consensus + survey:                                    ║ │
│ ║   Consensus: +180k  ERROR: -38k                                  ║ │
│ ║   ATL GDPNow-implied: +210k  ERROR: -8k                          ║ │
│ ║                                                                 ║ │
│ ║ One-sentence narrative: "Hiring re-accelerated in May, led by    ║ │
│ ║ healthcare and government, while revisions trimmed the prior     ║ │
│ ║ two months by a net -10k."                                       ║ │
│ ╚════════════════════════════════════════════════════════════════╝ │
└─────────────────────────────────────────────────────────────────────┘

┌─ NFP time-series chart (5y) ───────────────────────────────────────┐
│  Bars: monthly NFP (+ green / - red)                                │
│  Line: 3m moving average                                            │
│  Annotations: COVID, BoG hike cycles, debt ceiling                  │
│  Click any bar → opens vintage panel showing initial + revisions    │
└─────────────────────────────────────────────────────────────────────┘

┌─ Demographic cuts grid ────────────────────────────────────────────┐
│                Unemp %  Δ 12m  Particip %  Δ 12m   Avg unemp wks    │
│ All workers    3.9%     +0.1   62.6%       +0.3    19.4              │
│ Men            3.7%     +0.0   67.7%       +0.2    20.1              │
│ Women          4.1%     +0.2   58.0%       +0.4    18.5              │
│ White          3.4%     +0.1   62.1%       +0.2    18.7              │
│ Black          5.8%     +0.3   63.9%       +0.5    22.1              │
│ Hispanic       4.4%     +0.0   66.8%       +0.4    19.8              │
│ Age 16-19      11.2%    +0.5   37.5%       -0.2    11.9              │
│ Age 25-54      3.2%     +0.0   83.4%       +0.4    19.0              │
│ Age 55+        2.9%     +0.1   38.7%       +0.2    23.4              │
│ College+       2.0%     +0.0   72.5%       +0.3    16.7              │
│ HS only        4.5%     +0.2   58.0%       +0.1    21.4              │
└─────────────────────────────────────────────────────────────────────┘

┌─ JOLTS panel ──────────────────────────────────────────────────────┐
│  Openings   Hires    Quits    Layoffs   Quits/Layoffs (vitality)   │
│  8.0M       5.6M     3.4M     1.6M      2.1x (healthy threshold 2.0)│
│  Δ 12m: -0.5M / -0.2M / -0.3M / -0.1M                               │
│  Beveridge curve panel (link to view)                               │
└─────────────────────────────────────────────────────────────────────┘
```

```
╔══════════════════════════════════════════════════════════════════════╗
║ CROSS-COUNTRY GRID VIEW                                               ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Sortable grid (OECD LFS-equivalent) ──────────────────────────────┐
│ Country │Unemp%│Δ 12m│Particip%│Δ 12m│Real wage Δ12m│Trough since│
│ USA     │ 3.9  │ +0.1│ 62.6    │ +0.3│ +1.4         │ 2023m4     │
│ EUR     │ 6.4  │ -0.2│ 65.5    │ +0.4│ +1.1         │ 2024m3     │
│ JPN     │ 2.5  │ +0.0│ 63.1    │ +0.2│ +0.3         │ 2024m2     │
│ GBR     │ 4.4  │ +0.4│ 63.2    │ -0.1│ +1.8         │ 2024m6     │
│ DEU     │ 3.5  │ +0.3│ 76.8    │ +0.5│ +1.6         │ 2023m11    │
│ ESP     │ 11.0 │ -0.4│ 59.4    │ +0.3│ +1.2         │ 2024m1     │
│ FRA     │ 7.2  │ +0.1│ 68.4    │ +0.4│ +0.8         │ 2024m2     │
│ ITA     │ 7.0  │ -0.5│ 58.1    │ +0.6│ +0.9         │ 2024m4     │
│ KOR     │ 2.9  │ +0.0│ 64.2    │ +0.3│ +1.5         │ 2024m1     │
│ AUS     │ 4.1  │ +0.6│ 66.7    │ +0.2│ +1.0         │ 2024m3     │
│ ...                                                                  │
│ Sort by: unemp / particip / real wage / change                       │
└─────────────────────────────────────────────────────────────────────┘
```

```
╔══════════════════════════════════════════════════════════════════════╗
║ REAL WAGES VIEW                                                       ║
╚══════════════════════════════════════════════════════════════════════╝

  Cross-country real-wage growth, 5y stacked:
   - Nominal wage growth
   - minus CPI inflation
   = Real wage growth

  Visualization: per country, two-line chart (nominal vs CPI), with
  shaded area where real growth was negative.
  Grid: 6×6 small multiples for top economies.
  Per-country: link to detail.
```

```
╔══════════════════════════════════════════════════════════════════════╗
║ BEVERIDGE CURVE VIEW                                                  ║
╚══════════════════════════════════════════════════════════════════════╝

  Vacancy rate (Y) vs unemployment rate (X) for last 10y
  Single point = latest month, colored bright orange
  Trail = previous 24 months, fading from light to dark
  Annotation: "current curve is X.X% to the right of pre-COVID curve"
  Cross-country: small-multiple grid (US, EUR, GBR, JPN, AUS)

  This is the chart that tells the user whether the labor market is
  tightening on the supply side (curve shift right) or normalizing
  (movement along the curve).
```

```
╔══════════════════════════════════════════════════════════════════════╗
║ PHILLIPS CURVE VIEW                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

  Inflation (Y) vs unemployment rate (X), 25y
  Recent points larger and colored, distant points small and grey
  Slope: estimated via rolling regression, shown as label

  Each country gets its own Phillips curve panel.
  Reveals whether the curve has flattened (Y-axis insensitive to X)
  or steepened (rapid wage→inflation pass-through).
```

## The release card — the killer feature

The release card is the page's *headline product*. On NFP morning, every macro newsletter regurgitates the same numbers from the BLS PDF. OPENGEM's release card:

1. **Includes OPENGEM's own pre-release nowcast** (issued ~48h before, with prediction interval).
2. **Shows the error** (vs OPENGEM, vs Bloomberg consensus, vs Atlanta Fed GDPNow-implied).
3. **Surfaces revisions** to prior-2-month numbers — the most overlooked part of the release.
4. **Auto-generates the one-sentence narrative** with a citation to underlying data.
5. **Renders to OG-image** so Damian can paste it on X / Substack without manual editing.

This is the *single page that ships every month with measurable engagement*. If the OG-image card gets retweeted 200x on NFP morning, OPENGEM has earned its top-of-funnel.

## Data sources / adapter dependencies

| Input | Source | Adapter | Status |
|---|---|---|---|
| US BLS Employment Situation | BLS API | `opengem-data-bls` ✅ | ready |
| JOLTS | BLS JOLTS API | `opengem-data-bls` (extend) | partial |
| Establishment vs Household discrepancy | BLS internal series | `opengem-data-bls` extension | partial |
| OECD LFS | OECD ORDRA | `opengem-data-ordra` ✅ | ready |
| EU LFS | Eurostat | `opengem-data-eurostat` ⚠️ NOT YET BUILT | gap |
| ECI (Employment Cost Index) | BLS | `opengem-data-bls` extension | partial |
| Beveridge curve vacancy data | BLS JOLTS (US), Indeed Hiring Lab (cross-country) | `opengem-data-indeed` ⚠️ NOT YET BUILT | partial |
| Wage trackers | Atlanta Fed Wage Growth Tracker, ECB Wage Tracker | `opengem-data-atl-fed` ⚠️ NOT YET BUILT, `opengem-data-ecb` ⚠️ | gap |
| Real wages (deflation) | local CPI joins | already via `opengem-data-bls`, `opengem-data-ecb` | partial |

**Identified gaps**: Eurostat, Indeed Hiring Lab, Atlanta Fed Wage Tracker. Eurostat is the biggest — EU labor data quality is critical for the cross-country view.

## JSON contract — NFP release card

```json
{
  "release_id": "us-nfp-2026-05",
  "publication_date": "2026-06-05T08:30:00-04:00",
  "vintage": "2026-06-05",
  "headline_numbers": {
    "nfp_thousands": 218,
    "unemployment_rate_pct": 3.9,
    "ahe_mom_pct": 0.3,
    "ahe_yoy_pct": 4.0,
    "participation_pct": 62.6
  },
  "consensus": {
    "nfp_thousands": 180,
    "unemployment_rate_pct": 4.0,
    "ahe_mom_pct": 0.3,
    "ahe_yoy_pct": 4.0,
    "participation_pct": 62.6
  },
  "surprise": {
    "nfp_thousands": 38,
    "unemployment_rate_pct": -0.1,
    "ahe_yoy_pct": 0
  },
  "opengem_nowcast_pre_release": {
    "nfp_thousands": 198,
    "p10_p90": [165, 240],
    "issued_at": "2026-06-03T12:00:00-04:00",
    "error_pp": 0.0,
    "error_thousands": -20
  },
  "revisions_to_prior": [
    {"period": "2026-04", "prior_value": 185, "new_value": 175, "delta": -10},
    {"period": "2026-03", "prior_value": 245, "new_value": 258, "delta": +13}
  ],
  "demographic_cuts": [...],
  "auto_narrative": "Hiring re-accelerated in May, led by healthcare and government, while revisions trimmed the prior two months by a net -10k.",
  "og_image_url": "https://opengem.org/og/labor-nfp-2026-05.png",
  "cite_this": "https://opengem.org/labor/us/release/2026-05?v=2026-06-05"
}
```

## What this loop produced

- The US-deep + cross-country-shallow split as the page's architecture.
- The release card with OPENGEM nowcast + consensus + error + revisions + OG-image — the headline shareable.
- Demographic-cut grid, JOLTS panel, real-wage view, Beveridge curve, Phillips curve.
- A sortable cross-country grid for OECD LFS.
- Three adapter gaps named (Eurostat, Indeed, Atlanta Fed Wage Tracker).

## What comes next

- **L220** housing market page (parallel structure: deep US + cross-country shallow).
- **L214** inflation regime (real wages feed regime classifier).
- **L191** surprise index per indicator (general version of the release card's surprise lozenge).

## Related

- [[L001-vision-statement]]
- [[L214-inflation-regime-classifier]] — real-wage growth as input
- [[L220-housing-market]] — parallel page structure
- [[L213-recession-probability]] — labor consumes unemployment as input
- [[L146-iconography-system]] — `briefcase`, `arrow-up-right`, `clock`
