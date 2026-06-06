# L084 — GDELT-as-Feature Pipeline Design: BigQuery, Raw Zip, DOC API + Daily DAG

**Loop**: 084 / 300
**Phase**: 2 — Integration deep dive
**Date**: 2026-06-06
**Verdict**: **ADOPT-V1 (BigQuery Tier-A primary + Raw Tier-B mirror + DOC Tier-C live ticker)**

---

## What this loop sketches

L021 confirmed GDELT 2.0 as the single most strategically important open geopolitical substrate available — GREEN license, 15-minute cadence, 100+ language coverage, structured CAMEO/Goldstein/Theme/Tone scores. This loop converts that thesis into a *concrete daily ingestion pipeline* — the Dagster asset graph, the BigQuery cost envelope, the raw-zip fallback mirror, and the DOC API live sidebar — that we can build in Phase 5 without a second round of design.

The three-tier ingestion model (BigQuery primary, raw zip mirror, DOC API live) lands as the canonical pattern for *any* high-frequency event stream OPENGEM ingests — POLECAT (L023/L025), UCDP (L026), ACLED (L022/L085) all reuse this same three-tier shape.

## The pipeline at one glance

```
                    ┌──────────────────────────────────┐
                    │     GDELT public infrastructure    │
                    └──────────────────────────────────┘
                              │                    │
                ┌─────────────┴───┐                │
                │ BigQuery (free) │                │
                │ gdelt-bq.gdeltv2│                │
                └─────────────────┘                │
                        │                          │
                        ▼                          ▼
                ┌───────────────┐         ┌──────────────────┐
                │ Tier A: daily │         │ Tier C: live DOC │
                │ aggregation   │         │ API ticker poll  │
                │ jobs (Dagster)│         │ (5-min interval) │
                └───────────────┘         └──────────────────┘
                        │                          │
                        ▼                          ▼
                ┌───────────────────────────────────────────┐
                │  OPENGEM Vintage Store + R2 Parquet mirror │
                └───────────────────────────────────────────┘
                                    │
                                    ▼
                ┌───────────────────────────────────────────┐
                │  Tier B: raw 15-min zips mirrored          │
                │   monthly to R2 for cold-storage repro     │
                └───────────────────────────────────────────┘
                                    │
                                    ▼
                ┌───────────────────────────────────────────┐
                │  Downstream features →                     │
                │   - GeopoliticalPulse tile (L163)          │
                │   - L3 forecast features (Δ tone, Δ        │
                │     conflict, theme volatility)            │
                │   - OPENGEM-GPR variant (L024 ext 5)       │
                │   - Country page event tape (L123)         │
                └───────────────────────────────────────────┘
```

## Tier-A — BigQuery as the primary path

GDELT publishes its full corpus as Google BigQuery public datasets at `gdelt-bq.gdeltv2.*`. The relevant tables:

- `gdelt-bq.gdeltv2.events` — partitioned by day. Roughly 3M event-rows added daily.
- `gdelt-bq.gdeltv2.gkg` — partitioned by day. Roughly 500K-1M article-rows daily.
- `gdelt-bq.gdeltv2.gkg_partitioned` — same data, more efficient partition scheme.
- `gdelt-bq.gdeltv2.mentions` — article mentions resolved to events.

**Cost envelope.** Google's free tier is 1 TB/month of query bytes scanned. A typical daily GKG aggregation query that scans a single day partition costs **~3-5 GB** (the day is partitioned, the columns we select are a subset, the geographic filters reduce row count). 365 days × 5 GB = ~1.8 TB/year for daily refreshes — over the free tier, so we cache aggressively and only re-aggregate the trailing 7-30 days.

Realistic monthly query budget once we cache:
- Daily roll-up aggregate (last 7 days): 7 × 5 GB = 35 GB per day = ~1 TB/month. *Above the free tier by 20%.*
- Weekly roll-up backfill: 1 × 50 GB = 50 GB/week = ~200 GB/month.
- One-time historical pull (2015 → 2026): ~50 TB once. Run from a paid Google account or via a colab GPU node. Budget: ~$250 one-time at BigQuery's $5/TB rate.

We accept that we will exceed the free tier by ~$5-10/month at scale and budget accordingly. Cheaper than building our own ingest.

**Canonical daily query** (the Pulse aggregate):

