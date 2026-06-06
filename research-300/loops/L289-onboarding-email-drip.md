# L289 — Onboarding Email Drip: Day 0 / 3 / 7 / 14 / 30 Per Persona

**Loop**: 289 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis of this loop

A new user who signs up for OPENGEM has a 7-day window to convert from "signed up" to "habituated." The onboarding drip is what closes that window. Bad onboarding pushes users into the same inactive state as no onboarding; good onboarding teaches them how to make OPENGEM part of their workflow.

The persona role-tag from signup ([[L271]] §3, [[L280]] charter section) determines which drip a user gets. Five personas → five drip variants. The drips share the same five-email cadence (Day 0 / 3 / 7 / 14 / 30) but the content tracks each persona's [[L004]] JTBD.

Per [[L284]] section 9, users can opt out of the drip in their signup flow or any time via account preferences. Default: opt-in to the drip because it's useful; one-click unsubscribe in every email.

---

## The persona role tags (recap from L271 + L280)

Five role tags users self-select during signup:

| Tag | Persona archetype | Primary JTBD |
|---|---|---|
| `:reader:` | Default; Greg-like retail prosumer | "Show me the world's state in one screen" |
| `:writer:` | Substack writer / journalist / Marcus | "Let me cite this view in a post" |
| `:builder:` | Indie dev / Damian-coded | "Let me call OPENGEM from my workflow" |
| `:academic:` | Lin-like researcher | "Show me your track record + methodology" |
| `:institutional:` | Nadia-like enterprise | "Let me white-label / embed at scale" |

Each tag gets a tailored drip; the *structure* (5 emails, Day 0/3/7/14/30) is identical.

---

## The Day 0 email (universal across personas)

**Sent**: immediately after signup confirmation.
**Subject**: `Three things to try with OPENGEM in your first hour`

```
Hi [Name],

Welcome aboard. You signed up tagged as a [role]. Here are three things
to try in your first hour:

1. Your home pulse — six numbers, world economy, refreshed daily.
   https://opengem.com

2. The accountability ledger — every forecast we've ever published,
   scored against reality.
   https://opengem.com/accountability

3. {Persona-specific third item — see below}

Over the next 30 days, you'll get four more emails from us — one at
day 3, day 7, day 14, day 30. Each one teaches you something specific
about using OPENGEM for your work.

Reply to this email if anything is unclear. There's a human reading.

The OPENGEM team
opengem.com  ·  Apache-2.0  ·  CC-BY-4.0
```

The persona-specific third item:

- **`:reader:`**: "The country page for your country. https://opengem.com/countries/[their-country]"
- **`:writer:`**: "The 'cite this view' button on any chart. Try it: paste the URL into your next post."
- **`:builder:`**: "The MCP server. One snippet to ground Claude / ChatGPT in OPENGEM. https://opengem.com/mcp"
- **`:academic:`**: "The methodology page. Every model card. https://opengem.com/methodology"
- **`:institutional:`**: "The white-label embed example. https://opengem.com/embed/example"

---

## Day 3 emails — JTBD-1 deepening

**Sent**: 72 hours after signup.

### Reader (`:reader:`)

**Subject**: `Try the watchlist. Here are 3 ways people use it.`

```
You signed up 3 days ago. We hope you've poked around.

If you haven't yet: try the watchlist. It's the simplest way to use
OPENGEM regularly.

  https://opengem.com/watchlist

Three ways readers use it:

1. The 5-indicator daily pulse — pick the indicators you care about
   most. Get the morning email with the day's moves.

2. The country-specific alerts — set a threshold ("alert me if Mexico
   CPI crosses 5%") and we email you when it crosses.

3. The "share watchlist" link — your watchlist becomes a URL you can
   paste to a friend. Same dashboard view they see.

Reply to this email if you need help setting it up.
```

### Writer (`:writer:`)

**Subject**: `The cite-this-view URL. Why writers use it.`

```
The cite-this-view URL is the single most useful feature in OPENGEM if
you write about macro.

  https://opengem.com/forecasts/USA/gdp_yoy/4Q   ← the actual page
  https://opengem.com/cite/0adc7f3            ← the permanent vintage URL

Click the cite-this-view button on any chart. You get:

  - A permanent URL that resolves to the chart as it was on the date
    you clicked.
  - BibTeX, APA, Chicago, MLA citation blocks.
  - A DOI-style identifier (we're working on DataCite membership for Y2).

Why writers use it:

  - Your editors can verify the source 6 months later.
  - Your readers can click through to the live data.
  - The chart you cited stays the way you cited it. (No surprise
    revisions.)

Reply if you'd like a worked example.
```

### Builder (`:builder:`)

**Subject**: `The MCP server. Three install snippets.`

