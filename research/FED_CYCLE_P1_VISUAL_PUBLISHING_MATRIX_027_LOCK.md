# FED-CYCLE-P1-VISUAL-PUBLISHING-MATRIX-027 — LOCK

Date locked: 2026-09-25

## Purpose

Complete the highest-priority P1 visual gaps required by the six canonical 026 content packages, then create a channel-by-channel publishing matrix.

027 is a **visual completion + publishing orchestration layer**.

It does not add empirical evidence, forecasts, rankings, analog scores or investment recommendations.

## Frozen P1 visual universe

Exactly seven figure keys:

1. FIG-CASE-B02
2. FIG-CASE-B03
3. FIG-CTX-B04_CTX_02
4. FIG-CTX-B04_CTX_03
5. FIG-CTX-B05_CTX_03
6. FIG-CTX-B06_CTX_02
7. FIG-CTX-B06_CTX_03

These are the two P1 case figures plus the five priority hindsight/context cards frozen in 024.

No other P1/P2 figure may enter 027 v1.

## Render variants

Each of the seven figures is rendered as:

- SVG_RESEARCH
- PNG_16_9 at 1600x900
- PNG_1_1 at 1200x1200

Expected render count = 7 x 3 = **21 files**.

## Figure rules

### FIG-CASE-B02

Source:
- CASEBOOK_POLICY_SEQUENCE.csv
- CONTEXT_CLAIMS.csv
- CLM-CASE-B02

Required structure:
- T03_1987;
- T04_1987;
- T05_1988;
- three separate horizontal policy legs;
- Black Monday context between sub-cycles;
- Fed liquidity-response context;
- explicit note that no synthetic single FIRST_HIKE-to-FIRST_CUT path is constructed.

Must NOT show a fabricated four-asset B02 summary.

### FIG-CASE-B03

Source:
- CASEBOOK_POLICY_SEQUENCE.csv
- CASEBOOK_ASSET_PHASE_METRICS.csv
- CONTEXT_CLAIMS.csv
- CLM-CASE-B03

Required:
- 1994 FIRST_HIKE;
- 1995 LAST_HIKE / PAUSE / FIRST_CUT;
- Gold/Nasdaq/SP500/WTI FIRST_CUT +12M endpoint, MDD and trough month;
- context layer including the no-NBER-recession retrospective note.

### Five context cards

Each context card must display:
- broad episode;
- event date/period;
- claim-time class;
- canonical claim text;
- hindsight warning;
- source institution/title;
- source URL text;
- allowed-use boundary.

Cards:
- B04_CTX_02 = RETROSPECTIVE_DATING
- B04_CTX_03 = POST_ANCHOR_SHOCK
- B05_CTX_03 = RETROSPECTIVE_DATING
- B06_CTX_02 = RETROSPECTIVE_DATING
- B06_CTX_03 = POST_ANCHOR_SHOCK

No later event may be drawn as causing an earlier policy action.

## Publishing matrix

Exactly six 026 content objects x four delivery channels = **24 rows**.

Channels:

1. `DOUYIN_TIKTOK_SHORT`
2. `XIAOHONGSHU_CAROUSEL`
3. `WECHAT_LONGFORM`
4. `PANDAAI_EXPLANATION`

## Channel rules

### DOUYIN_TIKTOK_SHORT
- content basis: 026 60-90s script;
- hook: choose from 026 hooks;
- primary visual source: 16:9 evidence panels used as in-video evidence inserts;
- note: 027 does not render a full 9:16 video composition;
- disclaimer must appear in caption or closing card;
- no buy/sell CTA.

### XIAOHONGSHU_CAROUSEL
- 1:1 evidence cards;
- 5-9 card narrative;
- cover = question/myth, not asset recommendation;
- final card = evidence boundary + sources;
- do not turn asset comparison into ranking.

### WECHAT_LONGFORM
- use 026 long-form outline;
- SVG/16:9 research figures;
- source appendix required;
- context timing labels retained.

### PANDAAI_EXPLANATION
- machine-readable content object;
- return claim IDs + figure keys + freshness;
- current data only if a valid append-only current snapshot is supplied;
- no unsupported personalization or trade instruction.

## Visual readiness after 027

After successful rendering:

- CNT-01: VISUAL_COMPLETE_FOR_CANONICAL_PACKAGE
- CNT-02: VISUAL_COMPLETE_FOR_CANONICAL_PACKAGE, now including B03
- CNT-03: VISUAL_COMPLETE_FOR_CANONICAL_PACKAGE
- CNT-04: VISUAL_COMPLETE_FOR_CANONICAL_PACKAGE, now including five dedicated hindsight cards
- CNT-05: VISUAL_COMPLETE_FOR_CANONICAL_PACKAGE
- CNT-06: VISUAL_COMPLETE_FOR_CANONICAL_PACKAGE, now including B02

This readiness is about canonical evidence visuals, not a final platform-native 9:16 video file.

## Frozen outputs

- P1_RENDER_MANIFEST.csv
- P1_SOURCE_FILE_HASHES.csv
- PUBLISHING_MATRIX.csv
- PACKAGE_VISUAL_READINESS.csv
- PLATFORM_PUBLISHING_GUIDE_ZH.md
- FED_CYCLE_P1_VISUAL_PUBLISHING_MATRIX_027_REPORT.md
- QC.json
- figures/*.svg
- figures/*__16x9.png
- figures/*__1x1.png

## QC gates

PASS requires:

1. seven exact frozen P1 figure keys;
2. 21 rendered files;
3. 7 SVG_RESEARCH;
4. 7 PNG_16_9 at 1600x900;
5. 7 PNG_1_1 at 1200x1200;
6. nonempty render/source hashes;
7. B02 visibly contains T03/T04/T05 and an explicit no-synthetic-path boundary;
8. B02 does not fabricate a four-asset summary;
9. B03 contains four FIRST_CUT asset path rows;
10. all five context cards preserve exact claim-time class;
11. B04_CTX_03 and B06_CTX_03 visibly say POST_ANCHOR_SHOCK;
12. 24 publishing matrix rows;
13. exactly four channels per content package;
14. all six packages become canonical-visual-complete;
15. DOUYIN_TIKTOK_SHORT explicitly notes no full 9:16 composition is rendered;
16. CNT-04 remains REVERIFY_BEFORE_CURRENT_USE;
17. no buy/sell, best-asset, closest-analog, forecast-return or political-evaluation field;
18. no new p-values/inference;
19. private-paper inputs = false;
20. causal status = NONE;
21. deployment status = NOT_DEPLOYABLE.

## Interpretation boundary

027 completes evidence visuals and platform routing.

It does not produce a personalized investment recommendation, a political evaluation of Federal Reserve actors, or a current-cycle forecast.
