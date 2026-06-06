# L281 — Open Issues Kanban for v1: Top 30 Issues Prioritized

**Loop**: 281 / 30
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis of this loop

The PRD ([[L271]]) names what v1 must deliver. The ADRs ([[L272]]) name how it gets built. This loop sequences the 30 specific GitHub Issues that must close between today (W-12) and launch (W 0) for v1 to ship to spec. The issues are ordered by the dependency graph the PRD implies: data substrate first, then forecast pipeline, then API, then dashboard, then ledger, then launch surfaces.

Each issue lists: priority (P0 / P1 / P2), rough effort (XS / S / M / L / XL where XS ≤ 1 day, S = 1-3 days, M = 1 week, L = 2-3 weeks, XL = 1+ month), dependency, owner. P0 is "blocks launch"; P1 is "ships in v1 but de-scoped if needed"; P2 is "v1.1 candidate."

Owner is named even where there is only one team member (the founder). Naming makes accountability concrete.

---

## Track 1 — Data substrate (Issues 1-5)

### Issue #1 — Ingest POLECAT events into vintage store
- Priority: P0
- Effort: M (1 week)
- Dependency: none (foundation)
- Owner: founder
- Outcome: POLECAT weekly dump available at `data.opengem.com/polecat` and queryable by the geopolitical risk module. PLOVER ontology mapping locked in.

### Issue #2 — Wire UCDP API ingestion with token
- Priority: P0
- Effort: S
- Dependency: #1
- Owner: founder
- Outcome: UCDP daily delta loaded into the vintage store with attribution metadata. Conflict module reads from UCDP first, POLECAT second.

### Issue #3 — GDELT GKG nightly delta + tone overlay
- Priority: P0
- Effort: M
- Dependency: independent
- Owner: founder
- Outcome: GDELT nightly delta ingested; tone overlay aggregation for the geopolitical pulse map running.

### Issue #4 — World Bank Indicators API harvest into vintage store
- Priority: P0
- Effort: M
- Dependency: independent
- Owner: founder
- Outcome: 1,000+ World Bank series ingested with rate-limit-respecting cadence. Country × indicator matrix fill foundation.

### Issue #5 — IMF SDMX harvest + reconciliation with WB
- Priority: P0
- Effort: L
- Dependency: #4
- Owner: founder
- Outcome: IMF SDMX series ingested; WB / IMF reconciliation for overlapping series (with provenance-preserving choice rules per series).

---

## Track 2 — Forecast pipeline (Issues 6-10)

### Issue #6 — Wire Nixtla neuralforecast as L3 baseline
- Priority: P0
- Effort: L
- Dependency: #4
- Owner: founder
- Outcome: neuralforecast running nightly across Tier-V countries × headline indicators; outputs match the forecast.v1 schema.

### Issue #7 — statsmodels DFM + BVAR baselines (L1/L2)
- Priority: P0
- Effort: L
- Dependency: #4
- Owner: founder
- Outcome: L1 + L2 baselines running, outputting in forecast.v1 schema.

### Issue #8 — BMA combiner across L1/L2/L3
- Priority: P0
- Effort: M
- Dependency: #6, #7
- Owner: founder
- Outcome: BMA combiner produces the ensemble forecasts that the dashboard surfaces. Weights logged per vintage.

### Issue #9 — Bauer-Mertens recession probit
- Priority: P0
- Effort: M
- Dependency: independent (yield curve data)
- Owner: founder
- Outcome: Recession probability indicator running for USA + 8 other countries. Surfaced on the hero strip.

### Issue #10 — Forecast scoring pipeline (CRPS, log-score, PIT, MAE, RMSE)
- Priority: P0
- Effort: M
- Dependency: #6, #7, #8
- Owner: founder
- Outcome: Every forecast object gets scored as realized data lands. Scores stored in the vintage store; surfaced on /leaderboard and /accountability.

---

## Track 3 — API + MCP (Issues 11-15)

