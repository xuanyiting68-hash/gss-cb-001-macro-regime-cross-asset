# FED-CYCLE-PATH-001 — Long-History Cycle Path-Risk Lock
Date: 2026-09-24
Status: **FROZEN BEFORE ASSET-OUTCOME EXECUTION**

## 1. Purpose

Build a public-safe, reproducible long-history descriptive map of Fed tightening/easing cycle anchors and subsequent cross-asset path risk.

This module is deliberately descriptive. Realized target-rate actions are cycle markers, not identified monetary-policy shocks.

## 2. Policy-rate source and mechanical cycle construction

Primary policy-rate inputs are Federal Reserve target-rate series distributed through FRED:

- `DFEDTAR` for the single target rate before the target-range regime;
- `DFEDTARL` and `DFEDTARU` for the lower/upper target range; the public cycle marker uses the midpoint after the range begins.

A policy change is a non-zero change in the target/midpoint after numerical rounding tolerance.

A **tightening leg** is a consecutive run of positive target changes bounded by a negative target change or the edge of the source history.

A tightening leg enters the primary cycle registry only if:

- it has at least two positive target changes; and
- cumulative tightening is at least 50 bp.

These filters are fixed before asset outcomes are inspected.

For each qualifying tightening leg:

- `FIRST_HIKE` = first positive target change;
- `LAST_HIKE` = last positive target change before the next negative target change;
- `TIGHTENING_CYCLE_START` = `FIRST_HIKE`;
- `TIGHTENING_CYCLE_END` = `LAST_HIKE`;
- `FIRST_CUT` = first subsequent negative target change, if observed;
- `PAUSE_START` = first scheduled FOMC decision after `LAST_HIKE` and before `FIRST_CUT` at which the target/midpoint is unchanged.

An **easing leg** is the analogous consecutive run of negative target changes. `EASING_CYCLE_START` is its first cut and `EASING_CYCLE_END` is its last cut before the next hike.

`EMERGENCY_CUT` is a target/midpoint reduction of at least 25 bp that is not matched to a scheduled FOMC decision date within the timing tolerance used by the code. It is retained as a separate crisis-associated descriptive event and is not pooled with ordinary scheduled cuts without an explicit label.

Pre-1994 target changes are historical policy-target reconstructions rather than contemporaneously announced decisions; this is a mandatory interpretation boundary.

## 3. Scheduled-meeting registry

Scheduled FOMC decision dates are obtained from Federal Reserve historical meeting pages where available. Recent dates needed to complete modern-cycle pause classification may be supplied as an explicit, source-linked calendar supplement.

Conference calls are not scheduled meetings.

The meeting registry is constructed before any asset outcome is used.

## 4. Asset universe

### Price/index assets

- Gold spot, `XAUUSD` — Stooq public download, raw bytes not committed;
- S&P 500 cash index, `^SPX` — Stooq public download, raw bytes not committed;
- Nasdaq Composite, `NASDAQCOM` — FRED distribution; raw bytes not committed;
- WTI spot, `DCOILWTICO` — EIA/FRED;
- Nominal Broad U.S. Dollar Index, `DTWEXBGS` — Federal Reserve/FRED.

### Rate/inflation-compensation assets

- 2Y Treasury yield, `DGS2`;
- 10Y Treasury yield, `DGS10`;
- 10Y real yield, `DFII10`;
- 5Y breakeven inflation, `T5YIE`.

Coverage is allowed to differ by asset. No backfilling with future data and no silent splicing of non-equivalent series.

Stooq-derived raw market data are treated as redistribution-uncertain. Only provenance, hashes, normalized paths, derived event metrics and figures may be committed.

## 5. Event-time convention

For each asset/event:

- baseline = last valid observation strictly before the event date;
- event observation 1 = first valid observation on/after the event date;
- event-time path = observations `[-60, +252]` around the anchor where history exists;
- endpoint horizons = 1, 5, 20, 60, 120 and 252 valid asset observations.

This convention intentionally captures the event-day market move when the first post-event observation is the event date.

## 6. Price-asset path metrics

For Gold, S&P 500, Nasdaq, WTI and broad USD:

- cumulative return path from the pre-event baseline;
- endpoint returns at 1/5/20/60/120/252 observations;
- event-relative minimum return (MAE for a long exposure);
- event-relative maximum return (MFE);
- peak-to-trough maximum drawdown;
- time to peak;
- time to trough;
- annualized realized volatility at 20/60/120/252 observations;
- downside semivolatility at the same horizons;
- daily tail-loss frequency, defined as share of post-event daily returns below the pre-event 5th percentile estimated from the preceding 252 valid observations when at least 126 are available.

## 7. Recovery definition

Recovery is measured from the trough of the maximum peak-to-trough drawdown.

- 50% recovery = first post-trough observation that regains half the price distance from trough to the pre-drawdown peak;
- 100% recovery = first post-trough observation that regains the pre-drawdown peak;
- recovery search horizon = 756 valid observations after the trough;
- if the threshold is not reached inside the available/search window, the duration is right-censored.

If no positive peak-to-trough drawdown exists, recovery is marked not applicable rather than zero.

## 8. Rate-level metrics

For DGS2, DGS10, DFII10 and T5YIE:

- endpoint change in basis points at 1/5/20/60/120/252 observations;
- minimum and maximum event-relative bp excursion;
- time to minimum and maximum;
- realized volatility of daily bp changes at 20/60/120/252 observations.

Drawdown/recovery language is not applied to yield levels.

## 9. Gold priority outputs

Gold receives additional public-safe outputs:

- one row per cycle anchor with peak, trough, MDD, MAE/MFE, volatility and recovery metrics;
- normalized cycle-path figure for `FIRST_HIKE`;
- highlighted 2015 and 2022 `FIRST_HIKE` paths inside the same frozen framework;
- no hand-selected alternative windows for those two episodes.

The selected long-history Stooq series is a daily spot proxy; OHLC raw data are not redistributed.

## 10. Statistical status and multiple testing

`FED-CYCLE-PATH-001` is a **descriptive foundation module**, not a confirmatory causal test.

The runner reports distributions, quantiles, support, censoring and uncertainty-oriented summaries but does not use raw p-values to declare a cycle rule.

If later confirmatory testing is added, the following families are frozen separately:

1. endpoint-return family;
2. drawdown/adverse-excursion family;
3. recovery/survival family;
4. volatility/tail family;
5. correlation/diversification family.

BH-FDR is applied within a declared family. Events from the same cycle are never treated as independent replicates across anchor types. Overlapping-return inference must be dependence-aware.

## 11. Evidence boundary

Allowed language:

- **DATA FACT** for source/timing facts;
- **DESCRIPTIVE RESULT** for historical path distributions;
- **ASSOCIATIONAL EVIDENCE** only when an explicit statistical association is evaluated.

Not allowed from this module:

- “Fed hikes cause Gold/stocks to rise/fall”;
- structural monetary-policy claims;
- deterministic timing rules;
- deployment/trading claims.

OOS status: **NOT A FORECASTING MODEL / OOS NOT APPLICABLE TO THE DESCRIPTIVE FOUNDATION**.

## 12. QC gates

Hard fail if:

- policy registry has duplicate dates;
- target-range lower bound exceeds upper bound;
- no qualifying tightening cycles are found;
- Gold or S&P 500 has no usable observations around any qualifying cycle;
- event metrics violate internal identities (for example MDD < 0 or recovery time precedes the trough);
- a committed raw redistribution-uncertain Stooq file is created.

Soft warnings are preserved for short asset coverage, unavailable pause dates and right-censored recoveries.

