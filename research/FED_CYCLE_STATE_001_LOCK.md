# FED-CYCLE-STATE-001 — Predetermined-State Gold Heterogeneity Lock
Date: 2026-09-24
Status: **FROZEN BEFORE STATE-CONDITIONED GOLD OUTCOMES**

## 1. Purpose

Explain why Gold paths around mechanically defined Fed tightening anchors are heterogeneous without constructing regimes after seeing Gold outcomes.

Primary event: `FIRST_HIKE`.

Primary outcomes are inherited unchanged from the QC-passed long-history monthly Gold layer:

- clean +12M endpoint return;
- clean 24M maximum drawdown.

Secondary descriptive outcomes:

- +6M endpoint;
- +24M endpoint;
- MAE;
- MFE.

No outcome horizon, event date or Gold source is redefined here.

## 2. Event and outcome source

Event registry:

`results/fed_cycle_path_v1_1/FED_TIGHTENING_CYCLES.csv`

Gold outcomes:

`results/gold_long_history_monthly_v1/GOLD_MONTHLY_EVENT_METRICS.csv`

Primary FIRST_HIKE support before conditioning: 10 mechanical tightening legs.

The two 1987 legs remain separate because they are separate mechanical target-rate legs under the frozen cycle ontology. They are **not** claimed to be statistically independent macroeconomic experiments.

## 3. Information-timing tiers

A state can be dated before the event without being true vintage PIT data.

Therefore every state variable receives an explicit information class.

### Tier A — PREDETERMINED MARKET HISTORY

Historical market observations strictly dated before the event.

These are the closest to PIT in this public module because they are market-price/yield history rather than subsequently revised macro releases.

#### A1. Yield curve

Source: FRED `DGS10` and `DGS2`.

Use the last date strictly before the event on which both yields are observed.

`curve_bp = 100 * (DGS10 - DGS2)`

State:

- `INVERTED` if `curve_bp <= 0`;
- `POSITIVE` if `curve_bp > 0`.

No threshold tuning.

#### A2. Energy direction

Source: EIA/FRED `DCOILWTICO`.

Use the last valid WTI observation strictly before the event and the observation 126 valid WTI observations earlier.

`wti_126d_return = P_t / P_{t-126} - 1`

Binary state:

- `RISING` if return > 0;
- `FALLING_OR_FLAT` otherwise.

Additional fixed shock label:

- `SHOCK_UP` if return >= +20%;
- `SHOCK_DOWN` if return <= -20%;
- `NEUTRAL` otherwise.

The shock label is descriptive and is not substituted for the binary primary split after outcomes are seen.

### Tier B — RELEASE-LAG-AWARE CURRENT-VINTAGE MACRO HISTORY

These states use an observation month conservatively lagged far enough that the observation would normally have been released before the event, but the values are downloaded from the **current FRED vintage**.

They are therefore **not strict ALFRED PIT values**.

The project must not label them "real-time vintage".

#### B1. Inflation level

Source: BLS/FRED `CPIAUCNS` (monthly CPI-U, not seasonally adjusted).

For an event in month M0:

- state observation month = M-2;
- YoY inflation = CPI(M-2) / CPI(M-14) - 1.

State:

- `HIGH` if YoY > 3%;
- `LOW_OR_MODERATE` otherwise.

The 3% threshold is frozen before state-conditioned Gold outcomes.

It is a coarse CPI threshold and is **not** described as the Fed's inflation target.

#### B2. Inflation direction

Using the same release-lag convention:

- current YoY = YoY at M-2;
- comparison YoY = YoY at M-5.

State:

- `RISING` if current YoY > comparison YoY;
- `FALLING_OR_FLAT` otherwise.

#### B3. Growth state

Source: Federal Reserve/FRED `INDPRO`.

Use M-2 and M-14 current-vintage observations.

`ip_yoy = INDPRO(M-2) / INDPRO(M-14) - 1`

State:

- `STRONG` if YoY >= 2%;
- `WEAK` if YoY < 2%.

This is a fixed descriptive threshold, not a recession classifier.

#### B4. Ex-ante real-rate proxy

`real_rate_proxy = DGS10_last_pre_event - 100 * CPI_YOY_{M-2}`

State:

- `POSITIVE` if proxy > 0 percentage points;
- `NONPOSITIVE` otherwise.

This is a simple nominal-yield-minus-trailing-inflation proxy, not an identified expected real rate.

#### B5. Financial conditions

Source: Chicago Fed/FRED `NFCI`.

Use the last weekly NFCI observation strictly before the event.

State:

