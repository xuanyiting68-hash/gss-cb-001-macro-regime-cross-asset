# ENERGY-WEEKLY-TRANSITION-011 — Historical Mixed-State Transition Diagnostic

**POST-RUN DESCRIPTIVE / EXACT 004 MECHANISM RULE / NO P-VALUES**

- QC: **PASS**
- completed historical TIGHT_OR_MIXED events: 10
- ever clean within 4 releases: 6
- two-release confirmed within 4: 2
- DD confirmed within 4: 1
- SN confirmed within 4: 1

## Timing

|   historical_mixed_events |   ever_clean_within_4 |   ever_two_release_confirmed_within_4 |   confirmed_by_t2 |   confirmed_by_t3 |   confirmed_by_t4 |   dd_confirmed_within_4 |   sn_confirmed_within_4 |   candidate_only |   remains_mixed_or_incomplete |
|--------------------------:|----------------------:|--------------------------------------:|------------------:|------------------:|------------------:|------------------------:|------------------------:|-----------------:|------------------------------:|
|                        10 |                     6 |                                     2 |                 0 |                 2 |                 2 |                       1 |                       1 |                4 |                             4 |

## Outcome descriptives by transition group

| transition_group            |   n |   median_wti_4w |   negative_share_4w |   median_wti_8w |   negative_share_8w |   median_wti_13w |   negative_share_13w |   median_short_mae_8w |   median_short_mae_13w |
|:----------------------------|----:|----------------:|--------------------:|----------------:|--------------------:|-----------------:|---------------------:|----------------------:|-----------------------:|
| DD_CONFIRMED_WITHIN_4       |   1 |      0.0375838  |                 0   |       0.0733223 |                 0   |        0.073031  |                 0    |              0.128484 |               0.184228 |
| SN_CONFIRMED_WITHIN_4       |   1 |      0.126425   |                 0   |       0.0817505 |                 0   |        0.060933  |                 0    |              0.176265 |               0.176265 |
| CLEAN_CANDIDATE_ONLY        |   4 |     -0.00223504 |                 0.5 |       0.107319  |                 0   |        0.191233  |                 0.25 |              0.152403 |               0.209792 |
| REMAINS_MIXED_OR_INCOMPLETE |   4 |      0.0367122  |                 0.5 |      -0.0111833 |                 0.5 |       -0.0718824 |                 0.75 |              0.114384 |               0.114384 |

## Event paths

