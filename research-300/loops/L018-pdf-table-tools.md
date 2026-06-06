# L018 — Open-Source Financial Document Tools: PDF Tables from Central Banks

**Loop**: 018 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Why this loop exists

A lot of OPENGEM's most valuable data lives in **PDFs that no API will ever expose**:

- IMF Article IV consultation reports (per-country, every 1-2 years; selected indicators rarely make it into SDDS).
- BIS Quarterly Review tables (sometimes only in PDF for the most recent quarter; the SDMX feed lags).
- Central-bank Monetary Policy Reports (Fed Tealbook, ECB SMA, BoE Inflation Report, RBA Statement on Monetary Policy) — tables with staff projections.
- OECD Economic Outlook chapter annexes.
- World Bank Global Economic Prospects regional tables.
- BIS Annual Economic Report charts.
- National central bank inflation expectation surveys.

Many of these tables represent **the original source of truth** for forecasts and projections that other publications cite. Skipping them = depending on second-hand citation. For an accountability ledger thesis (L001), that's unacceptable. We need PDF-to-table tooling that actually works on the messy, mixed-grid, footnoted, multi-column financial-document layouts these bodies produce.

## The candidate stack

| Tool | GitHub | Stars | License | Last commit | Engine |
|---|---|---|---|---|---|
| **camelot-dev/camelot** | [camelot-dev/camelot](https://github.com/camelot-dev/camelot) | ~3.8k | MIT | June 2026 (v2.0.0) | pdfium / ghostscript / pdfplumber backends |
| **chezou/tabula-py** | [chezou/tabula-py](https://github.com/chezou/tabula-py) | ~2.3k | MIT | Dec 2024 (selective maintenance) | Java tabula-jar bridge |
| **jsvine/pdfplumber** | [jsvine/pdfplumber](https://github.com/jsvine/pdfplumber) | ~8.1k | MIT | 2026 active | pdfminer.six fork |
| **pymupdf/PyMuPDF** | [pymupdf/PyMuPDF](https://github.com/pymupdf/PyMuPDF) | ~7.8k | AGPL-3.0 + commercial | 2026 active | MuPDF |
| **DS4SD/docling** | [DS4SD/docling](https://github.com/DS4SD/docling) | ~25k+ | MIT | 2026 very active | Layout-aware ML pipeline (IBM Research) |
| **FinTabNet** (dataset) | IBM developer exchange | n/a | CDLA-Permissive | 2020 | Dataset only |

## Side-by-side, opinionated

### camelot — the workhorse

camelot-dev/camelot (forked and revived after the original atlanhq/camelot went stale in 2023) is the *right tool for clean lattice tables*. Five parsers — `lattice` (ruled tables), `stream` (whitespace), `network` (hybrid, new in v2), `hybrid`, and an optional ML mode. v2.0.0 (June 2026) ships with **pdfium as default backend** — no ghostscript install required. Output is pandas-native.

Where it wins: any table with visible borders. ECB SMA staff projections, OECD EO Annex tables, BIS Quarterly Review pages 80+. The lattice parser is the single most reliable table-extraction routine in the Python ecosystem.

Where it loses: borderless multi-column tables with stacked headers and footnoted rows (IMF Article IV, especially older vintages pre-2018). The `stream` parser tries but the cell-merging confuses it.

Install footprint: 200-300 MB after `pip install camelot-py[base]`. The pdfium wheel removes the Ghostscript dependency that made camelot painful to install on Windows for years.

### tabula-py — the Java bridge

A thin Python wrapper around the Java-based `tabula-jar`. Slower than camelot, harder to deploy (requires JRE 8+), but historically more accurate on certain *stream* (borderless) PDFs because tabula-jar's heuristics are different from camelot's. **Last meaningful commit was Dec 2024.** It's in "frozen, works" mode.

Install footprint: 150 MB Python + ~200 MB JRE. The JRE requirement is the dealbreaker for Cloud-Run-scale-to-zero deployments.

### pdfplumber — the surgical tool

When camelot fails on a weird layout, pdfplumber is the escape hatch. Pixel-level control over `extract_tables()` with explicit `table_settings` (line-detection thresholds, snap-tolerance, intersection-strategy). You get `find_tables()` returning bounding boxes you can debug visually with `to_image()`. **Visual debugging is what makes pdfplumber irreplaceable**: when an extraction fails, you can save a PNG with overlaid bbox lines and *see* why.

Use case: the "we have a weird IMF table from 2002 that no automated parser handles" tail.

Install footprint: ~150 MB. Pure Python (pdfminer.six fork).

### PyMuPDF — fast and license-traped

MuPDF wrapper — fastest text and image extraction in the Python ecosystem. Has `page.find_tables()` since v1.23 (2023). License is **AGPL-3.0** unless you buy a commercial license from Artifex. For OPENGEM's Apache-2.0 thesis, this is the same trap as OpenBB/CKAN — we avoid linking it into core code. (We *can* use it as an isolated CLI tool in our offline ETL pipeline if we don't redistribute, but the licensing-housekeeping cost is real.)

### docling — the IBM ML-pipeline newcomer

IBM Research's Deep Search team's open-source layout-aware document parser. Combines a TableFormer model trained on FinTabNet with layout analysis (TableTransformer fork) and produces structured Markdown / JSON with table-of-contents preservation. **The most exciting tool in this loop.** 

Where it wins: financial documents specifically. The training set (FinTabNet — SEC 10-K filings, 89k pages, CDLA-Permissive licensed) is structurally close to central-bank reports. On hard cases (merged-cell IMF tables, multi-period BoE projection grids) docling outperforms camelot in published benchmarks (~82% accuracy on FinTabNet test set per DocLD's benchmark vs ~78% for IBM's own GTE, ~65% for Microsoft's TATR).

Where it loses: install footprint is ~5 GB if you want all the layout models locally (or pay the latency of remote inference). Slow per-page (~1-5 seconds vs camelot's milliseconds).

### FinTabNet — the training dataset

Not a tool, a dataset. CDLA-Permissive license. 89,646 pages with 112,887 tables from S&P 500 annual reports. The OTSL conversion (DS4SD/FinTabNet_OTSL on HuggingFace) is the modern training format. We don't train; we benefit because docling, TableTransformer, and others have already trained on it. *The reason docling is so good on financial layouts is FinTabNet's coverage.*

## The proposed OPENGEM ETL strategy

A two-stage pipeline keyed on document class:

1. **Lattice-ruled PDFs (OECD EO, BIS Quarterly, ECB SMA, FRB SEP tables)** → camelot `lattice`. Fast, accurate, 5 ms per page. ~90% of central-bank publications use ruled tables.

2. **Borderless or mixed PDFs (older IMF Article IV, central-bank inflation reports with stacked headers)** → docling fallback. Slower but ML-robust. We containerize the docling models once and run them as a Cloud Run job that scales to zero.

3. **Edge cases that fail both** → pdfplumber with bespoke `table_settings`, hand-tuned per source. Document the recipe in `prototypes/pdf-extractors/<source>.py`. Expect ~10-15 such recipes for the long tail.

4. **Validation gate** → every extracted table runs through Great Expectations (L017 entry #22) checks: column count matches expected schema, last row sums to total, numeric columns parse cleanly, no NaN in primary key columns. A failed gate routes the table to a human-review queue, *not* to the published ledger.

Total dev investment: ~3 weeks for the core pipeline + 1 day per long-tail document class.

## What about the cost-benefit?

| Action | Cost | Benefit |
|---|---|---|
| Adopt camelot for 90% of documents | 1 week | Solid lattice-table coverage |
| Adopt docling for hard cases | 1 week + container budget | ML robustness on financial layouts |
| Adopt pdfplumber for edge cases | 0.5 week + per-source recipes | Last-resort visual-debug-driven extraction |
| Skip PDF tables entirely | 0 | Major coverage gap; depending on second-hand citation; breaks accountability thesis |
| Adopt PyMuPDF | 1 week + AGPL housekeeping | Speed; not worth the license cost |
| Train our own model on FinTabNet | 4-6 weeks | Net negative; docling already did this |

## The unsung lever: docling

**docling is the surprise of this loop and may end up being more strategically important than any of the dashboard libraries.** Reasoning:

- It's MIT, IBM-backed, currently ~25k+ stars and accelerating.
- It outputs *structured Markdown* — meaning we get headers, lists, and tables all preserved in a single LLM-friendly format. This is exactly the right input shape for L020 (FinGPT/FinNLP narrative generation) and L198 (forecast-to-narrative pipeline).
- The same pipeline that extracts BIS Quarterly Review tables for our ledger can re-parse a freshly published WEO PDF into Markdown-with-tables that our MCP server can serve to ChatGPT/Claude *with provenance intact*.
- IBM Research is investing in it as the open-data-pipeline-for-AI substrate. It's getting better fast.

This makes docling a candidate for the *document-ingestion substrate* role in OPENGEM, parallel to how Nixtla (L017) is the forecast substrate.

## What this loop produced

- Six-tool comparison with license, last-commit, and install-footprint data.
- Two-stage pipeline (camelot lattice + docling fallback + pdfplumber edge-case).
- Explicit AGPL rejection of PyMuPDF.
- Identification of docling as a strategic substrate.

## What comes next

- **L020** — FinGPT / FinNLP / FinRL: the narrative-generation half (docling feeds it).
- **L076** — Datasette + dclient: publishing the extracted tables.
- **L184** — Generic shock library (impulse responses): central-bank PDF tables are inputs.
- **L198** — Forecast-to-narrative pipeline: docling output is one input.
- **L286** — Failure-log page: PDF extraction failures get post-mortems too.

## Related

- [[L001-vision-statement]] — "every number is dated" demands first-party PDF extraction.
- [[L011-openbb-terminal]] / [[L016-data-publishing-platforms]] — AGPL trap rejection pattern.
- [[L017-awesome-quant-roundup]] — docling didn't appear in awesome-quant but should.
- [[L020-fingpt-finnlp-finrl]] — downstream narrative consumer of docling Markdown.
