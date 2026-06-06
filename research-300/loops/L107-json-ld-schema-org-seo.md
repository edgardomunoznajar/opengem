# L107 — JSON-LD + Schema.org for SEO: Which Types per Page, with Microdata Samples

**Loop**: 107 / 300
**Phase**: 2 — Deep dive on top candidates
**Date**: 2026-06-06

---

## Thesis of this loop

L007 ranked SEO as the #1 ROI channel for the credibility cohort and #2 for the volume cohort. The matrix-fill discipline (10,000 country×indicator pages indexed within 30 days of launch) was the headline tactic. This loop is the *machine-readable* layer that converts those 10,000 pages from "things Google indexes" into "things Google understands as datasets with provenance, statistical content, and authored news."

The schema.org vocabulary has a long tail of types. Most are wrong for OPENGEM (we are not Organization-with-product-catalog, we are not Restaurant-with-menu, we are not Recipe). The right types — narrowly — are: **`Dataset`** for indicator and forecast pages, **`Article`** + **`NewsArticle`** for the failure-log and editorial posts, **`Observation`** for individual data points, and **`StatisticalPopulation`** for the cross-country aggregates. There's a fifth, **`Question` / `QAPage`**, that we deploy on the methodology pop-ups to capture the "what is X" long-tail queries.

