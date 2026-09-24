# FED-CYCLE-PRECUT-STATE-019

**PREDETERMINED PRE-CUT STATE DIAGNOSTIC / NO P-VALUES**

- QC: **PASS**
- mechanical cycles: 8
- broad episodes: 6

## Independent broad-episode binary state support

| state                       |   true_broad_episodes |   false_broad_episodes | support_status                 |
|:----------------------------|----------------------:|-----------------------:|:-------------------------------|
| REALTIME_GROWTH_CONTRACTION |                     0 |                      6 | INSUFFICIENT_STATE_VARIATION   |
| CURVE_INVERTED              |                     3 |                      3 | SUPPORTED_BALANCED_DESCRIPTIVE |
| FINANCIAL_CONDITIONS_TIGHT  |                     1 |                      5 | INSUFFICIENT_STATE_VARIATION   |

## Binary pre-cut state contrasts

| state                       | state_value   |   n_broad_episodes | support_status                 |   median_risk3_trough_month |   median_late_trough_share |   mean_late_trough_share |
|:----------------------------|:--------------|-------------------:|:-------------------------------|----------------------------:|---------------------------:|-------------------------:|
| REALTIME_GROWTH_CONTRACTION | False         |                  6 | INSUFFICIENT_STATE_VARIATION   |                     8       |                   1        |                 0.925926 |
| CURVE_INVERTED              | False         |                  3 | SUPPORTED_BALANCED_DESCRIPTIVE |                     8       |                   1        |                 0.851852 |
| CURVE_INVERTED              | True          |                  3 | SUPPORTED_BALANCED_DESCRIPTIVE |                     8       |                   1        |                 1        |
| FINANCIAL_CONDITIONS_TIGHT  | False         |                  5 | INSUFFICIENT_STATE_VARIATION   |                     8       |                   1        |                 1        |
| FINANCIAL_CONDITIONS_TIGHT  | True          |                  1 | INSUFFICIENT_STATE_VARIATION   |                     4.66667 |                   0.555556 |                 0.555556 |

## Broad-episode rank diagnostics

| predictor            | outcome                   |   n_broad_episodes |   spearman_rho |   loo_min_rho |   loo_max_rho |   loo_defined_count |   loo_total_count | loo_all_defined   | loo_finite_sign_consistent   | pvalue_generated   |
|:---------------------|:--------------------------|-------------------:|---------------:|--------------:|--------------:|--------------------:|------------------:|:------------------|:-----------------------------|:-------------------|
| PRE_CUT_STRESS_COUNT | RISK3_MEDIAN_TROUGH_MONTH |                  6 |      -0.635642 |     -0.865181 |     -0.30429  |                   6 |                 6 | True              | True                         | False              |
| PRE_CUT_STRESS_COUNT | RISK3_LATE_TROUGH_SHARE   |                  6 |      -0.707107 |     -0.790569 |     -0.745356 |                   5 |                 6 | False             | True                         | False              |

## Component sensitivity

| specification   | outcome                   |   spearman_rho | post_run_diagnostic   |
|:----------------|:--------------------------|---------------:|:----------------------|
| FULL_COUNT      | RISK3_MEDIAN_TROUGH_MONTH |      -0.635642 | True                  |
| FULL_COUNT      | RISK3_LATE_TROUGH_SHARE   |      -0.707107 | True                  |
| DROP_GROWTH     | RISK3_MEDIAN_TROUGH_MONTH |      -0.635642 | True                  |
| DROP_GROWTH     | RISK3_LATE_TROUGH_SHARE   |      -0.707107 | True                  |
| DROP_CURVE      | RISK3_MEDIAN_TROUGH_MONTH |      -0.6742   | True                  |
| DROP_CURVE      | RISK3_LATE_TROUGH_SHARE   |      -1        | True                  |
| DROP_NFCI       | RISK3_MEDIAN_TROUGH_MONTH |      -0.127128 | True                  |
| DROP_NFCI       | RISK3_LATE_TROUGH_SHARE   |       0.141421 | True                  |
| CURVE_ONLY      | RISK3_MEDIAN_TROUGH_MONTH |      -0.127128 | True                  |
| CURVE_ONLY      | RISK3_LATE_TROUGH_SHARE   |       0.141421 | True                  |
| NFCI_ONLY       | RISK3_MEDIAN_TROUGH_MONTH |      -0.6742   | True                  |
| NFCI_ONLY       | RISK3_LATE_TROUGH_SHARE   |      -1        | True                  |

RT_IPT is real-time vintage. Curve/NFCI observations are strictly dated before FIRST_CUT.
Binary evidence support is judged at the independent broad-episode level.
This is a small-sample descriptive state diagnostic, not an OOS timing model.
