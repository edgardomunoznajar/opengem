---
loop: 131
phase: 3
title: Alerts UX — Thresholds, Methods, Limits
date: 2026-06-06
status: decided
---

# L131 — Alerts UX

**Loop**: 131 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design the alerts UX. Threshold types. Delivery methods (email, web push, RSS, webhook). Free vs paid limits.

## What can be alerted

Five alertable record types, each with type-appropriate thresholds:

### 1. Indicator value alerts

When an indicator crosses a threshold or moves by a magnitude.

- **Value-crossed**: `cpi:USA crosses 4%` (any direction); `cpi:USA crosses 4% upward`.
- **Magnitude-change**: `cpi:USA changes by 0.5pp month-over-month`.
- **Relative-change**: `cpi:USA changes by 1σ vs trailing 12-month mean`.
- **Above/below trailing band**: `cpi:USA above P90 of last-12-vintages forecast`.

### 2. Forecast revision alerts

When a forecast for a specific indicator × country × horizon shifts vintage-over-vintage.

- **P50 shift**: `gdp:USA:4Q P50 shifts by ≥0.1pp at next vintage`.
- **Band shift**: `gdp:USA:4Q P10-P90 band widens by ≥0.3pp`.
- **Consensus divergence**: `gdp:USA:4Q diverges from WEO by ≥0.5pp` (after a new WEO release).
- **Calibration breach**: `gdp:USA:4Q PIT drops below 0.65 over trailing 8 vintages`.

### 3. Scenario alerts

When a scenario pack changes state.

- **Pack fires**: `trade-latam fires`.
- **Pack arms**: `trade-latam arms` (probability crosses an inner threshold, near firing).
- **Pack probability shift**: `trade-latam P shifts by ≥0.1`.
- **Pack affects new country**: `trade-latam adds country to rollup`.

### 4. Event alerts

When an event matching a query is published.

- **Keyword match**: events containing "tariff" + country tag USA.
- **High-severity geo-tag**: any high-severity event tagged a specific country.
- **Calendar release**: scheduled release X arrives (e.g., "alert me 1h before next FOMC").

### 5. Ledger alerts

When OPENGEM's calibration on a cell changes meaningfully.

- **CRPS deterioration**: `/ledger/cpi/4Q CRPS rises ≥0.1 over trailing 8 vintages`.
- **PIT breach**: `/ledger/cpi/4Q PIT exits 0.70 band`.
- **Bias drift**: `/ledger/cpi/4Q absolute bias ≥0.2pp over trailing 8 vintages`.

This last category is unique to OPENGEM. No one else publishes alerts on their own miscalibration. It is the most honest alert type we offer.

## Composition rules

Alerts can be composed with AND / OR:

```
WHEN (cpi:USA crosses 4% upward)
 AND (trade-latam fires)
NOTIFY via email AND web push
```

Composed alerts are pro-tier (the free tier supports single-clause alerts only).

## Delivery methods

Four delivery methods, each with their own setup:

### Email

The default. Delivered to the email on file. Subject line includes the trigger. Body shows the matching record + chart thumbnail + link to the live page.

The user can pick delivery cadence:
- **Immediate** (within 5 min of detection).
- **Hourly digest** (batched within the hour).
- **Daily digest** (batched in the daily 8am UTC email).

### Web push

Browser push notification. Requires permission grant once. Same payload as email but truncated.

Web push is best for "watch this scenario, ping me when it fires." Less good for "alert when GDP revision exceeds 0.1pp" (which is more naturally an email or RSS).

### RSS / Atom

Each alert generates a per-user RSS feed: `https://opengem.world/feeds/alerts/{user-id}/{alert-id}.rss`. This feed contains one entry per trigger. The user pipes the RSS into their reader of choice (Feedly, Inoreader, Substack inbox, Discord webhook via IFTTT, etc.).

RSS is pro-tier. It is also the most legible "open" delivery — the user can pipe to any tool without OPENGEM building integrations.

### Webhook (pro+)

POST to a user-supplied URL with the JSON payload of the trigger. Includes alert metadata, the matching record state, signed timestamp, and a replay link. Standard Stripe-style webhook signatures for auth.

Webhook is for power users who pipe alerts into custom systems (trading systems, Slack via incoming webhook, Discord, Notion, n8n flows, etc.).

## The alert creation flow

From any record page, press `a` (or "Set alert" in the `⋮` menu):

```
+----------------------------------------------------+
| Set alert on: 🇺🇸 USA · CPI YoY                     [×] |
+----------------------------------------------------+
| WHEN                                                |
|                                                    |
| ⦿ Value crosses                                    |
|   [ 4.0 ] %  [ upward ▼ | downward | either ]     |
|                                                    |
| ○ Changes by                                       |
|   [ ___ ] pp  over [ month ▼ | quarter | year ]   |
|                                                    |
| ○ Above forecast band P[90]                        |
|                                                    |
| ○ Composition (pro+)                               |
|                                                    |
+----------------------------------------------------+
| NOTIFY                                              |
| [✓] Email     [ ] Web push     [ ] RSS              |
| Cadence: [ immediate ▼ ]                            |
+----------------------------------------------------+
| EXPIRES                                             |
| [ Never ▼ | 30 days | 1 year | on date ___ ]       |
+----------------------------------------------------+
| [Cancel] [Save alert]                              |
+----------------------------------------------------+
```

