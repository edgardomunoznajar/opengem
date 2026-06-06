# L217 — Exchange-Rate Misalignment Page

**Loop**: 217 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

Is the yuan undervalued? Is the dollar overvalued? Is the Turkish lira "fairly priced" given fundamentals? These questions drive trillions in capital allocation and are answered weekly inside every macro shop using the same handful of frameworks: **BIS REER** (real effective exchange rate), **PPP-based misalignment** (Penn-effect-corrected price level vs purchasing power), and **fundamentals-based misalignment** (the IMF EBA — External Balance Assessment — methodology). All three are open methodologies. All three produce numbers that are roughly comparable but rarely shown side-by-side outside academic papers. **Nobody publishes a per-country, vintaged, all-three FX misalignment dashboard.**

OPENGEM's FX misalignment page does for currency valuation what the recession-prob page does for recession risk: shows the headline number, shows the three methodologies behind it, lets the user toggle, shows the disagreement openly, and ranks countries on a scrollable grid. The page becomes the *currency valuation reference* for the macro internet — the page that an LLM agent queries when asked "is the rupee overvalued?"

This loop **decides** the three methodologies in detail, the side-by-side rendering, the composite, and how to handle EM currencies with limited data.

## The three methodologies

### 1. BIS REER deviation

The BIS publishes the Real Effective Exchange Rate (REER) for ~60 countries, daily for some and monthly for the rest, with a long historical sample. Misalignment = current REER vs long-run mean (HP-filtered trend). Simple, transparent, the canonical macro currency-strength chart.

**Pros**: long history, comparable, official source.
**Cons**: assumes the long-run mean is the equilibrium — doesn't condition on fundamentals shifting.

### 2. PPP-based misalignment (Penn-effect-corrected)

PPP-based misalignment uses the **OECD/Eurostat PPP comparison** (the same data Big Mac index uses, but rigorously) — the ratio of price levels between countries. Adjusted for the Penn effect (rich countries have higher relative price levels for non-tradables, so a "naive" PPP comparison overestimates EM under-valuation). The corrected PPP-based misalignment is the % deviation from the Penn-effect line.

**Pros**: theory-anchored, comparable across countries, decade-long established.
**Cons**: PPP data is updated every 3-6 years (ICP rounds), so the level changes slowly.

### 3. Fundamentals-based misalignment (IMF EBA-style)

The IMF EBA (External Balance Assessment) regresses the current account on policy variables (fiscal, demographic, FX reserves, oil-trader status, etc.) and fundamentals (debt-to-GDP, growth, etc.) cross-country. The residual is the "misalignment" — the part of the current account that fundamentals don't explain, which is attributed to FX valuation.

**Pros**: the only one of the three that *conditions on fundamentals*, used by the IMF in its annual ESR.
**Cons**: complex, sensitive to specification, only annual updates.

We run all three. For the composite, we **decide** an equal-weight average with a "disagreement flag" lozenge when the three disagree by more than 7pp. The composite is the headline; the three components are one click away.

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ EXCHANGE-RATE MISALIGNMENT — Cross-country                           │
│ Three methodologies. Composite. Vintaged. Every assumption named.    │
└──────────────────────────────────────────────────────────────────────┘

[Selector strip]
 [Country: ALL ▼]   [Method: composite / BIS REER / PPP-Penn / IMF-EBA ▼]   [Vintage: latest ▼]

