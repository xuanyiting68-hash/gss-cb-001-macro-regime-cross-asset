# FED-CYCLE-STRESS-LAYER-005 — Report

**DESCRIPTIVE STRESS-STATE LAYER / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

## QC

- QC gate: PASS
- primary supported cells: 12
- common 12-complete-month phase window;
- event month omitted;
- broad-episode weighting applied separately inside each observable × phase cell.

## Primary stress summaries

| observable    | anchor      |   n_legs |   n_broad_episodes |   weighted_median_change_3m |   weighted_median_change_6m |   weighted_median_change_12m |   weighted_median_max_stress_move |   weighted_median_stress_peak_month |   weighted_q75_max_stress_move | support_status    | unit_note                                                    |
|:--------------|:------------|---------:|-------------------:|----------------------------:|----------------------------:|-----------------------------:|----------------------------------:|------------------------------------:|-------------------------------:|:------------------|:-------------------------------------------------------------|
| BAA10Y_SPREAD | FIRST_CUT   |       10 |                  7 |                  -2         |                 -5          |                    5         |                        38         |                                   7 |                    108         | PRIMARY_SUPPORTED | basis points; max stress = max credit-spread widening        |
| BAA10Y_SPREAD | FIRST_HIKE  |       10 |                  7 |                   4         |                -27          |                  -21         |                        16         |                                   2 |                     28         | PRIMARY_SUPPORTED | basis points; max stress = max credit-spread widening        |
| BAA10Y_SPREAD | LAST_HIKE   |       10 |                  7 |                   7         |                 15          |                   -4         |                        31         |                                   5 |                     52         | PRIMARY_SUPPORTED | basis points; max stress = max credit-spread widening        |
| BAA10Y_SPREAD | PAUSE_START |        7 |                  7 |                   9         |                 -8          |                   23         |                        31         |                                   9 |                     49         | PRIMARY_SUPPORTED | basis points; max stress = max credit-spread widening        |
| COPPER        | FIRST_CUT   |        5 |                  5 |                  -0.0594487 |                  0.0253278  |                   -0.0700102 |                         0.199568  |                                   9 |                      0.256437  | PRIMARY_SUPPORTED | decimal return/MDD; max stress = 12M copper MDD              |
| COPPER        | FIRST_HIKE  |        5 |                  5 |                   0.0640324 |                  0.150754   |                    0.179263  |                         0.0683591 |                                  10 |                      0.0878285 | PRIMARY_SUPPORTED | decimal return/MDD; max stress = 12M copper MDD              |
| COPPER        | LAST_HIKE   |        5 |                  5 |                  -0.0541677 |                 -0.00538058 |                   -0.0191833 |                         0.150834  |                                  11 |                      0.172856  | PRIMARY_SUPPORTED | decimal return/MDD; max stress = 12M copper MDD              |
| COPPER        | PAUSE_START |        5 |                  5 |                   0.0408409 |                  0.0139263  |                   -0.0293181 |                         0.172856  |                                  11 |                      0.179125  | PRIMARY_SUPPORTED | decimal return/MDD; max stress = 12M copper MDD              |
| VIX           | FIRST_CUT   |        5 |                  5 |                  -0.369478  |                  1.57682    |                    5.21248   |                         8.53483   |                                   8 |                     12.6539    | PRIMARY_SUPPORTED | VIX points; max stress = max increase in monthly-average VIX |
| VIX           | FIRST_HIKE  |        5 |                  5 |                  -0.360909  |                  0.598654   |                   -4.10407   |                         4.25729   |                                   2 |                      5.18058   | PRIMARY_SUPPORTED | VIX points; max stress = max increase in monthly-average VIX |
| VIX           | LAST_HIKE   |        5 |                  5 |                  -2.27005   |                 -0.781353   |                    0.370731  |                         1.33261   |                                   3 |                      2.75871   | PRIMARY_SUPPORTED | VIX points; max stress = max increase in monthly-average VIX |
| VIX           | PAUSE_START |        5 |                  5 |                  -4.50838   |                 -2.06641    |                    1.80942   |                         3.45836   |                                  11 |                      6.29238   | PRIMARY_SUPPORTED | VIX points; max stress = max increase in monthly-average VIX |

## Evidence boundary

- VIX, Baa-10Y spread and copper are observed stress/mechanism variables.
- This module does not test optimized thresholds or forecasting rules.
- Visual alignment with asset drawdowns is not causal identification.
- No p-value/FDR family is run.
- OOS: not applicable.
- Deployment: none.