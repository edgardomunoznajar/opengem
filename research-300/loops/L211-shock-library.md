# L211 — Generic Shock Library Page

**Loop**: 211 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

A *shock library* is the macro-product equivalent of a button you press to ask "what happens to my country if X moves Y bp?" Every macro shop runs them internally — they are the table stakes that the Fed, the IMF, every CB, every macro hedge fund has been doing for 40 years. Nobody publishes them in a clickable, vintaged, comparable form. That is the open-shaped hole OPENGEM walks through.

The shock library page is the *single page that proves OPENGEM is a forecasting product, not a data scrape*. It is the page Damian (the YouTuber) screenshots when oil pops 8%, the page Nadia (the SWF analyst) cites when she needs a defensible "if-rates-shift" memo, the page Marcus (the FT journalist) embeds when the Fed surprises. If the home screen tile reads "oil shock → US CPI +0.8pp at 12m, P10-P90 [+0.3, +1.4]" and the click-through opens this page, OPENGEM is recognizable as a forecasting product in 90 seconds.

This loop **decides** the page structure, the visualization stack, the canonical JSON contract, and the four shocks that ship in v1.

## The four canonical shocks (v1)

We ship four impulse responses at launch. More are easy to add. The four are chosen because (a) they are the *most-asked questions* macro humans run, (b) each one stresses a *different* part of the model architecture (commodity, FX, external growth, monetary), and (c) all four can be sourced and identified from open data — no proprietary inputs required.

1. **Oil shock**: +25% Brent crude, sustained 4 quarters. Identified via Kilian-style structural VAR (oil supply, oil demand, global activity), open replication code available, OPENGEM keeps the Kilian-Murphy 2014 identification as the reference. Per-country IRF on CPI, GDP, current account, USD-pair FX, equity index.
2. **USD shock**: +10% trade-weighted USD (DXY-equivalent), sustained 4 quarters. Identified via sign-restriction BVAR (monetary policy + risk-on/risk-off), per-country IRF on net exports, terms-of-trade, headline inflation, EM rate response.
3. **China growth shock**: -2pp Chinese real GDP growth, sustained 4 quarters. Identified via Caldara-Iacoviello-Iacoviello (2020)-style external-demand shock. Per-country IRF on exports-to-China, commodity demand, regional growth spillover.
4. **Rate shock**: +100bp Fed funds rate surprise. Identified via Romer-Romer monetary surprise + Nakamura-Steinsson high-frequency identification (HFI). Per-country IRF on FX, sovereign yield, equity risk premium, EM credit spread.

Each shock has *two* invocation modes: **fixed-size** (the +25% / +10% / -2pp / +100bp above) and **calibrated** (the user picks the shock size — slider from 0.5x to 2.5x of canonical — and IRFs scale linearly within the linearization region with an "extrapolation warning" band beyond 1.5x).

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ SHOCK LIBRARY                                                        │
│ Pre-built impulse responses. Pick a shock, pick a country, see IRFs. │
│ Every shock vintaged, every IRF backtested, every assumption named.  │
└──────────────────────────────────────────────────────────────────────┘

[Selector strip — sticky]
 [Oil +25%] [USD +10%] [China -2pp] [Rate +100bp] [+ custom]   [country picker ▼]   [shock size: 1.0x ━━●━━━]

┌─ Headline strip ────────────────────────────────────────────────────┐
│ Shock: Oil +25% Brent (Kilian-Murphy SVAR)                          │
│ Country: United States                                              │
│ Horizon: 4Q ahead, peak impact at Q4                                │
│ Δ CPI: +0.8pp [P10-P90: +0.3, +1.4]                                 │
│ Δ GDP: -0.4pp [P10-P90: -0.9, -0.0]                                 │
│ Δ Curr.Acct.: -0.3pp of GDP                                         │
└─────────────────────────────────────────────────────────────────────┘

┌─ Main IRF chart (2/3 width) ────┐ ┌─ Sidecar: assumptions (1/3) ───┐
│ Multi-line IRF, 16Q horizon     │ │ Identification: Kilian-Murphy  │
│ CPI / GDP / CA / FX overlaid    │ │ Replication: github.com/...     │
│ Confidence bands (P10/P90 fan)  │ │ Vintage: 2026-06-01 (model v3) │
│ Tooltips: hover-Q reveals point │ │ Sample: 1986m1–2026m4          │
│ Click bandstone to expand       │ │ Backtest CRPS: 0.42 (rank 1/3) │
└─────────────────────────────────┘ │ Caveat: linearity above 1.5x    │
                                    │ Open: [JSON] [Notebook] [CSV]  │
                                    └────────────────────────────────┘

┌─ Cross-country sparkline grid ──────────────────────────────────────┐
│ Same shock, every country in OPENGEM coverage. 4Q peak Δ on CPI.    │
│ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐             │
│ │ US     │ │ EA     │ │ UK     │ │ JP     │ │ CN     │             │
│ │ ╭╮     │ │   ╭╮   │ │  ╭╮    │ │ ╭╮     │ │ ──╮    │             │
│ │+0.8pp  │ │+0.6pp  │ │+0.7pp  │ │+0.4pp  │ │-0.2pp  │             │
│ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘             │
│   ... 30+ more, sortable: highest CPI hit first, lowest GDP hit ... │
└─────────────────────────────────────────────────────────────────────┘

┌─ Variable selector tabs ────────────────────────────────────────────┐
│ [CPI] [GDP] [CurrAcct] [FX-USD] [Equity] [Sovereign yield] [Custom] │
└─────────────────────────────────────────────────────────────────────┘

