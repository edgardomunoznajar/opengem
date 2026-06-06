# L275 — Cost Projection (Cloudflare + R2 + DuckDB Cloud + AI)

**Loop**: 275 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis of this loop

A guerrilla-developer business is constrained by cost-per-active-user and cost-per-MCP-call, both of which compound non-linearly with growth if the architecture is wrong. This loop projects monthly infra cost across v0 (pre-launch), v1 (launch + 12 months), v2 (Y2), v3 (Y3) horizons, bottom-up, against the [[L272]] stack: Cloudflare Pages + R2 + Workers, Cloud Run for FastAPI + forecasting, Stripe, Resend, Plausible, and AI usage for narrative generation.

The headline finding: the Cloudflare-led architecture from ADR-024 keeps egress at zero, which means the dominant cost variable for the first 24 months is Cloud Run compute (the forecast pipeline) + AI tokens (narrative). Both are bounded and predictable. The architecture is sound for the projected revenue trajectory in [[L274]] KPI-7.

The second finding: at Y3 with Vendor-tier MCP traffic (10M+ calls/day), the Workers cost line crosses the others and becomes the largest single item — but it remains <5% of Vendor-tier ARR, so unit economics hold.

---

## The cost stack

Six variable cost lines + one fixed:

1. **Cloudflare Pages + Workers** — static hosting + serverless functions
2. **Cloudflare R2** — object storage (data, embeds, vintage snapshots)
3. **Cloud Run** — FastAPI service + forecast pipeline + Datasette
4. **AI tokens** — narrative generation (Claude / GPT for scenario / digest text)
5. **Stripe** — payment processing
6. **Resend** — transactional email
7. **Plausible / Umami** — analytics (fixed monthly fee)

Database costs are folded into Cloud Run (vintage store as Cloud SQL Postgres + SQLite-on-disk). DNS, domain registration, SSL — all under $50/year, ignored.

---

## v0 — Pre-launch (Q1-Q3 2026, before public launch)

The team is building. No paying customers yet. Internal dashboard + staging environments only.

| Line | Monthly cost (USD) | Notes |
|---|---|---|
| Cloudflare Pages | $0 | Free tier covers 500 builds + 1 TB egress |
| Workers | $5 | Workers Paid plan baseline |
| R2 | $0 | Free tier (10 GB storage, 10M Class A ops) |
| Cloud Run (FastAPI) | $20 | 2 vCPU / 4 GiB, scale-to-zero, ~100 req/day internal |
| Cloud Run (forecast pipeline) | $50 | Nightly pipeline run, ~30 min compute, no GPU |
| AI tokens (narrative) | $30 | ~1k pages × 500 tokens out × Claude 3.7 Sonnet pricing |
| Stripe | $0 | No transactions |
| Resend | $0 | Free tier (3k emails/mo) |
| Plausible | $19 | Solo plan |
| **Total monthly v0** | **~$124** | |

Annual v0 burn: ~$1,500. Founders self-fund.

---

## v1 — Launch + first 12 months (Q3 2026 → Q3 2027)

Public launch. Target KPI-5 trajectory: 50 WAU at month 1, 100 WAU at month 12. KPI-2 trajectory: 1k MCP calls/day at month 1, 100k MCP calls/day at month 12. KPI-7 trajectory: $0 MRR at month 1, ~$12k MRR at month 12.

| Line | Month 1 | Month 6 | Month 12 |
|---|---|---|---|
| Cloudflare Pages | $0 | $0 | $0 |
| Workers (requests + paid plan) | $5 | $15 | $40 |
| R2 (storage + ops) | $5 | $20 | $50 |
| Cloud Run (FastAPI, ~100 req/min avg) | $80 | $200 | $400 |
| Cloud Run (forecast pipeline) | $100 | $150 | $250 |
| AI tokens (narrative, ~3k pages updated daily) | $80 | $150 | $300 |
| Stripe (2.9% + 30¢) | $0 | $25 | $100 |
| Resend | $0 | $20 | $50 |
| Plausible | $19 | $19 | $19 |
| **Total month** | **~$289** | **~$599** | **~$1,209** |

Year-1 annualized: ~$8,800. Year-1 revenue (per KPI-7): ~$150k ARR. **Infra/revenue ratio at end Y1: ~6%, well under target 30%.**

Notes:

- Cloud Run is the dominant line. The forecasting pipeline is run nightly on a single c2-standard-8 instance, ~30 min wall clock, then scaled to zero. Forecast pipeline cost scales linearly with country×indicator coverage (which we control).
- Workers cost scales linearly with MCP calls. At 100k/day = 3M/mo, Workers Paid plan covers the first 10M; we're well under.
- R2 cost is dominated by storage. At 12 months we expect ~100 GB of vintage snapshots + embed PNGs + data tarballs. R2 storage is $0.015/GB/month; ~$1.50 storage + ~$45 operations.

