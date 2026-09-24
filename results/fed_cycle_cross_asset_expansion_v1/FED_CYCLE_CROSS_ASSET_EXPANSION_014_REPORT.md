# FED-CYCLE-CROSS-ASSET-EXPANSION-014 — Report

**DESCRIPTIVE / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

## QC

- QC gate: **PASS**
- Frozen historical cycles: 10 mechanical / 7 broad episodes
- Market acquisition failures: []
- Current live 2026 cycle is excluded from historical outcome summaries.
- Raw Yahoo / Case-Shiller source histories are not committed.

## Liquid market phase summary

| asset   | anchor      |   n_legs |   n_broad_episodes | support_status        |   weighted_median_ret_3m |   weighted_median_ret_6m |   weighted_median_ret_12m |   weighted_median_mdd_12m |   weighted_median_mdd_trough_month |   weighted_late_trough_share_7_12 |
|:--------|:------------|---------:|-------------------:|:----------------------|-------------------------:|-------------------------:|--------------------------:|--------------------------:|-----------------------------------:|----------------------------------:|
| BTC_USD | FIRST_CUT   |        2 |                  2 | LIMITED_DESCRIPTIVE   |              -0.106625   |              -0.109031   |                 0.0184793 |                 0.149179  |                                  6 |                          0.5      |
| BTC_USD | FIRST_HIKE  |        2 |                  2 | LIMITED_DESCRIPTIVE   |              -0.401825   |              -0.514154   |                -0.383838  |                 0.123641  |                                  8 |                          1        |
| BTC_USD | LAST_HIKE   |        2 |                  2 | LIMITED_DESCRIPTIVE   |              -0.26427    |               0.545917   |                 0.34783   |                 0.0723445 |                                 12 |                          1        |
| BTC_USD | PAUSE_START |        2 |                  2 | LIMITED_DESCRIPTIVE   |               0.393002   |               1.43072    |                 1.16705   |                 0.114933  |                                 11 |                          1        |
| DXY     | FIRST_CUT   |       10 |                  7 | SUPPORTED_DESCRIPTIVE |               0.0227772  |               0.0193167  |                -0.0133301 |                 0.0518179 |                                  8 |                          0.761905 |
| DXY     | FIRST_HIKE  |       10 |                  7 | SUPPORTED_DESCRIPTIVE |              -0.0209118  |              -0.0440331  |                 0.0300943 |                 0.0824487 |                                  8 |                          0.52381  |
| DXY     | LAST_HIKE   |       10 |                  7 | SUPPORTED_DESCRIPTIVE |               0.0252808  |              -0.00133003 |                -0.0125548 |                 0.0518179 |                                  8 |                          0.666667 |
| DXY     | PAUSE_START |        7 |                  7 | SUPPORTED_DESCRIPTIVE |              -0.00401101 |               0.00505926 |                -0.0125548 |                 0.0629969 |                                 11 |                          0.714286 |
| TLT     | FIRST_CUT   |        3 |                  3 | LIMITED_DESCRIPTIVE   |               0.0749633  |               0.0775176  |                 0.151305  |                 0.0363468 |                                  9 |                          0.666667 |
| TLT     | FIRST_HIKE  |        3 |                  3 | LIMITED_DESCRIPTIVE   |               0.0816644  |               0.108424   |                 0.0110366 |                 0.147885  |                                  9 |                          1        |
| TLT     | LAST_HIKE   |        3 |                  3 | LIMITED_DESCRIPTIVE   |               0.0715565  |               0.105928   |                 0.0563342 |                 0.0498322 |                                 12 |                          0.666667 |
| TLT     | PAUSE_START |        3 |                  3 | LIMITED_DESCRIPTIVE   |               0.0416117  |               0.0691406  |                 0.0868918 |                 0.0498322 |                                 10 |                          0.666667 |
| VNQ     | FIRST_CUT   |        3 |                  3 | LIMITED_DESCRIPTIVE   |               0.0139903  |               0.00999179 |                -0.0465288 |                 0.187917  |                                  7 |                          0.666667 |
| VNQ     | FIRST_HIKE  |        2 |                  2 | LIMITED_DESCRIPTIVE   |              -0.099639   |              -0.133303   |                -0.177621  |                 0.114488  |                                  7 |                          1        |
| VNQ     | LAST_HIKE   |        3 |                  3 | LIMITED_DESCRIPTIVE   |               0.0780219  |               0.131019   |                 0.189778  |                 0.0941642 |                                 12 |                          0.666667 |
| VNQ     | PAUSE_START |        3 |                  3 | LIMITED_DESCRIPTIVE   |               0.124598   |               0.165019   |                 0.235177  |                 0.0941642 |                                 11 |                          0.666667 |

## Direct housing phase summary

