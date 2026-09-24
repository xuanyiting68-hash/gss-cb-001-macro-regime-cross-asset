# FED-CYCLE-PHASE-CLOCK-004 — Multi-Anchor Cross-Asset Phase Clock
Date: 2026-09-24
Status: **FROZEN BEFORE PHASE-ANCHOR OUTCOME EXECUTION**

## 1. Purpose

Extend the FIRST_HIKE risk clock across the main realized policy-cycle anchors:

- FIRST_HIKE
- LAST_HIKE
- PAUSE_START
- FIRST_CUT

Question:

**Does historical path risk concentrate differently depending on where the economy is in the realized policy cycle?**

This is descriptive phase timing, not monetary-policy causal identification.

## 2. Canonical anchors

Use only the timing-corrected cycle registry:

`results/fed_cycle_path_v1_1/FED_TIGHTENING_CYCLES.csv`

No anchor is redefined here.

Interpretation boundary:

- 1994+ scheduled policy anchors use timing-corrected FOMC decision dates where resolved;
- pre-1994 target dates remain historical target reconstructions;
- unresolved emergency-cut candidates are excluded.

## 3. Assets

Primary price assets use the same sources as RISK-CLOCK-003:

- Gold: pinned World Bank/DataHub monthly series;
- S&P 500: Yahoo `^GSPC` daily history aggregated to monthly average;
- Nasdaq Composite: FRED `NASDAQCOM` aggregated to monthly average;
- WTI: EIA/FRED `DCOILWTICO` aggregated to monthly average.

Broad USD remains diagnostic only because long-history support is limited.

No raw redistribution-uncertain market history is committed.

## 4. Common timing convention

For every anchor occurring in calendar month M0:

- baseline = monthly average in M-1;
- event month M0 is omitted;
- clean event-time month 1 = M+1;
- clean event-time month 12 = M+12.

The primary phase clock window is **12 complete post-anchor months**.

The same convention is used for every phase and asset.

No phase receives a custom window after outcomes are inspected.

## 5. Cycle-level metrics

For each asset × cycle × anchor:

- +3M endpoint return;
- +6M endpoint return;
- +12M endpoint return;
- 12M maximum drawdown;
- event-relative MAE;
- MFE;
- eventual event-relative trough month within 12M;
- eventual 12M MDD trough month;
- running MDD by event month 1..12;
- new-event-low incidence;
- new-running-MDD incidence.

## 6. Timing bins

Frozen 12M timing bins:

- EARLY = months 1-3;
- MID = months 4-6;
- LATE = months 7-12.

For each asset × phase, report broad-episode-weighted share of 12M MDD troughs in each bin.

## 7. Broad-episode weighting

Use the same broad-episode ontology as RISK-CLOCK-003 / STATE-PANEL-002.

Within each asset × anchor sample:

- if a broad episode has k available mechanical legs, each receives weight 1/k;
- each broad episode therefore contributes total weight 1.

This weighting is recalculated for each asset × anchor because PAUSE_START availability differs by cycle.

## 8. Recovery

Recovery is measured from the 12M-window MDD trough.

Search horizon: 60 complete months after the trough.

Report broad-episode-weighted Kaplan-Meier:

- 50% recovery;
- 100% recovery;
- observed versus right-censored counts;
- KM median when reached.

## 9. Phase support

A phase × asset cell is PRIMARY_SUPPORTED only if:

- at least 5 mechanical legs;
- at least 4 broad episodes.

Otherwise it is diagnostic/limited support.

PAUSE_START is expected to have lower support than FIRST_HIKE/LAST_HIKE/FIRST_CUT; the support rule is not relaxed.

## 10. Comparison outputs

For each primary asset, produce a four-phase table containing:

- n legs;
- n broad episodes;
- weighted median +3M/+6M/+12M return;
- weighted median 12M MDD;
- weighted median MDD-trough month;
- EARLY/MID/LATE trough shares;
- weighted 50% and 100% recovery KM medians.

Also produce normalized phase-clock figures.

## 11. No cross-phase significance ranking

The same mechanical cycle can contribute to multiple anchors, and the post-anchor windows can overlap.

Therefore this module does **not** use ordinary independent-sample tests to rank phases.

No p-value family is executed.

The module reports distributions and timing maps only.

A future paired/within-cycle phase comparison would require a separately frozen dependence-aware design.

## 12. Hard QC

Fail if:

- any anchor differs from the canonical timing-corrected registry;
- event month enters the clean path;
- a path lacks M-1 baseline or all 12 post-anchor months;
- MDD is negative;
- MDD-trough month is outside 1..12;
- 100% recovery precedes 50% recovery;
- broad-episode weights fail to sum to 1 inside an available asset × anchor × episode cell;
- unsupported cells are labeled primary;
- raw source histories are committed.

## 13. Evidence status

Allowed:

- **DATA FACT**
- **DESCRIPTIVE RESULT**
- **INVESTMENT IMPLICATION** as risk measurement only
- **NOT YET VERIFIED**

Not allowed:

- "the Fed's last hike causes the bottom";
- "first cut is bullish/bearish" as a causal conclusion;
- deterministic phase-timing rules;
- live trading/deployment claims.

FDR: not applicable.
OOS: not a forecasting model.
Causality: none.
Deployment: none.
