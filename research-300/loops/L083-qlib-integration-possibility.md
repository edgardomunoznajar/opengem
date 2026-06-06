# L083 — Qlib Integration Possibility for the Forecast Pipeline

**Loop**: 083 / 300
**Phase**: 2 — Integration deep dive
**Date**: 2026-06-06
**Verdict**: **REJECT-WITH-REASON (asset class mismatch; steal three patterns, ignore the runtime)**

---

## Why this loop exists, and why it ends fast

L012 already concluded Qlib is "0% as substrate, 25% as reference pattern, 60% on the data layer" for OPENGEM. This Phase 2 loop's job is to *close the question with prejudice* by walking through what an actual Qlib integration would look like, demonstrating the cost, and recording the three specific patterns worth stealing without adopting the runtime. After this loop, Qlib is a closed chapter: cite it, learn from it, do not depend on it.

The forcing question is simple. OPENGEM's forecast pipeline lives in three layers:
- **L1** — deterministic baselines and consensus rebroadcasts (RW, AR(1), WEO, OECD EO).
- **L2** — single-method probabilistic forecasters (statsmodels DFM nowcast, Nixtla statsforecast ensemble, neuralforecast variants).
- **L3** — combiner over L2 variants, vintage-conditioned, with calibrated uncertainty.

Does Qlib fit anywhere in this stack? Inspecting `microsoft/qlib`'s actual structure — model zoo, expression engine, workflow YAML, backtester — the answer is no. Here is why, point by point, with the specific things worth stealing pulled out.

## The four-line rejection

1. **Output type mismatch.** Qlib produces point predictions of cross-sectional returns ranked into a portfolio. OPENGEM produces full predictive densities (P10/P50/P90 minimum) of macroeconomic levels, vintaged. Adapting any Qlib model to emit quantiles requires rewriting the `Record` / `SignalRecord` IC/rank-IC scoring layer. ~3 dev-weeks per model.
2. **No mixed-frequency story.** Qlib assumes one fundamental frequency per dataset. Our DFM workhorse is mixed-frequency by construction (quarterly GDP + monthly hard data + daily financial conditions). MIDAS / MF-DFM are not in Qlib's model zoo.
3. **No vintage discipline.** Qlib stores "latest as of now." OPENGEM's accountability thesis depends on (as_of_release_date, vintage_published_at). Bolting vintaging onto Qlib's data layer requires rewriting its on-disk format and breaks every cached pipeline.
4. **Asset class mismatch in the backtester.** Qlib's backtester is order-book-aware, position-sizing-aware, and TopkDropout-portfolio-aware. None of that applies to "did we predict Q4 GDP within the 95% credible band." We need a CRPS / log-score / PIT evaluator, which is none of Qlib's surface.

That's the verdict. Below is the cost of doing it anyway, and the three patterns worth stealing.

## What a forced integration costs

Suppose for argument we *did* try to use Qlib as the L2/L3 backbone. The integration plan would be:

- **Vintage adapter** (Qlib data layer → OPENGEM vintage store): ~4 dev-weeks. Qlib's expression DSL knows nothing about vintage axes. We'd add a third dimension to every dataset slot, modify the cache key, modify the expression engine to allow `Vintage(...)` operators, modify the loader. This is forking Qlib's data layer.

- **Quantile output for every L2 model**: ~3 dev-weeks per model × ~6 models = ~18 dev-weeks. The Qlib `Record` abstraction assumes scalar predictions. Quantile-aware records require subclassing or replacing `SignalRecord`, then redoing every model's prediction loop.

- **Mixed-frequency injection** into Qlib's dataset: ~6 dev-weeks. Qlib's `DatasetH` assumes a single time index. MIDAS / MF-DFM require per-feature frequency and a Mariano-Murasawa aggregation rule. Building that into Qlib's typed dataset is a rewrite.

- **Probabilistic scoring** (CRPS / log-score / PIT): ~2 dev-weeks. Qlib has zero infrastructure here. We'd add it from scratch.

- **Cross-country pooling rules**: ~3 dev-weeks. Qlib pools cross-sectional within an asset class; cross-country pooling for macro variables uses different conditioning logic (per L203).

**Total**: ~36 dev-weeks (~9 months) to bend Qlib into OPENGEM-shaped. For comparison, building L2/L3 native on statsmodels + PyMC + Nixtla statsforecast / neuralforecast + a CRPS-aware evaluator is ~12-16 dev-weeks (per the R14 architecture estimate). **Qlib costs us 2-3x more, with the additional risk of being out-of-step with both Qlib upstream and our own use case.** Reject.

## The three patterns worth stealing

Even though Qlib the runtime is rejected, three specific patterns in its source are good ideas worth re-implementing in OPENGEM-native form. We steal the *idea*, not the code.

### Pattern 1 — Expression DSL over a typed panel

Qlib's `Ref($close, -3) / $close - 1` syntax is a small DSL for "this feature is a transformation of these other features in the panel, computed lazily on read." Pattern is worth borrowing.

For OPENGEM, the equivalent would be:

```python
opengem.expr.eval(
    "(Lag(cpi, 3) - cpi) / Lag(cpi, 3) * 100",
    country="USA",
    vintage_at=date(2024, 9, 1),
)
```

The DSL gives analysts (and LLMs prompted to write OPENGEM queries) a compact, readable way to declare derived features without writing pandas. This lands cleanly in the eventual L210 counterfactual scenario engine, where the scenario is *itself* a set of derived feature expressions.

