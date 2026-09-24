# FED-CYCLE-VINTAGE-AUDIT-007 — Post-Run Robustness Diagnostic
Date: 2026-09-24
Status: **POST-RUN ROBUSTNESS / DOES NOT UPGRADE CONFIRMATORY STATUS**

## Trigger

The frozen real-time IPT audit produced a stronger negative within-cycle association with next-6M Gold return than the current-vintage INDPRO benchmark.

This diagnostic is defined **after observing that result**.

It cannot be used to claim a preregistered new discovery.

## Fixed robustness checks

Using the same real-time IPT construction and same estimator:

1. full sample;
2. exclude the 2022 mechanical cycle;
3. exclude early broad episodes B01 and B02;
4. later sample excluding B01/B02 and 2022.

For each restriction report:

- usable rows;
- cycles;
- broad episodes;
- real-time coefficient and exact broad-cluster p;
- same-row current-vintage coefficient and p;
- sign agreement.

No threshold, horizon or outcome changes.

## Broad-cluster score audit

For the full-sample next-6M Gold return test, report each broad episode's score contribution before sign-flip enumeration.

Purpose:

- determine whether the exact p-value reflects one dominant episode or same-direction cluster contributions.

No cluster is removed based on score magnitude.

## Revision-size audit

Across the 165 monthly rows report:

- Pearson correlation between current-vintage INDPRO YoY and real-time IPT YoY;
- median absolute revision gap;
- 90th percentile absolute revision gap;
- maximum absolute revision gap.

## Interpretation

Allowed:

- revision robustness / fragility statements;
- whether 2022 or early eras dominate.

Not allowed:

- retroactive confirmatory significance;
- forecasting/deployment claims;
- causal language.
