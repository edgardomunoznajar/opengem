# L272 — Architecture Decision Records (ADR-015 through ADR-025)

**Loop**: 272 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## What this loop produces

Eleven architecture decision records covering the v1 release stack. Each ADR follows the lightweight Michael Nygard convention: Context (the forcing condition), Decision (what we chose), Consequences (what we accept). One paragraph per section, no longer. ADRs 1-14 live in the parent OPENGEM repo and predate the dashboard work; this loop introduces ADRs 15-25 for the dashboard layer.

ADRs are not invitations to debate; they are timestamps. If you read an ADR and disagree, file an issue to amend it. Until amended, the ADR is the policy.

---

## ADR-015 — Next.js 15 for the dashboard frontend

**Context.** The dashboard needs to be (a) server-renderable for SEO at the country × indicator matrix scale (~10,000 pages by Y1), (b) deployable to Cloudflare Pages without a Node origin server, (c) capable of streaming partial responses for the home-pulse strip, (d) edge-aware for global P95 latency, (e) familiar enough to attract drive-by contributors. SvelteKit, Astro, Qwik, Solid were all evaluated in [[L074]].

**Decision.** Next.js 15 with the App Router and React Server Components. Tailwind v4 for styling. shadcn-style component scaffolds. TypeScript everywhere. Deployed to Cloudflare Pages with Workers for dynamic routes.

**Consequences.** We accept the React tax: bundle size is larger than Svelte, hydration model is more complex than Astro. We get massive ecosystem (next-i18next, next-mdx-remote, next-seo), great vintage history (Vercel uses it themselves), and the Cloudflare Pages runtime fits our serverless model. The risk is React server component churn between Next versions; we pin major version and review the upgrade cost annually.

---

## ADR-016 — TradingView Lightweight Charts for time-series visualization

**Context.** The dashboard renders thousands of small-multiple sparklines and several dozen full-bands forecast charts. Bundle weight, runtime perf, and Bloomberg-feel are all constraints. D3, Plotly, Vega-Altair, Highcharts, Recharts, Lightweight Charts, and ECharts were compared in [[L069]], [[L072]], [[L015]].

**Decision.** Lightweight Charts (Apache-2.0, ~45kb gzipped) for the bands chart, vintage-history chart, leaderboard time-series. Pure-SVG sparklines (no JS dep) for the tile-level micro-charts. Plotly for the long-tail explorer pages (forecast diff, calibration plots) where interactivity matters more than perf.

**Consequences.** We get terminal-grade rendering at terminal-grade weight. Lightweight Charts has a smaller API surface than Plotly, which means custom overlays (consensus bands, vintage rewind) need bespoke layering — we accept this. Pure-SVG sparklines are zero-JS and SSR-perfect but require us to write our own utility. The 45kb cost is paid once per page.

---

## ADR-017 — Finos Perspective for the leaderboard grid

**Context.** The forecast leaderboard is a (forecaster × country × indicator × horizon × window) matrix that can hit ~100k cells. TanStack Table, AG Grid, Glide DataGrid, and Finos Perspective were compared in [[L014]], [[L070]].

**Decision.** Finos Perspective (Apache-2.0) for the leaderboard grid because it streams Arrow data, supports server-pivot, and handles 100k+ cells without re-renders. TanStack Table for everything else (forecast strip, indicator table, country list) because the data sizes are tractable and the design language stays consistent.

**Consequences.** Perspective is a heavier dependency (~600kb gzipped wasm) and we accept loading it only on the leaderboard route via dynamic import. The wasm load adds ~200ms to first interaction on that page; we offset with a skeleton state. TanStack Table for the other tables gives us shared row/cell/header components that match the design system in [[L146-L150]].

---

## ADR-018 — Nixtla (neuralforecast / statsforecast / mlforecast) as the L3 forecasting stack

**Context.** The forecasting layer (specified in Phase 4) needs to produce point + bands forecasts at horizons from nowcast through 5Y across ~120 countries × ~50 indicators. statsmodels, Stan/PyMC, sktime, darts, Nixtla, and BGVAR-R were compared in [[L035]], [[L044]], [[L038]].

**Decision.** Nixtla's neuralforecast as the L3 (machine-learning) baseline; statsmodels DFM + Bayesian VAR as L1/L2 (econometric) baselines; BMA combiner over the L1/L2/L3 outputs (specified in [[L189]]). The Nixtla stack is Apache-2.0, GPU-optional, and has a clean API that fits our pipeline.

**Consequences.** We get a credible ML baseline without taking on the maintenance of building one. We accept Nixtla's release cadence (occasionally breaking) and pin minor versions. The BMA combiner is OPENGEM's own code, which means our differentiating IP is in the combiner not the bases — appropriate for an open-source project. If Nixtla drops a feature we need, we fork or rewrite at L3 level only.

