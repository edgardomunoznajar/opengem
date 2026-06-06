# opengem-recession-prob

🧪 alpha — first **Situation Subsystem** endpoint

Term-spread recession probability engine — Bauer-Mertens (FRBSF 2018) style
probit estimation of 12-month-ahead US recession probability from the 10y-3m
Treasury spread. Per R10 / R06, this is the first concrete endpoint of the
Situation Subsystem; per R12, it's a job no incumbent does as cleanly.

## What's in it

- **`TermSpreadModel`** — calibrated probit (or logit) of recession indicator on
  lagged term spread. Fits via simple iteratively-reweighted least squares; no
  scipy dependency required for IOC.
- **`RecessionProbabilityResult`** — typed result record with point probability,
  reliability interval, and provenance.
- **`recession_probability(spread, model)`** — pure function: given a current
  spread (in basis points) and a fitted model, return probability.
- **Pre-baked US model parameters** based on Bauer-Mertens 1972-2018 replication.
  Replaceable with re-fitted parameters at any time.

## Standalone usability

Pure stdlib + `opengem-types`. Anyone wanting a single-call recession-probability
function for any country can `pip install opengem-recession-prob`.

## Limitations

- Bauer-Mertens evidence is US-strongest; for non-US countries, AUC degrades.
  Each country needs its own calibration; this package provides US-fitted
  defaults plus an interface for custom parameters.
- 12-month horizon is the original Bauer-Mertens horizon; the package supports
  arbitrary horizons but only US-12m comes with bundled parameters at IOC.
