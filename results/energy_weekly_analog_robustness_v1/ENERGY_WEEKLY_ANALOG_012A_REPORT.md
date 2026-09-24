# ENERGY-WEEKLY-ANALOG-012A — Leave-One-Feature-Out Robustness

**CURRENT OUTCOME UNREALIZED / FROZEN 012 BENCHMARK UNCHANGED**

- original top-1: 2004-11-03
- top-1 preserved: 13/13 (100.0%)
- minimum original-top3 overlap: 2/3
- mean original-top3 overlap: 2.85/3
- features changing top-1: none

## Original top-3 appearance stability

| original_analog   |   top3_appearance_count |   appearance_share |
|:------------------|------------------------:|-------------------:|
| 2004-11-03        |                      13 |           1        |
| 2017-09-13        |                      13 |           1        |
| 2018-05-31        |                      11 |           0.846154 |

## Perturbations

| dropped_feature           | top1       |   top1_distance | top2       |   top2_distance | top3       |   top3_distance |   original_top3_overlap | original_top1_preserved   |
|:--------------------------|:-----------|----------------:|:-----------|----------------:|:-----------|----------------:|------------------------:|:--------------------------|
| WTI_r5                    | 2004-11-03 |        0.789917 | 2017-09-13 |         1.34047 | 2018-05-31 |         1.52733 |                       3 | True                      |
| WTI_r63                   | 2004-11-03 |        0.776132 | 2017-09-13 |         1.43205 | 2018-05-31 |         1.54492 |                       3 | True                      |
| GAS_r5                    | 2004-11-03 |        0.630765 | 2017-09-13 |         1.38809 | 2009-06-24 |         1.53134 |                       2 | True                      |
| GAS_r63                   | 2004-11-03 |        0.723281 | 2017-09-13 |         1.44097 | 2018-05-31 |         1.55275 |                       3 | True                      |
| HEAT_r5                   | 2004-11-03 |        0.73528  | 2017-09-13 |         1.25873 | 2026-04-15 |         1.37426 |                       2 | True                      |
| HEAT_r63                  | 2004-11-03 |        0.804976 | 2017-09-13 |         1.35778 | 2018-05-31 |         1.44629 |                       3 | True                      |
| JET_r5                    | 2004-11-03 |        0.760534 | 2018-05-31 |         1.41763 | 2017-09-13 |         1.45149 |                       3 | True                      |
| JET_r63                   | 2004-11-03 |        0.807565 | 2017-09-13 |         1.43169 | 2018-05-31 |         1.46264 |                       3 | True                      |
| pressure_score            | 2004-11-03 |        0.80753  | 2017-09-13 |         1.41422 | 2018-05-31 |         1.50527 |                       3 | True                      |
| inventory_improving_count | 2004-11-03 |        0.80767  | 2017-09-13 |         1.35993 | 2018-05-31 |         1.4688  |                       3 | True                      |
| demand_weak_count         | 2004-11-03 |        0.80767  | 2017-09-13 |         1.45191 | 2018-05-31 |         1.55435 |                       3 | True                      |
| throughput_weak           | 2004-11-03 |        0.80767  | 2018-05-31 |         1.45035 | 2017-09-13 |         1.45191 |                       3 | True                      |
| upstream_supply_up_count  | 2004-11-03 |        0.80767  | 2017-09-13 |         1.33997 | 2018-05-31 |         1.55435 |                       3 | True                      |

No perturbed run replaces the frozen 012 top-three benchmark.