┌─ Headline grid (cross-country, sortable) ──────────────────────────┐
│ Country │ Composite │ BIS REER │ PPP-Penn │ IMF-EBA │ Agreement│Flag│
│         │   misalig │  dev     │  dev     │  resid  │          │    │
│ USA     │  +11%     │  +8%     │  +10%    │  +15%   │ ✓ aligned│ 🟡 │
│ EUR     │   -2%     │   -1%    │   -3%    │   -2%   │ ✓ aligned│ ─  │
│ JPY     │  -18%     │  -22%    │  -16%    │  -16%   │ ✓ aligned│ 🟠 │
│ GBP     │   -4%     │   -3%    │   -5%    │   -4%   │ ✓ aligned│ ─  │
│ CHF     │  +14%     │  +12%    │  +16%    │  +14%   │ ✓ aligned│ 🟡 │
│ CNY     │   -8%     │   -2%    │   -14%   │   -8%   │ ⚠ split  │ 🟠 │
│ TRY     │  -33%     │  -45%    │  -28%    │  -26%   │ ⚠ split  │ 🔴 │
│ INR     │  -12%     │   -8%    │  -19%    │   -9%   │ ⚠ split  │ 🟠 │
│ ARS     │  -45%     │  -55%    │  -42%    │  -38%   │ ⚠ split  │ 🔴 │
│ ...                                                                  │
│ Sort by: composite |  largest disagreement  |  vintage shift  |  abs │
└─────────────────────────────────────────────────────────────────────┘

┌─ World map view ───────────────────────────────────────────────────┐
│  Choropleth: misalignment % deviation, diverging color scale.       │
│  Blue = undervalued, red = overvalued, zero = white.                │
│  Hover: country tooltip with all three numbers + composite.         │
└─────────────────────────────────────────────────────────────────────┘

┌─ Country detail (selected: CNY) ───────────────────────────────────┐
│                                                                     │
│ CHINA — CNY                                                          │
│ Composite misalignment: -8%  (UNDERVALUED, mild)                    │
│ Δ 3m: +2pp     Δ 12m: -3pp     Δ 5y: -11pp                          │
│                                                                     │
│ ┌─ Method-by-method line chart, 10y history ──────────────────────┐│
│ │  Y: -30% ... +20%                                                ││
│ │  X: 2016 → 2026                                                  ││
│ │  Lines:                                                          ││
│ │    ──── Composite                                                ││
│ │    ─ ─  BIS REER deviation                                       ││
│ │    ····· PPP-Penn corrected                                      ││
│ │    ──── IMF-EBA residual                                         ││
│ │  ▒▒▒  composite confidence band                                  ││
│ │  ▼▼   policy events (PBoC fixing changes, etc.)                  ││
│ └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│ ┌─ Disagreement waterfall ────────────────────────────────────────┐│
│ │  Why composite -8% vs BIS REER -2%?                              ││
│ │   - BIS REER trend assumption uses post-2015 mean (-3pp)         ││
│ │   - PPP-Penn includes ICP 2023 update (+10pp toward undervalued) ││
│ │   - IMF-EBA assumes neutral demographic adjustment               ││
│ └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
│ ┌─ Implied "equilibrium" FX ──────────────────────────────────────┐│
│ │  Current USDCNY: 7.20                                            ││
│ │  Composite-implied equilibrium: ~7.83 (-8% undervalued)          ││
│ │  BIS REER-implied: ~7.35 (-2%)                                   ││
│ │  PPP-Penn-implied: ~8.30 (-14%)                                  ││
│ │  IMF-EBA-implied:  ~7.83 (-8%)                                   ││
│ │  ⚠ Caveat: "equilibrium FX" is a model concept, not a target.    ││
│ └─────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

## "Disagreement" as a feature, not a bug

The page treats methodology disagreement as **information, not noise**. Where the three methods disagree, the page shows a `⚠ split` lozenge — a positive signal to the user that the question is unsettled. A click on the lozenge opens a waterfall chart showing exactly which assumption drives which method to which conclusion. This is the *anti-Statista* move applied to FX: we do not pretend to one true answer; we publish the disagreement transparently and let the user choose.

## EM-data handling

For ~50 EM currencies, BIS REER coverage is partial (BIS publishes ~60 currencies, but with varying quality/lag). For these, OPENGEM falls back to:

1. Build a "DIY REER" from a basket of bilateral nominal rates (open via central banks) and CPI series (open via national stats), with the trade weights derived from IMF DOTS.
2. Mark these with a "DIY REER" lozenge so users know it's not the BIS official series.
3. Flag the lag — some EM CPI is 2-3 months stale.

