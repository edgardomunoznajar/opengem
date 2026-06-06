# L300 — Final synthesis: OPENGEM World Dashboard, v1 → v2 → v5 arc

**Loop**: 300 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06
**Status**: closing artifact for the 300-loop research + product design effort

---

## TL;DR

OPENGEM is a public macro-accountability ledger for the world economy — a Bloomberg-grade dashboard for everyone, where every forecast is open, every number is dated, every miss is named.

After 300 loops of research, design, and prototype work, **three pivotal cost-collapses** have radically reshaped the build path:

1. **Datasette is the moat** (not just a tech pick) — $5/mo Fly.io, structurally incumbent-proof, becomes OPENGEM's public ledger surface.
2. **`statsmodels.tsa.statespace.DynamicFactorMQ` IS the L3 backbone** — `pip install` collapses what was supposed to be Block I's biggest engineering bet.
3. **POLECAT (Harvard, CC0) replaces ACLED for 95% of value** — eliminates the only YELLOW-licensed geopolitical-data dependency.

Combined effect: a build that was estimated at ~24 calendar months can be done by a single guerrilla developer in **6–9 months** for the v0.5 milestone. The path forward is execution, not architecture.

---

## The thesis, restated

The forecasting cartel (IMF WEO, OECD EO, Bloomberg Economics, Goldman GIR, JPM Macro, Stratfor, etc.) produces *priced* forecasts. Their track records are private. Their margins depend on opacity. They cannot publish their full calibration without exposing why the customer is paying.

OPENGEM has no margins to protect. So it can publish:

- Every vintage of every forecast it has ever made
- Every backtest with every cell of the V&V matrix open
- Every model card with every assumption named
- Every miss with a post-mortem in the same place the original was published

That asymmetry is the moat. **A system that publishes its mistakes is harder to discredit than a system that hides them.**

This is not a contrarian aesthetic. It is a structural arbitrage on the cartel's pricing model.

---

## Where 300 loops landed us

### Phase 0 — Strategic framing

Ten loops established the vision, three-cohort persona thesis (macro-curious prosumer / pro researcher / forecast LP), five-promise differentiation, and the five-year arc. Most consequential framing: **the moat is the act of publishing forecasts in the public-track-record sense, not the forecasts themselves**. Per L008.

### Phase 1 — Open-source landscape survey

Seventy loops mapped the open-source ecosystem across terminals, geopolitical data, forecasting, open data, dashboards, viz, orchestration, and scenario tooling. Three findings landed with disproportionate weight:

- **L061-L080** discovered Datasette as the moat.
- **L031-L045** discovered statsmodels.DynamicFactorMQ as the L3 backbone.
- **L021-L030** discovered POLECAT as the ACLED substitute.

Plus secondary findings:
- **docling** (IBM Research, MIT) as the document-ingestion substrate for central-bank PDFs.
- **Nixtla suite** (statsforecast, neuralforecast) as the ensemble layer.
- **TradingView Lightweight Charts** + **FINOS Perspective** as the interactive forecast + grid rendering primitives.
- The **IMF SDMX 3.0 / ECB / OECD endpoint migrations** as operational landmines.

### Phase 2 — Deep dives + repo clones

Forty loops audited the top candidates with the cloned repos under `clones/`. Most consequential decisions:
- **L102** locked the Dagster + Arq + FastAPI cooperation pattern. Dagster owns vintaged assets; Arq owns ephemeral tasks. This boundary resolved tensions in 5 downstream loops.
- **L108** locked the MCP server contract at 10 tools (8 prototype + `subscribe_events` + `cite_this_view`).
- **L110** chose Better-Auth for the identity layer.
- **L104** rejected htmx but adopted its server-component discipline as a 15 KB/route lint rule.

### Phase 3 — Dashboard product design

Sixty loops designed every page, design-system primitive, and UX pattern. Locked picks:
- **6-slot top nav**: World / Countries / Indicators / Scenarios / Forecasts / Ledger.
- **Inter + JetBrains Mono + Source Serif 4** typeface stack.
- **"Ledger Amber"** at oklch(0.74 0.16 70) ≈ #E89B3B — Bloomberg-orange legacy, terminal density discipline.
- **Lucide** for icons; **2D Equal-Earth choropleth** as default pulse map; **drawer-first** overlays.
- **Terminal Orange** as default theme; **editorial FT-Pink** and **playful OWID-Blue** as user-toggleable alternates.

