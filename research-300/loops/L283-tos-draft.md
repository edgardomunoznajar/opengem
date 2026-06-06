# L283 — Terms of Service Draft

**Loop**: 283 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis of this loop

A Terms of Service that a human reads end-to-end is more legally protective than a 12,000-word document a lawyer wrote that nobody opens. OPENGEM's brand depends on plain-English transparency in every public surface. The ToS is the same. Short, scannable, with a "what we will never charge for" clause mirrored from `/pricing`, an explicit acceptable-use policy that names the anti-personas from [[L009]] as out of scope, and an attribution requirement consistent with [[L282]] CC-BY-4.0.

This draft is non-attorney work product. It must be reviewed by a real lawyer before launch ([[L271]] §12 launch criterion 7). The structure and language below are the spec for that review; the lawyer's job is to harden the wording, not to redesign the structure.

The ToS lives at `opengem.com/terms`. Updates are version-tagged; the prior version is preserved at `opengem.com/terms/v1`, `opengem.com/terms/v2`, etc. Material changes trigger an email to subscribed users + a banner on the home page for 30 days.

---

## The Terms of Service (draft v1)

```
OPENGEM Terms of Service
Effective: 2026-09-30 (v1.0)

This is the agreement between you and OPENGEM. We've kept it short and
plain. The legalese version is reviewed by an actual lawyer and you can
download it as a PDF, but this page is the canonical reading.

1. WHAT OPENGEM IS

OPENGEM (the "Service") is a public dashboard, API, MCP server, and data
catalog for macroeconomic and geopolitical forecasting. The code is
Apache-2.0 licensed; the data is CC-BY-4.0 licensed; the model cards and
methodology pages are CC-BY-4.0.

You ("you") may use the Service as a visitor or as a registered user.
Registered users may have a free or paid subscription.

2. WHAT WE WILL NEVER CHARGE FOR

To make this concrete and binding, the following will remain free for all
users in perpetuity:

- The public dashboard at opengem.com — every country, every indicator,
  every forecast, every vintage
- The forecast track record at /accountability — every miss, every
  post-mortem
- Reading any historical vintage
- The methodology pages — every model card
- The Apache-2.0 source code
- The CC-BY-4.0 derived data, model outputs, and forecasts
- Embeddable widgets with OPENGEM attribution
- A baseline public API quota of 1,000 requests / day
- A baseline public MCP server quota of 100 invocations / day

We will not retroactively remove these from the free tier. Future changes
to the free quotas (up only, never down) will be announced 60 days in
advance via email and on the homepage banner.

3. ACCEPTABLE USE

You may:
- Use the Service for personal, professional, academic, and commercial
  purposes consistent with the licenses.
- Embed charts and data in your work with attribution.
- Build derivative products on top of our API and MCP.
- Cite our forecasts in publications.

You may not:
- Use the Service to make individual investment, trading, or financial
  decisions without independent professional advice. OPENGEM does not
  provide investment, trading, or financial advice.
- Scrape the dashboard in ways that bypass our API rate limits.
- Build a "private dashboard for trades" that pulls from our free MCP at
  intraday cadence — this is not the use case we provide. The MCP free
  quota is calibrated for human + LLM grounding, not high-frequency
  trading.
- Republish raw data from upstream sources we cite (FRED, World Bank,
  IMF, etc.) outside their respective licenses. We pass through their
  licenses; you must respect them.
- Misrepresent OPENGEM-derived data as your own original work without
  the required CC-BY-4.0 attribution.
- Reverse-engineer the methodology pages for commercial competing
  forecasting services without independently developing the methodology.
  (We publish methodology to enable reproducibility and audit; using it
  as a shortcut to a competing product without attribution is not the
  spirit.)
- Use the Service for any unlawful purpose, including sanctions evasion.

4. SUBSCRIPTIONS AND PAYMENTS

Paid tiers (Pro, Studio, Newsroom, Institutional, Vendor) provide
additional throughput, white-label embeds, custom subdomains, NDA
support, and other modifications. Detailed pricing at /pricing.

- Subscriptions auto-renew monthly or annually as selected.
- Cancellation: any time via the Stripe customer portal or by emailing
  billing@opengem.com. No retention emails, no friction. You retain
  access through the end of the paid period.
- Refunds: pro-rated refunds for cancellation in the first 7 days of
  each subscription period. No questions asked.
- Price changes: 60 days notice. Existing subscribers grandfathered at
  prior price for one additional billing cycle.

5. ATTRIBUTION REQUIREMENT (CC-BY-4.0)

If you embed an OPENGEM chart, quote an OPENGEM forecast, or republish
OPENGEM-derived data:

- Free, Pro, Newsroom, Institutional tiers: visible OPENGEM attribution
  required (logo or wordmark + link to opengem.com).
- Studio tier: white-label allowed (you may remove the OPENGEM wordmark
  from the chart); footer attribution link to opengem.com still required.
- Institutional tier: white-label with custom subdomain (e.g.,
  macro.yourorg.org powered by OPENGEM); footer attribution to opengem.com
  required.
- Vendor tier: contract-specific; default is footer attribution.

The attribution-link-required commitment is not waivable in any tier.
Brand attribution may be reduced; the link cannot disappear.

6. ACCOUNT, DATA, AND PRIVACY

We collect minimal data — email address (for paid accounts), API usage
metrics (for rate-limiting and billing), and aggregate analytics (via
Plausible/Umami, no cookies, no fingerprinting). Full privacy policy at
/privacy.

- We do not sell user data.
- We do not share user data with advertisers (there are no advertisers).
- We do not share user data with third parties except payment processors
  (Stripe) and email infrastructure (Resend) under data processing
  agreements.
- You may delete your account at any time. We retain billing records
  required by law (typically 7 years) and aggregate anonymous analytics.

7. INTELLECTUAL PROPERTY

- OPENGEM Code: Apache-2.0 license. You may fork, modify, and
  redistribute under the terms of Apache-2.0.
- OPENGEM Data + Forecasts + Methodology: CC-BY-4.0. You may
  redistribute under the terms of CC-BY-4.0 (with attribution).
- OPENGEM Wordmark, Mark, and Brand Identity: not part of either license.
  You may use them to identify and refer to OPENGEM (e.g., in press
  coverage, attribution, embed footers); you may not use them as your
  own product's identifier.

8. UPSTREAM DATA SOURCES

OPENGEM aggregates data from public upstream sources (FRED, World Bank,
IMF, OECD, BIS, ECB, GDELT, POLECAT, UCDP, and others — full list at
/about/licenses). Each upstream source has its own license. By using
OPENGEM-derived data, you acknowledge that downstream redistribution
must respect both OPENGEM's CC-BY-4.0 license and the upstream sources'
licenses where they apply (typically only when you redistribute the raw
upstream values, not the OPENGEM-aggregated views).

A few specific upstream sources have restrictions we pass through:
- ACLED: cited as benchmark only; raw data not redistributed via OPENGEM.
- OpenSanctions: free-tier non-commercial only; paid-tier endpoints
  touching sanctions data may be restricted until commercial licensing is
  finalized.
- Bloomberg / Stratfor / EIU / IHS / Fitch: cited as comparison
  benchmarks; their numbers are not redistributed.

9. NO WARRANTIES

OPENGEM forecasts are provided AS-IS. We make our best effort, publish
methodology and accuracy data, and run a public failure log. Despite this:

- Forecasts are not guarantees.
- Forecasts are not investment advice.
- Past forecast accuracy is not predictive of future accuracy.
- Data can be incorrect, delayed, or revised. Always verify against
  upstream sources for high-stakes decisions.
- The Service can have downtime, bugs, and errors.

To the maximum extent permitted by law, OPENGEM disclaims all warranties,
express or implied, including merchantability, fitness for a particular
purpose, and non-infringement.

10. LIMITATION OF LIABILITY

To the maximum extent permitted by law, OPENGEM, its founders, employees,
contractors, and affiliates are not liable for any indirect, incidental,
special, consequential, or punitive damages arising from your use of
the Service. Our total liability in any case is limited to the amount
you have paid us in the prior 12 months (or, for free-tier users, USD
100).

You agree to defend, indemnify, and hold OPENGEM harmless against claims
arising from your use of the Service in violation of these Terms or
applicable law.

11. CHANGES TO THESE TERMS

We may update these Terms. When we do:

- Material changes: 60 days advance email + homepage banner.
- Non-material clarifications: published with version tag; prior versions
  remain accessible at /terms/v[N].
- Continued use of the Service after the effective date of a change
  constitutes acceptance of the updated Terms.

We will *not*:
- Sneak in changes that gate previously-free features.
- Retroactively claim ownership of user-generated content beyond what
  these Terms specify.
- Change the attribution requirement to remove the upstream-link
  requirement.

12. TERMINATION

We may suspend or terminate your account for material breach of these
Terms (e.g., scraping the Service to bypass rate limits, using OPENGEM
for sanctions evasion, repeatedly misrepresenting OPENGEM-derived data
without attribution). Termination is preceded by written notice (email
+ 7 days to cure) except in cases of immediate legal risk.

You may terminate your account at any time. Termination does not affect
your CC-BY-4.0 rights to data you previously downloaded.

13. GOVERNING LAW

These Terms are governed by [jurisdiction TBD by founder + legal review].
Disputes are subject to the courts of [jurisdiction TBD].

14. CONTACT

Legal: legal@opengem.com
Billing: billing@opengem.com
Press: press@opengem.com
Security: security@opengem.com
Privacy: privacy@opengem.com

For acceptable-use violations, please use security@opengem.com.

---

Effective: 2026-09-30 (v1.0)
Prior versions: none

We will publish a plain-language explanation of any future material
changes alongside the legal text. That explanation is canonical for
interpretation purposes.
```

