# opengem-data-treasury

🧪 alpha

US Treasury FiscalData adapter. No auth, generous rate limits. Provides redundancy
for daily yield series (alternative to FRB H.15) and adds federal debt + MTS series.

## Catalog (IOC)

| OPENGEM SeriesId | Treasury endpoint |
|---|---|
| `US.TREAS.YIELDS.10Y.D` | daily_treasury_yield_curve_rates (record_date, avg_interest_rate_amt for 10-Year) |
| `US.TREAS.YIELDS.2Y.D`  | same dataset, 2-Year |
| `US.TREAS.YIELDS.3M.D`  | same dataset, 3-Month |
| `US.TREAS.DEBT.public.D` | debt_to_penny |
