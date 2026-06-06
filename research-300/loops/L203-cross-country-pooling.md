# L203 — Cross-Country Pooling Rules

**Loop**: 203 / 300
**Phase**: 4 — Forecasting product mechanics
**Date**: 2026-06-06

---

## The decision

A persistent question in panel macroeconometrics: when do we *pool* parameter estimates across countries (one model, all countries share coefficients) and when do we keep them *separate* (one model per country, country-specific coefficients)? Wrong answer in either direction degrades forecast skill.

This loop pins the decision tree for L3 variants in OPENGEM, the diagnostic test we run, and the hybrid mean-group / Bayesian shrinkage approach we default to.

## The trilemma

For a panel of N countries and T observations each, three choices:

1. **Fully pooled**: One coefficient set. Treats all countries as observationally equivalent. Maximum statistical efficiency but vulnerable to country heterogeneity bias.
2. **Fully separated**: N coefficient sets. Maximum flexibility but each country uses only T observations; in small T regimes (Tier-T countries, recent vintages) this is data-starved.
3. **Hybrid / partial pooling**: One *prior* over coefficients with country-specific posteriors. Shares signal across countries while allowing heterogeneity. The Bayesian middle path.

The literature consensus (Hsiao 1986, Pesaran 2006, Chudik-Pesaran 2015) is that *partial pooling dominates* in most panel macro settings when N is moderate (5-30) and T is moderate (50-200 quarters). OPENGEM's Tier-V Core sits exactly in this regime.

## The decision tree

```
For a given L3 variant V applied to a panel of countries C:

  Q1: Is N ≥ 5 AND T ≥ 40 for at least one indicator?
      NO  → keep country-separate (no pooling); use country-specific posteriors only.
      YES → continue to Q2.

  Q2: Does a Pesaran (2006) CD test on residuals reject cross-section independence?
      YES → strong evidence of common factors; use a *common factor* model
            (DFM with shared factors + country-specific loadings).
            Pool the factor structure; separate the loadings.
      NO  → continue to Q3.

  Q3: Does a Hausman test reject homogeneous coefficients?
      YES → coefficient heterogeneity present; use *mean-group + shrinkage*
            (Bayesian hierarchical with country-level coefficients drawn from
             a global prior whose variance is learned).
      NO  → coefficients are homogeneous; use fully pooled model.

  Q4: Does Q2 OR Q3 yield non-trivial pooling AND is the cell on the leaderboard
      (Tier-V Core only)?
      YES → publish pooled forecast.
      NO  → fall back to country-separate or fully pooled per Q1/Q3.
```

The tests are evaluated per L3 variant, per indicator, per horizon, at each weights-recompute epoch (quarterly).

## What "pooling" means per L3 variant

| Variant | Pooling strategy when triggered |
|---|---|
| L3-DFM | Common dynamic factors; country-specific loadings + idiosyncratic components. (Standard DFM panel formulation; Stock-Watson 2002.) |
| L3-ML-RIDGE | Hierarchical ridge: global coefficient vector β as prior; country-specific β_i shrunk toward β. (Multitask learning with Bayesian shrinkage.) |
| L3-BVAR-LARGE | Cross-country BVAR with Minnesota prior + cross-section restrictions; or Banbura-Giannone-Reichlin large BVAR with country fixed effects. |
| L3-TVP-VAR (L204) | Less suitable for pooling; typically country-separate. |
| L3-MF-DFM (L205) | Same pooling as L3-DFM. |

## The diagnostic test cadence

Pesaran CD and Hausman tests are computed quarterly on each `(variant, indicator, horizon)` cell. Results are stored in a `pooling_diagnostics` table:

```json
{
  "schema": "opengem.pooling_diagnostics.v1",
  "cell": {"variant": "L3-DFM", "indicator": "GDP-real-yoy", "horizon_q": 4},
  "computed_at": "2026-10-01T00:00:00Z",
  "n_countries": 26,
  "t_observations_min": 64,
  "t_observations_max": 112,
  "pesaran_cd_stat": 8.42,
  "pesaran_cd_pvalue": 0.0001,
  "pesaran_cd_reject_independence": true,
  "hausman_chi2": 5.32,
  "hausman_pvalue": 0.04,
  "hausman_reject_homogeneity": true,
  "pooling_recommendation": "common_factors_with_country_loadings",
  "recommendation_changed_from_last_quarter": false
}
```

## When pooling helps, when it hurts

Empirical guidance from prior macro panel work:

