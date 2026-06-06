# opengem-scenarios

🧪 alpha — **headline product surface**

OPENGEM's scenario engine. Per the rebaseline conversations, scenarios are the
*headline* product for the validator user — an international-politics YouTuber
whose competitive baseline is "ChatGPT and nothing else."

## What's in it

1. **`ScenarioPack`** — a registered canonical scenario with metadata, default
   identification choices, and pre-curated shock specs. Pack examples:
   - `russia-ukraine-energy` (RU oil/gas shock → EU GDP, US gasoline, global inflation)
   - `china-taiwan-disruption` (CN tech ban → TW GDP, US tech, global supply chain)
   - `iran-israel-escalation` (oil price spike + GPR spike → MEA region, OECD inflation)
   - `fed-plus-100bp` (US policy shock → global spillovers via L2)
   - `opec-supply-cut` (oil shock)
   - `eu-energy-shock` (gas price spike)
   - `us-election-regime` (fiscal-stance shift)
   - `china-stimulus` (PBOC ease)
   - `global-recession-trigger` (composite financial-conditions tightening)
   - `sanctions-on-tech` (export-control regime)

2. **`ScenarioLibrary`** — a typed registry of packs with discovery + filter API.

3. **`ScenarioInvocation`** — the bound-pack-with-execution-parameters object
   that gets handed to the Scenario Subsystem at runtime (or, in IOC, directly
   serialized as the input to L2/L1).

4. **`scenario_to_json` / `scenario_from_json`** — round-tripping the pack
   specs to disk and to the API surface.

## Architectural role

`opengem-scenarios` doesn't *execute* anything — it specifies. The execution
lives in `opengem-l2-bgvar` (spillover IRFs), `opengem-l1-us-core` (structural
identification), and eventually a runtime engine.

This keeps the package small, dependency-light (only `opengem-types`), and
publishable standalone as a *vocabulary* for geopolitical-economic scenarios.

## Standalone usability

`pip install opengem-scenarios` for anyone wanting a curated, typed library of
geopolitical-economic shock specifications. Tons of academic and policy work
needs this kind of structured vocabulary; OPENGEM exposes it openly.
