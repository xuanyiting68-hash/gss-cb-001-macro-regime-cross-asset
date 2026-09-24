# FED-CYCLE-GOLD-OOS-008 — Report

**TIME-ORDERED EPISODE-FORWARD OOS / NOT CAUSAL / NOT DEPLOYABLE**

## Frozen evidence gate

- status: **PRELIMINARY_OOS_CANDIDATE**
- M3 vs B2 episode-equal MSE reduction: 21.27%
- M3 episode wins vs B2: 3/4
- M3 OOS R² vs B0: 0.0338

## Model summary

| model                  |   oos_episodes |   episode_equal_mse |   episode_equal_mae |   oos_r2_vs_b0 |
|:-----------------------|---------------:|--------------------:|--------------------:|---------------:|
| B0_HIST_MEAN           |              4 |           0.0138649 |           0.0886148 |      0         |
| B1_GOLD_HISTORY        |              4 |           0.0151    |           0.0971596 |     -0.0890818 |
| B2_GOLD_PLUS_CYCLE_AGE |              4 |           0.017016  |           0.102038  |     -0.227266  |
| M3_PLUS_REALTIME_IPT   |              4 |           0.0133968 |           0.0910467 |      0.0337654 |
| D4_PLUS_CURRENT_INDPRO |              4 |           0.0143745 |           0.0943748 |     -0.0367492 |

## Per-episode metrics

| broad_episode_id   | model                  |   n_rows |        mse |       mae |
|:-------------------|:-----------------------|---------:|-----------:|----------:|
| B04                | B0_HIST_MEAN           |       18 | 0.00575359 | 0.0512909 |
| B05                | B0_HIST_MEAN           |       36 | 0.0275349  | 0.132093  |
| B06                | B0_HIST_MEAN           |       36 | 0.00618143 | 0.0628922 |
| B07                | B0_HIST_MEAN           |       29 | 0.0159898  | 0.108183  |
| B04                | B1_GOLD_HISTORY        |       18 | 0.0131161  | 0.0850982 |
| B05                | B1_GOLD_HISTORY        |       36 | 0.0246494  | 0.128458  |
| B06                | B1_GOLD_HISTORY        |       36 | 0.00810979 | 0.0712167 |
| B07                | B1_GOLD_HISTORY        |       29 | 0.0145248  | 0.103866  |
| B04                | B2_GOLD_PLUS_CYCLE_AGE |       18 | 0.0182704  | 0.100788  |
| B05                | B2_GOLD_PLUS_CYCLE_AGE |       36 | 0.0279291  | 0.138773  |
| B06                | B2_GOLD_PLUS_CYCLE_AGE |       36 | 0.010182   | 0.0768966 |
| B07                | B2_GOLD_PLUS_CYCLE_AGE |       29 | 0.0116823  | 0.0916965 |
| B04                | M3_PLUS_REALTIME_IPT   |       18 | 0.0065819  | 0.0606132 |
| B05                | M3_PLUS_REALTIME_IPT   |       36 | 0.0268867  | 0.135648  |
| B06                | M3_PLUS_REALTIME_IPT   |       36 | 0.012427   | 0.0935284 |
| B07                | M3_PLUS_REALTIME_IPT   |       29 | 0.00769156 | 0.0743969 |
| B04                | D4_PLUS_CURRENT_INDPRO |       18 | 0.009814   | 0.0737432 |
| B05                | D4_PLUS_CURRENT_INDPRO |       36 | 0.0272931  | 0.136525  |
| B06                | D4_PLUS_CURRENT_INDPRO |       36 | 0.0122498  | 0.0903847 |
| B07                | D4_PLUS_CURRENT_INDPRO |       29 | 0.008141   | 0.0768463 |

## Real-time IPT standardized coefficient by OOS fold

| test_broad_episode   | model                | feature    |   standardized_coefficient | feature_active_in_train   |   train_rows |   train_broad_episodes |
|:---------------------|:---------------------|:-----------|---------------------------:|:--------------------------|-------------:|-----------------------:|
| B04                  | M3_PLUS_REALTIME_IPT | RT_IPT_YOY |                 -0.049409  | True                      |           46 |                      3 |
| B05                  | M3_PLUS_REALTIME_IPT | RT_IPT_YOY |                 -0.0491649 | True                      |           64 |                      4 |
| B06                  | M3_PLUS_REALTIME_IPT | RT_IPT_YOY |                 -0.0497219 | True                      |          100 |                      5 |
| B07                  | M3_PLUS_REALTIME_IPT | RT_IPT_YOY |                 -0.0429661 | True                      |          136 |                      6 |

## Interpretation boundary

- no random split;
- every test broad episode is strictly later than all training episodes;
- training outcomes end before the test episode begins;
- no hyperparameter or feature selection;
- current-vintage D4 is diagnostic only and not PIT-deployable;
- maximum positive label is PRELIMINARY_OOS_CANDIDATE because only four independent future broad episodes are available.