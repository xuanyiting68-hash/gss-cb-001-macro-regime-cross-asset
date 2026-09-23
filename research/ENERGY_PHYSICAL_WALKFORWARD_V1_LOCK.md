# ENERGY-PHYSICAL-WF-001 — Release-Aware Physical Confirmation Lock
Date: 2026-09-24
Status: FROZEN BEFORE FIRST PHYSICAL EXTENSION RUN

## Research question

Among energy-price rollover episodes, does **observable physical normalization** improve the ability to distinguish durable WTI downside from false relief?

This phase is a public companion research module. It does not alter the private academic-paper specification.

## Source hierarchy

Primary public sources:

- U.S. EIA Weekly Petroleum Status Report (WPSR)
- EIA/FRED public weekly series for cross-checking and long-history values

Candidate weekly variables:

- U.S. commercial crude stocks excluding SPR
- total motor gasoline stocks
- distillate fuel oil stocks
- refinery utilization

The exact series IDs and units must be recorded in a source registry before estimation.

## Critical timing rule

The weekly observation period is **not** the information-availability date.

For each weekly observation, record the WPSR publication/release date. A physical variable may enter a state at date t only after its public release.

Holiday-shifted WPSR releases must use the actual release date. Do not impose a universal Wednesday assumption in the confirmatory run.

If exact release dates cannot be reconstructed for a historical week, mark the observation unavailable for the strict PIT specification.

## Starting event set

The price-layer S3 rollover events are generated only by the frozen `ENERGY-PRICE-WF-001` algorithm.

This physical extension may classify those events but may not create or delete price events after seeing future returns.

## Physical normalization blocks

Evaluate information available during the confirmation window after S3.

### Inventory normalization

Construct prior-history percentile/z-score states separately for:

- crude stocks excluding SPR;
- gasoline stocks;
- distillate stocks.

A product inventory is considered improving when its release-time state rises relative to its own recent seasonal/history benchmark.

Because petroleum inventories are strongly seasonal, the primary implementation must use a seasonal comparison rather than raw level changes alone.

Preferred primary transformation:
- deviation from a rolling same-week-of-year historical benchmark using only prior years.

### Refinery constraint state

Refinery utilization is not monotonic in interpretation:

- rising utilization can signal supply response;
- extremely high utilization can signal limited spare refining capacity;
- falling utilization can reflect outages or demand destruction.

Therefore it enters as a state variable, not a simple “higher is better” score.

Predeclared flags:

- `REFINERY_HIGH`: utilization above prior-history 90th percentile for the comparable seasonal window;
- `REFINERY_DROP`: utilization declines by at least 5 percentage points over the predeclared short window.

The 5pp drop is a demand-destruction/outage diagnostic, not evidence of supply normalization.

## Two confirmation channels

### P4A — Physical Supply Normalization Candidate

Require all of:

1. frozen price layer is S3;
2. price/product confirmation is present;
3. at least two of three inventory blocks move toward less-tight conditions;
4. no refinery-outage/high-utilization stress worsening;
5. no newly documented geopolitical/shipping supply shock during the confirmation window.

### P4B — Demand Destruction Candidate

Require:

1. frozen price layer is S3;
2. WTI/product prices are falling;
3. evidence of sharp throughput/activity deterioration, including a refinery-utilization drop or an independently defined growth/financial-stress indicator.

P4B is not pooled with P4A in the primary mechanism interpretation.

### PHYSICAL-VETO — False Relief / Persistent Tightness

Assign when S3 occurs but:

- gasoline/distillate inventories remain unusually tight or worsen;
- refinery constraints remain extreme/worsen;
- products reaccelerate;
- or a new physical supply disruption appears.

## Outcomes

WTI:
- 1M / 3M / 6M / 12M endpoint return;
- 3M / 6M short-side maximum adverse excursion;
- time to trough.

Cross-asset secondary outcomes:
- Gold;
- broad USD;
- 2Y / 10Y nominal yields;
- 10Y real yield;
- 5Y breakeven;
- broad equity index.

## Primary comparisons

Do not pool P4A and P4B as one “success” group.

Primary family:

1. P4A vs PHYSICAL-VETO — WTI 3M
2. P4A vs PHYSICAL-VETO — WTI 6M
3. P4A vs PHYSICAL-VETO — short MAE 3M
4. P4A vs PHYSICAL-VETO — short MAE 6M

BH-FDR at 10%.

P4B is reported as a separate mechanism family and requires adequate support before formal inference.

## Falsification

The physical layer adds no useful timing information if:

- P4A does not improve the price-only confirmed/veto separation;
- release-aware timing removes the effect;
- inventory signals are driven by one crisis;
- a simple WTI rollover benchmark performs as well;
- results reverse materially across broad historical eras.

## Evidence boundary

Even if supported, this is a state-dependent historical timing result, not a claim that a specific physical variable causes WTI to fall and not a personalized trading recommendation.

No social-media “short signal” language is allowed unless OOS and deployment gates are separately passed.
