# FED-CYCLE-CASH-HURDLE-HORIZON-CROSSING-041 — LOCK

Date frozen: 2026-09-27

## Objective

Extend 040 from a single 12M endpoint comparison to a fixed 3M / 6M / 12M opportunity-cost horizon map.

041 asks whether an asset that eventually clears or fails the matched mechanical cash hurdle does so consistently across the three canonical endpoint horizons.

This is a **discrete-horizon descriptive map**.

It is not:
- a monthly crossover-timing estimator;
- a forecast;
- an optimizer;
- a causal monetary-policy study;
- an asset/phase ranking;
- an allocation or trading system.

## Upstream canonical dependencies

All inputs are already public-safe and frozen in the repository:

- 004 QC + `PHASE_CYCLE_ASSET_METRICS.csv`
  - GOLD
  - SP500
  - NASDAQ
  - WTI
- 014 QC + `MARKET_PHASE_METRICS.csv`
  - DXY
  - BTC_USD
- 035 QC + `VUSTX_EXTENDED_PHASE_METRICS.csv`
  - VUSTX_LONG_TREASURY_PROXY
- 036 QC + `VGSIX_EXTENDED_PHASE_METRICS.csv`
  - VGSIX_REIT_PROXY
- 014 `CASH_PHASE_METRICS.csv`
  - cash_carry_3m
  - cash_carry_6m
  - cash_carry_12m
- 040 QC + `EVENT_HURDLE_REAL_RETURN_PANEL.csv`
  - canonical 12M matched-cash result for exact reproduction
- `data/public/CASH_HURDLE_REAL_RETURN_EVENT_INPUTS_20260927.csv`
  - frozen official anchor-month FEDFUNDS values

No live external download is allowed in the canonical 041 run.

## Asset universe and evidence tiers

Fixed order and tiers are inherited exactly from 040:

1. GOLD — CORE_SUPPORTED
2. SP500 — CORE_SUPPORTED
3. NASDAQ — CORE_SUPPORTED
4. WTI — CORE_SUPPORTED
5. DXY — CORE_SUPPORTED
6. VUSTX_LONG_TREASURY_PROXY — SUPPORTED_PROXY_DESCRIPTIVE
7. VGSIX_REIT_PROXY — LIMITED_PROXY_DESCRIPTIVE
8. BTC_USD — LIMITED_DESCRIPTIVE

No TLT or VNQ duplicate target rows.
No FRESX.
No housing.

## Phase universe

- FIRST_HIKE
- LAST_HIKE
- PAUSE_START
- FIRST_CUT

Phase labels are conditioning anchors, not identified policy shocks.

## Frozen horizon grid

Exactly:

- 3M
- 6M
- 12M

No other endpoint horizon may be added after seeing results.

### Asset timing

Canonical 004-style asset returns use:

- baseline = anchor month t - 1
- 3M endpoint = t + 3
- 6M endpoint = t + 6
- 12M endpoint = t + 12

Thus the economic holding interval includes anchor month t.

### Canonical 014 cash timing

014 cash carry uses:

- 3M = t+1 ... t+3
- 6M = t+1 ... t+6
- 12M = t+1 ... t+12

### Matched 041 cash hurdle

For h in {3,6,12}:

`matched_cash_h = (1 + cash014_post_h) * (1 + FEDFUNDS_t/100/12) - 1`

This adds anchor month t and aligns cash to the same t-1 → t+h endpoint grid as the asset return.

No intra-month timing, tax, fees, deposit spread or transaction cost is modeled.

## Frozen event-level metrics

For each asset × phase × cycle and each h in {3,6,12}:

- nominal_ret_h
- canonical_cash_014_post_h
- matched_cash_h
- asset_vs_cash_h = (1 + nominal_ret_h) / (1 + matched_cash_h) - 1
- nominal_positive_h
- beats_cash_h
- positive_nominal_but_not_cash_h

## Frozen three-horizon pattern

Encode each event as a three-character bit pattern in 3M/6M/12M order:

- `1` = beats matched cash
- `0` = does not beat matched cash

