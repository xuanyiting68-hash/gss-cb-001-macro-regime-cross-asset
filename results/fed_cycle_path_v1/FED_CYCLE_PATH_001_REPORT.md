# FED-CYCLE-PATH-001 — Long-History Descriptive Foundation
Generated: 2026-09-23

## Evidence status

**DESCRIPTIVE RESULT / REALIZED POLICY ACTION IS NOT AN IDENTIFIED MONETARY-POLICY SHOCK / NOT A FORECASTING MODEL / NOT DEPLOYABLE**

This run follows research/FED_CYCLE_PATH_001_LOCK.md. No horizon or cycle rule was changed after seeing asset outcomes.

## Policy-cycle QC

- Qualifying tightening cycles: 10
- Cycle start years: 1983, 1984, 1987, 1987, 1988, 1994, 1999, 2004, 2015, 2022
- Total event-registry rows: 135
- Emergency-cut rows: 46
- QC gate: PASS

## Asset coverage

| asset     | kind   | first_date   | last_date   |   rows |   usable_event_rows | source                                                    |
|:----------|:-------|:-------------|:------------|-------:|--------------------:|:----------------------------------------------------------|
| GOLD      | price  | 2000-08-30   | 2026-09-23  |   6541 |                  29 | Yahoo Finance public chart history                        |
| SP500     | price  | 1970-01-02   | 2026-09-23  |  14302 |                 103 | Yahoo Finance public chart history                        |
| NASDAQ    | price  | 1971-02-05   | 2026-09-22  |  14025 |                 103 | Nasdaq, Inc. via FRED                                     |
| WTI       | price  | 1986-01-02   | 2026-09-22  |   9506 |                  80 | U.S. Energy Information Administration via FRED           |
| USD_BROAD | price  | 2006-01-02   | 2026-09-18  |   5193 |                  23 | Board of Governors of the Federal Reserve System via FRED |
| DGS2      | rate   | 1976-06-01   | 2026-09-21  |  12573 |                 103 | Board of Governors of the Federal Reserve System via FRED |
| DGS10     | rate   | 1962-01-02   | 2026-09-21  |  16165 |                 103 | Board of Governors of the Federal Reserve System via FRED |
| DFII10    | rate   | 2003-01-02   | 2026-09-21  |   5934 |                  25 | Board of Governors of the Federal Reserve System via FRED |
| T5YIE     | rate   | 2003-01-02   | 2026-09-22  |   5935 |                  25 | Federal Reserve Bank of St. Louis via FRED                |

## Gold — FIRST_HIKE distribution

- 20D endpoint return: n=3, median=1.03%, IQR=[0.07, 2.49]%
- 60D endpoint return: n=3, median=4.69%, IQR=[1.46, 10.88]%
- 120D endpoint return: n=3, median=12.71%, IQR=[1.61, 15.62]%
- 252D endpoint return: n=3, median=6.81%, IQR=[5.09, 7.35]%
- 252-observation maximum drawdown: n=3, median=17.37%, IQR=[13.44, 17.63]%
- time to event-relative trough (obs): n=3, median=19.00, IQR=[10.50, 90.00]
- 50% recovery from MDD trough (obs): n=3, median=19.00, IQR=[14.00, 32.50]
- 100% recovery from MDD trough (obs): n=3, median=150.00, IQR=[122.50, 389.50]
- Full-recovery right-censored observations: 0

## Gold — 2015 and 2022 inside the same frozen framework

