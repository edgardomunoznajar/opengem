# L218 — Trade Balance + Capital Flows Page

**Loop**: 218 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The thesis of this loop

Trade flows are *the* fundamentals of international macro and the *most under-visualized* free data in the world. The IMF's DOTS (Direction of Trade Statistics) ships ~25,000 bilateral cells per month, covering ~200 countries. UN Comtrade ships ~5M product-level records per year. The IMF BOP (Balance of Payments) ships current-account, capital-account, financial-account per country quarterly. **All open. All ugly. All trapped in 1990s-era OECD/IMF web UIs.**

OPENGEM's trade-balance + capital-flows page is the page that makes a *bilateral matrix* feel native — a Brazil-rows-by-China-cols grid where each cell shows the trade balance, click any cell for the full bilateral story, hover for the time series. It is the page that makes Lin (the debt-sustainability researcher) say "I can finally see Argentina's BOP financing gap in one view." It is the page that makes Marcus (the FT journalist) embed a "China's bilateral surplus with the US, 25y" chart in 90 seconds.

This loop **decides** the bilateral-matrix UX, the BOP-stack visualization, the "who-trades-with-whom" map, and the capital-flow attribution layer.

## The four views

The page is organized as four pivot-style views on the same underlying DOTS + BOP + Comtrade data:

1. **Country flagship** — single country, multi-decade trade balance + BOP, with components stacked.
2. **Bilateral matrix** — 30×30 grid of major trading partners, each cell = trade balance (or % of GDP).
3. **Flow map** — geographic flow map (chord diagram or Sankey on a world map) showing the largest bilateral flows.
4. **Product drill-down** — per HS-code product, who exports to whom (Comtrade).

## Page structure (top to bottom)

```
┌──────────────────────────────────────────────────────────────────────┐
│ TRADE BALANCE + CAPITAL FLOWS                                        │
│ IMF DOTS (bilateral). IMF BOP (current+capital+financial). Comtrade. │
└──────────────────────────────────────────────────────────────────────┘

[View tabs]
 [Country flagship]  [Bilateral matrix]  [Flow map]  [Product drill-down]

[Selectors]
 [Year: 2026 ▼ | Range: 2000-2026 ▼]   [Frequency: M / Q / A ▼]   [Unit: $bn / % GDP ▼]

╔══════════════════════════════════════════════════════════════════════╗
║ COUNTRY FLAGSHIP — USA                                                ║
╚══════════════════════════════════════════════════════════════════════╝

┌─ Trade balance time series (25y) ──────────────────────────────────┐
│  Stacked area: goods balance + services balance + total              │
│  Y: -$1500bn ... +$200bn                                             │
│  X: 2000 → 2026                                                      │
│  Annotations: NAFTA→USMCA, China WTO, US-China tariffs, COVID, IRA   │
└─────────────────────────────────────────────────────────────────────┘

┌─ BOP decomposition (current + capital + financial) ────────────────┐
│  Three stacked bars per period:                                     │
│   Current account = goods + services + primary income + secondary   │
│   Capital account = capital transfers                               │
│   Financial account = FDI + portfolio + other inv + reserves        │
│  Identity: CA + KA + (-FA) = errors-and-omissions                   │
│  Reveals "who is financing the deficit / where is the surplus going"│
└─────────────────────────────────────────────────────────────────────┘

┌─ Top-10 bilateral partners snapshot ───────────────────────────────┐
│ Partner │ Goods exp │ Goods imp │ Net    │ %share │ trend         │
│ CHN     │ $145bn    │ $437bn    │ -$292bn│ 14%    │ ▼ since 2018   │
│ MEX     │ $325bn    │ $475bn    │ -$150bn│ 12%    │ ▲ post-USMCA   │
│ CAN     │ $354bn    │ $375bn    │ -$21bn │ 11%    │ ─ stable       │
│ DEU     │ $76bn     │ $159bn    │ -$83bn │ 5%     │ ─ stable       │
│ JPN     │ $79bn     │ $148bn    │ -$69bn │ 5%     │ ▼ slight       │
│ ...                                                                  │
└─────────────────────────────────────────────────────────────────────┘
```

