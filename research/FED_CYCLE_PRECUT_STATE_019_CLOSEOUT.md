# FED-CYCLE-PRECUT-STATE-019 — Closeout
Date: 2026-09-24
Status: **QC PASS / SIMPLE PRE-CUT STATE RULE NOT SUPPORTED / NEGATIVE DESCRIPTIVE RESULT / NOT OOS**

## 1. Purpose

Test whether simple states already observable before FIRST_CUT can distinguish later trough timing in the supported risk-asset set.

Outcome basket:
- SP500;
- NASDAQ;
- WTI.

Primary outcome objects:
- median FIRST_CUT trough month across the three assets;
- share of those three troughs occurring in months 7-12.

Pre-cut states:
- real-time RTDSM industrial-production YoY < 0;
- 10Y–2Y curve < 0;
- NFCI > 0.

No threshold was fit to the outcomes.

## 2. Timing and QC

Final v1.1 run:
- 8 mechanical cycles;
- 6 broad episodes;
- 8/8 rows have real-time RTDSM IPT;
- zero state-timing violations;
- zero 2026 live-cycle leakage;
- no p-values;
- late-trough threshold remains frozen at month 7.

QC: **PASS**.

## 3. v1.1 independent-support correction

The first run displayed cycle-level binary contrasts, but one broad episode can contain multiple nearby mechanical cycles.

v1.1 therefore classifies each binary state at the independent broad-episode level before judging support.

Support rule:
- >=3 broad episodes on both sides: SUPPORTED_BALANCED_DESCRIPTIVE;
- >=2 both sides: LIMITED_BINARY_DESCRIPTIVE;
- otherwise: INSUFFICIENT_STATE_VARIATION.

## 4. Real-time growth contraction — no variation

REALTIME_GROWTH_CONTRACTION:

- True broad episodes: **0**;
- False broad episodes: **6**.

All eight FIRST_CUT mechanical cycles in the usable sample had positive pre-cut real-time IPT YoY.

Therefore this binary state cannot explain cross-episode trough timing in the current sample.

Status:

**INSUFFICIENT_STATE_VARIATION.**

This is a negative design result, not evidence that real-time growth is irrelevant in general.

## 5. Yield-curve inversion — balanced support, no useful median separation

CURVE_INVERTED:

- True broad episodes: **3**;
- False broad episodes: **3**.

This is the only binary state with balanced descriptive support.

But the trough outcome does not separate:

### Not inverted
- median risk-3 trough month: **8**;
- median late-trough share: **1.0**;
- mean late-trough share: **0.852**.

### Inverted
- median risk-3 trough month: **8**;
- median late-trough share: **1.0**;
- mean late-trough share: **1.0**.

Thus a simple inverted/not-inverted flag does not distinguish the median late-trough clock here.

Status:

**SUPPORTED BALANCED DESCRIPTIVE / NO MATERIAL MEDIAN SEPARATION.**

## 6. NFCI tightness — insufficient independent support

FINANCIAL_CONDITIONS_TIGHT (NFCI > 0):

- True broad episodes: **1**;
- False broad episodes: **5**.

The one tight broad episode has an earlier trough profile, but one independent True episode is insufficient for a state rule.

Status:

**INSUFFICIENT_STATE_VARIATION.**

## 7. Composite PRE_CUT_STRESS_COUNT

Full broad-episode rank diagnostic:

### Median trough month
Spearman rho:
- **-0.636**.

All 6 leave-one-broad-episode correlations are defined and retain the negative sign:
- range about -0.865 to -0.304.

### Late-trough share
Spearman rho:
- **-0.707**.

Five of six leave-one-out correlations are defined and those finite correlations retain the negative sign.
One leave-one-out sample is undefined because the reduced outcome/state rank loses variation.

This negative direction is opposite the intuitive hypothesis that more pre-cut stress should imply later troughs.

## 8. Component sensitivity — composite result is NFCI-driven

Post-run component sensitivity is decisive.

For median trough month:

- full count: rho **-0.636**;
- drop growth: **-0.636**;
- drop curve: **-0.674**;
- drop NFCI: **-0.127**;
- curve-only: **-0.127**;
- NFCI-only: **-0.674**.

For late-trough share:

- full count: **-0.707**;
- drop NFCI: **+0.141**;
- curve-only: **+0.141**;
- NFCI-only: **-1.000**.

Because NFCI>0 occurs in only one independent broad episode, the strong negative composite ranking is largely a one-episode NFCI composition effect.

It is **not** promoted into a robust state relationship.

## 9. Research conclusion

The pre-cut simple-state hypothesis is **not supported as a usable historical rule**.

Specifically:

- real-time growth contraction has no cross-episode variation;
- yield-curve inversion has balanced support but no material median trough separation;
- NFCI tightness has only one True broad episode;
- the composite score's negative rank relation is dominated by that single NFCI-tight broad episode.

Therefore there is no basis to write:

`higher pre-cut stress count -> later trough`

or its opposite.

## 10. Product implication

Do not turn:
- curve inversion;
- NFCI sign;
- RT growth sign;
- or their naive additive count

into a PandaAI bottoming/timing score.

The more defensible product object remains:

`policy phase + contemporaneous observables + asset-specific historical risk clock + support strength + uncertainty`.

## 11. Next research decision

Do **not** fit a multivariate predictive model on only six broad FIRST_CUT episodes.

Highest-information next step, if this line is continued:

### FED-CYCLE-PRECUT-STRESS-LEVEL-020 — exploratory only

Use pre-anchor continuous stress levels already available before FIRST_CUT, especially:
- Baa–10Y spread level;
- VIX level where historically available;
- curve level;
- real-time RTDSM IPT growth.

Freeze the specification before reading the new contrasts.

Do not optimize thresholds.

Because the variable choice follows 018/019 results, classify 020 as:
**EXPLORATORY / MECHANISM-HYPOTHESIS**, not confirmatory forecasting.

If support remains too small or results remain composition-driven, stop this branch rather than adding variables.

## 12. Boundary

**NEGATIVE DESCRIPTIVE RESULT / PREDETERMINED STATES / REAL-TIME GROWTH / NO P-VALUES / NOT CAUSAL / NOT OOS / NOT DEPLOYABLE**
