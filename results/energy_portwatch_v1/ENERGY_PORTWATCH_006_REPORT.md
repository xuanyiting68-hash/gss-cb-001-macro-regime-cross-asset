# ENERGY-PORTWATCH-006 — Prospective External Maritime Context

**PROSPECTIVE EXTERNAL CONTEXT / NO DIRECTIONAL OUTCOME CLAIM**

- QC: **PASS**
- event: ENERGY005_2026-09-23
- external supply-shock context present: **True**
- active relevant PortWatch disruptions: 2
- petroleum chokepoint traffic-stress flag: True
- maximum PortWatch data lag: 4 days

## Chokepoint snapshot

| portid      | portname             | latest_settled_date   |   data_lag_days |   rows |   mean7_total |   mean7_tanker |   prior90_total |   prior90_tanker |   mean30_total |   mean30_tanker |   prior_year_total |   prior_year_tanker |   ratio7_prior90_total |   ratio7_prior90_tanker |   ratio30_prioryear_total |   ratio30_prioryear_tanker | acute_transit_stress   | structural_transit_stress   | rerouting_elevated   |
|:------------|:---------------------|:----------------------|----------------:|-------:|--------------:|---------------:|----------------:|-----------------:|---------------:|----------------:|-------------------:|--------------------:|-----------------------:|------------------------:|--------------------------:|---------------------------:|:-----------------------|:----------------------------|:---------------------|
| chokepoint1 | Suez Canal           | 2026-09-20            |               4 |   2820 |      41.8571  |      17        |        41.1111  |         16.0556  |       40.8667  |        16.2333  |            38.5479 |             14.6219 |               1.01815  |                1.05882  |                 1.06015   |                  1.11021   | False                  | False                       | False                |
| chokepoint4 | Bab el-Mandeb Strait | 2026-09-20            |               4 |   2820 |      24.7143  |       6.57143  |        30.9222  |         10.2778  |       26.2667  |         7.5     |            33.474  |             11.4658 |               0.79924  |                0.639382 |                 0.784689  |                  0.654122  | False                  | False                       | False                |
| chokepoint6 | Strait of Hormuz     | 2026-09-20            |               4 |   2820 |       3.14286 |       0.571429 |         9.45556 |          4.07778 |        4.03333 |         1.16667 |            85.5288 |             48.1781 |               0.332382 |                0.140132 |                 0.0471576 |                  0.0242157 | True                   | True                        | False                |
| chokepoint7 | Cape of Good Hope    | 2026-09-20            |               4 |   2820 |      88.5714  |      16.1429   |        90.5444  |         18.8     |       87.5667  |        17.8333  |            89.4603 |             16.8904 |               0.978209 |                0.858663 |                 0.978833  |                  1.05583   | False                  | False                       | False                |

## Active relevant official disruptions

|   eventid | eventtype   | eventname        | htmlname                                  | alertlevel   | fromdate            | todate   |   severitytext | pageid                           |
|----------:|:------------|:-----------------|:------------------------------------------|:-------------|:--------------------|:---------|---------------:|:---------------------------------|
|   1000000 | OT          | RED SEA TENSIONS | Trade Disruptions in the Red Sea          | RED          | 2023-12-16 00:00:00 | NaT      |            nan | 573013af3b6545deaeb50ed1cbaf9444 |
|  10000004 | OT          | HORMUZ-26        | Trade Disruptions in the Strait of Hormuz | RED          | 2026-03-01 00:00:00 | NaT      |                | cc317ba850e34c4dadbead6f7b336fb1 |

This snapshot is recorded after the event release but before any frozen 4W/8W/13W prospective outcome is observed.
It is not used to retroactively relabel the historical 004 event panel.
