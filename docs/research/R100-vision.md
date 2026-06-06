# R100 — Vision: The 5-Year Arc

| Field | Value |
|---|---|
| Document ID | OG1-RES-100 |
| Revision | A (vision draft 2026-05-24) |
| Date | 2026-05-24 |
| Status | **Aspirational — not part of Block I commitments.** |
| Purpose | Articulate where OPENGEM could go beyond the R99 rebaseline, to test whether Block I's discipline serves a worthy long arc. |

> Per program-owner direction "dream big," this document deliberately ignores resource constraints to ask: **what is OPENGEM at its full unfurling?** The rebaseline (R99) builds the foundation. This document asks what gets built on it.

---

## 1. The thesis

The world economy is forecast by a small cartel. Their forecasts are sold, cited, used to allocate trillions in capital and to justify policy. Almost none of them are publicly scored over time. Almost none of them are interrogable. Almost none of them admit their density. None of them are owned by the people who consume them.

**OPENGEM at its full unfurling is the public macro-accountability ledger.** It produces a sovereign-grade economic forecast and scenario engine, owned by a single private operator, but fully open in code, data, and method. Every forecast it has ever published is permanently stored, scored, and indexed. Every change in method is version-pinned. Every benchmark is named. It does not pretend to be more accurate than the incumbents at IOC — it just **never lies about how accurate it is.**

That asymmetry is the moat. The incumbents *cannot* publish their full track record without exposing their margins. OPENGEM, having no margins to protect, can. Over a long horizon, **a system that publishes its mistakes is harder to discredit than a system that hides them.** This is the lesson of climate models vs. opinion polls vs. macroeconometric models: the systems that survive a generation are the ones who survive their failures publicly.

## 2. The 5-year arc

### Year 0 — 2026: Block I (R99 rebaseline)

Tier-V OECD-26 + Situation subsystem. Vintage discipline. L3 workhorse. Open code. Personal use. Private agentic consumer (oblique-suite integration). **Foundation, not product.**

### Year 1 — 2027: Block I.5 — *Maturation*

- First full year of vintage-correct backtests with the new V&V matrix on Tier-V.
- Self-archive for Tier-T countries enters its second year. Some Tier-T countries can now produce 4Q backtest pairs.
- Public dashboard launched as `opengem.org` (or similar). Read-only for outsiders. No marketing.
- MCP server live for oblique-suite integration.
- Monthly **public model card** publication ritual begins. Each card includes accuracy results, drift detection, what changed in the model.

### Year 2 — 2028: Block II — *Width*

- **Coverage**: ~40 Tier-V countries (some Tier-T graduates as self-archive matures into 2y of vintages).
- **Variables**: add sectoral GVA (industry / services / agriculture splits where available), trade-balance components, current-account, fiscal balance.
- **L1 narrative cores**: add Australia, UK, euro-area aggregate. Now 4 country cores, all narrative-grade. Each has its own model card and identification choice document.
- **Climate-economy coupling** (Block III preview): integrate ENTSO-E + EIA + AEMO electricity grids; first emissions-to-output IRFs.
- **Public scoring vs. major incumbents**: publish quarterly comparison vs. WEO + OECD EO + (if access path resolves) Consensus.

### Year 3 — 2029: Block III — *Depth + sovereignty*

- **Sovereign forecast hosting**: offer OPENGEM as a service to small countries that don't have their own model (Pacific Islands, small Caribbean states, small African economies). Free or marginal cost. Their data ingestion adapters become Tier-V additions.
- **Custom topic model on news flow** (Bybee-Kelly-Manela-Xiu style) live. Daily news-attention covariates feed L3.
- **Custom geopolitical event model** built on GDELT + ACLED, replacing the wrap on Caldara-Iacoviello GPR with an own-built index that updates daily and is itself a scored forecast.
- **Forecast-of-the-leaderboard meta-model**: predicts when OPENGEM itself is likely to be wrong, based on regime detection and structural-break indicators.

### Year 4 — 2030: Block IV — *Public goods*

- **OPENGEM dataset published as a standard** — every other open-source economic forecaster can drop into the data layer and start. Vintages and benchmark forecasts as a service. Becomes the M-competition reference standard.
- **Annual "State of the Macro" report** published, citing OPENGEM's own track record, calling out incumbents' track records (with attribution), naming both winners and losers.
- **University course materials** built around OPENGEM. Curricula in graduate macro and forecasting use it as the live teaching laboratory.

