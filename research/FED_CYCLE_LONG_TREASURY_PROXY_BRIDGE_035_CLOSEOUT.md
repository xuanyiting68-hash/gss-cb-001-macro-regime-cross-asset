# FED-CYCLE-LONG-TREASURY-PROXY-BRIDGE-035 — CLOSEOUT

Date: 2026-09-26

## Final status

**QC PASS / BRIDGE_PASS_SUPPORTED_PROXY_EXTENSION / LONG-DURATION TREASURY HISTORY EXTENDED / NOT A FORECAST / NOT DEPLOYABLE**

035 tests whether VUSTX can be used as a longer-history proxy for the public TLT duration layer.

The bridge passes every frozen gate.

## Measurement bridge

Target:
- TLT
- iShares 20+ Year Treasury Bond ETF
- adjusted-close proxy used in 014

Candidate:
- VUSTX_LONG_TREASURY_PROXY
- Vanguard Long-Term Treasury Fund Investor Shares
- inception-era history starts 1986-05-19

The candidate is never relabeled as TLT.

## Overlap validation

Complete matched monthly return observations:
- 289
- 2002-08 through 2026-08
- current partial September 2026 excluded

Monthly returns:
- Pearson correlation: 0.9911
- Spearman correlation: 0.9933
- descriptive beta VUSTX on TLT: 0.8744
- intercept: +0.00040 monthly return

All frozen monthly gates pass.

## Common Fed-event validation

Common event rows:
- 12

12M return:
- sign agreement: 100%
- correlation: 0.9948
- median absolute difference: 0.68 percentage points

12M MDD:
- correlation: 0.9988
- median absolute difference: 0.68 percentage points

All frozen event-level gates pass.

## Common phase validation

All four phase directions agree between TLT and VUSTX on the common-event sample.

Phase 12M median absolute differences:
- median: 0.42 percentage points
- maximum: 1.62 percentage points

All frozen phase-summary gates pass.

## Final bridge decision

`BRIDGE_PASS_SUPPORTED_PROXY_EXTENSION`

Therefore VUSTX may be used as a longer-history **long-duration Treasury proxy** for descriptive Fed-cycle research.

This does not make the two vehicles identical.

Pre-2002 observations remain explicitly labeled:
`VUSTX_LONG_TREASURY_PROXY`

## Extended Fed-cycle evidence

### FIRST_HIKE
- 8 legs / 6 broad episodes
- 3M median: -2.2%
- 6M median: -2.6%
- 12M median: +1.0%
- 12M MDD median: 10.7%
- MDD trough month median: M9
- late-trough share: 88.9%
- support: SUPPORTED_PROXY_DESCRIPTIVE

Interpretation:
Long-duration Treasury exposure is not a simple immediate beneficiary at the start of tightening. The 12M endpoint is close to flat while interim drawdown is material.

### LAST_HIKE
- 8 legs / 6 broad episodes
- 3M: +6.0%
- 6M: +9.0%
- 12M: +9.9%
- MDD: 3.3%
- trough: M11
- late-trough share: 61.1%
- support: SUPPORTED_PROXY_DESCRIPTIVE

### PAUSE_START
- 6 legs / 6 broad episodes
- 3M: +6.7%
- 6M: +8.2%
- 12M: +15.1%
- MDD: 3.9%
- trough: M10
- late-trough share: 66.7%
- support: SUPPORTED_PROXY_DESCRIPTIVE

### FIRST_CUT
- 8 legs / 6 broad episodes
- 3M: +4.3%
- 6M: +7.4%
- 12M: +6.0%
- MDD: 4.5%
- trough: M10
- late-trough share: 72.2%
- support: SUPPORTED_PROXY_DESCRIPTIVE

## What changes relative to the original TLT layer

014/032 TLT evidence was based on only three broad episodes.

035 does not overwrite TLT.

Instead it adds a separately validated long-history proxy that materially increases historical coverage.

The main qualitative shift is that long-duration Treasury behavior can now be discussed with supported proxy evidence rather than only limited ETF evidence.

## Important interpretation

The strongest descriptive pattern is not “rate cuts are best for bonds.”

In the extended proxy sample:
- FIRST_HIKE has near-flat 12M median and deep interim MDD;
- LAST_HIKE and PAUSE show stronger 12M proxy returns;
- FIRST_CUT remains positive but weaker than PAUSE in the historical median.

This is a historical distribution, not a phase ranking or expected-return forecast.

## Reproducibility

Final authoritative workflow:
- run id: `36220691726`
- source commit: `59e98e7874dc4c7d5fe4b5c6beeadd1df877d11f`
- output commit: `6750e5891c8deb5b6d92a7d84aad010778bde0ad`
- result: SUCCESS

Earlier failed runs:
- `36220619581`: missing matplotlib dependency
- `36220657365`: missing scipy dependency for frozen Spearman gate

Neither failure changed research thresholds.

## QC

- bridge status: BRIDGE_PASS_SUPPORTED_PROXY_EXTENSION
- source hashes complete: true
- VUSTX first date: 1986-05-19
- matched monthly returns: 289
- partial current month used: false
- all bridge tests pass: true
- proxy extended rows: 30
- pre-2002 rows labeled TLT: 0
- yield-change substituted for total return: false
- best phase output: 0
- expected-return forecast: 0
- bond-buying recommendation: 0
- new p-values: false
- private-paper inputs: false
- causal status: NONE
- OOS: NOT_A_FORECASTING_MODEL
- deployment: NOT_DEPLOYABLE

## Next research gap

Next priority:
**036 Listed REIT Long-History Proxy Bridge**

VNQ begins in 2004, leaving the current REIT layer at only 2-3 episodes.

A defensible pre-VNQ listed-REIT proxy should be tested on the same principle:
- overlap validation first;
- no automatic evidence inheritance;
- proxy identity retained;
- only then extend Fed-cycle history.
