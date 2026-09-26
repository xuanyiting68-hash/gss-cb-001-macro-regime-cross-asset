# FED-CYCLE-REIT-DEEP-HISTORY-DUAL-BRIDGE-037 — CLOSEOUT

Date: 2026-09-26

## Final status

**QC PASS / DUAL_BRIDGE_FAIL_NO_DEEP_EXTENSION / NO 1987+ REIT EVIDENCE PROMOTION**

037 tests FRESX as a deep-history active listed-real-estate proxy.

The candidate is empirically very close to both VNQ and VGSIX, but the frozen dual-bridge decision fails one preregistered phase-direction gate.

No threshold is changed post-run.

## Candidate

FRESX_REIT_ACTIVE_PROXY
- Fidelity Real Estate Investment Portfolio
- official inception 1986-11-17
- Yahoo adjusted-close history begins 1986-11-14
- active management
- real-estate-sector mandate
- secondary benchmark context includes MSCI US IMI Real Estate 25/50 Linked

## Bridge A — FRESX vs VNQ

All frozen A gates pass.

Monthly overlap:
- 263 months
- Pearson 0.9933
- Spearman 0.9871
- beta 1.0250
- intercept -0.000136

Common event:
- 11 events
- 12M sign agreement 100%
- return correlation 0.9877
- median abs 12M-return difference 2.30pp
- MDD correlation 0.9874
- median abs MDD difference 0.97pp

Common phase:
- all four directions agree
- median abs 12M-return difference 3.29pp
- max abs difference 4.44pp

Bridge A: PASS.

## Bridge B — FRESX vs VGSIX

Most frozen B gates pass.

Monthly overlap:
- 363 months
- Pearson 0.9920
- Spearman 0.9861
- beta 1.0202
- intercept +0.000133

Common event:
- 16 events
- 12M sign agreement 100%
- return correlation 0.9838
- median abs 12M-return difference 2.57pp
- MDD correlation 0.9892
- median abs MDD difference 0.94pp

Common phase:
- median abs 12M-return difference 2.16pp
- max abs difference 4.33pp

One gate fails:
`B6 — all four phase directions agree`

## Exact phase disagreement

The disagreement is FIRST_HIKE only.

On the exact VGSIX/FRESX common sample:

- VGSIX 12M weighted median: +2.499%
- FRESX 12M weighted median: +3.971%
- absolute difference: 1.471pp

Frozen direction rule:
- POSITIVE > +3%
- NEGATIVE < -3%
- NEUTRAL otherwise

Therefore:
- VGSIX = NEUTRAL
- FRESX = POSITIVE

Other phases agree:
- LAST_HIKE: POSITIVE / POSITIVE
- PAUSE_START: POSITIVE / POSITIVE
- FIRST_CUT: NEGATIVE / NEGATIVE

This is a boundary-sensitive categorical failure, not a large continuous divergence.

However, the gate was frozen ex ante and remains binding.

## Final decision

`DUAL_BRIDGE_FAIL_NO_DEEP_EXTENSION`

FRESX is **not** promoted as a deep-history REIT proxy.

No 1987+ FRESX phase medians may be used as canonical REIT evidence.

The generated FRESX extended metrics remain diagnostic-only and carry:
`NOT_PROMOTED_DUAL_BRIDGE_FAIL`

## Why the fail is still useful

The result distinguishes two questions:

1. Is FRESX generally similar to listed REIT market exposure?
   - Empirically, yes: monthly and event correlations are very high.

2. Does it meet the exact frozen standard required to inherit the project's VNQ/VGSIX phase evidence?
   - No.

This is exactly the purpose of a predeclared measurement gate.

## Diagnostic, non-promoted FRESX full-history medians

These numbers are retained only to audit what was rejected.

They are **not canonical REIT phase evidence**.

- FIRST_HIKE: 12M +3.3%, MDD 11.3%
- LAST_HIKE: +15.9%, MDD 4.0%
- PAUSE_START: +17.2%, MDD 3.6%
- FIRST_CUT: +1.6%, MDD 6.7%

Sample would have been:
- 8 / 6 broad episodes for FIRST_HIKE, LAST_HIKE, FIRST_CUT
- 6 / 6 for PAUSE

But promotion is blocked.

## Reproducibility

Workflow:
- run id: `36221241038`
- source commit: `ad4823a2c92be388cebf443bd60a1a0cf86b05fd`
- output commit: `23865a7c236d82ca5fda8f8da30c4f2e8c48c7a3`
- result: SUCCESS

## QC

- 036 upstream bridge: PASS
- source hashes complete
- FRESX first date: 1986-11-14
- current partial month excluded
- VNQ bridge: all gates PASS
- VGSIX bridge: one B6 direction gate FAIL
- dual bridge: FAIL
- deep-history promotion: blocked
- pre-2004 rows labeled VNQ: 0
- active-management caveat retained
- national house-price substitution: false
- best phase output: 0
- expected-return forecast: 0
- REIT-buying recommendation: 0
- new p-values: false
- private-paper inputs: false
- causal status: NONE
- OOS: NOT_A_FORECASTING_MODEL
- deployment: NOT_DEPLOYABLE

## Canonical REIT state after 037

- VNQ: original ETF layer remains LIMITED_DESCRIPTIVE.
- VGSIX_REIT_PROXY: bridge-validated extension remains LIMITED_PROXY_DESCRIPTIVE at 4 broad episodes.
- FRESX_REIT_ACTIVE_PROXY: NOT_PROMOTED_DUAL_BRIDGE_FAIL.

Do not search additional active-fund proxies merely to obtain a passing result.

The next research priority should move to a genuinely different evidence gap rather than proxy-shopping.