**Cost to build**: ~2 dev-weeks for a v1 DSL with ~20 operators (Lag, Diff, Pct, RollMean, RollStd, ZScore, MA, EWM, Resample, ...).

### Pattern 2 — Workflow YAML for reproducible runs

Qlib's `workflow.yaml` is:

```yaml
qlib_init:
  provider_uri: "~/.qlib/qlib_data/cn_data"
market: csi300
benchmark: SH000300
task:
  model:
    class: LGBModel
    kwargs: {learning_rate: 0.0421}
  dataset:
    class: DatasetH
    kwargs:
      handler:
        class: Alpha158
        kwargs: {start_time: 2008-01-01, ...}
      segments:
        train: [2008-01-01, 2014-12-31]
        valid: [2015-01-01, 2016-12-31]
        test: [2017-01-01, 2020-08-01]
```

Declarative pipeline configs that survive reruns. For OPENGEM the equivalent is a per-forecast `run.yaml`:

```yaml
opengem_run:
  vintage_at: 2026-06-06
  target:
    country: USA
    indicator: gdp_real_growth
    horizon: 1Q
  model:
    class: opengem.l3.dfm.DynamicFactor
    config: configs/dfm_us_v3.yaml
  panel:
    series: configs/panels/us_tier_v.yaml
    sample: [2000-01-01, 2026-05-31]
  seed: 42
  reproducibility:
    lockfile: pdm.lock
    container_digest: sha256:abc...
```

This is the reproducibility envelope from L186. Borrowing the *idea* from Qlib (declarative + version-controlled + LLM-readable) is the right call. Borrowing the *schema* is not — we want a vintage-aware version. **Cost**: implicit, lands in L186 as the artifact.

### Pattern 3 — `qlib.contrib.report` for HTML render

Qlib ships a static HTML report after every backtest run: charts, attribution tables, run config dump. It's not pretty, but it's *automatic*. Every model run produces a static HTML report committed alongside the model output.

For OPENGEM, the equivalent is the per-forecast **methodology card + track-record sheet** that ships HTML at `https://opengem.org/m/{model_id}/{run_id}.html`. Self-contained, embeddable, citable. The pattern Qlib uses is the right one; Observable Framework (L066, L091) is the right tooling to *implement* it. Borrow the idea, not the renderer.

## The RD-Agent surprise

Qlib's README links prominently to **Microsoft RD-Agent**, an LLM-driven research-automation system. RD-Agent is where Microsoft's quant research team has shifted compute. The Qlib repo itself is now in "mature, selective-improvement" mode.

The strategic read: Qlib is moving from a *workhorse* to a *reference example* for RD-Agent demonstrations. New macro forecasting features are unlikely to land in Qlib's mainline. **For OPENGEM, this means betting on Qlib's roadmap is doubly wrong — it's not just asset-class-mismatched, it's also not where the upstream attention is.**

If RD-Agent matures into a generic forecast-research-automation agent (which seems to be its direction), it becomes worth a separate Phase 5 evaluation — not as a runtime substrate, but as an *internal tool* the OPENGEM team uses to author new L3 ensemble members. That's L255-ish or beyond.

## What we cite from Qlib regardless

OPENGEM's L133 forecast leaderboard already includes a "platform / framework" column. Qlib's mature deep-learning baselines (ALSTM, TFT, Transformer with quant-research-tuned defaults) become *citation entries* — when a user asks "what would a Microsoft-Qlib-style equity-RTN-prediction model look like applied to macro," we have a methodologically-comparable benchmark in mind. We may even run a benchmark Qlib-style model on macro data once, score it on CRPS, and publish the result as L200-style ledger evidence. The point is to publish the comparison openly, not adopt the runtime.

## The integration order verdict

Phase 2 schedule for Qlib: **NEVER**.

We do not write `import qlib` anywhere in the OPENGEM codebase. We may run Qlib in a notebook for one paper-vs-paper comparison study (Phase 6, post-launch). The DSL idea (Pattern 1) lands in OPENGEM as a 2-dev-week native build in Phase 5. The workflow-config idea (Pattern 2) lands in L186 implicitly. The auto-HTML-report idea (Pattern 3) lands in L091 via Observable Framework.

## What this loop produced

- Cost-of-forced-integration estimate (~36 dev-weeks) vs native build (~12-16 dev-weeks), with the 2-3x penalty justifying rejection.
- Three patterns worth stealing (expression DSL, workflow YAML, auto HTML report) with concrete OPENGEM-native landing points.
- The RD-Agent strategic note: Qlib's upstream attention has moved.
- A clean reject-with-reason that closes the Qlib question for the rest of the 300 loops.

## What comes next

- **L086** — NY Fed Nowcasting: where Qlib's seat is *actually* better filled.
- **L087** — Bayesian VAR Python stack: the other substrate question that Qlib won't help.
- **L088** — neuralforecast for L3 layer: the modern alternative to Qlib's deep-learning baselines.
- **L186** — Reproducibility envelope: where the workflow-YAML idea lands.

## Related

- [[L012-qlib]] — Phase 1 deep dive.
- [[L044-nixtla-stack]] — the modern forecasting alternative.
- [[L086-nyfed-nowcasting-reuse-vs-rewrite]] — what fills Qlib's seat.
- [[L087-bayesian-var-python-consolidation]] — adjacent question.
- [[L186-reproducibility-envelope]] — workflow YAML lands here.
- [[L210-counterfactual-scenarios]] — DSL pattern lands here.
- inspected source: `microsoft/qlib` README + L012 prior analysis.
