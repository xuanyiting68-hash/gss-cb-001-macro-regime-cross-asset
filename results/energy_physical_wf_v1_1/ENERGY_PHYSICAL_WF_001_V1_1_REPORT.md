# ENERGY-PHYSICAL-WF-001 v1.1 — First Release-Aware Data-Only Run
Date: 2026-09-24

## Status

**EXPLORATORY / STRICT-PIT DATA-ONLY PHYSICAL LAYER / NOT DEPLOYABLE**

A complete geopolitical/shipping shock veto has not yet been frozen, so even a small p/q-value cannot be upgraded to full P4A confirmation.

## QC

- Frozen price events preserved: True
- Strict PIT available: 12 / 13
- P4A_DATA_ONLY: 3
- PHYSICAL_VETO_DATA_ONLY: 9
- P4B refinery-drop candidates: 0
- QC gate: PASS

## Primary four-test data-only family

| test         |   n_p4a |   n_veto |   p4a_mean |   veto_mean |   p4a_median |   veto_median |   difference_median_p4a_minus_veto |   mann_whitney_p |   bh_q_4test_family |
|:-------------|--------:|---------:|-----------:|------------:|-------------:|--------------:|-----------------------------------:|-----------------:|--------------------:|
| WTI_fwd_3m   |       3 |        8 |   0.133103 |   0.0659261 |     0.160916 |     0.0968312 |                         0.064085   |         0.921212 |                   1 |
| WTI_fwd_6m   |       3 |        8 |   0.147797 |   0.160974  |     0.140683 |     0.244513  |                        -0.10383    |         0.775758 |                   1 |
| short_MAE_3m |       3 |        8 |   0.175499 |   0.228554  |     0.172804 |     0.17587   |                        -0.00306592 |         1        |                   1 |
| short_MAE_6m |       3 |        8 |   0.243433 |   0.333382  |     0.256018 |     0.270237  |                        -0.0142198  |         0.921212 |                   1 |

## Event panel