| cycle_id   |   cycle_start_year | event_type   | event_date          |     ret_20d |     ret_60d |   ret_120d |   ret_252d |       mdd |         mae |       mfe |   time_to_event_min_obs |   time_to_event_max_obs |   recovery50_obs_from_trough | recovery50_observed   |   recovery100_obs_from_trough | recovery100_observed   |   rv_60d_ann |   down_semivol_60d_ann |
|:-----------|-------------------:|:-------------|:--------------------|------------:|------------:|-----------:|-----------:|----------:|------------:|----------:|------------------------:|------------------------:|-----------------------------:|:----------------------|------------------------------:|:-----------------------|-------------:|-----------------------:|
| T09_2015   |               2015 | FIRST_HIKE   | 2015-12-16 00:00:00 |  0.010349   |  0.170759   |  0.185248  |  0.0681156 | 0.173712  | -0.0113839  | 0.284128  |                       2 |                     139 |                           46 | True                  |                           629 | True                   |    0.198424  |              0.111801  |
| T09_2015   |               2015 | LAST_HIKE    | 2018-12-20 00:00:00 |  0.0233209  |  0.042249   |  0.0695631 |  0.180577  | 0.0633426 |  0          | 0.23816   |                       0 |                     177 |                           30 | True                  |                            36 | True                   |    0.096918  |              0.0624446 |
| T09_2015   |               2015 | PAUSE_START  | 2019-01-30 00:00:00 |  0.00726189 | -0.0247668  |  0.0895124 |  0.19997   | 0.0633426 | -0.0297354  | 0.20532   |                      58 |                     250 |                           30 | True                  |                            36 | True                   |    0.0991163 |              0.0773482 |
| T09_2015   |               2015 | FIRST_CUT    | 2019-08-01 00:00:00 |  0.0783256  |  0.0510483  |  0.0905968 |  0.361966  | 0.117766  | -0.00364627 | 0.36975   |                       1 |                     251 |                            4 | True                  |                            13 | True                   |    0.142596  |              0.0933909 |
| T10_2022   |               2022 | FIRST_HIKE   | 2022-03-17 00:00:00 |  0.0395454  | -0.0176513  | -0.0950136 |  0.0336791 | 0.178967  | -0.145768   | 0.0404358 |                     161 |                      22 |                           19 | True                  |                            95 | True                   |    0.142577  |              0.108523  |
| T10_2022   |               2022 | LAST_HIKE    | 2023-07-27 00:00:00 | -0.0111669  |  0.00527893 |  0.0305061 |  0.194609  | 0.0742874 | -0.0701994  | 0.252627  |                      50 |                     245 |                            6 | True                  |                            10 | True                   |    0.116914  |              0.0714055 |
| T10_2022   |               2022 | PAUSE_START  | 2023-09-20 00:00:00 | -0.00921329 |  0.020218   |  0.120233  |  0.330092  | 0.0687814 | -0.0623944  | 0.336285  |                      12 |                     249 |                            6 | True                  |                             9 | True                   |    0.14776   |              0.0955848 |
| T10_2022   |               2022 | FIRST_CUT    | 2024-09-19 00:00:00 |  0.035673   |  0.0426383  |  0.133995  |  0.415493  | 0.0823693 | -0.0109674  | 0.433503  |                      42 |                     250 |                            5 | True                  |                            50 | True                   |    0.167312  |              0.132195  |

These two episodes are highlighted for interpretation only; they were not given different windows or thresholds.

## Distribution table