Verdict: **emit JSON-LD blocks on every page with the type-matrix below; use the `Dataset` type aggressively (Google's "Dataset Search" surface is a free-attention engine for OPENGEM); ship per-vintage `Observation` markup so a single page can rank for both "current CPI" and "CPI as of September 2024"; let the `NewsArticle` markup on failure-log posts trigger Google's "Top Stories" carousel when a major miss is published.**

---

## The type matrix

Per OPENGEM page family, the schema.org types emitted:

| Page family | Primary type | Secondary types | Notes |
|---|---|---|---|
| Country page `/c/{iso3}` | `Place` (Country) | `Dataset` (containing all indicators) | Includes `containsPlace` for cities if relevant |
| Indicator page `/i/{slug}` | `Dataset` | `StatisticalPopulation` | Variable, units, observation count |
| Country×indicator page `/c/{iso3}/{slug}` | `Dataset` | `Observation` × N (vintage history) | The flagship SEO surface |
| Scenario page `/s/{slug}` | `Dataset` | `Article` (methodology) | Probability is a `propertyValue` |
| Forecast page `/f/{id}` | `Dataset` | `Observation`, `Article` (methodology link) | `dateModified` per vintage |
| Methodology page `/methodology/{slug}` | `TechArticle` | `Question` / `QAPage` | Common questions inline |
| Leaderboard page `/leaderboard` | `Dataset` | `Table` | Ranked list |
| Track-record page `/track-record/{indicator}` | `Dataset` | `Observation` (forecast vs realized) | Honest |
| Failure-log post `/failure/{id}` | `NewsArticle` | `Article`, `Dataset` (the miss data) | Triggers Top Stories |
| About / governance `/about` | `Organization` | — | Single emitter |
| API docs `/api` | `WebAPI` (`SoftwareApplication`) | — | One-page emit |
| MCP install `/mcp` | `SoftwareApplication` | — | LLM-discoverable |

The pattern: **most OPENGEM pages are `Dataset`-shaped because they ARE datasets**. We are not pretending — every country×indicator page literally is a public dataset with `variableMeasured`, `observationDate`, `observationAbout`, etc. Google's Dataset Search has been live since 2018 and is one of the most underexploited indexing surfaces.

---

## The Dataset markup template (the workhorse)

This is the JSON-LD block emitted on every country×indicator page. It's the single most important template in the codebase because it powers ~10,000 pages.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Dataset",
  "@id": "https://opengem.org/c/USA/cpi_yoy",
  "name": "United States — Consumer Price Index, Year-over-Year",
  "description": "OPENGEM's tracked vintage of US headline CPI YoY, with nowcasts, forecasts, and consensus overlays. Updated daily; every vintage is preserved.",
  "url": "https://opengem.org/c/USA/cpi_yoy",
  "sameAs": [
    "https://fred.stlouisfed.org/series/CPIAUCSL"
  ],
  "creator": {
    "@type": "Organization",
    "name": "OPENGEM",
    "url": "https://opengem.org"
  },
  "publisher": {
    "@type": "Organization",
    "name": "OPENGEM",
    "url": "https://opengem.org",
    "logo": "https://opengem.org/static/logo-512.png"
  },
  "license": "https://creativecommons.org/licenses/by/4.0/",
  "isAccessibleForFree": true,
  "keywords": [
    "United States", "USA", "CPI", "inflation", "consumer prices",
    "macroeconomics", "forecast", "nowcast", "vintage data"
  ],
  "spatialCoverage": {
    "@type": "Country",
    "name": "United States",
    "identifier": "USA"
  },
  "temporalCoverage": "1947-01-01/..",
  "variableMeasured": {
    "@type": "PropertyValue",
    "name": "CPI YoY",
    "unitText": "percent",
    "value": 3.2,
    "minValue": -2.1,
    "maxValue": 13.5
  },
  "dateModified": "2026-06-06",
  "version": "v2026.06.06",
  "distribution": [
    {
      "@type": "DataDownload",
      "encodingFormat": "application/json",
      "contentUrl": "https://opengem.org/v1/forecasts?country=USA&indicator=cpi_yoy"
    },
    {
      "@type": "DataDownload",
      "encodingFormat": "text/csv",
      "contentUrl": "https://opengem.org/v1/forecasts.csv?country=USA&indicator=cpi_yoy"
    },
    {
      "@type": "DataDownload",
      "encodingFormat": "application/rss+xml",
      "contentUrl": "https://opengem.org/feeds/c/USA/cpi_yoy.rss"
    }
  ],
  "citation": "OPENGEM (2026). United States CPI YoY, vintage 2026-06-06. https://opengem.org/c/USA/cpi_yoy?v=2026-06-06"
}
</script>
```

Key choices:

- **`license` is CC-BY-4.0** — matches OPENGEM's data license commitment and signals "free to use" to Google.
- **`distribution` lists JSON, CSV, RSS** — three formats Google's Dataset Search surfaces explicitly.
- **`isAccessibleForFree: true`** — a Google ranking factor for the dataset carousel.
- **`citation`** — gives anyone copying the JSON-LD a ready-to-paste APA-style citation.

---

## The NewsArticle markup for failure-log posts

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "Why our 2026-Q1 USA GDP nowcast missed by 80bp",
  "datePublished": "2026-04-30T14:00:00Z",
  "dateModified": "2026-04-30T14:00:00Z",
  "author": {
    "@type": "Organization",
    "name": "OPENGEM"
  },
  "publisher": {
    "@type": "Organization",
    "name": "OPENGEM",
    "logo": {
      "@type": "ImageObject",
      "url": "https://opengem.org/static/logo-amp.png"
    }
  },
  "image": "https://opengem.org/static/failure/2026-q1-us-gdp.png",
  "articleSection": "Failure log",
  "about": {
    "@type": "Dataset",
    "name": "USA GDP nowcast",
    "url": "https://opengem.org/c/USA/gdp_yoy"
  }
}
</script>
```

This triggers Google's "Top Stories" carousel eligibility. A major miss with a published post-mortem becomes a Top Stories candidate the day it publishes — which converts the *act of admitting an error* into a brand-awareness moment.

---

## The Observation markup (per-vintage)

A country×indicator page emits one `Observation` for each material vintage in its lineage. Capped at the last 30 vintages on the main page; the full vintage list is on a `/c/{iso3}/{indicator}/vintages` sub-page that emits all of them.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Observation",
  "observationDate": "2026-06-06",
  "observationAbout": {
    "@type": "Country",
    "name": "United States",
    "identifier": "USA"
  },
  "measuredProperty": {
    "@type": "PropertyValue",
    "name": "CPI YoY",
    "unitText": "percent"
  },
  "value": 3.2,
  "marginOfError": {
    "@type": "QuantitativeValue",
    "minValue": 2.8,
    "maxValue": 3.6,
    "unitText": "percent",
    "description": "P10-P90 forecast band"
  }
}
</script>
```

The `marginOfError` field captures the forecast band. This is unusual machine-readable specificity — most Dataset markup on the web omits uncertainty intervals. OPENGEM ships them as a brand differentiator (L008's "every forecast names its uncertainty").

---

## The Question / QAPage markup for methodology pop-ups

The methodology page captures the "what is X" long-tail queries Google's People-Also-Ask surface serves:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "QAPage",
  "mainEntity": {
    "@type": "Question",
    "name": "How does OPENGEM compute the recession probability?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "OPENGEM uses the Bauer-Mertens (2018) probit model on the 10Y-3M Treasury spread, recalibrated quarterly with extended cross-country pooling. The full methodology is documented at https://opengem.org/methodology/recession-prob-bauer-mertens.",
      "url": "https://opengem.org/methodology/recession-prob-bauer-mertens"
    }
  }
}
</script>
```

