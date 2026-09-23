# ENERGY-PRICE-WF-001 — Long-History Price/Product Walk-Forward Lock
Date: 2026-09-24
Status: FROZEN BEFORE FIRST EXHAUSTIVE RUN

## Purpose

Test one narrow part of the Energy Reversal State Machine with long-history public data:

> After an extreme energy-price pressure episode begins to roll over, does **persistent refined-product price weakness** distinguish more durable WTI downside from false relief?

This phase is intentionally **price/product only**. It is not allowed to call the confirmation state “physical supply normalization” because inventories, refinery utilization and external physical-shock tags are not yet included.

## Official/public source series

Monthly EIA spot-price series distributed through FRED:

- WTI Cushing: `MCOILWTICO`
- U.S. Gulf Coast conventional regular gasoline: `MGASUSGULF`
- New York Harbor No. 2 heating oil: `MHOILNYH`
- U.S. Gulf Coast kerosene-type jet fuel: `MJFUELUSGULF`

Main common sample begins when all four series are available: 1990-04.

The code must record source URL, retrieval timestamp, SHA-256, row count, first date, last date and missing-value count. Raw downloads are used during computation but are not committed to the public repository.

## Point-in-time construction

All thresholds at month t use only observations dated before t.

No future outcome may affect event classification.

### Returns

For each price series:

- 1M log change
- 3M log change

### Prior-history z-score

For each 3M return at t:

`z_i(t) = [r_i,3m(t) - mean(r_i,3m before t)] / sd(r_i,3m before t)`

Minimum prior history: 60 complete common months.

### Energy price-pressure score

`PRESSURE(t) = mean(z_WTI, z_gasoline, z_heating_oil, z_jet)`

The extreme threshold at t is the 90th percentile of **prior** valid pressure scores.

### S2_PRICE_EXTREME

`PRESSURE(t) > prior_q90(t)`

### S3_INITIAL_ROLLOVER

Month t is an initial rollover when:

1. an S2_PRICE_EXTREME occurred in t, t-1 or t-2;
2. WTI 1M log change < 0;
3. at least 2 of 3 refined-product 1M log changes < 0.

Signals are clustered: after selecting an S3 event, do not select another S3 event for the next 6 months.

### One-month confirmation gate

Classification is made at t+1 and the forward-return anchor is the t+1 monthly WTI observation.

**PRICE_PRODUCT_CONFIRMED** if at t+1:

- WTI 1M log change <= 0; and
- at least 2 of 3 refined-product 1M log changes < 0.

Otherwise:

**FALSE_RELIEF_VETO**

This one-month waiting rule prevents the confirmation label from using information that was unavailable at the trade/research anchor.

## Primary outcomes

From the confirmation/veto anchor month:

WTI endpoint return:
- 1M
- 3M
- 6M
- 12M

Short-side path risk:
- max adverse excursion through 3M
- max adverse excursion through 6M

A positive adverse excursion means WTI rose against a hypothetical short.

No leverage, transaction-cost or position-size assumptions enter this phase.

## Primary inferential family

Four predeclared two-sided comparisons between PRICE_PRODUCT_CONFIRMED and FALSE_RELIEF_VETO:

1. 3M endpoint WTI return
2. 6M endpoint WTI return
3. 3M short-side max adverse excursion
4. 6M short-side max adverse excursion

Primary test: Mann–Whitney U.

Apply BH-FDR at 10% across these four tests.

Also report means, medians, negative-return share, support and raw p-values.

## Robustness only

Do not select the main conclusion from robustness runs.

- prior pressure threshold 80th percentile;
- prior pressure threshold 95th percentile;
- pre-2008 and 2009+ descriptive splits;
- 3-month vs 6-month event de-clustering.

## Falsification

The price/product persistence hypothesis is weakened if:

- confirmed events do not have more-negative 3M/6M WTI outcomes than veto events;
- confirmed events do not reduce short-side adverse excursion;
- any apparent effect is dominated by one crisis;
- results reverse across broad subperiods;
- a simple WTI rollover rule performs equally well.

## Interpretation boundary

Even a successful result is only:

**PUBLIC PRICE-PRODUCT TIMING EVIDENCE**

It is not evidence that physical supply normalized and is not a deployable short strategy.

The next gate must add EIA inventory/refinery data with release-aware timing and physical-shock tags.
