# FED-CYCLE-STATE-PANEL-002 — Within-Cycle Continuous-State Report

**ASSOCIATIONAL / DEPENDENCE-AWARE / NOT CAUSAL / NOT A FORECASTING MODEL / NOT DEPLOYABLE**

## Panel

- Monthly panel rows: 165
- Mechanical cycles: 10
- Broad episode clusters: 7
- Active window: first full month after FIRST_HIKE through month before FIRST_CUT, capped at 36 months.
- Cycle fixed effects: yes.
- Equal mechanical-cycle total regression weight: yes.
- Primary inference: exact broad-episode cluster sign-flip.

## Broad episode registry

| broad_episode_id   |   n_mechanical_legs | mechanical_cycle_ids       | first_hike_min      | first_hike_max      | cycle_start_years   |
|:-------------------|--------------------:|:---------------------------|:--------------------|:--------------------|:--------------------|
| B01                |                   2 | T01_1983;T02_1984          | 1983-03-31 00:00:00 | 1984-03-29 00:00:00 | 1983;1984           |
| B02                |                   3 | T03_1987;T04_1987;T05_1988 | 1987-01-05 00:00:00 | 1988-03-30 00:00:00 | 1987;1987;1988      |
| B03                |                   1 | T06_1994                   | 1994-02-04 00:00:00 | 1994-02-04 00:00:00 | 1994                |
| B04                |                   1 | T07_1999                   | 1999-06-30 00:00:00 | 1999-06-30 00:00:00 | 1999                |
| B05                |                   1 | T08_2004                   | 2004-06-30 00:00:00 | 2004-06-30 00:00:00 | 2004                |
| B06                |                   1 | T09_2015                   | 2015-12-16 00:00:00 | 2015-12-16 00:00:00 | 2015                |
| B07                |                   1 | T10_2022                   | 2022-03-16 00:00:00 | 2022-03-16 00:00:00 | 2022                |

## Frozen primary family

| predictor    | outcome         |   n_rows |   n_cycles |   n_broad_clusters |   beta_per_1sd_within |   within_predictor_rms_native_units |   p_broad_exact |   p_mechanical_exact | loo_broad_sign_stable   |   loo_broad_computable | status         |   max_cycle_weight_error |   bh_q_10pct_diagnostic |   by_q_10pct | by_fdr10_status   |
|:-------------|:----------------|---------:|-----------:|-------------------:|----------------------:|------------------------------------:|----------------:|---------------------:|:------------------------|-----------------------:|:---------------|-------------------------:|------------------------:|-------------:|:------------------|
| CPI_YOY      | GOLD_FWD_6M_RET |      165 |         10 |                  7 |           -0.0187666  |                          0.00871821 |        0.140625 |             0.169922 | True                    |                      7 | SUPPORTED_TEST |                        0 |                0.416667 |            1 | NO_BY_FDR10       |
| CPI_YOY      | GOLD_FWD_6M_MDD |      165 |         10 |                  7 |            0.005253   |                          0.00871821 |        0.765625 |             0.757812 | False                   |                      7 | SUPPORTED_TEST |                        0 |                0.859375 |            1 | NO_BY_FDR10       |
| CPI_MOMENTUM | GOLD_FWD_6M_RET |      165 |         10 |                  7 |           -0.00657609 |                          0.00672426 |        0.4375   |             0.472656 | True                    |                      7 | SUPPORTED_TEST |                        0 |                0.583333 |            1 | NO_BY_FDR10       |
| CPI_MOMENTUM | GOLD_FWD_6M_MDD |      165 |         10 |                  7 |            0.00129537 |                          0.00672426 |        0.859375 |             0.78125  | False                   |                      7 | SUPPORTED_TEST |                        0 |                0.859375 |            1 | NO_BY_FDR10       |
| INDPRO_YOY   | GOLD_FWD_6M_RET |      165 |         10 |                  7 |           -0.0127457  |                          0.0141961  |        0.125    |             0.111328 | True                    |                      7 | SUPPORTED_TEST |                        0 |                0.416667 |            1 | NO_BY_FDR10       |
| INDPRO_YOY   | GOLD_FWD_6M_MDD |      165 |         10 |                  7 |            0.00347046 |                          0.0141961  |        0.390625 |             0.398438 | True                    |                      7 | SUPPORTED_TEST |                        0 |                0.583333 |            1 | NO_BY_FDR10       |
| WTI_6M_RET   | GOLD_FWD_6M_RET |      156 |          8 |                  6 |           -0.00719455 |                          0.209074   |        0.4375   |             0.453125 | True                    |                      6 | SUPPORTED_TEST |                        0 |                0.583333 |            1 | NO_BY_FDR10       |
| WTI_6M_RET   | GOLD_FWD_6M_MDD |      156 |          8 |                  6 |            0.00837716 |                          0.209074   |        0.15625  |             0.15625  | True                    |                      6 | SUPPORTED_TEST |                        0 |                0.416667 |            1 | NO_BY_FDR10       |

