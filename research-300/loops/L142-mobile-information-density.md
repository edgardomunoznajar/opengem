---
loop: 142
phase: 3
title: Mobile Information Density — Portrait IA
date: 2026-06-06
status: decided
---

# L142 — Mobile Information Density

**Loop**: 142 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Portrait phone gets a different information architecture. Spec it.

OPENGEM's primary surface is desktop (per the personas — analyst, journalist, LP all work in 13-30" displays). Mobile is the *secondary* surface. But "secondary" does not mean "afterthought." A mobile user landing from a tweet, a Substack, or a press piece must get a coherent OPENGEM experience, not a degraded one.

## The mobile audience

Three primary mobile use cases:

1. **Quick check.** "What is the recession probability for the US right now?" Time-on-page: 30 seconds.
2. **Shared link.** "Someone tweeted a Trade-LATAM scenario; let me see what it is." Time-on-page: 2-3 minutes.
3. **Read the briefing.** Morning commute, reading the daily digest email and tapping through to read more. Time-on-page: 5-10 minutes.

None of these requires the full desktop density. All three require the page to load fast, render legibly, and let the user accomplish one task.

## The portrait reshape

Five rules govern the portrait IA:

1. **Six-slot top nav becomes four-slot bottom nav.**
2. **Right rails collapse below main content (not adjacent).**
3. **Drawers become bottom sheets.**
4. **Strips become horizontal-scroll tiles.**
5. **Tables become card lists.**

### Rule 1 — Six-slot nav → four-slot bottom nav

Desktop top nav: World / Countries / Indicators / Scenarios / Forecasts / Ledger.

Portrait bottom nav: **World / Explore / Ledger / Search**.

```
[ World ] [ Explore ] [ Ledger ] [ 🔍 ]
```

- **World** stays as the home.
- **Explore** is a collapsed Countries + Indicators + Scenarios + Forecasts. Tapping Explore opens a section selector.
- **Ledger** stays (it is brand-load-bearing).
- **Search** is the fourth slot. It opens the command bar (L128).

The bottom nav uses iOS-tab-bar conventions: sticky, ~56px tall, brand-tinted active state.

Sign-in lives in the Explore section header (top-right), not the nav.

### Rule 2 — Right rails collapse below

On desktop, country / indicator / scenario pages use a left-60% / right-40% split. On portrait, the right rail moves *below* the left content. The user scrolls past the primary content to reach the secondary rail.

For the country page (L123):
- First fold: header tile.
- Second fold: forecast strip.
- Third fold: forecast detail (with tabs).
- Fourth fold: situation tile (recession probability + GPR).
- Fifth fold: scenarios triggered.
- Sixth fold: event feed.
- Seventh fold: methodology link (button to open bottom sheet).

This is intentional fold ordering: the primary information is in the first three folds; the secondary information is below.

### Rule 3 — Drawers become bottom sheets

Right-edge slide-out drawers (provenance, methodology, watchlist) become bottom sheets on portrait. Tapping `[ⓘ provenance]` slides up from the bottom (iOS modal sheet convention).

The bottom sheet is draggable: drag-down to dismiss, drag-up to maximize to full screen.

Content inside the sheet uses the same structure as desktop but at portrait widths.

### Rule 4 — Strips become horizontal-scroll tiles

The desktop "strip" pattern (6 headline numbers in a row, e.g., on the World page or the Country page) does not fit on portrait. Convert to horizontal scroll:

```
| GPR 132▲ | RecProb 32%▲ | CPI 4.1%▼ | GSCPI 0.32▲ → swipe
```

The user can swipe horizontally to see all 6 numbers. Tap any tile for the indicator page. Snap-to-tile carousel UX.

The number of tiles is unchanged from desktop. We do not omit information — we change presentation.

### Rule 5 — Tables become card lists

Desktop scoreboard / leaderboard / hit-rate tables (per L133, L134) do not fit on portrait. Convert to card list:

```
+----------------------------+
| 1. OPENGEM L3-BMA           |
| CRPS 0.842 · PIT 0.78       |
| Bias -0.04 · MAE 0.31       |
+----------------------------+
| 2. FRB SEP                  |
| CRPS 0.871 · PIT 0.74       |
| ...                          |
+----------------------------+
```

One card per row. Sort and filter controls are at the top.

## Per-page mobile shape

### World page (mobile)

