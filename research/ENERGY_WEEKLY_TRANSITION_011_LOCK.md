# ENERGY-WEEKLY-TRANSITION-011 — Historical Post-Event Mechanism Transition Diagnostic
Date: 2026-09-24
Status: **POST-RUN DESCRIPTIVE DIAGNOSTIC / FROZEN BEFORE EXECUTION**

## 1. Purpose

Diagnose how previously completed TIGHT_OR_MIXED rollover events evolved over the next four WPSR releases.

This is a historical diagnostic designed after ENERGY-WEEKLY-STATE-004 and after the prospective two-release confirmation rule in ENERGY-WEEKLY-CONFIRMATION-009 was frozen.

It therefore cannot be confirmatory evidence.

## 2. Historical sample

Use selected ENERGY-WEEKLY-STATE-004 events satisfying:

- mechanism_class = TIGHT_OR_MIXED at the event release;
- 8W WTI outcome is complete.

Current expected sample size from 004:

10 events.

The prospective 2026-09-23 event is excluded because its outcome is not complete and because it belongs to the live validation path.

## 3. Post-event mechanism path

For each historical event, classify the next four observed WPSR releases using the **exact unchanged 004 mechanism rule**.

Record classes:
- T+1;
- T+2;
- T+3;
- T+4.

Do not alter:
- seasonal reference;
- four-release change;
- inventory/demand/throughput/upstream thresholds.

## 4. Apply the prospective 009 confirmation rule descriptively

Within the next four releases:

### DD_CONFIRMED_WITHIN_4
if any two consecutive releases are DEMAND_DESTRUCTION.

### SN_CONFIRMED_WITHIN_4
if any two consecutive releases are SUPPLY_NORMALIZATION.

### CLEAN_CANDIDATE_ONLY
if a clean class appears but never twice consecutively.

### REMAINS_MIXED_OR_INCOMPLETE
if no clean class appears.

If both DD and SN consecutive confirmations somehow occur, preserve the first confirmation and report the full path.

## 5. Descriptive outcomes

For each transition group report only:

- n;
- median WTI 4W / 8W / 13W;
- negative-return share;
- median short MAE 8W / 13W.

No p-values.
No FDR.
No threshold search.

## 6. Timing diagnostic

Report:
- first clean-class release number;
- first two-release confirmation number;
- share confirmed by T+2, T+3, T+4.

This informs how quickly a mixed rollover historically acquired clean physical confirmation.

## 7. Interpretation boundary

The diagnostic may support statements such as:

- clean confirmation is rare/common;
- demand-destruction confirmation tended to occur after N weekly releases;
- mixed states often persisted.

It may not support:
- causal claims;
- a validated trading rule;
- changing the current prospective event classification;
- changing 009 thresholds.

## 8. Hard QC

Fail if:
- historical completed TIGHT_OR_MIXED sample is not 10;
- prospective 2026-09-23 enters the historical diagnostic;
- 004 mechanism code is not reused;
- any event has duplicated post-event release rows;
- any T+k release is not strictly after the event release;
- p-values are generated.

## 9. Evidence boundary

**POST-RUN HISTORICAL TRANSITION DIAGNOSTIC / NO NEW INFERENCE FAMILY / NOT CAUSAL / NOT DEPLOYABLE**