| asset          | anchor      |   n_legs |   n_broad_episodes | support_status        |   weighted_median_ret_6m |   weighted_median_ret_12m |   weighted_median_ret_24m |   weighted_median_decline_24m |   weighted_median_trough_month_24m |
|:---------------|:------------|---------:|-------------------:|:----------------------|-------------------------:|--------------------------:|--------------------------:|------------------------------:|-----------------------------------:|
| US_HOUSE_PRICE | FIRST_CUT   |        7 |                  5 | SUPPORTED_DESCRIPTIVE |               0.00860611 |                 0.0521401 |                 0.126889  |                   0           |                                 18 |
| US_HOUSE_PRICE | FIRST_HIKE  |        7 |                  6 | SUPPORTED_DESCRIPTIVE |               0.0438444  |                 0.0528859 |                 0.118181  |                   0.000287514 |                                 10 |
| US_HOUSE_PRICE | LAST_HIKE   |        8 |                  6 | SUPPORTED_DESCRIPTIVE |               0.0203434  |                 0.0347335 |                 0.0733769 |                   0.0044325   |                                 17 |
| US_HOUSE_PRICE | PAUSE_START |        6 |                  6 | SUPPORTED_DESCRIPTIVE |               0.0218275  |                 0.037593  |                 0.0554744 |                   0.00134365  |                                 11 |

## Treasury-yield phase summary

| series   | anchor      |   n_legs |   n_broad_episodes | support_status        |   weighted_median_chg_3m_bp |   weighted_median_chg_6m_bp |   weighted_median_chg_12m_bp |   weighted_median_max_increase_12m_bp |   weighted_median_max_decrease_12m_bp |
|:---------|:------------|---------:|-------------------:|:----------------------|----------------------------:|----------------------------:|-----------------------------:|--------------------------------------:|--------------------------------------:|
| DGS10    | FIRST_CUT   |       10 |                  7 | SUPPORTED_DESCRIPTIVE |                    -12.342  |                    -31.6381 |                     -20.4786 |                             15.0864   |                              -67.3682 |
| DGS10    | FIRST_HIKE  |       10 |                  7 | SUPPORTED_DESCRIPTIVE |                     37.5738 |                     73.5955 |                      55.7773 |                            114.573    |                               13.5909 |
| DGS10    | LAST_HIKE   |       10 |                  7 | SUPPORTED_DESCRIPTIVE |                    -39.1    |                    -54.55   |                     -59.9163 |                             -0.714286 |                             -110.507  |
| DGS10    | PAUSE_START |        7 |                  7 | SUPPORTED_DESCRIPTIVE |                    -64.1455 |                    -77.3541 |                    -107.501  |                            -25.9565   |                             -130.8    |
| DGS2     | FIRST_CUT   |       10 |                  7 | SUPPORTED_DESCRIPTIVE |                    -26.2636 |                    -60.3528 |                    -166.582  |                            -16.6      |                             -166.582  |
| DGS2     | FIRST_HIKE  |       10 |                  7 | SUPPORTED_DESCRIPTIVE |                     54.5502 |                    115.368  |                     122.732  |                            167.823    |                               12.6077 |
| DGS2     | LAST_HIKE   |       10 |                  7 | SUPPORTED_DESCRIPTIVE |                    -19.9182 |                    -52.8446 |                    -124.567  |                              7.8134   |                             -130.764  |
| DGS2     | PAUSE_START |        7 |                  7 | SUPPORTED_DESCRIPTIVE |                    -72.8045 |                    -84.1316 |                    -127.924  |                            -17.2105   |                             -127.924  |

## Mechanical cash-carry benchmark

| asset               | anchor      |   n_legs |   n_broad_episodes | support_status        |   weighted_median_cash_carry_3m |   weighted_median_cash_carry_6m |   weighted_median_cash_carry_12m |   weighted_median_avg_dff_12m |
|:--------------------|:------------|---------:|-------------------:|:----------------------|--------------------------------:|--------------------------------:|---------------------------------:|------------------------------:|
| MECHANICAL_CASH_DFF | FIRST_CUT   |       10 |                  7 | SUPPORTED_DESCRIPTIVE |                      0.0130624  |                       0.0231851 |                        0.0449052 |                       4.40068 |
| MECHANICAL_CASH_DFF | FIRST_HIKE  |       10 |                  7 | SUPPORTED_DESCRIPTIVE |                      0.00911227 |                       0.0200638 |                        0.0472948 |                       4.6302  |
| MECHANICAL_CASH_DFF | LAST_HIKE   |       10 |                  7 | SUPPORTED_DESCRIPTIVE |                      0.0151027  |                       0.0300539 |                        0.0593702 |                       5.78136 |
| MECHANICAL_CASH_DFF | PAUSE_START |        7 |                  7 | SUPPORTED_DESCRIPTIVE |                      0.0151237  |                       0.0299072 |                        0.0587884 |                       5.72617 |

## Evidence boundary

- TLT/VNQ/BTC/DXY have shorter histories than the long-history Gold/equity/WTI layer; support labels must remain visible.
- TLT/VNQ adjusted-close histories are ETF proxies and do not replace security-level bond/real-estate decomposition.
- Case-Shiller is a slow national house-price index, not an investable total-return series.
- DGS2/DGS10 changes are yield changes, not bond returns.
- DFF cash carry is a mechanical benchmark that ignores fees, tax and intra-month compounding.
- No p-value/FDR family is run; no causal or trading claim is authorized.