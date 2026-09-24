# FED-CYCLE-VINTAGE-AUDIT-007 — Post-run robustness

**POST-RUN ROBUSTNESS ONLY / DOES NOT UPGRADE CONFIRMATORY STATUS**

## Restriction audit

| restriction           | outcome         |   same_sample_rows |   n_cycles |   n_broad_episodes | support_status             |   realtime_beta |   realtime_p_broad_exact |   realtime_p_mechanical_exact |   current_beta |   current_p_broad_exact |   current_p_mechanical_exact | beta_sign_agreement   |
|:----------------------|:----------------|-------------------:|-----------:|-------------------:|:---------------------------|----------------:|-------------------------:|------------------------------:|---------------:|------------------------:|-----------------------------:|:----------------------|
| FULL_SAMPLE           | GOLD_FWD_6M_RET |                165 |         10 |                  7 | SUPPORTED_FROZEN_THRESHOLD |     -0.0196473  |                 0.015625 |                     0.0253906 |   -0.0127457   |                0.125    |                     0.111328 | True                  |
| FULL_SAMPLE           | GOLD_FWD_6M_MDD |                165 |         10 |                  7 | SUPPORTED_FROZEN_THRESHOLD |      0.00322907 |                 0.71875  |                     0.734375  |    0.00347046  |                0.390625 |                     0.398438 | True                  |
| EXCLUDE_2022          | GOLD_FWD_6M_RET |                136 |          9 |                  6 | SUPPORTED_FROZEN_THRESHOLD |     -0.0148702  |                 0.03125  |                     0.0507812 |   -0.00819624  |                0.25     |                     0.222656 | True                  |
| EXCLUDE_2022          | GOLD_FWD_6M_MDD |                136 |          9 |                  6 | SUPPORTED_FROZEN_THRESHOLD |     -0.00138274 |                 0.59375  |                     0.546875  |    0.000405791 |                0.78125  |                     0.796875 | False                 |
| EXCLUDE_EARLY_B01_B02 | GOLD_FWD_6M_RET |                135 |          5 |                  5 | SUPPORTED_FROZEN_THRESHOLD |     -0.0298707  |                 0.0625   |                     0.0625    |   -0.0121053   |                0.4375   |                     0.4375   | True                  |
| EXCLUDE_EARLY_B01_B02 | GOLD_FWD_6M_MDD |                135 |          5 |                  5 | SUPPORTED_FROZEN_THRESHOLD |      0.00506534 |                 0.8125   |                     0.8125    |    0.00442239  |                0.6875   |                     0.6875   | True                  |
| LATER_EX_2022         | GOLD_FWD_6M_RET |                106 |          4 |                  4 | LIMITED_SUPPORT            |     -0.0233712  |               nan        |                   nan         |   -0.0024748   |              nan        |                   nan        | True                  |
| LATER_EX_2022         | GOLD_FWD_6M_MDD |                106 |          4 |                  4 | LIMITED_SUPPORT            |     -0.00463278 |               nan        |                   nan         |   -0.00173517  |              nan        |                   nan        | True                  |

## Full-sample broad-episode score contributions

| broad_episode_id   |   realtime_score_contribution |   score_sign |
|:-------------------|------------------------------:|-------------:|
| B01                |                  -0.0298491   |           -1 |
| B02                |                  -0.00858378  |           -1 |
| B03                |                  -0.000612186 |           -1 |
| B04                |                  -0.0323464   |           -1 |
| B05                |                  -0.035526    |           -1 |
| B06                |                  -0.017652    |           -1 |
| B07                |                  -0.071903    |           -1 |

## Revision-size audit

|   panel_rows |   paired_rows |   pearson_corr_current_vs_realtime |   median_abs_revision_gap_pp |   p90_abs_revision_gap_pp |   max_abs_revision_gap_pp |
|-------------:|--------------:|-----------------------------------:|-----------------------------:|--------------------------:|--------------------------:|
|          165 |           165 |                           0.900119 |                      1.03487 |                   2.73589 |                   3.89478 |