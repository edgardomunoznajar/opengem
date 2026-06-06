# L157 — Notebook Export

**Loop**: 157 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

"Open this view in Jupyter" is the single most defensive feature against vendor lock-in critique. We ship a one-click `.ipynb` that pulls live data from the OPENGEM API and reproduces the dashboard view in code.

The notebook export is also a *teaching tool*: it shows analysts exactly how to use the API.

## The contract

From any view with API-backed data:
- Toolbar button "Open in notebook" (Lucide `code` icon)
- Command palette: "Open in notebook" or "jupyter"
- Keyboard shortcut: none (avoid muddying the global map)

Emits a `.ipynb` file containing:

1. A title cell with the view URL and timestamp
2. Setup cells (imports, API client, auth)
3. Data-pull cells (querying the exact endpoints powering this view)
4. Reconstruction cells (matplotlib/plotly reproducing the chart)
5. A "go further" appendix with documented next steps

## The endpoint

```
GET /export/notebook?path=<encoded-view-url>&style=<plotly|matplotlib|altair>
```

Returns:
- `Content-Type: application/x-ipynb+json`
- `Content-Disposition: attachment; filename="opengem-<view-id>-<vintage>.ipynb"`

## Notebook structure

```
   ┌── Markdown ─────────────────────────────────┐
   │ # USA CPI YoY — OPENGEM notebook export      │
   │                                              │
   │ Generated from:                              │
   │ https://opengem.app/indicator/cpi-yoy?countries=usa
   │ Vintage: 2026-06-04                          │
   │ Exported: 2026-06-06 14:32 UTC               │
   │                                              │
   │ Run this notebook to reproduce the view in   │
   │ Python. No OPENGEM account required to run.  │
   └──────────────────────────────────────────────┘

   ┌── Code: setup ──────────────────────────────┐
   │ %pip install opengem-py pandas matplotlib    │
   │                                              │
   │ import opengem                                │
   │ import pandas as pd                            │
   │ import matplotlib.pyplot as plt              │
   │                                              │
   │ og = opengem.Client(api_key=None)            │
   └──────────────────────────────────────────────┘

   ┌── Markdown ─────────────────────────────────┐
   │ ## Pull the indicator                        │
   │ This calls the same endpoint the dashboard    │
   │ uses to render the chart.                    │
   └──────────────────────────────────────────────┘

   ┌── Code: fetch ──────────────────────────────┐
   │ data = og.indicator(                         │
   │   id="cpi-yoy",                              │
   │   countries=["usa"],                          │
   │   vintage="2026-06-04",                       │
   │   range=("2010-01-01", "2026-06-01"),         │
   │ )                                            │
   │                                              │
   │ df = data.to_pandas()                         │
   │ df.head()                                    │
   └──────────────────────────────────────────────┘

   ┌── Code: plot ───────────────────────────────┐
   │ fig, ax = plt.subplots(figsize=(10, 4))      │
   │ ax.plot(df.index, df["usa"], label="USA CPI") │
   │ ax.set_title("USA CPI YoY")                   │
   │ ax.set_ylabel("Percent change, YoY")           │
   │ ax.grid(alpha=0.3)                            │
   │ ax.legend()                                  │
   │ plt.show()                                   │
   └──────────────────────────────────────────────┘

   ┌── Markdown: appendix ───────────────────────┐
   │ ## Going further                              │
   │                                              │
   │ - Try other countries: `countries=["deu", "fra"]` │
   │ - Pull bands: `og.forecast(...).bands()`     │
   │ - Compare to consensus: `data.with_consensus()` │
   │                                              │
   │ See the full API reference at                 │
   │ https://opengem.app/api                       │
   └──────────────────────────────────────────────┘
```

## Per page-type recipes

The notebook content varies by source view:

### Country page

- Pull 6 default indicators (GDP, CPI, Unemp, Policy rate, FX, Reserves)
- Plot as small-multiples
- Appendix: "swap countries, swap indicators"

### Indicator page

- Pull the indicator across the selected countries
- Plot as a multi-line chart
- Appendix: "add forecast bands, add YoY transform"

### Forecast page

