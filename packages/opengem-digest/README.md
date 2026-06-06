# opengem-digest

🧪 alpha — **friend-facing output surface**

Daily digest renderer. Produces a structured JSON document (and a markdown
companion) that the friend (the international-politics YouTuber) reads in 5
minutes, with sections per triggered scenario pack plus situation indicators.

## The friend's workflow

1. Wake up.
2. Open today's digest (markdown or JSON), produced overnight by the system.
3. Skim the headlines + per-pack sections.
4. For any pack of interest, paste the JSON block into ChatGPT with the OPENGEM
   system prompt (see `opengem-narrative`).
5. ChatGPT produces a 3-paragraph video segment grounded in OPENGEM's numbers.

## What's in a digest

```json
{
  "digest_id": "20260525",
  "as_of": "2026-05-25",
  "situation": {
    "recession_probability_us_12m": { "value": 0.18, "model": "bauer_mertens_us_12m" },
    "gpr_global_latest": null,
    "gscpi_latest": null
  },
  "events": [
    { "event_id": "...", "title": "...", "tags": [...], "severity": "HIGH" }
  ],
  "scenarios": [
    {
      "pack_id": "russia-ukraine-energy",
      "title": "Russia-Ukraine energy disruption",
      "summary": "...",
      "invocation": { ... },
      "spec_json": { ... },
      "diff_from_yesterday": "new"  // or "unchanged", "magnitude_changed"
    }
  ],
  "data_sources": [...]
}
```

## Standalone usability

Pure stdlib + the small set of internal-OPENGEM types/scenarios. Anyone wanting
a daily digest renderer for their own scenario engine can install and reuse the
templates.
