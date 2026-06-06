# L292 — Academic outreach plan

**Loop**: 292 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis

Academic outreach is OPENGEM's **highest-leverage credibility move** in the first 18 months. Two academic citations are worth more than 1,000 dashboard views for the long-arc positioning ("cited next to WEO by 2031" per L010). The challenge is that economics academics are conservative consumers of new sources — they need replication packages, methodology rigor, peer review, and stable URLs.

OPENGEM is structurally suited to academic consumption *if* we publish in their format.

## The four academic asks (per OPENGEM page)

Every page that an academic might cite must answer:
1. **What is the citable unit?** A DOI-equivalent permanent identifier.
2. **What is the replication code?** A `replication-package/` link with a single `make replicate` entry.
3. **What is the data lineage?** Inputs traceable to upstream-agency series with vintage timestamps.
4. **What is the calibration evidence?** A scoring summary with reference to the V&V matrix.

The OPENGEM pages that meet all four at launch: `/forecasts/[id]` (with `cite_this_view` tool from L108 MCP), `/methodology/[topic]`, `/accountability`, `/track-record/[indicator]`. The rest will follow.

## The three outreach paths

### Path 1 — Direct researcher outreach

Targeted at 30 macroeconomists who *publish replicable empirical work* in real-time data, vintage discipline, nowcasting, or geopolitical economics:

| Researcher cohort | Why they matter | Outreach |
|---|---|---|
| **Chad Fulton (NY Fed)** | Author of `statsmodels.statespace.DynamicFactorMQ` — OPENGEM's L3 backbone | Single email: "we adopted your library, here's a public benchmark"; offer co-authored case-study |
| **Caldara & Iacoviello (Federal Reserve)** | GPR original authors; OPENGEM extends their methodology | Single email: "OPENGEM-GPR composite back-tests at R²=0.92 against your monthly drop; would you want to validate?" |
| **Bauer & Mertens (FRBSF)** | Recession probit original authors | Replication submission with annotated diff; ask if they'd accept it as a citation in their next NBER working paper |
| **Diebold & Stoughton** | Forecasting density / scoring rules | Submit OPENGEM's scoring methodology as case-study in their pedagogical work |
| **George Diebold and Frank Diebold** | Open-source macroeconometrics | Engage on twitter/x with specific OPENGEM scoring posts |
| **Domenico Giannone / Lucrezia Reichlin / Lippi** | DFM literature | Replication submission |
| **Brookings Hutchins Center economists** | Macro nowcasting publication venue | Pitch a guest blog about the open-substrate model |
| **Federal Reserve research economists at Atlanta, NY, SF, Chicago, Cleveland** | Nowcast methodologies | Specifically: link OPENGEM's daily updates against the Fed bank nowcasts (GDPNow, NY Fed Nowcast, Cleveland CPI) and invite cross-comparison |

### Path 2 — Conference + workshop

| Venue | What to submit | Cadence |
|---|---|---|
| **NBER Summer Institute (Macroeconomics + Forecasting)** | Working paper on the open-track-record discipline | Annual; submit Year 1 |
| **NBER Working Paper series** | Co-authored methodology + replication package | Submit when a model variant reaches publication-grade calibration |
| **Federal Reserve Conference on Macroeconomic Modelling** | Lightning talk + replication kit | Annual |
| **JEEA / Journal of Forecasting** | Short methodology note | Submit in Y2 |
| **MFM (Methodological Frontiers in Macroeconomics) workshop** | OPENGEM dataset + replication | Y2 |

### Path 3 — Replication kit publication

Every Block-I-and-beyond OPENGEM release ships a **replication kit** to:
- arXiv (cross-list econ.GN + cs.CY)
- SSRN (Macroeconomics network)
- Zenodo (with DOI minted for the dataset snapshot)
- IPOL (Image Processing Online) for the methodology articles

The kit format:
```
opengem-vNN/
├── README.md           # cite as: …
├── replicate.sh        # single command to reproduce all figures
├── data-lockfile.json  # SHA-256 of every input source
├── docker/             # container recipe
├── code/               # all model variants
└── figures/            # reproducible
```

## Sponsored chair / endowed gift?

**No, in the first 24 months.** Accepting endowment-style support from a single institution would create reputational dependency in the wrong direction. We accept conference-travel grants for individual researchers using OPENGEM data; we do not accept institutional endowment.

## What this loop produced

- The 4-question academic-credibility checklist
- The 30-researcher targeted outreach list
- The 5-venue conference / workshop submission cadence
- The replication-kit publication discipline
- The "no endowed chair" guardrail

## Related

- [[L271-master-prd]] — academic citation is a v1+ milestone
- [[L286-failure-log-page]] — academic credibility depends on owning the misses
- [[L298-postmortem-template]] — academic-grade post-mortem template
- [[L158-cite-this-view]] (in L146-L180 design batch) — the citation mechanism
