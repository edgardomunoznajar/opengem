# L170 — Top-of-Mind Feed

**Loop**: 170 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

A "top-of-mind feed" is the single most retention-driving feature OPENGEM can ship. It's the first thing the user wants to see: what changed today, ranked by significance.

Not chronological. Ranked. This is the Bloomberg "TOP" command, rebuilt openly.

## What's in the feed

Items in the feed are of these types:

| Type | Source | Example |
|---|---|---|
| **Data release** | Indicator with a scheduled release | "US CPI YoY released: 3.5%" |
| **Forecast revision** | Internal model output change | "OPENGEM lowered 2026 Q3 US GDP nowcast by 0.3pp" |
| **Pulse alert** | Pulse map composite | "Türkiye pulse stressed: top 3 today" |
| **GDELT event** | Tier-1 news flags | "Fed announces unscheduled meeting" |
| **Methodology change** | Internal | "Combiner v4.3 deployed" |
| **Accountability entry** | Internal | "Q1 2026 CPI nowcast scored: in band" |
| **Editorial post** | Curated | "Why we revised our recession-prob upward" |

Each item has: title, body (2-3 lines), source, timestamp, score, click target.

## The ranking algorithm

Items rank by a composite score:

```
   score = w_recency * recency_factor
         + w_magnitude * abs(change_z)
         + w_attention * baseline_user_clicks
         + w_diversity * diversity_penalty
         + w_relevance * personalization
```

Components:

| Component | Description | Default weight |
|---|---|---|
| `recency_factor` | exp(-Δt/τ) with τ = 6h | 0.30 |
| `change_z` | Standardized magnitude of the change | 0.30 |
| `baseline_clicks` | How often similar items got clicked historically | 0.10 |
| `diversity_penalty` | Penalizes too many items of same type or country | 0.15 |
| `personalization` | Boost for items related to watchlist / saved views | 0.15 |

For anonymous users, `personalization` defaults to 0. For logged-in users, it's computed from their behavior.

## The "decay then peak" shape

Items don't just decay with time. A breaking event has a "discovery curve" — score rises briefly as it's confirmed, then decays:

```
   score
     │       ╱──╲
     │      ╱    ╲___
     │_____╱         ╲___
     ──────────────────────  time
       discovered  peak     fade
```

This is implemented as:
```
   score = magnitude * gaussian(time, mean=t_publish+15min, σ=4h)
```

So fresh stuff doesn't dominate for the first 15 minutes; instead, the "validated and rising" stuff dominates the front of the feed.

## The feed UI

```
   Top of mind
   ─────────────────────────────────────────
   ┌─────────────────────────────────────┐
   │ 🇺🇸 USA CPI YoY released: 3.5%       │
   │ Above consensus (3.3%); surprise +0.7σ │
   │ 9 min ago · BLS                        │
   │ [view] [chart] [methodology]           │
   ├─────────────────────────────────────┤
   │ 🇩🇪 OPENGEM lowered 2026 Q3 GDP        │
   │ Now 1.2% (was 1.5%), -0.3pp revision  │
   │ 1h ago · OPENGEM model                 │
   │ [diff] [methodology]                  │
   ├─────────────────────────────────────┤
   │ 🌍 World pulse stressed                │
   │ Türkiye, Israel, Iran top stressed     │
   │ 2h ago · GDELT pulse                   │
   │ [open pulse map]                      │
   ├─────────────────────────────────────┤
   │ 🇯🇵 BOJ unscheduled committee meeting  │
   │ Reported by Reuters, confirmed         │
   │ 3h ago · GDELT high-confidence         │
   │ [details]                              │
   ├─────────────────────────────────────┤
   │ 📰 Q1 CPI accountability entry         │
   │ OPENGEM nowcast 3.1% vs actual 3.2%   │
   │ 6h ago · OPENGEM internal              │
   │ [accountability]                      │
   └─────────────────────────────────────┘

   [Show more]
```

Items are cards with:
- Icon for type (country flag or topic icon)
- Title
- 1-2 line body
- Time-ago
- Source
- Action chips

Hover an item: a small "expand" affordance shows a mini-chart inline.

## The feed lives on the home page

It's the right rail on the home page (per L122 layout). Sticky. Auto-refreshes every 60s on the home page; otherwise on user-triggered refresh.

It's also the entire content of `/feed`.

## Personalization controls

