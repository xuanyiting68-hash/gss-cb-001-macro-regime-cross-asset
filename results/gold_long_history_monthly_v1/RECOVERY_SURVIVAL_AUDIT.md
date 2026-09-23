# Gold monthly recovery survival audit

**DESCRIPTIVE / RIGHT-CENSORING AWARE / NOT CAUSAL / NOT DEPLOYABLE**

Observed-only recovery medians are not used as the overall recovery-time summary.
Kaplan–Meier estimates use the already-frozen recovery thresholds and 60-month search horizon.

## FIRST_HIKE

| event_type   | recovery_level   |   n_at_risk |   observed_recoveries |   right_censored |   km_median_months |   survival_not_recovered_6m |   survival_not_recovered_12m |   survival_not_recovered_24m |   survival_not_recovered_60m |   max_followup_months |
|:-------------|:-----------------|------------:|----------------------:|-----------------:|-------------------:|----------------------------:|-----------------------------:|-----------------------------:|-----------------------------:|----------------------:|
| FIRST_HIKE   | 50%              |          10 |                     8 |                2 |                  8 |                         0.6 |                          0.3 |                          0.2 |                          0.2 |                    60 |
| FIRST_HIKE   | 100%             |          10 |                     6 |                4 |                 19 |                         0.9 |                          0.7 |                          0.5 |                          0.4 |                    60 |

Interpretation:

- 50% recovery: 8/10 observed and 2/10 right-censored; KM median = 8 months.
- 100% recovery: 6/10 observed and 4/10 right-censored; KM median = 19 months.
- These are historical descriptive recovery distributions, not forecasts.
- No p-value/FDR family is executed; OOS is not applicable.