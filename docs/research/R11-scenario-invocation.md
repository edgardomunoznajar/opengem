# R11 — Scenario Subsystem Invocation Patterns (post-rescope)

| Field | Value |
|---|---|
| Document ID | OG1-RES-011 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Design memo for SSDD-006 post-R03 rescope.** |
| Authority | R03 §5.2/§5.3, master-doc v2.0 §5.6 |

---

## 1. Why this exists

R03's rescope removes L1+L2 from the baseline forecast critical path. They now live as **scenario satellites**: invoked on-demand by the Scenario Subsystem, with L1 in US-only and L2 re-estimated annually. This memo specifies the **invocation patterns** for the Scenario Subsystem — how L1, L2, and L3 are orchestrated when a scenario request arrives.

## 2. The scenario request lifecycle

```
1.  POST /v1/scenario  {shock_spec}
        │
        ▼
2.  Scenario Parser
    - Validates JSON shock structure
    - Resolves origin country, target variables, magnitude, horizon
        │
        ▼
3.  Identification Selector
    - Decides which identification strategy applies
    - Routes to one of three invocation paths
        │
        ├──▶  Path A: L2-only (default, all countries)
        ├──▶  Path B: L1(US) + L2 (US-origin shocks with structural interpretation needed)
        └──▶  Path C: L3-conditional (high-frequency, exogenous-shock-as-input)
        │
        ▼
4.  Propagator
    - Executes the chosen path
        │
        ▼
5.  L3 Conditional Update
    - For each country, takes the L2 spillover IRF and applies it as exogenous input to L3
    - Produces counterfactual density forecast per country×variable×horizon
        │
        ▼
6.  Fan-Chart Builder
    - Quantile rendering, PNG + JSON
        │
        ▼
7.  Cache Writer + Response
```

## 3. The three invocation paths

### 3.1 Path A — L2-only (default)

**Used when**: shock origin is non-US, identification is conventional (Cholesky / sign restrictions), and the user does not request structural interpretation.

**Steps**:
1. Retrieve cached annual L2 BGVAR posterior (from `posteriors/bgvar_YYYY.parquet`).
2. Apply shock as a variable-level innovation per the identification.
3. Compute IRF horizon-by-horizon for all Tier-V countries.
4. Pass IRF deltas to step 5 (L3 conditional update).

**Wall-clock budget**: ≤ 30s per scenario (uses cached posterior; no re-estimation).

**Example**: "+100bp Chinese policy rate shock" — L2 spillover IRFs to all countries via trade-weight matrix.

### 3.2 Path B — L1(US) + L2

**Used when**: shock origin is US AND structural-shock interpretation is required (e.g., "monetary policy shock decomposed via Taylor-rule identification" rather than "fund-rate-instrument shock with Cholesky ordering").

**Steps**:
1. Retrieve L1 US core posterior.
2. Identify the structural shock via L1 (e.g., orthogonalize via Taylor-rule restrictions).
3. Map the L1 structural shock to L2's US block via known mapping.
4. Apply via L2 spillover IRFs as in Path A.
5. Pass IRF deltas to L3 conditional update.

**Wall-clock budget**: ≤ 60s per scenario (L1 re-evaluation adds time).

**Example**: "Monetary policy shock of +100bp surprise, identified via Taylor-rule residual" — Path B with L1-derived identification.

### 3.3 Path C — L3-conditional

**Used when**: shock is an exogenous covariate that L3 already ingests (e.g., oil price shock, supply chain stress shock, GPR shock), and no structural identification is needed.

**Steps**:
1. Skip L1/L2.
2. Construct a counterfactual covariate path (e.g., oil price = baseline + shock path).
3. Re-run L3 forecast with the modified covariate path.
4. Produce density forecast deltas.

**Wall-clock budget**: ≤ 15s per scenario (no L1/L2 work).

**Example**: "+50% oil price for 4 quarters" — pure L3-conditional propagation.

## 4. Decision rules for path selection

```
def select_path(shock_spec):
    if shock_spec.is_covariate_only():
        return Path.C  # L3-conditional
    if shock_spec.origin_country == "US" and shock_spec.needs_structural_id:
        return Path.B  # L1(US) + L2
    return Path.A      # L2 default
```

A `shock_spec` declares both its targets and whether structural interpretation is requested. The default for most uses is Path A.

## 5. Caching strategy

Scenarios are cached by `(shock_spec_hash, posterior_hashes, code_sha)`:

| Cache layer | Key | TTL |
|---|---|---|
| Hot cache | Full `(shock, posteriors, code)` triplet | 30 days |
| L2 IRF cache | `(L2_posterior_hash, shock_spec)` independent of L3 | 1 year (until L2 re-estimated) |
| L3 conditional update cache | `(L2_irf_id, L3_posterior_hash, country)` | 30 days |

Cache invalidation: automatic on L2 annual re-estimation; automatic on L3 monthly recalibration; manual on `code_sha` change.

## 6. Shock specification grammar

```json
{
  "shock_id": "user-friendly-name",
  "type": "level_shock | path_shock | structural_shock",
  "origin": {
    "country": "US",
    "variable": "policy_rate",
    "magnitude": 1.0,
    "unit": "pp"
  },
  "horizon": {
    "start_period": "2026Q3",
    "length_quarters": 8
  },
  "identification": "cholesky | sign_restriction | structural",
  "needs_structural_id": false,
  "targets": {
    "countries": ["all_tier_v"],
    "variables": ["gdp", "cpi"],
    "horizons": [1, 4, 8]
  }
}
```

## 7. Failure modes

| Mode | Behavior |
|---|---|
| L2 posterior stale (>1y) | Warn in response; trigger out-of-band L2 re-est. job |
| L1 posterior stale (US only path) | Same; warn |
| Shock spec invalid | Return 400 with structured error |
| Scenario propagation produces NaN | Refuse to emit; M-08 degraded mode |
| Cache miss + propagation timeout | Best-effort partial response with completed countries only |

## 8. V&V for scenarios

Scenario outputs are harder to V&V than baseline forecasts because there's no "what actually happened" counterfactual. We use **stress-test plausibility checks** instead:

1. **Sign and magnitude sanity**: a +100bp Fed rate shock should reduce US GDP by 4Q at some magnitude in the ballpark of published estimates (e.g., -0.5 to -1.5pp at 4Q). Out-of-range warns model card.
2. **Cross-country spillover sanity**: monetary shocks propagate with country-specific magnitudes consistent with Komárek / Coenen / Galí style published IRFs.
3. **Idempotency**: same `shock_spec` produces same response within float tolerance (provenance check).
4. **Sensitivity**: small changes in shock magnitude produce smooth response surface (no discontinuities).

## 9. Open probes

1. **L1 / L2 mapping for Path B** — concrete linear algebra of how an L1-identified monetary shock plugs into L2's US block. Defer to SSDD-006 detail.
2. **Anvil-style scenario library**: pre-canned shocks (recession-triggering, oil-shock, geopolitical-event) maintained as a fixture set. Cross-link to oblique-anvil if useful.
3. **Streaming scenarios**: long-running multi-thousand-draw scenarios. Defer to v0.4+.

## 10. Bottom line

Three paths, clean decision rule, all caches scoped, scenario response within 60s on the canonical workload. The Scenario Subsystem becomes the **principal use case for L1 and L2** under the rev C architecture, and is the place where the *narrative* and *spillover* jobs OPENGEM still claims to do live.

---

*End of R11 Rev A.*
