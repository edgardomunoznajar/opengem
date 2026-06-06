# L274 — KPI Dashboard for the Dashboard (Meta)

**Loop**: 274 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis of this loop

OPENGEM is going to obsess over the world's macro data. It cannot fail to obsess equally over its own usage data. The meta-dashboard is the internal mirror: an at-a-glance view of whether the dashboard is doing what the strategy said it would do, with the same publication discipline we apply to forecasts (vintaged, scored, no silent retract).

The mistake to avoid is the "vanity metrics" trap. Twitter follower count, GitHub stars, Show HN points — these are leading-indicator-of-spikes, not leading-indicators-of-business. The meta-dashboard tracks the seven KPIs from [[L271]] section 13 plus three operational health KPIs, and *publishes the most important one quarterly* — `/accountability` views — as a public credibility signal.

The other rule: the KPI dashboard has the same data-quality standards as the public product. No "back-of-envelope estimate" rounding. Every number is timestamped, every change is logged, every dashboard slice is reproducible from the underlying event store.

---

## The eight KPIs (in priority order)

### KPI-1 — `/accountability` views per week

**Why it matters first.** This is the single most important metric because every view is a brand-credibility deposit. A user who lands on `/accountability` and reads the scoreboard + recent misses is being marketed to with the strongest possible message: "this organization shows you its own track record." The conversion path from `/accountability` visit to paid-tier signup is the highest-trust funnel we have.

**Target trajectory.**

| Horizon | Target views/week | Comment |
|---|---|---|
| Launch + 30 days | ≥ 100 | Word-of-mouth + Show HN tail |
| Launch + 90 days | ≥ 500 | First newsletter mentions + early Substack adoption |
| Launch + 365 days (Y1) | ≥ 5,000 | Compound from RSS + Substack + Twitter cards |
| Y2 | ≥ 25,000 | Press cite tail + academic citation network |
| Y3 | ≥ 100,000 | Incumbent-peer recognition + LLM-citation tail |
| Y5 | ≥ 500,000 | Citation-of-record positioning |

**Reporting.** Weekly internal. Quarterly *public* on `/retrospective/QX-YYYY` per [[L299]]. We commit to publishing this number even when it's bad. This commitment is itself a credibility deposit.

**Measurement.** Plausible / Umami custom event on `/accountability` page view. Bot filtering via Cloudflare bot management. Refresh-rate cap (multiple views from same IP within 5 min count once).

---

### KPI-2 — MCP tool calls per day

**Why it matters.** MCP is the future-shaped distribution channel from [[L007]]. Every MCP tool call is a passive distribution event — an LLM is grounding in OPENGEM for a user we'll never see. The total daily tool-call count tracks the size of the LLM-grounding flywheel.

**Target trajectory.**

| Horizon | Target calls/day |
|---|---|
| Launch + 30 days | ≥ 1,000 |
| Launch + 90 days | ≥ 10,000 |
| Y1 | ≥ 100,000 |
| Y2 | ≥ 1,000,000 |
| Y3 | ≥ 10,000,000 (first Vendor tier landed) |
| Y5 | ≥ 100,000,000 |

**Reporting.** Daily internal; aggregated weekly to the meta-dashboard. Tool-level breakdown (which of the 8 tools is most called) is published quarterly.

