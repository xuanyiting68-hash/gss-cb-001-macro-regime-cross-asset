# FED-CYCLE-PROSPECTIVE-GCF-012 — Proxy-Measurement Shadow Model Lock
Date: 2026-09-24
Status: **FROZEN BEFORE ANY PROSPECTIVE PROXY-MEASUREMENT PREDICTION**

## 1. Purpose

Create a separately versioned prospective Gold forecasting measurement specification after:

- OOS-008 produced a weak / benchmark-sensitive preliminary OOS candidate;
- INPUT-TIMING-010 showed the exact World Bank monthly Gold feature source is too delayed for strict pre-target issuance;
- GOLD-LIVE-BRIDGE-011 passed all 17/17 frozen feature-equivalence gates for a `GC=F` monthly-mean proxy.

This module freezes the model that could later be used for a true prospective episode.

It creates **no new forecast evidence** by itself.

## 2. Evidence inheritance boundary

Historical evidence remains attached to OOS-008.

This measurement-amended specification does **not** automatically inherit:

- OOS-008's preliminary OOS label;
- its MSE improvement;
- any forecast-performance claim.

BRIDGE-011 supports only feature measurement transport.

Therefore this module's initial evidence status is:

`PROXY_MEASUREMENT_SHADOW_READY / NO PROSPECTIVE EVIDENCE YET`.

## 3. Historical training measurement

Historical training data remain exactly the frozen OOS-008 feature panel:

`results/fed_cycle_gold_oos_v1/OOS_FEATURE_PANEL.csv`

Historical Gold predictors therefore remain World Bank monthly Gold features.

No historical `GC=F` replacement is used in model fitting.

Rationale: replacing historical training features after seeing bridge results would create a new backtest and risk contaminating consumed OOS evidence.

## 4. Live prospective measurement

For a future eligible prospective forecast month M only:

- `GOLD_RET_3M_LAGGED` is measured from calendar-month mean `GC=F` daily closes through M-1;
- `GOLD_RET_6M_LAGGED` likewise;
- `GOLD_VOL_6M_LAGGED` is the sample standard deviation of six monthly log changes ending M-1;
- each accepted proxy month requires >=10 valid daily observations;
- no calibration or mapping to World Bank Gold is fitted.

This is a deliberately versioned measurement substitution supported by BRIDGE-011.

## 5. Frozen target

Target remains:

`GOLD_FWD_6M_RET`

The target definition is unchanged from OOS-008 for eventual evaluation.

No target horizon alternative enters this module.

## 6. Frozen model family

### B0
Historical weighted mean.

### B1
- Gold 3M lagged return;
- Gold 6M lagged return;
- Gold 6M lagged volatility.

### B2
B1 plus:
- cycle age in months.

### M3
B2 plus:
- real-time IPT YoY.

No D4 current-vintage model enters the prospective path.

No regularization, feature selection, nonlinear transformation or hyperparameter search.

## 7. Freeze training model now

Because the current potential new episode begins in 2026 and all B01-B07 training targets are already realized, this module freezes the B0/B1/B2/M3 training model now.

Training data:

- B01-B07 only;
- all rows must have target-end periods strictly before 2026-09, the current candidate FIRST_HIKE month;
- hierarchical weights exactly as OOS-008:
  1. each broad episode total weight 1;
  2. within broad episode each mechanical cycle equal total weight;
  3. within cycle rows equal.

For B1/B2/M3:

- weighted linear regression with intercept;
- training-only weighted means/standard deviations;
- no variable selection;
- zero-variance predictor standardized to zero;
- coefficients/scalers serialized and hashed.

These frozen coefficients may not be altered if the current 2026 candidate later qualifies.

If the 2026 candidate never qualifies and a materially later cycle becomes the next prospective episode, a new protocol/version is required.

## 8. Prospective episode eligibility

Same frozen mechanical rule as PATH-001 / SHADOW-009:

- consecutive positive target changes bounded by a negative target change or source-history edge;
- at least 2 hikes;
- cumulative tightening >=50 bp.

Current 2026 edge run remains ineligible at 1 hike / 25 bp.

No prediction is created while ineligible.

## 9. Future issuance requirements

A future prediction requires all of:

1. current 2026 edge run has qualified under the frozen cycle rule;
2. forecast month is strictly after the qualification month;
3. no retroactive/backfilled forecast;
4. frozen model hash matches this module;
5. BRIDGE-011 remains the referenced measurement bridge;
6. completed M-1 `GC=F` monthly mean is available under the frozen proxy construction;
7. real-time IPT is available under the frozen M-2/M-14 same-vintage rule;
8. issue timestamp precedes the start of forecast month M;
9. active-episode outcomes have never entered training.

Actual issuance is a separate step and must append to an immutable prediction registry.

## 10. Production data boundary

Yahoo public chart history is a research acquisition path, not a declaration that production/commercial market-data licensing is resolved.

A production deployment requires an appropriate licensed data source or contractual right.

## 11. Hard QC

Fail if:

- bridge status is not `PROXY_FEATURE_BRIDGE_CANDIDATE`;
- training panel is not 165 rows / 7 broad episodes;
- any training target ends on/after the 2026 candidate FIRST_HIKE month;
- B04-B07 are removed from final historical training after their OOS role is complete;
- model features differ from the frozen family;
- training weights violate the frozen hierarchy;
- any outcome from the current prospective episode enters training;
- any prediction is created while the current cycle is ineligible;
- coefficient/model hash changes on rerun without a new protocol version.

## 12. Evidence boundary

**PROXY-MEASUREMENT PROSPECTIVE MODEL FREEZE / NO NEW FORECAST PERFORMANCE EVIDENCE / NOT CAUSAL / NOT DEPLOYABLE**
