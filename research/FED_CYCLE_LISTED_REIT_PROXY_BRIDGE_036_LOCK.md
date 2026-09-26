# FED-CYCLE-LISTED-REIT-PROXY-BRIDGE-036 — LOCK

Date locked: 2026-09-26

## Purpose

Test whether Vanguard Real Estate Index Fund Investor Shares (VGSIX) can serve as a longer-history listed-real-estate / REIT proxy for the public project's VNQ layer.

VGSIX begins in 1996; VNQ begins in 2004.

No evidence is inherited automatically. The overlap bridge must pass frozen gates first.

## Assets

### Target
VNQ
- Vanguard Real Estate ETF
- inception 2004-09-23
- adjusted-close proxy in 014

### Candidate proxy
VGSIX
- Vanguard Real Estate Index Fund Investor Shares
- inception 1996-05-13
- publicly traded real-estate equity index-fund exposure
- adjusted-close history acquired using the same Yahoo chart interface as VNQ

Proxy identity:
`VGSIX_REIT_PROXY`

Pre-VNQ history must never be labeled VNQ.

## Important benchmark caveat

VGSIX and VNQ are related Vanguard real-estate index products but are not identical securities.

Historical benchmark/index implementations may have changed over time.

Therefore:
- overlap similarity is measured empirically;
- no same-benchmark identity is assumed;
- bridge pass authorizes descriptive proxy extension only.

## Acquisition

Fetch fresh same-run adjusted-close histories for:
- VNQ
- VGSIX

Record:
- URL
- retrieval timestamp
- SHA256
- raw bytes
- first/last date
- adjusted-close field

Do not commit raw histories.

## Monthly transform

Match 014 exactly:
- calendar-month average of daily adjusted close.

Monthly return:
`monthly_avg_t / monthly_avg_{t-1} - 1`

Exclude the incomplete current month from bridge statistics.

## Frozen bridge gates

All gates must pass for:
`BRIDGE_PASS_SUPPORTED_PROXY_EXTENSION`

Otherwise:
`BRIDGE_FAIL_NO_HISTORY_EXTENSION`

### G1 — overlap depth
- matched monthly returns >= 240

### G2 — monthly co-movement
- Pearson >= 0.97
- Spearman >= 0.97

### G3 — scale similarity
Descriptive regression:
`VGSIX monthly return ~ beta * VNQ monthly return + intercept`

- beta in [0.80, 1.20]
- |intercept| <= 0.0030

### G4 — common-event endpoint agreement

Frozen Fed phase anchors with complete +12M coverage for both assets:
- 12M return sign agreement >= 85%
- 12M event-return Pearson correlation >= 0.95
- median absolute 12M return difference <= 0.04

### G5 — common-event path-risk agreement
- 12M MDD Pearson correlation >= 0.90
- median absolute MDD difference <= 0.04

### G6 — common-sample phase agreement

All four phases required.

Direction classification:
- POSITIVE if > +2%
- NEGATIVE if < -2%
- NEUTRAL otherwise

Requirements:
- all four phase directions agree
- median absolute phase 12M-return difference <= 0.03
- maximum absolute phase 12M-return difference <= 0.06

## Extension if bridge passes

Compute VGSIX proxy metrics over the full eligible historical cycle map:

- FIRST_HIKE
- LAST_HIKE
- PAUSE_START
- FIRST_CUT

Metrics parallel 014:
- +3M
- +6M
- +12M
- 12M MDD
- MDD trough month
- late-trough share

Support:
- >=5 legs and >=4 broad episodes -> SUPPORTED_PROXY_DESCRIPTIVE
- >=2 broad episodes -> LIMITED_PROXY_DESCRIPTIVE
- otherwise -> INSUFFICIENT_SUPPORT

Support belongs only to VGSIX_REIT_PROXY.

## Secondary 24M diagnostic

Where available:
- +24M return
- 24M MDD
- 24M trough month

Secondary descriptive only.

## Frozen outputs

- SOURCE_REGISTRY.csv
- MONTHLY_OVERLAP_DIAGNOSTICS.csv
- COMMON_EVENT_BRIDGE_PANEL.csv
- COMMON_PHASE_BRIDGE_SUMMARY.csv
- BRIDGE_GATE_AUDIT.csv
- VGSIX_EXTENDED_PHASE_METRICS.csv
- VGSIX_EXTENDED_PHASE_SUMMARY.csv
- VGSIX_24M_DIAGNOSTICS.csv
- REIT_INVESTOR_QUESTIONS.csv
- REIT_PROXY_SYNTHESIS_ZH.md
- PANDAAI_REIT_SCHEMA.json
- FED_CYCLE_LISTED_REIT_PROXY_BRIDGE_036_REPORT.md
- QC.json

## QC gates

PASS requires:

1. source hashes for VNQ and VGSIX;
2. VGSIX history consistent with 1996 inception era;
3. bridge excludes incomplete current month;
4. common events inherit frozen cycle map;
5. no current 2026 candidate;
6. all frozen gate families evaluated;
7. deterministic pass/fail;
8. failed bridge cannot promote extension;
9. passing extension remains labeled VGSIX_REIT_PROXY;
10. no pre-2004 history labeled VNQ;
11. no inference from national house-price series to listed REIT total returns;
12. no best phase;
13. no expected-return forecast;
14. no REIT-buying recommendation;
15. no p-values/inference;
16. private-paper inputs = false;
17. causal status = NONE;
18. OOS status = NOT_A_FORECASTING_MODEL;
19. deployment status = NOT_DEPLOYABLE.

## Interpretation boundary

036 tests measurement compatibility between a long-history real-estate index mutual fund and the VNQ ETF.

A passing bridge supports longer-history descriptive listed-real-estate research. It does not make the vehicles identical and does not convert historical medians into forecasts.
