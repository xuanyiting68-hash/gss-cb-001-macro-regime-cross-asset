# Current state — 2026-09-24

## Repository role

This is the public PandaAI / macro-regime / cross-asset research and social-media companion.

The unpublished academic Fed-reaction-function paper remains in a separate private repository and is not mirrored here.

## Current public evidence state

### P0-A — Gold 8-regime statistical re-audit
Status: **DESCRIPTIVELY INTERESTING / CONFIRMATORY EVIDENCE INSUFFICIENT / NOT DEPLOYABLE**

Audited summary:
- 24 regime × horizon excess-return tests: 0/24 pass BH-FDR 10%;
- weekday robustness: 0/24;
- 21 non-intercept factorial tests: 0/21;
- null block bootstrap family: 0/24.

### P0-B — Point vs trend
Status: **PRIMARY HYPOTHESES NOT SUPPORTED**

Statistical detectability is kept separate from economic significance and tradability.

### P0-C — Fed × China / A-shares
Status: **QUARANTINED / HYPOTHESIS-GENERATING**

Existing Fed-only exploratory averages are not formal evidence because realized FOMC action is not an identified monetary-policy shock, the formal China predetermined-state layer is incomplete, and the exploratory testing family does not confirm a robust effect.

### Fed-cycle risk paths
Status: **DESCRIPTIVE / NEEDS LONGER HISTORY**

Research object: endpoint return, maximum drawdown, time-to-trough, volatility, correlation shifts and 50%/100% recovery after First Hike, Last Hike, Pause, First Cut and Emergency Cut events.

### Household inflation / energy
Status: **MECHANISM CANDIDATE / NOT A TRADING SIGNAL**

The public work distinguishes crude shocks from downstream refined-product amplification. Refined-product pressure is useful as a household-energy pressure monitor but is not yet a validated next-month cross-asset predictor.

### Commodity reversal / physical energy
Status: **RISK-STATE RESEARCH USEFUL / DIRECTIONAL EDGE NOT ESTABLISHED / NOT DEPLOYABLE**

#### Price/product layer

The exhaustive public-source monthly walk-forward covers 1990-04 to 2026-08.

QC:
- 437 complete common months;
- 13 de-clustered rollover events;
- 6 price/product-confirmed events;
- 7 false-relief veto events.

Primary result: **0/4 pass BH-FDR 10%**; adjusted q≈0.224.

The strongest descriptive use remains asymmetric: the price/product filter looks more promising as a **false-relief / no-short risk veto** than as a positive short signal.

#### Release-aware physical-stock layer

The first release parser was found to be invalid because it truncated the historical registry and produced impossible 2017→2026 mappings for some later events. That execution is quarantined.

The corrected event-scoped EIA release registry preserves:
- 13 frozen price events;
- 12 strict-PIT physical events;
- zero bad timing mappings.

Corrected P4A_DATA_ONLY support:
- 3 P4A events;
- 9 physical-veto events;
- 1 strict-PIT unavailable event.

Frozen four-test family: **0/4 pass BH-FDR 10%; q=1.00**.

Within the six completed strict-PIT PRICE_PRODUCT_CONFIRMED episodes, all three P4A_DATA_ONLY episodes had positive WTI returns at both 3M and 6M. This falsifies the narrow idea that the current inventory-normalization rule is a reliable falling-WTI confirmation. It does not establish the opposite rule because n is only 3.

#### Stock-flow mechanism map

FLOW-002 adds product supplied, refinery crude inputs, field production and crude imports.

Among strict-PIT price-confirmed episodes:
- complete flow support: 4;
- FLOW_DD: 0;
- FLOW_SN: 1;
- FLOW_MIXED: 3.

The single FLOW_SN episode was not bearish. 2008 was still FLOW_MIXED at the release-aware decision date before its large later collapse; 2022 and 2023 show that weaker product-supplied components can coexist with different subsequent WTI directions.

Current conclusion:

**stocks and flows improve mechanism understanding, but do not yet provide a validated directional timing signal.**

## Immediate public queue

1. Preserve the failed stock-only rule and FLOW-002 as negative/mechanism evidence; do not retune them.
2. Design a genuinely weekly/daily PIT commodity event engine to remove monthly-average timing limitations and increase event support.
3. Freeze an independent geopolitical/physical shock registry before any full P4A claim.
4. Expand Fed-cycle risk-path research to more historical cycles, including Gold drawdown/recovery paths.
5. Add provenance-safe public charts/tables and tie every social-media claim to the evidence ledger.
6. Keep paper-specific identification work behind the firewall.
