# L243 — Command palette prototype

**Loop**: 243 / 300
**Phase**: 5 — Code prototypes
**Date**: 2026-06-06
**Artifact**: `prototypes/dashboard-next/components/CommandPalette.tsx`

---

## What was built

`⌘K` (Ctrl+K on Linux/Windows) opens a Bloomberg-style command palette over the entire dashboard. Type-ahead filtering, grouped results, route-on-enter.

## Why this matters

The command palette is the *single most important UX affordance* for a terminal-feel dashboard. Without it, OPENGEM is just another web app. With it, a user can ⌘K → "germany" → enter → land on `/countries/DEU` in 1.2 seconds. That's the friction floor we need to beat Bloomberg's classic 4-letter mnemonic ("DE <Country> GO").

## Command catalog (v0.1)

| Group | Commands | Shortcut |
|---|---|---|
| Page | Pulse (g h), Countries (g c), Indicators (g i), Scenarios (g s), Forecasts (g f), Leaderboard (g l), Methodology (g m), Accountability (g a), Events (g e), Vintage (v) | letter-pair |
| Country | USA, CHN, JPN, DEU, GBR, FRA, IND, BRA (+ extensible) | — |
| Indicator | GDP YoY, CPI YoY, Unemployment, Policy rate, GPR, GSCPI | — |
| Scenario | All triggered scenarios by slug | — |

Production catalog expands to: all Tier-V countries (22), all indicators (~40), all scenarios (10+ packs, dynamic), Tier-T fallback for 110 more countries.

## Implementation choices

- **Client component** (`"use client"`) — keyboard event handlers + state.
- **No external lib** for the prototype. The production version may swap to `cmdk` (already in package.json) for fuzzy match + virtualized rows.
- **Esc closes**. ⌘K toggles. Click outside closes.
- **Grouped by category**, not sorted into one flat list — the cognitive load of "what kind of thing am I jumping to" matters.
- **Shortcut hints inline** (right-aligned `<kbd>` pill).

## What's pending

- Fuzzy match (currently substring); swap to `cmdk` library.
- Recent-jumps history (last 5).
- Bound keys: `?` → keyboard cheatsheet overlay.
- "Forecast NNN" syntax: `forecast usa gdp 4q` jumps directly to a vintage-scoped forecast view.
- Search-by-vintage: `v 2024-09-01` → vintage rewinder.

## What comes next

- L244 — Compare-2 view (companion: ⌘K → "compare USA DEU" → diff).
- L242 — Watchlist persistence (companion: starring from the palette adds to watchlist).
- L173 — Vintage time machine (companion: ⌘K → "v 2024-09-01" → rewind).

## Related

- [[L128-universal-search-command-bar]] — the design spec for this component
- [[L152-keyboard-shortcuts]] — the full keyboard catalog
- [[L153-command-palette-catalog]] — every command, with synonyms
- [[L231-nextjs-scaffold]] — mounted in `app/layout.tsx`
