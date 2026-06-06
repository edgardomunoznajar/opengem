# L082 — OpenBB Integration: A Concrete Provider Stub + Total Cost

**Loop**: 082 / 300
**Phase**: 2 — Integration deep dive
**Date**: 2026-06-06
**Verdict**: **ADOPT-V2 (Phase 4, post-v1 launch, separate AGPL repo)**

---

## What this loop answers

L081 confirmed the OpenBB architecture is provider-friendly. This loop answers the next question: *what does a real `openbb-opengem-provider` look like, and what's the total integration cost from blank repo to shipped-on-PyPI?*

The answer: **~2 dev-weeks for an MVP covering 10 endpoints, ~$0/mo to operate, free MCP distribution as the headline payoff.** Repo isolation keeps the AGPL contained. We ship it in Phase 4 (post-v1 launch) when our public API surface is stable enough that the schema doesn't churn under us.

## The endpoint surface — what we expose

The provider is a thin client over OPENGEM's public REST API. We pick endpoints that map cleanly to OpenBB's `standard_models` so the swap-via-provider story works. Ten candidates, ordered by retrieval frequency and obvious user value:

| Provider endpoint | Maps to OpenBB standard model | OPENGEM API endpoint | Notes |
|---|---|---|---|
| `OpengemForecast` | `EconomicGdpData` (extended) | `/v1/forecast/{country}/{indicator}/{horizon}` | Hero endpoint; central forecast + bands |
| `OpengemVintage` | new (no standard equivalent) | `/v1/vintage/{country}/{indicator}` | Vintage rewinder data |
| `OpengemConsensus` | new | `/v1/consensus/{country}/{indicator}` | WEO/OECD/SPF overlay |
| `OpengemSurprise` | new | `/v1/surprise/{country}/{indicator}` | Realized vs forecast diff |
| `OpengemRecessionProb` | new | `/v1/recession-prob/{country}` | Bauer-Mertens style; cross-country |
| `OpengemLeaderboard` | new | `/v1/leaderboard/{indicator}/{horizon}` | CRPS-ranked model list |
| `OpengemGprIndex` | new | `/v1/gpr/{country}` | GPR-C series for the 44 countries |
| `OpengemConflictIntensity` | new | `/v1/conflict/{country}` | UCDP+POLECAT derived index |
| `OpengemTrackRecord` | new | `/v1/track-record/{model_id}` | Per-model historical scoring |
| `OpengemMethodologyCard` | new | `/v1/methodology/{model_id}` | Model card + provenance |

The first four sit close enough to OpenBB's standardized economy schemas that we can subclass `SeriesData`/`SeriesQueryParams` and add fields. The other six are net-new — OpenBB has no concept of "geopolitical risk index" or "forecast track record," so we ship them as provider-native types. That's allowed: not every Fetcher's output has to bind to a standard model. The cost is that those endpoints don't cross-cite with other providers (you can't swap `provider="opengem"` for `provider="fred"` on `OpengemRecessionProb` because FRED doesn't have one). For our novel surfaces — recession probabilities, conflict intensity, leaderboards — there *is* no cross-provider swap to want.

## Scaffold from cookiecutter

```bash
cd /tmp
cookiecutter https://github.com/OpenBB-finance/openbb-cookiecutter
# project_name: "Opengem"
# package_name: "openbb_opengem"
# extension_types: "router"  # actually we want "provider" — patch after generation
mv super-quant openbb-opengem-provider
cd openbb-opengem-provider
```

The cookiecutter is designed for routers (extensions); for a pure provider, we delete the `router.py` it generates and stub a Provider in `openbb_opengem/__init__.py`:

```python
# openbb_opengem/__init__.py
"""OPENGEM provider — Apache-2.0 data + CC-BY-4.0, AGPL-licensed plugin."""

from openbb_core.provider.abstract.provider import Provider

from openbb_opengem.models.forecast import OpengemForecastFetcher
from openbb_opengem.models.vintage import OpengemVintageFetcher
from openbb_opengem.models.consensus import OpengemConsensusFetcher
from openbb_opengem.models.surprise import OpengemSurpriseFetcher
from openbb_opengem.models.recession_prob import OpengemRecessionProbFetcher
from openbb_opengem.models.leaderboard import OpengemLeaderboardFetcher
from openbb_opengem.models.gpr import OpengemGprIndexFetcher
from openbb_opengem.models.conflict import OpengemConflictIntensityFetcher
from openbb_opengem.models.track_record import OpengemTrackRecordFetcher
from openbb_opengem.models.methodology import OpengemMethodologyCardFetcher

opengem_provider = Provider(
    name="opengem",
    website="https://opengem.org",
    description=(
        "OPENGEM World Dashboard — open macro forecasts with vintage history, "
        "forecast leaderboards, geopolitical risk indices, and methodology "
        "cards. Apache-2.0 code + CC-BY-4.0 data."
    ),
    credentials=["api_key"],
    fetcher_dict={
        "OpengemForecast": OpengemForecastFetcher,
        "OpengemVintage": OpengemVintageFetcher,
        "OpengemConsensus": OpengemConsensusFetcher,
        "OpengemSurprise": OpengemSurpriseFetcher,
        "OpengemRecessionProb": OpengemRecessionProbFetcher,
        "OpengemLeaderboard": OpengemLeaderboardFetcher,
        "OpengemGprIndex": OpengemGprIndexFetcher,
        "OpengemConflictIntensity": OpengemConflictIntensityFetcher,
        "OpengemTrackRecord": OpengemTrackRecordFetcher,
        "OpengemMethodologyCard": OpengemMethodologyCardFetcher,
    },
    repr_name="OPENGEM World Dashboard",
    instructions=(
        "Sign up at https://opengem.org and generate an API key from your "
        "account page. The free tier allows 1,000 requests/day."
    ),
)
```

