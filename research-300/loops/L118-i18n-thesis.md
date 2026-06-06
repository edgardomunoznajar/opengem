# L118 — i18n: English-Only at v1, the Y2 Decision, and What to Instrument Now to Make it Cheap Later

**Loop**: 118 / 300
**Phase**: 2 — Deep dive on top candidates
**Date**: 2026-06-06

---

## Thesis of this loop

OPENGEM's three-cohort thesis (L001) has implicit geography. The Damian-class YouTuber, the Greg-class blogger, the Marcus-class think-tank analyst, the Nadia-class sovereign-fund LP — all are *plausibly* US-based, but each cohort's *biggest* total addressable market lives outside the Anglosphere. Macro YouTubers in Portuguese, Spanish, German, Arabic, Hindi. Sovereign funds in Riyadh, Singapore, Beijing. Central-bank researchers in São Paulo, Mumbai, Frankfurt. Journalists in every G20 capital.

If OPENGEM ships English-only forever, we cede those markets to whatever competitor is willing to ship in their language. If we ship multi-lingual at v1 to chase them, we triple our content-maintenance burden before we've established product-market fit in our native English market. The right answer threads this: **English at v1; *instrument the codebase for i18n* at v1 so Y2 multilingual is a translation-volume problem, not an engineering project; pick the Y2 languages by where the cohort math says the leverage is, not by perceived prestige.**

Verdict: **English-only at v1, but with `next-intl` integrated, every UI string accessed through `t()`, every URL prefix-able with a locale, every chart title and methodology blurb stored as a translatable record. Y2 launch with five languages chosen by cohort-leverage analysis: Spanish, Portuguese (Brazilian), German, Japanese, Arabic. *Not* Mandarin Chinese at Y2 — the regulatory and audience-overlap calculus is different and warrants its own loop. Translation is via a hybrid: human-translated for evergreen surfaces (methodology, about, pricing, legal), DeepL-pre-translated + native-reviewed for the dashboard chrome, machine-only-with-disclaimer for forecast-narrative pull quotes (because they're auto-generated daily and can't sustain hand-translation cadence).**

---

## Why English-only at v1

Three reasons:

1. **Product-market-fit isn't proven yet in our native market.** Translating before PMF is the most common pre-revenue trap. Every translation locks in a UI pattern that may be wrong. Every translation is a recurring maintenance cost (every UI change becomes N copy changes). Get the English app right first.

2. **The volume cohort is concentrated in English at v1.** The Damian and Greg-class top-200 macro creators / bloggers are predominantly English-publishing (even when not US-based). The volume-cohort flywheel will be cheaper to spin up in English than in Spanish-first or Portuguese-first.

3. **The credibility cohort uses English as a working language.** Macro researchers everywhere read English-language papers. The Marcus-class think-tank analyst in Mumbai or Frankfurt or São Paulo reads English macroeconomics fluently. They will not feel excluded by an English v1 the way a retail prosumer would.

The cohort that *would* be excluded by English-only is the *retail prosumer in non-English markets* — the YouTube viewer in Brazil watching Damian-class content in Portuguese, not the Damian-class creator themselves. That cohort is real and material, and we get to them at Y2. They're not in the v1 ICP.

---

## What to instrument now (the i18n discipline at v1)

Even shipping English-only, every UI string and every page-template field must already flow through the i18n system. Otherwise, Y2 translation is a 3-month grep-and-replace project. With discipline, Y2 is a 2-week translator-coordination project.

The discipline:

### Rule 1 — No bare string literals in JSX

```tsx
// WRONG — bare string literal
<button>Search forecasts</button>

// RIGHT — through i18n
<button>{t("commands.search_forecasts")}</button>
```

A lint rule (`@formatjs/eslint-plugin`) errors on bare JSX text content in any file under `app/`, `components/`. The lint exception: explicit-numeric content (page numbers, mono-formatted code blocks).

### Rule 2 — All string keys are flat namespace, dot-separated, stable

```json
// locales/en/common.json
{
  "nav.home": "Home",
  "nav.countries": "Countries",
  "commands.search_forecasts": "Search forecasts",
  "errors.rate_limit_exceeded": "Daily request limit reached. Upgrade for more.",
  "page.country.headline": "{country} — macro snapshot, vintage {vintage}"
}
```