### Issue #11 — FastAPI service + OpenAPI 3.1 spec
- Priority: P0
- Effort: M
- Dependency: #5, #8, #10
- Owner: founder
- Outcome: REST API live with 18 endpoints from [[L271]] section 7; OpenAPI spec published at `api.opengem.com/openapi.json`.

### Issue #12 — MCP server (8 tools)
- Priority: P0
- Effort: M
- Dependency: #11
- Owner: founder
- Outcome: MCP server live at `mcp.opengem.com`; 8 tools from PRD section 8 functional; provenance + cite metadata included in every response.

### Issue #13 — RSS / Atom feed generator (3000+ feeds)
- Priority: P0
- Effort: M
- Dependency: #11
- Owner: founder
- Outcome: Per-country + per-indicator + per-scenario + digest feeds live at `feeds.opengem.com/*`.

### Issue #14 — Rate limiting + API key system
- Priority: P0
- Effort: S
- Dependency: #11
- Owner: founder
- Outcome: Cloudflare-backed rate limiting per the [[L276]] tier specifications. Free / Pro / Studio / Newsroom / Institutional caps enforced.

### Issue #15 — Webhook + alert delivery infrastructure
- Priority: P1
- Effort: M
- Dependency: #11
- Owner: founder
- Outcome: Webhook delivery for watchlist alerts (L131). Can de-scope to v1.1 if calendar tight.

---

## Track 4 — Dashboard pages (Issues 16-23)

### Issue #16 — Home page (`/`) — World Pulse + scenarios + forecast strip + Tier-V grid
- Priority: P0
- Effort: M
- Dependency: #11
- Owner: founder
- Outcome: `/` matches the wireframe in `/app/page.tsx`; all four sections live with real data.

### Issue #17 — Country page (`/countries/[iso3]`)
- Priority: P0
- Effort: L
- Dependency: #11, #16
- Owner: founder
- Outcome: 40+ countries live with situation tiles + forecast table + scenario impact + recent misses.

### Issue #18 — Indicator page (`/indicators/[id]`)
- Priority: P0
- Effort: M
- Dependency: #11, #16
- Owner: founder
- Outcome: 30+ indicators with cross-country comparison.

### Issue #19 — Forecast detail page with Lightweight Charts bands
- Priority: P0
- Effort: L
- Dependency: #11, #16
- Owner: founder
- Outcome: All v1 forecast cells have detail pages. Bands chart with consensus overlay; vintage history; methodology pop-up.

### Issue #20 — Leaderboard page with Finos Perspective grid
- Priority: P0
- Effort: M
- Dependency: #10, #11
- Owner: founder
- Outcome: `/leaderboard` operational; OPENGEM vs WEO vs OECD vs RW/AR(1); sortable by metric, time window.

### Issue #21 — Accountability ledger page (`/accountability`)
- Priority: P0
- Effort: M
- Dependency: #10, #11
- Owner: founder
- Outcome: Four-tile scoreboard + recent-misses table + publication-discipline checklist. Matches `/app/accountability/page.tsx`.

### Issue #22 — Methodology pages (`/methodology/[model]`)
- Priority: P0
- Effort: M
- Dependency: #6, #7, #8, #9
- Owner: founder
- Outcome: Every model card live with intended use, training data, eval metrics, limitations.

### Issue #23 — Scenario pages (`/scenarios/[slug]`)
- Priority: P0
- Effort: M
- Dependency: #11
- Owner: founder
- Outcome: 10+ canonical scenarios live with probability + triggers + affected countries + narrative.

---

## Track 5 — Embed + cite + provenance (Issues 24-26)

### Issue #24 — Embed widget (iframe + script SDK + PNG fallback)
- Priority: P0
- Effort: M
- Dependency: #16-#23
- Owner: founder
- Outcome: Embeds work in Substack, Ghost, Medium, WordPress, Reddit, Bluesky per [[L273]] Category 4 invariants.

### Issue #25 — Cite-this-view system with permanent URLs
- Priority: P0
- Effort: S
- Dependency: #11
- Owner: founder
- Outcome: Every view has a cite-this-view URL; BibTeX / APA / Chicago citation blocks available; URL resolves to the vintage-correct snapshot.

