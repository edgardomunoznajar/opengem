# R23 — Oblique-Lawyer Parallels and Lessons

| Field | Value |
|---|---|
| Document ID | OG1-RES-023 |
| Revision | A (2026-05-24) |
| Date | 2026-05-24 |
| Status | **Cross-suite learning memo — what oblique-lawyer's evolution suggests for OPENGEM.** |

---

## 1. Why this exists

The program owner already built and shipped **oblique-lawyer** through v0.4 → v0.4.1 with similar guerrilla-developer ethos. OPENGEM is the next major project in the oblique suite. Architectural and operational lessons transfer.

## 2. Shared posture

Both systems share:

| Pattern | oblique-lawyer | OPENGEM rev C |
|---|---|---|
| Single-maintainer | Yes | Yes |
| Java/Spring read API + Python data service | Yes | Yes |
| PostgreSQL + specialty extension | pgvector | TimescaleDB |
| Use-case-driven iteration | Loop-based (Loop 23 etc.) | Phase-based (R18) |
| Public/open license | Apache-2.0 / CC-BY-4.0 | Apache-2.0 / CC-BY-4.0 |
| MCP server for personal-agentic use | Planned v0.5 | Planned v0.4 |
| Iterative documentation-first | Yes (markdown-heavy) | Yes (R00–R25 + drafts) |

## 3. Lessons that transferred

From oblique-lawyer's history (per program-owner memory and recent loop notes):

### 3.1 Vintage of data discipline

oblique-lawyer's **embedding pipeline** initially had only 4.3% of sections embedded; major Acts had zero embeddings. The Loop 23 finding was that **data foundation always trumps model sophistication**. OPENGEM has internalized this: the upstream-agency adapter cohort, vintage discipline, and Tier-V/Tier-T separation come first. L3 forecast modeling comes after the data layer is solid.

### 3.2 Use-case-driven loops

oblique-lawyer's Loop 23 *discovered* the embedding gap by trying to serve use case #7 (compare regulatory paths). The use case forced the data limitation into visibility. OPENGEM's **R15 (personal use cases)** does the same thing in advance: name the use cases first, then ensure the architecture serves them.

### 3.3 Hybrid retrieval > pure approaches

oblique-lawyer landed on BM25 + semantic (RRF) hybrid for v0.4 — the hybrid retrieval is the differentiator. OPENGEM rev C's BMA combiner over L3 variants is the same kind of move: don't bet on a single model; combine.

### 3.4 Service boundary discipline

LAW-37 removed the keyword classifier from the risk-surface critical path; LAW-49/50 added type-based noise filter and comparison endpoint. **Each change was discrete, named, justified, and scoped.** OPENGEM's LOOP_PLAN v2 is structured to support the same iterative discipline.

### 3.5 Reproducibility and provenance

oblique-lawyer's risk surface is queryable for "why did this Act score this way." OPENGEM's hash quintuple (R16) is the same idea applied to forecasts.

## 4. Lessons NOT to transfer

### 4.1 oblique-lawyer's monetization push at v0.5

Memory says "next is v0.5 (MCP monetization)" for oblique-lawyer. OPENGEM has explicitly **deferred monetization** per program-owner direction 2026-05-24. Don't import the monetization pressure into OPENGEM's Block I scope.

### 4.2 Australian legal-specific data structure

oblique-lawyer operates on a single jurisdiction with a knowable legislation catalog (~6000 Australian Acts). OPENGEM operates on 26+ countries with overlapping but distinct data structures. **Don't assume a similar "one canonical schema" works** — Tier-V/Tier-T tiering exists precisely because the data heterogeneity is fundamental.

### 4.3 Embeddings as primary structure

oblique-lawyer's pgvector embedding panel is foundational. OPENGEM has **no equivalent** — macro forecasts are not "search problems." The temptation to "use embeddings somewhere because we have them in oblique-lawyer" should be resisted.

### 4.4 Neo4j graph layer

