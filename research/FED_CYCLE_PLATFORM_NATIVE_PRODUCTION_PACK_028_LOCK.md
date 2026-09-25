# FED-CYCLE-PLATFORM-NATIVE-PRODUCTION-PACK-028 — LOCK

Date locked: 2026-09-25

## Purpose

Turn the six canonical 026 content packages and 027 publishing routes into platform-native production assets while preserving the public evidence stack.

028 is a **production-copy / orchestration layer**, not a research module.

It creates no new returns, drawdowns, recovery statistics, forecasts, rankings, political evaluations or investment recommendations.

## Frozen package universe

Exactly six content packages:

1. CNT-01-FIRST-CUT-NOT-THE-BOTTOM
2. CNT-02-SAME-LABEL-DIFFERENT-PATHS
3. CNT-03-GOLD-VS-EQUITIES
4. CNT-04-HINDSIGHT-TRAPS
5. CNT-05-RECOVERY-CLOCK
6. CNT-06-1987-MULTI-LEG

## Frozen platform deliverables

### A. Douyin / TikTok production sheets

For every package:
- 9:16 production plan;
- 6-9 timed shots;
- start/end seconds;
- voiceover segment;
- on-screen text;
- evidence figure key where used;
- subtitle segment;
- source/caveat placement;
- cover/title text;
- caption copy.

028 does **not** render a final MP4.

The production sheet may use existing 16:9/1:1 evidence figures inside a vertical composition, but must not crop away source/claim footers.

### B. Xiaohongshu carousel copy

For every package:
- 6-9 cards;
- card number;
- cover/body/source-boundary role;
- headline;
- body copy;
- linked figure key;
- linked claim IDs;
- freshness rule;
- final post caption.

Every carousel ends with a source/boundary card.

### C. WeChat / deep-article drafts

Exactly six full Chinese article drafts.

Each article must contain:
1. title;
2. opening question;
3. evidence framework;
4. historical distribution/case evidence;
5. timing/hindsight distinction where relevant;
6. what the evidence does not prove;
7. inline figure placement markers;
8. source appendix;
9. mandatory boundary statement.

Article evidence must resolve to 022B CLAIM_IDs and existing figure keys.

### D. PandaAI explanation templates

Exactly six machine-readable templates.

Each template must include:
- content_id;
- intent examples;
- claim_ids;
- figure_keys;
- freshness rule;
- answer structure;
- required caveat;
- forbidden transformations;
- current-data rule;
- evidence status.

No template may convert historical distributions into individualized buy/sell instructions.

## Current-data rule

028 is based on the historical/content stack plus the frozen 023 current snapshot only as background architecture.

No current-market claim is added in 028.

If a future PandaAI answer needs current state:
- it must retrieve the latest valid append-only current snapshot;
- it must not silently use the 2026-09-25 snapshot as live data.

## Source discipline

All numerical content must come from:
- 026 content objects derived from canonical claim payload/wording; or
- direct 022B canonical claim payloads.

Historical event facts must come from:
- 022A source-audited claims.

No outside source is introduced by 028.

## Frozen outputs

- DOUYIN_TIKTOK_SHOTLISTS_ZH.csv
- DOUYIN_TIKTOK_CAPTIONS_ZH.md
- XIAOHONGSHU_CAROUSELS_ZH.csv
- XIAOHONGSHU_CAPTIONS_ZH.md
- WECHAT_DEEP_ARTICLES_ZH.md
- PANDAAI_EXPLANATION_TEMPLATES.json
- PLATFORM_NATIVE_INDEX.csv
- FED_CYCLE_PLATFORM_NATIVE_PRODUCTION_PACK_028_REPORT.md
- QC.json

## QC gates

PASS requires:

1. exactly six content packages;
2. exactly six Douyin/TikTok production plans;
3. each short-video plan has 6-9 shots;
4. all shot times are non-overlapping and monotonic within each package;
5. each plan ends with a boundary/caveat shot or explicit caption boundary;
6. no full-MP4-render claim;
7. exactly six Xiaohongshu carousels;
8. each carousel has 6-9 cards;
9. each carousel has exactly one COVER card and at least one SOURCE_BOUNDARY card;
10. exactly six full WeChat/deep-article drafts;
11. every article contains figure markers, source appendix and boundary statement;
12. exactly six PandaAI templates;
13. all referenced claim IDs exist in 022B;
14. all referenced figure keys exist in 024 and are rendered in 025/027 where the platform artifact says rendered;
15. CNT-04 retains REVERIFY_BEFORE_CURRENT_USE;
16. all numeric expressions are inherited from 026/022B and not separately re-estimated;
17. no buy/sell instruction;
18. no best-asset ranking;
19. no closest-current-analog ranking;
20. no deterministic bottom/forecast claim;
21. no political evaluation of Fed actors;
22. no new inference/p-values;
23. private-paper inputs = false;
24. causal status = NONE;
25. deployment status = NOT_DEPLOYABLE.

## Interpretation boundary

028 makes the project operationally ready for editorial production.

It does not make market decisions for the audience and does not convert descriptive evidence into a recommendation.
