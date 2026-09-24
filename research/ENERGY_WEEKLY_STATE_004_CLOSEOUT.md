# ENERGY-WEEKLY-STATE-004 — Closeout
Date: 2026-09-24
Status: **QC PASS / INDEPENDENT WEEKLY STRICT-PIT TEST / PRIMARY FAMILY INSUFFICIENT SUPPORT / NOT DEPLOYABLE**

## 1. Design

The module was frozen before event-outcome execution and uses the QC-passed PIT-003 release clock.

At every release:
- price inputs are strictly pre-release;
- physical/flow data become available only on their mapped EIA release date;
- WTI outcomes begin strictly after release;
- selected events are de-clustered by >91 calendar days.

## 2. Event support

- release-state rows: 1,288;
- raw rollover rows: 44;
- selected independent events: 17;
- first selected release: 2004-02-11;
- latest selected release: 2026-09-23.

Mechanism labels:
- TIGHT_OR_MIXED: 11;
- DEMAND_DESTRUCTION: 4;
- SUPPLY_NORMALIZATION: 1;
- DATA_INCOMPLETE: 1.

## 3. Frozen primary family

The confirmatory comparison was:

SUPPLY_NORMALIZATION vs TIGHT_OR_MIXED

with a minimum of 5 completed events per group.

Only one SUPPLY_NORMALIZATION event exists.

Therefore all four frozen primary tests are:

**INSUFFICIENT_SUPPORT**

and no p-value is promoted.

This is a support failure, not evidence that the mechanism has no effect.

## 4. Descriptive mechanism map

Among completed TIGHT_OR_MIXED events:
- 8-week WTI median: +7.08%;
- 13-week WTI median: +6.70%;
- 8-week negative-return share: 20%;
- 13-week negative-return share: 40%;
- 8-week short MAE median: 15.24%;
- 13-week short MAE median: 17.92%.

Among the four DEMAND_DESTRUCTION events:
- 8-week WTI median: -2.36%;
- 13-week WTI median: -7.07%;
- 13-week negative-return share: 75%;
- 8-week short MAE median: 13.22%;
- 13-week short MAE median: 13.60%.

The single SUPPLY_NORMALIZATION event:
- 8-week WTI: -5.75%;
- 13-week WTI: -13.20%;
- 8/13-week short MAE: +2.22%.

These descriptive differences are not a new confirmatory family.

## 5. Key interpretation

The pre-frozen supply-normalization state is too rare for inference.

The stronger product implication is asymmetric:

**TIGHT_OR_MIXED is not evidence that the rollover has become a durable bearish state.**

Historically, most completed TIGHT_OR_MIXED events did not produce negative 8-week WTI returns and short-side adverse excursion was material.

DEMAND_DESTRUCTION is a plausible mechanism candidate, but because its descriptive separation was observed after the 004 run and n=4, it must not be re-tested on the same 17 events as though it were pre-specified.

## 6. Prospective opportunity

The newest selected event is 2026-09-23.

At the 004 closeout:
- mechanism = TIGHT_OR_MIXED;
- 4/8/13-week outcomes are still unobserved in the canonical event panel.

This creates a clean prospective event that can be frozen now without backfilling.

## Boundary

**ASSOCIATIONAL MECHANISM CLASSIFICATION / PRIMARY FAMILY UNSUPPORTED FOR SAMPLE-SIZE REASONS / NO CAUSAL OR DEPLOYMENT CLAIM**
