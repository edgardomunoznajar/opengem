# L277 — Launch Plan: ProductHunt + HN + r/datasets + r/macroeconomics + econtwitter + Substack networks

**Loop**: 277 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis of this loop

The launch is not a single event. It is a six-week cadence that hits seven channels in deliberate sequence, with each channel chosen for the *cohort* it brings, not the volume it produces. The default founder instinct ("post to HN on Tuesday, blast Twitter, hope for the best") burns the launch on a single audience and leaves the credibility cohort untapped. This loop reverses the priority: warm-introduce to the credibility cohort first (econtwitter, academic Substacks, r/macroeconomics), then broaden to the volume cohort (HN, ProductHunt, broader Reddit, broader Twitter), then sustain through the long-arc channels (SEO, RSS, Substack mirror).

The launch story is *not* "we built a thing." The launch story is "we built the thing the cartel will not." Every launch post leads with the five promises from [[L008]] and the accountability ledger from [[L285]] — not with feature lists. The asymmetry is the headline.

---

## The six-week cadence

| Week | Channel sequence | Audience |
|---|---|---|
| W-2 | Soft-pre-launch warm intros | 20 named recipients across credibility cohort |
| W-1 | First public Substack mirror post + RSS go-live | Existing macro-RSS subscriber base |
| W 0 (launch) | econtwitter thread + Show HN + ProductHunt + r/macroeconomics + r/Economics | Volume cohort + LP cohort |
| W+1 | Academic Substacks (Joey Politano, Skanda Amarnath, Brad DeLong, Adam Tooze) | Credibility cohort tail |
| W+2 | YouTube embed campaign — first chart-of-the-week | YouTube volume cohort |
| W+3 | r/datasets + dev-tutorial Medium + Dev.to | Developer / data cohort |
| W+4 | First failure-log post-mortem (deliberately) | All cohorts; press attention |
| W+6 | First quarterly retrospective publication | All cohorts; KPI commitment |

---

## Channel-by-channel tactics

### W-2 — Soft pre-launch warm intros (20 recipients)

The single highest-ROI thing we do all year. Personal emails to 20 named recipients across the credibility cohort:

