# L215 — Financial Conditions Index Page

**Loop**: 215 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

A Financial Conditions Index (FCI) compresses ten-to-thirty market variables — rates, credit spreads, equity prices, USD, vol, real-estate yields, interbank stress — into a single z-score of "how easy is it to borrow / hold risk / invest." It is the single number that *most* matters to monetary policy transmission and the single number that *most* macro Twitter cares about. The Goldman GS FCI, the Bloomberg US FCI, the Chicago Fed NFCI, the Kansas City KCFSI, the IMF FCI — these are all separate, mutually inconsistent, mostly closed (Goldman and Bloomberg behind paywalls; Chicago Fed and KCFSI free but US-only).

There is no open, cross-country, *comparable* FCI. The IMF has been building one but it's quarterly-lag and country-by-country PDFs. OPENGEM's FCI page does for FCI what the recession page does for recession probability — publishes a daily, vintaged, per-country, comparable, *open* FCI with full component decomposition. That alone is a Bloomberg-grade contribution.

This loop **decides** the FCI methodology (PCA-driven, pooled cross-country), the page structure, the component-decomposition UX, and the trip-wire alerts.

## The methodology

The OPENGEM FCI is constructed per country as follows:

1. **Variable bundle (12 categories, ~25 series per country)**:
   - **Rate level**: 1y, 5y, 10y sovereign yield
   - **Real rate**: 5y real (inflation-linked or BEI-adjusted)
   - **Term spread**: 10y-3m, 10y-2y
   - **Credit (IG)**: investment-grade corporate spread
   - **Credit (HY)**: high-yield corporate spread
   - **Sovereign credit**: 5y CDS where available
   - **Equity level**: main equity index, scaled vs trend
   - **Equity vol**: VIX-equivalent (V2X for EU, NKY-V, etc.)
   - **FX**: trade-weighted exchange rate, scaled vs trend
   - **FX vol**: implied vol on USD-pair
   - **Real estate**: residential property price index vs trend (BIS PPS)
   - **Bank funding**: LIBOR-OIS-equivalent / 3m interbank spread / TED-equivalent

