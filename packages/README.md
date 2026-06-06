# OPENGEM Packages

Each subdirectory is an **independently publishable** Python package. Layout convention:

```
packages/<name>/
├── pyproject.toml       # standalone — could be uploaded to PyPI as-is
├── README.md            # explains the package, its API, and how to use standalone
├── src/<module>/        # Python source (module name matches PyPI distribution)
│   └── __init__.py
└── tests/
    └── test_*.py
```

## Architectural rules

1. **No cross-package imports** except via published interfaces.
   - Inter-package dependencies go through `dependencies = [...]` in `pyproject.toml`.
   - In dev: `uv` workspace resolves them to local paths.
   - In CI: workspace builds and tests each package in isolation.
2. **Stable public interfaces** are exposed only via `<module>/__init__.py`.
   - Anything starting with `_` is private; importing from internals across packages is forbidden by lint.
3. **Each package owns its dependencies.**
   - Don't pull a heavy dep into a leaf package "just because the workspace has it."
4. **Each package has its own README.** It must read coherently for someone arriving via PyPI, not via this monorepo.
5. **Each package has its own version.** No coupled bumps unless a contract changes.
6. **Tests run in isolation.** `pytest packages/<name>/tests/` must pass without requiring other packages to be importable.

## Package roster (initial)

### Foundation
- `opengem-types` — canonical dataclasses (Observation, Vintage, Forecast, ScenarioSpec)
- `opengem-vintage` — vintage storage primitives (Timescale + hashing)
- `opengem-data-base` — adapter abstract class + HTTP retry + schema-gate

### Data adapters (one per source)
- `opengem-data-bea` — BEA NIPA
- `opengem-data-bls` — BLS CPI / employment
- `opengem-data-frb` — FRB Board H.15 / G.17 / H.6
- `opengem-data-treasury` — Treasury FiscalData
- `opengem-data-census` — Census M3 / MRTS
- `opengem-data-ordra` — OECD ORDRA (vintage workhorse)
- `opengem-data-ecb` — ECB SDW
- `opengem-data-bis` — BIS Data Portal (rates, banking)
- `opengem-data-imf` — IMF SDMX
- `opengem-data-wb` — World Bank WDI
- `opengem-data-comtrade` — UN Comtrade
- `opengem-data-gscpi` — NY Fed GSCPI
- `opengem-data-portwatch` — IMF PortWatch
- `opengem-data-gpr` — Caldara-Iacoviello GPR
- `opengem-data-gdelt` — GDELT 2.0

### Models
- `opengem-l3` — DFM + ML residual + large BVAR + BMA combiner
- `opengem-l2-bgvar` — Bayesian GVAR via R subprocess
- `opengem-l1-us-core` — US semi-structural core
- `opengem-combiner` — generic BMA combiner over forecast variants

### Scenarios + situation
- `opengem-scenarios` — scenario grammar + library + invocation
- `opengem-scenario-chains` — multi-step composition
- `opengem-recession-prob` — Bauer-Mertens term-spread
- `opengem-event-detector` — news/event-based scenario triggers
- `opengem-country-dossier` — regional context layer

### Output
- `opengem-narrative` — analyst-grade prose generation (LLM-mediated)
- `opengem-digest` — daily JSON + markdown digest renderer

### Verification
- `opengem-vv` — V&V matrix evaluator + leaderboard
- `opengem-reproducibility` — hash quintuple + replay-and-diff CI

### Services (separate from libraries)
- `opengem-api` — Java/Spring Boot read API (under `packages/opengem-api/`, Maven-based)
- `opengem-mcp` — MCP server (Java module of `opengem-api`)

## Package status legend

In each package README:
- 🌱 — skeleton: directory + pyproject.toml + minimal __init__
- 🧪 — alpha: basic functionality + unit tests
- ✅ — beta: integration-tested, usable for IOC
- 🚀 — published-ready: standalone docs, CI green, ready to lift out
