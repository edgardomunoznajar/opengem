# R19 — Upstream-Agency Adapter Code Skeletons

| Field | Value |
|---|---|
| Document ID | OG1-RES-019 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Reference implementation skeletons for SSDD-001 v2's adapter cohort.** |
| Authority | R05 §6, R09 §4, R18 Phase 1 |

---

## 1. Why this exists

R18 Phase 1 plans four weeks of adapter work. This memo gives the skeleton for each adapter so the actual implementation week is *only* about filling in the API specifics. Saves time at execution.

## 2. Common adapter interface

```python
# src/opengem/adapters/base.py
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime
from typing import Iterator

@dataclass(frozen=True)
class Observation:
    series_id: str         # canonical OPENGEM series id (e.g., "US.BEA.NIPA.GDP_real.Q")
    observed_at: date      # reference period (start of quarter, month, day)
    vintage_at: date       # release date (when the agency published this value)
    value: float | None    # may be None for "not yet released"
    source_id: str         # 'BEA', 'BLS', 'FRB', 'TREAS', 'CENSUS'
    metadata: dict         # frequency, unit, original_id, etc.

@dataclass(frozen=True)
class PullManifest:
    """What was pulled in a single run."""
    source_id: str
    pulled_at: datetime
    series_pulled: list[str]
    observation_count: int
    vintage_hash: str

class Adapter(ABC):
    """All adapters implement this interface."""

    source_id: str
    series_catalog: dict[str, str]   # opengem_series_id → source_native_id

    @abstractmethod
    def pull_series(self, opengem_series_id: str) -> Iterator[Observation]:
        """Pull all historical observations for one series."""

    @abstractmethod
    def pull_release(self, as_of: date | None = None) -> Iterator[Observation]:
        """Pull the latest release values for all series in catalog."""

    def health_check(self) -> bool:
        """Cheap call to verify endpoint is reachable."""
        return True
```

## 3. BEA adapter skeleton

```python
# src/opengem/adapters/bea.py
import os
import requests
from datetime import date
from typing import Iterator
from .base import Adapter, Observation

BEA_BASE = "https://apps.bea.gov/api/data"

class BEAAdapter(Adapter):
    source_id = "BEA"

    # OPENGEM canonical series IDs mapped to (DataSetName, TableName, LineNumber)
    series_catalog = {
        "US.BEA.NIPA.GDP_real.Q":    ("NIPA", "T10101", 1),
        "US.BEA.NIPA.GDP_nominal.Q": ("NIPA", "T10105", 1),
        "US.BEA.NIPA.GDP_deflator.Q":("NIPA", "T10104", 1),
        "US.BEA.NIPA.PCE_def.M":     ("NIPA", "T20804", 1),
        # ... etc.
    }

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ["BEA_API_KEY"]

    def pull_series(self, opengem_series_id: str) -> Iterator[Observation]:
        dataset, table, line = self.series_catalog[opengem_series_id]
        params = {
            "UserID": self.api_key,
            "method": "GetData",
            "DataSetName": dataset,
            "TableName": table,
            "Frequency": "Q",
            "Year": "ALL",
            "ResultFormat": "JSON",
        }
        resp = requests.get(BEA_BASE, params=params, timeout=30)
        resp.raise_for_status()
        results = resp.json()["BEAAPI"]["Results"]
        for row in results["Data"]:
            if int(row["LineNumber"]) != line:
                continue
            yield Observation(
                series_id=opengem_series_id,
                observed_at=parse_bea_period(row["TimePeriod"]),
                vintage_at=date.today(),   # BEA returns latest revised; vintage is "today"
                value=float(row["DataValue"].replace(",", "")) if row["DataValue"] else None,
                source_id=self.source_id,
                metadata={"unit": row.get("UNIT_MULT"), "table": table},
            )

    def pull_release(self, as_of: date | None = None) -> Iterator[Observation]:
        for series_id in self.series_catalog:
            yield from self.pull_series(series_id)

def parse_bea_period(period: str) -> date:
    """e.g., '2026Q1' -> 2026-01-01"""
    year, q = period.split("Q")
    return date(int(year), (int(q) - 1) * 3 + 1, 1)
```

## 4. BLS adapter skeleton

