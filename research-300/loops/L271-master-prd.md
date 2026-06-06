# L271 — Master "World Dashboard PRD" v1 Draft

**Loop**: 271 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06
**Status**: Draft v1.0 — the canonical PRD for the v1 release

---

## 0. Document purpose

This is the spine of the v1 release. Every other Phase 6 artifact resolves back to a section of this PRD. If a Phase 1-5 loop and this PRD disagree, the PRD wins for the v1 cut; the loop is the longer-arc vision. If the team has fifteen minutes to explain OPENGEM to a serious external party (an academic, a journalist, a potential institutional buyer, an LLM vendor), they read this document aloud.

Length target: 4000+ words. Re-read every two weeks until launch.

---

## 1. Vision

**OPENGEM is the public macro-accountability ledger for the world economy.** A Bloomberg-grade dashboard for everyone, where every forecast is open, every number is dated, and every miss is named. The product is a Next.js single-page-application served from Cloudflare Pages, backed by a Python FastAPI service exposed through both HTTP and MCP, drawing from a vintage-correct data store derived from open public sources.

The thesis is the one in [[L001-vision-statement]]: the forecasting cartel — IMF WEO, OECD EO, Bloomberg Economics, Goldman GIR, Stratfor — produce priced forecasts whose track records are private. Their margins depend on opacity. OPENGEM has no margins to protect, so it can publish what they cannot: every vintage, every backtest, every miss, every methodology, with the post-mortem in the same place as the original. That is the asymmetry. Five years of compounded verifiable accuracy is impossible to copy because copying it means breaking the incumbent business model.

The v1 PRD operationalizes this thesis into shippable surface. We are not building the entire arc in one quarter; we are building the credible *seed* of it. Y1 success is a working system that proves the seed will compound: one hundred weekly humans, one academic citation, one press citation, the first failure-log post-mortem, the first three white-label customers. The PRD below specifies what we ship to make that seed real.

---

## 2. Personas (recap from L003, scoped for v1)

Three primary personas drive v1 decisions:

1. **Damian — the macro YouTuber.** 47k subscribers, weekly video, needs charts that look better than Bloomberg screenshots in his Final Cut timeline. He pastes OPENGEM PNG exports with a clean watermark; the watermark is search-friendly so his viewers Google "opengem" and discover the dashboard.

2. **Marcus — the journalist/researcher.** Reuters-trained, writes for FT, Bloomberg Opinion, occasionally Bloomberg Markets desk. Needs numbers with provenance he can defend in editorial review. Pastes the cite-this-view URL into Drafts; the URL resolves to a permanent vintage-stamped chart with full lineage. The provenance drawer is what wins him over.

3. **Nadia — the sovereign-fund LP / institutional researcher.** Works at a regional central bank, sovereign wealth fund, NGO, or think tank. Needs Bloomberg-grade visuals under her institution's brand. White-label embed at $499-$4,999/mo. The vendor checklist (L287) must pass.

Secondary personas (Greg the retail prosumer, Lin the geopolitics researcher, Priya the NGO data lead) are first-class users but their needs are satisfied as side-effects of building the three primary surfaces. Anti-personas (Yusuf the day trader, Aiko the BD intern, Kenji the Stratfor copy-paster) are explicitly refused — see [[L009-anti-personas]].

---

## 3. Jobs-to-be-done (recap from L004, scoped for v1)

The 25 atomic JTBDs cluster into seven jobs that v1 must satisfy:

1. **"Show me the world's state in one screen."** Hero strip + scenarios + forecast strip + country grid on home. Done at [[/app/page.tsx]].
2. **"Show me one country's macro state."** Country page with situation tiles + forecast table + scenario impact. Done at `/countries/[iso3]`.
3. **"Show me one indicator across countries."** Indicator cross-country table with forecast bands. Done at `/indicators/[id]`.
4. **"Show me a forecast with its bands, consensus, and provenance."** Forecast detail page with chart + P10/P50/P90 + WEO/OECD overlay + methodology pop-up.
5. **"Show me your track record."** Accountability ledger page with scoreboard + recent misses + post-mortems. Done at `/accountability` — [[L285]] specifies the content model.
6. **"Let me cite this view in a paper / post / video."** Cite-this-view URL with DataCite-style identifier; copyable BibTeX block.
7. **"Let me embed this chart in my workflow."** Embed iframe + script SDK + RSS feed + JSON-block per chart + MCP tool surface.

