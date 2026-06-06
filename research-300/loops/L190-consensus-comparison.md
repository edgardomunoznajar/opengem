# L190 — Consensus Comparison: WEO, OECD EO, FRB SEP, ECB SPF

**Loop**: 190 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

Four canonical consensus forecasters are always shown next to the OPENGEM forecast on the dashboard: IMF World Economic Outlook (WEO), OECD Economic Outlook (OECD EO), Federal Reserve Summary of Economic Projections (FRB SEP), and ECB Survey of Professional Forecasters (ECB SPF). This loop pins ingest cadence, horizon-matching rules, and UI surfacing.

These are the four most credible incumbents to compare against. Bloomberg Economics, Goldman GIR, JPM Macro etc. are *priced* — we cannot include them and stay license-clean. The four public/semi-public ones can.

## Why these four

| Source | Geography | Horizons | Frequency | License |
|---|---|---|---|---|
| **IMF WEO** | Global (~190 countries) | Current year + next year + 4 outer years | Twice yearly (April, October) + 2 interim updates | Public, free, attribution required |
| **OECD EO** | OECD-38 + key non-OECD (~50 total) | Current year + 2 forward | Twice yearly (May/June, November/December) | Public, free, attribution required |
| **FRB SEP** | USA only | Year-end values for current + 3 forward years + longer run | Quarterly (March, June, September, December FOMC) | Public, free |
| **ECB SPF** | Euro area aggregate | 1Y + 2Y + 5Y rolling | Quarterly | Public, free |

These four cover ~95% of the consensus-comparison demand for Tier-V Core countries. For non-OECD Tier-V countries (BRA, IND, IDN, etc.) we add WEO and OECD EO; SEP/SPF are silent.

## Ingest cadence

| Source | Ingest schedule | Adapter |
|---|---|---|
| WEO | Within 24 hours of public release. Twice a year (April + October) plus the two interim (January + July) updates as separate releases. | `opengem-data-imf-weo` |
| OECD EO | Within 24 hours of release. Twice a year. | `opengem-data-oecd-eo` |
| FRB SEP | Within 24 hours of FOMC date. Quarterly. | `opengem-data-frb-sep` |
| ECB SPF | Within 24 hours of release. Quarterly. | `opengem-data-ecb-spf` |

Each adapter writes to the same vintage store (`opengem-vintage`) as data series, with `series_id` prefixes:

- `WEO_GDP_USA_2026.04` (WEO forecast of USA GDP, released April 2026 round)
- `OECD-EO_GDP_USA_2026.05` (etc.)
- `FRB-SEP_GDP_USA_2026-Q1` (FOMC round)
- `ECB-SPF_HICP_EA_2026-Q2` (etc.)

Vintaged like any other series. A vintage from April 2024 of the WEO's 2026 GDP forecast is *not* updated by April 2026; the April 2024 publication is preserved.

## Horizon-matching is the hard problem

Each consensus publishes at a different "horizon basis":

- **WEO**: annual average for calendar years.
- **OECD EO**: annual average for calendar years.
- **FRB SEP**: Q4-over-Q4 (and policy rate as year-end level).
- **ECB SPF**: rolling 1Y / 2Y / 5Y from publication date, with annual average and HICP-style year-end values.

OPENGEM's native horizons (L187) are 1Q / 4Q / 8Q / 20Q from the forecast vintage date. These do not line up out of the box.

We resolve horizon matching with a *reconciliation table* stored per-pair-of-publications:

```json
{
  "schema": "opengem.consensus_horizon_match.v1",
  "country": "USA",
  "indicator": "GDP-real-yoy",
  "opengem_horizon": "4Q",
  "opengem_base_period": "2026-Q1",
  "opengem_scoring_period": "2027-Q1",
  "consensus_alignments": [
    {
      "source": "WEO",
      "vintage": "2026.04",
      "consensus_value": 2.10,
      "consensus_basis": "annual_average_2026",
      "alignment_method": "annual_average_to_yoy_q1",
      "alignment_note": "WEO 2026 annual avg → compare to OPENGEM 2027-Q1 YoY; approximate but standard"
    },
    {
      "source": "FRB-SEP",
      "vintage": "2026-Q1",
      "consensus_value": 2.20,
      "consensus_basis": "Q4-over-Q4-2026",
      "alignment_method": "q4_over_q4_to_yoy_q1",
      "alignment_note": "FRB SEP Q4/Q4 = OPENGEM 2026-Q4 YoY (one quarter prior to OPENGEM target); reported as adjacent comparison"
    }
  ]
}
```

