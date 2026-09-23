# FED-CYCLE-PATH-001 v1.1 — Timing-Corrected Long-History Descriptive Foundation
Generated: 2026-09-23

## Evidence status

**DESCRIPTIVE RESULT / REALIZED POLICY ACTION IS NOT AN IDENTIFIED MONETARY-POLICY SHOCK / NOT A FORECASTING MODEL / NOT DEPLOYABLE**

This run follows research/FED_CYCLE_PATH_001_LOCK.md plus research/FED_CYCLE_PATH_001_V1_1_TIMING_LOCK.md. v1 is quarantined; v1.1 corrects timing ontology without changing horizons or path-risk definitions.

## Policy-cycle QC

- Qualifying tightening cycles: 10
- Cycle start years: 1983, 1984, 1987, 1987, 1988, 1994, 1999, 2004, 2015, 2022
- Total event-registry rows: 97
- Timing-unresolved emergency-cut candidates (registry only): 8
- QC gate: PASS

## Asset coverage

| asset     | kind   | first_date   | last_date   |   rows |   usable_event_rows | source                                                    |
|:----------|:-------|:-------------|:------------|-------:|--------------------:|:----------------------------------------------------------|
| GOLD      | price  | 2000-08-30   | 2026-09-23  |   6541 |                  19 | Yahoo Finance public chart history                        |
| SP500     | price  | 1970-01-02   | 2026-09-23  |  14302 |                  57 | Yahoo Finance public chart history                        |
| NASDAQ    | price  | 1971-02-05   | 2026-09-22  |  14025 |                  57 | Nasdaq, Inc. via FRED                                     |
| WTI       | price  | 1986-01-02   | 2026-09-22  |   9506 |                  46 | U.S. Energy Information Administration via FRED           |
| USD_BROAD | price  | 2006-01-02   | 2026-09-18  |   5193 |                  16 | Board of Governors of the Federal Reserve System via FRED |
| DGS2      | rate   | 1976-06-01   | 2026-09-21  |  12573 |                  57 | Board of Governors of the Federal Reserve System via FRED |
| DGS10     | rate   | 1962-01-02   | 2026-09-21  |  16165 |                  57 | Board of Governors of the Federal Reserve System via FRED |
| DFII10    | rate   | 2003-01-02   | 2026-09-21  |   5934 |                  18 | Board of Governors of the Federal Reserve System via FRED |
| T5YIE     | rate   | 2003-01-02   | 2026-09-22  |   5935 |                  18 | Federal Reserve Bank of St. Louis via FRED                |

## Gold — FIRST_HIKE distribution

- 20D endpoint return: n=3, median=1.03%, IQR=[0.07, 1.72]%
- 60D endpoint return: n=3, median=4.69%, IQR=[0.35, 10.88]%
- 120D endpoint return: n=3, median=12.71%, IQR=[0.74, 15.62]%
- 252D endpoint return: n=3, median=6.81%, IQR=[3.23, 7.35]%
- 252-observation maximum drawdown: n=3, median=17.37%, IQR=[13.44, 17.63]%
- time to event-relative trough (obs): n=3, median=19.00, IQR=[10.50, 90.50]
- 50% recovery from MDD trough (obs): n=3, median=19.00, IQR=[14.00, 32.50]
- 100% recovery from MDD trough (obs): n=3, median=150.00, IQR=[122.50, 389.50]
- Full-recovery right-censored observations: 0

## Gold — 2015 and 2022 inside the same frozen framework

