# ENERGY-WEEKLY-STATE-004 — Strict-PIT Price × Stock-Flow Event Engine Lock
Date: 2026-09-24
Status: **FROZEN BEFORE EVENT-OUTCOME EXECUTION**

## 1. Research question

When a previously extreme petroleum price-pressure state begins to roll over, does newly released weekly physical information distinguish:

- **SUPPLY_NORMALIZATION**: inventories rebuild while upstream supply improves and demand/throughput do not materially weaken;
- **DEMAND_DESTRUCTION**: product demand weakens broadly while refinery throughput also weakens;
- **TIGHT_OR_MIXED**: neither mechanism is cleanly identified?

The primary frozen test is whether SUPPLY_NORMALIZATION has different subsequent WTI path outcomes from TIGHT_OR_MIXED.

DEMAND_DESTRUCTION is retained as a separately labeled mechanism state and is descriptive in v1.

## 2. Strict information clock

Use only the QC-passed `ENERGY-WEEKLY-PIT-003` release registry.

At an event release date R:

- price-state inputs use daily prices strictly before R;
- the week-ending physical/flow observation mapped to R becomes available at R;
- outcomes begin with the first WTI daily observation strictly after R.

No week-ending date is treated as an information date.

## 3. Price inputs

Official EIA series via FRED:

- DCOILWTICO — WTI Cushing spot;
- DGASUSGULF — Gulf Coast conventional gasoline spot;
- DHOILNYH — New York Harbor No. 2 heating oil spot;
- DJFUELUSGULF — Gulf Coast kerosene-type jet fuel spot.

Build an inner common daily price panel.

For each release date R, from the final common price observation strictly before R:

- 5-observation log return for each price;
- 63-observation log return for each price.

For each 63-observation return series, compute an expanding z-score using only prior release observations; minimum 52 prior release observations.

`PRESSURE_SCORE` = mean of the four 63-observation return z-scores.

`EXTREME` if PRESSURE_SCORE exceeds its own prior expanding 90th percentile, requiring 52 prior release observations.

## 4. Price-rollover event

At release R:

- an EXTREME state occurred in the current or previous 3 release observations;
- WTI 5-observation return < 0;
- at least 2 of gasoline/heating-oil/jet-fuel 5-observation returns < 0.

This is `ROLLOVER_RAW`.

De-cluster by retaining the first raw event and requiring **more than 91 calendar days** before another selected event.

No event threshold is altered after execution.

## 5. Weekly physical and flow inputs

Stocks / refinery:
- WCESTUS1 commercial crude stocks ex-SPR;
- WGTSTUS1 gasoline stocks;
- WDISTUS1 distillate stocks;
- WPULEUS3 refinery utilization.

Flows:
- WGFUPUS2 gasoline product supplied;
- WDIUPUS2 distillate product supplied;
- WKJUPUS2 jet-fuel product supplied;
- WCRRIUS2 refinery crude inputs;
- WCRFPUS2 field crude production;
- WCRIMUS2 crude imports.

For each weekly series and event week end:
- seasonal reference = mean of prior five years within ±1 ISO week;
- require at least 3 prior-year contributions;
- seasonal gap = (current - prior-seasonal-reference) / reference.

Mechanism changes are measured against the physical observation **four release rows earlier**.

## 6. Frozen mechanism classification

Compute four-release change in seasonal gap.

### Inventory normalization
`inventory_improving_count` = number of crude/gasoline/distillate stock gaps whose change is >0.

### Demand weakness
`demand_weak_count` = number of gasoline/distillate/jet product-supplied gaps whose change is <0.

### Throughput weakness
`throughput_weak` if refinery crude-input seasonal-gap change <0.

### Upstream supply improvement
`upstream_supply_up_count` = number of field-production/import seasonal gaps whose change is >0.

Classify in this order:

**DEMAND_DESTRUCTION**
- demand_weak_count >=2; and
- throughput_weak = True.

**SUPPLY_NORMALIZATION**
- inventory_improving_count >=2;
- upstream_supply_up_count >=1;
- throughput_weak = False;
- demand_weak_count <=1.

**TIGHT_OR_MIXED**
- all other complete cases.

Incomplete physical cases are labeled DATA_INCOMPLETE and excluded from the primary test.

## 7. Outcome convention

Execution anchor:
- first WTI daily observation strictly after release date.

Outcomes:
- 4-week = 20 WTI observations;
- 8-week = 40 observations;
- 13-week = 65 observations.

For each horizon:
- endpoint return;
- short-side maximum adverse excursion (MAE): maximum positive path return from execution anchor;
- short-side maximum favorable excursion (MFE): negative of minimum path return.

No same-release-day price is used as the execution anchor.

## 8. Frozen primary family

Primary comparison:

`SUPPLY_NORMALIZATION vs TIGHT_OR_MIXED`

Exclude DEMAND_DESTRUCTION from the primary family.

Four tests:
1. 8-week WTI endpoint return;
2. 13-week WTI endpoint return;
3. 8-week short MAE;
4. 13-week short MAE.

Require at least **5 independent selected events per group**. Otherwise label INSUFFICIENT_SUPPORT and do not promote a p-value.

Inference:
- two-sided event-label permutation test of median difference;
- exact enumeration if combinations <=200,000;
- otherwise 100,000 fixed-seed permutations;
- BH-FDR 10% across the four-test family.

Also report leave-one-event-out sign stability.

The expected supply-normalization direction is lower WTI endpoint return / lower short MAE than TIGHT_OR_MIXED, but two-sided p-values are used.

## 9. Secondary diagnostics

Descriptive only:
- DEMAND_DESTRUCTION outcomes;
- group counts by 2002-2009 / 2010-2017 / 2018-present;
- overall price-rollover event outcomes;
- 4-week outcomes.

No additional p-value family is created.

## 10. Hard QC

Fail computational QC if:
- PIT-003 QC is not PASS;
- any selected event uses a price observation on/after its release date;
- any outcome execution date is not strictly after release date;
- selected events are <=91 calendar days apart;
- duplicate selected release dates;
- physical week end does not map exactly to the PIT registry;
- seasonal reference uses current/future years;
- any required source has duplicate dates;
- raw source downloads are committed.

Low event support or null results do not fail computational QC.

## 11. Evidence boundary

**INDEPENDENT WEEKLY STRICT-PIT TEST / ASSOCIATIONAL MECHANISM CLASSIFICATION / NOT CAUSAL / NOT DEPLOYABLE**
