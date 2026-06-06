# L284 — Privacy Policy Draft

**Loop**: 284 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis of this loop

OPENGEM's privacy posture is *minimal data, plain language*. No PII unless a user signs up for a paid plan. No third-party cookies. No fingerprinting. No advertising trackers. Plausible (or Umami self-hosted) for aggregate analytics — both are cookieless, GDPR-compliant by design, and respect the L008 transparency brand. The choice between them is a separate sub-decision below.

The privacy policy is the contractual mirror of this minimalism. Plain English, no "we may share with our affiliates" weasel-language, no dark patterns. The policy is short for the same reason the ToS is short — a privacy policy users read end-to-end protects us better than one nobody opens.

The policy lives at `opengem.com/privacy`. Version-tagged like the ToS ([[L283]]). Material changes get 60-day notice + email + homepage banner.

---

## Plausible vs Umami — the analytics choice

The [[L265]] loop is scoped to evaluate; this Phase 6 loop makes the call:

| Criterion | Plausible | Umami |
|---|---|---|
| License | Open-core (cloud paid; self-host AGPL) | MIT |
| Self-host complexity | Medium (PostgreSQL + ClickHouse) | Low (PostgreSQL + Node) |
| Cloud pricing at OPENGEM scale | $19/mo (Solo), $39 (Business) | Free (self-host) |
| GDPR-by-design | YES | YES |
| Cookieless | YES | YES |
| Privacy reputation | Best-in-class | Good, less-known |
| Founder time to maintain | 0 (cloud) | Few hours/mo (self-host) |
| Data residency control | EU servers (cloud Plausible) | Wherever we host |

**Decision**: Plausible Cloud at v1. Self-host Umami as a fallback at Y2 if Plausible pricing scales unfavorably or we need full control over the analytics data.

Plausible's brand association with privacy-first analytics is a side credibility signal — the kind of users who care about OPENGEM's mission also tend to recognize Plausible as a "this is a serious-about-privacy project" signal.

---

## The Privacy Policy (draft v1)

