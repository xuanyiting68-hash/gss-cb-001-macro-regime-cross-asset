# FED-CYCLE-VINTAGE-AUDIT-007 — Real-Time Industrial Production Revision Audit
Date: 2026-09-24
Status: **FROZEN BEFORE VINTAGE-OUTCOME EXECUTION**

## 1. Purpose

Audit the strongest remaining revision-sensitive macro state in the Fed-cycle Gold work:

- `INDPRO` growth state.

The original STATE-001 / STATE-PANEL-002 macro histories were explicitly labeled:

`RELEASE_LAG_AWARE_CURRENT_VINTAGE_NOT_STRICT_ALFRED_PIT`.

This module replaces current-vintage industrial production with a genuine real-time vintage series where feasible and tests whether the prior descriptive/associational conclusions are materially altered.

This is a robustness/revision audit, not a new signal search.

## 2. Official real-time source

Primary source:

Federal Reserve Bank of Philadelphia
Real-Time Data Set for Macroeconomists (RTDSM)

Variable:

- `IPT` — Industrial Production Index: Total;
- monthly vintages;
- official RTDSM page states vintage coverage from 1962:M11 to present.

The workbook is discovered from the official IPT landing page and downloaded at runtime.

Raw workbook bytes are hashed and not committed.

## 3. CPI boundary

The original inflation state uses:

- FRED/BLS `CPIAUCNS`;
- not seasonally adjusted CPI-U.

Philadelphia Fed `PCPI` is seasonally adjusted and is **not the same series definition**.

Therefore this module does **not** substitute PCPI for CPIAUCNS.

CPI status remains:

`RELEASE_LAG_AWARE_NSA_CPI_NOT_STRICT_REALTIME_VINTAGE`.

BLS routine seasonal-factor revisions apply to seasonally adjusted CPI indexes; this does not justify relabeling the original unadjusted CPI history as an ALFRED-style real-time vintage.

No CPI state result is upgraded by this module.

## 4. Conservative vintage timing

RTDSM monthly vintage headers identify a vintage month, not an exact release timestamp usable for every historical event.

To avoid intra-month look-ahead:

For an information date in calendar month M:

- select the latest IPT vintage whose vintage calendar month is **no later than M-1**;
- never use an event-month/current-panel-month vintage.

This is intentionally conservative.

## 5. Observation timing

Keep the previously frozen state observation rule unchanged.

For event/panel month M:

- target industrial-production observation month = M-2;
- comparison base = M-14.

`IP_YOY = IPT_vintage(M-2) / IPT_vintage(M-14) - 1`.

The two values must come from the **same selected real-time vintage**.

If either observation is unavailable in that vintage:

- mark the row unavailable;
- do not silently switch vintages or current history.

## 6. Event-level audit

Use the 10 frozen FIRST_HIKE rows in:

`results/fed_cycle_state_v1/STATE_EVENT_PANEL.csv`.

For each event record:

- current-vintage `INDPRO_YOY_LAG2`;
- current `GROWTH_STATE`;
- real-time IPT YoY;
- real-time growth state using the unchanged threshold:
  - STRONG if YoY >= 2%;
  - WEAK otherwise;
- numeric revision gap in percentage points;
- whether state label flips.

Outputs:

- exact event comparison table;
- number/share of state flips;
- max and median absolute YoY revision gap.

No outcome-dependent threshold changes.

## 7. Within-cycle panel audit

Use the existing 165-row panel:

`results/fed_cycle_state_panel_v2/MONTHLY_STATE_PANEL.csv`.

For every panel month:

- compute real-time IPT YoY with the conservative prior-month vintage rule;
- retain the existing Gold next-6M return and MDD outcomes.

Re-run the exact same estimator used in STATE-PANEL-002 for `INDPRO_YOY` only:

- mechanical-cycle fixed effects;
- each mechanical cycle total weight = 1;
- within-cycle RMS scaling;
- exact broad-episode sign-flip inference;
- mechanical-cycle sign-flip sensitivity;
- leave-one-broad-episode-out sign stability.

Two pre-existing outcome diagnostics:

1. `GOLD_FWD_6M_RET`;
2. `GOLD_FWD_6M_MDD`.

This does not create a new confirmatory family or supersede STATE-PANEL-002.

## 8. Same-sample current-vintage benchmark

For each real-time IPT test:

- estimate the current-vintage `INDPRO_YOY` coefficient on the **exact same complete-case rows**;
- report:
  - current coefficient/p;
  - real-time coefficient/p;
  - sign agreement;
  - magnitude difference.

This avoids attributing sample-composition changes to data revisions.

## 9. Support

A panel diagnostic is supported only if the real-time complete-case sample has:

- at least 5 mechanical cycles;
- at least 4 broad episodes.

Otherwise label:

`INSUFFICIENT_SUPPORT`.

## 10. Hard QC

Fail if:

- RTDSM source is not official Philadelphia Fed;
- selected vintage month is the same as or later than the event/panel month;
- M-2 or M-14 is replaced by another observation month;
- values used in one YoY come from different vintages;
- original 2% growth threshold changes;
- current-vintage benchmark uses a different row sample from the real-time estimate;
- event rows are duplicated;
- broad-episode/cycle weights violate the frozen estimator;
- raw RTDSM workbook is committed.

## 11. Evidence status

Allowed:

- **DATA FACT**
- **REVISION ROBUSTNESS RESULT**
- **ASSOCIATIONAL ROBUSTNESS DIAGNOSTIC**
- **NOT CONFIRMED**

Not allowed:

- causal language;
- forecasting claims;
- trading/deployment claims;
- using the audit to reopen threshold tuning.

## 12. Interpretation rule

If real-time IPT materially changes event labels or panel coefficients:

- downgrade current-vintage growth-state claims.

If it does not:

- classify the growth-state result as **revision-robust within the tested RTDSM timing rule**.

Either outcome remains non-causal and non-deployable.
