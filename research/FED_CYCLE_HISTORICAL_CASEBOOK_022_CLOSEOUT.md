# FED-CYCLE-HISTORICAL-CASEBOOK-022 — CLOSEOUT

Date: 2026-09-25

## Final status

**QC PASS / SIX-EPISODE HISTORICAL CASEBOOK / EVIDENCE-LINKED / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

022 converts the existing public Fed-cycle research chain into a case-oriented evidence base for PandaAI and media production. It introduces no new price estimation, statistical inference, threshold search or predictive fitting.

## Primary case universe

- B02 — 1987-1989 tightening/easing sequence — 3 mechanical sub-cycles
- B03 — 1994-1995 tightening/easing cycle
- B04 — 1999-2001 tightening/easing cycle
- B05 — 2004-2007 tightening/easing cycle
- B06 — 2015-2019 tightening/easing cycle
- B07 — 2022-2024 tightening/easing cycle

B02 is deliberately preserved as a composite multi-leg episode. It is not compressed into a fictitious single policy path.

## Canonical evidence layers

### Policy chronology
- 30 policy-sequence rows.
- Event date / source-effective-date ontology is preserved from FED-CYCLE-PATH-001-v1.1.
- Pre-1994 historical-target reconstruction is explicitly flagged.

### Asset paths
- 120 GOLD / SP500 / NASDAQ / WTI cycle x phase rows.
- Evidence time: DESCRIPTIVE_PATH.
- Returns, MDD, trough month and recovery fields remain historical path outcomes.

### Pre-FIRST_CUT context
- 8 timing-audited rows across 6 broad episodes.
- Evidence time: REALTIME_KNOWABLE.
- 10Y-2Y curve, NFCI and RTDSM IPT are shown only as predetermined context.
- 019/020 remain binding negative evidence against a deterministic bottom-timing score.

### Stress/trough alignment
- 72 pair rows.
- Evidence time: EXPOST_ONLY.
- VIX/Baa/copper stress peaks and asset troughs are explicitly future-window statistics, not live signals.

### Rates and cash
- 90 rows.
- Treasury-yield changes and mechanical cash carry remain separate metric families.
- They are not ranked directly against price returns.

## Content-ready contrasts

The casebook now supports fact-checked comparisons such as:

- 2001 FIRST_CUT: Nasdaq +12M approximately -25.6%, 12M MDD approximately 40.8%, trough month 8.
- 2007 FIRST_CUT: S&P 500 +12M approximately -16.3%, 12M MDD approximately 21.0%, trough month 12.
- 2019 FIRST_CUT: S&P 500 +12M approximately +11.0%, but 12M MDD approximately 19.1% and trough month 8.
- 2024 FIRST_CUT: S&P 500 +12M approximately +20.2%, 12M MDD approximately 11.1%, trough month 7.
- Gold often differs from equities in the same FIRST_CUT windows; in 2001 its +12M path was positive while Nasdaq/S&P were negative.

These are historical path descriptions. They do not establish that the cut caused the path and they do not identify which case is the correct analog for a current cycle.

## Why this matters for media production

022 creates a reusable story grammar:

1. policy chronology;
2. what was actually knowable before the cut;
3. what assets did afterward;
4. where the maximum drawdown occurred;
5. when stress peaked;
6. what was only visible ex post;
7. what the case does and does not imply.

This supports short video hooks, long-form case studies, timelines and comparative graphics without silently mixing hindsight with real-time information.

## Reproducibility

Workflow:
- `.github/workflows/fed-cycle-historical-casebook-v1.yml`
- run id: 36039615659
- workflow source commit: `c0c47c6aed09a5240f1adf64c914ddfc7a2eb559`
- output commit: `e4345aa4de966497a96d5e942ea452906ce8d8f9`
- result: SUCCESS

QC:
- six primary broad episodes exactly;
- B02 mechanical cycles = 3;
- B03-B07 single-cycle violations = 0;
- evidence-time nulls = 0;
- p-values generated = false;
- private-paper inputs used = false;
- causal status = NONE;
- deployment status = NOT_DEPLOYABLE.

## Next layer

Proceed to a separately sourced enrichment layer, **022A Historical Context Registry**, adding public historical macro/event context with source-level provenance.

022A must not rewrite the canonical chronology or asset outcomes. It should add context columns such as:
- recession status/dates;
- inflation/growth background;
- major financial/economic stress event labels;
- Fed-stated policy context where sourceable;
- contemporaneous versus hindsight classification;
- official/source URL and retrieval note.

After 022A, use 021 + 022/022A to construct the claim registry, figure registry and content production library.