```python
# src/opengem/adapters/bls.py
import os
import requests
from datetime import date
from typing import Iterator
from .base import Adapter, Observation

BLS_BASE = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

class BLSAdapter(Adapter):
    source_id = "BLS"

    series_catalog = {
        "US.BLS.CPI.headline.NSA.M":  "CUUR0000SA0",
        "US.BLS.CPI.headline.SA.M":   "CUSR0000SA0",
        "US.BLS.CPI.core.SA.M":       "CUSR0000SA0L1E",
        "US.BLS.LNS.unemp_rate.SA.M": "LNS14000000",
        "US.BLS.CES.nonfarm.SA.M":    "CES0000000001",
        # ... etc.
    }

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ["BLS_API_KEY"]

    def pull_series(self, opengem_series_id: str) -> Iterator[Observation]:
        bls_id = self.series_catalog[opengem_series_id]
        payload = {
            "seriesid": [bls_id],
            "startyear": "2000",
            "endyear": str(date.today().year),
            "registrationkey": self.api_key,
        }
        resp = requests.post(BLS_BASE, json=payload, timeout=30)
        resp.raise_for_status()
        for series in resp.json()["Results"]["series"]:
            for row in series["data"]:
                yield Observation(
                    series_id=opengem_series_id,
                    observed_at=parse_bls_period(row["year"], row["period"]),
                    vintage_at=date.today(),
                    value=float(row["value"]) if row["value"] != "." else None,
                    source_id=self.source_id,
                    metadata={"bls_id": bls_id, "period_name": row["periodName"]},
                )

    def pull_release(self, as_of: date | None = None) -> Iterator[Observation]:
        # BLS API allows 50 series per call — batch
        for batch in batched(self.series_catalog, 50):
            ...

def parse_bls_period(year: str, period: str) -> date:
    """period = 'M01'..'M12' or 'Q01'..'Q04'"""
    if period.startswith("M"):
        return date(int(year), int(period[1:]), 1)
    if period.startswith("Q"):
        q = int(period[1:])
        return date(int(year), (q - 1) * 3 + 1, 1)
    raise ValueError(period)
```

## 5. FRB Board adapter skeleton

```python
# src/opengem/adapters/frb_board.py
import requests
from datetime import date
from typing import Iterator
from .base import Adapter, Observation

FRB_DDP = "https://www.federalreserve.gov/datadownload/Output.aspx"

class FRBBoardAdapter(Adapter):
    source_id = "FRB"

    # Series IDs from FRB DDP packages
    series_catalog = {
        "US.FRB.H15.DGS10":     ("H15", "DGS10"),
        "US.FRB.H15.DGS2":      ("H15", "DGS2"),
        "US.FRB.H15.DGS3MO":    ("H15", "DGS3MO"),
        "US.FRB.H15.FEDFUNDS":  ("H15", "FEDFUNDS"),
        "US.FRB.H6.M2SL":       ("H6", "M2SL"),
        "US.FRB.G17.INDPRO":    ("G17", "INDPRO"),
        # ... etc.
    }

    def pull_series(self, opengem_series_id: str) -> Iterator[Observation]:
        release, series = self.series_catalog[opengem_series_id]
        params = {
            "rel": release,
            "series": series,
            "from": "01/01/2000",
            "to": date.today().strftime("%m/%d/%Y"),
            "filetype": "csv",
            "label": "include",
        }
        resp = requests.get(FRB_DDP, params=params, timeout=30)
        resp.raise_for_status()
        for row in parse_frb_csv(resp.text):
            yield Observation(
                series_id=opengem_series_id,
                observed_at=row["date"],
                vintage_at=date.today(),
                value=row["value"],
                source_id=self.source_id,
                metadata={"release": release, "frb_id": series},
            )

    def pull_release(self, as_of: date | None = None) -> Iterator[Observation]:
        for series_id in self.series_catalog:
            yield from self.pull_series(series_id)
```

## 6. Treasury adapter skeleton

```python
# src/opengem/adapters/treasury.py
import requests
from datetime import date
from typing import Iterator
from .base import Adapter, Observation

TREAS_BASE = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service"

class TreasuryAdapter(Adapter):
    source_id = "TREAS"

    series_catalog = {
        "US.TREAS.daily_yield_curve.10y":    ("/v2/accounting/od/daily_treasury_yield_curve_rates", "avg_interest_rate_amt", {"security_desc": "10-Year"}),
        # ... etc.
    }

    def pull_series(self, opengem_series_id: str) -> Iterator[Observation]:
        endpoint, field, filter_ = self.series_catalog[opengem_series_id]
        params = {
            "filter": ",".join(f"{k}:{v}" for k, v in filter_.items()),
            "fields": f"record_date,{field}",
            "format": "json",
            "page[size]": 1000,
        }
        while True:
            resp = requests.get(TREAS_BASE + endpoint, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            for row in data["data"]:
                yield Observation(
                    series_id=opengem_series_id,
                    observed_at=parse_treas_date(row["record_date"]),
                    vintage_at=date.today(),
                    value=float(row[field]),
                    source_id=self.source_id,
                    metadata=filter_,
                )
            if not data.get("links", {}).get("next"):
                break
            # paginate

    def pull_release(self, as_of: date | None = None) -> Iterator[Observation]:
        for series_id in self.series_catalog:
            yield from self.pull_series(series_id)
```

