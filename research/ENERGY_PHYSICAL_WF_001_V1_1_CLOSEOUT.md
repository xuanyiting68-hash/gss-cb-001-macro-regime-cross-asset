# ENERGY-PHYSICAL-WF-001 v1.1 — Research Closeout
Date: 2026-09-24
Status: **DATA-ONLY HYPOTHESIS NOT SUPPORTED / FULL P4A NOT EVALUATED / NOT DEPLOYABLE**

## 1. Research question

Does release-aware U.S. inventory/refinery information add useful downside discrimination after the frozen energy-price rollover state?

The event universe and price-layer thresholds were preserved from `ENERGY-PRICE-WF-001`.

## 2. Timing correction before result interpretation

The price-layer data use monthly average spot prices. A monthly average stamped at month start is not known at month start.

Before interpreting the physical result, v1.1 therefore froze a stricter timing convention:

- baseline = last actual EIA WPSR release on/before S3 month-end;
- decision = first actual EIA WPSR release after the confirmation month-end;
- outcome anchor = first daily WTI observation on/after the decision release date.

This prevents the physical extension from treating a full-month average as if it had been observable at the beginning of the month.

## 3. Release-registry audit and superseded first execution

The first automated physical execution exposed a QC failure in the historical EIA release-date parser.

The parser silently produced an incomplete historical registry and, for some 2020–2023 events, incorrectly matched a 2017 baseline to a 2026 decision date.

That first execution is **QUARANTINED / INVALID FOR EVIDENCE**.

It remains in Git history only as an audit trail.

The corrected execution uses the event-scoped official release registry:

`data/public/ENERGY_PHYSICAL_EVENT_RELEASE_REGISTRY_V1.csv`

with explicit timing QC. The corrected run has:

- 24 baseline/decision registry rows;
- 12/13 strict-PIT events available;
- 1999 event unavailable under the current exact-release registry;
- zero bad timing mappings;
- zero duplicate event dates;
- frozen 13-event price universe preserved.

Only the corrected execution is admissible.

## 4. Physical variables

Official EIA weekly data:

- commercial crude stocks excluding SPR;
- total motor gasoline stocks;
- distillate fuel oil stocks;
- refinery utilization.

For inventories, the state is the deviation from a same-season prior-five-year reference using only prior years.

`inventory improving` means the seasonal gap is less tight / more abundant at the decision release than at the baseline release.

## 5. Data-only P4A classification

Because an independently frozen geopolitical/shipping shock-veto registry is not yet applied, the first run is explicitly `DATA_ONLY`.

`P4A_DATA_ONLY` requires:

- frozen PRICE_PRODUCT_CONFIRMED state;
- strict PIT mapping;
- at least two of three inventory blocks improving;
- no worsening high-utilization refinery constraint.

Corrected support:

- P4A_DATA_ONLY: **3**
- PHYSICAL_VETO_DATA_ONLY: **9**
- strict PIT unavailable: **1**

## 6. Frozen four-test family

### WTI 3M

P4A:
- mean **+13.31%**
- median **+16.09%**

Veto:
- mean **+6.59%**
- median **+9.68%**

raw Mann–Whitney p ≈ **0.921**

### WTI 6M

P4A:
- mean **+14.78%**
- median **+14.07%**

Veto:
- mean **+16.10%**
- median **+24.45%**

raw p ≈ **0.776**

### Short-side MAE 3M

P4A median:
- **+17.28%**

Veto median:
- **+17.59%**

raw p = **1.000**

### Short-side MAE 6M

P4A median:
- **+25.60%**

Veto median:
- **+27.02%**

raw p ≈ **0.921**

BH-FDR across the four frozen tests:

**0/4 pass at 10%.**

All adjusted q-values are **1.00**.

## 7. Stronger falsification check: within the frozen price-confirmed episodes

This is post-result diagnostic evidence, not a new confirmatory family.

There are six completed strict-PIT PRICE_PRODUCT_CONFIRMED episodes:

### P4A_DATA_ONLY — n=3

- 3M WTI median: **+16.09%**
- 6M WTI median: **+14.07%**
- positive WTI share: **3/3 at 3M and 3/3 at 6M**

### PRICE_CONFIRMED but non-P4A — n=3

- 3M WTI median: **−15.16%**
- 6M WTI median: **−8.90%**
- negative share: **2/3**

This does **not** validate the opposite rule because n is extremely small.

It does falsify the narrow claim that the current stock-normalization definition is a reliable confirmation of falling WTI.

## 8. Why the stock rule fails economically

Inventory accumulation is not a structural shock.

Stocks can rise because:

- supply recovered;
- imports increased;
- domestic production increased;
- refinery crude demand weakened;
- final product demand weakened;
- firms rebuilt inventories while demand remained strong;
- risk premia / geopolitical conditions kept prices elevated.

Therefore:

`inventory build != supply normalization != bearish WTI`

without observing the underlying flows.

## 9. Current verdict

### Supported

- Release-aware physical-state construction is feasible.
- Exact information timing materially matters.
- Inventory levels alone are economically ambiguous.
- The 13-event price universe can be preserved while adding public physical data.

### Not supported

- `P4A_DATA_ONLY` as currently defined does not add validated WTI downside timing.
- It does not improve the frozen price-layer result.
- It must not be marketed as a short signal.

### Not yet evaluated

Full P4A with:

- independently frozen geopolitical/shipping shock veto;
- complete supply-vs-demand flow decomposition.

## 10. Next research module

Do **not** retune v1.1 inventory thresholds.

The next module is a new post-lock hypothesis:

`ENERGY-FLOW-002`

It decomposes the stock state using:

- gasoline / distillate / jet product supplied;
- refinery crude inputs;
- domestic crude production;
- crude imports.

The goal is to separate:

`SUPPLY NORMALIZATION`

from:

`DEMAND DESTRUCTION`

and:

`MIXED / AMBIGUOUS STOCK BUILD`.

The first FLOW-002 run is descriptive / hypothesis-generating only because it is motivated by this v1.1 falsification.