- 5 academic macroeconomists with active Twitter (Olivier Blanchard's signal-boost network)
- 3 macro Substack writers (Joey Politano / Skanda Amarnath tier)
- 3 economist journalists (Soumaya Keynes / Adam Tooze / Mike Bird / Greg Ip tier)
- 3 IMF / OECD / BIS researchers who might cite us
- 3 macro YouTubers (Damian-class)
- 3 NGO/think-tank data leads (CGD, World Bank, OECD-adjacent)

Each email is 6 sentences:

```
Subject: An open macro dashboard that publishes its own track record — would love your eyes on it

Hi [Name],

We built OPENGEM — a public dashboard for the world economy where every
forecast is open, every miss is named, and every methodology is published.
Think Bloomberg-grade visuals, but the entire track record is on the
homepage instead of behind a paywall.

Public launch is [date]. Before then, we'd love to show you the [their
adjacent thing] page (we cite/built-on [their work / area]) and the
accountability ledger. If anything is wrong, telling us this week is
infinitely more useful than telling us after launch.

Coffee or 15min screenshare? No ask attached.

[Founder]
opengem.com/preview · access code [code]
```

Of 20 emails, expect: ~12 replies, ~7 calls or screen-shares, ~3 unprompted launch-day signal-boost mentions. That's the launch's most important conversion. The credibility cohort builds the brand on day one.

### W-1 — Substack mirror go-live + first post

The Substack at `opengem.substack.com` (per [[L007]] tactic) goes live one week before public launch with a single post: *"What is OPENGEM, and why does it publish its own track record?"* The post leads with the five promises, the accountability ledger preview, and a single chart with vintage-stamped lineage.

The Substack hits Substack's discovery engine before any other channel — its position in "macro" recommendations on launch day is determined by pre-launch subscriber count + engagement. We use the W-2 warm-intro list to subscribe and amplify.

Cross-post the same content as a personal Substack on Joey Politano-style if any of the 20 W-2 recipients agrees. (Don't ask twice. One ask is the cost of an intro; two is a transactional relationship that contaminates the brand.)

### W 0 — Launch day sequence (8am Pacific, Tuesday)

The actual public launch hits four surfaces simultaneously. Each is pre-drafted, scheduled, and rehearsed.

**econtwitter thread (8:00 am Pacific).** Founder account posts a 12-tweet thread:

```
1/ I built a public dashboard for the world economy where every forecast is
open, every miss is named, and every methodology is published. It's free.
opengem.com

2/ The forecasting cartel — Bloomberg Economics, IMF WEO, OECD EO — produces
priced forecasts whose track records are private. Their margins depend on
that opacity.

3/ OPENGEM has no margins to protect. So every forecast we have ever made
is on /accountability with the date we made it, the model that made it, and
the score we earned. [screenshot]

4-10/ [Show one chart per tweet: home pulse, country page, scenario page,
forecast detail, leaderboard, accountability, MCP demo.]

11/ Apache-2.0 code. CC-BY-4.0 data. RSS, JSON, embed, MCP server. Nothing is
gated. Paid tier is for velocity and fit, never substance. [pricing screenshot]

12/ If this is useful to your work, please share. If it's wrong, please tell
us — every error reported in the first 30 days gets named in our launch
retrospective.
```

Reply to the first 50 quote-tweets within 90 minutes. Pin the thread.

**Show HN (8:30 am Pacific, 30 min after econtwitter).** Pre-drafted post:

```
Show HN: OPENGEM — a Bloomberg-grade macro dashboard that publishes its own track record

I've spent the last [N] months building an open public dashboard for the world
economy. The thesis: the forecasting cartel's moat is opacity, so an
open-source dashboard that publishes its own miss log and methodology
becomes structurally credible in a way the incumbents cannot copy.

The stack: Next.js + Tailwind + Lightweight Charts on Cloudflare Pages,
FastAPI + Nixtla + statsmodels on Cloud Run, MCP server for LLM grounding,
Datasette for raw data, GitHub for the accountability ledger.

What's specifically asked-for: feedback on the methodology pages, the
accountability ledger UX, the MCP tool surface, and the embed widget. The
pricing is at /pricing and the never-charge-for-X commitment is on the page.

Apache-2.0 code, CC-BY-4.0 data. Free tier is the whole product.

opengem.com
github.com/opengem/opengem-1
```

Founder is at keyboard from 8:30 am to 12:30 pm Pacific to respond to every comment within ~20 minutes. The HN audience cares about *engagement quality* in the first four hours; presence is the conversion lever.

**ProductHunt launch (12:01 am Pacific, same Tuesday).** ProductHunt's 24-hour cycle starts at midnight Pacific. The launch is queued with hunter outreach two weeks prior. Asset bundle: 3 GIFs, 6 PNG screenshots, 1 logo, 1 hero image, 1 demo video (60s edit of the L279 90s script).

Tagline: *"The macro dashboard that publishes its own track record."*
Description: leads with the five promises, links to /accountability, links to /pricing.
First comment by founder: same as Show HN, lightly adapted.

**r/macroeconomics + r/Economics + r/datasets (8:45 am Pacific, 45 min after HN).** Three separate posts, each phrased for the subreddit's voice. Lead with the methodology page and the accountability ledger; never with the price page. Founder does *not* post; instead, ask one or two early-supporters from the W-2 warm-intro list to post organically. Self-promo via founder triggers downvote brigades; community-organic post earns karma.

### W+1 — Academic Substack outreach (post-launch credibility consolidation)

Now that the launch hit and there's some social proof to point at, reach out to academic Substackers individually:

- Joey Politano (Apricitas Economics) — invite to a guest post + co-byline on a "what's the future of open macro forecasting" piece.
- Skanda Amarnath (Employ America) — invite to ground his next labor-market piece in OPENGEM data with attribution.
- Brad DeLong — pure citation request; he's high-volume and citation-friendly.
- Adam Tooze (Chartbook) — long-shot but high-impact; pitch a co-branded chart-of-the-week.

Of four invitations, expect: 2 responses, 1 published collaboration within 30 days, 0 outright rejections (academic Substackers generally engage with open-data projects).

### W+2 — YouTube chart-of-the-week launch

The 10-YouTuber partnership program from [[L007]] tactic 3.1 launches the second week post-launch. Each participating channel (5-50k subs) gets:

- Free Studio-tier credit for 12 months
- An OPENGEM-branded chart template (matches the L145 broadcast theme)
- Editorial credit on the OPENGEM blog
- Co-branded "OPENGEM × [Channel]" landing page

In exchange: commit to use OPENGEM charts in at least one video per week with on-screen attribution + a clear shoutout. Total exchange value to OPENGEM: ~50-200k cumulative YouTube impressions per week within the first month.

### W+3 — r/datasets + dev tutorials

Two complementary moves:

1. **r/datasets post**: "OPENGEM — open vintage-correct macro data with provenance lineage." Submitted by a community member from the W-2 list, not founder. Reddit norms reward humility; the post leads with the data layer (Datasette at `data.opengem.com`) and the API spec, not the dashboard.

2. **Three dev tutorials**:
   - Medium: "Grounding Claude / ChatGPT in real macro data with the OPENGEM MCP server"
   - Dev.to: "Building an open macro dashboard with Next.js 15, Lightweight Charts, and Cloudflare Pages"
   - Substack: "Why we publish every forecast we ever made"

The Medium tutorial cross-posts to Anthropic's developer blog (we pitch it pre-launch); the Dev.to tutorial cross-posts to Cloudflare's developer blog; the Substack post is the OPENGEM mirror.

### W+4 — The first failure-log post-mortem (deliberately)

This is the most counterintuitive move in the launch plan. Within 30 days of launch, OPENGEM *publishes* a post-mortem on a real forecast miss. The miss is chosen deliberately:

- Small enough to be a learning moment, not a credibility catastrophe.
- Large enough that the post-mortem is genuinely instructive.
- A miss that *consensus also got wrong*, so the post-mortem can honestly say "we missed, and so did consensus, but here's why we missed."

The post is announced on Twitter, Substack, and HN ("Show HN: our first published forecast miss, with the post-mortem"). This is brand-positive in a way no competitor can copy. It is *the* launch move that the cartel cannot replicate. It is what the launch is *for*.

### W+6 — First quarterly retrospective

Six weeks post-launch, we publish the first `/retrospective/Q3-2026` page (template per [[L299]]). It includes:

- KPI-1 (`/accountability` views): the actual number, no rounding.
- KPI-2 through 8: the actuals.
- What we got right; what we got wrong.
- What we'll change for Q4.

This is published on the public retrospective page *and* announced on Twitter / Substack / HN. The launch story is now five rounds deep: warm intros → public launch → academic ratification → YouTube distribution → developer tutorials → published miss → quarterly retrospective. Each round is a credibility deposit.

---

## What we deliberately *don't* do at launch

- **No paid ads.** Google Ads, Twitter Ads, LinkedIn Ads — none at launch. The brand is "credibility-by-being-open," which paid amplification dilutes.
- **No press release.** Press picks up real stories, not press releases. We seed via the warm-intro list to journalists (Marcus persona) and let coverage emerge organically over Y1.
- **No "we raised $X" announcement.** OPENGEM is bootstrapped; even if it weren't, leading with funding would re-anchor the brand in startup-narrative, not credibility-narrative.
- **No HackerNews repost after 48 hours.** One Show HN, then never again until v2.

---

## Launch-day operations runbook

08:00 PT — founder posts econtwitter thread; primary monitoring begins
08:15 PT — auto-tweet from `@opengemcharts` bot of the day's most-anomalous chart
08:30 PT — founder posts Show HN; founder is at keyboard
08:45 PT — community member posts r/macroeconomics + r/Economics
09:00 PT — Substack mirror auto-publishes "Why we launched today" post
09:30 PT — community member posts r/datasets
10:00 PT — first response wave (HN should be at 50-100 points by now if all goes well)
12:00 PT — lunch break (founder); secondary monitor takes over
13:00 PT — founder back; respond to every comment that's accumulated
17:00 PT — debrief; collect feedback themes; queue first patches for tomorrow
20:00 PT — founder publishes "what we learned on day one" Twitter thread
24:00 PT — ProductHunt 24h cycle ends; final scoring

Backup: founder + one trusted collaborator on shared Slack throughout. Server uptime monitored every 5min. Cloudflare cache warmed in advance.

---

## What this loop produced

- A six-week launch cadence (W-2 through W+6) with seven distinct channels.
- Per-channel tactics: warm intros (20 recipients), Substack go-live, econtwitter thread, Show HN, ProductHunt, r/macroeconomics, r/datasets, YouTube partnerships, dev tutorials, deliberate first miss post-mortem, first quarterly retrospective.
- Launch-day hour-by-hour operations runbook.
- A list of moves explicitly *not* taken (no paid ads, no press release, no funding announcement, no HN repost).

## What comes next

- **L278** — press kit + screenshots referenced in PH + Show HN launches.
- **L279** — demo video script used in PH + Substack go-live.
- **L280** — Discord charter live before launch as the community-conversion surface.
- **L298** — post-mortem template that the W+4 deliberate-miss publication follows.

## Related

- [[L007-distribution-thesis]] — the nine channels this loop sequences for launch
- [[L008-differentiation]] — the five promises every launch post leads with
- [[L274-kpi-dashboard-meta]] — KPI-1 measurement begins at W 0
- [[L285-accountability-ledger]] — the page the W+4 deliberate-miss publishes into
- [[L299-quarterly-retrospective]] — the W+6 publication template
