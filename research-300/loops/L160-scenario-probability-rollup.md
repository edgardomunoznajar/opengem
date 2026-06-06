# L160 — Scenario Probability Rollup Visual

**Loop**: 160 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The decision

**Pick: horizontal segmented stacked bar with weighted-pdf strip and decision-tree expansion.**

Rejected: fan chart (we already use it for forecasts; would confuse), pie chart (it's a pie chart — see below), Sankey (over-decoration for ≤6 branches), violin plot (too noisy).

## Why not a pie chart

Three reasons.

1. **Comparison is hard.** Reading "branch A is 35% and branch B is 28%" off a pie requires angle estimation. Humans are bad at angles.
2. **It scales badly past 4 slices.** Most scenario packs have 5–8 branches.
3. **Pie charts encode percentage as area. The probability of a scenario branch is a single number; we shouldn't recruit two visual dimensions to encode it.**

The horizontal stacked bar wins on all three.

## Why not a fan chart for scenarios

A fan chart shows a continuous probability distribution over time. A scenario rollup shows a discrete branching with assigned probabilities. Different math, different chart. We use the fan for forecasts (L195) and the segmented bar for scenarios.

## The primary visual: segmented bar

```
   Scenario pack: 2026 Q3 Globe Pack
   ──────────────────────────────────────────────────────────
   ┌──────────────┬─────────┬────────┬────────┬──────────┐
   │ Baseline 42% │ Mild 22 │ Hot 14 │ Soft 12│ Crisis 10│
   └──────────────┴─────────┴────────┴────────┴──────────┘
    0           42%      64%     78%   90%        100%

   Cumulative line: ┃    ╱──╱──╱──╱──╱
                    ┃   ╱
                    ┃  ╱
                    ┃ ╱
                    ━━━━━━━━━━━━━━━━━━ 100%
```

- One bar, width = full container
- Each segment width proportional to probability
- Segment color per scenario (categorical, Tol's bright per L148)
- Label shows scenario name + probability
- Below: cumulative reference

## The fan strip (weighted PDF)

Below the bar, a slim strip shows the probability-weighted distribution over a target indicator (e.g., end-of-2026 GDP):

```
   Scenario weights × outcomes → distribution
   ──────────────────────────────────────────
                  ╱──╲
                ╱      ╲___
              ╱            ╲___
            ╱                  ╲
   ───────╱                      ╲────────
   GDP 2026 end:  P10=0.8%  P50=2.4%  P90=3.6%
```

This shows: even though each scenario has a point estimate, when weighted by probability, the implied uncertainty over the target indicator is a continuous distribution. This is the "moving from scenarios to forecast" handoff.

## Drill into a branch

Each segment in the bar is clickable. On click:
- Expands inline to show sub-branches if any (the tree depth)
- Or routes to `/scenario/<id>?branch=<id>` for full detail

```
   ┌──────────────┐
   │ Baseline 42% │  ← clicked
   └──────────────┘
        ↓
   ┌────────────────────────────────────────┐
   │  Baseline                               │
   │  ──────────────────────────────────    │
   │  Sub-branches:                          │
   │   ┌──────────┬───────────┬──────────┐  │
   │   │ B-soft 22│ B-base 12 │ B-firm 8 │  │
   │   └──────────┴───────────┴──────────┘  │
   │   (probabilities are within Baseline)   │
   │                                         │
   │  Outcome assumptions:                   │
   │   • Fed: 2 cuts                          │
   │   • CPI lands at 2.4% Q4                 │
   │   • Unemp stays 4.0%                     │
   │                                         │
   │  [ See full scenario →]                 │
   └────────────────────────────────────────┘
```

## Decision tree expansion (small multiples)

For users who want the tree directly, a "show tree" toggle renders as a dendrogram:

```
                            Globe Pack
                        ╱     │     ╲
                  Baseline  Mild  Hot
                    42%     22%   14%
                    │       │
                ╱──┼──╲     │
              B-s B-b B-f   ...
              22  12  8
```

Width-proportional edges to probability. Hover a node to see its label and conditional prob.

We default to bar, not tree. The bar is the at-a-glance answer; the tree is for the curious.

## Probability sourcing

Each segment's probability comes from one of:
- Methodology-defined (e.g., scenario pack ships with named weights)
- Calibrated via Brier scoring against historical similar packs (combiner output)
- Editorial override (clearly labeled "editorial weight" with attribution)

Each segment's tooltip shows which source.

## Tooltip on segment

```
   ┌─────────────────────────────────────┐
   │  Baseline                            │
   │  Probability: 42%                    │
   │  Source: combiner (calibrated)       │
   │  90% CI on probability: 35% – 49%   │
   │  Assumptions:                        │
   │   • Fed: 2 cuts                      │
   │   • Oil: $80–$95                     │
   │  Implies: GDP 2.1%, CPI 2.4%, U 4.0% │
   │  [ Open this branch ]                │
   └─────────────────────────────────────┘
```

## Color and ordering

- Scenarios ordered by probability descending (left-to-right).
- Baseline always uses neutral-500 (gray-ish) — visually "the default."
- Tail scenarios (Crisis, Boom) use bad and good ends of the diverging palette.
- Mid scenarios use Tol categorical for non-tail variants.

## Showing changes (vintage)

When a scenario pack is updated, the bar can show how the weights have shifted:

```
   Old (Q2 vintage):
   ┌──────────────┬──────┬──────┬──────┬─────┐
   │ Baseline 50%  │ M 20 │ H 12│ S 10│ C 8 │
   └──────────────┴──────┴──────┴──────┴─────┘

   New (Q3 vintage):
   ┌──────────────┬───────┬──────┬──────┬──────┐
   │ Baseline 42%  │ M 22 │ H 14 │ S 12 │ C 10 │
   └──────────────┴───────┴──────┴──────┴──────┘
                      Δ +2     Δ +2    Δ +2    Δ +2

   (baseline declined 8pp, redistributed evenly)
```

A "show diff" toggle overlays the old bar as a hairline reference.

## Single-bar discipline

We resisted the temptation to render a probability bar per indicator (e.g., "P(recession), P(rate cut), P(oil > $100)"). Those are *separate* probability questions. We render them as separate single-stat tiles, not as segments in one bar. The bar's segments must sum to 100% across mutually exclusive states.

## Implementation

- Layer 1: SVG segmented bar via custom render (Recharts can't do annotated stacked horizontal cleanly)
- Layer 2: Density strip via D3 KDE on weighted samples
- Layer 3: Decision tree via D3 `cluster()` layout, lazy-rendered when toggled

## Responsive

- Desktop: bar full-width, density strip below
- Tablet: bar full-width, density strip collapses to a single P10/P50/P90 line
- Mobile: bar stacks vertically (segments become rows), density strip optional

## Print

For PDF tearsheets (L143), the bar + density strip + a compact text table of probabilities renders as one block. The decision tree is omitted from print.

## The accountability arc (forward link)

Every published scenario rollup gets logged. When the time horizon passes, we score:
- Did the realized world land in the branch we assigned highest probability?
- What was our Brier score?
- Did the implied distribution capture the actual indicator?

These results render on the accountability page (L175) as another diff visualization. The scenario rollup → realized world transition is the "did we forecast it" test.

## Export

- PNG: the bar + density strip
- CSV: per-branch probability + outcome assumptions table
- JSON: full scenario tree
- Notebook: reconstructs the bar in Python (L157)

## What we won't ship

- 3D scenario visualizations (Sankey-with-depth, etc.). They're impressive in screenshots and useless in practice.
- Animated probability transitions between vintages on autoplay. Opt-in only.
- "Probability mass over time" (a stacked-area over the forecast horizon). Conceptually conflates "scenario weight" with "forecast distribution." Two charts, not one.
