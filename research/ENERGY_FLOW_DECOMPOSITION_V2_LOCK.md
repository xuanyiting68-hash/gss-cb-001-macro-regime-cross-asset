# ENERGY-FLOW-002 — Stock–Flow Mechanism Decomposition Lock
Date: 2026-09-24
Status: **POST-v1.1 HYPOTHESIS-GENERATING / FROZEN BEFORE FIRST FLOW RUN**

## Why a new module is required

`ENERGY-PHYSICAL-WF-001 v1.1` falsified a narrow interpretation:

> more inventory relative to seasonal normal + no worsening refinery constraint

did **not** identify subsequent WTI downside.

In the three P4A_DATA_ONLY episodes, WTI was positive at both 3M and 6M after the release-aware decision date.

This does not justify tuning the v1.1 inventory thresholds. Instead, it motivates a new mechanism question:

> **Why did inventories change?**

Inventory is a stock. A stock build can reflect supply recovery, weaker refinery demand, weaker final demand, imports, domestic production, exports, or inventory rebuilding under still-strong demand.

ENERGY-FLOW-002 is therefore a new post-lock research module, not a rescue of v1.1.

## Frozen event set and timing

Use the same 13 de-clustered S3 events from `ENERGY-PRICE-WF-001`.

Use the same curated official EIA baseline/decision release dates from:

`data/public/ENERGY_PHYSICAL_EVENT_RELEASE_REGISTRY_V1.csv`

Do not regenerate events, move decision dates or alter the price thresholds.

1999 remains strict-PIT unavailable unless a separate official exact-release reconstruction is completed.

## Existing stock variables

Retain v1.1 only as descriptive state variables:

- `WCESTUS1` — commercial crude stocks excluding SPR
- `WGTSTUS1` — total motor gasoline stocks
- `WDISTUS1` — distillate fuel oil stocks
- `WPULEUS3` — refinery utilization

Do not reinterpret the failed P4A_DATA_ONLY rule as confirmed evidence.

## New weekly flow variables

Official EIA weekly series:

### Downstream demand/use proxies

- `WGFUPUS2` — product supplied of finished motor gasoline
- `WDIUPUS2` — product supplied of distillate fuel oil
- `WKJUPUS2` — product supplied of kerosene-type jet fuel

Product supplied is treated as a petroleum-use/demand proxy, not a perfect measure of final household demand.

### Refinery throughput

- `WCRRIUS2` — U.S. refiner net input of crude oil

### Upstream supply/inflow

- `WCRFPUS2` — U.S. field production of crude oil
- `WCRIMUS2` — U.S. imports of crude oil

Exports / net imports may be added in a later accounting extension, but are not needed to define this first flow diagnostic.

## Point-in-time seasonal transformation

For every weekly flow series use the same release-aware baseline and decision observations as v1.1.

For each observation:

1. use only the five complete prior calendar years;
2. collect weeks within ±1 ISO week of the current observation;
3. average within each prior year;
4. average the prior-year contributions;
5. require at least 3 prior-year contributions.

Define:

`flow_seasonal_gap = (flow - prior_seasonal_reference) / prior_seasonal_reference`

and

`delta_flow_gap = decision_gap - baseline_gap`.

No future observations enter the state.

## Frozen mechanism flags

### DEMAND_WEAK_COUNT

Count the number of downstream product-supplied series with:

`delta_flow_gap < 0`

across gasoline, distillate and jet fuel.

### THROUGHPUT_WEAK

`delta_flow_gap(refinery crude input) < 0`

### UPSTREAM_SUPPLY_UP_COUNT

Count:

- domestic crude production `delta_flow_gap > 0`;
- crude imports `delta_flow_gap > 0`.

Range: 0–2.

## Post-lock mechanism candidates

These classifications apply only to frozen `PRICE_PRODUCT_CONFIRMED` episodes.

### FLOW_DD — Demand Destruction Candidate

Require:

- PRICE_PRODUCT_CONFIRMED;
- strict PIT available;
- DEMAND_WEAK_COUNT >= 2;
- THROUGHPUT_WEAK = true.

### FLOW_SN — Supply Normalization Candidate

Require:

- PRICE_PRODUCT_CONFIRMED;
- strict PIT available;
- at least 2 of 3 stock blocks improving under v1.1;
- UPSTREAM_SUPPLY_UP_COUNT >= 1;
- THROUGHPUT_WEAK = false;
- DEMAND_WEAK_COUNT <= 1.

### FLOW_MIXED

Any other strict-PIT PRICE_PRODUCT_CONFIRMED episode.

These labels are mechanism candidates, not causal identification.

## Outcomes

Use the v1.1 timing-corrected daily WTI outcomes from the first daily observation on/after decision date:

- 3M WTI return
- 6M WTI return
- 3M short-side MAE
- 6M short-side MAE

## Statistical status

Because this design was motivated by observing the v1.1 falsification and because the frozen price-confirmed sample is very small, the first FLOW-002 run is **descriptive / hypothesis-generating only**.

Do not create a new confirmatory p-value family on the same six price-confirmed episodes.

Report:

- event-level mechanism classification;
- group means/medians;
- sign counts;
- data support;
- whether 2008/2022-like downside episodes map to FLOW_DD.

A future confirmatory version requires a larger event universe or independent sample before formal inference.

## Falsification / interpretation

The flow decomposition is not useful if it does not separate economically distinct episodes or if classifications depend on one event.

Do not claim:

- inventory builds cause WTI to fall;
- product supplied is pure final demand;
- FLOW_DD is a validated short signal.

The objective is mechanism separation:

`Stock change → supply recovery vs throughput weakness vs demand destruction vs mixed state`.

## Public-source provenance

The official EIA series pages / historical XLS endpoints must be recorded with SHA-256, first/last date and row count.

No raw source workbook is committed to the public repo; derived event-level values and provenance are public-safe.
