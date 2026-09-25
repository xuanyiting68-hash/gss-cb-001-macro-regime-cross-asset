# FED-CYCLE-CNT02-FINAL-PUBLISHING-RC-031 — LOCK

Date locked: 2026-09-26

## Purpose

Finalize CNT-02 SAME_LABEL_DIFFERENT_PATHS into a deterministic first-release production candidate for 2026-09-28.

031 is a packaging/finalization layer only.

It does not:
- change empirical evidence;
- add current-market claims;
- create a forecast;
- publish content;
- render a final MP4.

## Authoritative upstream

Required PASS:
- 022B claim registry;
- 027 rendered case figures;
- 028 platform-native shotlist;
- 029 RC1 immutable evidence object;
- 030 release preflight.

CNT-02 must remain:
- preflight_status = GO_RC1;
- publication_status = NOT_PUBLISHED;
- immutable_evidence_sha256 = 48a659bb900be19707165bf8f6802e5ce31c514b59a9eb2ee050ccd89868a191.

## Final title

`同样叫“第一次降息”，为什么历史上的市场路径差这么多？`

## Final cover copy

Primary:
- line 1: `同样是第一次降息`
- line 2: `为什么市场路径完全不同？`
- kicker: `1995 / 2001 / 2007 / 2019 / 2024`

No return number appears on the cover.

## Final hook

Use RC1 Hook A only:

`同一个 FIRST_CUT 标签，2001、2007、2019、2024走出了完全不同的资产路径。`

Do not use Hook B in the first release.

Reason:
Hook B is numerically valid but editorially ambiguous because it states 2001 Nasdaq -25.6% and then 2024 +28.5% without repeating that the second number is also Nasdaq. 031 prohibits this ambiguity in release copy.

## Frozen 72-second sequence

1. 00-07s — hook
2. 07-18s — 1995 / S&P 500 +19.4% / FIG-CASE-B03
3. 18-29s — 2001 / Nasdaq -25.6%, MDD 40.8% / FIG-CASE-B04
4. 29-40s — 2007 / S&P 500 -16.3%, Gold +24.8% / FIG-CASE-B05
5. 40-51s — 2019 / S&P 500 +11.0%; 2024 / S&P 500 +20.2% / FIG-CASE-B06 then FIG-CASE-B07
6. 51-62s — synthesis: same policy label can coexist with different macro/financial conditions and later shocks
7. 62-72s — boundary: historical cases are not a current prediction template

## Vertical composition spec

Canvas:
- 1080x1920;
- title-safe top area: y=120-360;
- evidence panel area: y=420-1320;
- subtitle-safe area: y=1390-1650;
- source/boundary area: y=1670-1840.

Evidence figures are existing 16:9 renders embedded without removing their source/footer metadata.

No new visual interpretation may be added through arrows, signal colors, rankings or “winner/loser” labels.

## Subtitle requirements

Generate deterministic SRT:
- one subtitle cue per shot;
- timing exactly inherits 028 shot boundaries;
- no factual wording change;
- line wrapping is editorial only;
- final cue contains the non-prediction boundary.

## Final caption

Caption must:
- state the historical-case framing;
- name the compared assets when giving numbers;
- distinguish endpoint return from path risk;
- state that cases are not a current-cycle forecast;
- include the mandatory educational/investment boundary.

## Pinned comment

Must state:
- data are historical case paths;
- figures and claims are tied to the public research repository;
- later shocks are not backfilled into earlier policy reasoning;
- no current analog ranking or trade instruction is implied.

## Hashtags

Allowed neutral topical tags only:
- #美联储
- #降息周期
- #宏观研究
- #美股
- #黄金
- #金融市场

No action-oriented investment hashtag.

## Frozen outputs

- FINAL_RELEASE_COPY_ZH.md
- FINAL_COVER_SPEC_ZH.md
- VERTICAL_STORYBOARD_9X16.csv
- CNT02_FINAL_SUBTITLES_ZH.srt
- FINAL_CAPTION_AND_PINNED_COMMENT_ZH.md
- FINAL_ASSET_SEQUENCE.csv
- RELEASE_MANIFEST.json
- AMBIGUITY_AUDIT.csv
- QC.json
- FED_CYCLE_CNT02_FINAL_PUBLISHING_RC_031_REPORT.md

## QC gates

PASS requires:

1. upstream 030 CNT-02 = GO_RC1;
2. publication remains NOT_PUBLISHED;
3. immutable evidence hash exact match;
4. final title exact match;
5. final hook = RC1 Hook A;
6. Hook B not used in final release copy;
7. ambiguity audit identifies Hook B as valid-data-but-ambiguous;
8. exactly seven storyboard rows;
9. storyboard duration = 72 seconds;
10. exact 028 timing inherited;
11. exactly seven SRT cues;
12. final SRT cue contains the boundary;
13. B03/B04/B05/B06/B07 render refs all present;
14. every numeric statement is traceable to 022B/028;
15. no buy/sell CTA;
16. no best-asset ranking;
17. no current-analog ranking;
18. no deterministic bottom/forecast;
19. no political evaluation of Fed actors;
20. no new inference/p-values;
21. private-paper inputs = false;
22. causal status = NONE;
23. deployment status = NOT_DEPLOYABLE.

## Interpretation boundary

031 creates a final editorial production candidate.

It is ready for human/platform rendering and publication workflow, but it is not itself a publication action and it does not create an investment recommendation.
