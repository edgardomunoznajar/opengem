# L212 — Stress Test Scenarios Page

**Loop**: 212 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

The Fed publishes the CCAR (Comprehensive Capital Analysis and Review) "Supervisory Severely Adverse" scenario every February. The ECB publishes the SSM stress-test "Adverse" scenario every two years. The Bank of England publishes the ACS (Annual Cyclical Scenario). The IMF publishes the Article-IV "downside scenario" for every country it covers. **These are the most expensive macro scenarios on Earth** — hundreds of central-bank quants spend a year designing them, every regulated bank in the world has to run them, the path of every variable is public — and yet *no consumer-grade dashboard makes them comparable, embeddable, or queryable*. Bloomberg's "Scenarios" function is awful. TradingEconomics has nothing. Macrobond has a tab nobody opens.

OPENGEM's stress-test page is the page that makes a sovereign fund analyst say "I no longer need to download the CCAR PDF and key the numbers into Excel." It is the page that makes an FT journalist say "I can paste the ECB Adverse path into my piece in 30 seconds with a citation." It is the page that makes an LLM agent able to answer "given the latest CCAR Severely Adverse, what is the implied US unemployment trajectory?" without having to scrape a PDF.

This loop **decides** the page structure, how OPENGEM publishes the scenarios (vendor pass-through vs derived), and the comparison UX between OPENGEM's own scenarios and the regulators'.

## The four canonical packs (v1)

1. **CCAR Supervisory Severely Adverse** — Fed, US-focused, ~28 variables (real GDP, unemployment, CPI, equity prices, treasury yields, BBB spread, dollar index, several home-price indices, several commodity indices, foreign GDP for 5 regions). Quarterly path, 13Q ahead. Refreshed every February.
2. **ECB SSM Adverse / Severely Adverse** — euro-area-focused, ~30 variables per country (real GDP, unemployment, HICP, residential property prices, commercial property, long-term yields, equity, short-term rate, FX). Yearly path, 3Y ahead. Refreshed biennially.
3. **BoE ACS** — UK-focused, ~20 variables. Yearly path, 5Y ahead. Refreshed annually.
4. **IMF Article-IV Downside** — *one per country IMF surveils*, ~12 variables. Annual path, 5Y ahead. Refresh varies by Art-IV cycle.

## How OPENGEM publishes the scenarios — the publishing decision

Three options for ingestion, and we **decide** all three are required, at different layers:

| Layer | What it does | Cost | Refresh |
|---|---|---|---|
| **Pass-through** | Mirror the regulator's published path verbatim, with a "verbatim" provenance stamp. The user can cite OPENGEM as the host, but the data is the regulator's. | low (scrape + parse PDF / Excel) | when regulator publishes |
| **Derived (vintaged)** | Store each annual refresh as a separate vintage, allowing time-machine queries: "what did the CCAR-2022 Severely Adverse imply for 2023 unemployment?" | medium | annual |
| **Comparable (OPENGEM-rebased)** | Re-render the scenarios on OPENGEM's own variable schema (e.g., unify "BBB spread" between CCAR and ECB even when the underlying definitions differ) so they're side-by-side comparable. | high — requires concept-map + caveat layer | per refresh |

We ship **all three** in v1. The pass-through tab is "the original, verbatim." The vintaged tab is "every refresh, ever." The comparable tab is "OPENGEM's harmonized rendering with explicit definition gaps." Each tab is one click; the user picks the level of trust they need.

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ STRESS TEST SCENARIOS                                                │
│ Regulators' Severely Adverse paths, made comparable.                 │
│ Every refresh archived. Every variable vintaged.                     │
└──────────────────────────────────────────────────────────────────────┘

[Pack selector — sticky]
 [CCAR-2026 Severely Adverse]  [ECB-2025 Adverse]  [BoE-ACS-2026]  [IMF Art-IV ▼]   [vintage ▼: latest]

[View mode tabs]
 [Verbatim]   [Comparable]   [Vintaged history]   [Compare-2]

