# Next 30 days — actions for OPENGEM

**Source**: synthesized from research-300 findings through 2026-06-06. Will be superseded by L300 final synthesis when Phase 6 completes.

This is the actionable layer. Three findings have collapsed cost; this is how to spend the time freed up.

---

## Week 1 — Foundation (the three cost-collapses, instantiated)

### 1. Datasette mount at `data.opengem.org`

**What**: Fly.io machine ($5/mo) running Datasette pointed at a per-vintage SQLite snapshot of opengem-vintage's output.

**Why**: This IS the moat. Every other thing OPENGEM does becomes a public, queryable, vintage-stamped, SQL-able artifact. Bloomberg and Macrobond cannot match.

**How**:
```bash
# In opengem repo
poetry add datasette
# Add a Dagster asset: "publish_vintage_snapshot" that writes opengem.db
# Deploy: flyctl launch --image datasetteproject/datasette
# Mount opengem.db via volume; refresh on cron
```

**Done when**: `https://data.opengem.org` is live, queryable, with a vintage selector.

### 2. statsmodels DynamicFactorMQ → Tier-V backtest

**What**: Wire `statsmodels.tsa.statespace.DynamicFactorMQ` into a new `opengem-l3-dfm` package, fit on the 22 Tier-V countries.

**Why**: Block I's biggest design risk collapses to a 2-week fit. Chad Fulton's NY Fed implementation is BSD-3, drop-in compatible.

**How**:
```bash
mkdir packages/opengem-l3-dfm && cd packages/opengem-l3-dfm
poetry init  # depends on opengem-vintage, opengem-types, statsmodels>=0.14
# src/opengem_l3_dfm/fit.py — load Tier-V vintage data → fit DynamicFactorMQ → save forecast vintage
# tests/ — fit on US-only first, expand
```

**Done when**: a single `opengem-l3-dfm fit USA --indicator gdp_yoy --horizon 4Q` produces a `Forecast` object with valid p10/p50/p90 bands; backtest CRPS ≤ AR(1) on US.

### 3. POLECAT ingestion → replace GPR dependency

**What**: New `opengem-data-polecat` adapter pulling CC0 weekly events from Harvard Dataverse.

**Why**: Eliminates the only YELLOW-licensed event-data dependency (ACLED). Future-proofs the open-substrate promise.

**How**:
- Harvard Dataverse API → weekly POLECAT zip → PLOVER-coded events → opengem-vintage store
- Build a Goldstein-Scale-weighted aggregation per country
- Validate against the existing opengem-data-gpr R² ≥ 0.92 over 1985-2024

**Done when**: `opengem-data-polecat` ships with tests passing; the GPR composite uses POLECAT as a source.

## Week 2 — Public surface

### 4. `npm install` + deploy the Next.js scaffold to Cloudflare Pages

**What**: Take the research-300/prototypes/dashboard-next/ scaffold to production.

**How**:
```bash
cp -R research-300/prototypes/dashboard-next packages/opengem-dashboard
cd packages/opengem-dashboard
npm install
# Wire OPENGEM_API_URL to a Fly.io FastAPI deploy
# Push to Cloudflare Pages via git push
```

**Done when**: `https://opengem.org` shows the World Pulse with real (not fixture) data.

### 5. FastAPI service deploy on Fly.io

**What**: Take research-300/prototypes/api-stub/main.py and wire it to opengem-vintage + opengem-digest + opengem-recession-prob.

**Done when**: `https://api.opengem.org/v1/health` returns OK; `/v1/forecasts?country=USA&indicator=gdp_yoy` returns a real forecast.

### 6. MCP server v0.1 → PyPI

**What**: Build `packages/opengem-mcp/` with the 8 tools from L250.

**Why**: The monetization lever. Get it live before any paid-tier conversation.

**Done when**: `pip install opengem-mcp && opengem-mcp serve` works; a Claude Desktop user can `npx -y @opengem/mcp-server` and use `get_forecast`.

## Week 3 — Editorial discipline

### 7. Open the accountability ledger publicly

**What**: At `https://opengem.org/accountability`, publish the actual miss-log from the existing opengem-vintage backtests.

**Why**: The single most differentiated page in the world. Most dashboards hide misses; this one is the home page.

**Done when**: 3+ documented misses are live with post-mortems linked.

### 8. First daily digest cron + RSS feed

**What**: opengem-digest writes a markdown + JSON digest every morning; the dashboard's `/events` page reads it; an RSS feed at `/feeds/digest-daily.rss` syndicates it.

**Done when**: a YouTuber friend (per the OPENGEM thesis) can subscribe to the RSS in their feed reader and have it land in their morning workflow.

### 9. Write the first miss post-mortem

**What**: Find one historical forecast in opengem-vintage that missed. Write the post-mortem using the L298 template. Publish at `/postmortem/<country>-<indicator>-<vintage>`.

**Why**: The publication discipline only exists as words until there's at least one actual miss post-mortem to point at.

**Done when**: 1 post-mortem is live, linked from /accountability.

## Week 4 — Distribution lit

### 10. Embed SDK published at `https://opengem.org/embed/v1.js`

**What**: Take research-300/prototypes/dashboard-next/public/embed.js, publish at versioned URL, write the docs page.

**Done when**: 2-3 cooperative bloggers / Substack-ers have an OPENGEM tile on their site.

### 11. Submit to ProductHunt + HN + r/datasets

**What**: Per L277 launch plan. Coordinate with one cooperative academic + one cooperative journalist for pre-launch quotes.

**Done when**: Launch day complete; ≥1 piece of incoming press; ≥100 unique visitors.

### 12. Open the GitHub repo's `RFC-001: World Dashboard v1` issue

**What**: Externalize the research-300 work into a structured GitHub Discussion / RFC that solicits public input from the macro-open-source community.

**Done when**: RFC is published; ≥3 external comments; the comments inform the v1.1 roadmap.

---

## The pivotal sequencing rule

These twelve actions cluster three ways:

| Cluster | Effort | Returns |
|---|---|---|
| Substrate (1, 2, 3) | 2 weeks | Cost-collapse: ~50% of the technical risk gone |
| Public surface (4, 5, 6) | 2 weeks | First-product: someone external can use it |
| Discipline (7, 8, 9) | 1 week | Differentiation: the headline page is real |
| Distribution (10, 11, 12) | 1 week | Distribution: the world finds out |

The rule is: **substrate before surface, surface before discipline, discipline before distribution**. Inverting kills the project.

## What NOT to do in the next 30 days

- Don't onboard a co-founder. The cost-collapses make this feasible solo. Co-founders are for hard problems; this is now ~execution.
- Don't take VC. The financial model in L260 / L275 says solo at $25-120/mo hosting works.
- Don't build a custom DFM. Use statsmodels. Period.
- Don't license ACLED. POLECAT solves it. POLECAT first.
- Don't migrate off TimescaleDB. Through Y1 it's fine.
- Don't build a Streamlit dashboard for the public. Next.js. The decision is locked.
- Don't index ICEWS. It's discontinued.
- Don't try to chase intraday market data. Wrong cadence; will erode the differentiation.

## How L300 will sharpen this

When the Phase 6 agent completes L300, that synthesis will:
- Cross-check this 30-day list against the formal V&V matrix
- Add quarterly milestones (Q3 2026, Q4 2026, Q1 2027)
- Confirm or revise the "no co-founder, no VC" stance
- Tighten the success criteria for each cluster

Until then, this is the working plan.
