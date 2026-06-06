# L010 — 5-Year Arc Compressed

**Loop**: 010 / 300
**Phase**: 0 — Strategic framing
**Date**: 2026-06-06

---

## The thesis of this loop

A five-year arc has to be specific enough to be falsifiable and ambitious enough to be motivating. The temptation to write "and then revenue grows" or "and then we scale" produces unfalsifiable planning prose. This loop instead names, at each milestone:

- **Concrete features** that ship at that milestone (testable: did they ship or not?)
- **Concrete trust/credibility milestones** (testable: did the named external trust event happen?)
- **Concrete revenue milestones** (testable: did ARR cross the threshold?)

Five milestones: Y0 (launch), Y1 (consolidation), Y2 (institutional adoption), Y3 (incumbent peer), Y5 (citation-of-record). The arc compresses the L271 "World Dashboard PRD" and the L300 "OPENGEM v1 → v2 → v5" synthesis into a single forward-looking statement that the team can re-read every quarter.

The arc is opinionated. It commits to specific bets: the white-label tier crosses revenue at Y2; the MCP vendor tier lands by Y3; the press-citation moment happens by Y3 not later; the academic citation moment happens by Y5 because PhD pipelines are slow.

---

## Y0 — Launch (Q3 2026)

### Features that ship

- Public dashboard at `opengem.com`: country pages for all G20 + EU + ASEAN + key EM (40 countries minimum), with the five core indicators (CPI, GDP, Unemployment, Policy Rate, Current Account) on each, with forecast bands and consensus overlays.
- Indicator pages for the 20 most-trafficked macro series (US CPI, US NFP, US GDP, EZ HICP, JP CPI, CN CPI, IN CPI, BR CPI, etc.), each with cross-country comparison.
- Forecast page per country × indicator × horizon (nowcast / 1Q / 4Q / 2Y), with vintage history visible.
- Track-record open ledger page with the first six months of forecast accuracy data.
- Failure-log page (empty at launch, but live, with the schema).
- Five-promises page and refusal-scope page (L008, L009).
- Public API (1k req/day free), public MCP server (100 invocations/day free), RSS feeds (~500 at launch covering countries + indicators + scenarios), embeddable iframe widgets, JSON / CSV / SVG / PNG export on every chart.
- Methodology pop-up on every chart with model card links.
- Cite-this-view URL system with permanent identifiers.

### Trust / credibility milestones

- One non-Edgardo human (Damian, the YouTuber friend from L003) uses the dashboard daily and pastes its JSON into their workflow at least 5x in 30 days. (This is the L001 30-day test.)
- A Show HN at launch produces a top-5-position story for at least 4 hours.
- One academic econ Twitter account with >5k followers shares an OPENGEM chart unprompted within the first 60 days.
- The five-promises page is linked from at least 3 external blogs/Substacks within the first 90 days.

### Revenue milestones

- **Target: $0 ARR.** The launch tier is free-only. The Stripe + magic-link checkout is built but the paid tiers are not actively marketed. Revenue is a Y1 metric; Y0 is about velocity-of-build and trust-of-launch.
- We deliberately do not gate any paid tier in Y0. The price page exists, the tiers are described, but the team's energy is 100% on the free product and the launch story.

---

## Y1 — Consolidation (Q3 2027)

### Features that ship

- Country coverage expanded to 100+ countries; indicator coverage expanded to 30 core series per country plus ~80 deeper series for the G20.
- Vintage time machine UI ("rewind to Sept 2024 and see what we predicted") shipped and stable.
- Forecast leaderboard page comparing OPENGEM's nowcasts against WEO, OECD EO, Bloomberg Economics (where their public numbers are available), and consensus polls (Reuters poll, Bloomberg poll, FocusEconomics) — with sortable accuracy stats.
- First post-mortem in the failure log: a *named* miss with a public ex-post analysis. (The team will deliberately surface and post a meaningful miss in the first 18 months; this is brand-positive, not brand-negative, by Promise 2.)
- Geopolitical pulse map (GDELT-driven) shipped.
- Supply-chain pulse map (PortWatch + GSCPI) shipped.
- The first 5 white-label / Studio customers go live ("powered by OPENGEM" pages on real third-party domains).
- Compare-2 view (any two countries / indicators / scenarios side-by-side).
- Watchlist + alerts (saved user views with email/webhook notification on threshold crossings).
- Newsletter / Substack mirror at `opengem.substack.com` running weekly.
- Hosted MCP server with 10x throughput at the paid Studio tier.

### Trust / credibility milestones

- 100+ weekly active humans on the public dashboard (the L001 12-month test).
- 1 academic citation of OPENGEM in a working paper (SSRN / NBER / CEPR), with the OPENGEM team aware and able to point to it. (The L001 12-month test.)
- 1 press citation of OPENGEM in a top-tier outlet (FT, Reuters, Bloomberg article, Economist online, NYT business). The mention need not be the lead — even a footnote-tier cite counts as the Y1 marker.
- The first failure-log post-mortem is published and read by external commentary (a Substack writes about it, or an econ Twitter thread cites it as "this is what publishing-your-mistakes looks like in practice").

