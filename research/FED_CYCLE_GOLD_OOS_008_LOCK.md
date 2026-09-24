# FED-CYCLE-GOLD-OOS-008 — Real-Time Growth Incremental Forecast Audit
Date: 2026-09-24
Status: **FROZEN BEFORE OOS EXECUTION**

## 1. Purpose

Test the forecasting question that VINTAGE-AUDIT-007 deliberately did not answer:

**Does real-time industrial-production information add time-ordered out-of-sample value for next-6M Gold endpoint returns beyond simple Gold-history and policy-cycle-age benchmarks?**

This is a forecasting audit, not a causal design.

## 2. Target

Single primary target:

`GOLD_FWD_6M_RET`

from the existing monthly within-cycle panel.

No MDD target enters the primary OOS audit.

No alternative forecast horizon is tested.

## 3. Forecast population

Use the 165 monthly rows from:

`results/fed_cycle_state_panel_v2/MONTHLY_STATE_PANEL.csv`

merged one-to-one with real-time IPT from:

`results/fed_cycle_vintage_audit_v1/PANEL_REALTIME_IPT.csv`.

The existing broad episode IDs are frozen.

## 4. Time-ordered OOS design

No random train/test split.

Broad episodes are ordered chronologically:

- B01
- B02
- B03
- B04
- B05
- B06
- B07

The first OOS test episode is **B04**.

Thus every test fold has at least three earlier broad episodes available for training.

For test episode `Bg`:

- training data = all complete rows from broad episodes strictly earlier than `Bg`;
- test data = all rows in `Bg`;
- no rows from `Bg` enter model fitting;
- no later episodes enter model fitting.

Models are refit only when moving to the next broad episode.

Expected OOS episodes:

- B04;
- B05;
- B06;
- B07.

This is expanding-window, leave-future-episodes-out evaluation.

## 5. No outcome leakage

All predictors for panel month M must be observable before the first day of M.

### Gold own-history features

Use the same pinned monthly Gold source as prior modules.

For forecast month M:

- `GOLD_RET_3M_LAGGED = Gold(M-1)/Gold(M-4)-1`;
- `GOLD_RET_6M_LAGGED = Gold(M-1)/Gold(M-7)-1`;
- `GOLD_VOL_6M_LAGGED` = standard deviation of the six monthly log changes ending at M-1.

No M or later Gold price enters a predictor.

### Policy-cycle-age feature

`CYCLE_AGE_MONTHS` = number of calendar months from FIRST_HIKE month to M.

FIRST_HIKE has already occurred and is observable.

No LAST_HIKE or FIRST_CUT label is used because those can depend on future policy realizations.

### Real-time growth feature

`RT_IPT_YOY` from VINTAGE-AUDIT-007.

Its construction is frozen:

- observation M-2 relative to M-14;
- both values from the same RTDSM vintage;
- selected vintage no later than M-1.

## 6. Fixed model family

No hyperparameter search.

### B0 — Historical mean

Weighted expanding-window mean of the next-6M Gold return.

### B1 — Gold-history OLS

Predictors:

- GOLD_RET_3M_LAGGED;
- GOLD_RET_6M_LAGGED;
- GOLD_VOL_6M_LAGGED.

### B2 — Gold-history + policy-age OLS

B1 plus:

- CYCLE_AGE_MONTHS.

### M3 — Real-time growth model

B2 plus:

- RT_IPT_YOY.

### D4 — Current-vintage diagnostic

B2 plus:

- current-vintage `INDPRO_YOY`.

D4 is diagnostic only because current-revised INDPRO is not a deployable historical information set.

## 7. Model fitting

For B1/B2/M3/D4:

- linear regression with intercept;
- no regularization;
- no variable selection;
- predictors standardized using **training-fold weighted mean and weighted standard deviation only**;
- zero-variance training predictors are set to standardized zero;
- weighted least squares solved by least squares / pseudoinverse.

No model specification changes after OOS results.

## 8. Training weights

To prevent early multi-leg or long-duration episodes from dominating:

1. each training broad episode receives total weight 1;
2. within a broad episode, each mechanical cycle receives equal total weight;
3. within a mechanical cycle, rows share that cycle's weight equally.

The same hierarchy is used for evaluation weights inside each OOS episode.

Across the final OOS summary:

- each OOS broad episode receives equal total weight.

## 9. Primary OOS metric

Primary metric:

**episode-equal weighted MSE**.

For each model:

1. compute weighted MSE inside each test broad episode;
2. average the episode MSEs equally across B04-B07.

Primary incremental comparison:

`M3 vs B2`.

Report:

- episode-equal MSE;
- percentage MSE reduction of M3 relative to B2;
- count of OOS broad episodes where M3 MSE < B2 MSE.

## 10. Secondary OOS metrics

Report, without creating new success criteria:

- episode-equal MAE;
- episode-equal OOS R² versus B0;
- per-episode MSE/MAE;
- standardized RT_IPT coefficient in each training fold;
- D4 current-vintage diagnostic performance.

No directional trading accuracy metric is used.

## 11. Predeclared evidence gate

Because only four future broad episodes are available, the maximum evidence label is **PRELIMINARY_OOS_CANDIDATE**.

M3 receives that label only if all three conditions hold:

1. M3 episode-equal MSE < B2 episode-equal MSE;
2. M3 beats B2 on MSE in at least **3 of 4** OOS broad episodes;
3. M3 episode-equal OOS R² versus B0 > 0.

Otherwise:

`OOS_INCREMENTAL_VALUE_NOT_SUPPORTED`.

Even if the gate passes, do not call M3 a deployable forecasting model.

## 12. No significance fishing

No p-value/FDR family is run for the OOS metric.

With only four independent OOS broad episodes, formal episode-level inference is too coarse to justify a strong statistical claim.

The OOS gate is a predeclared forecasting-performance rule, not a significance test.

## 13. Hard QC

Fail if:

- any test row appears in its fold's training data;
- any later broad episode appears in training;
- fewer than 4 OOS broad episodes are evaluated;
- any Gold predictor uses M or later data;
- RT_IPT vintage timing differs from VINTAGE-AUDIT-007;
- train standardization uses test rows;
- model predictors change across folds;
- training/evaluation broad-episode weights fail their frozen hierarchy;
- D4 is presented as deployable PIT information;
- raw source histories are committed.

## 14. Interpretation

A passing result means:

**real-time growth showed preliminary incremental historical OOS forecasting value under this frozen episode-forward design.**

It does not mean:

- industrial production causes Gold returns;
- the model is production-ready;
- a live trading strategy is validated.

A failing result must be preserved and closes the forecasting escalation path for this specification unless a genuinely new ex-ante design is proposed.