---

## ADR-019 — docling for PDF/table extraction from source publications

**Context.** A meaningful fraction of macro data is published as PDF: IMF WEO tables, OECD EO chapters, central-bank monetary policy reports, BIS chapter annexes. We need to extract tables reliably. Camelot, Tabula, pdfplumber, AWS Textract, Adobe Extract, and docling were compared in [[L018]].

**Decision.** IBM's docling (MIT-licensed) as the primary extraction pipeline. Camelot + pdfplumber as fallbacks for specific failure modes. AWS Textract / Adobe Extract are out of scope (closed, per-call cost, license incompatible).

**Consequences.** docling's accuracy on bank/IMF table layouts is strong but not perfect; we accept a manual-review queue for high-stakes extractions (WEO headline tables, OECD EO key indicators). The fallback chain is automatic. We monitor docling release notes and re-baseline accuracy quarterly. If accuracy degrades, the fallback chain absorbs the failure.

---

## ADR-020 — Datasette for the public raw-data layer

**Context.** The dashboard surfaces aggregates and forecasts. Power users want raw data: every series, every observation, every vintage. We need a SQL-queryable read-only layer at `data.opengem.com`. Datasette, public S3 + Athena, public PostgreSQL, and DuckDB Cloud were compared in [[L076]], [[L077]].

**Decision.** Datasette (Apache-2.0) mounted at `data.opengem.com` exposing the vintage store as SQLite + Parquet. DuckDB-WASM at the page level for client-side query, demonstrated in [[L254]]. Both layers read-only; no write surface ever.

**Consequences.** Datasette is the right pattern for read-only public data: instant API, SQL query UI, JSON / CSV / Parquet export, embedded charting. We accept Datasette's single-process write bottleneck because we have no writes. The DuckDB-WASM layer lets prosumers run SQL in their browser without round-tripping; we accept the wasm payload (~6mb) only on data-explorer pages.

---

## ADR-021 — MCP tools as the public API canonical surface

**Context.** OPENGEM exposes data through REST API, RSS, JSON-block, embed, and MCP. The strategic question is which surface is *canonical* — which one the others derive from. REST-first vs MCP-first vs schema-first were debated in [[L108]], [[L177]].

**Decision.** MCP-first. Each MCP tool defines its input schema (Zod-typed), its output schema (Zod-typed), and its provenance contract (every response carries `vintage_id`, `source_url`, `methodology_url`). The REST API is generated from the MCP tool definitions. The RSS feeds are scheduled-cron projections of MCP tool outputs. The embed widget is an MCP-tool call with rendering on top.

**Consequences.** We bet that the LLM-grounding surface (MCP) is the durable one and the developer-API surface (REST) is the transitional one. By making MCP canonical we ensure both surfaces evolve in lockstep and avoid the trap of building two parallel APIs that drift. The risk is MCP protocol churn; we pin the protocol version and review every two months.

---

## ADR-022 — POLECAT over ACLED for the geopolitical event substrate

**Context.** OPENGEM needs a structured event-stream for the geopolitical risk module. ACLED, POLECAT, UCDP, GDELT, and ICEWS-legacy were evaluated in [[L021]]-[[L030]]. ACLED is the household name; POLECAT is the academic successor to ICEWS hosted on Harvard Dataverse.

**Decision.** POLECAT (CC0, Harvard Dataverse) + UCDP (CC-BY-4.0) + GDELT (free with citation) as the primary substrate. ACLED is YELLOW per EULA — published derived/transformative aggregates with attribution are permitted; raw row republication is not. ACLED-derived metrics stay free-tier-only at v1; paid-tier endpoints touching ACLED would require a commercial license negotiation we defer to Y2.

**Consequences.** POLECAT gives us ~95% of what ACLED provides, weekly cadence, ML-coded events on the PLOVER ontology, 2018-present coverage, with no EULA dance. UCDP gives us deeper history for fatal-conflict events. GDELT gives us the live tone overlay. ACLED becomes a *benchmark* on the leaderboard, not a *substrate* in the dashboard. If ACLED tightens licensing further, we lose nothing; if POLECAT degrades, we have GDELT + UCDP fallback.

---

## ADR-023 — Stripe Checkout for paid-tier monetization

**Context.** Five pricing tiers (Studio / Newsroom / Institutional / Vendor) require a payment surface. Stripe, Paddle, Lemon Squeezy, and rolling our own with Adyen were compared. The payment surface needs subscription billing, magic-link auth, EU VAT MOSS handling, SCA, and Apple/Google Pay.

**Decision.** Stripe Checkout for subscription flows. Stripe Customer Portal for self-serve plan changes. Stripe Billing for usage-based MCP overage. Magic-link auth via Resend + signed JWT (no password storage). Stripe handles all tax/VAT/SCA.