---

## v2 — Y2 (Q3 2027 → Q3 2028)

Institutional adoption. KPI-5: 1k WAU. KPI-2: 1M MCP calls/day. KPI-7: ~$1M ARR.

| Line | Y2-end month |
|---|---|
| Cloudflare Pages | $0 |
| Workers (33M req/mo MCP + 100M total) | $150 |
| R2 (~500 GB storage + heavier ops) | $200 |
| Cloud Run (FastAPI scaled, multi-instance) | $1,200 |
| Cloud Run (forecast pipeline, hourly cadence for nowcasts) | $800 |
| AI tokens (narrative + scenario synthesis, more countries) | $1,200 |
| Stripe (~$83k MRR × 2.9%) | $2,400 |
| Resend (~50k emails/mo) | $200 |
| Plausible | $39 (business plan) |
| **Total monthly Y2** | **~$6,189** |

Year-2 annualized: ~$74k. Year-2 revenue: ~$1M. **Infra/revenue ratio at end Y2: ~7%.**

Notes:

- Cloud Run FastAPI now runs at 2-4 instances continuously due to API + MCP load. Per-instance cost ~$300/mo at sustained ~50% CPU.
- The forecast pipeline shifts to hourly cadence for nowcast-critical series (GDPNow, inflation nowcast, FCI) while remaining daily/weekly for long-horizon. Compute roughly 3x v1.
- AI tokens scale ~3x. The narrative pipeline now generates text for ~10k pages updated 2-3x/week.
- Stripe is the surprise line item — 2.9% of MRR is meaningful at ~$80k MRR. We absorb it because Stripe is what makes the Studio + Newsroom funnel work.

---

## v3 — Y3 (Q3 2028 → Q3 2029)

Incumbent peer. KPI-5: 10k WAU. KPI-2: 10M MCP calls/day. KPI-7: ~$4-5M ARR. First Vendor tier landed at $1-2M ARR.

| Line | Y3-end month |
|---|---|
| Cloudflare Pages | $0 |
| Workers (330M req/mo MCP + 1B total) | $1,500 |
| R2 (~2 TB storage + heavy ops) | $700 |
| Cloud Run (FastAPI scaled, ~8 instances) | $3,500 |
| Cloud Run (forecast pipeline, sub-hourly nowcasts) | $2,400 |
| AI tokens (~30k pages, scenario synthesis at scale) | $4,000 |
| Stripe (~$400k MRR × 2.9%) | $11,500 |
| Resend (~200k emails/mo) | $500 |
| Plausible | $99 (high traffic) |
| Cloud monitoring + logging (Datadog Free + GCP ops) | $200 |
| **Total monthly Y3** | **~$24,400** |

Year-3 annualized: ~$293k. Year-3 revenue: ~$4-5M. **Infra/revenue ratio at end Y3: ~6-7%.**

Notes:

- The Vendor tier brings 50-100% of MCP traffic. Workers cost crosses Cloud Run for the first time but remains modest relative to Vendor-tier revenue (which we price per-million-MCP-call).
- AI token cost is the second-largest line. We absorb it because narrative generation is what makes the country/indicator pages 2x more cite-worthy than raw data dumps.
- Stripe becomes the *largest* single line item, dwarfing infra. This is correct for a SaaS at this scale, but it argues for evaluating ACH / wire payment paths for the Institutional + Vendor tiers (which we should be doing anyway by Y3).
- Forecast pipeline at sub-hourly cadence for nowcasts means continuous Cloud Run instances. We accept the cost; it's what makes the dashboard feel live.

---

## v4 — Y5 projection (Q3 2030 → Q3 2031)

Citation-of-record. KPI-5: 100k WAU. KPI-2: 100M MCP calls/day. KPI-7: ~$15-25M ARR. 3-5 Vendor tier accounts.

| Line | Y5-end month |
|---|---|
| Workers (3.3B req/mo) | $14,000 |
| R2 (~10 TB) | $2,500 |
| Cloud Run (FastAPI + forecast + Datasette) | $15,000 |
| AI tokens (everything at scale) | $25,000 |
| Stripe (~$1.5M MRR × 2.9%) | $43,500 |
| Resend | $1,500 |
| Plausible | $300 |
| Monitoring | $1,500 |
| **Total monthly Y5** | **~$103,300** |

Year-5 annualized: ~$1.24M. Year-5 revenue: ~$20M (midpoint). **Infra/revenue ratio: ~6%.**

Notes:

