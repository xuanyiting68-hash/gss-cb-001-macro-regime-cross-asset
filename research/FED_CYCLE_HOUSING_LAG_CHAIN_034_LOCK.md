# FED-CYCLE-HOUSING-LAG-CHAIN-034 — LOCK

Date locked: 2026-09-26

## Purpose

Study the descriptive slow-moving housing chain around the four canonical Fed-cycle phases:

`policy phase -> market/mortgage financing conditions -> housing activity -> national house-price path`

034 is a lag-structure and mechanism-context module.

It does not estimate a causal monetary-policy transmission coefficient and does not compare housing risk directly with traded-asset MDD.

## Canonical phase anchors

Use the existing public phase/cycle anchors already frozen in the project:

- FIRST_HIKE
- LAST_HIKE
- PAUSE_START
- FIRST_CUT

Cycle IDs / broad-episode IDs / episode weights must be inherited from the existing housing phase metrics / frozen cycle map.

No new cycle definition is allowed.

## Price layer

Do **not** re-estimate or replace the canonical house-price outcome layer.

Use:
- results/fed_cycle_cross_asset_expansion_v1/HOUSING_PHASE_METRICS.csv
- results/fed_cycle_cross_asset_expansion_v1/HOUSING_PHASE_SUMMARY.csv
- results/fed_cycle_recovery_extension_v1/HOUSING_RECOVERY_METRICS.csv
- results/fed_cycle_recovery_extension_v1/HOUSING_RECOVERY_SUMMARY.csv

Canonical house-price series:
- CSUSHPINSA
- S&P Cotality Case-Shiller U.S. National Home Price Index
- monthly / not seasonally adjusted
- available from 1987

Housing price risk remains:
`DECLINE_24M`

It must never be relabeled as 12M MDD.

## New financing/activity sources

### MORTGAGE30US
- 30-Year Fixed Rate Mortgage Average in the United States
- Freddie Mac PMMS via FRED
- weekly, ending Thursday
- 1971 onward
- copyrighted source history: raw bytes are not committed
- 2022-11-17 methodology change must be recorded

### DGS10
- 10-Year Treasury constant-maturity yield
- Board of Governors via FRED
- daily
- used only as financing-market context
- yield changes are not bond returns

### HOUST
- total privately-owned housing units started
- Census/HUD
- monthly SAAR
- 1959 onward

### PERMIT
- total privately-owned housing units authorized
- Census/HUD
- monthly SAAR
- 1960 onward

### HSN1F
- new one-family houses sold
- Census/HUD
- monthly SAAR
- 1963 onward

## Source-snapshot rule

034 may fetch current public source histories during its frozen run.

For each downloaded source:
- record retrieval timestamp;
- raw SHA256;
- first/last observation;
- row count;
- source URL;
- source/licensing note.

Do not commit raw MORTGAGE30US or Case-Shiller history.

Derived metrics and source hashes are public-safe.

Because FRED/Census/Freddie series can be revised, future reruns must be treated as new source snapshots if hashes change.

## Monthly transformations

### Mortgage / DGS10
Convert to calendar-month mean.

### Mortgage spread
`MORTGAGE_SPREAD_PP = monthly_mean(MORTGAGE30US) - monthly_mean(DGS10)`

This is a descriptive spread in percentage points.

### Housing activity
For HOUST / PERMIT / HSN1F:

1. retain official monthly SAAR level;
2. compute a trailing 3-month mean;
3. do not seasonally adjust again.

## Anchor baseline

For every event:

`baseline_month = anchor calendar month - 1 month`

This avoids using a partial anchor month that may mix pre/post-event observations.

### Financing baseline
Use the monthly mean in baseline_month.

### Activity baseline
Use trailing-3M mean ending in baseline_month.

## Horizons

Frozen horizons:
- +3 months
- +6 months
- +12 months
- +24 months

No interpolation of missing horizon endpoints.

If a horizon is not yet observed, retain null.

## Derived financing metrics

