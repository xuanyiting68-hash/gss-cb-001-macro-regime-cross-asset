# FED-CYCLE-EDITORIAL-RELEASE-CANDIDATE-029 — LOCK

Date locked: 2026-09-25

## Purpose

Freeze one editorial release candidate (RC1) for each of the six canonical content packages, define a four-week cross-platform release calendar, add a pre-publication evidence/freshness checklist, and create a post-publication performance-log schema.

029 is a **release-operations module**.

It does not create or change empirical evidence.

## Frozen content universe

Exactly six release candidates:

1. RC-CNT-01-FIRST-CUT-NOT-THE-BOTTOM
2. RC-CNT-02-SAME-LABEL-DIFFERENT-PATHS
3. RC-CNT-03-GOLD-VS-EQUITIES
4. RC-CNT-04-HINDSIGHT-TRAPS
5. RC-CNT-05-RECOVERY-CLOCK
6. RC-CNT-06-1987-MULTI-LEG

Each RC must resolve to one 026/028 content package.

## Immutable factual payload

The following are immutable within RC1:
- CLAIM_IDs;
- canonical evidence numbers;
- FIGURE_KEYs;
- freshness rule;
- mandatory caveat;
- source files/official URLs;
- evidence-time class;
- no-causal/no-forecast/no-deployment status.

Changing any immutable field requires a new upstream evidence/content build, not an editorial A/B variant.

## Editable editorial layer

The following may be A/B tested without changing evidence:
- cover wording;
- hook wording;
- first 3-7 seconds;
- thumbnail/cover layout;
- order of evidence cards within the allowed claim set;
- caption length;
- non-investment educational CTA.

Allowed CTA examples:
- “收藏这组历史周期数据”
- “关注后续加息/降息周期研究”
- “评论区说说你最想看哪个历史周期”

Not allowed:
- buy/sell CTA;
- urgency around financial action;
- “跟着买/抄底/上车” language;
- promises of returns.

## RC1 platform surfaces

Each release candidate must specify:

### Douyin/TikTok
- cover;
- selected hook;
- 9:16 shotlist source;
- evidence insert order;
- caption source;
- closing caveat;
- publication status.

### Xiaohongshu
- cover;
- carousel sequence;
- caption source;
- final source/boundary card;
- publication status.

### WeChat / deep article
- article title;
- article section/figure map;
- source appendix;
- publication status.

### PandaAI
- template ID;
- claim/figure set;
- freshness rule;
- current-data guard.

## Frozen four-week release order

Suggested publishing calendar begins 2026-09-28.

The schedule is editorial, not empirical.

Week 1:
- CNT-02 SAME_LABEL_DIFFERENT_PATHS
- CNT-04 HINDSIGHT_TRAPS

Week 2:
- CNT-01 FIRST_CUT_NOT_THE_BOTTOM
- CNT-05 RECOVERY_CLOCK

Week 3:
- CNT-03 GOLD_VS_EQUITIES
- CNT-06 1987_MULTI_LEG

Week 4:
- repurpose the strongest-performing two packages into deeper WeChat/PandaAI formats;
- no evidence changes are allowed based on performance.

Suggested cadence:
- Monday: primary short/video;
- Wednesday: Xiaohongshu carousel;
- Friday/Sunday: deep article or recap where suitable.

## Pre-publication preflight

Every release must check:

1. GitHub main still contains the referenced CLAIM_IDs and FIGURE_KEYs;
2. figure files referenced by the platform output exist;
3. freshness rule is satisfied;
4. any REVERIFY_BEFORE_CURRENT_USE claim is re-audited;
5. no current-state language relies on an expired snapshot;
6. numbers in copy match canonical claim payload/026 object;
7. title/hook changes do not alter factual meaning;
8. no prohibited buy/sell, best-asset, current-analog or deterministic-bottom language;
9. mandatory caveat remains present;
10. source/citation block remains available.

A failed preflight means HOLD, not silent editing.

## Performance log schema

029 defines a post-publication log only. It does not ingest or optimize on live performance yet.

Fields include:
- content_id;
- release_candidate_id;
- platform;
- publish_timestamp;
- title_variant;
- hook_variant;
- views;
- 3s_views;
- average_watch_time;
- completion_rate;
- likes;
- comments;
- saves;
- shares;
- profile_clicks;
- follows;
- link_clicks;
- notes;
- evidence_payload_changed flag.

The evidence_payload_changed flag must always be FALSE for normal editorial iterations.

If a future experiment changes factual payload, it is not an A/B editorial test and requires a new upstream version.

## Frozen outputs

- RELEASE_CANDIDATES.csv
- RELEASE_CALENDAR.csv
- PREFLIGHT_CHECKLIST.md
- PERFORMANCE_LOG_SCHEMA.csv
- EDITORIAL_AB_TEST_RULES.md
- RELEASE_CANDIDATES_ZH.md
- FED_CYCLE_EDITORIAL_RELEASE_CANDIDATE_029_REPORT.md
- QC.json

## QC gates

PASS requires:

1. exactly six RC1 objects;
2. one RC per 028 package;
3. all RC claim IDs exist in 022B;
4. all RC figure keys exist in 024 and rendered sets where used;
5. all immutable evidence payload hashes are recorded;
6. exactly six primary release slots across weeks 1-3;
7. each package appears exactly once in primary release slots;
8. week 4 is repurposing only;
9. CNT-04 is HOLD unless REVERIFY_BEFORE_CURRENT_USE preflight passes;
10. no current snapshot treated as perpetually live;
11. performance schema contains evidence_payload_changed;
12. editorial A/B rules prohibit factual-payload changes;
13. no buy/sell or return-promise CTA;
14. no best-asset ranking;
15. no current-analog ranking;
16. no deterministic bottom/forecast claim;
17. no political evaluation of Fed actors;
18. no new inference/p-values;
19. private-paper inputs = false;
20. causal status = NONE;
21. deployment status = NOT_DEPLOYABLE.

## Interpretation boundary

029 freezes publishing operations, not market conclusions.

Editorial performance may change how evidence is presented, never what the evidence says.
