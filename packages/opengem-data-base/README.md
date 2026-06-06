# opengem-data-base

🧪 alpha

Adapter base class + common patterns for OPENGEM data adapters. Provides:

- **`Adapter`** abstract base — every adapter (BEA, BLS, ECB, IMF, etc.) implements `pull_series` and `pull_release`.
- **`SeriesCatalog`** — typed mapping from OPENGEM canonical series IDs to source-native identifiers.
- **`AdapterError`** hierarchy — `RateLimitError`, `SchemaError`, `OutageError`, etc., for consistent error handling.
- **`retry`** decorator — exponential backoff for transient HTTP failures, with jitter.

## Usage (skeleton for an adapter author)

```python
from opengem_data_base import Adapter, SeriesCatalog
from opengem_types import Observation, SeriesId

class MyAdapter(Adapter):
    source_id = "MYSRC"
    catalog = SeriesCatalog({
        SeriesId("US.MYSRC.SOMETHING.M"): "src-id-001",
    })

    def pull_series(self, series_id):
        ...  # adapter-specific implementation

    def pull_release(self, as_of=None):
        for sid in self.catalog:
            yield from self.pull_series(sid)
```

## Why a dedicated base package

15+ adapters share the same retry/backoff logic, error taxonomy, and catalog
pattern. Centralizing here keeps each concrete adapter small and lets us
upgrade resilience for all of them at once.
