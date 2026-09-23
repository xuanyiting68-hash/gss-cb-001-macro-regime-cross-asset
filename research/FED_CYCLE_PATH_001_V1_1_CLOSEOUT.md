# FED-CYCLE-PATH-001 v1.1 — Closeout
Date: 2026-09-24
Status: **QC-PASSED DESCRIPTIVE FOUNDATION / LONG-HISTORY GOLD DAILY SUPPORT LIMITED / NOT DEPLOYABLE**

## 1. Research question

This module asks a path-risk question rather than an endpoint-only question:

`Fed cycle anchor -> path -> drawdown -> trough timing -> volatility -> 50% recovery -> 100% recovery`

Realized Fed target changes are descriptive cycle markers. They are not identified monetary-policy shocks.

## 2. Audit trail

### v1

The first completed v1 computation passed internal numerical QC, but post-run readback found a timing-ontology bug:

- modern target-series effective dates could differ from the FOMC decision date;
- the recent scheduled-meeting supplement stopped at 2024, which could falsely label 2025 scheduled cuts as emergencies;
- pre-1994 reconstructed target changes were not conceptually comparable to modern emergency announcements.

v1 is retained in `results/fed_cycle_path_v1/` but is **QUARANTINED / DO NOT CITE AS RESEARCH RESULT**.

### v1.1

The timing lock separates `source_effective_date` from `event_date`.

For scheduled modern changes, the asset anchor is the FOMC decision date. Hard QC verifies:

- 2022 FIRST_HIKE = 2022-03-16;
- 2023 LAST_HIKE for the 2022 leg = 2023-07-26;
- 2024 FIRST_CUT for the 2022 leg = 2024-09-18.

Pre-1994 anchors remain historical target reconstructions and carry that interpretation boundary.

Eight post-1994 unscheduled >=25 bp cuts remain `EMERGENCY_CUT_CANDIDATE` rows with unresolved announcement timing. They are registry-only and **zero** emergency rows enter asset metrics.

## 3. Policy-cycle registry

Mechanical rule:

- consecutive positive target changes;
- at least two hikes;
- cumulative tightening >=50 bp.

The corrected registry contains **10 qualifying tightening legs** beginning in:

1983, 1984, 1987, 1987, 1988, 1994, 1999, 2004, 2015, 2022.

These are mechanical policy-target legs, not a claim that all 10 are statistically independent macroeconomic regimes.

## 4. Asset coverage

Daily/market-frequency path layer:

- Gold: Yahoo `GC=F` continuous COMEX Gold futures proxy, 2000-08-30 onward;
- S&P 500: `^GSPC`, 1970 onward;
- Nasdaq Composite: `NASDAQCOM`, 1971 onward;
- WTI: `DCOILWTICO`, 1986 onward;
- Broad USD: `DTWEXBGS`, 2006 onward;
- 2Y Treasury: `DGS2`, 1976 onward;
- 10Y Treasury: `DGS10`, 1962 onward;
- 10Y real yield: `DFII10`, 2003 onward;
- 5Y breakeven: `T5YIE`, 2003 onward.

Raw redistribution-uncertain Yahoo history is not committed. Source hashes and derived results are public-safe.

## 5. Gold FIRST_HIKE — descriptive distribution

Daily Gold support is only **n=3 FIRST_HIKE tightening legs** because the reproducible daily proxy begins in 2000.

Across those three legs:

| Metric | Median | Range / support |
|---|---:|---:|
| 20-observation endpoint | +1.03% | -0.89% to +2.40% |
| 60-observation endpoint | +4.69% | -3.99% to +17.08% |
| 120-observation endpoint | +12.71% | -11.23% to +18.52% |
| 252-observation endpoint | +6.81% | -0.35% to +7.90% |
| 252-observation MDD | 17.37% | 9.52% to 17.90% |
| MAE from event baseline | -1.40% | -15.48% to -1.14% |
| MFE from event baseline | +16.18% | +2.94% to +28.41% |
| time to event-relative trough | 19 obs | 2 to 162 |
| 50% recovery from MDD trough | 19 obs | 9 to 46 |
| 100% recovery from MDD trough | 150 obs | 95 to 629 |
| 60-observation annualized realized vol | 14.17% | 13.90% to 19.84% |

### Interpretation

The strongest current Gold finding is not a directional rule.

**DESCRIPTIVE RESULT:** positive long-horizon endpoints can coexist with substantial intra-window drawdowns and very long recovery paths.

