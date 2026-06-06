# L074 — SvelteKit / Solid / Astro / Qwik Dashboard Alternatives vs Next.js

**Loop**: 074 / 300
**Phase**: 1 — Open-source landscape survey
**Date**: 2026-06-06

---

## Thesis of this loop

Next.js (L073) is the *boring, correct, default* choice for OPENGEM's interactive surface. This loop honestly stress-tests that decision against four credible 2026 alternatives. Spoiler: Next.js stays, but Astro is a close enough call that it deserves a serious explanation, and Astro is the *most likely* re-evaluation if the Next.js choice goes wrong.

The candidates:
- **SvelteKit** (Rich Harris / Vercel-employed): the most polished post-React framework.
- **SolidJS / Solid Start**: signal-based fine-grained reactivity, React-like syntax.
- **Astro**: static-first, island-architecture, content-focused.
- **Qwik / QwikCity**: resumability, fine-grained lazy loading.

Verdict: **Astro for content-heavy pages (almost ties Observable Framework)**. **Next.js for the dashboard app**. **SvelteKit, Solid, Qwik all SKIP** as primary choice, all worth understanding.

## The honest reason Next.js wins (and it isn't perf)

It is not faster than SolidJS. It is not smaller than SvelteKit. It does not have Qwik's resumability cold-start advantage. It is *categorically* less elegant than Astro for content-first sites.

Next.js wins because:

1. **The component ecosystem is the largest by a wide margin.** shadcn, Tremor, TanStack, react-globe.gl, lightweight-charts-react-wrapper, all of them are React-first. The "second-class" port to other frameworks adds 1-2 weeks of bug-chasing per integration. With six integrations, that's 6-12 weeks of additional work to use SvelteKit.

2. **AI-assisted dev is React-trained.** Claude, GPT, Cursor are 5-10× more productive on React/Next than on SvelteKit/Solid/Qwik. For a one-person team in 2026, this matters enormously.

3. **The hiring/contributing pool is largest.** If OPENGEM becomes a project anyone forks or contributes to, React expertise is the largest pool. Svelte is second-largest but a long way behind.

4. **The deployment story is fully solved.** Vercel + Next.js, Cloudflare Pages + Next.js, Fly.io + Next.js, self-hosted + Next.js — every path has multiple production-tested templates.

The drawbacks of Next.js — bundle size, hydration cost, RSC complexity, the constant App Router churn — are real but they don't outweigh the above.

## SvelteKit: the most appealing alternative, still loses

- **License**: MIT.
- **Strengths**: smallest bundles (compiler eliminates the framework runtime), best DX (genuinely cleaner template syntax, intuitive store/runes reactivity), now-mature SSR.
- **Weaknesses for OPENGEM**:
  - Component library port: shadcn-svelte exists, Tremor doesn't have a Svelte port, react-globe.gl requires a wrapper or skipping the React wrapper entirely.
  - LLM productivity gap (per above).
  - "Runes" syntax shift in Svelte 5 (2024) means much of the prior Svelte ecosystem is in transition; pre-runes code is being rewritten, post-runes code is still maturing.
- **Verdict**: **SKIP** for OPENGEM v1. **EVALUATE-LATER** at Y2-Y3 *only* if a single-author rewrite is on the table.

## Solid / Solid Start: most-React-like alternative

- **License**: MIT.
- **Strengths**: React-style JSX with signal-based fine-grained reactivity. The component model is familiar; the perf is markedly better than React because there's no virtual DOM diffing.
- **Weaknesses for OPENGEM**:
  - Smaller ecosystem than React (much smaller than Svelte).
  - LLM productivity gap.
  - Solid Start (the meta-framework) is younger and less battle-tested than Next.js or SvelteKit.
- **Verdict**: **SKIP** as primary. **EVALUATE-LATER** for component-perf-sensitive sub-pages (the live ticker, for example) where Solid's reactivity beats React's.

## Astro: the genuine close-call

Astro is *island architecture* with content-first defaults: write your pages in MDX/Markdown, ship zero JS by default, hydrate "islands" (interactive components) only where needed. Astro v5 (2024) added the Content Layer API which makes type-safe content collections trivial. v6 (2026) integrated Cloudflare's edge runtime and made SSR streaming first-class.

For OPENGEM's long-tail static pages (per-country, per-indicator, per-scenario explainer pages) Astro is *almost* as good as Observable Framework. The advantages of each:

- **Observable Framework**: data loaders at build time in any language; canonical for data-app authoring; tight integration with Observable Plot.
- **Astro**: full React/Vue/Svelte interactive island support; mature ecosystem; better-defined component model.

