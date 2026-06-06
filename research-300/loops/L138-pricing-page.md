---
loop: 138
phase: 3
title: Pricing Page — Three Tiers, FAQ, Calibration In-Place
date: 2026-06-06
status: decided
---

# L138 — Pricing Page

**Loop**: 138 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design `/pricing`. Three tiers. Layout. FAQ. Show OPENGEM's calibration *on the pricing page itself* — the most opinionated move.

## Why show calibration on the pricing page

Every macro-data vendor has a pricing page that shows logos, testimonials, and feature checklists. None of them show calibration. OPENGEM should be the first.

This is the brand thesis in one move: "Here is what we charge. Here is how often we are right." If a visitor lands on /pricing and sees the calibration scorecard alongside the tier prices, two things happen simultaneously:
1. They learn what they would be paying for.
2. They learn that the *measurement of value* is being shown to them, openly.

Bloomberg can't do this. WEO can't do this. OPENGEM can.

## The layout

```
+--------------------------------------------------------------------------+
| OPENGEM > Pricing                                                        |
| /pricing                                                                 |
+--------------------------------------------------------------------------+
| HERO                                                                     |
|                                                                          |
| Pricing for OPENGEM World Dashboard                                      |
|                                                                          |
| Free is free. Pro is for velocity. Team is for scale.                   |
| Every forecast is public on every tier.                                |
| There is no premium-forecast tier and there will never be.             |
|                                                                          |
+--------------------------------------------------------------------------+
| CALIBRATION SCORECARD (right here on the pricing page)                  |
|                                                                          |
| OPENGEM's calibration to date                                          |
| (trailing 24 vintages, aggregated across Tier-V core countries)       |
|                                                                          |
| INDICATOR     HORIZON  CRPS    vs WEO    PIT    BIAS    STATUS         |
|                                                                          |
| GDP YoY       1Q       0.71    -0.06     0.81   -0.03   PASS           |
| GDP YoY       4Q       0.84    -0.07     0.78   -0.04   PASS           |
| CPI YoY       1Q       0.62    -0.11     0.79   -0.02   PASS           |
| CPI YoY       4Q       0.84    -0.07     0.78   -0.04   PASS           |
| Unemployment  1Q       0.41    -0.04     0.83   -0.01   PASS           |
| Policy rate   1Q       0.18    -0.02     0.85   +0.01   PASS           |
| Recession     1Q       0.79*   +0.10*    —      —       AUC PASS       |
| (* = AUC, vs Bauer-Mertens baseline)                                    |
|                                                                          |
| [Full track record →]  [What is CRPS? →]  [Why we show this →]         |
+--------------------------------------------------------------------------+
| TIERS                                                                    |
|                                                                          |
| +----------------------+  +----------------------+  +----------------+ |
| | FREE                 |  | PRO                  |  | TEAM            | |
| | $0 / forever         |  | $X / month           |  | $Y / month       | |
| |                      |  | (yearly discount X%) |  | per seat          | |
| | For everyone.        |  | For the analyst.    |  | For the desk.    | |
| |                      |  |                      |  |                | |
| | Web dashboard        |  | Everything in Free,  |  | Everything in    | |
| | All forecasts        |  | plus:                |  | Pro, plus:        | |
| | All scenarios        |  |                      |  |                | |
| | Vintage rewind       |  | API 100k req/day    |  | API 1M req/day  | |
| | RSS / Atom feeds     |  | MCP velocity tier    |  | Multi-seat       | |
| | API 1k req/day       |  | RSS feed alerts (50) |  | Webhook delivery  | |
| | MCP base tier        |  | Web push + email    |  | Slack + Teams    | |
| | JSON-per-chart       |  | Composed alerts      |  | SLA: 99.9%       | |
| | Watchlist (1, 50 it.)|  | Watchlists (25 ×     |  | White-label       | |
| | Search + commands    |  |   250 items)         |  |   embeds          | |
| | Print tearsheets     |  | Embed widget         |  | Branded tearsheets|
| |                      |  | Cite-this-view       |  | Calibration       | |
| |                      |  | Notebook export      |  |   reports         | |
| |                      |  |                      |  | Priority support  | |
| |                      |  |                      |  |                  | |
| |                      |  |                      |  |                  | |
| | [Use OPENGEM]        |  | [Upgrade to Pro]     |  | [Contact sales]   | |
| +----------------------+  +----------------------+  +----------------+ |
|                                                                          |
+--------------------------------------------------------------------------+
| COMPARE TIERS (full feature matrix)                                     |
|                                                                          |
| FEATURE                                  FREE    PRO     TEAM            |
|                                                                          |
| Public dashboard                          ✓       ✓       ✓               |
| All forecasts at all horizons             ✓       ✓       ✓               |
| All scenarios with methodology            ✓       ✓       ✓               |
| Track record + miss log + calibration    ✓       ✓       ✓               |
| Vintage rewind on every chart            ✓       ✓       ✓               |
| Provenance drawer on every chart         ✓       ✓       ✓               |
| Reproducibility envelope download        ✓       ✓       ✓               |
| Replay-and-diff CI job                   2/mo    25/mo   unlimited       |
| Watchlists                                1×50   25×250  unlimited       |
| Daily email digest                       1       3      unlimited       |
| RSS / Atom feed                          ✓       ✓       ✓               |
| Alerts                                    3      50      unlimited       |
| Web push notifications                    ✓       ✓       ✓               |
| Email notifications                       ✓       ✓       ✓               |
| RSS alert feeds                           ✗       ✓       ✓               |
| Composed (AND/OR) alerts                  ✗       ✓       ✓               |
| Webhook alert delivery                    ✗       ✗       ✓               |
| Slack / Teams integration                 ✗       ✗       ✓               |
| API requests / day                        1k      100k   1M              |
| MCP server access                         base    velocity premium        |
| Notebook export                           ✗       ✓       ✓               |
| Embed widget                              ✗       ✓       ✓               |
| Cite-this-view                            ✗       ✓       ✓               |
| Print tearsheet (PDF)                     ✓       ✓       branded         |
| White-label embed                         ✗       ✗       ✓               |
| Custom calibration reports                ✗       ✗       ✓               |
| Multi-seat administration                 —       —       ✓               |
| SLA                                       —       —       99.9%          |
| Priority support                          —       email   priority        |
+--------------------------------------------------------------------------+
| FAQ                                                                      |
|                                                                          |
| Q: Why is everything public on the free tier?                            |
| A: Because the forecasts are accountability artifacts. Gating them      |
|    would compromise our commitment to "publish our mistakes."          |
|    The paid tiers are for velocity (more API throughput, more alerts),  |
|    not for hidden forecasts.                                            |
|                                                                          |
| Q: Why show calibration on the pricing page?                            |
| A: We want you to know whether we are worth paying for before you       |
|    pay. We are also confident enough in the numbers to print them.    |
|    If our calibration drops, the table updates. We will not hide it. |
|                                                                          |
| Q: What if I exceed my rate limit?                                      |
| A: Free tier: 429 errors until midnight UTC.                            |
|    Pro tier: 429 errors with a 5-minute backoff.                       |
|    Team tier: contact-us for burst overages.                           |
|                                                                          |
| Q: Can I cancel anytime?                                                 |
| A: Yes. Pro and Team tiers are month-to-month. Yearly discounts        |
|    are prorated refundable.                                             |
|                                                                          |
| Q: Do you offer education / non-profit / journalism discounts?         |
| A: Yes. Email education@opengem.world (academia), nonprofit@           |
|    opengem.world, or press@opengem.world. Standard offer: free Pro     |
|    for verified academic / non-profit / journalism use.                 |
|                                                                          |
| Q: Can I self-host?                                                     |
| A: Yes. The code is Apache-2.0; the data is CC-BY-4.0. You can       |
|    fork the entire stack and run it yourself. The paid tiers exist    |
|    because most people prefer not to operate infrastructure.            |
|                                                                          |
| Q: How does the MCP server pricing work?                                |
| A: Free tier gets baseline access (rate-limited). Pro tier gets        |
|    higher concurrency and lower latency. Team tier gets premium       |
|    SLA.                                                                  |
|                                                                          |
| Q: What's the refund policy?                                             |
| A: Full refund within 30 days, no questions. After 30 days, prorated.  |
|                                                                          |
| Q: Do you support enterprise procurement?                                |
| A: Yes. SOC 2, DPA, security questionnaires available for Team tier.   |
|    Email procurement@opengem.world.                                    |
|                                                                          |
| Q: What happens to my data if I cancel?                                  |
| A: Watchlists, alerts, and API tokens are retained for 90 days after  |
|    cancellation. You can export everything via /settings/export at any |
|    time.                                                                |
|                                                                          |
| Q: How do you handle data licensing for sources?                        |
| A: We honor each upstream publisher's terms. Some data (BLS, BEA, Fed) |
|    is public domain. Some (OECD) is CC-BY. Some (BIS) is restricted    |
|    redistribution; we link rather than re-host. See /about/license     |
|    for the full map.                                                    |
+--------------------------------------------------------------------------+
| FOOTER STRIP                                                            |
| Need something custom? Talk to us → custom@opengem.world                |
| (Government, academia, multi-team commercial)                            |
+--------------------------------------------------------------------------+
```

