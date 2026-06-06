# L187 — Forecast Horizons We Publish

**Loop**: 187 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

OPENGEM publishes forecasts at exactly **five horizons**: nowcast, 1Q-ahead, 4Q-ahead, 2Y-ahead, 5Y-ahead. No others on the public surface. Internally the engine can produce arbitrary horizons; the published set is fixed by policy.

This loop defends the choice, sets cadence rules per horizon, and pins which V&V matrix cells live at which horizon.

## Why exactly five

The "more horizons is better" instinct produces a dashboard with 20 horizon columns nobody can interpret. Five is the number where every horizon answers a *distinct, named question* and every question has a *distinct, defensible methodology*.

| Horizon | Question it answers | Primary user | Methodology family |
|---|---|---|---|
| Nowcast | "What is the current quarter doing, given what's reported so far?" | Trader, policy desk, YouTuber on the news cycle | Mixed-frequency DFM + bridge models |
| 1Q-ahead | "What does next quarter look like?" | Analyst, planner | DFM + ML + small BVAR ensemble |
| 4Q-ahead | "Where do we end up a year from now?" | CFO, sovereign-fund LP, policy maker | Full L3 stack with BMA |
| 2Y-ahead | "Are we still in the same regime in two years?" | Investment committee, strategic planning | TVP-VAR, regime-switching, large BVAR |
| 5Y-ahead | "What's the trend / structural path?" | Sovereign fund LP, pension fund, policy long-view | Stochastic trend, demographic + capital-stock anchor |

Adding a 3Q horizon adds nothing — nobody asks "what does 3 quarters look like" separately from 1Q and 4Q. Adding 10Y is dishonest — nobody is reliably accurate at 10Y in macro, and we are not going to fake it.

## Cadence rules per horizon

The cadence rule answers: how often is each horizon re-forecast?

| Horizon | Re-forecast cadence | Why this cadence |
|---|---|---|
| Nowcast | Daily for D-frequency variables (markets, term spreads), weekly for M-frequency, when new release lands for Q-frequency | Information arrives daily; nowcast staleness is visible |
| 1Q-ahead | Weekly + on every release of a high-information series (e.g. payrolls, CPI, GDP advance) | Sensitive to recent data; weekly is the operating rhythm |
| 4Q-ahead | Monthly, plus quarterly "deep run" with re-estimation | 4Q does not move on daily news; monthly is enough; quarterly deep run aligns with WEO/OECD comparison |
| 2Y-ahead | Quarterly | Moves slowly; quarterly aligns with the V&V matrix evaluation cycle |
| 5Y-ahead | Quarterly | Structural; quarterly is more than enough |

The dashboard shows a "last computed" timestamp next to each horizon's chart, so users see whether they are looking at a fresh nowcast or a quarter-old 5Y curve.

## Which V&V cells live at which horizon

The 17-cell V&V matrix (R08, R99) is concentrated at the operationally-relevant horizons. Restated against the five published horizons:

| Variable | Nowcast | 1Q | 4Q | 2Y (8Q) | 5Y (20Q) |
|---|---|---|---|---|---|
| GDP-real-yoy | C-00 | C-01 | C-03 | C-05 | C-07 |
| CPI-headline-yoy | C-N1 | C-08 | C-10 | C-11 | C-12 |
| Unemployment | C-N2 | C-13 | C-14 | C-15 | — |
| Policy rate | — | C-16 | C-17 | — | — |
| Recession-12m | — | — | C-18 | — | — |

Cells marked "—" are not in scope: 5Y-ahead unemployment and 5Y-ahead policy rate are weakly identified and excluded by policy. The 17 in-scope cells (renamed to include nowcast cells C-00, C-N1, C-N2) are the leaderboard scope.

## Why nowcast is first-class

Older macro forecasting systems treat nowcasting as an awkward cousin — separate model, separate publication, separate UI. OPENGEM treats nowcast as *horizon 0* on the same chart. The chart's leftmost point is the nowcast; immediately to its right is the realised history; immediately to its left (going forward in time) are 1Q/4Q/2Y/5Y. Visual continuity matters: the reader sees the current call without having to navigate.

Practically, this means:

- Nowcast is computed by the same combiner machinery (BMA over L3 variants), with mixed-frequency MIDAS as the dominant variant for high-information cycle (L205).
- Nowcast carries the same `forecast.v1` JSON contract (L181) with `horizon.h=0`.
- Nowcast feeds the **surprise index** (L191) when realised data arrives.

