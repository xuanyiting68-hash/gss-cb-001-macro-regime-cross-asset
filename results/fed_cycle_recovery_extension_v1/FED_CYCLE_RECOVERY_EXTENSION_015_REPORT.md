# FED-CYCLE-RECOVERY-EXTENSION-015 — New-Asset Recovery Clock

**DESCRIPTIVE / RIGHT-CENSORING PRESERVED / NOT CAUSAL / NOT A FORECAST**

- QC: **PASS**

## Liquid-market recovery summary

| asset   | anchor      | recovery_level   |   n_legs |   n_broad_episodes | support_status        |   positive_drawdown_episodes |   observed_recoveries |   right_censored |   weighted_km_median_months |
|:--------|:------------|:-----------------|---------:|-------------------:|:----------------------|-----------------------------:|----------------------:|-----------------:|----------------------------:|
| BTC_USD | FIRST_CUT   | 50%              |        2 |                  2 | LIMITED_DESCRIPTIVE   |                            2 |                     2 |                0 |                           2 |
| BTC_USD | FIRST_CUT   | 100%             |        2 |                  2 | LIMITED_DESCRIPTIVE   |                            2 |                     2 |                0 |                           2 |
| BTC_USD | FIRST_HIKE  | 50%              |        2 |                  2 | LIMITED_DESCRIPTIVE   |                            2 |                     2 |                0 |                           2 |
| BTC_USD | FIRST_HIKE  | 100%             |        2 |                  2 | LIMITED_DESCRIPTIVE   |                            2 |                     2 |                0 |                           3 |
| BTC_USD | LAST_HIKE   | 50%              |        2 |                  2 | LIMITED_DESCRIPTIVE   |                            2 |                     2 |                0 |                           2 |
| BTC_USD | LAST_HIKE   | 100%             |        2 |                  2 | LIMITED_DESCRIPTIVE   |                            2 |                     2 |                0 |                           4 |
| BTC_USD | PAUSE_START | 50%              |        2 |                  2 | LIMITED_DESCRIPTIVE   |                            2 |                     2 |                0 |                           2 |
| BTC_USD | PAUSE_START | 100%             |        2 |                  2 | LIMITED_DESCRIPTIVE   |                            2 |                     2 |                0 |                           3 |
| DXY     | FIRST_CUT   | 50%              |       10 |                  7 | SUPPORTED_DESCRIPTIVE |                           10 |                     7 |                3 |                           5 |
| DXY     | FIRST_CUT   | 100%             |       10 |                  7 | SUPPORTED_DESCRIPTIVE |                           10 |                     7 |                3 |                           6 |
| DXY     | FIRST_HIKE  | 50%              |       10 |                  7 | SUPPORTED_DESCRIPTIVE |                           10 |                    10 |                0 |                           6 |
| DXY     | FIRST_HIKE  | 100%             |       10 |                  7 | SUPPORTED_DESCRIPTIVE |                           10 |                     8 |                2 |                          11 |
| DXY     | LAST_HIKE   | 50%              |       10 |                  7 | SUPPORTED_DESCRIPTIVE |                           10 |                     8 |                2 |                           4 |
| DXY     | LAST_HIKE   | 100%             |       10 |                  7 | SUPPORTED_DESCRIPTIVE |                           10 |                     8 |                2 |                          12 |
| DXY     | PAUSE_START | 50%              |        7 |                  7 | SUPPORTED_DESCRIPTIVE |                            7 |                     6 |                1 |                           4 |
| DXY     | PAUSE_START | 100%             |        7 |                  7 | SUPPORTED_DESCRIPTIVE |                            7 |                     6 |                1 |                           8 |
| TLT     | FIRST_CUT   | 50%              |        3 |                  3 | LIMITED_DESCRIPTIVE   |                            3 |                     3 |                0 |                           1 |
| TLT     | FIRST_CUT   | 100%             |        3 |                  3 | LIMITED_DESCRIPTIVE   |                            3 |                     2 |                1 |                           3 |
| TLT     | FIRST_HIKE  | 50%              |        3 |                  3 | LIMITED_DESCRIPTIVE   |                            3 |                     2 |                1 |                           9 |
| TLT     | FIRST_HIKE  | 100%             |        3 |                  3 | LIMITED_DESCRIPTIVE   |                            3 |                     2 |                1 |                          30 |
| TLT     | LAST_HIKE   | 50%              |        3 |                  3 | LIMITED_DESCRIPTIVE   |                            3 |                     3 |                0 |                           2 |
| TLT     | LAST_HIKE   | 100%             |        3 |                  3 | LIMITED_DESCRIPTIVE   |                            3 |                     3 |                0 |                           3 |
| TLT     | PAUSE_START | 50%              |        3 |                  3 | LIMITED_DESCRIPTIVE   |                            3 |                     3 |                0 |                           2 |
| TLT     | PAUSE_START | 100%             |        3 |                  3 | LIMITED_DESCRIPTIVE   |                            3 |                     3 |                0 |                           2 |
| VNQ     | FIRST_CUT   | 50%              |        3 |                  3 | LIMITED_DESCRIPTIVE   |                            3 |                     3 |                0 |                           3 |
| VNQ     | FIRST_CUT   | 100%             |        3 |                  3 | LIMITED_DESCRIPTIVE   |                            3 |                     3 |                0 |                          12 |
| VNQ     | FIRST_HIKE  | 50%              |        2 |                  2 | LIMITED_DESCRIPTIVE   |                            2 |                     2 |                0 |                           2 |
| VNQ     | FIRST_HIKE  | 100%             |        2 |                  2 | LIMITED_DESCRIPTIVE   |                            2 |                     2 |                0 |                          21 |
| VNQ     | LAST_HIKE   | 50%              |        3 |                  3 | LIMITED_DESCRIPTIVE   |                            3 |                     3 |                0 |                           1 |
| VNQ     | LAST_HIKE   | 100%             |        3 |                  3 | LIMITED_DESCRIPTIVE   |                            3 |                     2 |                1 |                           2 |
| VNQ     | PAUSE_START | 50%              |        3 |                  3 | LIMITED_DESCRIPTIVE   |                            3 |                     3 |                0 |                           1 |
| VNQ     | PAUSE_START | 100%             |        3 |                  3 | LIMITED_DESCRIPTIVE   |                            3 |                     3 |                0 |                           2 |

