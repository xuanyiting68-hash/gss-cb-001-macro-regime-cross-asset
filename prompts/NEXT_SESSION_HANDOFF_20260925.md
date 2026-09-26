# NEXT SESSION HANDOFF — Public PandaAI / Macro Research
Date: 2026-09-25
Repository: https://github.com/xuanyiting68-hash/gss-cb-001-macro-regime-cross-asset

## Authoritative-state rule

Treat the latest GitHub `main` as the only authoritative state.

Canonical 019 closeout + handoff commit:

`c887905a128360c8a5735f4c7b0127b9689576c8`

The metadata update containing this line is necessarily newer than that commit. Always read the actual latest `main` first; latest `main` overrides every SHA written inside a handoff.

Do not reconstruct state from old chats, ZIPs, local notes or this handoff if GitHub has moved.

## Read first

1. `README.md`
2. `AGENTS.md`
3. `docs/CURRENT_STATE.md`
4. `docs/RESEARCH_PROTOCOL.md`
5. `docs/PAPER_FIREWALL.md`
6. `docs/EVIDENCE_LEDGER.csv`
7. `docs/CHANGELOG.md`
8. `docs/FILE_MANIFEST.csv`
9. `research/FED_CYCLE_TOTAL_RISK_CLOCK_017_CLOSEOUT.md`
10. `research/FED_CYCLE_STRESS_TROUGH_ALIGNMENT_018_CLOSEOUT.md`
11. `research/FED_CYCLE_PRECUT_STATE_019_CLOSEOUT.md`
12. `research/FED_CYCLE_PRECUT_STATE_019_V1_1_SUPPORT_AMENDMENT.md`

## Latest completed research chain

### 015 — recovery extension
Added TLT/VNQ/BTC/DXY/housing recovery clocks with recovery-risk-set support correction.

Key boundary:
- DXY recovery supported across all four phases;
- housing supported only at LAST_HIKE;
- TLT/VNQ/BTC remain limited.

### 016 — supported recovery map
Fully supported four-phase assets:
- DXY;
- GOLD;
- NASDAQ;
- SP500;
- WTI.

Post-trough full recovery after FIRST_CUT is not universally faster than PAUSE.

### 017 — total risk clock
Event-level anchor -> trough -> full prior-peak recovery.

Full-recovery medians for FIRST_HIKE / LAST_HIKE / PAUSE_START / FIRST_CUT:
- DXY: 17 / 15 / 13 / 13m;
- GOLD: 30 / 11 / 15 / 22m;
- NASDAQ: 14 / 11 / 10 / 15m;
- SP500: 12 / 12 / 14 / 14m;
- WTI: 12 / 29 / 17 / 20m.

FIRST_CUT vs PAUSE:
- slower 3/5;
- equal 2/5;
- faster 0/5.

This is descriptive, not a causal rate-cut effect.

### 018 — FIRST_CUT stress/trough timing
Ex-post timing alignment:
- Nasdaq/S&P MDD trough month equals maximum VIX-stress month in 5/5 modern paired episodes;
- equity Baa/copper stress is generally within ~1-2 months;
- WTI also aligns closely;
- Gold is a timing exception and often troughs before the later stress maximum.

Important:
both stress peak and trough are future-window statistics. 018 is mechanism timing, not a live bottoming signal.

### 019 — predetermined pre-cut state diagnostic
Uses:
- real-time RTDSM IPT growth;
- pre-cut 10Y–2Y curve;
- pre-cut NFCI;
- SP500/NASDAQ/WTI late-trough breadth.

Final v1.1 conclusion:

**SIMPLE PRE-CUT STATE RULE NOT SUPPORTED.**

Independent broad-episode support:
- RT growth contraction: 0 True / 6 False -> insufficient variation;
- curve inversion: 3 True / 3 False -> supported balanced, but median trough month is 8 in both groups and median late-trough share is 1 in both;
- NFCI > 0: 1 True / 5 False -> insufficient variation.

Composite PRE_CUT_STRESS_COUNT has negative rank correlation with late troughs, but component sensitivity shows this is largely driven by the single NFCI-tight broad episode:
- full rho for trough month about -0.636;
- drop NFCI about -0.127;
- NFCI-only about -0.674.

Do not promote the composite score.

## Energy prospective track remains armed, not matured

Do not disturb the frozen prospective chain:
- ENERGY005 current event remains the immutable 2026-09-23 TIGHT_OR_MIXED event;
- 008 outcome maturation is append-only;
- 009 mechanism confirmation is append-only;
- 010 PortWatch resolution is append-only;
- 012/012A analog benchmark is frozen;
- 013 prospective issuance chain remains armed.