Allowed patterns are exactly:

- 000
- 001
- 010
- 011
- 100
- 101
- 110
- 111

Derived descriptive labels:

- `NEVER_BEATS_OBSERVED_HORIZONS` = 000
- `BEATS_ALL_OBSERVED_HORIZONS` = 111
- `LATE_IMPROVEMENT_BY_12M` = 3M fails and 12M beats: 001 or 011
- `EARLY_ADVANTAGE_LOST_BY_12M` = (3M or 6M beats) and 12M fails: 010, 100 or 110
- `MIXED_NONMONOTONIC` includes 010, 101 or 110 when discussing non-monotonic observed-horizon states.

Also record:
- first_observed_beating_horizon ∈ {3M,6M,12M,NONE}
- last_observed_below_cash_horizon ∈ {3M,6M,12M,NONE}

These are **observed horizon labels**, not estimates of the actual crossover month between endpoints.

## Weighting

Preserve upstream broad-episode `episode_weight` exactly.

All asset × phase summaries use weighted medians and weighted shares.

Do not count multiple legs in one broad episode as independent full-weight observations.

## Frozen summary outputs

For each asset × phase:

- n legs
- n broad episodes
- evidence tier
- weighted median nominal return at 3M/6M/12M
- weighted median matched cash at 3M/6M/12M
- weighted median asset-vs-cash at 3M/6M/12M
- weighted share beats cash at 3M/6M/12M
- weighted share positive nominal but below cash at 3M/6M/12M
- weighted share 000
- weighted share 111
- weighted share late improvement by 12M
- weighted share early advantage lost by 12M

A separate pattern table reports all eight fixed patterns in fixed lexical order, including zero-weight patterns.

No performance sorting is allowed.

## Primary descriptive questions

Q1. How often is a positive 3M/6M/12M endpoint still below matched cash?
Q2. Which phase/asset cells have persistent 111 versus persistent 000 patterns?
Q3. How common is late improvement by 12M after failing cash at 3M?
Q4. How common is early cash-relative advantage that is lost by 12M?
Q5. Does the 040 12M interpretation hide materially different 3M/6M opportunity-cost paths?
Q6. Does FIRST_CUT endpoint/path-risk ambiguity also appear as horizon-dependent cash-relative performance?
Q7. Does VUSTX's supported proxy history show different 3M/6M/12M hurdle behavior around FIRST_HIKE vs later phases?
Q8. Do limited VGSIX/BTC samples remain visibly separated from supported evidence?

None authorizes a best asset, best phase or allocation conclusion.

## Hard QC gates

PASS requires:

1. upstream 004 / 014 / 035 / 036 / 040 QC all PASS;
2. exact asset identities and evidence tiers inherited from 040;
3. event panel row count = 232;
4. summary row count = 32;
5. horizon-long panel row count = 696;
6. exactly 37 canonical phase-cycle macro event keys;
7. no missing ret_3m / ret_6m / ret_12m;
8. no missing cash_carry_3m / 6m / 12m;
9. no missing anchor-month FEDFUNDS;
10. episode weights unchanged;
11. no FRESX / TLT / VNQ / housing leakage;
12. 12M matched cash reproduces 040 `matched_cash_carry` to <=1e-12 absolute;
13. 12M asset-vs-cash reproduces 040 `asset_vs_cash` to <=1e-12 absolute;
14. 12M beats-cash and positive-nominal-but-not-cash flags reproduce 040 exactly;
15. every pattern is in the frozen 8-pattern set;
16. no new p-values;
17. no optimized horizon;
18. no ranking / score / allocation;
19. no expected-return forecast;
20. no trade recommendation;
21. private-paper inputs = false.

## Statistical / deployment status

- causal status: NONE
- OOS status: NOT_A_FORECASTING_MODEL
- deployment status: NOT_DEPLOYABLE

## Interpretation boundary

041 can say that historical opportunity-cost status changed across the observed 3M/6M/12M endpoints.

It cannot say exactly when an unobserved crossover occurred between those endpoints.

It cannot convert a historical pattern into a current asset recommendation.
