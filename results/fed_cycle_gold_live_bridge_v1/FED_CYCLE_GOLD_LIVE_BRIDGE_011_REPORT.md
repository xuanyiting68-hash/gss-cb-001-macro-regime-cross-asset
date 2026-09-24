# FED-CYCLE-GOLD-LIVE-BRIDGE-011 — Report

**DATA-TRANSPORT / MEASUREMENT-EQUIVALENCE AUDIT / NO FORECAST PERFORMANCE EVIDENCE**

- QC: **PASS**
- bridge status: **PROXY_FEATURE_BRIDGE_CANDIDATE**
- common feature-complete months: 306
- overlap: 2001-03 to 2026-08

## Bridge metrics

|   common_feature_complete_months | first_common_month   | last_common_month   |   min_proxy_daily_obs_per_month |   level_median_abs_rel_gap |   level_p95_abs_rel_gap |   ret3_corr |   ret3_median_abs_diff |   ret3_sign_agreement |   ret6_corr |   ret6_median_abs_diff |   ret6_sign_agreement |   vol6_corr |   vol6_median_abs_diff |
|---------------------------------:|:---------------------|:--------------------|--------------------------------:|---------------------------:|------------------------:|------------:|-----------------------:|----------------------:|------------:|-----------------------:|----------------------:|------------:|-----------------------:|
|                              306 | 2001-03              | 2026-08             |                              16 |                  0.0013084 |              0.00710397 |    0.998386 |             0.00189745 |              0.990196 |    0.999394 |             0.00172309 |              0.990196 |    0.992803 |            0.000855202 |

## Frozen engineering gates

| gate                       | pass   |      observed | threshold   |
|:---------------------------|:-------|--------------:|:------------|
| coverage_common_months     | True   | 306           | >=240       |
| level_median_abs_rel_gap   | True   |   0.0013084   | <=0.02      |
| level_p95_abs_rel_gap      | True   |   0.00710397  | <=0.05      |
| ret3_corr                  | True   |   0.998386    | >=0.98      |
| ret3_median_abs_diff       | True   |   0.00189745  | <=0.015     |
| ret3_sign_agreement        | True   |   0.990196    | >=0.95      |
| ret6_corr                  | True   |   0.999394    | >=0.98      |
| ret6_median_abs_diff       | True   |   0.00172309  | <=0.02      |
| ret6_sign_agreement        | True   |   0.990196    | >=0.95      |
| vol6_corr                  | True   |   0.992803    | >=0.9       |
| vol6_median_abs_diff       | True   |   0.000855202 | <=0.006     |
| era_2000_2009_ret3_sign    | True   |   0.981132    | >=0.9       |
| era_2000_2009_ret6_sign    | True   |   0.981132    | >=0.9       |
| era_2010_2019_ret3_sign    | True   |   1           | >=0.9       |
| era_2010_2019_ret6_sign    | True   |   0.991667    | >=0.9       |
| era_2020_PRESENT_ret3_sign | True   |   0.9875      | >=0.9       |
| era_2020_PRESENT_ret6_sign | True   |   1           | >=0.9       |

## Era stability

| era          |   n_months |   ret3_sign_agreement |   ret6_sign_agreement |
|:-------------|-----------:|----------------------:|----------------------:|
| 2000_2009    |        106 |              0.981132 |              0.981132 |
| 2010_2019    |        120 |              1        |              0.991667 |
| 2020_PRESENT |         80 |              0.9875   |              1        |

## Interpretation boundary

- GC=F is a COMEX continuous futures proxy, not spot Gold.
- No mapping/calibration was fitted to improve agreement.
- No Gold forecast target or M3 forecast error was loaded.
- A bridge pass would justify only a separately versioned prospective measurement specification.
- OOS-008 evidence is not automatically inherited.
- Deployment remains prohibited.