oblique-lawyer uses Neo4j for the legislation-citation graph. OPENGEM rev C explicitly rejects Neo4j (ADR-004 carried forward from rev B): the trade-weight graph is small enough (matrix at 35 countries) that Postgres handles it; the cross-country graph structure doesn't need graph-DB semantics until possibly Block II.

## 5. Cross-suite integration points

OPENGEM is *built to be consumed* by oblique-lawyer (and other oblique projects):

### 5.1 AU macro context for risk-surface scoring

When OPENGEM v0.4 ships AU Tier-V coverage (estimated 6–9 months post-IOC), oblique-lawyer's risk-surface scoring can ingest the current AU macro state as a feature. Risk for, e.g., responsible-lending legislation increases when GDP is decelerating + CPI is high + unemployment rising.

### 5.2 Australian regulatory comparison overlay

The LAW-50 comparison endpoint compares two Australian regulatory descriptions. OPENGEM's `/compare` endpoint could *overlay* a macro state — "which regulatory path do you want under recession-probability 0.4 vs. 0.1?"

### 5.3 Shared infrastructure conventions

| Convention | oblique-lawyer | OPENGEM |
|---|---|---|
| Code structure | Maven multi-module Java + Python data service | Same |
| Database | PostgreSQL primary | Same + TimescaleDB |
| API | Spring Boot REST + OpenAPI 3.1 | Same |
| MCP | v0.5 plan | Block I scope |
| Documentation | Markdown in-repo + auto-rendered | Same |
| Lint/test | "max Lombok, DI everywhere, aggressive linting, full test pyramid" | Same — adopt explicitly |
| Deployment | Hetzner + Modal/RunPod for GPU bursts | Same |

OPENGEM should reuse oblique-lawyer's Java conventions, CI patterns, and deployment template directly. This is essentially **shared infrastructure** without explicit code sharing.

## 6. Risk patterns shared

Both projects share these single-maintainer risks (R17):

- Attention drift across 5+ active projects
- Schema-drift in upstream sources
- Iteration loop discipline can decay
- Bus factor of 1

Mitigations are also shared: doc-as-code, mechanized correctness, explicit sunset clauses.

## 7. Speed-of-shipping comparison

oblique-lawyer's timeline (per memory):
- v0.4 (hybrid retrieval) completed; LAW-37 closed.
- v0.4.1 completed (LAW-49 + LAW-50).
- v0.5 (MCP monetization) next.

If OPENGEM matches that velocity (~quarterly Block-completion):
- Block I IOC: ~Q4 2026.
- Block I v0.4: ~Q1 2027.
- Block I v1.0 + Block II start: ~Q3 2027.

These are aspirational; OPENGEM is more complex than oblique-lawyer (multi-country data, vintage discipline, V&V matrix), so apply a 1.5× factor: IOC realistic Q1 2027, v1.0 realistic Q4 2027.

## 8. Strategic decision: oblique-lawyer vs OPENGEM attention split

Both projects compete for owner attention. Block I OPENGEM (12 months) overlaps with oblique-lawyer v0.5+ work. Options:

1. **Sequential**: complete oblique-lawyer v0.5 monetization first; then start OPENGEM Block I.
2. **Parallel low-attention**: OPENGEM Block I phases 0–2 (data foundation only) run in parallel; OPENGEM Phase 3+ waits until oblique-lawyer v0.5 ships.
3. **Drop one**: focus exclusively on whichever has higher expected value.

R23 doesn't decide this — it's a program-owner decision. R23 just notes the conflict explicitly.

## 9. Bottom line

OPENGEM and oblique-lawyer share architecture, conventions, infrastructure patterns, and risk profile. They are siblings in the oblique suite. OPENGEM benefits from oblique-lawyer's hard-won lessons (data foundation first; use-case-driven; hybrid combinations; reproducibility). Cross-suite integration is concrete (AU macro context flows into oblique-lawyer's risk-surface). Attention conflict between the two is real and the owner must manage it.

---

*End of R23 Rev A.*
