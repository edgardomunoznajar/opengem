# L011 — OpenBB Terminal / Platform: Deep Dive

**Loop**: 011 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## The repo at a glance

- **GitHub**: [github.com/OpenBB-finance/OpenBB](https://github.com/OpenBB-finance/OpenBB) (renamed from `OpenBBTerminal` — the rebrand to "Open Data Platform" already happened).
- **Stars**: ~68.7k, ~6.9k forks. By a wide margin the largest open-source finance platform on GitHub.
- **License**: **AGPL-3.0**. This is the single most important fact in the whole loop — see "license trap" below.
- **Primary language**: Python (~80%) + TypeScript for the Workspace UI.
- **Last commit**: pushed within the last 24 hours (June 2026). Active, well-funded (OpenBB raised Series A from OSS Capital). 6,852 commits on `develop`.
- **Homepage**: openbb.co, with a hosted Workspace at `pro.openbb.co` and a CLI surface at `openbb-cli`.
- **Roadmap signal**: latest stable tagged "ODP Desktop" (April 2026). The brand has clearly shifted from "Terminal" (CLI-centric, scripting-oriented) to "Open Data Platform" (multi-surface — CLI, REST, MCP, Workspace, AI agents).

## What it actually is

OpenBB is three layers stacked on top of each other:

1. **OpenBB Platform** (formerly OpenBB SDK) — a Python library that wraps ~50 data providers (FMP, Polygon, Intrinio, FRED, World Bank, IMF, Yahoo, Alpha Vantage, etc.) behind a unified, typed schema. You write `obb.economy.gdp(country="USA", provider="oecd")` and it gives you back a Pydantic model. This is the *interesting* layer for OPENGEM.
2. **OpenBB CLI** (`openbb-cli`) — the terminal interface most users know. A Python click/Textual REPL that issues commands and renders ASCII/plotly charts. Cosmetic; the real value lives one layer down.
3. **OpenBB Workspace** (Pro / Desktop) — a web/desktop UI hosted at `pro.openbb.co` and packaged as an Electron desktop. **Closed-source freemium**. Free tier has limits; paid tier adds AI agents, multi-user, white-label embeds. This is OpenBB Inc.'s revenue layer.

The provider abstraction is the load-bearing wall. Everything else is consumption surfaces over it.

## The provider system, concretely

A provider in OpenBB Platform is a separate Python package registered as a Poetry entry point under `openbb_provider_extension`. The structure is roughly:

```
openbb_myprovider/
  models/
    gdp.py         # Pydantic Fetcher class — extends QueryParams + Data
    cpi.py
  utils/
    helpers.py
  __init__.py      # myprovider = Provider(name=..., fetcher_dict={...})
pyproject.toml     # [tool.poetry.plugins."openbb_provider_extension"]
                   # myprovider = "openbb_myprovider:myprovider"
```

Each `Fetcher` defines three classmethods: `transform_query`, `extract_data`, `transform_data`. A `QueryParams` Pydantic model declares the inputs; a `Data` Pydantic model declares the output schema, which must conform to the standardized model already defined in `openbb_core` (e.g. `EconomicGdpData` with fields `date`, `value`, `country`). That standardized schema is the trick — providers are interchangeable because they all coerce to the same wire types.

There's a `openbb-cookiecutter` template that generates the scaffold. Onboarding a new provider is roughly a day's work for a developer who already understands the data source. The harder part is the testing matrix (every endpoint needs an integration test against the live API), not the code.

## "Can OPENGEM ride on it as a provider?"

**Yes, technically. No, strategically. Here's why.**

### What we'd gain by writing an `openbb-opengem` provider

- Distribution: 68.7k stargazers, 100k+ pip installs/month, Workspace users, MCP server users.
- Free QA: OpenBB's typed Pydantic schema forces us to expose forecasts in a clean canonical shape. That discipline is good even if no one uses the provider.
- A pre-built MCP server. OpenBB already ships an MCP server that re-exposes any registered provider as a tool. Free MCP distribution to ChatGPT/Claude/etc. — we don't have to build the MCP layer.
- Credibility-by-association in the "open finance" community.

### What we'd pay

- **AGPL-3.0 license incompatibility risk.** OpenBB Platform is AGPL. Any extension we ship into the OpenBB process inherits AGPL obligations. OPENGEM's stated license is **Apache-2.0 code + CC-BY-4.0 data** (L001). If we publish a provider that gets compiled/linked into AGPL code at runtime, our provider plugin code probably needs to be AGPL too. We can dual-license the *provider package* without contaminating the OPENGEM core repo, but it's a real legal-housekeeping cost. ~1 day of license review + a separate repo (`openbb-opengem-provider`) under AGPL or dual-licensed.
- ~1 dev-week to write the Fetcher classes for our top 10 endpoints (forecasts, vintages, leaderboard, surprise index).
- ~0.5 dev-week to wire integration tests against our own API.
- Maintenance tax: every time OpenBB bumps its `openbb_core` schema, the provider needs a chase. Empirically that's a once-a-quarter half-day across the OpenBB extension ecosystem.

### Net call

**Build the provider, but do not depend on OpenBB.** The provider is a distribution channel, not a substrate. The OPENGEM dashboard, MCP server, and data pipeline must stand independently. The provider repo lives separately, AGPL-isolated, and ships in Phase 4 (post-v1) when our API is stable.

Crucially, we do **not** want to *rebuild OPENGEM as an OpenBB extension*. OpenBB is built for equity-and-crypto-tilted retail and prosumer use; its macro surface is shallow (a few FRED/OECD/IMF endpoints). Our edge — vintage forecasts, accountability ledger, geopolitics overlay — has no home in OpenBB's information architecture. We need our own dashboard.

## Cost-benefit table

| Action | Cost (dev-weeks) | Benefit |
|---|---|---|
| Write `openbb-opengem-provider` as separate AGPL repo, expose 10 endpoints | 2 | Free MCP distribution; 68.7k-star repo discoverability |
| Adopt OpenBB Platform internally as our data layer | 8+ | -ve; AGPL contamination + we lose our schema autonomy |
| Submit our provider into OpenBB's official monorepo | 1 (post-write) | Higher visibility but we surrender release cadence |
| Ignore OpenBB entirely | 0 | We lose a real distribution channel |

**Recommendation**: build the provider as a separate AGPL-licensed repo, list it in OpenBB's community providers index, but never let the OPENGEM core depend on `openbb_core`. Time-box this to L082 in Phase 2 — not a v1 launch blocker, but a deliberate Phase 4 distribution play.

## What this loop produced

- Repo metadata (license, stars, activity).
- Three-layer architecture summary (Platform / CLI / Workspace).
- Provider system mechanics (Poetry entry points + Pydantic Fetchers + standardized core schemas).
- Explicit AGPL trap warning.
- Build/Buy/Ignore decision with dev-week estimates.

## What comes next

- **L012** — Qlib: equity-only, but worth understanding its DFM/ensemble pieces.
- **L020** — FinGPT/FinNLP/FinRL: same AI4Finance family worth weighing against OpenBB's MCP play.
- **L082** — Concrete provider-repo scaffold sketch (Phase 2 deep dive).
- **L108** — OPENGEM's own MCP server contract: must not duplicate what OpenBB already exposes.

## Related

- [[L001-vision-statement]] — Apache-2.0 + CC-BY-4.0 commitment is why AGPL contamination matters.
- [[L020-fingpt-finnlp-finrl]] — competing/complementing MCP play in the same neighborhood.
- [[L017-awesome-quant-roundup]] — OpenBB is the gravity well in this graph.
- [[L082-openbb-integration]] — Phase 2 detailed provider scaffold.
