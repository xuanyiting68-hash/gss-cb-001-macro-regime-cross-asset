# FED-CYCLE-P0-VISUAL-EVIDENCE-PACK-025 — LOCK

Date locked: 2026-09-25

## Purpose

Render the 13 frozen P0 figure specifications from FED-CYCLE-FIGURE-REGISTRY-024 into reproducible public-safe visual artifacts.

025 is a **rendering / communication module only**.

It must not:
- re-estimate any market statistic;
- change claim wording;
- choose new samples;
- optimize visual scales to strengthen a narrative;
- introduce analog scores, rankings or forecasts.

## Frozen figure universe

Exactly 13 figure keys, inherited from 024 P0:

1. FIG-PHASE-DXY-FIRST_CUT
2. FIG-PHASE-GOLD-FIRST_CUT
3. FIG-PHASE-NASDAQ-FIRST_CUT
4. FIG-PHASE-SP500-FIRST_CUT
5. FIG-PHASE-WTI-FIRST_CUT
6. FIG-RECOVERY-FIRSTCUT-VS-PAUSE
7. FIG-GUARD-019
8. FIG-GUARD-020
9. FIG-CASE-B04
10. FIG-CASE-B05
11. FIG-CASE-B06
12. FIG-CASE-B07
13. FIG-CURRENT-023-REGIME-SNAPSHOT

No additional figure may enter v1 after lock.

## Frozen output variants

For each figure:

- `SVG_RESEARCH`: vector research/publication version;
- `PNG_16_9`: 1600x900 social/video version;
- `PNG_1_1`: 1200x1200 square social-card version.

Expected rendered files = 13 x 3 = **39**.

In addition:
- `RENDER_MANIFEST.csv`
- `P0_VISUAL_INDEX.md`
- `FED_CYCLE_P0_VISUAL_EVIDENCE_PACK_025_REPORT.md`
- `QC.json`

## Source rules

All empirical values must come from already-QC-passed canonical files.

### Phase cards
Source:
- 022B CLAIM_REGISTRY.csv metric_payload and claim metadata.

No recomputation of +12M return, MDD, trough month or full-recovery duration.

### Recovery synthesis
Source:
- `results/fed_cycle_total_risk_clock_v1/SUPPORTED_TOTAL_CLOCK_SUMMARY.csv`

Only DXY/GOLD/NASDAQ/SP500/WTI.
Only PAUSE_START versus FIRST_CUT.
No ranking label.

### 019 guardrail
Source:
- `results/fed_cycle_precut_state_v1/BINARY_STATE_SUPPORT.csv`
- `results/fed_cycle_precut_state_v1/BINARY_STATE_CONTRASTS.csv`
- claim CLM-GUARD-019.

### 020 guardrail
Source:
- `results/fed_cycle_precut_stress_level_v1/CONTINUOUS_RANK_DIAGNOSTICS.csv`
- claim CLM-GUARD-020.

Full-sample diagnostics must be visually primary.

### Historical cases B04-B07
Sources:
- `CASEBOOK_POLICY_SEQUENCE.csv`
- `CASEBOOK_ASSET_PHASE_METRICS.csv`
- `CONTEXT_CLAIMS.csv`

The figure must distinguish:
- policy chronology;
- FIRST_CUT asset path outcomes;
- official-source context;
- RETROSPECTIVE_DATING / POST_ANCHOR_SHOCK.

### Current 023 snapshot
Sources:
- `CURRENT_POLICY_GATE.csv`
- `CURRENT_OBSERVABLES.csv`
- `CURRENT_STATE_DERIVED.csv`
- 024 current-regime spec.

Must visibly show:
- qualification FALSE;
- snapshot clock;
- observation periods;
- no forecast / no analog score.

## Visual grammar

### Common
- restrained research style;
- no red/green trade-signal palette;
- neutral colors only;
- no pictorial arrows implying causality;
- no unlabeled dual-axis comparisons;
- footer includes figure key and linked claim ID(s);
- disclaimer readable in all three output variants.

### Phase cards
Four separate metric panels:
1. +12M endpoint
2. 12M MDD magnitude
3. median trough month
4. anchor-to-full-recovery median

### Recovery synthesis
Paired dot/segment chart:
- x-axis = months;
- one row per asset;
- PAUSE_START and FIRST_CUT explicitly labeled;
- textual note: slower 3/5, equal 2/5, faster 0/5;
- no "winner".

### 019
Table/bar diagnostic emphasizing:
- state-support counts;
- curve inversion 3/3 balance;
- median risk3 trough month = 8 on both curve states;
- insufficient state variation for RT growth and NFCI.

### 020
Forest-style diagnostic:
- full-sample rho point;
- LOO min-max horizontal interval;
- row label includes sample n;
- VIX n=5;
- annotation: all full-sample predictors fail frozen robustness requirement.

### Historical case timelines
Top: dated policy sequence.
Bottom: four FIRST_CUT asset evidence cards/rows with +12M endpoint, MDD, trough month.
Context annotations must preserve timing class.

### Current snapshot
Five groups:
- Policy gate
- Rates / curve
- Inflation expectations
- Stress / credit
- Real economy / inflation

Freshness/observation dates must remain visible.

## Render manifest

Every file row must contain:
- figure_key
- variant
- relative_path
- linked_claim_ids
- source_files
- sha256
- byte_size
- width_px
- height_px
- render_status

SVG width/height may use logical dimensions; PNG dimensions must be exact.

## QC gates

PASS requires:

1. exactly 13 P0 figure keys;
2. all 13 match 024 P0 queue exactly;
3. 39 rendered files;
4. 13 SVG_RESEARCH;
5. 13 PNG_16_9 at 1600x900;
6. 13 PNG_1_1 at 1200x1200;
7. all file hashes non-empty;
8. all byte sizes > 0;
9. every figure links back to canonical claim IDs/spec;
10. phase cards reproduce 022B metric_payload exactly;
11. recovery figure uses exactly five supported assets and PAUSE_START/FIRST_CUT only;
12. 019 figure contains no timing-signal output;
13. 020 figure visually uses FULL_AVAILABLE rows, not VIX-common sensitivity as primary;
14. B04-B07 preserve context timing classes;
15. current 023 figure displays qualification FALSE;
16. no analog score / rank / forecast field or label;
17. no new p-values/inference;
18. private-paper inputs = false;
19. causal status = NONE;
20. deployment status = NOT_DEPLOYABLE.

## Interpretation boundary

025 is a visual delivery layer.

Rendered figures may be reused publicly if their disclaimer, claim linkage and source boundary remain intact.

They are not new evidence, forecasts, causal estimates or investment recommendations.
