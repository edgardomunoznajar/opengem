# L007 — Distribution Thesis

**Loop**: 007 / 300
**Phase**: 0 — Strategic framing
**Date**: 2026-06-06

---

## The thesis of this loop

Distribution decides whether OPENGEM wins. Product quality is necessary; channel-strategy is sufficient. The mistake to avoid is the "build it and they will come" trap that kills 99% of open-source dashboards — the world is littered with technically-excellent macro tools that nobody uses because the maker never built the channel strategy alongside the product.

The three cohorts from L001 have *different* high-ROI channels. The volume cohort (Damian, Greg) is best reached via creator-platform amplification (YouTube, Substack, Twitter). The credibility cohort (Marcus, Lin, Priya) is reached via citation surfaces (academic, journalistic). The forecast-LP cohort (Nadia) is reached via word-of-mouth + content marketing + warm intros, not any cold channel.

Nine channels are ranked below by ROI per cohort. Each gets three concrete tactics. The recommendations cut against the default "Twitter and HackerNews" instinct — the actual highest-ROI moves are weirder and slower.

---

## The nine channels

### 1. SEO (search)

**ROI rank: Volume cohort #2, Credibility cohort #1, LP cohort #4.**

Why it works: macro queries are *long-tail intent-rich*. Someone Googling "India CPI YoY 2026 consensus" has demonstrated buying intent for exactly the chart OPENGEM serves. TradingEconomics has dominated this surface for a decade by brute-forcing the country×indicator matrix. We follow their playbook with provenance as the differentiator.

**Three tactics.**
1. **Matrix-fill discipline from week one.** Every country × indicator page must exist and rank within 30 days of launch. Auto-generated pages with structured JSON-LD, canonical URLs, internal cross-linking, sparkline previews. ~200 countries × ~50 core indicators = 10,000 pages launched simultaneously.
2. **Schema.org + JSON-LD on every page.** The page header includes `Dataset`, `Observation`, `StatisticalPopulation`, `Article` markup with vintage timestamps and citations. Google's rich-result eligibility for datasets and the experimental "dataset answer" cards become near-automatic.
3. **The forecast-revision blog engine.** Once a week, a static-generated post for each significantly-revised forecast: "Our [country] [indicator] forecast was revised from X to Y on [date] because [reason]." Two years of weekly posts = ~5,000 highly-cited revision posts that compound search authority.

---

### 2. RSS / Atom feeds

**ROI rank: Volume cohort #5, Credibility cohort #2, LP cohort #6.**

Why it works: serious macro-readers (the Lin-Priya-Marcus axis) live in Feedly / NetNewsWire / their own RSS-to-Slack pipelines. RSS gets *zero* attention as a distribution channel because it's unfashionable, which is exactly why the surface is uncluttered and the ROI is high. The OPENGEM-curious Lin would happily subscribe to "weekly Zambia debt-sustainability digest" if it existed.

**Three tactics.**
1. **A feed per slice that matters.** Per-country feeds, per-indicator feeds, per-forecast-pack feeds, per-scenario-pack feeds, "all forecast revisions" feed, "all failure-log posts" feed. Total ~3,000 feeds launched at v1, each with a stable URL.
2. **Each item carries the full payload.** RSS items include the chart as a hosted PNG, the JSON-block, the cite-this-view URL, the source citation. A reader can paste an item into a memo without leaving the feed reader.
3. **A Substack-friendly digest feed.** Curated daily digest "Today's OPENGEM" that's specifically formatted for Substackers to repost / quote / link. Sub-bullet: build a Buttondown / Beehiiv newsletter mirror so non-RSS-natives can subscribe by email.

---

### 3. YouTube embed

**ROI rank: Volume cohort #1, Credibility cohort #6, LP cohort #7.**

Why it works: Damian and his 47k subscribers are the prototype. Every macro YouTuber needs charts. A clean OPENGEM chart with a recognizable visual identity, embedded as a thumbnail-friendly PNG with a clear "opengem.com" watermark, becomes *free marketing* in every video that uses it. The viewer who Googles "where did Damian's chart come from" lands on OPENGEM.

**Three tactics.**
1. **The "chart of the week" partnership program.** 10 mid-tier macro YouTubers (5-50k subs each) get an early-access dashboard, an editorial credit on the OPENGEM blog, and a custom OPENGEM-branded chart template. In exchange they commit to use OPENGEM charts in at least one video per week with on-screen attribution.
2. **PNG-export with cinema-grade visual design.** Damian's pain is "the chart looks retail." Solve it: OPENGEM PNG exports look like Bloomberg, with three preset themes (terminal, editorial, broadcast). Watermark is in the corner, visible enough to drive search-traffic, subtle enough that Damian doesn't strip it.
3. **A "data source" page optimized for video descriptions.** Damian pastes `opengem.com/c/us/cpi?v=2026-06` into his description and the page lands on a clean static page with the chart, the methodology, the citation. The view-counter is visible (social-proof) and a "subscribe to this chart's RSS" button is one click.

