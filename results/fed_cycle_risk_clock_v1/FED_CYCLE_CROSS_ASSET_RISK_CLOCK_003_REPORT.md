# FED-CYCLE-CROSS-ASSET-RISK-CLOCK-003 — Report

**DESCRIPTIVE TIMING DISTRIBUTION / NOT CAUSAL / NOT A FORECASTING MODEL / NOT DEPLOYABLE**

## QC

- QC gate: PASS
- Primary supported assets: GOLD, NASDAQ, SP500, WTI
- Event month omitted; clock uses months 1-24 after FIRST_HIKE event month.
- Primary aggregation gives each broad episode equal total weight.

## MDD timing summary

| asset   |   n_legs |   n_broad_episodes |   weighted_median_mdd_trough_month |   weighted_q75_mdd_trough_month |   mdd_trough_share_early_1_6 |   mdd_trough_share_mid_7_12 |   mdd_trough_share_late_13_24 |   weighted_median_mdd_24m |   weighted_median_ret_12m |   weighted_median_ret_24m | support_status    |
|:--------|---------:|-------------------:|-----------------------------------:|--------------------------------:|-----------------------------:|----------------------------:|------------------------------:|--------------------------:|--------------------------:|--------------------------:|:------------------|
| GOLD    |       10 |                  7 |                                 12 |                              23 |                     0        |                   0.5       |                      0.5      |                 0.14094   |                 0.0307112 |                 0.0465116 | PRIMARY_SUPPORTED |
| NASDAQ  |       10 |                  7 |                                  7 |                              16 |                     0.404762 |                   0.333333  |                      0.261905 |                 0.12185   |                 0.0650484 |                 0.166747  | PRIMARY_SUPPORTED |
| SP500   |       10 |                  7 |                                 11 |                              21 |                     0.333333 |                   0.190476  |                      0.47619  |                 0.0846855 |                 0.0797901 |                 0.165599  | PRIMARY_SUPPORTED |
| WTI     |        8 |                  6 |                                 15 |                              17 |                     0.333333 |                   0.0555556 |                      0.611111 |                 0.206508  |                 0.224463  |                 0.277585  | PRIMARY_SUPPORTED |

## Recovery summary

| asset     | recovery_level   |   n_legs |   n_broad_episodes |   observed_recoveries |   right_censored |   weighted_km_median_months |
|:----------|:-----------------|---------:|-------------------:|----------------------:|-----------------:|----------------------------:|
| GOLD      | 50%              |       10 |                  7 |                     8 |                2 |                           8 |
| GOLD      | 100%             |       10 |                  7 |                     6 |                4 |                          13 |
| NASDAQ    | 50%              |       10 |                  7 |                     9 |                1 |                           2 |
| NASDAQ    | 100%             |       10 |                  7 |                     9 |                1 |                           8 |
| SP500     | 50%              |       10 |                  7 |                     9 |                1 |                           4 |
| SP500     | 100%             |       10 |                  7 |                     9 |                1 |                           9 |
| USD_BROAD | 50%              |        2 |                  2 |                     2 |                0 |                           3 |
| USD_BROAD | 100%             |        2 |                  2 |                     2 |                0 |                          17 |
| WTI       | 50%              |        8 |                  6 |                     8 |                0 |                           3 |
| WTI       | 100%             |        8 |                  6 |                     7 |                1 |                           8 |

## Evidence boundary

- These are historical timing distributions around realized Fed cycle markers.
- They do not imply that Fed hikes caused the trough timing.
- No p-value/FDR family is run.
- OOS is not applicable; this is not a forecasting model.
- Use as a risk clock, not a deterministic market-timing rule.