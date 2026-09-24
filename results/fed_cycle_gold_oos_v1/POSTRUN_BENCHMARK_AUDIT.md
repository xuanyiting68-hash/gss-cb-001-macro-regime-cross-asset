# FED-CYCLE-GOLD-OOS-008 — Post-run benchmark sanity audit

**NO REFITTING / FROZEN OOS GATE UNCHANGED**

## Comparator sensitivity

| comparison                                     |   mse_improvement_fraction |   mae_improvement_fraction |   mse_episode_wins |   mae_episode_wins |   total_episodes |
|:-----------------------------------------------|---------------------------:|---------------------------:|-------------------:|-------------------:|-----------------:|
| M3_PLUS_REALTIME_IPT vs B0_HIST_MEAN           |                  0.0337654 |                 -0.0274434 |                  2 |                  1 |                4 |
| M3_PLUS_REALTIME_IPT vs B1_GOLD_HISTORY        |                  0.112799  |                  0.0629154 |                  2 |                  2 |                4 |
| M3_PLUS_REALTIME_IPT vs B2_GOLD_PLUS_CYCLE_AGE |                  0.212693  |                  0.107721  |                  3 |                  3 |                4 |
| M3_PLUS_REALTIME_IPT vs D4_PLUS_CURRENT_INDPRO |                  0.0680151 |                  0.0352646 |                  3 |                  3 |                4 |

## M3 signed bias by OOS broad episode

| broad_episode_id   |   weighted_signed_bias |   weighted_mean_actual |   weighted_mean_prediction |
|:-------------------|-----------------------:|-----------------------:|---------------------------:|
| B04                |             -0.0281505 |            -0.00697874 |                 -0.0351292 |
| B05                |             -0.127694  |             0.100594   |                 -0.0271009 |
| B06                |              0.0734042 |             0.0169511  |                  0.0903553 |
| B07                |             -0.0310849 |             0.0803488  |                  0.049264  |

Episode-equal signed bias: -0.028381

## Prediction range

| series                   |       min |      max |   mean_unweighted |
|:-------------------------|----------:|---------:|------------------:|
| REALIZED_GOLD_FWD_6M_RET | -0.14094  | 0.415094 |         0.0540849 |
| M3_PREDICTION            | -0.147083 | 0.126421 |         0.0258276 |