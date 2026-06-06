# L288 — Email Transactional Templates

**Loop**: 288 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis of this loop

Transactional email is the most-read writing OPENGEM produces. The user signed up; their attention is at peak; their decision to engage further is shaped in the first email. Every transactional we send should reinforce the brand from [[L008]]: terminal-density typography, plain language, no marketing fluff, links to the accountability ledger embedded as a credibility signal. The signup email is more brand-defining than the home page hero.

This loop specifies the templates: signup confirmation, password reset (magic-link), alert delivery, weekly digest. Each template ships in both HTML and plain-text (per RFC 8058). Each uses the OPENGEM transactional sender (`hello@opengem.com` for product, `alerts@opengem.com` for alerts, `digest@opengem.com` for the weekly), with appropriate `List-Unsubscribe` headers.

Render engine: Resend's React Email primitives (Maily / react-email). Open-source MJML as backup.

All templates pass the Gmail / Outlook / Apple Mail / Spark client rendering tests + the [accessible email checklist](https://www.htmlemailcheck.com/) before launch.

---

## Sender hygiene

| Sender | Purpose | DKIM / DMARC / SPF |
|---|---|---|
| `hello@opengem.com` | Product transactionals (signup, password) | All passing |
| `alerts@opengem.com` | User-configured alerts | All passing |
| `digest@opengem.com` | Weekly digest | All passing |
| `support@opengem.com` | Customer support replies | All passing |
| `legal@opengem.com` | Legal notices | All passing |

DMARC: `p=reject` from launch. SPF + DKIM via Resend. BIMI logo registration in Y1.

No-reply addresses are *avoided*. Every transactional email is reply-able and routes to a real human inbox. This is a small cost (~10 replies/week at launch growing to ~100/week at Y2) and a meaningful trust signal.

---

## Template 1 — Signup confirmation

**Subject**: `Welcome to OPENGEM. Your magic-link is below.`

**Plain text:**

```
Welcome to OPENGEM.

You signed up at opengem.com. To finish setting up your account, click
the link below to confirm your email:

   https://opengem.com/auth/confirm?token=[MAGIC]

This link expires in 24 hours.

If you didn't sign up, ignore this email. Your address won't be added.

A few things you might want to do next:

  - Set your watchlist: https://opengem.com/watchlist
  - Try the MCP server: https://opengem.com/mcp
  - Read our accountability ledger: https://opengem.com/accountability

Reply to this email if anything is unclear. There's a real human at
the other end.

The OPENGEM team
opengem.com  ·  Apache-2.0 code  ·  CC-BY-4.0 data
```

**HTML version**: same content, JetBrains Mono for inline-code, terminal-amber link color, minimal styling. Single column, 600px max width.

**Design notes:**

- The "your magic-link is below" subject is clear and not spammy. Avoids "Welcome aboard!" or "We're so excited."
- The accountability ledger link is in the *signup* email. The first email a new user reads contains the most important link on the dashboard.
- "There's a real human at the other end" is the brand promise made tangible.
- No images embedded. (Some clients block images by default; we want the email to work in plaintext.)
- The footer mentions the licenses as a passive credibility signal.

---

## Template 2 — Magic-link / password reset

**Subject**: `Sign in to OPENGEM`

**Plain text:**

```
Hi [Name or "there"],

Click the link below to sign in to OPENGEM. The link expires in 15 minutes.

   https://opengem.com/auth/signin?token=[MAGIC]

If you didn't request this, ignore the email. No action is taken until
the link is clicked.

Account: [email]
Requested at: [timestamp]
Device: [User-Agent summary]
Approximate location: [country, based on Cloudflare]

If this doesn't look right, lock your account immediately:

   https://opengem.com/account/lock?token=[LOCK]

Reply to this email if you need help.

The OPENGEM team
```

**Design notes:**

- 15-minute expiry. Short.
- "Account, requested at, device, approximate location" — security signal.
- The "lock immediately" link is a distinct security action. Magic-link auth is generally safer than passwords, but we still surface security context.
- No reset password "link." Magic-link is the only path; no passwords are stored. Privacy by design.

---

## Template 3 — Watchlist alert

**Subject**: `[OPENGEM Alert] {country} {indicator} crossed your threshold`

Example subject: `[OPENGEM Alert] USA CPI YoY crossed 3.0% — 3.2% as of 2026-08-15`

**Plain text:**

```
You set an alert for {country} {indicator} {threshold-condition}.

Your alert just fired.

  Indicator:    {country} {indicator}
  Threshold:    {operator} {threshold}
  Latest value: {value} (vintage {date})
  Prior value:  {prior_value} (vintage {prior_date})
  Source:       {publisher}

   https://opengem.com/forecasts/{country}/{indicator}/{horizon}#vintage={date}

OPENGEM forecast for this series next quarter:
  Point: {forecast_point}%
  P10-P90: {p10}% to {p90}%

The methodology that produced this forecast:
  https://opengem.com/methodology/{model}

Your other active alerts:
  - {alert_summary_1}
  - {alert_summary_2}

Pause or modify alerts:
  https://opengem.com/account/alerts

Reply to this email if you need help.

The OPENGEM team
```

**Design notes:**

- Subject contains the key information (no clickbait). User can triage in inbox preview.
- The forecast for the *next* quarter is included — once an alert fires, the user usually wants context on what we're predicting next.
- Methodology link surfaces the model card so a user who wants to interpret the alert in context can do so.
- "Pause or modify alerts" is one click. Friction-free unsubscribe-from-this-alert is part of the brand.

---

## Template 4 — Weekly digest

**Subject**: `OPENGEM Weekly — {date_range} — {headline_signal}`

Example: `OPENGEM Weekly — Aug 12-18, 2026 — Geopolitical risk index +14%, US recession prob -2%`

**Plain text:**

```
OPENGEM Weekly  ·  {date_range}
─────────────────────────────────────────────────────────

The week in three numbers:

  US recession (12m):       {value}%  ({delta})
  GPR nowcast:              {value}   ({delta})
  GSCPI supply chain:       {value}   ({delta})

Top moves this week:

  1. {country} {indicator}: from {prior} to {current} ({delta}).
     → https://opengem.com/forecasts/{...}

  2. {country} {indicator}: from {prior} to {current} ({delta}).
     → https://opengem.com/forecasts/{...}

  3. {country} {indicator}: from {prior} to {current} ({delta}).
     → https://opengem.com/forecasts/{...}

Forecast revisions this week:

  - {country} {indicator} {horizon}: revised from {prior} to {current}
    because {reason}. → https://opengem.com/forecasts/{...}

  - [up to 3 revisions]

New post-mortems published this week:

  - {country} {indicator} {vintage} miss — post-mortem at
    https://opengem.com/postmortem/{slug}

Scenarios trending up:

  - {scenario}: probability {prior}% → {current}%.

Scenarios trending down:

  - {scenario}: probability {prior}% → {current}%.

Reading from elsewhere this week:

  - {curated_link_1}
  - {curated_link_2}

─────────────────────────────────────────────────────────
Unsubscribe: https://opengem.com/account/unsubscribe?token=[T]
Manage preferences: https://opengem.com/account/digest

All data: opengem.com  ·  Apache-2.0  ·  CC-BY-4.0
```

**Design notes:**

- Subject contains the headline signal. Readers triage in inbox preview.
- "Three numbers, three moves, three revisions, three post-mortems, three scenarios up, three scenarios down" structure makes the digest scannable in 60 seconds.
- The post-mortem section is *part* of the weekly digest. Misses are not a separate quarterly newsletter; they're surfaced in the normal-cadence reading.
- "Reading from elsewhere this week" is curated by the founder + content lead. A small, branded long-tail link list (Adam Tooze post, Joey Politano chart, a relevant NBER working paper). This is brand-consistent (acknowledging the broader ecosystem) and earns reciprocal mentions.
- Length: target ~1,500 words total. Scannable in 5 minutes.

---

## Template 5 — Failure-log notification (subscribers opt-in)

**Subject**: `[OPENGEM] New post-mortem: {country} {indicator} {vintage} miss`

**Plain text:**

```
We published a new post-mortem on a forecast miss.

  Forecast:  {country} {indicator} {horizon} at vintage {date}
  Predicted: {point}% ({p10}-{p90}%)
  Realized:  {actual}%
  Miss:      {miss_pp} pp ({direction})
  Class:     {miss_class}

  Post-mortem: https://opengem.com/postmortem/{slug}

  Why we missed:
  {one-paragraph summary, ≤80 words, pulled from Section 4 of post-mortem}

  What we changed:
  - {action_1}
  - {action_2}

This email goes to subscribers of our failure-log notifications. To
unsubscribe from just this stream:
  https://opengem.com/account/preferences/failure-log

Or unsubscribe from everything:
  https://opengem.com/account/unsubscribe?token=[T]

The OPENGEM team
opengem.com
```

**Design notes:**

- Failure-log notifications are *opt-in*. The audience is researchers, journalists, advanced users who actively want to be notified when we miss.
- Subject line is calibrated for inbox preview to convey "this is a substantive post" not "this is marketing."
- The "Why we missed" paragraph is a one-paragraph summary. Most readers will not click through; the email itself is the artifact.
- The unsubscribe-from-just-failure-log link is critical. Users who want everything *except* failure-log notifications should not have to leave entirely.

---

## Cross-template patterns

Five patterns common to all transactional templates:

### Pattern 1 — `List-Unsubscribe` headers per RFC 8058

```
List-Unsubscribe: <https://opengem.com/account/unsubscribe?token=[T]>, <mailto:unsubscribe@opengem.com>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

One-click unsubscribe is functional. Gmail / Outlook respect it; users see the native unsubscribe button.

### Pattern 2 — Plain text always paired with HTML

Every template has a plain-text version that conveys all information. Email clients that strip HTML still get the full content.

### Pattern 3 — No images at v1

Avoid image-loading concerns. Use JetBrains Mono for inline code, terminal-amber for links, ASCII separators for visual structure. The brand carries through typography.

### Pattern 4 — Footer with license attribution

Every email ends with:

```
opengem.com  ·  Apache-2.0 code  ·  CC-BY-4.0 data
```

Passive credibility signal in every read.

### Pattern 5 — Reply-able sender

No `noreply@`. Every sender accepts replies and routes to a human inbox. We accept the support volume; we get the brand benefit.

---

## Anti-patterns we don't use

- **No "click here" CTA buttons.** Plain-text-style links. Buyers can copy-paste them.
- **No tracking pixels in transactional templates.** Aggregate analytics only via Resend's clickthrough tracking (which can be disabled per email).
- **No "follow us on Twitter" calls.** Brand-coherent voice: direct, useful, terminal-feeling.
- **No emoji in subject lines.** Some clients render them inconsistently and they read as casual.
- **No "exclusive offer" framing.** Pricing is on the page; we do not run email-only promotions.
- **No automatic re-engagement campaigns** ("we miss you!"). Users who churned chose to. We respect it.

---

## Resend setup

| Setting | Value |
|---|---|
| Custom domain | mail.opengem.com (separate from app domain) |
| DKIM | Generated by Resend on domain verification |
| DMARC | `v=DMARC1; p=reject; rua=mailto:dmarc@opengem.com` |
| SPF | `v=spf1 include:_spf.resend.com -all` |
| Bounce handling | Auto-suppression after 3 hard bounces |
| Complaints | Auto-suppression after 1 spam complaint |

Resend's developer-facing API + open-source primitives (react-email) make template iteration friction-low. Cost (per [[L275]]): $0 at v0; ~$50/mo at Y1; ~$500/mo at Y3.

---

## What this loop produced

- Five transactional email templates (signup, magic-link, alert, weekly digest, failure-log notification) with plain-text + HTML specs.
- Cross-template patterns (RFC 8058 unsubscribe, dual-format, no images, license footer, reply-able sender).
- Anti-patterns (no CTA buttons, no tracking pixels, no re-engagement campaigns).
- Resend setup checklist with DKIM / DMARC / SPF specifics.

## What comes next

- **L289** — onboarding email drip uses the signup template as its first step.
- **L290** — renewal / churn flow uses templates 1-2 as transactional inserts.

## Related

- [[L008-differentiation]] — promise + brand language threads through every email
- [[L284-privacy-policy-draft]] — opt-out + unsubscribe per privacy section 9
- [[L285-accountability-ledger-spec]] — accountability link surfaces in signup email
- [[L289-onboarding-email-drip]] — uses template 1 as step 0
- [[L290-renewal-churn-flow]] — uses templates 1+2 inline
