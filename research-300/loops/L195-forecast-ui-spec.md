# L195 — Forecast UI on the Chart: Final Spec

**Loop**: 195 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

The forecast chart is the dashboard's signature visual. It must show, in one frame, on a 320 px phone and a 2560 px monitor:

1. The realised history.
2. The OPENGEM forecast bands at five horizons.
3. The consensus overlay (WEO / OECD EO / FRB SEP / ECB SPF).
4. The revision arrow (toggleable).
5. The miss-log link.

This loop pins the final spec — what is on the chart by default, what is toggleable, what tooltips render, what API powers it.

## Chart anatomy at default load

```
┌──────────────────────────────────────────────────────────────────────────┐
│ USA · Real GDP YoY · 4Q ahead             [share] [embed] [API] [CSV]    │ ← header bar
│ Last updated 2026-06-06 08:00 UTC · model OPENGEM L3 BMA v3.2.1 [card]   │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  6%┤                                                                     │
│    │           realised line                                             │
│  4%┤             ╱                                                       │
│    │           ╱     ╱╲                                                  │
│    │         ╱  ╲   ╱  ╲                                                 │
│  2%┤───────╱─────╲─╱────╲──●═══════════════ P50 = 2.18                   │
│    │     ╱        ╲       ╲▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ P10-P90 80% band            │
│    │   ╱                    ◆ WEO 2.10        Δ ▲ OECD EO 2.05           │
│  0%┤                            ■ FRB SEP 2.20                           │
│    │                                                                     │
│    └────────────────────────┬─────────────────────────────────────────►  │
│    2020   2022   2024   2026  | 2027 (target)                            │
│                              now                                         │
│                                                                          │
│ ╭───────────────╮ ╭───────────────╮ ╭───────────────╮ ╭───────────────╮  │
│ │ TRUST BADGES  │ │ TRACK RECORD  │ │ MISS LOG      │ │ DOWNLOAD      │  │
│ │ ▣ vintage-cor │ │ vs AR(1): 83% │ │ 3 recent miss │ │ JSON · CSV    │  │
│ │ ▣ ensemble-3  │ │ vs WEO: ✓ DM  │ │ → 2025-Q1     │ │ Parquet · PDF │  │
│ │ ▣ pit-passed  │ │ PIT-KS: 0.42  │ │ → 2023-Q4     │ │ embed snippet │  │
│ ╰───────────────╯ ╰───────────────╯ ╰───────────────╯ ╰───────────────╯  │
│                                                                          │
│ [ Bands: 80% ▼ ]  [ Show prior vintage ]  [ Show consensus ]  [ Tab: chart/data/sources/methodology ] │
└──────────────────────────────────────────────────────────────────────────┘
```

## Element-by-element spec

### Header bar

- Country name, indicator label, horizon.
- "Last updated" timestamp.
- Model identifier with link to model card (L181 `model_card_url`).
- Action icons: share (copy permalink), embed (iframe snippet), API (curl/Python/Java snippets), CSV download.

### Main chart panel

| Layer | Style | Toggleable |
|---|---|---|
| Realised history | solid 1.5 px line, brand colour | No (always on) |
| OPENGEM P50 line | solid 2 px line, brand colour, dashed beyond `now` | No |
| OPENGEM 80% band (P10-P90) | shaded region, 30% opacity teal, widens with horizon | Toggleable via band selector |
| OPENGEM 50% band (P25-P75) | shaded region, 60% opacity teal, nested | Toggle via "expand fan" |
| Consensus markers (4) | distinct shapes per source: ◆ WEO ▲ OECD ■ FRB ★ ECB | Toggle group "Show consensus" |
| Vertical "now" line | dotted black, "now" label | No |
| Revision arrow | solid arrow from prior P50 to current P50 | Toggle "Show prior vintage" |
| Realised target value (after target date passes) | solid black dot, label | Auto on once date passes |
| Multi-vintage trajectory (faded lines) | five most recent prior vintages, 30% opacity | Toggle "Show vintage history" |

### Hover tooltips

| Hover target | Tooltip content |
|---|---|
| Any P50 point | "Date / Forecast P50 = X / Band P10-P90 = [X, Y] / Vintage_id" |
| Consensus marker | "Source / Vintage / Value / Horizon-match note (L190)" |
| Revision arrow | "Δ = -0.12 pp / Drivers: data -0.08, code -0.02, weights -0.01" |
| Realised target | "Realised on date / Value / OPENGEM error / WEO error / OECD EO error" |

Tooltips are accessible (aria-described-by) and keyboard-navigable (left/right arrows step through points).

### Trust badges panel

A horizontal strip below the chart shows up to 4 trust badges from the L199 catalog. Each badge is a small chip with an info icon → opens a popover with the badge's earning criterion and a verification link.

