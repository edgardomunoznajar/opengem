# L005 — North-Star Metric

**Loop**: 005 / 300
**Phase**: 0 — Strategic framing
**Date**: 2026-06-06

---

## The thesis of this loop

A north-star metric is the single number that, if it moves in the right direction over the right time horizon, *means the product is winning*. It is the metric the team optimizes when in doubt. It must be:

1. **Causal** — moving it should require building something users genuinely value, not gaming a counter.
2. **Forward-leading** — it should foreshadow revenue and growth, not lag them.
3. **Honest** — it should be easy to compute, hard to fake, and visible to the team daily.
4. **Specific to OPENGEM's positioning** — a generic SaaS metric (MAU, NPS) won't do; the metric must encode what makes OPENGEM *different* from incumbents.

Three candidates below. The recommendation arrives at the end.

---

## Candidate A — **Vintaged-forecast-views per day** (VFV/d)

**Definition.** The count of distinct page-views per day where (a) the user is viewing a forecast chart and (b) the page shows the forecast's vintage history (i.e. the user is engaging with the "this forecast was made on date X" provenance, not just glancing at the headline number).

**The argument for.** This metric directly encodes the OPENGEM thesis: *the value of a forecast comes from its vintage history, not its headline number.* If users are viewing forecasts *with provenance*, they are by definition engaging with the differentiator. Each VFV is a user-action that no incumbent can serve as cheaply (because no incumbent publishes its vintage history publicly).

**The argument against.** It's a *consumption* metric, not a *creation* metric. A VFV is what happens after OPENGEM has done its work; it does not capture whether the work was good. It also slightly overweights the public dashboard surface vs the API/MCP surface, where the same "vintaged forecast view" might happen invisibly inside an LLM context window without a page-view to count.

**Leading indicators if we picked this.**
- Forecast-page bounce rate (low bounce = users are actually reading the vintage history).
- Vintage-toggle clicks per page-view (users actively rewinding to older vintages).
- Share-button clicks on forecast pages (users distributing the provenance, not just the number).

---

## Candidate B — **Verified citations per week** (VC/w)

**Definition.** The count of citations per week, *originating outside OPENGEM*, that point to a permanent OPENGEM identifier (a cite-this-view URL, a forecast-version DOI, a vintage-stamped chart embed). Verified means: the citation resolves, the embed is rendered, the URL has been hit at least once from the citing surface (Substack, FT, working paper, NGO brief, Wikipedia, YouTube description, Reddit comment).

**The argument for.** This metric directly encodes *trust*. Trust is the thing OPENGEM's positioning is staked on, and trust is *only* measurable by whether other humans hand their reputation to OPENGEM by citing it. A citation is the unfakeable signal that a credibility-cohort user (Marcus, Lin, Priya) chose OPENGEM over Bloomberg / WEO / Macrobond as the source-of-record. Citations also have compounding effects: a citation in an FT piece drives traffic for a year; a citation in an academic paper drives traffic for a decade.

**The argument against.** Citations are *slow*. A working paper that cites OPENGEM might take 18 months between view and published-PDF. A North Star metric that takes 18 months to register changes is not a daily-team metric; it's a quarterly-board metric. We need a metric the team can move *this sprint*. Also, citations are hard to verify automatically; tracking inbound links and Substack embeds is mechanical, but counting academic citations requires Google Scholar scraping with substantial lag.

**Leading indicators if we picked this.**
- Cite-this-view button clicks per session.
- Embed-iframe load count from external referrers.
- Number of distinct external domains hitting the OPENGEM ledger per week.

---

## Candidate C — **MCP-tool-invocations per day** (MTI/d)

**Definition.** The count of unique MCP tool invocations per day from external clients (Claude, ChatGPT, Gemini, Mistral, local LLMs) calling OPENGEM's MCP server endpoints (get_country_indicator, get_forecast, get_vintage, get_scenario, etc).

**The argument for.** This is the *future-shaped* metric. LLMs are now the primary surface humans use to ask the world economy a question. If OPENGEM is the substrate LLMs route through for grounded macro answers, we win the entire stack without having to build a chat product. MCP invocations are the cleanest signal that LLMs are routing through us. And the unit economics are beautiful: each MTI is a tiny inference call that costs us microcents and benefits us by enrolling the calling LLM's user as an indirect OPENGEM consumer.

**The argument against.** It's an *infrastructure* metric, not a *value* metric. An MCP server can be hammered by a single client doing 1000 calls/minute for a single research session, and that would look like a north-star victory while serving exactly one human. The metric also encodes a bet that MCP wins as a protocol; if MCP fades or fragments (which is plausible at this date), the metric becomes a liability. And MCP traffic is *invisible to the public*: incumbents cannot see it, but neither can the OPENGEM community use it as a public trust signal.

