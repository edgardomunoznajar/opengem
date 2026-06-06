# L013 — Backtrader / VectorBT / Zipline-Reloaded: The Dashboarding Angle

**Loop**: 013 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Why this loop exists

These three are the canonical Python backtesting frameworks. They will not be the substrate of OPENGEM — we don't backtest equity strategies, we backtest *macro forecasts against vintages* (different math, see L185). But each emits a distinctive *visual artifact* that has been refined by hundreds of thousands of users. Looking at what they ship by default tells us what a "credible quant tearsheet" looks like in 2026, which informs every forecast page (L195), track-record page (L134), and accountability ledger page (L175) we'll build.

## The three repos at a glance

| Repo | GitHub | Stars | License | Last commit | Plot story |
|---|---|---|---|---|---|
| **Backtrader** | [mementum/backtrader](https://github.com/mementum/backtrader) | 21.8k | GPL-3.0 | Aug 2024 (mostly dormant) | Matplotlib only, static |
| **VectorBT** | [polakowo/vectorbt](https://github.com/polakowo/vectorbt) | 7.8k | Apache 2.0 + **Commons Clause** | Apr 2026 (v1.0.0 active) | Plotly + ipywidgets, interactive |
| **Zipline-Reloaded** | [stefan-jansen/zipline-reloaded](https://github.com/stefan-jansen/zipline-reloaded) | 1.8k | Apache 2.0 | Jan 2026 (selective maintenance) | None — outputs DataFrame, you BYO plotting (typically pyfolio-reloaded) |

### License flags

- **Backtrader = GPL-3.0**. Same contamination risk as OpenBB's AGPL — any code that links Backtrader at runtime inherits GPL. We avoid.
- **VectorBT = Apache 2.0 + Commons Clause**. Commons Clause is a non-OSI clause that forbids "selling the software." For OPENGEM, where the paid tier is API throughput rather than reselling the codebase, this is **probably fine** — but it makes VectorBT not-quite-FOSS, and any white-label-embed customer asking "is your stack 100% Apache/MIT?" gets a "well, except for…" answer. We avoid.
- **Zipline-Reloaded = Apache 2.0**. Clean. The boring choice is the safe choice.

## What each one *emits* visually

### Backtrader → static matplotlib panels

The default `cerebro.plot()` produces a multi-panel chart:
- Top: equity curve.
- Middle band per indicator: indicator value with shaded buy/sell zones.
- Bottom: candlestick OHLC with overlaid trade markers (green/red triangles), volume bars.
- Side annotations: cash, position size, broker value.

Aesthetic: 2012-era matplotlib, no interactivity, PNG-export-only. Looks like a textbook. Not useless for printable tearsheets (L143) — actually quite good for *PDF export* because it's static-first. But not what OPENGEM's live dashboard wants.

### VectorBT → Plotly interactive dashboards

VectorBT was built from day one around Plotly. Its `Portfolio.plot()` method returns a `plotly.graph_objects.Figure` that you can mutate, embed, or convert to JSON. The default output:
- Equity curve with shaded drawdown bands.
- Per-trade scatter (color-coded P&L).
- Returns distribution with VaR markers.
- Heatmap of parameter-sweep results — the *one* artifact VectorBT does better than anything else (a 2D heatmap of Sharpe over (lookback_window × stop_loss) is its signature image).
- Subplot composition: dynamic adding via `vbt.plotting.make_subplots()`.

It also ships first-class **QuantStats** integration: `Portfolio.stats()` → DataFrame, then `quantstats.reports.html(returns, output='tearsheet.html')` produces a self-contained HTML report with sortino, calmar, omega, monthly heatmap, drawdown underwater plot, rolling sharpe — all in Plotly.

This is the most studyable artifact in the three-repo set. The Plotly call patterns transfer directly. OPENGEM's forecast page (L195) needs an analog of that heatmap-of-parameter-sweeps: ours would be a heatmap of (model_variant × forecast_horizon) MAE or CRPS, vintage-conditioned. The visual idiom is identical.

### Zipline-Reloaded → nothing, by design

Zipline outputs a tidy pandas DataFrame with columns `period_open, period_close, returns, sharpe, max_drawdown, portfolio_value`, etc. No plotting is in scope. The companion library is **pyfolio-reloaded** (also Stefan Jansen), which generates a multi-page PDF tearsheet via matplotlib. Pyfolio is deprecated-feeling — most users now pipe Zipline DataFrames straight into QuantStats instead.

## What we steal for OPENGEM

### Steal (visual idioms)

1. **The Plotly subplot grid from VectorBT.** Forecast page = top panel (point + band), middle panel (consensus overlay), bottom panel (revision history). The vbt subplot composition pattern is the template.
2. **The QuantStats HTML tearsheet.** Self-contained-HTML-with-embedded-Plotly is the right pattern for our "cite-this-view" exports (L155, L158). One HTML file, no server roundtrip, embeddable in Substack and Medium.
3. **The parameter-sweep heatmap.** Reframed: (model × horizon) calibration heatmap, (country × indicator) coverage heatmap, (vintage × horizon) miss heatmap.
4. **The drawdown underwater plot.** Reframed: forecast-miss underwater plot — y-axis is "rolling 4Q forecast MAE", x-axis is calendar time, shaded recessions. *This single chart is the central visual of the accountability ledger.* I'm calling it now.
5. **Backtrader's PDF-first export discipline.** Even though matplotlib looks dated, the fact that it renders identically in print is gold for the L143 tearsheet PDF.

### Don't steal

1. **The frameworks themselves.** None of them backtest macro forecasts. The math is wrong (Sharpe assumes daily IID returns; macro forecast scoring is CRPS over quarterly densities). Build the evaluator native.
2. **Backtrader's matplotlib defaults.** Too dated.
3. **Zipline's bundle abstraction.** Bundles assume equity OHLC; vintages assume `(country, indicator, release_date, as_of_date)` panel.

## License decision

OPENGEM dashboard will **import none of the three** at runtime. We'll use Plotly directly (Apache 2.0/MIT — see L062), QuantStats only on internal eval scripts (and even there, optional). License surface stays clean.

## Cost-benefit, if we ever wanted to integrate

| Action | Cost | Benefit |
|---|---|---|
| Bolt VectorBT under forecast-eval | 2 weeks + Commons Clause headache | Net negative — wrong scoring math |
| Steal Plotly subplot idiom for forecast page | 0.5 week | Direct |
| Steal QuantStats HTML pattern for cite-this-view | 1 week | Direct, big win |
| Adopt pyfolio-reloaded for PDF tearsheets | 1 week | Maybe — see L246 |

## Surprise of the loop

**Backtrader's last commit was August 2024 — i.e. the most-starred Python backtester is effectively unmaintained.** It still gets pip-installed thousands of times per week. There's a real product opportunity for a "Backtrader 2.0" with Plotly defaults under a clean Apache license, but that's not OPENGEM's fight.

## What this loop produced

- Three-row repo summary with license traps named (GPL, Commons Clause, Apache).
- A library of *visual idioms* worth stealing, each tied to a downstream OPENGEM loop.
- The "forecast-miss underwater plot" as the load-bearing chart for the accountability ledger.

## What comes next

- **L014** — Finos Perspective: the streaming-grid story for live indicator pages.
- **L015** — TradingView Lightweight Charts: forecast bands + consensus overlay.
- **L062** — Dash (Plotly) deep dive: the Plotly server-side story.
- **L175** — Accountability page using the underwater-miss chart.
- **L246** — Print-tearsheet prototype (server-side SVG → PDF).

## Related

- [[L001-vision-statement]] — "publishes its mistakes" demands the underwater-miss chart.
- [[L011-openbb-terminal]] — license-flag pattern (AGPL/GPL/CC vs Apache/MIT).
- [[L014-finos-perspective]] — streaming grid complement to these PDF-tearsheet idioms.
- [[L015-lightweight-charts]] — the live-chart half of the visual stack.
- [[L175-accountability-page]] — the home of the underwater-miss chart.
