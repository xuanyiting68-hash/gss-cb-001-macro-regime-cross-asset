# FED-CYCLE-PRECUT-STRESS-LEVEL-020

**EXPLORATORY CONTINUOUS PRE-CUT LEVEL DIAGNOSTIC / SIMPLE CONTINUOUS RULE NOT SUPPORTED**

## QC

- QC: **PASS**
- 8 mechanical cycles / 6 broad episodes.
- VIX support: 5 broad episodes.
- No 2026 realized-outcome leakage.
- No p-values, threshold search, interactions, composite score or fitted multivariate model.

## Main result

Full-sample Spearman rho versus median SP500/Nasdaq/WTI trough month:

- Baa spread level: **+0.075**;
- VIX level: **-0.211**;
- curve stress: **+0.029**;
- real-time growth stress: **-0.177**.

Every predictor fails the frozen full-sample composition-robustness requirement because leave-one-broad-episode diagnostics change sign.

LOO ranges:

- Baa: **-0.264 to +0.564**;
- VIX: **-0.632 to +0.316**;
- curve stress: **-0.738 to +0.316**;
- growth stress: **-0.564 to +0.264**.

## Late-trough-share design limit

The broad-episode late-trough share is 0.556 for B02 and 1.000 for every episode B03-B07.

The six-episode outcome therefore has only two unique values. The VIX-supported B03-B07 sample is constant at 1.000, so VIX/late-share rank correlation is undefined.

The full-sample curve-stress/late-share rho is +0.655, but dropping B02 makes the outcome constant and the LOO correlation undefined. This is not composition-robust evidence.

## VIX common-sample audit

On B03-B07, curve stress versus median trough month has rho **-0.738**, with all five LOO correlations negative (-0.949 to -0.447).

But restoring B02 changes the full-sample rho to **+0.029**. The attractive modern/VIX-sample pattern is therefore sample-composition sensitive and is not promoted.

## Conclusion

Continuous pre-cut levels do **not** rescue the failed 019 timing-rule hypothesis.

Per the frozen stopping rule, stop this small-sample FIRST_CUT timing-rule branch rather than adding variables or transformations.

**Evidence boundary: EXPLORATORY / MECHANISM-HYPOTHESIS / NEGATIVE-LIMITED / NOT CAUSAL / NOT OOS / NOT DEPLOYABLE.**
