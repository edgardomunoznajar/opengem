# L161 — Country-Card Grid Pattern

**Loop**: 161 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

The country grid is OPENGEM's "world view." It's the page a YouTuber or journalist opens when their question is "what's happening globally right now?" We design it as a **grid of grids** — pre-defined country sets (G20, G7, etc.) each rendered as a small-multiples card grid.

## The country card (atom)

```
   ┌─────────────────────────────────────────┐
   │ 🇩🇪 Germany                       g d  │
   │  ───────────────────────────────────    │
   │                                          │
   │  CPI YoY       3.4%   ▲ +0.2pp           │
   │  ─╱─╲╱─        (Apr 2026)                │
   │                                          │
   │  GDP nowcast   1.1%   ▼ -0.1pp           │
   │  ──╲╱──                                  │
   │                                          │
   │  Unemp         5.6%   ⌃ flat            │
   │  ──╲──                                   │
   │                                          │
   │  Policy rate   3.50%  ⌃ held             │
   │  ───────                                 │
   │                                          │
   │  Pulse:  ⚠ stressed                      │
   └─────────────────────────────────────────┘
   width: ~280px
   height: ~280px (square-ish)
```

Card components:
- Flag + country name + ISO3 (top-right)
- 4 default indicators, each with: value + delta badge + sparkline
- "Pulse" status (composite signal — see below)
- Click anywhere → country page

Density: 4 indicators × 1 sparkline each = 4 density units (per L149). Card budget: 5 units.

## The "grid of grids" — pre-defined cohorts

The top of the world page offers cohort tabs:

```
   [ All ] [ G7 ] [ G20 ] [ EU ] [ ASEAN ] [ BRICS ] [ OECD ] [ Custom ]
```

Selecting a cohort reflows the grid:

### G7 layout
3 columns × 3 rows (one cell empty):
```
   ┌────────┬────────┬────────┐
   │ 🇺🇸 USA │ 🇩🇪 DEU │ 🇫🇷 FRA │
   ├────────┼────────┼────────┤
   │ 🇮🇹 ITA │ 🇯🇵 JPN │ 🇬🇧 GBR │
   ├────────┼────────┼────────┤
   │ 🇨🇦 CAN │   —    │   —    │
   └────────┴────────┴────────┘
```

### G20 layout
5 columns × 4 rows:
```
   ┌──┬──┬──┬──┬──┐
   │  │  │  │  │  │
   ├──┼──┼──┼──┼──┤
   │  │  │  │  │  │
   ├──┼──┼──┼──┼──┤
   │  │  │  │  │  │
   ├──┼──┼──┼──┼──┤
   │  │  │  │  │  │
   └──┴──┴──┴──┴──┘
```

### EU layout (27)
6 columns × 5 rows (27 fits with 3 empty):
EU members in alphabetic order.

### ASEAN (10)
5 columns × 2 rows.

### BRICS (11)
4 columns × 3 rows (one empty).

### OECD (38)
5 columns × 8 rows.

### All (200+)
A virtualized grid (TanStack Virtual or react-window) — paginated by region with filters.

### Custom
User-defined cohort. Saved per account. Up to 50 countries.

## Ordering within a cohort

Default: by GDP descending. Stable, doesn't surprise.

Toggle: "Sort by..."
- GDP (default)
- Population
- Recent CPI surprise
- Pulse score (descending stress)
- Alphabetic

A small sort dropdown above the grid.

## The "pulse" badge

Each card carries a single composite-signal pulse:

| Pulse | Visual | Trigger |
|---|---|---|
| `calm` | green dot | All four indicators within normal range |
| `mixed` | yellow dot | One indicator beyond 1σ |
| `stressed` | orange dot | Two+ indicators beyond 1σ |
| `crisis` | red badge | Multiple indicators beyond 2σ OR explicit crisis flag |
| `stale` | gray | Data >30d behind expected cadence |

Pulse is computed from the same indicator set displayed on the card. Hover for breakdown.

## The cohort overlay (the "grid of grids")

When the user hovers over a tab, the grid morphs to show the cohort layout with subtle highlight on member countries — making the cohort *spatially memorable*. This is the "grid of grids" pattern: each cohort gets its own spatial signature so the user can visually identify "the G7 grid" from "the EU grid."

For paying users, the world view shows TWO cohorts side-by-side (e.g., G7 on the left, ASEAN on the right). For free users: one cohort at a time.

## Indicator-picker per cohort

The default 4 indicators are: CPI, GDP, Unemp, Policy Rate. The user can swap (per cohort, saved):

```
   Indicators shown:
    1. CPI YoY                  [change ▼]
    2. GDP nowcast              [change ▼]
    3. Unemployment             [change ▼]
    4. Policy rate              [change ▼]
   [ + add 5th ]                (paid)
```

Free tier: exactly 4. Paid: up to 6.

## Watchlist as a cohort

A user's watchlist is treated as a cohort. Tab labeled "Watchlist" appears when the user has saved any country.

## URL pattern

```
/?cohort=g7
/?cohort=g20&sort=pulse
/?cohort=custom&id=<watchlist-id>
/?cohort=g7&indicators=cpi-yoy,gdp-nowcast,unemp,policy-rate
```

Per L154, the URL is deep-linkable. Sharing a cohort view shares everything.

## Mobile reflow

At < 640px:
- Tabs collapse to a dropdown
- Grid becomes 1 column (vertical stack of cards)
- Each card retains the 4 indicators
- Page is intentionally long — scrolling is fine

At 640–1024px:
- 2 columns
- Cohort tabs visible

## The card's interactive layer

- Hover card: subtle border highlight
- Click country name → country page (per L154)
- Click sparkline → drawer with mini-chart (L149 Level 3)
- Click delta badge → tooltip with provenance
- Click pulse dot → tooltip explaining the composite
- Right-click → context menu (compare, watch, alert)

## Empty states

If a country has no data for a slot (e.g., a small emerging economy missing reliable CPI):

```
   CPI YoY       —     (no data)
   ─────────              
```

The card is not removed — explicit absence is visible. The pulse downgrades.

## Server data

One endpoint:

```
GET /api/cards?cohort=g7&indicators=cpi-yoy,gdp-nowcast,unemp,policy-rate&vintage=2026-06-04
```

Returns:

```json
{
  "vintage": "2026-06-04",
  "cohort": "g7",
  "countries": [
    {
      "iso3": "USA",
      "indicators": [
        { "id": "cpi-yoy", "value": 3.4, "delta": 0.2, "spark": [3.1, 3.2, 3.3, 3.4, 3.4, 3.6, 3.4] }
      ],
      "pulse": "mixed"
    }
  ]
}
```

Cached aggressively. CDN-edge served.

## Cohort customization (paid)

Paid tier: define "my cohort" — e.g., a sovereign fund tracks 23 specific countries. The custom cohort is shareable via URL.

## The seventh tab: "Hot now"

Auto-populated by ranking pulse scores across all 200+ countries. Top 12 stressed countries today. Visualizes "where's the world tense."

## Implementation

- Layout: CSS grid with responsive auto-fill
- Virtualization: TanStack Virtual for the "All" view
- Card rendering: server-component-first, sparklines hydrated client-side
- State: cohort + indicators persisted in localStorage, mirrored to URL
- Animation: 200ms layout transition when changing cohorts

## Performance

- "All countries" view: 230+ cards rendered. With virtualization, only ~30 visible at once.
- Sparklines: pre-rendered SVG strings server-side for the first viewport, hydrated for interaction.
- Total payload: target <120KB initial HTML + 80KB JS for the cohort grid.
