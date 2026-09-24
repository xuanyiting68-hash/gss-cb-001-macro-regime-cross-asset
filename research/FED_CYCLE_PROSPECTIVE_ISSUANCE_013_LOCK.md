# FED-CYCLE-PROSPECTIVE-ISSUANCE-013 — Append-Only Forecast Issuance Lock
Date: 2026-09-24
Status: **FROZEN BEFORE ANY PROSPECTIVE FORECAST ISSUANCE**

## 1. Purpose

Freeze the operational gate that may append the first genuinely prospective prediction for the proxy-measurement model in FED-CYCLE-PROSPECTIVE-GCF-012.

This module cannot alter the model. It can only decide:

- issue one immutable prediction row; or
- refuse issuance and record why.

At freeze date the correct result is refusal because the current 2026 tightening edge run is only 1 hike / 25 bp.

## 2. Immutable upstream dependencies

Required prospective specification SHA256:

`f3d3eff3020af41665da93151962d0a488b14f642bf3e7e68dcf16cb156787b4`

Required frozen training-model SHA256:

`96520e9316a0cbcc18085f0dfa2d7432fab9892d715e7893fcf5ad2b172ba50d`

Required measurement bridge:

`FED-CYCLE-GOLD-LIVE-BRIDGE-011 / PROXY_FEATURE_BRIDGE_CANDIDATE`

If any dependency differs, issuance must fail closed.

## 3. Cycle activation

Inherit the frozen mechanical tightening rule:

- consecutive positive target changes since the last cut;
- at least 2 hikes;
- cumulative tightening >= 50 bp.

The date of the hike that first satisfies both conditions is the qualification date.

The earliest prospective forecast month is the month after qualification.

No forecast month before that month may ever be backfilled.

## 4. Forecast-month selection

The issuer never searches historical months.

On a run at UTC timestamp T:

- candidate forecast month = calendar month immediately after the month containing T;
- required live Gold feature month = candidate forecast month - 1.

The issuer may create a row only if the candidate forecast month is at or after the frozen earliest prospective forecast month.

This deliberately avoids walking backward through missed months.

## 5. Strict issue-time rule

Prediction issue timestamp must be strictly before the first instant of the candidate forecast month in UTC.

The completed M-1 Gold proxy features and RT-IPT input must already be available at issue time.

If the input is not ready before the boundary, that month's forecast is skipped permanently.

No late issuance.

## 6. Live Gold measurement

Use BRIDGE-011 exactly:

- Yahoo public chart history for `GC=F`;
- daily close;
- calendar-month arithmetic mean;
- minimum 10 valid daily closes in every month required by the feature window;
- 3M and 6M lagged returns;
- 6M volatility = sample standard deviation of six monthly log changes.

No calibration to World Bank Gold.

To avoid issuing from an incomplete current calendar month, the required Gold month is considered complete only if:

- the run date is the last calendar day of that month; and
- the proxy contains a valid daily observation on or after the last Monday-Friday calendar date of that month minus 3 calendar days.

This is a conservative operational gate. Failure means skip, not threshold tuning.

## 7. Real-time IPT

Use the VINTAGE-AUDIT-007 rule:

For forecast month M:

- target industrial-production observation = M-2;
- comparison observation = M-14;
- both from the same RTDSM vintage;
- selected vintage <= M-1.

The YoY input must be numerically available at issue time.

## 8. Cycle age

`CYCLE_AGE_MONTHS` is the calendar-month distance from FIRST_HIKE month to forecast month M.

FIRST_HIKE is already observed.

No LAST_HIKE or future policy information is used.

## 9. Frozen prediction calculation

Load the exact 012 serialized weighted means, weighted SDs and coefficients.

For B1/B2/M3:

`prediction = intercept + sum(beta_j * ((x_j - mean_j) / sd_j))`

for active features.

B0 is the frozen historical weighted mean.

No fitting occurs in the issuer.

## 10. Append-only registry

Canonical registry:

`results/fed_cycle_prospective_gcf_v1/PREDICTION_REGISTRY.csv`

Prediction ID:

`GCF012_<episode>_<forecast-month>`

Rules:

- ID must be unique;
- an existing row may never be overwritten;
- no row is deleted;
- realized target/error fields remain blank at issuance;
- target realization is a separate later audit step;
- an attempted duplicate must refuse issuance.

## 11. Provenance captured per issued row

Record:

- prediction ID;
- episode ID;
- forecast month;
- issue timestamp UTC;
- spec/model hashes;
- bridge ID;
- Yahoo raw-response SHA256;
- RTDSM workbook SHA256;
- selected RTDSM vintage;
- exact five M3 feature values;
- B0/B1/B2/M3 predictions;
- target-end month;
- status = ISSUED_UNREALIZED.

## 12. Current expected result

With repository state on 2026-09-24:

- current edge run = 1 hike / 25 bp;
- cycle activation fails;
- registry remains empty;
- issuance count = 0;
- readiness status = WAITING_CYCLE_QUALIFICATION.

## 13. Hard QC

Fail if:

- 012 spec/model hashes differ from frozen values;
- BRIDGE-011 status differs;
- registry schema differs;
- duplicate prediction IDs exist;
- any existing registry row is silently rewritten;
- a prediction is issued before 2 hikes / 50 bp;
- a prediction is issued for a retroactive month;
- issue timestamp is on/after forecast-month start;
- incomplete Gold month is used;
- RT-IPT is unavailable;
- model fitting occurs;
- raw Yahoo/RTDSM source files are committed.

## 14. Evidence boundary

**FORECAST ISSUANCE INFRASTRUCTURE / NO FORECAST PERFORMANCE EVIDENCE UNTIL TARGETS MATURE / NOT CAUSAL / NOT DEPLOYABLE**