### Revenue milestones

- **Target: $100k ARR.**
- ~25 Studio customers × $99/mo × 12 = ~$30k ARR.
- ~10 Newsroom customers × $499/mo × 12 = ~$60k ARR.
- ~1 Institutional customer × $4,999/mo × 12 = ~$60k ARR.
- Rough mix; total ~$100-150k ARR. Single-founder operability still holds. CAC is ~zero because all conversion is via free tier.

---

## Y2 — Institutional adoption (Q3 2028)

### Features that ship

- Scenario pages with probability-weighted multi-path forecasts (recession, stagflation, hard-landing, soft-landing, geopolitical-shock packs).
- Counterfactual scenarios: "what if [sanctions hit / oil shock / specific geopolitical event] happened tomorrow." Pre-built scenario library with ~50 named packs.
- Forecast-revisions log with cross-vintage diff visualizations.
- Methodology pages with full model cards, downloadable parameters, replication code links.
- Notebook export ("open this view in Jupyter") with a one-click GitHub Codespace.
- Cite-this-view URLs now resolve as DataCite-style citable identifiers; academic users can paste OPENGEM citations into bibliographies and Zotero handles them correctly.
- Custom-domain Institutional white-label tier in active use by at least 3 named NGOs / think tanks (e.g. a `macro.cgd.org`-style integration with at least one CGD-class institution).
- Mobile PWA, accessible everywhere users open the public dashboard.
- Multi-language support (English first; Spanish, Portuguese, French, German added by end-of-Y2).
- The forecast-vendor tier is open and *empty*: published price, no LLM vendor has signed yet, but the framework is built.

### Trust / credibility milestones

- 1,000+ weekly active humans on the public dashboard.
- 10+ academic citations across published journal articles and working papers.
- 5+ press citations across top-tier outlets including at least one *FT macro column* mention.
- The forecast leaderboard is referenced in an external analyst comparison post (e.g., a Substack ranks OPENGEM vs Bloomberg Economics vs consensus and OPENGEM places competitively).
- The CGD-class NGO integration produces a published policy brief that visibly uses OPENGEM data as its empirical foundation.

### Revenue milestones

- **Target: $1M ARR.**
- ~150 Studio customers × $99/mo × 12 = ~$180k ARR.
- ~40 Newsroom customers × $499/mo × 12 = ~$240k ARR.
- ~10 Institutional customers × $4,999/mo × 12 = ~$600k ARR.
- Mix ~$1M ARR. Founder + 1 part-time engineer + 1 part-time content lead. Operating-cost line ~$200-300k → ~$700-800k net.

---

## Y3 — Incumbent peer (Q3 2029)

### Features that ship

- Coverage matrix is *complete* for the G20 + EU + ASEAN + key EM + Africa-50 (a ~120-country footprint). Every country × indicator × horizon cell is filled. This is the TradingEconomics-matrix-fill discipline at completion.
- A *consensus index* tile per country/indicator: "what do the 8 major forecasters collectively say, and where does OPENGEM differ." The page becomes a *meta-product* aggregating other forecasters.
- The forecast leaderboard is now *the* leaderboard cited by macro Twitter. When an analyst says "the OPENGEM nowcast has been more accurate than consensus for 6 quarters running for US CPI," that statement is checkable on the leaderboard page.
- The MCP server is the *built-in macro tool* in at least one LLM platform's marketplace (the Vendor tier converts: Anthropic, OpenAI, or Mistral signs).
- Embeddable widgets are used in 1,000+ external sites (counted via embed-iframe domain telemetry).
- The Track Record page now has 36+ months of OPENGEM forecast history with statistically meaningful samples for headline indicators.
- The Failure Log has ~20 named post-mortems, each one a brand-positive trust artifact.

### Trust / credibility milestones

- 10,000+ weekly active humans on the public dashboard.
- 50+ academic citations.
- 25+ press citations including at least 5 *front-page* or *column-anchor* mentions in top outlets.
- An IMF / OECD / central bank publication references OPENGEM as a comparison or external-validation reference. (The Y3 institutional-recognition moment.)
- Wikipedia uses OPENGEM as a citation in at least 50 macro-economic articles.
- A book published in 2028 or 2029 uses OPENGEM in its empirical chapter and credits the platform by name.

### Revenue milestones

- **Target: $4-5M ARR.**
- ~500 Studio × $99/mo = ~$600k.
- ~150 Newsroom × $499/mo = ~$900k.
- ~30 Institutional × $4,999/mo = ~$1.8M.
- 1 Vendor (LLM platform) at ~$1-2M depending on per-million-invocation pricing.
- Mix ~$4-5M ARR. Team grows to ~6-10 people including engineering, content, sales, ops. The single-founder phase ends; the team-building phase begins.

---

## Y5 — Citation-of-record (Q3 2031)

### Features that ship

