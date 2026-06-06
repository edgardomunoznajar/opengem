---
loop: 130
phase: 3
title: Watchlist UX — Persistence, Share, Default Lists
date: 2026-06-06
status: decided
---

# L130 — Watchlist UX

**Loop**: 130 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design the watchlist. Persistence rules. Share-by-URL. Default watchlists. Free vs paid limits.

## The shape

A watchlist is a named, ordered set of records. Records can be: countries, indicators, scenarios, forecasts, ledger cells. A user can have many watchlists. One is active at a time.

The watchlist surfaces in two places:
1. **Header pill** (top-right): shows active watchlist name + record count + tiny mover indicator.
2. **Right-slide drawer**: full editing surface, reached via the pill or `w` keystroke (when not on a record page; `w` adds to watchlist when on a record page).

## Persistence rules

Three persistence tiers, deliberate:

### Tier 1 — Local-only (no account)

Stored in `localStorage` under key `opengem.watchlists.v1`. Schema:

```json
{
  "active": "wl_default",
  "lists": {
    "wl_default": {
      "name": "My Watchlist",
      "created": "2026-06-06T10:00:00Z",
      "items": [
        { "kind": "country", "id": "USA", "added": "..." },
        { "kind": "country", "id": "EUR", "added": "..." },
        { "kind": "indicator", "id": "cpi-yoy", "added": "..." }
      ],
      "ordering": "manual"
    }
  }
}
```

Survives browser refresh. Lost on cookie clear, lost across devices, lost on incognito. The 30-second visitor gets a watchlist that follows them within their session and persists naturally — no friction.

### Tier 2 — URL-shareable (no account)

A watchlist can be encoded into a URL. The encoding: base64url-encoded compact JSON of just the items array. Generated via `> watchlist share` or the share button in the drawer.

```
https://opengem.world/?wl=eyJpdGVtcyI6W3sia2luZCI6ImNvdW50cnkiLCJpZCI6IlVTQSJ9LHsia2luZCI6ImNvdW50cnkiLCJpZCI6IkVVUiJ9XX0
```

When a user lands on a URL with `?wl=...`, the dashboard offers to import:

```
+----------------------------------------------------+
| Someone shared a watchlist with you.                |
|                                                    |
| 3 items: USA, EUR, CPI YoY                         |
|                                                    |
| [Import to my watchlists] [Try without importing]  |
| [Discard]                                          |
+----------------------------------------------------+
```

Maximum URL-encoded watchlist: 100 items (URL length budget ~2000 chars). Watchlists beyond 100 items must use Tier 3 (account-backed).

### Tier 3 — Account-backed (sign-in)

When the user signs in (magic link email + optional GitHub OAuth), their localStorage watchlists are merged into the server-backed catalog. After sign-in:
- All watchlists sync across devices.
- Unlimited list count (free tier: 3; pro tier: 25; team tier: unlimited).
- Each list can have up to 250 items.
- Each list gets a stable shortlink: `https://opengem.world/w/{slug}` (e.g., `/w/edgardo-g20-recession`).

The localStorage watchlists become the seed. There is no UX moment where the user has to "save" a watchlist; sign-in is the persistence boundary.

## Default watchlists

When a user arrives cold (no localStorage, no account), the active watchlist is empty. We do NOT preload a default watchlist with G20 countries — that would clutter the UX and give the user a list they did not curate.

Instead, the empty-state in the watchlist drawer offers preset watchlists to import:

```
+----------------------------------------------------+
| Watchlist                                          |
|                                                    |
| Your watchlist is empty.                          |
|                                                    |
| START WITH A PRESET                                |
|                                                    |
| 🌐 G7 Watch              7 countries               |
| 🌐 G20 Watch             19 countries              |
| 🌐 BRICS+ Watch          10 countries              |
| 🌐 ASEAN-5 Watch         5 countries               |
| 🌐 EU-27                  27 countries             |
| 🌐 LATAM Big-5           5 countries               |
| 📊 Recession watch       12 countries + RecProb    |
| 📊 Inflation watch       12 countries + CPI/Core   |
| 📊 Central bank watch    24 central banks + rates  |
| ⚠️ Scenarios firing today  4 packs                  |
|                                                    |
| Or build your own → search countries, indicators... |
+----------------------------------------------------+
```

Each preset is one click. The user can edit after import (remove items, rename the list, etc.).

This is the editorial choice: the *user* should curate. We *suggest*. We do not *push*.

## The drawer

Press `w` on a non-record page, or click the header pill, to open:

```
+----------------------------------------------------+
| Watchlist: My Watchlist           [...menu] [×]   |
+----------------------------------------------------+
| Active list ▼ My Watchlist (8 items)               |
+----------------------------------------------------+
| 🇺🇸 USA                                  ⋮          |
|    GDP 2.4% ▼ · CPI 2.9% ▼ · RecProb 34%▲          |
| 🇪🇺 EUR                                  ⋮          |
|    GDP 0.6% ▲ · CPI 2.4% ▼ · RecProb 41%▲          |
| 🇨🇳 CHN                                  ⋮          |
|    GDP 5.1% ▼ · CPI 0.4% ▲ · RecProb 19%▼          |
| 📊 CPI YoY (world)                      ⋮          |
|    4.1% ▼0.2pp · 12 country movers today           |
| ⚠️ Trade-LATAM                          ⋮          |
|    P=0.62 · fired today                            |
| ⚠️ Red-Sea-#4                            ⋮          |
|    P=0.78 · fired today                            |
| 🎯 /ledger/cpi-yoy/4Q                    ⋮          |
|    CRPS 0.84 vs WEO 0.91 (-7%)                     |
| 🎯 /ledger/gdp/1Q                        ⋮          |
|    CRPS 0.71 vs WEO 0.77 (-8%)                     |
+----------------------------------------------------+
| [+ Add by search] [⇄ Sort] [⤒ Share] [📋 Export]   |
+----------------------------------------------------+
| Daily digest: ON · email + RSS                     |
| Alerts on movers: ON · 0.5σ threshold              |
+----------------------------------------------------+
```

Each row shows a one-line readout (today's value + delta or relevant scoring metric). Click row → open record. The `⋮` menu has: pin/unpin, remove, set alert, view in compare, copy URL.

## Sorting

Three sort modes:
- **Manual** (default): user-controlled drag order.
- **By mover**: largest absolute %-change today first.
- **By alphabetical**: A-Z by display name.

User can pin items at the top regardless of sort.

## Multiple watchlists

The user can have multiple named watchlists. Switching is one click in the drawer header. Examples:
- "My Watchlist" (default; the user's daily set)
- "EM crisis watch" (custom; on/off based on news flow)
- "Hedge fund Z's sample" (imported from a public share link; read-only)

The active watchlist is what the home page's "Watchlist" row renders (per L122), what the daily digest emails, what `> watchlist:movers` queries.

## Alerts integration

Each watchlist item can have an alert attached (L131 designs alerts). The drawer shows an alert indicator next to items with active alerts. New alerts can be added directly from the drawer (the `⋮` menu's "Set alert" option).

## Daily digest

If the user signs in and opts in, the active watchlist drives a daily email at the user's chosen time. The email is a tiny version of the watchlist drawer plus the day's top movers.

The digest links to a `https://opengem.world/digest/{user-id}/{date}` page that mirrors the email and is shareable.

## Sharing watchlists

Two share paths:
1. **URL-encoded** (Tier 2): for one-off sharing, no account on either end. Maximum 100 items.
2. **Account-backed shortlink** (Tier 3): for stable sharing. The shortlink remains valid even if the watchlist is later edited (the sharer can flip "freeze contents" vs "live updates" in the share dialog).

A shared watchlist can be imported into the recipient's watchlists (copy on import) or viewed read-only.

## Free vs paid limits

| Tier | Lists | Items per list | Daily digest | Alerts |
|---|---|---|---|---|
| Anonymous (localStorage) | 1 (active) | 50 | no | no |
| Free signed-in | 3 | 50 | yes (1 daily) | 3 alerts |
| Pro ($X/mo) | 25 | 250 | yes (3 daily + RSS) | 50 alerts + webhook |
| Team ($Y/mo) | unlimited | 1000 | yes + slack/teams | unlimited + SLA |

Limits are enforced server-side at sign-in. Anonymous tier limits are enforced client-side (best-effort).

## Privacy

Watchlist contents are private by default. The only thing that leaves the user's browser without explicit action is the localStorage write (which never leaves the device). Signing in syncs the watchlist to the server account-bound store; nothing more.

Share URLs are *opt-in*. The user must explicitly generate one. We do not auto-share. We do not include user identifiers in the URL hash.

## What this loop produced

- Three-tier persistence: localStorage (anonymous) → URL-encoded (share) → account (sync).
- Watchlist items: countries, indicators, scenarios, forecasts, ledger cells.
- Empty state offers 10 preset watchlists (G7, G20, BRICS+, ASEAN-5, EU-27, LATAM-5, Recession watch, Inflation watch, CB watch, Scenarios firing today).
- Drawer shows one-line readout per item, with `⋮` menu for actions.
- Three sort modes (manual, mover, alphabetical) plus pin-to-top.
- Multiple named watchlists, one active at a time.
- Daily digest integration when signed in.
- Free vs paid limits (anonymous 1×50; free 3×50; pro 25×250; team unlimited).
- Privacy default: contents never leave device without explicit user action.

## What comes next

- **L131** designs Alerts UX (each watchlist item can attach an alert).
- **L139** designs the 3-step onboarding flow ("pick 3 watchlist items" is step 1).
- **L161** designs the country card grid (one of the preset watchlist sources).
- **L242** prototypes watchlist persistence in code.
- **L288** designs email transactional templates (daily digest).

## Related

- [[L121-information-architecture]] — watchlist pill is a header element
- [[L122-home-screen]] — watchlist row on the home page
- [[L128-search-command-bar]] — `> watchlist`, `> watch`, etc.
- [[L131-alerts-ux]] — alerts attach to watchlist items
- [[L139-onboarding-flow]] — pick 3 watchlist items in step 1