Use future data only through the frozen append-only rules.

## Recommended next task

Do not immediately fit a prediction model on six broad FIRST_CUT episodes.

If continuing the Fed-cycle mechanism line, the next candidate is:

### FED-CYCLE-PRECUT-STRESS-LEVEL-020

Goal:
test whether **continuous pre-anchor stress levels** contain more descriptive information than the failed binary 019 states.

Candidate predetermined inputs:
- Baa–10Y spread level at/before FIRST_CUT;
- VIX level where supported;
- 10Y–2Y curve level;
- real-time RTDSM IPT YoY.

Rules:
- freeze exact specification before running;
- use only observations available before FIRST_CUT;
- no threshold search;
- no p-value fishing;
- preserve broad-episode dependence;
- classify as EXPLORATORY / MECHANISM-HYPOTHESIS because variable selection follows 018/019;
- do not call it forecasting without a separate time-ordered OOS design;
- if support/composition remains weak, stop the branch rather than add variables.

A reasonable alternative is to stop the explanatory branch now and prioritize the prospective append-only energy/Fed issuance systems as new observations mature.

## Public/private firewall

Do not move into this public repository:
- unpublished private reaction-function panel;
- exact private Tealbook/staff FFR paths;
- private S6D.3 results;
- restricted raw data;
- private correspondence.

## GitHub workflow rule

For every QC-passed public-safe milestone:
- commit reproducible protocol/code/derived outputs;
- update `docs/CURRENT_STATE.md`;
- update `docs/EVIDENCE_LEDGER.csv`;
- update `docs/CHANGELOG.md`;
- update `docs/FILE_MANIFEST.csv`;
- read GitHub back after the commit.

Preserve null results and failed hypotheses.

## Post-handoff update — 020 completed

The earlier recommendation to run 020 is now superseded.

FED-CYCLE-PRECUT-STRESS-LEVEL-020 status:

**QC PASS / CONTINUOUS PRE-CUT LEVEL RULE NOT SUPPORTED / BRANCH STOP.**

Key facts:
- 8 mechanical cycles / 6 broad episodes;
- VIX support = 5 broad episodes;
- full-sample trough-month rho: Baa +0.075, VIX -0.211, curve stress +0.029, real-time growth stress -0.177;
- every full-sample predictor fails composition robustness;
- late-trough share has only two unique values and is constant in the VIX sample;
- the stronger B03-B07 curve result is sample-composition sensitive and disappears when B02 is restored.

Do not add variables or fit a multivariate FIRST_CUT timing score on this sample.

Updated next priority:
1. prospective append-only evidence maturation in the already-frozen Fed/energy registries;
2. evidence-linked PandaAI risk-distribution integration rather than deterministic timing signals;
3. never reuse consumed OOS-008 B04-B07 evidence to tune M3.

## Post-handoff update — 021 completed

FED-CYCLE-CROSS-ASSET-MASTER-SYNTHESIS-021 is now complete and QC-passed.

Canonical outputs:
- 52 price-asset x phase rows / 13 assets;
- 12 policy/rate/cash context rows;
- 12 stress-context rows;
- machine-readable PandaAI risk-distribution reference;
- five fully supported four-phase core assets: DXY, GOLD, NASDAQ, SP500, WTI.

The synthesis introduces no new estimation or inference. Preserve upstream support labels. TLT/VNQ/BTC remain limited; Asia remains diagnostic; housing retains its slow-moving 24M ontology.

FIRST_CUT is now especially content-ready because 021 puts endpoint, interim drawdown, trough timing and total recovery on one row. Do not infer that positive +12M endpoints mean risk ended at the cut.

019 and 020 remain negative timing-rule guardrails. Do not fit a new small-sample FIRST_CUT score.

Updated next priority:
1. **022 Historical Fed Cycle Casebook** — episode timelines for representative cycles, with real-time-vs-ex-post separation;
2. prospective append-only maturation of already-frozen Fed/energy registries when their gates genuinely become eligible;
3. after 022, build the content evidence/claim registry and reusable chart library from 021 + casebook evidence.

## Post-handoff update — 022 completed

FED-CYCLE-HISTORICAL-CASEBOOK-022 is complete and QC-passed.

Primary cases: B02-B07. B02 is COMPOSITE_MULTI_LEG with three preserved mechanical sub-cycles; B03-B07 are single-cycle cases.

