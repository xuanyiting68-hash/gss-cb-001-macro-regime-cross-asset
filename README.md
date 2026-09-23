# GSS-CB-001 Macro Regime × Cross-Asset — Public Research & Media Lab

This is the **public companion repository** for the PandaAI / macro-regime / cross-asset research and evidence-based social-media workstream.

It is deliberately separated from the private academic-paper repository.

## Scope

This repository is for:

- audited public-facing macro-finance research summaries;
- Fed-cycle / drawdown / recovery research;
- Gold regime and cross-asset diagnostics;
- household-inflation, energy, crack-spread and commodity-turning-point research;
- reproducible public-source methods and derived tables;
- PandaAI research artifacts;
- social-media content whose claims are tied to an evidence status.

It is **not** the canonical repository for the unpublished Fed-reaction-function paper.

## Academic-paper firewall

Paper-specific identification work stays private. In particular, this public repository must not contain:

- exact unpublished staff FFR paths or meeting-level Tealbook/Greenbook extractions;
- the private frozen FOMC reaction panel;
- private/unpublished S6D.3 regression artifacts;
- restricted or non-redistributable source files;
- any private correspondence or personal information.

General research practices may be reused publicly: point-in-time discipline, source timing, evidence ledgers, falsification rules, multiple-testing control, OOS validation, and explicit causal-language boundaries.

See `docs/PAPER_FIREWALL.md`.

## Start here

1. Read `AGENTS.md`.
2. Read `docs/CURRENT_STATE.md`.
3. Read `docs/RESEARCH_PROTOCOL.md`.
4. Read `docs/EVIDENCE_LEDGER.csv`.
5. Read `docs/TRANSFER_AUDIT_20260924.md`.
6. Read `prompts/START_NEXT_CHAT.md` before continuing research in a new session.

## Public-safe research already imported

- `research/P0A_V3_PUBLIC_REAUDIT_PROTOCOL.md`
- `research/P0B_P0C_PUBLIC_STATUS.md`
- `research/FED_CYCLE_DRAWDOWN_RECOVERY_PREREG.md`
- `research/HICP_ENERGY_002_PUBLIC_CLOSEOUT.md`
- `research/ENERGY_REVERSAL_STATE_MACHINE_V2.md`
- `research/ENERGY_PRICE_WALKFORWARD_V1_LOCK.md`
- `research/ENERGY_PRICE_WF_001_CLOSEOUT.md`
- `research/ENERGY_PHYSICAL_WALKFORWARD_V1_LOCK.md`
- `research/ENERGY_PHYSICAL_WF_001_V1_1_TIMING_AMENDMENT.md`
- `research/ENERGY_PHYSICAL_WF_001_V1_1_CLOSEOUT.md`
- `research/ENERGY_FLOW_DECOMPOSITION_V2_LOCK.md`
- `research/ENERGY_FLOW_002_CLOSEOUT.md`
- `results/energy_price_wf_v1/`
- `results/energy_physical_wf_v1_1/`
- `results/energy_flow_v2/`
- `content/README.md`

The larger local social-content package is intentionally **not yet imported**. It should first pass a final claim/source audit so dated or exploratory statements cannot be separated from their evidence labels.

## Current public research tracks

### 1. Gold / regime audit
P0-A v3 re-audits the earlier Gold 8-regime work using excess returns relative to unconditional Gold drift, calendar-ordered HAC, null block bootstrap, factorial interactions, weekday robustness and FDR.

Current public status: **descriptively interesting / confirmatory evidence insufficient / not deployable**.

### 2. Point vs trend
P0-B asks whether smoothed macro trends systematically dominate point surprises.

Current public status: **primary hypotheses not supported**. Statistical detectability is kept separate from economic significance and tradability.

### 3. Fed × China / A-shares
P0-C exploratory Fed-only results are retained only as **quarantined / hypothesis-generating** because realized FOMC action is not an identified monetary-policy shock and the formal China-state conditioning layer is incomplete.

### 4. Fed-cycle risk paths
The public workstream studies not only endpoint returns but also maximum drawdown, time-to-trough, volatility, correlation shifts, and 50% / 100% recovery after First Hike, Last Hike, Pause, First Cut and Emergency Cut events.

### 5. Household inflation / energy
The energy workstream distinguishes crude-price shocks from downstream refined-product amplification and studies household fuel inflation, inflation expectations, Fed repricing and cross-asset risk paths.

### 6. Commodity turning points
The Commodity Reversal workstream tests transition states rather than the naive rule “price is high, therefore short.”

The first exhaustive 1990–2026 price/product walk-forward is complete: 13 de-clustered rollover events and **0/4 primary confirmed-vs-veto tests pass BH-FDR 10%**. The more promising descriptive use is a **false-relief veto / risk warning**, not a validated short signal.

The subsequent release-aware inventory/refinery layer also failed to establish downside timing: corrected P4A_DATA_ONLY n=3 and **0/4 tests pass FDR (q=1.00)**. A first stock-flow mechanism map then added product supplied, refinery inputs, production and imports; support remains too small for inference and no directional edge is established.

Current product implication: the energy stack is a **risk-state / mechanism engine**, not a buy/sell engine.

## Evidence labels

Every result should be tagged as one of:

- **DESCRIPTIVE**
- **ASSOCIATIONAL**
- **MECHANISM / STRUCTURAL CANDIDATE**
- **CAUSAL**
- **QUARANTINED / HYPOTHESIS-GENERATING**

And one of:

- **PASS**
- **PASS WITH BOUNDARIES**
- **MIXED**
- **NOT SUPPORTED**
- **NEED ROBUSTNESS**
- **NOT DEPLOYABLE**

## Public communication rule

No result becomes a social-media claim just because a raw p-value is small.

A public claim must state:

- what sample and horizon it refers to;
- whether it is descriptive or causal;
- whether multiple-testing correction was passed;
- whether it survived OOS where forecasting is claimed;
- important limitations.

## No investment advice

This repository is for research, education and reproducibility. Historical descriptive patterns and research hypotheses are not personalized investment advice and are not guarantees of future returns.
