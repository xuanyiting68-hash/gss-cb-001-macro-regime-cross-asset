# ENERGY-PRICE-WF-001 — Research Closeout
Date: 2026-09-24
Status: **EXPLORATORY WALK-FORWARD / NULL CONFIRMATORY FAMILY / NOT DEPLOYABLE**

## Research question

After an extreme energy-price pressure episode begins to roll over, does one additional month of persistent WTI/refined-product weakness distinguish durable downside from false relief?

The specification was frozen before the exhaustive run.

## Data and QC

Public EIA monthly spot-price series via FRED:

- WTI;
- U.S. Gulf Coast conventional gasoline;
- New York Harbor No. 2 heating oil;
- U.S. Gulf Coast jet fuel.

Common sample: **1990-04 through 2026-08**, 437 complete months.

QC:
- missing common months: 0;
- duplicate dates: 0;
- non-positive price cells: 0;
- 34 extreme-pressure months;
- 18 raw rollover months;
- 13 de-clustered S3 events.

Acquisition in the successful run was direct FRED CSV for all four series. Raw source bytes were hashed but were not committed to the public repository.

## Event classification

After the initial rollover, the design waits one month.

- **PRICE_PRODUCT_CONFIRMED**: WTI remains non-positive and at least 2/3 refined-product prices continue to decline.
- **FALSE_RELIEF_VETO**: that persistence condition fails.

Observed events:
- confirmed: 6;
- veto: 7.

One 2026 veto event does not yet have complete 3M/6M forward outcomes.

## Primary results

### WTI 3M

Confirmed:
- mean: **-3.49%**
- median: **+2.55%**
- negative share: **50%**

Veto:
- mean: **+14.89%**
- median: **+13.62%**
- negative share among completed events: **0%**

Mann–Whitney raw p ≈ **0.132**.

### WTI 6M

Confirmed:
- mean: **-3.62%**
- median: **+5.35%**
- negative share: **33.3%**

Veto:
- mean: **+27.42%**
- median: **+20.87%**
- negative share among completed events: **0%**

Mann–Whitney raw p ≈ **0.132**.

### Short-side adverse excursion

3M median MAE:
- confirmed: **+4.60%**
- veto: **+11.31%**

6M median MAE:
- confirmed: **+10.96%**
- veto: **+19.57%**

The confirmed group therefore had smaller adverse excursion descriptively.

## Multiple testing

Four primary tests were declared:

1. WTI 3M return
2. WTI 6M return
3. 3M short MAE
4. 6M short MAE

After BH-FDR at 10%:

**0/4 survive.**

All adjusted q-values are approximately **0.224**.

Therefore the primary confirmatory verdict is:

**NOT CONFIRMED.**

## Robustness

### Leave-one-event-out

For all four primary metrics, the sign of the confirmed-minus-veto difference remains in the same direction in every leave-one-event-out run.

This means the descriptive difference is not created by one single event.

### Historical-era heterogeneity

The pre-2008 subset does **not** reproduce the post-2008 separation.

The 2008+ subset is much stronger.

Support in each subperiod is very small, so this cannot be called a structural break. It is a warning that the relationship is not historically uniform.

### 2008 influence

Removing the selected 2008 crisis event reduces the magnitude, but the confirmed-minus-veto differences remain in the same direction.

## What the result actually says

The one-month price/product persistence rule is **not a validated short signal**.

The confirmed group is too heterogeneous:
- its 3M median WTI return is positive;
- its 6M median is also positive;
- primary FDR does not pass.

The more interesting asymmetric result is the **veto** side.

In this sample, completed FALSE_RELIEF_VETO events were followed by positive WTI returns at both 3M and 6M.

That suggests the filter may be more useful as:

> **“do not assume the reversal is confirmed yet”**

than as:

> **“short WTI now.”**

This is exactly the role a risk-control state machine should have.

## PandaAI implication

Do not convert S3/S4 into a binary buy/sell signal.

A better product representation is:

- pressure state;
- rollover state;
- confirmation state;
- false-relief veto;
- evidence confidence;
- horizon-specific risk distribution;
- max adverse excursion.

For example:

`PRICE ROLLOVER + PRODUCT PERSISTENCE = reversal candidate, not directional approval`

`PRICE ROLLOVER + PRODUCT REACCELERATION = false-relief warning`

## Next gate

The price layer cannot tell whether weakness reflects:

- genuine supply normalization;
- demand destruction;
- temporary price noise;
- or renewed physical supply risk.

The next research layer is therefore the already-frozen:

`ENERGY-PHYSICAL-WF-001`

using release-aware EIA inventories and refinery utilization.

## Evidence classification

**DESCRIPTIVE / ASSOCIATIONAL TIMING EVIDENCE**

**PRIMARY FAMILY NOT SUPPORTED AFTER FDR**

**FALSE-RELIEF VETO: PROMISING HYPOTHESIS**

**NOT DEPLOYABLE**
