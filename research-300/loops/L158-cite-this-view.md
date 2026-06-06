# L158 — Cite-This-View

**Loop**: 158 / 300
**Phase**: 3 — Product design
**Date**: 2026-06-06

---

## The thesis

Academics, journalists, and government staffers will cite OPENGEM only if there is a stable, citation-grade identifier for every view. We give every URL a DOI-flavored permanent identifier and a generated citation in BibTeX / APA / Chicago / MLA / Vancouver.

The asymmetry: Bloomberg charts can't be cited (no public URL). OECD tables can be cited but the citation has no vintage. OPENGEM gives every view a vintaged ID, automatically.

## The identifier scheme

```
opengem:<entity>:<id>:<vintage>:<view-hash>

Examples:
opengem:indicator:cpi-yoy:2026-06-04:7f2a
opengem:forecast:f-01j7kabcd:2026-06-04:c11d
opengem:country:usa:2026-06-04:9a8f
```

Components:
- `opengem:` — namespace
- `<entity>` — entity type (country, indicator, forecast, scenario, news, ...)
- `<id>` — entity ID (ISO-3 code, slug, UUID v7)
- `<vintage>` — ISO date of the data vintage being cited
- `<view-hash>` — 4-char hash of the view parameters (countries, range, bands, etc.)

The hash makes view-specific URLs uniquely citable. Two different filter configurations on the same indicator get different IDs.

## DOI integration

We register OPENGEM as a DOI prefix via DataCite (or Crossref, but DataCite is more dataset-friendly). For pages we deem "high-value to cite," we mint a true DOI:

```
DOI: 10.<opengem-prefix>/cpi-yoy.usa.20260604.7f2a
```

DOIs resolve via `https://doi.org/...` to the canonical OPENGEM URL.

V1: mint DOIs lazily — first time a user clicks "Cite this view" with a non-trivial vintage pin, we mint the DOI and cache. DataCite charges nominal fees ($1/DOI for repositories — well within budget).

V2: every "view-of-record" (defined below) gets a DOI automatically on creation.

## Views of record

Not every URL needs a DOI. Three classes:

| Class | Identifier | DOI? |
|---|---|---|
| **Ephemeral** | URL only | No |
| **Citeable** | opengem:... | On request |
| **View-of-record** | opengem:... + DOI | Always |

Views of record (criteria):
- Every published forecast at vintage time
- Every leaderboard snapshot at end-of-quarter
- Every accountability-ledger entry
- Every methodology page on first publication

Editorial decision per class — applied automatically.

## The cite-this-view UI

Triggered by:
- Toolbar quote icon (Lucide `library`)
- Command palette: "cite"
- Keyboard: `mod + shift + c` (copy)
- Footer of any page: "Cite this view →"

Opens a **drawer** (L150/L151):

```
   ┌────────────────────────────────┐
   │  ✕  Cite this view              │
   │  ──────────────────────────────  │
   │                                  │
   │  Permanent ID:                   │
   │  opengem:indicator:cpi-yoy:2026-06-04:7f2a │
   │  [ Copy ]                        │
   │                                  │
   │  DOI:                            │
   │  10.99999/cpi-yoy.usa.20260604.7f2a │
   │  [ Copy ] [ Resolve in DOI.org → ]│
   │                                  │
   │  Citation format:                │
   │   ◉ APA                          │
   │   ○ Chicago                      │
   │   ○ MLA                          │
   │   ○ Vancouver                    │
   │   ○ BibTeX                       │
   │                                  │
   │  ┌────────────────────────────┐ │
   │  │ OPENGEM. (2026, June 4).    │ │
   │  │ US CPI year-over-year. From │ │
   │  │ https://opengem.app/...     │ │
   │  │ [doi:10.99999/...]          │ │
   │  └────────────────────────────┘ │
   │  [ Copy ]                        │
   │                                  │
   │  ────────────────────────────────│
   │  Reproducibility envelope:       │
   │   • Vintage: 2026-06-04           │
   │   • Methodology: combiner-v4.2    │
   │   • Data sources: FRED, ECB SDW   │
   │   • Container digest:              │
   │     sha256:7f2a8c9d...            │
   │  [ Download provenance manifest ] │
   └────────────────────────────────┘
```

The drawer:
- Shows the OPENGEM ID and DOI prominently
- Provides citation in the user's preferred format (sticky preference)
- Offers BibTeX entry for LaTeX users
- Links to the full provenance manifest (machine-readable JSON of every input)

## BibTeX example