```
╔══════════════════════════════════════════════════════════════════════╗
║ BILATERAL MATRIX                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

                            COLUMNS = importer
                  USA   CHN   DEU   JPN   GBR   FRA   IND   MEX   CAN   BRA
ROWS = exporter ╔═════╤═════╤═════╤═════╤═════╤═════╤═════╤═════╤═════╤═════╗
       USA     ║  -  │ 145 │ 76  │ 79  │ 71  │ 39  │ 41  │ 325 │ 354 │ 36  ║
       CHN     ║ 437 │  -  │ 102 │ 167 │ 79  │ 31  │ 118 │ 119 │ 75  │ 73  ║
       DEU     ║ 159 │ 96  │  -  │ 24  │ 89  │ 116 │ 13  │ 8   │ 8   │ 8   ║
       JPN     ║ 148 │ 158 │ 22  │  -  │ 12  │ 6   │ 11  │ 11  │ 9   │ 6   ║
       GBR     ║ 65  │ 38  │ 39  │ 8   │  -  │ 31  │ 8   │ 4   │ 7   │ 3   ║
       FRA     ║ 45  │ 25  │ 84  │ 7   │ 33  │  -  │ 6   │ 2   │ 3   │ 4   ║
       IND     ║ 79  │ 19  │ 11  │ 6   │ 12  │ 6   │  -  │ 8   │ 5   │ 3   ║
       MEX     ║ 475 │ 9   │ 6   │ 4   │ 5   │ 2   │ 3   │  -  │ 18  │ 4   ║
       CAN     ║ 375 │ 21  │ 6   │ 11  │ 11  │ 2   │ 3   │ 8   │  -  │ 4   ║
       BRA     ║ 36  │ 102 │ 4   │ 5   │ 6   │ 4   │ 5   │ 5   │ 3   │  -  ║
                ╚═════╧═════╧═════╧═════╧═════╧═════╧═════╧═════╧═════╧═════╝

Cell color encoding:
  - Diagonal: grey (own-country)
  - Light blue: small flow
  - Dark blue: large flow
  - Red overlay on top-2 imbalances per row
Cell hover: tooltip with last-12m trend sparkline + YoY change.
Cell click: opens full bilateral page (X exports to Y, history, products).
Toggle: % of GDP | $bn | % of total trade
```

```
╔══════════════════════════════════════════════════════════════════════╗
║ FLOW MAP                                                              ║
╚══════════════════════════════════════════════════════════════════════╝

  World map (Kepler.gl) with arcs:
   - Arc thickness = volume of the bilateral flow
   - Arc color = direction (red = deficit for origin)
   - Filter: top-N flows, single-country source, single-region pair
   - Animation: scrub time slider 2000 → 2026 showing flow shift

  Alternative: chord diagram (D3) for top-30 flows in a circle.
  Toggle.
```

```
╔══════════════════════════════════════════════════════════════════════╗
║ PRODUCT DRILL-DOWN (Comtrade)                                         ║
╚══════════════════════════════════════════════════════════════════════╝

  HS-code picker: e.g., HS-85 (electrical machinery)
  Filter to: USA imports of HS-85
  Top exporters chart: CHN $230bn, MEX $98bn, TAI $76bn, KOR $52bn, VNM $48bn ...
  Time series of each top exporter, 10y.
  Concentration index (HHI): 0.41 (moderately concentrated).
  Resilience score: based on top-5 share + alternative-supplier availability.
```

## The bilateral matrix UX — the headline feature

The bilateral matrix is the **headline visualization** and the page's "Bloomberg-killer" claim. Every macro analyst wants this view; nobody has it free. The matrix:

- Defaults to top-30 economies (sortable: G20, G7, EU27, EM-major).
- Cell value: net bilateral trade in $bn, configurable to % of GDP or % of exporter's total trade.
- Hover: 60-month sparkline + YoY change + the underlying time series link.
- Click: opens the full **A→B page** (e.g., "USA imports from China") with the long history, the product breakdown, the structural-break detection, the related geopolitical events (tariffs, sanctions) overlaid.
- Time slider: scrub from 2000 to today and see the matrix re-render.
- Highlight modes: "biggest deficits" / "biggest surpluses" / "biggest changes" / "biggest absolute"

