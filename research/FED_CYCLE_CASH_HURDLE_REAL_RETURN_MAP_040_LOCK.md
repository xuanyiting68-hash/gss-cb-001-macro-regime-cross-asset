# FED-CYCLE-CASH-HURDLE-REAL-RETURN-MAP-040 — LOCK

Date frozen: 2026-09-27

## Objective

Build a phase-by-phase, event-matched opportunity-cost and purchasing-power map for the public Fed-cycle evidence stack.

This module asks:

1. Did a historical positive nominal endpoint also clear a matched mechanical cash hurdle?
2. Did it preserve purchasing power after matched CPI inflation?
3. How did those endpoint outcomes coexist with 12M path drawdown?
4. Which conclusions remain robust once asset-specific sample support is preserved?

This is **descriptive historical measurement**, not a forecast, allocation model, ranking, trading score, or causal monetary-policy study.

## Canonical upstream inputs

Public-safe repository outputs only:

- `results/fed_cycle_phase_clock_v1/PHASE_CYCLE_ASSET_METRICS.csv`
  - GOLD
  - SP500
  - NASDAQ
  - WTI
- `results/fed_cycle_cross_asset_expansion_v1/MARKET_PHASE_METRICS.csv`
  - DXY
  - BTC_USD
- `results/fed_cycle_long_treasury_proxy_bridge_035_v1/VUSTX_EXTENDED_PHASE_METRICS.csv`
  - VUSTX_LONG_TREASURY_PROXY
- `results/fed_cycle_listed_reit_proxy_bridge_036_v1/VGSIX_EXTENDED_PHASE_METRICS.csv`
  - VGSIX_REIT_PROXY
- `results/fed_cycle_cross_asset_expansion_v1/CASH_PHASE_METRICS.csv`
  - canonical 014 post-anchor 12M DFF cash benchmark for cross-check only

Fresh public FRED histories:

- DFF — Effective Federal Funds Rate
- CPIAUCSL — CPI for All Urban Consumers: All Items, seasonally adjusted

Fresh source bytes must be SHA256-registered. Raw histories are not committed.

## Frozen asset universe and evidence tiers

Fixed display order:

1. GOLD — CORE_SUPPORTED
2. SP500 — CORE_SUPPORTED
3. NASDAQ — CORE_SUPPORTED
4. WTI — CORE_SUPPORTED
5. DXY — CORE_SUPPORTED
6. VUSTX_LONG_TREASURY_PROXY — SUPPORTED_PROXY_DESCRIPTIVE
7. VGSIX_REIT_PROXY — LIMITED_PROXY_DESCRIPTIVE
8. BTC_USD — LIMITED_DESCRIPTIVE

No TLT/VNQ duplicate target rows are added because 035/036 already define the preferred proxy routing for historical-depth work.

No housing row is included because housing remains a separate 24M slow-moving DECLINE_24M object.

## Frozen phase universe

- FIRST_HIKE
- LAST_HIKE
- PAUSE_START
- FIRST_CUT

Realized phase labels are conditioning anchors, not identified monetary-policy shocks.

## Matched event window

For an anchor in calendar month `t`:

- baseline month = `t-1`
- endpoint month = `t+12`

This exactly follows the canonical monthly price-grid convention used by PHASE-CLOCK-004 for `ret_12m`.

### Matched CPI inflation

`inflation_matched = CPI(t+12) / CPI(t-1) - 1`

This is an **ex-post purchasing-power diagnostic using current-vintage CPI history**. It is not a real-time policy-information variable and not ALFRED PIT.

### Matched cash hurdle

To avoid treating the existing 014 post-anchor 12-month cash carry as exactly horizon-matched to the price endpoint, 040 constructs a new comparison benchmark on the same monthly grid:

- monthly average DFF for months `t ... t+12`
- mechanical monthly compounding:
  `matched_cash = Π_m (1 + DFF_m/100/12) - 1`