┌─ Channel decomposition (collapsed by default) ─────────────────────┐
│ How the oil shock propagates to US CPI:                             │
│  - Direct (gasoline/heating): +0.55pp                               │
│  - Indirect (transportation/food): +0.15pp                          │
│  - Second-round (wage-price): +0.10pp                               │
└─────────────────────────────────────────────────────────────────────┘

┌─ History strip ────────────────────────────────────────────────────┐
│ Past oil-shock episodes (auto-tagged): 1973, 1979, 1990, 2008,     │
│ 2011, 2022. Click → side-by-side: model IRF vs realized path.      │
└─────────────────────────────────────────────────────────────────────┘

[Methodology pop-up trigger]   [Cite this view]   [Share permalink]
```

## Visualization stack — concrete

- **Main IRF chart**: Lightweight Charts (TradingView OSS) with custom band-fill plugin for P10/P90. Multi-line with toggle.
- **Cross-country sparkline grid**: TanStack Table cells with inline mini-sparklines rendered via Observable Plot (lighter than Plotly for tiny multiples).
- **Headline strip**: pure HTML/CSS lozenges, no chart library.
- **Channel decomposition**: stacked-bar (Plotly Express) inside an accordion, collapsed by default — pros expand, prosumers don't.
- **History strip**: a horizontal sortable grid of `<a>` tags; clicking opens a side-by-side modal with two IRF charts (model vs realized).
- **Maps**: optional — a click on "view world map" replaces the sparkline grid with a choropleth (Kepler.gl, hex-binned ΔCPI at 4Q peak).

## Data sources / adapter dependencies

| Shock | Drives via | Adapters needed | Status today |
|---|---|---|---|
| Oil | Brent crude (EIA, IEA backup), oil futures (CME settle, free 1d lag) | `opengem-data-eia` ⚠️ NOT YET BUILT, `opengem-data-cme` ⚠️ NOT YET BUILT | gap |
| USD | DXY constituents (FRB H.10) | `opengem-data-frb` ✅ | ready |
| China growth | NBS quarterly GDP + monthly indicators | `opengem-data-cnsbs` ⚠️ NOT YET BUILT (China NBS adapter) | gap |
| Rate | Fed funds futures, SOFR strip, Romer-Romer dates | `opengem-data-frb` ✅ + `opengem-data-cme` ⚠️ NOT YET BUILT | partial |

**Identified gap**: an EIA energy adapter, a CME futures-settle adapter, and a China NBS adapter need to be added to the package roster before this page can ship its full v1. The DSB shock library page is a forcing function to commission those three adapters.

## JSON contract (per-shock-per-country)

```json
{
  "shock_id": "oil-plus25-brent-kilian-murphy-svar",
  "shock_family": "oil",
  "shock_size": "+25% Brent, sustained 4Q",
  "calibrated_multiplier": 1.0,
  "identification": {
    "method": "Kilian-Murphy 2014 SVAR",
    "replication_url": "https://github.com/opengem/shocks/blob/main/oil-km2014.ipynb",
    "vintage": "2026-06-01",
    "model_version": "shocks-v3.2.1",
    "sample": "1986m1-2026m4"
  },
  "country": "USA",
  "horizon_quarters": 16,
  "irfs": [
    {
      "variable": "cpi_yoy_pp",
      "median": [0.05, 0.20, 0.45, 0.80, 0.75, 0.60, 0.40, 0.25, 0.15, 0.08, 0.04, 0.02, 0.01, 0.01, 0.00, 0.00],
      "p10": [0.00, 0.05, 0.20, 0.30, 0.25, 0.20, 0.10, 0.05, 0.02, 0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
      "p90": [0.10, 0.40, 0.80, 1.40, 1.30, 1.10, 0.85, 0.65, 0.45, 0.30, 0.18, 0.10, 0.06, 0.04, 0.02, 0.01]
    },
    { "variable": "gdp_qoq_ann_pp", "median": [...], "p10": [...], "p90": [...] }
  ],
  "channel_decomposition": {
    "direct_passthrough": 0.55,
    "indirect_input_cost": 0.15,
    "second_round_wage_price": 0.10
  },
  "calibration": {
    "backtest_crps": 0.42,
    "backtest_rank_vs_consensus": "1/3",
    "linearity_safe_range_multiplier": [0.5, 1.5]
  },
  "caveats": [
    "Linearity assumed; extrapolation above 1.5x flagged.",
    "Does not condition on monetary policy response; see scenario-chain for joint shock."
  ],
  "history_episodes": ["1973oil", "1979oil", "1990oil", "2008oil", "2011oil", "2022oil"],
  "cite_this": "https://opengem.org/shocks/oil-plus25/usa?v=2026-06-01"
}
```

## What this loop produced

- The four-shock v1 lineup, each with named identification.
- The page wireframe with sticky selector, sidecar assumptions, sparkline grid, channel decomposition, and history strip.
- The visualization stack — Lightweight Charts + TanStack + Observable Plot + Kepler.gl + Plotly Express.
- The JSON contract that becomes the cite-this-view object.
- Three adapter gaps named (EIA, CME, China NBS).

## What comes next

- **L212** does stress-test scenarios (CCAR / ECB severely adverse) which compose multiple shocks into a single named pack.
- **L196** wires scenario triggers — event-detector firing the shock library.
- **L235** is the forecast-page prototype that embeds the IRF chart primitive.

## Related

- [[L001-vision-statement]] — every forecast vintaged, every assumption named
- [[L196-scenario-triggers]] — what fires which shock
- [[L210-counterfactual-scenarios]] — close cousin: sanctions, oil shock, geopolitical event
- [[L212-stress-tests]] — composed multi-shock packs
- [[L235-forecast-page-prototype]] — IRF chart primitive
- [[L146-iconography-system]] — `waves`, `target`, `crystal-ball` icons used here
