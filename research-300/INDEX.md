# research-300 — Index

The 300-loop world-dashboard research + product design effort for OPENGEM. Started 2026-06-06.

## Directory map

```
research-300/
├── INDEX.md                                — this file
├── QUEUE.md                                — the 300-loop tracker (autonomously updated)
├── loops/                                  — one markdown artifact per loop (or batch)
├── synthesis/                              — cross-cutting digests
│   └── MIDPOINT-FINDINGS.md                — the three pivotal cost-collapses (read first)
├── clones/                                 — open-source repos cloned for inspection
└── prototypes/                             — working code prototypes
    ├── dashboard-next/                     — Next.js + Tailwind + shadcn dashboard
    └── api-stub/                           — FastAPI service stub the dashboard talks to
```

## Read order — for a cold reader (i.e. Edgardo later, or a collaborator)

### 30-minute read

1. `loops/L001-vision-statement.md` — the one-sentence and twelve-word pitches; the three-cohort thesis.
2. `synthesis/MIDPOINT-FINDINGS.md` — the three pivotal cost-collapses discovered mid-run.
3. `prototypes/dashboard-next/README.md` — the implemented scaffold inventory.
4. `prototypes/dashboard-next/app/accountability/page.tsx` — *the* page that doesn't exist anywhere else.

### 90-minute read

5. `loops/L002-competitive-landscape.md` — the 12 incumbents and the empty quadrant
6. `loops/L008-differentiation.md` — the 5 promises no incumbent can credibly make
7. `loops/L010-five-year-arc.md` — the Y0→Y5 trajectory
8. `loops/L271-master-prd.md` — the canonical v1 PRD
9. `loops/L300-final-synthesis.md` — (when Phase 6 completes) the closing synthesis

### Domain-specific reads

| If you want to | Read |
|---|---|
| Survey open-source forecasting infrastructure | `loops/L031-L045-*.md` (15 deep dives) |
| Survey open-source geopolitical data | `loops/L021-L030-*.md` (10 deep dives, GREEN/YELLOW/RED triage) |
| Survey open data sources | `loops/L046-L060-*.md` (15 deep dives, with rate-limit math + endpoint traps) |
| Survey viz toolkits + dashboards | `loops/L061-L080-*.md` (20 deep dives) |
| See dashboard page-level design | `loops/L121-L145-*.md` (25 design decisions) |
| See design-system specs | `loops/L146-L180-*.md` (35 design specs) |
| See forecasting product mechanics | `loops/L181-L210-*.md` (30 mechanism specs) |
| See thematic page designs | `loops/L211-L230-*.md` (20 thematic pages, e.g. trade matrix, sovereign debt, SSP scenarios) |
| See Phase 2 integration deep-dives | `loops/L081-L120-*.md` (40 code-and-integration decisions) |
| See launch + governance | `loops/L271-L300-*.md` (30 synthesis + launch artifacts) |

## Pivotal findings (from `synthesis/MIDPOINT-FINDINGS.md`)

1. **Datasette is the moat, not just a tech pick.** $5/mo Fly.io. Bloomberg structurally cannot match.
2. **statsmodels DynamicFactorMQ IS the L3 backbone.** BSD-3, by Chad Fulton (NY Fed staff economist). `pip install statsmodels` collapses Block I's biggest design risk.
3. **POLECAT replaces ACLED for 95% of value.** CC0 license. The geopolitical-event substrate becomes 100% republishable.

Combined effect: OPENGEM goes from ~24-month-to-product to ~6-9-month-to-product for a single guerrilla developer.

## Adopted technical picks (consolidated across all surveys)

### Forecasting / data
- **statsmodels.tsa.statespace.DynamicFactorMQ** — L3 backbone
- **Nixtla suite** (statsforecast / neuralforecast) — Apache-2.0 ensemble layer
- **PyMC + numpyro** — Bayesian VAR layer
- **BGVAR (R, via subprocess)** — L2 spillover layer

### Data sources (open)
- **GDELT 2.0 + GKG** (geopolitics, free + attribution) — daily pulse
- **POLECAT** (CC0, Harvard) — ACLED substitute
- **UCDP** (CC-BY-4.0) — conflict substrate
- **World Bank Indicators API** — multi-country fallback
- **IMF SDMX 3.0** (NOTE: 3.0 endpoint; 2.1 retired)
- **ECB Data Portal** (CC0, `data-api.ecb.europa.eu`)
- **BIS Statistics warehouse** (LBS, CBS, EER, CREDIT_GAPS, TC)
- **OECD ORDRA + EO archives** (`sdmx.oecd.org`)

### Frontend
- **Next.js 15** (App Router, RSC)
- **Tailwind v4** + **shadcn/ui** + **Tremor** (KPI cards)
- **TradingView Lightweight Charts** (Apache-2.0, 45KB) — forecast bands chart
- **FINOS Perspective** — indicator grid + leaderboard streaming
- **TanStack Table** — Pro grids
- **globe.gl** — 3D geopolitical pulse
- **Kepler.gl** — flat supply-chain map
- **Observable Plot** — line/area/sparkline/heatmap workhorse
- **Observable Framework** — long-tail SEO substrate

### Data publishing / SEO
- **Datasette** ($5/mo Fly.io) — the strategic moat surface at `data.opengem.org`
- **DuckDB-WASM** — client-side SQL queries
- **Parquet-on-R2** — cold vintage tier

### Backend
- **FastAPI** (Python) — public REST API
- **Dagster** (already in repo) — orchestration
- **TimescaleDB** through Y1, **Iceberg** at 500GB+ in Y2-Y3
- **Stripe Checkout** — Pro tier
- **Resend** — magic-link auth + transactional email

### Distribution
- **MCP server** (`@opengem/mcp-server`) — the monetization lever
- **RSS/Atom feeds** — per page, per scenario, per country, miss-feed
- **Embed SDK** (`embed.js`, ~3KB) — drop-in tile/chart embeds
- **JSON-LD + schema.org** — every page machine-discoverable
- **Plausible** (self-hosted) — privacy-respecting analytics

### Deploy
- **Cloudflare Pages** — Next.js dashboard
- **Cloudflare R2** — static assets + cold vintage tier
- **Fly.io** — Python FastAPI + Datasette + Plausible

Total v1 hosting: ~$25/mo. Y1 with 10k DAU: ~$120/mo.

## Documents not in this directory

- `/mnt/bigdata/home/edgardo/projectsd/opengem/docs/research/` — the original 28+ pre-PDR research memos
- `/mnt/bigdata/home/edgardo/projectsd/opengem/docs/design/` — the 27-document loop-plan (LOOP_PLAN-v2.md is the master)
- `/mnt/bigdata/home/edgardo/projectsd/opengem/MORNING-BRIEFING.md` — the program-owner morning brief

## How to use this work

1. **For Edgardo (alone)**: read INDEX.md → synthesis/MIDPOINT-FINDINGS.md → loops/L300-final-synthesis.md (when ready). Make Y0 plan from the three findings.
2. **For collaborators**: same path + `loops/L271-master-prd.md` to align on v1 scope.
3. **For implementers**: `prototypes/dashboard-next/` is the running scaffold; `npm install && npm run dev` after wiring up `OPENGEM_API_URL`.