**Consequences.** We accept Stripe's ~3% take. We get global payment coverage, mature subscription primitives, and an Apple/Google Pay UX out of the box. The magic-link flow keeps our PII surface minimal — email is the only identifier we store. Stripe's webhook reliability is excellent. The risk is Stripe vendor lock-in; we keep the customer model in our own DB with Stripe IDs as foreign keys, so migration is technically tractable if needed.

---

## ADR-024 — Cloudflare Pages + R2 + Workers as the deployment substrate

**Context.** OPENGEM is global, low-revenue-per-user, latency-sensitive (LLM grounding), bandwidth-heavy (charts + downloads), and single-founder operated. Vercel, Netlify, AWS Amplify, Cloudflare Pages + R2, and self-hosted Kubernetes were compared in [[L269]].

**Decision.** Cloudflare Pages for the Next.js dashboard. Cloudflare R2 for object storage (data tarballs, embed PNGs, vintage snapshots). Cloudflare Workers for dynamic routes (MCP server, cite-this-view redirector, embed widget). FastAPI service on Cloud Run for the heavy forecasting backend. Datasette on Cloud Run with R2-backed SQLite.

**Consequences.** R2 has zero egress fees, which collapses our largest cost variable to near-zero compared to AWS S3. Workers' V8 isolates give us ~5ms cold start, which makes the MCP server feel native. The Cloudflare CDN edge is the most distributed in the industry. We accept Cloudflare-specific Worker APIs (we abstract our handlers with hono so we could migrate if needed). The single biggest risk is Cloudflare outages — multi-region failover is not realistic at our scale, but R2 has independent geographic redundancy.

---

## ADR-025 — GitHub-hosted accountability ledger and post-mortem corpus

**Context.** The accountability ledger and post-mortem corpus are core brand artifacts. They need to be public, append-only, audit-trail-bearing, and (ideally) community-contributable. CMS (Sanity, Contentful), GitHub repo, S3 + Markdown, Datasette tables, and Obsidian Publish were compared.

**Decision.** A public GitHub repository (`opengem/accountability-ledger`, Apache-2.0 license for code, CC-BY-4.0 for content) holds the canonical post-mortem corpus as Markdown + JSON. The dashboard at `/accountability` and `/postmortem/[slug]` reads from this repo at build time. Pull-request workflow for amendments. Issues for community-flagged misses we may have missed.

**Consequences.** Every post-mortem has a git-traceable history. Every amendment shows up as a PR with reviewer signoff. The community can flag misses we missed by opening an issue. GitHub gives us free auditability, free CDN (via raw.githubusercontent.com), free authentication for contributors. The risk is GitHub-the-platform changes; we mirror the repo to an S3 bucket nightly as backup. The post-mortem URLs use slugs that are independent of the git path so we can migrate hosts without breaking citations.

---

## Cross-cutting consequences

Three observations across the eleven ADRs:

1. **Cloudflare + Stripe + GitHub is the operational triangle.** No other vendors are foundational. Postgres / Redis / Auth0 / Algolia are all explicitly avoided where Cloudflare / GitHub / our own code can substitute. Total third-party vendor count at v1: 5 (Cloudflare, Stripe, GitHub, Resend for transactional email, Plausible for analytics).

2. **Open licenses everywhere.** Apache-2.0 (Next.js, Lightweight Charts, Perspective, docling, Datasette, our own code), MIT (TanStack, hono), CC-BY-4.0 / CC0 (POLECAT, UCDP, GDELT, our own data). Single license-incompatible decision avoided: rejecting AWS-only services and EULA-laden datasets.

3. **MCP-first means surface unification.** ADR-021 is the most strategic decision. By making MCP the canonical contract, every downstream surface (REST, RSS, embed) is generated from the same source. Drift between surfaces becomes structurally impossible.

---

## What this loop produced

- ADRs 15-25, one paragraph per section (context / decision / consequences).
- Cross-cutting analysis identifying the Cloudflare-Stripe-GitHub triangle, open-license discipline, and MCP-first surface unification.
- Pointers to upstream Phase 1/2/5 loops where each decision was first surfaced.

## What comes next

- **L273** — V&V matrix that validates the ADRs hold under load.
- **L275** — cost projection that costs out the Cloudflare + R2 + Cloud Run line items.
- **L282** — license audit that verifies the ADR-020/024/025 license claims.

## Related

- [[L271-master-prd]] — the PRD whose architecture choices these ADRs encode
- [[L011-openbb-terminal]] through [[L080-scenario-engine-libs]] — Phase 1 evaluations underpinning the ADRs
- [[L269-deploy-plan]] — ADR-024 prototype
- [[L250-mcp-server]] — ADR-021 prototype
- [[L300-final-synthesis]] — re-reads these ADRs against five-year actuals
