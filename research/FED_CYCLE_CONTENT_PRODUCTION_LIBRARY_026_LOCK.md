# FED-CYCLE-CONTENT-PRODUCTION-LIBRARY-026 — LOCK

Date locked: 2026-09-25

## Purpose

Build a platform-ready Chinese-language content production library from the canonical 022B claim registry and 025 P0 visual pack.

026 is a **publishing / education layer**, not a research extension.

No new empirical result may be created.

## Frozen content packages

Exactly six packages, inherited from the 022B routing packs:

1. `CNT-01-FIRST-CUT-NOT-THE-BOTTOM`
2. `CNT-02-SAME-LABEL-DIFFERENT-PATHS`
3. `CNT-03-GOLD-VS-EQUITIES`
4. `CNT-04-HINDSIGHT-TRAPS`
5. `CNT-05-RECOVERY-CLOCK`
6. `CNT-06-1987-MULTI-LEG`

## Frozen deliverables per package

Every package must contain:

- Chinese primary title;
- 3 hook options;
- 60-90 second short-video script;
- long-form article/video outline;
- linked CLAIM_IDs;
- linked FIGURE_KEYs;
- source block;
- mandatory caveat block;
- prohibited wording block;
- freshness rule;
- visual readiness status;
- platform tags.

## Visual readiness

### READY_P0_VISUAL
Packages whose main factual story can be produced with already-rendered 025 P0 figures:
- CNT-01
- CNT-02
- CNT-03
- CNT-04
- CNT-05

### TEXT_READY_VISUAL_PENDING_P1
- CNT-06

The 1987-89 multi-leg story is text/claim ready but its dedicated FIG-CASE-B02 remains a P1 spec and is not part of the 025 rendered P0 pack.

Do not silently substitute another figure and imply it is B02.

## Package evidence rules

### CNT-01 — FIRST_CUT_NOT_THE_BOTTOM

Required claims:
- CLM-PHASE-DXY-FIRST_CUT
- CLM-PHASE-GOLD-FIRST_CUT
- CLM-PHASE-NASDAQ-FIRST_CUT
- CLM-PHASE-SP500-FIRST_CUT
- CLM-PHASE-WTI-FIRST_CUT
- CLM-SYNTH-017-FIRSTCUT-RECOVERY
- CLM-GUARD-019
- CLM-GUARD-020
- CLM-CASE-B04
- CLM-CASE-B05
- CLM-CASE-B06
- CLM-CASE-B07

Main figures:
- five FIRST_CUT phase cards;
- recovery synthesis;
- B04-B07 case timelines;
- 019/020 guardrails.

Core message:
`FIRST_CUT is a policy-phase label, not a deterministic market-bottom signal.`

### CNT-02 — SAME_LABEL_DIFFERENT_PATHS

Required claims:
- CLM-CASE-B03
- CLM-CASE-B04
- CLM-CASE-B05
- CLM-CASE-B06
- CLM-CASE-B07

Rendered main figures:
- FIG-CASE-B04
- FIG-CASE-B05
- FIG-CASE-B06
- FIG-CASE-B07

B03 may be described from the canonical claim, but its figure is not P0-rendered.

Core message:
`the same FIRST_CUT label has historically coexisted with materially different asset paths.`

### CNT-03 — GOLD_VS_EQUITIES

Required claims:
- CLM-PHASE-GOLD-FIRST_CUT
- CLM-PHASE-SP500-FIRST_CUT
- CLM-PHASE-NASDAQ-FIRST_CUT
- CLM-CASE-B04
- CLM-CASE-B05
- CLM-CASE-B06
- CLM-CASE-B07

Main figures:
- Gold / SP500 / Nasdaq FIRST_CUT cards;
- B04-B07 case timelines.

Core message:
`Gold and U.S. equities can have different paths within the same policy phase; phase labels do not create a universal asset ranking.`

### CNT-04 — HINDSIGHT_TRAPS

Required claims:
- CLM-CTX-B04_CTX_02
- CLM-CTX-B04_CTX_03
- CLM-CTX-B05_CTX_03
- CLM-CTX-B06_CTX_02
- CLM-CTX-B06_CTX_03
- CLM-CTX-B07_CTX_02

