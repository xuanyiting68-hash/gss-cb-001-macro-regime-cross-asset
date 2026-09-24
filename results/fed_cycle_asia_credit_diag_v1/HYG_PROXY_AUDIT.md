# HYG price-proxy audit

**LIMITED-SUPPORT PRICE-MARKET CONTEXT / NOT OAS / NOT CAUSAL / NOT DEPLOYABLE**

| observable      | anchor      |   n_legs |   n_broad_episodes | support_status   |   weighted_median_ret_3m |   weighted_median_ret_6m |   weighted_median_ret_12m |   weighted_median_mdd_12m |   weighted_median_mdd_trough_month |   weighted_late_trough_share_7_12 |
|:----------------|:------------|---------:|-------------------:|:-----------------|-------------------------:|-------------------------:|--------------------------:|--------------------------:|-----------------------------------:|----------------------------------:|
| HYG_PRICE_PROXY | FIRST_CUT   |        3 |                  3 | LIMITED_SUPPORT  |               0.00802712 |               0.00785131 |                -0.0342111 |                0.111871   |                                  8 |                               1   |
| HYG_PRICE_PROXY | FIRST_HIKE  |        2 |                  2 | LIMITED_SUPPORT  |              -0.0942214  |              -0.116417   |                -0.113879  |                0.0726794  |                                  2 |                               0.5 |
| HYG_PRICE_PROXY | LAST_HIKE   |        2 |                  2 | LIMITED_SUPPORT  |              -0.027953   |               0.0328098  |                 0.0433326 |                0.00822657 |                                  3 |                               0   |
| HYG_PRICE_PROXY | PAUSE_START |        2 |                  2 | LIMITED_SUPPORT  |               0.0283354  |               0.0373233  |                 0.0675486 |                0.00822657 |                                  1 |                               0   |

The FRED ICE BofA OAS history is currently truncated to the most recent three years; HYG is retained separately as a price proxy and is not pooled with OAS.