# ENERGY-WEEKLY-ANALOG-012A — Leave-One-Feature-Out Robustness Diagnostic
Date: 2026-09-24
Status: **POST-012 ROBUSTNESS / CURRENT OUTCOME STILL UNREALIZED**

## 1. Purpose

Assess whether the frozen ENERGY-WEEKLY-ANALOG-012 nearest-neighbor structure is dominated by any single feature.

This diagnostic does not alter:
- the 012 feature set;
- K=3;
- scaling rule;
- frozen top-three benchmark;
- current event classification.

## 2. Diagnostic

For each of the 13 frozen active features:

- remove exactly that feature;
- retain the other 12;
- reuse the 012 historical-only center/scale values for retained features;
- recompute equal-weight RMS standardized distance;
- record top-1 and top-3 historical analogs.

The current event remains excluded from scaling.

## 3. Stability metrics

Report:

- share of 13 leave-one-feature-out runs in which the original top-1 (2004-11-03) remains top-1;
- appearance count of each original top-3 analog inside the perturbed top-3 sets;
- minimum and mean overlap between each perturbed top-3 and the original top-3;
- any feature whose removal changes top-1.

No outcome is used to judge which perturbation is preferred.

## 4. Interpretation

High top-1/top-3 stability supports using 012 as a robust historical similarity reference.

Low stability weakens analog interpretation.

No perturbed analog set replaces the frozen 012 benchmark.

## 5. Hard QC

Fail if:
- current ENERGY005 outcome is realized;
- any outcome field enters distance;
- any perturbation changes more than one feature at a time;
- original 012 top-3 is overwritten.

## 6. Evidence boundary

**PROSPECTIVE ANALOG ROBUSTNESS DIAGNOSTIC / NO FORECAST MODEL / NOT CAUSAL / NOT DEPLOYABLE**