```
You tagged yourself as a builder. The MCP server is what you want.

  https://opengem.com/mcp

Three install snippets to copy-paste:

1. Claude Desktop:
   [code snippet — 4 lines]

2. Cursor:
   [code snippet]

3. ChatGPT (with Anthropic-compatible MCP):
   [code snippet]

Once installed, you can ask your LLM: "What's the OPENGEM forecast
for German GDP growth next quarter?" The LLM will call our MCP, get
the answer with vintage + provenance, and reply with the cite-this-view
URL.

Free tier: 100 invocations / day. If you need more, the Pro tier at
$29/mo lifts it to 10k/day.

Reply if you hit a snag.
```

### Academic (`:academic:`)

**Subject**: `Our methodology pages. Why academics use them.`

```
The methodology pages are written for academic readers.

  https://opengem.com/methodology

Each model has a card per the Mitchell et al. structure:
  - Intended use
  - Training data + vintage
  - Evaluation metrics
  - Known limitations
  - Code link (Apache-2.0)

Specifically useful for academic work:

  - Every forecast object has a reproducibility envelope (git SHA +
    data lockfile + container digest). You can byte-replicate.
  - Our scoring methodology page documents CRPS / log-score / PIT /
    MAE / RMSE definitions per indicator and horizon.
  - The accountability ledger is a working dataset for studying
    forecast accountability. We've had researchers cite it; if you
    do, we'd love to know.

Reply if you'd like a worked replication example.
```

### Institutional (`:institutional:`)

**Subject**: `White-label embed. Three examples.`

```
You tagged yourself as institutional. White-label embed is the v1
surface that matters most for you.

  https://opengem.com/embed/example

Three live examples of white-label use:

  1. [Sample think-tank with macro.[org].org subdomain]
  2. [Sample NGO embed in publication]
  3. [Sample university research center with custom theme]

The Institutional tier ($4,999/mo) gets you:
  - Custom subdomain (macro.yourorg.org powered by OPENGEM)
  - Private theme + branding
  - Custom data slices for your specific country / indicator set
  - SOC2 documentation when available (Y2 target)
  - NDA support
  - Unlimited API + MCP throughput
  - Quarterly calibration report comparing your usage to peers

If your procurement requires SOC2 specifically, schedule a call:
  sales@opengem.com

We have a vendor questionnaire pre-filled at
  https://opengem.com/about/vendor-questionnaire.pdf
```

---

## Day 7 emails — habituation push

**Sent**: 7 days after signup.

### Universal Day 7 framing

```
Subject: 7 days in. The two ways OPENGEM becomes habit.

Hi [Name],

A week ago you signed up. Most users who become daily readers do one
of two things in their first week:

1. They set up an RSS feed of their watchlist.
   https://opengem.com/watchlist#rss

2. They subscribe to the weekly digest.
   https://opengem.com/account/digest

Either becomes habit. Neither requires you to remember to visit the
dashboard.

{Persona-specific addition — see below}

Reply if you need help with either.
```

Persona-specific addition:

- **Reader**: "If you're a country-specific reader (USA, Eurozone, India, China are most-watched), the country-feed is the right primitive. Subscribe to the per-country RSS."
- **Writer**: "If you write weekly, the weekly digest feeds nicely into your draft cycle. Many writers use it as a 'topics this week' starter."
- **Builder**: "If you're building automation, the JSON API of your watchlist + the MCP server is the right combination. Saves you from polling."
- **Academic**: "The post-mortem feed is the most useful one for academics. It's a working dataset of forecast accountability events."
- **Institutional**: "If your organization wants the digest white-labeled for internal distribution, that's the Newsroom tier ($499/mo). Reach out if interested."

---

## Day 14 emails — deeper feature

**Sent**: 14 days after signup. By now the user is either habituated or churned.

### Universal Day 14 framing

```
Subject: 14 days. Here's the feature most users miss.

Hi [Name],

Most users miss this feature: the vintage time machine.

  https://opengem.com/forecasts/USA/gdp_yoy/4Q   ← any forecast page
  Click the "Vintage" button at the top of the chart.
  Drag the slider back to a past date.
  Watch the chart change to show what we were predicting then.

Why it matters:

  - We don't retroactively edit forecasts. The chart you see at
    September 2024 is exactly what we showed at September 2024.
  - You can verify our track record yourself. Pick any past date,
    see what we predicted, compare to what happened.
  - {Persona-specific value-prop}

It's a small UX feature that proves a big claim ("publishes its own
track record").

Reply if you'd like a walkthrough.
```

Persona-specific value-prop:

