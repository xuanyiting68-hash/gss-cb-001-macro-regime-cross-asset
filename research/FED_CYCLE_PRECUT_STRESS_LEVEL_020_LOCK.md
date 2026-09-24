# FED-CYCLE-PRECUT-STRESS-LEVEL-020 — Continuous Pre-Cut Stress Level Lock
Date: 2026-09-25
Status: **FROZEN BEFORE 020 ASSOCIATION EXECUTION / EXPLORATORY MECHANISM-HYPOTHESIS / NO P-VALUES**

## 1. Purpose

Follow the negative binary-state result in FED-CYCLE-PRECUT-STATE-019 with one tightly bounded question:

**Do continuous stress levels observed before FIRST_CUT contain more descriptive information about later equity/oil trough timing than the failed binary 019 states?**

This module is explicitly exploratory because predictor selection follows the completed 018/019 diagnostics.

It is not a forecasting model, not causal identification and not a trading rule.

## 2. Outcomes

Reuse the already-frozen 019 outcomes for the supported FIRST_CUT risk basket:

- SP500;
- NASDAQ;
- WTI.

At the mechanical-cycle level:

- `RISK3_MEDIAN_TROUGH_MONTH` = median FIRST_CUT MDD trough month across SP500/NASDAQ/WTI;
- `RISK3_LATE_TROUGH_SHARE` = share of those troughs at month >= 7.

No new outcome horizon, threshold or asset is introduced.

Broad episode remains the independent descriptive unit.

## 3. Frozen continuous predictors

Use exactly four predetermined pre-anchor continuous variables.

### 3.1 BAA_SPREAD_LEVEL

Moody's Baa minus 10Y Treasury spread from FRED series `BAA10YM`.

Use the STRESS-LAYER-005 `FIRST_CUT` `baseline_value`, which is the last monthly spread observation in the month immediately preceding the FIRST_CUT anchor month.

Higher value = wider credit spread / more credit stress.

### 3.2 VIX_LEVEL

CBOE VIX from FRED series `VIXCLS`.

Use the STRESS-LAYER-005 `FIRST_CUT` `baseline_value`, defined as the monthly-average VIX in the month immediately preceding the FIRST_CUT anchor month.

Higher value = more volatility stress.

Because VIX history starts later than the full Fed-cycle sample, VIX is expected to have less support and must be labeled separately.

### 3.3 CURVE_STRESS_BP

Use the already-audited 019 pre-cut 10Y-2Y curve level:

`CURVE_STRESS_BP = -CURVE_BP`

This orientation makes higher values represent more inversion / greater curve stress.

The observation date must remain strictly before FIRST_CUT.

### 3.4 GROWTH_STRESS

Use real-time RTDSM industrial-production growth from VINTAGE-AUDIT-007 / 019:

`GROWTH_STRESS = -RT_IPT_YOY`

This orientation makes higher values represent weaker real-time growth.

The RTDSM vintage period must remain strictly earlier than the 019 panel month.

## 4. Explicit exclusions

Do not add:

- NFCI to the 020 primary predictor set;
- CPI;
- copper;
- revised INDPRO;
- returns, drawdowns or recovery variables as predictors;
- interactions;
- nonlinear transformations;
- optimized thresholds;
- regression-selected weights;
- composite stress scores.

NFCI is excluded because 019 already showed strong component sensitivity to the single NFCI-tight broad episode. The purpose of 020 is to test a minimal continuous-level extension, not expand the variable set after seeing results.

## 5. Aggregation and weighting

Mechanical-cycle rows inherit the existing broad-episode weights:

- each broad episode total weight = 1;
- if a broad episode has multiple mechanical cycles, split weight equally.

For each continuous predictor and each outcome, aggregate to one broad-episode row using the existing within-episode weights.

No episode receives extra weight because it contains more mechanical legs.

## 6. Frozen diagnostics

For each predictor and each outcome report:

1. number of mechanical cycles with nonmissing predictor/outcome;
2. number of independent broad episodes;
3. broad-episode Spearman rank correlation;
4. leave-one-broad-episode-out Spearman correlations;
5. `loo_defined_count`, `loo_total_count`, `loo_all_defined`;
6. whether all finite LOO correlations retain the full-sample sign;
7. minimum and maximum finite LOO rho;
8. maximum absolute change in rho from deleting one broad episode.

No p-values and no significance labels.

### VIX common-sample audit

Because VIX begins later, also recompute BAA_SPREAD_LEVEL, CURVE_STRESS_BP and GROWTH_STRESS on exactly the VIX-supported broad episodes.

This is a sample-composition audit only. It must not replace the full-support diagnostics.

## 7. Support labels

At the broad-episode level:

- `SUPPORTED_EXPLORATORY`: >= 6 broad episodes;
- `LIMITED_EXPLORATORY`: 5 broad episodes;
- `INSUFFICIENT_SUPPORT`: < 5 broad episodes.

A strong rho with LIMITED/INSUFFICIENT support is not promoted.

A relation is not called composition-robust unless:

- full rho is defined;
- every LOO rho is defined;
- every LOO rho retains the full-sample sign.

Even then, the result remains exploratory and non-OOS.

## 8. Comparison with 019

020 may state that a continuous level appears more or less informative than the corresponding 019 binary flag only descriptively.

It may not claim:

- superior forecasting;
- predictive accuracy;
- validated bottom timing;
- a deployable PandaAI score.

No 019 threshold is retuned.

## 9. Hard QC

Fail if:

- any 019 state timing violation is introduced;
- any RTDSM vintage is not earlier than its panel month;
- any 2026 live cycle enters the realized-outcome sample;
- the risk asset set differs from SP500/NASDAQ/WTI;
- the late-trough threshold differs from month 7;
- any predictor outside the four frozen variables is used;
- any p-value is generated;
- the VIX common-sample audit changes the primary sample.

## 10. Stopping rule

After these four predictors and the frozen diagnostics are run:

- do not add variables because a result is weak;
- do not transform predictors to improve rho;
- do not search thresholds;
- do not fit a multivariate model on the same six broad episodes.

If the continuous-level evidence is unstable, composition-driven or support-limited, close the branch as negative/limited evidence and prioritize prospective append-only maturation.

## 11. Evidence boundary

**EXPLORATORY / MECHANISM-HYPOTHESIS / PREDETERMINED PRE-CUT LEVELS / NO P-VALUES / NOT CAUSAL / NOT OOS / NOT DEPLOYABLE**