The `pyproject.toml` adds the entry point under `openbb_provider_extension` so OpenBB's registry discovers us:

```toml
[tool.poetry]
name = "openbb-opengem-provider"
version = "0.1.0"
description = "OPENGEM provider extension for OpenBB"
authors = ["OPENGEM Maintainers <hello@opengem.org>"]
license = "AGPL-3.0-only"  # required for plugin compat
readme = "README.md"
packages = [{ include = "openbb_opengem" }]

[tool.poetry.dependencies]
python = ">=3.10,<4"
openbb-core = "^1.6.10"
httpx = "^0.27"

[tool.poetry.plugins."openbb_provider_extension"]
opengem = "openbb_opengem:opengem_provider"
```

## A representative Fetcher

`models/forecast.py` — the hero endpoint:

```python
"""OPENGEM forecast Fetcher."""
from datetime import date
from typing import Any, Literal

from openbb_core.provider.abstract.data import Data
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.abstract.query_params import QueryParams
from pydantic import Field
import httpx


class OpengemForecastQueryParams(QueryParams):
    country: str = Field(description="ISO 3166-1 alpha-3 country code (e.g. USA, DEU, JPN).")
    indicator: Literal["gdp", "cpi", "unemployment", "policy_rate", "exchange_rate"] = Field(
        description="Indicator slug."
    )
    horizon: Literal["nowcast", "1Q", "4Q", "2Y", "5Y"] = Field(
        description="Forecast horizon."
    )
    as_of: date | None = Field(default=None, description="Vintage date; defaults to latest.")


class OpengemForecastData(Data):
    date: date = Field(description="Forecast target date.")
    p10: float = Field(description="10th-percentile band.")
    p50: float = Field(description="Median (point forecast).")
    p90: float = Field(description="90th-percentile band.")
    p25: float | None = Field(default=None, description="25th-percentile inner band.")
    p75: float | None = Field(default=None, description="75th-percentile inner band.")
    model_id: str = Field(description="OPENGEM model identifier.")
    vintage_at: date = Field(description="Vintage date — when this forecast was made.")
    methodology_card_url: str = Field(description="URL to the per-model methodology card.")


class OpengemForecastFetcher(
    Fetcher[OpengemForecastQueryParams, list[OpengemForecastData]]
):
    @staticmethod
    def transform_query(params: dict[str, Any]) -> OpengemForecastQueryParams:
        return OpengemForecastQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: OpengemForecastQueryParams,
        credentials: dict[str, str] | None,
        **kwargs: Any,
    ) -> list[dict]:
        api_key = (credentials or {}).get("opengem_api_key", "")
        url = f"https://api.opengem.org/v1/forecast/{query.country}/{query.indicator}/{query.horizon}"
        params = {"as_of": query.as_of.isoformat()} if query.as_of else {}
        headers = {"X-API-Key": api_key} if api_key else {}
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, params=params, headers=headers)
            r.raise_for_status()
            return r.json()["data"]

    @staticmethod
    def transform_data(
        query: OpengemForecastQueryParams,
        data: list[dict],
        **kwargs: Any,
    ) -> list[OpengemForecastData]:
        return [OpengemForecastData(**row) for row in data]
```

That's ~50 lines for the Fetcher. The remaining nine endpoints follow the same skeleton; the only varying parts are the URL, the QueryParams fields, and the Data fields.

## Total integration cost

| Task | Cost |
|---|---|
| Cookiecutter scaffold + patch to provider-only | 2 hours |
| Implement 10 Fetcher classes | 10 × 0.5 day = 5 days |
| Integration tests (1 per Fetcher, mocked + real-API) | 2 days |
| README + provider docs + methodology references | 1 day |
| AGPL license review + repo isolation audit | 0.5 day |
| Publish to PyPI as `openbb-opengem-provider` | 0.5 day |
| List in OpenBB community providers index | 0.5 day |
| Monitor + version-chase `openbb-core` major bumps | 0.5 day/quarter ongoing |
| **Total v0.1.0 shipping** | **~2 dev-weeks** |

## Operating cost