Every page of v1 services at least one of these seven. If a page services none, it does not ship in v1.

---

## 4. Information architecture (from L121-L122)

Top-level navigation (8 entries, hard cap):

```
PULSE   COUNTRIES   INDICATORS   SCENARIOS   FORECASTS   LEADERBOARD   METHODOLOGY   ACCOUNTABILITY
```

Plus an always-visible command palette (`⌘K`) that searches across countries, indicators, scenarios, and forecast IDs. Plus a persistent footer band that says: *"Every number on this page is vintage-stamped. Click any chart for the source."*

Second-level routes:

- `/` — Pulse (home)
- `/countries` — country grid; `/countries/[iso3]` — per-country page
- `/indicators` — indicator catalog; `/indicators/[id]` — cross-country forecast for one indicator
- `/scenarios` — scenarios index; `/scenarios/[slug]` — scenario detail
- `/forecasts` — forecast strip overview; `/forecasts/[country]/[indicator]/[horizon]` — forecast detail
- `/leaderboard` — forecast accuracy comparison vs WEO / OECD / consensus
- `/methodology` — methodology landing; `/methodology/[model]` — per-model card
- `/accountability` — track record + recent misses + post-mortems
- `/postmortem/[slug]` — individual miss post-mortem
- `/cite/[id]` — permanent cite-this-view URL
- `/embed/[id]` — embed iframe target
- `/api` — API documentation
- `/mcp` — MCP install
- `/pricing` — pricing tiers
- `/about`, `/governance`, `/changelog`, `/terms`, `/privacy`

URL convention: never re-key, never re-slug. Once published, the URL is permanent. See [[L154-url-convention]].

---

## 5. Page-by-page specifications

### 5.1 Home (`/`)

Four sections, top to bottom:

1. **World Pulse** — six situation indicator tiles (US recession 12m, geopolitical risk, supply chain pressure, US financial conditions, US inflation nowcast, US GDP nowcast). Each tile is a hover-clickable card with sparkline, delta, and as-of timestamp.
2. **Active scenarios** — top four scenarios by probability × impact, each with probability pill, affected countries, one-line description, link to scenario detail.
3. **Forecast strip — 4Q ahead** — sortable table of forecasts for Tier-V countries × headline indicators, with OPENGEM point + bands + WEO + OECD + badges.
4. **Countries — Tier-V coverage** — 22-card grid of Tier-V economies, each with flag + recession-prob pill + 3-metric mini-grid.

Wireframe: see `/app/page.tsx` in the prototype.

### 5.2 Country page (`/countries/[iso3]`)

Six sections:

1. Country header (flag, name, recession prob, GPR, regime classifier badges, as-of)
2. Five situation tiles specific to country (CPI, GDP, Unemp, Policy Rate, Current Account)
3. Forecast table — all indicators × all horizons we cover for this country, with OPENGEM + WEO + OECD + badges
4. Scenario impact panel — top three active scenarios affecting this country
5. Recent misses panel — last six misses for this country, with post-mortem links
6. Methodology + provenance + RSS + cite-this-view affordances

### 5.3 Indicator page (`/indicators/[id]`)

Five sections:

1. Indicator header (name, definition, source, units)
2. Cross-country comparison chart (sparklines or small multiples) for Tier-V + selected Tier-T
3. Forecast table — every country we cover for this indicator × every horizon
4. Methodology pop-up linked to the model that generates this indicator's nowcast
5. RSS + JSON + cite-this-view affordances

