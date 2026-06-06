# OPENGEM Daily Digest — 2026-05-25

`digest_id: 20260525`

## Situation

| Indicator | Value |
|---|---|
| Recession probability (US, 12m) | 36.7% (us_12m_bauer_mertens_replication) |
| Term spread 10y-3m (bp) | -15.0 |
| Geopolitical Risk (global) | 185.0 (z=+2.10) |
| Global Supply Chain Pressure | +1.40 |
| VIX | 38.0 |

## Events detected

- **[HIGH]** Putin announces escalation in Donbas; gas markets jolt
- **[HIGH]** Taiwan tensions surge as Beijing drills near TSMC
- **[HIGH]** Iran-Israel direct exchange reported; Hormuz risk spikes
- **[HIGH]** term_spread_10y_3m threshold crossed: -15.0 < 0.0
- **[HIGH]** vix threshold crossed: 38.0 > 35.0

## Scenarios (4)

### Russia-Ukraine energy disruption `🆕 NEW`

**Pack:** `russia-ukraine-energy`

Continuation or escalation of Russia-Ukraine conflict produces a sustained shock to European natural gas and global oil prices. Effects: EU GDP down, OECD inflation up, ECB rate path higher.

**Rationale:** Caldara-Iacoviello GPR for RU is a leading indicator; historical oil-price shocks of $20-40/bbl produce -0.3 to -0.8pp Euro Area GDP at 4Q (Hamilton 2003; IEA energy-shock literature). Identification: oil-supply shock + EU gas-import disruption Cholesky-ordered to allow demand-side response.

**Notes:** auto-triggered from RU/UA news

**References:**
- Caldara-Iacoviello (2022) GPR Index
- Hamilton (2003) JoE oil-price shocks
- IEA World Energy Outlook scenario library

**Paste this JSON into ChatGPT with the OPENGEM prompt:**

```json
{
  "scenario_id": "russia-ukraine-energy@2026-05-25",
  "shocks": [
    {
      "country": "RU",
      "variable": "equity_index",
      "magnitude": -15.0,
      "unit": "pct",
      "start_period": "2026-07-01",
      "length_quarters": 2
    },
    {
      "country": "EA",
      "variable": "gdp_deflator",
      "magnitude": 2.0,
      "unit": "pp",
      "start_period": "2026-07-01",
      "length_quarters": 4
    }
  ],
  "shock_type": "structural_shock",
  "identification": "structural",
  "target_countries": [
    "EA",
    "DE",
    "IT",
    "UK",
    "US"
  ],
  "target_variables": [
    "gdp_real",
    "cpi_headline",
    "policy_rate"
  ],
  "target_horizons_q": [
    1,
    4,
    8
  ],
  "metadata": {
    "pack_id": "russia-ukraine-energy",
    "magnitude_scale": "1.0",
    "invoked_at": "2026-05-25",
    "notes": "auto-triggered from RU/UA news"
  }
}
```

### China-Taiwan strategic disruption `🆕 NEW`

**Pack:** `china-taiwan-disruption`

Escalation in the Taiwan Strait (blockade, sanctions, or limited kinetic action) disrupts semiconductor supply chains globally. Effects: US/EU/JP tech sectors contract; global supply chain pressure spikes; CN GDP slows; KR/JP semiconductors directly hit.

**Rationale:** TSMC produces ~90% of leading-edge semiconductors. Sustained disruption maps to GSCPI spike of +2 to +4 sigma (similar to 2021-2022 supply-chain crisis). NY Fed Liberty Street estimates supply-chain stress of this magnitude adds ~1pp to PPI inflation in the US and EA at 4Q.

**Notes:** auto-triggered from Taiwan headlines

**References:**
- NY Fed SR1017 (GSCPI methodology)
- Boehm-Flaaen-Pandalai-Nayar (2019) — Japan tsunami supply-chain effects

**Paste this JSON into ChatGPT with the OPENGEM prompt:**

