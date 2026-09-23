# ENERGY-FLOW-002 — First Stock–Flow Mechanism Map
Date: 2026-09-24

## Status

**POST-v1.1 / DESCRIPTIVE / HYPOTHESIS-GENERATING / NOT DEPLOYABLE**

No new confirmatory p-value family is created on the same six price-confirmed episodes.

## QC and support

- Strict-PIT events: 12
- Strict-PIT complete price-confirmed events: 4
- FLOW_DD: 0
- FLOW_SN: 1
- FLOW_MIXED: 3
- QC gate: PASS

## Price-confirmed mechanism map

| s3_date             | decision_date       | price_layer_classification   | flow_classification   |   inventory_improving_count |   demand_weak_count | throughput_weak   |   upstream_supply_up_count |   wti_fwd_3m |   wti_fwd_6m |   short_mae_3m |   short_mae_6m |
|:--------------------|:--------------------|:-----------------------------|:----------------------|----------------------------:|--------------------:|:------------------|---------------------------:|-------------:|-------------:|---------------:|---------------:|
| 2005-10-01 00:00:00 | 2005-12-07 00:00:00 | PRICE_PRODUCT_CONFIRMED      | FLOW_SN               |                           2 |                   1 | False             |                          2 |    0.0353476 |    0.193402  |       0.150648 |       0.256018 |
| 2008-07-01 00:00:00 | 2008-09-04 00:00:00 | PRICE_PRODUCT_CONFIRMED      | FLOW_MIXED            |                           1 |                   0 | False             |                          1 |   -0.594407  |   -0.580702  |       0.135383 |       0.135383 |
| 2022-07-01 00:00:00 | 2022-09-08 00:00:00 | PRICE_PRODUCT_CONFIRMED      | FLOW_MIXED            |                           1 |                   3 | False             |                          2 |   -0.151594  |   -0.0890052 |       0.107449 |       0.107449 |
| 2023-10-01 00:00:00 | 2023-12-06 00:00:00 | PRICE_PRODUCT_CONFIRMED      | FLOW_MIXED            |                           2 |                   2 | False             |                          1 |    0.160916  |    0.109307  |       0.172804 |       0.271238 |

## Group descriptives

| flow_classification   | metric       |   n |       mean |     median |   negative_share |
|:----------------------|:-------------|----:|-----------:|-----------:|-----------------:|
| FLOW_MIXED            | wti_fwd_3m   |   3 | -0.195028  | -0.151594  |         0.666667 |
| FLOW_MIXED            | wti_fwd_6m   |   3 | -0.1868    | -0.0890052 |         0.666667 |
| FLOW_MIXED            | short_mae_3m |   3 |  0.138545  |  0.135383  |       nan        |
| FLOW_MIXED            | short_mae_6m |   3 |  0.171357  |  0.135383  |       nan        |
| FLOW_SN               | wti_fwd_3m   |   1 |  0.0353476 |  0.0353476 |         0        |
| FLOW_SN               | wti_fwd_6m   |   1 |  0.193402  |  0.193402  |         0        |
| FLOW_SN               | short_mae_3m |   1 |  0.150648  |  0.150648  |       nan        |
| FLOW_SN               | short_mae_6m |   1 |  0.256018  |  0.256018  |       nan        |

## Interpretation boundary

This module is a mechanism map, not a validated forecast.
It was designed after observing the v1.1 stock-only falsification, so its first run cannot be treated as an independent confirmatory test.

The purpose is to distinguish stock accumulation caused by different flow states before deciding whether an independently testable follow-up is warranted.