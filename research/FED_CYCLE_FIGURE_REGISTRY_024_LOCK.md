# FED-CYCLE-FIGURE-REGISTRY-024 — LOCK

Date locked: 2026-09-25

## Purpose

Create the canonical visual-evidence specification layer for the public Fed-cycle / cross-asset research program.

024 maps the 47 stable 022B claim-level `figure_key` values into explicit chart/card specifications and adds one supplemental current-state figure for 023.

Total frozen figure specs in v1: **48**.

024 creates specifications and build priorities. It does not re-estimate any empirical result and does not optimize visuals for a desired narrative.

## Frozen figure universe

### A. 20 CORE_PHASE_EVIDENCE_CARD figures

One for each 022B core asset x phase claim.

Figure key inherited exactly from 022B:
`FIG-PHASE-{ASSET}-{PHASE}`

Visual grammar:
- evidence card / compact small-multiple;
- +12M endpoint;
- 12M MDD magnitude;
- median trough month;
- anchor-to-full-recovery median;
- sample/support footer.

Required visual rule:
- endpoint return and MDD must never share a single unlabeled axis;
- drawdown magnitude must be explicitly labeled as path risk, not negative return;
- trough month/recovery month are historical medians, not forecasts.

### B. 6 HISTORICAL_CASE_TIMELINE figures

Keys:
- FIG-CASE-B02 ... FIG-CASE-B07

Visual grammar:
- dated policy chronology;
- FIRST_CUT marker;
- four-asset +12M endpoint/MDD/trough summary for B03-B07;
- B02 must show three separate mechanical sub-cycles.

Required visual rule:
- do not flatten B02;
- later shocks/context from 022A may be annotation layers but must retain claim-time class.

### C. 18 HISTORICAL_CONTEXT_CARD figures

Keys inherited from 022A through 022B:
`FIG-CTX-{022A_CLAIM_ID}`

Visual grammar:
- source-backed context card;
- event date/period;
- claim-time class;
- concise paraphrase;
- source institution;
- hindsight warning.

Required visual rule:
- RETROSPECTIVE_DATING and POST_ANCHOR_SHOCK must use explicit hindsight labels;
- no visual arrow implying that a later event caused an earlier policy action.

### D. 2 METHOD_GUARDRAIL figures

- FIG-GUARD-019
- FIG-GUARD-020

Visual grammar:
- 019: state-variation / contrast table emphasizing unsupported timing-rule result;
- 020: full-sample rho + leave-one-out stability diagnostic emphasizing sign instability.

Required visual rule:
- no green/red "signal" colors;
- no cherry-picked five-episode curve result promoted above the full-sample conclusion.

### E. 1 RECOVERY_SYNTHESIS figure

- FIG-RECOVERY-FIRSTCUT-VS-PAUSE

Visual grammar:
- asset-level paired comparison of anchor-to-full-recovery months for PAUSE_START vs FIRST_CUT;
- five fully supported assets only;
- descriptive comparison, no winner label.

### F. 1 CURRENT_REGIME_SNAPSHOT figure

Supplemental key:
- FIG-CURRENT-023-REGIME-SNAPSHOT

Visual grammar:
- current policy gate;
- rates/curve;
- breakevens;
- stress/credit;
- real economy/inflation;
- freshness badges;
- historical-reference CLAIM_ID footer.

Required visual rule:
- must show current cycle qualification FALSE;
- must not show an analog score or current asset recommendation.

## Required registry fields

Each figure spec must include:

- figure_key
- figure_family
- linked_claim_ids
- source_modules
- source_files
- data_scope
- visual_grammar
- primary_encodings
- required_annotations
- required_disclaimer
- prohibited_visual_implications
- freshness_rule
- output_formats
- priority
- build_status
- public_safe
- causal_status
- deployment_status

## Frozen priority tiers

### P0
Core social/research visuals that should be built first:
- five FIRST_CUT core asset cards;
- FIG-RECOVERY-FIRSTCUT-VS-PAUSE;
- FIG-GUARD-019;
- FIG-GUARD-020;
- FIG-CASE-B04;
- FIG-CASE-B05;
- FIG-CASE-B06;
- FIG-CASE-B07;
- FIG-CURRENT-023-REGIME-SNAPSHOT.

Total P0 = 13.

### P1
- remaining 15 core phase cards;
- FIG-CASE-B02;
- FIG-CASE-B03;
- selected hindsight cards for 2001/2007/2019.

### P2
- remaining context cards.

No empirical meaning is attached to priority tier; it is a production-order field only.

## Frozen output formats

Specs may list:
- PNG_16_9
- PNG_1_1
- SVG_RESEARCH
- JSON_SPEC

No figure is considered evidence by itself; it must resolve back to claim/data sources.

## Prohibited operations

024 must NOT:
- choose axes that hide drawdowns or exaggerate differences;
- truncate scales without explicit labeling;
- add best/worst rankings;
- add current-cycle analog scores;
- label historical trough months as forecasts;
- turn 019/020 guardrails into signals;
- omit sample/support/freshness labels;
- use causal arrows not supported by the evidence class;
- import private-paper inputs.

## QC gates

PASS requires:

1. exactly 47 unique claim-linked figure keys from 022B;
2. exactly one supplemental 023 figure key;
3. total figure specs = 48;
4. every 022B figure_key maps 1:1;
5. every context figure preserves 022A timing class;
6. B02 figure family explicitly preserves three sub-cycles;
7. B04/B06 later-shock figures retain POST_ANCHOR_SHOCK;
8. B07 current NBER context figure retains REVERIFY_BEFORE_CURRENT_USE;
9. exactly 13 P0 figures;
10. no blank source/annotation/disclaimer fields;
11. no ranking/analog/forecast visual field;
12. no new inference or p-values;
13. private-paper inputs = false;
14. causal status = NONE;
15. deployment status = NOT_DEPLOYABLE.

## Interpretation boundary

024 controls visual communication.

A figure spec being PUBLIC_SAFE means the underlying claim can be visualized under the stated rules. It does not mean the visual is predictive, causal, or an investment recommendation.