```bibtex
@misc{opengem-cpi-usa-20260604,
  author = {{OPENGEM}},
  title = {United States Consumer Price Index, year-over-year},
  year = {2026},
  month = {6},
  day = {4},
  publisher = {OPENGEM},
  doi = {10.99999/cpi-yoy.usa.20260604.7f2a},
  url = {https://opengem.app/indicator/cpi-yoy?countries=usa&vintage=2026-06-04},
  note = {OPENGEM view ID opengem:indicator:cpi-yoy:2026-06-04:7f2a}
}
```

## APA example

```
OPENGEM. (2026, June 4). United States Consumer Price Index, year-over-year. OPENGEM. https://doi.org/10.99999/cpi-yoy.usa.20260604.7f2a
```

## Chicago example

```
OPENGEM. "United States Consumer Price Index, year-over-year." Last modified June 4, 2026. https://doi.org/10.99999/cpi-yoy.usa.20260604.7f2a.
```

## Permanence promise

The citation contract requires:

1. The URL behind the cite resolves forever (per L154's stability promise).
2. The vintage-pinned data does NOT change. Future revisions don't overwrite — they get their own vintage.
3. The methodology used at vintage time is preserved. If the methodology changes, the old version remains in the methodology catalog with the same ID.
4. If a methodology is later determined to be flawed, we publish a CORRECTION linked to the original. We do not retract.

This is the open accountability ledger thesis (L008, L175). The original view stays cite-able even if we publicly say later it was wrong.

## Cite-by-LLM

The MCP server exposes a tool `cite.lookup(view_url)` returning the cite payload as JSON. LLM agents writing research summaries can pull the citation directly. The MCP also exposes `cite.list(date_range)` to retrieve all newly-minted DOIs (for academic indexers).

## Citation index

V2: build a `/citations` page where users can:
- Search citations they've made
- Export a `.bib` of all citations they've used
- See which OPENGEM views have been cited externally (when CrossRef/DataCite citation tracking lights up)

## OAI-PMH harvester

For academic indexers and library systems, OPENGEM exposes an OAI-PMH endpoint at `/oai`. Standard protocol, returns Dublin Core for every view-of-record. Lets institutional repositories index OPENGEM data automatically.

## Schema.org

Every page emits JSON-LD with `schema.org/Dataset` markup. Google Scholar and Dimensions index automatically.

```json
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "name": "United States CPI year-over-year",
  "identifier": "opengem:indicator:cpi-yoy:2026-06-04:7f2a",
  "url": "https://opengem.app/indicator/cpi-yoy?countries=usa&vintage=2026-06-04",
  "datePublished": "2026-06-04",
  "creator": { "@type": "Organization", "name": "OPENGEM" },
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "distribution": [
    { "@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": "..." },
    { "@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": "..." }
  ]
}
```

## What we will NOT cite

- Personal annotated views (those have share-tokens, not DOIs)
- News feed snapshots (news has its own URL but we don't mint DOIs for feeds)
- Compare views with > 5 entities (combinatorial explosion of DOIs)
- Watchlist views (private)

## Implementation

- ID generation: a deterministic function `cite_id(canonical_url, vintage) → string`
- DOI minting: lazy. First click triggers a background job to register via DataCite API. The drawer shows "Minting DOI..." for ~10s, then refreshes.
- Provenance manifest: a JSON blob stored in the vintage store (R2/S3) keyed by ID
- Storage: every cited view gets an entry in `cite_index` (DuckDB-backed Datasette mount)

## Reproducibility envelope

Every cite-this-view includes a downloadable "provenance manifest":

```json
{
  "id": "opengem:indicator:cpi-yoy:2026-06-04:7f2a",
  "doi": "10.99999/cpi-yoy.usa.20260604.7f2a",
  "url": "https://opengem.app/indicator/cpi-yoy?countries=usa&vintage=2026-06-04",
  "view_params": { "countries": ["usa"], "yoy": true, "range": ["2010-01-01", "2026-06-01"] },
  "data_sources": [
    { "source": "FRED", "series": "CPIAUCSL", "retrieved_at": "2026-06-04T12:00:00Z", "checksum": "sha256:..." }
  ],
  "methodology": { "id": "combiner-v4.2", "url": "https://opengem.app/methodology/combiner-v4-2" },
  "container_digest": "sha256:7f2a8c9d...",
  "lockfile": "https://opengem.app/lockfiles/2026-06-04.lock"
}
```

This is the "scientific reproducibility" contract. Five years from now, an academic should be able to download the manifest and rerun the pipeline byte-for-byte.

(See L186 for the reproducibility envelope details — this view surfaces what L186 builds.)
