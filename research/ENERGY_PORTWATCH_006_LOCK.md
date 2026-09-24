# ENERGY-PORTWATCH-006 — Prospective External Maritime Shock Context Lock
Date: 2026-09-24
Status: **FROZEN BEFORE PORTWATCH EXECUTION / BEFORE ENERGY005 OUTCOME MATURITY**

## 1. Purpose

Add an independent external physical-shock context layer to the already frozen ENERGY-WEEKLY-PROSPECTIVE-005 event.

This module uses IMF PortWatch machine-readable maritime data and disruption records.

It does **not** retroactively reclassify ENERGY-WEEKLY-STATE-004 historical events.

## 2. Timing boundary

PortWatch daily AIS-derived records are published with a lag and may be revised.

Historical first-publication vintages are not reconstructed here.

Therefore:
- historical 004 events are not relabeled with today's PortWatch history;
- the current prospective event receives a retrieval-time snapshot only;
- the snapshot timestamp and source hashes are preserved before the event's 4W/8W/13W outcomes mature.

This is a prospective external-context overlay, not a historical strict-PIT backfill.

## 3. Official PortWatch endpoints

Daily chokepoint table:

`Daily_Chokepoints_Data/FeatureServer/0`

Required IDs and names:
- chokepoint1 = Suez Canal;
- chokepoint4 = Bab el-Mandeb Strait;
- chokepoint6 = Strait of Hormuz;
- chokepoint7 = Cape of Good Hope.

Fields:
- date;
- portid;
- portname;
- n_total;
- n_tanker;
- capacity_tanker;
- capacity.

PortWatch disruption database:

`portwatch_disruptions_database/FeatureServer/0`

Use fields including:
- eventid;
- eventtype;
- eventname;
- htmlname;
- htmldescription;
- alertlevel;
- fromdate;
- todate;
- severitytext;
- pageid.

Raw JSON is hashed but not committed.

## 4. Current traffic diagnostics

For each chokepoint, using the latest settled PortWatch date:

- 7-day mean total transits;
- 7-day mean tanker transits;
- prior 90-day mean total/tanker excluding the latest 7 days;
- prior-calendar-year mean total/tanker when available.

Predeclared flags:

### ACUTE_TRANSIT_STRESS
True if either:
- 7D total <= 50% of prior-90D total mean; or
- 7D tanker <= 50% of prior-90D tanker mean.

### STRUCTURAL_TRANSIT_STRESS
True if either:
- 30D total <= 60% of prior-calendar-year total mean; or
- 30D tanker <= 60% of prior-calendar-year tanker mean.

These thresholds are engineering context rules, not tuned to WTI outcomes.

### REROUTING_ELEVATED
Cape of Good Hope 7D total >= 125% of its prior-90D total mean.

## 5. Active disruption context

At retrieval time, preserve PortWatch disruptions that are active and whose text contains one of:

- Hormuz;
- Red Sea;
- Suez;
- Bab el-Mandeb / Mandeb.

The keyword list is frozen before retrieval.

## 6. Prospective event overlay

Required event:

`ENERGY005_2026-09-23`

The module reads only its immutable prospective registry state.

It does not use realized WTI outcome fields.

Snapshot:
- retrieval timestamp;
- latest settled date per chokepoint;
- traffic diagnostics/flags;
- active relevant disruption records;
- an overall boolean `EXTERNAL_SUPPLY_SHOCK_CONTEXT_PRESENT`.

Overall context is true if:
- at least one relevant official PortWatch disruption is active; or
- Hormuz, Bab el-Mandeb or Suez has ACUTE_TRANSIT_STRESS or STRUCTURAL_TRANSIT_STRESS.

Cape rerouting is supporting context, not sufficient by itself.

## 7. Interpretation

A positive external-shock context means:

the rollover occurs while an independently measured maritime disruption remains material.

It does **not** say WTI must rise or fall.

It acts as a mechanism-veto/context layer against over-interpreting U.S. stocks/flows as a complete global supply-normalization signal.

## 8. Hard QC

Fail if:
- any required chokepoint ID returns the wrong name;
- any required chokepoint has fewer than 2,500 daily rows;
- duplicate portid/date rows exist;
- latest settled data are more than 14 days old at retrieval;
- disruption database returns fewer than 100 records;
- the prospective event is missing, realized, or not TIGHT_OR_MIXED;
- any WTI outcome is used to set an external-context threshold;
- raw PortWatch JSON is committed.

## 9. Evidence boundary

**PROSPECTIVE EXTERNAL PHYSICAL CONTEXT / NO DIRECTIONAL FORECAST CLAIM / NOT CAUSAL / NOT DEPLOYABLE**
