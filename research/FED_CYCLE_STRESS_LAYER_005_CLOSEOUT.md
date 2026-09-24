# FED-CYCLE-STRESS-LAYER-005 — Closeout
Date: 2026-09-24
Status: **QC-PASSED DESCRIPTIVE STRESS MAP / MECHANISM CONTEXT ONLY / NOT DEPLOYABLE**

## 1. Purpose

STRESS-LAYER-005 adds three public stress observables to the four-anchor Fed-cycle phase map:

- VIX;
- Moody's Baa minus 10Y Treasury spread;
- copper.

The module asks how observable stress evolves after FIRST_HIKE, LAST_HIKE, PAUSE_START and FIRST_CUT.

It does not search for a trading threshold or causal driver.

## 2. QC and support

QC passed:

- 924 stress-path rows;
- 77 stress × phase × cycle rows;
- **12/12 primary observable × phase cells supported**;
- 0 event-month violations;
- 0 VIX monthly-max consistency violations;
- 0 negative copper-MDD violations;
- 0 broad-episode-weight violations;
- 0 canonical-anchor-date violations.

Support:

- VIX: 5 mechanical cycles / 5 broad episodes across each phase;
- copper: 5 / 5;
- Baa–10Y spread: 10 / 7 for FIRST_HIKE/LAST_HIKE/FIRST_CUT and 7 / 7 for PAUSE_START.

## 3. VIX phase map

Metric:

weighted median **maximum increase in monthly-average VIX** within the next 12 complete months.

| Anchor | Median max VIX increase | Median stress-peak month | +12M VIX change |
|---|---:|---:|---:|
| FIRST_HIKE | +4.26 points | 2 | -4.10 |
| LAST_HIKE | +1.33 | 3 | +0.37 |
| PAUSE_START | +3.46 | 11 | +1.81 |
| FIRST_CUT | **+8.53** | **8** | **+5.21** |

75th percentile maximum increase after FIRST_CUT is about **+12.65 VIX points**.

### DESCRIPTIVE RESULT

Among the four phase anchors, FIRST_CUT has the largest median subsequent VIX stress increase in the five-cycle modern sample.

This does not mean the cut caused volatility.

A first cut often occurs because the macro/financial environment is already changing.

## 4. Credit-spread phase map

Metric:

weighted median **maximum Baa–10Y spread widening** inside the next 12 complete months.

| Anchor | Median max widening | Median peak month | +12M spread change |
|---|---:|---:|---:|
| FIRST_HIKE | +16 bp | 2 | -21 bp |
| LAST_HIKE | +31 bp | 5 | -4 bp |
| PAUSE_START | +31 bp | 9 | +23 bp |
| FIRST_CUT | **+38 bp** | **7** | +5 bp |

FIRST_CUT 75th-percentile maximum widening is about **108 bp**.

### DESCRIPTIVE RESULT

Credit stress is more pronounced after FIRST_CUT than after FIRST_HIKE on the median maximum-widening measure.

Again, this is a phase association, not a causal effect of cutting rates.

## 5. Copper phase map

| Anchor | +3M | +6M | +12M | Median 12M MDD | MDD trough month |
|---|---:|---:|---:|---:|---:|
| FIRST_HIKE | +6.40% | +15.08% | +17.93% | **6.84%** | 10 |
| LAST_HIKE | -5.42% | -0.54% | -1.92% | **15.08%** | 11 |
| PAUSE_START | +4.08% | +1.39% | -2.93% | **17.29%** | 11 |
| FIRST_CUT | -5.94% | +2.53% | -7.00% | **19.96%** | 9 |

### DESCRIPTIVE RESULT

Copper shows a monotonic-looking increase in median 12M MDD across these phase labels in this five-cycle sample:

FIRST_HIKE < LAST_HIKE < PAUSE_START < FIRST_CUT.

This pattern is visually interesting but is **not** assigned a trend p-value or promoted into a universal cycle law.

## 6. Joint interpretation with PHASE-CLOCK-004

PHASE-CLOCK-004 found:

- S&P FIRST_CUT 12M MDD median ≈ 13.99%;
- Nasdaq ≈ 17.48%;
- WTI ≈ 22.23%;
- late-window trough mass is especially high after FIRST_CUT.

STRESS-LAYER-005 adds descriptive context:

- VIX maximum increase is largest after FIRST_CUT;
- credit maximum widening is largest after FIRST_CUT;
- copper 12M MDD is largest after FIRST_CUT.

### MECHANISM CANDIDATE

The combined evidence is consistent with a view that FIRST_CUT often occurs around a broader deterioration/stress transition rather than representing an immediate all-clear signal.

### CAUSAL EVIDENCE

**None.**

The Fed can cut in response to worsening conditions, so reverse causality/endogeneity is central.

## 7. Evidence boundary

### DATA FACT
- all 12 frozen observable × phase cells pass support/QC;
- no stress threshold was optimized;
- raw source histories are not committed.

### DESCRIPTIVE RESULT
- FIRST_CUT has the highest median maximum VIX increase, Baa spread widening and copper MDD in this frozen comparison.

### MECHANISM CANDIDATE
- first-cut phases may coincide with broader financial/cyclical stress.

### CAUSAL EVIDENCE
None.

### FDR
Not applicable. No p-value family is run.

### OOS
Not applicable. Not a forecasting model.

### DEPLOYMENT
Not deployable.

## 8. Product implication

For PandaAI, FIRST_CUT should not be rendered as a green "risk resolved" state.

A better representation is:

'policy phase + observed stress indicators + asset-specific historical path-risk distribution + uncertainty'.

No threshold-based signal is authorized by this module.
