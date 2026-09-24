# FED-CYCLE-PRECUT-STRESS-LEVEL-020

**EXPLORATORY CONTINUOUS PRE-CUT LEVEL DIAGNOSTIC / SIMPLE CONTINUOUS RULE NOT SUPPORTED**

## Full available-sample diagnostics

| sample         | predictor        | outcome                   |   n_broad_episodes | support_status        |   spearman_rho |   loo_defined_count |   loo_total_count | loo_all_defined   | loo_finite_sign_consistent   |   loo_min_rho |   loo_max_rho |   max_abs_loo_change | pvalue_generated   |
|:---------------|:-----------------|:--------------------------|-------------------:|:----------------------|---------------:|--------------------:|------------------:|:------------------|:-----------------------------|--------------:|--------------:|---------------------:|:-------------------|
| FULL_AVAILABLE | BAA_SPREAD_LEVEL | RISK3_MEDIAN_TROUGH_MONTH |                  6 | SUPPORTED_EXPLORATORY |      0.0746352 |                   6 |                 6 | True              | False                        |     -0.263523 |      0.564288 |            0.489653  | False              |
| FULL_AVAILABLE | BAA_SPREAD_LEVEL | RISK3_LATE_TROUGH_SHARE   |                  6 | SUPPORTED_EXPLORATORY |      0.132842  |                   5 |                 6 | False             | False                        |      0        |      0.353553 |            0.220711  | False              |
| FULL_AVAILABLE | VIX_LEVEL        | RISK3_MEDIAN_TROUGH_MONTH |                  5 | LIMITED_EXPLORATORY   |     -0.210819  |                   5 |                 5 | True              | False                        |     -0.632456 |      0.316228 |            0.527046  | False              |
| FULL_AVAILABLE | VIX_LEVEL        | RISK3_LATE_TROUGH_SHARE   |                  5 | LIMITED_EXPLORATORY   |    nan         |                   0 |                 5 | False             | False                        |    nan        |    nan        |          nan         | False              |
| FULL_AVAILABLE | CURVE_STRESS_BP  | RISK3_MEDIAN_TROUGH_MONTH |                  6 | SUPPORTED_EXPLORATORY |      0.0294245 |                   6 |                 6 | True              | False                        |     -0.737865 |      0.316228 |            0.767289  | False              |
| FULL_AVAILABLE | CURVE_STRESS_BP  | RISK3_LATE_TROUGH_SHARE   |                  6 | SUPPORTED_EXPLORATORY |      0.654654  |                   5 |                 6 | False             | True                         |      0.707107 |      0.707107 |            0.0524531 | False              |
| FULL_AVAILABLE | GROWTH_STRESS    | RISK3_MEDIAN_TROUGH_MONTH |                  6 | SUPPORTED_EXPLORATORY |     -0.176547  |                   6 |                 6 | True              | False                        |     -0.564288 |      0.263523 |            0.44007   | False              |
| FULL_AVAILABLE | GROWTH_STRESS    | RISK3_LATE_TROUGH_SHARE   |                  6 | SUPPORTED_EXPLORATORY |     -0.130931  |                   5 |                 6 | False             | False                        |     -0.353553 |      0        |            0.222623  | False              |

## VIX common-sample audit

| sample            | predictor        | outcome                   |   n_broad_episodes | support_status      |   spearman_rho |   loo_defined_count |   loo_total_count | loo_all_defined   | loo_finite_sign_consistent   |   loo_min_rho |   loo_max_rho |   max_abs_loo_change | pvalue_generated   |
|:------------------|:-----------------|:--------------------------|-------------------:|:--------------------|---------------:|--------------------:|------------------:|:------------------|:-----------------------------|--------------:|--------------:|---------------------:|:-------------------|
| VIX_COMMON_SAMPLE | BAA_SPREAD_LEVEL | RISK3_MEDIAN_TROUGH_MONTH |                  5 | LIMITED_EXPLORATORY |     -0.0811107 |                   5 |                 5 | True              | False                        |     -0.894427 |      0.316228 |             0.813316 | False              |
| VIX_COMMON_SAMPLE | BAA_SPREAD_LEVEL | RISK3_LATE_TROUGH_SHARE   |                  5 | LIMITED_EXPLORATORY |    nan         |                   0 |                 5 | False             | False                        |    nan        |    nan        |           nan        | False              |
| VIX_COMMON_SAMPLE | CURVE_STRESS_BP  | RISK3_MEDIAN_TROUGH_MONTH |                  5 | LIMITED_EXPLORATORY |     -0.737865  |                   5 |                 5 | True              | True                         |     -0.948683 |     -0.447214 |             0.290651 | False              |
| VIX_COMMON_SAMPLE | CURVE_STRESS_BP  | RISK3_LATE_TROUGH_SHARE   |                  5 | LIMITED_EXPLORATORY |    nan         |                   0 |                 5 | False             | False                        |    nan        |    nan        |           nan        | False              |
| VIX_COMMON_SAMPLE | GROWTH_STRESS    | RISK3_MEDIAN_TROUGH_MONTH |                  5 | LIMITED_EXPLORATORY |     -0.105409  |                   5 |                 5 | True              | False                        |     -0.316228 |      0.894427 |             0.999836 | False              |
| VIX_COMMON_SAMPLE | GROWTH_STRESS    | RISK3_LATE_TROUGH_SHARE   |                  5 | LIMITED_EXPLORATORY |    nan         |                   0 |                 5 | False             | False                        |    nan        |    nan        |           nan        | False              |

Late-trough share has only two unique full-sample values and is constant in the VIX-supported sample.
No p-values, optimized thresholds, new predictors, composites or fitted multivariate models are generated.

**Boundary: exploratory mechanism-hypothesis only; not causal, not OOS and not deployable.**
