# FED-CYCLE-FOUR-PHASE-INVESTOR-ATLAS-032 — LOCK

Date locked: 2026-09-26

## Purpose

Convert the existing QC-passed 021 cross-asset master synthesis into a decision-support / education knowledge atlas organized around the four canonical Fed-cycle phase anchors:

- FIRST_HIKE
- LAST_HIKE
- PAUSE_START
- FIRST_CUT

032 is a synthesis and interpretation module.

It does not estimate new returns, fit a forecasting model, choose a best asset, or create a trading rule.

## Authoritative inputs

Required upstream PASS:
- FED-CYCLE-CROSS-ASSET-MASTER-SYNTHESIS-021
- FED-CYCLE-PRECUT-STATE-019
- FED-CYCLE-PRECUT-STRESS-LEVEL-020

Primary files:
- results/fed_cycle_cross_asset_master_synthesis_v1/MASTER_ASSET_PHASE_MAP.csv
- results/fed_cycle_cross_asset_master_synthesis_v1/POLICY_RATE_CASH_CONTEXT.csv
- results/fed_cycle_cross_asset_master_synthesis_v1/PHASE_STRESS_CONTEXT.csv
- results/fed_cycle_cross_asset_master_synthesis_v1/RECOVERY_RISK_CLOCK_MAP.csv

## Evidence tiers

### CORE_SUPPORTED
- DXY
- GOLD
- NASDAQ
- SP500
- WTI

These may support descriptive four-phase comparisons.

### SUPPORTED_SLOW_MOVING
- US_HOUSE_PRICE

Must preserve its 24-month slow-moving path metric. Do not compare its DECLINE_24M directly with 12-month MDD.

### DIAGNOSTIC_ASIA
- HANG_SENG
- KOSPI
- NIKKEI_225
- SHANGHAI_COMPOSITE

Use only as diagnostic regional heterogeneity evidence.

### LIMITED_EXTENSION
- BTC_USD
- TLT
- VNQ

Do not promote limited-sample medians into stable cycle rules.

## Frozen research questions

032 must answer, from existing evidence only:

1. Does FIRST_HIKE historically imply negative 12-month U.S. equity returns?
2. What changes between FIRST_HIKE and LAST_HIKE?
3. What does PAUSE_START look like for equities, rates, cash and commodities?
4. Why is FIRST_CUT not equivalent to a market bottom?
5. Does easing begin only after Treasury yields fall?
6. Is cash carry already low by the pause?
7. How do Gold and DXY differ across phases?
8. How does WTI differ from equities across phases?
9. What does the stress layer say around FIRST_CUT?
10. Why must endpoint return and path risk be separated?
11. What do recovery clocks add beyond 12-month return?
12. What can and cannot be said about TLT?
13. What can and cannot be said about VNQ?
14. What can and cannot be said about Bitcoin?
15. Why is housing a different clock from traded assets?
16. Do Asian equity markets share one uniform Fed-cycle response?
17. Which apparent market rules are contradicted by the historical medians?
18. Which findings are strong enough for public education?
19. Which findings remain diagnostic or limited?
20. What information should PandaAI surface for each phase without making a recommendation?

## Four-phase signature rules

A phase signature is a descriptive bundle only.

For each phase, 032 may report:
- five core-asset 3M/6M/12M medians;
- path-risk metric/value;
- trough month;
- recovery clock where supported;
- DGS2 / DGS10 changes;
- mechanical cash carry context;
- Baa spread / VIX / copper stress context.

It may summarize cross-variable coexistence in prose.

It must not:
- call one phase the best time to buy;
- create a composite opportunity score;
- convert phase medians into expected returns;
- infer that realized Fed actions caused asset returns;
- assign probabilities to future outcomes.

## Frozen myth-audit categories

Allowed statuses:
- NOT_SUPPORTED_AS_SIMPLE_RULE
- DESCRIPTIVELY_SUPPORTED_WITH_BOUNDARIES
- MIXED_BY_ASSET_OR_PHASE
- LIMITED_SAMPLE
- DIAGNOSTIC_ONLY

No YES/NO investment recommendation.

## Important interpretation guardrails

### FIRST_HIKE
A negative 3-month equity median can coexist with a positive 12-month median. Do not summarize only one horizon.

### LAST_HIKE / PAUSE
Treasury-yield declines and still-high cash carry may coexist. Do not imply that declining market yields mean cash carry immediately disappears.

### FIRST_CUT
Positive median 12-month equity endpoints may coexist with materially larger MDD, later troughs, and higher stress. Do not label this a clean bullish easing regime.

### Rates
DGS2/DGS10 changes are yield changes in basis points, not bond total returns.

### Housing
US house price uses a 24-month slow-moving decline metric and cannot be visually or numerically ranked against 12-month traded-asset MDD.

### Limited assets
BTC/TLT/VNQ have short histories in the current design. Any large medians remain limited descriptive evidence.

## Frozen outputs

- CORE_FOUR_PHASE_ATLAS.csv
- RATES_CASH_FOUR_PHASE_ATLAS.csv
- STRESS_FOUR_PHASE_ATLAS.csv
- EXTENSION_ASSET_ATLAS.csv
- INVESTOR_QUESTION_REGISTRY.csv
- MYTH_AUDIT.csv
- FOUR_PHASE_SIGNATURES_ZH.md
- INVESTOR_KNOWLEDGE_SYNTHESIS_ZH.md
- PANDAAI_PHASE_EXPLANATION_SCHEMA.json
- FED_CYCLE_FOUR_PHASE_INVESTOR_ATLAS_032_REPORT.md
- QC.json

## QC gates

PASS requires:

1. exactly 20 core asset x phase rows;
2. exactly 12 rates/cash rows;
3. exactly 12 stress rows;
4. all eight extension/diagnostic assets retain all four phases where upstream provides them;
5. evidence tier/support labels preserved exactly;
6. no housing/traded-asset path-risk metric conflation;
7. exactly 20 investor questions;
8. every question links to explicit source rows/fields;
9. myth audit uses only frozen allowed statuses;
10. FIRST_CUT equity synthesis simultaneously mentions positive endpoint medians and elevated path risk;
11. rates synthesis distinguishes yield changes from bond returns;
12. limited BTC/TLT/VNQ claims retain LIMITED_SAMPLE;
13. Asia claims retain DIAGNOSTIC_ONLY;
14. no best-asset / best-phase output;
15. no current-analog ranking;
16. no deterministic bottom rule;
17. no expected-return forecast;
18. no new p-values/inference;
19. private-paper inputs = false;
20. causal status = NONE;
21. OOS status = NOT_A_FORECASTING_MODEL;
22. deployment status = NOT_DEPLOYABLE.

## Interpretation boundary

032 is an investor-education knowledge atlas.

It is intended to improve understanding of historical phase-dependent distributions and risk paths. It does not decide an allocation or trade for the user.