**Measurement.** Cloudflare Workers analytics + custom event tagging per tool. Source attribution (which LLM platform's MCP client) where determinable.

---

### KPI-3 — Vintaged-views per day

**Why it matters.** A "vintaged view" is a page load that includes a `?vintage=YYYY-MM-DD` query parameter, indicating the user rewound to a historical snapshot. This is the most engaged form of dashboard use — the user is actively exploring our track record. The Marcus journalist persona and the Lin academic persona both produce vintaged views; Damian rarely does.

**Target trajectory.**

| Horizon | Target |
|---|---|
| Launch + 30 days | ≥ 50/day |
| Launch + 90 days | ≥ 250/day |
| Y1 | ≥ 1,000/day |
| Y2 | ≥ 5,000/day |
| Y3 | ≥ 25,000/day |

**Reporting.** Weekly internal. Notable in that this is a *depth* metric — vintaged-views per total-views is a leading indicator of academic-citation conversion (the Lin persona path).

---

### KPI-4 — Embed impressions per week

**Why it matters.** Embed impressions count every external site that renders an OPENGEM iframe or static PNG with our tracker. This is the third-party reach signal that drives all top-of-funnel growth.

**Target trajectory.**

| Horizon | Target impressions/week | Distinct domains |
|---|---|---|
| Launch + 30 days | ≥ 1,000 | ≥ 20 |
| Launch + 90 days | ≥ 10,000 | ≥ 100 |
| Y1 | ≥ 100,000 | ≥ 500 |
| Y2 | ≥ 1,000,000 | ≥ 2,000 |
| Y3 | ≥ 10,000,000 | ≥ 5,000 |

**Reporting.** Weekly. Domain-level breakdown is internal-only (privacy concern); aggregate count is public.

**Measurement.** Pixel beacon on embed renders, with domain extracted from the `Referer` header. Bot-filtered.

---

### KPI-5 — DAU / WAU / MAU

**Why it matters.** Total active humans on the public dashboard. Tracked because comparable metrics in the open-source-dashboard space exist for benchmarking (OWID, TradingEconomics, OECD Data Portal).

**Target trajectory.**

| Horizon | Target WAU |
|---|---|
| Launch + 30 days | ≥ 50 |
| Launch + 90 days | ≥ 200 |
| Y1 | 100+ (the [[L001]] 12-month test) |
| Y2 | 1,000+ |
| Y3 | 10,000+ |
| Y5 | 100,000+ |

**Reporting.** Weekly DAU / WAU / MAU + ratio (DAU/WAU is a stickiness signal; ratio > 0.3 means daily-habit users).

**Measurement.** Plausible / Umami visitor tracking, privacy-respecting (no PII, no fingerprinting, no third-party cookies).

---

### KPI-6 — API requests per day

**Why it matters.** API request volume is the developer-integration signal. Lower priority than MCP because we believe the LLM-grounding surface dominates the developer-API surface long-term, but a meaningful API user base is the precondition for the Newsroom and Institutional tier conversions.

**Target trajectory.**

| Horizon | Target requests/day |
|---|---|
| Launch + 30 days | ≥ 5,000 |
| Launch + 90 days | ≥ 50,000 |
| Y1 | ≥ 500,000 |
| Y2 | ≥ 5,000,000 |
| Y3 | ≥ 50,000,000 |

**Reporting.** Weekly. Breakdown by endpoint (which routes are popular) is internal monthly review.

---

### KPI-7 — Paid conversions

**Why it matters.** The revenue signal. Tracked as conversion-funnel events (visit pricing page → start checkout → complete subscription → first 30 days retained).

**Target trajectory.**

| Horizon | Studio MRR | Newsroom MRR | Institutional MRR | Total ARR |
|---|---|---|---|---|
| Launch + 90 days | $500 | $0 | $0 | ~$6k |
| Y1 | $2,500 | $5,000 | $5,000 | ~$150k |
| Y2 | $15,000 | $20,000 | $50,000 | ~$1M |
| Y3 | $50,000 | $75,000 | $150,000 + Vendor | ~$4-5M |
| Y5 | $300,000+ | $300,000+ | $1M+ + Vendor | ~$15-25M |

**Reporting.** Weekly MRR + new-customer-count internal. Monthly cohort analysis (which week-of-signup cohorts retain best). Quarterly external — the *aggregate* MRR is published as a transparency signal (the granular customer breakdown is not).

---

### KPI-8 — Churn

**Why it matters.** Churn is the leading indicator of product-strategy failure. Studio churn > 8%/month means the embed isn't sticky enough. Institutional churn > 3%/year means the white-label isn't delivering. Vendor churn is catastrophic if it happens — every Vendor account is structurally retained because switching off OPENGEM-grounded LLM responses is product-affecting.

**Target trajectory.**

| Tier | Acceptable monthly churn |
|---|---|
| Studio | ≤ 7% |
| Newsroom | ≤ 4% |
| Institutional | ≤ 2% |
| Vendor | ≤ 1% (annual) |

**Reporting.** Weekly counts of cancellation events. Monthly cohort churn analysis. Exit-survey responses captured for every churn event (single question: "What changed?").

**Measurement.** Stripe webhook events on subscription cancellation. Customer-portal exit-survey via Resend.

---

## Three operational health KPIs (not strategic, but watched)

### Op-1 — V&V matrix pass rate (from [[L273]])

Daily rolling rate of V&V invariants passing. Target: 100%. Any sustained breach is escalated.

### Op-2 — Forecast pipeline freshness

Time since most recent forecast vintage update. Target: ≤ 24h for headline indicators, ≤ 168h (1 week) for long-tail. Stale forecasts that aren't refreshed within the cadence trigger a P1 alert.

### Op-3 — Infra cost / paid-MRR ratio

Cost from [[L275]] divided by current MRR. Target: ≤ 30% at Y1, ≤ 15% at Y2, ≤ 8% at Y3. If the ratio drifts above target, either pricing needs revisiting or infra needs optimization.

---

## The internal dashboard surface

The meta-KPI dashboard lives at `internal.opengem.com/kpi`, accessible to founders + advisory board members. Layout (same density-first principles as the public dashboard):

```
─────────────────────────────────────────────────────────
META-KPI DASHBOARD                       as of 2026-06-06
─────────────────────────────────────────────────────────

ACCOUNTABILITY VIEWS         312/wk    ↑12%   target: ≥100
MCP TOOL CALLS               4,827/day ↑8%    target: ≥1k
VINTAGED VIEWS               94/day    ↑18%   target: ≥50
EMBED IMPRESSIONS            1,847/wk  ↑22%   target: ≥1k
WAU                          81        ↑6%    target: ≥50
API REQUESTS                 12,433/d  ↑11%   target: ≥5k
PAID MRR                     $147      new    target: $500
CHURN (Studio)               0%        n=3    target: ≤7%

V&V PASS RATE                100%      24h    target: 100%
FORECAST FRESHNESS           2.3h      max    target: ≤24h
INFRA / PAID-MRR              n/a      no MRR target: ≤30%

QUARTERLY PUBLIC REPORT      next: 2026-09-30
─────────────────────────────────────────────────────────
```

Sparkline for each metric showing the last 12 weeks of trajectory. Hover for full series. The same design language as the public dashboard — internal team sees the world through the same lens as users.

---

## The publication discipline (for KPIs themselves)

The meta-dashboard inherits the L008 publication promises:

- **No retroactive metric redefinition.** If we change how WAU is calculated, the change is announced in the changelog, the prior series is preserved under its original definition with a `superseded` marker, and the new series starts forward.
- **Quarterly publication of the headline KPI.** `/accountability` views per quarter is published on the public retrospective page ([[L299]]). The number is the number — we don't round, we don't editorialize, we don't omit a bad quarter.
- **Vintage history of every quarterly retrospective.** Once published, the retrospective is permanent. Amendments append a new section; they do not edit in place.

This is the meta-discipline: OPENGEM commits to the same standards for its *own* metrics that it requires from incumbents for *their* forecasts. Asking the cartel to publish what they cannot while we hide what we can would be hypocrisy that the brand cannot afford.

---

## What this loop produced

- Eight strategic KPIs ranked by priority, each with target trajectory across launch, Y1, Y2, Y3, Y5.
- Three operational health KPIs.
- An internal dashboard layout mirroring the public dashboard's density-first design.
- A publication discipline that makes the meta-metrics subject to the same L008 promises as the public forecasts.

## What comes next

- **L275** — cost projection feeds Op-3.
- **L290** — churn flow operationalizes KPI-8.
- **L299** — quarterly retrospective template operationalizes the publication discipline.

## Related

- [[L005-north-star-metric]] — VC/w is the north star above the eight tracked KPIs
- [[L008-differentiation]] — the publication discipline mirrors the five promises
- [[L271-master-prd]] — section 13 names the KPIs this loop expands
- [[L273-vv-matrix-dashboard]] — V&V feeds Op-1
- [[L299-quarterly-retrospective]] — public publication of KPI-1