## Why three tiers (and not four, and not two)

Two tiers (free + paid) compresses the price ladder too aggressively. The macro-curious YouTuber on free needs to step up to "more API + alerts" without committing to enterprise pricing. The team tier exists for desks that need multi-seat, SLA, and white-label.

Four tiers (free + starter + pro + team) over-segments. The "starter" tier between free and pro creates buyer ambiguity ("which do I need?") and dilutes the upgrade decision. Pro absorbs starter at a single price point.

Three is the cleanest mental model: free (everyone), pro (the analyst), team (the desk). Each tier has a clear archetype.

## Why velocity is the price ladder (not content)

The L001 vision commits to never gating forecasts. That commitment must be visible on the pricing page itself ("Every forecast is public on every tier"). The price ladder must be on dimensions OPENGEM legitimately can charge for:

- **Velocity**: API throughput, MCP throughput, alert delivery.
- **Convenience**: Alerts, RSS feeds, webhooks, embeds.
- **Scale**: More watchlist items, more daily digests, multi-seat.
- **Fit**: White-label embeds, custom calibration reports, SLA.

These are real value-adds. They are not artificial gates.

## The calibration scorecard placement

The scorecard sits *above* the tier comparison cards. This is intentional: the reader sees "here is how OPENGEM performs" before "here is what OPENGEM costs." The price/performance question is invited.