┌─ Headline panel ───────────────────────────────────────────────────┐
│ CCAR 2026 Supervisory Severely Adverse                             │
│ Published: 2026-02-13 | Vintage: ccar-2026-sa                       │
│ Source: federalreserve.gov/.../2026-stress-test-scenarios.pdf       │
│ Variables: 28 | Horizon: 13Q | Frequency: Quarterly                 │
│ Peak unemployment: 10.5% (Q5)  ┊  Peak GDP drawdown: -7.5% (Q3)     │
└─────────────────────────────────────────────────────────────────────┘

┌─ Multi-variable comparison chart (large, full width) ──────────────┐
│ Small multiples: 4×3 grid of mini-line-charts, each = 1 variable.   │
│ Hover any → expands to large chart below.                           │
│                                                                     │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                                 │
│ │GDP %y│ │Unemp │ │CPI %y│ │10y%  │                                 │
│ │ ╲╱   │ │  ╱   │ │  ╲╱  │ │ ╲ ╱  │                                 │
│ └──────┘ └──────┘ └──────┘ └──────┘                                 │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                                 │
│ │BBB sp│ │Equity│ │DXY   │ │HPI   │                                 │
│ │   ╱  │ │ ╲    │ │  ╱   │ │ ╲    │                                 │
│ └──────┘ └──────┘ └──────┘ └──────┘                                 │
│ ... (28 total, scrollable)                                          │
└─────────────────────────────────────────────────────────────────────┘

┌─ Focus chart ──────────────────────────────────────────────────────┐
│ US Unemployment Rate, CCAR-2026 Severely Adverse vs realized        │
│ ────                                                                │
│ Y-axis: 3% → 11%, X-axis: Q-1 → Q13                                 │
│ Lines:                                                              │
│   ─── CCAR-2026 SA path (Fed, official)                             │
│   ─── CCAR-2025 SA path (prior vintage, dotted)                     │
│   ─── OPENGEM L3 forecast (baseline)                                │
│   ─── Realized (for periods past)                                   │
│   ▒▒▒ OPENGEM consensus band (P10-P90)                              │
└─────────────────────────────────────────────────────────────────────┘

┌─ Comparable mode: side-by-side packs ──────────────────────────────┐
│ CCAR-2026 SA  |  ECB-2025 Adverse  |  BoE ACS-2026  |  IMF DD-USA  │
│ ───────────────────────────────────────────────────────────────────│
│ Peak Δ GDP    │ -7.5% Q3          │ -3.0% Y2       │ -5.0% Y2       │ -4.0% Y2 │
│ Peak Unemp    │ 10.5% Q5          │ 11.8% Y3       │ 8.0% Y2        │ 7.5% Y2  │
│ HPI drawdown  │ -38% peak-to-trough│ -16% trough    │ -33% trough    │ n/a      │
│ Equity drawdown│ -55% trough      │ -50% trough    │ -52% trough    │ n/a      │
│ Definition diff flags: [HPI] [Unemp def] [Currency]                 │
└─────────────────────────────────────────────────────────────────────┘

┌─ Vintaged history mode ────────────────────────────────────────────┐
│ Every CCAR Severely Adverse, side-by-side, 2013 → 2026               │
│ Slider: [2013][2014]...[2025][2026]                                 │
│ Reveals how the "stress" definition has drifted over time.          │
│ Trend annotation: avg peak Unemp drift +1.8pp over decade.          │
└─────────────────────────────────────────────────────────────────────┘