- Pull the forecast with bands
- Plot the observed history + fan
- Overlay consensus (WEO/OECD)
- Appendix: "score this forecast against actuals using `og.score()`"

### Scenario page

- Pull the scenario tree
- Plot the branch outcomes
- Render the probability bar
- Appendix: "compute weighted-average projection"

### Compare page

- Pull both objects
- Render side-by-side and overlay
- Appendix: "compute correlation and rolling beta"

## The Python client

Notebook ships against `opengem-py` (the official Python client). Pinned to a recent version. The client:

- Wraps the REST API with typed methods
- Caches vintage-pinned responses locally (`.opengem-cache/`)
- Authentication-free for public endpoints (rate-limited)
- API key for paid tier (`og.Client(api_key=os.environ["OPENGEM_KEY"])`)

The client is published to PyPI under Apache-2.0. Code lives in `opengem/clients/python` in the monorepo.

## Style options

The `style` query param:
- `matplotlib` (default — universal, no extra deps beyond matplotlib)
- `plotly` (interactive, requires plotly)
- `altair` (declarative grammar, for the Observable-fluent crowd)

Each style emits the same data cells; only the plot cells differ.

## R notebook?

Deferred. Python notebook is the V1 commitment. R support (via an `opengem-r` client and `.Rmd` export) is a paid-tier feature for V2 — academic outreach (L292) will surface demand.

## "Open in Jupyter" online

Where possible we link to a one-click hosted notebook:

- "Open in Colab" button → uploads to Colab pre-loaded
- "Open in Binder" button → spins up a public Binder
- "Open in DeepNote" / "Hex" — future, after demand signal

The Colab path uses `https://colab.research.google.com/github/...` with the notebook hosted as a gist on the OPENGEM org. We generate the gist on demand and redirect.

The Binder path uses `mybinder.org/v2/gh/...`. Slower cold-start; useful for "I don't have Python installed."

## R/Stata/MATLAB integration (deferred)

`og` Python client + `notebook` export covers ~90% of the prosumer analyst world. R is the next add. Stata and MATLAB are paid-tier API-only — they can hit `/api/v1/...` directly without a client library, with curl examples in the docs.

## What the notebook MUST NOT do

- Embed credentials or API keys
- Require login to run (public endpoints only by default)
- Use Pandas-only patterns that exclude beginners (provide both `pandas` and a plain Python alternative for the simplest examples)
- Take more than 30 seconds to run end-to-end

The "30 seconds" rule means we don't pull 50 years of daily data by default. Range defaults are sensible.

## Notebook metadata

Each notebook ships with:
- `metadata.kernelspec`: Python 3.11
- `metadata.opengem.export_date`
- `metadata.opengem.view_url`
- `metadata.opengem.vintage`
- `metadata.opengem.client_version`

Versioning lets us evolve the export format. Old notebooks remain runnable because the client is backward-compatible.

## Licensing on emitted notebooks

Notebook content is CC-BY-4.0 (attribution to OPENGEM). Code in the notebook is Apache-2.0. Users can modify, redistribute, publish. We ask for attribution but don't enforce.

## Implementation

- Endpoint: Next.js route handler `/api/export/notebook`
- Notebook generation: `nbformat` Python library (server-side, via a small Python sidecar service called from Next via HTTP — or rewrite in TS with a JSON-only nbformat builder)
- Caching: per (canonical-URL, vintage, style) tuple — TTL = next vintage
- Streaming: emit the notebook progressively for large views

Per L154, the notebook URL is itself a deep link, and the `<link rel="alternate" type="application/x-ipynb+json">` is set in `<head>` on every API-backed page. So a power user can `curl` a page URL with the right Accept header to get the notebook directly.

## MCP exposure

The MCP server exposes a tool `notebook.export(view_url)` that returns the notebook JSON. So an LLM agent asked "give me a Python notebook reproducing this OPENGEM view" can call the tool directly.

## Telemetry

- Count notebook exports per page type
- Count Colab vs Binder vs direct download
- Count subsequent API calls from the python client (via UA string)

These signal "real adoption beyond clicking around the dashboard."
