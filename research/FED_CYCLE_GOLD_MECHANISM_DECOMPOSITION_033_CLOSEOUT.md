# FED-CYCLE-GOLD-MECHANISM-DECOMPOSITION-033 — CLOSEOUT

Date: 2026-09-26

## Final status

**QC PASS / MULTI-MECHANISM GOLD EVIDENCE MAP / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

033 integrates the public Gold state, monthly panel, phase-clock, stress-alignment and literature-context evidence without creating a driver score or trading rule.

## Main result

The public evidence stack does **not** justify a single-driver Gold story.

Gold behavior around Fed cycles is state-dependent:
- inflation level and inflation direction can point in different directions;
- real-yield support is limited in this design;
- USD diagnostics are counterintuitive and remain secondary;
- weak-growth and rising-energy event states show descriptive heterogeneity;
- Gold stress timing differs materially from U.S. equities;
- Fed phase is a conditioning label, not a causal Gold shock.

## Fed-phase profile

Gold 12M historical medians:
- FIRST_HIKE: +3.1%
- LAST_HIKE: -2.8%
- PAUSE_START: +4.9%
- FIRST_CUT: +4.1%

The four phases do not form a monotonic “more easing -> more Gold” sequence.

## Inflation

### Inflation level
FIRST_HIKE:
- HIGH inflation: Gold 12M median -11.8%
- LOW_OR_MODERATE: +6.5%
- oriented difference: -18.3%
- n=5 vs 5
- LOO sign stable

### Inflation direction
FIRST_HIKE:
- RISING: +3.1%
- FALLING_OR_FLAT: -11.8%
- oriented difference: +14.8%
- n=7 vs 3
- LOO sign stable

Therefore:
`high inflation` and `rising inflation` are not interchangeable Gold states.

## Growth and energy

Growth:
- STRONG: Gold 12M median -3.5%
- WEAK: +4.8%
- LOO sign stable

Energy direction:
- RISING: +3.6%
- FALLING_OR_FLAT: -2.6%
- LOO sign stable

These are descriptive state contrasts, not identified causal contributions.

## Real rates

The public design does not verify a stable textbook inverse real-rate/Gold rule.

Monthly REAL_RATE_PROXY:
- beta per 1SD: +0.0180
- broad exact p ~0.266
- secondary diagnostic only

Actual DFII10:
- 101 monthly rows
- only 3 cycles / 3 broad clusters
- status: INSUFFICIENT_SUPPORT

This is an evidence limitation, not proof that real yields do not matter in general.

External literature is retained as context only; it also contains regime-dependent real-rate/Gold findings.

## USD

The repository retains its counterintuitive USD evidence rather than deleting it.

Event-level diagnostic:
- USD RISING: Gold 12M median +3.6%
- USD FALLING_OR_FLAT: -11.8%
- difference +15.4%
- n=5 vs 5
- LOO sign stable

Monthly within-cycle USD_6M_RET:
- beta per 1SD: +0.0183
- broad exact p = 0.03125
- LOO sign stable
- 165 rows / 10 cycles / 7 broad clusters

But:
- it is a secondary diagnostic;
- the secondary family has no FDR survivor;
- source-era restrictions weaken precision.

Therefore USD remains a mechanism candidate / heterogeneity clue, not a confirmed positive Gold driver.

## Financial conditions

NFCI:
- beta per 1SD ~ -0.0067
- broad exact p ~0.594
- LOO sign stability false

Status:
`NO_STABLE_ASSOCIATION`

## Stress timing

FIRST_CUT paired timing:

### Gold vs Baa credit spread
- Gold trough median: M5
- Baa stress peak median: M7
- median lead: -3m
- near-2m share: 14.3%
- 10 legs / 7 broad episodes

### Gold vs VIX
- Gold trough median: M4
- VIX stress peak median: M8
- median lead: -4m
- near-2m share: 40%
- 5 legs / 5 broad episodes

### Gold vs copper
- Gold trough median: M4
- copper stress peak median: M9
- near-2m share: 60%
- 5 legs / 5 broad episodes

Gold can complete part of its adjustment before broader equity/credit stress peaks. This is ex-post timing evidence, not a real-time entry signal.

## Literature context

The frozen literature registry contains:
- Baur & Lucey (2010)
- Baur & McDermott (2010)
- Erb & Harvey (2013)
- Baur (2011)
- Apergis et al. (2019)

The literature is used only to contextualize:
- hedge vs safe-haven definitions;
- short-lived / cross-market safe-haven behavior;
- practical-horizon inflation-hedge limitations;
- multi-driver sensitivity;
- regime-dependent real-rate relationships.

External literature never overwrites repository findings.

## Product implication

PandaAI Gold explanations should expose:

`Fed phase + inflation level + inflation direction + growth state + real-rate evidence status + USD evidence status + energy state + stress timing + support/multiplicity/PIT caveat`

It must not output:
- dominant driver score;
- best Gold phase;
- expected Gold return;
- Gold bottom date;
- buy/sell instruction.

## Reproducibility

Workflow:
- `.github/workflows/fed-cycle-gold-mechanism-decomposition-033-v1.yml`
- run id: `36214221972`
- source commit: `13d17127238af303a177d87a8cd7a172b3093eff`
- output commit: `65e32b9b173bffe05230cf1fec25ac8bad3e60f3`
- result: SUCCESS

## QC summary

- Gold phase rows: 4
- supported FIRST_HIKE state contrasts: 4
- USD event diagnostic: 1
- monthly secondary diagnostics: 6
- Gold stress-timing rows: 3
- literature context rows: 5
- mechanism evidence rows: 12
- mechanism claim rows: 17
- supported event LOO sign stable: true
- USD promoted to confirmed driver: false
- USD FDR survivor: false
- DFII10: INSUFFICIENT_SUPPORT
- inverse real-rate rule claimed: false
- inflation level/direction separated: true
- safe-haven trading signal: false
- mechanism ranking: false
- multivariate score: false
- expected-return forecast: false
- new p-values: false
- private-paper inputs: false
- causal status: NONE
- OOS: NOT_A_FORECASTING_MODEL
- deployment: NOT_DEPLOYABLE

## Next research priority

Proceed to **034 Housing Lag Chain**:
- policy rates / Treasury rates / mortgage rates;
- transaction/activity response;
- house-price response;
- lag structure across FIRST_HIKE / LAST_HIKE / PAUSE_START / FIRST_CUT;
- slow-moving path and recovery;
- no direct comparison of housing 24M decline with traded-asset 12M MDD.
