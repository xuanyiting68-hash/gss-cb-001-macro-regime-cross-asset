# FED-CYCLE-PROSPECTIVE-SHADOW-009 — Prospective Gold Shadow Benchmark Lock
Date: 2026-09-24
Status: **FROZEN BEFORE ANY NEW PROSPECTIVE PREDICTION**

## 1. Purpose

Convert the historical OOS-008 result into an append-only prospective validation architecture without reusing B04-B07 for tuning.

This module does **not** upgrade OOS-008 into a deployable model. It freezes how genuinely new evidence will be collected.

## 2. Upstream evidence boundary

Upstream module:

- `FED-CYCLE-GOLD-OOS-008`
- canonical status: `PRELIMINARY_OOS_CANDIDATE / WEAK AND BENCHMARK-SENSITIVE / NOT DEPLOYABLE`
- historical OOS episodes B04-B07 are **consumed evidence** for that specification.

B04-B07 may be used as historical training data once they are in the past for a genuinely new prospective episode, but they may not be used to alter features, target, thresholds, transformations, model family or success criteria.

## 3. Frozen prospective cycle eligibility

The prospective episode must inherit the existing FED-CYCLE-PATH-001 mechanical tightening-leg rule:

- consecutive positive target changes bounded by a negative target change or source-history edge;
- at least **2** positive target changes;
- cumulative tightening at least **50 bp**.

No provisional B08 test episode is created after only one 25 bp hike.

If a future edge run qualifies, broad-episode assignment inherits the existing broad-cluster rule. The current 2026 candidate is far enough from B07 that, if it later qualifies, it would become the next broad episode rather than being merged into B07.

## 4. No retroactive predictions

A forecast for month M may be registered only if:

1. the new tightening leg already satisfies the frozen qualification rule before month M begins;
2. FIRST_HIKE is already observed;
3. every model input is available before the prediction issue timestamp;
4. the prediction is written before its target outcome is observed;
5. no prediction is backfilled for an earlier month after qualification occurs.

Therefore, if cycle qualification is first achieved during month Q, the earliest eligible forecast month is Q+1.

## 5. Frozen target

Single target:

`GOLD_FWD_6M_RET`

Same economic meaning as OOS-008: Gold return from the completed month immediately before forecast month M through the end of M+5.

No alternative horizon is added inside this module.

## 6. Frozen model family

Prospective comparators:

### B0
Historical weighted mean.

### B1
- lagged Gold 3M return;
- lagged Gold 6M return;
- lagged Gold 6M volatility.

### B2
B1 plus:
- months since FIRST_HIKE.

### M3
B2 plus:
- real-time IPT YoY.

D4 current-revised INDPRO is **not** part of the live prospective path because the purpose is a genuinely point-in-time shadow benchmark.

No feature selection, regularization, threshold search, nonlinear transformation or target-window shopping is allowed.

## 7. Training/refit policy

At activation of a new eligible broad episode:

- fit B0/B1/B2/M3 using only prior broad episodes;
- only training rows whose 6M targets are fully realized before the new episode begins may enter;
- preserve the OOS-008 hierarchical weighting rule;
- training-fold standardization uses training data only;
- freeze coefficients and scalers for the entire prospective broad episode;
- never refit on outcomes from the active prospective episode.

This mirrors the episode-forward logic of OOS-008 and prevents intra-episode feedback.

## 8. Input provenance

Every prospective prediction must record:

- issue timestamp UTC;
- forecast month and target-end month;
- model-spec SHA256;
- code commit SHA;
- training cutoff and training episode IDs;
- Gold source commit/hash;
- real-time IPT source hash and vintage period;
- exact feature values;
- B0/B1/B2/M3 predictions.

A source update may supply new observations but may not silently rewrite a previously issued prediction.

## 9. Append-only prediction registry

Canonical registry:

`results/fed_cycle_prospective_shadow_v1/PREDICTION_REGISTRY.csv`

Rules:

- prediction IDs are immutable;
- existing prediction rows are never overwritten to improve fit;
- realized targets are appended only after the target becomes observable;
- forecast errors are computed from the originally issued prediction;
- corrections require a separate correction row / audit note, never deletion of the original row.

## 10. Evaluation

The active prospective episode is evaluated only after sufficient targets mature.

Report:

- MSE and MAE versus B0/B1/B2;
- signed bias;
- prediction range versus realized range;
- count of monthly wins;
- calibration diagnostics.

No statistical significance claim is made from a single future episode.

No deployment/trading claim is permitted without materially larger independent prospective evidence plus a separate trading-objective/cost/risk design.

## 11. Current 2026 gate

The public policy-change registry contains the 2026-09-16 scheduled FOMC hike, +25 bp.

Under the frozen mechanical-cycle rule this is currently only:

`PROSPECTIVE_CANDIDATE / NOT YET ELIGIBLE`

because the edge run has only one hike and cumulative tightening is only 25 bp.

The runner must therefore produce **zero prospective predictions** at this stage.

## 12. Hard QC

Fail if:

- policy-change dates are duplicated or unsorted;
- sign and HIKE/CUT labels conflict;
- a prospective episode is activated before the frozen 2-hike/50bp rule is met;
- a prediction is backfilled for a month beginning before qualification;
- any active-episode outcome enters model fitting;
- B04-B07 are used for specification tuning;
- an existing prediction row is deleted or silently rewritten;
- model-spec hash changes without a new explicit protocol/version;
- raw redistribution-uncertain data are committed.

## 13. Evidence label

Current module status before any eligible new episode:

**PROSPECTIVE ARCHITECTURE FROZEN / ARMED / NO NEW FORECAST EVIDENCE YET / NOT DEPLOYABLE**

This is a research-infrastructure milestone, not a positive forecasting result.
