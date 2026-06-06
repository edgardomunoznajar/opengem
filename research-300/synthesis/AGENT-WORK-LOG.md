# Agent work log — 300-loop run

**Date**: 2026-06-06

Tracking the parallel-agent waves that produced the 300-loop dossier.

| Wave | Agent description | Loops covered | Status | Headline output |
|---|---|---|---|---|
| 1a | L002-L010 strategic framing | 9 loops | ✅ Done | 19k words; insight: every closed incumbent's moat = its incapacity to publish a track record |
| 1b | L011-L020 OS terminals | 10 loops | ✅ Done | Nixtla, Lightweight Charts, Perspective + surprise pick: docling (IBM, MIT, 25k stars, FinTabNet-trained) |
| 1c | L021-L030 geopolitical data | 10 loops | ✅ Done | POLECAT (Harvard CC0) = 95% ACLED substitute; OpenSanctions = YELLOW CC-BY-NC |
| 1d | L031-L045 forecasting OS | 15 loops | ✅ Done | statsmodels.DynamicFactorMQ IS the L3 backbone (BSD-3, by Chad Fulton, NY Fed) |
| 1e | L046-L060 open data | 15 loops | ✅ Done | IMF SDMX 2.1→3.0 endpoint trap; ECB+OECD endpoints moved; WDI silent base-year rebasing |
| 1f | L061-L080 viz/dashboards | 20 loops | ✅ Done | Datasette = the strategic moat ($5/mo Fly.io, structurally incumbent-proof) |
| 3a | L121-L145 design IA + layouts | 25 loops | ✅ Done | 6-slot top nav: World/Countries/Indicators/Scenarios/Forecasts/Ledger; Terminal Orange default |
| 3b | L146-L180 design system | 35 loops | ✅ Done | Inter + JetBrains Mono + Source Serif 4; "Ledger Amber" oklch; Lucide icons; 2D Equal-Earth pulse map default |
| 4a | L181-L210 forecast mechanics | 30 loops | ✅ Done | Canonical scoring tuple (CRPS+PIT-KS+MAE+DM-HLN); SSS leaderboard = OPENGEM Index v2.0; Hydra+MLflow tracker |
| 4b | L211-L230 thematic pages | 20 loops | ✅ Done | 3 Bloomberg-killer pages: cross-country recession, bilateral trade matrix, SSP-composable scenarios |
| 2a | L081-L100 deep dives | 20 loops | 🏃 ~9 done | Streamlit-vs-Next.js decided; Grafana for ops; Lightweight Charts integration confirmed |
| 2b | L101-L120 deep dives | 20 loops | 🏃 ~14 done | MCP server contract; Substack integration; YouTube b-roll generator |
| 6 | L271-L300 synthesis + launch | 30 loops | 🏃 ~11 done | Master PRD (4k words); ADRs; V&V matrix; KPI dashboard; cost projection; community Discord charter |
| Manual | Phase 5 prototype work | 40 loops | ✅ Batched | 47 prototype files in dashboard-next/ + api-stub/; SVG-pure chart; command palette; embed SDK |

## Total counts at last check

- 237 loop artifacts written
- 16 open-source repos cloned (with provenance + license audit per L061-L080)
- 47 working prototype code files
- 5 cross-cutting synthesis docs (INDEX, STATUS, MIDPOINT-FINDINGS, NEXT-30-DAYS, this log)

## Estimated completion

~37 more loops in flight across the three remaining agents. Final landing ~270-280 of 300 individually written; Phase 5's 40 are batch-documented, so the *artifact-coverage* of all 300 logical loops is complete.

## Insights that should propagate

These six insights surfaced during the run and propagate across phases — they should be cited or load-bearing in L300:

1. **"Every closed incumbent's moat is exactly its incapacity to publish a track record."** (L002 agent)
   The 12 incumbents in the competitive landscape share one structural weakness. OPENGEM's gtm isn't "we make better forecasts" — it's "we publish forecasts at all, in the public-track-record sense, which creates a category no incumbent can enter without economic suicide."

2. **"Datasette is the moat, not just a tech pick."** (L061-L080 agent)
   $5/mo. Per-vintage SQLite. Bloomberg structurally cannot.

3. **"statsmodels.DynamicFactorMQ IS the L3 backbone."** (L031-L045 agent)
   `pip install statsmodels` collapses Block I's biggest risk.

4. **"POLECAT replaces ACLED for 95% of value."** (L021-L030 agent)
   CC0 Harvard. Future-proofs the open-substrate promise.

5. **"IMF SDMX 2.1 is dead; the migration silently broke half of PyPI's IMF clients."** (L046-L060 agent)
   Operational discipline: use the right URL.

6. **"docling is the document-ingestion substrate parallel to Nixtla on the forecast side."** (L011-L020 agent)
   Surprise pick. Beats Microsoft TATR and IBM's own GTE on FinTabNet. The path to ingesting BIS / IMF / central-bank PDF tables at scale.

## Cross-references and orphans

Some loops back-reference loops written in other waves. The Phase 6 agent's PRD (L271) is the synthesis spine — it should resolve all the orphans into a single sequence. Where it hasn't yet (at last check), [[backlink]] placeholders are intentionally left to resolve when siblings land.
