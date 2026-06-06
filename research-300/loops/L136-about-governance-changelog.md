---
loop: 136
phase: 3
title: About / Governance / Changelog
date: 2026-06-06
status: decided
---

# L136 — About / Governance / Changelog

**Loop**: 136 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The brief

Design `/about` and its sub-pages. Editorial values. Sponsorship policy. Version history.

## Why this page exists

Every serious infrastructure publisher needs an About page that the reader can audit. The journalist, the LP, the academic reviewer will look at this page early. They will ask: who is OPENGEM? what does it not do? where does the money come from? what happens if it changes?

The page is not marketing. It is a public commitment ledger.

## The structure (top-level page)

```
+--------------------------------------------------------------------------+
| OPENGEM > About                                                          |
| /about                                                                   |
+--------------------------------------------------------------------------+
| HEADER                                                                   |
|                                                                          |
| OPENGEM is the public macro-accountability ledger for the world         |
| economy — a Bloomberg-grade dashboard for everyone, where every          |
| forecast is open, every number is dated, and every miss is named.       |
|                                                                          |
| Founded 2026. Apache-2.0 code. CC-BY-4.0 data + docs + model cards.    |
+--------------------------------------------------------------------------+
| INDEX                                                                    |
|                                                                          |
|   1. Vision and editorial values                                        |
|   2. Governance and ownership                                           |
|   3. Sponsorship policy                                                  |
|   4. Funding and financial disclosures                                  |
|   5. Team and contributors                                               |
|   6. Version history (changelog)                                        |
|   7. Roadmap                                                            |
|   8. License and attribution                                            |
|   9. Trust commitments                                                  |
|  10. How to contribute                                                  |
|  11. Contact and security                                                |
|                                                                          |
+--------------------------------------------------------------------------+
```

## 1. Vision and editorial values

This section restates L001 in user-readable form. Three musts. Three must-nots. The 12-word pitch:

> A world dashboard that publishes its mistakes so the incumbents cannot hide theirs.

The editorial values list, verbatim:

- **Provenance over polish.** Every number is dated and sourced. Charts that cannot be sourced do not ship.
- **Mistakes in the same place.** When a forecast misses, the post-mortem is published on the same surface, not a footnote.
- **Open by default.** Code Apache-2.0. Data CC-BY-4.0. Model cards open. API public.
- **Machine-readable first.** Every page renders cleanly as JSON. The MCP server is co-equal with the web UI.
- **No black box.** Every forecast lists its model, weights, and replay envelope.
- **Velocity, not secrecy.** The paid tier is for speed, scale, and fit. Never for hidden numbers.

## 2. Governance and ownership

```
+--------------------------------------------------------------------------+
| 2. Governance and ownership                                              |
+--------------------------------------------------------------------------+
| Project owner: OPENGEM Trust (to be incorporated as a US 501(c)(3)      |
|   pending v1 launch). Until incorporation, the project is operated by  |
|   Edgardo Muñoz Najar as sole maintainer, with intent to transfer       |
|   on incorporation.                                                     |
|                                                                          |
| Code repository: github.com/opengem/opengem (Apache-2.0)                |
|                                                                          |
| Editorial board: TBD at v1 launch. Target composition: 3-5 members      |
|   with macro / forecasting / open-data / journalism backgrounds.       |
|                                                                          |
| Voting authority: editorial board has veto over scenario-pack inclusion |
|   and methodology changes. Maintainer has day-to-day operational         |
|   authority. Disputes resolved by published vote.                       |
|                                                                          |
| Forking rights: Apache-2.0 grants unrestricted forking. We commit to    |
|   not litigate or interfere with forks of any kind.                    |
+--------------------------------------------------------------------------+
```

The "trust" framing matters. OPENGEM is not a for-profit. It is a public-interest infrastructure project that may take limited venture-aligned capital but operates under a non-profit governance shell. The page commits to this explicitly so future capital cannot quietly redirect editorial.

## 3. Sponsorship policy

```
+--------------------------------------------------------------------------+
| 3. Sponsorship policy                                                    |
+--------------------------------------------------------------------------+
| OPENGEM accepts sponsorship under three rules:                          |
|                                                                          |
| RULE 1 — Sponsorship is never editorial.                                 |
|   No sponsor may direct what scenarios are published, what indicators   |
|   are covered, what countries are added, or what data sources are       |
|   used. Sponsorship is for infrastructure (servers, data licensing,      |
|   developer time), not editorial direction.                            |
|                                                                          |
| RULE 2 — Sponsorship is disclosed.                                      |
|   Every active sponsor is listed in section 4 with the dollar amount   |
|   and the period. Past sponsors remain listed for 5 years after end.   |
|                                                                          |
| RULE 3 — Sponsorship is not exclusive.                                  |
|   No sponsor is granted exclusive access to data, forecasts, or         |
|   API. The paid tier exists for everyone at the same price.            |
|                                                                          |
| WHAT WE WILL NOT ACCEPT                                                  |
|   - Sponsorship conditioned on editorial coverage.                      |
|   - Sponsorship from entities subject to active US/EU sanctions.       |
|   - Sponsorship that would compromise the open-data commitment.        |
|                                                                          |
| HOW TO SPONSOR                                                          |
|   Email sponsor@opengem.world. Standard sponsorship contract template   |
|   is public: [sponsorship-contract.md].                                |
+--------------------------------------------------------------------------+
```

