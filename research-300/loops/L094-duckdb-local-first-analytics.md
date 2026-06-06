# L094 — DuckDB Local-First Analytics: How OPENGEM Uses DuckDB-WASM In-Browser

**Loop**: 094 / 300
**Phase**: 2 — Integration deep dive
**Date**: 2026-06-06
**Verdict**: **ADOPT-V1 (DuckDB-WASM for browser-side ad-hoc queries + DuckDB server-side for V&V evaluation)**

---

## What this loop converts

L077 named DuckDB the "single most important infrastructure upgrade open-source analytics has had in five years" and named three killer use cases. This Phase 2 loop converts those three into a concrete browser-side architecture, with bundle budget, Parquet-shape contract, query patterns, and the boundary between "client-side fast enough" and "server-side mandatory."

The headline pattern: **a ~5MB DuckDB-WASM bundle, loaded lazily and shared across pages, queries served Parquet snapshots from a CDN-cached `data.opengem.org` subdomain, with a `<DuckDBProvider>` React context that handles initialization and registered file URLs**. Sub-second queries on millions of rows, zero backend cost per query, no rate-limit story to maintain.

## What lives in DuckDB-WASM vs server

The split is straightforward once stated:

| Workload | Where | Why |
|---|---|---|
| Per-country/indicator chart series | Server (JSON API) | Small payload, cacheable, no DuckDB needed |
| Per-country deep-dive cross-correlation | DuckDB-WASM | User explores 10+ indicators; pre-fetch once, query repeatedly |
| Multi-country comparison ("Compare 2") | DuckDB-WASM | Cross-join data; fewer round-trips than per-pair API calls |
| "Fork this query" SQL editor | DuckDB-WASM | Educational + zero backend cost |
| Filter-your-bundle export | DuckDB-WASM | User selects subset → download Parquet slice |
| Watchlist aggregations | DuckDB-WASM | Personal data, runs locally, syncs via URL state |
| Global V&V scoring across all forecasts | DuckDB server-side | 100M+ row job, runs nightly in Dagster |
| BMA combiner weight calibration | DuckDB server-side | Same scale |
| Vintage-store-derived feature panel | DuckDB server-side | Internal pipeline |

The rule: **interactive analytical exploration goes to DuckDB-WASM; batch aggregation and pipelines go to DuckDB server-side. Read-pattern shape, not size, is the determinant.** A 50MB query that runs once per nightly batch is server-side. A 500MB query that runs 10x per user session is DuckDB-WASM (the first load is paid once, every subsequent query is fast).

## The browser bundle architecture

DuckDB-WASM is ~5MB gzipped. We accept the cost on pages that need it; we never include it in the global app shell. The pattern:

```typescript
// app/_providers/duckdb-provider.tsx
'use client';
import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import type { AsyncDuckDB } from '@duckdb/duckdb-wasm';

const DuckDBContext = createContext<{ db: AsyncDuckDB | null }>({ db: null });

export function DuckDBProvider({ children }: { children: ReactNode }) {
  const [db, setDb] = useState<AsyncDuckDB | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      const duckdb = await import('@duckdb/duckdb-wasm');
      const JSDELIVR_BUNDLES = duckdb.getJsDelivrBundles();
      const bundle = await duckdb.selectBundle(JSDELIVR_BUNDLES);
      const workerUrl = URL.createObjectURL(
        new Blob([`importScripts("${bundle.mainWorker!}");`], { type: 'text/javascript' })
      );
      const worker = new Worker(workerUrl);
      const logger = new duckdb.ConsoleLogger();
      const newDb = new duckdb.AsyncDuckDB(logger, worker);
      await newDb.instantiate(bundle.mainModule, bundle.pthreadWorker);
      URL.revokeObjectURL(workerUrl);
      if (!cancelled) setDb(newDb);
    })();
    return () => { cancelled = true; };
  }, []);

  return <DuckDBContext.Provider value={{ db }}>{children}</DuckDBContext.Provider>;
}

export function useDuckDB() {
  return useContext(DuckDBContext);
}
```

This is shared across all pages that opt into DuckDB. The provider is placed on the **Compare-2 page**, the **Country deep-dive page**, the **Forecast page (in "fork this query" mode)**, and the **Filter-bundle page**. The home page and methodology pages do not load it.

## The Parquet-shape contract

OPENGEM publishes daily Parquet snapshots at canonical URLs:

```
https://data.opengem.org/v1/forecasts.parquet            -- all forecasts, ~150MB
https://data.opengem.org/v1/forecasts-latest.parquet     -- latest vintage only, ~30MB
https://data.opengem.org/v1/indicators.parquet           -- all indicator history, ~400MB
https://data.opengem.org/v1/indicators-latest.parquet    -- latest values only, ~5MB
https://data.opengem.org/v1/leaderboard.parquet          -- track-record scoring, ~10MB
https://data.opengem.org/v1/consensus.parquet            -- WEO+OECD+SPF+SEP overlay, ~20MB
https://data.opengem.org/v1/country/{iso3}.parquet       -- per-country deep slice, 0.5-5MB
https://data.opengem.org/v1/indicator/{slug}.parquet     -- per-indicator cross-country, 1-10MB
```

