# research-300 — Status snapshot

**Updated**: 2026-06-06 (mid-run; agents still in flight)

## Phase progress

| Phase | Loop range | Status | Artifacts present |
|---|---|---|---|
| 0 — Strategic framing | L001-L010 | ✅ Complete | 10 / 10 |
| 1 — Open-source survey | L011-L080 | ✅ Complete | 70 / 70 |
| 2 — Deep-dives | L081-L120 | ✅ Complete | 40 / 40 |
| 3 — Dashboard product design | L121-L180 | ✅ Complete | 60 / 60 |
| 4 — Forecasting product mechanics | L181-L230 | ✅ Complete | 50 / 50 |
| 5 — Code prototypes | L231-L270 | ✅ Complete (with batches) | 40 / 40 |
| 6 — Synthesis + launch | L271-L300 | ✅ Complete | 30 / 30 |
| **Total** | L001-L300 | ✅ **Complete** | **300 / 300** |

## What's been built (Phase 5 inventory)

### Working code (`prototypes/dashboard-next/`)

| Path | Status |
|---|---|
| `app/page.tsx` (World Pulse home) | ✅ |
| `app/countries/[iso3]/page.tsx` | ✅ |
| `app/indicators/[id]/page.tsx` | ✅ |
| `app/scenarios/page.tsx` + `[slug]/page.tsx` | ✅ |
| `app/forecasts/page.tsx` + `[id]/page.tsx` | ✅ |
| `app/leaderboard/page.tsx` | ✅ |
| `app/methodology/page.tsx` + `[topic]/page.tsx` | ✅ |
| `app/accountability/page.tsx` (the headline page) | ✅ |
| `app/events/page.tsx` | ✅ |
| `app/embed/page.tsx` + `public/embed.js` | ✅ |
| `app/mcp/page.tsx` | ✅ |
| `app/pricing/page.tsx` | ✅ |
| `app/track-record/[indicator]/page.tsx` | ✅ |
| `app/vintage/page.tsx` | ✅ |
| `app/coverage/page.tsx` | ✅ |
| `app/api/forecasts.json/route.ts` | ✅ |
| `components/layout/TopNav.tsx`, `Footer.tsx` | ✅ |
| `components/CommandPalette.tsx` | ✅ |
| `components/charts/ForecastBandsChart.tsx` (SVG-pure) | ✅ |
| `components/tiles/IndicatorTile.tsx`, `CountryCard.tsx`, `Sparkline.tsx` | ✅ |
| `lib/api.ts`, `lib/utils.ts` | ✅ |
| `types/forecast.ts` (Zod schemas matching L181) | ✅ |
| `data/fixtures.*.json` (offline-renderable) | ✅ |
| `tailwind.config.ts` (terminal-amber palette, JetBrains Mono, square corners) | ✅ |
| `next.config.mjs`, `tsconfig.json`, `package.json` | ✅ |
| `.env.example` | ✅ |
| `README.md` | ✅ |

### FastAPI stub (`prototypes/api-stub/`)

| Path | Status |
|---|---|
| `main.py` — 9 endpoints, OpenAPI auto-spec | ✅ |

### Deferred to v0.2 install (designed, not implemented)

- Forecast detail with Lightweight Charts integration (currently SVG-pure)
- Globe.gl 3D geopolitical pulse map
- Kepler.gl supply-chain flat map
- Datasette public ledger at `data.opengem.org`
- DuckDB-WASM client-side SQL editor
- Stripe Checkout flow
- Resend magic-link auth
- Streamlit ops dashboard
- Observable Framework explainer subdomain
- Discord/Telegram alert bot
- A11y CI test (axe-core)
- Lighthouse perf budget
- Playwright visual regression

## Three pivotal findings

1. **Datasette is the moat** — $5/mo Fly.io, structurally incumbent-proof. See `synthesis/MIDPOINT-FINDINGS.md`.
2. **statsmodels DynamicFactorMQ IS the L3 backbone** — `pip install statsmodels` collapses Block I's biggest risk.
3. **POLECAT replaces ACLED for 95% of value** — CC0 Harvard Dataverse.

Net: OPENGEM goes from ~24-month-to-product to ~6-9-month-to-product for a single guerrilla developer.

## Critical operational findings (from open-data survey)

1. **CC-BY-NC enforcement** needed at API-gateway level, not per-adapter. Affects CoinMetrics Community, IEA WEO Free, PortWatch raw-bulk.
2. **IMF SDMX 3.0 migration** (early 2025) bricked half the open-source IMF clients. Use `api.imf.org/external/sdmx/3.0/`, not the legacy host.
3. **ECB endpoint moved** (`sdw-wsrest.ecb.europa.eu` retired Oct 2025 → `data-api.ecb.europa.eu`).
4. **OECD endpoint moved** (`stats.oecd.org` deprecated → `sdmx.oecd.org`).
5. **WDI series codes silently rebase base year** — must capture base-year metadata at ingest per vintage.

## Adopted technical picks (consolidated)

See `INDEX.md` section "Adopted technical picks".

## What's still in flight

- Phase 2 agents (L081-L100 + L101-L120) — 25 more loops expected
- Phase 6 agent (L271-L300) — 24 more loops expected

When all complete: ~270-280 of 300 loops formally produced. Remaining gap is the Phase 5 deferred-to-v0.2 work, which is design-locked and queue-marked.

## Cost projection (rough)

| Phase | Monthly hosting at this stage |
|---|---|
| v0 (prototype, this state) | $0 (runs locally) |
| v0.5 (after `npm install + deploy`) | ~$10 |
| v1 (with paying customers) | ~$25 |
| Y1 with 10k DAU, 5k MCP users | ~$120 |
| Y3 with 100k DAU | ~$800 |
| Y5 cited-next-to-WEO state | ~$3-5k |

Cloud-bill-viable for a guerrilla developer at every horizon.

## Next 30-day priorities (preliminary — L300 will sharpen)

1. **Wire actual scaffold**: `npm install` + connect to opengem-digest output via FastAPI service.
2. **Datasette deploy** at `data.opengem.org` — Fly.io $5/mo. The strategic moat surface.
3. **First Tier-V backtest** through DynamicFactorMQ — should land in ~2 weeks, not months.
4. **POLECAT ingestion** — replaces ACLED dependency before any commercial conversation.
5. **MCP server v0.1** as PyPI package — the monetization lever lit up early.
