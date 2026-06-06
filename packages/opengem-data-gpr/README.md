# opengem-data-gpr

🧪 alpha

Caldara-Iacoviello **Geopolitical Risk Index (GPR)** adapter — global + 44 country-specific
indexes, monthly since 1985.

Per R06 §4, GPR is a primary information-surface input for OPENGEM's
Stratfor-grade scenarios — it's the canonical academic measure of geopolitical
tension and predicts lower investment, stock prices, and employment.

## Series

- `WORLD.GPR.GPR.global.M` — global GPR
- `<country>.GPR.GPR.country.M` — country-specific GPR for 44 countries

## Source

CSV at https://www.matteoiacoviello.com/gpr_files/ (monthly updates)
Replication code on openICPSR.