| s3_date             | price_anchor_month   | price_layer_classification   | strict_pit   | baseline_release_date   | decision_date       |   inventory_improving_count |   refinery_util_baseline |   refinery_util_decision |   refinery_worsening |   refinery_drop_5pp | physical_classification   |   wti_fwd_3m |   wti_fwd_6m |   short_mae_3m |   short_mae_6m |
|:--------------------|:---------------------|:-----------------------------|:-------------|:------------------------|:--------------------|----------------------------:|-------------------------:|-------------------------:|---------------------:|--------------------:|:--------------------------|-------------:|-------------:|---------------:|---------------:|
| 1999-10-01 00:00:00 | 1999-11-01 00:00:00  | FALSE_RELIEF_VETO            | UNAVAILABLE  | NaT                     | NaT                 |                         nan |                    nan   |                    nan   |                  nan |                 nan | STRICT_PIT_UNAVAILABLE    |  nan         |  nan         |    nan         |     nan        |
| 2002-06-01 00:00:00 | 2002-07-01 00:00:00  | FALSE_RELIEF_VETO            | AVAILABLE    | 2002-06-26 00:00:00     | 2002-08-07 00:00:00 |                           1 |                     92.5 |                     91.8 |                    0 |                   0 | PHYSICAL_VETO_DATA_ONLY   |   -0.0458992 |    0.318661  |      0.160647  |       0.318661 |
| 2003-03-01 00:00:00 | 2003-04-01 00:00:00  | PRICE_PRODUCT_CONFIRMED      | AVAILABLE    | 2003-03-26 00:00:00     | 2003-05-07 00:00:00 |                           2 |                     88.5 |                     94.3 |                    0 |                   0 | P4A_DATA_ONLY             |    0.203044  |    0.140683  |      0.203044  |       0.203044 |
| 2004-11-01 00:00:00 | 2004-12-01 00:00:00  | PRICE_PRODUCT_CONFIRMED      | AVAILABLE    | 2004-11-24 00:00:00     | 2005-01-05 00:00:00 |                           3 |                     92.9 |                     94.8 |                    1 |                   0 | PHYSICAL_VETO_DATA_ONLY   |    0.286109  |    0.37549   |      0.308454  |       0.377102 |
| 2005-10-01 00:00:00 | 2005-11-01 00:00:00  | PRICE_PRODUCT_CONFIRMED      | AVAILABLE    | 2005-10-26 00:00:00     | 2005-12-07 00:00:00 |                           2 |                     80.7 |                     90.6 |                    0 |                   0 | P4A_DATA_ONLY             |    0.0353476 |    0.193402  |      0.150648  |       0.256018 |
| 2007-12-01 00:00:00 | 2008-01-01 00:00:00  | FALSE_RELIEF_VETO            | AVAILABLE    | 2007-12-27 00:00:00     | 2008-02-06 00:00:00 |                           3 |                     88.1 |                     84.3 |                    0 |                   0 | PHYSICAL_VETO_DATA_ONLY   |    0.397659  |    0.360372  |      0.397659  |       0.667164 |
| 2008-07-01 00:00:00 | 2008-08-01 00:00:00  | PRICE_PRODUCT_CONFIRMED      | AVAILABLE    | 2008-07-30 00:00:00     | 2008-09-04 00:00:00 |                           1 |                     87.2 |                     88.7 |                    0 |                   0 | PHYSICAL_VETO_DATA_ONLY   |   -0.594407  |   -0.580702  |      0.135383  |       0.135383 |
| 2009-07-01 00:00:00 | 2009-08-01 00:00:00  | FALSE_RELIEF_VETO            | AVAILABLE    | 2009-07-29 00:00:00     | 2009-09-02 00:00:00 |                           2 |                     84.6 |                     87.2 |                    0 |                   0 | PHYSICAL_VETO_DATA_ONLY   |    0.126268  |    0.170366  |      0.191092  |       0.221814 |
| 2016-07-01 00:00:00 | 2016-08-01 00:00:00  | FALSE_RELIEF_VETO            | AVAILABLE    | 2016-07-27 00:00:00     | 2016-09-08 00:00:00 |                           2 |                     92.4 |                     93.7 |                    1 |                   0 | PHYSICAL_VETO_DATA_ONLY   |    0.0673945 |    0.0461894 |      0.0858702 |       0.143817 |
| 2020-09-01 00:00:00 | 2020-10-01 00:00:00  | FALSE_RELIEF_VETO            | AVAILABLE    | 2020-09-30 00:00:00     | 2020-11-04 00:00:00 |                           1 |                     75.8 |                     75.3 |                    0 |                   0 | PHYSICAL_VETO_DATA_ONLY   |    0.441878  |    0.686425  |      0.441878  |       0.695663 |
| 2022-07-01 00:00:00 | 2022-08-01 00:00:00  | PRICE_PRODUCT_CONFIRMED      | AVAILABLE    | 2022-07-27 00:00:00     | 2022-09-08 00:00:00 |                           1 |                     92.2 |                     90.9 |                    0 |                   0 | PHYSICAL_VETO_DATA_ONLY   |   -0.151594  |   -0.0890052 |      0.107449  |       0.107449 |
| 2023-10-01 00:00:00 | 2023-11-01 00:00:00  | PRICE_PRODUCT_CONFIRMED      | AVAILABLE    | 2023-10-25 00:00:00     | 2023-12-06 00:00:00 |                           2 |                     85.6 |                     90.5 |                    0 |                   0 | P4A_DATA_ONLY             |    0.160916  |    0.109307  |      0.172804  |       0.271238 |
| 2026-06-01 00:00:00 | 2026-07-01 00:00:00  | FALSE_RELIEF_VETO            | AVAILABLE    | 2026-06-24 00:00:00     | 2026-08-05 00:00:00 |                           1 |                     96.1 |                     96.5 |                    1 |                   0 | PHYSICAL_VETO_DATA_ONLY   |  nan         |  nan         |    nan         |     nan        |

## Interpretation boundary

This run asks whether release-aware U.S. inventory/refinery information adds discrimination beyond the frozen price layer.

It does not identify causality, it does not yet apply an independently frozen geopolitical/shipping veto, and it is not a trading system.