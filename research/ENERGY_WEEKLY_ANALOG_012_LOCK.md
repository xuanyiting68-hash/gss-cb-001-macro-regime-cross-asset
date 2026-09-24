# ENERGY-WEEKLY-ANALOG-012 — Prospective Historical Analog Benchmark Lock
Date: 2026-09-24
Status: **FROZEN BEFORE CURRENT EVENT OUTCOME MATURITY**

## 1. Purpose

Construct a prospective historical analog benchmark for the still-unrealized event:

`ENERGY005_2026-09-23`

The benchmark answers:

**Which completed historical TIGHT_OR_MIXED rollover events looked most similar at the time of release, using only pre-outcome frozen features?**

This is not a forecasting model.

## 2. Analog pool

Historical pool:

- selected ENERGY-WEEKLY-STATE-004 events;
- mechanism_class = TIGHT_OR_MIXED at event release;
- 8W and 13W WTI outcomes complete;
- exclude the live 2026-09-23 event.

Expected pool:

10 events.

## 3. Frozen feature set

Use only fields already frozen in the 004 event panel before outcomes:

Price state:
- WTI_r5;
- WTI_r63;
- GAS_r5;
- GAS_r63;
- HEAT_r5;
- HEAT_r63;
- JET_r5;
- JET_r63;
- pressure_score.

Physical mechanism state:
- inventory_improving_count;
- demand_weak_count;
- throughput_weak encoded 0/1;
- upstream_supply_up_count.

No outcome-derived feature enters the distance.

## 4. Scaling

Fit scaling only on the completed historical analog pool.

For each feature:
- center = historical median;
- scale = 1.4826 × MAD;
- if robust scale <=1e-12, fallback to historical sample standard deviation;
- if fallback scale <=1e-12, exclude that feature from distance.

The current live event does not affect scaling.

## 5. Distance

For every historical analog:

`distance = sqrt(mean(z_difference_j^2))`

over all active frozen features.

Equal weights.

No feature selection after seeing distances or outcomes.

## 6. Top-K

Freeze:

`K = 3`

before execution.

Report:
- top three historical analog event dates;
- distance;
- mechanism counts;
- realized 4W/8W/13W WTI;
- 8W/13W short MAE;
- unweighted top-3 median outcome reference.

No distance weighting.

No nearest-neighbor hyperparameter tuning.

## 7. Prospective benchmark status

Because current ENERGY005 outcomes are still blank, the analog set and top-3 reference are genuinely selected before current-event outcome maturity.

Future realized ENERGY005 outcomes may be compared with this frozen benchmark, but the analog set cannot be changed afterward.

## 8. Interpretation

Allowed:

- current state resembles historical events A/B/C under the frozen feature metric;
- historical analog paths were heterogeneous or concentrated;
- top-3 historical median provides a prospective reference distribution.

Not allowed:

- calling the top-3 median a validated forecast;
- changing K/features/scaling after current outcomes appear;
- using current outcome to reselect analogs.

## 9. Hard QC

Fail if:
- current event has any realized 4W/8W/13W outcome;
- historical pool size is not 10;
- current event enters scaling;
- outcome fields enter distance;
- top K differs from 3;
- distance has missing active features;
- current-event feature vector differs from frozen 004/005 values.

## 10. Evidence boundary

**GENUINELY PROSPECTIVE HISTORICAL ANALOG BENCHMARK / NO MODEL FIT TO OUTCOME / NOT CAUSAL / NOT DEPLOYABLE**
