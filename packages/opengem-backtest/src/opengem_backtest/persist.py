"""Turn final forecasts into the datasette publication shape.

The ``forecasts`` table that the public Datasette/API/dashboard consume expects
flat records with nested ``bands``/``provenance``; see opengem-datasette. This
module converts ``DensityForecast`` records into that shape.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


def _period_str(d: Any) -> str:
    """A date -> 'YYYYQn' quarter label."""
    if hasattr(d, "year") and hasattr(d, "month"):
        return f"{d.year}Q{(d.month - 1) // 3 + 1}"
    return str(d)


def forecast_records(
    forecasts: list[Any],
    *,
    vintage_id: str,
    base_period: str,
    model_id: str = "opengem_l3_dfm_v0.1",
    model_card_url: str | None = "https://opengem.org/methodology/l3-dfm",
    git_sha: str | None = None,
    data_lockfile_hash: str | None = None,
    badges: list[str] | None = None,
) -> list[dict]:
    """Convert DensityForecast records into datasette ``forecasts`` input dicts."""
    generated_at = datetime.now(UTC).isoformat()
    out: list[dict] = []
    for f in forecasts:
        q = f.quantiles
        out.append(
            {
                "vintage_id": vintage_id,
                "model_id": model_id,
                "model_card_url": model_card_url,
                "country": str(f.country),
                "indicator": str(f.variable),
                "horizon": f"{f.horizon_q}Q",
                "base_period": base_period,
                "scoring_period": _period_str(f.forecast_for_period),
                "point": float(q.p50),
                "bands": {"p10": float(q.p10), "p50": float(q.p50), "p90": float(q.p90)},
                "provenance": {
                    "git_sha": git_sha,
                    "data_lockfile_hash": data_lockfile_hash,
                    "generated_at": generated_at,
                },
                "badges": badges or ["real-data"],
            }
        )
    return out