| Indicator | Pooling typical verdict | Reason |
|---|---|---|
| GDP-real-yoy (Tier-V Core) | Pool factors, separate loadings | Common global cycle exists; country-specific transmission differs |
| CPI-headline-yoy | Pool partially; energy/food separation | Common commodity shock; country-specific monetary transmission |
| Unemployment | Country-separate | Labour markets are highly country-specific (institutions) |
| Policy rate | Country-separate | Independent central banks |
| Recession-prob 12m | Mostly separate but use cross-country residual checks | Term spread structure differs |
| Trade-weighted FX | Pool a lot | Global FX market |

OPENGEM's IOC default is *partial pooling for GDP and CPI, country-separate for UR and policy rate*. The diagnostic tests in the loop can override this on a case-by-case basis.

## Implementation: the Bayesian hierarchical sketch

For the L3-ML-RIDGE variant with partial pooling, the Stan / PyMC implementation:

```python
# packages/opengem-l3-ml/src/opengem_l3_ml/hierarchical.py

import pymc as pm

with pm.Model() as model:
    # Global prior on coefficients
    mu_beta = pm.Normal("mu_beta", mu=0, sigma=1, shape=K_FEATURES)
    tau_beta = pm.HalfCauchy("tau_beta", beta=0.5, shape=K_FEATURES)

    # Country-specific coefficients drawn from global prior
    beta_country = pm.Normal(
        "beta_country",
        mu=mu_beta[None, :],
        sigma=tau_beta[None, :],
        shape=(N_COUNTRIES, K_FEATURES),
    )

    # Observation model
    for c in range(N_COUNTRIES):
        y_c = pm.Normal(
            f"y_{c}",
            mu=X[c] @ beta_country[c, :],
            sigma=sigma_c,
            observed=y[c],
        )

    posterior = pm.sample(draws=2000, tune=1000)
```

The hierarchy lets countries with thin data borrow from countries with rich data, while still allowing each country's coefficient to differ. `tau_beta` learned from data — when it is small, pooling is strong; when large, country-separate dominates.

## Validating that pooling improves forecasts

After pooling weight is set, OPENGEM compares:

- Pooled-variant predictive density.
- Country-separate variant predictive density.
- Equal-weight combination of the two.

On the holdout fold, the rule is: ship the variant (or combination) with lowest holdout CRPS averaged across cell countries. If pooling reduces CRPS by ≥3% (a meaningful threshold), it ships as the L3 default; otherwise the country-separate model ships.

## Tier-T treatment

Tier-T countries (the ~110 not in Tier-V) lack the OOS history for country-separate estimation. **They benefit most from pooling.** The L3 pipeline for Tier-T defaults to fully-pooled or partially-pooled with a strong global prior. Tier-T forecasts are tagged "pooled-from-Tier-V" on the dashboard, with a methodology link.

This is the path by which OPENGEM eventually serves 100+ countries without 100 country-specific models: borrow the Tier-V global signal, apply country-specific loadings if data permits.

## Pitfalls

1. **Country-specific structural breaks** (e.g. China 2015, Argentina 2018) can violate the pooling assumption. The Pesaran CD test catches some but not all.
   *Mitigation*: scenario subsystem (L196) flags structural breaks; pooling diagnostics recomputed within 1 month of a flagged country.

2. **Shrinking toward the wrong global mean** when Tier-V is OECD-biased.
   *Mitigation*: when forecasting an emerging-market country, the pooling prior is weighted toward emerging-market peers (Mexico, Turkey, Brazil) when available, not the OECD aggregate.

3. **Computational cost of MCMC sampling** for the hierarchical model.
   *Mitigation*: VB (variational Bayes) fallback for the L3-ML-RIDGE hierarchy when wall-clock is constrained; documented in methodology.

## What this loop produced

- Decision tree for pooling (Pesaran CD → Hausman → recommendation).
- Pooling strategy per L3 variant.
- Diagnostic test cadence + storage schema.
- Indicator-typical verdicts.
- Bayesian hierarchical PyMC sketch.
- Validation rule (3% CRPS threshold).
- Tier-T treatment via pooled-from-Tier-V.

## What comes next

- **L204** — TVP-VAR specifically does *not* pool well; deserved its own loop.
- **L205** — mixed-frequency models with pooling.

## Related

- [[R14-l3-architecture]] — variant taxonomy.
- [[L189-bma-combiner]] — combiner consumes pooled or separate variants.
- [[L204-tvp-var]] — variant that does not pool.
- [[L205-mixed-frequency-models]] — pooling variant for MF-DFM.
- [[R07-tier-v-roster]] — Tier-V Core vs Extended vs T.
