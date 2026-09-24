# FED-CYCLE-VINTAGE-AUDIT-007 — Closeout
Date: 2026-09-24
Status: **QC-PASSED REAL-TIME REVISION AUDIT / RETURN ASSOCIATION STRENGTHENED / MDD RELATION NOT CONFIRMED / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

## 1. Purpose

VINTAGE-AUDIT-007 asks whether the Fed-cycle Gold growth-state evidence survives when current-vintage industrial production is replaced by the information that was actually available in real time.

Primary real-time source:

- Federal Reserve Bank of Philadelphia RTDSM;
- monthly `IPT` industrial-production vintages;
- official vintage coverage parsed from 1962-11 through 2026-08.

The original CPI state is not replaced because STATE-001 uses `CPIAUCNS` (not seasonally adjusted), while Philadelphia Fed `PCPI` is seasonally adjusted and is not the same series definition.

## 2. Frozen real-time timing rule

For information month M:

- target IP observation = M-2;
- base observation = M-14;
- both values must come from the same RTDSM vintage;
- selected vintage must be no later than M-1.

This deliberately prevents same-month vintage look-ahead.

The original growth threshold remains unchanged:

- STRONG if YoY >= 2%;
- WEAK otherwise.

## 3. Source and parser QC

Official Philadelphia Fed workbook:

- parsed cells: **477,136**;
- distinct monthly vintages: **766**;
- first vintage: **1962-11**;
- last vintage: **2026-08**;
- 10/10 FIRST_HIKE events have real-time IPT support;
- 165/165 monthly panel rows have real-time IPT support.

Hard QC:

- 0 event vintage-timing violations;
- 0 panel vintage-timing violations;
- 0 M-2 target-period violations;
- 0 cycle-weight violations;
- raw workbook not committed.

## 4. Event-level revision impact

Across the ten FIRST_HIKE events:

- growth-state flips: **1/10**;
- median absolute YoY revision gap: **2.225 percentage points**;
- maximum absolute revision gap: **4.035 pp**.

The only state flip is 2022:

- current-vintage INDPRO YoY: **+1.32% -> WEAK**;
- real-time IPT YoY available before the event month: **+4.12% -> STRONG**.

This is a material example of why revised macro history should not automatically be treated as the state policymakers/investors observed at the time.

## 5. Event-level Gold contrast after the label revision

The original STATE-001 current-vintage classification:

- STRONG n=6;
- WEAK n=4.

Real-time IPT classification:

- STRONG n=7;
- WEAK n=3.

### +12M Gold return

STRONG minus WEAK median difference:

- current-vintage labels: **-8.31 percentage points**;
- real-time IPT labels: **-9.12 pp**.

The direction and approximate scale survive the 2022 label revision.

### +24M Gold return

STRONG minus WEAK:

- current: **-16.07 pp**;
- real-time: **-5.50 pp**.

The longer-horizon endpoint contrast weakens materially.

### 24M MDD

STRONG minus WEAK:

- current: **+2.67 pp**;
- real-time: **-0.47 pp**.

The prior event-level MDD separation does **not** survive the real-time label revision.

### Interpretation

The event-level growth-state story is therefore not one single robust object:

- +12M endpoint direction is revision-robust in this n=10 descriptive sample;
- +24M endpoint magnitude is revision-sensitive;
- MDD contrast is revision-fragile.

No event-level significance test is added.

## 6. Within-cycle same-sample revision audit

All 165 panel rows are available under both:

- current-vintage INDPRO YoY;
- real-time IPT YoY.

Estimator is unchanged from STATE-PANEL-002:

- mechanical-cycle fixed effects;
- equal total weight per cycle;
- 7 broad episode clusters;
- exact whole-cluster sign-flip inference;
- overlapping outcomes are not treated as IID.

### Gold next-6M endpoint return

Current-vintage INDPRO, same 165 rows:

- beta: **-1.27 pp Gold return per 1 within-cycle growth SD**;
- broad exact p: **0.125**;
- mechanical-cycle exact p: 0.1113.

Real-time IPT:

- beta: **-1.96 pp / SD**;
- broad exact p: **0.015625**;
- mechanical-cycle exact p: 0.02539;
- leave-one-broad-episode sign stable.

The coefficient sign is the same, but the real-time specification is more negative.

### Gold next-6M MDD

Current:

- beta: +0.35 pp;
- broad p: 0.390625.

