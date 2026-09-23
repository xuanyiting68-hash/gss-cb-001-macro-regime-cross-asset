# FED-CYCLE-GOLD-LONGHIST-MONTHLY-001 — Report
Generated: 2026-09-23

Status: **QC-PASSED DESCRIPTIVE LONG-HISTORY ROBUSTNESS / NOT CAUSAL / NOT DEPLOYABLE**

## Source and frequency boundary

- Source commit: 95bfea9197222dcda13d8c4d9928fb631fe745aa
- Eligible monthly sample: 1960-01 to 2026-08
- Modern source: World Bank Commodity Markets via datasets/gold-prices.
- License: ODC-PDDL-1.0.
- 1833-1959 pseudo-monthly repeated annual averages are excluded.
- Event month is omitted from clean outcome measurement.

## FIRST_HIKE support

- Mechanical tightening legs with clean monthly Gold support: 10
- +1M: n=10, median=0.015503, range=[-0.118126, 0.043642]
- +3M: n=10, median=0.005062, range=[-0.158859, 0.146409]
- +6M: n=10, median=-0.019022, range=[-0.160896, 0.174954]
- +12M: n=10, median=0.002436, range=[-0.197556, 0.219949]
- +24M: n=10, median=0.005754, range=[-0.360489, 0.552083]
- 24M MDD: n=10, median=0.166356, range=[0.038265, 0.391039]
- time-to-event-relative-min: n=10, median=4.500000, range=[0.000000, 24.000000]
- 50% recovery: n=8, median=6.000000, range=[2.000000, 19.000000]
- 100% recovery: n=6, median=12.000000, range=[6.000000, 30.000000]

## Cross-frequency audit

| cycle_id   |   cycle_start_year | event_date          |   world_bank_monthly_ret_12m |   world_bank_monthly_mdd_24m |   gc_f_daily_ret_252obs |   gc_f_daily_mdd_252obs | endpoint_sign_agrees   |
|:-----------|-------------------:|:--------------------|-----------------------------:|-----------------------------:|------------------------:|------------------------:|:-----------------------|
| T08_2004   |               2004 | 2004-06-30 00:00:00 |                    0.122396  |                     0.117037 |              0.0789809  |               0.0951754 | True                   |
| T09_2015   |               2015 | 2015-12-16 00:00:00 |                    0.0653775 |                     0.136567 |              0.0681156  |               0.173712  | True                   |
| T10_2022   |               2022 | 2022-03-16 00:00:00 |                    0.0307112 |                     0.14094  |             -0.00347202 |               0.178967  | False                  |

Different frequency/instrument results are diagnostic only and are never pooled.

## Full distribution summary

