# ENERGY-WEEKLY-STATE-004 — Strict-PIT Weekly Mechanism Test

**INDEPENDENT WEEKLY STRICT-PIT / ASSOCIATIONAL / NOT CAUSAL / NOT DEPLOYABLE**

- QC: **PASS**
- release-state rows: 1288
- raw price-rollover rows: 44
- de-clustered selected events: 17
- mechanism counts: {'TIGHT_OR_MIXED': 11, 'DEMAND_DESTRUCTION': 4, 'DATA_INCOMPLETE': 1, 'SUPPLY_NORMALIZATION': 1}
- supported frozen primary tests: 0/4
- BH-FDR 10% survivors: 0/4

## Frozen primary family

| metric        | kind   |   n_supply_normalization |   n_tight_or_mixed | status               |   median_supply_normalization |   median_tight_or_mixed |   median_difference_sn_minus_mixed |   p_two_sided | permutation_method   | loo_sign_stable   |   bh_q_10pct | bh_fdr_10pct_pass   |
|:--------------|:-------|-------------------------:|-------------------:|:---------------------|------------------------------:|------------------------:|-----------------------------------:|--------------:|:---------------------|:------------------|-------------:|:--------------------|
| wti_fwd_8w    | return |                        1 |                 10 | INSUFFICIENT_SUPPORT |                    -0.0574899 |               0.0707752 |                                nan |           nan |                      | False             |          nan | False               |
| wti_fwd_13w   | return |                        1 |                 10 | INSUFFICIENT_SUPPORT |                    -0.131984  |               0.066982  |                                nan |           nan |                      | False             |          nan | False               |
| short_mae_8w  | mae    |                        1 |                 10 | INSUFFICIENT_SUPPORT |                     0.0221862 |               0.152403  |                                nan |           nan |                      | False             |          nan | False               |
| short_mae_13w | mae    |                        1 |                 10 | INSUFFICIENT_SUPPORT |                     0.0221862 |               0.179187  |                                nan |           nan |                      | False             |          nan | False               |

## Mechanism descriptives

| mechanism_class      | metric        |   n |       mean |     median |   negative_share |
|:---------------------|:--------------|----:|-----------:|-----------:|-----------------:|
| DATA_INCOMPLETE      | wti_fwd_4w    |   1 | -0.0890161 | -0.0890161 |             1    |
| DATA_INCOMPLETE      | wti_fwd_8w    |   1 | -0.022254  | -0.022254  |             1    |
| DATA_INCOMPLETE      | wti_fwd_13w   |   1 |  0.100461  |  0.100461  |             0    |
| DATA_INCOMPLETE      | short_mae_4w  |   1 |  0.0683516 |  0.0683516 |           nan    |
| DATA_INCOMPLETE      | short_mae_8w  |   1 |  0.0866317 |  0.0866317 |           nan    |
| DATA_INCOMPLETE      | short_mae_13w |   1 |  0.160388  |  0.160388  |           nan    |
| DEMAND_DESTRUCTION   | wti_fwd_4w    |   4 |  0.0586318 |  0.0530129 |             0.5  |
| DEMAND_DESTRUCTION   | wti_fwd_8w    |   4 | -0.0257334 | -0.023614  |             0.5  |
| DEMAND_DESTRUCTION   | wti_fwd_13w   |   4 | -0.0804404 | -0.0706966 |             0.75 |
| DEMAND_DESTRUCTION   | short_mae_4w  |   4 |  0.100578  |  0.102002  |           nan    |
| DEMAND_DESTRUCTION   | short_mae_8w  |   4 |  0.1176    |  0.132182  |           nan    |
| DEMAND_DESTRUCTION   | short_mae_13w |   4 |  0.136504  |  0.136046  |           nan    |
| SUPPLY_NORMALIZATION | wti_fwd_4w    |   1 | -0.133765  | -0.133765  |             1    |
| SUPPLY_NORMALIZATION | wti_fwd_8w    |   1 | -0.0574899 | -0.0574899 |             1    |
| SUPPLY_NORMALIZATION | wti_fwd_13w   |   1 | -0.131984  | -0.131984  |             1    |
| SUPPLY_NORMALIZATION | short_mae_4w  |   1 |  0.0221862 |  0.0221862 |           nan    |
| SUPPLY_NORMALIZATION | short_mae_8w  |   1 |  0.0221862 |  0.0221862 |           nan    |
| SUPPLY_NORMALIZATION | short_mae_13w |   1 |  0.0221862 |  0.0221862 |           nan    |
| TIGHT_OR_MIXED       | wti_fwd_4w    |  10 |  0.0502714 |  0.0263129 |             0.4  |
| TIGHT_OR_MIXED       | wti_fwd_8w    |  10 |  0.087137  |  0.0707752 |             0.2  |
| TIGHT_OR_MIXED       | wti_fwd_13w   |  10 |  0.0554579 |  0.066982  |             0.4  |
| TIGHT_OR_MIXED       | short_mae_4w  |  10 |  0.103583  |  0.087106  |           nan    |
| TIGHT_OR_MIXED       | short_mae_8w  |  10 |  0.164646  |  0.152403  |           nan    |
| TIGHT_OR_MIXED       | short_mae_13w |  10 |  0.196303  |  0.179187  |           nan    |

## Era diagnostics

| era          | mechanism_class      |   n |   median_wti_fwd_13w |   median_short_mae_13w |
|:-------------|:---------------------|----:|---------------------:|-----------------------:|
| 2002_2009    | DATA_INCOMPLETE      |   1 |            0.100461  |              0.160388  |
| 2002_2009    | TIGHT_OR_MIXED       |   3 |            0.237475  |              0.237475  |
| 2010_2017    | DEMAND_DESTRUCTION   |   3 |           -0.0180639 |              0.186429  |
| 2010_2017    | TIGHT_OR_MIXED       |   1 |            0.149017  |              0.18211   |
| 2018_PRESENT | DEMAND_DESTRUCTION   |   1 |           -0.123329  |              0.0856622 |
| 2018_PRESENT | SUPPLY_NORMALIZATION |   1 |           -0.131984  |              0.0221862 |
| 2018_PRESENT | TIGHT_OR_MIXED       |   7 |            0.0125961 |              0.16998   |

Interpretation must distinguish supply normalization from demand destruction and mixed/tight states. A null or low-support result is preserved.