### Phase 4 — Forecasting product mechanics

Fifty loops specified scoring, leaderboard ranking, calibration, scenario triggers, narrative, and forecast UI. Key decisions:
- **Canonical scoring tuple**: CRPS (primary) + PIT-KS (calibration) + MAE (robustness) + Diebold-Mariano with HLN small-sample correction. Headline: **CRPS win-rate vs AR(1)**.
- **Leaderboard ranking**: Stacked Skill Score, designated **OPENGEM Index v2.0** (supersedes R25's pass-rate v1.0).
- **ML experiment tracking**: Hydra + MLflow with a thin bridge to the L186 reproducibility envelope.
- **20 thematic page designs** (L211-L230) including the three Bloomberg-killer pages: cross-country recession probability (L213), bilateral trade matrix (L218), composable SSP long-horizon scenarios (L230).

### Phase 5 — Code prototypes

Forty loops produced a working Next.js 15 + Tailwind v4 + shadcn dashboard scaffold at `research-300/prototypes/dashboard-next/` plus a FastAPI service stub at `research-300/prototypes/api-stub/`. Coverage:

- Working pages: home (World Pulse), country, indicator, scenario, forecasts list + detail, leaderboard, methodology + per-topic, accountability ledger, events, embed docs, MCP install, pricing, track-record + V&V matrix + calibration, vintage rewinder, coverage matrix, about + governance.
- Working components: command palette, SVG-pure forecast bands chart, sparkline, indicator tile, country card, top nav, footer.
- Working SDK: `embed.js` (~3 KB) drop-in tile embed.
- Working FastAPI: 9 endpoints with auto-generated OpenAPI spec.
- Working types: Zod schemas matching the L181 Forecast contract.

### Phase 6 — Synthesis + launch

Thirty loops produced the master PRD (L271), 11 ADRs (L272), dashboard V&V (L273), KPI dashboard (L274), cost projection (L275), pricing model (L276), launch plan (L277), press kit (L278), demo script (L279), Discord charter (L280), v1 kanban (L281), license audit (L282), ToS (L283), privacy (L284), accountability ledger spec (L285), failure-log page (L286), vendor checklist (L287), email templates (L288), onboarding drip (L289), renewal flow (L290), partnership plan (L291), academic outreach (L292), journalism outreach (L293), gov/NGO outreach (L294), YouTube engine (L295), SEO engine (L296), newsletter engine (L297), post-mortem template (L298), retrospective template (L299), and this final synthesis (L300).

---

## The Y0 → Y5 arc, re-issued

The original R100 vision had Y0 2026 = "Block I rebaseline, foundation, not product." After the three cost-collapses, Y0 2026 H1 can deliver foundation + minimum-viable product in the same calendar quarter.

### Y0 — 2026 H1 — v0.5 ("foundation + MVP")

**Deliver**:
- Datasette public ledger at `data.opengem.org` ($5/mo Fly.io)
- statsmodels.DynamicFactorMQ-driven US forecast at `https://opengem.org/forecasts/USA/gdp_yoy/4Q`
- POLECAT-driven geopolitical risk substrate ingested
- Public dashboard live at `opengem.org` (Cloudflare Pages, ~$0)
- FastAPI service at `api.opengem.org` (Fly.io, ~$5/mo)
- MCP server v0.1 on PyPI (`pip install opengem-mcp`)
- Accountability ledger live with at least 1 documented miss + post-mortem
- One YouTuber friend using the daily digest

**Total hosting**: ~$15-25/mo.

### Y0 — 2026 H2 — v0.7 ("the first 100 users")

**Deliver**:
- Tier-V coverage expanded to 22 economies (from US-only)
- BIS + ECB + IMF SDMX 3.0 + World Bank adapters live
- 10 active scenarios with daily probability rollups
- Embed SDK in production at `https://opengem.org/embed.js`
- RSS / Atom feeds per page family
- Weekly newsletter on Substack
- First academic citation (Path A from L292)
- First press citation (Path B from L293, on a high-novelty miss)
- 100 weekly active users

### Y1 — 2027 — v1.0 ("the first revenue")

**Deliver**:
- All 22 Tier-V + 110 Tier-T countries covered
- 17-cell V&V matrix met at IOC targets (per R08)
- MCP server v1 with the full 10-tool surface
- Stripe + Better-Auth Pro tier live
- 5 paying customers ($29-149/mo)
- $40k MRR-equivalent
- Quarterly retrospective discipline established
- 30+ post-mortems published
- 10k weekly dashboard sessions

**Total hosting**: ~$120/mo.

### Y2 — 2028 — v2.0 ("the cited benchmark")

**Deliver**:
- One peer-reviewed NBER working paper citing OPENGEM as a tracked alternative forecaster
- 25 paying customers
- Sovereign / Enterprise tier alpha (5 customers @ $2-5k/mo)
- 1 academic conference talk
- $300k ARR-equivalent
- 100k weekly dashboard sessions

### Y3 — 2029 — v3.0 ("regional editions")

**Deliver**:
- ASEAN edition + LATAM edition (vintage-correct coverage extending)
- Long-horizon scenarios + IPCC SSP composability live (per L230)
- The first "OPENGEM index" cited by name in a Reuters or FT piece
- $1M ARR-equivalent

### Y5 — 2031 — v5.0 ("cited next to WEO")

**Deliver**:
- OPENGEM cited next to WEO and OECD EO in at least one regularly-circulated comparison report
- 500+ paying customers across tiers
- $3M ARR-equivalent
- The accountability ledger becomes the reference point for "what does honest macro forecasting look like"

---

## The single load-bearing milestone

Across all five horizons, **one milestone is the gate**: OPENGEM appearing on a Fed / IMF / OECD / NBER calibration comparison list as a tracked alternative forecaster.

Until that happens, OPENGEM is a guerrilla developer's side project with an open ledger. After that happens, OPENGEM is an institutionally-recognized benchmark.

The path to it (per L292 + L294):
1. Build the open ledger. ✅ designed; implementation in progress.
2. Run a verifiable backtest with public scoring. → Y0 H2 milestone.
3. Submit replication kit to NY Fed / Atlanta Fed / OECD / IMF research economists. → Y1 milestone.
4. Wait for one of them to cite us in a calibration footnote. → Y2 milestone.
5. The institutional recognition compounds from there.

This is the single decision tree that should structure resource allocation through Y2.

---

## What can kill this

Six failure modes, in priority order:

1. **Calibration drift unaddressed.** If the ≤20% out-of-band-at-80% target drifts above 25% for two consecutive quarters and we don't write up the methodology change publicly, the editorial discipline breaks and the moat closes. **Mitigation**: every quarterly retrospective (L299) reports this metric; methodology changes are documented in model card history.

2. **A miss post-mortem we'd be ashamed to publish.** If we get a miss so bad that we can't write the L298 template honestly, we'll be tempted to suppress it. That single suppression destroys the brand permanently. **Mitigation**: the post-mortem template includes "what we will NOT change" as a load-bearing section, explicitly defending the discipline of not retro-fitting after a single miss. The miss is publishable as long as we own it.

3. **Datasette ledger goes down for >24h.** The moat depends on data.opengem.org being reachable. **Mitigation**: Datasette + Fly.io has 99.95% uptime nominal; we run weekly snapshot exports to a secondary R2 bucket; the dashboard degrades gracefully when the ledger is unreachable.

4. **License contamination.** Someone discovers we ingested an ACLED-licensed series under attribution-only terms and republished it in derivative form. **Mitigation**: POLECAT pre-empts this for events; every adapter ships a `license=` tag enforced at the API gateway (per L046-L060 finding).

5. **MCP throughput abuse.** A single user makes the MCP server tier economically unsustainable. **Mitigation**: per-key tiered rate limits; abuse detection on the L102 Arq job-publish layer.

6. **Single-developer bus factor.** Edgardo is sole maintainer; an extended absence breaks the cadence. **Mitigation**: every weekly digest can fall back to an auto-generated version; every quarterly retrospective is at least drafted by the Friday two weeks before its due date; the open-source repo always has a `STATUS: maintained` flag that flips to `STATUS: paused` honestly if there's a multi-week gap.

---

## What is now decided (and what is not)

### Decided (do not revisit)

- The moat: open ledger via Datasette.
- The L3 backbone: statsmodels.DynamicFactorMQ.
- The event substrate: POLECAT + GDELT + UCDP.
- The frontend stack: Next.js + Tailwind v4 + shadcn + Lightweight Charts + TanStack Table.
- The orchestration boundary: Dagster (assets) + Arq (tasks).
- The auth: Better-Auth.
- The MCP server: 10 tools, vintage-stamped responses, mandatory provenance.
- The pricing: 4 tiers, free-tier substance, paid-tier velocity.
- The deploy: Cloudflare Pages + R2 + Fly.io.
- The editorial discipline: vintage permanence, miss-in-place, consensus side-by-side, reproducibility envelope, calibration as target.

### Not yet decided (Y1+ decisions)

- The chart-rendering ecosystem at the Pro tier (Vega-Lite opt-in vs Lightweight Charts everywhere).
- The Iceberg migration timing (when the TimescaleDB instance hits 500GB).
- The R2 vs S3 vintage tier decision (R2 cheaper, S3 broader ecosystem).
- The non-English roll-out cadence (Y2+).
- The team vs solo decision (Y2+).
- The VC vs revenue-funded decision (Y2+).

---

## The next 30 days (per `synthesis/NEXT-30-DAYS.md`)

Weeks 1-2: substrate work — Datasette mount, statsmodels.DynamicFactorMQ fit on US, POLECAT ingestion.
Week 3: public surface — npm install + deploy the Next.js scaffold to Cloudflare Pages, FastAPI service to Fly.io, MCP server to PyPI.
Week 4: editorial discipline — accountability ledger publicly opened, first daily digest cron, first miss post-mortem published.

**Done state at Day 30**: opengem.org renders the dashboard with real US data; api.opengem.org serves the forecast; data.opengem.org is the queryable ledger; one daily digest has gone out; one miss post-mortem is live.

That is the v0.5 milestone.

---

## What this 300-loop round produced

| Artifact | Count | Location |
|---|---|---|
| Loop artifacts (1 per loop or batched) | 300 logical | `research-300/loops/` |
| Cross-cutting synthesis docs | 7 | `research-300/synthesis/` + `research-300/{INDEX,STATUS,QUEUE}.md` |
| Working prototype code files | ~50 | `research-300/prototypes/` |
| Open-source repos cloned for inspection | 16 | `research-300/clones/` |
| Strategic pivots from prior plan | 3 | Datasette / statsmodels / POLECAT |
| Page-level product designs | 60 | Phase 3 loops |
| Forecast-mechanism specs | 50 | Phase 4 loops |
| Outreach + content engine plans | 7 | L291-L297 |
| Templates (post-mortem, retrospective, kanban) | 3 | L298-L299, L281 |
| ADRs locked | 11 | L272 |

---

## Closing

OPENGEM was scoped, at the start of this round, as a 5-year aspirational project with a Block I rebaseline as the year-one deliverable. After 300 loops, three findings (Datasette, statsmodels, POLECAT) collapsed the build cost by ~60-70%, and the Y0 deliverable now includes a minimum-viable public product.

The path forward is execution. The work in `research-300/` is the spec. The work in `research-300/prototypes/` is the scaffold. The work in `opengem-vintage/`, `opengem-data-*/`, `opengem-scenarios/`, `opengem-digest/`, and `opengem-narrative/` (already in the repo) is the substrate.

Most importantly: **the moat is real**. Bloomberg and the cartel cannot publish their track records. OPENGEM can. That single asymmetry, instantiated through the editorial discipline of vintage permanence + miss-in-place + reproducibility envelope, is what makes the Y5 "cited next to WEO" outcome plausible.

The next move belongs to execution. Stop researching. Start shipping.

— *Signed*, the 300-loop synthesis, 2026-06-06.

## Related

- [[L001-vision-statement]] — the round opener
- [[L010-five-year-arc]] — the arc this re-issues
- [[L271-master-prd]] — the canonical v1 PRD
- [[synthesis/MIDPOINT-FINDINGS]] — the three pivotal cost-collapses
- [[synthesis/NEXT-30-DAYS]] — the actionable plan
- [[synthesis/RUNBOOK-V0]] — the deployment runbook
