# ENERGY-WEEKLY-OUTCOME-008 — Prospective Outcome Maturation Lock
Date: 2026-09-24
Status: **FROZEN BEFORE FIRST 4W PROSPECTIVE OUTCOME MATURITY**

## 1. Purpose

Mature ENERGY-WEEKLY-PROSPECTIVE-005 outcomes without changing the state known at event registration.

The prospective event snapshot and its historical reference distribution remain immutable.

Only frozen realized outcome fields may be populated after the required WTI observation count exists.

## 2. Upstream

Canonical prospective registry:

`results/energy_weekly_prospective_v1/PROSPECTIVE_EVENT_REGISTRY.csv`

Immutable snapshot chain:

`results/energy_weekly_prospective_v1/EVENT_CHAIN.csv`

Current first event:

`ENERGY005_2026-09-23`

Required current state before any realization:
- mechanism = TIGHT_OR_MIXED;
- realization_status = UNREALIZED;
- registration snapshot chain verifies.

## 3. WTI source and convention

Use the same official EIA/FRED DCOILWTICO acquisition path and exact outcome convention as ENERGY-WEEKLY-STATE-004.

For event release date R:

- execution anchor = first valid WTI observation strictly after R;
- p0 = WTI at execution anchor.

Frozen horizons:
- 4W = endpoint at 20 WTI observations after p0;
- 8W = endpoint at 40 observations after p0;
- 13W = endpoint at 65 observations after p0.

For horizon H with n observations:

require at least n+1 WTI observations beginning at the execution anchor.

Only then calculate:
- endpoint return;
- short MAE = maximum positive path return from p0;
- short MFE = negative of minimum path return from p0.

No calendar-day approximation may substitute for the observation-count rule.

## 4. Partial maturity

Horizon fields mature independently.

Allowed statuses:
- UNREALIZED;
- REALIZED_4W;
- REALIZED_8W;
- REALIZED_13W_COMPLETE.

Examples:
- if only 20-observation endpoint exists, write only 4W fields;
- do not infer 8W/13W from calendar time;
- once a horizon is realized it cannot be overwritten by a later source revision without an explicit versioned correction protocol.

## 5. Immutable registration snapshot

The first 23 prospective registry fields are immutable and chained in ENERGY-WEEKLY-PROSPECTIVE-005.

Before any realization:
- recompute the complete immutable chain;
- require every stored chain link to match.

Outcome maturation must not change any immutable field.

## 6. Append-only outcome audit

Create:

`OUTCOME_AUDIT.csv`

One row per event-horizon realization.

Fields include:
- sequence;
- event ID;
- horizon;
- realized timestamp UTC;
- execution date / WTI;
- endpoint date / WTI;
- DCOILWTICO raw-source SHA256;
- endpoint return;
- short MAE;
- short MFE;
- previous audit hash;
- row hash.

Each event-horizon pair is unique.

No audit row may be deleted or overwritten.

## 7. Registry integrity after realization

After writing newly matured outcome fields:
- preserve all immutable registration fields byte-for-value in canonical field order;
- update exact registry-file SHA256 in `REGISTRY_INTEGRITY.json`;
- leave the immutable event-chain tail unchanged;
- record count of realized horizons.

## 8. Current expected execution

On 2026-09-24 the 2026-09-23 event cannot possibly have 20 post-release WTI observations.

Expected:
- newly realized horizons = 0;
- realization status = UNREALIZED;
- outcome audit rows = 0;
- immutable snapshot chain = PASS.

This zero-result is the correct test of no-early-settlement behavior.

## 9. Hard QC

Fail if:
- prospective registry/event chain does not verify;
- any immutable field changes;
- a horizon is written before n+1 observations exist;
- an already realized event-horizon is recomputed or overwritten;
- duplicate event-horizon audit keys exist;
- execution date is not strictly after release;
- endpoint date is not after execution;
- source SHA is absent for a realized horizon;
- current run creates any 4W/8W/13W value without sufficient observations.

## 10. Evidence boundary

**PROSPECTIVE OUTCOME ACCOUNTING / NO NEW MODEL / NO RETUNING / NOT CAUSAL / NOT DEPLOYABLE**
