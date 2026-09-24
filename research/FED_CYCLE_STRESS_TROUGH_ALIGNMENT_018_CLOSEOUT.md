# FED-CYCLE-STRESS-TROUGH-ALIGNMENT-018 — Closeout
Date: 2026-09-24
Status: **QC PASS / POST-ANCHOR STRESS–TROUGH TIMING MAP / NOT A REAL-TIME SIGNAL**

## 1. Purpose

Explain the late-trough pattern identified after FIRST_CUT by aligning, episode by episode:

- asset maximum-drawdown trough month;
- maximum VIX stress month;
- maximum Baa–10Y widening month;
- maximum copper drawdown month.

All inputs are frozen outputs from PHASE-CLOCK-004 and STRESS-LAYER-005.

## 2. QC and support

- 78 paired event rows;
- 12 asset × stress cells;
- 12/12 pass timing-descriptive support;
- zero duplicate-cycle violations;
- zero ID mismatches;
- zero timing-range violations;
- no p-values;
- no current 2026 cycle.

QC: **PASS**.

## 3. Equities — VIX alignment is exceptionally tight

### NASDAQ × VIX
Across 5 cycles / 5 broad episodes:
- median Nasdaq trough month: 8;
- median VIX stress-peak month: 8;
- median lead: 0 months;
- same-month share: **100%**;
- within ±2 months: **100%**;
- both in months 7-12: **100%**.

### SP500 × VIX
Identical timing summary:
- trough month 8;
- VIX peak month 8;
- same-month share **100%**;
- near ±2m **100%**;
- both late **100%**.

Interpretation:

In the five modern FIRST_CUT episodes where VIX is available, the maximum equity drawdown trough and the maximum VIX stress increase occur in the same event month.

This is ex-post timing alignment, not a live bottoming indicator.

## 4. Equities — credit and copper also cluster near troughs

For Nasdaq and S&P:

### Baa–10Y spread
- median stress peak month 7 vs asset trough month 8;
- weighted median absolute gap 1 month;
- near ±2m share ≈ **71%**.

### Copper
- median stress peak month 9 vs asset trough 8;
- median absolute gap 1 month;
- near ±2m share **80%**.

Thus late equity troughs after FIRST_CUT are typically part of a broader stress transition rather than isolated equity-only drawdowns.

## 5. WTI

WTI median FIRST_CUT trough month: 11.

### VIX
- median peak month 8;
- weighted median lead +1 month;
- before-or-same share 80%;
- within ±2m share 80%;
- both late share 100%.

### Copper
- median peak month 9;
- median lead 0;
- within ±2m share 80%.

### Baa spread
- median peak month 7;
- median lead +1;
- before-or-same share 100%.

WTI stress/trough alignment is therefore also tight, but tends to place the asset trough slightly later than the broad stress peak.

## 6. Gold is structurally different

Gold does not share the equity/WTI alignment.

### Gold × VIX
- paired-sample Gold trough month 4;
- VIX peak month 8;
- median lead -4 months;
- near ±2m share only 40%.

### Gold × Baa spread
- trough month 5;
- spread stress peak month 7;
- median lead -3 months;
- near share ~14%.

Gold often reaches its MDD trough before the later FIRST_CUT financial-stress maximum.

This is consistent with Gold having a different macro/real-rate/USD channel than equities and oil.

## 7. Cross-observable synthesis

Across the four supported asset pairs:

### VIX
- median pair-level lead = 0;
- median near-2m share = **90%**;
- median before-or-same share = 90%;
- median both-late share = 100%.

### Copper
- median lead = 0;
- near share = **80%**;
- both-late share = 80%.

### Baa spread
- median lead = 0;
- near share ≈ **69%**.

The aggregate alignment is driven by equities and WTI; Gold is the important exception.

## 8. Interpretation

The FIRST_CUT late-trough result in 017 is consistent with a broader post-cut stress transition:
- VIX stress;
- credit-spread widening;
- cyclical commodity weakness;
- equity/oil drawdown troughs.

But stress peaks and asset troughs are both future-window statistics.

Therefore 018 explains historical timing; it does **not** create a real-time leading signal.

## 9. Boundary

**POST-ANCHOR MECHANISM TIMING / SUPPORTED DESCRIPTIVE / NOT A REAL-TIME SIGNAL / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**
