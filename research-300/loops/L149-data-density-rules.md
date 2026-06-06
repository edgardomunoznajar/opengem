# L149 — Data-Density Rules

**Loop**: 149 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The rule, in one sentence

**Use the smallest data viz that lets the user answer the next question without a click.**

If they need a click anyway, downgrade further. If they can't answer at all, upgrade.

## The four density levels

| Level | Format | Information conveyed | Space |
|---|---|---|---|
| 0 | **Number-only** | Current value | 1 cell |
| 1 | **Badge / lozenge** | Value + state (up/down/neutral) | 1 cell |
| 2 | **Sparkline** | Recent trajectory + current | 1 row (~120×24px) |
| 3 | **Mini-chart with axis** | Trajectory + scale + key levels | tile (~280×120px) |
| 4 | **Full chart** | All of above + bands, overlays, interaction | full panel |

## The decision tree

```
            ┌── Q: Can user answer THE next question
            │       with just the number?
            │       YES → Level 0
            └── NO ──┐
                    ├── Q: Is the next question
                    │       "is it good or bad / up or down"?
                    │       YES → Level 1 (badge)
                    └── NO ──┐
                             ├── Q: Is the next question
                             │       "how has it moved recently"?
                             │       YES → Level 2 (sparkline)
                             └── NO ──┐
                                      ├── Q: Does the user need to
                                      │       compare ranges or read levels?
                                      │       YES → Level 3 (mini-chart)
                                      └── NO ──┐
                                                YES → Level 4 (full)
```

## Worked examples

### Country card on the world grid (L161)

- User question: "is Germany inflation hot?"
- Decision: Level 1 (a 12-month change with a directional badge) + Level 2 (sparkline for context) stacked. Total: ~280×80px.

### Indicator row in a watchlist

- User question: "where is this now and what did it just do?"
- Decision: Level 1 in two columns (latest value, day's change) + Level 2 (sparkline of last 30 obs).

### Forecast panel on the country page

- User question: "what is the model saying, with bands, vs consensus?"
- Decision: Level 4 — full chart with P10/P50/P90 bands, consensus overlay, vintage marker.

### Geopolitical pulse card

- User question: "is the world calmer or hotter today?"
- Decision: Level 0 — a single number (the GPR composite) + tiny arrow. Click for Level 4 globe.

## Lozenge / badge anatomy

```
   ┌─────────────┐
   │ ▲ +0.4 pp   │   ← chip background = bg-good-100 (light) / bg-good-900 (dark)
   └─────────────┘     foreground = text-good-700 / text-good-200
                       border-radius = 4px
                       padding = 2px 8px
                       font: text-xs, font-medium, tabular-nums
```

Three variants by direction: `good` (up = positive context), `bad` (down), `neutral`. Note that "up" is not always "good" (e.g., unemployment up = bad), so we map by *outcome* not by *direction*. Use the `polarity` token on the indicator to flip.

## Sparkline anatomy

```
   ──────────╱──╲╱──   ← 1.5px stroke
                       last point: 3px filled circle in semantic color
                       no axes, no labels
                       width: 96–160px, height: 20–32px
                       padding: 2px top, 2px bottom (for stroke endpoints)
```

- Stroke color: `text-secondary` (neutral) — never use a categorical color, because rows of sparklines look like a Christmas tree.
- Endpoint dot: tiny, in semantic color, encoding most-recent direction.
- Tooltip on hover: shows period covered + min/max. No interactive scrubbing at this size — that requires Level 3.

Library: hand-rolled SVG generator (no Recharts overhead at this scale; 200 sparklines on a page must render in <16ms).

## Mini-chart anatomy

```
   ┌─────────────────────────┐
   │           ╱╲            │
   │      ╱╲  ╱  ╲___        │
   │     ╱  ╲╱       ╲       │
   │ ___╱             ╲___   │
   │                         │
   │ Jan  Apr  Jul  Oct      │   ← axis only at bottom, 3–4 ticks
   └─────────────────────────┘
   ~280 × 120 px
```

Includes:
- One axis (x always, y sometimes if range matters)
- 3–5 ticks max
- Subtle horizontal gridline at zero or trend reference
- Single series, semantic color
- Tooltip on hover (Level 3 always interactive)
- Click → upgrades to Level 4 in a drawer or new tab

## Full chart anatomy

See L195 (Forecast UI). Includes bands, overlays, vintage markers, brushable x-axis, annotations layer (L156), methodology pop-up (L172).

## The "stop adding" rule

Three explicit anti-patterns:

1. **Don't add a sparkline next to a badge that already encodes direction.** Pick one. If both, ask why.
2. **Don't add a number label to a sparkline.** That's what Level 3 is for.
3. **Don't show a full chart at <400px wide.** Downgrade to mini-chart at that breakpoint.

## Page-level density budgets

Each page has a maximum **density budget** in "data ink units":

| Page | Budget | What it buys |
|---|---|---|
| World home | 80 units | 40 country-card sparklines + 20 KPI tiles + 10 grid tiles + 10 ledger items |
| Country page | 100 | Hero KPI + 30 indicator mini-charts + 8 forecast panels |
| Indicator page | 60 | 1 full chart + 25 country comparison rows (each 1 sparkline + 1 badge) |
| Scenario page | 40 | 4 full charts + scenario tree + probability bar |
| Forecast page | 50 | 1 full chart + diff overlays + leaderboard table |

(Unit defined heuristically: a badge = 1, a sparkline = 1, a mini-chart = 3, a full chart = 8, a KPI tile = 1.)

The budget is checked at design review. Going over forces a downgrade somewhere.

## Implementation tokens

```ts
export const density = {
  // sparkline
  sparkWidth: 120,
  sparkHeight: 24,
  sparkStroke: 1.5,
  sparkPad: 2,

  // mini-chart
  miniWidth: 280,
  miniHeight: 120,
  miniTickCountX: 4,
  miniTickCountY: 0, // suppress unless range needed

  // full chart
  fullMinWidth: 480,
  fullMinHeight: 280,
  fullPad: { t: 16, r: 16, b: 32, l: 48 },
}
```

## Mobile demotion ladder

On viewports < 640px:
- Level 4 → Level 3 (mini-chart in a card, tap to open full in a drawer)
- Level 3 → Level 2 (sparkline + a "Full chart →" affordance)
- Level 2 → stays
- Level 1 → stays
- Level 0 → stays

L142 (mobile density) extends this with stacking and pagination rules.

## "What if I just need to see THE number" rule

Some moments warrant Level 0 splashed huge — the inflation print on release day, the recession-probability tile (L166), the policy rate dot. The mega-numeric token from L147 (72px) renders these. One per page maximum. The rest must work at lower density.