Main rendered figures:
- FIG-CASE-B04
- FIG-CASE-B05
- FIG-CASE-B06
- FIG-CASE-B07

Core message:
`what we know today is not the same as what was knowable at the policy anchor.`

### CNT-05 — RECOVERY_CLOCK

Required claims:
- CLM-SYNTH-017-FIRSTCUT-RECOVERY
- all five FIRST_CUT core phase claims.

Main figures:
- FIG-RECOVERY-FIRSTCUT-VS-PAUSE
- five FIRST_CUT phase cards.

Core message:
`endpoint return, interim drawdown and full-recovery time are different investment-risk objects.`

### CNT-06 — 1987_MULTI_LEG

Required claims:
- CLM-CASE-B02
- CLM-CTX-B02_CTX_01
- CLM-CTX-B02_CTX_02
- CLM-CTX-B02_CTX_03

Figure dependency:
- FIG-CASE-B02 (P1 / not rendered in 025)

Core message:
`1987-89 should not be compressed into one standard Fed cycle.`

## Short-video script rules

Target:
- 60-90 seconds;
- Chinese;
- educational tone;
- concise numbers only from canonical claims;
- explicitly distinguish history from current prediction.

Required structure:
1. hook;
2. one-sentence thesis;
3. 2-4 evidence points;
4. one boundary/caveat;
5. educational close.

Do not include:
- buy/sell calls;
- asset-allocation instruction;
- "必涨/必跌";
- deterministic bottom date;
- political evaluation of the Fed;
- causal claim unsupported by the registry.

## Long-form outline rules

Each outline must include:

1. question / misconception;
2. evidence framework;
3. historical distribution or case evidence;
4. real-time vs hindsight distinction where relevant;
5. what the evidence does not prove;
6. reusable figure map;
7. source / claim appendix.

## Source block

Every package must expose:
- claim IDs;
- figure IDs;
- official-source URLs inherited through context claims where applicable;
- canonical repo source files.

No external source may be added in 026 without a new source-audit step.

## Freshness rules

- historical claims: inherit 022B freshness;
- rendered visuals: inherit 024/025 freshness;
- any package containing CLM-CTX-B07_CTX_02 must be `REVERIFY_BEFORE_CURRENT_USE`;
- any package using current 023 state in a future extension must use a new append-only current snapshot, not overwrite 2026-09-25.

## Frozen output files

- `CONTENT_OBJECTS.csv`
- `CONTENT_LIBRARY.json`
- `SHORT_VIDEO_SCRIPTS_ZH.md`
- `LONGFORM_OUTLINES_ZH.md`
- `SOURCE_AND_CAVEAT_BLOCKS.md`
- `CONTENT_CLAIM_FIGURE_MAP.csv`
- `FED_CYCLE_CONTENT_PRODUCTION_LIBRARY_026_REPORT.md`
- `QC.json`

## QC gates

PASS requires:

1. exactly six content packages;
2. package IDs exactly match frozen universe;
3. every referenced claim exists in 022B;
4. every referenced figure exists in 024;
5. READY_P0_VISUAL packages reference at least one rendered 025 P0 figure;
6. CNT-06 is explicitly TEXT_READY_VISUAL_PENDING_P1;
7. CNT-06 does not falsely claim FIG-CASE-B02 is rendered;
8. CNT-04 freshness = REVERIFY_BEFORE_CURRENT_USE;
9. all numeric expressions in generated scripts are derived from claim payload/wording, not separately re-estimated;
10. every script contains a history/not-forecast boundary;
11. zero buy/sell language;
12. zero deterministic analog/ranking/forecast instruction;
13. no new p-values/inference;
14. private-paper inputs = false;
15. causal status = NONE;
16. deployment status = NOT_DEPLOYABLE.

## Interpretation boundary

026 is a content-production system.

A package being ready means:
> its claims and visuals are traceable to the public evidence stack and can be adapted to a platform without changing factual content.

It does not mean:
> the content is an investment recommendation, market forecast, or evaluation of a political/policy actor.
