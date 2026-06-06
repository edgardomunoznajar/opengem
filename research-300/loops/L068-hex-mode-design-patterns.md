# L068 — Hex / Mode: Closed-Source Design References, Patterns OPENGEM Should Steal

**Loop**: 068 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

Hex and Mode are closed-source paid notebook BI platforms — Hex is the present-day frontier ($25/seat/mo individual, $100+/seat/mo team, recently acquired massive enterprise traction in 2024-2025), Mode is the older incumbent (Thoughtspot-acquired 2023, in slow decline as the new owner shifts focus). Neither is adoptable by OPENGEM — they are SaaS, closed, per-seat priced, and architecturally hostile to "publish-as-static-site" workflows.

But both are gold mines for *design patterns* OPENGEM should steal verbatim. The two products invented or popularized the following affordances that the open-source world has only partially absorbed:

1. **Notebook-as-app**: the same artifact authors data work and renders the final product.
2. **App publish step**: the notebook becomes a "report" via an explicit publish action, with a clean public URL.
3. **Magic AI prompts**: the "I want a chart of X by Y" → AI-generated query + chart.
4. **Stored datasets / certified queries**: the semantic layer is bottom-up, *authored* by analysts in the same tool.
5. **Snapshot views**: every report is auto-archived at each publish; the "as-of" view is a click.
6. **Embed scripts**: every chart has a one-line embed code that drops it into Notion, Substack, etc.

This loop is shorter than the OSS deep dives because there is no adoption decision — only a *pattern theft* list. Verdict for adoption of either: **SKIP**.

## Hex's design heritage and what to steal

Hex's product is structured around the *App layer* sitting on top of a *Notebook layer*. The notebook is where analysts write SQL + Python + visualization code; the app layer is a drag-and-drop UI builder that turns notebook cells into widgets users can configure. The publish step takes a snapshot of the notebook output + the app UI definition, freezes it into a static archive, and serves the archived version with optional live re-execution.

**Patterns OPENGEM should steal**:

- **Two-mode authoring**. The same artifact has a "build mode" (where the OPENGEM operator iterates) and a "view mode" (where the public reader interacts). Observable Framework has this implicitly (`preview` vs `build`); make it explicit in the OPENGEM docs.
- **Magic AI prompts on top of grounded data**. Hex's "ask the data" pattern is exactly the MCP server angle. OPENGEM exposes an MCP server; "ask the OPENGEM forecast" from inside ChatGPT/Claude is the same Hex affordance, *without* the per-seat lock-in.
- **Notebook agent for explanation drafting**. Hex's "notebook agent" (2025 GA) drafts a narrative around the analyst's queries. OPENGEM should ship a "draft me a tearsheet" tool that takes a country + horizon and emits the methodology-grounded narrative as a starting point.
- **Sidebar navigation + KPI strip + content grid**. The standard Hex app layout (~280px sidebar, 4-6 KPI metric strip across top, content grid below) is the *terminal-grade dashboard layout*. Steal it for the OPENGEM country page.
- **Schedule-and-email a report**. Hex lets you schedule any report to email. OPENGEM should ship "subscribe to this country's monthly digest" from week one — RSS, email, both.
- **Branded public links**. Hex's public report URLs are clean, have OG metadata, render previews in Slack. OPENGEM must match this discipline — every page is sharable, every OG card is rich, every Slack/Discord paste shows a preview.

## Mode's design heritage and what to steal

Mode is older (founded 2013), more SQL-centric, less Python-flexible than Hex. Pre-acquisition it was the go-to "we live in the warehouse" BI tool for mid-stage startups. The Thoughtspot acquisition has slowed its roadmap; new buyers in 2026 should not adopt Mode.

**Patterns OPENGEM should steal**:

- **Visual SQL editor + raw SQL view**, side by side. The visual editor surfaces joins, filters, group-bys; the SQL view shows the underlying query. Analysts toggle between modes. OPENGEM's "how is this number computed" affordance should follow this template — show the friendly methodology summary by default, with an "(see the SQL/query)" expand.
- **Liveboards**. Mode's term for "set of charts that share a parameter and re-render together." OPENGEM's country page is a liveboard parameterized by country.
- **Definitions**. Mode's "definition" is a named SQL CTE that other queries can reference. This is the semantic layer in microcosm. OPENGEM's "indicator" is the macro-data analog — a named series with a methodology, referenceable by ID across pages.
- **The "Latest" and "Snapshot" toggle on every chart**. Every chart in Mode lets the viewer toggle between "as-of now" and "as-of when the report was published." OPENGEM must do this — the *vintage drawer* is the multi-vintage version, but a simple two-state toggle handles 90% of cases.

## What both products do that OPENGEM should NOT steal

- **Per-seat pricing**. Antithetical to the public-ledger thesis.
- **Closed source**. Antithetical to the composable-substrate thesis.
- **Auth-gated default**. Hex and Mode default to private; OPENGEM defaults to public.
- **Notebook-as-the-only-authoring-mode**. OPENGEM authors data work in Python repos with version control, not in a SaaS notebook. The notebook idiom is for *exploration*, not for production assets.
- **"Schedule a snapshot" instead of "rebuild on every commit"**. OPENGEM's discipline must be that data updates trigger rebuilds (or vintage rollovers), not that humans schedule daily refreshes.

## What this means for OPENGEM's product roadmap

Three specific commitments fall out of this loop:

1. **Every page has an "explain this view" affordance** that pops up the methodology, the underlying SQL/query, the data sources, the model card. (Mode's "definition" pattern, generalized.)
2. **Every page is shareable with a clean OG card** including a server-rendered preview image of the lead chart. (Hex's public-link discipline, made strategic.)
3. **The MCP server is the "magic prompt" layer**. We don't build an in-product chat. We expose tools; the user's existing LLM (ChatGPT, Claude, Gemini) is the chat client. (Hex's notebook-agent, decoupled.)

## Cost (of stealing the patterns, not the tools)

| Pattern | Implementation cost | Loop |
|---|---|---|
| Two-mode authoring | 0 (Observable Framework gives it) | L066 |
| MCP "ask the forecast" | 2 weeks | L108 |
| Sidebar+KPI+grid layout | 1 week | L122 |
| Schedule/email digest | 2 weeks | L106 |
| Branded public links + OG | 1 week | L107 |
| Methodology pop-up everywhere | 2 weeks | L132 |
| Latest/Snapshot toggle | 1 week | L132 |

## Verdict

- **Hex adoption**: **SKIP**. Wrong economic shape (per-seat closed SaaS).
- **Mode adoption**: **SKIP**. Wrong economic shape *and* the product is in slow decline post-acquisition.
- **Steal-the-patterns**: **ADOPT-V1** for every pattern in the list above. Track each as an explicit OPENGEM affordance.

## Cost summary

| Use | Cost | Ramp |
|---|---|---|
| Hex license | (skipped) | (skipped) |
| Mode license | (skipped) | (skipped) |
| Pattern theft | $0 (engineering time, ~6 weeks aggregate) | various |

## What comes next

- **L069** picks the visualization library family across OPENGEM chart types.
- **L122** drafts home-screen layout candidates (Hex-pattern theft starts here).

## Related

- [[L066-observable-framework]] — gives us two-mode authoring for free
- [[L108-mcp-server-contract]] — the "magic prompt" decoupled into MCP
- [[L122-home-screen-layouts]] — Hex sidebar+KPI+grid layout adopted here
- [[L132-vintage-drawer]] — Mode's latest/snapshot, made strategic