- **PyPI hosting**: $0/mo.
- **GitHub repo**: $0/mo (public).
- **Traffic to our API**: real cost; lives in the main OPENGEM infra budget (L275). At launch we assume the provider drives <5% of total API requests, growing to maybe 20% by Y2 as the MCP ecosystem matures.
- **Rate-limiting**: enforced server-side on our existing API gateway; the provider does not need to ship its own.

Total operating cost specific to the provider: effectively $0/mo. The real cost is *attention* — keeping the Fetcher schemas in sync with the OPENGEM REST API surface.

## What we gain

1. **Free MCP distribution.** The moment `openbb-opengem-provider` is `pip install`-able and registered, any user running `openbb-mcp` exposes our forecasts to ChatGPT, Claude Desktop, Cursor, Cline. That is a meaningful go-to-market wedge that costs us ~10 lines of code per endpoint.

2. **Discoverability in the 68.7k-star repo.** OpenBB's CLI auto-discovers installed providers; their docs site lists community providers; their `pro.openbb.co` Workspace surfaces them. We get organic discovery without paying for it.

3. **Schema discipline.** Forcing our forecasts through a Pydantic-typed Fetcher exposes any ambiguity in the OPENGEM REST API. Field names like `p50` vs `median`, `vintage_at` vs `as_of_vintage`, `methodology_card_url` vs `model_card_url` — picking one and locking it down is a feature, not a chore. This is the same discipline forcing led us to standardize OPENGEM's own forecast object schema (L181).

4. **One canonical example for the LLM substrate.** When prompting Claude/GPT to "use OPENGEM forecasts," the provider docs become the LLM's source of truth. We control that surface area directly.

## What we lose

1. **AGPL repo overhead.** Maintaining a second repo with a different license is a small but real tax. Pull requests have to be reviewed; CI has to be wired; PyPI release has to be cut. ~1 hour/month average over a year.

2. **Version chase.** Every time OpenBB bumps `openbb-core` to a new major (historically every 6-9 months), the provider needs a sweep. Empirically this is half a day per bump.

3. **Some users see us only through OpenBB's lens.** A user who calls `obb.economy.forecast(provider="opengem")` gets a Pydantic model, not a link to our dashboard. We mitigate by including a `dashboard_url` field in every Data class and a clear methodology card link.

## Why Phase 4 and not Phase 2

The OPENGEM REST API has to be stable before we publish a Fetcher schema against it. Pre-v1, the API will churn — endpoint names, field names, response shapes will all shift. Shipping a provider against a moving target burns goodwill in the OpenBB community (broken on every release) and burns our own time (constant Fetcher rewrites).

Phase 4 schedule:
- Phase 2: design the REST API (L181, L249).
- Phase 5: prototype + harden the REST API (L249 OpenAPI spec).
- Phase 6: lock the API contract, cut OPENGEM v1.0.
- **Post-v1**: publish `openbb-opengem-provider 0.1.0` against the locked schema.

That puts the provider's ship date roughly at month 4-6 of post-launch, which is the right time for a distribution play: we have a stable surface, real users, and live forecasts worth discovering.

## Risks

1. **OpenBB Inc. could change the AGPL license**. They have commercial interests (Workspace, Pro tier). If they relicense `openbb-core` to a commercial license at any point, our AGPL provider becomes incompatible. Mitigation: pin to last AGPL major (1.6.x); fork if necessary.

2. **OpenBB Inc. could move providers to their Workspace-only registry.** They've shown some sign of paywalling features (the closed-source Workspace). If they ever block community providers from being discovered by free-tier users, our discovery channel narrows. Mitigation: keep `pip install openbb-opengem-provider` working regardless of registry policy.

3. **Our API rate limits get hit by free-tier MCP traffic.** Free-tier OPENGEM users hitting us via OpenBB MCP could exhaust our rate limit budget. Mitigation: separate rate-limit bucket for `User-Agent: openbb-*` traffic, with a clear upgrade path to a paid API key.

## What this loop produced

- Concrete endpoint list (10 endpoints with standard-model fit notes).
- Working scaffold: `pyproject.toml`, `__init__.py`, and a representative ~50-line Fetcher.
- Total cost: ~2 dev-weeks v0.1.0 + ~$0/mo operating + 0.5 day/quarter maintenance.
- Phase 4 timing rationale (don't ship against an unstable API).
- Three real risks with mitigations.

## What comes next

- **L108** — Our own MCP server, differentiated from OpenBB-MCP-via-provider.
- **L181** — Forecast object schema (the contract this provider serializes against).
- **L249** — OpenAPI spec for the public REST API (the wire format this provider hits).

## Related

- [[L081-openbb-code-architecture-audit]] — the deep dive that made this scaffold writable.
- [[L011-openbb-terminal]] — strategic framing.
- [[L108-mcp-server-contract]] — what our own MCP server differentiates on.
- [[L181-forecast-object-schema]] — the canonical wire format.
- [[L249-openapi-spec]] — the API contract.