2. **Standardization**: each series z-scored against its own 5-year rolling mean and std. Positive z = tighter conditions (this is the *opposite* of Goldman's convention, which we acknowledge in the methodology pop-up — we use "positive = tight" because it reads as "negative = easy / supportive" which matches macro intuition).

3. **Aggregation**: PCA on the z-score matrix, take PC1 as the FCI. Per-country PCA loadings are published in a sidecar. Daily refresh.

4. **Pooled cross-country comparability**: a second "comparable" rendering re-projects each country's FCI onto a *pooled* PCA basis (estimated on the OECD-major set, 2000-present), so a US FCI z-score can be read meaningfully against a German FCI z-score. This is the *value-add* over single-country FCIs.

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ FINANCIAL CONDITIONS INDEX — Cross-country, daily, comparable        │
└──────────────────────────────────────────────────────────────────────┘

[Selector strip]
 [Country: USA ▼]   [Mode: country-native PCA / pooled cross-country ▼]   [Vintage: latest ▼]

┌─ Headline row ─────────────────────────────────────────────────────┐
│  USA FCI: +1.2σ (TIGHT)   30d: +0.4   90d: +0.8   12m: +1.5         │
│  Status lozenge: 🟧 TIGHTENING   vs. pre-pandemic norm: +0.7σ tighter│
│  Last data point: 2026-06-05  ┊  PC1 explains 67% of variance       │
└─────────────────────────────────────────────────────────────────────┘

┌─ Main FCI timeline (5y) ───────────────────────────────────────────┐
│  Y: -3σ ... +3σ                                                     │
│  X: 2021 → 2026 daily                                               │
│  Lines:                                                             │
│    ─── USA FCI (PC1)                                                │
│    ─── 5y mean ref line at zero                                     │
│    ▒▒▒ ±1σ band (mean ±1σ)                                          │
│    ▼▼  rate-decisions, financial-stress events                      │
│  Toggle: overlay another country (DEU, JPN, GBR)                    │
└─────────────────────────────────────────────────────────────────────┘

┌─ Component decomposition (stacked-bar over time) ──────────────────┐
│  How each of the 12 categories contributes to current FCI.          │
│  Today: 1.2σ = +0.3 from rates + +0.3 from credit + +0.4 from FX    │
│         + +0.2 from equity vol + +0.1 from RE - +0.1 from term      │
│  Visualization: 12-color stacked bar, sortable by contribution.     │
│  Time series version: stacked area over 5y showing how the          │
│   composition of "tightness" has shifted.                           │
└─────────────────────────────────────────────────────────────────────┘

┌─ Cross-country FCI grid (sortable) ────────────────────────────────┐
│ Country     │ FCI (σ) │ 30d Δ │ 90d Δ │ Status   │ Sparkline 90d   │
│ USA         │ +1.2    │ +0.4  │ +0.8  │ TIGHTENING│ ▁▂▂▃▃▄▅▅▆▇█    │
│ EUR-area    │ +0.6    │ +0.2  │ +0.3  │ MILD T   │ ▂▂▃▃▃▄▄▄▅▅▆     │
│ JPN         │ -0.4    │ -0.1  │ -0.2  │ EASY     │ ▄▄▃▃▃▂▂▂▂▁▁     │
│ GBR         │ +0.8    │ +0.1  │ +0.4  │ TIGHTENING│ ▃▃▃▄▄▄▅▅▅▆▆    │
│ CHN         │ -0.7    │ -0.2  │ -0.3  │ EASING   │ ▄▄▄▃▃▃▃▂▂▂▁     │
│ ... 30+                                                              │
└─────────────────────────────────────────────────────────────────────┘

┌─ World map view (toggle) ──────────────────────────────────────────┐
│  Choropleth: countries shaded red (tight) → blue (easy).            │
│  Color anchored to ±2σ.                                             │
│  Click → drills into country page.                                  │
└─────────────────────────────────────────────────────────────────────┘

┌─ Tripwire alerts ──────────────────────────────────────────────────┐
│ Show countries whose FCI:                                           │
│  - crossed +2σ this week (4 countries flagged: TUR, ARG, ZAF, NGA)  │
│  - had a >0.5σ jump in 24h (1 country flagged: ARG)                 │
│  - has been >+1σ for >6 months (8 countries — entrenched tightness) │
│ Each entry → click → country detail.                                 │
└─────────────────────────────────────────────────────────────────────┘

[Methodology pop-up]  [Calibration plot]  [Compare to NFCI / KCFSI for US]
```

## The comparison panel (against existing FCIs for US)

A dedicated panel on the US page shows OPENGEM-FCI alongside:
- Chicago Fed **NFCI** (free, weekly)
- Kansas City **KCFSI** (free, monthly)
- Goldman **GS US FCI** (proxy: reconstructed weekly from public components, with a "best-effort, not the official GS series" lozenge)
- Bloomberg **US FCI** (proxy: similar reconstruction)

This is the **accountability frame**. If OPENGEM's FCI diverges from NFCI, the page openly shows the divergence and asks the user to judge. Over time the page also publishes "which FCI predicts US GDP slowdown best?" — a rolling Brier-equivalent for FCI calls — so the user can see *whose* FCI has the best track record. This is the meta-game: OPENGEM not only publishes its own FCI, it scores all the public ones.

## Component decomposition UX — the "lever" view

Click any component (e.g., "credit-IG") → opens a side-drawer:

- The actual series (e.g., US IG corporate spread, last 5y, log scale).
- This component's contribution to FCI today (+0.18σ).
- Counterfactual: "if this component reverted to its 5y mean, FCI would be: +0.91σ" (a number the user can quote).
- Cross-country: this component's value, ranked across all countries.
- Source attribution.

The lever view is *the* feature that lets a macro user say "the entire FCI tightness story is credit, not equity vol" with a screenshot.

## Data sources / adapter dependencies

| Component | US | Euro-area | UK | EM | Status |
|---|---|---|---|---|---|
| Rate level | FRB H.15 ✅ | ECB SDW ⚠️ | BoE Bankstats ⚠️ | BIS rates ⚠️ | partial |
| IG / HY credit spreads | FRED (ICE BofA) ✅ via FRB adapter | ECB ⚠️ | BoE ⚠️ | EMBI via JPM (closed) — proxy via World Bank ⚠️ | gap for non-US |
| CDS | DTCC public Tuesday file ⚠️ NOT YET BUILT | DTCC ⚠️ | DTCC ⚠️ | DTCC ⚠️ | gap |
| Equity index | Stooq / Yahoo via `opengem-data-stooq` ⚠️ NOT YET BUILT | same | same | same | gap |
| Equity vol | CBOE VIX ⚠️ NOT YET BUILT, V2X, NKY-V ⚠️ | gap | gap | gap | gap |
| FX TWI | FRB H.10 ✅ (DXY-like), BIS REER ⚠️ | BIS ⚠️ | BIS ⚠️ | BIS ⚠️ | partial |
| FX vol | CBOE EUR-V, JPY-V, etc. ⚠️ NOT YET BUILT | gap | gap | gap | gap |
| RE prices | BIS PPS ⚠️ NOT YET BUILT | BIS ⚠️ | BIS ⚠️ | BIS ⚠️ | gap |
| Bank funding | FRED (SOFR-OIS, 3m TBill-OIS) ✅ via FRB | ECB ⚠️ | BoE ⚠️ | BIS ⚠️ | partial |

**Identified gaps**: DTCC CDS public file adapter, Stooq adapter for equity indices, CBOE adapter for equity vol indices, BIS Property Price adapter, BIS REER adapter. The FCI page is a *strong forcing function* — it requires almost the entire market-data adapter stack.

## JSON contract

```json
{
  "country": "USA",
  "vintage": "2026-06-06",
  "fci_native_pc1": 1.21,
  "fci_pooled_cross_country": 1.08,
  "status_label": "TIGHTENING",
  "deltas": {"30d": +0.41, "90d": +0.82, "1y": +1.47},
  "vs_pre_pandemic_avg": +0.7,
  "components": [
    {"category": "rate_level", "z": 1.5, "weight": 0.20, "contribution": +0.30},
    {"category": "real_rate", "z": 1.3, "weight": 0.10, "contribution": +0.13},
    {"category": "term_spread", "z": -0.7, "weight": 0.08, "contribution": -0.06},
    {"category": "credit_ig", "z": 1.0, "weight": 0.10, "contribution": +0.10},
    {"category": "credit_hy", "z": 1.6, "weight": 0.08, "contribution": +0.13},
    {"category": "sovereign_cds", "z": 0.4, "weight": 0.05, "contribution": +0.02},
    {"category": "equity_level", "z": -0.8, "weight": 0.10, "contribution": -0.08},
    {"category": "equity_vol", "z": 1.2, "weight": 0.07, "contribution": +0.08},
    {"category": "fx_twi", "z": 1.2, "weight": 0.08, "contribution": +0.10},
    {"category": "fx_vol", "z": 0.6, "weight": 0.05, "contribution": +0.03},
    {"category": "re_prices", "z": 0.5, "weight": 0.05, "contribution": +0.03},
    {"category": "bank_funding", "z": 1.0, "weight": 0.04, "contribution": +0.04}
  ],
  "comparison_vs_other_fcis": {
    "chicago_fed_nfci": -0.3,
    "kansas_city_kcfsi": -0.1,
    "gs_us_fci_proxy": 0.9,
    "bloomberg_us_fci_proxy": 1.0
  },
  "pca_diagnostics": {
    "pc1_explained_variance": 0.67,
    "loading_top_3": ["rate_level", "credit_hy", "fx_twi"]
  },
  "cite_this": "https://opengem.org/fci/usa?v=2026-06-06"
}
```

## What this loop produced

- A 12-category, ~25-series-per-country FCI methodology with PCA aggregation.
- A *pooled cross-country* second-rendering so countries are comparable.
- The page structure: headline, 5y timeline, component decomposition, cross-country grid, world map, tripwire panel, US-comparison panel.
- A "lever view" component drilldown that publishes counterfactual numbers.
- Five major adapter gaps named (DTCC CDS, Stooq, CBOE vol, BIS PPS, BIS REER).

## What comes next

- **L216** is sovereign risk (CDS / ratings) — a downstream consumer of FCI.
- **L213** recession-prob and **L214** inflation-regime both use FCI as an input.
- **L235** forecast page that surfaces "easing implied 90d ahead" from FCI dynamics.

## Related

- [[L001-vision-statement]]
- [[L213-recession-probability]] — FCI feeds recession prob
- [[L214-inflation-regime-classifier]] — FCI feeds regime
- [[L216-sovereign-risk]] — credit components of FCI overlap
- [[L211-shock-library]] — IRFs are shocks *to* FCI
- [[L146-iconography-system]] — `gauge`, `flame`, `landmark`
