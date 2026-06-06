# L159 — Forecast Diff

**Loop**: 159 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

OPENGEM publishes vintaged forecasts. The single most differentiating chart we can show is:
- This is what we said TODAY.
- This is what we said LAST WEEK.
- This is what WEO says.
- This is what we got WRONG last quarter.

Diff is the form of accountability the cartel can't match. We design the visualization.

## The four diff comparators

Per forecast view, the user can layer four reference curves:

| Layer | Source | Default color |
|---|---|---|
| **Current** | This vintage's forecast | brand-amber |
| **Previous** | Same forecast at the previous vintage | info-400 (subtle blue) |
| **Consensus** | WEO, OECD EO, FRB SEP, ECB SPF (auto-selected) | neutral-500 |
| **Actuals** | Realized data (where applicable) | text-primary, thick |

Stacked, these form the diff visualization.

## The visualization, picked

**A small-multiples mini-strip below a primary fan chart.**

```
   ┌───────────────────────────────────────────────────────┐
   │  US CPI YoY — forecast 4Q ahead                        │
   │  ───────────────────────────────────────────────────  │
   │                                                        │
   │                              ╱─P90                     │
   │                          ╭───╯                          │
   │                      ╭───╯       P50 ──────             │
   │  Actuals ━━━━━━━━━╭──╯                                │
   │                  ╱     ╲────P10                        │
   │                ╱                                       │
   │   ────────────╳───┬───┬───┬───┬───┬                   │
   │                 0   1Q  2Q  3Q  4Q                     │
   │                                                        │
   ├───────────────────────────────────────────────────────┤
   │ DIFF                                                    │
   │ ┌───────┬─────────┬─────────┬─────────┬─────────┐    │
   │ │ Today │ -1wk    │ -1mo    │ WEO     │ OECD    │    │
   │ │ ▲0.3  │ +0.2pp  │ +0.5pp  │ -0.1pp  │ -0.2pp  │    │
   │ │       │ ⌃ same  │ revised │ above   │ above   │    │
   │ └───────┴─────────┴─────────┴─────────┴─────────┘    │
   └───────────────────────────────────────────────────────┘
```

The diff strip at the bottom shows:
- The current P50 forecast value
- Delta vs each comparator
- A directional badge (revised up, revised down, in line)

Click any diff cell → toggles the corresponding overlay on the main chart.

## The overlay mode

When the user toggles "show previous vintage," the previous P50 line overlays:

```
   ┌───────────────────────────────────────────┐
   │           ╱─P90 (current)                  │
   │       ╭───╯                                 │
   │   ╭───╯       P50 (current) ─────           │
   │   ╭ . . . . . P50 (previous, dashed) . .   │
   │  ╱     ╲────P10 (current)                  │
   │ ╱                                           │
   │ ──────────────────────────────────         │
   └───────────────────────────────────────────┘
```

Visual rules:
- Current = solid line + fill
- Previous = dashed line (no fill)
- Consensus = dotted line (no fill)
- Actuals = thick solid black/white

Color is reserved for current. Comparators are tonal (dashed/dotted/thick), not chromatic. This keeps the chart readable when 4 layers stack.

## Animation mode (the killer)

The toolbar "Animate revisions" button cycles through vintages over 10 seconds, showing the forecast morphing:

```
   t=0    t=1    t=2    t=3    t=4    t=5    t=6
   ───    ── ─   ─ ──   ─── ─  ────   ────   ────
                                         actual!
```

Each frame: vintage date stamp + the forecast at that vintage.

This is the GIF format from L155. The export-as-GIF button on this view emits the animation as a shareable GIF.

## The forecast-vs-realized diff

When sufficient time has passed for actuals to land:

```
   ┌───────────────────────────────────────────┐
   │  Forecast made 2025-09-01 for 2026-Q1     │
   │  ───────────────────────────────────────  │
   │  Forecast: 3.2% (P10=2.1%, P90=4.0%)      │
   │  Actual:   3.5%                            │
   │                                             │
   │  Error: +0.3pp                              │
   │  PIT:    0.71  (within band)                │
   │  CRPS:   0.42                               │
   │  Rank:   2nd of 5 vintages this quarter     │
   │                                             │
   │  vs WEO at same vintage: WEO 3.0%, error +0.5pp │
   │  vs OECD:                3.4%, error +0.1pp │
   │                                             │
   │  [ See post-mortem ]   [ See methodology ]  │
   └───────────────────────────────────────────┘
```

This tile is the accountability page's atom (L175). Each forecast-actual pair has one.

## The leaderboard diff

On the leaderboard (L133), each row shows a forecast's diff against the eventual actual and against consensus:

```
   Rank  Forecaster  CRPS  Error  vs WEO
   ──────────────────────────────────────
   1     OPENGEM     0.34  +0.1   beat by 0.4pp
   2     NY Fed      0.41  -0.2   beat by 0.1pp
   3     WEO         0.55  +0.5   —
   4     Bloomberg   0.63  +0.7   missed
```

## Implementation

- Library: D3 for the fan + overlay logic (Recharts is too rigid for vintage overlays)
- Data fetch: `/api/forecast/<id>?vintages=current,prev,prev-month&consensus=weo,oecd&actuals=1`
- Server returns a single JSON blob with all overlay curves
- Caching: per (id, set-of-vintages) tuple

## The "what changed" tooltip

Hovering a region where two forecasts diverge shows a tooltip:

```
   ┌─────────────────────────────────────┐
   │  Forecast at 2026-Q2                │
   │  Today:    P50 = 3.4%               │
   │  -1 week:  P50 = 3.2%               │
   │  Δ = +0.2pp (revised up)            │
   │                                     │
   │  Driver attribution:                │
   │  • CPI surprise +0.4pp (May print)  │
   │  • Wage growth slightly above prior │
   │                                     │
   │  [ See vintage diff ]                │
   └─────────────────────────────────────┘
```

Driver attribution is generated by the combiner pipeline (L189) and exposed via the API.

## Color rules

- Current forecast: brand-amber 500 fill (12% opacity for bands) + amber 700 line
- Previous vintage: info-500 dashed line, no fill
- Consensus: neutral-500 dotted line, no fill
- Actuals: text-primary 2px solid line + dot markers
- Realized-error region (when forecast is in the past): hatched semi-transparent overlay between forecast band and actual

The hatched overlay is critical: it's the "we got this wrong, and here's by how much" surface.

## Mobile

On viewports < 640px:
- Drop the diff strip below the chart
- Show only "Today vs Actual" + "Today vs WEO" pills
- Tapping a pill toggles the overlay
- Animation mode replaced by a "scrub" slider

## What we won't do

- Bar charts of forecast vs actual (looks like a stock app; reads as small data)
- Tornado diagrams for driver attribution (too high-context for the dashboard surface; reserve for methodology page)
- Side-by-side small multiples per vintage (eats space; the animation tells the story better)
- Floating annotation labels ("here's where we got it wrong") — let the user add those with the annotation layer (L156)

## Export formats

- PNG: the full diff visualization with diff strip
- GIF: the animated revision sequence
- CSV: the underlying numeric table (vintage, horizon, P50, P10, P90)
- JSON: API-native shape
- Notebook: reconstructs the diff in Python (L157)

## The terminal-feel touch

The diff cells use the JetBrains Mono numeric font (L147). Deltas are tabular and aligned. Direction badges use the iconography of L146 (`arrow-up-right`, `arrow-down-right`, `arrow-right`). The mini diff strip looks like a Bloomberg watch ticker — for a reason.
