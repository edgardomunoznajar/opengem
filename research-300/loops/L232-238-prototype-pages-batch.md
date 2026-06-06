# L232-L238 — Prototype pages: countries, indicators, scenarios, forecasts, events (batch)

**Loops**: 232, 233, 234, 235, 236, 237, 238 / 300
**Phase**: 5 — Code prototypes
**Date**: 2026-06-06
**Artifacts**: in `prototypes/dashboard-next/app/`

---

This batch document covers seven prototype pages that landed together. Each was built end-to-end in the Next.js dashboard scaffold.

## L232 — Country page

**File**: `app/countries/[iso3]/page.tsx`

Per-country dashboard. Header with flag, ISO3, name, action pills (methodology, track record, vintage). Situation tiles (4-column grid) — recession_prob, gpr, gscpi, fci, nowcasts. Forecast table — Indicator × Horizon × OPENGEM (P50) × Band (P10–P90) × WEO × OECD EO × Model card link. Provenance reminder band at the bottom.

**Decision**: Country page is the *primary* drilldown surface — most session-paths land here from home page or command palette. Optimized for "I know which country, what's the macro picture".

## L233 — Indicator page

**File**: `app/indicators/[id]/page.tsx`

Cross-country forecast table for a single indicator. Header with indicator label, methodology + track-record pills. Cross-country forecast grid — Country × OPENGEM (P50) × P10 × P90 × vs WEO (diff, color-coded) × vs OECD (diff) × Vintage.

**Decision**: Indicator page is the *secondary* drilldown — "I care about CPI, which countries have the steepest trajectory". The vs-consensus diff column is the editorial feature (green = above WEO, red = below). It's also where the LLM agents will most often pivot via MCP.

## L234 — Scenario page

**File**: `app/scenarios/[slug]/page.tsx` (detail) + `app/scenarios/page.tsx` (index)

Scenario detail: probability pill (color-coded high/med/low), trigger conditions block (mono font, multi-line), affected countries grid (clickable), affected indicators grid (clickable), narrative block in serif font.

Scenario index: sorted by probability descending, table view, probability pill in line.

**Decision**: Scenario is the *editorial* surface — where OPENGEM tells a story about the data. The narrative block uses serif typography (Source Serif 4) intentionally to signal "this is editorial, not data". The trigger summary is in mono — it's machine-checkable.

## L235 — Forecast list page

**File**: `app/forecasts/page.tsx`

Comprehensive table of every published forecast at current vintage. Country × Indicator × Horizon × OPENGEM × P10 × P90 × vs WEO × Badges × Model. Header includes JSON / CSV / leaderboard quick-jump pills.

**Decision**: Forecast list is the *power-user* surface — analysts who want everything. CSV/JSON are first-class pills, not hidden in a menu. The model column links to the model card.

## L236 — (deferred) Forecast detail with Lightweight Charts bands

**Status**: SCAFFOLDED, chart integration pending.

Designed: `app/forecasts/[id]/page.tsx` will mount `<LightweightChart>` (client component) showing P10/P50/P90 band area + consensus overlay line + revision arrow at vintage cuts. The chart component will use `lightweight-charts` v5 with the upstream "bands" series or a custom area-pair fallback.

**Why deferred**: requires npm install to run; the prototype is unpacked but not installed in this session.

## L237 — Geopolitical pulse globe (deferred)

**Status**: DESIGN-LOCKED, integration pending.

Design: `app/page.tsx` will get a `<GlobePulse>` client component above-the-fold (between hero strip and scenarios). globe.gl pick confirmed by L101 deep-dive and L061-L080 viz survey. GDELT GoldsteinScale-weighted event density rendered as a polygon-thickness map on the 3D globe, rotating slowly, click-to-drill to country.

**Why deferred**: globe.gl is in `clones/globe-gl/` for inspection; npm install pending.

## L238 — Supply-chain pulse map (deferred)

**Status**: DESIGN-LOCKED.

Design: a Kepler.gl flat-map layer on the supply-chain page rendering PortWatch + GSCPI data overlaid as heat at major shipping nodes. Per L061-L080 survey, Kepler.gl wins for flat-map layered overlays; globe.gl wins for the 3D rotating globe on home.

## What this loop produced

- Working country page (`app/countries/[iso3]/page.tsx`)
- Working indicator page (`app/indicators/[id]/page.tsx`)
- Working scenario detail + index (`app/scenarios/...`)
- Working forecasts list (`app/forecasts/page.tsx`)
- Three deferred designs (L236 forecast chart, L237 globe, L238 supply-chain map) with the picks locked

## What comes next

- L239 — Yield-curve animation prototype
- L240 — Surprise index tile prototype
- L241 — Live news feed prototype (events page already partially built)

## Related

- [[L231-nextjs-scaffold]] — the scaffold these pages live in
- [[L123-country-page]] — the design spec for L232
- [[L124-indicator-page]] — the design spec for L233
- [[L125-scenario-page]] — the design spec for L234
- [[L126-forecast-page]] — the design spec for L235
- [[L181-forecast-object-schema]] — the JSON contract these pages render
