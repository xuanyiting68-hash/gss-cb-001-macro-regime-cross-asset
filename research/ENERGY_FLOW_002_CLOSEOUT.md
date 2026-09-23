# ENERGY-FLOW-002 — Research Closeout
Date: 2026-09-24
Status: **DESCRIPTIVE / HYPOTHESIS-GENERATING / INSUFFICIENT SUPPORT / NOT DEPLOYABLE**

## 1. Why this module exists

The prior release-aware stock-only rule did not confirm WTI downside.

Rather than retuning the failed inventory rule, FLOW-002 asked a different post-lock mechanism question:

> Can stock changes be separated into supply recovery, demand destruction, or mixed flow states?

The design was frozen before the first flow run, but it was motivated by the v1.1 falsification. It is therefore not an independent confirmatory test.

## 2. Public weekly flow data

Official EIA weekly series:

Demand/use proxies:
- finished motor gasoline product supplied (`WGFUPUS2`);
- distillate fuel oil product supplied (`WDIUPUS2`);
- kerosene-type jet fuel product supplied (`WKJUPUS2`).

Refinery throughput:
- refiner net input of crude oil (`WCRRIUS2`).

Upstream supply/inflow:
- field production of crude oil (`WCRFPUS2`);
- crude oil imports (`WCRIMUS2`).

All are transformed relative to prior five-year same-season history using only prior observations.

## 3. QC and support

- Frozen price events: 13.
- Strict-PIT events available: 12.
- Strict-PIT, flow-complete PRICE_PRODUCT_CONFIRMED episodes: **4**.
- FLOW_DD: **0**.
- FLOW_SN: **1**.
- FLOW_MIXED: **3**.
- QC gate: **PASS**.

Two older PRICE_PRODUCT_CONFIRMED episodes are incomplete because one or more exact-week historical flow values are unavailable in the selected official weekly series. They are not filled with future data and are not imputed post hoc.

## 4. Event mechanism map

### 2005 rollover — FLOW_SN

The only Supply-Normalization Candidate:

- inventories improving count: 2/3;
- demand-weak count: 1/3;
- refinery throughput not weak;
- upstream supply-up count: 2/2.

Subsequent WTI:
- 3M: **+3.53%**
- 6M: **+19.34%**

This is not a bearish outcome.

### 2008 rollover — FLOW_MIXED

At the release-aware decision date:

- demand-weak count: 0/3;
- throughput weak: false;
- upstream supply-up count: 1/2.

Subsequent WTI:
- 3M: **−59.44%**
- 6M: **−58.07%**

The later collapse was not yet visible in the frozen demand-flow rule at the decision date.

This is a major timing lesson:

> an eventual demand-destruction episode does not imply that demand destruction was observable at the earlier reversal-decision timestamp.

### 2022 rollover — FLOW_MIXED

- demand-weak count: **3/3**;
- throughput weak: false;
- upstream supply-up count: 2/2.

Subsequent WTI:
- 3M: **−15.16%**
- 6M: **−8.90%**

Demand/use proxies weakened broadly, but the strict FLOW_DD rule was not satisfied because refinery crude input had not weakened relative to its seasonal benchmark.

### 2023 rollover — FLOW_MIXED

- demand-weak count: 2/3;
- throughput weak: false;
- upstream supply-up count: 1/2.

Subsequent WTI:
- 3M: **+16.09%**
- 6M: **+10.93%**

This demonstrates why product-supplied weakness alone cannot be treated as a validated bearish WTI signal.

## 5. What was learned

### A. Inventory abundance is not direction

The v1.1 result already rejected:

`more inventory -> bearish WTI`

as a general timing rule.

### B. Demand weakness is not sufficient by itself

2022 and 2023 both show multiple weaker product-supplied components, but their subsequent WTI directions differ.

### C. Demand destruction can be observable too late

The 2008 event is the clearest example.

The large subsequent collapse was real, but the frozen decision-date flow state did not yet classify as FLOW_DD.

### D. The data architecture is informative even when the signal fails

The research now has a release-aware event map that distinguishes:

- price rollover;
- stock state;
- product-use state;
- refinery throughput;
- upstream supply/inflow;
- future WTI path.

This is suitable for risk-state interpretation and further mechanism research.

## 6. Current evidence verdict

FLOW-002 does **not** establish:

- a Supply-Normalization short signal;
- a Demand-Destruction short signal;
- a deployable WTI directional model.

It also cannot support formal statistical inference with only four complete post-lock price-confirmed flow episodes.

Current classification:

**MECHANISM MAP USEFUL / DIRECTIONAL EDGE NOT ESTABLISHED / NOT DEPLOYABLE**

## 7. Strategic research implication

The next improvement should not be another threshold tweak on the same six episodes.

The remaining high-value directions are:

1. move the event engine from monthly-average prices to a genuinely weekly/daily PIT price state to increase event support and remove monthly-average timing limitations;
2. build an independently frozen geopolitical/physical shock registry;
3. combine demand-flow information with broader growth/financial-condition indicators;
4. test the resulting design on a larger or independent event universe.

For PandaAI, the current energy stack is best treated as a **risk-state engine** rather than a buy/sell engine.
