# Runbook — taking the v0 prototype to a live demo

**Audience**: future Edgardo (or a collaborator). Goal: get from the research-300/prototypes scaffold to a public URL serving real OPENGEM data, in one focused work session.

**Estimated time**: 4-6 hours, end-to-end.

---

## Phase 1 — local install + run (45 minutes)

```bash
# Take the scaffold out of research-300/ and into a real package
cp -R research-300/prototypes/dashboard-next packages/opengem-dashboard
cp -R research-300/prototypes/api-stub packages/opengem-api-stub

cd packages/opengem-dashboard

# Install deps (Next.js 15 + Tailwind v4 + shadcn)
npm install

# Start the dashboard against bundled fixtures
npm run dev
# → http://localhost:3000 — renders with the fixture data
```

In a second shell:

```bash
cd packages/opengem-api-stub
pip install fastapi uvicorn pydantic
uvicorn main:app --reload --port 8001
# → http://localhost:8001/docs — Swagger UI
```

In the dashboard, copy `.env.example` to `.env.local`:

```
OPENGEM_API_URL=http://localhost:8001
```

Refresh `http://localhost:3000` — should now load from the FastAPI service.

**Done when**: home page renders with situation tiles, scenarios, forecast strip, and country grid. Command palette opens with ⌘K. /accountability renders the miss ledger.

## Phase 2 — wire to opengem-vintage (90 minutes)

Replace `_load()` in `packages/opengem-api-stub/main.py` with calls into the real opengem-vintage store:

```python
from opengem_vintage import VintageStore
from opengem_vintage.queries import latest_situation, latest_forecasts, scenario_invocations

store = VintageStore.from_settings()  # reads opengem config

@app.get("/v1/situation")
def situation() -> list[dict]:
    return [s.model_dump() for s in latest_situation(store)]

@app.get("/v1/scenarios")
def scenarios() -> list[dict]:
    return [s.model_dump() for s in scenario_invocations(store, threshold=0.05)]

@app.get("/v1/forecasts")
def forecasts(country=None, indicator=None, horizon=None):
    return [f.model_dump() for f in latest_forecasts(store, country=country, indicator=indicator, horizon=horizon)]
```

Restart uvicorn. Refresh dashboard. Should now show real data.

**Done when**: at least one real OPENGEM forecast renders end-to-end in the browser.

## Phase 3 — fit a real L3 model on US (90 minutes)

Create `packages/opengem-l3-dfm/`:

```python
# src/opengem_l3_dfm/fit.py
import statsmodels.api as sm
from opengem_vintage import VintageStore, load_vintage_panel
from opengem_types import Forecast, Bands

def fit_us_gdp(store: VintageStore, vintage_date: str) -> Forecast:
    panel = load_vintage_panel(store, country="USA", vintage=vintage_date)
    model = sm.tsa.statespace.DynamicFactorMQ(
        panel,
        factors=2,
        factor_orders=1,
    )
    res = model.fit(disp=False)
    f = res.get_forecast(steps=4)
    p10, p50, p90 = f.predicted_mean - 1.28 * f.var_pred_mean ** 0.5, f.predicted_mean, f.predicted_mean + 1.28 * f.var_pred_mean ** 0.5
    return Forecast(
        vintage_id=vintage_date,
        model_id="opengem-l3-dfm-v0.1-us",
        country="USA", indicator="gdp_yoy", horizon="4Q",
        point=float(p50.iloc[-1]),
        bands=Bands(p10=float(p10.iloc[-1]), p50=float(p50.iloc[-1]), p90=float(p90.iloc[-1])),
        ...
    )
```

Wire it as a Dagster asset (already in `opengem/deploy/dagster/`):

```python
@asset
def us_gdp_4q_forecast(opengem_vintage_store) -> Forecast:
    return fit_us_gdp(opengem_vintage_store, today_vintage())
```

**Done when**: `dagster run --select us_gdp_4q_forecast` produces a `Forecast` object that lands in the vintage store. Refresh dashboard → US country page shows the real number.

## Phase 4 — deploy (60 minutes)

