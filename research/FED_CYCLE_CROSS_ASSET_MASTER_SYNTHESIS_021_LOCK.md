# FED-CYCLE-CROSS-ASSET-MASTER-SYNTHESIS-021 — LOCK

Date locked: 2026-09-25

## Purpose

Build a canonical, machine-readable synthesis layer over already-QC-passed public Fed-cycle modules for PandaAI, research handoff and evidence-linked educational/social-media production.

This module is an **integration layer, not a new empirical search**.

## Frozen evidence inputs

Only consume already-produced public derived outputs from:

1. PHASE-CLOCK-004
2. STRESS-LAYER-005
3. ASIA-CREDIT-DIAG-006
4. CROSS-ASSET-EXPANSION-014
5. RECOVERY-EXTENSION-015
6. SUPPORTED-RECOVERY-MAP-016
7. TOTAL-RISK-CLOCK-017
8. STRESS-TROUGH-ALIGNMENT-018
9. PRECUT-STATE-019
10. PRECUT-STRESS-LEVEL-020

No private-paper inputs are permitted.

## Canonical phase ontology

- FIRST_HIKE
- LAST_HIKE
- PAUSE_START
- FIRST_CUT

## Frozen output families

### A. MASTER_ASSET_PHASE_MAP

One row per price asset x phase where an upstream public module provides a phase summary.

Core supported assets:
- GOLD
- SP500
- NASDAQ
- WTI
- DXY

Extension assets:
- TLT
- VNQ
- BTC_USD
- US_HOUSE_PRICE

Diagnostic Asia assets:
- HANG_SENG
- NIKKEI_225
- KOSPI
- SHANGHAI_COMPOSITE

Fields retain upstream support status and provenance. Missing unsupported metrics remain null.

### B. POLICY_RATE_CASH_CONTEXT

Keep cash carry and Treasury-yield changes separate from price-return metrics.

Inputs:
- MECHANICAL_CASH_DFF
- DGS2
- DGS10

No cross-family ranking is allowed.

### C. PHASE_STRESS_CONTEXT

Retain phase-level:
- VIX
- BAA10Y_SPREAD
- COPPER

These are mechanism context, not causal or predictive signals.

### D. RECOVERY_RISK_CLOCK_MAP

Attach recovery metrics only when an upstream supported-recovery / total-risk-clock output exists.

Post-trough recovery and anchor-to-recovery clocks must remain distinct:
- post-trough KM 50% / 100% recovery months;
- anchor-to-50% / anchor-to-100% total clock months.

Do not silently fill limited/unsupported cells with estimates from another module.

### E. PANDAAI_RISK_DISTRIBUTION_REFERENCE

Machine-readable JSON projection of the canonical evidence map for educational product use.

Each record must expose:
- evidence class;
- support;
- source module(s);
- causal status;
- OOS status;
- deployment status;
- allowed-use note;
- forbidden-claim note.

## Frozen evidence language

Default classification:
- evidence_class = DESCRIPTIVE, except stress context = MECHANISM_CONTEXT;
- causal_status = NONE;
- oos_status = NOT_A_FORECASTING_MODEL;
- deployment_status = NOT_DEPLOYABLE.

Asia cells remain diagnostic even when internally adequate.
Limited TLT/VNQ/BTC cells remain limited.
019/020 negative results remain explicit guardrails against deterministic FIRST_CUT bottom-timing rules.

## Prohibited operations

This module must NOT:
- run new p-values or FDR procedures;
- search thresholds, transformations, interactions or composites;
- fit a multivariate timing score;
- rank assets as best/worst;
- infer causality from realized Fed anchors;
- convert historical medians into a trading signal;
- use B04-B07 consumed OOS-008 evidence to tune M3;
- import any private-paper Tealbook/staff path/reaction-function/S6D.3 material.

## QC gates

PASS requires:

1. only frozen upstream files are read;
2. all phase labels are in the canonical four-phase ontology;
3. all upstream support labels are preserved;
4. no p-value fields are generated;
5. recovery clocks are attached only by exact asset x phase keys;
6. duplicate canonical asset x phase rows = 0;
7. private-paper terms / paths = 0;
8. causal_status is NONE for all rows;
9. deployment_status is NOT_DEPLOYABLE for all rows;
10. FIRST_CUT deterministic timing guardrail is included in report/JSON.

## Interpretation boundary

021 answers:

> What has the public research already established descriptively about cross-asset path risk, recovery clocks and stress context across realized Fed-cycle phases?

It does **not** answer:

> What should an investor buy now, what will bottom next, or what did Fed policy causally do?