The reconciliation honestly flags *approximate* matches with the note explaining what was done. The dashboard chart hovers over a consensus dot to show the alignment note. No silent conversion.

When alignment is impossible (e.g. OPENGEM publishes 8Q but FRB SEP only covers current year + 2 forward), the consensus is shown as "out of scope at this horizon" with an explicit absence marker. Honest absence > false presence.

## How the consensus overlay surfaces on the chart

The forecast chart (L195) shows the OPENGEM forecast as a fan; the consensus overlay shows each of the four sources as a marker at their nearest matching horizon:

```
       OPENGEM forecast (fan)
              |
   ─────●─────●─────●─────●─────●────
        nowcast 1Q  4Q  2Y  5Y
                         |
                         ◆ WEO     (annual avg ↔ 4Q yoy approximation)
                         ▲ OECD EO (annual avg ↔ 4Q yoy approximation)
                         ■ FRB SEP (Q4/Q4 ↔ 4Q yoy adjacent)
                         ★ ECB SPF (where applicable for euro area)
```

Each marker has a tooltip with:
- The exact consensus value.
- The consensus vintage date.
- The horizon-match method + alignment note.
- A link to the source publication.

## Comparison view

A secondary view ("vs. consensus" tab) shows a table:

```
Forecast: USA Real GDP YoY, target 2027-Q1, as of 2026-06-06

Source         Value   Vintage      Δ vs OPENGEM   Confidence       Horizon match
OPENGEM L3 BMA  2.18%  2026-06-06    —              80%: 1.04-3.28%  exact
IMF WEO         2.10%  2026-04-22   -0.08 pp       point only        annual avg ≈
OECD EO         2.05%  2026-05-29   -0.13 pp       point only        annual avg ≈
FRB SEP         2.20%  2026-03-19   +0.02 pp       80%: 1.6-2.8%     Q4/Q4 adj
ECB SPF         n/a    —             —              —                n/a (US-only)
```

Sorted by `Δ vs OPENGEM`; the dashboard cell shading is sign-aware (green for close, orange for big gap).

## The "where consensus was wrong, OPENGEM was right" panel

A retrospective panel pairs each consensus' published forecasts with their realised outcomes, and ranks them. This is the "track record" view. The dashboard surfaces:

```
2025-Q1 realised: USA Real GDP YoY = 2.85%
─────────────────────────────────────────────────
Forecast (as of 2024-Q1)         Error
OPENGEM L3 BMA  2.6%             -0.25 pp ✓
IMF WEO         2.1%             -0.75 pp ✗
OECD EO         2.0%             -0.85 pp ✗
FRB SEP         2.3%             -0.55 pp
```

The same retrospective is computed for *every* forecast we have published, building the cumulative track record (L184 leaderboard, L200 failure log).

## Ingest reliability

Each consensus has known release-day gotchas:

- WEO releases the database on the same day as the headline narrative report, but the *Excel database file* is sometimes delayed by 6-12 hours. The adapter retries every 30 minutes for 24 hours, then alerts.
- OECD EO publishes both a "annex tables" PDF and a SDMX-formatted dataset. The SDMX dataset is canonical.
- FRB SEP releases the dot plot at FOMC; the *individual projection medians* are in the PDF. The adapter parses the PDF table.
- ECB SPF data is published on the ECB SDW with a standard dataflow ID; trivial to fetch.

Adapter test coverage requires sample mock responses for at least the most recent release per source. CI re-tests on every release ingestion.

## What about Bloomberg consensus

Bloomberg Economics' consensus survey is paywalled. We do not include it. We also do not include Reuters Polls, Consensus Economics, or buy-side desk forecasts. The boundary is *publicly available with redistribution-permitting license*. That is the contract.

This means the comparison panel is honest about what it can and cannot show. The dashboard footer notes: "Bloomberg, Reuters and Consensus Economics excluded due to license. To compare, see [methodology page]."

## What this loop produced

- The four canonical consensus sources fixed.
- Ingest cadence per source.
- Horizon-match reconciliation schema with explicit alignment notes.
- Chart overlay UI sketch.
- "vs. consensus" tab spec.
- Retrospective track-record panel.
- Explicit exclusion of paywalled sources.

## What comes next

- **L191** — surprise index built on consensus baselines.
- **L195** — full forecast chart UI.

## Related

- [[L181-forecast-object-schema]] — `consensus_overlay` block.
- [[L191-surprise-index]] — uses consensus as the baseline expectation.
- [[L195-forecast-ui-spec]] — chart rendering.
- [[L184-leaderboard-ranking]] — leaderboard scores OPENGEM vs these four.
- [[R99-synthesis]] — V&V matrix benchmarks include WEO and OECD EO.
