# NEXT SESSION HANDOFF — Public PandaAI / Macro Research
Date: 2026-09-25
Repository: https://github.com/xuanyiting68-hash/gss-cb-001-macro-regime-cross-asset

## Authoritative-state rule

Treat the latest GitHub `main` as the only authoritative state.

At handoff creation, the latest research result commit before canonical closeout is:

`d60e38b60f82571347ea380de01c6daa33268f15`

A later canonical-closeout/handoff commit will supersede it. Always read the actual latest `main` first.

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