```
+----------------------------+
| OPENGEM ☰  📝 2026-06-06   |
+----------------------------+
| HEADLINE                    |
| "Trade-LATAM and Red-Sea    |
|  packs fired; EZ recession  |
|  risk +3pp"                 |
|                            |
| [view scenario]              |
+----------------------------+
| STRIP (horizontal scroll)   |
| GPR 132▲ | RecProb 32%▲ | → |
+----------------------------+
| WATCHLIST (if exists)       |
| 🇺🇸 USA  RecProb 34%▲       |
| 🇪🇺 EUR  RecProb 41%▲       |
| 🇨🇳 CHN  RecProb 19%▼       |
+----------------------------+
| TODAY'S SCENARIOS (4)       |
| [card list, 1 per row]      |
+----------------------------+
| TODAY'S EVENTS (12)         |
| [card list, 1 per row]      |
+----------------------------+
| FOOTER STRIP                 |
| Open ledger calibration 0.72|
| [/ledger]                    |
+----------------------------+
[ World ][ Explore ][ Ledger ][ 🔍 ]
```

### Country page (mobile)

```
+----------------------------+
| ← USA                       |
+----------------------------+
| HEADER TILE                  |
| 🇺🇸 UNITED STATES            |
| GDP 2.4% ▲0.1               |
| CPI 2.9% ▼0.2               |
| Unemp 3.7%  PR 5.25%        |
| 4-tile P50 minibar          |
+----------------------------+
| STRIP                       |
| RecProb 34%▲ GPR 89▲ →      |
+----------------------------+
| FORECAST (tabbed)            |
| [GDP | CPI | Unemp | PR]    |
| chart with bands             |
+----------------------------+
| SCENARIOS (4)                |
| [card list]                  |
+----------------------------+
| RECENT EVENTS                |
| [card list]                  |
+----------------------------+
| [Methodology] [Watchlist+]   |
+----------------------------+
[ World ][ Explore ][ Ledger ][ 🔍 ]
```

### Indicator page (mobile)

```
+----------------------------+
| ← CPI YoY                   |
+----------------------------+
| HEADLINE                     |
| World aggregate 4.1% ▼      |
| P50 4Q 3.6%                  |
| Consensus 3.9%               |
+----------------------------+
| SMALL-MULTIPLES (1-column)  |
|                            |
| 🇺🇸 USA 2.9% ▼   sparkline    |
|       P50 4Q 2.6%           |
|       consensus 2.8         |
| ────                         |
| 🇪🇺 EUR 2.4% ▼   sparkline   |
|       ...                    |
| ────                         |
| (one per row, scroll for     |
|  the full G20)              |
+----------------------------+
| CONTROLS (sticky bottom)    |
| [Vintage] [Horizon] [...]   |
+----------------------------+
[ World ][ Explore ][ Ledger ][ 🔍 ]
```

The 19-panel grid becomes a 1-column list. Each row is a card with the country, the value, the spark, the band, and the consensus dot.

### Forecast page (mobile)

```
+----------------------------+
| ← US CPI YoY 4Q             |
+----------------------------+
| HEADLINE                     |
| P50 2.6%                     |
| P10-P90 1.9% - 3.4%          |
| Consensus 2.8% (-0.2pp)      |
+----------------------------+
| MAIN CHART (full width)     |
+----------------------------+
| VINTAGE REWIND               |
| [slider, large touch target]|
+----------------------------+
| MISS LOG (card list)         |
| [last 8 vintages]            |
+----------------------------+
| MODEL CARD (summary, expand) |
+----------------------------+
| [Full model] [Replay] [API] |
+----------------------------+
[ World ][ Explore ][ Ledger ][ 🔍 ]
```

The model card collapses to a one-tap-to-expand summary on mobile. Full model card opens in a bottom sheet.

### Scenario page (mobile)

```
+----------------------------+
| ← Trade-LATAM                |
+----------------------------+
| HEADER                       |
| Trade-LATAM                  |
| Status: FIRED today          |
| Global P: 0.62               |
| Affects: 12 countries        |
+----------------------------+
| NARRATIVE                    |
| (3 paragraphs)               |
+----------------------------+
| AFFECTED MAP                 |
| (full-width, square)         |
+----------------------------+
| PROBABILITY ROLLUP           |
| (card list per country)      |
+----------------------------+
| TRIGGER CONDITIONS           |
+----------------------------+
| RELATED SCENARIOS            |
+----------------------------+
| [Methodology] [Alert me]     |
+----------------------------+
```

