# L280 — Community Discord / Forum Charter

**Loop**: 280 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis of this loop

[[L007]] ranked Discord as a low-volume but high-engagement community channel — a *closed-loop conversion funnel* for the $5k+/month tiers. This loop writes the charter: rules, channels, moderation principles, and the single signature ritual that makes OPENGEM's Discord different from every other open-source-project Discord — the *publish-misses pinned post*. The Discord is brand-consistent: every member sees the accountability discipline mirrored in how the community itself is run.

Discord is the choice over Slack (no free indexable archive) and Matrix (smaller network effect). Discourse forum is a complement (long-form, threaded, search-indexable) but not the primary surface. Both go live at v1; Discourse is at `forum.opengem.com`, Discord is invite-link from the home page footer.

---

## Charter (the public-facing document)

```
# OPENGEM Community — Charter

Welcome. This is the community for people who use OPENGEM, build with it,
critique it, fork it, embed it, and occasionally point out where we got
something wrong. The charter below is short on purpose.

## What this community is

A place to:
- Ask questions about the dashboard, the data, the API, the MCP server.
- Suggest features, file bugs, propose new countries / indicators / scenarios.
- Discuss macro forecasting in good faith.
- Tell us when we missed (we will publish the miss; see below).
- Talk to other people who care about open public macro infrastructure.

## What this community is not

- A trading floor. We do not discuss intraday markets, day trades, or alpha
  signals.
- A political forum. We discuss policy when relevant to forecasting; we do
  not host partisan debate.
- A free-help-desk for unrelated economic research. OPENGEM is the topic.
- A place to promote competing closed products. Open complements (OWID,
  OpenBB, statsmodels, Nixtla, Datasette) are welcome to be discussed.

## Rules

1. Be specific. Vague critiques don't help us improve.
2. Cite sources. If you're pointing at a number, link the cite-this-view URL.
3. No PII. Don't paste API keys, magic-link tokens, customer information.
4. No paid promotion without permission. Sharing your own Substack / YouTube
   that uses OPENGEM is encouraged (we want the embed flywheel); promoting
   unrelated products is not.
5. Disagreement is welcome; disrespect is not. The mod team is small and
   tired. Don't make us do extra work.
6. Don't dox or screenshot conversations to external platforms. The Discord
   is semi-public (anyone can join) but conversations are not press
   material. Press inquiries go to press@opengem.com.

## Moderation principles

- Mods are members + occasionally a founder. We don't run a corporate trust
  & safety operation.
- Bans are public: if you're banned, the reason is posted in #announcements.
  No silent removals.
- Appeals: DM the mod or email mods@opengem.com. We try to respond within
  3 business days.
- Three-strike rule: warning, temp ban (7 days), permanent ban.

## The publish-misses pinned post

[Always pinned in #announcements.]

If you find a forecast we got wrong, a methodology that's broken, or a data
provenance error — tell us here. We will:

1. Acknowledge in this thread within 48 hours.
2. Open a public GitHub issue if confirmed.
3. Publish a post-mortem on /accountability if the miss is significant.
4. Credit the reporter (with consent) in the post-mortem.

This is not lip service. The accountability ledger at /accountability is the
operational instance of this commitment. Every reported miss we confirm
becomes a public artifact.
```

Pinned in `#announcements`. Linked from the home page footer. Quoted in `welcome.md` for the Discourse forum.

---

## Channel structure

Six top-level channels (kept deliberately small):

| Channel | Purpose | Read | Write |
|---|---|---|---|
| `#welcome` | Charter pin + introduction | All | Mods |
| `#announcements` | Releases, post-mortems, retrospectives, "publish-misses" pin | All | Mods |
| `#general` | Cross-cutting discussion | All | All |
| `#feature-requests` | Threaded requests, voted via emoji | All | All |
| `#data-questions` | Specific questions about data + provenance | All | All |
| `#dev` | API + MCP + integration questions | All | All |

Adding a seventh channel requires a Discourse forum thread + 7-day comment window + mod approval. We do not let channel sprawl happen by accident; every channel costs ongoing moderation attention.

Voice channels: one only, called `#office-hours`, open during scheduled "office hours" sessions per [[L007]] tactic 9.2 — monthly, founder + early adopters, 90 minutes, recorded and posted to YouTube.

---

## The publish-misses pinned post (full text)

The pinned post in `#announcements` is the operational signature of OPENGEM's accountability brand. Full text:

```
# PUBLISH-MISSES THREAD (always pinned)

This community runs the same discipline as the OPENGEM dashboard: when we
miss, we name it.

## How to report a miss

If you've found a forecast we got wrong, a methodology that's broken, or a
data provenance error, reply here with:

- The cite-this-view URL of the forecast
- The realized value or the data source showing the error
- Your assessment of why it's a miss

We will:

1. **Acknowledge within 48 hours** in this thread.
2. **Confirm or counter-argue within 7 days**, with a written explanation
   of either acceptance ("you're right, here's our analysis") or rejection
   ("we don't think this is a miss, here's why").
3. **If confirmed**: open a public GitHub issue tagged `confirmed-miss`,
   assign an owner, and publish a post-mortem on /accountability within 30
   days.
4. **Credit you publicly** (with your consent and preferred attribution)
   in the post-mortem.

## Confirmed misses log

[Auto-updated by a bot from the accountability-ledger GitHub repo. Every
confirmed-miss issue links here as it's resolved.]

- 2026-08-12: USA-GDP-4Q-2026Q2 — reported by @Marcus-Reuters, confirmed,
  post-mortem at /postmortem/usa-gdp-2026q2.
- 2026-09-03: IND-CPI-1Q-2026Q3 — reported by @LinAcademic, under review.

## Why we do this

The forecasting cartel hides its misses because publishing them would
break the sales motion. OPENGEM publishes its misses because the brand
depends on being structurally honest. This thread is the most direct way
to participate in that discipline.

If you've never reported a forecast miss to a public forum before: welcome.
The first one is easy. We're glad to learn from it.
```

