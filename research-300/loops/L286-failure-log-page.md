# L286 — Failure-Log Page: Format for Individual Miss Post-Mortems

**Loop**: 286 / 300
**Phase**: 6 — Synthesis + launch
**Date**: 2026-06-06

---

## The thesis of this loop

[[L285]] specified the accountability ledger landing page. This loop specifies the *individual post-mortem* page that any miss-entry links to — `/postmortem/[slug]`. The page format inherits the [[L200]] schema and the [[L298]] template; this loop is the *presentation* layer specification. How the page reads, how it loads, how it cross-links, how it preserves the original forecast context, and how the team writes new entries without breaking the discipline.

A post-mortem is not a press release. It is forensics. The format is austere: what we forecast, what happened, what we got wrong, why, what we changed, did the change work. No marketing prose, no exculpatory framing, no "lessons we want to share with our valued community." The format prevents drift toward PR-speak; the template forces concrete language.

---

## The page URL contract

`/postmortem/[slug]` where slug follows the schema from [[L200]]:

```
{country-iso3}-{indicator-key}-{vintage}[-{horizon}][-{miss-class}]

examples:
/postmortem/usa-gdp-2025q2
/postmortem/deu-cpi-2025q1
/postmortem/jpn-policy-2024q4-2q
/postmortem/recession-soft-landing-prob-2024-scenario-miss
```

The slug is permanent. Once assigned, it never changes. Even if we rewrite the indicator-key in our internal taxonomy, the URL stays.

---

## Page layout

Six sections plus header + footer, in order:

### Header

```
[Country flag] [Country name] [Indicator] [Horizon] [Vintage]

OPENGEM forecast: {forecast_point}% (P10-P90 = {p10}% to {p90}%)
Realized: {actual}%
Miss: {miss_pp} pp  ({inside_or_outside_p10_p90})
Miss class: {miss_class}
Post-mortem published: {date}
```

Visually: the same density-first style as the rest of the dashboard. Header is dense, no decorative graphics. The reader has all the relevant numbers in 5 seconds.

### Section 1 — "What we forecast" (≤200 words)

A narrative restatement of the forecast at vintage time. Includes:

- The forecast point, P10, P90.
- The methodology badge (model name + version).
- A *link to the original forecast object* preserved at its original URL.
- The original chart, rendered as it was at vintage time (not rerendered with current data).

This section anchors the post-mortem in what was actually published — not a summary, not a paraphrase. Original artifact.

### Section 2 — "What actually happened" (≤200 words)

The realized data point, vintage-stamped. Includes:

- The realized value, the date the realized data was published, the source.
- The z-score from P50.
- A side-by-side chart showing the forecast bands and the realized trajectory.
- A note on whether *consensus also missed* (Bloomberg Economics, WEO, OECD EO, FocusEconomics) — if yes, we say so; if no, we say so. Both directions are brand-positive (honesty signal).

### Section 3 — "What we got wrong" (≤500 words)

The diagnostic walk-through. Specifically:

1. Which inputs were available at vintage time but did not load enough signal into the model?
2. Which inputs were *not yet visible* at vintage time but would have changed the call?
3. Did the BMA combiner weight a weak variant too heavily?
4. Did consensus also miss in the same direction? If so, the miss is partly structural to the data environment; if not, it's OPENGEM-specific.

This section is written by the forecasting lead (founder at v1). It is not edited for narrative; it is edited for accuracy.

### Section 4 — "Why we got it wrong" (≤500 words)

Diagnostic in plain prose. State the model failure mode in technical language but accessible to a numerate reader. No blame on individuals.

Style guide for this section:

- Lead with the structural cause, not the proximate cause. "The DFM under-weighted services consumption" not "we should have re-trained sooner."
- Name the model failure type using the [[L200]] taxonomy.
- Reference any prior misses that share the same root cause. If this miss is a recurrence, acknowledge it explicitly.
- If we genuinely don't know why, say so. ("This miss is partially diagnosed; the model failure is consistent with a regime change in [variable], but we have not yet isolated which factor drove it.")

### Section 5 — "What we changed" (any length, structured)

A list of concrete actions. Each action must link to a GitHub PR or issue. No vague "we will be more careful."

```
1. Increased BVAR prior tightness on services-consumption coefficient.
   PR: github.com/opengem/opengem-1/pull/452
2. Added employment-to-population ratio as DFM factor.
   PR: github.com/opengem/opengem-1/pull/453
3. Documented the miss as a teaching example in the methodology guide.
   PR: github.com/opengem/opengem-1/pull/454
```

