# L181 — Forecast Object Schema (JSON Contract)

**Loop**: 181 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

Every OPENGEM forecast — whether served from the dashboard chart, the REST `/v1/forecast` endpoint, the MCP tool `forecast.get`, or copy-pasted into ChatGPT — is rendered from a single canonical JSON object. **One schema, one source of truth, one contract.** Versioned `forecast.v1`. Anything that violates the schema is not a forecast; it is a draft.

This loop pins that schema. It is consumed downstream by L182 (lineage), L186 (reproducibility envelope), L190 (consensus overlay), L195 (chart UI), and L198 (narrative pipeline).

## Design constraints

1. **Self-describing on the wire.** A reader who fetches the JSON without prior context must be able to figure out (a) what was forecast, (b) when, (c) by whom, (d) how to replay it, (e) what its track record is. No out-of-band lookup required.
2. **Round-trippable.** Any forecast emitted by OPENGEM can be deserialised, re-serialised, and re-emitted byte-identical. This implies a strict canonical form (sorted keys, fixed float precision, UTC timestamps in ISO-8601 with `Z` suffix, no nulls where omission is equivalent).
3. **Density-first, point-second.** The point estimate (`p50`) is a *projection* of the density; the density is the primitive. Consumers who only want a point pull `p50`, but the schema requires the bands.
4. **Provenance-stamped at every level.** Vintage IDs, container digests, code SHAs, data lockfile hashes — all required, none optional, even in dev. A "fake" dev forecast that omits them is invalid by construction.
5. **Backward compatibility via additive evolution.** New optional fields can be added without bumping the major version. Removal or semantic change of an existing required field bumps `v2`.

## The schema (`forecast.v1`)

```json
{
  "schema": "opengem.forecast.v1",
  "forecast_id": "fcst_2026-06-06_USA_GDP_4Q_OPENGEM-L3-BMA_v3.2.1",
  "vintage_id": "vint_2026-06-06T08:00:00Z_USA-quartet",
  "model_id": "OPENGEM-L3-BMA",
  "model_version": "3.2.1",
  "model_card_url": "https://opengem.org/models/opengem-l3-bma/3.2.1",
  "country": "USA",
  "country_tier": "V-Core",
  "indicator": {
    "id": "GDP-real-yoy",
    "label": "Real GDP, year-over-year",
    "unit": "percent_per_year",
    "frequency": "Q"
  },
  "horizon": {
    "h": 4,
    "unit": "Q",
    "label": "4Q-ahead"
  },
  "base_period": "2026-Q1",
  "scoring_period": "2027-Q1",
  "released_at": "2026-06-06T08:00:00Z",
  "point": 2.18,
  "bands": {
    "p10": 1.04,
    "p25": 1.49,
    "p50": 2.18,
    "p75": 2.83,
    "p90": 3.28
  },
  "density": {
    "type": "gaussian_mixture",
    "components": [
      {"weight": 0.41, "mean": 2.31, "sd": 0.84, "model_id": "L3-DFM"},
      {"weight": 0.34, "mean": 2.06, "sd": 0.91, "model_id": "L3-ML-RIDGE"},
      {"weight": 0.25, "mean": 1.99, "sd": 0.97, "model_id": "L3-BVAR-LARGE"}
    ],
    "samples_url": "https://opengem.org/forecasts/fcst_2026-06-06_USA_GDP_4Q.../samples.parquet"
  },
  "consensus_overlay": {
    "weo": {"value": 2.10, "released_at": "2026-04-22", "horizon_match": "annual_average"},
    "oecd_eo": {"value": 2.05, "released_at": "2026-05-29", "horizon_match": "annual_average"},
    "frb_sep": {"value": 2.20, "released_at": "2026-03-19", "horizon_match": "Q4-over-Q4"},
    "ecb_spf": null
  },
  "provenance": {
    "git_sha": "9b3a4f7c8d1e2a5b6c7d8e9f0a1b2c3d4e5f6a7b",
    "container_digest": "sha256:8e1d7a9c4b2f5e6d3a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1",
    "data_lockfile": "sha256:1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b",
    "vintage_inputs": [
      {"series_id": "BEA-T10101-A191RL", "vintage_at": "2026-05-29T16:30:00Z", "hash": "sha256:..."},
      {"series_id": "BLS-CPIAUCSL", "vintage_at": "2026-06-05T12:30:00Z", "hash": "sha256:..."},
      {"series_id": "FRB-H15-DGS10", "vintage_at": "2026-06-06T07:15:00Z", "hash": "sha256:..."}
    ],
    "build_url": "https://github.com/opengem/opengem-1/actions/runs/8742193845",
    "replayable_via": "opengem replay --forecast-id fcst_2026-06-06_USA_GDP_4Q..."
  },
  "miss_log_url": "https://opengem.org/track-record/USA/GDP-real-yoy/4Q",
  "track_record_snapshot": {
    "crps_oos_window": "2014-Q1..2025-Q4",
    "crps_vs_ar1_winrate": 0.83,
    "pit_ks_pass": true,
    "dm_vs_weo_pvalue": 0.42,
    "n_observations": 168
  },
  "trust_badges": ["vintage-correct", "ensemble-of-3", "pit-passed", "peer-replicated"],
  "license": "CC-BY-4.0",
  "citation": "OPENGEM (2026). USA Real GDP 4Q-ahead forecast, vintage 2026-06-06. opengem.org/forecasts/fcst_2026-06-06_USA_GDP_4Q_OPENGEM-L3-BMA_v3.2.1"
}
```

