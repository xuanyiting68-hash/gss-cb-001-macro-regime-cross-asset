# COMMODITY-HOUSEHOLD-CHAIN-042 — acquisition gate and frozen exploratory design

Locked 2026-09-27 before computation. Public companion only. Preserve all failed and unavailable comparisons.

## Availability and gaps

- Existing repo: EIA release-aware weekly energy prices/flows, de-clustered rollover events, prospective 2026-09-23 event; no farm-to-retail grain panel or point-in-time CBOT term structure.
- Official downloadable historical WTI daily spot, BLS monthly average white-bread and gasoline retail prices, USDA ERS farm-to-consumer spreads, current WASDE/BLS/EIA snapshots. Verify each endpoint, units and latest observation before use.
- Grain spot/cash bids, delivery-grade/location matched CBOT futures, historical curves and executable bid/ask, USDA archived vintages, CFTC timestamped positioning, inflation-expectation survey vintages and identified monetary-policy shocks are not assembled. Thus no futures basis, causal pass-through or net-profit test is possible in this milestone.
- Current-vintage data cannot be used as if known historically. Monthly BLS bread prices are released the next month. Daily WTI and weekly EIA must use release/observation distinctions.

## Frozen analysis prior to inspecting outcomes

1. Case years: 2008 (global demand collapse after high oil), 2020 (pandemic demand collapse), 2022 (Russia invasion and energy/grain supply/logistics), and 2026 (current context, incomplete). Selection is mechanism-motivated, not selected for gains. No claim that the event uniquely identifies a structural shock.
2. A reproducible *measurement illustration*, if complete BLS average-price history can be acquired: for calendar years 2008, 2020, 2022, compare January→December percentage changes in BLS national regular gasoline and white pan bread price per pound. Report within-year peak-to-following-trough drawdown and months to regain the January price, with censoring at December 2026. WTI monthly mean of available daily spot quotes uses same calendar years. No forward-looking strategy or inference from three selected years.
3. Complete-sample distribution: across all *complete calendar years* shared by the three available series, report median and 10th/90th percentile Jan→Dec changes, alongside three cases. Do not treat yearly observations as independent structural shocks. Coverage and missing data must be explicit.
4. Context-only economic links: crude/refined spread, farm wheat/flour/bread, corn/feed/ethanol and soybean/meal/oil; do not assign causal pass-through coefficients or lags without release-aware matched panels. ERS food dollar is an aggregate share, not a grain-to-bread elasticity.
5. Trading hypotheses are limited to three distinct pre-specified mechanisms: (H1) product-led energy squeeze; (H2) stocks/yield-revision grain tightness; (H3) demand-destruction disinflation with rate/FX confounds. Freeze candidate signals/confirmations/invalidations in the report, but label untested. A deployment claim requires separately acquired point-in-time futures curves and cash basis, rolling method, instrument costs, walk-forward OOS versus buy-and-hold/cash and repo baselines, and one BH-FDR family at q=10% across all predeclared assets/horizons.
6. QC: original URLs, observation timestamps, units, no future years, deterministic script, no private content, valid sequence of dates, all missing rows visible. All historical numbers here are descriptive; no p-values, FDR, OOS or profit inference.

## Acquisition amendment after first BLS/WTI run (no threshold or event change)

FRED lists IMF benchmark global monthly wheat/corn/soybean prices, USD/metric ton, updated 2026-08-17 through July 2026; these are neither U.S. local cash bids nor CBOT executable futures. Add the same preselected 2008/2020/2022 Jan→Dec path and complete 2007–2024 year distribution using those three series. This is an additional descriptive context panel, explicitly post-initial-run; do not use it to select or test a trading rule. IMF/FRED marks data copyrighted with attribution, so do not redistribute raw monthly series: publish only derived annual statistics and normalized case plots, with source and retrieval hashes.
