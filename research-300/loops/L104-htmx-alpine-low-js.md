# L104 — htmx + Alpine for a Low-JS Server-Rendered Alt: When (if Ever) OPENGEM Should Use It

**Loop**: 104 / 300
**Phase**: 2 — Deep dive on top candidates
**Date**: 2026-06-06

---

## Thesis of this loop

Next.js + React (L073) is the right pick for the OPENGEM main dashboard — the command palette, the globe, the lightweight-charts forecast bands, the multi-pane comparison views all benefit from a real component tree and client-side state. But there is a *second* surface of OPENGEM whose constraints invert the calculus: the public **SEO matrix** (10,000 country×indicator pages from L007's tactic 1), the **embed PNG/SVG renderers**, and the **RSS-item landing pages** that need to load in under 200ms on a 3G connection in Lagos because that's where the Damian-class audience actually lives.

This loop tests whether OPENGEM should adopt htmx + Alpine as a parallel, server-rendered stack for the SEO surface, keeping Next.js for the interactive app. The honest answer is *almost yes, but actually no* — Next.js's app-router with `output: 'export'` for the static pages gets us 95% of the htmx wins without the cost of running two stacks. The 5% delta isn't worth the doubled mental overhead for a one-person team.

Verdict: **SKIP htmx + Alpine as a parallel stack. ADOPT the discipline they represent: every country×indicator page must be server-rendered, hydration-free, sub-15KB JS payload, RSS/JSON-block-friendly. Achieve that within Next.js using app-router server components, `export const dynamic = "force-static"`, and a strict "no client component on this route" lint rule.** Keep htmx + Alpine in the back pocket as the migration target if Next.js's hydration costs become an actual revealed problem at scale (which would be a Y3 conversation, not Y1).

---

## The case *for* htmx + Alpine (taken seriously)

htmx is the "HTML over the wire" library popularized by Carson Gross. The server returns HTML fragments in response to `hx-get` / `hx-post` requests, and htmx swaps them into the DOM. Alpine.js is a tiny (~7KB) Vue-flavored reactive sprinkle library. Together they let you build interactive web applications with virtually no JavaScript on the client — the server stays the source of truth, the client is dumb.

Why this matters for OPENGEM's SEO surface:

1. **Bundle size at the floor.** htmx is 14KB gzipped. Alpine is 7KB gzipped. Total: 21KB. A Next.js app router page with React 19 hydration is ~80KB just for the framework, plus ~20KB per route for components. The htmx page is 4x lighter.

2. **No hydration cost.** React hydration is the work of "the server sent HTML, now the client re-runs the component tree to attach event handlers." For a content-heavy country page this can be 100-300ms of main-thread work on a mid-tier Android phone. htmx has zero hydration.

3. **Better Lighthouse scores out of the box.** "Total Blocking Time" and "Interaction to Next Paint" both fall when there's no hydration. Google's search ranking uses these signals.

4. **Cheaper to crawl.** Googlebot crawls server-rendered pages without running JavaScript. Crawl budget is finite; 10,000 pages crawled in real time vs 10,000 pages crawled in client-rendered mode is a meaningful difference for how fast OPENGEM gets indexed.

5. **The mental model is simpler for a non-React contributor.** A junior contributor or an open-source PR-er who knows Jinja templates and Python can ship an htmx page in an afternoon. A React Server Component requires understanding the RSC mental model, which is non-trivial.

6. **Server-side caching is trivial.** An htmx response is just HTML. Cloudflare caches it as `Cache-Control: public, max-age=3600`. A Next.js RSC response involves React serialization markers and is more annoying to cache (though doable).

---

## The case *against* — and why it wins

1. **Two stacks is worse than one stack 95% as good.** OPENGEM is a one-person team. Maintaining a Python (FastAPI + Jinja + htmx) SEO frontend *and* a Next.js + React main app means duplicated chart components, duplicated typography, duplicated theme tokens, duplicated cite-this-view widgets. The cost of duplication is paid every week forever.

2. **Next.js can serve the SEO surface flat too.** With `app-router` + `output: 'export'` + `force-static` + no client components, a Next.js country page renders to a static HTML file at build time. No hydration unless there's a `"use client"` boundary on the page. The framework footprint is small enough (Next 15 + React 19 minimum runtime is ~38KB gzipped, *not* loaded on static-only pages because the page is just HTML).

3. **The htmx interaction model is wrong for the chart-heavy parts.** OPENGEM's country pages have interactive lightweight-charts and sparklines. Those want client-side state — zoom, hover tooltips, vintage selector. htmx's "swap an HTML fragment on click" model would require a roundtrip per zoom step, which is unacceptably slow. So even an htmx-based SEO page would still need *some* client-side JS, just less of it. The savings narrow once charts are real.

4. **The RSC model captures most of the htmx wins.** Server components do exactly what htmx wants: render HTML on the server, no JS needed unless a `"use client"` boundary is crossed. The discipline of "server component by default; client component only where you can name a specific interactive reason" is the htmx discipline expressed in React-shaped code.

5. **The team-knowledge-investment matters.** Next.js + React + Tailwind is the OPENGEM team's strength. Adopting htmx adds a stack the team has to maintain in parallel. A pure-htmx shop wouldn't have this tradeoff; we do.

---

## The discipline OPENGEM adopts (without adopting htmx)

The verdict isn't "ignore htmx's lesson"; it's "internalize htmx's lesson inside Next.js." The discipline:

1. **Every country×indicator page is a server component.** No `"use client"` at the page level. The page renders to HTML; the only client JS is the global theme toggle and the command palette.

2. **Static export the SEO matrix.** `app/c/[iso3]/[indicator]/page.tsx` exports `dynamic = "force-static"` and `generateStaticParams` returns the cartesian product of (Tier-V countries) × (top-30 indicators). At build time, ~660 pages are pre-rendered. Tier-T countries hit the dynamic edge function with `revalidate: 3600`.

3. **No global state libs on these pages.** No Redux, no Zustand, no Jotai, no React Context except for `ThemeProvider` (which is global anyway). The SEO matrix doesn't need state — it's read-only.

4. **Bundle budget per route: 15KB gzipped excluding framework.** A CI step rejects PRs that push the per-route bundle above this threshold. The framework (~50KB shared across all routes) is paid once; per-route is the constraint.

5. **Charts on SEO pages are SVG, not lightweight-charts.** The country page renders the main forecast chart as a static SVG (server-rendered via the Vega-Lite Compiler API). The interactive lightweight-charts version is on `app/c/[iso3]/[indicator]/interactive` — a separate route loaded only if the user clicks "explore." This keeps the SEO landing-page bundle near zero while preserving the interactive surface for engaged users.

6. **The cite-this-view widget is a `<details>` element with inline content, not a popover lib.** Native HTML, zero JS.

---

## When would we revisit?

Concrete triggers that would flip the verdict toward adopting htmx:

- If Next.js per-route framework bundle grows above 100KB by 2027 (currently ~50KB on Next 15; if Next 16 regresses, we re-evaluate).
- If a real contributor base materializes who is more comfortable with Python + Jinja than React. Unlikely for OPENGEM's audience profile.
- If a specific A/B test shows >10% bounce-rate improvement on htmx-rendered country pages vs Next.js-rendered. Worth running this test at Y2.

Until then, the discipline above gets us 95% of the win without the parallel-stack tax.

---

## Next-step: the lint rule

```javascript
// .eslintrc.cjs — enforce "no client component on SEO routes"
module.exports = {
  overrides: [
    {
      files: ["app/c/**/page.tsx", "app/i/**/page.tsx", "app/s/**/page.tsx"],
      rules: {
        "no-restricted-syntax": [
          "error",
          {
            selector: "Program > ExpressionStatement > Literal[value='use client']",
            message: "SEO matrix pages must be server components. Move interactive code to a child route or component on /interactive.",
          },
        ],
      },
    },
  ],
};
```

And the bundle budget enforcer:

```json
// next.config.mjs (excerpt)
"experimental": {
  "bundlePagesRouterDependencies": true
},
"webpack": (config) => {
  config.performance = {
    maxAssetSize: 15 * 1024,
    maxEntrypointSize: 65 * 1024,
    hints: "error"
  };
  return config;
}
```

---

## What this loop produced

- Verdict: SKIP htmx as a parallel stack; ADOPT the discipline within Next.js.
- A six-rule discipline for the SEO matrix surface.
- Triggers for revisiting the verdict (bundle bloat, contributor profile, A/B evidence).
- Concrete lint rule + bundle budget enforcer.

## What comes next

- **L107** — JSON-LD on every server-rendered page makes the SEO bet pay off.
- **L116** — SVG export uses the same server-rendered chart pipeline.
- **L267** — Lighthouse perf-budget script enforces the 15KB-per-route rule in CI.

## Related

- [[L073-next-tailwind-dashboard-starters]] — Next.js + Tailwind is the main app stack
- [[L074-sveltekit-solid-astro-qwik]] — alternative frameworks considered and skipped
- [[L075-static-vs-dynamic-quarto-hugo]] — static-export discipline lives here
- [[L107-json-ld-schema-org-seo]] — schema markup pairs with server rendering
- [[L116-print-grade-svg-tearsheets]] — same SVG pipeline serves both