The scorecard data is auto-updated from the ledger. If OPENGEM's calibration drops, the table updates on the pricing page. We do not freeze the scorecard at a flattering moment.

## Pricing strategy notes (private to L138)

These are decisions for the loop, not for the page:

- **Anchor on the analyst.** Pro tier is the heart of the revenue model. Free is the funnel; Team is the upside.
- **Price Pro low at launch (~$X/mo where X is plausibly $25-49).** Drive volume. Raise once cohort retention is proven (Y2+).
- **Team tier is contact-sales.** Custom contract; multi-seat; white-label; SLA; ~$Y/mo where Y is plausibly $500-2000 base + per-seat.
- **Yearly discount: 20%.** Standard SaaS.
- **No "limited-time" pricing.** No countdown timers. No fake scarcity. The brand cannot afford that voice.

## Compare tiers table

The full matrix below the tier cards is honest. Every feature is in the matrix. There are no hidden features that "scale up" on a tier. The matrix is the contract.

## FAQ

Ten Q&As, covering:
1. Why public-by-default on free.
2. Why calibration is on the pricing page.
3. Rate-limit behavior.
4. Cancellation.
5. Discounts (academia, non-profit, journalism).
6. Self-host option.
7. MCP server pricing.
8. Refund policy.
9. Enterprise procurement.
10. Data retention after cancellation.

Plus #11: Data licensing of upstream sources.

This Q&A set anticipates the journalist, the procurement officer, the academic, and the bootstrapper. Each lands a question without making the FAQ feel cluttered.

## Conversion mechanics

The Free tier CTA is "Use OPENGEM" (not "Sign up free!"). This is intentional: the free tier is the product, not a trial.

The Pro tier CTA is "Upgrade to Pro" — assumes you are already on Free.

The Team tier CTA is "Contact sales" — Team is a relationship sale.

Checkout is via Stripe (per L109 and L260). Pro is one-click. Team is sales-assisted with a 30-minute call slot in Calendly.

## Mobile

On mobile (L142), the tier cards stack vertically. The calibration scorecard becomes a horizontal-scroll table. The FAQ is accordion-collapsed by default.

## What this loop produced

- Three-tier structure: Free / Pro / Team.
- Calibration scorecard *above* the tier cards on the pricing page itself.
- Hero copy commits to public-forecasts-on-every-tier.
- Tier dimensions: velocity, convenience, scale, fit.
- Full feature comparison matrix (no hidden tier-up features).
- FAQ (11 questions).
- Pricing strategy (anchor on analyst, price Pro low at launch, Team is contact-sales).
- Yearly discount 20%.
- Education / non-profit / journalism: free Pro tier for verified use.
- Self-host option acknowledged.
- Auto-updating calibration scorecard.

## What comes next

- **L139** designs the onboarding flow (entry to Free tier).
- **L260** designs the Stripe checkout flow.
- **L287** designs the vendor checklist for paid-tier procurement.
- **L131** integrates: alerts limits per tier are documented here.

## Related

- [[L001-vision-statement]] — commits to no-secret-forecasts, velocity-only-pricing
- [[L121-information-architecture]] — /pricing URL space
- [[L131-alerts-ux]] — alerts per-tier limits
- [[L134-track-record-page]] — calibration scorecard sourced here
- [[L137-api-docs-page]] — rate limits cross-referenced
- [[L260-pricing-page-stripe-checkout]] — checkout prototype
