# Public research and reproducibility protocol

## Evidence classes

Every claim must be classified as:

- **DESCRIPTIVE**
- **ASSOCIATIONAL**
- **MECHANISM / STRUCTURAL CANDIDATE**
- **CAUSAL**
- **QUARANTINED / HYPOTHESIS-GENERATING**

## Evidence gates

Where relevant, a result should pass:

1. provenance/schema QC;
2. point-in-time / timing validity;
3. implementation audit;
4. inference;
5. multiple-testing correction;
6. economic magnitude;
7. robustness;
8. time-ordered OOS;
9. deployment realism.

Do not jump from a raw coefficient or chart to a trading claim.

## Time-series rules

- No random train/test split for forecasting.
- No future information in state classification.
- Release-sensitive macro data must use information available at the relevant time.
- Revised history cannot silently replace vintage data.
- Overlapping forward returns require dependence-aware inference.
- Cluster events so one long episode is not counted many times.

## Monetary-policy rules

- HIKE/HOLD/CUT is an action label, not a structural monetary-policy shock.
- Do not claim Fed causality from realized action comparisons alone.
- Separate target, path and information components when identification permits.
- A HOLD does not imply policy was inactive in every dimension.

## Commodity / energy rules

- Separate upstream crude shocks from downstream product amplification.
- Distinguish quantity loss, rerouting cost and risk-premium channels where possible.
- Label unmatched product-minus-crude measures as proxies.
- High price alone is not a reversal/short signal.
- Supply normalization and demand destruction are different mechanisms.
- False relief / renewed physical pressure must remain a veto state.

## Gold rules

Gold should not be treated as a one-variable inflation hedge.

Candidate channels include:
- real yields;
- USD;
- inflation compensation;
- growth/risk state;
- safe-haven demand;
- liquidity/policy path.

When testing incremental regime information, compare conditional results with unconditional Gold drift.

## Statistics

- Predeclare testing families for confirmatory work.
- Report raw p and adjusted q where multiple testing matters.
- Report effect size, uncertainty, support and economic magnitude.
- Preserve nulls and failed hypotheses.
- Do not select horizons or thresholds after inspecting significance.
- Reproducing the same code output does not automatically validate the statistical question.

## Forecasting and deployment

A forecasting claim requires walk-forward OOS and benchmark comparison.

A deployment claim additionally requires realistic timing, costs/slippage where relevant, turnover, max adverse excursion, drawdown and a frozen position/risk rule.

## Public communication

Where material, state:
- sample period;
- horizon/event definition;
- descriptive vs causal status;
- FDR/OOS status;
- important limitations.

Avoid unsupported language such as “this proves,” “the strategy works,” or causal claims that the design cannot identify.