## 7. Census adapter skeleton

```python
# src/opengem/adapters/census.py
import os
import requests
from datetime import date
from typing import Iterator
from .base import Adapter, Observation

CENSUS_BASE = "https://api.census.gov/data"

class CensusAdapter(Adapter):
    source_id = "CENSUS"

    series_catalog = {
        "US.CENSUS.M3.inventory_to_sales.M": ("m3_advance", "cell_value", {"data_type_code": "IM", "category_code": "0"}),
        # ... etc.
    }

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("CENSUS_API_KEY")

    def pull_series(self, opengem_series_id: str) -> Iterator[Observation]:
        ...  # Census API specifics vary by endpoint; pattern is similar

    def pull_release(self, as_of: date | None = None) -> Iterator[Observation]:
        for series_id in self.series_catalog:
            yield from self.pull_series(series_id)
```

## 8. Adapter test skeleton

```python
# tests/adapters/test_bea.py
import pytest
from opengem.adapters.bea import BEAAdapter, parse_bea_period
from datetime import date

def test_parse_period():
    assert parse_bea_period("2026Q1") == date(2026, 1, 1)
    assert parse_bea_period("2024Q4") == date(2024, 10, 1)

@pytest.fixture
def golden_bea_response():
    """Pre-recorded BEA response for 2024Q4 GDP."""
    return {
        "BEAAPI": {
            "Results": {
                "Data": [
                    {"LineNumber": "1", "TimePeriod": "2024Q4",
                     "DataValue": "23,500.123", "UNIT_MULT": "billions_chained"}
                ]
            }
        }
    }

def test_pull_series_parsing(monkeypatch, golden_bea_response):
    """BEA adapter parses canonical response correctly."""
    class FakeResp:
        def json(self): return golden_bea_response
        def raise_for_status(self): pass

    monkeypatch.setattr("requests.get", lambda *a, **k: FakeResp())
    adapter = BEAAdapter(api_key="test-key")
    obs = list(adapter.pull_series("US.BEA.NIPA.GDP_real.Q"))
    assert len(obs) == 1
    assert obs[0].observed_at == date(2024, 10, 1)
    assert obs[0].value == 23500.123

@pytest.mark.integration
def test_pull_series_live():
    """Smoke test against actual BEA API (skipped in PR CI; runs in nightly)."""
    adapter = BEAAdapter()
    obs = list(adapter.pull_series("US.BEA.NIPA.GDP_real.Q"))
    assert len(obs) > 100  # at least 25 years of quarterly data
```

## 9. Storage write skeleton

```python
# src/opengem/storage/vintage.py
import hashlib
import json
from typing import Iterable
from sqlalchemy.orm import Session
from opengem.adapters.base import Observation, PullManifest

def write_vintage_batch(session: Session, source_id: str, observations: Iterable[Observation]) -> PullManifest:
    """Persist a batch of observations and compute the vintage_hash."""
    obs_list = sorted(observations, key=lambda o: (o.series_id, o.observed_at))
    series_pulled = sorted({o.series_id for o in obs_list})

    # Canonical bytes for hash
    canonical = "\n".join(
        f"{o.series_id}|{o.observed_at.isoformat()}|{o.vintage_at.isoformat()}|{o.value}"
        for o in obs_list
    ).encode("utf-8")
    vintage_hash = "sha256:" + hashlib.sha256(canonical).hexdigest()

    for o in obs_list:
        session.execute(
            "INSERT INTO raw_observation (series_id, observed_at, vintage_at, value) "
            "VALUES (:series_id, :observed_at, :vintage_at, :value) ON CONFLICT DO NOTHING",
            {"series_id": o.series_id, "observed_at": o.observed_at,
             "vintage_at": o.vintage_at, "value": o.value},
        )

    session.execute(
        "INSERT INTO vintage_snapshot (vintage_hash, source_id, manifest) "
        "VALUES (:hash, :src, :manifest)",
        {"hash": vintage_hash, "src": source_id,
         "manifest": json.dumps({"series_pulled": series_pulled, "n_obs": len(obs_list)})}
    )
    session.commit()

    return PullManifest(
        source_id=source_id,
        pulled_at=datetime.utcnow(),
        series_pulled=series_pulled,
        observation_count=len(obs_list),
        vintage_hash=vintage_hash,
    )
```

## 10. Bottom line

Five adapter skeletons + one storage skeleton + test patterns = ~600 lines of Python at IOC. Filling in the API specifics for each agency is bounded work; the architecture is set.

The skeletons are intentionally **boring**: standard requests + dataclasses + SQLAlchemy. No exotic dependencies. Easy to maintain or hand off.

---

*End of R19 Rev A.*
