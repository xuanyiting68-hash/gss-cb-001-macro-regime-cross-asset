# Fed Cycle × Drawdown × Volatility × Recovery
## Pre-Registration / Compute Specification
Date: 2026-09-23
Status: NEXT RESEARCH — NOT YET A CONFIRMATORY RESULT

## Research question

Instead of asking only “what is the average return after a hike/cut?”, estimate the full risk path after monetary-policy cycle turning points:

- When does an asset peak or trough?
- How deep is maximum drawdown?
- How quickly does volatility expand or normalize?
- How do cross-asset correlations change?
- How long does 50% and 100% recovery take?
- How do these distributions vary across macro states and shock origins?

## Event ontology

Construct cycle events before viewing asset outcomes:

- FIRST_HIKE
- LAST_HIKE
- PAUSE_START
- FIRST_CUT
- EMERGENCY_CUT
- TIGHTENING_CYCLE_START / END
- EASING_CYCLE_START / END

Realized action labels are descriptive cycle markers, not structural monetary-policy shocks.

## Predetermined state taxonomy

Do not treat all hiking/easing cycles as homogeneous.

Candidate pre-event state dimensions:

- inflation level/trend;
- growth level/trend;
- labor-market tightness;
- real-rate level;
- yield curve;
- financial conditions;
- oil/commodity shock state;
- independently identified geopolitical supply shock.

## Assets

Minimum cross-asset universe:

- US equities
- Gold
- US 2Y and 10Y yields
- 10Y real yield
- broad USD
- WTI
- copper
- major China equity indices

Optional later: credit spreads, volatility indices, crypto and FX.

## Event-time horizons

Daily event time:
- approximately [-60, +252] market observations

Report:
- 1D
- 5D
- 20D
- 60D
- 120D
- 252D

Preserve the full path rather than only endpoint returns.

## Primary outcome families

### Return path
- cumulative return;
- abnormal/excess return versus asset-specific benchmark.

### Drawdown path
- event-relative and peak-to-trough drawdown;
- time to peak;
- time to trough;
- drawdown duration.

### Recovery
Record:
- time to 50% recovery;
- time to 100% recovery;
- right-censoring if recovery does not occur inside the window.

### Volatility
- realized volatility;
- downside semivolatility;
- tail-loss frequency.

### Correlation / diversification
Track before/after correlation shifts across:
- equities/bonds;
- equities/Gold;
- USD/Gold;
- oil/rates/inflation expectations;
- China/US equities.

## Statistical design

### Event-study layer
Estimate mean and median paths with uncertainty bands.

### Local-projection layer
Use identified monetary shocks when available:

`Δy(t+h) = α(h) + β(h) Shock(t) + γ(h) Shock(t)×State(t-1) + controls + error(t+h)`

Realized HIKE/HOLD/CUT remains descriptive.

### Survival layer
Use Kaplan–Meier and hazard models for:
- time to trough;
- 50% recovery;
- 100% recovery.

### Distributional layer
Study downside tails and quantiles, not only means.

## Evidence hierarchy

1. Descriptive cycle association.
2. Market-repricing association.
3. Identified monetary-policy shock.
4. State-dependent causal transmission under defensible identification.

Never upgrade level 1/2 evidence into level 3/4 language.

## Multiple testing

Predefine separate families for:
- return endpoints;
- drawdown;
- recovery;
- volatility;
- correlation.

Apply BH-FDR within the declared family.

## Investment-relevance gate

A historical pattern is investment-relevant only if:

- economically material;
- uncertainty is informative;
- not driven by one cycle;
- state definition is predetermined;
- robust to reasonable horizon/calendar choices;
- timing information was available in real time.

A historical average is never presented as a deterministic forecast.
