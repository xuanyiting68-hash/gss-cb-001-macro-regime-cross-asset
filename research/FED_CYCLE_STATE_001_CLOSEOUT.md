# FED-CYCLE-STATE-001 — Closeout
Date: 2026-09-24
Status: **QC-PASSED DESCRIPTIVE / SMALL-N MECHANISM CANDIDATES / NOT CONFIRMATORY / NOT DEPLOYABLE**

## 1. Question

Can predetermined or release-lag-aware macro/market states help describe why Gold paths differ across the 10 frozen FIRST_HIKE tightening legs?

This module does **not** ask which variable causally "drives" Gold.

## 2. Timing and data status

Hard QC passes:

- FIRST_HIKE event rows: 10;
- market-timing violations: 0;
- macro M-2 timing violations: 0;
- unsupported splits presented as supported: 0;
- raw source histories committed: false.

Information classes remain explicit:

- yield curve and WTI: `PREDETERMINED_MARKET_HISTORY`;
- CPI/INDPRO/NFCI: `RELEASE_LAG_AWARE_CURRENT_VINTAGE_NOT_STRICT_ALFRED_PIT`.

Current-vintage revised macro histories are **not** labeled real-time vintages.

## 3. Supported primary state contrasts

Support rule: at least 3 FIRST_HIKE episodes in each binary state.

### Inflation level: HIGH (>3%) vs LOW_OR_MODERATE

Support: 5 vs 5.

Gold +12M median:

- HIGH: **-11.76%**
- LOW_OR_MODERATE: **+6.54%**
- oriented median difference: **-18.30 percentage points**
- leave-one-leg-out sign stability: **10/10 same sign**

24M Gold MDD median:

- HIGH: **22.54%**
- LOW_OR_MODERATE: **13.66%**
- difference: **+8.88 percentage points**
- LOO sign stability: **10/10**

**MECHANISM CANDIDATE, NOT CAUSAL:** high CPI level is associated in this small event sample with weaker +12M Gold endpoints and deeper 24M drawdowns.

### Inflation direction: RISING vs FALLING_OR_FLAT

Support: 7 vs 3.

Gold +12M median:

- RISING: **+3.07%**
- FALLING_OR_FLAT: **-11.76%**
- difference: **+14.84 percentage points**
- computable LOO sign stability: **7/7**

24M MDD median:

- RISING: **14.09%**
- FALLING_OR_FLAT: **19.91%**
- difference: **-5.82 percentage points**
- LOO sign stability: **7/7**

This differs from the inflation-level contrast. That is not treated as a contradiction to be tuned away: level and direction encode different episode structures.

### Growth state: STRONG (INDPRO YoY >=2%) vs WEAK

Support: 6 vs 4.

Gold +12M median:

- STRONG: **-3.51%**
- WEAK: **+4.80%**
- difference: **-8.31 percentage points**
- LOO sign stability: **10/10**

24M MDD median:

- STRONG: **18.16%**
- WEAK: **15.48%**
- difference: **+2.67 percentage points**
- LOO sign stability: **10/10**

This is a descriptive mechanism candidate only. INDPRO is current-vintage rather than strict historical vintage.

### Energy direction: WTI 126-observation RISING vs FALLING_OR_FLAT

WTI support begins later, so usable support is 5 vs 3.

Gold +12M median:

- RISING: **+3.62%**
- FALLING_OR_FLAT: **-2.58%**
- difference: **+6.21 percentage points**
- computable LOO sign stability: **7/7**

24M MDD median:

- RISING: **16.40%**
- FALLING_OR_FLAT: **13.66%**
- difference: **+2.74 percentage points**
- LOO sign stability: **7/7**

This does not establish that oil direction drives Gold. It is a candidate state relation for a better-powered continuous panel design.

## 4. Unsupported primary state contrasts

### Yield curve

- INVERTED: **0**
- POSITIVE: **10**

