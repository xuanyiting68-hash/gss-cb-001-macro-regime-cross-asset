# FED-CYCLE-STATE-PANEL-002 — USD secondary diagnostic

**POST-RUN / HYPOTHESIS-GENERATING / NOT CAUSAL / NOT DEPLOYABLE**

## Secondary-family multiplicity

- Predeclared secondary tests: 12
- BH-FDR 10% diagnostic survivors: 0
- BY-FDR 10% diagnostic survivors: 0

USD full-sample row with secondary-family adjustments:

| predictor   | outcome         |   n_rows |   n_cycles |   n_broad_clusters |   beta_per_1sd_within |   within_predictor_rms_native_units |   p_broad_exact |   p_mechanical_exact | loo_broad_sign_stable   |   loo_broad_computable | status         |   max_cycle_weight_error | multiplicity_status               |   bh_q_secondary_audit |   by_q_secondary_audit | secondary_bh_fdr10_status   | secondary_by_fdr10_status   |
|:------------|:----------------|---------:|-----------:|-------------------:|----------------------:|------------------------------------:|----------------:|---------------------:|:------------------------|-----------------------:|:---------------|-------------------------:|:----------------------------------|-----------------------:|-----------------------:|:----------------------------|:----------------------------|
| USD_6M_RET  | GOLD_FWD_6M_RET |      165 |         10 |                  7 |             0.0182619 |                           0.0327629 |         0.03125 |            0.0136719 | True                    |                      7 | SUPPORTED_TEST |                        0 | SECONDARY_DIAGNOSTIC_NO_FDR_CLAIM |                  0.375 |                      1 | NO_BH_FDR10                 | NO_BY_FDR10                 |

## USD source/era restrictions

| restriction                    |   n_rows |   n_cycles |   n_broad_clusters |   beta_per_1sd_within |   p_broad_exact |   p_mechanical_exact | status               |
|:-------------------------------|---------:|-----------:|-------------------:|----------------------:|----------------:|---------------------:|:---------------------|
| FULL_SAMPLE                    |      165 |         10 |                  7 |             0.0182619 |         0.03125 |            0.0136719 | SUPPORTED_DIAGNOSTIC |
| EXCLUDE_2022_MODERN_USD_SOURCE |      136 |          9 |                  6 |             0.0205328 |         0.0625  |            0.0234375 | SUPPORTED_DIAGNOSTIC |
| POST_1994_CYCLES_ONLY          |      135 |          5 |                  5 |             0.0238884 |         0.125   |            0.125     | SUPPORTED_DIAGNOSTIC |
| EXCLUDE_EARLY_B01_B02          |      135 |          5 |                  5 |             0.0238884 |         0.125   |            0.125     | SUPPORTED_DIAGNOSTIC |

## Interpretation

- The unadjusted USD exact p-value is a secondary diagnostic and does not survive family-level multiplicity control if the audit reports zero survivors.
- Sign stability across restrictions may retain USD as a mechanism candidate, but cannot establish a driver ranking.
- Within-cycle fixed effects reduce the perfect event-level era separation seen in STATE-001, but they do not create causal identification.
- No forecasting/OOS or deployment claim is made.