## BY-FDR 10% survivors

No primary test survives BY-FDR 10%.

## Secondary continuous diagnostics

| predictor          | outcome         |   n_rows |   n_cycles |   n_broad_clusters |   beta_per_1sd_within |   within_predictor_rms_native_units |   p_broad_exact |   p_mechanical_exact | loo_broad_sign_stable   |   loo_broad_computable | status               |   max_cycle_weight_error | multiplicity_status               |
|:-------------------|:----------------|---------:|-----------:|-------------------:|----------------------:|------------------------------------:|----------------:|---------------------:|:------------------------|-----------------------:|:---------------------|-------------------------:|:----------------------------------|
| CURVE_BP           | GOLD_FWD_6M_RET |      163 |          9 |                  7 |          -0.00134349  |                          36.3249    |        0.953125 |            0.886719  | False                   |                      7 | SUPPORTED_TEST       |                        0 | SECONDARY_DIAGNOSTIC_NO_FDR_CLAIM |
| CURVE_BP           | GOLD_FWD_6M_MDD |      163 |          9 |                  7 |           0.00237464  |                          36.3249    |        0.484375 |            0.484375  | True                    |                      7 | SUPPORTED_TEST       |                        0 | SECONDARY_DIAGNOSTIC_NO_FDR_CLAIM |
| DGS10_LEVEL        | GOLD_FWD_6M_RET |      165 |         10 |                  7 |           0.00353799  |                           0.430015  |        0.890625 |            0.880859  | False                   |                      7 | SUPPORTED_TEST       |                        0 | SECONDARY_DIAGNOSTIC_NO_FDR_CLAIM |
| DGS10_LEVEL        | GOLD_FWD_6M_MDD |      165 |         10 |                  7 |          -0.00385018  |                           0.430015  |        0.65625  |            0.640625  | False                   |                      7 | SUPPORTED_TEST       |                        0 | SECONDARY_DIAGNOSTIC_NO_FDR_CLAIM |
| REAL_RATE_PROXY_PP | GOLD_FWD_6M_RET |      165 |         10 |                  7 |           0.0180413   |                           0.991203  |        0.265625 |            0.275391  | True                    |                      7 | SUPPORTED_TEST       |                        0 | SECONDARY_DIAGNOSTIC_NO_FDR_CLAIM |
| REAL_RATE_PROXY_PP | GOLD_FWD_6M_MDD |      165 |         10 |                  7 |          -0.00629066  |                           0.991203  |        0.875    |            0.851562  | False                   |                      7 | SUPPORTED_TEST       |                        0 | SECONDARY_DIAGNOSTIC_NO_FDR_CLAIM |
| NFCI               | GOLD_FWD_6M_RET |      165 |         10 |                  7 |          -0.00673306  |                           0.228797  |        0.59375  |            0.734375  | False                   |                      7 | SUPPORTED_TEST       |                        0 | SECONDARY_DIAGNOSTIC_NO_FDR_CLAIM |
| NFCI               | GOLD_FWD_6M_MDD |      165 |         10 |                  7 |          -4.31027e-05 |                           0.228797  |        0.984375 |            0.976562  | False                   |                      7 | SUPPORTED_TEST       |                        0 | SECONDARY_DIAGNOSTIC_NO_FDR_CLAIM |
| USD_6M_RET         | GOLD_FWD_6M_RET |      165 |         10 |                  7 |           0.0182619   |                           0.0327629 |        0.03125  |            0.0136719 | True                    |                      7 | SUPPORTED_TEST       |                        0 | SECONDARY_DIAGNOSTIC_NO_FDR_CLAIM |
| USD_6M_RET         | GOLD_FWD_6M_MDD |      165 |         10 |                  7 |          -0.00470617  |                           0.0327629 |        0.171875 |            0.171875  | True                    |                      7 | SUPPORTED_TEST       |                        0 | SECONDARY_DIAGNOSTIC_NO_FDR_CLAIM |
| DFII10             | GOLD_FWD_6M_RET |      101 |          3 |                  3 |           0.0399595   |                           0.481409  |      nan        |          nan         | False                   |                      0 | INSUFFICIENT_SUPPORT |                        0 | SECONDARY_DIAGNOSTIC_NO_FDR_CLAIM |
| DFII10             | GOLD_FWD_6M_MDD |      101 |          3 |                  3 |          -0.0171042   |                           0.481409  |      nan        |          nan         | False                   |                      0 | INSUFFICIENT_SUPPORT |                        0 | SECONDARY_DIAGNOSTIC_NO_FDR_CLAIM |

## Interpretation boundary

- Current-vintage CPI/INDPRO/NFCI histories are not strict ALFRED PIT vintages.
- Exact sign-flip inference preserves whole broad episode blocks; rows are not treated as IID.
- BY-FDR is the public primary multiplicity rule; BH is shown only as a diagnostic.
- A surviving association would still not identify a causal Gold driver.
- OOS: not applicable; this is not a forecasting model.
- Deployment: none.