### Issue #26 — Provenance drawer + methodology pop-up on every chart
- Priority: P0
- Effort: S
- Dependency: #16-#23
- Owner: founder
- Outcome: Every chart has a hover-source-citation + click-to-methodology affordance. Verifies V&V Category 7.

---

## Track 6 — Monetization + launch surface (Issues 27-30)

### Issue #27 — Pricing page + Stripe checkout (5 tiers)
- Priority: P0
- Effort: M
- Dependency: independent
- Owner: founder
- Outcome: `/pricing` shows the [[L276]] 5-tier structure; Stripe checkout functional for Pro / Studio / Newsroom / Institutional; Vendor tier "contact us" form.

### Issue #28 — Marketing surfaces: `/why-different`, `/about`, `/governance`, `/changelog`, `/terms`, `/privacy`
- Priority: P0
- Effort: M
- Dependency: independent
- Owner: founder + content lead
- Outcome: All seven marketing pages live with content from L008, L283, L284, L271 §17.

### Issue #29 — Press kit + demo video deployed at `/press`
- Priority: P0
- Effort: M
- Dependency: launch-day video production
- Owner: founder
- Outcome: Press kit ZIP + HTML index live; 90s and 30s video files hosted on R2; founder bio + boilerplate + headlines per [[L278]].

### Issue #30 — Discord + Discourse community surfaces live
- Priority: P0
- Effort: S
- Dependency: #28
- Owner: founder
- Outcome: Discord instance live with the 6 channels from [[L280]]; charter + publish-misses pin posted; Discourse forum at `forum.opengem.com` mirrored; both linked from home page footer.

---

## Sequencing summary

```
W-12 — W-8  : Track 1 (data substrate) + Track 2 (forecast pipeline)
W-8  — W-5  : Track 3 (API + MCP) + Track 4 (dashboard pages)
W-5  — W-2  : Track 5 (embed + cite) + Track 6 (monetization + launch surface)
W-2  — W 0  : V&V hardening, external party trial, soft launch
W 0         : Public launch
```

Track 1 and Track 2 run in parallel after Issue #4 lands (the data substrate Issue #4 unblocks both pipelines). Track 3 starts when Track 2 has at least one model running end-to-end (Issue #8). Track 4 starts when Track 3 has the API stub serving (Issue #11). Tracks 5 and 6 can start independently of Track 4 as soon as the prototype is rendering.

---

## P1 / P2 backlog (top 10)

Carrying over to v1.1 release (Q1 2027):

| # | Title | Effort |
|---|---|---|
| 31 | Vintage time machine UI (rewind to historical) | L |
| 32 | Compare-2 view (any two countries / indicators) | M |
| 33 | Watchlist + alerts UX | M |
| 34 | Command palette (cmdk) | S |
| 35 | Notebook export with Codespaces button | M |
| 36 | Globe map (globe.gl) for geopolitical pulse | L |
| 37 | Mobile PWA refinements | M |
| 38 | DataCite member registration for cite-URLs | S |
| 39 | Plotly Resampler integration for 1M-point series | M |
| 40 | First Institutional white-label customer onboarding | L |

These are not v1 blockers but are v1.1 sprint candidates. Surfaced now so they don't get re-discovered as crises later.

---

## What this loop produced

- 30 prioritized issues across 6 tracks, with effort estimates and dependencies.
- Sequencing plan that maps each track to weeks W-12 → W 0.
- A P1/P2 backlog of 10 v1.1 candidates.

## What comes next

- The kanban is loaded into GitHub Issues at `github.com/opengem/opengem-1/issues` with the labels and milestones to match.
- Daily standup against the kanban from W-12 through W 0.
- **L287** — vendor checklist runs in parallel with Track 6 for Institutional readiness.

## Related

- [[L271-master-prd]] — the PRD this kanban operationalizes
- [[L272-adrs]] — ADRs the issues respect
- [[L273-vv-matrix-dashboard]] — V&V matrix the closed issues are validated against
- [[L277-launch-plan]] — launch surface the closed issues enable
