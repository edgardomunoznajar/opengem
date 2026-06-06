# L287 — Vendor Checklist for Paid Tier (SOC2, Security Review, DPA)

**Loop**: 287 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis of this loop

The Institutional and Vendor tiers ([[L276]]) are where revenue concentrates by Y2-Y3. Institutional buyers (regional central banks, NGOs, sovereign funds, university research centers) and Vendor buyers (LLM platforms embedding OPENGEM) cannot sign without passing their procurement teams' vendor onboarding. That onboarding is a checklist: SOC2, ISO 27001, DPA, security review questionnaire, references, financial standing.

A single-founder OPENGEM cannot become SOC2-compliant in 12 months. But we can be *visibly progressing toward* SOC2 such that an Institutional buyer can put us in a "pre-approved with risk acceptance" bucket. This loop specifies the v1 checklist (what we have at launch), the Y1 checklist (what we add in the first 12 months), and the Y2 checklist (the moment SOC2 Type I becomes table stakes).

The mistake to avoid: assuming we can wing it for the first Institutional customer. We will lose deals because their procurement team needs paperwork. We have to have at least *something* by launch, with a credible path to more.

---

## V1 launch — minimum vendor-ready checklist

What an Institutional buyer can verify on Day 1 of launch:

| Item | Status at v1 | Where it lives |
|---|---|---|
| Privacy Policy | YES | /privacy ([[L284]]) |
| Terms of Service | YES | /terms ([[L283]]) |
| Data Processing Agreement (DPA) template | YES | available on request from privacy@opengem.com |
| Subprocessor list | YES | /about/subprocessors |
| Security disclosure process | YES | /security |
| Breach notification SLA (72h GDPR-compliant) | YES | privacy section 10 |
| Sub-processor DPAs (Stripe, Cloudflare, Resend, Plausible) | YES | linked from /about/subprocessors |
| Open source code (Apache-2.0) | YES | github.com/opengem |
| Incident response runbook | YES | internal, available on NDA |
| Backup + restore SLO | YES (R2 + nightly DB snapshot) | /security/backup-policy |
| Data residency commitment (best-effort EU) | YES | /privacy section 12 |
| Single sign-on (SAML 2.0 / OIDC) | NO (Y1) | — |
| SOC2 Type I | NO (Y2) | — |
| ISO 27001 | NO (Y3+) | — |
| Cyber insurance | NO (Y2) | — |
| Penetration test annual report | NO (Y2) | — |
| Background checks on personnel | NO (single founder) | — |
| Business continuity plan | YES (minimal, one founder) | /about/continuity |
| Financial standing letter | YES (founder's audited financial statement) | available on request, NDA |

Of 19 items, 12 are YES at v1. The 7 NOs are explicitly named, with explicit Y1 / Y2 / Y3 timelines.

---

## The vendor questionnaire pre-filled

Most procurement teams send a vendor questionnaire (SIG, CAIQ, custom Excel sheet). The single most efficient thing OPENGEM does is *pre-fill the standard ones*. We publish a public version at `/about/vendor-questionnaire.pdf`.

The pre-filled questionnaire covers:

### Section 1 — Company overview

- Company name: OPENGEM (legal entity TBD at v1; founder's sole proprietorship until incorporation)
- Founded: 2026
- Headquarters: [founder location]
- Number of employees: 1 (founder) at v1; expanding per [[L010]]
- Open-source / Apache-2.0 code: github.com/opengem

### Section 2 — Data processing

- We process customer email addresses, billing data, API usage data, optional watchlist content.
- We do not process customer-content data; the customer does not send us data — we serve them data.
- Data residency: best-effort EU for analytics (Plausible Cloud EU); CDN routing prefers EU for EU users; primary application data on Cloudflare D1 with global edge replication.
- Retention: 7 years for billing (legal requirement); 30 days for server logs; user-account-deletion within 30 days of request.

### Section 3 — Sub-processors

Public list at `/about/subprocessors`:

| Sub-processor | Purpose | Data class | DPA available |
|---|---|---|---|
| Stripe | Payment processing | Billing PII | YES |
| Cloudflare | Hosting, CDN | All processed data | YES |
| Resend | Transactional email | Email + content | YES |
| Plausible Cloud | Aggregate analytics | No PII | YES |

### Section 4 — Security controls

- TLS 1.3 for all traffic.
- API keys hashed at rest.
- Encryption at rest on Cloudflare D1 and R2.
- Authenticated admin access requires magic-link + 2FA (v1.1).
- Backup: nightly R2 snapshot; PITR on D1 for 30 days.
- Incident response runbook: published internally, available on NDA.
- OWASP Top-10 mitigation: yes.

### Section 5 — Compliance posture

- GDPR: compliant by design (no fingerprinting, cookieless, EU residency available).
- CCPA / CPRA: compliant; data subject rights honored.
- SOC2: not at v1; Type I targeted Y2.
- ISO 27001: not at v1; Y3 target.
- PCI-DSS: not applicable (Stripe handles all card data).

### Section 6 — Business continuity

- Single founder at v1; concentration risk.
- BC plan: succession to advisory board + 30-day legal escrow if founder unavailable; full open-source repo means any institutional buyer can self-host on cease of OPENGEM operations.
- Insurance: TBD Y2.

### Section 7 — Open-source assurance

- Apache-2.0 license + CC-BY-4.0 data + CC-BY-4.0 model cards.
- Forkable. Buyer can self-host indefinitely.
- Even on shutdown, the data + code remain available under the licenses.

---

## The trust artifacts that don't need certifications

Some Institutional buyers will accept the following *instead of* full SOC2 if we present them well:

### Artifact 1 — The accountability ledger ([[L285]])

For a buyer evaluating OPENGEM's reliability, the accountability ledger is a stronger signal than a SOC2 attestation. SOC2 says "we follow our procedures"; the accountability ledger says "here is everything that has ever gone wrong, in public." Procurement teams who are sophisticated about evaluating data vendors will recognize this as a stronger signal.

### Artifact 2 — The reproducibility envelope (per [[L186]])

Every forecast has a reproducibility envelope (git SHA + data lockfile + container digest + generated-at timestamp). The Institutional buyer can replay any forecast from public inputs. This is verifiable supply-chain-of-trust at a level Bloomberg Terminal cannot match.

### Artifact 3 — The open source code (Apache-2.0)

Buyer can self-audit. No "trust us, the security review went well"; they can clone the repo and audit.

### Artifact 4 — The five promises ([[L008]])

Published commitments that the buyer can hold us to. A SOC2 attestation is a year old by the time it lands; the L008 promises are publicly audited every day.

The pitch to a forward-looking Institutional buyer:

```
We don't have SOC2 Type I yet. We will by Y2.

In the meantime, the L008 five-promises page, the /accountability ledger,
and the reproducibility envelope give you a stronger audit trail than any
SOC2 attestation. The code is open; the data is open; the methodology is
open. There is no part of the supply chain you cannot inspect.

If your procurement requires SOC2 specifically, we can sign an NDA and
share our Y2 roadmap. If your procurement accepts equivalent assurances
via open-source verifiability, we propose this stack of artifacts as
that equivalent.
```

The argument lands with sophisticated buyers (CGDs, World Bank prospects group, university research centers, central-bank-affiliated think tanks). It will not land with bank IT / treasury procurement teams who require checklist compliance — that's a Y2-Y3 customer cohort.

---

## The Y1 roadmap

What we add by end of Y1:

| Item | Quarter | Effort |
|---|---|---|
| SAML 2.0 / OIDC for Newsroom + Institutional | Q1 2027 | ~3 weeks |
| Cyber insurance (~$1M general + ~$2M cyber, $5k/yr est) | Q1 2027 | 2 weeks engagement |
| Annual penetration test (external vendor) | Q2 2027 | 4 weeks + ~$15k |
| SOC2 Type I readiness assessment (Vanta or Drata) | Q3 2027 | starts Y1 Q3 |
| Background-check policy + DPA process docs hardening | Q4 2027 | ~2 weeks |

The single non-engineering cost: ~$25-30k in Y1 for insurance, pen test, SOC2 readiness platform. This is folded into the [[L275]] Y2 cost projection.

---

## The Y2 SOC2 Type I path

SOC2 Type I is the moment Institutional revenue *requires* it. It's a Y2 target because:

- SOC2 readiness work takes 6-9 months.
- Auditor engagement takes 3 months.
- Total: ~12-15 months from start. So if we want Type I in Q3 2028, we start in Q3-Q4 2027.

Vanta and Drata are the obvious vendors. Cost: ~$30-40k/year. We choose one in Q3 2027 alongside the readiness assessment.

Type II (the more rigorous attestation, observing controls over 6+ months) is a Y3 target.

---

## Failure mode — when we lose a deal because of procurement

Some Institutional deals will not close in Y1. The cause will be one of:

1. **"You don't have SOC2."** → Refer them to the trust-artifacts pitch above; if rejected, schedule a follow-up for Y2 Q4.
2. **"You don't have SAML SSO."** → Y1 Q1 target; schedule follow-up for Q2 2027.
3. **"You're a single founder; concentration risk is unacceptable."** → Refer them to the open-source-as-business-continuity argument; if rejected, schedule for Y2 when team grows.
4. **"Your subprocessor list doesn't match our vendor-approval list."** → We do not switch subprocessors for any one customer; we document the rationale and they decide.

For each lost deal, we capture the reason in a tracking sheet. By Y1 end, the pattern tells us which gap to close first.

---

## What this loop produced

- A v1-launch checklist (12 YES / 7 NO with explicit Y1/Y2/Y3 timelines).
- A pre-filled vendor questionnaire at `/about/vendor-questionnaire.pdf`.
- Four trust artifacts that substitute for missing certifications (accountability ledger, reproducibility envelope, open-source code, five promises).
- The pitch to forward-looking buyers that frames the substitutes credibly.
- A Y1 roadmap of additions (SSO, cyber insurance, pen test, SOC2 readiness start).
- The Y2 SOC2 Type I path (start Q3 2027, ship Q3-Q4 2028).
- A failure-mode capture process for lost deals.

## What comes next

- **L283** + [[L284]] reviewed by attorney for vendor-grade compliance.
- Q3 2027: SOC2 readiness vendor selection.
- **L294** — government / NGO outreach plan uses this checklist as the qualifying conversation tool.

## Related

- [[L271-master-prd]] — section 12 launch criterion 7 (legal review) ties to this
- [[L276-pricing-model-evaluation]] — Institutional + Vendor tiers depend on this
- [[L284-privacy-policy-draft]] — DPA referenced from this
- [[L275-cost-projection]] — Y2 cost projection includes the trust-artifacts spend