If an action is owned but not yet shipped, link to the issue tracking it. The reader can see whether we followed through.

### Section 6 — "Did the change work?" (filled in N≥4 quarters later)

Initially blank, with a placeholder: *"Will be updated at {next-review-date} after N=4 quarters of post-fix forecasts."*

Updated quarterly. The team adds:

- Has the miss class recurred? (yes/no)
- What does the PIT plot look like now?
- What does the leaderboard rank look like for this (country, indicator, horizon) cell?
- A brief paragraph (≤100 words) on whether the fix held.

This section turns the post-mortem from a one-time confession into a *continuous accountability artifact*. The post-mortem is never "done"; it accumulates evidence that the change worked (or didn't).

### Section 7 — "Lessons learned" (≤200 words)

A bulleted summary that other forecasters could carry away. Style: terse, not preachy.

```
- Q1 2024 vintage data missed the labour-market acceleration that became
  visible Q2-Q3.
- DFM factor set was static; needed online refit on emerging structural break.
- Online-refit triggers should be tied to a variance-shift detector,
  not a calendar.
```

### Footer

```
─────────────────────────────────────────────────────────
Reviewed by: {founder}, {external-reviewer}
Published: {date}
Last quarterly update: {date}
Cite this post-mortem: opengem.com/postmortem/{slug}#bibtex

Discussion: github.com/opengem/accountability-ledger/discussions/{N}

Related post-mortems:
  - Similar miss in {other-country} {indicator}: /postmortem/[slug]
  - Prior miss in same series: /postmortem/[slug]

Forecasts since fix (current vintage):
  {current forecast point + bands}
  Methodology: /methodology/{model}
─────────────────────────────────────────────────────────
```

The footer cross-links to:

1. The reviewer signoff (founder is always one; external is a community-confirmed-miss reporter or advisory board member).
2. The publication and last-update dates.
3. A cite-this-postmortem BibTeX block.
4. Discussion link on GitHub Discussions.
5. Related post-mortems (other countries with the same miss type, prior misses on the same series).
6. The *current* forecast for the same (country, indicator, horizon) — readers should see what we're predicting now, contextualized by our prior miss.

---

## The writing discipline

Three style rules for the writer:

1. **Prefer concrete over abstract.** "The DFM under-weighted services consumption" beats "we underestimated the strength of the services sector."

2. **Name the model failure type.** Use [[L200]] taxonomy: direction miss / magnitude miss / calibration drift / scenario miss / replay failure. This makes posts comparable across misses.

3. **No exculpation.** Do not write "in retrospect, this was hard to predict." Either it was hard to predict (acknowledge as a structural feature of the problem) or we should have predicted it (acknowledge as our failure). Avoid the middle ground that reads as defensiveness.

Three style rules for the editor:

1. **Strip marketing language.** Any phrase that sounds like a press release ("we remain committed to," "valued community," "lessons we want to share") gets cut.

2. **Verify every claim links somewhere.** A vague claim ("we improved the model") without a PR link gets rejected.

3. **Cross-check against the original forecast object.** Section 1's numbers must match the preserved forecast object exactly.

---

## The publication cadence

Per [[L200]] section 8 + [[L285]] section "edit discipline":

- **Detection** is automatic. The forecast-scoring pipeline flags a miss within 24h of realized data landing.
- **Acknowledgment** is required within 48 hours of detection. A stub post-mortem with `post_mortem_published_at: null` and the badge "post-mortem pending" appears at `/postmortem/[slug]`.
- **Publication** is required within 30 days of detection. If we miss the 30-day deadline, the "post-mortem overdue" badge appears on the misses table (visible to everyone).
- **Quarterly update** is required for section 6 starting N=4 quarters after publication.

---

## Cross-linking from forecast detail pages

Per [[L271]] section 5.5, the forecast detail page links to:

```
This forecast object has been scored against realized data.

[Inside band ✓ | Outside band — miss recorded]

If miss: link to /postmortem/[slug]
If inside band: "Inside the 80% confidence interval. Scored: {date}."
```

A user reading any forecast immediately sees whether it was right or wrong. No need to navigate to `/accountability` separately. The accountability is *in-context*.

---

## What a typical post-mortem looks like (excerpt)

```
[Header]
🇺🇸 USA · GDP (real, YoY) · 4Q horizon · 2025-Q2 vintage

OPENGEM forecast: 1.4% (P10-P90 = 0.6% to 2.2%)
Realized: 2.6%
Miss: +1.2 pp (outside band)
Miss class: magnitude miss
Post-mortem published: 2025-08-12

[Section 1]
At vintage 2025-Q2, we forecast US GDP growth 4 quarters ahead at 1.4% YoY,
with an 80% interval of 0.6% to 2.2%. The forecast came from our L3-BMA
ensemble (Nixtla neuralforecast component-weighted 0.41, BVAR-baseline
weighted 0.32, DFM weighted 0.27). [Link to original forecast object.]

[Section 2]
Realized GDP growth for 2026-Q2 came in at 2.6% YoY (BEA, advance estimate
released 2025-04-25, subsequently revised to 2.55% in the second estimate).
Bloomberg Economics forecast 1.8% (also outside their reported 90%
interval). WEO October 2024 projected 2.1%. OECD EO November 2024 projected
2.0%. Both consensus forecasts missed, but in the same direction as OPENGEM
and by smaller magnitude.

[Section 3]
The DFM factor weighting under-weighted services-consumption acceleration.
The L3 neuralforecast picked up some of the surprise (its individual point
was 1.7% before the BMA combiner pulled it down toward the more pessimistic
BVAR). The BMA combiner's weighting did not reflect the BVAR's structural
under-performance on this series during 2024-2025.

[Section 4]
The structural cause was a regime shift in services-sector wage growth
that the static DFM did not detect. The static DFM was last trained on
data through 2024-Q1; the services regime shift became visible in
2024-Q3/Q4. We should have triggered an online refit when the
employment-to-population ratio crossed its prior 3-year peak, but our
trigger logic was calendar-based.

[Section 5]
1. Increased BVAR prior tightness on services-consumption coefficient.
   PR #452, merged 2025-07-15.
2. Added employment-to-population ratio as a DFM factor with online
   refit trigger. PR #453, merged 2025-08-01.
3. Switched DFM training-trigger from calendar-based to variance-shift
   detector. PR #454, merged 2025-08-10.

[Section 6]
[Will be filled in at 2026-08-10 after N=4 quarters of post-fix forecasts.]

[Section 7]
- Q4 2024 services-consumption acceleration was detectable in
  employment-to-population ratio data available 2024-Q4.
- Calendar-based DFM refit triggers fail when structural breaks are
  off-calendar. Variance-shift detectors are more responsive.
- BMA combiner weights should sanity-check against extreme single-model
  outcomes; an under-performing model dragging the combiner down on a
  high-stakes call is a known anti-pattern.

[Footer]
Reviewed by: founder, advisory board member [name]
Published: 2025-08-12
Last quarterly update: 2026-02-12 (Q4 2025 review)
Cite this post-mortem: opengem.com/postmortem/usa-gdp-2025q2#bibtex

Discussion: github.com/opengem/accountability-ledger/discussions/47

Related post-mortems:
  - Similar miss in 2024-Q2 UK GDP: /postmortem/gbr-gdp-2024q2
  - Prior US GDP miss: /postmortem/usa-gdp-2023q1

Forecasts since fix (current vintage):
  USA GDP 4Q-ahead (2026-Q4 vintage): 2.1% (P10-P90 = 1.4-2.8%)
  Methodology: /methodology/dfm-l3-bma-v3.2
```

This is what a good post-mortem looks like. Concrete, specific, linked, free of exculpation.

---

## What this loop produced

- Page URL contract + permanent slug discipline.
- Six-section layout with word-count budgets and content rules per section.
- Editorial style rules for writer + editor.
- Publication cadence (48h ack, 30d publish, quarterly section-6 update).
- Cross-linking discipline from forecast detail pages.
- A concrete worked example.

## What comes next

- **L298** — the literal template files (Markdown + YAML frontmatter) per this spec.
- **L285** — the accountability ledger page surfaces these post-mortems.

## Related

- [[L008-differentiation]] — promise 2 → this page operationalizes
- [[L200-failure-log]] — Phase 4 spec → page presents
- [[L285-accountability-ledger-spec]] — landing page → individual entry pages
- [[L298-postmortem-template]] — the literal template
- [[L271-master-prd]] — section 5.5 references this page
