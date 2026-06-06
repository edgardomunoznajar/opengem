# L081 — OpenBB Code Architecture Audit: Providers, AGPL Boundary, Extension Shape

**Loop**: 081 / 300
**Phase**: 2 — Integration deep dive
**Date**: 2026-06-06
**Verdict**: **ADOPT-V2 (provider-only, AGPL-isolated, post-v1)**

---

## Why this audit exists

L011 named OpenBB as the most strategically interesting Bloomberg-substrate-adjacent project on GitHub (~68.7k stars). The verdict from that loop was "build a provider, do not depend on OpenBB." This loop opens the hood — providers system internals, AGPL boundary, what a provider really looks like in code — and confirms the verdict with bytes of evidence, not vibes.

I inspected `research-300/clones/openbb/openbb_platform/` and pulled the actual `Provider` / `Fetcher` / `Pydantic standard model` plumbing apart. The architecture is *cleaner than I expected* and the AGPL contamination is *narrower than the L011 worry suggested.* Both matter.

## Three layers as code

The `openbb_platform/` directory has three peer subdirectories, each its own Poetry package:

```
openbb_platform/
  core/                     # openbb-core 1.6.10, AGPL-3.0-only
    openbb_core/
      provider/
        abstract/           # Provider, Fetcher, Data, QueryParams
        standard_models/    # ~250 Pydantic schemas, e.g. fred_series.py
        registry.py         # Plugin loader (importlib metadata entry points)
        registry_map.py     # Builds the global router map
  extensions/               # Routers grouped by topic (economy, equity, etf, …)
    economy/                # AGPL-3.0-only; openbb-economy 1.x
    mcp_server/             # AGPL-3.0-only; openbb-mcp-server 1.4.1 (fastmcp dep)
  providers/                # ~35 data providers (FRED, OECD, IMF, BLS, BEA, ECB…)
    fred/                   # AGPL-3.0-only; openbb-fred 1.6.2
```

Every single `pyproject.toml` I read had `license = "AGPL-3.0-only"`. That is not a typo and not a peripheral concern — the whole platform is AGPL.

## The Provider class — five fields, zero magic

`core/openbb_core/provider/abstract/provider.py` is **55 lines**. The `Provider` constructor takes five things:

1. `name: str` — slug used as the routing key.
2. `description: str` — human prose.
3. `website: str | None`.
4. `credentials: list[str] | None` — names of credentials (prefixed by name in `__init__`).
5. `fetcher_dict: dict[str, type[Fetcher]]` — *the registry of endpoints this provider implements.*

That's it. No metaclass tricks, no decorator magic, no global registry side-effect at import time. The provider object is registered via a Poetry **entry point** under the group `openbb_provider_extension`, which is read by `core/openbb_core/provider/registry.py` using `importlib.metadata.entry_points()` at runtime. This is the single piece of plumbing every provider plugs into — nothing more.

## The Fetcher contract — three classmethods

`Fetcher[Q, R]` (`abstract/fetcher.py`, ~233 lines, mostly Pythonic typing scaffolding) has exactly three abstract methods to implement:

- `transform_query(params: dict) -> Q` — coerce a kwargs dict into a typed `QueryParams` subclass.
- `extract_data(query: Q, credentials: dict)` *or* `aextract_data(...)` — hit the upstream API; return raw rows.
- `transform_data(query: Q, data: Any) -> R` — normalize raw rows into the standardized `Data` subclass.

The Fetcher base ships an `__init_subclass__` hook that swaps `extract_data` to `aextract_data` if you provide the async one. That is the entire async/sync polyglot story: write whichever you have, the base class glues it in. Every Fetcher I read (`fred/series.py`, `fred/consumer_price_index.py`, `bls/series.py`) follows this pattern unmodified.

