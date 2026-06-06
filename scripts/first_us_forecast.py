#!/usr/bin/env python
"""First real US forecast — the single command for Goal B.

FRED discovery -> vintage store -> backtest -> final forecast -> publish.

IMPORTANT: FRED is used here as ONE-TIME DISCOVERY only. OPENGEM's architecture
mandates upstream agencies (BEA/BLS/FRB) for production data; FRED's ToS forbids
caching/redistribution. So the raw pulled series land ONLY in a gitignored local
SQLite store (data/). We commit derived outputs (the forecast + scores) as a
JSON summary under docs/, never the raw FRED data.

The underlying series (real GDP, CPI, Treasury yields) are public-domain US
federal statistics; FRED is merely a convenient discovery mirror.

Usage:
    FRED_API_KEY=... python scripts/first_us_forecast.py
    # or it will read FRED_API_KEY / FRED_KEY from ../algotrader/.env
"""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path

from opengem_backtest.cli import _print_report, _publish
from opengem_backtest.run import RunResult, run_us_pipeline
from opengem_types import Observation, SeriesId, SeriesMeta
from opengem_vintage import SQLiteVintageStore

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data"
STORE_PATH = DATA / "us_vintage.sqlite"
SNAP_PATH = DATA / "us_forecast.db"
SUMMARY_PATH = REPO / "docs" / "first-us-forecast.json"

FRED_URL = "https://api.stlouisfed.org/fred/series/observations"

# (FRED id, canonical OPENGEM series id, source, variable_kind, frequency)
SERIES = [
    ("GDPC1", "US.BEA.NIPA.GDP_real.Q", "BEA", "gdp_real", "Q"),
    ("CPIAUCSL", "US.BLS.CPI.headline_SA.M", "BLS", "cpi_headline", "M"),
]


def _fred_key() -> str:
    for var in ("FRED_API_KEY", "FRED_KEY"):
        if os.environ.get(var):
            return os.environ[var]
    env = REPO.parent / "algotrader" / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            for var in ("FRED_API_KEY=", "FRED_KEY="):
                if line.startswith(var):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("No FRED key found (set FRED_API_KEY, or run the offline pipeline test).")


def _fetch(fred_id: str, key: str, start: str = "1960-01-01") -> list[tuple[date, float]]:
    query = urllib.parse.urlencode(
        {"series_id": fred_id, "api_key": key, "file_type": "json", "observation_start": start}
    )
    with urllib.request.urlopen(f"{FRED_URL}?{query}", timeout=60) as resp:
        payload = json.load(resp)
    out: list[tuple[date, float]] = []
    for obs in payload.get("observations", []):
        raw = obs.get("value")
        if raw in (".", "", None):
            continue
        out.append((date.fromisoformat(obs["date"]), float(raw)))
    return out


def _summary(result: RunResult) -> dict:
    head = result.headline("gdp_yoy", "1Q")
    targets = []
    for tr in result.targets:
        targets.append(
            {
                "target": tr.target,
                "n_origins": tr.n_origins,
                "leaderboard": tr.leaderboard,
                "final_forecast": [
                    {
                        "horizon": f"{f.horizon_q}Q",
                        "scoring_period": f"{f.forecast_for_period.year}Q{(f.forecast_for_period.month - 1) // 3 + 1}",
                        "p10": round(f.quantiles.p10, 3),
                        "p50": round(f.quantiles.p50, 3),
                        "p90": round(f.quantiles.p90, 3),
                    }
                    for f in tr.forecasts
                ],
            }
        )
    return {
        "generated_at": datetime.now().astimezone().isoformat(),
        "vintage_date": result.vintage_date,
        "panel_quarters": result.panel_quarters,
        "base_period": result.base_period,
        "data_source": "FRED discovery (real US public-domain series)",
        "headline_gdp_yoy_1Q": head,
        "targets": targets,
    }


def main() -> int:
    key = _fred_key()
    DATA.mkdir(exist_ok=True)
    if STORE_PATH.exists():
        STORE_PATH.unlink()

    store = SQLiteVintageStore(str(STORE_PATH))
    store.initialize()
    today = date.today()
    print(f"Pulling real US series from FRED (discovery) as-of {today} ...")
    for fred_id, sid, src, kind, freq in SERIES:
        store.register_source(src, src)
        store.register_series(
            SeriesMeta(
                series_id=SeriesId(sid), source=src, description=f"FRED:{fred_id}",
                unit="index", frequency=freq, country="US", variable_kind=kind,
            )
        )
        pairs = _fetch(fred_id, key)
        obs = [
            Observation(
                series_id=SeriesId(sid), observed_at=d, vintage_at=today, value=v,
                source=src, metadata={"fred_id": fred_id, "discovery": "FRED"},
            )
            for d, v in pairs
        ]
        store.write_batch(obs, src, datetime.now())
        print(f"  {fred_id:10s} -> {sid:28s} {len(obs):4d} obs  ({pairs[0][0]} .. {pairs[-1][0]})")

    result = run_us_pipeline(store, today.isoformat(), horizons=(1, 4), min_train=40, max_origins=24)
    store.close()

    _print_report(result)
    _publish(result, str(SNAP_PATH))

    SUMMARY_PATH.write_text(json.dumps(_summary(result), indent=2))
    print(f"\nwrote derived summary -> {SUMMARY_PATH.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