```json
{
  "scenario_id": "china-taiwan-disruption@2026-05-25",
  "shocks": [
    {
      "country": "CN",
      "variable": "gdp_real",
      "magnitude": -2.0,
      "unit": "pp",
      "start_period": "2026-07-01",
      "length_quarters": 4
    },
    {
      "country": "US",
      "variable": "gdp_deflator",
      "magnitude": 1.0,
      "unit": "pp",
      "start_period": "2026-07-01",
      "length_quarters": 4
    }
  ],
  "shock_type": "structural_shock",
  "identification": "structural",
  "target_countries": [
    "US",
    "JP",
    "KR",
    "DE",
    "EA",
    "CN"
  ],
  "target_variables": [
    "gdp_real",
    "cpi_headline",
    "industrial_production"
  ],
  "target_horizons_q": [
    1,
    4,
    8
  ],
  "metadata": {
    "pack_id": "china-taiwan-disruption",
    "magnitude_scale": "1.0",
    "invoked_at": "2026-05-25",
    "notes": "auto-triggered from Taiwan headlines"
  }
}
```

### Iran-Israel direct escalation `🆕 NEW`

**Pack:** `iran-israel-escalation`

Direct kinetic exchange between Iran and Israel triggers oil-price spike (Hormuz risk premium), regional GPR surge, and global risk-off.

**Rationale:** Strait of Hormuz carries ~20% of global oil. Even partial disruption produces $30-60/bbl oil-price spike based on historical Hormuz episodes (1980s tanker war comparator). GPR spikes 50-150 points (Caldara-Iacoviello).

**Notes:** auto-triggered from Iran-Israel events

**References:**
- Caldara-Iacoviello GPR country-specific series for IR and IL
- Hamilton oil-price shocks literature

**Paste this JSON into ChatGPT with the OPENGEM prompt:**

```json
{
  "scenario_id": "iran-israel-escalation@2026-05-25",
  "shocks": [
    {
      "country": "IL",
      "variable": "gpr",
      "magnitude": 100.0,
      "unit": "level",
      "start_period": "2026-07-01",
      "length_quarters": 2
    },
    {
      "country": "US",
      "variable": "gdp_deflator",
      "magnitude": 1.5,
      "unit": "pp",
      "start_period": "2026-07-01",
      "length_quarters": 2
    }
  ],
  "shock_type": "structural_shock",
  "identification": "narrative",
  "target_countries": [
    "US",
    "EA",
    "UK",
    "JP",
    "IL"
  ],
  "target_variables": [
    "gdp_real",
    "cpi_headline",
    "equity_index"
  ],
  "target_horizons_q": [
    1,
    2,
    4
  ],
  "metadata": {
    "pack_id": "iran-israel-escalation",
    "magnitude_scale": "1.0",
    "invoked_at": "2026-05-25",
    "notes": "auto-triggered from Iran-Israel events"
  }
}
```

### Global recession trigger (financial conditions tightening) `🆕 NEW`

**Pack:** `global-recession-trigger`

Composite financial-conditions tightening + risk-off across DM and EM. Models a 2008-style global recession trigger.

**Rationale:** Gilchrist-Zakrajsek excess bond premium shock literature: +1 sigma EBP shock reduces global IP by 1-2% over 4Q.

**Notes:** auto-triggered from term-spread inversion

**References:**
- Gilchrist-Zakrajsek (2012) AER
- IMF WEO recession chapters

**Paste this JSON into ChatGPT with the OPENGEM prompt:**

```json
{
  "scenario_id": "global-recession-trigger@2026-05-25",
  "shocks": [
    {
      "country": "US",
      "variable": "equity_index",
      "magnitude": -25.0,
      "unit": "pct",
      "start_period": "2026-07-01",
      "length_quarters": 2
    }
  ],
  "shock_type": "structural_shock",
  "identification": "structural",
  "target_countries": [
    "US",
    "EA",
    "JP",
    "UK",
    "BR",
    "IN"
  ],
  "target_variables": [
    "gdp_real",
    "industrial_production",
    "unemployment_rate"
  ],
  "target_horizons_q": [
    1,
    4,
    8
  ],
  "metadata": {
    "pack_id": "global-recession-trigger",
    "magnitude_scale": "1.0",
    "invoked_at": "2026-05-25",
    "notes": "auto-triggered from term-spread inversion"
  }
}
```

---

**Data sources:** BIS CBPOL, FRB H.15, ORDRA, NY Fed GSCPI, Caldara-Iacoviello GPR