---

## Drafting principles that drove the structure

1. **Lead with what we will not charge for.** Section 2 is the brand promise turned into a contract clause. This is the strongest legal protection for our credibility because the language is binding.

2. **Acceptable use names the anti-personas.** Section 3 explicitly says "we do not provide investment advice" and "we do not support intraday trading bots." This protects us from misuse claims and aligns with [[L009]].

3. **Cancellation friction is zero, explicit.** Section 4 commits to no retention emails, no friction, no questions asked on first-week refunds. This is brand-defining for a SaaS in 2026 where retention dark-patterns are the norm.

4. **Attribution is non-waivable in any tier.** Section 5 keeps the citation flywheel from [[L005]] intact even at Vendor tier. This is the structural guarantee that white-label revenue does not break the brand.

5. **Upstream license pass-through is explicit.** Section 8 acknowledges that OPENGEM is a derivative work of public upstream sources and that downstream redistribution must respect both.

6. **"We will not" language.** Section 11 commits not to sneak gating changes, not to retroactively claim user content, not to remove attribution. These are public commitments that, once made, are very hard to walk back without brand damage.

7. **Short.** ~1,800 words. Reads in 10 minutes. Compare to Bloomberg Terminal's ToS at ~12,000 words.

---

## What requires legal review before launch