### Pricing page (mobile)

Tiers stack vertically. Calibration scorecard remains horizontal-scroll table.

### Compare-2 page (mobile)

Tab-stack: one side at a time with a chip control to swap. Diff strip always visible at the bottom.

```
+----------------------------+
| ← Compare USA vs EUR        |
+----------------------------+
| [ 🇺🇸 USA |  🇪🇺 EUR ] tabs   |
+----------------------------+
| USA · CPI YoY                |
| 2.9% ▼ P50 4Q 2.4%          |
| chart                       |
| scenarios + events         |
+----------------------------+
| DIFF                        |
| CPI gap: USA +0.5pp         |
| P50 4Q gap: USA +0.2pp      |
| ...                          |
+----------------------------+
| [Swap sides ⇄]              |
+----------------------------+
```

## What is NOT done on mobile

- **Globe.gl 3D globe**: not loaded. Replaced by a flat regional map.
- **Vintage rewind animation play**: button hidden; vintage slider works but no play mode.
- **Replay-and-diff**: button hidden; user must use desktop to launch a replay job (the CI job page is desktop-only).
- **Embed widget preview**: redirect to /docs/embed for the desktop view.
- **Print tearsheet**: not directly invocable from mobile; user opens the share menu and emails themselves a link to the desktop print view.

These are explicit *exclusions* with rationale (mobile cannot reliably afford the rendering cost or the precision target).

## Typography on mobile

- Base: 14px (vs 13px desktop dense).
- Headline: 24-28px.
- Min tap target: 44pt × 44pt (iOS HIG).
- Line height: 1.5 (vs 1.4 desktop).
- Color: identical to desktop theme (per L145).

The slightly larger base font and line height trades density for legibility. The density loss is compensated by the per-page reshape rules above.

## Performance budget

- First Contentful Paint: ≤1.5s on mid-tier 4G.
- Largest Contentful Paint: ≤2.5s.
- Time-to-Interactive: ≤3.5s.
- Bundle size: ≤180KB gzipped for the World page critical path.

The mobile-first build optimizes for these. Heavy charts use Lightweight Charts (≤45KB gzipped) instead of Plotly (≥800KB gzipped). The globe and any 3D rendering are excluded entirely on mobile detection.

## PWA install prompt

OPENGEM offers a Progressive Web App install on mobile. After the user has visited 3 times (deduped sessions), an install prompt appears:

```
+----------------------------+
| OPENGEM on your home screen |
| One tap to the world feed.   |
| [Install]  [Not now]         |
+----------------------------+
```

Install yields:
- Home-screen icon.
- Offline-capable read of the most recent watchlist data.
- Background sync of the daily digest.

## Mobile-specific keyboard shortcuts

None. Touch interfaces do not have keyboard shortcuts. The command bar (`⌘K` on desktop) is reachable on mobile via the bottom-nav Search icon.

## What this loop produced

- Five rules for portrait reshape: 6-slot nav → 4-slot bottom nav; right rails collapse below; drawers become bottom sheets; strips become horizontal-scroll tiles; tables become card lists.
- Per-page mobile spec for World, Country, Indicator, Forecast, Scenario, Pricing, Compare-2.
- Explicit exclusions on mobile (globe, vintage play, replay-and-diff, embed preview, direct print).
- Typography: 14px base, 44pt tap targets, 1.5 line-height.
- Performance budget: FCP ≤1.5s, LCP ≤2.5s, TTI ≤3.5s, 180KB critical path.
- PWA install prompt after 3 deduped sessions.

## What comes next

- **L115** integrates with: PWA-first thesis.
- **L263** prototypes the mobile layout in code.
- **L267** sets up the Lighthouse perf budget for the mobile build.

## Related

- [[L121-information-architecture]] — six-slot nav collapses to four
- [[L122-home-screen]] — World page mobile shape
- [[L123-country-page]] — country page mobile shape
- [[L132-provenance-drawer]] — drawer becomes bottom sheet
- [[L145-dashboard-themes]] — colors carry across to mobile
- [[L263-mobile-layout-prototype]] — code prototype
- [[L267-lighthouse-perf-budget]] — perf budget enforcement