## 4. Funding and financial disclosures

```
+--------------------------------------------------------------------------+
| 4. Funding and financial disclosures                                     |
+--------------------------------------------------------------------------+
| Current funding (2026):                                                  |
|   Founder bootstrapping: ~$X                                            |
|   No active sponsors at v1 launch.                                      |
|   No grants pending.                                                    |
|                                                                          |
| Operating costs (annual estimate, per R22):                             |
|   Block I:         ~$1,000  (Cloudflare + R2 + small DuckDB Cloud)      |
|   Block II:        ~$3,000                                                |
|   Block IV+:       ~$6,000                                                |
|                                                                          |
| Revenue (none at v1; targeted at Y1):                                   |
|   Free tier: web dashboard, JSON, RSS, MCP (rate-limited).               |
|   Pro tier ($X/mo): API velocity, MCP velocity, alerts, RSS feeds,    |
|                     dashboards embeds.                                  |
|   Team tier ($Y/mo): white-label embeds, calibration reports, SLA.    |
|                                                                          |
| Past sponsors: (none yet)                                                |
|                                                                          |
| Financial transparency: annual disclosure published Q1 of each year.   |
+--------------------------------------------------------------------------+
```

## 5. Team and contributors

```
+--------------------------------------------------------------------------+
| 5. Team and contributors                                                 |
+--------------------------------------------------------------------------+
| Core maintainer: Edgardo Muñoz Najar (Twitter @___, GitHub @___, ORCID) |
|                                                                          |
| Open contributors: github.com/opengem/opengem/graphs/contributors        |
|                                                                          |
| Editorial board (TBD at v1 launch): see governance.                     |
|                                                                          |
| Acknowledgments:                                                        |
|   - Bauer & Mertens (2018) for the term-spread probit replication       |
|   - Caldara & Iacoviello (2022) for the GPR Index                       |
|   - NY Fed for the GSCPI                                                 |
|   - BIS for the CBPOL series                                             |
|   - WTO, BLS, BEA, FRB, OECD, IMF, ECB for the open data substrate    |
|   - Mehrotra et al for BGVAR                                             |
+--------------------------------------------------------------------------+
```

## 6. Version history (changelog)

```
+--------------------------------------------------------------------------+
| 6. Version history                                                       |
+--------------------------------------------------------------------------+
| 2026-06-06   World Dashboard v0.1 (pre-launch, Phase 3 design)          |
|              Loops L001-L145 of 300 produced.                          |
|                                                                          |
| 2026-05-24   CONOPS rev C accepted (R99 rebaseline).                   |
|              17 packages, 183 tests passing.                          |
|              Stratfor-grade e2e demo green.                            |
|                                                                          |
| 2026-04-15   Trade-LATAM v3, Red-Sea v2, Oil-shock v2 packs updated.   |
|                                                                          |
| 2026-03-01   opengem-vintage, opengem-data-bea released.               |
|                                                                          |
| 2026-02-15   opengem-types, opengem-data-base released.                |
|                                                                          |
| 2026-01-15   Project repository created.                                |
|                                                                          |
| [Full changelog with per-package version diffs →]                       |
+--------------------------------------------------------------------------+
```

The changelog is auto-generated from git tags plus per-package changelogs. It includes:
- Code commits (release notes per tagged version).
- Methodology changes (per L135 version history).
- Forecast model retrains.
- Data source additions / removals.
- License changes.
- Governance changes.

## 7. Roadmap

```
+--------------------------------------------------------------------------+
| 7. Roadmap                                                               |
+--------------------------------------------------------------------------+
| 2026-Q3   v1 public launch (dashboard + API + MCP)                       |
|           Tier-V core US + EZ + UK + JP + CA + AUS                       |
|                                                                          |
| 2026-Q4   Block II expansion (40+ Tier-V countries)                      |
|           Forecaster leaderboard public                                  |
|                                                                          |
| 2027-Q1   White-label embeds (Team tier launch)                         |
|           Public API v1.0 GA                                             |
|           MCP server v1.0 GA                                             |
|                                                                          |
| 2027-Q2   First academic citation goal (per L001 12-month horizon)      |
|                                                                          |
| 2028-Q1   Block III: depth + sovereign-grade hosting                     |
|                                                                          |
| 2031-Q1   5-year retrospective                                           |
|                                                                          |
| [Detailed roadmap with milestone gates →]                                |
+--------------------------------------------------------------------------+
```

## 8. License and attribution