Five specific items the founder will not finalize without an attorney:

1. **Jurisdiction (Section 13).** Founder is Spain-based; legal incorporation is TBD. Defaults to founder's residence-of-incorporation until decided.

2. **Limitation of liability cap (Section 10).** The "USD 100" for free-tier users may need adjustment per jurisdiction.

3. **GDPR-specific addenda.** EU users may need a separate DPA reference (this is in the Privacy Policy [[L284]] but the ToS may need a pointer).

4. **California-specific privacy law references.** CCPA / CPRA may require additional sections.

5. **The acceptable-use specifics.** Sanctions evasion language needs to align with EU and US sanctions regimes; attorney to verify.

Legal review SLA: 3 weeks from W-6 to W-3. Cost: ~$3,000 estimated.

---

## Versioning discipline

The ToS is version-tagged. v1.0 ships at launch. Future versions follow the [[L283]] commitment: material changes 60 days in advance with notice; prior versions preserved at `/terms/v[N]`. The version history page itself is a credibility artifact — readers can see every change we've made.

The ToS commits us to the same publication discipline we apply to forecasts. Vintage history. No silent retract. Misses (legal mistakes) acknowledged in version notes.

---

## What this loop produced

- A ~1,800-word plain-English Terms of Service draft.
- A "what we will never charge for" clause mirroring the pricing page promise.
- An acceptable-use section that names the anti-personas as out of scope.
- A 60-day notice commitment for material changes.
- A versioning discipline preserving prior ToS versions.
- A list of five items requiring attorney finalization.

## What comes next

- Attorney review (W-6 → W-3).
- **L284** — Privacy policy draft companion.
- **L287** — vendor checklist references the ToS section 4 + 7.

## Related

- [[L008-differentiation]] — promise 5 (embed/export/expose) → ToS section 5
- [[L009-anti-personas]] — refusals → ToS section 3
- [[L276-pricing-model-evaluation]] — pricing structure → ToS section 4
- [[L282-license-audit]] — license matrix → ToS sections 7-8
- [[L284-privacy-policy-draft]] — privacy companion
