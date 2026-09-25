# FED-CYCLE-FIGURE-REGISTRY-024 — CLOSEOUT

Date: 2026-09-25

## Final status

**QC PASS / 48 VISUAL EVIDENCE SPECS / CLAIM-LINKED / NOT CAUSAL / NOT DEPLOYABLE**

024 creates the canonical visual specification layer over the 022B claim registry and 023 current-state dashboard.

It creates no new empirical result. It defines how existing evidence may be visualized without changing the evidence boundary.

## Registry coverage

- 47 claim-linked figure specs mapped 1:1 from 022B;
- 1 supplemental current-state figure from 023;
- 48 total unique figure keys.

Visual families:
- CORE_PHASE_EVIDENCE_CARD: 20
- HISTORICAL_CASE_TIMELINE: 6
- HISTORICAL_CONTEXT_CARD: 18
- METHOD_GUARDRAIL: 2
- RECOVERY_SYNTHESIS: 1
- CURRENT_REGIME_SNAPSHOT: 1

Production tiers:
- P0: 13
- P1: 22
- P2: 13

Priority is production order only, not evidence strength or asset ranking.

## P0 build queue

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

## Binding visual controls

### Asset-phase cards
Endpoint return, drawdown magnitude, trough timing and recovery duration are separate objects and must use explicitly separated encodings.

A positive 12-month endpoint may not visually imply that interim drawdown risk was small or that the trough occurred at the policy anchor.

### Historical cases
B02 remains a three-sub-cycle sequence.

B04/B06 later shocks may be annotated only with their 022A timing class and may not be drawn as if they caused the earlier first-cut decision.

No case may receive a closest-current-analog label.

### Historical context
RETROSPECTIVE_DATING and POST_ANCHOR_SHOCK cards retain explicit hindsight labels.

B07's current NBER chronology context retains `REVERIFY_BEFORE_CURRENT_USE`.

### Method guardrails
019/020 are negative-result visuals:
- no trade-signal colors;
- no composite timing score;
- no promotion of the five-episode curve sensitivity above the full-sample 020 result.

### Current 023 dashboard
Must display:
- one hike / 25bp;
- prospective qualification FALSE;
- snapshot clock and observation dates;
- historical FIRST_HIKE claims as reference distributions only.

It may not contain:
- similarity meter;
- closest analog;
- asset rank;
- expected return;
- trade signal.

## Reproducibility

Workflow:
- `.github/workflows/fed-cycle-figure-registry-024-v1.yml`
- run id: 36102502076
- source commit: `bc30fed26806ee80abb2f4d5ce80654763f2b202`
- output commit: `6c378b7cf56699056958b7b721b767b41dba9eac`
- result: SUCCESS

QC:
- total specs = 48;
- unique keys = 48;
- claim-linked specs = 47;
- supplemental current specs = 1;
- context timing preserved = true;
- B02 three-sub-cycle guardrail = true;
- B04/B06 post-anchor-shock guardrail = true;
- B07 reverify freshness = true;
- P0 = 13;
- blank visual-boundary fields = 0;
- analog-score fields = 0;
- asset-ranking fields = 0;
- forecast-return fields = 0;
- new inference = false;
- p-values = false;
- private-paper inputs = false;
- causal status = NONE;
- deployment = NOT_DEPLOYABLE.

## Next milestone

Proceed to **025 P0 Visual Evidence Pack**.

025 should render the 13 P0 specifications reproducibly from canonical data, with:
- research SVG/PNG outputs;
- social 16:9 and 1:1 variants where useful;
- machine-readable render manifest;
- exact linked CLAIM_IDs;
- source hashes / input file references;
- automated checks that required disclaimers and annotations are present.

Rendered visuals remain communication artifacts, not new empirical evidence.
