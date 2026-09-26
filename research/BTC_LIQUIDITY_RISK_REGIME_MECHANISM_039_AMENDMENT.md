# BTC-LIQUIDITY-RISK-REGIME-MECHANISM-039 — POST-RUN STATE-SUPPORT AMENDMENT

Date: 2026-09-26

## Motivation

The preregistered 039 state contrasts correctly label support within each scope.

The first run shows that a FULL_SAMPLE contrast can meet the >=18-per-state threshold even when one or more fixed eras have little or no variation in one state.

The clearest case is M2:
- FULL_SAMPLE has 124 expanding vs 18 contracting/flat months;
- ERA_1 and ERA_2 each contain zero contracting/flat months;
- ERA_3 contains 38 expanding vs 18 contracting/flat months.

Therefore a separate cross-era state-comparability audit is required before public interpretation.

## Added diagnostic

For each frozen mechanism, compute from the already-generated state contrasts:

- full-sample support status;
- minimum state count in each era;
- number of eras with SUPPORTED_DESCRIPTIVE;
- number with LIMITED_DESCRIPTIVE;
- number with INSUFFICIENT_VARIATION.

Cross-era comparability labels:

- ROBUST_STATE_COMPARABILITY:
  all three eras are SUPPORTED_DESCRIPTIVE.

- PARTIAL_STATE_COMPARABILITY:
  no era is INSUFFICIENT_VARIATION, but at least one is LIMITED_DESCRIPTIVE.

- WEAK_STATE_COMPARABILITY:
  at least one era is INSUFFICIENT_VARIATION.

## Interpretation

This diagnostic does not change correlation estimates, state cutoffs, or support thresholds.

If FULL_SAMPLE is supported but cross-era comparability is WEAK, the full-sample state contrast must not be described as a stable cross-era mechanism.

## Added output

- BTC_STATE_SUPPORT_AUDIT.csv

## Added QC

- uses only preregistered state rows;
- no new cutoff;
- no post-hoc regime;
- no p-value;
- no forecast;
- no causal promotion.