Canonical 022 outputs separate:
- policy chronology;
- REALTIME_KNOWABLE pre-cut context from 019;
- DESCRIPTIVE_PATH asset/rate/cash outcomes;
- EXPOST_ONLY stress/trough alignment from 018.

Counts: 30 policy rows, 120 asset-phase rows, 8 real-time pre-cut rows, 72 ex-post alignment rows, 90 rate/cash rows.

Do not use 022 to claim causal Fed effects or to select a current analog. 019/020 remain negative timing-rule guardrails.

Updated next priority:
1. **022A Historical Context Registry** — independently source recession/macro/stress/policy-context facts and tag contemporaneous vs hindsight;
2. then build a Claim Registry + Figure Registry + Content Evidence Library from 021 + 022/022A;
3. maintain prospective Fed/energy registries append-only under frozen gates.

## Post-handoff update — 022A completed

FED-CYCLE-HISTORICAL-CONTEXT-022A is complete and QC-passed.

Coverage: 18 official-source context claims across B02-B07 and 21 normalized source links.

Anti-hindsight rules are now machine-checked: 2001/2007 recession dating is retrospective; September 11 is post-Jan-2001; COVID is post-Jul-2019; current B07 NBER status is as-of audit only.

022 remains canonical for policy chronology/asset metrics; 022A is context enrichment only.

Updated next priority:
1. **022B Content Claim Registry** from 021 + 022 + 022A, with stable CLAIM_ID, exact wording, support/sample, source modules, evidence-time, allowed/prohibited wording, figure dependency and freshness rule;
2. **023 Real-Time Regime Dashboard** for current state versus historical distributions without current-cycle analog overclaiming;
3. then Figure Registry + Content Evidence Library / Myth-vs-Evidence packages.

## Post-handoff update — 022B completed

FED-CYCLE-CONTENT-CLAIM-REGISTRY-022B is complete and QC-passed.

47 canonical claims now form the reusable publishing/PandaAI evidence layer:
- 20 core asset-phase claims;
- 6 historical case claims;
- 18 official-source context claims;
- 2 negative timing-rule guardrails;
- 1 FIRST_CUT-vs-PAUSE recovery synthesis.

Six content-routing packs are frozen. Hooks/titles may vary later, but factual payloads should resolve to stable CLAIM_IDs.

Do not change 019/020 negative conclusions; do not select a current analog or create an asset ranking from the registry.

Updated next priority:
1. **023 Real-Time Regime Dashboard** — release-aware current policy/macro/market observables + historical-distribution links + freshness/uncertainty; no single-analog selection;
2. Figure Registry keyed to the 022B figure IDs;
3. Content Evidence Library / Myth-vs-Evidence production packages.

## Post-handoff update — 023 completed

FED-CYCLE-REALTIME-REGIME-DASHBOARD-023 is complete and QC-passed.

Snapshot: 2026-09-25 16:08 Australia/Sydney.

Current prospective Fed state remains `EDGE_TIGHTENING_CANDIDATE__NOT_YET_QUALIFIED`: 1 hike / 25bp since 2026-09-16, target 3.75%-4.00%, frozen >=2 hikes and >=50bp gate still false, zero prospective prediction rows.

Current release-aware observables include EFFR, 2Y/10Y, 5Y/10Y breakevens, VIX, Baa-10Y spread, NFCI, unemployment, industrial production and headline/core PCE. Derived curve = +26bp NON_INVERTED; NFCI = LOOSER_THAN_AVERAGE; PCE/core PCE both >2%; INDPRO YoY positive.

023 links five FIRST_HIKE 022B asset distribution claims plus the 019/020 timing-rule guardrails. It generates no closest analog, similarity score, asset ranking or forecast.

Updated next priority:
1. **024 Figure Registry and Visual Evidence Specs** keyed to 022B `figure_key` values;
2. reusable visual/chart generation for the six content packs;
3. Content Evidence Library / Myth-vs-Evidence production assets;
4. keep prospective Fed/energy chains append-only and fail-closed.

## Post-handoff update — 024 completed

FED-CYCLE-FIGURE-REGISTRY-024 is complete and QC-passed.

48 unique visual specs now exist: 47 map 1:1 from 022B CLAIM_ID figure keys and one is the supplemental current 023 regime snapshot.

Families: 20 phase cards, 6 case timelines, 18 context cards, 2 method guardrails, 1 recovery synthesis, 1 current snapshot. Production tiers: P0=13/P1=22/P2=13.