The flat namespace avoids the "where do I put this key" debate. Dot-separation gives semantic grouping for the translator. Variable interpolation is `{var}` (ICU MessageFormat compatible).

### Rule 3 — Methodology / about / pricing / legal copy lives in MDX with frontmatter for `locale`

```mdx
---
slug: cf-nowcast-v3
locale: en
last_updated: 2026-04-15
authors: ["edgardo"]
---

# CF Nowcast v3.1

The Cleveland Fed-style nowcast adapted ...
```

Y2 adds a `locale: es` counterpart file. The route handler picks the right MDX based on the URL prefix.

### Rule 4 — URL convention supports locale prefix

```
opengem.org/c/USA/cpi_yoy        → English (no prefix at v1)
opengem.org/es/c/USA/cpi_yoy     → Spanish (Y2)
opengem.org/pt-BR/c/USA/cpi_yoy  → Brazilian Portuguese (Y2)
```

We *do not* ship `/en/...` prefixed URLs at v1 because they break existing SEO and embed URLs. The English URL stays prefix-free; new languages get prefixes.

### Rule 5 — Charts emit translatable titles + axis labels

```tsx
<LineChart
  title={t("charts.forecast_band.title", { country, indicator })}
  xAxisLabel={t("charts.time_axis")}
  yAxisLabel={t("charts.indicator.cpi_yoy.axis")}
/>
```

Per-indicator-axis labels are namespaced: `charts.indicator.cpi_yoy.axis` = "CPI YoY (%)". This file becomes the master indicator-name translation dictionary at Y2.

### Rule 6 — Numbers and dates use Intl

```tsx
const fmt = new Intl.NumberFormat(locale, { maximumFractionDigits: 2 });
const dateFmt = new Intl.DateTimeFormat(locale, { dateStyle: "medium" });
```

Brazilian Portuguese formats `3.2` as `3,2` and dates as `15 de junho de 2026`. The `Intl` API handles all of this without our code knowing. At v1 in English, `Intl` is still the right primitive.

### Rule 7 — `next-intl` for the React side, `babel-fish` (or equivalent) for the FastAPI side

Two i18n systems — one per stack — that share the same JSON locale files via a build step. The FastAPI side uses i18n primarily for: alert email bodies, error messages, MCP tool descriptions, RSS feed item titles.

---

## The Y2 language pick (by cohort math)

The five Y2 languages are chosen by *cohort-leverage* — which language unlocks the largest incremental cohort whose buying decision is shaped by language?

- **Spanish (es)**: ~500M speakers, *huge* macro-YouTuber ecosystem in Spain + Latin America, sovereign-fund-LP coverage in Mexico + Chile, central-bank coverage in Argentina + Colombia. The single biggest cohort-leverage unlock.
- **Portuguese (Brazilian, pt-BR)**: Brazil alone is the world's 8th-largest economy and a top-5 macro-watching market by volume. Distinct from Portugal-Portuguese for cultural and economic reasons.
- **German (de)**: not the largest cohort but the *highest-margin* — Bundesbank, the ECB Frankfurt, German sovereign funds, German Newsroom-tier publications (Handelsblatt, FAZ, Süddeutsche). Lots of Institutional-tier money.
- **Japanese (ja)**: BOJ + GPIF + Japanese hedge-fund analyst cohort. High-margin, low-noise; the Japanese macro community is small but engaged.
- **Arabic (ar)**: Gulf sovereign funds + Middle Eastern Newsroom-tier publications. The Arabic language carries the geopolitical-substack audience as well — Lebanon, Jordan, Egypt analyst cohorts.

We do *not* ship Mandarin Chinese (zh-CN) at Y2:

- Cohort overlap with the existing English-reading audience in China is higher than people assume.
- Regulatory exposure: any product showing geopolitical-risk metrics for China + neighbors could attract attention. Better to handle Mandarin in a dedicated loop with sovereign-policy review.
- Translation quality and ongoing maintenance for Mandarin is structurally more expensive (technical macro vocabulary that doesn't directly map).

**Mandarin: Y3 decision, separate loop.**

Hindi, French, Russian, Korean: all reasonable Y2.5/Y3 candidates. We pick five at Y2 because translation volume scales with language count and we can't sustain >5 cleanly.

---

## What we do not translate, ever

- **Vintage IDs and ISO dates**: always ISO-8601, always UTC, no localized formats. Vintage is the brand promise; localizing it breaks reproducibility.
- **Country codes**: ISO-3 (USA, BRA, IND) everywhere. Localized country *names* appear in chart legends; the *codes* in URLs and APIs are universal.
- **Indicator slugs**: `cpi_yoy`, `gdp_yoy` are universal. Only the *display* names are translated.
- **Methodology model names**: "Bauer-Mertens 2018" is a proper noun, not translated.
- **Cite-this-view payload**: the citation string itself is in the locale, but the underlying identifier (`opengem:USA/cpi_yoy/2026-06-06`) is universal.

The discipline: the *identifier layer* is universal; the *presentation layer* is translated. This mirrors the L154 URL convention.

---

## Translation production at Y2

The hybrid pipeline:

- **Evergreen surfaces** (methodology, about, pricing, legal, terms, privacy): native-speaker translation by a professional service ($0.12-0.18/word). Reviewed by a domain expert (macro economist) for each language. ~30k words total at Y2 launch. One-time cost ~$5-8k per language.
- **Dashboard chrome** (UI strings, command catalog, navigation): DeepL Pro pre-translation, then native-reviewed and edited. ~3k strings. Recurring cost ~$200/month for DeepL Pro + ~$1k/quarter per language for review.
- **Forecast narrative pull-quotes** (L198 pipeline output): DeepL machine translation, displayed with a small disclaimer "Translated automatically; original English version is canonical." Updated daily; no human review possible at that cadence.

The disclaimer is critical: it makes the auto-translated content honest. The brand stays "every word is named and dated" even when the word is a translation.

---

## Translation review workflow

Translators get access to a `/translate` dashboard backed by Crowdin-style platform (Tolgee, since it's open-source and good in 2026). Strings are presented in context (the actual UI rendered in the source language, with the translation field beside it). Reviewers see diff-vs-existing-translation for updates.

The workflow integrates with CI: a PR that adds a new English string also adds a placeholder for every locale; the placeholder fails CI until a translator fills it in. Or — for "merge now, translate later" — the placeholder shows the English string with a `[en]` marker visible at runtime so we know what's still untranslated.

---

## Next-step: the next-intl scaffold

```typescript
// app/[[...locale]]/layout.tsx
import { NextIntlClientProvider } from "next-intl";
import { getMessages } from "next-intl/server";

const SUPPORTED_LOCALES = ["en"] as const;          // v1
// Y2: ["en", "es", "pt-BR", "de", "ja", "ar"]

export default async function LocaleLayout({
  children,
  params: { locale = "en" },
}: { children: React.ReactNode; params: { locale?: string } }) {
  if (!SUPPORTED_LOCALES.includes(locale as any)) {
    return notFound();
  }
  const messages = await getMessages({ locale });
  return (
    <html lang={locale} dir={locale === "ar" ? "rtl" : "ltr"}>
      <body>
        <NextIntlClientProvider locale={locale} messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
```

```json
// locales/en/common.json — the v1 starting file (~600 strings)
{
  "nav.home": "Home",
  "nav.countries": "Countries",
  "nav.indicators": "Indicators",
  "page.country.headline": "{country} — macro snapshot, vintage {vintage}",
  "charts.indicator.cpi_yoy.axis": "CPI YoY (%)",
  "errors.rate_limit_exceeded": "Daily request limit reached. Upgrade for more.",
  "...": "..."
}
```

---

## What this loop produced

- A reasoned v1 English-only stance.
- Seven discipline rules to instrument i18n at v1 without translating.
- A Y2 language pick: Spanish, Portuguese (BR), German, Japanese, Arabic. Mandarin deferred.
- A what-we-never-translate identifier-layer / presentation-layer split.
- A hybrid Y2 translation production pipeline (native / DeepL+review / DeepL-only with disclaimer).
- A next-intl scaffold ready for v1 wiring.

## What comes next

- **L154** — URL convention loop supports locale prefix.
- **L198** — narrative pipeline accepts a locale parameter (Y2).
- **Y2 loop TBD** — Mandarin-specific decision.

## Related

- [[L154-url-convention]] — locale prefix slot
- [[L198-narrative-pipeline]] — pull-quote translation pipeline
- [[L001-vision-statement]] — three-cohort thesis driving language pick
- [[L007-distribution-thesis]] — channels per language unlock distinct cohorts
- [[L107-json-ld-schema-org-seo]] — hreflang tags emitted at Y2