### Year 5 — 2031: Block V — *Reflection*

- Five-year retrospective on what the public-leaderboard discipline produced. Did OPENGEM beat consensus on Tier-V over 5y? Did it become a citation standard? Did it influence any incumbent's transparency? Honest accounting either way.
- Decision point: continue private, fork to a non-profit foundation, hand off to a university, or sunset cleanly.

## 3. What this requires of Block I

The 5-year arc imposes design constraints that go past R99:

| Constraint | Reason | Block I must |
|---|---|---|
| Every forecast is preserved indefinitely | Public accountability | Storage architecture must not have a "rotate after N days" path |
| Every model card is publishable | Public reasoning | Model card generation is a first-class pipeline output, not a manual artifact |
| Every change is version-pinned | Public reproducibility | Hash triplet enforcement at the API layer |
| The leaderboard is open code | Public trust | Ranking algorithm itself in the public repo with its own model card |
| External users must work | Future sovereignty hosting | API design accepts non-self consumers from day 1 |
| Data is sovereign-grade | Future country adoption | National-statistics-agency ToS compatibility is a hard requirement |
| The system must outlive the maintainer | Public good ambition | Bus factor mitigation is non-negotiable |

These constraints are **already in the R99 rebaseline**. The arc didn't *cause* the constraints; it **validates** them.

## 4. The wide jobs-to-be-done OPENGEM eventually does

| Year | Job-to-be-done | Customer / user |
|---|---|---|
| 0 | Personal density forecasts for self-use | Self |
| 0 | Agentic input for oblique-suite | Self |
| 1 | Independent benchmark of my own previous economic intuitions | Self |
| 1 | Independent benchmark of consensus | Anyone reading the dashboard |
| 2 | Operational forecast for small policy shops who can't afford GEM/NiGEM | Independent analysts |
| 2 | Calibration reference for academic forecasters | Macro academics |
| 3 | Sovereign-grade forecasting infrastructure for small economies | Small national stat agencies |
| 3 | Public scorekeeper of incumbents | Journalists, regulators |
| 4 | Standard dataset / benchmark suite | Forecasting researchers worldwide |
| 4 | Teaching laboratory | Universities |
| 5 | Five-year retrospective; possibly the longest-running public-scored multi-country forecast | The general public |

The point: **Block I is not built for the year-0 use case alone.** It's built so the year-3+ use cases are reachable without re-architecting. The R99 rebaseline preserves that reachability.

## 5. Where the dream collides with reality

It's worth saying clearly what could break this arc:

- **Year 1 V&V matrix fails badly.** If Tier-V doesn't beat anything on 4Q GDP density, the public-accountability framing becomes "OPENGEM publishes its mistakes; here are many." That's fine — that *is* the value proposition. But if the failure is wholesale (e.g., 0/8 cells clear), the path forward is honest re-baseline, not pretending.
- **FRED-substitution adapter cohort proves brittle.** Five US agencies, each with their own API quirks, each rotating their schemas. Maintenance burden. Could become the actual scaling constraint.
- **Bus factor of 1 catches up.** Five years is enough time for life to intervene. Mitigation through doc-as-code is necessary but not sufficient. Year-2 should reckon with handoff / co-maintainer recruitment.
- **The hosted-sovereignty year-3 idea doesn't have demand.** Small economies may not want to outsource forecasting to a private project. Diplomatic complexity. Skip if it doesn't naturally materialize.
- **Incumbent counterattack.** If OPENGEM ever becomes large enough to threaten Oxford Economics / NIESR / Moody's revenue, expect a response (better marketing, free tiers, IP claims). Block IV is when this likely shows up. The defense is *track record* — five years of public scoring is hard to outflank.
- **Public-accountability culture shifts.** If the macro forecasting profession becomes more public-scored in general, OPENGEM's moat narrows. But that's a *win for the world*, even if not for OPENGEM specifically. Acceptable failure mode.

## 6. The single sentence

OPENGEM is a personal-scale, public-accountability macroeconometric forecasting system whose Block I builds the foundation for a five-year arc toward becoming a sovereign-grade open forecast infrastructure, accountable to its own public track record, owned by no institution, and irreducibly more honest than the systems it eventually displaces.

That sentence is aspirational and may not survive contact with year 1's data. But it is what the rebaselined Block I is designed to make *possible*, not what it is *required to deliver*.

---

*End of R100 — Vision Rev A.*
