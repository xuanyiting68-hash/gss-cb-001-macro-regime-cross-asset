# FED-CYCLE-PROSPECTIVE-INPUT-TIMING-010 — Live Input Timing Audit Lock
Date: 2026-09-24
Status: **FROZEN BEFORE LIVE-TIMING EXECUTION**

## 1. Purpose

Audit whether the exact public-source input contract used by `FED-CYCLE-GOLD-OOS-008` can be transported into the append-only prospective architecture in `FED-CYCLE-PROSPECTIVE-SHADOW-009` **without observing any part of the target window before forecast issuance**.

This is an operational/timing audit. It does not evaluate forecast accuracy and cannot upgrade OOS-008 evidence.

## 2. Why this audit is required

OOS-008 was a historical episode-forward test. Its Gold features were built from a monthly Gold series sourced from the World Bank Commodity Markets Pink Sheet through `datasets/gold-prices`.

For forecast month M, OOS-008 uses:

- Gold 3M return ending M-1;
- Gold 6M return ending M-1;
- Gold 6M volatility ending M-1;
- real-time IPT based on M-2 / M-14 using a vintage no later than M-1.

The target is the next-6M Gold endpoint return from the M-1 monthly baseline through M+5.

For a strict prospective transfer, the forecast must therefore be issued **before month M begins**, while all frozen predictors must already be observable.

## 3. Gold source timing test

Primary Gold source contract remains the OOS-008 source:

- `datasets/gold-prices/data/monthly.csv`;
- modern observations sourced from World Bank Commodity Markets.

The audit queries recent GitHub commit history for that monthly file. For each newly introduced latest monthly observation P:

- identify the first observed commit timestamp that contains P;
- define the target-window start as the first calendar day of P+1;
- compute `release_lag_hours = first_seen_commit_timestamp - start(P+1)`.

Strict exact-transport requirement:

`release_lag_hours <= 0`

for every uncensored audited recent monthly introduction.

If recent monthly values first become available only after the next month begins, the exact OOS-008 Gold input contract is classified:

`SOURCE_TIMING_REPAIR_REQUIRED`.

No alternative Gold source is substituted inside this module.

## 4. RTDSM real-time IPT readiness

Use the same official Philadelphia Fed RTDSM IPT discovery/parser as VINTAGE-AUDIT-007.

Record:

- landing-page hash;
- workbook hash;
- last available vintage;
- current next-calendar-month information requirement;
- whether `RT_IPT_YOY` can be computed under the frozen M-2/M-14 rule using a vintage no later than M-1.

A current RTDSM shortfall is an operational dependency. It is not automatically treated as a permanent structural failure because the RTDSM file can update later in the month.

## 5. Current next-month dry readiness

At run date R:

- `current_month = month(R)`;
- `next_forecast_month = current_month + 1`.

This is a source-readiness probe only. It does **not** imply that the Fed-cycle eligibility gate has been met and does not issue a forecast.

The module reports whether the exact OOS-008 Gold and RT-IPT inputs would be available for that next month.

## 6. No outcome use

This module does not load:

- prospective Gold targets;
- B04-B07 forecast errors for re-optimization;
- any active-episode outcome.

No model is fit or refit.

## 7. Evidence interpretation

Possible statuses:

### EXACT_LIVE_TRANSPORT_READY
Only if the exact source contract can satisfy strict pre-target issuance timing.

### SOURCE_TIMING_REPAIR_REQUIRED
If the historical monthly source contract cannot supply required inputs before the target month starts.

### CURRENT_SOURCE_REFRESH_PENDING
For a current RTDSM lag that may resolve before an otherwise eligible forecast issue.

A negative readiness result is preserved. Thresholds or timing rules are not changed after execution.

## 8. If exact transport fails

The next module must be frozen separately before testing any replacement:

1. a legally/provenance-safe live Gold source bridge that reproduces the historical feature definition closely enough; or
2. an explicit publication-lag/target-timing amendment that is treated as a new prospective specification.

Neither path inherits OOS-008's positive OOS label automatically.

## 9. Hard QC

Fail the audit itself if:

- fewer than four uncensored recent Gold monthly introductions can be reconstructed;
- commit timestamps or monthly observation periods cannot be ordered;
- the official RTDSM workbook cannot be discovered/parsed;
- model outcomes or prediction errors are loaded;
- raw vendor/benchmark files are committed;
- any prospective prediction is created.

A successful QC run may legitimately conclude `SOURCE_TIMING_REPAIR_REQUIRED`.

## 10. Evidence boundary

**TIMING / DATA-PROVENANCE AUDIT ONLY / NO NEW FORECAST PERFORMANCE EVIDENCE / NOT CAUSAL / NOT DEPLOYABLE**