This is **the** page where Damian (the YouTuber) finds his Sunday-night b-roll. He picks "biggest changes since 2018" — China-US row turns red, China-Vietnam row turns green — and screenshots.

## Capital flows attribution layer

For each country's financial account, the page breaks down into:

- **FDI** (greenfield + M&A; UNCTAD source).
- **Portfolio inflows** (debt + equity; IIF + IMF BOP).
- **Other investment** (bank lending, official lending).
- **Reserve assets** (central bank intervention).

The visualization is a stacked-area chart over time showing the net change of each component. A bank-lending crisis (2008) shows as a sharp drop in "other investment"; a FDI boom (e.g., Mexico post-USMCA) shows as a sustained green band. Each component links to the underlying series.

## Data sources / adapter dependencies

| Input | Source | Adapter | Status |
|---|---|---|---|
| Bilateral trade (DOTS) | IMF DOTS | `opengem-data-imf` ⚠️ NOT YET BUILT (in roster) | gap |
| BOP | IMF BOP/IIP via SDMX | `opengem-data-imf` | gap |
| UN Comtrade | UN Comtrade API | `opengem-data-comtrade` ⚠️ NOT YET BUILT (in roster) | gap |
| FDI | UNCTAD + national CBs | `opengem-data-unctad` ⚠️ NOT YET BUILT | gap |
| Portfolio flows | IIF Capital Flows | `opengem-data-iif` ⚠️ NOT YET BUILT | gap |
| GDP (for % normalization) | IMF WEO + WB | `opengem-data-imf`, `opengem-data-wb` ⚠️ | partial |

**Identified gaps**: IMF DOTS, Comtrade, UNCTAD, IIF adapters. All named in the roster but not yet built. The trade page is *the* forcing function to ship IMF DOTS + Comtrade at minimum.

## JSON contract

### Country flagship
```json
{
  "country": "USA",
  "vintage": "2026-06-06",
  "current_account": {
    "balance_usdbn": -944,
    "goods_balance": -1110,
    "services_balance": +280,
    "primary_income": -75,
    "secondary_income": -39,
    "as_pct_gdp": -3.4
  },
  "financial_account": {
    "fdi_net": -150,
    "portfolio_net": +680,
    "other_investment_net": +210,
    "reserves_change": -3,
    "errors_omissions": -28
  },
  "bilateral_top10": [
    {"partner": "CHN", "exports": 145, "imports": 437, "net": -292},
    ...
  ],
  "cite_this": "https://opengem.org/trade/usa?v=2026-06-06"
}
```

### Bilateral cell
```json
{
  "exporter": "USA",
  "importer": "CHN",
  "vintage": "2026-06-06",
  "period": "2026-Q1-annualized",
  "flow_usdbn": 145,
  "yoy_change_pct": -8.3,
  "as_pct_exporter_total_exports": 7.1,
  "history_60m": [...],
  "structural_break_dates": ["2018-07-01 tariff", "2022-08 chip rules"],
  "top_products_hs2": ["HS-12 oilseeds", "HS-88 aircraft", "HS-84 machinery"]
}
```

## What this loop produced

- The four-view layout: country flagship + bilateral matrix + flow map + product drill-down.
- The bilateral matrix UX as the headline feature with time scrubbing and click-to-drill.
- A capital-flow attribution layer over the BOP decomposition.
- Six adapter gaps named (IMF DOTS, Comtrade, UNCTAD, IIF, IMF BOP, plus WB extension).

## What comes next

- **L226** supply-chain bottleneck page (consumes Comtrade + PortWatch).
- **L217** FX misalignment (consumes BOP).
- **L225** alliances/sanctions (overlays on the bilateral matrix).

## Related

- [[L001-vision-statement]]
- [[L226-supply-chain-bottleneck]]
- [[L225-alliances-sanctions]]
- [[L217-exchange-rate-misalignment]]
- [[L216-sovereign-risk]] — capital flow signals
- [[L146-iconography-system]] — `ship`, `package`, `handshake`
