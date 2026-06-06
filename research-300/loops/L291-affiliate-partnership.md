# L291 — Affiliate / partnership plan

**Loop**: 291 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis

OPENGEM does not run an affiliate program in the conventional sense. Affiliate-driven growth is contraindicated by the editorial discipline: paying for distribution introduces incentive misalignment ("did the affiliate recommend us because we're good, or because they get paid?"). OPENGEM's GTM relies on the open ledger being self-evident, and the brand depending on credibility, not affiliate margin.

What OPENGEM *does* run is a **partnerships** program — non-monetary, mutual-attribution, technical-cooperation arrangements with a small list of strategically aligned organizations.

## Tier-1 partner list (initiated within 90 days of launch)

| Partner | What we offer | What we ask | Format |
|---|---|---|---|
| **Our World in Data (OWID)** | Cross-linking from OPENGEM long-horizon pages (L222, L223, L230) to OWID's underlying data sources | Cross-link from OWID economic-growth + climate pages to OPENGEM forecasts | Reciprocal `<link rel="cite">` + footer cross-mention |
| **Datasette / Simon Willison** | Public showcase as the largest production Datasette deployment in macro | Inclusion in Datasette's "datasette-powered" gallery | Single blog post + maintenance acknowledgement |
| **Nixtla** | Production case study using statsforecast/neuralforecast at scale on macro panels | Co-authored blog post on macro-forecasting benchmarks | Joint technical writeup |
| **Bauer-Mertens (Federal Reserve Bank of San Francisco)** | Replication of their recession-probability methodology as a tracked public series | Light review of OPENGEM's replication faithfulness | Single email; their citation in our methodology page |
| **Cline Center (Univ. Illinois)** | Largest external use of POLECAT for production macro signals | Citation in POLECAT documentation | Mutual citation |

## Tier-2 partner list (initiated within 180 days)

- **arXiv / SSRN** — replication-package landing page convention; if OPENGEM publishes a model variant that ships an open replication kit, link directly from the paper's SSRN landing page.
- **Substack networks** — informal cross-posting agreements with 3-5 macro-Substacks (e.g., Conor Sen, Joey Politano). Not paid syndication; offer free Pro-tier embeds in exchange for one cite of OPENGEM per post that uses our forecast.
- **Macroeconomic Twitter/X micro-influencers** — pre-launch outreach to 10 accounts with >25k followers + active macro discourse; offer them a "founder tier" (free Pro for 12 months) in exchange for honest review.
- **GitHub Macroeconomics community** — engagement with `awesome-quant`, `awesome-economics` repo curators to get OPENGEM listed.
- **MCP plugin galleries** — when Anthropic, OpenAI, Cursor, and Continue.dev publish MCP plugin marketplaces, OPENGEM is in the first cohort listed under "Data & Analytics".

## What we will NOT do

- **No "refer-a-friend" credit.** Distorts user motivation.
- **No commission to Substack-ers for paying conversions.** Same reason.
- **No co-marketing payments to news outlets.** Would corrupt the journalism outreach (L293).
- **No "partner content" articles.** OPENGEM publishes its own findings; partners cite or don't cite.

## Mutual-attribution discipline

Every partner receives a `<link rel="cite">` in the page metadata pointing at their canonical source. In exchange we ask for a single hyperlink + textual attribution in the partner's relevant page. Reciprocity is symmetric, not bilateral-asymmetric.

## Measurement

- Partner-driven referral traffic tracked via Plausible (no UTMs, no per-partner cookie discrimination).
- Quarterly partner check-in (single email).
- Any partner that ceases to cite OPENGEM gets the same OPENGEM treatment as before — partnerships are recognition, not coercion.

## What this loop produced

- Tier-1 + Tier-2 partner lists
- The "non-monetary mutual attribution" model
- Explicit anti-affiliate stance with reasoning

## Related

- [[L007-distribution-thesis]] — partnerships are channel 5 of 6
- [[L008-differentiation]] — the editorial discipline that forbids paid amplification
- [[L292-academic-outreach]] / [[L293-journalism-outreach]] — adjacent outreach tracks
