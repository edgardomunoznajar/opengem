# opengem-data-bls

🧪 alpha

BLS adapter for OPENGEM. Pulls CPI, unemployment rate, nonfarm payrolls, PPI from the BLS Public Data API v2.

## Requires

- Free registered key from https://www.bls.gov/developers/ (set as `BLS_API_KEY`).
- Without a key, BLS v2 allows up to 3 years per call; with a key, 20 years.

## Series catalog (IOC)

| OPENGEM SeriesId | BLS series_id |
|---|---|
| `US.BLS.CPI.headline_NSA.M` | CUUR0000SA0 |
| `US.BLS.CPI.headline_SA.M` | CUSR0000SA0 |
| `US.BLS.CPI.core_SA.M` | CUSR0000SA0L1E |
| `US.BLS.LNS.unemp_rate.M` | LNS14000000 |
| `US.BLS.CES.nonfarm_payrolls.M` | CES0000000001 |
| `US.BLS.CES.avg_hourly_earnings.M` | CES0500000003 |
| `US.BLS.PPI.final_demand.M` | WPUFD4 |
