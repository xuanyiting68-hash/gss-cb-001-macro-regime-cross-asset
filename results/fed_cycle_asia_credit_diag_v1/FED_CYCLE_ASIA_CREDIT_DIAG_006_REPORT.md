# FED-CYCLE-ASIA-CREDIT-DIAG-006 — Report

**DESCRIPTIVE LIMITED-SUPPORT DIAGNOSTICS / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

## QC

- QC gate: PASS
- Asia markets acquired: 4
- Yahoo acquisition failures: 0
- common 12-complete-month phase window;
- event month omitted;
- no p-value/FDR family is run.

## Asia equity phase summaries

| market             | anchor      |   n_legs |   n_broad_episodes | support_status      |   weighted_median_ret_3m |   weighted_median_ret_6m |   weighted_median_ret_12m |   weighted_median_mdd_12m |   weighted_median_mdd_trough_month |   weighted_late_trough_share_7_12 |
|:-------------------|:------------|---------:|-------------------:|:--------------------|-------------------------:|-------------------------:|--------------------------:|--------------------------:|-----------------------------------:|----------------------------------:|
| HANG_SENG          | FIRST_CUT   |        8 |                  6 | ADEQUATE_DIAGNOSTIC |               0.0596083  |               0.0107464  |               -0.0866544  |                 0.156189  |                                  8 |                          0.833333 |
| HANG_SENG          | FIRST_HIKE  |        8 |                  6 | ADEQUATE_DIAGNOSTIC |              -0.0981664  |              -0.0827698  |               -0.0124334  |                 0.160677  |                                  7 |                          0.722222 |
| HANG_SENG          | LAST_HIKE   |        8 |                  6 | ADEQUATE_DIAGNOSTIC |               0.086112   |              -0.0556515  |               -0.031075   |                 0.130341  |                                  7 |                          0.555556 |
| HANG_SENG          | PAUSE_START |        6 |                  6 | ADEQUATE_DIAGNOSTIC |               0.109988   |               0.0236975  |               -0.026045   |                 0.130341  |                                  7 |                          0.666667 |
| KOSPI              | FIRST_CUT   |        4 |                  4 | ADEQUATE_DIAGNOSTIC |              -0.0187885  |              -0.0234213  |                0.0430558  |                 0.164009  |                                  8 |                          0.75     |
| KOSPI              | FIRST_HIKE  |        4 |                  4 | ADEQUATE_DIAGNOSTIC |              -0.0150879  |              -0.0148254  |                0.00741771 |                 0.0660002 |                                  1 |                          0.5      |
| KOSPI              | LAST_HIKE   |        4 |                  4 | ADEQUATE_DIAGNOSTIC |              -0.0761806  |              -0.0309072  |                0.0305665  |                 0.0798076 |                                  3 |                          0.5      |
| KOSPI              | PAUSE_START |        4 |                  4 | ADEQUATE_DIAGNOSTIC |              -0.00328281 |               0.00451713 |                0.0123232  |                 0.0767364 |                                  7 |                          0.75     |
| NIKKEI_225         | FIRST_CUT   |       10 |                  7 | ADEQUATE_DIAGNOSTIC |               0.0417929  |               0.105266   |                0.0959827  |                 0.126088  |                                  8 |                          0.904762 |
| NIKKEI_225         | FIRST_HIKE  |       10 |                  7 | ADEQUATE_DIAGNOSTIC |               0.0216497  |               0.0556116  |                0.0281164  |                 0.105943  |                                 10 |                          0.738095 |
| NIKKEI_225         | LAST_HIKE   |       10 |                  7 | ADEQUATE_DIAGNOSTIC |              -0.0251726  |               0.0161916  |                0.0895512  |                 0.0719684 |                                  4 |                          0.333333 |
| NIKKEI_225         | PAUSE_START |        7 |                  7 | ADEQUATE_DIAGNOSTIC |               0.0295524  |               0.105266   |                0.130597   |                 0.0836972 |                                  9 |                          0.714286 |
| SHANGHAI_COMPOSITE | FIRST_CUT   |        4 |                  4 | ADEQUATE_DIAGNOSTIC |               0.0335419  |               0.0351959  |               -0.287332   |                 0.0859278 |                                  9 |                          0.75     |
| SHANGHAI_COMPOSITE | FIRST_HIKE  |        4 |                  4 | ADEQUATE_DIAGNOSTIC |              -0.120641   |              -0.162775   |               -0.113824   |                 0.131673  |                                  6 |                          0.5      |
| SHANGHAI_COMPOSITE | LAST_HIKE   |        4 |                  4 | ADEQUATE_DIAGNOSTIC |               0.0602485  |               0.111214   |                0.125834   |                 0.0639243 |                                  6 |                          0.5      |
| SHANGHAI_COMPOSITE | PAUSE_START |        4 |                  4 | ADEQUATE_DIAGNOSTIC |               0.0757381  |               0.144974   |                0.196197   |                 0.0639243 |                                  8 |                          1        |

## US high-yield OAS phase summary

| observable        | anchor    |   n_legs |   n_broad_episodes | support_status       |   weighted_median_change_3m_bp |   weighted_median_change_6m_bp |   weighted_median_change_12m_bp |   weighted_median_max_widening_bp |   weighted_median_peak_month |
|:------------------|:----------|---------:|-------------------:|:---------------------|-------------------------------:|-------------------------------:|--------------------------------:|----------------------------------:|-----------------------------:|
| US_HIGH_YIELD_OAS | FIRST_CUT |        1 |                  1 | INSUFFICIENT_SUPPORT |                       -61.0849 |                       -19.4658 |                        -57.7905 |                           66.8675 |                            7 |

## Acquisition failures

None.

## Evidence boundary

- China/Asia results are descriptive Fed-cycle path diagnostics only.
- Existing P0-C China identification quarantine remains unchanged.
- High-yield OAS is a stress observable, not a causal mediator estimate.
- Support labels are diagnostic coverage labels, not significance labels.
- No OOS/deployment claim.