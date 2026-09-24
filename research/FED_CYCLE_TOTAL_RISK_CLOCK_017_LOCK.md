# FED-CYCLE-TOTAL-RISK-CLOCK-017 — Anchor-to-Trough-to-Recovery Lock
Date: 2026-09-24
Status: **FROZEN BEFORE EXECUTION / SUPPORT-FILTERED DESCRIPTIVE SYNTHESIS**

## 1. Purpose

Measure the full historical risk clock from a policy-cycle anchor to:

1. maximum-drawdown trough;
2. 50% recovery of that drawdown;
3. 100% recovery back to the prior peak.

This extends the post-trough recovery work in PHASE-CLOCK-004 and RECOVERY-EXTENSION-015.

## 2. Why event-level recomputation is required

Do not add:
- median trough month + median recovery month.

Those medians may come from different episodes.

Instead compute, for each episode:

`anchor_to_50 = mdd_trough_month + recovery50_months`

`anchor_to_100 = mdd_trough_month + recovery100_months`

and then perform weighted survival analysis on those event-level total durations.

## 3. Supported evidence only

Use only asset × anchor cells listed as:

`SUPPORTED_RECOVERY_DESCRIPTIVE`

in FED-CYCLE-SUPPORTED-RECOVERY-MAP-016.

Expected fully supported four-phase liquid assets:
- GOLD;
- NASDAQ;
- SP500;
- WTI;
- DXY.

Housing:
- US_HOUSE_PRICE only where 016 marks recovery supported.

Do not place TLT/VNQ/BTC or limited housing cells in the main table.

## 4. Drawdown clock

For 004 core liquid assets:
- use mdd_trough_month from PHASE_CYCLE_ASSET_METRICS.

For DXY:
- use mdd_trough_month from MARKET_RECOVERY_METRICS.

For housing:
- use trough_month_24m from HOUSING_RECOVERY_METRICS.

Only positive-drawdown episodes enter recovery survival.

## 5. Total recovery duration

For recovery level L in {50,100}:

If recovery is observed:

`total_duration_L = trough_month + recoveryL_months`

If right-censored:

`total_censor_duration = trough_month + recovery_censor_months`

Use the same broad-episode weights already frozen in the source modules.

## 6. Outputs

For each supported asset × anchor:
- positive-drawdown episodes;
- positive-drawdown broad episodes;
- weighted median trough month;
- weighted share of troughs in months 7+;
- weighted KM median anchor-to-50% recovery months;
- weighted KM median anchor-to-100% recovery months;
- observed / censored recovery counts.

For assets supported across all four anchors, provide one four-phase total-clock comparison.

## 7. Frozen questions

Q1. Does FIRST_CUT shorten the **total** time from policy anchor to prior-peak recovery versus PAUSE_START?

Q2. Which assets historically have delayed troughs that make a seemingly fast post-trough recovery misleading?

Q3. Are long recovery clocks driven more by late troughs, slow post-trough repair, or both?

No causal claim is allowed.

## 8. QC

Fail if:
- any limited recovery cell enters the main supported table;
- any total recovery duration is less than its trough month;
- observed 100% total duration is less than observed 50% total duration;
- broad-episode weights differ from source metrics;
- any current 2026 live-cycle row appears;
- source event-level metrics are changed.

## 9. Evidence boundary

**SUPPORTED DESCRIPTIVE TOTAL RISK CLOCK / NO NEW PRICE ESTIMATION / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**