| cycle_id   |   cycle_start_year | event_type   | event_date          |     ret_20d |     ret_60d |   ret_120d |    ret_252d |       mdd |         mae |       mfe |   time_to_event_min_obs |   time_to_event_max_obs |   recovery50_obs_from_trough | recovery50_observed   |   recovery100_obs_from_trough | recovery100_observed   |   rv_60d_ann |   down_semivol_60d_ann |
|:-----------|-------------------:|:-------------|:--------------------|------------:|------------:|-----------:|------------:|----------:|------------:|----------:|------------------------:|------------------------:|-----------------------------:|:----------------------|------------------------------:|:-----------------------|-------------:|-----------------------:|
| T09_2015   |               2015 | FIRST_HIKE   | 2015-12-16 00:00:00 |  0.010349   |  0.170759   |  0.185248  |  0.0681156  | 0.173712  | -0.0113839  | 0.284128  |                       2 |                     139 |                           46 | True                  |                           629 | True                   |    0.198424  |              0.111801  |
| T09_2015   |               2015 | LAST_HIKE    | 2018-12-19 00:00:00 |  0.0334615  |  0.0409063  |  0.0662024 |  0.178834   | 0.0633426 |  0          | 0.241034  |                       0 |                     178 |                           30 | True                  |                            36 | True                   |    0.0967881 |              0.0624446 |
| T09_2015   |               2015 | PAUSE_START  | 2019-01-30 00:00:00 |  0.00726189 | -0.0247668  |  0.0895124 |  0.19997    | 0.0633426 | -0.0297354  | 0.20532   |                      58 |                     250 |                           30 | True                  |                            36 | True                   |    0.0991163 |              0.0773482 |
| T09_2015   |               2015 | FIRST_CUT    | 2019-07-31 00:00:00 |  0.0778485  |  0.0421068  |  0.08862   |  0.366301   | 0.117766  | -0.00615509 | 0.366301  |                       2 |                     252 |                            4 | True                  |                            13 | True                   |    0.142342  |              0.0935338 |
| T10_2022   |               2022 | FIRST_HIKE   | 2022-03-16 00:00:00 |  0.0240452  | -0.0398507  | -0.112349  | -0.00347202 | 0.178967  | -0.154843   | 0.0293828 |                     162 |                      23 |                           19 | True                  |                            95 | True                   |    0.141729  |              0.110708  |
| T10_2022   |               2022 | LAST_HIKE    | 2023-07-26 00:00:00 | -0.0191984  |  0.00234257 |  0.0447625 |  0.230178   | 0.0742874 | -0.0671691  | 0.256709  |                      51 |                     246 |                            6 | True                  |                            10 | True                   |    0.116416  |              0.0714055 |
| T10_2022   |               2022 | PAUSE_START  | 2023-09-20 00:00:00 | -0.00921329 |  0.020218   |  0.120233  |  0.330092   | 0.0687814 | -0.0623944  | 0.336285  |                      12 |                     249 |                            6 | True                  |                             9 | True                   |    0.14776   |              0.0955848 |
| T10_2022   |               2022 | FIRST_CUT    | 2024-09-18 00:00:00 |  0.0333668  |  0.0633776  |  0.126717  |  0.434115   | 0.0823693 | -0.00860199 | 0.436931  |                      43 |                     251 |                            5 | True                  |                            50 | True                   |    0.163075  |              0.127348  |

These two episodes are highlighted for interpretation only; they were not given different windows or thresholds.

## Distribution table