P0 is frozen to five FIRST_CUT core-asset cards, FIRST_CUT-vs-PAUSE recovery, 019/020 guardrails, B04-B07 cases and the current 023 snapshot.

Do not add analog scores, rankings, forecasts or signal colors. Context timing and freshness must remain visible.

Updated next priority:
1. **025 P0 Visual Evidence Pack** — render the 13 P0 specs reproducibly with claim/source linkage and render QC;
2. then build platform-specific 16:9 / 1:1 content packages from the same canonical figures;
3. maintain prospective Fed/energy chains append-only and fail-closed.

## Post-handoff update — 025 completed

FED-CYCLE-P0-VISUAL-EVIDENCE-PACK-025 is complete and QC-passed.

The frozen 13-figure P0 queue is now rendered into 39 canonical artifacts: 13 SVG_RESEARCH, 13 PNG_16_9 (1600x900) and 13 PNG_1_1 (1200x1200). Every render and actual input source has SHA256 provenance.

Automated visual-boundary checks pass: B04 9/11 and B06 COVID stay POST_ANCHOR_SHOCK; current 023 figure shows qualification FALSE/no-analog; 019/020 contain no BUY/SELL leakage; no analog score/ranking/forecast exists.

The connector cannot directly return binary PNG bodies for manual pixel review; do not claim such a review unless performed through another supported rendering surface. SVG text and file/dimension/hash integrity are audited.

Updated next priority:
1. **026 Content Production Library** from 022B claims + 025 figures;
2. platform-ready short/long content packages that preserve CLAIM_ID/FIGURE_KEY/source/caveat linkage;
3. prospective Fed/energy registries remain append-only and fail-closed.

## Post-handoff update — 026 completed

FED-CYCLE-CONTENT-PRODUCTION-LIBRARY-026 is complete and QC-passed.

Six canonical Chinese production packages now exist. Each contains three hooks, a 60-90s short-video script, long-form outline, CLAIM_ID/FIGURE_KEY/source/caveat/freshness linkage. Five are READY_P0_VISUAL; 1987 multi-leg remains TEXT_READY_VISUAL_PENDING_P1 because FIG-CASE-B02 is not yet rendered.

All numeric content is derived from canonical claim payload/wording. Six of six scripts explicitly say historical evidence is not current prediction. No buy/sell, deterministic bottom, closest-analog, best-asset or unsupported causal claim is generated.

Updated next priority:
1. **027 P1 Visual Completion + Publishing Matrix** — render B02/B03 + five priority hindsight/context cards, then map packages to Douyin/TikTok, Xiaohongshu, WeChat/long-form and PandaAI;
2. keep CLAIM_ID / FIGURE_KEY / freshness / caveat controls intact across platform adaptations;
3. append a new current-regime snapshot only when genuinely new releases or Fed actions materially change 023;
4. prospective Fed/energy chains remain append-only and fail-closed.

## Post-handoff update — 027 completed

FED-CYCLE-P1-VISUAL-PUBLISHING-MATRIX-027 is complete and QC-passed.

Seven P1 figures are now rendered in 21 artifacts: B02, B03, 2001 retrospective dating, 9/11 post-anchor shock, 2007 retrospective dating, 2020 retrospective dating and COVID post-anchor shock.

The final corrected publishing matrix has 24 rows = six content packages x four channels. New P1 visuals are routed into the relevant rows: CNT-02 includes B03, CNT-04 includes all five hindsight cards and CNT-06 includes B02.

All six packages are VISUAL_COMPLETE_FOR_CANONICAL_PACKAGE. Douyin/TikTok remains script/evidence ready but no finished 9:16 composition is claimed.

Updated next priority:
1. **028 Platform-Native Production Pack** — 9:16 shot/subtitle plans, Xiaohongshu final carousel copy, complete WeChat/deep-article drafts and PandaAI explanation templates;
2. keep every output linked to CLAIM_ID / FIGURE_KEY / freshness / caveat metadata;
3. append new current-state snapshots only on genuine new data/policy changes;
4. prospective Fed/energy chains remain append-only and fail-closed.

## Post-handoff update — 028 completed

FED-CYCLE-PLATFORM-NATIVE-PRODUCTION-PACK-028 is complete and QC-passed.

Six canonical packages now have platform-native production assets: 42 Douyin/TikTok timed shots, 42 Xiaohongshu cards, six complete Chinese deep-article drafts and six PandaAI explanation templates. All evidence remains linked to canonical claims/figures/freshness rules.