There is no FIRST_HIKE cross-sectional variation under the frozen 10Y-2Y definition.

Therefore the current event sample cannot answer whether curve inversion changes post-FIRST_HIKE Gold behavior.

### Ex-ante real-rate proxy

- POSITIVE: **9**
- NONPOSITIVE: **1** — 2022 only.

The split is insufficient and perfectly time-separated at the one nonpositive observation.

The actual TIPS 10Y real-yield series `DFII10` has only **3** FIRST_HIKE observations.

Therefore:

**NOT YET VERIFIED:** this event-level sample cannot establish a real-yield state effect.

### NFCI

- TIGHT: **2**
- LOOSE_OR_AVERAGE: **8**

Insufficient support.

## 5. USD diagnostic

The frozen source bridge passes:

- six-month return-sign agreement between legacy `TWEXM` and modern `DTWEXAFEGS`: **95.74%**.

FIRST_HIKE support is balanced:

- USD RISING: 5;
- FALLING_OR_FLAT: 5.

Naively, the descriptive contrast is large:

- +12M Gold median: +3.62% vs -11.76%;
- MDD median: 13.66% vs 22.54%;
- LOO signs remain stable.

But the chronological audit finds **perfect era separation**:

- all five FALLING_OR_FLAT events: **1983-1988**;
- all five RISING events: **1994-2022**.

Therefore the USD contrast is classified:

**ERA-CONFOUNDED DESCRIPTIVE DIAGNOSTIC**

It cannot establish USD direction as a Gold mechanism in this sample.

## 6. What can and cannot be said

### DATA FACT

- all state timestamps pass the frozen timing QC;
- four primary binary states have n>=3 on both sides;
- yield curve, real-rate proxy and NFCI do not have adequate event-level contrast support;
- USD passes the source bridge but is perfectly separated by historical era.

### DESCRIPTIVE RESULT

Inflation level/direction, growth and energy direction produce nontrivial historical differences in Gold +12M and MDD medians.

### ASSOCIATIONAL EVIDENCE

At most **hypothesis-generating**.

The group differences are small-n, repeated across only 10 mechanical tightening legs, and part of the macro state data are current-vintage rather than strict ALFRED vintages.

### CAUSAL EVIDENCE

**None.**

### FDR

**Not run.**

No raw p-value family is generated in STATE-001 because the event sample is too small for a credible multi-split confirmatory exercise.

### OOS

**Not applicable.**

This is not a forecasting model.

### DEPLOYMENT

**Not deployable.**

## 7. Core research conclusion

The current evidence does not justify a statement such as:

`Real Yield / USD / Oil is the dominant driver of Gold after Fed hikes.`

A more defensible conclusion is:

`Gold heterogeneity is state-dependent in ways worth testing, but the 10-event cross-section is too small and too confounded to identify a dominant state variable.`

The strongest supported role of STATE-001 is **feature selection for the next design**, not mechanism confirmation.

## 8. Next research design

The next high-information module should move from one row per FIRST_HIKE to a **within-cycle monthly state panel**.

Reason:

- n=10 is too small for multivariate event-level mechanism inference;
- a monthly panel creates repeated within-cycle state transitions rather than comparing only ten starting points;
- continuous state variables can be used instead of arbitrary binary labels;
- cycle fixed effects / cycle clustering can absorb persistent era differences;
- inference can be clustered/block-bootstrap by policy cycle;
- state variables must remain lagged/predetermined;
- revised macro variables should either use ALFRED vintages or retain an explicit current-vintage limitation.

Candidate continuous states:

- CPI YoY level and 3M change;
- industrial-production YoY;
- 10Y-2Y slope;
- nominal 10Y;
- real-rate proxy / TIPS where available;
- WTI 6M return;
- USD 6M return with source-regime controls;
- NFCI.

Primary outcome should remain Gold monthly path risk rather than a single endpoint.