| asset   | event_type             | metric                      |   n |          mean |       median |           q25 |           q75 |         min |          max |
|:--------|:-----------------------|:----------------------------|----:|--------------:|-------------:|--------------:|--------------:|------------:|-------------:|
| GOLD    | FIRST_CUT              | ret_20d                     |   4 |   0.0396202   |   0.0455322  |   0.022417    |   0.0627354   | -0.0104321  |   0.0778485  |
| GOLD    | FIRST_CUT              | ret_60d                     |   4 |   0.0508184   |   0.0527422  |   0.0226382   |   0.0809224   | -0.0357675  |   0.133557   |
| GOLD    | FIRST_CUT              | ret_120d                    |   4 |   0.147518    |   0.107668   |   0.0714017   |   0.183784    |  0.0197467  |   0.354987   |
| GOLD    | FIRST_CUT              | ret_252d                    |   4 |   0.235276    |   0.22555    |   0.0775719   |   0.383254    |  0.0558867  |   0.434115   |
| GOLD    | FIRST_CUT              | mdd                         |   4 |   0.135133    |   0.100068   |   0.08161     |   0.153591    |  0.0793319  |   0.261065   |
| GOLD    | FIRST_CUT              | mae                         |   4 |  -0.0160775   |  -0.00737854 |  -0.0188397   |  -0.00461631  | -0.0495529  |   0          |
| GOLD    | FIRST_CUT              | mfe                         |   4 |   0.324378    |   0.383905   |   0.297919    |   0.410364    |  0.092772   |   0.436931   |
| GOLD    | FIRST_CUT              | time_to_event_min_obs       |   4 |  19           |  16.5        |   1.5         |  34           |  0          |  43          |
| GOLD    | FIRST_CUT              | recovery50_obs_from_trough  |   4 |   6.25        |   5          |   4.75        |   6.5         |  4          |  11          |
| GOLD    | FIRST_CUT              | recovery100_obs_from_trough |   4 |  86.25        |  40          |  25.75        | 100.5         | 13          | 252          |
| GOLD    | FIRST_CUT              | rv_60d_ann                  |   4 |   0.156801    |   0.152708   |   0.137887    |   0.171622    |  0.124522   |   0.197263   |
| GOLD    | FIRST_CUT              | down_semivol_60d_ann        |   4 |   0.110949    |   0.110441   |   0.0924245   |   0.128966    |  0.0890967  |   0.13382    |
| GOLD    | FIRST_HIKE             | ret_20d                     |   3 |   0.00849235  |   0.010349   |   0.000715924 |   0.0171971   | -0.0089172  |   0.0240452  |
| GOLD    | FIRST_HIKE             | ret_60d                     |   3 |   0.0592625   |   0.046879   |   0.00351413  |   0.108819    | -0.0398507  |   0.170759   |
| GOLD    | FIRST_HIKE             | ret_120d                    |   3 |   0.0666775   |   0.127134   |   0.00739235  |   0.156191    | -0.112349   |   0.185248   |
| GOLD    | FIRST_HIKE             | ret_252d                    |   3 |   0.0478748   |   0.0681156  |   0.0323218   |   0.0735482   | -0.00347202 |   0.0789809  |
| GOLD    | FIRST_HIKE             | mdd                         |   3 |   0.149285    |   0.173712   |   0.134444    |   0.17634     |  0.0951754  |   0.178967   |
| GOLD    | FIRST_HIKE             | mae                         |   3 |  -0.0600798   |  -0.0140127  |  -0.0844277   |  -0.0126983   | -0.154843   |  -0.0113839  |
| GOLD    | FIRST_HIKE             | mfe                         |   3 |   0.158432    |   0.161783   |   0.0955831   |   0.222956    |  0.0293828  |   0.284128   |
| GOLD    | FIRST_HIKE             | time_to_event_min_obs       |   3 |  61           |  19          |  10.5         |  90.5         |  2          | 162          |
| GOLD    | FIRST_HIKE             | recovery50_obs_from_trough  |   3 |  24.6667      |  19          |  14           |  32.5         |  9          |  46          |
| GOLD    | FIRST_HIKE             | recovery100_obs_from_trough |   3 | 291.333       | 150          | 122.5         | 389.5         | 95          | 629          |
| GOLD    | FIRST_HIKE             | rv_60d_ann                  |   3 |   0.159726    |   0.141729   |   0.140377    |   0.170076    |  0.139026   |   0.198424   |
| GOLD    | FIRST_HIKE             | down_semivol_60d_ann        |   3 |   0.104086    |   0.110708   |   0.100229    |   0.111254    |  0.0897491  |   0.111801   |
| GOLD    | LAST_HIKE              | ret_20d                     |   3 |   0.0373211   |   0.0334615  |   0.00713151  |   0.0655808   | -0.0191984  |   0.0977002  |
| GOLD    | LAST_HIKE              | ret_60d                     |   3 |   0.0208144   |   0.0191943  |   0.0107684   |   0.0300503   |  0.00234257 |   0.0409063  |
| GOLD    | LAST_HIKE              | ret_120d                    |   3 |   0.0619465   |   0.0662024  |   0.0554825   |   0.0705385   |  0.0447625  |   0.0748746  |
| GOLD    | LAST_HIKE              | ret_252d                    |   3 |   0.17657     |   0.178834   |   0.149767    |   0.204506    |  0.120699   |   0.230178   |
| GOLD    | LAST_HIKE              | mdd                         |   3 |   0.0981819   |   0.0742874  |   0.068815    |   0.115602    |  0.0633426  |   0.156916   |
| GOLD    | LAST_HIKE              | mae                         |   3 |  -0.031785    |  -0.028186   |  -0.0476776   |  -0.014093    | -0.0671691  |   0          |
| GOLD    | LAST_HIKE              | mfe                         |   3 |   0.231451    |   0.241034   |   0.218823    |   0.248872    |  0.196611   |   0.256709   |
| GOLD    | LAST_HIKE              | time_to_event_min_obs       |   3 |  39.6667      |  51          |  25.5         |  59.5         |  0          |  68          |
| GOLD    | LAST_HIKE              | recovery50_obs_from_trough  |   3 |  18.6667      |  20          |  13           |  25           |  6          |  30          |
| GOLD    | LAST_HIKE              | recovery100_obs_from_trough |   3 |  44.3333      |  36          |  23           |  61.5         | 10          |  87          |
| GOLD    | LAST_HIKE              | rv_60d_ann                  |   3 |   0.153564    |   0.116416   |   0.106602    |   0.181952    |  0.0967881  |   0.247488   |
| GOLD    | LAST_HIKE              | down_semivol_60d_ann        |   3 |   0.101348    |   0.0714055  |   0.066925    |   0.1208      |  0.0624446  |   0.170195   |
| GOLD    | PAUSE_START            | ret_20d                     |   3 |  -0.0126912   |  -0.00921329 |  -0.0226677   |  -0.000975701 | -0.0361222  |   0.00726189 |
| GOLD    | PAUSE_START            | ret_60d                     |   3 |  -0.0236939   |  -0.0247668  |  -0.0456498   |  -0.00227437  | -0.0665328  |   0.020218   |
| GOLD    | PAUSE_START            | ret_120d                    |   3 |   0.0674968   |   0.0895124  |   0.0411285   |   0.104873    | -0.00725534 |   0.120233   |
| GOLD    | PAUSE_START            | ret_252d                    |   3 |   0.188419    |   0.19997    |   0.117583    |   0.265031    |  0.035196   |   0.330092   |
| GOLD    | PAUSE_START            | mdd                         |   3 |   0.0893911   |   0.0687814  |   0.066062    |   0.102415    |  0.0633426  |   0.136049   |
| GOLD    | PAUSE_START            | mae                         |   3 |  -0.0748594   |  -0.0623944  |  -0.0974213   |  -0.0460649   | -0.132448   |  -0.0297354  |
| GOLD    | PAUSE_START            | mfe                         |   3 |   0.203279    |   0.20532    |   0.136776    |   0.270803    |  0.068231   |   0.336285   |
| GOLD    | PAUSE_START            | time_to_event_min_obs       |   3 |  37.3333      |  42          |  27           |  50           | 12          |  58          |
| GOLD    | PAUSE_START            | recovery50_obs_from_trough  |   3 |  18.6667      |  20          |  13           |  25           |  6          |  30          |
| GOLD    | PAUSE_START            | recovery100_obs_from_trough |   3 |  41.6667      |  36          |  22.5         |  58           |  9          |  80          |
| GOLD    | PAUSE_START            | rv_60d_ann                  |   3 |   0.1539      |   0.14776    |   0.123438    |   0.181292    |  0.0991163  |   0.214825   |
| GOLD    | PAUSE_START            | down_semivol_60d_ann        |   3 |   0.114538    |   0.0955848  |   0.0864665   |   0.133132    |  0.0773482  |   0.17068    |
| GOLD    | TIGHTENING_CYCLE_END   | ret_20d                     |   3 |   0.0373211   |   0.0334615  |   0.00713151  |   0.0655808   | -0.0191984  |   0.0977002  |
| GOLD    | TIGHTENING_CYCLE_END   | ret_60d                     |   3 |   0.0208144   |   0.0191943  |   0.0107684   |   0.0300503   |  0.00234257 |   0.0409063  |
| GOLD    | TIGHTENING_CYCLE_END   | ret_120d                    |   3 |   0.0619465   |   0.0662024  |   0.0554825   |   0.0705385   |  0.0447625  |   0.0748746  |
| GOLD    | TIGHTENING_CYCLE_END   | ret_252d                    |   3 |   0.17657     |   0.178834   |   0.149767    |   0.204506    |  0.120699   |   0.230178   |
| GOLD    | TIGHTENING_CYCLE_END   | mdd                         |   3 |   0.0981819   |   0.0742874  |   0.068815    |   0.115602    |  0.0633426  |   0.156916   |
| GOLD    | TIGHTENING_CYCLE_END   | mae                         |   3 |  -0.031785    |  -0.028186   |  -0.0476776   |  -0.014093    | -0.0671691  |   0          |
| GOLD    | TIGHTENING_CYCLE_END   | mfe                         |   3 |   0.231451    |   0.241034   |   0.218823    |   0.248872    |  0.196611   |   0.256709   |
| GOLD    | TIGHTENING_CYCLE_END   | time_to_event_min_obs       |   3 |  39.6667      |  51          |  25.5         |  59.5         |  0          |  68          |
| GOLD    | TIGHTENING_CYCLE_END   | recovery50_obs_from_trough  |   3 |  18.6667      |  20          |  13           |  25           |  6          |  30          |
| GOLD    | TIGHTENING_CYCLE_END   | recovery100_obs_from_trough |   3 |  44.3333      |  36          |  23           |  61.5         | 10          |  87          |
| GOLD    | TIGHTENING_CYCLE_END   | rv_60d_ann                  |   3 |   0.153564    |   0.116416   |   0.106602    |   0.181952    |  0.0967881  |   0.247488   |
| GOLD    | TIGHTENING_CYCLE_END   | down_semivol_60d_ann        |   3 |   0.101348    |   0.0714055  |   0.066925    |   0.1208      |  0.0624446  |   0.170195   |
| GOLD    | TIGHTENING_CYCLE_START | ret_20d                     |   3 |   0.00849235  |   0.010349   |   0.000715924 |   0.0171971   | -0.0089172  |   0.0240452  |
| GOLD    | TIGHTENING_CYCLE_START | ret_60d                     |   3 |   0.0592625   |   0.046879   |   0.00351413  |   0.108819    | -0.0398507  |   0.170759   |
| GOLD    | TIGHTENING_CYCLE_START | ret_120d                    |   3 |   0.0666775   |   0.127134   |   0.00739235  |   0.156191    | -0.112349   |   0.185248   |
| GOLD    | TIGHTENING_CYCLE_START | ret_252d                    |   3 |   0.0478748   |   0.0681156  |   0.0323218   |   0.0735482   | -0.00347202 |   0.0789809  |
| GOLD    | TIGHTENING_CYCLE_START | mdd                         |   3 |   0.149285    |   0.173712   |   0.134444    |   0.17634     |  0.0951754  |   0.178967   |
| GOLD    | TIGHTENING_CYCLE_START | mae                         |   3 |  -0.0600798   |  -0.0140127  |  -0.0844277   |  -0.0126983   | -0.154843   |  -0.0113839  |
| GOLD    | TIGHTENING_CYCLE_START | mfe                         |   3 |   0.158432    |   0.161783   |   0.0955831   |   0.222956    |  0.0293828  |   0.284128   |
| GOLD    | TIGHTENING_CYCLE_START | time_to_event_min_obs       |   3 |  61           |  19          |  10.5         |  90.5         |  2          | 162          |
| GOLD    | TIGHTENING_CYCLE_START | recovery50_obs_from_trough  |   3 |  24.6667      |  19          |  14           |  32.5         |  9          |  46          |
| GOLD    | TIGHTENING_CYCLE_START | recovery100_obs_from_trough |   3 | 291.333       | 150          | 122.5         | 389.5         | 95          | 629          |
| GOLD    | TIGHTENING_CYCLE_START | rv_60d_ann                  |   3 |   0.159726    |   0.141729   |   0.140377    |   0.170076    |  0.139026   |   0.198424   |
| GOLD    | TIGHTENING_CYCLE_START | down_semivol_60d_ann        |   3 |   0.104086    |   0.110708   |   0.100229    |   0.111254    |  0.0897491  |   0.111801   |
| NASDAQ  | FIRST_CUT              | ret_20d                     |  10 |   0.0234638   |   0.00821336 |  -0.0256781   |   0.0431406   | -0.0539861  |   0.209816   |
| NASDAQ  | FIRST_CUT              | ret_60d                     |  10 |   0.00539027  |   0.034211   |  -0.0489051   |   0.06659     | -0.205636   |   0.136534   |
| NASDAQ  | FIRST_CUT              | ret_120d                    |  10 |  -0.0075732   |   0.00872857 |  -0.129364    |   0.112106    | -0.225675   |   0.17832    |
| NASDAQ  | FIRST_CUT              | ret_252d                    |  10 |   0.0676476   |   0.0752327  |  -0.0965878   |   0.246645    | -0.164149   |   0.283833   |
| NASDAQ  | FIRST_CUT              | mdd                         |  10 |   0.23294     |   0.24222    |   0.115516    |   0.290929    |  0.0786303  |   0.502233   |
| NASDAQ  | FIRST_CUT              | mae                         |  10 |  -0.163278    |  -0.146799   |  -0.229162    |  -0.0837923   | -0.379024   |   0          |
| NASDAQ  | FIRST_CUT              | mfe                         |  10 |   0.189113    |   0.225865   |   0.090323    |   0.274755    |  0.0157079  |   0.326315   |
| NASDAQ  | FIRST_CUT              | time_to_event_min_obs       |  10 | 116.9         | 129.5        |  65.75        | 165.25        |  0          | 238          |
| NASDAQ  | FIRST_CUT              | recovery50_obs_from_trough  |  10 | 100.2         |  40          |  15.5         |  85.75        |  5          | 589          |
| NASDAQ  | FIRST_CUT              | recovery100_obs_from_trough |   8 | 148.5         |  54          |  43.25        | 258.25        | 10          | 446          |
| NASDAQ  | FIRST_CUT              | rv_60d_ann                  |  10 |   0.18227     |   0.157041   |   0.092645    |   0.206244    |  0.0702516  |   0.538738   |
| NASDAQ  | FIRST_CUT              | down_semivol_60d_ann        |  10 |   0.131368    |   0.102606   |   0.0697638   |   0.151661    |  0.0532822  |   0.389925   |
| NASDAQ  | FIRST_HIKE             | ret_20d                     |  10 |   0.00370943  |   0.00311744 |  -0.0281563   |   0.030528    | -0.0827444  |   0.109834   |
| NASDAQ  | FIRST_HIKE             | ret_60d                     |  10 |  -0.0125672   |  -0.0442511  |  -0.0739495   |   0.0465303   | -0.310438   |   0.214766   |
| NASDAQ  | FIRST_HIKE             | ret_120d                    |  10 |   0.0399068   |   0.0199858  |  -0.0812836   |   0.102276    | -0.219611   |   0.420478   |
| NASDAQ  | FIRST_HIKE             | ret_252d                    |  10 |   0.0314111   |  -0.00820226 |  -0.0708355   |   0.0868634   | -0.174032   |   0.46056    |
| NASDAQ  | FIRST_HIKE             | mdd                         |  10 |   0.227812    |   0.206713   |   0.139621    |   0.344504    |  0.0783621  |   0.373185   |
| NASDAQ  | FIRST_HIKE             | mae                         |  10 |  -0.143338    |  -0.135142   |  -0.166775    |  -0.091172    | -0.358872   |  -0.0260082  |
| NASDAQ  | FIRST_HIKE             | mfe                         |  10 |   0.196069    |   0.113525   |   0.0752488   |   0.198264    |  0          |   0.910829   |
| NASDAQ  | FIRST_HIKE             | time_to_event_min_obs       |  10 |  99.5         |  63          |  38.25        | 173.5         | 29          | 228          |
| NASDAQ  | FIRST_HIKE             | recovery50_obs_from_trough  |  10 |  66.2         |  38.5        |  22.5         |  89           |  7          | 244          |
| NASDAQ  | FIRST_HIKE             | recovery100_obs_from_trough |   9 | 225.333       | 181          |  64           | 446           | 19          | 472          |
| NASDAQ  | FIRST_HIKE             | rv_60d_ann                  |  10 |   0.209312    |   0.179228   |   0.10737     |   0.254362    |  0.100732   |   0.459768   |
| NASDAQ  | FIRST_HIKE             | down_semivol_60d_ann        |  10 |   0.159515    |   0.141335   |   0.076374    |   0.181053    |  0.0535772  |   0.410234   |
| NASDAQ  | LAST_HIKE              | ret_20d                     |  10 |   0.000552395 |   0.0258557  |  -0.0161409   |   0.0474933   | -0.201588   |   0.0674705  |
| NASDAQ  | LAST_HIKE              | ret_60d                     |  10 |   0.0129934   |   0.0573636  |  -0.044074    |   0.0963204   | -0.274994   |   0.137173   |
| NASDAQ  | LAST_HIKE              | ret_120d                    |  10 |   0.0293425   |   0.0481384  |  -0.0837253   |   0.143205    | -0.228364   |   0.295776   |
| NASDAQ  | LAST_HIKE              | ret_252d                    |  10 |   0.0542354   |   0.109011   |  -0.120786    |   0.228193    | -0.421901   |   0.392082   |
| NASDAQ  | LAST_HIKE              | mdd                         |  10 |   0.219534    |   0.13822    |   0.0844192   |   0.332487    |  0.0685446  |   0.616625   |
| NASDAQ  | LAST_HIKE              | mae                         |  10 |  -0.174664    |  -0.0983125  |  -0.274203    |  -0.0467892   | -0.545743   |   0          |
| NASDAQ  | LAST_HIKE              | mfe                         |  10 |   0.199065    |   0.212899   |   0.114644    |   0.286429    |  0.0266644  |   0.416565   |
| NASDAQ  | LAST_HIKE              | time_to_event_min_obs       |  10 |  95.6         |  77.5        |  18.25        | 162           |  0          | 242          |
| NASDAQ  | LAST_HIKE              | recovery50_obs_from_trough  |   9 |  46.7778      |  17          |   6           |  88           |  5          | 124          |
| NASDAQ  | LAST_HIKE              | recovery100_obs_from_trough |   9 | 170.556       |  38          |  30           | 295           | 21          | 446          |
| NASDAQ  | LAST_HIKE              | rv_60d_ann                  |  10 |   0.186415    |   0.134222   |   0.0805221   |   0.209971    |  0.0599953  |   0.47536    |
| NASDAQ  | LAST_HIKE              | down_semivol_60d_ann        |  10 |   0.133266    |   0.0968419  |   0.0531817   |   0.130944    |  0.0261046  |   0.417854   |
| NASDAQ  | PAUSE_START            | ret_20d                     |   7 |   0.0167435   |   0.0150667  |  -2.24107e-05 |   0.0488184   | -0.0703256  |   0.0748717  |
| NASDAQ  | PAUSE_START            | ret_60d                     |   7 |   0.0752678   |   0.0771864  |   0.017467    |   0.135747    | -0.00951163 |   0.152771   |
| NASDAQ  | PAUSE_START            | ret_120d                    |   7 |   0.112914    |   0.1591     |   0.147676    |   0.185329    | -0.312439   |   0.277731   |
| NASDAQ  | PAUSE_START            | ret_252d                    |   7 |   0.15745     |   0.260786   |   0.173172    |   0.317948    | -0.462358   |   0.321481   |
| NASDAQ  | PAUSE_START            | mdd                         |   7 |   0.16881     |   0.101786   |   0.0776951   |   0.119661    |  0.0685446  |   0.616625   |
| NASDAQ  | PAUSE_START            | mae                         |   7 |  -0.118401    |  -0.0485173  |  -0.0934976   |  -0.00898371  | -0.575326   |   0          |
| NASDAQ  | PAUSE_START            | mfe                         |   7 |   0.273787    |   0.312444   |   0.218218    |   0.348303    |  0.107726   |   0.363298   |
| NASDAQ  | PAUSE_START            | time_to_event_min_obs       |   7 |  47.8571      |  23          |   5           |  54           |  0          | 194          |
| NASDAQ  | PAUSE_START            | recovery50_obs_from_trough  |   6 |   9.16667     |   6.5        |   5.25        |  10           |  5          |  21          |
| NASDAQ  | PAUSE_START            | recovery100_obs_from_trough |   6 |  31.6667      |  30          |  21.25        |  39.5         | 11          |  58          |
| NASDAQ  | PAUSE_START            | rv_60d_ann                  |   7 |   0.160196    |   0.124725   |   0.106274    |   0.191753    |  0.0786306  |   0.32196    |
| NASDAQ  | PAUSE_START            | down_semivol_60d_ann        |   7 |   0.108267    |   0.0691009  |   0.0602792   |   0.137624    |  0.0540692  |   0.238892   |

## Interpretation boundary

- DATA FACT: the cycle registry is mechanically derived from target-rate changes plus scheduled-meeting dates.
- DESCRIPTIVE RESULT: asset paths, drawdowns, volatility and recovery are historical distributions around those markers.
- NOT CAUSAL: this module does not identify target/path/information monetary shocks.
- FDR: no confirmatory p-value family is executed in this foundation run; future confirmatory families are predeclared in the lock.
- OOS: not applicable to this descriptive foundation; no forecasting claim is made.
- Investment implication: use the output as a risk-distribution and timing map, not as a deterministic trade rule.