## Housing recovery summary

| asset          | anchor      | recovery_level   |   n_legs |   n_broad_episodes | support_status        |   positive_drawdown_episodes |   observed_recoveries |   right_censored |   weighted_km_median_months |
|:---------------|:------------|:-----------------|---------:|-------------------:|:----------------------|-----------------------------:|----------------------:|-----------------:|----------------------------:|
| US_HOUSE_PRICE | FIRST_CUT   | 50%              |        7 |                  5 | SUPPORTED_DESCRIPTIVE |                            3 |                     2 |                1 |                           4 |
| US_HOUSE_PRICE | FIRST_CUT   | 100%             |        7 |                  5 | SUPPORTED_DESCRIPTIVE |                            3 |                     2 |                1 |                          28 |
| US_HOUSE_PRICE | FIRST_HIKE  | 50%              |        7 |                  6 | SUPPORTED_DESCRIPTIVE |                            4 |                     4 |                0 |                           2 |
| US_HOUSE_PRICE | FIRST_HIKE  | 100%             |        7 |                  6 | SUPPORTED_DESCRIPTIVE |                            4 |                     4 |                0 |                           2 |
| US_HOUSE_PRICE | LAST_HIKE   | 50%              |        8 |                  6 | SUPPORTED_DESCRIPTIVE |                            5 |                     4 |                1 |                           2 |
| US_HOUSE_PRICE | LAST_HIKE   | 100%             |        8 |                  6 | SUPPORTED_DESCRIPTIVE |                            5 |                     4 |                1 |                           3 |
| US_HOUSE_PRICE | PAUSE_START | 50%              |        6 |                  6 | SUPPORTED_DESCRIPTIVE |                            4 |                     3 |                1 |                           1 |
| US_HOUSE_PRICE | PAUSE_START | 100%             |        6 |                  6 | SUPPORTED_DESCRIPTIVE |                            4 |                     3 |                1 |                           2 |

## Reading rule

- Liquid assets use the exact PHASE-CLOCK-004 12M MDD definition and search recovery up to 60 months after trough.
- Housing uses its predeclared 24M drawdown window and then the same prior-peak 50%/100% recovery logic.
- Missing KM medians mean at least half the broad-episode-weighted risk set did not recover within observed/censored support.
- TLT/VNQ/BTC support remains limited where 014 labels it limited.
