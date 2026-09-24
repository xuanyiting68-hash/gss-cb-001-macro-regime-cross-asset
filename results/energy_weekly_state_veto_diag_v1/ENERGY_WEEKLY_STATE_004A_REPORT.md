# ENERGY-WEEKLY-STATE-004A — Post-Run Veto Robustness

**POST-RUN DESCRIPTIVE DIAGNOSTIC / NO NEW P-VALUE FAMILY**

- completed TIGHT_OR_MIXED events: 10
- 8W leave-one-out median positive in every run: **True**
- 2018-present TIGHT_OR_MIXED median WTI 8W: **6.61%**
- 2018-present TIGHT_OR_MIXED median WTI 13W: **1.26%**
- DEMAND_DESTRUCTION n=4, median WTI 13W: **-7.07%**

## Sample robustness

| sample                 |   n_events |   n_8w |   median_wti_8w |   negative_share_8w |   median_short_mae_8w |   n_13w |   median_wti_13w |   negative_share_13w |   median_short_mae_13w |
|:-----------------------|-----------:|-------:|----------------:|--------------------:|----------------------:|--------:|-----------------:|---------------------:|-----------------------:|
| MIXED_ALL              |         10 |     10 |       0.0707752 |            0.2      |              0.152403 |      10 |        0.066982  |                 0.4  |               0.179187 |
| MIXED_EXCLUDE_2004     |          8 |      8 |       0.0661164 |            0.25     |              0.139252 |       8 |        0.0125961 |                 0.5  |               0.16998  |
| MIXED_PRE_2018         |          4 |      4 |       0.107319  |            0        |              0.152403 |       4 |        0.193246  |                 0.25 |               0.209792 |
| MIXED_2018_PRESENT     |          6 |      6 |       0.0661164 |            0.333333 |              0.146089 |       6 |        0.0125961 |                 0.5  |               0.16998  |
| DEMAND_DESTRUCTION_ALL |          4 |      4 |      -0.023614  |            0.5      |              0.132182 |       4 |       -0.0706966 |                 0.75 |               0.136046 |

## Leave-one-out

| dropped_release_date   |   n_events |   n_8w |   median_wti_8w |   negative_share_8w |   median_short_mae_8w |   n_13w |   median_wti_13w |   negative_share_13w |   median_short_mae_13w |
|:-----------------------|-----------:|-------:|----------------:|--------------------:|----------------------:|--------:|-----------------:|---------------------:|-----------------------:|
| 2004-02-11             |          9 |      9 |       0.0682281 |            0.222222 |              0.15002  |       9 |         0.060933 |             0.444444 |               0.176265 |
| 2004-11-03             |          9 |      9 |       0.0733223 |            0.222222 |              0.15002  |       9 |         0.060933 |             0.444444 |               0.176265 |
| 2009-06-24             |          9 |      9 |       0.0733223 |            0.222222 |              0.154786 |       9 |         0.073031 |             0.333333 |               0.18211  |
| 2017-09-13             |          9 |      9 |       0.0682281 |            0.222222 |              0.154786 |       9 |         0.060933 |             0.444444 |               0.176265 |
| 2018-05-31             |          9 |      9 |       0.0682281 |            0.222222 |              0.15002  |       9 |         0.073031 |             0.444444 |               0.18211  |
| 2020-07-01             |          9 |      9 |       0.0733223 |            0.222222 |              0.154786 |       9 |         0.073031 |             0.333333 |               0.18211  |
| 2021-01-27             |          9 |      9 |       0.0682281 |            0.222222 |              0.15002  |       9 |         0.060933 |             0.444444 |               0.176265 |
| 2022-03-16             |          9 |      9 |       0.0682281 |            0.222222 |              0.154786 |       9 |         0.060933 |             0.444444 |               0.176265 |
| 2022-06-23             |          9 |      9 |       0.0733223 |            0.111111 |              0.154786 |       9 |         0.073031 |             0.333333 |               0.18211  |
| 2026-04-15             |          9 |      9 |       0.0733223 |            0.111111 |              0.15002  |       9 |         0.073031 |             0.333333 |               0.18211  |

## Judgment

The descriptive TIGHT_OR_MIXED veto is substantially more robust at 8 weeks than at 13 weeks.
Its 8-week median remains positive after removing individual events, after excluding 2004, and in the 2018-present subset.
The 13-week separation decays materially in the modern subset, where the median is only slightly positive and the negative-return share is 50%.

DEMAND_DESTRUCTION remains a promising bearish mechanism candidate at 13 weeks, but n=4 and the pattern was observed post-run, so it is not promoted to confirmatory evidence.
