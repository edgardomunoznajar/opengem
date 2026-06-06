/**
 * JSON-LD / schema.org metadata generators.
 *
 * OPENGEM's editorial discipline says: every page is machine-discoverable.
 * Google + Bing + LLM indexers + future AI agents all read schema.org JSON-LD;
 * publishing it cheaply lifts our discoverability ceiling.
 *
 * Per L107 deep-dive (JSON-LD + schema.org for SEO).
 */

import type { Forecast, Scenario, SituationTile } from "@/types/forecast";

const ORG = {
  "@type": "Organization",
  name: "OPENGEM",
  url: "https://opengem.org",
  logo: "https://opengem.org/logo.png",
  sameAs: [
    "https://github.com/opengem",
  ],
};

const DATASET_BASE = {
  "@context": "https://schema.org",
  "@type": "Dataset",
  publisher: ORG,
  license: "https://creativecommons.org/licenses/by/4.0/",
  isAccessibleForFree: true,
  creator: ORG,
  funder: ORG,
};

export function countryDatasetJsonLd(iso3: string, countryName: string) {
  return {
    ...DATASET_BASE,
    name: `${countryName} — macro forecasts (OPENGEM)`,
    description: `OPENGEM forecasts and situation indicators for ${countryName} (${iso3}). Vintage-correct, scored, machine-readable.`,
    url: `https://opengem.org/countries/${iso3}`,
    keywords: [iso3, countryName, "macro forecast", "GDP", "CPI", "OPENGEM"],
    spatialCoverage: {
      "@type": "Place",
      addressCountry: iso3,
      name: countryName,
    },
    distribution: [
      {
        "@type": "DataDownload",
        encodingFormat: "application/json",
        contentUrl: `https://opengem.org/api/countries/${iso3}.json`,
      },
      {
        "@type": "DataDownload",
        encodingFormat: "text/csv",
        contentUrl: `https://opengem.org/api/countries/${iso3}.csv`,
      },
    ],
  };
}

export function indicatorDatasetJsonLd(indicatorId: string, label: string) {
  return {
    ...DATASET_BASE,
    name: `${label} — cross-country forecasts (OPENGEM)`,
    description: `OPENGEM cross-country forecasts for ${label}. Vintage-correct, side-by-side with WEO and OECD EO consensus.`,
    url: `https://opengem.org/indicators/${indicatorId}`,
    keywords: [label, indicatorId, "cross-country", "macro forecast", "OPENGEM"],
    distribution: [
      {
        "@type": "DataDownload",
        encodingFormat: "application/json",
        contentUrl: `https://opengem.org/api/indicators/${indicatorId}.json`,
      },
    ],
  };
}

export function forecastObservationJsonLd(f: Forecast) {
  return {
    "@context": "https://schema.org",
    "@type": "Observation",
    name: `${f.country} ${f.indicator} forecast at horizon ${f.horizon}`,
    observationDate: f.scoring_period,
    measuredProperty: {
      "@type": "PropertyValue",
      name: f.indicator,
      unitText: "percent",
      value: f.point,
      minValue: f.bands.p10,
      maxValue: f.bands.p90,
    },
    publisher: ORG,
    license: "https://creativecommons.org/licenses/by/4.0/",
    sameAs: f.model_card_url,
  };
}

export function scenarioNewsArticleJsonLd(s: Scenario) {
  return {
    "@context": "https://schema.org",
    "@type": "AnalysisNewsArticle",
    headline: s.name,
    articleBody: s.description,
    articleSection: "Forecast",
    datePublished: s.triggered_at,
    author: ORG,
    publisher: ORG,
    inLanguage: "en",
    mentions: s.affected_countries.map((c) => ({
      "@type": "Place",
      addressCountry: c,
    })),
  };
}

export function reportJsonLd(name: string, description: string, url: string) {
  return {
    "@context": "https://schema.org",
    "@type": "Report",
    name,
    description,
    url,
    publisher: ORG,
    author: ORG,
    license: "https://creativecommons.org/licenses/by/4.0/",
  };
}

export function organizationJsonLd() {
  return {
    "@context": "https://schema.org",
    ...ORG,
    description:
      "Open-source world dashboard for macro + geopolitics. Every forecast vintaged. Every miss named.",
    foundingDate: "2026",
    knowsAbout: [
      "Macroeconomic forecasting",
      "Geopolitical risk",
      "Recession probability",
      "Open data",
      "Scenario analysis",
    ],
  };
}

/**
 * Helper to emit a <script type="application/ld+json"> tag from a page's server component.
 *
 * Usage:
 *   <JsonLd data={countryDatasetJsonLd("USA", "United States")} />
 */
export function jsonLdScript(data: unknown): string {
  return JSON.stringify(data, null, 0);
}
