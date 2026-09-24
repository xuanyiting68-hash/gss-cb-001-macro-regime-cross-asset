# FED-CYCLE-STATE-PANEL-002 — Closeout
Date: 2026-09-24
Status: **QC-PASSED / PRIMARY ASSOCIATIONS NOT CONFIRMED / USD SECONDARY MECHANISM CANDIDATE ONLY / NOT DEPLOYABLE**

## 1. Purpose

STATE-PANEL-002 upgrades the 10-row FIRST_HIKE state cross-section into a within-cycle monthly panel.

It asks whether changes in macro/market states inside the same mechanical tightening leg are associated with subsequent Gold path risk.

It does not identify monetary-policy causality or a structural Gold driver.

## 2. Design

Panel:

- 165 monthly rows;
- 10 mechanical tightening legs;
- 7 broad episode clusters;
- first full month after FIRST_HIKE through month before FIRST_CUT;
- maximum 36 complete months per leg.

Dependence handling:

- mechanical-cycle fixed effects;
- each mechanical cycle receives total regression weight 1;
- overlapping monthly forward outcomes are not treated as IID;
- primary inference uses exact broad-episode cluster sign-flip;
- nearby 1983-84 legs are clustered together;
- 1987 Jan / 1987 Aug / 1988 legs are clustered together.

Primary multiplicity:

- 4 preselected predictors × 2 primary outcomes = 8 tests;
- public primary rule = Benjamini-Yekutieli FDR 10%;
- BH-FDR is diagnostic only.

Hard QC:

- 0 first-cut-month violations;
- 0 pre-first-hike complete-month violations;
- 0 36M-cap violations;
- 0 market-timing violations;
- 0 macro-period violations;
- 0 equal-cycle-weight violations;
- all 8 primary tests supported.

## 3. Primary family result

**0/8 survive BY-FDR 10%.**

**0/8 survive BH-FDR 10% diagnostic.**

### CPI YoY level

Per one within-cycle state SD:

- next-6M Gold return coefficient: **-1.88 percentage points**
  - broad exact p = **0.140625**
  - mechanical-cycle p = 0.169922
  - BY q = 1.00
  - LOO broad sign stable
- next-6M Gold MDD coefficient: **+0.53 percentage points**
  - broad p = **0.765625**
  - BY q = 1.00
  - LOO broad sign not stable

### CPI momentum

- next-6M return: **-0.66 pp / within-cycle SD**
  - broad p = 0.4375
  - BY q = 1.00
- next-6M MDD: **+0.13 pp**
  - broad p = 0.859375
  - BY q = 1.00

### Industrial-production YoY

- next-6M return: **-1.27 pp / within-cycle SD**
  - broad p = **0.125**
  - mechanical p = 0.111328
  - BY q = 1.00
  - LOO broad sign stable
- next-6M MDD: **+0.35 pp**
  - broad p = 0.390625
  - BY q = 1.00

### WTI six-month return

Support:

- 156 rows;
- 8 mechanical cycles;
- 6 broad episode clusters.

Results:

- next-6M Gold return: **-0.72 pp / within-cycle SD**
  - broad p = 0.4375
  - BY q = 1.00
- next-6M Gold MDD: **+0.84 pp / within-cycle SD**
  - broad p = 0.15625
  - BY q = 1.00
  - LOO broad sign stable

## 4. What changed relative to STATE-001

STATE-001 found visually large binary event-level differences for inflation level, inflation direction, growth and WTI direction.

Those contrasts were based on **between-cycle FIRST_HIKE differences**.

STATE-PANEL-002 instead asks whether **within the same tightening leg**, continuous changes in those states map into future Gold return/MDD.

Under this stronger design, none of the eight frozen primary tests survives even BH-FDR 10%.

### Interpretation

**ASSOCIATIONAL EVIDENCE NOT CONFIRMED.**

The STATE-001 binary patterns should not be upgraded into robust regime rules.

A plausible interpretation is that part of the apparent STATE-001 separation reflected:

