# ENERGY-WEEKLY-PROSPECTIVE-005 — Append-Only Live Energy Event Registry Lock
Date: 2026-09-24
Status: **FROZEN BEFORE THE FIRST LIVE EVENT OUTCOME IS OBSERVED**

## 1. Purpose

Convert ENERGY-WEEKLY-STATE-004 from a completed historical strict-PIT study into an append-only prospective event record.

The first live event is already present in the canonical 004 selected-event panel:

- release date: 2026-09-23;
- mechanism class: TIGHT_OR_MIXED;
- 4W / 8W / 13W WTI outcomes: not yet observed in the canonical panel.

The goal is to preserve the state exactly as known before those outcomes mature.

## 2. Upstream dependency

Canonical source:

`results/energy_weekly_state_v1/SELECTED_EVENT_PANEL.csv`

Required upstream module:

`ENERGY-WEEKLY-STATE-004`

Required upstream QC:

`PASS`

No reclassification is allowed inside this module.

## 3. Prospective event eligibility

A selected 004 event may be appended only if:

1. `SELECTED = True`;
2. release date is observed;
3. mechanism class is already assigned by the frozen 004 rules;
4. the event is not already in the prospective registry;
5. all frozen 4W/8W/13W endpoint and MAE/MFE outcome fields are blank at registration.

If any outcome is already available, the event cannot be backfilled as a prospective event.

## 4. Frozen state snapshot

For each registered event preserve at least:

- event ID;
- week end;
- release date;
- price-as-of date;
- upstream source-file SHA256;
- pressure score and prior q90;
- WTI/product short-horizon price changes;
- inventory-improving count;
- demand-weak count;
- throughput-weak flag;
- upstream-supply-up count;
- mechanism class;
- historical same-class completed-event support available at registration;
- historical same-class 8W/13W endpoint medians;
- historical same-class 8W/13W short-MAE medians;
- registration timestamp UTC.

These values are immutable after registration.

## 5. Interpretation map

This is a state label, not a trade command.

### TIGHT_OR_MIXED
`ROLLOVER_WITHOUT_CLEAN_PHYSICAL_CONFIRMATION`

Interpretation:
price rollover exists, but the frozen stock-flow mechanism does not identify either clean supply normalization or clean demand destruction.

### DEMAND_DESTRUCTION
`DEMAND_DESTRUCTION_CANDIDATE`

### SUPPLY_NORMALIZATION
`SUPPLY_NORMALIZATION_CANDIDATE`

### DATA_INCOMPLETE
`MECHANISM_DATA_INCOMPLETE`

No class-specific rule is altered based on subsequent WTI performance.

## 6. Outcome maturity

Frozen horizons inherit 004 exactly:

- 4W = 20 WTI observations;
- 8W = 40 WTI observations;
- 13W = 65 WTI observations.

For each horizon retain:
- endpoint return;
- short MAE;
- short MFE.

Realized fields may be appended only when available from the same upstream outcome convention.

No earlier state field may be rewritten during realization.

## 7. Evaluation

A single prospective event does not generate a significance claim.

For each realized event report:

- its realized path;
- its percentile/rank versus the historical same-class distribution frozen at registration;
- whether the realized direction matched or contradicted the historical class median.

Across multiple future registered events, only descriptive prospective calibration is reported until a new pre-frozen inferential design is written.

## 8. First live event

The first event must be:

`ENERGY005_2026-09-23`

Frozen 004 state:
- week end = 2026-09-18;
- price as of = 2026-09-22;
- mechanism = TIGHT_OR_MIXED;
- inventory improving count = 2;
- demand weak count = 1;
- throughput weak = True;
- upstream supply up count = 1.

Economic interpretation:

two inventory blocks improved and one upstream supply block improved, but refinery throughput weakened. Therefore the pre-frozen rule does **not** call this supply normalization.

## 9. Append-only integrity

Maintain:

- `PROSPECTIVE_EVENT_REGISTRY.csv`;
- `EVENT_CHAIN.csv`;
- `REGISTRY_INTEGRITY.json`.

Every new event row is chained by SHA256 to the previous row hash.

Existing event snapshots cannot be overwritten.

## 10. Hard QC

Fail if:

- 004 QC is not PASS;
- an event with any already-realized frozen outcome is registered retroactively;
- a duplicate event ID is appended;
- any prior immutable snapshot field changes;
- chain verification fails;
- upstream selected-event file hash is missing;
- the first event is not 2026-09-23 TIGHT_OR_MIXED;
- the first event has any outcome already populated at registration.

## 11. Evidence boundary

**GENUINELY PROSPECTIVE ENERGY EVENT REGISTRY / NO OUTCOME EVIDENCE YET / ASSOCIATIONAL STATE ONLY / NOT CAUSAL / NOT DEPLOYABLE**
