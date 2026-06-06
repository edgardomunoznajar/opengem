# opengem-backtest

The **accountability engine** (a minimal SSDD-007): the thing that makes an
OPENGEM forecast *scored* rather than merely *issued*.

- `metrics` — CRPS (from quantiles + closed-form Gaussian), MAE, RMSE, PIT.
- `baselines` — AR(1) and random-walk density forecasts (the bars every model
  must clear).
- `replay` — rolling-origin backtest: at each historical quarter, fit the model
  and the baselines on data available then, forecast `h` quarters ahead, and
  score against the realized actual.
- `leaderboard` — aggregate per-model CRPS/MAE into leaderboard rows.
- `cli` — `opengem-backtest us` runs the whole thing for the US GDP/CPI panel.

CRPS is the primary metric (lower is better); the V&V bar for GDP-1Q is
"beat AR(1) and random-walk by CRPS."
