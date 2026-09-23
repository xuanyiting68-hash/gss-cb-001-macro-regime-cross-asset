# ENERGY-PHYSICAL-WF-001 v1.1 — Mechanism Diagnostic
Date: 2026-09-24

## Status

**POST-RESULT / HYPOTHESIS-GENERATING / NOT A NEW CONFIRMATORY FAMILY**

The frozen primary result remains the four-test P4A_DATA_ONLY vs PHYSICAL_VETO_DATA_ONLY family.

## Within the frozen price-confirmed episodes

- Completed price-confirmed episodes with strict PIT: 6.
- P4A_DATA_ONLY: 3.
- Price-confirmed but non-P4A: 3.

| physical_subgroup       | metric       |   n |       mean |     median |   negative_share |
|:------------------------|:-------------|----:|-----------:|-----------:|-----------------:|
| P4A_DATA_ONLY           | wti_fwd_3m   |   3 |  0.133103  |  0.160916  |         0        |
| P4A_DATA_ONLY           | wti_fwd_6m   |   3 |  0.147797  |  0.140683  |         0        |
| P4A_DATA_ONLY           | short_mae_3m |   3 |  0.175499  |  0.172804  |       nan        |
| P4A_DATA_ONLY           | short_mae_6m |   3 |  0.243433  |  0.256018  |       nan        |
| PRICE_CONFIRMED_NON_P4A | wti_fwd_3m   |   3 | -0.153297  | -0.151594  |         0.666667 |
| PRICE_CONFIRMED_NON_P4A | wti_fwd_6m   |   3 | -0.0980725 | -0.0890052 |         0.666667 |
| PRICE_CONFIRMED_NON_P4A | short_mae_3m |   3 |  0.183762  |  0.135383  |       nan        |
| PRICE_CONFIRMED_NON_P4A | short_mae_6m |   3 |  0.206645  |  0.135383  |       nan        |

### Direct diagnostic

- P4A 3M WTI median: +16.09%; positive share: 100.0%.
- P4A 6M WTI median: +14.07%; positive share: 100.0%.
- Non-P4A price-confirmed 3M median: -15.16%.
- Non-P4A price-confirmed 6M median: -8.90%.

Under the current rule, inventory normalization does not behave like a downside-confirmation variable. In the three P4A_DATA_ONLY episodes, WTI is positive at both 3M and 6M after the release-aware decision date.

That does **not** establish the opposite rule. Support is only three events. It falsifies the narrow interpretation that 'more inventories relative to seasonal normal + no refinery worsening' is by itself a reliable falling-WTI confirmation.

## Inventory-improvement-count diagnostic

|   inventory_improving_count | metric     |   n |      mean |    median |   negative_share |
|----------------------------:|:-----------|----:|----------:|----------:|-----------------:|
|                           1 | wti_fwd_3m |   2 | -0.373001 | -0.373001 |                1 |
|                           1 | wti_fwd_6m |   2 | -0.334854 | -0.334854 |                1 |
|                           2 | wti_fwd_3m |   3 |  0.133103 |  0.160916 |                0 |
|                           2 | wti_fwd_6m |   3 |  0.147797 |  0.140683 |                0 |
|                           3 | wti_fwd_3m |   1 |  0.286109 |  0.286109 |                0 |
|                           3 | wti_fwd_6m |   1 |  0.37549  |  0.37549  |                0 |

Among the small price-confirmed sample, a larger inventory-improvement count is not monotonically associated with more-negative WTI outcomes.

## Mechanism interpretation

Inventory accumulation is economically ambiguous. Stocks can rise because supply recovered, because imports/production rose, because refinery demand weakened, because final demand weakened, or because firms rebuilt inventories while demand and risk premia remained strong.

The next research design therefore needs **flows**, not only stocks:

- product supplied (gasoline, distillate, jet) as demand/use proxies;
- refinery crude inputs / throughput;
- domestic crude production;
- crude imports/net imports;
- later, independently frozen geopolitical/shipping shock tags.

## Evidence verdict

**The v1.1 physical-stock rule does not add validated downside timing information.**

Do not tune the v1.1 thresholds to rescue it. Preserve it as a negative/falsification result and treat any flow-decomposition model as a new post-lock hypothesis.