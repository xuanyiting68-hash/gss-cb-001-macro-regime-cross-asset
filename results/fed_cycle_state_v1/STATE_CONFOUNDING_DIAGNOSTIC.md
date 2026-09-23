# FED-CYCLE-STATE-001 — Confounding diagnostic

**DESCRIPTIVE / ASSOCIATIONAL DIAGNOSTIC / NOT CAUSAL / NOT DEPLOYABLE**

## USD frozen-gate result

| state_var                | state_a   | state_b         | outcome      |   n_a |   n_b |   median_a |   median_b |   oriented_median_diff_a_minus_b | status                | loo_sign_stable   |
|:-------------------------|:----------|:----------------|:-------------|------:|------:|-----------:|-----------:|---------------------------------:|:----------------------|:------------------|
| USD_DIRECTION_DIAGNOSTIC | RISING    | FALLING_OR_FLAT | gold_ret_12m |     5 |     5 |  0.0362319 |  -0.117647 |                        0.153879  | SUPPORTED_DESCRIPTIVE | True              |
| USD_DIRECTION_DIAGNOSTIC | RISING    | FALLING_OR_FLAT | gold_mdd_24m |     5 |     5 |  0.136567  |   0.225389 |                       -0.0888214 | SUPPORTED_DESCRIPTIVE | True              |

## Chronological-separation audit

| state_var                | state_a   | state_b          |   n_a |   n_b | years_a                                      | years_b                                           |   min_year_a |   max_year_a |   min_year_b |   max_year_b | perfect_time_separation   | time_separation_direction   |
|:-------------------------|:----------|:-----------------|------:|------:|:---------------------------------------------|:--------------------------------------------------|-------------:|-------------:|-------------:|-------------:|:--------------------------|:----------------------------|
| INFLATION_LEVEL          | HIGH      | LOW_OR_MODERATE  |     5 |     5 | 1983;1984;1987;1988;2022                     | 1987;1994;1999;2004;2015                          |         1983 |         2022 |         1987 |         2015 | False                     | OVERLAPPING_ERAS            |
| INFLATION_DIRECTION      | RISING    | FALLING_OR_FLAT  |     7 |     3 | 1984;1987;1994;1999;2004;2015;2022           | 1983;1987;1988                                    |         1984 |         2022 |         1983 |         1988 | False                     | OVERLAPPING_ERAS            |
| GROWTH_STATE             | STRONG    | WEAK             |     6 |     4 | 1984;1987;1988;1994;1999;2004                | 1983;1987;2015;2022                               |         1984 |         2004 |         1983 |         2022 | False                     | OVERLAPPING_ERAS            |
| YIELD_CURVE_STATE        | INVERTED  | POSITIVE         |     0 |    10 |                                              | 1983;1984;1987;1987;1988;1994;1999;2004;2015;2022 |          nan |          nan |         1983 |         2022 | False                     |                             |
| REAL_RATE_PROXY_STATE    | POSITIVE  | NONPOSITIVE      |     9 |     1 | 1983;1984;1987;1987;1988;1994;1999;2004;2015 | 2022                                              |         1983 |         2015 |         2022 |         2022 | True                      | A_ALL_BEFORE_B              |
| ENERGY_DIRECTION_STATE   | RISING    | FALLING_OR_FLAT  |     5 |     3 | 1987;1987;1999;2004;2022                     | 1988;1994;2015                                    |         1987 |         2022 |         1988 |         2015 | False                     | OVERLAPPING_ERAS            |
| NFCI_STATE               | TIGHT     | LOOSE_OR_AVERAGE |     2 |     8 | 1983;1988                                    | 1984;1987;1987;1994;1999;2004;2015;2022           |         1983 |         1988 |         1984 |         2022 | False                     | OVERLAPPING_ERAS            |
| USD_DIRECTION_DIAGNOSTIC | RISING    | FALLING_OR_FLAT  |     5 |     5 | 1994;1999;2004;2015;2022                     | 1983;1984;1987;1987;1988                          |         1994 |         2022 |         1983 |         1988 | True                      | B_ALL_BEFORE_A              |

## Interpretation

- USD bridge sign agreement: 95.74%.
- USD FIRST_HIKE support: 5 rising vs 5 falling/flat.
- Perfect chronological separation: True (B_ALL_BEFORE_A).
- Therefore the USD contrast is severely era-confounded in this event sample and cannot establish USD as a Gold driver.
- No state is ranked as dominant.
- No p-values/FDR are run; leave-one-leg-out sign stability remains a fragility diagnostic only.