# FED-CYCLE-HOUSING-LAG-CHAIN-034 — POST-RUN DIAGNOSTIC AMENDMENT

Date: 2026-09-26

## Why this amendment exists

The first QC-passed 034 run exposed a phase-clock artifact that must be handled explicitly before interpretation.

The preregistered financing pressure month is the maximum mortgage-rate change in the **forward 0..24 month window relative to M-1**.

That metric is valid for the frozen design, but it does not necessarily locate the **cycle-level mortgage-rate peak**.

This matters particularly at LAST_HIKE / PAUSE_START / FIRST_CUT, where mortgage rates may already have peaked before the anchor.

Therefore:

- the original preregistered forward-window metrics remain canonical and are not replaced;
- a clearly labeled post-run timing diagnostic is added;
- no p-values, model fitting, threshold optimization or forecasting is introduced.

## Added diagnostic A — paired ordering shares

Do not infer ordering by subtracting phase-level medians.

Instead compute episode-level paired indicators and then episode-weighted shares:

1. forward mortgage pressure before-or-same as activity trough:
   `activity_median_trough_month_24m >= mortgage_max_pressure_month_24m`

2. activity trough before-or-same as house-price trough, restricted to episodes with `decline_24m > 0`:
   `trough_month_24m >= activity_median_trough_month_24m`

3. forward mortgage pressure before-or-same as house-price trough, restricted to positive price-decline episodes.

These are descriptive ordering shares only.

## Added diagnostic B — cycle-window absolute mortgage peak

For MORTGAGE30US only, locate the maximum **absolute monthly mortgage-rate level** in:

`anchor month - 12 months ... anchor month + 24 months`

Store:
- absolute peak level;
- peak month offset relative to phase anchor;
- activity trough minus absolute mortgage peak month;
- house-price trough minus absolute mortgage peak month where decline_24m > 0.

This diagnostic is intended to reveal when the phase anchor occurs **after** the financing peak.

It must be labeled:
`POST_RUN_DIAGNOSTIC__ANCHOR_RESET_AUDIT`

## Interpretation rule

If phase-level standalone medians and paired episode ordering disagree, paired ordering takes precedence for sequencing interpretation.

Neither form is causal.

## Added outputs

- `HOUSING_ORDERING_DIAGNOSTICS.csv`

Existing outputs remain.

## Added QC

PASS requires:
- original preregistered files/metrics remain present;
- paired shares are computed from episode-level rows, not differences of phase medians;
- absolute mortgage peak uses exactly [-12,+24] months;
- diagnostic is labeled post-run;
- no primary result is overwritten;
- no causal language is introduced.
