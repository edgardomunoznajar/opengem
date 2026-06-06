# L290 — Renewal / Churn Flow

**Loop**: 290 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis of this loop

A renewal flow that uses dark patterns (hidden cancel buttons, "wait, here's 50% off" pop-ups, retention specialists on the phone) extracts ~10-20% extra revenue at the cost of brand damage that compounds against [[L008]] over time. OPENGEM's brand cannot survive dark-pattern retention; the value proposition is "we don't hide anything from you," and that has to extend to the cancellation flow.

This loop specifies the renewal + churn flow: how subscriptions renew, what we email before renewal, how a user cancels, what we do when they do, and what the exit survey captures. The flow is intentionally friction-low. We trade ~10% gross-revenue retention for a brand-coherent posture and the long-arc loyalty it produces.

The pricing tiers from [[L276]] (Pro / Studio / Newsroom / Institutional / Vendor) each get a tier-appropriate variant of the flow.

---

## Subscription lifecycle states

```
TRIALING  →  ACTIVE  →  RENEWING  →  ACTIVE  →  ...
                              ↓
                         CANCELLING
                              ↓
                          CANCELLED
                              ↓
                    GRACE PERIOD (paid period continues)
                              ↓
                            ENDED
```

Five named states:

1. **ACTIVE** — paid subscription, auto-renews at end of period.
2. **RENEWING** — 7 days before period end; renewal pre-notification window.
3. **CANCELLING** — user clicked cancel; we acknowledge; grace period through end of paid period.
4. **CANCELLED** — at end of paid period; subscription ends.
5. **ENDED** — subscription is gone; account returns to free tier.

Subscription state is tracked in Stripe + our own DB (Cloudflare D1). Stripe is source of truth; we reconcile via webhooks.

---

## The pre-renewal email (Studio, Newsroom, Institutional)

**Sent**: 7 days before period end.
**Subject**: `Your OPENGEM subscription renews in 7 days`

```
Hi [Name],

Your OPENGEM [tier] subscription renews on [date] at [price].

You'll be charged: [price] on [date]
Card: [last-4 of card]

What you'll get for the next billing cycle:
  - [Tier-specific features bullet 1]
  - [Tier-specific features bullet 2]
  - [Tier-specific features bullet 3]

What you used in the past cycle:
  - Pages viewed: [count]
  - Forecasts cited: [count]
  - API requests: [count]
  - MCP invocations: [count]
  - Watchlist alerts: [count]

To change plan: https://opengem.com/account/billing
To cancel:       https://opengem.com/account/cancel?token=[T]

Reply to this email if anything is unclear.

The OPENGEM team
```

**Design notes:**

- Lead with the renewal date and amount. No surprise charges.
- Show the user's *actual usage* — if they didn't use it, they should know.
- Cancel link is prominent. Not hidden in a footer.
- No "wait, here's an offer" pop-ups. The price you signed up for is the price that renews.

---

## The renewal confirmation email

**Sent**: day of renewal charge, immediately after successful payment.
**Subject**: `Your OPENGEM subscription renewed`

```
Hi [Name],

We charged your [card] $[price] for OPENGEM [tier].

Receipt: https://opengem.com/account/receipts/[id]
Next renewal: [date]

The receipt is also archived in your account at
https://opengem.com/account/billing.

Reply to this email if anything is unclear.

The OPENGEM team
```

Short, transactional. The user is paying customer; no marketing.

---

## The cancellation flow

When a user clicks "cancel" in their account:

### Step 1 — Acknowledge

**Page**: `/account/cancel?token=[T]`

```
You're about to cancel your OPENGEM [tier] subscription.

Your subscription continues through [end-of-paid-period date]
(no further charges).

After that, your account returns to the free tier. You keep:
  - Your account, your email
  - Your watchlist
  - Your saved views, cite-this-view URLs you've generated
  - Your role tag

You lose:
  - [Tier-specific features lost]

Before you cancel, would you like to tell us why?

[Single-question dropdown, optional]
  - Not using it enough
  - Found a similar tool I prefer
  - Pricing changed for me
  - Specific feature missing: ___
  - Personal/work change
  - Prefer not to say

[Confirm cancellation]
```

**Design notes:**

- Single page. No "are you sure?" gauntlet.
- Says clearly what they keep + what they lose.
- One optional question. Optional. Skippable.
- The confirm button is the prominent action.

### Step 2 — Confirmation email

**Sent**: immediately after cancellation confirmed.
**Subject**: `Your OPENGEM subscription is cancelled`

```
Hi [Name],

Your OPENGEM [tier] subscription is cancelled. You won't be charged again.

Your subscription continues through [end date]. After that, your account
returns to the free tier.

What you keep:
  - Account, email, watchlist, role tag
  - Cite-this-view URLs you generated
  - The free tier (which is the whole product)

We'd love to know what we could have done better. If you have 90 seconds,
reply with your honest take. We read every reply.

The OPENGEM team
opengem.com
```

**Design notes:**

- Same calm tone as everywhere else.
- "We read every reply" — and we do. Cancellation replies inform product roadmap.
- No "come back!" guilt-tripping.
- No "your subscription continues, in case you change your mind" friction — they cancelled; we respect it.

---

## What we capture on cancellation

The exit-survey dropdown answer goes into our internal cancellation tracker. We bucket reasons:

| Reason | Code |
|---|---|
| Not using it enough | UNDER_USE |
| Found a similar tool I prefer | COMPETITOR |
| Pricing changed for me | PRICE_SENSITIVE |
| Specific feature missing | FEATURE_GAP |
| Personal/work change | LIFE_CHANGE |
| Prefer not to say | NO_REASON |

Per [[L274]] KPI-8, we track these in aggregate. By Y1 we'll know which feature gaps drive the most cancellations and prioritize accordingly.

