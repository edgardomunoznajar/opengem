# opengem-vintage

🧪 alpha

Vintage-correct storage primitives. Persists `Observation` records into a vintage-discipline store: every release writes a new row; revisions never overwrite priors.

## What's in it

- **SQL schema** for `raw_observation` (TimescaleDB hypertable), `vintage_snapshot`, `series_meta`, `source`
- **`VintageStore` interface** with two implementations:
  - `PostgresVintageStore` — TimescaleDB-backed; production use
  - `SQLiteVintageStore` — in-memory; for tests and local exploration
- **`write_batch`** — atomically write a batch of observations + the snapshot row with a deterministic `vintage_hash`
- **`at(vintage_date)`** — query view that returns "data as known on date X" (latest vintage per series ≤ X)

## Why vintage discipline

Backtests using revised data are unfalsifiable. Real-world forecasting always uses real-time data. This package enforces the rule at the storage layer: revisions become new rows, not overwrites.

## Usage

```python
from opengem_vintage import SQLiteVintageStore
from opengem_types import Observation, SeriesId
from datetime import date, datetime

store = SQLiteVintageStore(":memory:")
store.initialize()

obs = [
    Observation(
        series_id=SeriesId("US.BEA.NIPA.GDP_real.Q"),
        observed_at=date(2026, 1, 1),
        vintage_at=date(2026, 4, 28),
        value=23500.123,
        source="BEA",
    ),
]

snapshot = store.write_batch(obs, source_id="BEA", pulled_at=datetime(2026, 4, 28, 14, 0))
print(snapshot.vintage_hash)  # sha256:...

# Query "as known on" a date
view = store.at(date(2026, 4, 30))
rows = list(view.iter_series("US.BEA.NIPA.GDP_real.Q"))
```

## Standalone usability

Install via `pip install opengem-vintage`. Bring your own Postgres or use SQLite for prototyping. The `VintageStore` interface is small and stable.

## Schema

See `sql/schema.sql` for the canonical Postgres+TimescaleDB schema. The SQLite implementation uses the same logical schema without hypertable partitioning.
