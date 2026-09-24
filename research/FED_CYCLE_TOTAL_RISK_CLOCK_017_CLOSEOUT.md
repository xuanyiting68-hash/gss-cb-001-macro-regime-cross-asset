# FED-CYCLE-TOTAL-RISK-CLOCK-017 — Closeout
Date: 2026-09-24
Status: **QC PASS / SUPPORTED EVENT-LEVEL ANCHOR→TROUGH→RECOVERY CLOCK / NOT CAUSAL**

## 1. Purpose

Measure the full historical risk clock from a policy-cycle anchor to:

1. maximum-drawdown trough;
2. 50% repair of that drawdown;
3. 100% recovery back to the prior peak.

This is deliberately different from reporting post-trough recovery alone.

## 2. Why event-level total time matters

A common shortcut is:

median trough month + median recovery month.

That is invalid because the two medians may come from different episodes.

017 therefore computes total durations at the event level and only then applies broad-episode-weighted survival analysis.

## 3. Supported evidence set

Main supported four-phase assets:

- DXY;
- GOLD;
- NASDAQ;
- SP500;
- WTI.

Housing contributes one supported recovery cell:

- US_HOUSE_PRICE at LAST_HIKE.

No limited TLT/VNQ/BTC or limited housing cells enter the main four-phase table.

## 4. Main result — FIRST_CUT is not a faster total recovery phase

For the five fully supported four-phase assets, comparing FIRST_CUT with PAUSE_START:

- FIRST_CUT total 100% recovery is **slower in 3/5**;
- **equal in 2/5**;
- **faster in 0/5**.

This is stronger than the post-trough-only result because it incorporates the delay before the maximum drawdown is reached.

## 5. Asset-specific total risk clocks

### DXY

Weighted median trough month:
- FIRST_HIKE 8;
- LAST_HIKE 8;
- PAUSE_START 11;
- FIRST_CUT 8.

Anchor-to-full-recovery KM median:
- FIRST_HIKE **17m**;
- LAST_HIKE **15m**;
- PAUSE_START **13m**;
- FIRST_CUT **13m**.

### GOLD

Trough month:
- FIRST_HIKE 11;
- LAST_HIKE 6;
- PAUSE_START 9;
- FIRST_CUT 5.

Anchor-to-full recovery:
- FIRST_HIKE **30m**;
- LAST_HIKE **11m**;
- PAUSE_START **15m**;
- FIRST_CUT **22m**.

Gold FIRST_HIKE is the longest supported Gold clock because it combines a very late trough with slow post-trough recovery.

### NASDAQ

Trough month:
- FIRST_HIKE 7;
- LAST_HIKE 8;
- PAUSE_START 7;
- FIRST_CUT 8.

Anchor-to-full recovery:
- FIRST_HIKE **14m**;
- LAST_HIKE **11m**;
- PAUSE_START **10m**;
- FIRST_CUT **15m**.

### SP500

Trough month:
- FIRST_HIKE 4;
- LAST_HIKE 9;
- PAUSE_START 9;
- FIRST_CUT 8.

Anchor-to-full recovery:
- FIRST_HIKE **12m**;
- LAST_HIKE **12m**;
- PAUSE_START **14m**;
- FIRST_CUT **14m**.

### WTI

Trough month:
- FIRST_HIKE 10;
- LAST_HIKE 7;
- PAUSE_START 9;
- FIRST_CUT 11.

Anchor-to-full recovery:
- FIRST_HIKE **12m**;
- LAST_HIKE **29m**;
- PAUSE_START **17m**;
- FIRST_CUT **20m**.

WTI LAST_HIKE is the longest WTI total clock even though the trough is not especially late; the persistence comes mainly from slow post-trough repair.

## 6. Housing supported cell

US_HOUSE_PRICE at LAST_HIKE:

- 5 positive-drawdown episodes across 5 broad episodes;
- weighted median trough month: **17m**;
- anchor-to-50% recovery: **19m**;
- anchor-to-100% recovery: **20m**;
- 4 observed full recoveries;
- 1 right-censored.

This confirms that national housing risk can be much slower-moving than listed markets.

## 7. Key interpretation

The total risk clock separates two different mechanisms:

### Late-trough risk
The asset may continue deteriorating long after the policy anchor.

Examples:
- Gold FIRST_HIKE trough month 11;
- WTI FIRST_CUT month 11;
- DXY PAUSE month 11;
- national housing LAST_HIKE month 17.

### Slow-repair risk
The trough occurs, but prior-peak recovery takes a long time.

Examples:
- Gold FIRST_HIKE total clock 30m;
- WTI LAST_HIKE 29m.

Therefore a fast post-trough bounce does not imply a short policy-anchor-to-recovery risk window.

## 8. Policy-cycle interpretation

The supported historical evidence does not support the narrative:

`FIRST_CUT = drawdown risk is over and recovery clock accelerates`.

In this sample, FIRST_CUT is never faster than PAUSE_START on total full recovery among the five fully supported four-phase assets.

This is a descriptive phase association, not evidence that rate cuts cause slower recovery.

## 9. Boundary

**SUPPORTED DESCRIPTIVE TOTAL RISK CLOCK / EVENT-LEVEL CENSORING PRESERVED / NO NEW PRICE ESTIMATION / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**
