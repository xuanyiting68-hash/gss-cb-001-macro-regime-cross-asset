# FED-CYCLE-STATE-PANEL-002 — Within-Cycle Continuous-State Lock
Date: 2026-09-24
Status: **FROZEN BEFORE PANEL OUTCOME EXECUTION**

## 1. Purpose

Upgrade FED-CYCLE-STATE-001 from a 10-row FIRST_HIKE cross-section to a within-cycle monthly panel.

The goal is to test whether **within the same mechanical tightening leg**, changes in predeclared macro/market states are associated with subsequent Gold path risk.

This is designed to reduce, not eliminate:

- era confounding;
- arbitrary binary-regime dependence;
- domination by long cycles;
- false precision from overlapping monthly outcomes.

It remains associational and non-causal.

## 2. Cycle sample

Canonical cycle registry:

`results/fed_cycle_path_v1_1/FED_TIGHTENING_CYCLES.csv`

All 10 frozen mechanical tightening legs remain eligible.

For each cycle:

- first eligible panel month = first complete calendar month after `FIRST_HIKE`;
- last eligible panel month = calendar month immediately before `FIRST_CUT`;
- maximum window = first 36 complete months after `FIRST_HIKE`.

Thus:

`panel_end = min(month_before_FIRST_CUT, FIRST_HIKE_month + 36)`.

The FIRST_CUT month is excluded.

No panel month is chosen based on Gold outcomes.

## 3. Broad episode clusters

Mechanical legs that begin within **18 calendar months** of the immediately preceding eligible leg are assigned to the same broad episode cluster.

The rule is applied chronologically before outcome analysis.

Purpose: nearby target-rate legs are not treated as fully independent macroeconomic experiments.

Expected structure under the frozen registry:

- 1983 and 1984 legs cluster together;
- 1987 Jan, 1987 Aug and 1988 legs cluster together;
- 1994, 1999, 2004, 2015 and 2022 form separate later clusters.

Primary inference uses broad episode clusters.

Mechanical-cycle clustering is sensitivity only.

## 4. Gold source and monthly timing

Gold source remains the pinned, openly licensed monthly series used in:

`FED-CYCLE-GOLD-LONGHIST-MONTHLY-001`

Pinned source:

- repository: `datasets/gold-prices`;
- commit: `95bfea9197222dcda13d8c4d9928fb631fe745aa`;
- 1960+ source: World Bank Commodity Markets;
- pre-1960 repeated annual averages excluded.

For panel decision month `M`:

- baseline Gold = monthly average in `M-1`;
- first outcome month = `M`;
- 3-month endpoint = monthly average in `M+2`;
- 6-month endpoint = monthly average in `M+5`.

The baseline and six complete outcome months define the forward path.

## 5. Primary Gold outcomes

### O1. Forward 6-complete-month endpoint return

`GOLD_FWD_6M_RET = Gold(M+5) / Gold(M-1) - 1`

### O2. Forward 6-complete-month maximum drawdown

Using:

`[Gold(M-1), Gold(M), ..., Gold(M+5)]`

compute peak-to-trough maximum drawdown.

This is a path-risk outcome, not an endpoint.

## 6. Secondary Gold outcomes

Fixed before execution:

- forward 3-complete-month endpoint return;
- forward 3-complete-month MDD;
- forward 6-month MAE from the M-1 baseline;
- forward 6-month MFE from the M-1 baseline;
- forward 6-month downside semivolatility.

Secondary outcomes do not enter the primary multiple-testing family.

## 7. State timing

Panel information date is the **start of month M**.

No state observation dated on or after the first day of M may enter a strict pre-month market state.

### 7.1 Current-vintage macro states

These remain explicitly:

`RELEASE_LAG_AWARE_CURRENT_VINTAGE_NOT_STRICT_ALFRED_PIT`

For decision month M:

- CPI state month = M-2;
- INDPRO state month = M-2.

### 7.2 Strict pre-month market history

For yields, WTI, NFCI and USD:

- use the last valid observation strictly before the first calendar day of M;
- trailing market returns use only observations dated before M.

## 8. Primary predictor family

STATE-001 selected the following four mechanism candidates before this panel was designed.

No other predictor is added to the primary family.

### X1. CPI YoY level

`CPI_YOY = CPI(M-2)/CPI(M-14)-1`

### X2. CPI YoY 3-month change

`CPI_MOMENTUM = CPI_YOY(M-2) - CPI_YOY(M-5)`

### X3. Industrial-production YoY

`INDPRO_YOY = INDPRO(M-2)/INDPRO(M-14)-1`

