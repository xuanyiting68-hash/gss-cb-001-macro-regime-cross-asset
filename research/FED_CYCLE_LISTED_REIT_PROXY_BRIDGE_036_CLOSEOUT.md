# FED-CYCLE-LISTED-REIT-PROXY-BRIDGE-036 — CLOSEOUT

Date: 2026-09-26

## Final status

**QC PASS / BRIDGE_PASS_SUPPORTED_PROXY_EXTENSION / PROXY HISTORY EXTENDED / EVIDENCE STILL LIMITED / NOT A FORECAST / NOT DEPLOYABLE**

036 tests VGSIX as a longer-history listed-real-estate proxy for VNQ.

The measurement bridge passes every frozen gate, but the historical event count remains below the preregistered threshold for SUPPORTED_PROXY_DESCRIPTIVE.

## Official product context

VGSIX:
- Vanguard Real Estate Index Fund Investor Shares
- inception: 1996-05-13

VNQ:
- Vanguard Real Estate ETF
- inception: 2004-09-23

The vehicles are highly related but not treated as identical.

Pre-2004 VGSIX history is never labeled VNQ.

## Overlap validation

Complete matched monthly returns:
- 263
- 2004-10 through 2026-08

Monthly:
- Pearson: 0.999873
- Spearman: 0.999791
- beta VGSIX on VNQ: 1.00063
- intercept: -0.000084

Common events:
- 11

12M return:
- sign agreement: 100%
- correlation: 0.999981
- median absolute difference: 0.18 percentage points

12M MDD:
- correlation: 0.999991
- median absolute difference: 0.02 percentage points

Common phase:
- all four directions agree
- median absolute phase 12M-return difference: 0.16 percentage points
- maximum: 0.22 percentage points

All frozen bridge gates pass.

## Final bridge decision

`BRIDGE_PASS_SUPPORTED_PROXY_EXTENSION`

Measurement compatibility is exceptionally strong.

However, bridge validity and sample support are separate concepts.

## Extended proxy evidence

VGSIX_REIT_PROXY:

### FIRST_HIKE
- 4 legs / 4 broad episodes
- 3M: -8.2%
- 6M: -13.4%
- 12M: +2.5%
- 12M MDD: 11.5%
- trough M7
- late-trough share: 75%
- support: LIMITED_PROXY_DESCRIPTIVE

### LAST_HIKE
- 4 / 4
- 3M: +7.7%
- 6M: +9.3%
- 12M: +18.8%
- MDD: 4.3%
- trough M6
- support: LIMITED_PROXY_DESCRIPTIVE

### PAUSE_START
- 4 / 4
- 3M: +8.4%
- 6M: +10.6%
- 12M: +21.4%
- MDD: 4.3%
- trough M5
- support: LIMITED_PROXY_DESCRIPTIVE

### FIRST_CUT
- 4 / 4
- 3M: +1.4%
- 6M: +0.9%
- 12M: -4.8%
- MDD: 8.3%
- trough M7
- late-trough share: 75%
- support: LIMITED_PROXY_DESCRIPTIVE

## Main interpretation

The proxy extension sharpens the REIT story but does not establish a stable law.

The extended sample suggests:
- tightening starts can produce substantial short-horizon listed-REIT weakness even when the 12M endpoint later recovers;
- LAST_HIKE / PAUSE historically have stronger median listed-REIT endpoints in this small sample;
- FIRST_CUT is not automatically favorable and has a negative 12M median in the four-episode proxy sample.

Because there are only four broad episodes, none of these are promoted beyond LIMITED_PROXY_DESCRIPTIVE.

## Reproducibility

Workflow:
- run id: `36220948636`
- source commit: `930f49f236f80d6cd46c366872991da2881ab48a`
- output commit: `c8c8eda8d17da1579bc61d357a4c205816de047a`
- result: SUCCESS

## QC

- bridge pass: true
- source hashes: complete
- VGSIX first date: 1996-05-13
- matched monthly returns: 263
- partial month excluded
- all bridge gates pass
- extended proxy rows: 16
- pre-2004 rows labeled VNQ: 0
- national house-price series substituted: false
- best phase output: 0
- expected-return forecast: 0
- REIT-buying recommendation: 0
- new p-values: false
- private-paper inputs: false
- causal status: NONE
- OOS: NOT_A_FORECASTING_MODEL
- deployment: NOT_DEPLOYABLE

## Remaining REIT evidence gap

The limiting factor is now historical depth, not VGSIX/VNQ measurement compatibility.

Next candidate:
- FRESX — Fidelity Real Estate Investment Portfolio
- inception 1986-11-17

Because FRESX is actively managed rather than an index clone, any extension must use a stricter **dual bridge**:
1. FRESX vs VNQ overlap;
2. FRESX vs VGSIX overlap;
3. event and path-risk agreement;
4. no automatic inheritance if either bridge fails.
