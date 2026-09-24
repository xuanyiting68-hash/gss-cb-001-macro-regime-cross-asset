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