## Vintage handling

The composite is recomputed daily. The PPP-Penn input only updates with each ICP round (most recently 2023). When the ICP refreshes, every country's PPP-Penn misalignment shifts at once — a known artifact. The page shows a *vintage marker* (a vertical line on the timeline) at every ICP refresh date, so users see "this jump is the 2023 ICP, not a 2023 market event."

## Data sources / adapter dependencies

| Input | Source | Adapter | Status |
|---|---|---|---|
| BIS REER (official 60 currencies) | BIS Statistical Warehouse | `opengem-data-bis` ⚠️ NOT YET BUILT | gap |
| Bilateral FX rates | ECB EUR-base, FRB H.10 USD-base, exchangerate.host | `opengem-data-frb` ✅, `opengem-data-ecb` ⚠️ | partial |
| National CPI (for DIY REER) | per-country statistics offices via IMF | `opengem-data-imf` | partial |
| Trade weights (DIY REER) | IMF DOTS | `opengem-data-imf` extension | partial |
| PPP price-level data | OECD PPP + Eurostat + Penn World Tables | `opengem-data-ordra` (extend), `opengem-data-pwt` ⚠️ NOT YET BUILT | partial |
| ICP rounds | World Bank ICP | `opengem-data-wb` extension | partial |
| IMF EBA model output | IMF ESR (annual PDF) + IMF GAS replication code | `opengem-data-imf` + `opengem-eba-replication` ⚠️ NOT YET BUILT | gap |

**Identified gaps**: BIS adapter (named in roster but not built), Penn World Tables adapter, IMF EBA replication module. The IMF EBA gap is the deepest — the methodology is open but the implementation requires building a cross-country regression pipeline.

## JSON contract

```json
{
  "country": "CHN",
  "currency": "CNY",
  "vintage": "2026-06-06",
  "composite_misalignment_pct": -8,
  "components": {
    "bis_reer_deviation_pct": -2,
    "ppp_penn_corrected_pct": -14,
    "imf_eba_residual_pct": -8
  },
  "agreement_flag": "split",
  "disagreement_attribution": {
    "bis_reer_trend_assumption_window": "post-2015",
    "ppp_penn_icp_round": "2023",
    "eba_demographic_adjustment": "neutral"
  },
  "implied_equilibrium_fx": {
    "current_usd_cny": 7.20,
    "composite_implied": 7.83,
    "by_method": {"bis_reer": 7.35, "ppp_penn": 8.30, "imf_eba": 7.83},
    "caveat": "equilibrium FX is a model concept, not a policy target"
  },
  "history_5y_quarterly": [
    {"date": "2021-06", "composite": -19, "bis_reer": -14, "ppp_penn": -25, "imf_eba": -18}
  ],
  "data_quality_flags": ["BIS REER coverage: official", "EM-DIY REER not used here"],
  "cite_this": "https://opengem.org/fx-misalignment/cny?v=2026-06-06"
}
```

## What this loop produced

- The three-methodology lineup (BIS REER, PPP-Penn, IMF-EBA) with explicit pros/cons.
- A disagreement-as-feature design pattern — split lozenges that *reward* methodological transparency.
- The country detail panel with a "disagreement waterfall" that explains *why* methods diverge.
- A DIY REER fallback for EM currencies with thin BIS coverage.
- Vintage markers on the timeline for ICP refresh events.
- Three adapter gaps named (BIS, Penn World Tables, IMF EBA replication).

## What comes next

- **L218** trade balance + capital flows — the variables that drive misalignment.
- **L216** sovereign risk — undervalued EM currencies are often distress signals.
- **L195** forecast UI for showing implied FX paths.

## Related

- [[L001-vision-statement]]
- [[L218-trade-balance-capital-flows]]
- [[L216-sovereign-risk]]
- [[L215-financial-conditions-index]] — FX is an FCI input
- [[L211-shock-library]] — USD shock here
- [[L146-iconography-system]] — `coins`, `git-compare-arrows`, `alert-triangle`
