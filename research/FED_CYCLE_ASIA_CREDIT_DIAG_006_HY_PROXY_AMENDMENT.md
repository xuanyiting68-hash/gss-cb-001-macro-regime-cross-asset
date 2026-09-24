# FED-CYCLE-ASIA-CREDIT-DIAG-006 — High-Yield Price-Proxy Amendment
Date: 2026-09-24
Status: **FROZEN AFTER OAS SOURCE-COVERAGE AUDIT / BEFORE HYG OUTCOME EXECUTION**

## 1. Trigger

The frozen FRED series `BAMLH0A0HYM2` was acquired successfully but currently exposes only:

- 2023-09-25 onward.

FRED's current series note states that, beginning in April 2026, the ICE BofA OAS series includes only the most recent three years of observations.

Therefore the long-history OAS diagnostic is data-limited, not computationally failed.

The original OAS result remains in the repository as:

`INSUFFICIENT_SUPPORT`.

It is not backfilled from an unlicensed/vendor source.

## 2. Additional proxy

Freeze one separate market-price proxy:

- iShares iBoxx $ High Yield Corporate Bond ETF;
- Yahoo symbol: `HYG`;
- daily closes aggregated to monthly averages.

HYG is a **high-yield bond price proxy**.

It is not:

- an option-adjusted spread;
- a direct substitute for ICE BofA OAS;
- a pure credit-risk measure.

It contains duration, spread, liquidity, coupon and ETF-market effects.

## 3. Timing

Use the same four canonical anchors:

- FIRST_HIKE
- LAST_HIKE
- PAUSE_START
- FIRST_CUT

For anchor month M0:

- baseline = M-1 monthly average;
- omit M0;
- use M+1..M+12.

## 4. Metrics

For every supported HYG cycle × phase:

- +3M return;
- +6M return;
- +12M return;
- 12M MDD;
- MDD-trough month;
- late-trough share months 7-12.

## 5. Support labels

Use the already frozen diagnostic labels:

- ADEQUATE_DIAGNOSTIC: >=4 legs and >=4 broad episodes;
- LIMITED_SUPPORT: >=2 legs and >=2 broad episodes;
- INSUFFICIENT_SUPPORT otherwise.

No threshold is relaxed.

## 6. Interpretation

HYG results may be used only as:

**LIMITED-SUPPORT HIGH-YIELD PRICE-MARKET CONTEXT.**

They must not be pooled with OAS as if they measure the same object.

No causal, FDR, OOS or deployment claim.