Real-time:

- beta: +0.32 pp;
- broad p: 0.71875.

There is no supported MDD association.

## 7. What the exact p=0.015625 means

The post-run score audit shows that all seven broad episode score contributions for the real-time IPT -> next-6M Gold return relation are negative:

- B01 negative;
- B02 negative;
- B03 negative;
- B04 negative;
- B05 negative;
- B06 negative;
- B07 negative.

With seven broad clusters, the two-sided exact sign-flip probability of all cluster contributions lining up in the observed direction is:

`2 / 2^7 = 0.015625`.

Therefore the small exact p-value is driven importantly by **7/7 sign unanimity across broad episodes**.

It should not be described as high-precision forecasting evidence.

## 8. Post-run restriction audit

These restrictions were specified only **after** the full-sample result was observed and are robustness diagnostics, not confirmatory tests.

### Excluding 2022

Support:

- 136 rows;
- 9 cycles;
- 6 broad episodes.

Real-time IPT -> Gold next-6M return:

- beta: **-1.49 pp / SD**;
- broad exact p: **0.03125**.

Thus the full-sample relation is not created solely by the 2022 state flip.

### Excluding early B01/B02 episodes

Support:

- 135 rows;
- 5 cycles;
- 5 broad episodes.

Real-time coefficient:

- **-2.99 pp / SD**;
- broad exact p: **0.0625**.

The sign remains negative, but exact inference becomes coarse as the number of independent broad episodes falls.

### Excluding both early B01/B02 and 2022

- 106 rows;
- 4 cycles;
- 4 broad episodes.

This falls below the frozen minimum of 5 mechanical cycles.

Status:

**LIMITED SUPPORT — no exact p-value promoted.**

The coefficient remains negative (-2.34 pp / SD), but it is not treated as a supported test.

## 9. Revision-size diagnostics across the 165 monthly rows

Current-vintage versus real-time growth:

- Pearson correlation: **0.900**;
- median absolute YoY revision gap: **1.03 pp**;
- 90th percentile absolute gap: **2.74 pp**;
- maximum absolute gap: **3.89 pp**.

Thus current and real-time histories are highly correlated but economically meaningful revisions remain common enough to matter for state classification and coefficients.

## 10. Evidence classification

### DATA FACT

- official RTDSM IPT provides full real-time support for all 10 events and all 165 panel rows;
- one of ten event growth labels flips;
- revision gaps are economically non-trivial.

### REVISION ROBUSTNESS RESULT

The negative relation between within-cycle growth and next-6M Gold endpoint return becomes stronger under the conservative real-time IPT construction and remains negative after excluding 2022 and after excluding early episodes.

### ASSOCIATIONAL ROBUSTNESS CANDIDATE

The real-time endpoint-return result is a stronger mechanism candidate than the current-vintage INDPRO result.

However:

- VINTAGE-AUDIT-007 was defined as a revision audit, not a new confirmatory testing family;
- restriction checks are post-run;
- only seven broad clusters exist in the full sample;
- there is no OOS forecast;
- there is no causal identification.

Therefore it is **not** promoted to a confirmed Gold predictor.

### MDD EVIDENCE

Not confirmed.

The within-cycle MDD coefficient remains unsupported and the event-level MDD contrast disappears under the real-time label.

## 11. CPI boundary

The project must continue to distinguish:

- original `CPIAUCNS` = not seasonally adjusted CPI-U;
- Philadelphia Fed `PCPI` = seasonally adjusted CPI.

They are not interchangeable.

VINTAGE-AUDIT-007 does not upgrade the CPI state into a strict real-time-vintage object.

## 12. Product implication

For PandaAI:

- revised macro history and real-time macro state should be separate data objects;
- any historical replay should prefer the information set available at that time;
- growth state can be shown with a provenance flag such as `REALTIME_VINTAGE` versus `CURRENT_REVISED`;
- the Gold endpoint relationship can be shown only as historical associational context with uncertainty.

Do not convert this result into an automatic Gold trading signal.

## 13. Research implication

The next stronger question is not:

"Can we tune the 2% growth threshold?"

It is:

**Does real-time macro information add time-ordered forecasting value beyond policy phase, Gold's own history and simple market-state benchmarks?**

That requires a separately frozen walk-forward OOS design and should not reuse in-sample exact p-values as proof of forecasting value.