```
OPENGEM Privacy Policy
Effective: 2026-09-30 (v1.0)

This is what we collect about you, why we collect it, and what we do
with it. The short answer: as little as possible.

1. WHAT WE COLLECT

If you visit OPENGEM as a logged-out user:

- Aggregate, cookie-free analytics via Plausible: which pages you
  visited, the country (not IP) you visited from, your browser type,
  the referring URL. No persistent identifier. No fingerprint. Plausible
  cannot identify you across sessions or sites.
- Server logs: timestamp, requested URL, HTTP status code, response
  time, generic User-Agent. IP addresses are recorded in the logs and
  are deleted after 30 days (we retain hashed IPs for an additional 30
  days for security forensics, then deleted).

If you create a free or paid account:

- Your email address (used as your account identifier; we do not collect
  names, phone numbers, billing addresses except as required by Stripe
  for payment processing).
- Your role tag (optional; you self-declare as writer/builder/academic/
  institutional during signup).
- Your API key usage data: requests per day, MCP tool calls per day,
  per-tool breakdown.
- Your watchlist + saved views (if you create any).
- For paid users: subscription tier, billing history.

If you contact us:

- The content of your message (legal, billing, press, security inquiries).
- Your email address (for the reply).
- We retain this for the lesser of 5 years or "as long as needed to
  resolve and learn from the inquiry."

2. WHAT WE DO NOT COLLECT

- We do not collect or store the content of your prompts to LLMs that
  use our MCP server. The MCP responses we send are determined by your
  arguments; we do not see your prompt.
- We do not run third-party advertising trackers, fingerprinting
  scripts, or behavioral profiling.
- We do not set persistent third-party cookies.
- We do not store your IP address beyond 30 days (security forensics
  excepted, see above).
- We do not collect device IDs, advertising IDs, or any cross-site
  identifier.
- We do not collect children's data; the service is not directed at
  children under 13.

3. WHY WE COLLECT WHAT WE COLLECT

- Email: to identify your account, send transactional email (signup
  confirmation, billing receipts, alerts you've enabled, post-mortem
  notifications you've subscribed to).
- API usage: to enforce rate limits per the pricing tier you're on, to
  detect abuse, to bill you accurately.
- Analytics: to know what's used so we can prioritize features. We
  publish aggregate analytics quarterly as part of our public
  retrospective at /retrospective.
- Server logs: to debug, to detect security incidents, to maintain
  uptime.

4. WHAT WE DO WITH IT

- We use it to run the Service. That's it.
- We do not sell your data.
- We do not share your data with advertisers (we have none).
- We do not share your data with brokers or aggregators.
- We share necessary subsets with:
  - Stripe: payment processing (your name, email, billing info as
    required by Stripe's flow).
  - Resend: transactional email delivery (your email + the email body).
  - Plausible Cloud: aggregate analytics (no personal identifiers).
  - Cloudflare: hosting infrastructure (IP addresses pass through CDN
    routing).
  - Our payment processor: for paid accounts as required by financial
    regulation.

Each of these third parties has a data processing agreement consistent
with GDPR / CCPA / similar regulations. They process the data on our
behalf for the specific purpose we engaged them; they do not use it for
their own marketing.

5. HOW LONG WE KEEP IT

- Account data: as long as your account exists, plus 90 days after
  deletion to allow account-restoration during accidental cancellation.
- Billing records: 7 years (required by financial regulations).
- Server logs (with IP): 30 days, then deleted.
- Analytics: aggregate, anonymous, retained indefinitely.
- Contact form messages: 5 years or until resolved.

You may request earlier deletion via privacy@opengem.com (see Section 7).

6. WHERE WE STORE IT

- Account data + billing: Cloudflare D1 + Stripe servers (Stripe is
  PCI-DSS certified; data hosted in regions per their published
  policies).
- Server logs: Cloudflare's log infrastructure.
- Analytics: Plausible Cloud (EU servers).
- Email: Resend infrastructure.

Most of our processing happens in Cloudflare's global edge network. We
do not have a specific data residency policy at v1 (we are not
contractually obligated to one). If you require a specific data
residency (EU-only, US-only) for a paid plan, contact sales@opengem.com
and we can discuss the Institutional or Vendor tier.

7. YOUR RIGHTS

Regardless of where you are, you can:

- Request a copy of all the data we have about you. Email
  privacy@opengem.com; we respond within 30 days.
- Request deletion of all data we have about you. Email
  privacy@opengem.com; we delete within 30 days (subject to legal
  retention requirements for billing).
- Correct any data you believe is inaccurate.
- Withdraw consent for any non-essential processing (analytics is
  legitimate-interest under GDPR; you can request opt-out anyway and we
  honor it).

If you're in the EU (GDPR) or California (CCPA / CPRA), you have
additional rights to know what categories of data we collect, who we
share it with, and the right to non-discriminatory service if you
exercise these rights. We will not throttle, downgrade, or charge you
for exercising these rights.

8. COOKIES AND TRACKING

OPENGEM uses these cookies and similar storage:

| Cookie / storage | Purpose | First or third party | Persistent |
|---|---|---|---|
| Session cookie | Login session | First-party | Session-only |
| API key (localStorage) | Authenticated API calls | First-party | Until logout |
| Watchlist (localStorage) | Saved views | First-party | Until cleared |
| Theme preference (localStorage) | Dark/light mode | First-party | Until cleared |

We do NOT use:
- Google Analytics, Facebook Pixel, or any advertising platform tracker.
- Third-party cookies of any kind.
- Cross-site tracking pixels.
- Fingerprinting scripts.

If your browser blocks third-party cookies (which we have none of), the
Service works perfectly. If your browser blocks first-party cookies, you
cannot log in but can still use the public dashboard.

9. NOTIFICATIONS WE SEND YOU

If you have an account, we send:

- Account essentials: signup confirmation, password reset (magic link),
  billing receipts, subscription notifications.
- Optional: forecast revision alerts, watchlist threshold alerts, weekly
  digest, post-mortem alerts (you control which ones in your account
  settings).
- Service-critical: outage announcements, material policy changes (60
  days advance per ToS), security incident notifications.

You cannot unsubscribe from account-essentials or service-critical
notifications without closing your account. You can unsubscribe from all
optional notifications via in-account preferences or the unsubscribe
link in any optional email.

10. SECURITY

- We use TLS 1.3 for all traffic.
- API keys are hashed at rest (we cannot recover your key; we can
  regenerate).
- We follow OWASP top-10 mitigations.
- We have a public security disclosure process — see /security or email
  security@opengem.com with security findings; we acknowledge within
  72h.
- We do not yet have SOC2 (Y2 target for Institutional tier).
- Despite best efforts, no system is 100% secure. If we detect a breach
  affecting your data, we will notify you within 72 hours of discovery,
  consistent with GDPR Article 33 + CCPA.

11. CHILDREN

The Service is not directed at children under 13 (or under 16 in the EU,
or local-equivalent age). We do not knowingly collect data from children
under these thresholds. If you become aware that a child has provided us
data, contact privacy@opengem.com and we will delete it.

12. INTERNATIONAL DATA TRANSFERS

OPENGEM is operated globally. Data may be processed in multiple
jurisdictions including the EU (Plausible Cloud, our chosen primary
analytics processor), the US (Stripe, Cloudflare), and other countries
where our infrastructure providers operate.

If you're in the EU, we rely on:
- Standard Contractual Clauses with our US-based processors (Stripe,
  Cloudflare, Resend).
- Plausible Cloud's EU-only data residency for analytics.
- Our Cloudflare configuration to prefer EU edge nodes for EU visitors.

13. CHANGES

- Material changes: 60 days advance email + homepage banner.
- Non-material changes (clarifications, contact info updates, infra
  partner additions with same data class): published with version tag;
  prior versions remain at /privacy/v[N].
- You can subscribe to a "privacy-policy-changes" RSS feed at
  /privacy/feed.rss for proactive notification.

14. CONTACT

Privacy: privacy@opengem.com
Data subject requests: privacy@opengem.com
Security: security@opengem.com
General: hello@opengem.com

Our Data Protection Officer: [TBD by founder + legal review; default to
founder at v1]

---

Effective: 2026-09-30 (v1.0)
Prior versions: none
```