The first 028 run failed because a negated sentence contained a prohibited analog-ranking phrase; wording was corrected without weakening QC. Final workflow passed. No final MP4 is claimed and nothing has been published automatically.

The project is now editorial-production ready. Updated next priority:
1. **029 Editorial Release Candidate + Content Calendar** — freeze one release candidate per package, platform-specific cover/caption/figure sequence, publishing cadence and preflight checklist;
2. separate A/B hook testing from immutable factual payload;
3. add post-publication performance-log schema without modifying research claims;
4. append new current-state snapshots only on genuine new releases/policy actions;
5. prospective Fed/energy chains remain append-only and fail-closed.

## Post-handoff update — 029 completed

FED-CYCLE-EDITORIAL-RELEASE-CANDIDATE-029 is complete and QC-passed.

Six RC1 release candidates now freeze immutable evidence hashes while allowing only editorial packaging A/B changes. The final calendar has six unique primary release slots across weeks 1-3, zero date collisions, and week 4 repurpose placeholders. CNT-04 requires re-verification before release.

Preflight checklist, editorial A/B rules and performance-log schema are frozen. Normal editorial experiments must keep evidence_payload_changed = FALSE.

The public project now has an end-to-end chain from research to claim registry to figures to platform-native production to release control.

Updated next priority:
1. execute per-release preflight and publishing workflow;
2. create **030 Current-Cycle Topical Brief** only when new current data/policy genuinely change 023, or when a time-sensitive current explainer is explicitly needed;
3. use performance data to improve packaging only, never to rewrite empirical claims;
4. prospective Fed/energy registries remain append-only and fail-closed.

## Post-handoff update — 030 completed

FED-CYCLE-RELEASE-PREFLIGHT-030 is complete and QC-passed.

All six RC1 objects pass internal integrity. CNT-02 SAME_LABEL_DIFFERENT_PATHS is GO_RC1 for the 2026-09-28 primary release, with exact immutable evidence hash, seven-shot plan and five rendered 16:9 case figures bundled; publication status remains NOT_PUBLISHED.

CNT-04 HINDSIGHT_TRAPS remains HOLD_REVERIFY for 2026-10-01 because the current NBER chronology claim must be re-audited near release. Do not promote it before that external check. The other four RCs are READY_NOT_DUE.

Updated next priority:
1. execute final editorial/platform preflight for CNT-02 close to 2026-09-28 and publish only on explicit user request through an available platform workflow;
2. re-audit the official NBER chronology near 2026-10-01 before releasing CNT-04;
3. preserve immutable evidence hashes through all editorial packaging;
4. append current-state snapshots only when genuine new data/policy changes occur;
5. prospective Fed/energy chains remain append-only and fail-closed.

## Post-handoff update — 031 completed

FED-CYCLE-CNT02-FINAL-PUBLISHING-RC-031 is complete and QC-passed.

The 2026-09-28 CNT-02 first-release package is now finalized as GO_RC1 / NOT_PUBLISHED: exact title, non-numeric cover, Hook A, seven-shot 72-second 9:16 storyboard, B03-B07 evidence sequence, seven-cue Chinese SRT, final caption and pinned comment. Immutable evidence hash is unchanged.

Hook B is data-valid but editorially ambiguous because its 2024 +28.5% value is Nasdaq while the second asset label is omitted; it is prohibited for the first release. Final copy explicitly names assets.

Subtitle handling was hardened after QC/readback caught numeric-token truncation. Final SRT preserves +20.2% exactly and no text truncation is allowed.

Updated next priority:
1. do not add more retrospective timing-rule research to this branch;
2. on/near 2026-09-28, run same-day integrity/pre-publication check for CNT-02 and publish only on explicit user instruction through an available platform workflow;
3. re-audit NBER near 2026-10-01 before promoting CNT-04 from HOLD_REVERIFY;
4. preserve immutable evidence hashes through all compositing and publication steps;
5. prospective Fed/energy registries remain append-only and fail-closed.

## Post-handoff update — 032 completed

FED-CYCLE-FOUR-PHASE-INVESTOR-ATLAS-032 is complete and QC-passed.

The project now has a four-phase investor knowledge atlas across 20 core asset-phase rows, 12 rates/cash rows, 12 stress rows and 32 extension/diagnostic rows, plus 20 evidence-linked investor questions and 12 myth audits.