### Track record panel

A condensed view of the cell's leaderboard performance:

- CRPS-vs-AR(1) win rate (e.g. "83%").
- DM-vs-WEO verdict (e.g. "✓ not statistically worse, p=0.42").
- PIT-KS p-value (e.g. "0.42, passes").
- Click-through to the calibration plot (L193) and full V&V cell page.

### Miss log panel

Last 3 most recent forecast errors > 1 standard deviation:

- Date of realised.
- Magnitude of miss.
- Click-through to that vintage's post-mortem (L200).

### Download panel

- JSON: the full `forecast.v1` object.
- CSV: the realised + forecast time series.
- Parquet: the density samples.
- PDF tearsheet: a printable summary for paid Pro users (white-labelled for Institutional tier).
- Embed snippet: `<iframe src="https://opengem.org/embed/forecast/{forecast_id}"></iframe>`.

### Control row

- **Bands selector**: "80% (default)" / "50%" / "90%" / "All quantiles".
- **Show prior vintage**: toggles revision arrow.
- **Show vintage history**: toggles multi-vintage trajectory.
- **Show consensus**: toggles consensus markers (all 4 on by default).
- **Tab strip**: chart / data table / sources / methodology.

The "data" tab shows the raw realised + forecast table; the "sources" tab lists every input series with its vintage; the "methodology" tab is the model card excerpt.

## Mobile-specific changes

On screens < 768 px:

- Trust + track record + miss log + download collapse into a sliding bottom drawer.
- Consensus markers stack vertically with explicit labels (no shape-only).
- Default band shrinks to 50% (P25-P75) — narrower band reads better on small screen.
- Tabs become a scrollable horizontal strip.

## Performance budget

- Initial page weight: ≤ 60 KB gzipped HTML+CSS+critical JS.
- First contentful paint: ≤ 1.0 s on 4G.
- Time to interactive: ≤ 2.5 s.
- The chart library is Lightweight Charts (cf. L015 / L131). The data API call is a single round trip returning the `forecast.v1` JSON + history series.

## URL scheme

```
https://opengem.org/forecast/{country}/{indicator}/{horizon}
```

Examples:

- `/forecast/USA/GDP-real-yoy/4Q`
- `/forecast/JPN/CPI-headline-yoy/1Q`
- `/forecast/EA/HICP-yoy/2Y`

Query params for view state:

- `?vintage_id=` — pin to a specific historical vintage.
- `?bands=80|50|90|all` — band default.
- `?show_revision=1` — revision arrow on.
- `?show_history=1` — multi-vintage trajectory on.

The URL is the share-target; views are deep-linkable.

## Embed surface

A separate `/embed/forecast/{forecast_id}` route returns the chart only (no header bar, no tabs, no panels), sized for iframe. Bloggers and Substack writers paste:

```html
<iframe
  src="https://opengem.org/embed/forecast/fcst_2026-06-06_USA_GDP_4Q_OPENGEM-L3-BMA_v3.2.1"
  width="100%" height="320" frameborder="0" loading="lazy"
  title="OPENGEM USA Real GDP 4Q-ahead forecast">
</iframe>
```

The embed is the L008 distribution lever — every chart pasted into a Substack is a backlink.

## API endpoints powering the chart

```
GET /v1/forecast/{country}/{indicator}/{horizon}       → forecast.v1 JSON
GET /v1/realised/{country}/{indicator}                  → realised time series
GET /v1/consensus/{country}/{indicator}/{horizon}       → consensus markers per L190
GET /v1/revisions/{country}/{indicator}/{horizon}       → revision history per L192
GET /v1/badges/{forecast_id}                            → trust badges per L199
```

The chart bundles 5 calls into a single batch via `GET /v1/forecast-card/{country}/{indicator}/{horizon}` which returns the union. One round trip on the wire; the dashboard never hits 5 endpoints serially.

## What this loop produced

- Final chart anatomy.
- Layer-by-layer style and toggleability.
- Tooltip content per hover target.
- Trust + track record + miss log + download panels.
- Mobile collapse behaviour.
- URL scheme + query params for shareable views.
- Embed iframe surface.
- API endpoint set powering the chart.

## What comes next

- **L196** — scenario triggers that may render an overlay band on the chart.
- **L198** — narrative LLM segment shown in a sidebar.

## Related

- [[L181-forecast-object-schema]] — JSON contract.
- [[L188-band-quantiles]] — band defaults.
- [[L190-consensus-comparison]] — markers.
- [[L192-forecast-revisions]] — revision arrow.
- [[L193-calibration-plots]] — link target.
- [[L199-trust-signals]] — badge panel source.
- [[L200-failure-log]] — miss-log link target.
- [[L008-differentiation]] — embed-as-distribution thesis.