## Field-by-field rationale

- `schema` is the version pin. Every parser checks it before doing anything else.
- `forecast_id` is a deterministic, content-addressable name: `fcst_{released_at_date}_{country}_{indicator}_{horizon}_{model}_{version}`. Two requests with the same inputs produce the same ID.
- `vintage_id` points at the L182 lineage record. It is the foreign key into the vintage store.
- `model_card_url` is a hard requirement, not optional. Every forecast must be traceable to a human-readable methodology page.
- `country_tier` (`V-Core`, `V-Extended`, `T`) signals whether this forecast is on the leaderboard. Tier-T forecasts publish but do not score.
- `indicator` is a structured object, not a string. Unit and frequency are required so the consumer knows what the number means without a lookup.
- `base_period` is the last observation known to the model. `scoring_period` is the period the forecast is *for*. These two anchor the forecast in time unambiguously.
- `point` is the headline number consumers see. It equals `bands.p50` by convention; the duplication is intentional for low-friction reading.
- `bands` carries the canonical five-quantile cut (P10/P25/P50/P75/P90). L188 picks P10/P50/P90 as the chart default but the JSON always carries five.
- `density.samples_url` points to a Parquet file of N=10,000 Monte Carlo draws for downstream consumers who need the full distribution.
- `consensus_overlay` carries the four canonical incumbents (WEO, OECD EO, FRB SEP, ECB SPF) with `horizon_match` flagging the apples-to-apples reconciliation (L190).
- `provenance` is mandatory and exhaustive. Every byte needed for L186 replay is here or referenced by hash.
- `track_record_snapshot` is a pre-computed summary so the dashboard chart can render trust signals (L199) without a second API call.
- `trust_badges` is the enumerated set of badges this forecast qualifies for (L199 catalog).

## What goes on the wire vs. what stays on disk

The JSON above is ~3 KB. The full density samples Parquet is ~80 KB. The vintage inputs hash list points at ~500 KB of raw series in the vintage store. The dashboard hits the JSON; the MCP tool returns the JSON; the replay command pulls everything.

## Validation

A JSON Schema file (`schemas/forecast.v1.json`) ships with the `opengem-types` package. CI runs every emitted forecast through the schema validator. A forecast that fails schema validation is rejected from publication — it does not get to the dashboard.

## What this loop produced

- Canonical `forecast.v1` JSON contract with worked example.
- Required vs. optional field map.
- Deterministic `forecast_id` naming convention.
- Hard rule: provenance fields are mandatory.

## What comes next

- **L182** — vintage lineage record this object references.
- **L186** — full reproducibility envelope around the provenance block.
- **L195** — chart UI that consumes this object.

## Related

- [[L001-vision-statement]] — "every number is dated, every miss is named" — the schema operationalises this.
- [[R16-reproducibility]] — hash quintuple this provenance block instantiates.
- [[R99-synthesis]] — V&V matrix that scores these forecasts.
- [[L186-reproducibility-envelope]] — full envelope spec.
- [[L188-band-quantiles]] — canonical band cut.
- [[L190-consensus-comparison]] — overlay sources.
- [[L195-forecast-ui-spec]] — how this renders on a chart.