```sql
-- runs at 03:00 UTC, aggregates yesterday's GKG
SELECT
  PARSE_DATE('%Y%m%d', SUBSTR(CAST(DATE AS STRING), 1, 8)) AS day,
  Locations.CountryCode AS country,
  COUNT(*) AS article_count,
  AVG(V2Tone[OFFSET(0)]) AS avg_tone,
  STDDEV_POP(V2Tone[OFFSET(0)]) AS tone_dispersion,
  APPROX_QUANTILES(V2Tone[OFFSET(0)], 100)[OFFSET(10)] AS tone_p10,
  APPROX_QUANTILES(V2Tone[OFFSET(0)], 100)[OFFSET(90)] AS tone_p90,
  COUNTIF(SearchTheme(V2Themes, 'ECON_')) AS econ_themed,
  COUNTIF(SearchTheme(V2Themes, 'WB_2024_FINANCIAL')) AS fin_themed,
  COUNTIF(SearchTheme(V2Themes, 'CRISISLEX_C03_WELLBEING')) AS crisis_themed,
  COUNTIF(SearchTheme(V2Themes, 'MILITARY')) AS military_themed,
  ARRAY_AGG(STRUCT(DocumentIdentifier, V2Tone[OFFSET(0)] AS tone) ORDER BY V2Tone[OFFSET(0)] LIMIT 5) AS most_negative
FROM `gdelt-bq.gdeltv2.gkg_partitioned`,
  UNNEST(SPLIT(V2Locations, ';')) AS Locations
WHERE _PARTITIONTIME = TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
  AND Locations LIKE '%#%' -- has a country code
GROUP BY day, country
HAVING article_count >= 5;
```

This single query produces the day's per-country tone aggregates, theme counts, and top-most-negative-article links. Cost: ~3 GB scanned (it's a single partition).

## Tier-B — Raw zip mirror for cold-storage reproducibility

GDELT also publishes raw 15-minute CSV drops at `http://data.gdeltproject.org/gdeltv2/<yyyymmddhhmmss>.export.CSV.zip` and `.gkg.csv.zip`. The `lastupdate.txt` pointer file tells you the newest batch.

We use Tier-B for two purposes:

1. **Cold-storage reproducibility.** Once a month, we mirror the trailing 30 days of raw GDELT zip files to R2 (`gdelt-raw/yyyy-mm-dd/<batch>.zip`). When a vintage-citation later needs to reproduce a forecast, the raw inputs are immutable and addressable.
2. **Backfill / failover.** If BigQuery is down or pricing changes, we have the source data and can re-run derived aggregates locally via DuckDB.

Mirror cost: ~30 GB/month of new GDELT data × $0.015/GB-month for R2 = **$0.45/month** ongoing. Cumulative storage at 5 years: ~1.8 TB × $0.015 = ~$27/month. Manageable.

## Tier-C — DOC API for the live ticker overlay

The DOC 2.0 REST API at `api.gdeltproject.org/api/v2/doc/doc` returns search results over the article corpus with full-text queries, theme filters, tone filters, and trendline endpoints. Free, rate-limited at "be reasonable" (no published cap, soft-enforced at maybe 60 calls/min).

We use Tier-C for:

- **The Geopolitical Pulse live ticker** at the bottom of the dashboard (L163, L170): poll every 5 minutes for the latest 10 most-mentioned crisis-themed articles per region.
- **The "explain this spike" drilldown**: when the daily GKG aggregate shows a tone-spike for a country, the user clicks through to a DOC-API-backed view that shows the top articles driving the spike, in real time.

The DOC API is the only Tier with sub-day latency. The Tier-A daily aggregate is yesterday's data; the Tier-C live ticker is the last 60 minutes.

## Dagster DAG layout

Six assets, organized into two groups (`gdelt_daily` and `gdelt_live`):

```python
# packages/opengem-data-gdelt/src/opengem_data_gdelt/dagster_assets.py
from dagster import asset, Definitions, ScheduleDefinition, define_asset_job
from datetime import date, timedelta

@asset(group_name="gdelt_daily", compute_kind="bigquery")
def gdelt_gkg_country_tone_daily(context) -> Path:
    """Per-country tone + theme aggregates for the trailing day. ~3GB/run."""
    sql = render_template("gkg_country_tone_daily.sql", day=context.partition_key)
    df = bigquery_client.query(sql).result().to_dataframe()
    out = R2_PATH / f"gkg-country-tone/dt={context.partition_key}/agg.parquet"
    df.to_parquet(out)
    return out

@asset(group_name="gdelt_daily", compute_kind="bigquery")
def gdelt_events_conflict_daily(context) -> Path:
    """Per-country CAMEO conflict-class event counts + Goldstein moments."""
    ...

@asset(group_name="gdelt_daily", deps=[gdelt_gkg_country_tone_daily, gdelt_events_conflict_daily])
def gdelt_geo_pulse_features(context) -> Path:
    """Daily-resolution feature panel for L3 forecast layer + Pulse tile."""
    tone = pd.read_parquet(R2_PATH / f"gkg-country-tone/dt={context.partition_key}/agg.parquet")
    events = pd.read_parquet(R2_PATH / f"events-conflict/dt={context.partition_key}/agg.parquet")
    panel = combine_features(tone, events)
    out = VINTAGE_STORE.write_batch(panel, source_id="gdelt", pulled_at=now())
    return out

@asset(group_name="gdelt_daily", compute_kind="duckdb")
def gdelt_raw_mirror_monthly(context) -> Path:
    """Mirror trailing 30 days of raw 15-min zips to R2 cold storage."""
    for batch_url in fetch_recent_batch_urls(days=30):
        copy_to_r2(batch_url)
    return R2_PATH / "gdelt-raw/manifest.json"

@asset(group_name="gdelt_live", compute_kind="http")
def gdelt_doc_live_ticker(context) -> dict:
    """Last-60-min top crisis-themed articles per region. Polled by frontend."""
    results = doc_api_search(theme="CRISISLEX_C03", time_window="1h", per_region=10)
    return cache_set("gdelt:live-ticker", results, ttl=300)
```

