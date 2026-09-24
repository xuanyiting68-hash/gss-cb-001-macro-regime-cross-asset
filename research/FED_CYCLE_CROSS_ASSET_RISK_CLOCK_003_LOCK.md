# FED-CYCLE-CROSS-ASSET-RISK-CLOCK-003 — Frozen Specification
Date: 2026-09-24
Status: **FROZEN BEFORE EVENT-TIME RISK-CLOCK EXECUTION**

## 1. Purpose

Build a month-by-month risk clock after `FIRST_HIKE` for major price assets.

Primary question:

**when does path risk actually concentrate after the first hike?**

This module is descriptive. It does not identify a monetary-policy causal effect.

## 2. Event registry

Use the QC-passed timing-corrected cycle registry:

`results/fed_cycle_path_v1_1/FED_TIGHTENING_CYCLES.csv`

Primary event: `FIRST_HIKE`.

The 10 mechanical tightening legs remain unchanged.

Broad episode clusters are inherited mechanically from STATE-PANEL-002:

- 1983-84 together;
- 1987 Jan / 1987 Aug / 1988 together;
- 1994;
- 1999;
- 2004;
- 2015;
- 2022.

## 3. Asset universe

Primary price assets:

- Gold monthly, pinned World Bank/DataHub series;
- S&P 500 cash index, Yahoo `^GSPC` daily history aggregated to monthly average;
- Nasdaq Composite, FRED `NASDAQCOM` daily history aggregated to monthly average;
- WTI spot, EIA/FRED `DCOILWTICO` daily history aggregated to monthly average.

Diagnostic only:

- Broad USD `DTWEXBGS`, because long-history FIRST_HIKE support is limited.

Raw Yahoo/FRED histories are used transiently and not committed.

## 4. Monthly timing convention

For an event in month M0:

- baseline = monthly average in M-1;
- event month M0 is omitted because it mixes pre/post-event observations;
- event-time month 1 = M+1;
- event-time month 24 = M+24.

Primary risk clock window: **24 complete post-event months**.

No alternative window is selected after outcomes.

## 5. Cycle-level path metrics

For each asset × FIRST_HIKE leg and each event month k=1..24:

- cumulative return from M-1 baseline;
- running maximum drawdown through k;
- event-relative running minimum return through k;
- `NEW_EVENT_LOW`: month k is a new minimum level relative to baseline and all previous complete post-event months;
- `NEW_RUNNING_MDD`: running MDD at k strictly exceeds all earlier running-MDD values.

Over the full 24M window also record:

- eventual event-relative trough month;
- eventual MDD trough month;
- eventual 24M MDD;
- maximum favorable excursion;
- 12M and 24M endpoint returns.

## 6. Trough timing and hazard

For each asset:

### 6.1 Event-relative trough CDF

At event month k:

weighted share of episodes whose 24M event-relative trough occurs at or before k.

### 6.2 MDD-trough CDF

At event month k:

weighted share of episodes whose 24M maximum-drawdown trough occurs at or before k.

### 6.3 Discrete MDD-trough hazard

At month k:

`weight(trough_month == k) / weight(trough_month >= k)`

among episodes whose MDD trough has not occurred before k.

This is a descriptive empirical hazard, not a structural hazard model.

## 7. Broad-episode weighting

Nearby mechanical legs are not treated as fully independent.

Each mechanical leg receives:

`episode_weight = 1 / number_of_legs_in_its_broad_episode`.

Thus each broad episode contributes total weight 1 when support exists.

Primary aggregate risk-clock summaries use these weights.

Unweighted mechanical-leg summaries may be retained as sensitivity.

## 8. Timing bins

Frozen timing bins:

- EARLY = months 1-6;
- MID = months 7-12;
- LATE = months 13-24.

For each asset report weighted share of eventual MDD troughs in each bin.

No alternative bin cut is selected after outcomes.

## 9. Recovery

Recovery is measured from the 24M-window MDD trough.

Search horizon: 60 complete months after the trough.

- 50% recovery = regain half the price distance from MDD trough to its pre-drawdown peak;
- 100% recovery = regain the pre-drawdown peak;
- unrecovered observations are right-censored.

Report Kaplan-Meier recovery curves by asset.

## 10. Gold priority

Gold receives:

- full 10-leg monthly long-history clock;
- highlighted 2015 and 2022 paths under the same frozen timing convention;
- no separate hand-tuned windows.

Daily `GC=F` results remain a separate proxy layer and are not pooled into this monthly clock.

## 11. Support rules

Primary risk-clock reporting requires:

- at least 5 mechanical legs;
- at least 4 broad episodes.

Assets below support remain diagnostic only.

## 12. Statistical status

This is a **descriptive timing-distribution module**.

No p-value family is executed.

- FDR: not applicable;
- OOS: not a forecasting model;
- causality: none;
- deployment: none.

## 13. Hard QC

Fail if:

- event month enters the clean path;
- any path begins without M-1 baseline;
- any reported primary asset has fewer than 5 legs or 4 broad episodes;
- broad-episode weights do not sum to 1 within each episode when its legs are available;
- MDD is negative;
- MDD-trough month is outside 1..24;
- 100% recovery precedes 50% recovery when both are observed;
- raw redistribution-uncertain market history is committed.

## 14. Evidence language

Allowed:

- **DATA FACT**
- **DESCRIPTIVE RESULT**
- **INVESTMENT IMPLICATION** as risk measurement/timing only
- **NOT YET VERIFIED**

Not allowed:

- “Fed hikes cause the market to bottom in month X”;
- deterministic timing rules;
- trading/deployment claims.

The purpose is a historical **risk distribution + timing map**, not a signal.
