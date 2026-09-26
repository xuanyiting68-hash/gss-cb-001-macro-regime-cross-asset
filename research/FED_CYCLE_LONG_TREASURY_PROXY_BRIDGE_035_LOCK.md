# FED-CYCLE-LONG-TREASURY-PROXY-BRIDGE-035 — LOCK

Date locked: 2026-09-26

## Purpose

Test whether Vanguard Long-Term Treasury Fund Investor Shares (VUSTX) can serve as a longer-history **proxy** for the public project's TLT duration layer.

VUSTX began in 1986, while TLT begins in 2002.

035 must first validate the overlap. Historical extension is allowed only if frozen bridge gates pass.

No evidence is inherited automatically from TLT.

## Assets

### Target
TLT
- iShares 20+ Year Treasury Bond ETF
- adjusted-close total-return proxy in 014
- history begins 2002-07-30

### Candidate proxy
VUSTX
- Vanguard Long-Term Treasury Fund Investor Shares
- long-term U.S. Treasury mutual fund
- official inception: 1986-05-19
- adjusted-close history acquired through the same Yahoo chart interface used by 014

The proxy must always be labeled:
`VUSTX_LONG_TREASURY_PROXY`

Never relabel pre-2002 VUSTX history as TLT.

## Acquisition

Fetch fresh same-run adjusted-close histories for:
- TLT
- VUSTX

Use Yahoo public chart JSON and record:
- URL
- retrieved timestamp
- raw SHA256
- bytes
- first/last date
- adjusted-close field

Do not commit raw histories.

## Monthly transform

Exactly match 014:
- calendar-month average of daily adjusted close.

Monthly return for overlap validation:
`monthly_avg_t / monthly_avg_{t-1} - 1`

## Frozen overlap window

Use all complete matched months from the later first-available month through the last complete calendar month.

Do not use an incomplete current month in bridge statistics.

## Frozen bridge gates

All gates must pass for:
`BRIDGE_PASS_SUPPORTED_PROXY_EXTENSION`

Otherwise:
`BRIDGE_FAIL_NO_HISTORY_EXTENSION`

### G1 — overlap depth
- matched monthly return observations >= 240

### G2 — monthly co-movement
- Pearson correlation >= 0.95
- Spearman correlation >= 0.95

### G3 — scale similarity
OLS-style descriptive slope:
`VUSTX monthly return ~ beta * TLT monthly return + intercept`

- beta in [0.75, 1.25]
- |intercept| <= 0.0025 monthly return

No causal interpretation.

### G4 — common-event endpoint agreement

Using frozen Fed phase anchors for which both assets have full +12M coverage:
- 12M return sign agreement >= 85%
- Pearson correlation of event 12M returns >= 0.90
- median absolute event 12M return difference <= 0.05

### G5 — common-event path-risk agreement
- Pearson correlation of 12M MDD >= 0.80
- median absolute MDD difference <= 0.04

### G6 — phase-summary agreement

On the exact common-event sample:
- four phase rows required;
- phase 12M direction must agree, with values inside +/-2% treated as NEUTRAL;
- median absolute phase 12M-return difference <= 0.04;
- maximum absolute phase 12M-return difference <= 0.07.

## Extension if bridge passes

Compute VUSTX proxy metrics on the full frozen historical cycle map:

- FIRST_HIKE
- LAST_HIKE
- PAUSE_START
- FIRST_CUT

Metrics exactly parallel 014:
- +3M return
- +6M return
- +12M return
- 12M MDD
- MDD trough month
- late-trough share

Use broad-episode weights exactly as the frozen cycle design.

Support label:
- if >=5 legs and >=4 broad episodes: `SUPPORTED_PROXY_DESCRIPTIVE`
- if >=2 broad episodes: `LIMITED_PROXY_DESCRIPTIVE`
- otherwise: `INSUFFICIENT_SUPPORT`

This support belongs to the **VUSTX proxy**, not TLT.

## Additional 24M diagnostic

If +24M data are available for an event:
- +24M return
- 24M MDD
- 24M trough month

This is a secondary descriptive extension and must not change bridge status.

## Frozen outputs

- SOURCE_REGISTRY.csv
- MONTHLY_OVERLAP_DIAGNOSTICS.csv
- COMMON_EVENT_BRIDGE_PANEL.csv
- COMMON_PHASE_BRIDGE_SUMMARY.csv
- BRIDGE_GATE_AUDIT.csv
- VUSTX_EXTENDED_PHASE_METRICS.csv
- VUSTX_EXTENDED_PHASE_SUMMARY.csv
- VUSTX_24M_DIAGNOSTICS.csv
- LONG_TREASURY_INVESTOR_QUESTIONS.csv
- LONG_TREASURY_SYNTHESIS_ZH.md
- PANDAAI_LONG_TREASURY_SCHEMA.json
- FED_CYCLE_LONG_TREASURY_PROXY_BRIDGE_035_REPORT.md
- QC.json

## QC gates

PASS requires:

1. source hashes for both TLT and VUSTX;
2. VUSTX first history date consistent with 1986 inception era;
3. last bridge month is complete, not partial current month;
4. common-event anchor map is frozen project map;
5. no current 2026 candidate;
6. all six frozen bridge gate families evaluated;
7. bridge pass/fail is deterministic from frozen thresholds;
8. if bridge fails, no extended evidence is promoted;
9. if bridge passes, asset remains labeled VUSTX_LONG_TREASURY_PROXY;
10. no pre-2002 data are labeled TLT;
11. yield-change evidence is not substituted for total-return evidence;
12. no best phase;
13. no expected-return forecast;
14. no bond-buying recommendation;
15. no new p-values/inference;
16. private-paper inputs = false;
17. causal status = NONE;
18. OOS status = NOT_A_FORECASTING_MODEL;
19. deployment status = NOT_DEPLOYABLE.

## Interpretation boundary

035 is a measurement/proxy validation exercise.

A passing bridge means VUSTX provides a defensible longer-history **duration proxy** for descriptive Fed-cycle research. It does not make VUSTX and TLT identical instruments.
