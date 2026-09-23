# ENERGY-PRICE-WF-001 — First Exhaustive Public-Source Walk-Forward
Date: 2026-09-24

## Evidence status

**EXPLORATORY WALK-FORWARD / PRICE-PRODUCT LAYER ONLY / NOT DEPLOYABLE**

This run follows the frozen ENERGY_PRICE_WALKFORWARD_V1_LOCK protocol.
It does not use inventory/refinery data and therefore does not identify physical supply normalization.

## Data QC

- Common sample: 1990-04-01 to 2026-08-01
- Complete common months: 437
- Missing common months: 0
- Duplicate dates: 0
- Non-positive price cells: 0
- S2 extreme months: 34
- Raw S3 rollover months: 18
- De-clustered S3 events: 13

## Event counts

- PRICE_PRODUCT_CONFIRMED: 6
- FALSE_RELIEF_VETO: 7

## Primary four-test family

| test         |   n_confirmed |   n_veto |   confirmed_mean |   veto_mean |   confirmed_median |   veto_median |   difference_median_confirmed_minus_veto |   mann_whitney_p |   bh_q_4test_family |
|:-------------|--------------:|---------:|-----------------:|------------:|-------------------:|--------------:|-----------------------------------------:|-----------------:|--------------------:|
| WTI_fwd_3m   |             6 |        6 |       -0.0348641 |    0.148926 |          0.0255461 |      0.136239 |                               -0.110693  |         0.132035 |            0.224001 |
| WTI_fwd_6m   |             6 |        6 |       -0.036187  |    0.274199 |          0.0535116 |      0.208695 |                               -0.155183  |         0.132035 |            0.224001 |
| short_MAE_3m |             6 |        7 |        0.078456  |    0.151264 |          0.0459709 |      0.113148 |                               -0.0671776 |         0.172359 |            0.224001 |
| short_MAE_6m |             6 |        7 |        0.123313  |    0.254032 |          0.109646  |      0.195662 |                               -0.0860155 |         0.224001 |            0.224001 |

## Group descriptives

| classification          | metric       |   n |       mean |     median |   negative_share |
|:------------------------|:-------------|----:|-----------:|-----------:|-----------------:|
| FALSE_RELIEF_VETO       | WTI_fwd_1m   |   7 |  0.0273893 |  0.0390863 |         0.142857 |
| FALSE_RELIEF_VETO       | WTI_fwd_3m   |   6 |  0.148926  |  0.136239  |         0        |
| FALSE_RELIEF_VETO       | WTI_fwd_6m   |   6 |  0.274199  |  0.208695  |         0        |
| FALSE_RELIEF_VETO       | WTI_fwd_12m  |   6 |  0.197723  |  0.10932   |         0.166667 |
| FALSE_RELIEF_VETO       | short_mae_3m |   7 |  0.151264  |  0.113148  |       nan        |
| FALSE_RELIEF_VETO       | short_mae_6m |   7 |  0.254032  |  0.195662  |       nan        |
| PRICE_PRODUCT_CONFIRMED | WTI_fwd_1m   |   6 | -0.0300941 | -0.0383284 |         0.666667 |
| PRICE_PRODUCT_CONFIRMED | WTI_fwd_3m   |   6 | -0.0348641 |  0.0255461 |         0.5      |
| PRICE_PRODUCT_CONFIRMED | WTI_fwd_6m   |   6 | -0.036187  |  0.0535116 |         0.333333 |
| PRICE_PRODUCT_CONFIRMED | WTI_fwd_12m  |   6 |  0.0121155 | -0.0432976 |         0.5      |
| PRICE_PRODUCT_CONFIRMED | short_mae_3m |   6 |  0.078456  |  0.0459709 |       nan        |
| PRICE_PRODUCT_CONFIRMED | short_mae_6m |   6 |  0.123313  |  0.109646  |       nan        |

## Simple WTI rollover benchmark

- De-clustered simple-rollover events: 46
- 3M mean: -2.30%; median: -3.47%; negative share: 57.8%
- 6M mean: +1.53%; median: +0.27%; negative share: 48.9%

## Interpretation boundary

Even a supportive result is public price-product timing evidence only. It is not proof of physical supply normalization and it is not a deployable short strategy.

The next gate is a release-aware EIA inventory/refinery extension.

## Source registry

| series_id    | title                                                               | source                                          | unit       | first_date   | last_date   | sha256                                                           |
|:-------------|:--------------------------------------------------------------------|:------------------------------------------------|:-----------|:-------------|:------------|:-----------------------------------------------------------------|
| MCOILWTICO   | Crude Oil Prices: West Texas Intermediate (WTI) - Cushing, Oklahoma | U.S. Energy Information Administration via FRED | USD/barrel | 1986-01-01   | 2026-08-01  | 15d15b27577192946d70dd0170018862489d42da469a440a2d4daa2e00388629 |
| MGASUSGULF   | Conventional Gasoline Prices: U.S. Gulf Coast, Regular              | U.S. Energy Information Administration via FRED | USD/gallon | 1986-06-01   | 2026-08-01  | e5910c1507c8cc71676507aa2fb6dac7fce388486bc8b311f207075bd4632937 |
| MHOILNYH     | No. 2 Heating Oil Prices: New York Harbor                           | U.S. Energy Information Administration via FRED | USD/gallon | 1986-06-01   | 2026-08-01  | 220070049984d5f5254bb2aed290a8ec1ac751773f92c9ed307f12c532d19b1c |
| MJFUELUSGULF | Kerosene-Type Jet Fuel Prices: U.S. Gulf Coast                      | U.S. Energy Information Administration via FRED | USD/gallon | 1990-04-01   | 2026-08-01  | c4644fa3e41f3dda350f20f4b9874bd355853d5f328247360615c95279b5741c |