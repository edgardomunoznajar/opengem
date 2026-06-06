# L216 — Sovereign Risk Page

**Loop**: 216 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

Sovereign credit risk is the *most asymmetric* market in the world: priced by three rating agencies (Moody's, S&P, Fitch) whose business model is the rating itself, traded on CDS via DTCC public Tuesday files, and fundamentally driven by debt-to-GDP, primary balance, interest coverage, FX reserves, and political/institutional quality. **Every input is open or semi-open. No public dashboard combines them.** Bloomberg has the data behind paywalls. The IMF DSA tool is buried in PDFs. Trading Economics has ratings tables that are stale.

OPENGEM's sovereign risk page is the page that makes Lin (the NGO debt sustainability researcher) say "I no longer need to wait for the IMF Article IV PDF" and makes Nadia (the SWF analyst) say "this is the receipts page for our EM exposure memo." It is the page that, six months from launch, gets cited by Reuters when a country gets downgraded.

This loop **decides** the page structure, the *composite risk score* methodology, the rating-history visualization, and how OPENGEM handles closed CDS data via the DTCC public file and EM proxies.

## The page's four pillars

The page is organized around four pillars, each a tab:

1. **Market-implied** — 5y CDS, sovereign bond spreads (over US-treas or German-bund), implied default probability, credit indices (EMBI proxies).
2. **Agency ratings** — Moody's, S&P, Fitch current ratings + outlook + watch flags + full history. Composite "rating consensus."
3. **Fundamentals** — debt-to-GDP, primary balance, interest-coverage ratio, gross financing need, FX reserves, current account, refinancing schedule.
4. **OPENGEM composite** — z-score combination of (1)+(2)+(3), with explicit weights, vintaged, backtested against actual default / restructuring events.

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ SOVEREIGN RISK — Cross-country composite                             │
│ Market-implied + agency ratings + fundamentals.                      │
└──────────────────────────────────────────────────────────────────────┘

[Selector strip]
 [Country: ALL ▼ | EM only | DM only]   [Vintage: latest ▼]   [Sort: composite risk ▼]

┌─ Headline grid (top 10 by risk) ───────────────────────────────────┐
│ Rank│Country │ Composite │ Δ 30d │ Rating  │ 5y CDS │ DGDP │  Flag │
│  1  │ARG     │ 91/100    │  +4   │ CCC-/Caa3│ 1842bp│ 96%  │ 🔴 watch│
│  2  │TUR     │ 82/100    │  +6   │ B+/Caa1  │  680bp│ 38%  │ 🔴 watch│
│  3  │EGY     │ 78/100    │  +2   │ B-/Caa1  │  720bp│ 95%  │ 🟠     │
│  4  │PAK     │ 75/100    │  +1   │ CCC+/Caa3│ 1150bp│ 71%  │ 🟠     │
│  5  │NGA     │ 71/100    │  -1   │ B-/Caa1  │  540bp│ 38%  │ 🟠     │
│ ...                                                                  │
└─────────────────────────────────────────────────────────────────────┘

┌─ World map view (toggle) ──────────────────────────────────────────┐
│  Choropleth: composite risk score 0-100, green→red.                 │
│  Hover: country tooltip with rating + CDS + composite.              │
│  Click: drill into country detail.                                  │
└─────────────────────────────────────────────────────────────────────┘

┌─ Country detail (selected: ARG) ───────────────────────────────────┐
│                                                                     │
│ ╔═══════════════════════════════════════════════════════╗           │
│ ║ ARGENTINA                                              ║           │
│ ║ Composite: 91/100  🔴 HIGH RISK                        ║           │
│ ║ Δ 30d: +4    Δ 90d: +11    Δ 1y: +18                   ║           │
│ ╚═══════════════════════════════════════════════════════╝           │
│                                                                     │
│ ┌─ Market-implied tab ────────────────────────────────────────────┐│
│ │ 5y CDS spread (5y history line chart, log scale): 1842bp        ││
│ │ Implied 5y cumulative default prob (40% recovery): 67%          ││
│ │ Sovereign bond spread (10y ARG-USD vs UST10): 1620bp            ││
│ │ EMBI Global spread proxy: 1580bp                                ││
│ │ Vol of CDS (30d realized): 28bp daily                           ││
│ └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│ ┌─ Agency ratings tab ────────────────────────────────────────────┐│
│ │ ──────────────────────────────────────────────────────────────  ││
│ │ Current:    Moody's Caa3 / S&P CCC- / Fitch CCC                ││
│ │ Outlook:    Negative / Negative / Stable                        ││
│ │ Composite:  9/22 on Moody's scale (where 1 = Aaa, 22 = D)       ││
│ │ Watch:      None active                                          ││
│ │                                                                  ││
│ │ Rating history timeline (24y):                                  ││
│ │ ║║║║║║║║║║║║║║║║║║║║║║║║                                        ││
│ │ Moody's: B...Ba...B...Caa...D(2020 restruct)...Ca...Caa3        ││
│ │ S&P:     B+...BB-...B-...CCC...SD...CCC...CCC-                  ││
│ │ Fitch:   BB-...B+...B-...CCC...RD...CCC...CCC                   ││
│ │ Δ vs 1y ago: Moody's -2 notches, S&P -2 notches, Fitch -1       ││
│ └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│ ┌─ Fundamentals tab ──────────────────────────────────────────────┐│
│ │ Debt-to-GDP:           96%    (▲ from 89% LY, threshold 70%)    ││
│ │ Primary balance:      -2.1%   (▼ from +0.4% LY, threshold +1%)  ││
│ │ Interest coverage:     2.3x   (▼ from 3.1x LY, threshold 4x)    ││
│ │ FX reserves (months):  3.2    (▼ from 5.1 LY, threshold 6m)     ││
│ │ Gross financing need: 22% GDP (▲ from 18% LY)                   ││
│ │ Refinancing schedule (next 24m, stacked bar by quarter):        ││
│ │  Q3-26: $8B  Q4-26: $6B  Q1-27: $11B  Q2-27: $7B  ...           ││
│ └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│ ┌─ OPENGEM composite breakdown ──────────────────────────────────┐ │
│ │ Composite score = 91/100                                       │ │
│ │  - Market signal contribution:    +34 (37%)                    │ │
│ │  - Rating signal contribution:    +28 (31%)                    │ │
│ │  - Fundamentals contribution:     +29 (32%)                    │ │
│ │ Weighting derived from out-of-sample CRPS over 2000-2024        │ │
│ │ default/restructuring events (n=14).                            │ │
│ └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

## CDS data sourcing — the key decision

CDS spreads are *de facto* closed (Markit, ICE Data Services) — but the **DTCC publishes a weekly public file** (every Tuesday) with aggregate notional and number-of-trades per reference entity. This is the *open backbone* of sovereign CDS that very few people use. OPENGEM uses DTCC weekly for the underlying market signal and *interpolates* daily via:

- **Sovereign bond spread vs benchmark** (open, calculable from any open bond curve).
- **EMBI proxy** (constructed from open prices of the largest 3-5 bonds per issuer).
- **CDX/iTraxx index** (close-of-day public via index providers' tickers).

The page is transparent about this — every CDS number has a "source: DTCC weekly (open) + sovereign-spread interpolation (own model)" lozenge. We do not pretend to have Markit-grade tick data; we publish a defensible daily estimate.

## Ratings methodology — composite rating mapping

The three agencies use *different scales* — Moody's letter+number, S&P/Fitch letter+sign. OPENGEM publishes a **uniform 22-point scale** (1=Aaa to 22=D), maps each agency's rating onto it, and computes a "consensus rating" as the median. Where agencies disagree by ≥2 notches, the page flags "agency divergence" with an `alert-triangle` icon and lists the split.

Rating change history is its own micro-page — every notch up or down, dated, with the announcement text linked. The user can subscribe to RSS for any country.

## Composite score — weights and accountability

The composite score is **not** a Bloomberg black box. It's a defined formula:

```
composite = 100 * sigmoid(0.4*z_market + 0.3*z_rating + 0.3*z_fundamentals)
```

The weights are *learned* on the historical sample of sovereign distress events (default, restructuring, near-miss bailout) — but the formula and the weights are published openly. Every quarter the weights are re-estimated; the changes are logged in the changelog.

The page carries a panel showing: "Out-of-sample backtest — did the composite predict the 2020 ARG, 2022 SRI, 2024 PAK distress events?" — with hit/miss markers and Brier scores. This is *the* accountability frame for the page.

## Data sources / adapter dependencies

| Pillar | Inputs | Adapter | Status |
|---|---|---|---|
| CDS | DTCC weekly file | `opengem-data-dtcc` ⚠️ NOT YET BUILT | gap |
| Sovereign bond spreads | World Bank GEM (open), national CB data | `opengem-data-wb` + per-CB | partial |
| Moody's ratings | Moody's "Rated Sovereigns" page (HTML, semi-open) | `opengem-data-moodys` ⚠️ NOT YET BUILT | gap |
| S&P ratings | S&P "Sovereign Ratings List" (HTML, semi-open) | `opengem-data-sp` ⚠️ NOT YET BUILT | gap |
| Fitch ratings | Fitch "Sovereign Ratings" page | `opengem-data-fitch` ⚠️ NOT YET BUILT | gap |
| Debt-to-GDP | IMF WEO + Fiscal Monitor | `opengem-data-imf` | partial |
| Primary balance | IMF Fiscal Monitor + national budgets | `opengem-data-imf` + per-country gov adapter | partial |
| FX reserves | IMF IFS (open) | `opengem-data-imf` | partial |
| Refinancing schedules | IIF + World Bank + national debt offices | `opengem-data-iif` ⚠️ NOT YET BUILT | gap |

**Identified gaps**: DTCC, the three rating-agency scrapers, IIF for refinancing schedules. **The three rating-agency adapters are the most legally sensitive** — agencies publish ratings on their websites but assert IP rights over the *interpretation*. We mirror the *fact of the rating* with attribution and link to the agency's announcement; we never republish the rating commentary.

## JSON contract

```json
{
  "country": "ARG",
  "vintage": "2026-06-06",
  "composite_score": 91,
  "composite_delta": {"30d": +4, "90d": +11, "1y": +18},
  "market_implied": {
    "cds_5y_bp": 1842,
    "cds_source": "DTCC weekly + sovereign-spread interpolation",
    "implied_5y_default_prob_at_40pc_recovery": 0.67,
    "bond_spread_10y_vs_ust": 1620,
    "embi_proxy_spread": 1580
  },
  "agency_ratings": {
    "moodys": {"rating": "Caa3", "outlook": "negative", "as_of": "2026-04-15", "scale22": 17},
    "sp":     {"rating": "CCC-",  "outlook": "negative", "as_of": "2026-05-02", "scale22": 17},
    "fitch":  {"rating": "CCC",   "outlook": "stable",   "as_of": "2026-03-21", "scale22": 17},
    "consensus_scale22": 17,
    "divergence_flag": false,
    "history_url": "https://opengem.org/ratings/arg/history"
  },
  "fundamentals": {
    "debt_to_gdp_pct": 96,
    "primary_balance_pct_gdp": -2.1,
    "interest_coverage_x": 2.3,
    "fx_reserves_months_imports": 3.2,
    "gross_financing_need_pct_gdp": 22,
    "current_account_pct_gdp": -1.8
  },
  "backtest": {
    "historical_distress_events_predicted": ["arg2020", "srl2022"],
    "historical_distress_events_missed": [],
    "brier_score_2010_2024": 0.14
  },
  "cite_this": "https://opengem.org/sovereign-risk/arg?v=2026-06-06"
}
```

## What this loop produced

- The four-pillar structure (market / agency / fundamentals / composite).
- A *daily* CDS estimate built on DTCC weekly + sovereign-spread interpolation, with transparent sourcing.
- A uniform 22-point rating scale that resolves the Moody's-vs-S&P-vs-Fitch inconsistency.
- A learned-weights composite with backtest history and openly published formula.
- Seven adapter gaps named (DTCC, three rating agencies, IIF, plus IMF extension).

## What comes next

- **L224** is sovereign debt sustainability (DSA-style stress) — composes with this page.
- **L225** is alliances + sanctions — informs political-risk leg of fundamentals.
- **L195** wires the forecast band UI used in the composite-score history chart.

## Related

- [[L001-vision-statement]]
- [[L215-financial-conditions-index]] — overlap in credit components
- [[L224-sovereign-debt-sustainability]]
- [[L225-alliances-sanctions]]
- [[L213-recession-probability]] — sovereign risk feeds country-level recession
- [[L146-iconography-system]] — `landmark`, `alert-triangle`, `flag`, `gavel`
