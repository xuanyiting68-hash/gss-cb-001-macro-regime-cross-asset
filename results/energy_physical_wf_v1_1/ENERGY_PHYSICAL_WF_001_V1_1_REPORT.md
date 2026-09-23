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
- P4B refinery-drop candidates: 1
- QC gate: PASS

## Primary four-test data-only family

| test         |   n_p4a |   n_veto |   p4a_mean |   veto_mean |   p4a_median |   veto_median |   difference_median_p4a_minus_veto |   mann_whitney_p |   bh_q_4test_family |
|:-------------|--------:|---------:|-----------:|------------:|-------------:|--------------:|-----------------------------------:|-----------------:|--------------------:|
| WTI_fwd_3m   |       3 |        8 |  0.0993702 |   0.0194132 |    0.0952539 |      0.105572 |                         -0.0103183 |         0.606543 |            0.808725 |
| WTI_fwd_6m   |       3 |        5 |  0.159947  |   0.0355316 |    0.210041  |      0.165768 |                          0.0442732 |         0.571429 |            0.808725 |
| short_MAE_3m |       3 |        8 |  0.136729  |   0.135407  |    0.134418  |      0.105572 |                          0.0288454 |         0.353914 |            0.808725 |
| short_MAE_6m |       3 |        5 |  0.201685  |   0.236209  |    0.238301  |      0.179676 |                          0.0586243 |         1        |            1        |

## Event panel

| s3_date             | price_anchor_month   | price_layer_classification   | strict_pit   | baseline_release_date   | decision_date       |   inventory_improving_count |   refinery_util_baseline |   refinery_util_decision |   refinery_worsening |   refinery_drop_5pp | physical_classification   |   wti_fwd_3m |   wti_fwd_6m |   short_mae_3m |   short_mae_6m |
|:--------------------|:---------------------|:-----------------------------|:-------------|:------------------------|:--------------------|----------------------------:|-------------------------:|-------------------------:|---------------------:|--------------------:|:--------------------------|-------------:|-------------:|---------------:|---------------:|
| 1999-10-01 00:00:00 | 1999-11-01 00:00:00  | FALSE_RELIEF_VETO            | UNAVAILABLE  | NaT                     | NaT                 |                         nan |                    nan   |                    nan   |                  nan |                 nan | STRICT_PIT_UNAVAILABLE    |  nan         |  nan         |    nan         |     nan        |
| 2002-06-01 00:00:00 | 2002-07-01 00:00:00  | FALSE_RELIEF_VETO            | AVAILABLE    | 2002-06-26 00:00:00     | 2002-08-28 00:00:00 |                           1 |                     92.5 |                     91.9 |                    0 |                   0 | PHYSICAL_VETO_DATA_ONLY   |   -0.0367361 |    0.298481  |      0.0897209 |       0.340869 |
| 2003-03-01 00:00:00 | 2003-04-01 00:00:00  | PRICE_PRODUCT_CONFIRMED      | AVAILABLE    | 2003-03-26 00:00:00     | 2003-05-29 00:00:00 |                           3 |                     88.5 |                     94.3 |                    0 |                   0 | P4A_DATA_ONLY             |    0.0895369 |    0.0500858 |      0.111835  |       0.111835 |
| 2004-11-01 00:00:00 | 2004-12-01 00:00:00  | PRICE_PRODUCT_CONFIRMED      | AVAILABLE    | 2004-11-24 00:00:00     | 2005-01-26 00:00:00 |                           3 |                     92.9 |                     91   |                    0 |                   0 | P4A_DATA_ONLY             |    0.11332   |    0.210041  |      0.163934  |       0.254918 |
| 2005-10-01 00:00:00 | 2005-11-01 00:00:00  | PRICE_PRODUCT_CONFIRMED      | AVAILABLE    | 2005-10-26 00:00:00     | 2005-12-29 00:00:00 |                           3 |                     80.7 |                     88.9 |                    0 |                   0 | P4A_DATA_ONLY             |    0.0952539 |    0.219715  |      0.134418  |       0.238301 |
| 2007-12-01 00:00:00 | 2008-01-01 00:00:00  | FALSE_RELIEF_VETO            | AVAILABLE    | 2007-12-27 00:00:00     | 2008-02-27 00:00:00 |                           3 |                     88.1 |                     84.7 |                    0 |                   0 | PHYSICAL_VETO_DATA_ONLY   |    0.293403  |    0.186565  |      0.335375  |       0.459082 |
| 2008-07-01 00:00:00 | 2008-08-01 00:00:00  | PRICE_PRODUCT_CONFIRMED      | AVAILABLE    | 2008-07-30 00:00:00     | 2008-09-24 00:00:00 |                           1 |                     87.2 |                     66.7 |                    0 |                   1 | PHYSICAL_VETO_DATA_ONLY   |   -0.691689  |   -0.500562  |      0.043991  |       0.043991 |
| 2009-07-01 00:00:00 | 2009-08-01 00:00:00  | FALSE_RELIEF_VETO            | AVAILABLE    | 2009-07-29 00:00:00     | 2009-09-30 00:00:00 |                           3 |                     84.6 |                     84.6 |                    0 |                   0 | PHYSICAL_VETO_DATA_ONLY   |    0.126171  |    0.165768  |      0.150014  |       0.179676 |
| 2016-07-01 00:00:00 | 2016-08-01 00:00:00  | FALSE_RELIEF_VETO            | AVAILABLE    | 2016-07-27 00:00:00     | 2016-09-28 00:00:00 |                           1 |                     92.4 |                     90.1 |                    0 |                   0 | PHYSICAL_VETO_DATA_ONLY   |    0.14744   |    0.027406  |      0.14744   |       0.157425 |
| 2020-09-01 00:00:00 | 2020-10-01 00:00:00  | FALSE_RELIEF_VETO            | AVAILABLE    | 2017-12-28 00:00:00     | 2026-06-10 00:00:00 |                           0 |                     95.7 |                     95.3 |                    0 |                   0 | PHYSICAL_VETO_DATA_ONLY   |    0.105572  |  nan         |      0.105572  |     nan        |
| 2022-07-01 00:00:00 | 2022-08-01 00:00:00  | PRICE_PRODUCT_CONFIRMED      | AVAILABLE    | 2017-12-28 00:00:00     | 2026-06-10 00:00:00 |                           0 |                     95.7 |                     95.3 |                    0 |                   0 | PHYSICAL_VETO_DATA_ONLY   |    0.105572  |  nan         |      0.105572  |     nan        |
| 2023-10-01 00:00:00 | 2023-11-01 00:00:00  | PRICE_PRODUCT_CONFIRMED      | AVAILABLE    | 2017-12-28 00:00:00     | 2026-06-10 00:00:00 |                           0 |                     95.7 |                     95.3 |                    0 |                   0 | PHYSICAL_VETO_DATA_ONLY   |    0.105572  |  nan         |      0.105572  |     nan        |
| 2026-06-01 00:00:00 | 2026-07-01 00:00:00  | FALSE_RELIEF_VETO            | AVAILABLE    | 2026-06-24 00:00:00     | 2026-08-05 00:00:00 |                           1 |                     96.1 |                     96.5 |                    1 |                   0 | PHYSICAL_VETO_DATA_ONLY   |  nan         |  nan         |    nan         |     nan        |

## Interpretation boundary

This run asks whether release-aware U.S. inventory/refinery information adds discrimination beyond the frozen price layer.

It does not identify causality, it does not yet apply an independently frozen geopolitical/shipping veto, and it is not a trading system.