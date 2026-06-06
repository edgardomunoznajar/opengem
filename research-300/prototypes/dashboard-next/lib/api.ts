/**
 * Typed client for the OPENGEM public API.
 * In dev, points at the FastAPI service at OPENGEM_API_URL.
 * Falls back to bundled fixtures so the dashboard renders even when offline.
 */

import { Forecast, ForecastSchema, Scenario, ScenarioSchema, SituationTile, SituationTileSchema } from "@/types/forecast";
import fixturesScenarios from "@/data/fixtures.scenarios.json";
import fixturesForecasts from "@/data/fixtures.forecasts.json";
import fixturesSituation from "@/data/fixtures.situation.json";

const BASE = process.env.OPENGEM_API_URL ?? "";

async function fetchJson<T>(path: string, fallback: T): Promise<T> {
  if (!BASE) return fallback;
  try {
    const res = await fetch(`${BASE}${path}`, { next: { revalidate: 60 } });
    if (!res.ok) return fallback;
    return (await res.json()) as T;
  } catch {
    return fallback;
  }
}

export async function getSituation(): Promise<SituationTile[]> {
  const raw = await fetchJson<unknown>("/v1/situation", fixturesSituation);
  return Array.isArray(raw)
    ? (raw as unknown[]).map((r) => SituationTileSchema.parse(r))
    : [];
}

export async function getForecasts(opts?: {
  country?: string;
  indicator?: string;
  horizon?: string;
}): Promise<Forecast[]> {
  const params = new URLSearchParams();
  if (opts?.country) params.set("country", opts.country);
  if (opts?.indicator) params.set("indicator", opts.indicator);
  if (opts?.horizon) params.set("horizon", opts.horizon);
  const q = params.toString() ? `?${params.toString()}` : "";
  const raw = await fetchJson<unknown>(`/v1/forecasts${q}`, fixturesForecasts);
  return Array.isArray(raw)
    ? (raw as unknown[]).map((r) => ForecastSchema.parse(r))
    : [];
}

export async function getScenarios(): Promise<Scenario[]> {
  const raw = await fetchJson<unknown>("/v1/scenarios", fixturesScenarios);
  return Array.isArray(raw)
    ? (raw as unknown[]).map((r) => ScenarioSchema.parse(r))
    : [];
}

export async function getCountry(iso3: string): Promise<{
  iso3: string;
  name: string;
  situation: SituationTile[];
  forecasts: Forecast[];
}> {
  const [situation, forecasts] = await Promise.all([
    getSituation().then((s) => s.filter((x) => !x.country || x.country === iso3)),
    getForecasts({ country: iso3 }),
  ]);
  return {
    iso3,
    name: COUNTRY_NAMES[iso3] ?? iso3,
    situation,
    forecasts,
  };
}

export const COUNTRY_NAMES: Record<string, string> = {
  USA: "United States",
  CHN: "China",
  JPN: "Japan",
  DEU: "Germany",
  GBR: "United Kingdom",
  FRA: "France",
  IND: "India",
  ITA: "Italy",
  BRA: "Brazil",
  CAN: "Canada",
  RUS: "Russia",
  KOR: "South Korea",
  AUS: "Australia",
  MEX: "Mexico",
  ESP: "Spain",
  IDN: "Indonesia",
  NLD: "Netherlands",
  SAU: "Saudi Arabia",
  TUR: "Turkey",
  CHE: "Switzerland",
  POL: "Poland",
  ARG: "Argentina",
  SWE: "Sweden",
  BEL: "Belgium",
  IRL: "Ireland",
  ZAF: "South Africa",
};

export const INDICATORS: Record<string, { label: string; unit: string }> = {
  gdp_yoy: { label: "GDP Growth (YoY)", unit: "%" },
  cpi_yoy: { label: "CPI Inflation (YoY)", unit: "%" },
  unemployment: { label: "Unemployment Rate", unit: "%" },
  policy_rate: { label: "Policy Rate", unit: "%" },
  gpr: { label: "Geopolitical Risk", unit: "idx" },
  gscpi: { label: "Supply Chain Pressure", unit: "σ" },
  recession_prob_12m: { label: "Recession Probability (12m)", unit: "%" },
};
