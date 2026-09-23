# FED-CYCLE-GOLD-LONGHIST-MONTHLY-001 — Recovery Survival Amendment
Date: 2026-09-24
Status: **POST-RUN STATISTICAL-HANDLING CORRECTION / NO OUTCOME OR THRESHOLD CHANGE**

## Trigger

The frozen monthly run correctly stored right-censoring fields, but its descriptive report also printed simple medians among **observed recoveries only**.

That observed-only median is not an appropriate population recovery-time summary when some paths are right-censored.

For FIRST_HIKE full recovery, only 6 of 10 paths are observed within the search window. Treating the median of those six as the overall recovery median would bias the summary toward faster recoveries.

## Correction

Add Kaplan–Meier survival estimates using the already-frozen recovery definitions.

For each event type and each recovery threshold:

- duration = observed recovery time when recovery occurs;
- otherwise duration = frozen `recovery_censor_months`;
- event indicator = 1 for observed recovery, 0 for right-censored;
- Kaplan–Meier survival = probability that recovery has **not yet occurred**.

Report:

- n at risk;
- number observed;
- number censored;
- KM median recovery time, defined as the first month at which survival <= 0.5, if reached;
- survival/not-yet-recovered share at 6, 12, 24 and 60 months where estimable.

## No specification changes

This amendment does **not** change:

- Fed event dates;
- Gold source;
- event-month omission;
- endpoint horizons;
- MDD/MAE/MFE;
- recovery thresholds;
- 60-month recovery search horizon;
- any trading or causal claim.

It corrects only the statistical summary of already-defined censored durations.

## Evidence status

Still:

**DESCRIPTIVE / NOT CAUSAL / NO FDR CLAIM / OOS NOT APPLICABLE / NOT DEPLOYABLE**