- **Reader**: "It's the calmest way to learn how forecasting actually works — see how predictions evolved."
- **Writer**: "Citations to prior-vintage forecasts are stable. The URL doesn't break when we revise."
- **Builder**: "The vintage scrubber is mirrored in the API. `?vintage=YYYY-MM-DD` parameter on any forecast endpoint."
- **Academic**: "Time-machine views work in replication. Lock your data vintage and your forecast vintage; replay the chart exactly."
- **Institutional**: "Compare your institution's prior forecasts (if you publish them) against OPENGEM's track record on the same series. Several of our Institutional customers use this for internal review."

---

## Day 30 emails — credibility round-trip

**Sent**: 30 days after signup.

### Universal Day 30 framing

```
Subject: 30 days. Here's what you've used. Here's what's new.

Hi [Name],

You signed up 30 days ago. Here's what we noticed:

  - Pages visited: {count}
  - Forecasts viewed: {count}
  - Watchlist alerts triggered: {count}
  - Cite-this-view URLs you generated: {count}

(We share this with you because you'd want to know. We don't share it
with anyone else.)

Three things from us:

1. The accountability ledger updated this week. We published a new
   post-mortem on {recent miss}. We were wrong by {amount}; here's
   the post-mortem: {link}.
2. {Persona-specific update}.
3. Pricing reminder: the free tier is the whole product. The paid
   tier is for velocity (throughput) and fit (white-label). We never
   gate substance. If you want to see how that translates: see
   https://opengem.com/pricing.

If OPENGEM isn't useful to you, unsubscribe one-click below. No
hard feelings.

Reply if anything's been bothering you. We read every reply.

The OPENGEM team
```

Persona-specific update:

- **Reader**: "We added {N} new countries this month. See the coverage page."
- **Writer**: "We're talking with {Substack name} about co-bylined posts. If you'd be open to similar collaborations, reply."
- **Builder**: "We shipped {X} MCP tool / API feature. See the changelog at /changelog."
- **Academic**: "{Paper / replication kit / data dump} is now available. See /methodology."
- **Institutional**: "We landed our first Institutional customer publicly: {if applicable}. Open conversation about your use case anytime."

The credibility round-trip — the Day 30 email leads with "we missed by X; here's the post-mortem" — is the most important brand move in the entire drip. The user, 30 days in, sees the brand promise in action: misses are surfaced, not hidden.

---

## What we don't send

- **No "we miss you" re-engagement emails.** If a user goes dormant, we let them. The Day 30 email is the last touchpoint; after that, weekly digest only if subscribed.
- **No surveys.** Replies to transactional emails are our research.
- **No "limited time offer" pricing.** OPENGEM's pricing is stable; we don't manufacture urgency.
- **No "your account is at risk" scare-language.** Even at billing failure, we use plain language and offer 30 days to resolve.

---

## A/B testing discipline

Tests on the drip are limited to:
- Subject lines (open rate).
- Send time (open rate per persona).
- Call-to-action positioning (click-through to dashboard).

Tests are *not* run on:
- The credibility-round-trip framing (the brand promise stays consistent).
- The unsubscribe friction (one-click forever).
- The persona-specific content (changes only on intentional product evolution).

Cohort comparison: track 30-day-retention by drip variant. If a variant retains worse than control, we revert. If it retains better, we promote to default.

---

## Metrics

The drip is judged on:

| Metric | Y1 target |
|---|---|
| Day-0 open rate | ≥ 70% (post-signup is peak attention) |
| Day-30 open rate | ≥ 35% |
| 30-day retention (any session in days 7-30) | ≥ 40% |
| Persona role-tag selection (vs default) | ≥ 60% (most users self-tag) |
| Conversion to first paid tier | ≥ 1.5% by Day 30 |

These are realistic for an open-source-credibility brand. The brand pre-selects users who care about transparency; that translates into higher engagement than a typical SaaS drip.

---

## What this loop produced

- A five-email drip (Day 0 / 3 / 7 / 14 / 30) with persona-specific variants for `:reader:`, `:writer:`, `:builder:`, `:academic:`, `:institutional:`.
- A Day 30 "credibility round-trip" framing that surfaces post-mortems to new users.
- A list of anti-patterns (no re-engagement, no urgency, no survey).
- A/B testing discipline that protects brand consistency.
- Y1 success metrics.

## What comes next

- **L290** — renewal / churn flow for paid users at end-of-subscription.
- **L288** transactional templates support the drip.
- **L274** — KPI dashboard tracks drip conversion as KPI-7 feeder.

## Related

- [[L003-personas]] — drip variants per persona
- [[L004-jtbd-map]] — JTBD per persona drives Day 3 content
- [[L008-differentiation]] — Day 30 credibility round-trip executes promise 2
- [[L288-email-transactional-templates]] — template foundation
- [[L289]] — itself, the drip