| event_type   | metric                         |   n |         mean |      median |         q25 |         q75 |        min |        max |
|:-------------|:-------------------------------|----:|-------------:|------------:|------------:|------------:|-----------:|-----------:|
| FIRST_CUT    | ret_1m                         |  10 |  0.0367245   |  0.0233885  | -0.00503654 |  0.0780919  | -0.0332103 |  0.135338  |
| FIRST_CUT    | ret_3m                         |  10 |  0.0153223   | -0.0185727  | -0.0472444  |  0.0623819  | -0.0804598 |  0.207519  |
| FIRST_CUT    | ret_6m                         |  10 |  0.0822735   |  0.0441753  | -0.0253482  |  0.137348   | -0.0977011 |  0.455639  |
| FIRST_CUT    | ret_12m                        |  10 |  0.0736963   | -0.0197766  | -0.0666825  |  0.196238   | -0.136476  |  0.48502   |
| FIRST_CUT    | ret_24m                        |   9 |  0.0745875   | -0.0107817  | -0.164948   |  0.317343   | -0.181141  |  0.498632  |
| FIRST_CUT    | mdd_24m                        |  10 |  0.183945    |  0.194323   |  0.144572   |  0.23556    |  0.0405904 |  0.274272  |
| FIRST_CUT    | mae                            |  10 | -0.105935    | -0.0960088  | -0.177904   | -0.0101476  | -0.258065  |  0         |
| FIRST_CUT    | mfe                            |  10 |  0.281367    |  0.162569   |  0.053871   |  0.41598    |  0.0223325 |  1.03239   |
| FIRST_CUT    | time_to_event_min_months       |  10 | 10.7         |  8.5        |  0.75       | 21          |  0         | 24         |
| FIRST_CUT    | recovery50_months_from_trough  |   6 |  4.66667     |  2          |  2          |  2.75       |  1         | 18         |
| FIRST_CUT    | recovery100_months_from_trough |   5 | 14.4         | 17          | 10          | 19          |  1         | 25         |
| FIRST_CUT    | rv_12m_ann                     |  10 |  0.114994    |  0.109414   |  0.0973991  |  0.130172   |  0.0506347 |  0.214054  |
| FIRST_CUT    | down_semivol_12m_ann           |  10 |  0.0744569   |  0.0937807  |  0.0310419  |  0.100644   |  0.0158283 |  0.137829  |
| FIRST_HIKE   | ret_1m                         |  10 | -0.00519895  |  0.0155027  | -0.011653   |  0.0248377  | -0.118126  |  0.0436422 |
| FIRST_HIKE   | ret_3m                         |  10 |  0.0134176   |  0.00506246 | -0.01942    |  0.0504391  | -0.158859  |  0.146409  |
| FIRST_HIKE   | ret_6m                         |  10 |  0.00268004  | -0.0190218  | -0.0871193  |  0.119622   | -0.160896  |  0.174954  |
| FIRST_HIKE   | ret_12m                        |  10 | -0.0097252   |  0.00243571 | -0.0993218  |  0.0580911  | -0.197556  |  0.219949  |
| FIRST_HIKE   | ret_24m                        |  10 |  0.0171061   |  0.00575448 | -0.109052   |  0.133665   | -0.360489  |  0.552083  |
| FIRST_HIKE   | mdd_24m                        |  10 |  0.183003    |  0.166356   |  0.13766    |  0.21882    |  0.0382653 |  0.391039  |
| FIRST_HIKE   | mae                            |  10 | -0.118986    | -0.087956   | -0.188264   | -0.00645995 | -0.391039  |  0         |
| FIRST_HIKE   | mfe                            |  10 |  0.167093    |  0.102208   |  0.0285962  |  0.216093   |  0         |  0.757812  |
| FIRST_HIKE   | time_to_event_min_months       |  10 |  8.6         |  4.5        |  0.25       | 16.25       |  0         | 24         |
| FIRST_HIKE   | recovery50_months_from_trough  |   8 |  7.5         |  6          |  3          | 10.25       |  2         | 19         |
| FIRST_HIKE   | recovery100_months_from_trough |   6 | 14.8333      | 12          | 10.25       | 17.5        |  6         | 30         |
| FIRST_HIKE   | rv_12m_ann                     |  10 |  0.116446    |  0.110595   |  0.0883769  |  0.135839   |  0.0513765 |  0.213069  |
| FIRST_HIKE   | down_semivol_12m_ann           |  10 |  0.0788807   |  0.0893408  |  0.0566603  |  0.0957628  |  0.0302207 |  0.128208  |
| LAST_HIKE    | ret_1m                         |  10 |  0.000815181 |  0.00829618 | -0.0203294  |  0.0221065  | -0.0607407 |  0.0581491 |
| LAST_HIKE    | ret_3m                         |  10 | -0.00784573  | -0.0155687  | -0.0420469  |  0.0433413  | -0.114074  |  0.0655201 |
| LAST_HIKE    | ret_6m                         |  10 | -0.00689469  | -0.0118419  | -0.0480459  |  0.0416365  | -0.140805  |  0.113022  |
| LAST_HIKE    | ret_12m                        |  10 |  0.0155654   | -0.0283598  | -0.0485587  |  0.0588713  | -0.136476  |  0.234174  |
| LAST_HIKE    | ret_24m                        |  10 |  0.105889    |  0.00651042 | -0.135834   |  0.268135   | -0.214751  |  0.718991  |
| LAST_HIKE    | mdd_24m                        |  10 |  0.150068    |  0.142007   |  0.101145   |  0.216438   |  0.0156134 |  0.274272  |
| LAST_HIKE    | mae                            |  10 | -0.115153    | -0.108142   | -0.149927   | -0.0744048  | -0.258065  |  0         |
| LAST_HIKE    | mfe                            |  10 |  0.231782    |  0.0977633  |  0.0722845  |  0.355913   |  0.0223325 |  0.725682  |
| LAST_HIKE    | time_to_event_min_months       |  10 | 12.6         | 12          |  4.5        | 22.5        |  0         | 24         |
| LAST_HIKE    | recovery50_months_from_trough  |   7 |  6.57143     |  3          |  2          | 10          |  1         | 18         |
| LAST_HIKE    | recovery100_months_from_trough |   6 | 13.5         | 13.5        |  7          | 18.5        |  1         | 28         |
| LAST_HIKE    | rv_12m_ann                     |  10 |  0.103675    |  0.104446   |  0.0982299  |  0.12531    |  0.0464842 |  0.131232  |
| LAST_HIKE    | down_semivol_12m_ann           |  10 |  0.0662537   |  0.0759356  |  0.03312    |  0.0950352  |  0.0126266 |  0.119246  |
| PAUSE_START  | ret_1m                         |   7 |  0.0117739   |  0.0254545  | -0.0122759  |  0.0411483  | -0.0567823 |  0.056     |
| PAUSE_START  | ret_3m                         |   7 |  0.00484744  | -0.00363636 | -0.0133526  |  0.0289889  | -0.0494624 |  0.0557582 |
| PAUSE_START  | ret_6m                         |   7 |  0.0191854   |  0.0159151  | -0.0223265  |  0.08672    | -0.140805  |  0.1304    |
| PAUSE_START  | ret_12m                        |   7 |  0.0744534   |  0.0488959  | -0.034953   |  0.149599   | -0.0967742 |  0.33976   |
| PAUSE_START  | ret_24m                        |   7 |  0.251423    |  0.167273   |  0.00851017 |  0.408472   | -0.152688  |  0.911412  |
| PAUSE_START  | mdd_24m                        |   7 |  0.117489    |  0.133264   |  0.067194   |  0.142007   |  0.0156134 |  0.255144  |
| PAUSE_START  | mae                            |   7 | -0.0819577   | -0.0757098  | -0.11019    | -0.0280544  | -0.221505  |  0         |
| PAUSE_START  | mfe                            |   7 |  0.340495    |  0.167273   |  0.0788019  |  0.551007   |  0.0451613 |  0.911412  |
| PAUSE_START  | time_to_event_min_months       |   7 |  9.14286     |  6          |  1.5        | 16          |  0         | 23         |
| PAUSE_START  | recovery50_months_from_trough  |   5 |  5           |  2          |  1          |  6          |  1         | 15         |
| PAUSE_START  | recovery100_months_from_trough |   5 | 12.8         | 13          |  5          | 17          |  1         | 28         |
| PAUSE_START  | rv_12m_ann                     |   7 |  0.0944938   |  0.102189   |  0.0831819  |  0.10598    |  0.0497129 |  0.131232  |
| PAUSE_START  | down_semivol_12m_ann           |   7 |  0.0502871   |  0.0367048  |  0.0288498  |  0.0721506  |  0.0125204 |  0.100783  |

## Evidence boundary

- DATA FACT: the monthly layer covers all frozen FIRST_HIKE tightening legs if QC passes.
- DESCRIPTIVE RESULT: monthly Gold paths expand breadth beyond the daily futures proxy.
- CAUSAL EVIDENCE: none.
- FDR: no confirmatory p-value family in this module.
- OOS: not applicable; this is not a forecasting model.
- DEPLOYMENT: none.