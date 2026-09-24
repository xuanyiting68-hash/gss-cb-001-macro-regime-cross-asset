# ENERGY-WEEKLY-CONFIRMATION-009 — Post-Event Physical Confirmation Lock
Date: 2026-09-24
Status: **FROZEN BEFORE FIRST POST-EVENT WPSR RELEASE**

## 1. Purpose

Track whether weekly physical data **after** the frozen event `ENERGY005_2026-09-23` subsequently confirm:

- clean SUPPLY_NORMALIZATION;
- broad DEMAND_DESTRUCTION;
- or continued TIGHT_OR_MIXED conditions.

This does not rewrite the 2026-09-23 event label.

## 2. Information boundary

Use only:
- official EIA weekly series;
- actual/frozen WPSR release dates;
- the same seasonal-gap and 4-release-change mechanism definition as ENERGY-WEEKLY-STATE-004.

Do not use:
- future WTI returns;
- realized ENERGY005 4W/8W/13W outcomes;
- PortWatch to define U.S. stock-flow class;
- revised event thresholds.

## 3. Fresh post-event release clock

Preserve the QC-passed PIT-003 registry through its current final row.

For later 2026 week ends:
- fetch the four core EIA weekly grids;
- form the exact common week-ending grid;
- assign the official holiday exception where present;
- otherwise assign the following Wednesday under the frozen PIT-003 WPSR rule;
- include only releases whose release date is <= execution date.

No future scheduled release is treated as observed.

## 4. Mechanism classification

For every observed post-event release reuse the exact 004 mechanism rule:

DEMAND_DESTRUCTION if:
- demand_weak_count >=2; and
- throughput_weak = True.

SUPPLY_NORMALIZATION if:
- inventory_improving_count >=2;
- upstream_supply_up_count >=1;
- throughput_weak = False;
- demand_weak_count <=1.

Otherwise:
- TIGHT_OR_MIXED.

Incomplete cases remain DATA_INCOMPLETE.

The original ENERGY005 event class remains immutable.

## 5. Confirmation hysteresis

A single clean weekly classification is only a **candidate**.

### DEMAND_DESTRUCTION_CONFIRMED
Require two consecutive observed post-event WPSR releases classified DEMAND_DESTRUCTION.

### SUPPLY_NORMALIZATION_CONFIRMED
Require two consecutive observed post-event WPSR releases classified SUPPLY_NORMALIZATION.

### NO_CLEAN_CONFIRMATION
If neither two-release sequence has occurred.

This two-release rule is frozen before the first post-event WPSR release and is not tuned to WTI outcomes.

## 6. State priority

If both states somehow occur sequentially over time, preserve the full transition path.

Current-state label is determined by the last two observed post-event releases:
- same clean class twice -> corresponding CONFIRMED state;
- one clean class once -> corresponding CANDIDATE;
- otherwise -> NO_CLEAN_CONFIRMATION.

No historical row is deleted when state changes.

## 7. Append-only registry

Create:

`POST_EVENT_CONFIRMATION_REGISTRY.csv`

One row per observed WPSR release after 2026-09-23.

Capture:
- week end;
- release date;
- source hashes;
- mechanism class;
- inventory/demand/throughput/upstream counts;
- confirmation state after this release;
- append timestamp;
- previous hash / row hash.

Existing rows cannot be changed.

## 8. Current expected execution

As of 2026-09-24, the event release was 2026-09-23.

The next regular WPSR release has not yet occurred.

Expected:
- post-event observed releases = 0;
- confirmation registry rows = 0;
- current state = WAITING_NEXT_WPSR_RELEASE;
- no confirmation candidate or confirmed state.

## 9. Hard QC

Fail if:
- original ENERGY005 event is missing or not immutable TIGHT_OR_MIXED;
- any prospective realized WTI outcome is used;
- a future release date is included;
- mechanism rule differs from 004;
- confirmation is assigned from only one release;
- duplicate release dates/week ends occur;
- append-only hash chain fails.

## 10. Evidence boundary

**POST-EVENT PHYSICAL CONFIRMATION TRACKER / NO PRICE-OUTCOME USE / NOT CAUSAL / NOT DEPLOYABLE**
