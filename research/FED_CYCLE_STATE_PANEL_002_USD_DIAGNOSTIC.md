# FED-CYCLE-STATE-PANEL-002 — Secondary Multiplicity and USD Robustness Audit
Date: 2026-09-24
Status: **POST-RUN DIAGNOSTIC / HYPOTHESIS-GENERATING ONLY**

## Trigger

FED-CYCLE-STATE-PANEL-002 passed all frozen QC gates.

Primary family result:

- 8/8 tests supported;
- 0/8 survive BY-FDR 10%;
- 0/8 survive BH-FDR 10% diagnostic.

Among the predeclared secondary diagnostics, `USD_6M_RET -> GOLD_FWD_6M_RET` has the smallest broad-cluster exact p-value.

Because USD was **not** in the primary family, this observation cannot be promoted to a confirmatory result.

## Audit A — secondary-family multiplicity

The secondary family was predeclared as:

6 predictors × 2 primary Gold outcomes = 12 tests.

For the audit only, apply:

- BH-FDR across all 12 `p_broad_exact` values;
- BY-FDR across all 12 `p_broad_exact` values.

These adjusted values are post-run diagnostics and do not retroactively turn the secondary family into the primary confirmatory family.

## Audit B — USD source/era robustness

Re-estimate the already-defined within-cycle USD association under the same estimator and broad-cluster sign-flip logic for:

1. full sample;
2. excluding the 2022 cycle, leaving only the legacy `TWEXM` source regime;
3. post-1994 cycles only, reducing the early-1980s era contrast;
4. excluding broad episodes B01 and B02, an equivalent conservative later-era restriction.

No USD horizon, lag or scaling rule is changed.

## Interpretation

A stable sign across restrictions may justify retaining USD as a **mechanism candidate**.

It does not establish:

- causality;
- a dominant driver ranking;
- forecasting value;
- trading value.

If the secondary family does not survive multiplicity control, the public evidence status remains **NOT CONFIRMED** even if an unadjusted exact p-value is small.