If the cancellation reply email contains specific feedback, the founder reads it and (if substantive) opens a GitHub issue. Cancellation feedback often surfaces the most useful product-direction signals because the user has nothing to gain from saying it.

---

## Grace period — what happens after the end date

When the subscription ends:

- Account state transitions from ACTIVE → ENDED.
- Paid features become inaccessible (API rate limit drops to free tier; white-label is removed; etc).
- Custom subdomain (Institutional) redirects to `opengem.com` for 30 days, then expires.
- Stored data (watchlists, saved views, cite-this-view URLs) is *retained* — these are not paid-tier features.
- No additional email beyond the cancellation confirmation. We don't send "your subscription has ended" or "we miss you."

Users can resubscribe at any time. Returning subscribers pick up where they left off — same account, same role, same saved views. No "welcome back!" friction.

---

## The failed-payment flow

When Stripe reports a failed charge (card declined, expired, insufficient funds):

### Step 1 — Day-of failure email

**Subject**: `OPENGEM couldn't charge your card`

```
Hi [Name],

We tried to charge your [card] $[price] for your OPENGEM [tier]
subscription, but the charge failed.

Reason: [Stripe-provided reason summary, e.g., "Your card was declined"]

What you can do:
  1. Update your card: https://opengem.com/account/billing
  2. Use a different payment method
  3. Reach out to billing@opengem.com if you have questions

Your subscription is in a grace period for 7 days. After that, your
account returns to the free tier.

Reply if you need help.

The OPENGEM team
```

### Step 2 — Day-3 reminder

Soft reminder. Same content, "Day 3 of 7 grace period" subject line.

### Step 3 — Day-7 final

```
Subject: Your OPENGEM subscription returns to free tier today.
```

After Day 7 grace ends, subscription returns to free tier. No additional email beyond this.

The grace period is real. We do not retry-and-retry-and-retry the card. Three notifications, then we let it go.

---

## Institutional / Vendor variants

Institutional and Vendor subscriptions have additional complexity:

### Pre-renewal touchpoint (Institutional)

- 30 days before renewal: email + (optional) call from founder to surface any conversation about expanded use case, additional sub-units, custom features.
- This is not a "save the deal" call. It's a "let's understand how this is working for you" call.

### Cancellation flow (Institutional)

- The cancel URL still works. No phone-only cancellation.
- Founder is automatically notified on Institutional cancellation. Within 5 business days, founder reaches out to the customer with a single question: "What would have made this stick?" The conversation, if granted, is product input. No "let's negotiate."
- If they say "you don't have SOC2," that's [[L287]] gap. Closed deals lost on procurement go into a separate tracker.

### Vendor cancellation

- Vendor tier is a contract; cancellation follows the contract terms (typically 60 days notice + transition assistance).
- A Vendor cancellation is a P0 internal event. Founder + sales lead + advisory board on the post-mortem.

---

## Cohort retention discipline

Per [[L274]] KPI-8, monthly retention is tracked per cohort:

| Tier | Acceptable monthly churn |
|---|---|
| Pro ($29) | ≤ 7% |
| Studio ($99) | ≤ 5% |
| Newsroom ($499) | ≤ 4% |
| Institutional ($4,999) | ≤ 2% |
| Vendor | ≤ 1% annual |

If a cohort drifts above its acceptable churn, we don't add retention specialists — we investigate the *cause* via the cancellation-reason data and address the cause. Most retention problems are product problems disguised as conversion problems. The brand commits to addressing the underlying issue, not papering over it.

---

## What we explicitly don't do

- **No retention specialists.** A user clicks cancel; they cancel. No phone call.
- **No "wait, here's 50% off" pop-up.** The price we charge is the price. We don't offer post-hoc discounts.
- **No exit-intent guilt trip.** No "OPENGEM has helped you cite N forecasts. Are you sure you want to leave?"
- **No reactivation campaigns.** Users who cancelled chose to. We respect it. They're welcome back any time, but we don't re-engage them.
- **No subscription resurrection by changing the card on file silently.** If a card is updated by Stripe Card Updater Service, we email the user to confirm before charging.
- **No silent reactivation of features after free-tier reversion.** We turn off paid features cleanly.

These are dark patterns common in SaaS. Avoiding them costs revenue. The brand requires it.

---

## Brand calibration check

Every email + every page in this flow is read by founder before any of them ship. The brand calibration check is:

1. Does the language sound like OPENGEM (plain, direct, no "valued community")?
2. Does the flow respect the user's decision (no "wait, are you sure")?
3. Does the flow give the user concrete information (what they keep, what they lose)?
4. Is the cancellation friction *less* than the friction to sign up? (It must be.)

If any answer is no, we revise. This is a brand check; it does not get A/B-tested.

---

## What this loop produced

- Five subscription states (ACTIVE / RENEWING / CANCELLING / CANCELLED / ENDED) with transitions.
- Pre-renewal email + renewal confirmation + cancellation flow specifications.
- A failed-payment grace-period flow (3 emails over 7 days, then sunset).
- Institutional / Vendor variants with founder-direct outreach.
- A list of dark patterns we explicitly do not use.
- A brand calibration check applied to every flow component.

## What comes next

- **L274** — KPI-8 churn tracking operationalizes this.
- **L288** — transactional templates support all the email steps.
- **L289** — onboarding drip prepares users to *not* churn in the first place.

## Related

- [[L008-differentiation]] — promise 5 (no paywall on substance) extends here to friction-low cancellation
- [[L274-kpi-dashboard-meta]] — KPI-8 measures the cohorts
- [[L276-pricing-model-evaluation]] — tier structure this flow handles
- [[L288-email-transactional-templates]] — templates this flow uses
- [[L289-onboarding-email-drip]] — counterpart-flow for new users