| event_release_date   | event_week_end   | event_original_class   | t1_release_date   | t1_class        | t2_release_date   | t2_class             | t3_release_date   | t3_class             | t4_release_date   | t4_class           | transition_group            |   first_clean_release_number |   first_confirm_release_number | first_confirm_class   |   wti_fwd_4w |   wti_fwd_8w |   wti_fwd_13w |   short_mae_8w |   short_mae_13w |
|:---------------------|:-----------------|:-----------------------|:------------------|:----------------|:------------------|:---------------------|:------------------|:---------------------|:------------------|:-------------------|:----------------------------|-----------------------------:|-------------------------------:|:----------------------|-------------:|-------------:|--------------:|---------------:|----------------:|
| 2004-02-11           | 2004-02-06       | TIGHT_OR_MIXED         | 2004-02-19        | DATA_INCOMPLETE | 2004-02-25        | DATA_INCOMPLETE      | 2004-03-03        | TIGHT_OR_MIXED       | 2004-03-10        | DATA_INCOMPLETE    | REMAINS_MIXED_OR_INCOMPLETE |                          nan |                            nan | nan                   |    0.226601  |    0.444509  |     0.26601   |      0.444509  |       0.590553  |
| 2004-11-03           | 2004-10-29       | TIGHT_OR_MIXED         | 2004-11-10        | DATA_INCOMPLETE | 2004-11-17        | SUPPLY_NORMALIZATION | 2004-11-24        | DATA_INCOMPLETE      | 2004-12-01        | TIGHT_OR_MIXED     | CLEAN_CANDIDATE_ONLY        |                            2 |                            nan | nan                   |   -0.0498982 |    0.0682281 |     0.237475  |      0.154786  |       0.237475  |
| 2009-06-24           | 2009-06-19       | TIGHT_OR_MIXED         | 2009-07-01        | TIGHT_OR_MIXED  | 2009-07-08        | TIGHT_OR_MIXED       | 2009-07-15        | SUPPLY_NORMALIZATION | 2009-07-22        | TIGHT_OR_MIXED     | CLEAN_CANDIDATE_ONLY        |                            3 |                            nan | nan                   |   -0.0195122 |    0.0571019 |    -0.0450502 |      0.0571019 |       0.0571019 |
| 2017-09-13           | 2017-09-08       | TIGHT_OR_MIXED         | 2017-09-20        | TIGHT_OR_MIXED  | 2017-09-27        | DEMAND_DESTRUCTION   | 2017-10-04        | TIGHT_OR_MIXED       | 2017-10-12        | TIGHT_OR_MIXED     | CLEAN_CANDIDATE_ONLY        |                            2 |                            nan | nan                   |    0.0150421 |    0.14641   |     0.149017  |      0.15002   |       0.18211   |
| 2018-05-31           | 2018-05-25       | TIGHT_OR_MIXED         | 2018-06-06        | TIGHT_OR_MIXED  | 2018-06-13        | SUPPLY_NORMALIZATION | 2018-06-20        | SUPPLY_NORMALIZATION | 2018-06-27        | TIGHT_OR_MIXED     | SN_CONFIRMED_WITHIN_4       |                            2 |                              3 | SUPPLY_NORMALIZATION  |    0.126425  |    0.0817505 |     0.060933  |      0.176265  |       0.176265  |
| 2020-07-01           | 2020-06-26       | TIGHT_OR_MIXED         | 2020-07-08        | TIGHT_OR_MIXED  | 2020-07-15        | TIGHT_OR_MIXED       | 2020-07-22        | TIGHT_OR_MIXED       | 2020-07-29        | TIGHT_OR_MIXED     | REMAINS_MIXED_OR_INCOMPLETE |                          nan |                            nan | nan                   |   -0.0115849 |    0.0589105 |    -0.0357407 |      0.0650727 |       0.0650727 |
| 2021-01-27           | 2021-01-22       | TIGHT_OR_MIXED         | 2021-02-03        | TIGHT_OR_MIXED  | 2021-02-10        | TIGHT_OR_MIXED       | 2021-02-18        | TIGHT_OR_MIXED       | 2021-02-24        | DEMAND_DESTRUCTION | CLEAN_CANDIDATE_ONLY        |                            4 |                            nan | nan                   |    0.177765  |    0.165901  |     0.233448  |      0.264447  |       0.264447  |
| 2022-03-16           | 2022-03-11       | TIGHT_OR_MIXED         | 2022-03-23        | TIGHT_OR_MIXED  | 2022-03-30        | DEMAND_DESTRUCTION   | 2022-04-06        | DEMAND_DESTRUCTION   | 2022-04-13        | TIGHT_OR_MIXED     | DD_CONFIRMED_WITHIN_4       |                            2 |                              3 | DEMAND_DESTRUCTION    |    0.0375838 |    0.0733223 |     0.073031  |      0.128484  |       0.184228  |
| 2022-06-23           | 2022-06-17       | TIGHT_OR_MIXED         | 2022-06-29        | TIGHT_OR_MIXED  | 2022-07-07        | TIGHT_OR_MIXED       | 2022-07-13        | TIGHT_OR_MIXED       | 2022-07-20        | TIGHT_OR_MIXED     | REMAINS_MIXED_OR_INCOMPLETE |                          nan |                            nan | nan                   |   -0.0847162 |   -0.143486  |    -0.27652   |      0.0420831 |       0.0420831 |
| 2026-04-15           | 2026-04-10       | TIGHT_OR_MIXED         | 2026-04-22        | TIGHT_OR_MIXED  | 2026-04-29        | TIGHT_OR_MIXED       | 2026-05-06        | TIGHT_OR_MIXED       | 2026-05-13        | TIGHT_OR_MIXED     | REMAINS_MIXED_OR_INCOMPLETE |                          nan |                            nan | nan                   |    0.0850093 |   -0.0812772 |    -0.108024  |      0.163695  |       0.163695  |

This diagnostic is hypothesis-generating only. It does not alter the current live event, 009 confirmation rule, or 008 outcome accounting.
