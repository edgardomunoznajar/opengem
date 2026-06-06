"""`opengem-backtest us` — run the US forecast + backtest from a vintage store."""

from __future__ import annotations

import argparse
from datetime import date

from opengem_vintage import SQLiteVintageStore

from opengem_backtest.persist import _period_str
from opengem_backtest.run import RunResult, run_us_pipeline


def _print_report(result: RunResult) -> None:
    print(
        f"\nOPENGEM US run — vintage {result.vintage_date} — "
        f"panel {result.panel_quarters} quarters (through {result.base_period})\n"
    )
    for tr in result.targets:
        print(f"== {tr.target} ==  (backtest over {tr.n_origins} origins)")
        print(
            f"  {'rank':>4} {'model':<16} {'hzn':>4} {'CRPS':>8} "
            f"{'CRPS~med':>9} {'MAE':>8} {'hit80':>6} {'n':>4}"
        )
        for row in tr.leaderboard:
            print(
                f"  {row['rank']:>4} {row['model']:<16} {row['horizon']:>4} "
                f"{row['crps']:>8.3f} {row['crps_median']:>9.4f} "
                f"{row['mae']:>8.4f} {row['hit_rate']:>6.2f} {row['n']:>4}"
            )
        print("  final forecast (latest vintage):")
        for f in tr.forecasts:
            q = f.quantiles
            print(
                f"    {f.horizon_q}Q -> {_period_str(f.forecast_for_period)}: "
                f"p50={q.p50:6.2f}  [p10={q.p10:6.2f}, p90={q.p90:6.2f}]"
            )
        print()

    head = result.headline("gdp_yoy", "1Q")
    if head:
        verdict = "BEATS" if head["beats_ar1"] else "does NOT beat"
        print(
            f"HEADLINE (gdp_yoy 1Q): DFM CRPS={head['crps_dfm']:.4f} vs "
            f"AR(1)={head['crps_ar1']:.4f} vs RW={head['crps_rw']:.4f} "
            f"-> DFM {verdict} AR(1) over {head['n']} origins"
        )


def _publish(result: RunResult, out_path: str) -> None:
    from opengem_datasette import snapshot_to_sqlite

    from opengem_backtest.persist import forecast_records

    recs: list[dict] = []
    for tr in result.targets:
        recs += forecast_records(
            tr.forecasts,
            vintage_id=result.vintage_date,
            base_period=result.base_period,
            badges=["real-data", "discovery:FRED"],
        )
    snapshot_to_sqlite(out_path, vintage=date.fromisoformat(result.vintage_date), forecasts=recs)
    print(f"published datasette snapshot -> {out_path} ({len(recs)} forecasts)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="opengem-backtest", description=__doc__)
    parser.add_argument("command", choices=["us"], help="which pipeline to run")
    parser.add_argument("--store", required=True, help="path to the SQLite vintage store")
    parser.add_argument("--vintage", required=True, help="ISO vintage date, e.g. 2026-06-06")
    parser.add_argument("--max-origins", type=int, default=None, help="cap backtest origins (speed)")
    parser.add_argument("--publish", default=None, help="write a Datasette snapshot .db to this path")
    args = parser.parse_args(argv)

    store = SQLiteVintageStore(args.store)
    try:
        result = run_us_pipeline(store, args.vintage, max_origins=args.max_origins)
    finally:
        store.close()

    _print_report(result)
    if args.publish:
        _publish(result, args.publish)
    return 0