## Why 5Y-ahead is in scope despite weak skill

Some forecasting infrastructures stop at 2Y because skill is empirically near-zero at 5Y for most macro variables. OPENGEM keeps 5Y in scope on three grounds:

1. **Long-horizon LP demand.** Sovereign funds and pension funds make 5-10 year allocations. They need *a* number even if it is wide. OPENGEM publishes wide bands honestly rather than refusing to forecast.
2. **Anchor-of-anchors.** A 5Y point is a sanity check on shorter-horizon forecasts. If the 5Y CPI says 8% but the 4Q says 2% then something is incoherent.
3. **Disciplined publication of low-skill bands.** Publishing 5Y *with appropriately wide bands* is more useful than publishing 5Y *with falsely narrow bands*. The V&V matrix at 5Y demands no skill above climatology; it demands honest calibration. PIT-KS pass at 5Y is the criterion.

We do *not* publish 10Y or longer. The data does not support it and the consumer surface gets cluttered.

## How the dashboard chart renders all five

```
   Past (realised)     │  Forecast (bands)
      │                  │
      │                  │  Nowcast  1Q    4Q     2Y       5Y
   ───┴──────────────────┼───●──────●─────●──────●────────●────►  time
                         │   |       \_    \_    \_       \_
                         │   |  P10-P90 fan widening with horizon
                         │   |
                          ←── "as of 2026-06-06 08:00 UTC"
```

The bands at nowcast are narrow (we know a lot about the current quarter); they widen monotonically to 5Y. Consensus overlays (L190) draw as dotted lines at the same five horizons where overlap exists.

## API contract per horizon

Each horizon is a separate `forecast.v1` JSON object with its own `forecast_id`. The dashboard fetches all five in a single API call:

```
GET /v1/forecasts?country=USA&indicator=GDP-real-yoy&horizons=nowcast,1Q,4Q,2Y,5Y
→ returns array of 5 forecast.v1 objects, each independently replayable.
```

If a horizon is not in scope for an indicator (e.g. policy rate at 5Y), the response includes a `{horizon: "5Y", status: "out_of_scope", reason: "..."}` entry. Honest absence beats false presence.

## Cadence enforcement

The publishing engine (a Dagster job graph) carries a cadence policy per `(indicator, horizon)`. If a horizon's last publish is stale beyond its cadence rule (e.g. nowcast not refreshed for 25 hours), the dashboard chart shows a "stale: 25h overdue" badge and the leaderboard temporarily masks that cell. Staleness is itself a public signal.

## Tier-T treatment

Tier-T countries get the same five horizons but a smaller V&V cell set (only 1Q + 4Q for GDP and CPI). The dashboard shows the bands but tags them with a "tracked-only" badge: no leaderboard inclusion, no historical track record yet, just the forecast. Over time as their vintage history grows, they migrate cells to Tier-V eligibility.

## What we deliberately don't publish

| Not published | Reason |
|---|---|
| 3Q-ahead | Redundant with 1Q and 4Q; no distinct user question |
| 6Q / 12Q | Same — these are between 4Q and 2Y already covered |
| Monthly-horizon forecasts (e.g. "May payrolls forecast") | Outside macro scope; that's BLS-watcher trading territory, not the OPENGEM mission |
| 10Y / 20Y / 50Y | Empirically dishonest; structural models drift faster than 10Y forecasts age |
| Daily intraday | "Not real-time intraday" — explicit must-not from L001 |

## What this loop produced

- The five canonical horizons + the question each answers.
- Cadence rules per horizon.
- V&V cell mapping by `(indicator, horizon)`.
- Reasoning to keep 5Y in despite low skill.
- Stale-cadence enforcement policy.
- Explicit list of horizons we refuse to publish.

## What comes next

- **L188** — bands at each horizon.
- **L205** — mixed-frequency methodology supporting the nowcast.

## Related

- [[L181-forecast-object-schema]] — JSON contract per horizon.
- [[L195-forecast-ui-spec]] — chart rendering.
- [[L205-mixed-frequency-models]] — nowcast machinery.
- [[R08-vv-matrix-detail]] — V&V cells per horizon.
- [[L191-surprise-index]] — fed by nowcast.
