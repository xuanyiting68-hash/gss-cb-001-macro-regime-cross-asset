# FED-CYCLE-STRESS-TROUGH-ALIGNMENT-018 — FIRST_CUT Stress/Trough Timing Lock
Date: 2026-09-24
Status: **FROZEN BEFORE EXECUTION / POST-ANCHOR MECHANISM TIMING / NOT PREDICTIVE**

## 1. Purpose

Explain the delayed drawdown risk identified by TOTAL-RISK-CLOCK-017 after FIRST_CUT.

Question:

**Do broad financial/cyclical stress peaks occur before, near, or after asset maximum-drawdown troughs in the same historical FIRST_CUT episodes?**

This module aligns already-computed event-level outputs.

It does not estimate a trading signal and does not claim that stress causes the trough.

## 2. Upstream frozen modules

Asset troughs:
- PHASE-CLOCK-004 event-level metrics.

Stress timing:
- STRESS-LAYER-005 event-level metrics.

No raw market source is reacquired.

No threshold is optimized.

## 3. Assets

Primary asset troughs:
- GOLD;
- SP500;
- NASDAQ;
- WTI.

All use their frozen 12M MDD trough month.

## 4. Stress observables

### BAA10Y_SPREAD
Stress peak:
- month of maximum Baa–10Y spread widening inside 12 complete months.

Historical support:
- 10 mechanical cycles / 7 broad episodes at FIRST_CUT.

### VIX
Stress peak:
- month of maximum increase in monthly-average VIX.

Historical support:
- 5 mechanical cycles / 5 broad episodes at FIRST_CUT.

### COPPER
Stress peak:
- month of maximum 12M drawdown.

Historical support:
- 5 mechanical cycles / 5 broad episodes at FIRST_CUT.

## 5. Pairwise timing

For each same-cycle asset × stress observable pair:

`lead_months = asset_mdd_trough_month - stress_peak_month`

Interpretation:
- positive: stress peak occurs before asset trough;
- zero: same month;
- negative: stress peak occurs after asset trough.

Report broad-episode-weighted:
- median lead_months;
- share stress peak before trough;
- share same month;
- share stress peak before-or-same;
- median absolute timing gap.

## 6. Near-coincidence window

Predeclare:

`NEAR = |lead_months| <= 2`

Report weighted near-coincidence share.

This is a descriptive timing window, not a signal threshold.

## 7. FIRST_CUT integrated comparison

For each asset, report:
- weighted median asset trough month from paired sample;
- each stress observable's weighted median peak month;
- pairwise median lead;
- near-coincidence share.

Also report whether the stress peak and asset trough both lie in the late half:

`month >= 7`.

## 8. Support

A pair is:
- SUPPORTED_TIMING_DESCRIPTIVE if >=5 mechanical cycles and >=4 broad episodes;
- LIMITED_TIMING_DESCRIPTIVE if >=2 broad episodes below supported threshold;
- INSUFFICIENT_SUPPORT otherwise.

No p-values.

## 9. Interpretation boundary

Allowed:
- stress escalation historically clustered near later FIRST_CUT drawdowns;
- credit/VIX/copper stress was usually earlier/later/near the asset trough.

Not allowed:
- stress peak predicts the trough in real time;
- the first cut causes stress;
- stress causes the asset drawdown.

The stress peak itself is a future-window statistic and therefore cannot be used as a live leading indicator.

## 10. Hard QC

Fail if:
- non-FIRST_CUT rows enter;
- cycle or broad-episode identifiers mismatch;
- timing months are outside 1-12;
- 2026 live cycle enters;
- any pair has duplicated cycle rows;
- any p-value is produced.

## 11. Evidence boundary

**POST-ANCHOR MECHANISM-TIMING ALIGNMENT / NO REAL-TIME SIGNAL / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**
