# FED-CYCLE-REIT-DEEP-HISTORY-DUAL-BRIDGE-037 — LOCK

Date locked: 2026-09-26

## Purpose

Test whether Fidelity Real Estate Investment Portfolio (FRESX) can provide a defensible 1986-era listed-real-estate proxy extension.

Because FRESX is actively managed, it must pass a **dual bridge**:

1. FRESX vs VNQ;
2. FRESX vs the already validated VGSIX_REIT_PROXY.

No historical evidence extension is allowed unless both bridge families pass.

## Assets

### Target ETF
VNQ
- Vanguard Real Estate ETF
- inception 2004-09-23
- canonical 014 listed-REIT ETF proxy

### High-fidelity reference proxy
VGSIX_REIT_PROXY
- Vanguard Real Estate Index Fund Investor Shares
- inception 1996-05-13
- validated against VNQ in 036
- 036 status: BRIDGE_PASS_SUPPORTED_PROXY_EXTENSION

### Deep-history candidate
FRESX_REIT_ACTIVE_PROXY
- Fidelity Real Estate Investment Portfolio
- inception 1986-11-17
- active real-estate sector fund
- Fidelity states it normally invests at least 80% in real-estate-industry and related securities
- secondary benchmark context: MSCI US IMI Real Estate 25/50 Linked

FRESX must remain explicitly labeled as an active proxy.

Pre-VNQ FRESX history must never be called VNQ.

## Why a dual bridge is required

FRESX is not an index clone.

Active security selection can introduce:
- tracking drift;
- style drift;
- idiosyncratic holdings;
- expense differences;
- benchmark-transition effects.

A direct VNQ bridge alone is not sufficient.

The longer VGSIX overlap provides a second measurement check.

## Acquisition

Fetch fresh same-run adjusted-close histories for:
- VNQ
- VGSIX
- FRESX

Record:
- URL
- retrieval timestamp
- SHA256
- raw bytes
- first/last date
- adjusted-close field

Exclude incomplete current month from all bridge statistics.

Do not commit raw histories.

## Monthly transform

Match 014 / 036:
- monthly average of daily adjusted close;
- monthly return = monthly average ratio - 1.

## Frozen dual-bridge gates

Final pass status:
`DUAL_BRIDGE_PASS_SUPPORTED_DEEP_PROXY_EXTENSION`

Any failure:
`DUAL_BRIDGE_FAIL_NO_DEEP_EXTENSION`

### A. FRESX vs VNQ

#### A1 — depth
- matched monthly returns >= 240

#### A2 — monthly co-movement
- Pearson >= 0.92
- Spearman >= 0.92

#### A3 — scale similarity
- beta in [0.70, 1.30]
- |intercept| <= 0.0040

#### A4 — common-event endpoints
- 12M sign agreement >= 80%
- event 12M-return Pearson >= 0.90
- median absolute 12M-return difference <= 0.08

#### A5 — path risk
- 12M MDD correlation >= 0.85
- median absolute MDD difference <= 0.06

#### A6 — four-phase common-sample agreement
Direction:
- POSITIVE > +3%
- NEGATIVE < -3%
- NEUTRAL otherwise

Requirements:
- all four phase directions agree
- median absolute phase 12M-return difference <= 0.06
- max absolute phase 12M-return difference <= 0.10

### B. FRESX vs VGSIX

#### B1 — depth
- matched monthly returns >= 330

#### B2 — monthly co-movement
- Pearson >= 0.92
- Spearman >= 0.92

#### B3 — scale similarity
- beta in [0.70, 1.30]
- |intercept| <= 0.0040

#### B4 — common-event endpoints
- 12M sign agreement >= 85%
- event 12M-return Pearson >= 0.90
- median absolute 12M-return difference <= 0.08

#### B5 — path risk
- 12M MDD correlation >= 0.85
- median absolute MDD difference <= 0.06

#### B6 — four-phase common-sample agreement
- all four phase directions agree under +/-3% neutral band
- median absolute phase 12M-return difference <= 0.06
- max absolute phase 12M-return difference <= 0.10

## Extension if both bridges pass

Compute FRESX_REIT_ACTIVE_PROXY over the full frozen historical cycle map.

Metrics:
- +3M
- +6M
- +12M
- 12M MDD
- MDD trough month
- late-trough share

Support:
- >=5 legs and >=4 broad episodes -> SUPPORTED_DEEP_PROXY_DESCRIPTIVE
- >=2 broad episodes -> LIMITED_DEEP_PROXY_DESCRIPTIVE
- otherwise -> INSUFFICIENT_SUPPORT

This evidence belongs to FRESX_REIT_ACTIVE_PROXY only.

## Secondary 24M layer

Where observed:
- +24M return
- 24M MDD
- trough month

Secondary descriptive only.

## Frozen outputs

- SOURCE_REGISTRY.csv
- VNQ_BRIDGE_MONTHLY.csv
- VGSIX_BRIDGE_MONTHLY.csv
- VNQ_COMMON_EVENT_PANEL.csv
- VGSIX_COMMON_EVENT_PANEL.csv
- VNQ_COMMON_PHASE_SUMMARY.csv
- VGSIX_COMMON_PHASE_SUMMARY.csv
- DUAL_BRIDGE_GATE_AUDIT.csv
- FRESX_EXTENDED_PHASE_METRICS.csv
- FRESX_EXTENDED_PHASE_SUMMARY.csv
- FRESX_24M_DIAGNOSTICS.csv
- REIT_DEEP_HISTORY_INVESTOR_QUESTIONS.csv
- REIT_DEEP_HISTORY_SYNTHESIS_ZH.md
- PANDAAI_REIT_DEEP_HISTORY_SCHEMA.json
- FED_CYCLE_REIT_DEEP_HISTORY_DUAL_BRIDGE_037_REPORT.md
- QC.json

## QC gates

PASS requires:

1. 036 upstream bridge PASS;
2. all three source hashes complete;
3. FRESX history consistent with 1986 inception era;
4. both overlap windows exclude incomplete current month;
5. all A and B frozen gates evaluated;
6. deterministic dual-pass/fail;
7. any A/B failure prevents deep-history promotion;
8. passing extension remains FRESX_REIT_ACTIVE_PROXY;
9. no pre-2004 observation labeled VNQ;
10. active-management caveat retained;
11. no national house-price substitution;
12. no best REIT phase;
13. no expected-return forecast;
14. no REIT-buying recommendation;
15. no new p-values/inference;
16. private-paper inputs = false;
17. causal status = NONE;
18. OOS status = NOT_A_FORECASTING_MODEL;
19. deployment status = NOT_DEPLOYABLE.

## Interpretation boundary

037 is a measurement-validation exercise.

A dual-bridge pass supports longer-history listed-real-estate **proxy** research. It does not convert an active mutual fund into an index ETF and does not create a forward return signal.
