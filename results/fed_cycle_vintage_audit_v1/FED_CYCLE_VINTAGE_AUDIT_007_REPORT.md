# FED-CYCLE-VINTAGE-AUDIT-007 — Report

**REAL-TIME REVISION AUDIT / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

## Event-level revision summary

- events: 10
- real-time IPT available: 10
- growth-state flips: 1
- flip share: 0.100
- median absolute YoY revision gap: 2.225 pp
- max absolute YoY revision gap: 4.035 pp

| cycle_id   | event_date          | event_month   | target_period   | selected_vintage_period   |   current_vintage_indpro_yoy |   realtime_ipt_yoy |   revision_gap_pp | current_growth_state   | realtime_growth_state   | state_flip   |
|:-----------|:--------------------|:--------------|:----------------|:--------------------------|-----------------------------:|-------------------:|------------------:|:-----------------------|:------------------------|:-------------|
| T01_1983   | 1983-03-31 00:00:00 | 1983-03       | 1983-01         | 1983-02                   |                   -0.021386  |        -0.0319829  |          1.0597   | WEAK                   | WEAK                    | False        |
| T02_1984   | 1984-03-29 00:00:00 | 1984-03       | 1984-01         | 1984-02                   |                    0.110304  |         0.150655   |         -4.03513  | STRONG                 | STRONG                  | False        |
| T03_1987   | 1987-01-05 00:00:00 | 1987-01       | 1986-11         | 1986-12                   |                    0.0153572 |         0.0088141  |          0.654308 | WEAK                   | WEAK                    | False        |
| T04_1987   | 1987-08-27 00:00:00 | 1987-08       | 1987-06         | 1987-07                   |                    0.0551944 |         0.0322061  |          2.29883  | STRONG                 | STRONG                  | False        |
| T05_1988   | 1988-03-30 00:00:00 | 1988-03       | 1988-01         | 1988-02                   |                    0.0768326 |         0.0602219  |          1.66107  | STRONG                 | STRONG                  | False        |
| T06_1994   | 1994-02-04 00:00:00 | 1994-02       | 1993-12         | 1994-01                   |                    0.0340773 |         0.046832   |         -1.27546  | STRONG                 | STRONG                  | False        |
| T07_1999   | 1999-06-30 00:00:00 | 1999-06       | 1999-04         | 1999-05                   |                    0.0430725 |         0.0205636  |          2.2509   | STRONG                 | STRONG                  | False        |
| T08_2004   | 2004-06-30 00:00:00 | 2004-06       | 2004-04         | 2004-05                   |                    0.0261512 |         0.0481381  |         -2.19868  | STRONG                 | STRONG                  | False        |
| T09_2015   | 2015-12-16 00:00:00 | 2015-12       | 2015-10         | 2015-11                   |                   -0.0272507 |         0.00374532 |         -3.0996   | WEAK                   | WEAK                    | False        |
| T10_2022   | 2022-03-16 00:00:00 | 2022-03       | 2022-01         | 2022-02                   |                    0.0131813 |         0.0412475  |         -2.80661  | WEAK                   | STRONG                  | True         |

## Same-sample within-cycle revision tests

| outcome         |   same_sample_rows |   n_cycles |   n_broad_episodes |   realtime_beta_per_1sd |   realtime_p_broad_exact |   realtime_p_mechanical_exact | realtime_loo_sign_stable   |   current_same_sample_beta_per_1sd |   current_same_sample_p_broad_exact |   current_same_sample_p_mechanical_exact | current_same_sample_loo_sign_stable   | beta_sign_agreement   |   beta_difference_realtime_minus_current | status                   |   max_cycle_weight_error |
|:----------------|-------------------:|-----------:|-------------------:|------------------------:|-------------------------:|------------------------------:|:---------------------------|-----------------------------------:|------------------------------------:|-----------------------------------------:|:--------------------------------------|:----------------------|-----------------------------------------:|:-------------------------|-------------------------:|
| GOLD_FWD_6M_RET |                165 |         10 |                  7 |             -0.0196473  |                 0.015625 |                     0.0253906 | True                       |                        -0.0127457  |                            0.125    |                                 0.111328 | True                                  | True                  |                             -0.00690159  | SUPPORTED_REVISION_AUDIT |                        0 |
| GOLD_FWD_6M_MDD |                165 |         10 |                  7 |              0.00322907 |                 0.71875  |                     0.734375  | False                      |                         0.00347046 |                            0.390625 |                                 0.398438 | True                                  | True                  |                             -0.000241394 | SUPPORTED_REVISION_AUDIT |                        0 |

## CPI boundary

- Original inflation state uses CPIAUCNS (not seasonally adjusted).
- Philadelphia Fed PCPI is seasonally adjusted and is not substituted.
- This module upgrades only industrial production to an exact RTDSM real-time vintage audit.