---

## Onboarding flow

A new member who joins gets:

1. **Welcome message** in `#welcome` (mod-posted, identical for all): "Hi. Read the charter (1 min). Read the publish-misses pin (2 min). Introduce yourself in `#general` (optional)."
2. **Friction-free first post**: no role requirement, no "wait 7 days" rule. The community is small enough that lurkers are fine and contributors are welcome immediately.
3. **Role assignment** (optional, self-served): roles include `:reader:` (default), `:writer:` (uses OPENGEM in published work), `:builder:` (uses OPENGEM in code), `:academic:` (uses OPENGEM in research), `:institutional:` (representing an org). Roles unlock no permissions; they help mods route questions and help members find each other.

---

## Moderation operations

| Cadence | What happens |
|---|---|
| Daily | Founder skims `#announcements`, `#feature-requests`, publish-misses replies. ~10 minutes. |
| Weekly | Mod summary: top 3 feature requests, top 3 confirmed misses, top 3 community contributions. Posted to `#announcements`. |
| Monthly | Founder hosts `#office-hours` voice for 90 min. Recorded + posted to YouTube. |
| Quarterly | Charter review: any rules to add, change, remove based on the quarter's friction? Public proposal + comment period before changes. |

Mod team starts as: founder + 2-3 early adopters who self-volunteered (from the W-2 warm-intro list). Pay: nothing direct; they get the `:mod:` role + free Studio-tier credit + first-named in retrospectives.

---

## Discourse forum (`forum.opengem.com`)

Discourse is the long-form complement. Threaded, search-indexable, archive-friendly. Categories:

- **Announcements** (read-only for non-mods, mirrors Discord `#announcements`)
- **Data & provenance** (long-form data questions)
- **Methodology** (long-form methodology discussions)
- **Feature requests** (mirrors Discord `#feature-requests` but threaded)
- **Show & Tell** (members showcase their OPENGEM-powered work)
- **Confirmed misses** (mirrors Discord publish-misses thread)
- **General**

Bridging: a bot syncs `#announcements` from Discord → Discourse and confirmed-miss replies in both directions. Members can subscribe to Discourse topics via email; Discord doesn't natively support that.

Self-hosted Discourse on Cloud Run. Cost: ~$30/month. Worth it for the SEO indexability that Discord lacks.

---

## What we explicitly *don't* do

- **No Slack.** Slack's free tier truncates history; OPENGEM commits to permanent searchable archives. Discord (free, full archive) + Discourse (SEO-indexable) cover the same ground.
- **No private channels.** Every channel is public. If a conversation needs to be private (security disclosure, customer support), it routes to email.
- **No reaction-role gimmicks.** No "react with 👋 to get the @reader role." Roles are explicit self-assignment.
- **No XP / levels / gamification.** OPENGEM's brand is seriousness; gamification reads as MMO.
- **No bots beyond the announcement-sync, the publish-misses log, and the publish-misses bot.** Custom commands compound moderation cost.

---

## Y1 health metrics

The community is a leading indicator. We watch:

| Metric | Y1 target |
|---|---|
| Members joined | 500 |
| Weekly active (posted in 7 days) | 50 |
| Confirmed misses reported by community | 5 |
| Feature requests with ≥10 reactions | 10 |
| Office-hours attendance | 20 avg, peaking at 50 |
| Mod-team size | 4 (founder + 3 community) |

If `Confirmed misses` exceeds 5/quarter by Y1, that's brand-positive — the community is doing the auditing we promised they could. If it stays at 0, either we're forecasting perfectly (unlikely) or the community isn't engaged enough to audit. The mod team's Y1 focus is making the publish-misses thread *active*.

---

## What this loop produced

- A short public-facing charter for OPENGEM's Discord + Discourse community.
- Six-channel Discord structure with one voice channel for monthly office hours.
- The publish-misses pinned post (full text), which is the brand-consistent ritual that no other open-source-project community has.
- Onboarding flow with optional self-served roles.
- Moderation cadence (daily / weekly / monthly / quarterly).
- Discourse forum complement with auto-sync to Discord.
- A list of explicit non-features (no Slack, no private channels, no gamification, no bot sprawl).
- Y1 health metrics with a target on community-confirmed misses.

## What comes next

- **L298** — post-mortem template that the publish-misses thread populates.
- **L299** — quarterly retrospective surfaces community-confirmed misses publicly.
- **L274** — KPI dashboard tracks `confirmed misses by community` as a meta-signal.

## Related

- [[L007-distribution-thesis]] — Discord channel #9 expanded here
- [[L008-differentiation]] — five promises mirrored in the publish-misses pin
- [[L285-accountability-ledger]] — the page community-confirmed misses publish into
- [[L298-postmortem-template]] — the template applied to community-reported misses