A page can emit up to ~12 Q&A pairs; Google rotates them in PAA.

---

## Anti-patterns to avoid

- **Don't emit `Organization` on every page.** Once is enough (the homepage and the about page). Overemitting fragments Google's understanding of OPENGEM's brand identity.
- **Don't emit `Product` markup.** OPENGEM is not a product catalog; the paid tier is a `SoftwareApplication` with pricing on its dedicated page.
- **Don't emit `Article` on dataset pages.** They aren't articles; they're datasets with optional methodology prose. Mixing types confuses Google's classifier.
- **Don't lie about `isAccessibleForFree`.** If a page is gated (paid tier), mark `isAccessibleForFree: false`. Misrepresenting cost gets you delisted from Dataset Search.
- **Don't ship empty `keywords` arrays.** Either emit a meaningful keywords list or omit the field.

---

## The emission strategy: server components, one component per type

The JSON-LD blocks are emitted by typed React components in the server-render path:

```tsx
// components/seo/DatasetJsonLd.tsx
export function DatasetJsonLd(props: DatasetProps) {
  const ld = buildDatasetLd(props); // pure builder
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(ld) }}
    />
  );
}
```

```tsx
// app/c/[iso3]/[indicator]/page.tsx
export default async function Page({ params }: Props) {
  const data = await fetchIndicatorData(params.iso3, params.indicator);
  return (
    <>
      <DatasetJsonLd {...mapToDatasetLd(data)} />
      {data.vintages.slice(0, 30).map((v) => (
        <ObservationJsonLd key={v.vintage_id} vintage={v} />
      ))}
      <CountryIndicatorPage data={data} />
    </>
  );
}
```

Every page family has a dedicated `<XxxJsonLd>` server component. A unit test asserts that the emitted JSON validates against Google's structured-data testing schema.

---

## Next-step: the schema-validation CI step

```yaml
# .github/workflows/seo-validate.yml
- name: Validate JSON-LD on key routes
  run: |
    npx @lhci/cli@latest collect --urls=https://opengem-preview.org/c/USA/cpi_yoy,https://opengem-preview.org/i/cpi_yoy,https://opengem-preview.org/s/oil_shock_2026,https://opengem-preview.org/failure/2026-q1-us-gdp
    pnpm run check:schema-org -- --strict
```

Where `check:schema-org` runs against the snapshotted JSON-LD output and validates against the schema.org JSON-Schema export from `schema.org/version/latest/schema.json`.

---

## What this loop produced

- A 12-row type matrix mapping every page family to its JSON-LD types.
- A full `Dataset` markup template with license, distribution formats, and citation.
- A `NewsArticle` template for failure-log posts (Top Stories trigger).
- A `Observation` template with `marginOfError` for forecast bands.
- A `QAPage` template for methodology long-tail queries.
- The server-component emission strategy.
- A CI schema-validation step.

## What comes next

- **L154** — URL convention loop pairs with this; the `@id` field is `canonical_url`.
- **L158** — cite-this-view emits the `citation` field used here.
- **L248** — JSON-LD injection implementation (Phase 5 code).

## Related

- [[L007-distribution-thesis]] — SEO is the #1 credibility channel
- [[L154-url-convention]] — canonical URL conventions feed @id
- [[L158-cite-this-view]] — citation format reused in Dataset.citation
- [[L248-json-ld-injection]] — implementation prototype loop
- [[L008-differentiation]] — vintage discipline = `Observation` per vintage