---

### 4. Substack syndication

**ROI rank: Volume cohort #3, Credibility cohort #4, LP cohort #5.**

Why it works: Substack writers are an unusual hybrid — they have audiences (volume cohort), they have credibility, and they have economic incentive to source good charts (their paid subscribers will churn if posts are sloppy). They're also the *easiest* persona to convert because pasting an OPENGEM embed into a Substack post takes one click and improves the post immediately.

**Three tactics.**
1. **Embed iframe that handles Substack's CSP perfectly.** Substack is finicky with iframes; OPENGEM ships an embed that uses a Substack-compatible URL format and falls back gracefully to a static PNG with a citation link if iframe is blocked. Same embed works on Beehiiv, Ghost, WordPress, Medium.
2. **A "Substack starter pack" landing page.** Targeted at the 200 macro-adjacent Substacks (Joey Politano, Skanda Amarnath, Brad DeLong, Adam Tooze, Heather Cox Richardson when she touches econ, etc.) with a tutorial, three template posts, and an offer of free Studio-tier ($99/mo plan) for the first 100 Substacks that adopt OPENGEM embeds.
3. **Reverse-syndication of OPENGEM's own posts.** OPENGEM's weekly digest + failure-log posts publish *also* as a Substack at `opengem.substack.com`. Substack's discovery algorithm cross-recommends OPENGEM to readers of adjacent stacks.

---

### 5. MCP-as-distribution

**ROI rank: Volume cohort #6, Credibility cohort #5, LP cohort #2.**

Why it works: this is the *novel* channel and the one nobody else is exploiting. The MCP server makes OPENGEM available inside Claude, ChatGPT, Gemini, Mistral, every LLM. Every time a user asks an LLM "what's the consensus for German GDP growth," the LLM can call OPENGEM, get the answer with provenance, and cite OPENGEM in the reply. This is *passive distribution at LLM scale*.

**Three tactics.**
1. **Submit OPENGEM MCP to every major LLM's marketplace.** Anthropic's MCP gallery, OpenAI's GPT marketplace, Google's Gemini Extensions, Mistral's Le Chat directory. All free MCP tier. The submission process becomes a recurring channel-maintenance ritual.
2. **Auto-attribution in every MCP response.** OPENGEM's MCP tools always return responses that include a `source_url` field pointing back to the cite-this-view URL. LLMs that respect source attribution (which most do for grounded answers) will surface "according to OPENGEM" in the chat — driving brand awareness through every chat session.
3. **The MCP-tutorial content engine.** "How to ground your Claude chats in real macro data with OPENGEM" tutorial posts on Medium, Dev.to, Anthropic's developer-blog cross-post. Every LLM-developer tutorial is a long-tail traffic source for the next 5 years.

---

### 6. Twitter / X cards

**ROI rank: Volume cohort #4, Credibility cohort #3, LP cohort #3.**

Why it works: macro Twitter is a small, very influential community. ~500 accounts drive the entire macro-conversation; if 30 of them adopt OPENGEM charts in their threads, the dashboard becomes "the macro chart provider" in roughly six months. The trick is making OPENGEM charts irresistible to *paste*.

**Three tactics.**
1. **Twitter-card meta tags optimized for chart unfurls.** Every OPENGEM URL unfurls to a high-resolution chart-image preview with the title, subtitle, and provenance line baked into the image. Posting an OPENGEM URL produces a *better* visual than uploading a chart screenshot directly — that's the conversion trigger.
2. **The "@OPENGEMcharts" daily auto-poster.** A bot account that posts the day's three most-anomalous indicator moves with charts and links. Build an audience of 5k followers in 6 months by being consistently useful in the macro feed. Cross-post to Bluesky.
3. **The macro-Twitter influencer kit.** Direct-message 50 named macro accounts with a personalized embed, a thank-you letter for past good work, and a free Studio-tier credit. ~20% conversion = 10 high-quality adopters = 50,000+ impressions per OPENGEM chart shared.

---

### 7. Reddit

**ROI rank: Volume cohort #7, Credibility cohort #7, LP cohort #8.**

Why it works: r/Economics (3M+ subscribers), r/AskEconomics (200k), r/EconMonitor (50k), r/macroeconomics (50k), r/finance, r/CredibleDefense (for geopolitics), r/geopolitics (300k). These communities have specific norms — citation-heavy, no self-promotion — that OPENGEM's positioning is uniquely well-suited to navigate. A user posting "here's the OPENGEM chart with the vintage-stamped provenance link" earns karma rather than getting downvoted.

**Three tactics.**
1. **A reddit-friendly chart URL format.** OPENGEM URLs unfurl in Reddit's chart preview, the linked page is mobile-friendly, the citation link is at top-of-page. No paywalled-content surprises.
2. **Recurring weekly threads.** r/Economics already runs "Indicator Wednesday" style threads; OPENGEM moderators contribute curated chart-of-the-week posts. Build community goodwill before any promotional move.
3. **Avoid the self-promo trap.** Hard rule: OPENGEM team members never post their own product to a subreddit. We make the product good enough that users post it themselves. We seed by giving 20 mid-tier macro-redditors free Studio tier and a thank-you for past contributions.

