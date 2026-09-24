# FED-CYCLE-GOLD-OOS-008 — Closeout
Date: 2026-09-24
Status: **PRELIMINARY OOS CANDIDATE / WEAK AND BENCHMARK-SENSITIVE / NOT CAUSAL / NOT DEPLOYABLE**

## 1. Question

VINTAGE-AUDIT-007 found a stronger within-cycle historical association between real-time industrial-production growth and next-6M Gold endpoint returns.

OOS-008 asks the harder question:

**does real-time IPT add genuine time-ordered forecasting value beyond Gold's own lagged history and simple policy-cycle age?**

## 2. Frozen OOS design

Target:

- Gold next-6M endpoint return only.

No random split.

Broad-episode forward chaining:

- train B01-B03 -> test B04;
- train B01-B04 -> test B05;
- train B01-B05 -> test B06;
- train B01-B06 -> test B07.

Thus:

- 4 independent future broad-episode test blocks;
- 119 OOS monthly prediction rows.

Training outcomes are required to end before each test episode starts.

QC confirms:

- 0 target-window overlap violations;
- 0 same/future-episode training violations;
- 0 hierarchical-weight violations;
- 0 Gold feature timing violations;
- 0 real-time vintage timing violations;
- 0 predictor-specification violations.

## 3. Frozen model family

### B0
Weighted historical mean.

### B1
Lagged Gold history:

- 3M lagged return;
- 6M lagged return;
- 6M lagged volatility.

### B2
B1 plus:

- months since FIRST_HIKE.

### M3
B2 plus:

- real-time IPT YoY.

### D4
B2 plus:

- current-revised INDPRO YoY.

D4 is diagnostic only and is not a historically deployable PIT model.

No regularization, hyperparameter search or feature selection is used.

## 4. Predeclared OOS gate

M3 receives `PRELIMINARY_OOS_CANDIDATE` only if:

1. M3 episode-equal MSE < B2;
2. M3 beats B2 on MSE in at least 3/4 OOS broad episodes;
3. M3 OOS R² versus B0 > 0.

Result:

**PASS.**

- M3 vs B2 MSE reduction: **21.27%**;
- M3 beats B2 in **3/4** OOS episodes;
- M3 OOS R² versus B0: **+3.38%**.

Frozen evidence label:

**PRELIMINARY_OOS_CANDIDATE.**

## 5. Full model comparison

Episode-equal OOS metrics:

| Model | MSE | MAE | OOS R² vs B0 |
|---|---:|---:|---:|
| B0 historical mean | 0.013865 | 0.088615 | 0.000 |
| B1 Gold history | 0.015100 | 0.097160 | -0.089 |
| B2 Gold + cycle age | 0.017016 | 0.102038 | -0.227 |
| **M3 + real-time IPT** | **0.013397** | **0.091047** | **+0.0338** |
| D4 + current INDPRO | 0.014374 | 0.094375 | -0.0367 |

### Immediate implication

The large 21.27% MSE improvement versus B2 must be interpreted in context:

**B2 itself performs substantially worse than the historical-mean benchmark.**

The more demanding comparison is M3 versus B0.

## 6. Benchmark-sensitivity audit

No models were refit in this post-run audit.

### M3 versus historical mean B0

- MSE improvement: **+3.38%**;
- MSE episode wins: **2/4**;
- MAE improvement: **-2.74%**;
- MAE episode wins: **1/4**.

Thus M3 only narrowly beats the historical mean on squared error and does not beat it on absolute error.

### M3 versus Gold-history B1

- MSE improvement: **11.28%**;
- MAE improvement: **6.29%**;
- episode wins: only **2/4** on both metrics.

### M3 versus current-vintage D4

- MSE improvement: **6.80%**;
- MAE improvement: **3.53%**;
- MSE wins: **3/4**;
- MAE wins: **3/4**.

This is useful evidence that the real-time vintage representation is more appropriate than the current-revised growth history for this forecasting experiment.

It is still based on only four future broad episodes.

## 7. Per-episode behavior

M3 versus B2 on MSE:

- B04: M3 wins;
- B05: M3 wins;
- B06: M3 loses;
- B07: M3 wins.

M3 versus B0 on MSE:

- wins only B05 and B07;
- loses B04 and B06.

The forecasting gain is therefore not uniform across future episodes.

## 8. Forecast coefficient stability

The standardized real-time IPT coefficient in M3 is negative in every expanding-window training fold:

- B04 test fold: -0.0494;
- B05: -0.0492;
- B06: -0.0497;
- B07: -0.0430.

The sign and approximate magnitude are unusually stable across the four training windows.

This is supportive of the mechanism candidate but does not overcome the limited OOS sample or benchmark sensitivity.

## 9. Calibration / bias

Episode-equal signed prediction bias for M3:

**-2.84 percentage points.**

By OOS broad episode:

- B04: -2.82pp;
- B05: -12.77pp;
- B06: +7.34pp;
- B07: -3.11pp.

Calibration is therefore unstable by episode.

Prediction range:

- realized next-6M Gold return: **-14.09% to +41.51%**;
- M3 prediction: **-14.71% to +12.64%**.

The linear model materially compresses the upside tail and does not capture the largest positive realizations.

## 10. What OOS-008 establishes

### DATA FACT

- time ordering and target-window separation pass hard QC;
- M3 passes the predeclared preliminary OOS gate;
- real-time M3 outperforms current-vintage D4 on aggregate MSE/MAE and in 3/4 episodes.

### PRELIMINARY OOS EVIDENCE

There is some evidence that real-time growth contains incremental information beyond the specific B2 Gold-history + cycle-age linear benchmark.

### IMPORTANT LIMITATION

The incremental value is **weak relative to the strongest naive benchmark**:

- only +3.38% MSE improvement versus historical mean;
- negative MAE improvement versus historical mean;
- only 2/4 MSE episode wins against B0.

Therefore the correct label is:

**PRELIMINARY OOS CANDIDATE / BENCHMARK-SENSITIVE.**

Not:

- validated predictor;
- robust trading edge;
- deployable model.

## 11. Causal status

None.

Industrial production may co-move with other macro/market states. OOS forecasting performance does not identify a causal mechanism.

## 12. Statistical status

No OOS p-value/FDR family is run.

Only four independent future broad episodes exist, making formal episode-level inference extremely coarse.

The frozen performance gate is not a significance test.

## 13. Deployment status

**NOT DEPLOYABLE.**

Missing before any deployment escalation:

- materially larger independent prospective sample;
- better calibration;
- robustness across loss functions;
- robustness to alternative predeclared market benchmarks;
- live/prospective data-pipeline validation;
- transaction/trading objective definition.

## 14. Research decision

Do **not** tune M3 further on B04-B07.

Those episodes are now used OOS evidence and should be treated as consumed for this specification.

The clean next step is prospective validation on genuinely new future data or a substantively new pre-frozen hypothesis, not another parameter search on the same four episodes.