This is precisely why endpoint return alone is an incomplete risk statistic.

## 6. Gold 2015 vs 2022 under one frozen specification

### 2015 FIRST_HIKE — 2015-12-16

- 20D: +1.03%
- 60D: +17.08%
- 120D: +18.52%
- 252D: +6.81%
- MDD: 17.37%
- MAE: -1.14%
- MFE: +28.41%
- full recovery from the MDD trough: 629 valid Gold observations

### 2022 FIRST_HIKE — 2022-03-16

- 20D: +2.40%
- 60D: -3.99%
- 120D: -11.23%
- 252D: -0.35%
- MDD: 17.90%
- MAE: -15.48%
- MFE: +2.94%
- event-relative trough: 162 valid observations after the anchor
- 50% recovery from the MDD trough: 19 observations
- 100% recovery: 95 observations

### Interpretation

**DESCRIPTIVE RESULT:** 2015 and 2022 produced materially different path shapes under the same event rule and horizons.

**NOT YET VERIFIED:** the module does not yet establish which predetermined macro states explain that heterogeneity.

## 7. Cross-asset FIRST_HIKE path risk

### S&P 500 — n=10 tightening legs

- 252D endpoint median: **+4.99%**
- MDD median: **11.31%**
- time-to-event-relative-trough median: **55 observations**
- 50% recovery median: **31 observations**
- 100% recovery median: **136 observations**
- 60D annualized realized-vol median: **15.95%**

### Nasdaq — n=10

- 252D endpoint median: **-0.82%**
- MDD median: **20.67%**
- time-to-event-relative-trough median: **63 observations**
- 50% recovery median: **38.5 observations**
- 100% recovery: n=9 observed, median **181 observations**
- 60D annualized realized-vol median: **17.92%**

### WTI — n=8

- 252D endpoint median: **+22.04%**
- MDD median: **30.16%**
- time-to-event-relative-trough median: **85.5 observations**
- 50% recovery median: **33.5 observations**
- full recovery: n=7 observed, median **70 observations**
- 60D annualized realized-vol median: **35.96%**

### Broad USD — n=2

Coverage is too small for a meaningful cycle-generalization statement.

### Treasury-rate layer

For FIRST_HIKE anchors:

- 2Y yield, n=10: median 252-observation change **+118.5 bp**;
- 10Y yield, n=10: median 252-observation change **+58 bp**;
- 10Y real yield, n=3: median 252-observation change **-6 bp**;
- 5Y breakeven, n=3: median 252-observation change **-11 bp**.

The real-yield and breakeven support is too small to explain Gold heterogeneity yet.

## 8. What this module does and does not establish

### DATA FACT

- v1.1 timing QC passes;
- 10 qualifying tightening legs exist under the frozen mechanical rule;
- modern scheduled decision dates are mapped separately from target effective dates;
- the daily Gold proxy supports only three FIRST_HIKE legs.

### DESCRIPTIVE RESULT

- endpoint returns can obscure materially larger path risk;
- equities, Nasdaq, WTI and Gold have very different MDD/recovery distributions around the same class of cycle anchor;
- 2015 and 2022 Gold paths differ substantially under identical measurement rules.

### CAUSAL EVIDENCE

**None.**

Realized Fed action remains a descriptive marker.

### FDR / multiple testing

No confirmatory p-value family is executed in this foundation module.

Therefore there are no FDR “discoveries” to report.

### OOS

Not applicable to this descriptive foundation. It is not a forecasting model.

### DEPLOYMENT

**NOT DEPLOYABLE.**

The outputs can inform a risk-distribution map and the design of later state-dependent tests, but not a deterministic trade rule.

## 9. Primary information gain

The main information gain is methodological and economic:

`endpoint return != path risk`

A positive 252-day return does not imply a benign path. The relevant investment-research object is the joint distribution of:

`endpoint + MDD + MAE/MFE + trough timing + volatility + recovery`.

## 10. Next locked research direction

The daily Gold layer is too short for a serious long-history claim.

The next module should therefore build a **native-frequency long-history Gold layer** from an openly licensed historical Gold series, extending the cycle sample backward without mixing monthly observations with daily futures data.

After that support expansion, the project can freeze state dependence using predetermined/PIT variables:

- inflation level/trend;
- growth state;
- yield-curve state;
- real-rate state;
- USD state;
- energy shock state;
- financial-condition state.

No state threshold should be tuned after observing Gold outcomes.