┌─ Sidecar: pack metadata ───────────────────────────────────────────┐
│ Source PDF: [link]                                                  │
│ XLSX original: [link]                                                │
│ OPENGEM mirror (verbatim): [JSON] [CSV]                             │
│ OPENGEM rebased (comparable): [JSON] [CSV]                          │
│ Variable schema mapping: [open table]                               │
│ Refresh history: 2013, 14, 15, ..., 2026                            │
│ Open in Notebook: [Jupyter]                                          │
└─────────────────────────────────────────────────────────────────────┘
```

## Comparable-mode mechanics

The pain point is that CCAR's "BBB spread" is the Moody's BBB-AAA spread over treasuries; ECB's "non-financial corporate credit spread" is iTraxx Crossover-aligned; BoE's is sterling-IG-corporate-vs-gilt. These are *not the same thing*. The Comparable mode does not silently rebase them — it shows them side-by-side, **flags the definition gap with a `⚠ definition diff` lozenge**, and on hover reveals the methodology pop-up explaining how OPENGEM maps them. The pop-up always offers a "show me the verbatim numbers instead" toggle.

This is the *anti-Statista* move. Statista repackages and watermarks. OPENGEM rebases and *names* the rebasing.

## Data sources / adapter dependencies

| Pack | Source | Adapter needed | Status |
|---|---|---|---|
| CCAR | federalreserve.gov annual PDF + XLSX | `opengem-data-frb` (extend) — PDF parser + XLSX loader | ✅ FRB adapter exists, extension required |
| ECB SSM | eba.europa.eu + ecb.europa.eu | `opengem-data-eba` ⚠️ NOT YET BUILT | gap |
| BoE ACS | bankofengland.co.uk PDFs | `opengem-data-boe` ⚠️ NOT YET BUILT | gap |
| IMF Art-IV | imf.org per-country PDFs (irregular) | `opengem-data-imf` (extend) — Art-IV scraper + LLM-mediated extraction | ⚠️ extension required |

**Identified gaps**: EBA adapter, BoE adapter, IMF Art-IV scraper. Article-IV downside scenarios are the *trickiest* — they're embedded in narrative PDFs and require an LLM-assisted extraction pipeline.

## JSON contract (per-pack)

```json
{
  "pack_id": "ccar-2026-severely-adverse",
  "publisher": "Federal Reserve Board",
  "publication_date": "2026-02-13",
  "vintage": "2026-02-13",
  "supersedes": "ccar-2025-severely-adverse",
  "country_focus": "USA",
  "horizon": {"length_quarters": 13, "frequency": "Q"},
  "variables": [
    {
      "schema_name": "us_unemp_rate_pct",
      "regulator_name": "Unemployment rate, percent, quarterly average",
      "comparable_concept": "unemployment_rate.headline",
      "path": [4.1, 4.5, 6.2, 8.4, 9.8, 10.5, 10.3, 9.8, 9.0, 8.3, 7.6, 7.0, 6.5],
      "definition_diff_vs_opengem_canonical": null
    },
    {
      "schema_name": "us_bbb_corporate_spread_bp",
      "regulator_name": "BBB corporate yield spread, basis points",
      "comparable_concept": "ig_credit_spread.bbb",
      "path": [125, 200, 380, 550, 600, 580, 520, 450, 380, 320, 280, 240, 220],
      "definition_diff_vs_opengem_canonical": "moody's BBB-AAA; ECB uses iTraxx Crossover-aligned"
    }
  ],
  "comparison_metrics": {
    "peak_unemp_pct": 10.5,
    "peak_gdp_drawdown_pct": -7.5,
    "peak_equity_drawdown_pct": -55,
    "peak_hpi_drawdown_pct": -38
  },
  "source_links": {
    "pdf": "https://www.federalreserve.gov/.../2026-stress-test-scenarios.pdf",
    "xlsx": "https://www.federalreserve.gov/.../2026-stress-test-data.xlsx"
  },
  "cite_this": "https://opengem.org/stress/ccar-2026-sa?v=2026-02-13"
}
```

## What this loop produced

- The four-pack v1 lineup (CCAR, ECB SSM, BoE ACS, IMF Art-IV).
- The publishing-layer decision: pass-through + vintaged + comparable, all three shipped.
- The page structure with four view tabs and a comparable-mode side-by-side that explicitly *flags* definition diffs.
- The JSON contract.
- Three adapter gaps named (EBA, BoE, IMF Art-IV extraction).

## What comes next

- **L213** is the cross-country recession-prob page (a derived stress signal).
- **L186** is the reproducibility envelope; stress packs need their own vintaging discipline.
- **L196** wires the scenario triggers that select between packs.

## Related

- [[L001-vision-statement]] — open ledger, named methodology, vintaged history
- [[L002-competitive-landscape]] — Bloomberg's "Scenarios" function and why it's bad
- [[L211-shock-library]] — single-shock cousin; stress tests are *composed* shocks
- [[L196-scenario-triggers]]
- [[L235-forecast-page-prototype]]
- [[L146-iconography-system]] — `alert-triangle`, `gauge`, `gavel`
