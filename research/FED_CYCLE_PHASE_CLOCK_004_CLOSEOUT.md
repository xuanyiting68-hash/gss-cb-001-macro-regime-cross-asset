# FED-CYCLE-PHASE-CLOCK-004 — Closeout
Date: 2026-09-24
Status: **QC-PASSED DESCRIPTIVE PHASE MAP / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

## 1. Purpose

PHASE-CLOCK-004 places four realized policy-cycle anchors into one common 12-complete-month cross-asset framework:

- FIRST_HIKE
- LAST_HIKE
- PAUSE_START
- FIRST_CUT

The goal is to describe how historical path risk differs across policy-cycle locations.

It does not identify the causal effect of a hike, pause or cut.

## 2. Design and QC

Common convention:

- baseline = month before anchor month;
- anchor month omitted;
- outcomes use the next 12 complete months;
- broad-episode weighting is recalculated inside each asset × anchor cell;
- no independent-sample cross-phase significance test.

QC passed:

- 1,824 phase-path rows;
- 152 phase × asset × cycle rows;
- **16/16 primary asset × phase cells supported**;
- 0 event-month violations;
- 0 negative-MDD violations;
- 0 MDD-trough timing violations;
- 0 recovery-order violations;
- 0 broad-episode weight violations;
- 0 canonical-anchor-date violations.

## 3. Gold phase map

Broad-episode-weighted medians:

| Anchor | +3M | +6M | +12M | 12M MDD | MDD trough month | 100% recovery KM |
|---|---:|---:|---:|---:|---:|---:|
| FIRST_HIKE | -1.02% | -1.81% | +3.07% | 11.58% | 11 | 19m |
| LAST_HIKE | -1.39% | +1.32% | -2.81% | 9.09% | 6 | 6m |
| PAUSE_START | -0.36% | +1.59% | +4.89% | 7.57% | 9 | 5m |
| FIRST_CUT | -1.29% | +6.00% | +4.06% | 5.43% | 5 | 12m |

### DESCRIPTIVE RESULT

Gold's median 12M drawdown is lower around PAUSE_START and FIRST_CUT than around FIRST_HIKE in this sample.

But FIRST_CUT full recovery is not the fastest: its weighted full-recovery KM median is 12 months versus 5 months after PAUSE_START.

Therefore endpoint return, MDD depth and recovery time remain distinct risk dimensions.

## 4. S&P 500 phase map

| Anchor | +3M | +6M | +12M | 12M MDD | MDD trough month | late trough share M7-12 |
|---|---:|---:|---:|---:|---:|---:|
| FIRST_HIKE | -2.62% | +3.81% | +7.98% | 5.86% | 4 | 40.48% |
| LAST_HIKE | +2.15% | +9.80% | +16.65% | 4.22% | 9 | 66.67% |
| PAUSE_START | +10.06% | +16.00% | +24.64% | 4.22% | 9 | 71.43% |
| FIRST_CUT | +1.69% | +3.76% | +10.98% | 13.99% | 8 | 90.48% |

### DESCRIPTIVE RESULT

The historically strongest S&P median endpoint in this phase map occurs after PAUSE_START, not after FIRST_CUT.

More importantly for risk:

- PAUSE_START median 12M MDD = **4.22%**;
- FIRST_CUT median 12M MDD = **13.99%**.

About **90.5%** of broad-episode-weighted FIRST_CUT MDD trough mass occurs in months 7-12.

This is a strong reason not to equate "first cut" with "risk is over."

It is not evidence that the cut causes the later drawdown.

## 5. Nasdaq phase map

| Anchor | +3M | +6M | +12M | 12M MDD | MDD trough month | late trough share M7-12 |
|---|---:|---:|---:|---:|---:|---:|
| FIRST_HIKE | -6.24% | -0.94% | +6.50% | 12.18% | 7 | 59.52% |
| LAST_HIKE | +1.19% | +8.31% | +15.59% | 4.00% | 8 | 59.52% |
| PAUSE_START | +9.85% | +18.87% | +28.09% | 4.00% | 7 | 57.14% |
| FIRST_CUT | +3.24% | +2.99% | +6.04% | 17.48% | 8 | 90.48% |

