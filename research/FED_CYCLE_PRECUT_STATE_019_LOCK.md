# FED-CYCLE-PRECUT-STATE-019 — Predetermined FIRST_CUT State × Late-Trough Breadth Lock
Date: 2026-09-24
Status: **FROZEN BEFORE EXECUTION / PRE-ANCHOR STATE DIAGNOSTIC / NO P-VALUES**

## 1. Purpose

Move from the ex-post stress alignment in STRESS-TROUGH-018 toward information that was available **before** FIRST_CUT.

Question:

**Were later equity/oil troughs more common when the pre-cut state already showed growth contraction, yield-curve inversion or tight financial conditions?**

This is a small-sample descriptive mechanism diagnostic, not a forecasting model.

## 2. Outcome object

Use the supported FIRST_CUT trough months already frozen in TOTAL-RISK-CLOCK-017 for:

- SP500;
- NASDAQ;
- WTI.

Gold is excluded from the primary breadth outcome because STRESS-TROUGH-018 shows materially different timing.

For every mechanical cycle with all three assets available:

### RISK3_MEDIAN_TROUGH_MONTH
Median of the three FIRST_CUT MDD trough months.

### RISK3_LATE_TROUGH_SHARE
Share of the three troughs occurring at month >= 7.

The threshold month 7 is inherited from prior phase-clock late-window definitions and is not chosen from 019 outcomes.

No return or recovery endpoint enters the state definition.

## 3. Pre-cut information month

Use the last STATE-PANEL-002 monthly row strictly before FIRST_CUT for each cycle.

Require:
- panel_month_start < FIRST_CUT date;
- yield_obs_date < FIRST_CUT;
- nfci_obs_date < FIRST_CUT.

For growth, replace revised INDPRO with the already-audited real-time RTDSM IPT value from VINTAGE-AUDIT-007 for the same cycle/panel_month.

Require RTDSM vintage period < panel_month.

## 4. Frozen predetermined states

### REALTIME_GROWTH_CONTRACTION
`RT_IPT_YOY < 0`

This is a natural zero-growth boundary.

### CURVE_INVERTED
`CURVE_BP < 0`

10Y–2Y spread below zero.

### FINANCIAL_CONDITIONS_TIGHT
`NFCI > 0`

Positive NFCI means financial conditions are tighter than historical average.

No threshold is optimized.

## 5. Composite state count

`PRE_CUT_STRESS_COUNT`

= number of the three binary states above that are true, range 0-3.

The score is additive only for descriptive ordering.

No coefficient is fit to choose weights.

## 6. Weighting

Mechanical cycles remain the unit row.

Within each broad episode:
- total weight = 1;
- if multiple mechanical cycles are present, split weight equally.

No broad episode receives extra weight because it contains several nearby cycles.

## 7. Frozen diagnostics

Report:

1. cycle-level state panel;
2. broad-episode-level weighted aggregation;
3. for each binary state, weighted median RISK3_MEDIAN_TROUGH_MONTH and RISK3_LATE_TROUGH_SHARE for state=False vs True;
4. Spearman rank correlation between PRE_CUT_STRESS_COUNT and each outcome after broad-episode aggregation;
5. leave-one-broad-episode-out sign stability of those two rank correlations.

No p-values.

## 8. Support

Primary result requires:
- at least 6 mechanical cycles;
- at least 5 broad episodes;
- all three pre-cut state variables nonmissing;
- all three risk-asset troughs observed.

If support falls below this, report limited/insufficient rather than changing variables.

## 9. Current-vintage boundary

- RT_IPT_YOY is real-time-vintage safe under VINTAGE-AUDIT-007.
- CURVE_BP and NFCI are market/financial observations with pre-cut observation dates.
- This module does not claim all historical financial series are unrevised in every implementation detail.
- CPI is deliberately excluded because the project does not have a like-for-like real-time vintage for the original CPI series.

## 10. Interpretation

Allowed:
- pre-cut stress states were descriptively associated with later/earlier trough breadth;
- signs were/weren't stable across broad-episode leave-one-out checks.

Not allowed:
- these states predict trough timing out of sample;
- the Fed cut caused later troughs;
- thresholds form a trading rule.

## 11. Hard QC

Fail if:
- any state observation date is on/after FIRST_CUT;
- real-time IPT vintage is not earlier than panel_month;
- outcome asset set differs from SP500/NASDAQ/WTI;
- month-7 threshold changes;
- current 2026 cycle enters;
- p-values are generated.

## 12. Evidence boundary

**PREDETERMINED PRE-CUT STATE DIAGNOSTIC / REAL-TIME GROWTH + PRE-CUT MARKET STATES / NO P-VALUES / NOT CAUSAL / NOT OOS / NOT DEPLOYABLE**