- At Y5, the team is 25-40 people. Salaries dominate total burn (~$5-8M annually). Infra is ~$1.24M which is meaningful but not constraining.
- Workers + Cloud Run + AI tokens are roughly co-equal at Y5. Each ~$15-25k/mo.
- Stripe is still the single largest line item. Evaluate Adyen for cross-border at scale; consider whether building our own ACH layer makes sense for the Institutional tier.
- R2 holds ~10 TB at Y5: vintage snapshots over 5 years × all forecast objects × all countries × all indicators is a fat archive but very compressible (mostly numeric). R2 storage cost is negligible.

---

## Sensitivity to growth surprises

What if KPI-2 grows 10x faster than projected (the LLM-vendor lands earlier)?

| Scenario | MCP/day at Y1 | Workers cost at Y1 | Revenue impact |
|---|---|---|---|
| Base | 100k | $40/mo | $150k ARR |
| 10x MCP, no Vendor | 1M | $200/mo | $150k ARR (no monetization) |
| 10x MCP + Vendor lands | 1M | $200/mo + $2M from Vendor | $2.15M ARR |

The architecture absorbs 10x MCP growth at <$200/mo additional cost. The constraint isn't infra; it's whether a Vendor tier converts. If yes, ARR jumps an order of magnitude with effectively zero infra cost increase.

What if KPI-5 grows 10x faster (viral moment)?

| Scenario | WAU at Y1 | Workers cost | Cloud Run cost | Total monthly |
|---|---|---|---|---|
| Base | 100 | $40 | $400 | $1,200 |
| 10x WAU | 1,000 | $150 | $800 | $1,800 |

A 10x organic growth surprise costs us ~$600/mo more. Trivial relative to the upside.

The downside scenarios:

| Scenario | Hit |
|---|---|
| Cloudflare R2 pricing changes (egress fees added) | +$50k/yr at Y3, +$300k/yr at Y5 |
| Stripe pricing changes (raise to 3.5%) | +$50k/yr at Y3 |
| AI token pricing drops (Claude/GPT halve) | -$25k/yr at Y3 (good news) |
| Cloud Run cold-start hit (regional outage) | UX hit, no direct cost |

The asymmetric risk is R2 egress. Our entire architecture depends on R2's zero-egress model. If Cloudflare changes that, we have a multi-quarter migration to AWS S3 + CloudFront with proportionally larger costs. Mitigation: monitor R2 pricing announcements, keep the data layer abstracted so migration is technically tractable.

---

## Single-founder operability check

Y1 monthly infra ≈ $1,200; Y2 ≈ $6,200; Y3 ≈ $24,400. A single founder can manage:

- Y1: yes, no question. Total infra is below the cost of one developer-tools subscription bundle.
- Y2: yes. Founder + one part-time engineer per [[L010]] roadmap.
- Y3: tight. At $24k/mo infra + ~$2M revenue, the team grows to 6-10 per [[L010]]. Founder is no longer sole operator.

The cost structure does not force a hiring decision before the revenue justifies it. This is the goal: revenue-funded growth, no VC bridge round.

---

## Comparison vs incumbents

For context: Bloomberg's infrastructure spend is roughly 8-10% of revenue (~$1B on ~$11B revenue). Macrobond, FactSet, and Refinitiv are in similar ranges. OPENGEM at 6-7% across all horizons is competitive but not exceptional — the savings vs incumbents come from architecture (Cloudflare zero-egress, scale-to-zero serverless) rather than from being cheaper at the unit level.

The 6-7% ratio also leaves a substantial reserve. We can absorb a year of flat revenue without infra forcing layoffs.

---

## What this loop produced

- Bottom-up cost model for v0/v1/v2/v3/Y5 horizons.
- Per-line monthly cost across Cloudflare Pages + Workers, R2, Cloud Run, AI tokens, Stripe, Resend, Plausible.
- Sensitivity analysis on MCP-growth and WAU-growth surprises.
- Single-founder operability check across horizons.
- Infra/revenue ratio held at 6-7% across all horizons.
- Asymmetric downside: R2 egress pricing change is the single biggest risk to absorb.

## What comes next

- **L276** — pricing model that the revenue projections feed.
- **L287** — vendor checklist for paid tier (SOC2 etc cost lines folded in).
- **L290** — churn flow that determines retention against the cost base.

## Related

- [[L272-adrs]] — ADR-024 (Cloudflare + R2) is the architectural premise this cost projection rests on
- [[L274-kpi-dashboard-meta]] — KPI-7 (revenue) and Op-3 (infra/MRR) feed this
- [[L271-master-prd]] — section 13 references this projection
- [[L300-final-synthesis]] — re-audits at Y5
