# ENERGY-PHYSICAL-WF-001 v1.1 — Timing Amendment
Date: 2026-09-24
Status: FROZEN BEFORE FIRST PHYSICAL RESULT

## Why this amendment is necessary

The price-layer event file uses monthly average spot prices dated at the first day of each month. A monthly average for month t is not known on the first day of t.

Therefore, the original price-layer forward-return anchor is valid for descriptive historical comparison but is **not a real-time execution timestamp**.

Before running the physical extension, the timing convention is corrected.

This amendment is a pre-result implementation correction, not a response to observed physical results.

## Frozen event set

Do not regenerate or retune the 13 S3 price events from `ENERGY-PRICE-WF-001`.

The physical layer only classifies the already-frozen event set.

## Information dates

For each event:

- `s3_month` = frozen S3 month.
- `confirmation_month` = frozen price/product anchor month.
- `baseline_information_date` = last actual WPSR release date on or before the final calendar day of `s3_month`.
- `decision_date` = first actual WPSR release date after the final calendar day of `confirmation_month`.

Thus the physical decision is never back-dated to the monthly price timestamp.

## Release-date reconstruction

Primary historical release registry:

- EIA This Week in Petroleum archive rows for 2002–2025, which explicitly report **Release date** and **Week ending**.
- EIA WPSR current/previous-issue records for 2026.
- If an exact historical release date cannot be reconstructed from an official EIA record, strict-PIT status is `UNAVAILABLE` and that event is not used in the strict primary comparison.

Do not silently assume that every release was Wednesday.

## Weekly physical series

Official EIA weekly series:

- `WCESTUS1` — U.S. commercial crude stocks excluding SPR.
- `WGTSTUS1` — U.S. ending stocks of total motor gasoline.
- `WDISTUS1` — U.S. ending stocks of distillate fuel oil.
- `WPULEUS3` — U.S. refinery utilization of operable capacity.

Values are matched to their actual WPSR release dates through the release registry.

## Seasonal inventory benchmark

For each inventory series and each week-ending observation:

1. use only the five **complete prior calendar years**;
2. collect observations whose ISO week number is within ±1 of the current ISO week;
3. within each prior year, average available observations in that ±1-week window;
4. seasonal reference = mean across the prior-year contributions;
5. require at least 3 prior-year contributions.

Define:

`seasonal_gap = (inventory - seasonal_reference) / seasonal_reference`

Higher seasonal_gap = more inventory relative to normal = less physical tightness.

## Inventory improvement

For each of crude, gasoline and distillate:

`IMPROVING = seasonal_gap(decision) > seasonal_gap(baseline)`

No magnitude threshold is introduced in v1.1.

The count of improving inventory blocks is therefore fixed before seeing outcomes.

## Refinery state

At each baseline/decision observation, construct the same five-prior-year ±1 ISO-week seasonal reference set for refinery utilization.

Define:

- `REFINERY_HIGH` = current utilization > 90th percentile of the prior seasonal reference observations.
- `REFINERY_WORSENING` = decision is REFINERY_HIGH and decision utilization > baseline utilization.
- `REFINERY_DROP` = decision utilization - baseline utilization <= -5 percentage points.

`REFINERY_DROP` is a demand-destruction/outage diagnostic, not supply-normalization evidence.

## Data-only physical classification

Because a complete independently audited geopolitical/shipping shock-veto registry is not yet frozen, the first execution must use explicit `DATA_ONLY` labels.

### P4A_DATA_ONLY

Require all:

1. frozen price-layer classification = `PRICE_PRODUCT_CONFIRMED`;
2. strict PIT release mapping available;
3. at least 2 of 3 inventory blocks are IMPROVING;
4. `REFINERY_WORSENING = false`.

### PHYSICAL_VETO_DATA_ONLY

Strict-PIT event that does not satisfy P4A_DATA_ONLY.

### P4B_REFINERY_DROP_CANDIDATE

Separately flag if:

- frozen price layer is PRICE_PRODUCT_CONFIRMED; and
- `REFINERY_DROP = true`.

Do not pool P4B with P4A.

## Outcome timing correction

The physical classification is known only on `decision_date`.

Therefore the primary physical-extension WTI outcomes must start **after decision_date**, not from the monthly confirmation average.

Use daily public WTI spot data:

- execution anchor = first non-missing WTI daily observation on or after decision_date;
- 3M endpoint = nearest available WTI observation on or after decision_date + 3 calendar months;
- 6M endpoint = nearest available WTI observation on or after decision_date + 6 calendar months;
- 3M/6M short-side MAE = maximum WTI rise from the execution anchor inside the corresponding calendar window.

This timing-corrected outcome family supersedes the monthly-average anchor for the physical extension only. It does not overwrite the archived price-layer results.

## Primary family status

Because the geopolitical/shipping shock veto is not yet frozen, the first `DATA_ONLY` run is **exploratory / mechanism-building**, even if its four tests are numerically FDR-significant.

The four tests remain:

1. P4A_DATA_ONLY vs PHYSICAL_VETO_DATA_ONLY — WTI 3M
2. same — WTI 6M
3. same — short MAE 3M
4. same — short MAE 6M

BH-FDR 10% is reported.

No result may be called full P4A confirmation until the shock-veto registry is independently frozen and applied.
