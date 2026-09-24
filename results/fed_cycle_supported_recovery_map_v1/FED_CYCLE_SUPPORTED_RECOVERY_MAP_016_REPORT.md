# FED-CYCLE-SUPPORTED-RECOVERY-MAP-016

**SUPPORTED DESCRIPTIVE SYNTHESIS / NO NEW PRICE ESTIMATION**

- QC: **PASS**
- fully supported four-phase assets: DXY, GOLD, NASDAQ, SP500, WTI
- FIRST_CUT universally faster than PAUSE_START: **False**

## Four-phase supported recovery map

| asset   |   recovery50_first_hike |   recovery50_last_hike |   recovery50_pause_start |   recovery50_first_cut |   recovery100_first_hike |   recovery100_last_hike |   recovery100_pause_start |   recovery100_first_cut | fastest_full_recovery_phase   | slowest_full_recovery_phase   |   first_hike_minus_pause_full_months |   first_cut_minus_pause_full_months |
|:--------|------------------------:|-----------------------:|-------------------------:|-----------------------:|-------------------------:|------------------------:|--------------------------:|------------------------:|:------------------------------|:------------------------------|-------------------------------------:|------------------------------------:|
| DXY     |                       6 |                      4 |                        4 |                      5 |                       11 |                      12 |                         8 |                       6 | FIRST_CUT                     | LAST_HIKE                     |                                    3 |                                  -2 |
| GOLD    |                       4 |                      3 |                        1 |                      2 |                       19 |                       6 |                         5 |                      12 | PAUSE_START                   | FIRST_HIKE                    |                                   14 |                                   7 |
| NASDAQ  |                       2 |                      1 |                        1 |                      2 |                        8 |                       3 |                         3 |                       3 | LAST_HIKE                     | FIRST_HIKE                    |                                    5 |                                   0 |
| SP500   |                       2 |                      1 |                        2 |                      3 |                        4 |                       1 |                         3 |                       5 | LAST_HIKE                     | FIRST_CUT                     |                                    1 |                                   2 |
| WTI     |                       2 |                      5 |                        5 |                      3 |                        3 |                      19 |                         8 |                       9 | FIRST_HIKE                    | LAST_HIKE                     |                                   -5 |                                   1 |

## Main descriptive finding

PAUSE_START full recovery is faster than FIRST_HIKE for 4/5 fully supported assets.
Relative to PAUSE_START, FIRST_CUT full recovery is slower for 3, equal for 1, and faster for 1.

Therefore FIRST_CUT does not universally accelerate recovery.
Asset-specific recovery clocks remain necessary.
