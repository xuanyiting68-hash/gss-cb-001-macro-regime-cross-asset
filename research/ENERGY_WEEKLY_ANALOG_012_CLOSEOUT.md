# ENERGY-WEEKLY-ANALOG-012 — Closeout
Date: 2026-09-24
Status: **QC PASS / GENUINELY PROSPECTIVE HISTORICAL ANALOG BENCHMARK / CURRENT OUTCOME UNREALIZED**

## 1. Purpose

Freeze the closest completed historical TIGHT_OR_MIXED analogs to ENERGY005_2026-09-23 before any current 4W/8W/13W outcome is observed.

## 2. Analog design

Historical pool:
- 10 completed TIGHT_OR_MIXED events.

Frozen feature set:
- 9 price-state features;
- 4 physical-mechanism features;
- 13 active features total.

Scaling:
- historical-pool median/MAD;
- SD fallback only when MAD is zero.

Distance:
- equal-weight RMS standardized distance.

Top K:
- 3.

Current event does not enter scaling.
No outcome field enters distance.
No model is fit to outcome.

## 3. Top three analogs

### 1. 2004-11-03
Distance: 0.776

Pre-outcome mechanism:
- inventory improving 2;
- demand weak 1;
- throughput weak True;
- upstream supply up 1.

Outcomes:
- 4W -4.99%;
- 8W +6.82%;
- 13W +23.75%;
- short MAE 8W +15.48%;
- short MAE 13W +23.75%.

This is especially close because the physical count state matches the current event exactly and the pressure score is nearly identical.

### 2. 2017-09-13
Distance: 1.395

Outcomes:
- 4W +1.50%;
- 8W +14.64%;
- 13W +14.90%;
- short MAE 8W +15.00%;
- short MAE 13W +18.21%.

### 3. 2018-05-31
Distance: 1.493

Outcomes:
- 4W +12.64%;
- 8W +8.18%;
- 13W +6.09%;
- short MAE 8W/13W +17.63%.

## 4. Frozen top-3 prospective reference

- median WTI 4W: +1.50%;
- median WTI 8W: +8.18%;
- median WTI 13W: +14.90%;
- 8W range: +6.82% to +14.64%;
- 13W range: +6.09% to +23.75%;
- median short MAE 8W: +15.48%;
- median short MAE 13W: +18.21%.

All three analogs were positive at both 8W and 13W.

## 5. Current event state

ENERGY005_2026-09-23 remains:

- outcome UNREALIZED;
- TIGHT_OR_MIXED;
- external supply-shock context active;
- external PortWatch state CRITICAL_TRAFFIC_STRESS;
- zero post-event WPSR confirmation rows.

Therefore the analog benchmark is frozen before current outcome information.

## 6. Interpretation

The analog benchmark is consistent with the earlier 004A 8W bearish-confirmation veto.

However:
- n=3 is small;
- analog matching is not a forecast model;
- all analog outcomes are historical;
- current geopolitical context may differ materially.

The top-3 reference is therefore a prospective benchmark, not a directional forecast.

## 7. Boundary

**PROSPECTIVE HISTORICAL ANALOG BENCHMARK / NO OUTCOME-FITTED MODEL / NOT CAUSAL / NOT DEPLOYABLE**