- between-cycle composition;
- era differences;
- coarse binary thresholds;
- small n=10 event support.

This is a research result, not a failure to find a desired signal.

## 5. Secondary diagnostics

### Yield curve

Within-cycle 10Y-2Y changes show no meaningful Gold-return association:

- return p = 0.953125;
- MDD p = 0.484375.

### Nominal 10Y

No supported secondary association:

- return p = 0.890625;
- MDD p = 0.65625.

### Simple real-rate proxy

Return coefficient is positive in the within-cycle diagnostic:

- +1.80 pp / within-cycle SD;
- broad p = 0.265625.

MDD:

- -0.63 pp;
- p = 0.875.

No confirmatory claim.

Actual TIPS 10Y real yield DFII10 remains insufficient:

- 3 mechanical cycles;
- 3 broad clusters.

### NFCI

No supported relation:

- return p = 0.59375;
- MDD p = 0.984375.

## 6. USD secondary diagnostic

Full sample:

- +1.83 pp next-6M Gold return per within-cycle USD-return SD;
- broad exact p = **0.03125**;
- mechanical-cycle p = 0.01367;
- LOO broad sign stable.

But USD was **secondary**, not primary.

Across the full 12-test secondary family:

- BH-FDR 10% survivors: **0**;
- BY-FDR 10% survivors: **0**;
- USD BH q = **0.375**;
- USD BY q = **1.00**.

Restriction audit:

| Restriction | Broad clusters | Beta | broad p |
|---|---:|---:|---:|
| Full sample | 7 | +1.83 pp | 0.03125 |
| Exclude 2022 / modern USD source | 6 | +2.05 pp | 0.0625 |
| Post-1994 cycles only | 5 | +2.39 pp | 0.125 |
| Exclude early B01/B02 | 5 | +2.39 pp | 0.125 |

The sign is stable but evidence weakens as independent broad episodes decline.

Status:

**MECHANISM CANDIDATE / NOT MULTIPLICITY-CONFIRMED.**

Do not write “USD predicts Gold” or “USD is the dominant Gold driver.”

## 7. Evidence classification

### DATA FACT

- 165-row monthly panel;
- 10 mechanical cycles;
- 7 conservative broad episode clusters;
- 8/8 frozen primary tests supported computationally;
- 0/8 BY-FDR 10% survivors;
- 0/8 BH-FDR 10% diagnostic survivors.

### DESCRIPTIVE RESULT

Within-cycle coefficients for CPI, growth and WTI are generally small relative to the large between-cycle binary contrasts seen in STATE-001.

### ASSOCIATIONAL EVIDENCE

Primary family: **NOT CONFIRMED.**

USD: secondary hypothesis-generating candidate only.

### CAUSAL EVIDENCE

**None.**

### OOS

**Not applicable.**

This is not a forecasting model.

### DEPLOYMENT

**Not deployable.**

## 8. Main research implication

The evidence currently argues against building PandaAI around simple rules such as:

- high inflation -> Gold state X;
- rising WTI -> Gold state Y;
- real yield positive -> Gold state Z.

The more defensible product object remains:

'policy-cycle location + current state + path-risk distribution + uncertainty'

rather than a deterministic state label.

## 9. Next highest-information research step

Two gaps now dominate:

### A. Cross-asset risk clock

The project already knows endpoint/MDD distributions, but not yet the full **event-time hazard map** of when drawdown risk concentrates after FIRST_HIKE.

Next module should estimate, by asset and event month:

- probability that the eventual 12M/24M trough has already occurred;
- drawdown-depth distribution by event month;
- new-low / new-MDD incidence;
- time-to-trough hazard;
- recovery hazard after trough.

This directly answers:

- “第一次加息后，真正危险的是第几个月？”
- “最大回撤通常发生在什么时候？”

### B. Vintage-safe state layer

Any stronger macro-state claim should use real-time vintages where feasible rather than current-vintage CPI/INDPRO/NFCI history.

Until then, current-vintage state work stays explicitly limited.
