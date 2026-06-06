# L299 — Quarterly retrospective template

**Loop**: 299 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The template

Every quarter on a fixed date (the first Friday after quarter-end) OPENGEM publishes a retrospective at `/retrospective/Q{N}-{YYYY}`. Structure is mechanical. No exceptions.

```markdown
# OPENGEM Quarterly Retrospective — Q{N} {YYYY}

**Period covered**: {YYYY-QN-start} → {YYYY-QN-end}
**Published**: {date}
**Author**: {Edgardo / contributor}

---

## TL;DR (300 words)

What changed in Q{N}. The three most consequential miss post-mortems. The three most successful forecasts. The one product / methodology shift that mattered most. The one thing that broke.

## Forecast scoring — Q{N} summary

### V&V matrix updates

How each cell of the 17-cell V&V matrix moved. Use the same PASS/WARN/FAIL pill format as the dashboard track-record page.

| Country | nowcast | 1Q | 4Q | 2Y | 5Y |
|---|---|---|---|---|---|
| USA | (prev → now) | ... | ... | ... | ... |
| CHN | ... | ... | ... | ... | ... |
| ... | | | | | |

### CRPS by indicator

| Indicator | Q{N-1} CRPS | Q{N} CRPS | Δ vs prior | vs AR(1) |
|---|---|---|---|---|
| gdp_yoy 4Q | ... | ... | ... | ... |
| cpi_yoy 4Q | ... | ... | ... | ... |
| ... | | | | |

### Calibration drift

Plot of PIT calibration over the past 4 quarters. If the 80% band miss rate has drifted >22% over the trailing 4 quarters, we acknowledge it here and reference the methodology change (if any) that addresses it.

## Top 3 forecast misses this quarter

For each: 1 paragraph + link to the full post-mortem.

## Top 3 forecast successes this quarter

For each: 1 paragraph. Specifically when we were ≥1pp from consensus on a relevant indicator and turned out closer to truth.

Critical: this section is **secondary** to the misses section. We celebrate quietly. The misses get prominence because the editorial discipline says so. If we don't have anything genuinely surprising to celebrate, we say so:

> No notable forecast was particularly close to truth this quarter where consensus was meaningfully off. Calibration was solid across the board, but no individual forecast stood out as a contrarian win.

## Methodology changes

| Change | Vintage applied | Rationale | Impact estimate |
|---|---|---|---|
| ... | ... | ... | ... |

Empty if no methodology changed.

## Product changes

| Page / feature | Change | Reason |
|---|---|---|
| ... | ... | ... |

## Operational metrics

| Metric | Q{N-1} | Q{N} | Δ |
|---|---|---|---|
| MAU (dashboard) | ... | ... | ... |
| API requests / day P50 | ... | ... | ... |
| MCP tool calls / day | ... | ... | ... |
| Paid subscribers | ... | ... | ... |
| Adapter uptime (P99) | ... | ... | ... |
| Vintage publication SLA hit rate | ... | ... | ... |

## What broke

Honest list of operational failures, data outages, model failures, security incidents. No-incident quarters say "no notable incidents."

## What's next quarter

A short, honest preview. Specifically: the one milestone we're committed to + the one risk we're aware of.

## Reproducibility — the snapshot

Every retrospective is paired with a SQLite snapshot of the OPENGEM database at the date of publication:

`https://data.opengem.org/snapshots/opengem-Q{N}-{YYYY}.db`

Future researchers can reproduce every chart and number in this document from that snapshot.

## Signed

{author}, {date}.

Comments are open at [GitHub Discussions]({url}).
```

## Why the retrospective is quarterly, not monthly

- **Quarterly aligns with macroeconomic data cadence.** Most major series score on a quarterly basis.
- **Monthly would feel performative.** Quarterly gives space for the calibration plot to mean something.
- **Annual would be too slow.** Calibration drift becomes invisible at annual.

## Why first Friday after quarter-end

- **Friday afternoon UTC** gets weekend reading from European + Asian audiences.
- **First Friday** gives us 5-7 days after quarter-end to score forecasts on the last week of the quarter.

## What we will NOT include

- **No "lessons learned" generic blather.** Concrete facts only.
- **No vendor brag.** This isn't a sponsor announcement.
- **No vague language about "challenging quarter."** Either calibration drifted or it didn't.
- **No retroactive narrative.** We don't rewrite the past to be "predictable in hindsight."

## What this loop produced

- The full quarterly retrospective template
- The "miss-prominent, success-quiet" editorial choice
- The paired SQLite snapshot publication
- The first-Friday-after-quarter-end discipline
- The "no vendor brag" + "no retroactive narrative" guardrails

## Related

- [[L298-postmortem-template]] — individual miss template (this aggregates them)
- [[L008-differentiation]] — the publication discipline
- [[L194-coverage-page]] (in forecast mechanics) — the matrix this updates
- [[L274-kpi-dashboard-meta]] — the metrics this reports against
- [[L297-substack-newsletter-engine]] — newsletter linkage on retrospective week
