# opengem-datasette

Export OPENGEM vintage snapshots to SQLite for Datasette publication.

This is **the strategic moat surface**. Per L076 (research-300/loops) and the midpoint
synthesis: Datasette + per-vintage SQLite + Parquet-on-R2 = a public, queryable, vintage-stamped
ledger Bloomberg structurally cannot match.

## What it does

1. **Snapshot export** — given a `VintageStore`, write a self-contained SQLite database
   containing observations, forecasts, scenarios, and miss records as of a vintage date.
2. **Metadata enrichment** — emit Datasette `metadata.yaml` with table descriptions, licenses,
   per-table example queries, and per-column descriptions. These show up automatically as
   helpful prose on the Datasette UI.
3. **CLI** — `opengem-snapshot --vintage 2026-06-06 --out opengem-snapshot.db`

## CLI usage

```bash
# Snapshot today's vintage
opengem-snapshot --vintage today --out opengem-snapshot.db

# Or a specific date
opengem-snapshot --vintage 2026-06-06 --out opengem-2026-06-06.db

# Inspect the result with the Datasette CLI
datasette serve opengem-snapshot.db --metadata metadata.yaml
```

## Fly.io deployment

See `deploy/fly.toml`. The pattern is: a tiny VM that runs `datasette serve`
mounted on a persistent volume containing the latest snapshot. A separate Dagster
asset writes a fresh snapshot to the volume on the same cadence as `vintage_observations`.

Total cost: ~$5/mo for the VM + R2 storage for cold vintage tier.

## Permanent vintage URLs

Each vintage publishes at a permanent URL:

- Current: `https://data.opengem.org`
- Per-vintage archive: `https://data.opengem.org/v/2026-06-06`
- Per-table direct: `https://data.opengem.org/opengem/forecasts.json?country=USA`

This is the URL grammar that backs the L173 vintage-time-machine in the dashboard.

## License

Apache-2.0 (code) + CC-BY-4.0 (data emitted into the SQLite snapshot).

## See also

- L076 — Datasette deep-dive: this is the moat
- synthesis/MIDPOINT-FINDINGS.md — finding #1
- L173 — vintage time machine UX
- L095 — Datasette public ledger pattern