Key descriptive synthesis: FIRST_HIKE can show weak 3M equity medians but positive 12M endpoints; LAST_HIKE/PAUSE can show falling Treasury yields while cash carry stays high; FIRST_CUT can show positive 12M equity endpoints while drawdowns/troughs/stress remain materially adverse. BTC/TLT/VNQ stay LIMITED, Asian equities DIAGNOSTIC, housing uses a separate 24M clock.

Updated research priority:
1. **033 Gold Mechanism Decomposition** — Gold vs real yields, DXY, breakevens/inflation expectations and financial stress by phase and historical case;
2. preserve association/causal boundaries and avoid fitting a trading score unless separately pre-registered;
3. after Gold, evaluate housing lag-chain and longer-history proxies for TLT/VNQ/BTC;
4. current-state/prospective Fed and energy chains remain append-only and fail-closed.

## Post-handoff update — 033 completed

FED-CYCLE-GOLD-MECHANISM-DECOMPOSITION-033 is complete and QC-passed.

The public Gold evidence now has a multi-mechanism map covering Fed phase, inflation level/direction, growth, energy, USD, real-rate proxy/DFII10, NFCI and stress timing, with five frozen external-literature context rows. The evidence does not justify a single dominant Gold driver.

Important guardrails: USD remains secondary/no FDR survivor; DFII10 remains INSUFFICIENT_SUPPORT; no inverse real-rate rule is asserted; inflation level and direction stay separate; Gold stress timing is ex-post and not a safe-haven entry signal.

Updated next priority:
1. **034 Housing Lag Chain** — policy/rates/mortgage rates -> housing activity -> house prices -> recovery timing;
2. keep housing on its slow-moving 24M clock and do not compare DECLINE_24M with traded-asset MDD;
3. after housing, evaluate longer-history bond/REIT proxies and Asia local-policy/USD/credit mechanisms;
4. current-state/prospective Fed and energy chains remain append-only and fail-closed.

## Post-handoff update — 034 completed

FED-CYCLE-HOUSING-LAG-CHAIN-034 is complete and QC-passed.

034 adds MORTGAGE30US, DGS10, HOUST, PERMIT and HSN1F to the canonical national house-price layer. House-price values remain exactly the 014/015 Case-Shiller results and risk remains DECLINE_24M.

Key result: housing sequencing is phase-dependent, not a universal fixed lag chain. A post-run diagnostic amendment was added transparently after the first successful run showed phase-median subtraction can misrepresent episode ordering. The absolute mortgage peak in [-12,+24] precedes/same-month as activity trough in weighted shares of 67% FIRST_HIKE and 100% LAST_HIKE/PAUSE/FIRST_CUT, but activity-before-price ordering is only 57%-77% among positive-decline episodes.

B05 and B07 are separately auditable: 2004-07 becomes a deep housing bust later in the cycle, while 2022-23 combines a much larger mortgage-rate shock and activity contraction with resilient national prices.

Updated next priority:
1. longer-history long-duration Treasury proxy bridge beyond TLT inception, with overlap validation before any evidence inheritance;
2. then longer-history real-estate/REIT proxy if a defensible public series exists;
3. Bitcoin remains structurally short-history and should be handled through mechanism/liquidity research rather than pretending a long Fed-cycle sample exists;
4. current-state/prospective Fed and energy chains remain append-only and fail-closed.

## Post-handoff update — 035 completed

FED-CYCLE-LONG-TREASURY-PROXY-BRIDGE-035 is complete and QC-passed with BRIDGE_PASS_SUPPORTED_PROXY_EXTENSION.

VUSTX was validated as a separately labeled long-duration Treasury proxy against TLT: 289 monthly overlap returns, Pearson 0.991, Spearman 0.993, descriptive beta 0.874; common-event 12M direction agreement 100%, return correlation 0.995 and MDD correlation 0.999. All frozen bridge gates pass.

The proxy extends descriptive duration evidence to 1987+ without relabeling VUSTX as TLT. Extended proxy medians: FIRST_HIKE +1.0% 12M / 10.7% MDD; LAST_HIKE +9.9%; PAUSE +15.1%; FIRST_CUT +6.0%. All remain historical distributions, not forecasts.

Updated next priority:
1. **036 Listed REIT Long-History Proxy Bridge** — seek a defensible pre-VNQ listed-REIT proxy and apply the same overlap-first gate structure;
2. if the bridge passes, extend REIT phase evidence while retaining proxy identity;
3. if it fails, keep VNQ LIMITED_DESCRIPTIVE rather than weakening standards;
4. Bitcoin remains short-history and should be deepened through mechanism/liquidity research, not synthetic historical backfill.
