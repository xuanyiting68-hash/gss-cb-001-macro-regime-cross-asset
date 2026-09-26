# FED-CYCLE-GOLD-MECHANISM-DECOMPOSITION-033 — LOCK

Date locked: 2026-09-26

## Purpose

Build a public-safe evidence map for Gold across Fed-cycle states and macro/market mechanisms.

The module asks:

> In this research design, what evidence actually supports or fails to support the common stories that Gold is driven by inflation, real yields, the U.S. dollar, growth weakness, energy shocks, or financial stress?

033 does not search for a profitable trading rule and does not force a single dominant driver.

## Authoritative repository inputs

Required PASS:
- FED-CYCLE-STATE-001
- FED-CYCLE-STATE-PANEL-002
- FED-CYCLE-PHASE-CLOCK-004
- FED-CYCLE-STRESS-TROUGH-ALIGNMENT-018
- FED-CYCLE-FOUR-PHASE-INVESTOR-ATLAS-032

Files:
- results/fed_cycle_state_v1/STATE_CONTRASTS.csv
- results/fed_cycle_state_v1/STATE_LOO_STABILITY.csv
- results/fed_cycle_state_v1/USD_STATE_CONTRASTS.csv
- results/fed_cycle_state_panel_v2/PRIMARY_TESTS.csv
- results/fed_cycle_state_panel_v2/SECONDARY_DIAGNOSTICS.csv
- results/fed_cycle_state_panel_v2/USD_ROBUSTNESS_AUDIT.csv
- results/fed_cycle_cross_asset_master_synthesis_v1/MASTER_ASSET_PHASE_MAP.csv
- results/fed_cycle_stress_trough_alignment_v1/SUPPORTED_TIMING_PAIRS.csv

## External literature role

External literature is contextual, not an upstream empirical input.

The frozen literature registry may include:
- Baur & Lucey (2010): hedge vs safe-haven definitions and short-lived safe-haven evidence;
- Baur & McDermott (2010): international heterogeneity in Gold safe-haven behavior;
- Erb & Harvey (2013): practical-horizon inflation-hedge skepticism;
- Baur (2011): Gold properties can change between simple and multivariate models; USD/commodity relations matter;
- Apergis et al. (2019): real-rate/Gold relationships can be regime-dependent and need not have the textbook inverse sign.

Literature context must never overwrite repository results.

## Frozen mechanism families

1. INFLATION_LEVEL
2. INFLATION_DIRECTION
3. GROWTH_STATE
4. ENERGY_DIRECTION
5. USD_DIRECTION
6. REAL_RATE_PROXY
7. DFII10_REAL_YIELD
8. NFCI_FINANCIAL_CONDITIONS
9. STRESS_TIMING
10. FED_PHASE

## Evidence statuses

Allowed:
- SUPPORTED_DESCRIPTIVE
- SECONDARY_DIAGNOSTIC
- INSUFFICIENT_SUPPORT
- NO_STABLE_ASSOCIATION
- LITERATURE_CONTEXT

No mechanism ranking score is allowed.

## Frozen interpretation rules

### Inflation
Keep inflation level and inflation direction separate.

A high inflation level and rising inflation are not the same state and may have different Gold associations.

### Real yields
Do not state that the repository proves an inverse real-yield/Gold relation.

- event-level REAL_RATE_PROXY_STATE lacks adequate support;
- monthly REAL_RATE_PROXY is secondary diagnostic only;
- actual DFII10 has only three broad cycles in the current panel and is INSUFFICIENT_SUPPORT.

External literature may be cited to show that empirical real-rate/Gold relations are regime-dependent.

### USD
Keep the counterintuitive repository diagnostic.

- event-level USD_DIRECTION_DIAGNOSTIC and monthly USD_6M_RET show positive-oriented Gold associations in this design;
- the monthly full-sample USD row has an unadjusted exact p-value but no secondary-family FDR survivor;
- source-era restrictions weaken precision;
- therefore USD remains a mechanism candidate, not a stable driver law.

Do not delete this result because it conflicts with common market intuition.

### Stress / safe haven
Gold's stress timing must be separated from U.S.-equity stress timing.

At FIRST_CUT:
- Gold troughs can precede Baa/VIX stress peaks;
- this is compatible with Gold behaving differently during stress;
- it does not establish a real-time safe-haven trading signal.

### Fed phase
Fed phase is a conditioning label, not a causal Gold shock.

## Frozen outputs

- GOLD_MECHANISM_EVIDENCE_MATRIX.csv
- GOLD_PHASE_PROFILE.csv
- GOLD_FIRST_HIKE_STATE_CONTRASTS.csv
- GOLD_MONTHLY_SECONDARY_DIAGNOSTICS.csv
- GOLD_STRESS_TIMING_MAP.csv
- GOLD_MECHANISM_LITERATURE_REGISTRY.csv
- GOLD_MECHANISM_CLAIM_REGISTRY.csv
- GOLD_MECHANISM_SYNTHESIS_ZH.md
- GOLD_MECHANISM_MYTH_AUDIT.csv
- PANDAAI_GOLD_MECHANISM_SCHEMA.json
- FED_CYCLE_GOLD_MECHANISM_DECOMPOSITION_033_REPORT.md
- QC.json

## QC gates

PASS requires:

1. all four Gold phase rows preserved;
2. supported FIRST_HIKE state contrasts copied exactly;
3. LOO stability preserved for supported event-state contrasts;
4. monthly secondary diagnostics preserve their multiplicity status;
5. USD full-sample secondary diagnostic is not promoted to a confirmed driver;
6. DFII10 remains INSUFFICIENT_SUPPORT;
7. REAL_RATE_PROXY does not become a textbook inverse relation claim;
8. inflation level and direction remain separate;
9. Gold stress-timing rows for Baa/Copper/VIX preserved;
10. safe-haven interpretation remains conditional and non-deployable;
11. literature claims are clearly tagged LITERATURE_CONTEXT;
12. no mechanism winner/ranking;
13. no multivariate score;
14. no expected-return forecast;
15. no trading signal;
16. no new p-values beyond copied upstream values;
17. private-paper inputs = false;
18. causal status = NONE;
19. OOS status = NOT_A_FORECASTING_MODEL;
20. deployment status = NOT_DEPLOYABLE.

## Interpretation boundary

033 answers which Gold stories are supported, contradicted, limited, or unresolved within the public evidence stack.

It does not decide whether to buy or sell Gold.
