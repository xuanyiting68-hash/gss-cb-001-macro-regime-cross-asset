# FED-CYCLE-GOLD-LONGHIST-MONTHLY-001 — Frozen Specification
Date: 2026-09-24
Status: **FROZEN BEFORE MONTHLY GOLD OUTCOME EXECUTION**

## Purpose

Extend Gold coverage across all qualifying Fed tightening legs without pretending that a monthly historical series is daily data.

This module is a **native-frequency monthly robustness layer** complementing, not replacing, the daily `GC=F` futures-proxy layer in FED-CYCLE-PATH-001 v1.1.

## Source

Pinned source package:

- repository: `datasets/gold-prices`
- source commit: `95bfea9197222dcda13d8c4d9928fb631fe745aa`
- resource: `data/monthly.csv`
- package license: `ODC-PDDL-1.0`
- modern source stated by the package: World Bank Commodity Markets ("Pink Sheet")

Only observations from **1960-01 onward** are eligible.

The package notes that 1833-1959 monthly rows repeat annual averages; those rows are excluded entirely.

Raw source bytes are used transiently and hashed. Derived outputs and provenance are committed.

## Policy anchors

Use the QC-passed timing-corrected registry from:

`results/fed_cycle_path_v1_1/FED_TIGHTENING_CYCLES.csv`

No Fed event is redefined in this module.

Primary anchor: `FIRST_HIKE`.

Secondary descriptive anchors:

- `LAST_HIKE`
- `PAUSE_START`
- `FIRST_CUT`

Pre-1994 anchors retain the v1.1 interpretation boundary: historical target reconstructions rather than exact modern announcement timestamps.

## Monthly timing convention

A monthly average that contains the event date mixes pre-event and post-event prices.

Therefore the **event month is omitted from clean outcome measurement**.

For an event in calendar month `M0`:

- baseline = monthly average in `M-1`;
- `+1M` = monthly average in `M+1`, the first complete calendar month after the event month;
- `+3M`, `+6M`, `+12M`, `+24M` = the corresponding complete calendar months after `M0`.

The event-month monthly average is stored only for audit if needed and is never used as a clean endpoint.

This convention sacrifices immediate event response in exchange for avoiding event-month mixture.

## Path-risk window

Clean path for path-risk metrics:

`baseline (M-1) -> M+1 -> M+2 -> ... -> M+24`

The mixed event month is omitted.

Metrics:

- endpoint returns at +1M/+3M/+6M/+12M/+24M;
- MAE/MFE relative to the M-1 baseline;
- maximum peak-to-trough drawdown across the clean baseline/post-month path;
- time to event-relative minimum and maximum in complete post-event months;
- time from MDD peak to trough;
- 12M and 24M annualized realized volatility from consecutive clean post-event monthly observations;
- downside semivolatility on the same basis.

## Recovery

Recovery is measured from the MDD trough:

- 50% recovery = first later monthly average regaining half the distance from trough to the pre-drawdown peak;
- 100% recovery = first later monthly average regaining the pre-drawdown peak;
- search horizon = 60 complete post-event months;
- unrecovered paths are right-censored.

## Cross-frequency audit

For 2004, 2015 and 2022 FIRST_HIKE legs, compare:

- daily `GC=F` 252-observation endpoint;
- World Bank/DataHub monthly +12M endpoint.

This is a **measurement/proxy robustness diagnostic** only. Different instruments and frequencies are not expected to match exactly and must not be pooled.

## Statistical status

This is a descriptive support-expansion module.

No confirmatory p-value family is executed.

- FDR: not applicable in this module;
- OOS: not applicable;
- causality: none;
- deployment: none.

## Hard QC

Fail if:

- pinned source cannot be fetched;
- modern monthly source does not contain continuous 1960+ observations needed around the Fed sample;
- FIRST_HIKE monthly support is not all 10 qualifying tightening legs;
- event-month data enter any clean endpoint or clean path-risk metric;
- any MDD is negative;
- 100% recovery precedes 50% recovery when both are observed;
- raw source data are written into the public results directory.

## Interpretation boundary

Allowed:

- **DATA FACT**
- **DESCRIPTIVE RESULT**
- **NOT YET VERIFIED**
- **INVESTMENT IMPLICATION** only as a risk-measurement implication.

Not allowed:

- “Fed hikes cause Gold to …”
- universal Gold timing rules;
- combining monthly World Bank Gold with daily COMEX futures as one homogeneous sample;
- treating monthly averages as event-day prices.