```
+--------------------------------------------------------------------------+
| 8. License and attribution                                               |
+--------------------------------------------------------------------------+
| Code:           Apache-2.0                                              |
| Data:           CC-BY-4.0                                              |
| Documentation:  CC-BY-4.0                                              |
| Model cards:    CC-BY-4.0                                              |
| Forecasts:      CC-BY-4.0                                              |
|                                                                          |
| Citation requirement: For academic citation, please use the URN.       |
|                                                                          |
| Trademark: OPENGEM is a project name; we make no exclusive claim.      |
|                                                                          |
| Data source attribution: each indicator page lists its source(s)        |
|   with the original publisher's terms. We honor publisher TOS strictly.|
+--------------------------------------------------------------------------+
```

## 9. Trust commitments

```
+--------------------------------------------------------------------------+
| 9. Trust commitments                                                     |
+--------------------------------------------------------------------------+
| The following are operational commitments enforced by code and          |
| organizational discipline:                                              |
|                                                                          |
| (A) NO RETROACTIVE EDITING                                              |
|     Once a forecast vintage is published, the vintage row is permanent. |
|     If a bug is found, the correction is published as a new vintage     |
|     with a note pointing to the corrected predecessor. The original     |
|     vintage row is never removed.                                       |
|                                                                          |
| (B) PROVENANCE ON EVERY CHART                                            |
|     Every chart has a provenance drawer (L132). CI lint enforces        |
|     presence.                                                           |
|                                                                          |
| (C) METHODOLOGY MANDATORY                                                |
|     Every scenario pack has a methodology page (L135) with 11 sections. |
|     CI lint enforces presence.                                          |
|                                                                          |
| (D) MISS LOG PUBLIC                                                      |
|     Every forecast cell has a public miss log. Largest misses get       |
|     public post-mortems within 30 days.                                 |
|                                                                          |
| (E) FORECAST RE-RUNS PUBLIC                                              |
|     The "Replay this forecast" feature is available on every forecast. |
|     Replay outputs are archived and citable.                             |
|                                                                          |
| (F) SOURCE LINKING, NOT PARAPHRASING                                    |
|     Event stream links to original sources. We do not republish.        |
|                                                                          |
| (G) CHANGELOG TRANSPARENT                                                |
|     Every change to code, methodology, or governance is in the          |
|     changelog. We do not edit history.                                  |
|                                                                          |
| (H) NO PROPRIETARY FORECAST GATING                                       |
|     All forecasts are publicly accessible at the same depth.           |
|     The paid tier is for velocity, not for content.                     |
+--------------------------------------------------------------------------+
```

This is the brand contract. Each commitment links to the operational mechanism (a CI lint, a process, a code module).

## 10. How to contribute

Links to:
- GitHub `CONTRIBUTING.md`.
- Open issues kanban.
- Roadmap of accepting-contributors-for items.
- Editorial board application process (when board exists).
- Submit-a-critique flow for methodology pages.
- Forecaster registration process (for adding your forecasts to the leaderboard).

## 11. Contact and security

```
+--------------------------------------------------------------------------+
| 11. Contact and security                                                 |
+--------------------------------------------------------------------------+
| General contact: hello@opengem.world                                    |
| Sponsorship:     sponsor@opengem.world                                  |
| Press:           press@opengem.world                                    |
| Security:        security@opengem.world (PGP key fingerprint: ___)     |
|                                                                          |
| Vulnerability disclosure policy: 90-day responsible disclosure.        |
|   Acknowledgment within 7 days; published advisory within 90 days     |
|   or earlier upon mutual agreement.                                    |
|                                                                          |
| Mailing list: news@opengem.world (low-volume, monthly).                |
| RSS: /news.rss                                                         |
+--------------------------------------------------------------------------+
```

## What this loop produced

- About page structure: 11 numbered sections.
- Vision/values verbatim from L001 in reader-readable form.
- Governance: project owned by OPENGEM Trust (to be incorporated as 501(c)(3)); maintainer + editorial board.
- Sponsorship: never editorial, always disclosed, never exclusive.
- Financial disclosure: annual transparency.
- Eight named trust commitments (A through H), each linked to operational enforcement (CI lint, code module, or process).
- Changelog auto-generated from git + methodology version history.
- Roadmap quarterly through 2031 (per L001 5-year arc).
- Security: 90-day responsible disclosure, PGP key.

## What comes next

- **L137** designs the API docs page (linked from contribute section).
- **L178** designs the footer + legal patterns.
- **L283** designs the Terms of Service.
- **L284** designs the Privacy Policy.
- **L285** designs the accountability ledger landing page.

## Related

- [[L001-vision-statement]] — vision sourced from this loop
- [[L121-information-architecture]] — /about URL space
- [[L132-provenance-drawer]] — Trust commitment (B) enforced here
- [[L135-methodology-page]] — Trust commitment (C) enforced here
- [[L283-terms-of-service]] — legal frame
- [[L284-privacy-policy]] — legal frame
