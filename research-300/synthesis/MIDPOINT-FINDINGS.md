# Mid-flight synthesis — three pivotal cost collapses

**Date**: 2026-06-06 (during the 300-loop run)
**Status**: Phase 1 substantially complete; Phase 2, 3, 4, 5, 6 in flight.

---

## The three findings that change the build cost

After Phase 1 (open-source landscape) substantially completed, three findings emerged that each materially reduce OPENGEM's build cost — and together they reduce it by roughly 60-70%.

### 1. Datasette is the moat, not just a tech pick

**Source**: L061-L080 viz/dashboards survey (agent finding).

Simon Willison's Datasette + a per-vintage SQLite snapshot pattern gives OPENGEM:

- Permanent vintage URLs (the foundation of "publishes its mistakes")
- `wget`-able raw data on every page
- Permalinks that paste-share to Substack as fully-functional dataset views
- DuckDB-WASM client-side SQL queries against the open ledger
- Total operating cost: ~$5/mo on Fly.io

Bloomberg / Macrobond / IMF *structurally cannot* publish in this form without breaking their pricing models. OPENGEM has no such constraint. The Datasette+DuckDB-WASM+Parquet substrate is the actual moat — *data so portable the incumbents can't match it* — for $15/mo total ops.

### 2. statsmodels DynamicFactorMQ IS the L3 backbone

**Source**: L031-L045 forecasting OS survey (agent finding).

`statsmodels.tsa.statespace.DynamicFactorMQ` is the NY Fed Nowcasting framework (Bok et al. 2017) implemented natively in Python:

- BSD-3-Clause (clean with our Apache-2.0)
- Maintained by Chad Fulton — NY Fed staff economist, lead author of statsmodels.statespace
- Zero re-implementation: `pip install statsmodels`
- Block I's biggest design risk (build the L3 forecast backbone) collapses to a pip install

This is the single largest engineering-cost reduction in the entire round.

### 3. POLECAT replaces ACLED for 95% of value

**Source**: L021-L030 geopolitical data survey (agent finding).

POLECAT (Cline Center, Harvard Dataverse):

- **CC0** license — public domain
- Weekly cadence
- PLOVER-coded event taxonomy (modern, well-documented)
- 2018-present coverage

ACLED is **YELLOW EULA** — bans republication of derived rows on competing dashboards. POLECAT gives us substantially the same product without the licensing landmine.

Combined with GDELT (free with attribution) and UCDP (CC-BY-4.0), OPENGEM's geopolitical-event substrate is 100% republishable, without paying or risking license churn.

## What these collapse together

| Layer | Old cost (estimated) | New cost |
|---|---|---|
| L3 forecast backbone | 4-6 months building DFM + MCMC + state-space | `pip install statsmodels` + 2 weeks fitting |
| Open-ledger surface | 3 months building custom export tooling | $5/mo Datasette + 1 week setup |
| Geopolitical event substrate | 6 months ACLED commercial negotiation + integration | 2 weeks ingesting POLECAT + GDELT + UCDP |

Total build-cost reduction (rough): **9-12 person-months → 1-1.5 person-months** for these three layers.

## Architectural implications

1. **OPENGEM is now feasible by a single guerrilla developer in calendar 6-9 months**, not 24 months.
2. The **distinctive technical effort** shifts from "build the data plumbing" to "publish the open ledger and build the LLM-grounding MCP surface."
3. The **most leveraged remaining work** is: (a) the dashboard UX (Next.js scaffold built this session), (b) the MCP server surface, (c) the vintage-snapshot publishing pipeline, (d) the editorial discipline that turns the open ledger into a story.

## What this means for Y1-Y5 arc

The Y0 milestone in `L100-vision.md` was Block I rebaseline — foundation, not product. After these three findings, Block I can be **foundation + minimum-viable product** in the same calendar quarter:

| Was | Now |
|---|---|
| Y0 2026: Block I rebaseline only | Y0 2026 H1: Block I + v0.x dashboard + Datasette ledger live |
| Y1 2027: Block I.5 maturation | Y1 2027: v1 dashboard + MCP monetization + first paying customers |
| Y2 2028: Block II expansion | Y2 2028: 5 paying customers, 1 academic citation, first press-cite |
| Y3 2029: regional editions | Y3 2029: $300k ARR, journalism-grade pickup |
| Y5 2031: cited next to WEO | Y5 2031: $3M ARR, cited next to WEO + OECD EO |

The Y5 cited-next-to-WEO end-state from L010 remains plausible — and now it's plausible *earlier in the funnel*.

## Cross-references

- L008 — Differentiation: "publishes its mistakes" → now grounded in Datasette
- L010 — Five-year arc: pulled forward by 6-12 months
- L100 — Vision: rebaseline framing remains correct; product framing strengthens
- L260 — Pricing/MCP: monetization thesis sharpens because L3 is cheap
- L271 (forthcoming PRD) — should bake these three findings into the v1 spec

## Open follow-ups

- Confirm the Datasette + Parquet vintage pattern handles >100GB cleanly (L076-L078 verdict says YES; verify in prototype).
- Confirm DynamicFactorMQ supports mixed-frequency + ragged-edge ingestion at the cadence OPENGEM needs (L032 says yes; verify with NY Fed paper replication).
- Negotiate Harvard Dataverse / Cline Center attribution wording for POLECAT republication (likely trivial — CC0 is permissive).

---

This synthesis goes into `research-300/synthesis/` not `loops/` because it's a cross-cutting digest, not a single-loop artifact. It will be referenced by L300 (the final synthesis) when that agent completes.
