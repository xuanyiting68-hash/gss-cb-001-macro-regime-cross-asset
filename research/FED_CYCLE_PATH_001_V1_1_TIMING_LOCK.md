# FED-CYCLE-PATH-001 v1.1 — Timing Ontology Lock
Date: 2026-09-24
Status: **FROZEN BEFORE CORRECTED ASSET-OUTCOME EXECUTION**

This amendment supersedes only the event-date/timing ontology of v1. All horizons, path-risk metrics, recovery definitions, raw-data boundaries and descriptive interpretation limits remain unchanged.

## 1. Separate policy implementation date from research event date

Every target change retains:

- `source_effective_date`: the date carried by the target-rate source;
- `event_date`: the date used to anchor asset outcomes;
- `event_date_basis`: the provenance class for `event_date`.

The source date is never overwritten.

## 2. Scheduled modern FOMC changes

For target changes from 1994 onward:

- construct the policy direction/run from the target series in source-effective-date order;
- if a target change lies within one calendar day after, on, or one calendar day before a scheduled FOMC decision date, anchor the asset event to that scheduled FOMC decision date;
- label `event_date_basis = FOMC_SCHEDULED_DECISION_DATE`.

This rule is fixed before corrected asset outcomes are examined.

Examples that are hard-QC assertions:

- the 2022 tightening first hike must anchor to **2022-03-16**, not the 2022-03-17 implementation date;
- the 2023 final scheduled hike must anchor to **2023-07-26**, not 2023-07-27;
- the 2024 first scheduled cut must anchor to **2024-09-18**, not 2024-09-19.

## 3. Historical pre-1994 target changes

For target changes before 1994:

- `event_date = source_effective_date`;
- `event_date_basis = HISTORICAL_TARGET_RECONSTRUCTION`.

These events are allowed in long-history descriptive path summaries but are not interpreted as exact contemporaneous FOMC announcement timestamps.

The report must separate this limitation from modern decision-day timing.

## 4. Scheduled-meeting calendar

The scheduled-decision registry uses Federal Reserve historical meeting pages plus an explicit modern decision-date supplement.

The modern supplement must include regular FOMC decision dates through the currently observed 2026 sample, and at minimum the 2025 decision dates:

- 2025-01-29
- 2025-03-19
- 2025-05-07
- 2025-06-18
- 2025-07-30
- 2025-09-17
- 2025-10-29
- 2025-12-10

and 2026 through 2026-09-16.

## 5. Pause-start timing

`PAUSE_START` is the first scheduled decision date strictly after the mapped `LAST_HIKE` event date and strictly before the mapped `FIRST_CUT` event date.

It remains a descriptive policy-cycle marker.

## 6. Emergency-cut ontology

Pre-1994 reconstructed target changes are **never** labeled `EMERGENCY_CUT`.

For 1994 onward, a >=25 bp target decline unmatched to a scheduled decision within the ±1-day mapping tolerance may enter the registry only as:

`EMERGENCY_CUT_CANDIDATE`

with:

- `event_date = source_effective_date`;
- `event_date_basis = UNSCHEDULED_EFFECTIVE_DATE_TIMING_UNRESOLVED`;
- `outcome_eligible = False`.

No `EMERGENCY_CUT_CANDIDATE` is included in asset-outcome calculations until its official announcement/decision timestamp is independently resolved.

This preserves the required emergency-event ontology without treating an implementation date as a verified announcement timestamp.

## 7. Tightening-cycle construction

The frozen v1 cycle-leg rule remains:

- consecutive positive target changes bounded by a negative target change or source-history edge;
- at least two positive changes;
- cumulative tightening >=50 bp.

This can produce more than one qualifying tightening leg in a calendar year. Such legs are mechanical policy-target legs, not claims of statistically independent macroeconomic cycles.

## 8. Asset-outcome event set

v1.1 asset outcomes are computed only for:

- `FIRST_HIKE`;
- `LAST_HIKE`;
- `PAUSE_START`;
- `FIRST_CUT`;
- `TIGHTENING_CYCLE_START`;
- `TIGHTENING_CYCLE_END`.

Emergency-cut candidates are registry-only until timing resolution.

## 9. Hard QC additions

The corrected run fails if:

- 2022 FIRST_HIKE is not 2022-03-16;
- 2023 LAST_HIKE for the 2022 leg is not 2023-07-26;
- 2024 FIRST_CUT for the 2022 leg is not 2024-09-18;
- any pre-1994 row is labeled `EMERGENCY_CUT` or `EMERGENCY_CUT_CANDIDATE`;
- a 2025 scheduled cut is classified as an emergency candidate solely because of missing calendar coverage;
- any timing-unresolved emergency candidate enters `EVENT_ASSET_METRICS.csv`;
- any original v1 MDD/recovery identity gate fails.

## 10. Evidence status

v1.1 remains:

**DESCRIPTIVE RESULT / REALIZED POLICY ACTION IS NOT AN IDENTIFIED MONETARY-POLICY SHOCK / NOT A FORECASTING MODEL / NOT DEPLOYABLE**

No causal claim is introduced by correcting the event timestamp.
