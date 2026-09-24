# FED-CYCLE-ASIA-CREDIT-DIAG-006 — Asia Equity × High-Yield Credit Phase Diagnostics
Date: 2026-09-24
Status: **FROZEN BEFORE OUTCOME EXECUTION**

## 1. Purpose

Extend the public cross-asset phase map into shorter-history markets without pretending they have the same support as the long-history U.S./Gold/WTI sample.

Predeclared diagnostics:

### Asia equity price indices
- Hang Seng Index: Yahoo `^HSI`;
- Shanghai Composite: Yahoo `000001.SS`;
- Nikkei 225: Yahoo `^N225`;
- KOSPI Composite: Yahoo `^KS11`.

### High-yield credit stress
- ICE BofA US High Yield Index Option-Adjusted Spread: FRED `BAMLH0A0HYM2`.

The goal is historical path/stress mapping around realized U.S. Fed-cycle phases.

No causal Fed-to-Asia claim is made.

## 2. Canonical policy anchors

Use only:

`results/fed_cycle_path_v1_1/FED_TIGHTENING_CYCLES.csv`

Anchors:

- FIRST_HIKE
- LAST_HIKE
- PAUSE_START
- FIRST_CUT

Anchor dates are copied directly from the timing-corrected registry.

Pre-1994 timing retains the historical-target-reconstruction limitation.

## 3. Common timing convention

For any anchor in calendar month M0:

- baseline = monthly average in M-1;
- event month M0 is omitted;
- event-time months 1..12 = M+1..M+12.

No market receives a custom horizon.

## 4. Asia equity metrics

Daily Yahoo closes are aggregated to calendar-month averages.

For each market × cycle × anchor:

- +3M cumulative return;
- +6M cumulative return;
- +12M cumulative return;
- 12M maximum drawdown;
- event-relative MAE;
- MFE;
- MDD-trough month;
- late-trough share in months 7-12.

Recovery is not a primary output in this limited-support extension.

## 5. High-yield OAS metrics

Use FRED `BAMLH0A0HYM2` daily history aggregated to calendar-month average.

Baseline:

- M-1 monthly average OAS.

For M+1..M+12:

- OAS change from baseline in basis points;
- running maximum widening.

Cycle × phase metrics:

- +3M / +6M / +12M OAS change;
- maximum 12M widening;
- month of maximum widening.

No OAS threshold is optimized.

## 6. Broad-episode weighting

Use the same broad episode ontology as STATE-PANEL-002.

Within each market/observable × anchor:

- available mechanical legs in the same broad episode share total weight 1;
- each available broad episode contributes total weight 1.

## 7. Support labels

This module has **no primary-confirmatory tier**.

Support is classified only as:

### ADEQUATE_DIAGNOSTIC
- at least 4 mechanical legs;
- at least 4 broad episodes.

### LIMITED_SUPPORT
- at least 2 mechanical legs;
- at least 2 broad episodes;
- but below ADEQUATE_DIAGNOSTIC.

### INSUFFICIENT_SUPPORT
- fewer than 2 legs or fewer than 2 broad episodes.

These labels do not imply statistical confirmation.

The threshold is frozen before outcomes and is not relaxed after seeing results.

## 8. P0-C / China boundary

Shanghai and Hang Seng results are **descriptive Fed-cycle path diagnostics only**.

They do not resolve the existing P0-C identification gap.

Do not claim:

- U.S. Fed actions causally move A-shares;
- a formal Fed × China state interaction;
- a tradable China rule.

The existing P0-C quarantine remains in force.

## 9. Comparison outputs

For each Asia index × anchor:

- support;
- weighted median +3M/+6M/+12M return;
- weighted median 12M MDD;
- weighted median MDD-trough month;
- weighted late-trough share.

For HY OAS × anchor:

- support;
- weighted median +3M/+6M/+12M OAS change;
- weighted median maximum widening;
- weighted median peak-widening month.

## 10. No significance family

No p-value/FDR family is run.

Reasons:

- short market histories;
- overlapping phase windows;
- repeated cycles across anchors;
- module purpose is coverage mapping, not confirmatory ranking.

Any forecasting claim requires a separately frozen time-ordered OOS design.

## 11. Hard QC

Fail if:

- any included anchor differs from the canonical registry;
- event month enters a clean path;
- baseline M-1 is missing for a reported path;
- Asia-index MDD is negative;
- MDD-trough month is outside 1..12;
- HY OAS widening is not expressed consistently in basis points;
- broad-episode weights fail to sum to 1 inside an available market × anchor × episode cell;
- support labels do not follow the frozen thresholds;
- raw Yahoo/FRED histories are committed.

A single unavailable Yahoo symbol does not invalidate the entire module. It must be recorded as an acquisition failure and excluded from derived metrics rather than silently substituted.

## 12. Evidence status

Allowed:

- **DATA FACT**
- **DESCRIPTIVE RESULT**
- **LIMITED-SUPPORT DIAGNOSTIC**
- **MECHANISM CONTEXT**

Not allowed:

- causal Fed-to-Asia language;
- "best/worst market" ranking;
- optimized trading thresholds;
- OOS/deployment claims.

FDR: not applicable.
OOS: not a forecasting model.
Causality: none.
Deployment: none.
