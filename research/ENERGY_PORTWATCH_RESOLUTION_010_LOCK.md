# ENERGY-PORTWATCH-RESOLUTION-010 — External Supply-Shock Resolution State Machine
Date: 2026-09-24
Status: **FROZEN BEFORE ANY FUTURE PORTWATCH RECOVERY SNAPSHOT**

## 1. Purpose

Define in advance when the external maritime supply-shock context identified in ENERGY-PORTWATCH-006 may be downgraded or resolved.

This prevents future price outcomes from driving an ad hoc declaration that the shock has ended.

No WTI outcome is used.

## 2. Inputs

Use the same official IMF PortWatch endpoints and frozen 006 traffic diagnostics for:

- Suez Canal;
- Bab el-Mandeb Strait;
- Strait of Hormuz;
- Cape of Good Hope.

Relevant official disruption text remains frozen to:
- Hormuz;
- Red Sea;
- Suez;
- Bab el-Mandeb / Mandeb.

Petroleum-stress chokepoints:
- Suez;
- Bab el-Mandeb;
- Hormuz.

## 3. Frozen traffic stress

Reuse 006 exactly.

### ACUTE_TRANSIT_STRESS
True if either:
- 7D total <=50% of prior-90D total mean; or
- 7D tanker <=50% of prior-90D tanker mean.

### STRUCTURAL_TRANSIT_STRESS
True if either:
- 30D total <=60% of prior-calendar-year total mean; or
- 30D tanker <=60% of prior-calendar-year tanker mean.

No new price-based threshold is introduced.

## 4. Resolution state machine

### CRITICAL_TRAFFIC_STRESS
If any petroleum chokepoint has either:
- ACUTE_TRANSIT_STRESS; or
- STRUCTURAL_TRANSIT_STRESS.

### TRAFFIC_RECOVERED_ALERT_ACTIVE
If:
- no petroleum chokepoint traffic-stress flag is active; but
- at least one relevant active PortWatch disruption has alertlevel RED.

### RESOLUTION_CANDIDATE
If:
- no petroleum traffic stress; and
- no relevant active RED disruption;
- but this is the first clean snapshot.

### RESOLVED
Require two clean snapshots satisfying:
- no petroleum traffic stress;
- no relevant active RED disruption;
- latest-settled dates are at least 7 calendar days apart.

Once RESOLVED, later clean snapshots remain RESOLVED.

Any renewed petroleum traffic stress immediately returns state to CRITICAL_TRAFFIC_STRESS.

Any renewed relevant RED alert with no traffic stress returns state to TRAFFIC_RECOVERED_ALERT_ACTIVE.

## 5. External-context boolean

`EXTERNAL_SUPPLY_SHOCK_CONTEXT_ACTIVE = True`

for:
- CRITICAL_TRAFFIC_STRESS;
- TRAFFIC_RECOVERED_ALERT_ACTIVE;
- RESOLUTION_CANDIDATE.

It becomes False only at:

`RESOLVED`.

Thus one clean snapshot cannot erase the external-risk veto.

## 6. Append-only snapshots

Create:

`PORTWATCH_STATE_REGISTRY.csv`

One row per materially new PortWatch snapshot, requiring:
- a newer latest-settled date; or
- a changed official relevant disruption-state hash.

Capture:
- snapshot timestamp;
- latest-settled date;
- relevant active RED count;
- petroleum traffic-stress boolean;
- Hormuz frozen traffic ratios;
- state;
- clean-snapshot streak;
- external-context boolean;
- source hashes;
- previous row hash / row hash.

No prior snapshot may be rewritten.

## 7. Current expected state

From the 006 snapshot:
- Hormuz acute stress = True;
- Hormuz structural stress = True;
- relevant active RED disruptions = 2.

Expected first state:

`CRITICAL_TRAFFIC_STRESS`

with:

`EXTERNAL_SUPPLY_SHOCK_CONTEXT_ACTIVE = True`.

## 8. Hard QC

Fail if:
- 006 traffic definitions change;
- any WTI outcome is loaded;
- required chokepoint names mismatch;
- a duplicate unchanged snapshot is appended;
- resolution is declared after only one clean snapshot;
- two clean snapshots used for RESOLVED are less than 7 days apart;
- append-only chain fails.

## 9. Evidence boundary

**EXTERNAL PHYSICAL-RISK STATE MACHINE / NO DIRECTIONAL FORECAST / NOT CAUSAL / NOT DEPLOYABLE**
