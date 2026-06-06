# opengem-types

🧪 alpha

Canonical typed dataclasses for the OPENGEM system. Pure stdlib, no runtime dependencies. The vocabulary every other package speaks.

## What's in it

- `Observation` — a single time-series data point with vintage metadata
- `SeriesId` — canonical, hierarchical series identifier
- `VintageSnapshot` — a snapshot manifest with content hash
- `Forecast` / `DensityForecast` — point and density forecast records
- `ScenarioSpec` — structured shock specification
- `RunProvenance` — the hash quintuple `(code_sha, vintage_hash, prior_hash, posterior_hash, run_id)`
- `Country` / `Variable` / `Frequency` / `Horizon` — enums for canonical identifiers

## Usage

```python
from opengem_types import Observation, SeriesId, VintageSnapshot
from datetime import date

obs = Observation(
    series_id=SeriesId("US.BEA.NIPA.GDP_real.Q"),
    observed_at=date(2026, 1, 1),
    vintage_at=date(2026, 4, 28),
    value=23500.123,
    source="BEA",
)
```

## Standalone usability

This package can be installed alone via `pip install opengem-types` and used as a vocabulary for any economic-data pipeline. No OPENGEM dependency required.

## Why a dedicated package

Every other OPENGEM package (`opengem-data-*`, `opengem-l3`, `opengem-scenarios`, etc.) imports these types. Centralizing them prevents cross-package vocabulary drift and lets each package depend only on stable schemas, not on each other.
