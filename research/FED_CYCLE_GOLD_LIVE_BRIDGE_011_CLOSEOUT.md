# FED-CYCLE-GOLD-LIVE-BRIDGE-011 — Closeout
Date: 2026-09-24
Status: **QC PASS / PROXY FEATURE BRIDGE CANDIDATE / NO FORECAST PERFORMANCE EVIDENCE / NOT DEPLOYABLE**

## 1. Trigger

INPUT-TIMING-010 established that the exact World Bank monthly Gold source used by OOS-008 arrives too late for strict pre-target prospective issuance.

BRIDGE-011 therefore tests a single pre-frozen candidate:

`GC=F` continuous COMEX Gold futures daily close, aggregated to calendar-month mean.

No forecast outcome is used.

## 2. Reference and candidate

Reference:
- pinned World Bank Gold monthly series used by OOS-008.

Candidate:
- Yahoo Finance public chart history for `GC=F`;
- explicitly treated as a COMEX continuous futures proxy, not spot Gold;
- monthly proxy = arithmetic mean of valid daily closes;
- at least 10 daily observations required;
- raw Yahoo JSON not committed.

No scaling, calibration or regression bridge is fitted.

## 3. Coverage

Feature-complete overlap:

- **306 months**;
- 2001-03 through 2026-08;
- minimum daily proxy observations in an accepted month: **16**;
- duplicate daily dates: **0**.

## 4. Level sanity diagnostic

Although price level is not an OOS-008 model feature:

- median absolute relative monthly-price gap: **0.13%**;
- 95th percentile absolute relative gap: **0.71%**.

Frozen gates were <=2.0% and <=5.0%.

Both pass.

## 5. 3M return feature

Frozen thresholds:
- correlation >=0.98;
- median absolute difference <=1.5pp;
- sign agreement >=95%.

Observed:
- correlation: **0.99839**;
- median absolute difference: **0.19pp**;
- sign agreement: **99.02%**.

All pass.

## 6. 6M return feature

Frozen thresholds:
- correlation >=0.98;
- median absolute difference <=2.0pp;
- sign agreement >=95%.

Observed:
- correlation: **0.99939**;
- median absolute difference: **0.17pp**;
- sign agreement: **99.02%**.

All pass.

## 7. 6M volatility feature

Frozen thresholds:
- correlation >=0.90;
- median absolute difference <=0.006.

Observed:
- correlation: **0.99280**;
- median absolute difference: **0.000855**.

Both pass.

## 8. Era stability

Frozen era sign-agreement threshold: >=90%.

### 2000-2009
- 3M: 98.11%;
- 6M: 98.11%.

### 2010-2019
- 3M: 100%;
- 6M: 99.17%.

### 2020-present
- 3M: 98.75%;
- 6M: 100%.

All era gates pass.

## 9. Frozen gate outcome

Engineering gates:

**17/17 PASS.**

Bridge status:

`PROXY_FEATURE_BRIDGE_CANDIDATE`

This is a strong feature-measurement transport result, not a forecast result.

## 10. Important boundary

This module does **not** establish that:

- GC=F futures and World Bank/London Gold are the same instrument;
- OOS-008 was historically validated using GC=F;
- M3's historical OOS performance transfers unchanged;
- Yahoo is the final licensed production market-data source;
- the model is deployable.

The result establishes only that the three Gold input features used by OOS-008 are very close under the frozen proxy construction across the available overlap.

## 11. Workflow reproducibility note

The first GitHub Actions execution failed before research execution because `beautifulsoup4` was missing from the bridge workflow environment when importing the existing path runner.

The dependency was added and the exact same frozen research specification was rerun.

No threshold, source definition, feature, sample gate or interpretation rule changed.

The second run passed computational QC.

## 12. Research decision

The next legitimate step is a separately versioned prospective measurement amendment:

- historical training measurement remains the World Bank Gold series;
- live prospective Gold features may use the predeclared `GC=F` monthly-mean bridge;
- bridge provenance/hash must be recorded;
- the active prospective episode must remain outcome-isolated;
- no OOS-008 evidence is automatically inherited by the measurement-amended prospective specification;
- production/licensing suitability remains a separate deployment requirement.

## 13. Evidence boundary

**DATA TRANSPORT / MEASUREMENT EQUIVALENCE / PROXY CANDIDATE / NO FORECAST PERFORMANCE CLAIM / NOT CAUSAL / NOT DEPLOYABLE**
