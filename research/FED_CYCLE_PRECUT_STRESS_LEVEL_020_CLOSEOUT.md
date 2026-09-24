# FED-CYCLE-PRECUT-STRESS-LEVEL-020 — Closeout
Date: 2026-09-25
Status: **QC PASS / CONTINUOUS PRE-CUT LEVEL RULE NOT SUPPORTED / BRANCH STOP**

## Purpose

020 tests whether four continuous stress levels already observable before FIRST_CUT contain more descriptive information about later SP500/Nasdaq/WTI trough timing than the failed binary states in 019.

The specification was frozen before 020 association execution.

Predictors:

- Baa–10Y spread level;
- VIX level where supported;
- curve stress = minus 10Y–2Y spread;
- real-time growth stress = minus RTDSM IPT YoY.

No NFCI extension, threshold search, interaction, nonlinear transformation, composite score or fitted multivariate model is permitted.

## QC

- 8 mechanical cycles / 6 broad episodes;
- Baa / curve / real-time growth support = 6 broad episodes;
- VIX support = 5 broad episodes;
- zero 2026 realized-outcome leakage;
- zero Baa/VIX anchor-date mismatches;
- no p-values.

QC: **PASS**.

## Median trough timing

Full-sample Spearman rho:

- Baa spread: **+0.075**;
- VIX: **-0.211**;
- curve stress: **+0.029**;
- real-time growth stress: **-0.177**.

All four fail composition robustness. Their leave-one-broad-episode ranges cross zero:

- Baa: -0.264 to +0.564;
- VIX: -0.632 to +0.316;
- curve: -0.738 to +0.316;
- growth: -0.564 to +0.264.

No robust monotone historical trough-timing rule is established.

## Late-trough-share degeneracy

Broad-episode late-trough share:

- B02 = **0.556**;
- B03 = **1.000**;
- B04 = **1.000**;
- B05 = **1.000**;
- B06 = **1.000**;
- B07 = **1.000**.

Thus the full sample has only two unique outcome values and the VIX-supported sample has no variation at all.

The apparently positive curve-stress/late-share rho is therefore effectively tied to whether B02 is present and is not composition-robust.

## Common-sample diagnostic

On the VIX-supported B03-B07 sample, curve stress versus median trough month has rho **-0.738** and all five LOO correlations remain negative.

Restoring B02 changes the full-sample rho to **+0.029**.

This is a sample-composition effect, not a historical timing rule.

## Comparison with 019

019 showed that binary growth contraction lacked variation, binary curve inversion had no median separation and NFCI tightness had only one True broad episode.

020 shows that replacing binary states with continuous levels still does not generate a robust timing rule. The problem is therefore not merely coarse thresholds.

## Product implication

Do not create a PandaAI bottoming/timing score from Baa, VIX, curve depth, real-time growth or a combination fit to these six episodes.

The defensible object remains:

`policy phase + current observables + asset-specific historical path-risk distribution + support strength + uncertainty + evidence class`.

## Branch decision

**STOP THE SMALL-SAMPLE FIRST_CUT TIMING-RULE BRANCH.**

Do not add predictors or transformations to 020.

Next priority is prospective append-only evidence maturation and evidence-linked PandaAI integration. This does not reuse consumed OOS-008 B04-B07 evidence to tune M3.

## Boundary

**EXPLORATORY / MECHANISM-HYPOTHESIS / NEGATIVE-LIMITED / NO P-VALUES / NOT CAUSAL / NOT OOS / NOT DEPLOYABLE**