- OPENGEM is structurally complete. The dashboard is operating as a *production* system, with focus shifting from feature-shipping to research depth, data partnerships, and methodology refinement. Phase 4 (forecasting product mechanics, L181-L230) is largely shipped.
- A *forecast model marketplace*: external researchers can submit forecast models that OPENGEM evaluates, leaderboards, and (if accepted) integrates into the production stack with attribution. Open-science-style contribution.
- The cite-this-view URL system is registered as a *DataCite member* with proper DOI-style citable identifiers. OPENGEM URLs are quotable as DOIs in academic style guides.
- The MCP server handles 100M+ tool invocations per month across 5+ LLM-vendor partners.
- The Failure Log is ~50+ named post-mortems and has become a *teaching resource* — cited in econometrics courses as a case study in forecast accountability.
- The Accountability Page is referenced in business-school curricula as a model of "open accountability infrastructure."

### Trust / credibility milestones

- 100,000+ weekly active humans on the public dashboard.
- 200+ academic citations including at least 20 in top-5 economics journals (AER, QJE, JPE, ReStud, Econometrica) or Macro top journals (AEJ:Macro, JME).
- 100+ press citations including regular mentions in *FT macro columns, NYT business, WSJ heard-on-the-street, Bloomberg View, Economist*.
- **The headline moment**: OPENGEM is referenced in a major press piece *next to* WEO and OECD EO as a third comparison benchmark. The phrasing is something like: "The IMF's October WEO projects 2.1% growth for India; the OECD's November update projects 2.4%; OPENGEM's open-vintage leaderboard projects 2.7% with a 90% interval of 2.2-3.1%." This is the L001 5-year test, met.
- A government-sponsored body (a national audit office, a parliamentary research service, an EU-level body) commissions a review of forecast institutions and includes OPENGEM as a peer to WEO / EO.
- A graduate course at an economics PhD program teaches "macro forecasting" using OPENGEM's open ledger as the primary data source.

### Revenue milestones

- **Target: $15-25M ARR.**
- Studio + Newsroom + Institutional tiers compound to ~$8-12M ARR.
- Vendor tier (LLM platform partners) compounds to ~$7-12M ARR.
- The asymmetry of the LLM-vendor tier shows: 3-5 vendor accounts at $2-4M each become the dominant revenue line.
- Team size ~25-40 people. Profitable. Sustainable. Independent (no need for VC bridge round; possibly a strategic round to accelerate Africa / South Asia coverage).

---

## The trajectory in one paragraph

OPENGEM launches in Q3 2026 as a public-only free dashboard with G20 + EU + ASEAN + key EM coverage, the five promises (L008), the refusal scope (L009), and the cite-this-view system. By end of Y1 it has 100+ weekly humans, one academic and one press citation, and ~$100-150k ARR from white-label tiers. By Y2 it has 1,000+ humans, 10 academic citations, 5 press citations, and $1M ARR with the first three institutional integrations live. By Y3 it has 10,000+ humans, 50 academic citations, 25 press citations, an IMF / OECD recognition event, and $4-5M ARR with the first LLM-vendor tier conversion. By Y5 it is referenced *next to* WEO and OECD EO in major press, taught in PhD programs, and operating at $15-25M ARR with sustained profitability — independent of VC funding, owned by the founding team and ESOP.

The product wins not by being faster than Bloomberg, not by having more data than Macrobond, not by having better narrative than Stratfor. It wins by being the *only* macro forecasting institution whose track record is publicly verifiable by anyone, in real time, with no payment required. Five years of compounded verifiable accuracy is impossible to dispute and impossible to copy. That is the moat. That is why the arc converges to "cited next to WEO."

---

## What this loop produced

- Five milestones (Y0, Y1, Y2, Y3, Y5) with concrete features, trust events, and ARR targets per milestone.
- A specific revenue mix at each year with named ARR contributions from each pricing tier.
- A "trajectory in one paragraph" compression suitable for a deck, a memo, or a Twitter thread.
- A concrete headline moment as the Y5 test: OPENGEM referenced next to WEO and OECD EO in major press.

## What comes next

- **L011** begins Phase 1 — the open-source landscape survey, starting with OpenBB Terminal deep-dive.
- The Y0 → Y1 transition is the most important: L011-L120 must produce the *technical substrate* for the Y0 launch.
- The arc above will be re-read at every quarterly retrospective (L299) and updated against actuals.

## Related

- [[L001-vision-statement]] — the original three-horizon test (30 days / 12 months / 5 years) sharpened here
- [[L005-north-star-metric]] — VC/w is the leading indicator that determines whether the arc holds
- [[L006-pricing-thesis]] — the pricing tiers whose revenue is named at each milestone
- [[L008-differentiation]] — the five promises whose compounded credibility produces the Y5 moment
- [[L009-anti-personas]] — the refusals that constrain the arc to a brand-coherent trajectory
- [[L271-master-prd]] — the Phase 6 PRD that operationalizes this arc into the v1 release
- [[L300-final-synthesis]] — the closing loop that audits this arc against 5 years of actuals
