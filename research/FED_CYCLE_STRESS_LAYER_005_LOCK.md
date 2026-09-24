# FED-CYCLE-STRESS-LAYER-005 — VIX × Credit Spread × Copper Phase Diagnostics
Date: 2026-09-24
Status: **FROZEN BEFORE STRESS-PATH EXECUTION**

## 1. Purpose

Add public, reproducible stress-state observables to the Fed-cycle phase framework.

Predeclared observables:

1. VIX — equity volatility/stress;
2. Baa minus 10Y Treasury spread — broad credit stress;
3. Copper — cyclical/global-demand-sensitive commodity price.

Question:

**How do observable stress conditions evolve after FIRST_HIKE, LAST_HIKE, PAUSE_START and FIRST_CUT?**

This is a descriptive mechanism layer. It is not a trading-signal search.

## 2. Canonical phase anchors

Use the timing-corrected cycle registry:

`results/fed_cycle_path_v1_1/FED_TIGHTENING_CYCLES.csv`

Anchors:

- FIRST_HIKE
- LAST_HIKE
- PAUSE_START
- FIRST_CUT

No anchor is redefined.

Pre-1994 timing retains the historical-target-reconstruction limitation.

## 3. Sources

### 3.1 VIX

FRED `VIXCLS`.

Daily source is aggregated by calendar month into:

- monthly average VIX;
- monthly maximum VIX.

Coverage is expected to begin in 1990.

### 3.2 Broad credit spread

FRED `BAA10YM`:

Moody's Seasoned Baa Corporate Bond Yield Relative to 10-Year Treasury Constant Maturity.

Use the source at its native monthly frequency.

Unit: percentage points.

### 3.3 Copper

FRED `PCOPPUSDM`:

Global price of Copper.

Use native monthly observations.

Raw source histories are not committed; only hashes, derived paths and metadata are public outputs.

## 4. Common phase timing

For anchor month M0:

- baseline = M-1;
- anchor month M0 is omitted;
- event months 1..12 = M+1..M+12.

All three stress observables use the same 12-complete-month phase window.

## 5. VIX metrics

Baseline:

- M-1 monthly average VIX.

For M+1..M+12 record:

- monthly average VIX;
- monthly maximum VIX;
- change in monthly-average VIX from baseline;
- running maximum monthly-average VIX change.

Cycle × phase summary:

- +3M average-level change;
- +6M change;
- +12M change;
- maximum monthly-average VIX increase;
- maximum daily VIX level observed inside the 12 complete months;
- month of maximum monthly-average VIX increase.

No VIX threshold is used to classify a signal.

## 6. Credit-spread metrics

Baseline:

- BAA10YM in M-1.

For M+1..M+12 record change from baseline in basis points.

Cycle × phase summary:

- +3M / +6M / +12M change in bp;
- maximum 12M widening in bp;
- maximum 12M tightening in bp;
- month of maximum widening.

No spread threshold is optimized.

## 7. Copper metrics

Baseline:

- copper price in M-1.

For M+1..M+12:

- cumulative return;
- running MDD.

Cycle × phase summary:

- +3M / +6M / +12M return;
- 12M MDD;
- event-relative MAE/MFE;
- MDD trough month.

## 8. Broad-episode weighting

Use the same broad-episode ontology as STATE-PANEL-002 / RISK-CLOCK-003.

Within each observable × phase:

- available mechanical legs in the same broad episode share total weight 1;
- each broad episode contributes total weight 1.

## 9. Support

A stress observable × phase cell is PRIMARY_SUPPORTED only if:

- at least 5 mechanical legs;
- at least 4 broad episodes.

Otherwise it remains diagnostic.

Support thresholds are not relaxed.

## 10. Primary descriptive outputs

For every supported phase:

### VIX
- weighted median maximum VIX increase;
- weighted median month of maximum increase;
- weighted median +12M VIX change.

### Credit spread
- weighted median maximum widening;
- weighted median month of maximum widening;
- weighted median +12M change.

### Copper
- weighted median 12M return;
- weighted median 12M MDD;
- weighted median MDD-trough month.

## 11. Relation to asset-risk phase map

The stress layer may be shown beside PHASE-CLOCK-004.

It must not be described as causal evidence that VIX/credit/copper "caused" equity/Gold/WTI paths.

Because the same historical cycles generate both stress and asset paths, simple visual co-movement is descriptive/mechanism evidence only.

## 12. No post-hoc predictive test

No p-value/FDR family is run in STRESS-LAYER-005.

The module does not test thresholds, signals or forecasting rules.

If a stress observable appears informative, any predictive/OOS test requires a separately frozen design.

## 13. Hard QC

Fail if:

- phase anchor differs from canonical registry;
- event month enters the clean path;
- baseline M-1 is missing for a reported cell;
- VIX monthly maximum is below its monthly average;
- credit spread basis-point conversion is inconsistent;
- copper MDD is negative;
- broad-episode weights fail to sum to 1 in an available cell;
- unsupported cells are labeled primary;
- raw source histories are committed.

## 14. Evidence status

Allowed:

- **DATA FACT**
- **DESCRIPTIVE RESULT**
- **MECHANISM CANDIDATE**
- **NOT YET VERIFIED**

Not allowed:

- "VIX predicts the crash" from this module;
- "credit widening causes equities to fall";
- optimized stress thresholds;
- deployment/trading claims.

FDR: not applicable.
OOS: not a forecasting model.
Causality: none.
Deployment: none.
