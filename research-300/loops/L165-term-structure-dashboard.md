# L165 — Term-Structure Dashboard

**Loop**: 165 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The decision

**Pick: small-multiples of yield curves per country, with a "stack on one chart" toggle for cross-country comparison, plus a 3D surface view as the showcase mode.**

Yield curves want both per-country detail and cross-country comparison. We optimize for both, decisively.

## The atom: one country's yield curve

```
   ┌───────────────────────────────────────┐
   │  United States Treasury curve          │
   │  ──────────────────────────────────   │
   │                                         │
   │   5%─                                   │
   │      │  ╲                                │
   │   4%─    ╲___                            │
   │              ╲_____                      │
   │   3%─               ╲___                 │
   │                          ╲_____          │
   │   2%─                            ╲       │
   │                                          │
   │   1Y  2Y  3Y  5Y  7Y 10Y    20Y   30Y    │
   │                                          │
   │  10Y-2Y: -0.42  ⚠ inverted               │
   │  10Y-3M: -0.65  ⚠ inverted               │
   │  Curve type: inverted                    │
   │  Last: 2026-06-04                        │
   └───────────────────────────────────────┘
```

The card shows:
- Curve as a line across maturities
- Overlay: T-1 (yesterday), T-7 (last week), T-30 (last month) as fainter lines
- Key spreads underneath: 10Y-2Y, 10Y-3M
- Curve shape classification: inverted / normal / flat / humped / steep
- Vintage stamp

## Small-multiples view (default)

For the "yield curves across G7" view:

```
   Yield curves, G7
   ──────────────────────────────────────────────────
   ┌──────────┬──────────┬──────────┬──────────┐
   │ USA      │ DEU      │ FRA      │ GBR      │
   │ inverted │ normal   │ normal   │ flat     │
   │ ─╲___    │ ─╱──     │ ─╱──     │ ────     │
   ├──────────┼──────────┼──────────┼──────────┤
   │ JPN      │ ITA      │ CAN      │          │
   │ steep    │ steep    │ inverted │          │
   │ ─╱╱╱     │ ─╱╱──    │ ─╲___    │          │
   └──────────┴──────────┴──────────┴──────────┘
```

Each cell uses the same y-axis range (auto-computed from the union of all visible curves) so visual comparison is stable.

## "Stack on one chart" toggle

When toggled:

```
   All curves on one chart
   ──────────────────────────────────────────
                                                
   5%─                                          
                                                
   4%─  ─USA──╲                                 
              ╲___                              
   3%─        ──── ── ──   ─CAN_                
              GBR╲    ╲___                      
   2%─         FRA  ── ─DEU      ──             
                                                
   1Y  2Y  5Y  10Y  20Y  30Y                   
                                                
   Click a label to highlight; toggle to hide.
```

One line per country, colored by Tol categorical (L148). Use case: "are all G7 curves inverted, or just USA?"

## The 3D surface

Pick a country, then view its yield curve over time as a 3D surface:

```
        rate
         │   ╱──╲
         │  ╱    ╲___
         │ ╱         ╲___
         │/              ╲___
         ────────────────────
        date           maturity
```

- Library: `plotly.js` (handles 3D well, with rotation/zoom)
- Use case: "show me how the US curve has evolved over 5 years"
- Color encoding: positive (steep) = green, negative (inverted) = red

3D surface is the showcase view, not the default. The flat charts answer 95% of the questions.

## The spread strip

Below the small-multiples, a strip of key spreads across all countries:

```
   Key spreads (10Y-2Y)
   ──────────────────────────────────────────
   USA   DEU   FRA   GBR   JPN   ITA   CAN
   -0.42  +0.85  +0.71  +0.15  +1.35  +0.95  -0.18
   🔴    🟢     🟢     🟡     🟢     🟢     🔴
```

Color-coded: red = inverted, green = normal.

Click a country to focus its full curve above.

## The historical spread strip

Below that, the 10Y-2Y spread over the last 5 years per country:

```
   USA  10Y-2Y    ─╱╲╱─╲╱──╲___╱──╲╲   -0.42
   DEU  10Y-2Y    ─╱─╲╱──╱──╱╲─╱──    +0.85
   FRA  10Y-2Y    ─╱─╲╱──╱──╱─╲╱──    +0.71
   ...
```

Sparkline per country. Recession bands shaded (NBER official + country-specific).

## Curve classifier

Shape buckets:
- **Normal**: positive slope, monotonic
- **Steep**: positive slope > 1.5σ above 5y avg
- **Flat**: max-min < 50bp
- **Inverted**: negative slope across 10Y-2Y
- **Humped**: peak at mid-maturity

Each card shows a classification badge. Useful for at-a-glance scanning.

## Maturity sliders

The user can pick which maturities to show:

```
   Maturities:
   [☑ 1M] [☑ 3M] [☑ 6M] [☑ 1Y] [☑ 2Y] [☑ 5Y] [☑ 7Y] [☑ 10Y] [☑ 20Y] [☑ 30Y]
   ──────────────────────────────────────────────────────────────────────────
```

Default: 1Y, 2Y, 5Y, 10Y, 30Y (the "Treasury benchmark" set). Toggle on/off.

## Curve animation

"Animate over time" button plays the last 24 months as 24 monthly frames:

```
   t=0  t=1  t=2  ...  t=23
   ─╱─  ─╲─  ─╲___  ...  ─╲╱─
```

Frame stamp shows year/month. Exportable as GIF (L155).

Useful for telling the story of "watch the US curve invert in real time."

## Forward curves (forecast overlay)

For each country, toggle the OPENGEM-forecasted curve at horizons 3M, 6M, 12M ahead:

```
   USA today    ─╲___
   USA forecast 6M ─╲╱
   ```

Two lines, the forecast as a dashed line with bands. Bands controlled by L195 conventions.

## Real vs nominal

Toggle "Show real yields" — overlays TIPS / inflation-linked curves where available (US, UK, France, Japan, Germany).

## URL contract

```
/term-structure
/term-structure?cohort=g7
/term-structure?countries=usa,deu,fra,gbr&maturities=1y,2y,5y,10y,30y
/term-structure?country=usa&mode=3d
/term-structure?country=usa&compare=2024-06-04,2026-06-04
```

## The "shock" view

Pick a country + a date when a known event hit (e.g., Aug 2024 Japan FX shock, Sept 2024 Fed cut). The chart overlays the curve before/after the event:

```
   USA curve, Sept 18 2024 (Fed cut day)
   Before (Sept 17): ─╲___
   After  (Sept 18): ─╲___ (similar, but lower at short end)
   Delta:            ───── 50bp at front, 10bp at long end
```

Editorially curated event list available; user can pick a custom date.

## Implementation

- Library 2D: D3 line generator
- Library 3D: Plotly surface
- Server endpoint: `/api/term-structure?countries=...&date=...&maturities=...`
- Data sources: FRB H.15 for US, ECB SDW for euro area, BoE for UK, BoJ for Japan, Treasury Dept for Canada — auto-pulled
- Cache: 1h (yield curves move during NY trading hours; we don't need real-time intraday)

## Mobile

At <640px:
- One country at a time (the cohort tabs become a swipeable carousel)
- 3D mode disabled
- Spread strip becomes a list below the chart

## Coverage

Tier-V countries (full curves available): USA, GBR, DEU, FRA, ITA, JPN, CAN, ESP, NLD, SWE, NOR, CHE, AUS, NZL, CHN, IND, KOR, BRA, MEX. ~20 countries.

For other countries: we show what we have (often just policy rate + 10Y if available) and label the rest as "unavailable."

## Editorial

- "Inversion watch" curated list of countries with inverted curves, with editorial commentary
- "Steepest curves" list (often emerging markets in distress)
- "Recession signal strength" rollup: 10Y-2Y inversion duration per country, scored against historical recessions

These are the editorial entry points to the dashboard for the "is the world about to crash" question.

## What we won't ship

- Live order-book on bonds. Not our space.
- Implied OIS forward path with explicit cuts. We expose it via the policy-rate page (future loop) but not on term-structure.
- Credit curves (corporate). V2 — currently planning sovereign-only for L165.
