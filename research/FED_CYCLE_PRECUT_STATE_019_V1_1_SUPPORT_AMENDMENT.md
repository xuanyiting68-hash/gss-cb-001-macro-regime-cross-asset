# FED-CYCLE-PRECUT-STATE-019 v1.1 — Support and Component-Sensitivity Amendment
Date: 2026-09-24
Status: **POST-RUN EVIDENCE AUDIT / NUMERIC OUTCOMES UNCHANGED**

## Trigger

The initial 019 run passed timing/QC, but post-run audit found that binary-state support must be judged at the independent broad-episode level and that the composite PRE_CUT_STRESS_COUNT requires component sensitivity analysis.

## Independent broad-episode classification

For each binary state, first compute the within-broad-episode share of mechanical cycles in the True state.

Classify a broad episode True when the share is >= 0.5, otherwise False.

Evidence labels:
- SUPPORTED_BALANCED_DESCRIPTIVE: at least 3 broad episodes in each state;
- LIMITED_BINARY_DESCRIPTIVE: at least 2 in each state but below supported;
- INSUFFICIENT_STATE_VARIATION: either state has fewer than 2 broad episodes.

This prevents one broad episode from appearing on both sides of a binary contrast.

## Expected support implications

- REALTIME_GROWTH_CONTRACTION: no True broad episodes -> INSUFFICIENT_STATE_VARIATION.
- CURVE_INVERTED: 3 True / 3 False broad episodes -> SUPPORTED_BALANCED_DESCRIPTIVE.
- FINANCIAL_CONDITIONS_TIGHT: 1 True / 5 False -> INSUFFICIENT_STATE_VARIATION.

## Composite sensitivity

Recompute broad-episode Spearman rank diagnostics for:
- full PRE_CUT_STRESS_COUNT;
- drop growth component;
- drop curve component;
- drop NFCI component;
- curve-only share;
- NFCI-only share.

These are post-run diagnostics, not confirmatory tests.

## LOO audit

Replace the single boolean LOO sign-stability field with:
- loo_defined_count;
- loo_total_count;
- loo_all_defined;
- loo_finite_sign_consistent.

A correlation is not called fully LOO-stable if any leave-one-out sample is undefined because one variable becomes constant.

## Boundary

**POST-RUN SUPPORT/SENSITIVITY AUDIT / NO THRESHOLD RETUNING / NO P-VALUES / NOT OOS / NOT CAUSAL / NOT DEPLOYABLE**
