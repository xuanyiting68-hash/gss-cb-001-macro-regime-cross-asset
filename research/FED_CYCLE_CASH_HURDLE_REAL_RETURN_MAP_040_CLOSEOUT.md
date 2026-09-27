# FED-CYCLE-CASH-HURDLE-REAL-RETURN-MAP-040 — CLOSEOUT

Date: 2026-09-27

## Final status

**QC PASS / EVENT-MATCHED CASH-HURDLE + EX-POST REAL-RETURN MAP / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

040 adds an opportunity-cost and purchasing-power layer to the existing four-phase Fed-cycle atlas.

The key result is not an asset ranking. It is a measurement correction:

> A positive nominal 12M endpoint is not automatically a win relative to contemporaneous cash, not automatically a purchasing-power gain, and not automatically a low-risk path.

## Reproducibility and QC

Canonical main output commit:

`2aed4fd7fca06e6702e06dfb1fb139bede73703f`

Canonical output commit message:

`Run FED-CYCLE-CASH-HURDLE-REAL-RETURN-MAP-040 [skip ci]`

Independent PR reproduction:

- workflow run: `36299046081`
- job: `108563157173`
- result: SUCCESS
- artifact: `cash-hurdle-040-output`
- artifact SHA256: `3730c0a63cef2c6f7fec6dbbf7a85ed071a58d7819af706807ca148600aac9e5`

QC:

- upstream 004 / 014 / 035 / 036: PASS
- event rows: 232 / 232
- phase-summary rows: 32 / 32
- frozen macro event inputs: 37 / 37
- source hashes complete: true
- broad-episode weight violations: 0
- asset-identity violations: 0
- missing metric rows: 0
- rejected FRESX leakage: 0
- duplicate TLT/VNQ target rows: 0
- housing rows in 12M traded-asset panel: 0
- evidence-tier violations: 0
- supported-minimum-count violations: 0
- event-input period-alignment violations: 0
- private paper inputs: false
- new p-values: false
- optimized horizons/thresholds: false
- asset rankings: false
- expected-return forecasts: false
- trade recommendations: false

Frozen event input SHA256:

`4717a52938ef9e200492607bbac7febbe54e508100564be56c4482e821c6c34b`

## Acquisition amendments

The original lock required fresh FRED DFF/CPI acquisition at run time.

GitHub-hosted runners repeatedly timed out on FRED daily DFF transport. Two failed diagnostic runs documented the failure:

- direct DFF URL timed out;
- 1983+ date-scoped DFF URL also timed out.

AMENDMENT 01 changed only transport to the official monthly FEDFUNDS representation of the daily effective federal funds rate average.

AMENDMENT 02 then removed live-network dependence entirely by freezing the exact 37 canonical event inputs from official FRED monthly FEDFUNDS and CPIAUCSL tables.

No event, formula, horizon, asset, threshold, evidence tier or observed return was changed.

The final canonical runner is network-independent.

## Frozen measurement convention

For anchor month `t`:

- asset baseline: `t-1`
- asset endpoint: `t+12`
- canonical 014 cash component: months `t+1 ... t+12`
- 040 matched cash hurdle:
  `(1 + cash014_post12) × (1 + FEDFUNDS_t/100/12) - 1`
- matched CPI inflation:
  `CPI(t+12) / CPI(t-1) - 1`
- asset-vs-cash:
  `(1 + nominal asset return)/(1 + matched cash) - 1`
- real asset return:
  `(1 + nominal asset return)/(1 + matched inflation) - 1`

Current-vintage CPI is an ex-post purchasing-power diagnostic. It is not ALFRED point-in-time information.

## Cross-cutting finding

Across the 232 asset × event rows:

- positive nominal 12M endpoint rows: **136**
- positive nominal rows that still failed matched cash: **30**
- positive nominal rows that still failed matched inflation: **14**

These are row counts, not independent statistical observations. Canonical phase summaries preserve broad-episode weighting.

This is the central 040 knowledge upgrade:

**nominally positive ≠ opportunity-cost win ≠ purchasing-power win.**

## Cash timing convention audit

Adding the anchor month to the existing 014 post12 cash benchmark changes the hurdle by:

- median absolute difference: **0.55pp**
- maximum absolute difference: **1.06pp**

This is not large enough to justify a new model, but it is large enough that the timing convention should be explicit, especially in high-rate episodes.

## Supported evidence: Gold

### FIRST_HIKE

Weighted medians:

- nominal 12M: **+3.1%**
- matched cash: **+5.0%**
- matched inflation: **+3.7%**
- asset vs cash: **-2.4%**
- real asset return: **-2.8%**
- MDD: **11.6%**

So the familiar positive nominal Gold endpoint does not survive either the cash hurdle or purchasing-power hurdle at the weighted-median level.

This is not evidence that Gold is unattractive in every tightening cycle. Event heterogeneity remains large.

### LAST_HIKE

- nominal: **-2.8%**
- asset vs cash: **-8.2%**
- real: **-5.6%**
- MDD: **9.1%**

### PAUSE_START

- nominal: **+4.9%**
- asset vs cash: **-1.3%**
- real: **+1.9%**
- MDD: **7.6%**

This is a particularly useful distinction: the historical median preserves purchasing power but still does not clear contemporaneous cash.

### FIRST_CUT

- nominal: **+4.1%**
- asset vs cash: **-0.05%**
- real: **+2.2%**
- MDD: **5.4%**

The median is essentially flat versus the matched cash hurdle, not a clean cash-relative outperformance statement.