This is a mechanical opportunity-cost benchmark. It ignores taxes, fees, deposit-product spreads, reinvestment frictions and within-month timing.

The existing 014 `cash_carry_12m` over months `t+1 ... t+12` is retained only as `canonical_cash_014_post12` for timing-convention audit; it is not the primary hurdle in 040.

## Frozen event-level derived metrics

For each asset × phase × cycle event:

- `nominal_ret_12m` = canonical upstream `ret_12m`
- `mdd_12m` = canonical upstream path MDD
- `matched_cash_carry`
- `canonical_cash_014_post12`
- `matched_inflation`
- `asset_vs_cash = (1 + nominal_ret_12m) / (1 + matched_cash_carry) - 1`
- `real_asset_return = (1 + nominal_ret_12m) / (1 + matched_inflation) - 1`
- `real_cash_return = (1 + matched_cash_carry) / (1 + matched_inflation) - 1`

Flags:

- `nominal_positive`
- `beats_cash`
- `beats_inflation` (real asset return > 0)
- `beats_both`
- `positive_nominal_but_not_cash`
- `positive_nominal_but_not_inflation`

No risk-adjusted score, Sharpe ratio, utility score, rank, optimizer or allocation weight is permitted.

## Weighting

Preserve the upstream asset × phase `episode_weight`.

Do not reweight one long broad episode into multiple independent observations.

All phase summaries use weighted medians and weighted shares.

## Frozen summary outputs

For every asset × phase:

- n legs
- n broad episodes
- evidence tier
- weighted median nominal return
- weighted median matched cash carry
- weighted median matched inflation
- weighted median asset-vs-cash gap
- weighted median real asset return
- weighted median real cash return
- weighted median MDD
- weighted share nominal positive
- weighted share beats cash
- weighted share beats inflation
- weighted share beats both
- weighted share positive nominal but not cash
- weighted share positive nominal but not inflation

No sorting by performance magnitude.

## Primary descriptive questions

Q1. How often does a positive nominal endpoint fail the matched cash hurdle?
Q2. How often does a positive nominal endpoint fail to preserve purchasing power?
Q3. Does FIRST_CUT still look uniformly benign after cash, inflation and path risk are shown together?
Q4. Does high mechanical cash carry materially change interpretation around LAST_HIKE / PAUSE?
Q5. Do supported duration-proxy results remain positive after the hurdle adjustment?
Q6. How different are endpoint conclusions from path-risk conclusions?
Q7. Which apparent patterns disappear when limited-history BTC/REIT evidence is kept in its own tier?
Q8. How large is the timing-convention difference between matched cash and canonical 014 post12 cash?

These questions are descriptive; none authorizes a best asset or best phase conclusion.

## QC gates

Hard fail if:

- any upstream QC dependency used here is not PASS;
- any event has missing DFF or CPI for the frozen matched window;
- any event loses its canonical asset identity;
- any VUSTX pre-TLT history is relabeled TLT;
- any VGSIX pre-VNQ history is relabeled VNQ;
- any FRESX rejected 037 history enters the panel;
- any housing row is mixed into the 12M traded-asset panel;
- broad-episode weights fail their existing within-cell normalization;
- any new p-value, optimized threshold/horizon, forecast, current analog, asset ranking, best-phase label or trade recommendation is generated.

QC also records, without a pass/fail optimization target:

- median and max absolute difference between the new matched-grid cash hurdle and canonical 014 post12 cash;
- sample counts by evidence tier;
- current-vintage CPI boundary.

## Statistical status

No confirmatory p-value family is planned.

- causal status: NONE
- OOS status: NOT_A_FORECASTING_MODEL
- deployment status: NOT_DEPLOYABLE

## Interpretation boundary

A historical asset can have:

- positive nominal return,
- but fail cash;
- positive nominal return,
- but lose purchasing power;
- positive endpoint,
- yet still experience material MDD.

040 is designed to expose these distinctions without converting them into an investment recommendation.