### X4. WTI approximately six-month return

Using daily `DCOILWTICO`:

- last valid observation strictly before M;
- observation 126 valid WTI observations earlier.

`WTI_6M_RET = P_t/P_{t-126}-1`

## 9. Secondary continuous diagnostics

These are predeclared diagnostics but do not enter the primary FDR family:

- 10Y-2Y curve slope in bp;
- 10Y nominal Treasury yield;
- nominal-10Y-minus-CPI real-rate proxy;
- NFCI;
- USD approximately six-month return;
- 10Y TIPS real yield `DFII10` where available.

USD uses the same own-series regime rule as STATE-001:

- `TWEXM` before 2020;
- `DTWEXAFEGS` from 2020 onward.

No level splicing.

STATE-001's 95.74% overlap sign-agreement audit is retained as the source-regime diagnostic.

## 10. Estimator

Each predictor/outcome test is estimated separately.

### 10.1 Cycle fixed effects

For the test-specific complete-case sample:

- demean predictor within each mechanical cycle;
- demean outcome within each mechanical cycle.

This removes each cycle's time-invariant level.

### 10.2 Equal-cycle weighting

Long cycles must not dominate short cycles.

Within each test:

- a cycle with `n_g` usable monthly rows receives row weight `1/n_g`.

Therefore each mechanical cycle contributes total weight 1.

### 10.3 Predictor scaling

The within-cycle demeaned predictor is divided by its equal-cycle-weighted RMS scale.

Reported coefficient:

**change in Gold outcome per one within-cycle state standard-deviation move**.

Outcome remains in decimal-return/drawdown units.

## 11. Dependence-aware primary inference

Monthly forward outcomes overlap heavily.

Rows are therefore **never** treated as independent observations.

### 11.1 Primary p-value

Use exact broad-episode cluster sign-flip inference.

For each test:

1. compute the equal-cycle-weighted within-cycle score contribution for each broad episode cluster;
2. enumerate all `2^G` sign assignments for the G usable broad episode clusters;
3. compare the absolute observed summed score with the exact sign-flip distribution.

The reported `p_broad_exact` is two-sided.

Minimum support:

- at least 5 mechanical cycles;
- at least 4 broad episode clusters;
- non-zero within-cycle predictor variation.

Otherwise: `INSUFFICIENT_SUPPORT`.

### 11.2 Mechanical-cycle sensitivity

Repeat the sign-flip test treating each mechanical cycle as the cluster.

This is sensitivity only because nearby early legs may not be independent.

## 12. Multiple-testing family

Primary family:

`4 predictors × 2 primary outcomes = 8 tests`.

Primary multiplicity control:

- **Benjamini-Yekutieli FDR at 10%**, using `p_broad_exact`.

BY is chosen because it controls FDR under arbitrary dependence and the eight tests share overlapping outcomes/states.

Also report BH q-values as a less-conservative diagnostic, but:

**public confirmatory language follows BY, not BH.**

No horizon, predictor or family member is removed after seeing results.

## 13. Robustness diagnostics

For each supported primary test:

- leave-one-broad-episode-out coefficient sign stability;
- coefficient under mechanical-cycle sign-flip sensitivity;
- usable row count;
- mechanical cycle count;
- broad episode count.

These are robustness diagnostics, not separate discoveries.

## 14. Hard QC

Fail if:

- any panel state month is outside the frozen active-cycle window;
- FIRST_CUT month enters the panel;
- any market-state observation date is on/after the first day of panel month;
- CPI/INDPRO state month is later than M-2;
- Gold source differs from the pinned monthly source;
- a cycle's total regression weight differs materially from 1;
- primary family is not exactly 8 tests;
- unsupported tests receive p-values/discovery labels;
- raw source histories are committed;
- primary inference uses row-level IID standard errors.

## 15. Evidence language

Allowed:

- **DATA FACT**
- **DESCRIPTIVE RESULT**
- **ASSOCIATIONAL EVIDENCE**
- **MECHANISM CANDIDATE**
- **NOT YET VERIFIED**

Not allowed:

- causal wording;
- "predicts" unless a separately locked OOS forecasting design is run;
- "dominant driver" rankings from coefficient size alone;
- deployment/trading claims.

## 16. OOS and deployment

- OOS: **NOT A FORECASTING MODEL**
- causal evidence: **NONE**
- deployment: **NOT DEPLOYABLE**

A BY-FDR survivor, if any, would mean a dependence-aware within-cycle historical association survived the frozen family. It would still not establish causality or live trading value.