## Supported evidence: U.S. equities

### S&P 500

FIRST_HIKE:
- nominal **+8.0%**
- vs cash **+2.5%**
- real **+5.8%**
- MDD **5.9%**

LAST_HIKE:
- nominal **+16.7%**
- vs cash **+10.9%**
- real **+13.9%**
- MDD **4.2%**

PAUSE_START:
- nominal **+24.6%**
- vs cash **+13.2%**
- real **+20.3%**
- MDD **4.2%**

FIRST_CUT:
- nominal **+11.0%**
- vs cash **+2.1%**
- real **+8.2%**
- MDD **14.0%**

The FIRST_CUT result preserves the 032 warning: a positive endpoint can coexist with materially worse path risk.

### Nasdaq

FIRST_HIKE:
- nominal **+6.5%**
- vs cash **-0.8%**
- real **+4.4%**
- MDD **12.2%**

LAST_HIKE:
- nominal **+15.6%**
- vs cash **+9.2%**
- real **+12.3%**
- MDD **4.0%**

PAUSE_START:
- nominal **+28.1%**
- vs cash **+16.6%**
- real **+23.8%**
- MDD **4.0%**

FIRST_CUT:
- nominal **+6.0%**
- vs cash **-3.4%**
- real **+1.0%**
- MDD **17.5%**

Nasdaq FIRST_CUT is one of the clearest examples of why nominal endpoint, cash opportunity cost, purchasing power and path risk should not be collapsed into one number.

## Supported evidence: WTI and DXY

WTI:

- FIRST_HIKE nominal **+22.4%**, vs cash **+17.8%**, real **+19.9%**, MDD **18.8%**
- LAST_HIKE nominal **+5.0%**, vs cash **-0.7%**, real **+2.6%**, MDD **19.6%**
- PAUSE_START nominal **-4.6%**, vs cash **-10.4%**, real **-8.1%**, MDD **18.0%**
- FIRST_CUT nominal **-16.9%**, vs cash **-24.3%**, real **-20.9%**, MDD **22.2%**

DXY:

- FIRST_HIKE nominal **+3.0%**, vs cash **-2.5%**, real **+1.0%**
- LAST_HIKE nominal **-1.3%**, vs cash **-8.1%**, real **-4.7%**
- PAUSE_START nominal **-1.3%**, vs cash **-7.5%**, real **-4.7%**
- FIRST_CUT nominal **-1.3%**, vs cash **-6.5%**, real **-3.9%**

These are historical distributions, not policy prescriptions.

## Supported proxy evidence: long-duration Treasury

VUSTX_LONG_TREASURY_PROXY remains separately labeled from TLT.

FIRST_HIKE:
- nominal **+1.0%**
- vs cash **-3.6%**
- real **-0.9%**
- MDD **10.7%**

LAST_HIKE:
- nominal **+9.9%**
- vs cash **+0.9%**
- real **+5.2%**
- MDD **3.3%**

PAUSE_START:
- nominal **+15.1%**
- vs cash **+6.8%**
- real **+10.5%**
- MDD **3.9%**

FIRST_CUT:
- nominal **+6.0%**
- vs cash **+1.8%**
- real **+4.2%**
- MDD **4.5%**

PAUSE_START has a 100% weighted beats-cash and beats-inflation share in the six broad episodes available to this proxy, but 040 does **not** convert that descriptive record into a “best phase” label.

## Limited evidence remains limited

### VGSIX_REIT_PROXY

Bridge-valid history still has only four legs / four broad episodes.

Its attractive LAST_HIKE / PAUSE hurdle-adjusted results do not upgrade the evidence tier.

Status remains:

`LIMITED_PROXY_DESCRIPTIVE`

### BTC_USD

Bitcoin still has only two broad Fed-cycle episodes in this phase framework.

039 is the richer Bitcoin mechanism module. 040 phase results remain:

`LIMITED_DESCRIPTIVE`

No synthetic history or support promotion is permitted.

## Counterexamples that matter

Examples preserved in the canonical counterexample panel include:

- Gold FIRST_HIKE 1999: nominal positive, but below cash and inflation.
- Gold FIRST_HIKE 2022: nominal positive and slightly above cash, but negative real return.
- S&P 500 FIRST_HIKE 1987 and 1994: nominal positive but below both cash and inflation.
- Nasdaq FIRST_HIKE 1984: nominal positive and real positive but below cash.
- Nasdaq FIRST_CUT 1989: nominal positive and real positive but below cash.
- VUSTX FIRST_HIKE multiple episodes: positive nominal endpoints that do not clear cash.
- VGSIX FIRST_HIKE 1999: positive nominal endpoint but below cash and inflation.

The purpose of these cases is to falsify simplistic interpretation, not to identify a replacement trading rule.

## Product implication

PandaAI may expose:

- nominal endpoint distribution;
- matched mechanical cash hurdle;
- ex-post matched inflation;
- real asset return;
- asset-vs-cash gap;
- MDD/path risk;
- evidence tier;
- historical counterexamples;
- timing-convention caveat.

PandaAI must not output:

- best asset;
- best phase;
- expected return;
- optimized allocation;
- current analog ranking;
- buy/sell instruction;
- causal Fed claim.

## Research implication

040 materially improves the investor knowledge system because it separates four questions that were previously easy to conflate:

1. Did the asset finish positive?
2. Did it beat available cash?
3. Did it preserve purchasing power?
4. What path risk was endured?

The next module should build on this distinction rather than returning to proxy-shopping or small-sample phase rankings.