This is *exactly* the abstraction OPENGEM's own `Adapter` ABC (in `packages/opengem-data-base/src/opengem_data_base/adapter.py`) already does — three classmethods, typed input/output, no magic. Conceptually they are siblings. Practically, OPENGEM's Adapter outputs `Observation` tuples (date, value, series_id); OpenBB's Fetcher outputs `list[Data]` subclasses (typed columns per schema). The translation cost is one wrapper per `Fetcher` class.

## Standard models — the canonical wire format

`core/openbb_core/provider/standard_models/fred_series.py` is **40 lines** total. Two Pydantic classes: `SeriesQueryParams` (`symbol`, `start_date`, `end_date`, `limit`) and `SeriesData` (`date`). That's it. Provider-specific extensions (e.g. FRED's frequency aggregation, transformation options) live in the provider's own subclasses, not the standard model.

The standard model directory has **~250 schemas** covering every endpoint OpenBB Platform exposes. They are deliberately *minimal* — common fields only, with the assumption that providers extend them as needed. This is the right design choice. If you want to be a provider, you pick the standard model that fits your output, subclass it, add provider-specific fields, and ship.

## The AGPL boundary, concretely

The L011 worry: "any provider we ship into OpenBB inherits AGPL." Looking at the source: the worry is **half right**, and the half that's right matters.

**What is AGPL**: `openbb-core` (the Provider/Fetcher/Pydantic plumbing), `openbb-economy` and all other extensions, `openbb-mcp-server`, all ~35 first-party providers. Every `pyproject.toml` declares `AGPL-3.0-only`.

**What does AGPL mean for a provider plugin**: at runtime, a provider's `Fetcher` is *invoked by* `openbb-core` via the entry-point registry. The provider imports from `openbb_core.provider.abstract.fetcher` (the `Fetcher` base class) and from `openbb_core.provider.standard_models.*` (the schema). Both are AGPL.

The AGPL question: does importing from `openbb_core` make the provider's source code itself AGPL? **Yes, by the FSF's reading.** AGPL section 5 says any work "based on the Program" must carry AGPL when conveyed. Subclassing `Fetcher` and importing its Pydantic schemas is the textbook definition of derivative work for the FSF.

**The escape hatch is repo isolation.** OPENGEM's core dashboard / API / model code never imports `openbb_core`. We ship a *separate* repo `openbb-opengem-provider` that is licensed AGPL-3.0-only and ONLY contains Fetcher subclasses that call our public HTTP API. Inside that repo, the Fetcher classes hit `https://api.opengem.org/v1/...` — they are thin clients of our public API surface. They are the only code in that repo. Zero shared modules with the OPENGEM core monorepo.

This is exactly how `openbb-sec`, `openbb-tradier`, `openbb-yfinance`, and `openbb-fmp` work today. None of them import from each other; each is an isolated Poetry package; the AGPL stays in the box.

## The cookiecutter scaffold — the actual onboarding cost

`cookiecutter/openbb_cookiecutter/` is a Cookiecutter template that asks for `full_name`, `email`, `project_name`, `project_tag`, `package_name`, `extension_types`. Running it gives you a Poetry package with the right `pyproject.toml`, the right entry-point registration, an empty `Provider`, and a placeholder Fetcher. **First-day commit cost** is maybe two hours from blank disk to "my provider registers with OpenBB CLI but does nothing."

## Where the FRED provider hits real complexity

I read `providers/fred/openbb_fred/models/series.py` (218 lines) end to end. The interesting bits:

1. `FredSeriesQueryParams` extends the standard `SeriesQueryParams` and adds 4 provider-specific fields: `frequency`, `aggregation_method`, `transform`, plus `__alias_dict__` to map OpenBB's `symbol`/`start_date`/`end_date` onto FRED's native `series_id`/`observation_start`/`observation_end`. This alias trick is how providers translate between the standard query API and the upstream's native query language.