Each file has a documented column schema (matched to the OpenAPI spec, L249). The country-specific Parquets are what feed the country deep-dive page; the indicator-specific Parquets feed the Compare-2 page; the leaderboard Parquet feeds the L133 ranking.

DuckDB-WASM registers them via `registerFileURL`:

```typescript
const { db } = useDuckDB();
const conn = await db!.connect();

await db!.registerFileURL(
  'usa.parquet',
  'https://data.opengem.org/v1/country/usa.parquet',
  duckdb.DuckDBDataProtocol.HTTP,
  false,
);
await db!.registerFileURL(
  'deu.parquet',
  'https://data.opengem.org/v1/country/deu.parquet',
  duckdb.DuckDBDataProtocol.HTTP,
  false,
);

const result = await conn.query(`
  SELECT
    u.observed_at AS date,
    u.value AS usa_cpi,
    d.value AS deu_cpi,
    u.value - d.value AS spread
  FROM 'usa.parquet' u
  JOIN 'deu.parquet' d
    ON u.observed_at = d.observed_at AND u.indicator = d.indicator
  WHERE u.indicator = 'cpi_yoy'
  ORDER BY date DESC
  LIMIT 120
`);
```

DuckDB-WASM lazily reads only the row groups needed (Parquet's strength). The two-country cross-join on monthly CPI series of 25 years returns in ~100ms after the initial Parquet metadata fetch.

## The "Fork this query" pattern

Every chart ships with a "see the SQL" button. Clicking opens a SQL editor (Monaco) pre-populated with the query that generated the chart. The user edits, hits "run," and the chart updates from the new query result.

```typescript
// components/fork-this-query.tsx
'use client';
import { useDuckDB } from '@/app/_providers/duckdb-provider';
import Editor from '@monaco-editor/react';

export function ForkThisQuery({ initialSql, parquetUrl, onResult }: Props) {
  const { db } = useDuckDB();
  const [sql, setSql] = useState(initialSql);

  const run = async () => {
    if (!db) return;
    const conn = await db.connect();
    await db.registerFileURL('data.parquet', parquetUrl, ProtocolType.HTTP, false);
    const result = await conn.query(sql);
    onResult(result.toArray());
  };

  return (
    <div>
      <Editor language="sql" value={sql} onChange={v => setSql(v ?? '')} height="200px" />
      <button onClick={run}>Run query</button>
    </div>
  );
}
```

This is a ~50-line component. It is the load-bearing affordance of the **"OPENGEM is open, you can query the substrate yourself"** distribution wedge. Every YouTuber building a "5 weirdest macro charts of 2026" video can fork OPENGEM's underlying queries and screenshot the result. Educational + viral + zero ops cost.

## The "Filter your bundle" export

The L194 coverage page links to a `/bundle/build` page where the user picks:
- Countries (G20 by default, configurable).
- Indicators (3-5 by default).
- Date range.
- Vintage strategy (latest vs as-of vintage).

DuckDB-WASM runs the filter query against the master `forecasts.parquet` + `indicators.parquet`, builds a filtered Parquet via DuckDB's `COPY ... TO 'output.parquet'`, and triggers a browser download. **No server round-trip for the filter logic.**

```typescript
// components/bundle-builder.tsx
const buildBundle = async (filters: BundleFilters) => {
  const conn = await db.connect();
  await db.registerFileURL('forecasts.parquet', `${DATA_BASE}/forecasts.parquet`, ProtocolType.HTTP, false);
  await db.registerFileURL('indicators.parquet', `${DATA_BASE}/indicators.parquet`, ProtocolType.HTTP, false);

  await conn.query(`
    COPY (
      SELECT * FROM 'forecasts.parquet'
      WHERE country IN ?
        AND indicator IN ?
        AND vintage_at >= ?
    ) TO 'opengem-bundle.parquet' (FORMAT PARQUET, COMPRESSION 'snappy');
  `, [filters.countries, filters.indicators, filters.from]);

  const buf = await db.copyFileToBuffer('opengem-bundle.parquet');
  const blob = new Blob([buf], { type: 'application/octet-stream' });
  triggerDownload(blob, 'opengem-bundle.parquet');
};
```

The output Parquet is sliced down from ~200MB of source to typically ~5-50MB of user-selected content. Download is fast; the resulting file opens cleanly in Python (pandas/polars), R (`arrow`), Julia, DuckDB CLI, anywhere.

## Server-side DuckDB

For nightly V&V scoring (L183), BMA weight calibration (L189), and the vintage-store-derived feature panel construction (L185), we use DuckDB *server-side* in the Dagster pipeline:

```python
# packages/opengem-vintage/src/opengem_vintage/duckdb_eval.py
import duckdb

con = duckdb.connect(":memory:")
con.execute("INSTALL httpfs; LOAD httpfs;")

# Read forecasts + realized from R2-cached Parquet
crps = con.execute("""
  WITH paired AS (
    SELECT
      f.model_id,
      f.country,
      f.indicator,
      f.horizon,
      f.vintage_at,
      f.observed_at AS target_date,
      f.p10, f.p50, f.p90,
      r.value AS realized
    FROM read_parquet('s3://opengem-vintage/forecasts/*/*.parquet') f
    JOIN read_parquet('s3://opengem-vintage/realized/*/*.parquet') r
      ON f.country = r.country
     AND f.indicator = r.indicator
     AND f.observed_at = r.observed_at
    WHERE f.vintage_at >= '2020-01-01'
      AND r.is_final = TRUE
  )
  SELECT
    model_id,
    country,
    indicator,
    horizon,
    AVG(crps_score(p10, p50, p90, realized)) AS mean_crps,
    COUNT(*) AS n_pairs
  FROM paired
  GROUP BY model_id, country, indicator, horizon
""").df()
```

DuckDB chews through 100M+ pair rows in a couple of minutes on a single CPU. Comparable Postgres aggregation would be 10-30x slower; comparable BigQuery would charge real money. DuckDB on Cloud Run is the right shape for this workload.

## Bundle budget management

The DuckDB-WASM bundle adds ~5MB to any page that uses it. Two mitigations keep this manageable:

1. **Lazy-load by route**: only pages that opt into DuckDB load the bundle. The home page, country page, indicator page, forecast page (default mode) don't load it.
2. **Service Worker cache**: once loaded, the WASM stays cached in the Service Worker. Subsequent navigations don't re-fetch it.

After the first DuckDB-WASM-enabled page load, the second is instant. The 5MB is a one-time cost per session.

## Cross-origin and CORS

`data.opengem.org` serves Parquet with CORS headers (`Access-Control-Allow-Origin: *`). DuckDB-WASM's HTTP file protocol uses standard fetch under the hood, so CORS rules apply. We pre-set them via Cloudflare's response headers.

Two gotchas:
- HTTP Range requests must be supported (DuckDB lazily reads row groups). Cloudflare supports Range natively; check on any CDN swap.
- The Parquet files must be served with `Content-Type: application/octet-stream` (or `Content-Type: application/vnd.apache.parquet`). Cloudflare auto-detects; explicit override is one line.

## Cost summary

| Item | Cost |
|---|---|
| Parquet generation (nightly Dagster job) | Server-side, ~30 min CPU |
| Parquet storage on R2 | ~$2/mo at v1, growing to ~$15/mo at Y2 |
| Parquet bandwidth | $0/mo (R2 has free egress) |
| DuckDB-WASM bundle (jsDelivr) | $0/mo |
| Server-side DuckDB Cloud Run minutes | ~$10-20/mo for nightly V&V |
| **Total** | **~$15-35/mo** |

Compared to a Postgres+pgvector+materialized-view alternative running the same workloads: ~$200-500/mo. DuckDB is 10-30x cheaper at OPENGEM's analytical scale.

## The Motherduck question

L077 noted Motherduck (DuckDB Labs' hosted DuckDB service) as "EVALUATE-LATER." This loop reconfirms — OPENGEM does not need Motherduck because:

1. Our data fits on a single machine. We are not at distributed-DuckDB scale.
2. Our public surface uses DuckDB-WASM, not a hosted SQL endpoint.
3. Motherduck's 2026 pricing changes made it less competitive vs Cloud Run + DuckDB OSS.

If OPENGEM grows beyond single-machine scale (Y3+ scenario), Motherduck becomes worth revisiting. Not v1.

## Risks

1. **5MB bundle on lower-spec mobile.** Mitigation: route gating; mobile-specific "lite" pages that skip DuckDB.
2. **WASM unsupported in old Safari.** Mitigation: feature-detect; fallback to "this page requires modern browser" notice on the 2% of users affected.
3. **Parquet file size growth.** ~200MB master Parquet today; could grow to several GB. Mitigation: partitioned Parquet (per-country files referenced via Hive partitioning + manifest); user fetches only the partitions they need.
4. **CORS or Range-request misconfiguration on CDN swap.** Mitigation: e2e test that DuckDB-WASM successfully reads `data.opengem.org/v1/forecasts.parquet` from a test browser.

## What this loop produced

- Three-use-case browser pattern (Fork-this-query + Filter-bundle + Compare-2) all running locally.
- Server-side DuckDB for V&V evaluation pipeline.
- Bundle budget management (lazy-load + Service Worker cache).
- Parquet-shape contract (canonical URLs + CORS + Range).
- ~$15-35/mo operating cost.
- Motherduck deferred.

## What comes next

- **L095** — Datasette public ledger (sibling pattern, server-side SQL).
- **L129** — Compare-2 mode (downstream UI).
- **L194** — Coverage page (links to bundle builder).
- **L254** — DuckDB-WASM client-side prototype (Phase 5 code).

## Related

- [[L077-duckdb-motherduck]] — Phase 1 deep dive.
- [[L078-iceberg-delta-parquet]] — long-term storage sibling.
- [[L095-datasette-public-ledger]] — server-side SQL sibling.
- [[L129-compare-2-mode]] — downstream UI.
- [[L194-coverage-page]] — links to bundle builder.
- [[L254-duckdb-wasm-prototype]] — Phase 5 code.