```
   ┌──────────────────────────────────┐
   │  Tune your feed                   │
   │  ──────────────────────────────  │
   │  Cohort: ☑ G7  ☐ G20  ☐ EU       │
   │  Countries (extra):                │
   │     [+ TUR] [+ ISR]                │
   │  Types: ☑ Data releases            │
   │         ☑ Forecast revisions       │
   │         ☑ Pulse alerts             │
   │         ☐ Methodology updates      │
   │         ☑ Accountability          │
   │  Boost: ☑ Watchlist items          │
   │  Mute:  [+ press releases]         │
   └──────────────────────────────────┘
```

Saved per account. Anonymous users get sensible defaults.

## Editorial promotion

Each day, OPENGEM editorial promotes 1-3 items. These appear pinned at top with a small "editor's pick" badge.

Editorial picks are rare (3 per day max). Their job is to surface things the algorithm would miss — e.g., methodological insight, second-order implication.

## The feed reading mode

Clicking "view" on a feed item opens a stretched detail view:

```
   ┌─────────────────────────────────────────────────────┐
   │  ← Back to feed                                       │
   │                                                        │
   │  🇺🇸 USA CPI YoY released: 3.5%                       │
   │  ────────────────────────────────────                 │
   │                                                        │
   │  [Chart: actual vs OPENGEM forecast vs consensus]     │
   │                                                        │
   │  OPENGEM forecast: 3.32%                              │
   │  Bloomberg consensus median: 3.30%                    │
   │  Actual print: 3.50%                                   │
   │  Surprise: +0.2pp (+0.7σ)                              │
   │                                                        │
   │  Component breakdown:                                  │
   │  • Shelter: +0.5pp YoY (above)                        │
   │  • Energy: -0.8pp YoY (in line)                       │
   │  ...                                                   │
   │                                                        │
   │  [Cite this view] [Open in notebook] [Share]          │
   └─────────────────────────────────────────────────────┘
```

## Why it works

- One scroll = a full briefing
- Ranked = the user trusts they're not missing the big thing
- Open = methodology and source visible
- Forkable = paid users can build private feeds

## RSS / Atom

The feed has an Atom representation at `/feed.atom`. Each item is an `<entry>` with full HTML body. Used by:
- Power users with RSS readers
- LLM agents pulling daily briefings
- Substack syndication (paste the Atom URL)

See L179 for the feed catalog.

## Push channels (V2)

- Email digest (daily): top 10 items
- Slack webhook (alerts): personalized
- Discord webhook
- Telegram bot

V2 — V1 is web-only + RSS.

## Implementation

- Backend: a `feed_index` table updated by stream processors
- Scorer: a cron-like job runs every 2 minutes, computing scores for items in the last 48h, persists ranked snapshot
- API: `/api/feed?cohort=g7&types=data,forecast,pulse&since=2026-06-06T00:00:00Z`
- UI: paginated, virtualized for older items
- Cache: 60s TTL on the ranked snapshot

## "What I missed" mode

For returning users: "Show me what changed since my last visit" — filters the feed to items since `last_visit`. Highlights the top 5.

```
   You were here 2 days ago. Since then:
   • US CPI hot print
   • Fed minutes hawkish
   • OPENGEM raised 2026 recession prob by 6pp
   ...
```

Anonymous users get this via localStorage timestamp.

## Mobile

At <640px:
- Feed is the entire home page below the hero
- Cards stack vertically
- Auto-refresh disabled (battery)
- "Pull to refresh" gesture supported

## Empty states

```
   ┌────────────────────────────────────┐
   │  No new items in your feed yet.    │
   │                                      │
   │  Try:                                │
   │   • Broaden your country cohort     │
   │   • Add types (pulse, methodology)  │
   │   • Check the world pulse map →    │
   └────────────────────────────────────┘
```

## Anti-patterns avoided

- Infinite scroll. We paginate with "Show more" — feels less doomscroll, more newspaper.
- Chronological-only. Users will see the same noisy press releases otherwise; ranking is the value.
- Notification dots. We don't decorate the icon with "5 new" badges by default — feels social-media-y.
- Comments / reactions. The feed is read-only.

## Accountability arc

The feed itself is logged: which items appeared, in what order, when. The accountability page (L175) shows the feed's track record — e.g., "of the items ranked top-10 daily over the last year, how many led to a major data move?"

This is the "feed honesty" test. Most ranked feeds in finance are gamed by ad revenue. OPENGEM's feed is gamed by *being right* — and that's auditable.