### DESCRIPTIVE RESULT

Nasdaq shows the same qualitative phase contrast as S&P in this sample:

- PAUSE_START has a strong positive 12M endpoint and relatively shallow median MDD;
- FIRST_CUT has a much deeper median 12M MDD despite a positive 12M endpoint.

Again, this is descriptive phase association, not a causal effect of cutting rates.

## 6. WTI phase map

| Anchor | +3M | +6M | +12M | 12M MDD | MDD trough month | late trough share M7-12 |
|---|---:|---:|---:|---:|---:|---:|
| FIRST_HIKE | +17.19% | +14.88% | +22.45% | 18.79% | 10 | 66.67% |
| LAST_HIKE | +8.79% | -0.53% | +5.01% | 19.60% | 7 | 66.67% |
| PAUSE_START | -11.66% | -2.06% | -4.57% | 17.99% | 9 | 66.67% |
| FIRST_CUT | -3.74% | +2.88% | -16.94% | 22.23% | 11 | 100.00% |

### DESCRIPTIVE RESULT

WTI's FIRST_CUT phase is the clearest late-risk case:

- median +12M return = **-16.94%**;
- median 12M MDD = **22.23%**;
- median MDD trough month = **11**;
- 100% of broad-episode-weighted MDD trough mass is in months 7-12.

This still does not mean the first cut causes oil weakness. A first cut can coincide with deteriorating macro conditions.

## 7. The common "first cut = safe" narrative

The four assets do not support a universal phase rule.

In this descriptive sample:

- Gold FIRST_CUT median MDD is relatively shallow;
- S&P and Nasdaq FIRST_CUT median MDDs are much deeper than after PAUSE_START;
- WTI FIRST_CUT has a negative median +12M endpoint and the latest risk concentration.

Therefore:

**FIRST_CUT is a policy-cycle marker, not a universal risk-off or risk-on signal.**

## 8. Recovery

Selected broad-episode-weighted full-recovery KM medians:

### Gold
- FIRST_HIKE: 19m
- LAST_HIKE: 6m
- PAUSE_START: 5m
- FIRST_CUT: 12m

### Nasdaq
- FIRST_HIKE: 8m
- LAST_HIKE: 3m
- PAUSE_START: 3m
- FIRST_CUT: 3m

### S&P 500
- FIRST_HIKE: 4m
- LAST_HIKE: 1m
- PAUSE_START: 3m
- FIRST_CUT: 5m

### WTI
- FIRST_HIKE: 3m
- LAST_HIKE: 19m
- PAUSE_START: 8m
- FIRST_CUT: 9m

Recovery speed and drawdown depth do not move one-for-one.

## 9. Evidence classification

### DATA FACT
- all 16 primary asset × phase cells satisfy the frozen support rule;
- all canonical anchor dates match the timing-corrected registry;
- one common 12M convention is applied to every phase.

### DESCRIPTIVE RESULT
- phase-risk profiles differ materially across assets;
- S&P/Nasdaq pause and first-cut phases have very different MDD distributions;
- WTI risk is especially late after FIRST_CUT;
- Gold does not share the same FIRST_CUT pattern.

### CAUSAL EVIDENCE
**None.**

The same cycles appear at multiple anchors and windows overlap.

### FDR
Not applicable. No p-value family is run.

### OOS
Not applicable. This is not a forecasting model.

### DEPLOYMENT
Not deployable.

## 10. Investment-research implication

PandaAI should represent the policy cycle as a **phase-conditioned risk distribution**, not as:

- "hiking = bearish";
- "pause = bullish";
- "cut = safe."

A more useful product primitive is:

'policy phase + asset + path-risk clock + uncertainty + state context'.

## 11. Next research priority

The descriptive phase map now makes a new question possible:

**Do cross-asset stress indicators change before the later drawdowns?**

The next public-safe extension should add, where historical coverage permits:

- VIX;
- credit spreads;
- copper;
- broader financial-conditions diagnostics.

These should be treated as risk-state observables, not retrofitted trading signals.
