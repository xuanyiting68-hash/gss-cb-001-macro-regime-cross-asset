# FED-CYCLE-SUPPORTED-RECOVERY-MAP-016 — Evidence-Filtered Recovery Synthesis Lock
Date: 2026-09-24
Status: **FROZEN SYNTHESIS / NO NEW OUTCOME ESTIMATION**

## Purpose

Combine PHASE-CLOCK-004 and RECOVERY-EXTENSION-015 into one evidence-filtered recovery map.

No raw price data are re-estimated.

## Supported recovery cells

### PHASE-CLOCK-004
Include only cells whose phase support status is:
`PRIMARY_SUPPORTED`.

This includes the core long-history assets:
- GOLD;
- SP500;
- NASDAQ;
- WTI.

Exclude USD_BROAD from the supported map because it is diagnostic limited support.

### RECOVERY-EXTENSION-015
Include only cells with:
`recovery_support_status = SUPPORTED_RECOVERY_DESCRIPTIVE`.

This includes:
- DXY across all four anchors;
- US_HOUSE_PRICE at LAST_HIKE only.

TLT, VNQ, BTC and other housing recovery cells remain in a separate limited watchlist.

## Main four-phase comparison

Only assets with supported recovery evidence at all four anchors may enter the four-phase contrast table.

Expected:
- GOLD;
- SP500;
- NASDAQ;
- WTI;
- DXY.

For each:
- 50% KM recovery median;
- 100% KM recovery median;
- fastest full-recovery phase;
- slowest full-recovery phase;
- FIRST_HIKE minus PAUSE_START full-recovery months;
- FIRST_CUT minus PAUSE_START full-recovery months.

## Frozen question

Does FIRST_CUT universally accelerate full recovery relative to PAUSE_START?

A universal statement is supported only if FIRST_CUT full-recovery median is strictly lower than PAUSE_START for every fully supported asset.

No p-value is used.

## Evidence boundary

**SUPPORTED DESCRIPTIVE SYNTHESIS / NO NEW PRICE ESTIMATION / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**