### Dashboard → Cloudflare Pages

```bash
cd packages/opengem-dashboard
# Connect to GitHub repo if not already
npx wrangler pages project create opengem-dashboard
git push  # triggers auto-deploy
```

Set env vars in Cloudflare dashboard:
- `OPENGEM_API_URL=https://api.opengem.org`

### API → Fly.io

```bash
cd packages/opengem-api-stub
fly launch --name opengem-api --region iad
fly secrets set OPENGEM_VINTAGE_URL=...
fly deploy
```

### Datasette → Fly.io

```bash
# Vintage snapshot to SQLite
opengem-vintage export --vintage today --to opengem-snapshot.db

# Deploy Datasette
fly launch --image datasetteproject/datasette --name opengem-data
fly volumes create snapshots --size 10
# Mount /snapshots, copy opengem-snapshot.db
fly deploy
```

**Done when**:
- `https://opengem.org` shows the live dashboard
- `https://api.opengem.org/v1/health` returns OK
- `https://data.opengem.org` serves the public ledger

## Phase 5 — open the accountability page (30 minutes)

Find one historical forecast that missed. Write the post-mortem in markdown:

```bash
mkdir -p packages/opengem-dashboard/content/postmortem
cat > packages/opengem-dashboard/content/postmortem/usa-gdp-2025q2.md << 'EOF'
# USA GDP 2025-Q2 — forecast missed

**Vintage**: 2024-Q4-1500Z
**Forecast**: 1.4% (band 0.8–2.0%)
**Actual**: 2.6%
**Miss**: +1.2pp (outside 80% band)

## Why we missed
[Your post-mortem here — be honest about what the model didn't see and what should change next vintage]

## What changed
[Specific code or methodology delta in next vintage]
EOF

# Wire as MDX route
# Add to /postmortem/[slug]/page.tsx in dashboard
```

**Done when**: `https://opengem.org/postmortem/usa-gdp-2025q2` renders the post-mortem.
The accountability page should link to it from the miss-log table.

## Phase 6 — MCP server (90 minutes)

```bash
mkdir packages/opengem-mcp && cd packages/opengem-mcp
# pyproject.toml depending on mcp, opengem-vintage, opengem-types
# src/opengem_mcp/server.py — implement the 8 tools per L108 + L250
# Publish to PyPI: `poetry publish`
# Publish npm wrapper to npmjs: @opengem/mcp-server
```

Add to your own Claude Desktop config:

```json
{
  "mcpServers": {
    "opengem": {
      "command": "npx",
      "args": ["-y", "@opengem/mcp-server"]
    }
  }
}
```

Restart Claude. Ask "what's OPENGEM's recession probability for the US?" — should return a live, vintage-stamped answer.

**Done when**: a fresh Claude conversation can ground itself in OPENGEM data via MCP.

## Phase 7 — measurement (15 minutes)

Mount Plausible (self-hosted Fly.io). Add the snippet to dashboard layout.

Open `/about/telemetry` — see your own dashboard usage in real-time. *Your analytics are public.*

**Done when**: Plausible is recording page views; the public telemetry page shows the count.

---

## Total time: ~6 hours

After this runbook, OPENGEM has:
- A live, open, vintage-stamped world dashboard
- A real L3 forecast (US GDP) generated by `statsmodels`
- A live MCP server for LLM grounding
- A live accountability ledger with at least one real post-mortem
- A live Datasette ledger at data.opengem.org
- Public analytics

This is the "v0.5" milestone — foundation + minimum-viable product in the same calendar quarter.

## Common pitfalls

- **Don't skip the FastAPI step.** The dashboard's fallback fixtures hide bugs. Make the API the source of truth.
- **Don't try to do all 22 Tier-V countries on day 1.** US alone. Expand once the loop is proven.
- **Don't write a custom DFM.** Use statsmodels. The build-vs-buy decision is locked.
- **Don't deploy the API to Cloudflare Workers.** Python on Fly.io is the path; Cloudflare Workers Python is still rough.
- **Don't pre-monetize.** Free tier first; Pro tier when there's actual MCP throughput demand.