**Leading indicators if we picked this.**
- Distinct upstream LLM clients per week.
- Distinct end-user (chat-id-hashed) MCP invocations per day.
- Conversion rate from MCP invocation → page-view of the underlying source.

---

## The recommendation

**Pick Candidate B — Verified Citations per week — as the north-star metric.**

Yes, even with the lag.

The reasoning:

1. **The thesis of OPENGEM is trust.** L001 commits to "a system that publishes its mistakes is harder to discredit than a system that hides them." The only measurable form of trust is *third-party attribution*. VC/w measures exactly this and nothing else does.

2. **The lag problem is solvable by decomposition.** VC/w is the headline metric; we don't measure it raw — we measure its *leading indicators*, which are visible weekly: cite-this-view clicks, embed iframe loads per external domain, count of distinct citing domains. These are real-time team-actionable metrics that compose into VC/w on a 60-90 day rolling basis.

3. **It survives the surface-fragmentation problem.** It does not matter whether the citation comes from a Substack embed, a YouTube description, a working paper bibliography, or an MCP-routed Claude conversation that links back to the source URL. Any path back to OPENGEM through a verifiable reference counts. So VC/w gracefully accommodates whatever surface dominates in 2027, 2028, 2029.

4. **It blocks the obvious gaming surface.** A team optimizing for VFV/d could chase clickbait charts; a team optimizing for MTI/d could chase API spam. A team optimizing for VC/w has to make charts/forecasts that *real publishers, with their own reputational risk, choose to attach themselves to*. There is no gameable shortcut. The only way to move VC/w is to be more trustworthy than alternatives.

5. **It rewards credibility-cohort behavior, which drives revenue.** The personas that cite OPENGEM (Marcus, Lin, Priya, Nadia in her memos) are precisely the personas whose institutions become paid customers in the white-label / API / MCP tiers. So VC/w is leading-indicator for revenue without being a vanity metric.

The other two candidates aren't bad — they are sub-metrics. VFV/d is the *consumption metric* and MTI/d is the *infrastructure metric*. We track both. We just don't optimize against them as primary.

---

## Leading indicators (the daily team-actionable proxies for VC/w)

The team will see the following five numbers on the team dashboard, refreshed daily, with weekly trend bars:

| # | Leading indicator | Why it leads VC/w | Target trajectory |
|---|---|---|---|
| 1 | **Cite-this-view clicks per session** | Direct intent to cite | >0.5% of sessions by Q1; >2% by Q4 |
| 2 | **Distinct embed-iframe domains per week** | Distinct publishers attaching to OPENGEM | 10 by Q1; 100 by Q4; 500 by Y2 |
| 3 | **Vintaged-forecast-page session depth** | Pro users engaging with provenance | >3 minute median by Q1 |
| 4 | **MCP tool invocations from distinct clients per week** | LLM-routed indirect citations | 100 by Q1; 10,000 by Y2 |
| 5 | **External backlinks to OPENGEM URLs (Ahrefs / Ahrefs-substitute)** | Manual citations not captured by embed loads | 100 by Q1; 1,000 by Y2 |

VC/w is the rollup metric reported quarterly. The five leaders are the daily metrics.

---

## Anti-pattern to watch

The team **must not** game VC/w by promoting OPENGEM citations into low-quality surfaces (link farms, sub-reddit spam, bot-Substacks). A "citation" from a content mill is technically a citation but corrodes the brand. The team should weight citations by the *credibility surface* they originate from:

- **Heavy weight (5x):** academic working papers (NBER, CEPR, SSRN, repec), major newspapers (FT, WSJ, NYT, Economist, Reuters wire), official-body briefings (IMF, OECD, World Bank, central banks), Wikipedia.
- **Medium weight (1x):** Substacks with >1k paid subscribers, YouTube channels with >50k subscribers, established economist Twitter, mid-tier financial press.
- **No weight:** link farms, low-quality blogs, anonymous Twitter, low-engagement Reddit threads, AI-generated content sites.

The metric is *credibility-weighted citations per week*, and the credibility-classification is published openly so the team can be held accountable for the weights it chose.

---

## What this loop produced

- Three candidate north-star metrics evaluated honestly with for/against.
- A pick: **Verified Citations per week** as the north-star, with five daily-actionable leading indicators.
- A credibility-weighting scheme to block the obvious gaming surface.
- The two other candidates retained as sub-metrics, not primary.

## What comes next

- **L006** translates the credibility-cohort framing into the pricing thesis.
- **L007** translates the embed-and-citation framing into the distribution thesis.
- **L271** (Phase 6 master PRD) re-encodes the leading-indicator dashboard.

## Related

- [[L001-vision-statement]] — the trust thesis VC/w directly measures
- [[L003-personas]] — the credibility-cohort personas whose behavior moves VC/w
- [[L004-jtbd-map]] — the cite-this-view primitive is one of the five core features
- [[L008-differentiation]] — the five promises that make a citation worth attaching to
