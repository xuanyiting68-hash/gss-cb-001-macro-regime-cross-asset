# FED-CYCLE-HISTORICAL-CASEBOOK-022 — LOCK

Date locked: 2026-09-25

## Purpose

Convert the already-QC-passed Fed-cycle evidence chain into a reproducible episode-level historical casebook for:

- deep research;
- PandaAI evidence retrieval;
- long-form articles;
- short/long video scripts;
- timeline graphics;
- later claim and figure registries.

This is a **case-organization and evidence-linking module**, not a new predictive model.

## Primary casebook universe

Freeze six broad episodes:

| broad_episode_id | content label | structure |
|---|---|---|
| B02 | 1987-1989 tightening/easing sequence | COMPOSITE_MULTI_LEG |
| B03 | 1994-1995 tightening/easing cycle | SINGLE_MECHANICAL_CYCLE |
| B04 | 1999-2001 tightening/easing cycle | SINGLE_MECHANICAL_CYCLE |
| B05 | 2004-2007 tightening/easing cycle | SINGLE_MECHANICAL_CYCLE |
| B06 | 2015-2019 tightening/easing cycle | SINGLE_MECHANICAL_CYCLE |
| B07 | 2022-2024 tightening/easing cycle | SINGLE_MECHANICAL_CYCLE |

B01 (1983-1984) is not part of the primary six-case media set in 022. It remains available in upstream research and may be added later as a clearly labeled legacy appendix.

### Critical B02 rule

B02 contains T03_1987, T04_1987 and T05_1988.

Do **not** collapse their policy anchors into one fictitious FIRST_HIKE/LAST_HIKE/FIRST_CUT sequence.

The episode table may summarize the span, but the policy sequence and asset metrics must preserve sub-cycle rows and episode weights.

## Frozen public inputs

Only consume existing public derived files:

1. `results/fed_cycle_path_v1_1/FED_TIGHTENING_CYCLES.csv`
2. `results/fed_cycle_path_v1_1/FED_CYCLE_EVENTS.csv`
3. `results/fed_cycle_phase_clock_v1/PHASE_CYCLE_ASSET_METRICS.csv`
4. `results/fed_cycle_stress_layer_v1/STRESS_CYCLE_PHASE_METRICS.csv`
5. `results/fed_cycle_stress_trough_alignment_v1/PAIR_TIMING_PANEL.csv`
6. `results/fed_cycle_precut_state_v1/PRECUT_STATE_CYCLE_PANEL.csv`
7. `results/fed_cycle_cross_asset_expansion_v1/RATE_PHASE_METRICS.csv`
8. `results/fed_cycle_cross_asset_expansion_v1/CASH_PHASE_METRICS.csv`

Relevant upstream QC files must all be PASS.

No private-paper inputs are permitted.

## Evidence-time taxonomy

Every casebook fact must be assigned one of:

### REALTIME_KNOWABLE
Information explicitly constructed from observations available at/before the relevant anchor under upstream timing rules.

In 022 this includes the audited 019 pre-FIRST_CUT context:
- curve observation;
- NFCI observation;
- real-time RTDSM IPT growth;
- corresponding observation/vintage dates.

Important: 019/020 failed as a bottom-timing rule. These fields are context, not predictive evidence.

### DESCRIPTIVE_PATH
Post-anchor market/rate/cash outcomes used to describe what happened historically:
- returns;
- MDD / MAE / MFE;
- trough timing;
- recovery;
- Treasury-yield changes;
- cash carry.

These are historical outcomes, not information that was knowable at the anchor.

### EXPOST_ONLY
Future-window statistics that can only be known after the path unfolds:
- VIX / Baa / copper maximum stress move;
- stress-peak month;
- asset-trough vs stress-peak alignment.

They must never be phrased as live timing signals.

## Frozen output objects

1. `CASEBOOK_EPISODES.csv`
   - six broad episodes;
   - cycle count;
   - cycle IDs;
   - span;
   - structure flag;
   - source-era caveat.

2. `CASEBOOK_POLICY_SEQUENCE.csv`
   - sub-cycle-preserving policy anchors;
   - event date;
   - source effective date;
   - event-date basis;
   - n hikes;
   - cumulative hike bp;
   - target before/after;
   - phase sequence.

3. `CASEBOOK_ASSET_PHASE_METRICS.csv`
   - GOLD / SP500 / NASDAQ / WTI;
   - FIRST_HIKE / LAST_HIKE / PAUSE_START / FIRST_CUT;
   - exact upstream cycle rows;
   - evidence_time = DESCRIPTIVE_PATH.

4. `CASEBOOK_PRECUT_REALTIME_CONTEXT.csv`
   - audited 019 predetermined context;
   - evidence_time = REALTIME_KNOWABLE;
   - explicit failed-timing-rule guardrail.

5. `CASEBOOK_EXPOST_STRESS_ALIGNMENT.csv`
   - 018 asset/stress timing pairs;
   - evidence_time = EXPOST_ONLY.

6. `CASEBOOK_RATE_CASH_CONTEXT.csv`
   - DGS2 / DGS10 changes and mechanical cash carry;
   - evidence_time = DESCRIPTIVE_PATH;
   - no direct ranking against price returns.

7. `CASEBOOK_REFERENCE.json`
   - machine-readable evidence-linked casebook.

8. `FED_CYCLE_HISTORICAL_CASEBOOK_022_REPORT.md`
   - research-facing synthesis.

9. `CASEBOOK_CONTENT_BRIEFS.md`
   - one mechanically grounded brief per broad episode;
   - facts only from frozen repo evidence;
   - no external narrative facts in 022.

10. `QC.json`

## Prohibited operations

022 must NOT:

- create new p-values or FDR families;
- fit or tune a predictive rule;
- search for thresholds;
- rank cases or assets as best/worst;
- treat a realized Fed anchor as a structural policy shock;
- use ex-post stress peaks as if known in real time;
- overwrite the 019/020 negative timing-rule conclusion;
- infer macro/news explanations not present in the frozen inputs;
- import private-paper material.

## QC gates

PASS requires:

1. exact six broad episodes B02-B07;
2. B02 contains exactly three mechanical cycles and remains sub-cycle-preserving;
3. B03-B07 contain one mechanical cycle each;
4. all asset phase rows trace to PHASE-CLOCK-004;
5. all REALTIME_KNOWABLE rows trace to 019 timing-audited inputs;
6. all EXPOST_ONLY rows trace to 018;
7. evidence_time taxonomy has no nulls;
8. no p-values generated;
9. no private-paper inputs;
10. causal_status = NONE;
11. oos_status = NOT_A_FORECASTING_MODEL;
12. deployment_status = NOT_DEPLOYABLE.

## Interpretation boundary

022 answers:

> What sequence and cross-asset path occurred in these historical Fed-cycle episodes, what information was available before the first cut, and what only became visible after the path unfolded?

022 does not answer:

> Which historical case is the correct analog today, what will bottom next, or what should be bought/sold now?

