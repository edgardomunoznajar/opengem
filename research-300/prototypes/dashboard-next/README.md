# OPENGEM World Dashboard — Prototype

Next.js 15 + Tailwind v4 + shadcn-style components + Lightweight Charts.

**Status**: scaffolded under research-300/prototypes/dashboard-next as part of the 300-loop product-design effort. Not yet `npm install`-ed in this repo. The scaffold is the architectural spec; running it requires:

```bash
cd research-300/prototypes/dashboard-next
npm install
npm run dev
```

## What's here

| Path | Purpose |
|---|---|
| `app/page.tsx` | Home — World Pulse hero strip + scenarios + forecast strip + Tier-V country grid |
| `app/countries/[iso3]/page.tsx` | Per-country page — situation tiles + forecast table |
| `app/scenarios/page.tsx` | Scenarios index — ranked by probability |
| `app/scenarios/[slug]/page.tsx` | Scenario detail — trigger, affected countries, narrative |
| `app/indicators/[id]/page.tsx` | Cross-country forecast table for a single indicator |
| `app/leaderboard/page.tsx` | Forecast leaderboard — OPENGEM vs WEO vs OECD EO vs RW/AR(1) baseline |
| `components/layout/TopNav.tsx` | Top nav — Pulse · Countries · Indicators · Scenarios · Forecasts · Leaderboard · Methodology |
| `components/tiles/IndicatorTile.tsx` | Bloomberg-style indicator tile with sparkline + delta + as-of |
| `components/tiles/CountryCard.tsx` | Country card with flag, recession-prob pill, 3-metric grid |
| `components/tiles/Sparkline.tsx` | Pure-SVG sparkline (no JS dep) |
| `lib/api.ts` | Typed client — points at OPENGEM FastAPI, falls back to bundled fixtures |
| `lib/utils.ts` | `cn`, `fmt`, `isoToFlag`, `deltaSign` |
| `types/forecast.ts` | Zod schemas for Forecast, Scenario, SituationTile — match L181 spec |
| `data/fixtures.*.json` | Offline-renderable fixtures |
| `tailwind.config.ts` | Terminal-amber palette, JetBrains Mono numerals, square borders |

## Design decisions baked in

- **Dark by default.** Terminal palette: amber on near-black. Light theme planned.
- **Information density first.** 13–14px base, tight line-heights, `tabular-nums` for all numerics.
- **Square corners.** Bloomberg-style 2-px radii, not the rounded-2xl modern default.
- **Sparkline + delta + as-of on every tile.** Always know what you're looking at and when.
- **Provenance promise visible on every page.** A footer band reminds users every number is vintage-stamped.
- **Tier-V country focus on home.** 22 vintage-correct economies; Tier-T (tracked-only) is on indicator pages but de-emphasized.
- **Consensus overlay everywhere.** OPENGEM number is always shown next to WEO + OECD EO so the reader can compare.
- **Badges per forecast.** `ensemble-of-N`, `replicated`, `high-coverage`, `experimental` — instant trust signal.

## What's still scaffolded (TODO)

- Forecast detail page with bands chart (Lightweight Charts integration)
- Vintage rewinder (URL `/vintage/2024-09-01/...`)
- Command palette (cmdk)
- Globe map for geopolitical pulse (globe.gl integration)
- Accountability ledger page
- MCP server install page
- Pricing page
- Embed widget JS contract
- Track-record page with calibration plot

## How this connects to the rest of OPENGEM

The dashboard is a thin presentation layer on top of:

1. **opengem-vintage** — vintage-correct store (TimescaleDB + SQLite + in-memory).
2. **opengem-recession-prob** — Bauer-Mertens term-spread probit.
3. **opengem-event-detector** — market + news event detectors.
4. **opengem-scenarios** — canonical pack library + invocations.
5. **opengem-digest** — daily JSON + markdown digest (which the dashboard reads).
6. **opengem-narrative** — ChatGPT system prompts (which the scenario page surfaces).

The FastAPI service that this dashboard talks to lives elsewhere in the repo
(currently scoped as part of the architecture but not yet implemented as a
single Python service — see `docs/design/20-interfaces/OG1-ICD-002` for the spec).

## License

Apache-2.0 (matching the rest of OPENGEM).
