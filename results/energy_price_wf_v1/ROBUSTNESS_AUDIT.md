# ENERGY-PRICE-WF-001 — Robustness Audit
Date: 2026-09-24

## Status

**ROBUSTNESS / EXPLORATORY — DOES NOT UPGRADE THE PRIMARY RESULT**

Primary BH-FDR results remain authoritative.

## Leave-one-event-out

The sign of the confirmed-minus-veto difference remains negative in every leave-one-event-out run for all four primary metrics.

- wti_fwd_3m: mean-difference range -0.242 to -0.089; median-difference range -0.149 to -0.072.
- wti_fwd_6m: mean-difference range -0.379 to -0.185; median-difference range -0.179 to -0.132.
- short_mae_3m: mean-difference range -0.108 to -0.045; median-difference range -0.113 to -0.021.
- short_mae_6m: mean-difference range -0.167 to -0.076; median-difference range -0.099 to -0.075.

Interpretation: the descriptive separation is not created by a single event alone.

## Era heterogeneity

| sample                    | metric       |   n_confirmed |   n_veto |   confirmed_mean |   veto_mean |   mean_diff_confirmed_minus_veto |   confirmed_median |   veto_median |   median_diff_confirmed_minus_veto |
|:--------------------------|:-------------|--------------:|---------:|-----------------:|------------:|---------------------------------:|-------------------:|--------------:|-----------------------------------:|
| pre_2008                  | wti_fwd_3m   |             3 |        2 |        0.13485   |    0.122068 |                       0.0127816  |          0.0919418 |      0.122068 |                        -0.0301264  |
| pre_2008                  | wti_fwd_6m   |             3 |        2 |        0.199207  |    0.186664 |                       0.0125426  |          0.214678  |      0.186664 |                         0.0280137  |
| pre_2008                  | short_mae_3m |             3 |        2 |        0.156912  |    0.13727  |                       0.0196417  |          0.122942  |      0.13727  |                        -0.0143278  |
| pre_2008                  | short_mae_6m |             3 |        2 |        0.213761  |    0.207664 |                       0.00609709 |          0.214678  |      0.207664 |                         0.00701372 |
| 2008_plus                 | wti_fwd_3m   |             3 |        4 |       -0.204578  |    0.162356 |                      -0.366934   |         -0.0992847 |      0.154303 |                        -0.253588   |
| 2008_plus                 | wti_fwd_6m   |             3 |        4 |       -0.271581  |    0.317967 |                      -0.589547   |         -0.17978   |      0.315105 |                        -0.494885   |
| 2008_plus                 | short_mae_3m |             3 |        5 |        0         |    0.156861 |                      -0.156861   |          0         |      0.113148 |                        -0.113148   |
| 2008_plus                 | short_mae_6m |             3 |        5 |        0.0328657 |    0.272579 |                      -0.239713   |          0         |      0.195662 |                        -0.195662   |
| exclude_2008_crisis_event | wti_fwd_3m   |             5 |        6 |        0.0599202 |    0.148926 |                      -0.0890063  |          0.0567558 |      0.136239 |                        -0.079483   |
| exclude_2008_crisis_event | wti_fwd_6m   |             5 |        6 |        0.0895661 |    0.274199 |                      -0.184633   |          0.0770323 |      0.208695 |                        -0.131663   |
| exclude_2008_crisis_event | short_mae_3m |             5 |        7 |        0.0941472 |    0.151264 |                      -0.0571165  |          0.0919418 |      0.113148 |                        -0.0212067  |
| exclude_2008_crisis_event | short_mae_6m |             5 |        7 |        0.147976  |    0.254032 |                      -0.106056   |          0.120696  |      0.195662 |                        -0.0749661  |

The pre-2008 subset does not reproduce the later-sample separation, while the 2008+ subset is much stronger. Support is very small in each era, so this is a heterogeneity warning rather than evidence of a structural break.

Excluding the selected 2008 crisis event leaves the confirmed-minus-veto differences in the same direction, but the effect is smaller.

## Verdict

The price/product persistence filter is more promising as a **false-relief veto / risk filter** than as a positive short signal.

Why:
- veto events have strongly positive descriptive 3M/6M WTI outcomes in the completed sample;
- confirmed events are heterogeneous and do not have reliably negative medians;
- none of the four primary comparisons passes BH-FDR 10%;
- broad-era stability is not established.

Next gate: release-aware physical inventories/refinery state.