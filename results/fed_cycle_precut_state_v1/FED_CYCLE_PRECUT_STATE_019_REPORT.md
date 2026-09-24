# FED-CYCLE-PRECUT-STATE-019

**PREDETERMINED PRE-CUT STATE DIAGNOSTIC / NO P-VALUES**

- QC: **PASS**
- mechanical cycles: 8
- broad episodes: 6

## Binary pre-cut state contrasts

| state                       | state_value   |   n_cycles |   n_broad_episodes |   weighted_median_risk3_trough_month |   weighted_median_late_trough_share |   weighted_mean_late_trough_share |
|:----------------------------|:--------------|-----------:|-------------------:|-------------------------------------:|------------------------------------:|----------------------------------:|
| REALTIME_GROWTH_CONTRACTION | False         |          8 |                  6 |                                    8 |                            1        |                          0.925926 |
| CURVE_INVERTED              | False         |          4 |                  3 |                                    8 |                            1        |                          0.833333 |
| CURVE_INVERTED              | True          |          4 |                  4 |                                    8 |                            1        |                          1        |
| FINANCIAL_CONDITIONS_TIGHT  | False         |          5 |                  5 |                                    8 |                            1        |                          1        |
| FINANCIAL_CONDITIONS_TIGHT  | True          |          3 |                  1 |                                    5 |                            0.333333 |                          0.555556 |

## Broad-episode rank diagnostics

| predictor            | outcome                   |   n_broad_episodes |   spearman_rho |   loo_min_rho |   loo_max_rho | loo_sign_stable   | pvalue_generated   |
|:---------------------|:--------------------------|-------------------:|---------------:|--------------:|--------------:|:------------------|:-------------------|
| PRE_CUT_STRESS_COUNT | RISK3_MEDIAN_TROUGH_MONTH |                  6 |      -0.635642 |     -0.865181 |     -0.30429  | True              | False              |
| PRE_CUT_STRESS_COUNT | RISK3_LATE_TROUGH_SHARE   |                  6 |      -0.707107 |     -0.790569 |     -0.745356 | False             | False              |

RT_IPT is real-time vintage. Curve/NFCI observations are strictly dated before FIRST_CUT.
This is a small-sample descriptive state diagnostic, not an OOS timing model.
