# L231 — Next.js + Tailwind dashboard scaffold

**Loop**: 231 / 300
**Phase**: 5 — Code prototypes
**Date**: 2026-06-06
**Artifact**: `prototypes/dashboard-next/`

---

## What was built

A working Next.js 15 + Tailwind v4 + shadcn-style dashboard scaffold under `prototypes/dashboard-next/`, terminal-aesthetic, dark by default, ready to `npm install && npm run dev`.

## Stack picked

| Layer | Pick | Why |
|---|---|---|
| Framework | Next.js 15 (App Router, RSC) | Best-in-class server components, file routing, ecosystem, SEO control. SSG + ISR for vintaged pages. |
| Styling | Tailwind v4 | New engine (Lightning), faster, native CSS. Component primitives via shadcn vendor. |
| Components | shadcn/ui patterns (Radix primitives) | Vendor not dependency — full ownership; matches our terminal-square aesthetic when tuned. |
| Charts | TradingView Lightweight Charts (canvas) | Sub-50KB, terminal-feel, fast pan/zoom. Plotly resampler reserved for explainer pages. |
| Tables | TanStack Table | Lightweight, headless, virtualized. AG-Grid skipped (license/weight). |
| Type validation | Zod | Mirror Python pydantic schemas at the network boundary. |
| Numerals | JetBrains Mono with `tabular-nums` | Tight columns; Bloomberg-feel. |

## Files written

```
prototypes/dashboard-next/
├── package.json                      # deps + scripts
├── tsconfig.json                     # @/* aliases
├── next.config.mjs                   # external pkg whitelist for charts
├── tailwind.config.ts                # terminal palette + Mono numerals
├── postcss.config.mjs
├── README.md                         # full inventory + decisions
├── app/
│   ├── globals.css                   # @tailwind + tile components
│   ├── layout.tsx                    # root layout + TopNav + Footer + CommandPalette
│   ├── page.tsx                      # World Pulse home
│   ├── countries/[iso3]/page.tsx
│   ├── indicators/[id]/page.tsx
│   ├── scenarios/page.tsx
│   ├── scenarios/[slug]/page.tsx
│   ├── forecasts/page.tsx
│   ├── leaderboard/page.tsx
│   ├── methodology/page.tsx
│   ├── accountability/page.tsx       # THE distinctive page — open miss ledger
│   ├── events/page.tsx
│   └── embed/page.tsx
├── components/
│   ├── CommandPalette.tsx            # ⌘K + grouped routing
│   ├── layout/TopNav.tsx
│   ├── layout/Footer.tsx
│   └── tiles/
│       ├── Sparkline.tsx             # pure-SVG, no JS dep
│       ├── IndicatorTile.tsx
│       └── CountryCard.tsx
├── lib/
│   ├── api.ts                        # typed fetch + COUNTRY_NAMES + INDICATORS
│   └── utils.ts                      # cn, fmt, isoToFlag, deltaSign
├── types/forecast.ts                 # Zod schemas for Forecast, Scenario, SituationTile
├── data/
│   ├── fixtures.situation.json
│   ├── fixtures.scenarios.json
│   └── fixtures.forecasts.json
└── public/embed.js                   # drop-in embed SDK (zero-dep)
```

## Design decisions baked in

1. **Terminal palette**: amber on near-black. JetBrains Mono for all numerics. Square 2-px corners (not rounded-2xl modern default).
2. **Information density**: 13-14px base font, tabular-nums, sparkline-on-every-tile.
3. **Consensus overlay default**: every forecast row shows WEO + OECD EO + delta — comparison-against-cartel is the default view.
4. **Badges per forecast**: `ensemble-of-N`, `replicated`, `high-coverage`, `experimental` — instant trust signal.
5. **Provenance reminder on every page**: a footer band reminds users every number is vintage-stamped.
6. **Tier-V country focus on home**: 22 vintage-correct economies; Tier-T (tracked-only) is on indicator pages but de-emphasized.
7. **`/accountability` is in the top nav**. Most dashboards hide misses. We surface them. That single editorial choice IS the product differentiation.

## What's pending in the scaffold

- Forecast detail page with Lightweight Charts bands
- Vintage rewinder (URL `/vintage/2024-09-01/...`)
- Globe map for geopolitical pulse (globe.gl integration)
- MCP server install page
- Pricing page
- Track-record page with calibration plot
- Tests (Vitest unit + Playwright e2e)

## Sister artifacts

- `prototypes/api-stub/main.py` — minimal FastAPI stub the dashboard talks to (loops L232-ish)

## What comes next

- L232 — Country page detail (already partially built)
- L233 — Indicator page detail (already partially built)
- L235 — Forecast detail page with Lightweight Charts bands
- L237 — Globe pulse prototype

## Related

- [[L121-information-architecture]] — top nav structure
- [[L122-home-screen-layout]] — World Pulse layout
- [[L181-forecast-object-schema]] — the typed schema mirrored in `types/forecast.ts`
- [[L011-openbb-terminal]] — the closed-incumbent baseline
- [[L073-nextjs-tailwind-starters]] — the stack candidates surveyed