### 5.4 Scenario page (`/scenarios/[slug]`)

Six sections:

1. Scenario header (name, probability, triggers, affected countries, as-of)
2. Narrative description (Markdown body)
3. Trigger conditions + probability synthesis
4. Affected-country panel — per-country impact deltas vs baseline
5. Historical analogue (if applicable)
6. Methodology + provenance + cite-this-view

### 5.5 Forecast detail (`/forecasts/[country]/[indicator]/[horizon]`)

Eight sections:

1. Forecast header (country, indicator, horizon, vintage, methodology badge)
2. Bands chart (Lightweight Charts) with P10/P50/P90 fan + WEO/OECD overlay
3. Vintage history — every prior vintage of this forecast, hover-rewindable
4. Comparison table vs WEO, OECD EO, Bloomberg Economics (where public), consensus
5. Input lineage drawer — what data fed this forecast, with vintage stamps
6. Methodology pop-up — full model card
7. Score history — accuracy of this forecast object over its lifetime
8. Cite-this-view + embed + RSS

### 5.6 Leaderboard (`/leaderboard`)

Single page:

1. Filterable matrix — rows are forecasters (OPENGEM, WEO, OECD EO, Bloomberg Economics, consensus, RW/AR(1) baseline), columns are (country × indicator × horizon).
2. Cell content: accuracy score (CRPS, log-score, MAE, RMSE) with the metric selectable.
3. Time window selectable (last 4 quarters, last 8, last 12, all-time).
4. Headline summary: where OPENGEM beats consensus, where consensus beats OPENGEM, where the field is too tight to call.

### 5.7 Methodology (`/methodology` and `/methodology/[model]`)

Index page lists every model we run. Each model page has the full Model Card per Mitchell et al. format (adapted for econometric forecasting): intended use, training data, evaluation metrics, known limitations, ethical considerations, assumptions, code link.

### 5.8 Accountability (`/accountability`)

See [[L285]] for the full spec. Headline summary + four-tile scoreboard (published / scored / out-of-band / pending) + recent-misses table + publication-discipline checklist. The page that does not exist anywhere else.

### 5.9 Cite-this-view (`/cite/[id]`)

Permanent URL for any view a user has cited. Resolves to:

1. The original chart, rendered as it was at vintage time (not as-of-now).
2. BibTeX + RIS + APA + Chicago + MLA citation blocks.
3. DOI-style identifier (DataCite member status Y2).
4. Citation graph — who else has cited this view.

### 5.10 Embed (`/embed/[id]`)

Iframe target with minimal chrome. Three sizes: 320×200 (thumbnail), 600×400 (standard), 900×600 (large). Themes: terminal, editorial, broadcast. Auto-resizes; uses postMessage for parent-frame integration.

---

## 6. Forecasting mechanics (recap from Phase 4)

The forecasting layer underneath the dashboard is specified in [[L181-forecast-object-schema]] through [[L230]]. The dashboard surfaces these objects without re-implementing them.

Key contract:

- **Forecast objects are immutable.** Once published, a forecast is permanent. Revisions create new vintages with forward-link pointers. See [[L182]].
- **Bands are P10/P50/P90 by default.** Optionally P5/P25/P75/P95 for high-stakes forecasts (recession probability, debt sustainability). See [[L188]].
- **Scoring is automatic.** CRPS, log-score, PIT, signed MAE, calibration-band coverage. See [[L183]].
- **Vintage history is queryable.** Rewind UI ("Show me what OPENGEM was predicting in Sept 2024"). See [[L173-vintage-time-machine]].
- **Misses are detected within 24h of realised data landing.** Post-mortem is human-authored within 7 days. See [[L200-failure-log]].

The dashboard layer does not produce forecasts; it surfaces them. Producer / consumer separation is preserved.

---

## 7. API (recap from L249-openapi-spec)

Public REST API at `api.opengem.com/v1` with OpenAPI 3.1 spec. Core endpoints:

