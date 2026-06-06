/**
 * OPENGEM forecast object contract.
 * Mirrors the L181 design loop spec.
 * Every forecast emitted by the dashboard MUST conform to this shape.
 */

import { z } from "zod";

export const HorizonSchema = z.enum([
  "nowcast",
  "1Q",
  "4Q",
  "2Y",
  "5Y",
]);
export type Horizon = z.infer<typeof HorizonSchema>;

export const BandsSchema = z.object({
  p10: z.number(),
  p50: z.number(),
  p90: z.number(),
});
export type Bands = z.infer<typeof BandsSchema>;

export const ProvenanceSchema = z.object({
  git_sha: z.string(),
  container_digest: z.string().optional(),
  data_lockfile_hash: z.string(),
  generated_at: z.string(), // ISO-8601
});
export type Provenance = z.infer<typeof ProvenanceSchema>;

export const ConsensusOverlaySchema = z.object({
  weo: z.number().optional(),
  oecd_eo: z.number().optional(),
  frb_sep: z.number().optional(),
  ecb_spf: z.number().optional(),
  spf: z.number().optional(),
});
export type ConsensusOverlay = z.infer<typeof ConsensusOverlaySchema>;

export const ForecastSchema = z.object({
  vintage_id: z.string(), // e.g. "2026-06-06-1200Z"
  model_id: z.string(),   // e.g. "opengem-l3-dfm-bma-v0.4"
  model_card_url: z.string().url(),
  country: z.string().length(3), // ISO-3166-1 alpha-3
  indicator: z.string(),         // e.g. "gdp_yoy", "cpi_yoy", "policy_rate"
  horizon: HorizonSchema,
  base_period: z.string(),       // ISO period anchor
  scoring_period: z.string(),    // when this gets evaluated against truth
  point: z.number(),
  bands: BandsSchema,
  consensus_overlay: ConsensusOverlaySchema.optional(),
  provenance: ProvenanceSchema,
  miss_log_url: z.string().url().optional(),
  scoring: z.object({
    pit: z.number().optional(),
    crps: z.number().optional(),
    mae: z.number().optional(),
    rmse: z.number().optional(),
    hit: z.boolean().optional(),
  }).optional(),
  badges: z.array(z.enum([
    "high-coverage",
    "peer-reviewed",
    "replicated",
    "ensemble-of-N",
    "single-source",
    "experimental",
  ])).optional(),
});
export type Forecast = z.infer<typeof ForecastSchema>;

export const ScenarioSchema = z.object({
  slug: z.string(),
  name: z.string(),
  description: z.string(),
  trigger_summary: z.string(),
  probability: z.number().min(0).max(1),
  triggered_at: z.string(),
  affected_countries: z.array(z.string().length(3)),
  affected_indicators: z.array(z.string()),
  methodology_url: z.string().url(),
  narrative_block: z.string().optional(),
});
export type Scenario = z.infer<typeof ScenarioSchema>;

export const SituationTileSchema = z.object({
  kind: z.enum([
    "recession_prob",
    "gpr_nowcast",
    "gscpi",
    "fci",
    "inflation_nowcast",
    "gdp_nowcast",
    "surprise_index",
    "yield_curve",
  ]),
  country: z.string().length(3).optional(), // some are global
  value: z.number(),
  delta: z.number().optional(),
  spark: z.array(z.number()).optional(),
  as_of: z.string(),
  source_url: z.string().url(),
});
export type SituationTile = z.infer<typeof SituationTileSchema>;