---

### 8. HackerNews

**ROI rank: Volume cohort #8, Credibility cohort #8, LP cohort #9.**

Why it works: less than commonly assumed. HN is a *one-time launch surface*, not a sustained distribution channel. A successful Show HN drives 30k-100k visitors over 48 hours, of which maybe 1% are real users a week later. The value is the *launch credibility* and the secondary effect on SEO (HN backlinks are high-quality).

**Three tactics.**
1. **A Show HN at v1 launch.** Title: "OPENGEM — a Bloomberg-grade macro dashboard that publishes its own track record." Pre-draft the post. Time the launch for a Tuesday-Thursday 8-10am Pacific. Have founder-account ready to respond to top comments within 30 minutes.
2. **A second "Ask HN" after 3 months.** "Ask HN: what macro indicators would you want OPENGEM to add?" Drives a second wave of attention and demonstrates community-listening.
3. **Avoid HN as a sustained channel.** No reposts, no spam, no "Show HN" for every minor feature. HN is a launch event and a backlink, not a campaign.

---

### 9. Discord

**ROI rank: Volume cohort #9, Credibility cohort #9, LP cohort #10.**

Why it works: a small, dedicated power-user community matters more than a wide casual audience. The 300 most-engaged OPENGEM users in a Discord become the QA team, the feature-request engine, and the first paid customers. The community-management overhead is the constraint.

**Three tactics.**
1. **A read-mostly Discord with a #releases channel.** Auto-posts on forecast revisions, failure-log posts, new features. Low maintenance. Members can discuss in threads.
2. **A monthly "office hours" voice channel.** Founder + early adopters in a 90-minute voice session, discussing methodology, taking feature requests. Recorded and posted as a YouTube backlink — double-duty distribution.
3. **Discord as the path to white-label conversion.** Discord power-users self-identify as institutional buyers; sales conversations happen in DM with low ceremony. Discord is the *closed-loop conversion funnel* for the $5k+/month tiers.

---

## Ranked channel ROI by cohort (the matrix)

Each cell: estimated 18-month ROI per dollar of effort, rank 1-9 (1 = highest ROI).

| Channel | Volume cohort (Damian, Greg) | Credibility cohort (Marcus, Lin, Priya) | LP cohort (Nadia, Newsroom, Institutional) |
|---|---|---|---|
| SEO | 2 | 1 | 4 |
| RSS | 5 | 2 | 6 |
| YouTube embed | 1 | 6 | 7 |
| Substack syndication | 3 | 4 | 5 |
| MCP-as-distribution | 6 | 5 | 2 |
| Twitter / X cards | 4 | 3 | 3 |
| Reddit | 7 | 7 | 8 |
| HackerNews | 8 | 8 | 9 |
| Discord | 9 | 9 | 10 (community → DM sales) |

### What the matrix reveals

- **The volume cohort is won via YouTube, SEO, Substack, Twitter.** These are the channels that drive top-of-funnel.
- **The credibility cohort is won via SEO, RSS, Twitter, Substack.** RSS punches above its weight because serious researchers actually use it.
- **The LP cohort is won via MCP, Twitter, SEO, with conversion through Discord/email.** They don't come from cold channels; they come from being seen *adjacent to* warm signals.
- **HackerNews and Discord are launch-event and community-management, not sustained-acquisition.**

The high-ROI consensus channels (top 3 across cohorts): **SEO + Twitter + Substack + RSS + YouTube embed.** Five channels carry the load. The other four are second-tier and tactical.

---

## What this loop produced

- Nine distribution channels ranked by ROI per cohort, with three concrete tactics each.
- A 9 × 3 matrix mapping channels to cohorts.
- A concentration finding: SEO + Substack + RSS + YouTube + Twitter covers the load.
- A counterintuitive: HackerNews is a launch event, not a sustained channel; RSS and YouTube embeds are *higher* ROI than the default-instinct channels.

## What comes next

- **L107** (Phase 2) — JSON-LD + schema.org for SEO operationalization.
- **L111** (Phase 2) — Embeddable widgets design.
- **L112** (Phase 2) — Substack integration deep-dive.
- **L177** (Phase 3) — MCP-server install page.
- **L295-L297** (Phase 6) — YouTube + SEO + Substack engine plans, scaled.

## Related

- [[L001-vision-statement]] — three-cohort thesis the channel matrix decomposes
- [[L002-competitive-landscape]] — TradingEconomics's SEO lesson informs the matrix-fill discipline
- [[L005-north-star-metric]] — VC/w benefits most from RSS, Substack, and embed channels
- [[L006-pricing-thesis]] — Studio / Newsroom / Institutional tiers map to the channel mix