```
GET  /v1/situation                                 — top-level pulse
GET  /v1/countries                                 — country catalog
GET  /v1/countries/{iso3}                          — country detail
GET  /v1/indicators                                — indicator catalog
GET  /v1/indicators/{id}                           — indicator cross-country
GET  /v1/scenarios                                 — scenarios index
GET  /v1/scenarios/{slug}                          — scenario detail
GET  /v1/forecasts                                 — forecast strip
GET  /v1/forecasts/{country}/{indicator}/{horizon} — forecast detail
GET  /v1/forecasts/{country}/{indicator}/{horizon}/vintage/{vintage} — historical
GET  /v1/leaderboard                               — forecast leaderboard
GET  /v1/methodology/{model}                       — model card
GET  /v1/track-record/{country}                    — accountability data
GET  /v1/failures/{entry_id}                       — single miss entry
GET  /v1/cite/{id}                                 — citation metadata
```

Rate limits per tier: Free 1k/day; Studio 100k/day; Newsroom 1M/day; Institutional unlimited.

RSS / Atom feeds per slice. Aim: ~3,000 feeds at v1 (per country × per indicator × per scenario × digest).

---

## 8. MCP (recap from L108, L177, L250)

Public MCP server at `mcp.opengem.com` (`mcp+https://mcp.opengem.com/sse`). Eight tools at v1:

1. `get_forecast(country, indicator, horizon)` — point + bands + consensus
2. `compare_forecasts(forecasts[])` — multi-forecast comparison
3. `list_scenarios(min_probability)` — active scenarios
4. `get_recession_probability(country, horizon)` — Bauer-Mertens style probit output
5. `get_gpr_nowcast(country)` — Caldara-Iacoviello GPR
6. `rewind_vintage(forecast_id, vintage_date)` — historical view
7. `get_leaderboard(country, indicator, metric, window)` — accuracy comparison
8. `list_misses(country, since)` — recent miss entries with post-mortem links

Every tool response includes `vintage_id`, `source_url`, and `methodology_url`. LLMs that respect source attribution will surface "according to OPENGEM" in their replies. This is the passive distribution engine.

Throughput per tier: Free 100/day per IP; Researcher 10k/day; Team 100k/day; Vendor 1M+/day.

---

## 9. Embed widget (recap from L245)

JavaScript SDK at `embed.opengem.com/v1/sdk.js`. Three integration modes:

1. **Iframe** — `<iframe src="https://opengem.com/embed/[id]?theme=terminal&size=standard" />`
2. **Script SDK** — `<div id="opengem-chart" data-view="USA-cpi-4Q-2026Q3"></div>` + `<script src="...sdk.js"></script>`
3. **Static PNG fallback** — `<img src="https://opengem.com/embed/[id].png?theme=terminal&size=standard" />`

Watermark: subtle but visible; clickable to the source page. White-label tier (Studio+) removes the OPENGEM brand-mark; attribution link in footer remains mandatory (this is in the EULA, not removable).

---

## 10. Monetization (recap from L006, L260, L276)

Five tiers:

| Tier | Price | Audience |
|---|---|---|
| **Free** | $0 forever | Everyone. Public dashboard, RSS, JSON, embed with attribution, 1k API/day, 100 MCP/day |
| **Studio** | $99/mo | Substack writers, mid-tier publishers, freelance analysts. White-label embed, 100k API, 10k MCP |
| **Newsroom** | $499/mo | Small newsrooms, magazines, think-tank comms. 10 seats, branded digest, 1M API, 100k MCP |
| **Institutional** | $4,999/mo + setup | NGOs, sovereign funds, regional central banks. Custom subdomain, NDA, SOC2, unlimited |
| **Vendor** | Custom | LLM platforms. OEM-tier MCP, per-million pricing, co-marketing |

The free tier is the whole product. The paid tier never gates substance; it gates velocity and fit. The "never charge for" block is on the pricing page in the same visual weight as the tier comparison. See [[L283-tos-draft]] for the contractual mirror.

