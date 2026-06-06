# opengem-data-bea

🧪 alpha

BEA NIPA adapter — Bureau of Economic Analysis US National Income and Product Accounts. Replaces FRED-as-source for US NIPA series (ADR-010, R09).

## Requires

- Free API key from https://apps.bea.gov/api/signup/ (set as `BEA_API_KEY` env var)

## Series catalog

OPENGEM canonical IDs → BEA `(DataSetName, TableName, LineNumber)`:

| OPENGEM SeriesId | BEA Table |
|---|---|
| `US.BEA.NIPA.GDP_real.Q` | NIPA T10101 line 1 (Real GDP, annualized chained dollars) |
| `US.BEA.NIPA.GDP_nominal.Q` | NIPA T10105 line 1 (Nominal GDP) |
| `US.BEA.NIPA.GDP_deflator.Q` | NIPA T10104 line 1 (GDP price deflator) |
| `US.BEA.NIPA.PCE_real.Q` | NIPA T10101 line 2 |
| `US.BEA.NIPA.GovExp_real.Q` | NIPA T10101 line 21 |
| `US.BEA.NIPA.Investment_real.Q` | NIPA T10101 line 6 |
| `US.BEA.NIPA.NetExports_real.Q` | NIPA T10101 line 14 |
| `US.BEA.NIPA.PCE_deflator.M` | NIPA T20804 line 1 |
| `US.BEA.NIPA.GDI.Q` | NIPA T10703 line 1 |

(More series in `catalog.py`; this is the IOC subset.)

## Usage

```python
from opengem_data_bea import BEAAdapter
from opengem_types import SeriesId

adapter = BEAAdapter()  # picks up BEA_API_KEY from env
for obs in adapter.pull_series(SeriesId("US.BEA.NIPA.GDP_real.Q")):
    print(obs.observed_at, obs.value)
```

## ToS posture

This adapter calls BEA's public API directly. **It does not use FRED** per OPENGEM ADR-010
(FRED's 2024 ToS prohibits caching). BEA's terms permit programmatic access and
caching of derived data; see [BEA API User Guide](https://apps.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf).