---

## Drafting principles

1. **Lead with what we collect and what we don't.** Sections 1 and 2 give the reader the full picture in 60 seconds. Most privacy policies bury this; we lead with it.

2. **Plain English throughout.** No "may, in our discretion, share with third parties for business purposes." Specific named partners with specific purposes.

3. **The opt-outs are real.** Section 7 commits to 30-day deletion. No "we may retain for legitimate business purposes" escape hatch beyond legally required billing records.

4. **The cookies table is concrete.** Section 8 lists every cookie/localStorage entry, its purpose, and its persistence. Compared to most policies that say "we use cookies for various purposes," this is a credibility deposit.

5. **The security commitment names a 72h breach notification window.** This matches GDPR Article 33 and is publicly committed.

6. **The DPO is named.** Section 14 commits to a Data Protection Officer (default founder at v1). This is what GDPR requires; we make it visible.

---

## Cookieless commitment — the credibility signal

The line "If your browser blocks third-party cookies (which we have none of), the Service works perfectly" is the most-quotable single sentence in the policy. It commits us to a posture: OPENGEM has *no* third-party cookies. Ever. Not analytics, not embeds, not anything. This is enforceable as a public commitment.

The Plausible / Umami choice supports this commitment at the analytics layer. The embed widget at [[L245]] must be implemented without third-party cookies (we already design for this). The Stripe Checkout iframe is a third-party iframe but does not set our cookies; payment is handled inside Stripe's domain.

---

## What requires legal review before launch

Same five items as L283 + three privacy-specific:

1. Jurisdiction-specific addenda (CCPA, GDPR, LGPD, PIPEDA per market).
2. DPO statutory requirements (does our scale require one statutorily?).
3. Cross-border transfer mechanism finalization (SCCs vs alternatives).

Legal review SLA: same 3 weeks from W-6 to W-3 alongside ToS.

---

## What this loop produced

- A ~1,600-word plain-English Privacy Policy draft.
- A decision on Plausible Cloud over Umami (Plausible at v1, Umami self-host as Y2 fallback).
- A cookieless commitment that no third-party cookies ever ship.
- A 30-day data deletion SLA, 72h breach notification window, concrete cookies table.
- Versioning discipline preserving prior policy versions.

## What comes next

- Attorney review (W-6 → W-3).
- **L287** — vendor checklist for paid tier references this policy.
- **L289** — onboarding email drip references the cookieless commitment.

## Related

- [[L008-differentiation]] — promise 5 (machine-readable) aligns with the no-fingerprint commitment
- [[L283-tos-draft]] — companion ToS draft
- [[L265-telemetry-privacy-analytics]] — the analytics evaluation this loop resolves
- [[L287-vendor-checklist-paid-tier]] — DPA references this policy