The choice between them is closer than this loop has space to fully analyze (and that's what L091 will do in Phase 2). The first-cut answer:

- **Observable Framework** for the data-loader-heavy pages (where the build-time loader is in Python and pulls from the OPENGEM adapter library).
- **Astro** as a *plausible alternative* if Observable Framework's incremental build performance becomes a bottleneck.
- **Next.js** for the interactive dashboard app surface (home, country page interactive view, forecast page).

This loop's verdict: **EVALUATE-LATER** Astro as the Observable Framework backup plan. Don't adopt it now; keep it in the on-deck circle.

## Qwik: fascinating, premature

- **License**: MIT.
- **Strengths**: *resumability*. Qwik serializes the framework state into the HTML and "resumes" instead of hydrating. The result is genuinely faster cold-load JS execution than any other framework. For mobile-heavy traffic this is real.
- **Weaknesses for OPENGEM**:
  - Ecosystem is *tiny*. No shadcn-qwik, no tremor-qwik, no qwik-globe-gl.
  - LLM productivity gap is the worst of the candidates.
  - Qwik 2.0 is in development as of mid-2026 and the framework is still settling on its API.
- **Verdict**: **SKIP**. Revisit in Y3.

## Bundle / perf benchmarks (for reality)

Movie-app benchmark (a community comparison test on 7 frameworks):
- Astro: smallest initial JS (~5KB).
- Qwik: smallest interactive JS (~7KB).
- SvelteKit: smallest framework runtime (~10KB).
- Solid: smallest virtual-DOM-free render.
- Next.js: typically ~80-150KB framework + components.

For OPENGEM's per-page JS budget of ~100KB above-the-fold, Next.js fits comfortably with discipline. Smaller is not the differentiator — *consistency* and *ecosystem* are.

## The wildcard: Remix / React Router 7

Remix merged into React Router 7 in 2024, becoming a "framework" mode of React Router. It is the closest competitor to Next.js *within the React world*. For some workloads (heavy nested routing, classical web app feel) it can beat Next.js on ergonomics. For OPENGEM specifically:

- Same ecosystem as Next.js (React-based).
- Better defaults for forms and data mutation (less relevant — OPENGEM is read-mostly).
- Cleaner separation of server data loading and rendering.
- Slightly smaller community and fewer prebuilt templates.

**EVALUATE-LATER** as a within-React alternative if Next.js App Router specifically becomes painful. The OPENGEM team can switch React frameworks without rewriting components.

## Hosting cost (all alternatives)

- All four frameworks support Cloudflare Pages free tier ($0/mo).
- All four support Fly.io self-host ($15-30/mo).
- SvelteKit, Astro have first-class SSG mode (zero compute cost). Solid, Qwik also do but the ecosystem is less polished.
- Next.js on Vercel free tier covers Y1; SSG-able pages cost $0.

## Ramp-up

- Next.js: 1 day for a competent dev (presumed baseline).
- SvelteKit: 1 week if React-only background; 2 days if Svelte-experienced.
- Solid: 2 days from React.
- Astro: 1-2 days from any modern framework.
- Qwik: 2 weeks (steep mental model shift).

## Verdict

- **Next.js (App Router) + Tailwind v4 + shadcn + Tremor**: **ADOPT-V1** for OPENGEM's interactive dashboard surface.
- **Astro**: **EVALUATE-LATER** as the static-long-tail backup if Observable Framework underperforms in Y1.
- **SvelteKit**: **SKIP**. Revisit in Y3 if single-author rewrite is on the table.
- **Solid / Solid Start**: **SKIP**. Possible perf-pocket adoption for the live ticker page in Y2.
- **Qwik**: **SKIP**. Premature.
- **Remix / React Router 7**: **EVALUATE-LATER** as Next.js alternative inside React.

## Cost summary

| Framework | License | Cost | Y1 ramp | Hosting |
|---|---|---|---|---|
| Next.js | MIT | $0 | 1 day | $0-20/mo |
| Astro | MIT | $0 (skipped) | 1-2 days | $0/mo |
| SvelteKit | MIT | $0 (skipped) | 1 week | $0/mo |
| Solid | MIT | $0 (skipped) | 2 days | $0/mo |
| Qwik | MIT | $0 (skipped) | 2 weeks | $0/mo |

## What comes next

- **L075** examines static-site patterns (Hugo + Datasette, Quarto).
- **L089** is the Phase 2 deep dive on the Streamlit-vs-Next.js call.

## Related

- [[L073-next-tailwind-dashboard-starters]] — the winning React stack
- [[L066-observable-framework]] — the static long-tail counterpart
- [[L089-streamlit-vs-nextjs-frontend]] — Phase 2 reconfirmation
