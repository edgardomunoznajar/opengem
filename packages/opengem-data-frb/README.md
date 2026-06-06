# opengem-data-frb

🧪 alpha

Federal Reserve Board adapter — H.15 (rates), G.17 (industrial production / capacity), H.6 (M2).
Uses the DataDownload Program (DDP) CSV endpoints.

## Catalog (IOC)

| OPENGEM SeriesId | FRB DDP series |
|---|---|
| `US.FRB.H15.DGS10.D` | 10-Year Treasury constant maturity rate, daily |
| `US.FRB.H15.DGS2.D`  | 2-Year |
| `US.FRB.H15.DGS3MO.D`| 3-Month |
| `US.FRB.H15.FEDFUNDS.D` | Effective federal funds rate, daily |
| `US.FRB.H15.DFEDTARU.D` | Federal funds target rate (upper bound) |
| `US.FRB.H15.DFEDTARL.D` | Federal funds target rate (lower bound) |
| `US.FRB.G17.INDPRO.M` | Industrial production index, monthly |
| `US.FRB.G17.CAPUTL.M` | Capacity utilization, monthly |
| `US.FRB.H6.M2.M`     | M2 money stock, monthly |