- `TIGHT` if NFCI > 0;
- `LOOSE_OR_AVERAGE` if NFCI <= 0.

Positive NFCI is defined by the source as tighter-than-average conditions and negative as looser-than-average.

Historical NFCI values are current-vintage factor estimates and can be revised; therefore this state is not labeled strict PIT.

## 4. Limited-support diagnostics

These variables are recorded but are not promoted to primary state-conditioned conclusions if support is insufficient.

### D1. Market 10Y TIPS real yield

Source: `DFII10`.

Use last observation strictly before event.

Coverage begins only in 2003, so expected FIRST_HIKE support is approximately 3.

State: positive versus nonpositive.

No generalization from this diagnostic to the 1980s/1990s cycles.

### D2. USD direction

Legacy source: `TWEXM`, weekly major-currency dollar index through 2019.

Modern source: `DTWEXAFEGS`, nominal advanced-foreign-economies dollar index.

For each source regime, direction is the sign of an approximately six-month own-series return:

- TWEXM: 26 weekly observations;
- DTWEXAFEGS: 126 valid daily observations.

The series are not level-spliced.

A bridge diagnostic over their overlapping history measures the share of common sampled weeks for which six-month return signs agree.

USD state-conditioned Gold summaries may be shown only if:

- bridge sign agreement >= 90%; and
- each state group has at least 3 FIRST_HIKE events.

Otherwise USD remains a row-level mechanism diagnostic.

This bridge threshold is frozen before Gold state-conditioned results.

## 5. Primary state family

The predeclared state variables are:

1. `INFLATION_LEVEL`
2. `INFLATION_DIRECTION`
3. `GROWTH_STATE`
4. `YIELD_CURVE_STATE`
5. `REAL_RATE_PROXY_STATE`
6. `ENERGY_DIRECTION_STATE`
7. `NFCI_STATE`

No other split may be added to the primary family after observing Gold outcomes.

## 6. Support rule

For a binary state contrast:

- both groups must have at least 3 FIRST_HIKE observations to be displayed as a state-conditioned comparison;
- otherwise status = `INSUFFICIENT_SUPPORT`.

Thresholds are not changed to rescue support.

## 7. Statistical status

STATE-001 is a **descriptive/associational mechanism map**, not a confirmatory causal test.

For each supported state × outcome contrast report:

- group n;
- group median;
- group IQR;
- median difference using a fixed lexical orientation stored in the state definition;
- leave-one-leg-out sign stability of the median difference.

No p-value is computed in STATE-001.

Reason: with only 10 mechanical legs, repeated binary splits create extremely low-powered and dependence-sensitive tests. Reporting a collection of raw p-values would create false precision.

Therefore:

- BH-FDR: **NOT RUN / NOT APPLICABLE TO THIS DESCRIPTIVE STATE MAP**;
- OOS: **NOT A FORECASTING MODEL**;
- causality: **NONE**;
- deployment: **NONE**.

A future confirmatory state model requires a separate lock, larger support and dependence-aware inference.

## 8. Leave-one-leg-out stability

For each supported state × primary outcome contrast:

- remove one tightening leg at a time;
- recompute the oriented median difference if both remaining groups still have n>=3;
- `LOO_SIGN_STABLE = TRUE` only if every computable leave-one-out median difference has the same non-zero sign as the full-sample difference.

This is a fragility diagnostic, not statistical significance.

## 9. Hard QC

Fail if:

- any state uses data dated on/after the event when strict-pre-event timing is required;
- CPI or INDPRO state month is later than M-2;
- Gold outcome table differs from the already committed monthly module;
- any primary split threshold is changed in code;
- a comparison with either group n<3 is presented as supported;
- limited-support DFII10 is promoted to long-history evidence;
- USD mixed-source direction is promoted without the frozen bridge audit;
- raw redistribution-uncertain source histories are committed.

## 10. Evidence language

Allowed:

- **DATA FACT**
- **DESCRIPTIVE RESULT**
- **ASSOCIATIONAL EVIDENCE** with explicit current-vintage/PIT limitations
- **MECHANISM CANDIDATE**
- **NOT YET VERIFIED**

Not allowed:

- "high inflation causes Gold to outperform after hikes";
- "this state predicts Gold" from this module;
- "real-time state" for current-vintage revised macro histories;
- trading/deployment claims.

## 11. Information-value rule

The module is useful even if no state cleanly separates Gold outcomes.

A null/fragile map would imply that simple binary macro regimes are not sufficient to explain historical tightening-cycle Gold heterogeneity and should be preserved as evidence against over-simple narratives.