| asset   | event_type             | metric                      |   n |         mean |        median |           q25 |           q75 |         min |          max |
|:--------|:-----------------------|:----------------------------|----:|-------------:|--------------:|--------------:|--------------:|------------:|-------------:|
| GOLD    | EMERGENCY_CUT          | ret_20d                     |  10 |   0.0262798  |   0.0339638   |  -0.0163055   |   0.0620326   | -0.139344   |   0.151151   |
| GOLD    | EMERGENCY_CUT          | ret_60d                     |  10 |   0.0847474  |   0.0581805   |   0.00560768  |   0.154082    | -0.0620262  |   0.270428   |
| GOLD    | EMERGENCY_CUT          | ret_120d                    |  10 |   0.137426   |   0.0917837   |   0.054326    |   0.184456    |  0.011716   |   0.393055   |
| GOLD    | EMERGENCY_CUT          | ret_252d                    |   8 |   0.108363   |   0.126253    |   0.0531355   |   0.171022    | -0.0297457  |   0.190193   |
| GOLD    | EMERGENCY_CUT          | mdd                         |  10 |   0.186081   |   0.204302    |   0.102217    |   0.249379    |  0.0771812  |   0.297348   |
| GOLD    | EMERGENCY_CUT          | mae                         |  10 |  -0.0710226  |  -0.052305    |  -0.090776    |  -0.0143021   | -0.199705   |   0          |
| GOLD    | EMERGENCY_CUT          | mfe                         |  10 |   0.236491   |   0.223305    |   0.147119    |   0.312079    |  0.092772   |   0.430523   |
| GOLD    | EMERGENCY_CUT          | time_to_event_min_obs       |  10 |  49.2        |  19           |   3.25        |  52           |  0          | 208          |
| GOLD    | EMERGENCY_CUT          | recovery50_obs_from_trough  |  10 |  26.6        |  26           |  14           |  26.75        |  7          |  58          |
| GOLD    | EMERGENCY_CUT          | recovery100_obs_from_trough |   7 | 256.429      |  95           |  39           | 449           | 30          | 694          |
| GOLD    | EMERGENCY_CUT          | rv_60d_ann                  |  10 |   0.243201   |   0.243755    |   0.185378    |   0.294823    |  0.105327   |   0.377006   |
| GOLD    | EMERGENCY_CUT          | down_semivol_60d_ann        |  10 |   0.164072   |   0.163172    |   0.111714    |   0.184929    |  0.0881382  |   0.285754   |
| GOLD    | FIRST_CUT              | ret_20d                     |   4 |   0.040316   |   0.0466853   |   0.0241467   |   0.0628546   | -0.0104321  |   0.0783256  |
| GOLD    | FIRST_CUT              | ret_60d                     |   4 |   0.047869   |   0.0468433   |   0.0230368   |   0.0716755   | -0.0357675  |   0.133557   |
| GOLD    | FIRST_CUT              | ret_120d                    |   4 |   0.149832   |   0.112296    |   0.0728843   |   0.189243    |  0.0197467  |   0.354987   |
| GOLD    | FIRST_CUT              | ret_252d                    |   4 |   0.229537   |   0.223383    |   0.0775719   |   0.375348    |  0.0558867  |   0.415493   |
| GOLD    | FIRST_CUT              | mdd                         |   4 |   0.135133   |   0.100068    |   0.08161     |   0.153591    |  0.0793319  |   0.261065   |
| GOLD    | FIRST_CUT              | mae                         |   4 |  -0.0160416  |  -0.00730686  |  -0.0206138   |  -0.00273471  | -0.0495529  |   0          |
| GOLD    | FIRST_CUT              | mfe                         |   4 |   0.324383   |   0.385629    |   0.300505    |   0.409507    |  0.092772   |   0.433503   |
| GOLD    | FIRST_CUT              | time_to_event_min_obs       |   4 |  18.5        |  16           |   0.75        |  33.75        |  0          |  42          |
| GOLD    | FIRST_CUT              | recovery50_obs_from_trough  |   4 |   6.25       |   5           |   4.75        |   6.5         |  4          |  11          |
| GOLD    | FIRST_CUT              | recovery100_obs_from_trough |   4 |  86.25       |  40           |  25.75        | 100.5         | 13          | 252          |
| GOLD    | FIRST_CUT              | rv_60d_ann                  |   4 |   0.157923   |   0.154954    |   0.138078    |   0.174799    |  0.124522   |   0.197263   |
| GOLD    | FIRST_CUT              | down_semivol_60d_ann        |   4 |   0.112125   |   0.112793    |   0.0923174   |   0.132601    |  0.0890967  |   0.13382    |
| GOLD    | FIRST_HIKE             | ret_20d                     |   3 |   0.0136591  |   0.010349    |   0.000715924 |   0.0249472   | -0.0089172  |   0.0395454  |
| GOLD    | FIRST_HIKE             | ret_60d                     |   3 |   0.0666623  |   0.046879    |   0.0146138   |   0.108819    | -0.0176513  |   0.170759   |
| GOLD    | FIRST_HIKE             | ret_120d                    |   3 |   0.072456   |   0.127134    |   0.0160601   |   0.156191    | -0.0950136  |   0.185248   |
| GOLD    | FIRST_HIKE             | ret_252d                    |   3 |   0.0602585  |   0.0681156   |   0.0508973   |   0.0735482   |  0.0336791  |   0.0789809  |
| GOLD    | FIRST_HIKE             | mdd                         |   3 |   0.149285   |   0.173712    |   0.134444    |   0.17634     |  0.0951754  |   0.178967   |
| GOLD    | FIRST_HIKE             | mae                         |   3 |  -0.0570548  |  -0.0140127   |  -0.0798903   |  -0.0126983   | -0.145768   |  -0.0113839  |
| GOLD    | FIRST_HIKE             | mfe                         |   3 |   0.162116   |   0.161783    |   0.10111     |   0.222956    |  0.0404358  |   0.284128   |
| GOLD    | FIRST_HIKE             | time_to_event_min_obs       |   3 |  60.6667     |  19           |  10.5         |  90           |  2          | 161          |
| GOLD    | FIRST_HIKE             | recovery50_obs_from_trough  |   3 |  24.6667     |  19           |  14           |  32.5         |  9          |  46          |
| GOLD    | FIRST_HIKE             | recovery100_obs_from_trough |   3 | 291.333      | 150           | 122.5         | 389.5         | 95          | 629          |
| GOLD    | FIRST_HIKE             | rv_60d_ann                  |   3 |   0.160009   |   0.142577    |   0.140801    |   0.170501    |  0.139026   |   0.198424   |
| GOLD    | FIRST_HIKE             | down_semivol_60d_ann        |   3 |   0.103358   |   0.108523    |   0.0991359   |   0.110162    |  0.0897491  |   0.111801   |
| GOLD    | LAST_HIKE              | ret_20d                     |   3 |   0.036618   |   0.0233209   |   0.00607697  |   0.0605105   | -0.0111669  |   0.0977002  |
| GOLD    | LAST_HIKE              | ret_60d                     |   3 |   0.0222407  |   0.0191943   |   0.0122366   |   0.0307216   |  0.00527893 |   0.042249   |
| GOLD    | LAST_HIKE              | ret_120d                    |   3 |   0.0583146  |   0.0695631   |   0.0500346   |   0.0722189   |  0.0305061  |   0.0748746  |
| GOLD    | LAST_HIKE              | ret_252d                    |   3 |   0.165295   |   0.180577    |   0.150638    |   0.187593    |  0.120699   |   0.194609   |
| GOLD    | LAST_HIKE              | mdd                         |   3 |   0.0981819  |   0.0742874   |   0.068815    |   0.115602    |  0.0633426  |   0.156916   |
| GOLD    | LAST_HIKE              | mae                         |   3 |  -0.0327952  |  -0.028186    |  -0.0491927   |  -0.014093    | -0.0701994  |   0          |
| GOLD    | LAST_HIKE              | mfe                         |   3 |   0.229133   |   0.23816     |   0.217385    |   0.245393    |  0.196611   |   0.252627   |
| GOLD    | LAST_HIKE              | time_to_event_min_obs       |   3 |  39.3333     |  50           |  25           |  59           |  0          |  68          |
| GOLD    | LAST_HIKE              | recovery50_obs_from_trough  |   3 |  18.6667     |  20           |  13           |  25           |  6          |  30          |
| GOLD    | LAST_HIKE              | recovery100_obs_from_trough |   3 |  44.3333     |  36           |  23           |  61.5         | 10          |  87          |
| GOLD    | LAST_HIKE              | rv_60d_ann                  |   3 |   0.153774   |   0.116914    |   0.106916    |   0.182201    |  0.096918   |   0.247488   |
| GOLD    | LAST_HIKE              | down_semivol_60d_ann        |   3 |   0.101348   |   0.0714055   |   0.066925    |   0.1208      |  0.0624446  |   0.170195   |
| GOLD    | PAUSE_START            | ret_20d                     |   3 |  -0.0126912  |  -0.00921329  |  -0.0226677   |  -0.000975701 | -0.0361222  |   0.00726189 |
| GOLD    | PAUSE_START            | ret_60d                     |   3 |  -0.0236939  |  -0.0247668   |  -0.0456498   |  -0.00227437  | -0.0665328  |   0.020218   |
| GOLD    | PAUSE_START            | ret_120d                    |   3 |   0.0674968  |   0.0895124   |   0.0411285   |   0.104873    | -0.00725534 |   0.120233   |
| GOLD    | PAUSE_START            | ret_252d                    |   3 |   0.188419   |   0.19997     |   0.117583    |   0.265031    |  0.035196   |   0.330092   |
| GOLD    | PAUSE_START            | mdd                         |   3 |   0.0893911  |   0.0687814   |   0.066062    |   0.102415    |  0.0633426  |   0.136049   |
| GOLD    | PAUSE_START            | mae                         |   3 |  -0.0748594  |  -0.0623944   |  -0.0974213   |  -0.0460649   | -0.132448   |  -0.0297354  |
| GOLD    | PAUSE_START            | mfe                         |   3 |   0.203279   |   0.20532     |   0.136776    |   0.270803    |  0.068231   |   0.336285   |
| GOLD    | PAUSE_START            | time_to_event_min_obs       |   3 |  37.3333     |  42           |  27           |  50           | 12          |  58          |
| GOLD    | PAUSE_START            | recovery50_obs_from_trough  |   3 |  18.6667     |  20           |  13           |  25           |  6          |  30          |
| GOLD    | PAUSE_START            | recovery100_obs_from_trough |   3 |  41.6667     |  36           |  22.5         |  58           |  9          |  80          |
| GOLD    | PAUSE_START            | rv_60d_ann                  |   3 |   0.1539     |   0.14776     |   0.123438    |   0.181292    |  0.0991163  |   0.214825   |
| GOLD    | PAUSE_START            | down_semivol_60d_ann        |   3 |   0.114538   |   0.0955848   |   0.0864665   |   0.133132    |  0.0773482  |   0.17068    |
| GOLD    | TIGHTENING_CYCLE_END   | ret_20d                     |   3 |   0.036618   |   0.0233209   |   0.00607697  |   0.0605105   | -0.0111669  |   0.0977002  |
| GOLD    | TIGHTENING_CYCLE_END   | ret_60d                     |   3 |   0.0222407  |   0.0191943   |   0.0122366   |   0.0307216   |  0.00527893 |   0.042249   |
| GOLD    | TIGHTENING_CYCLE_END   | ret_120d                    |   3 |   0.0583146  |   0.0695631   |   0.0500346   |   0.0722189   |  0.0305061  |   0.0748746  |
| GOLD    | TIGHTENING_CYCLE_END   | ret_252d                    |   3 |   0.165295   |   0.180577    |   0.150638    |   0.187593    |  0.120699   |   0.194609   |
| GOLD    | TIGHTENING_CYCLE_END   | mdd                         |   3 |   0.0981819  |   0.0742874   |   0.068815    |   0.115602    |  0.0633426  |   0.156916   |
| GOLD    | TIGHTENING_CYCLE_END   | mae                         |   3 |  -0.0327952  |  -0.028186    |  -0.0491927   |  -0.014093    | -0.0701994  |   0          |
| GOLD    | TIGHTENING_CYCLE_END   | mfe                         |   3 |   0.229133   |   0.23816     |   0.217385    |   0.245393    |  0.196611   |   0.252627   |
| GOLD    | TIGHTENING_CYCLE_END   | time_to_event_min_obs       |   3 |  39.3333     |  50           |  25           |  59           |  0          |  68          |
| GOLD    | TIGHTENING_CYCLE_END   | recovery50_obs_from_trough  |   3 |  18.6667     |  20           |  13           |  25           |  6          |  30          |
| GOLD    | TIGHTENING_CYCLE_END   | recovery100_obs_from_trough |   3 |  44.3333     |  36           |  23           |  61.5         | 10          |  87          |
| GOLD    | TIGHTENING_CYCLE_END   | rv_60d_ann                  |   3 |   0.153774   |   0.116914    |   0.106916    |   0.182201    |  0.096918   |   0.247488   |
| GOLD    | TIGHTENING_CYCLE_END   | down_semivol_60d_ann        |   3 |   0.101348   |   0.0714055   |   0.066925    |   0.1208      |  0.0624446  |   0.170195   |
| GOLD    | TIGHTENING_CYCLE_START | ret_20d                     |   3 |   0.0136591  |   0.010349    |   0.000715924 |   0.0249472   | -0.0089172  |   0.0395454  |
| GOLD    | TIGHTENING_CYCLE_START | ret_60d                     |   3 |   0.0666623  |   0.046879    |   0.0146138   |   0.108819    | -0.0176513  |   0.170759   |
| GOLD    | TIGHTENING_CYCLE_START | ret_120d                    |   3 |   0.072456   |   0.127134    |   0.0160601   |   0.156191    | -0.0950136  |   0.185248   |
| GOLD    | TIGHTENING_CYCLE_START | ret_252d                    |   3 |   0.0602585  |   0.0681156   |   0.0508973   |   0.0735482   |  0.0336791  |   0.0789809  |
| GOLD    | TIGHTENING_CYCLE_START | mdd                         |   3 |   0.149285   |   0.173712    |   0.134444    |   0.17634     |  0.0951754  |   0.178967   |
| GOLD    | TIGHTENING_CYCLE_START | mae                         |   3 |  -0.0570548  |  -0.0140127   |  -0.0798903   |  -0.0126983   | -0.145768   |  -0.0113839  |
| GOLD    | TIGHTENING_CYCLE_START | mfe                         |   3 |   0.162116   |   0.161783    |   0.10111     |   0.222956    |  0.0404358  |   0.284128   |
| GOLD    | TIGHTENING_CYCLE_START | time_to_event_min_obs       |   3 |  60.6667     |  19           |  10.5         |  90           |  2          | 161          |
| GOLD    | TIGHTENING_CYCLE_START | recovery50_obs_from_trough  |   3 |  24.6667     |  19           |  14           |  32.5         |  9          |  46          |
| GOLD    | TIGHTENING_CYCLE_START | recovery100_obs_from_trough |   3 | 291.333      | 150           | 122.5         | 389.5         | 95          | 629          |
| GOLD    | TIGHTENING_CYCLE_START | rv_60d_ann                  |   3 |   0.160009   |   0.142577    |   0.140801    |   0.170501    |  0.139026   |   0.198424   |
| GOLD    | TIGHTENING_CYCLE_START | down_semivol_60d_ann        |   3 |   0.103358   |   0.108523    |   0.0991359   |   0.110162    |  0.0897491  |   0.111801   |
| NASDAQ  | EMERGENCY_CUT          | ret_20d                     |  46 |   0.0292781  |   0.0178013   |  -0.0128536   |   0.0416894   | -0.115996   |   0.209816   |
| NASDAQ  | EMERGENCY_CUT          | ret_60d                     |  46 |   0.0774101  |   0.0646935   |  -0.0152154   |   0.16156     | -0.256459   |   0.54746    |
| NASDAQ  | EMERGENCY_CUT          | ret_120d                    |  46 |   0.133578   |   0.12023     |   0.00923914  |   0.215257    | -0.203309   |   0.669981   |
| NASDAQ  | EMERGENCY_CUT          | ret_252d                    |  44 |   0.210272   |   0.18907     |   0.104485    |   0.320471    | -0.384253   |   0.821476   |
| NASDAQ  | EMERGENCY_CUT          | mdd                         |  46 |   0.166571   |   0.129742    |   0.10014     |   0.164145    |  0.0747687  |   0.502233   |
| NASDAQ  | EMERGENCY_CUT          | mae                         |  46 |  -0.0930484  |  -0.0404461   |  -0.122741    |  -0.01474     | -0.43756    |   0          |
| NASDAQ  | EMERGENCY_CUT          | mfe                         |  46 |   0.310299   |   0.245691    |   0.187887    |   0.376244    |  0.0162321  |   0.892282   |
| NASDAQ  | EMERGENCY_CUT          | time_to_event_min_obs       |  46 |  62.8913     |  39           |   4.5         | 104           |  0          | 251          |
| NASDAQ  | EMERGENCY_CUT          | recovery50_obs_from_trough  |  46 |  97.2174     |  35           |  11           |  81           |  1          | 589          |
| NASDAQ  | EMERGENCY_CUT          | recovery100_obs_from_trough |  44 | 133.136      |  71           |  32.75        | 105           | 10          | 595          |
| NASDAQ  | EMERGENCY_CUT          | rv_60d_ann                  |  46 |   0.184429   |   0.144285    |   0.112392    |   0.169247    |  0.0702516  |   0.658171   |
| NASDAQ  | EMERGENCY_CUT          | down_semivol_60d_ann        |  46 |   0.124863   |   0.0919267   |   0.0733219   |   0.121092    |  0.0267382  |   0.46213    |
| NASDAQ  | FIRST_CUT              | ret_20d                     |  10 |   0.0255829  |   0.00821336  |  -0.0256781   |   0.0450073   | -0.0481507  |   0.209816   |
| NASDAQ  | FIRST_CUT              | ret_60d                     |  10 |   0.00697913 |   0.034211    |  -0.0439397   |   0.06659     | -0.205636   |   0.132561   |
| NASDAQ  | FIRST_CUT              | ret_120d                    |  10 |  -0.0077081  |   0.000459872 |  -0.129364    |   0.112106    | -0.225675   |   0.17832    |
| NASDAQ  | FIRST_CUT              | ret_252d                    |  10 |   0.0710232  |   0.0752327   |  -0.0965878   |   0.246645    | -0.164149   |   0.296796   |
| NASDAQ  | FIRST_CUT              | mdd                         |  10 |   0.23294    |   0.24222     |   0.115516    |   0.290929    |  0.0786303  |   0.502233   |
| NASDAQ  | FIRST_CUT              | mae                         |  10 |  -0.162012   |  -0.145449    |  -0.226673    |  -0.0837923   | -0.379024   |   0          |
| NASDAQ  | FIRST_CUT              | mfe                         |  10 |   0.191972   |   0.225865    |   0.090323    |   0.284478    |  0.0157079  |   0.326315   |
| NASDAQ  | FIRST_CUT              | time_to_event_min_obs       |  10 | 116.7        | 129           |  65.75        | 165           |  0          | 238          |
| NASDAQ  | FIRST_CUT              | recovery50_obs_from_trough  |  10 | 100.2        |  40           |  15.5         |  85.75        |  5          | 589          |
| NASDAQ  | FIRST_CUT              | recovery100_obs_from_trough |   8 | 148.5        |  54           |  43.25        | 258.25        | 10          | 446          |
| NASDAQ  | FIRST_CUT              | rv_60d_ann                  |  10 |   0.182259   |   0.157377    |   0.092645    |   0.206048    |  0.0702516  |   0.538738   |
| NASDAQ  | FIRST_CUT              | down_semivol_60d_ann        |  10 |   0.131237   |   0.102973    |   0.0697638   |   0.151152    |  0.0532822  |   0.389925   |
| NASDAQ  | FIRST_HIKE             | ret_20d                     |  10 |   0.00198393 |   0.00311744  |  -0.0281563   |   0.0219428   | -0.0827444  |   0.109834   |
| NASDAQ  | FIRST_HIKE             | ret_60d                     |  10 |  -0.0189463  |  -0.0442511   |  -0.0739495   |   0.0465303   | -0.310438   |   0.214766   |
| NASDAQ  | FIRST_HIKE             | ret_120d                    |  10 |   0.0385073  |   0.0199858   |  -0.0812836   |   0.102276    | -0.219611   |   0.420478   |
| NASDAQ  | FIRST_HIKE             | ret_252d                    |  10 |   0.0274793  |  -0.00820226  |  -0.0708355   |   0.0868634   | -0.174032   |   0.46056    |
| NASDAQ  | FIRST_HIKE             | mdd                         |  10 |   0.227812   |   0.206713    |   0.139621    |   0.344504    |  0.0783621  |   0.373185   |
| NASDAQ  | FIRST_HIKE             | mae                         |  10 |  -0.146202   |  -0.135142    |  -0.166775    |  -0.091172    | -0.358872   |  -0.0260082  |
| NASDAQ  | FIRST_HIKE             | mfe                         |  10 |   0.191969   |   0.0958904   |   0.0738161   |   0.198264    |  0          |   0.910829   |
| NASDAQ  | FIRST_HIKE             | time_to_event_min_obs       |  10 |  99.4        |  63           |  38.25        | 172.75        | 29          | 228          |
| NASDAQ  | FIRST_HIKE             | recovery50_obs_from_trough  |  10 |  66.2        |  38.5         |  22.5         |  89           |  7          | 244          |
| NASDAQ  | FIRST_HIKE             | recovery100_obs_from_trough |   9 | 225.333      | 181           |  64           | 446           | 19          | 472          |
| NASDAQ  | FIRST_HIKE             | rv_60d_ann                  |  10 |   0.209069   |   0.179228    |   0.10737     |   0.254362    |  0.100732   |   0.459768   |
| NASDAQ  | FIRST_HIKE             | down_semivol_60d_ann        |  10 |   0.160485   |   0.141335    |   0.076374    |   0.181053    |  0.0535772  |   0.410234   |

## Interpretation boundary

- DATA FACT: the cycle registry is mechanically derived from target-rate changes plus scheduled-meeting dates.
- DESCRIPTIVE RESULT: asset paths, drawdowns, volatility and recovery are historical distributions around those markers.
- NOT CAUSAL: this module does not identify target/path/information monetary shocks.
- FDR: no confirmatory p-value family is executed in this foundation run; future confirmatory families are predeclared in the lock.
- OOS: not applicable to this descriptive foundation; no forecasting claim is made.
- Investment implication: use the output as a risk-distribution and timing map, not as a deterministic trade rule.