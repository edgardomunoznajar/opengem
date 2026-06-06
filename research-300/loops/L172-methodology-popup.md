# L172 — Methodology Pop-Up Contract

**Loop**: 172 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

Every chart in OPENGEM has a methodology pop-up. The pop-up is the contract that says: this number isn't magic; here's how it was made; here's what could go wrong with it.

This is the trust differentiator. Bloomberg shows a number. OPENGEM shows a number plus how it was made plus where it could be wrong.

## Trigger

Every chart has a small `info` icon (Lucide #28) in the toolbar:

```
   ┌────────────────────────────────────────────┐
   │  USA CPI Forecast (4Q ahead)        ⓘ  ⋮  │
   │  ───────────────────────────────────────  │
   │                                              │
   │     [chart]                                  │
   │                                              │
   └────────────────────────────────────────────┘
```

Click `ⓘ` → opens methodology Popover (per L150).

Same accessible affordance: `?` key when the chart is focused.

## The popover (preview level)

```
   ┌──────────────────────────────────────────────┐
   │  Methodology: Combiner v4.2 + DFM             │
   │  ──────────────────────────────────────────  │
   │                                                │
   │  This forecast blends two models:              │
   │   • Bauer-Mertens (40%) — yield-curve-based   │
   │   • Cleveland-style DFM (60%) — short-term     │
   │                                                │
   │  Weights calibrated against historical CPI    │
   │  surprise. Last calibration: 2026-Q1.         │
   │                                                │
   │  Data sources:                                 │
   │   • FRED (CPIAUCSL, daily)                    │
   │   • Cleveland Fed daily inflation index       │
   │   • Treasury yield curves (daily)             │
   │                                                │
   │  Refresh cadence: daily                        │
   │  Last refreshed: 2026-06-04 14:30 UTC         │
   │  Vintage: 2026-06-04                           │
   │                                                │
   │  Known caveats:                                │
   │   ⚠ Shelter component lags 6 months            │
   │   ⚠ COVID-period (2020-2022) weighted half     │
   │                                                │
   │  [ See full methodology →]                    │
   │  [ Open in notebook →]                         │
   │  [ Cite this view →]                           │
   └──────────────────────────────────────────────┘
   max-width: 480px
```

The preview level fits in the popover. Five sections, every one mandatory:

1. **Title + version**: "Combiner v4.2 + DFM" — the model identifier
2. **Components and weights**: which models, what proportion
3. **Data sources**: what feeds in
4. **Refresh + vintage**: when it last ran
5. **Caveats**: what could go wrong (≥1 caveat, mandatory)
6. **Links**: full methodology, notebook, cite

## The full methodology page (drilldown)

Click "See full methodology →" → routes to `/methodology/<id>`:

```
   ┌────────────────────────────────────────────────┐
   │  ← Back                                          │
   │                                                  │
   │  Combiner v4.2 + DFM                            │
   │  Used in: USA CPI Forecast (4Q ahead), and 12   │
   │  other indicators across 7 countries.            │
   │  ──────────────────────────────────────────    │
   │                                                  │
   │  ## Overview                                     │
   │  Two paragraphs of plain-language overview.      │
   │                                                  │
   │  ## Components                                   │
   │  Table of components with weights and links.     │
   │                                                  │
   │  ## Data sources                                 │
   │  Full list with refresh cadence, license.        │
   │                                                  │
   │  ## Math                                         │
   │  Equations (KaTeX).                              │
   │  Code snippet (Python, runnable).                │
   │                                                  │
   │  ## Backtest                                     │
   │  Calibration plot.                               │
   │  CRPS, MAE over horizon × country.               │
   │  Comparison to consensus.                        │
   │                                                  │
   │  ## Caveats and limitations                      │
   │  Detailed list with examples.                    │
   │                                                  │
   │  ## Changelog                                    │
   │  Version history with rationale.                 │
   │                                                  │
   │  ## References                                   │
   │  Academic citations, prior work.                 │
   │                                                  │
   │  [Open notebook] [Edit on GitHub] [Cite]         │
   └────────────────────────────────────────────────┘
```

This is the full document. Long-form. Source-controlled in a Git repo (`opengem/methodology/<id>.md`).

## The methodology object schema

```json
{
  "id": "combiner-v4-2-dfm",
  "version": "4.2",
  "title": "Combiner v4.2 + DFM",
  "summary": "Two-line summary",
  "components": [
    { "id": "bauer-mertens", "weight": 0.4 },
    { "id": "cleveland-dfm", "weight": 0.6 }
  ],
  "data_sources": [
    {
      "name": "FRED",
      "series": ["CPIAUCSL"],
      "license": "public",
      "refresh": "daily",
      "url": "https://fred.stlouisfed.org/series/CPIAUCSL"
    }
  ],
  "refresh_cadence": "daily",
  "last_refreshed": "2026-06-04T14:30:00Z",
  "vintage": "2026-06-04",
  "caveats": [
    { "severity": "warn", "text": "Shelter component lags 6 months" },
    { "severity": "warn", "text": "COVID-period (2020-2022) weighted half" }
  ],
  "code_url": "https://github.com/opengem/forecasting/tree/v4.2/combiner",
  "notebook_url": "/export/notebook?methodology=combiner-v4-2-dfm",
  "doi": "10.99999/methodology/combiner-v4-2"
}
```

## The mandatory caveats

Every methodology has ≥1 caveat. This is enforced at publish time — a methodology with zero caveats is rejected.

Why: every model has known limitations. Listing them publicly is the trust differentiator. Hiding them is the cartel move.

Caveat severities:
- `info`: methodological note, not a flaw
- `warn`: known weakness, mitigated
- `error`: known weakness, NOT yet mitigated — display prominently

If any caveat is `error`-level, the chart itself shows a small ⚠ in the corner with a tooltip.

## The "Why is this different from..." link

For methodology pages mirroring established public methods (Bauer-Mertens, GDPNow, Cleveland-Fed-class), an optional callout:

```
   ┌──────────────────────────────────────────────┐
   │  Compared to Bauer-Mertens (FRBSF original):  │
   │                                                │
   │  Same: probit model, term spread variables   │
   │  Different:                                    │
   │   + Extended to 12 countries (FRBSF: US only) │
   │   + Daily refresh (FRBSF: monthly)            │
   │   + Calibration against OECD recession dates │
   │     (FRBSF: NBER only)                         │
   └──────────────────────────────────────────────┘
```

## The methodology changelog

Every methodology has a changelog. Versions are immutable.

```
   v4.2  2026-Q1 calibration update; shelter component refined
   v4.1  2025-Q4 added MIDAS bridge for jobs data
   v4.0  2025-09 ensemble re-architecture
   v3.2  2025-Q2 added Cleveland Fed source
   ...
```

Each prior version's URL still resolves and shows the methodology AS IT WAS. This is the open-archive contract.

When a chart uses an older vintage's forecast, the methodology link points to the version that was actually used (not the latest). The "this version is superseded" banner appears.

## The "code link" — the ultimate transparency

Every methodology has a `code_url` linking to the exact commit + file path that implements it. Public repo, Apache-2.0.

For users who want to validate: clone the repo, check out the commit pinned in the methodology, run the notebook, see the same numbers.

## The reproduce contract

Combined with the cite-this-view (L158) provenance manifest, a methodology is reproducible byte-for-byte:

```
   provenance manifest    →  cite ID
       ├─ data sources    →  hashed inputs
       ├─ methodology     →  pinned methodology ID + version
       ├─ container       →  Docker digest
       └─ lockfile        →  exact dependency versions
```

Run `opengem reproduce <cite-id>` → re-runs the pipeline. Reproducibility test in CI.

## Empty / degraded methodology

For early-stage methodologies (e.g., beta features):

```
   ⚠ Beta methodology — accuracy not yet established.
   No vintage-locked backtest available. Use at your own risk.
   See: /accountability/beta-methods
```

The chart still renders but with a "beta" badge and the popover has the warning above the standard contract.

## What the pop-up MUST NOT do

- Hide the data sources
- Skip caveats
- Use marketing language
- Be longer than 1 popover height (use the full page for that)
- Require login to view (always public)

## Performance

- Methodology JSON cached in browser localStorage after first fetch
- Popover renders in <30ms after data is in cache
- First-load fetch <50KB per methodology

## MCP exposure

The MCP server exposes:
- `methodology.summary(id)` — returns the preview JSON
- `methodology.full(id)` — returns the full markdown
- `methodology.list(filter)` — returns the catalog

LLM agents can pull methodology to inform their responses.

## Editorial tone

The popover writes in present tense, active voice, plain language. Examples:

✓ "This forecast blends two models."
✗ "This forecast is computed via blending of multiple models with calibrated weights."

The full page can be more technical (it's for analysts). The popover is for the prosumer.

## Coverage requirement

Every published forecast, indicator nowcast, scenario probability, surprise index, pulse score, recession probability — every number derived from a model — must have a methodology pop-up.

Raw data (e.g., "official BLS CPI print") doesn't need methodology; instead it has a provenance pop-up.

Provenance pop-up is a sibling concept (L132). Methodology = how OPENGEM computed it. Provenance = where the underlying data came from.

Both can co-exist on a chart that combines raw data + model output.

## The asymmetric move

Bloomberg charts have no methodology pop-up. The user must search Bloomberg's terminal help system or call their sales engineer.

OPENGEM charts have one. It opens. It explains. It links to runnable code.

This is the trust asymmetry, surfaced.