Schedule definitions:
- `gdelt_daily_job` runs daily at 03:00 UTC.
- `gdelt_raw_mirror_monthly_job` runs on the 1st of each month at 04:00 UTC.
- `gdelt_doc_live_ticker_job` runs every 5 minutes during dashboard hours (06:00-22:00 UTC; off-cycle outside).

## Trade-offs explored

### Why BigQuery primary instead of raw zip primary?

Pulling 96 raw 15-min zips per day, decompressing, parsing CSV, ingesting into local DuckDB = ~25 minutes per day on a single-core box. BigQuery does the same aggregation in 8 seconds at a marginal cost of pennies. Engineer time saved at scale (~150 hours/year of compute babysitting) buys back the BigQuery bill many times over.

### Why not DOC API as primary?

DOC API is best-effort, rate-limited, and lacks the structured Goldstein/CAMEO/Theme fields at the per-row level. It's a search engine over the article corpus, not a structured event extract. Wrong primitive for the L3 feature pipeline.

### Why mirror raw zips at all?

Two scenarios force the mirror:
1. Google deprecates the BigQuery public dataset or moves it behind a paywall. Has happened with prior Google datasets. We must own the raw bytes.
2. A user disputes a vintage-published forecast and asks for the inputs. We need to point them at an immutable zip file with a SHA256, not a Google-hosted BigQuery snapshot.

Cold-mirror cost is ~$30/month at maturity. Cheap insurance.

## Features the pipeline produces for L3

Eight derived features per country per day, fed into the L3 ensemble:

1. **avg_tone** — global tone average, signed.
2. **tone_dispersion** — within-day standard deviation of tone.
3. **tone_p10 / tone_p90** — left/right tail of tone distribution.
4. **conflict_event_count** — CAMEO QuadClass=4 events.
5. **goldstein_min_5d** — minimum 5-day rolling Goldstein.
6. **military_theme_share** — share of articles flagged with MILITARY theme.
7. **econ_theme_share** — share of articles with ECON_ theme prefix.
8. **crisis_theme_share** — CRISISLEX_C03 share.

These feed the recession-probability tile (L213), the FX-misalignment forecast (L217), and the OPENGEM-GPR variant (L024 extension 5).

## Risks

1. **BigQuery cost overruns.** If queries are accidentally written to scan full tables instead of partitions, a single bad run can cost $50+. Mitigation: budget alerts at $25/month, all queries reviewed for `_PARTITIONTIME` clauses, dry-run in CI.

2. **GDELT schema changes.** GDELT 3.0 has been rumored. Schema breakage would force a Fetcher rewrite. Mitigation: pin the column list explicitly in SQL; add a schema-snapshot test against the BigQuery `INFORMATION_SCHEMA` once a week.

3. **Tone score is noisy.** CAMEO miscoding + sarcasm + headline-bias all produce false signals. Mitigation: the L3 layer treats tone as a noisy feature, not a label; the published Pulse tile shows uncertainty bands.

4. **Country geocoding ambiguity.** GDELT's `Locations.CountryCode` field has known biases toward English-language coverage. Mitigation: cross-validate against POLECAT (L025) and UCDP (L026) for the same country-day pairs.

## What this loop produced

- Three-tier ingestion architecture with concrete BigQuery / R2 / DOC-API roles.
- Cost envelope: ~$5-10/mo BigQuery overage + ~$1-30/mo R2 storage growing → ~$50/mo at year 5.
- Dagster asset graph with six assets, three schedules.
- Canonical SQL for the daily country-tone aggregate.
- Eight derived features mapped to downstream L3 / tile / page consumers.

## What comes next

- **L085** — ACLED rate-limit feasibility (where GDELT serves as the GREEN fallback).
- **L097** — Dagster exploit plan (the asset graph design lands there).
- **L163** — Geopolitical pulse map (the tile this feature pipeline serves).
- **L213** — Recession-probability page (downstream consumer).

## Related

- [[L021-gdelt-gkg]] — Phase 1 deep dive, license, schema.
- [[L022-acled]] / [[L085-acled-rate-limit-feasibility]] — YELLOW alternative this pipeline insulates us from.
- [[L025-cline-center]] / [[L026-ucdp]] — sibling GREEN event substrates.
- [[L097-dagster-fully-exploit]] — the asset graph design.
- [[L163-geopolitical-pulse-map]] — downstream tile.
- [[L213-recession-prob-page]] — downstream model consumer.
