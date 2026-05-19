# OPENGEM — Open Global Economic Macroeconometric Forecasting System

**Program:** OPENGEM-1
**Block:** I
**Lifecycle:** Waterfall (DoD-5000 / MIL-STD-498 derived)
**Status:** Pre-PDR — design phase
**License:** Apache-2.0 (code) / CC-BY-4.0 (docs, data, model cards)

## Mission

Deliver an open-source, continuously verifiable, multi-country macroeconomic forecasting and scenario system at operational parity (≥70% use-case coverage) with proprietary incumbents (Oxford Economics GEM, NIESR NiGEM, Moody's Analytics), at a sustaining cost of <USD 200/month, with statistical performance auditable in public.

## Repository Layout

```
docs/
  design/
    00-program/      Program-level documents (CONOPS, StRS, SRS, SAD, AGP, CMP)
    10-subsystems/   SSDDs — Subsystem Design Documents
    20-interfaces/   ICDs — Interface Control Documents
    30-data/         DBDD — Database Design Document
    40-vv/           V&V Plan and test specifications
    50-risk/         Risk Management Plan and register
    60-schedule/     WBS, master schedule, gate criteria
    70-cm/           Configuration Management
```

## Current Phase

Design only. **No implementation code committed at this stage.**

Per the project charter:
1. Concept (CONOPS, StRS) → System Requirements Review (SRR)
2. Requirements (SRS, ICDs) → System Design Review (SDR)
3. Preliminary Design (SAD, SSDDs) → **Preliminary Design Review (PDR)**
4. Critical Design (DBDD, frozen ICDs, V&V plan) → CDR
5. Implementation (post-CDR only)

## Entry Point

Start at [`docs/design/00-program/00-master-design-document-v1.0.md`](docs/design/00-program/00-master-design-document-v1.0.md) — the integrated v1.0 design document set, which links forward to per-subsystem documents as they are realized.
