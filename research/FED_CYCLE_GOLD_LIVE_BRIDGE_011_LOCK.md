# FED-CYCLE-GOLD-LIVE-BRIDGE-011 — GC=F Feature-Transport Audit Lock
Date: 2026-09-24
Status: **FROZEN BEFORE BRIDGE EXECUTION**

## 1. Purpose

Test whether a same-month observable public market proxy can reproduce the **Gold input features** used by OOS-008 closely enough to be considered for a new prospective measurement specification.

This module is triggered by the negative result in INPUT-TIMING-010:

- the exact World Bank monthly Gold source arrives after the following target month has already begun;
- exact historical-source transport therefore fails strict pre-target issuance.

This module does not test forecast performance.

## 2. Candidate proxy

Candidate:

- Yahoo Finance public chart history for `GC=F`;
- interpreted as a continuous COMEX Gold futures proxy;
- daily close;
- raw JSON bytes are not committed.

This candidate is chosen because the repository already uses `GC=F` as an explicitly labeled futures proxy in FED-CYCLE-PATH-001.

It is **not** XAUUSD spot and is not assumed equivalent ex ante.

## 3. Reference series

Reference:

- pinned `datasets/gold-prices` monthly Gold series used by OOS-008;
- modern source: World Bank Commodity Markets;
- monthly Gold price represents the World Bank monthly benchmark series.

No revised alternative reference is selected after results.

## 4. Monthly proxy construction

For each calendar month:

- aggregate all valid `GC=F` daily closes by arithmetic mean;
- require at least 10 valid daily observations;
- no scaling or calibration to the World Bank series;
- no regression mapping;
- no outcome-based adjustment.

The arithmetic monthly mean is selected because the World Bank monthly Gold series is itself an average of daily benchmark rates.

## 5. Feature construction

For both reference and proxy monthly prices, identically compute:

- `RET_3M = P_t / P_{t-3} - 1`;
- `RET_6M = P_t / P_{t-6} - 1`;
- `VOL_6M` = sample standard deviation (ddof=1) of six monthly log changes ending at t.

These are the transport analogues of the lagged Gold predictors in OOS-008.

No Gold target return is loaded.

## 6. Frozen engineering-equivalence gates

The bridge receives:

`PROXY_FEATURE_BRIDGE_CANDIDATE`

only if **all** gates pass.

### Coverage

- at least 240 common feature-complete months.

### Level diagnostic

Not a model input, but required as a source sanity check:

- median absolute relative monthly-price gap <= 2.0%;
- 95th percentile absolute relative gap <= 5.0%.

### 3M return feature

- Pearson correlation >= 0.98;
- median absolute difference <= 1.5 percentage points;
- sign agreement >= 95%.

### 6M return feature

- Pearson correlation >= 0.98;
- median absolute difference <= 2.0 percentage points;
- sign agreement >= 95%.

### 6M volatility feature

- Pearson correlation >= 0.90;
- median absolute difference <= 0.006 in monthly-log-return standard-deviation units.

### Era stability

For each era with at least 24 complete observations:

- 2000-2009;
- 2010-2019;
- 2020-present;

both 3M and 6M return sign agreement must be >= 90%.

No threshold is changed after seeing results.

## 7. Why no p-values

This is an engineering transport audit, not a hypothesis-significance family.

The question is whether measurement disagreement is small enough under predeclared tolerances, not whether correlation differs statistically from zero.

No p-value or FDR family is used.

## 8. Interpretation

A pass means only:

**GC=F monthly-mean derived features are sufficiently close to the historical World Bank Gold features under this frozen engineering gate to justify a separately versioned prospective measurement specification.**

It does not mean:

- futures and spot are economically identical;
- OOS-008 has been revalidated using GC=F;
- M3 forecast performance transfers unchanged;
- a live trading model is validated.

A fail means the GC=F bridge is not supported under this frozen definition and must not be silently substituted.

## 9. Hard QC

Fail the audit itself if:

- fewer than 240 common feature-complete months;
- fewer than 10 daily proxy observations are used in an accepted month;
- duplicate daily dates remain;
- raw Yahoo JSON is committed;
- any OOS-008 target or forecast error is loaded;
- any calibration/regression map from GC=F to the World Bank series is fitted;
- bridge thresholds change after execution.

## 10. Evidence boundary

**DATA-TRANSPORT / MEASUREMENT-EQUIVALENCE AUDIT / NO FORECAST PERFORMANCE EVIDENCE / NOT CAUSAL / NOT DEPLOYABLE**