After save, a confirmation toast: "Alert set. Will fire when CPI USA crosses 4% upward."

## The alerts management page

`/alerts` is the management surface:

```
+-------------------------------------------------------------+
| ALERTS  (5 active · 12 fired this month)                    |
+-------------------------------------------------------------+
| FILTERS [Active | Muted | Triggered last 7d] [Search ___]   |
+-------------------------------------------------------------+
| 🇺🇸 USA · CPI YoY crosses 4% upward                            |
|   Email + Web push · immediate · expires Never              |
|   Last fired: never                                          |
|   [edit] [mute] [delete]                                     |
+-------------------------------------------------------------+
| 🇪🇺 EUR · GDP:4Q P50 shifts ≥0.1pp                              |
|   Email · daily digest · expires never                       |
|   Last fired: 2026-06-02 — view trigger →                    |
|   [edit] [mute] [delete]                                     |
+-------------------------------------------------------------+
| ⚠️ Trade-LATAM fires                                            |
|   Email + Web push · immediate · expires Never              |
|   Last fired: 2026-06-06 — view trigger →                    |
|   [edit] [mute] [delete]                                     |
+-------------------------------------------------------------+
| 🎯 /ledger/cpi-yoy/4Q PIT exits 0.70 band                       |
|   Email · daily digest · expires Never                       |
|   Last fired: never                                          |
|   [edit] [mute] [delete]                                     |
+-------------------------------------------------------------+
| [+ New alert] [Manage delivery channels]                    |
+-------------------------------------------------------------+
```

Each alert has a triggered history (click "view trigger →" to see the matching record state at the moment of trigger — vintaged, citable, archived).

## Mute vs delete

- **Mute** (temporarily silence): pause delivery for N days. Alert continues to monitor; just doesn't notify.
- **Delete** (permanent): removes the alert and the trigger history.

The default mute durations are: 1h, 1d, 7d, until a specific date.

## Anti-spam / dedup

Alerts dedup within a 4-hour window: an alert that triggers and re-triggers within 4 hours fires once. The user can override this in the alert config (set dedup window to 0 to allow every trigger).

When an alert composition has many triggers in a short window (e.g., a scenario keeps re-firing as conditions evolve), the email collapses into one summary email with the trigger count and a link to the full trigger history.

## Free vs paid limits

| Tier | Alerts max | Methods | Composition | Webhook | RSS feeds |
|---|---|---|---|---|---|
| Anonymous (no account) | 0 | — | — | — | — |
| Free signed-in | 3 | Email + Web push | single-clause | no | no |
| Pro ($X/mo) | 50 | + RSS | AND/OR composition | no | yes |
| Team ($Y/mo) | unlimited | + Webhook + Slack/Teams | full DSL | yes | yes |

The anonymous tier gets no alerts — alerts require a delivery target (email at minimum), which requires sign-in.

## Why these limits

Free tier is generous on the things that cost OPENGEM nothing (email push, web push, 3 alerts is enough for "watch the recession-probability cell for my country plus a scenario or two"). Pro tier unlocks composition (the power-user surface) and RSS (the durable, open delivery channel). Team tier unlocks webhook (the integration channel) and unlimited alerts.

This means the upgrade pressure is at "I want 4 alerts" not "I want any alerts." The free tier is honestly useful.

## Quiet hours and timezone

Each user sets a default timezone and quiet hours (default 22:00–07:00 user-local). Non-urgent alerts batch into the next non-quiet window. Urgent alerts (scenario fires, high-severity events) can override quiet hours per-alert.

## Trigger history archive

Every alert trigger is archived as a vintage-stamped record:

```
GET /alerts/{alert-id}/triggers
```

The archive is per-user, sortable, downloadable as JSON or CSV, kept for 2 years on free tier, indefinitely on pro/team.

This means a journalist can subscribe to "trade-latam fires" and then 18 months later cite the exact moment a fire happened.

## What this loop produced

- Five alertable record types: indicator value, forecast revision, scenario, event, ledger calibration.
- Threshold types per record type (crossing, change magnitude, relative-σ, consensus divergence, calibration breach).
- AND/OR composition (pro+).
- Four delivery methods: email, web push, RSS, webhook.
- Three cadences: immediate, hourly digest, daily digest.
- Alerts page with edit/mute/delete.
- Dedup window: 4h default, configurable.
- Free vs paid: 3 / 50 / unlimited; methods + composition + RSS gated by tier.
- Quiet hours + timezone per user.
- Trigger history archive for citation.
- Ledger-calibration alerts unique to OPENGEM ("alert me when our own forecast PIT drops").

## What comes next

- **L130** — alerts attach to watchlist items
- **L132** — methodology drawer shows alert state for the displayed record
- **L184** — leaderboard ranking informs ledger-calibration alerts
- **L186** — reproducibility envelope; trigger payload includes envelope
- **L288** — email transactional templates for alerts

## Related

- [[L121-information-architecture]] — /alerts URL space
- [[L128-search-command-bar]] — `> alert` command
- [[L130-watchlist-ux]] — watchlist items can have attached alerts
- [[L134-track-record-page]] — ledger-calibration alerts surface from track record
- [[L186-reproducibility-envelope]] — webhook payload includes envelope