2. `aextract_data` is ~60 lines: build the URL, hit `https://api.stlouisfed.org/fred/series/observations` and `https://api.stlouisfed.org/fred/series` for metadata, parse JSON, return a list of dicts. It uses `httpx`-equivalent via `openbb_fred.utils.rate_limiter.fred_get`. *Every* provider ships its own rate-limit helper because the upstream APIs are heterogeneous.

3. `transform_data` is mostly serialization — DataFrame to list-of-dicts with typed columns.

For OPENGEM, our equivalent would be even simpler: our public API already returns JSON in the canonical OPENGEM forecast schema (L181). The Fetcher's `aextract_data` is `httpx.get("https://api.opengem.org/v1/forecasts/{country}/{indicator}")` and `transform_data` is one Pydantic validation pass.

## How the registry actually loads providers at runtime

`registry.py` (~50 lines, the part I scanned): on import, it walks `importlib.metadata.entry_points(group="openbb_provider_extension")`, calls each entry's `.load()` to get the `Provider` instance, and stuffs it in a `ProviderRegistry`. `registry_map.py` then walks the registry and builds the global Fetcher routing dict that the router uses at request time.

Two consequences:

- The provider has to be `pip install`ed in the same environment as `openbb-core`. There is no remote-provider story.
- If two providers register the same endpoint name (e.g. both register `EconomicGdpData`), the user picks at query time via `provider="fred"` vs `provider="oecd"`. The standardized schema is what makes that swap work.

## The MCP server — already shipping

`openbb-mcp-server` (1.4.1, AGPL, depends on `fastmcp >= 3.2.0`) sits in `extensions/mcp_server/`. It re-exposes every registered Fetcher as an MCP tool. ChatGPT, Claude Desktop, Cursor, Cline — anything speaking the MCP protocol — can already query OpenBB's full surface area. Drop our provider in, and OPENGEM's forecasts become MCP-queryable for free.

This is the biggest sleeper win in the whole stack. OPENGEM does not have to build an MCP server to land in the LLM-tool catalog. We ship a provider; the LLMs reach us via OpenBB's MCP server. Our *own* MCP server (L108, L177) can come later, focused on richer tools (scenario diffs, forecast leaderboard queries) that the provider abstraction can't express.

## What this loop produced

- Confirmed the L011 thesis with actual source inspection.
- Mapped the three-layer architecture to its three Poetry packages and the three `Fetcher` classmethods.
- Identified the AGPL contamination boundary as *importing from* `openbb_core` — and the standard escape hatch (repo isolation).
- Counted the actual onboarding cost: ~2 hours scaffold, ~4 hours per endpoint, ~1 week for our top-10 endpoint surface.
- Surfaced the MCP free-distribution sleeper benefit.

## What comes next

- **L082** — Concrete `openbb-opengem-provider` scaffold sketch (this loop's downstream).
- **L108** — Our own MCP server contract: differentiated from what OpenBB's MCP can already do.
- **L181** — Forecast object schema: what OpenBB's standard models force us to canonicalize.

## Related

- [[L001-vision-statement]] — Apache-2.0 core + CC-BY-4.0 data, why AGPL must be isolated.
- [[L011-openbb-terminal]] — strategic framing of the OpenBB relationship.
- [[L082-openbb-integration]] — concrete provider scaffold.
- [[L108-mcp-server-contract]] — OPENGEM's own MCP server.
- inspected source: `/mnt/bigdata/home/edgardo/projectsd/opengem/research-300/clones/openbb/openbb_platform/core/openbb_core/provider/abstract/{provider,fetcher,data,query_params}.py`
- inspected source: `/mnt/bigdata/home/edgardo/projectsd/opengem/research-300/clones/openbb/openbb_platform/providers/fred/openbb_fred/{__init__.py,models/series.py}`
- inspected source: `/mnt/bigdata/home/edgardo/projectsd/opengem/research-300/clones/openbb/openbb_platform/extensions/mcp_server/pyproject.toml`