24-month ARR target: $1.6M. 60-month ARR target: $15-25M with Vendor tier compounding.

---

## 11. V&V (verification + validation)

Three V&V layers operate in parallel:

1. **Forecast V&V** — CRPS / log-score / PIT / calibration / coverage. Operated by the forecasting product. Surfaced at [[L194-coverage-page]].
2. **Dashboard V&V** — Lighthouse perf budget, a11y score, SEO score, embed-in-the-wild test, MCP round-trip latency, time-to-first-pixel. Specified at [[L273]].
3. **Brand V&V** — five-promises audit: every chart resolves to source, every forecast carries vintage, every page links to methodology, every miss is named, every export is open.

V&V failures are not silently fixed. Significant drift triggers a public note on the changelog page. The L008 promises are not aspirations; they are testable invariants.

---

## 12. Launch criteria (the v1 release gate)

We do not ship v1 until all of the following are true:

1. **Coverage**: 40+ countries × 5 core indicators × 4 horizons. ~800 forecast cells live.
2. **Lighthouse**: home + country + forecast detail score ≥ 90 perf, ≥ 95 a11y, ≥ 95 SEO.
3. **MCP round-trip**: 8 tools live, all under 1.5s P95 latency.
4. **Embed**: works in Substack, Ghost, Medium, WordPress, Reddit, Bluesky. Tested by a real external party (Damian).
5. **Accountability ledger**: live at `/accountability` with the four-tile scoreboard, recent-misses table, publication-discipline checklist. Zero misses logged at launch is fine; the schema is live.
6. **Five-promises page**: live at `/why-different` with the comparison matrix. Every claim verifiable.
7. **Terms, privacy, license**: live and reviewed by a lawyer. License audit (L282) passes.
8. **Pricing page + Stripe checkout**: live. The free tier is fully functional; the paid tiers can be subscribed to even if no one does in week one.
9. **OpenAPI + MCP install page**: live with copy-paste install snippets for Claude Desktop, Cursor, ChatGPT, VS Code.
10. **At least one external party**: Damian uses the dashboard for one video; the embed runs in his published episode.

If 1-9 are met but 10 is not, we delay launch until Damian (or equivalent) has used the product in anger. The launch story is *not* a Show HN; it is a credible external user's first use, which we *then* tell on HN.

---

## 13. Post-launch metrics (the meta-dashboard from L274)

Eight KPIs tracked on an internal dashboard:

1. **DAU / WAU / MAU** — active humans on the public surface
2. **MCP tool calls/day** — passive LLM distribution
3. **Vintaged-views/day** — depth-of-engagement signal
4. **Embed impressions** — third-party reach
5. **/accountability views** — the most important KPI; every visit is a brand-credibility deposit
6. **API requests** — bottom of the integration funnel
7. **Paid conversions** — free → Studio, Studio → Newsroom, Newsroom → Institutional
8. **Churn** — paid → cancelled, with reason captured in exit survey

Reported weekly internally, monthly in the public changelog. The /accountability views metric is published quarterly on the retrospective page (L299).

---

## 14. Non-goals for v1

Explicitly out of scope for v1 (these are Y1-Y2 items):

- Counterfactual scenarios with simulation (Y2)
- Notebook export with one-click Codespaces (Y2)
- Multi-language UI (Y2)
- Mobile-native app (PWA-first; native is Y3+)
- Real-time intraday data (never — see [[L001]] musts-not)
- Black-box AI forecast (never)
- Premium forecasts behind paywall (never)
- Day-trader / Stratfor-copy-paster anti-personas (see [[L009]])

If a feature request lands in v1 scope and matches a non-goal, the answer is no, with a link to this section.

---

## 15. Open risks

Five risks the team accepts at v1:

1. **The ACLED license** — we depend on POLECAT + UCDP as GREEN substitutes. If POLECAT degrades, we have a fallback gap. Mitigation: ingest both, treat ACLED as benchmark-only.
2. **The OpenSanctions CC-BY-NC license** — paid tier surface that touches sanctions data needs a commercial license. Mitigation: written interpretation requested pre-launch; sanctions data isolated to a feature flag for paid tier.
3. **The first failure-log post-mortem** — if our first published miss is sloppy or evasive, the brand promise collapses. Mitigation: founder + one external editor review every post-mortem before publish; first one is a *small* miss to learn the process on.
4. **The Lighthouse budget** — if we miss the ≥90 perf score on launch day, the SEO compounds slowly. Mitigation: perf budget is a CI gate, not a target; PRs that regress perf are blocked.
5. **The white-label conversion** — if zero institutions buy in the first six months, the 24-month ARR target is at risk. Mitigation: pre-launch sales conversations with three named NGOs; soft-launch the Institutional tier with a charter customer.

Each risk has a named owner and a quarterly review.

---

## 16. The release calendar

| Week | Milestone |
|---|---|
| W-12 | PRD frozen (this document). Begin parallel build tracks. |
| W-10 | Forecast pipeline produces all v1 forecast cells. |
| W-8 | Dashboard prototype renders all v1 pages with fixture data. |
| W-6 | API + MCP live in staging. OpenAPI spec published. |
| W-5 | Accountability ledger live in staging. Failure-log schema deployed. |
| W-4 | License audit passes. ToS + Privacy live. |
| W-3 | External party (Damian) trial use. |
| W-2 | Press kit + screenshots + demo video finalized. |
| W-1 | Soft launch — five hand-picked external users, founders + early supporters. |
| W-0 | Public launch — Show HN, ProductHunt, r/datasets, econtwitter, Substack mirror live. |

W-12 is approximately Q2 2026 if we hold to the Q3 2026 launch named in [[L010-five-year-arc]].

---

## 17. Owner + governance

Single accountable owner at v1: Edgardo (founder). Decisions follow the L136 governance model: founder has final call; advisory board (3 macro economists + 2 open-data leaders + 1 LLM-product specialist) reviews quarterly; community feedback channels via Discord (L280) and GitHub Issues.

Changes to this PRD post-W-12 require: (a) owner approval, (b) recorded rationale in the changelog page, (c) downstream artifact updates within 5 business days. PRD drift is a P0 incident.

---

## What this loop produced

- The canonical v1 product requirements document.
- Sections covering vision, personas, JTBDs, IA, page-by-page, forecasting mechanics, API, MCP, embed, monetization, V&V, launch criteria, post-launch metrics, non-goals, risks, calendar, governance.
- 17 numbered sections, 4000+ words.
- A frozen scope that all downstream Phase 6 loops resolve against.

## What comes next

- **L272** — ADRs for the eleven architectural decisions referenced throughout this PRD.
- **L273** — V&V matrix that operationalizes Section 11.
- **L274** — KPI dashboard that operationalizes Section 13.
- **L281** — kanban that decomposes Sections 5 + 12 into shippable issues.

## Related

- [[L001-vision-statement]] — the thesis this PRD operationalizes
- [[L002-competitive-landscape]] — the cartel the PRD is written against
- [[L003-personas]] / [[L004-jtbd-map]] — the humans the PRD serves
- [[L006-pricing-thesis]] / [[L007-distribution-thesis]] / [[L008-differentiation]] — strategic framing the PRD encodes
- [[L010-five-year-arc]] — the arc this PRD is the v1 seed of
- [[L121-information-architecture]] through [[L180]] — Phase 3 design artifacts referenced by section 5
- [[L181-forecast-object-schema]] through [[L230]] — Phase 4 forecasting mechanics referenced by section 6
- [[L231-nextjs-scaffold]] / [[L260-pricing-checkout]] — Phase 5 prototype artifacts the PRD ships
- [[L300-final-synthesis]] — the closing loop that re-reads this PRD against five years of actuals
