"""opengem-snapshot CLI — produce a SQLite snapshot of a vintage.

Usage:
    opengem-snapshot --vintage 2026-06-06 --out opengem-2026-06-06.db

The CLI is intentionally thin: it loads from whatever VintageStore is
available via the environment and delegates to ``snapshot_to_sqlite``. The
real work is in the snapshot module.

When ``--vintage today`` is passed, today's UTC date is used.

When ``--vintage demo`` is passed, the CLI emits a snapshot from bundled
fixture data — useful for local Datasette deploys before the production
backend is wired.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, date, datetime
from pathlib import Path

from opengem_datasette.snapshot import snapshot_to_sqlite, write_metadata


def _parse_vintage(arg: str) -> date:
    if arg == "today":
        return datetime.now(UTC).date()
    return date.fromisoformat(arg)


def _load_demo_fixtures():
    """Load the dashboard's fixture JSON if available; else use a tiny inline set."""
    candidates = (
        Path(__file__).parent.parent.parent.parent.parent
        / "research-300"
        / "prototypes"
        / "dashboard-next"
        / "data",
        Path.cwd() / "research-300" / "prototypes" / "dashboard-next" / "data",
    )
    base = next((c for c in candidates if c.is_dir()), None)
    if base is None:
        return [], [], [], []

    def _load(name: str):
        p = base / name
        if not p.exists():
            return []
        try:
            return json.loads(p.read_text())
        except (OSError, json.JSONDecodeError):
            return []

    forecasts = _load("fixtures.forecasts.json")
    scenarios = _load("fixtures.scenarios.json")
    # Synthetic observations from the situation tiles
    situation = _load("fixtures.situation.json")
    observations = []
    for tile in situation:
        country = tile.get("country") or "WORLD"
        observations.append({
            "series_id": f"{country}.OPENGEM.{tile['kind']}.tile.D",
            "observed_at": tile.get("as_of"),
            "vintage_at": tile.get("as_of"),
            "value": tile.get("value"),
            "source": "OPENGEM",
            "metadata": {"country": country, "kind": tile["kind"]},
        })
    return observations, forecasts, scenarios, []


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="opengem-snapshot",
        description="Export an OPENGEM vintage snapshot to SQLite for Datasette.",
    )
    p.add_argument(
        "--vintage",
        required=True,
        help="Vintage date (YYYY-MM-DD), 'today', or 'demo' for fixture-driven snapshot.",
    )
    p.add_argument(
        "--out",
        default="opengem-snapshot.db",
        help="Output SQLite path. Default: opengem-snapshot.db.",
    )
    p.add_argument(
        "--metadata",
        default=None,
        help="Emit a Datasette metadata.yaml at this path (default: <out>.metadata.yaml).",
    )
    args = p.parse_args(argv)

    if args.vintage == "demo":
        observations, forecasts, scenarios, misses = _load_demo_fixtures()
        vintage = datetime.now(UTC).date()
    else:
        vintage = _parse_vintage(args.vintage)
        try:
            from opengem_vintage import VintageStore  # type: ignore[import-not-found]
        except ImportError:
            print(
                "ERROR: opengem_vintage not available. Use --vintage demo to emit "
                "fixture-driven snapshot instead.",
                file=sys.stderr,
            )
            return 2
        store = VintageStore.from_settings()  # type: ignore[attr-defined]
        observations = store.list_observations(vintage_at=vintage)
        forecasts = store.list_forecasts(vintage_at=vintage)
        scenarios = store.list_scenarios(vintage_at=vintage)
        misses = store.list_misses(vintage_at=vintage)

    out = snapshot_to_sqlite(
        args.out,
        vintage=vintage,
        observations=observations,
        forecasts=forecasts,
        scenarios=scenarios,
        misses=misses,
    )
    print(f"wrote {out}")

    metadata_path = Path(args.metadata) if args.metadata else out.with_suffix(".metadata.yaml")
    write_metadata(metadata_path, vintage=vintage)
    print(f"wrote {metadata_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
