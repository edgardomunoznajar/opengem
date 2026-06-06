# L016 — Data Publishing Platforms: CKAN, DataHub.io, PortalJS, Frictionless, Datasette

**Loop**: 016 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Why this loop exists

OPENGEM's accountability ledger needs a place to publish raw vintage forecasts as downloadable, citable artifacts. The "ledger" can't just live inside the dashboard; the *whole point* is that anyone — analyst, journalist, sovereign LP, LLM, academic — can grab the file and verify the claim independently. We need to pick a publishing pattern. This loop surveys the canonical FOSS data-publishing stack.

**The shortlist (and why each made the cut)**:

| Repo | GitHub | Stars | License | Last commit | Niche |
|---|---|---|---|---|---|
| **CKAN** | [ckan/ckan](https://github.com/ckan/ckan) | ~5.0k | AGPL-3.0 | June 2026 | Enterprise data portal |
| **DataHub.io** | (datahub.io site) | n/a (site) | Cloud freemium | Active (Datopian-managed) | Hosted, gov-focused |
| **PortalJS** | [datopian/portaljs](https://github.com/datopian/portaljs) | ~700 | MIT | Active 2026 | Modern Next.js data portal framework |
| **Frictionless / Data Package** | [frictionlessdata/datapackage](https://github.com/frictionlessdata/datapackage) | ~574 | Unlicense | May 2026 | Open spec, not a hosting product |
| **Datasette** | [simonw/datasette](https://github.com/simonw/datasette) | ~10k+ | Apache 2.0 | Continuous | SQLite-backed read-only data publishing |

(DataHub LinkedIn metadata catalog — `datahub-project/datahub`, 12k stars, Apache 2.0 — is **a different product** despite the name. It's a metadata discovery tool for internal data ecosystems, not a public-data-publishing platform. Excluded from this loop. Disambiguated in the table for searchers who confuse the two.)

## CKAN — the heavy incumbent

**The story**: built by the Open Knowledge Foundation in 2006. Powers `data.gov`, `data.gov.uk`, `data.gov.au`, `open.canada.ca/data`, `data.humdata.org`, and hundreds of national and city portals. Stewards: Datopian and Link Digital. Currently shipping CKAN 2.12 with a 3.0 architectural refresh in the pipeline. Designated a UN Digital Public Good.

**Architecture**: Python (Flask + Pylons-legacy migration in progress) + PostgreSQL + Solr (search index) + Redis (queue). Plugin ecosystem of 100+ extensions: harvesters, themes, auth, datastore-API. The DataStore extension turns CSV uploads into queryable PostgreSQL tables exposed via a tabular REST API.

**Footprint**: ~3 services (Postgres + Solr + Redis + the Python app). Production setup is Docker Compose or Kubernetes. Realistic minimum: 4 GB RAM, 2 vCPU. Not "small."

**License**: AGPL-3.0. Same flag as OpenBB — anything we host that's a derivative work has AGPL obligations. **For OPENGEM, this matters less here than at OpenBB**, because we'd be running CKAN as a *standalone server*, not linking to its code. The runtime separation keeps our Apache-2.0 dashboard code clean.

**When to use it**: if OPENGEM ever needs an open-data-portal-grade catalog with hundreds of datasets, taxonomies, harvesters, multi-tenant publishing, and government-style metadata schemas (DCAT-AP, etc.). For v1, **way overkill.**

## DataHub.io — the hosted cousin

**The story**: launched 2017 by Datopian as a hosted CKAN-flavored data marketplace, originally backed by the Open Knowledge Foundation. After a sleepy 2020–2024, it's been revitalized as "DataHub Cloud" with chat-first AI overlays (Queryless, OpenClaw integrations) in 2025-2026. The classic "core datasets" (country codes, currencies, language codes — Frictionless Data Packages with curated metadata) are still maintained.

**License**: the site is freemium SaaS. The underlying tooling (CKAN, Frictionless, PortalJS) is FOSS.

**When to use it**: if we want a *zero-server* mirror of the OPENGEM ledger for discovery, with the SEO juice of being on `datahub.io/opengem`. Plausible v2 distribution play. Not a v1 dependency.

## PortalJS — the modern data-portal framework

**The story**: Datopian's Next.js-native rewrite of the data-portal experience, MIT-licensed. Treats CKAN, GitHub, and Frictionless as pluggable backends. AI-friendly: scaffolded via Claude Code skills, with explicit attention to LLM-agent-driven portal building.

**Footprint**: Next.js + a backend of choice. Tiny — runs on Vercel / Cloudflare Pages / a static host. The CKAN-backend mode requires a CKAN install; the GitHub-backend mode requires only a repo of CSV/Parquet files; the Frictionless-backend mode requires a `datapackage.json`.

**When to use it**: this is the *strongest fit* for OPENGEM's "publish the raw ledger as a navigable open catalog" page. We host `ledger.opengem.com` as a PortalJS site with a GitHub or R2-stored backend, MIT-licensed templates, our brand on top. We avoid the CKAN install entirely.

## Frictionless / Data Package — the spec layer

**The story**: an open standard (Data Package, Table Schema, Tabular Data Resource) developed by Open Knowledge. A `datapackage.json` is a thin metadata wrapper around a folder of CSV/JSON files that names the schema, dialect, licenses, sources, and provenance. The Python and JS libraries (`frictionless-py`, `frictionless-js`) validate, transform, and publish.

**License**: spec is CC-BY; reference implementations are MIT.

**When to use it**: as the publishing format. Every OPENGEM vintage drop = one Data Package with a `datapackage.json` declaring the forecast schema, vintage date, model card link, V&V scorecard URL, CC-BY-4.0 license. This is the *minimum* commitment we should make at v1.

## Datasette — the dark horse

**The story**: Simon Willison's read-only-SQLite-as-website tool. Apache 2.0. Aggressive plugin ecosystem (`datasette-plugins.com` lists ~100 plugins). Mature, opinionated, single-developer-maintained-but-stable.

**Architecture**: a SQLite database file becomes a navigable web UI + REST API + GraphQL + Atom feed + CSV/JSON export — auto-generated. Add a plugin like `datasette-cluster-map` and your geo-tagged rows become an interactive map. Add `datasette-vega` and you get Vega-Lite charts per query. Everything is hyperlinked and citable by SQL query.

**Footprint**: a single Python process + a SQLite file. Runs on Cloud Run / Fly.io / Vercel-via-`datasette-publish-vercel`. Realistic minimum: 256 MB RAM. We could publish the entire OPENGEM ledger as one SQLite database with daily snapshots.

**When to use it**: for the `/data` raw-access surface (L095, L253). Pair it with PortalJS for the *curated* catalog view and Datasette for the *raw-SQL-power-user* view. The combination is hard to beat for "machine-readable forecasts with provenance the LLM can chew on" (L001).

## The proposed stack for OPENGEM's open ledger

| Surface | Tool | Why |
|---|---|---|
| Publishing format | **Frictionless Data Package** | Open spec, CC-BY licensed, every vintage drop = one package |
| Curated catalog UI | **PortalJS** on Cloudflare Pages | MIT, Next.js, AI-friendly, no server tax |
| Raw SQL / API access | **Datasette** at `/data` | Free SQL + JSON + CSV + Atom for every query |
| Storage backend | **GitHub + R2** | Public versioned history of every vintage |
| Discovery mirror | **DataHub.io** community account | Zero-cost distribution; v2 |
| Heavy enterprise portal | **CKAN** | Skip; revisit only if we partner with a gov body |

Total infrastructure cost at v1: under $10/month. PortalJS is static on Pages; Datasette runs on Cloud Run with scale-to-zero; R2 is cheap object storage; GitHub is free for public repos.

## Cost-benefit

| Action | Cost | Benefit |
|---|---|---|
| Adopt Frictionless Data Package as publishing format | 1 week (schema + tooling) | Standards-compliant, citable, LLM-friendly |
| Stand up PortalJS catalog | 1 week | Discoverable open ledger UI |
| Stand up Datasette `/data` | 0.5 week | Raw SQL + auto-feeds; *defines* the "open ledger" promise |
| Stand up CKAN | 3+ weeks | Net negative at our scale |
| Mirror to DataHub.io | 0.5 week (v2) | SEO + distribution; defer |

## Surprise of the loop

**Datasette is the unsung gem.** It's been around since 2017, Simon Willison-maintained, and it does something none of the other tools quite do: it turns a tidy SQLite file into a *fully navigable, fully citable, fully machine-readable* website with zero configuration. For the *accountability ledger* page (L175, L259, L285), where the value proposition is "you can verify every cell of every backtest" — Datasette's "every URL is an SQL query you can share and the response is JSON, CSV, or Atom" model is *exactly* the right primitive. The full-stack "Bloomberg killer" instinct pushed us toward CKAN; the realist instinct says Datasette + PortalJS + Frictionless wins.

## What this loop produced

- Disambiguation: DataHub.io (Datopian/public-data publishing) ≠ DataHub (LinkedIn/internal metadata).
- Four-row stack proposal: Frictionless + PortalJS + Datasette + GitHub/R2.
- Explicit rejection of CKAN for v1.
- DataHub.io mirror deferred to v2 as a distribution play.

## What comes next

- **L076** — Datasette + dclient for read-only data publishing (Phase 2 deep dive).
- **L078** — Iceberg / Delta Lake for vintage storage at scale.
- **L095** — Datasette public-ledger pattern (Phase 2).
- **L175** — Accountability page architecture.
- **L259** — Track-record open ledger page (Phase 5 prototype).

## Related

- [[L001-vision-statement]] — "every vintage of every forecast it has ever made (provenance-stamped)" needs this stack.
- [[L011-openbb-terminal]] — AGPL trap, again (CKAN).
- [[L014-finos-perspective]] — pivot/grid for *interactive* views on the ledger; PortalJS+Datasette for *publishing* it.
- [[L095-datasette-pattern]] — concrete design.
- [[L175-accountability-page]] — downstream consumer of this stack.