For MORTGAGE30US, DGS10, MORTGAGE_SPREAD_PP:
- baseline level;
- level at +3/+6/+12/+24m;
- change from baseline in percentage points;
- max increase over months 0..24;
- min change over months 0..24;
- month of max financing pressure;
- month of minimum rate/spread.

No claim that mortgage spread is a pure credit-risk premium.

## Derived activity metrics

For HOUST, PERMIT, HSN1F:
- 3M-average level at baseline;
- percent change at +3/+6/+12/+24m;
- minimum percent change in months 0..24;
- trough month in 0..24;
- maximum percent change in 0..24;
- peak month in 0..24.

## Lag-chain pairing

For episodes with canonical house-price path data, build:

- mortgage max-pressure month;
- HOUST trough month;
- PERMIT trough month;
- HSN1F trough month;
- house-price trough month if canonical DECLINE_24M > 0;
- price decline magnitude;
- recovery timing if available.

Descriptive lag variables may include:
- activity_trough_month - mortgage_pressure_month
- price_trough_month - activity_trough_month

These are timing differences only.

They must not be called causal transmission lags.

## Frozen summary questions

1. How quickly do mortgage rates move after each Fed phase anchor?
2. Does mortgage-rate pressure peak before housing activity troughs?
3. Which activity series reacts earlier: permits, starts, or new-home sales?
4. Does activity generally weaken before national house prices decline?
5. How long after FIRST_HIKE do housing activity and prices reach their worst point?
6. What changes by LAST_HIKE?
7. What changes by PAUSE_START?
8. What changes by FIRST_CUT?
9. Why can house prices remain positive while housing activity contracts?
10. Why can mortgage rates fall before house prices recover?
11. How exceptional is 2006-09 relative to other episodes?
12. What does the 2022-24 episode show about financing pressure versus price resilience?
13. What can be said about housing recovery clocks?
14. What cannot be inferred causally from these medians?
15. What should PandaAI show for housing without turning the chain into a house-price forecast?

## Frozen outputs

- HOUSING_FINANCING_PHASE_METRICS.csv
- HOUSING_ACTIVITY_PHASE_METRICS.csv
- HOUSING_FINANCING_PHASE_SUMMARY.csv
- HOUSING_ACTIVITY_PHASE_SUMMARY.csv
- HOUSING_LAG_CHAIN_EPISODE_PANEL.csv
- HOUSING_LAG_CHAIN_PHASE_SUMMARY.csv
- HOUSING_CASE_AUDIT.csv
- HOUSING_INVESTOR_QUESTION_REGISTRY.csv
- HOUSING_LAG_CHAIN_SYNTHESIS_ZH.md
- PANDAAI_HOUSING_LAG_SCHEMA.json
- SOURCE_REGISTRY.csv
- FED_CYCLE_HOUSING_LAG_CHAIN_034_REPORT.md
- QC.json

## QC gates

PASS requires:

1. cycle/phase anchors exactly inherit the canonical project map;
2. no current 2026 tightening candidate enters historical outcome summaries;
3. raw source SHA256 recorded for all new downloaded series;
4. MORTGAGE30US methodology-change note retained;
5. activity uses trailing 3M averages exactly;
6. anchor baseline is M-1 exactly;
7. no missing horizon value is interpolated;
8. house-price outcomes exactly match canonical 014/015 inputs;
9. housing path-risk label remains DECLINE_24M;
10. DGS10/mortgage changes are labeled rate changes, not bond returns;
11. lag differences are descriptive timing, not causal transmission estimates;
12. B05 housing-bust episode remains visible and is not averaged away;
13. 2022/23 housing episode remains separately auditable;
14. no best housing phase;
15. no expected house-price forecast;
16. no home-buying recommendation;
17. no new p-values/inference;
18. private-paper inputs = false;
19. causal status = NONE;
20. OOS status = NOT_A_FORECASTING_MODEL;
21. deployment status = NOT_DEPLOYABLE.

## Interpretation boundary

034 studies historical sequencing of financing, activity and prices.

It does not estimate how much a specific Fed action causes house prices to change, and it does not tell a household when to buy property.
