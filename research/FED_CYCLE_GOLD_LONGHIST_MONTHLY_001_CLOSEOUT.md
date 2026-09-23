# FED-CYCLE-GOLD-LONGHIST-MONTHLY-001 — Closeout
Date: 2026-09-24
Status: **QC-PASSED DESCRIPTIVE LONG-HISTORY / DIRECTIONAL RULE NOT ESTABLISHED / NOT DEPLOYABLE**

## 1. Purpose

This module extends Gold coverage across the frozen Fed tightening-leg registry without pretending monthly historical data are daily event prices.

It complements the daily `GC=F` futures-proxy layer in FED-CYCLE-PATH-001 v1.1.

It does not pool different Gold instruments or frequencies.

## 2. Source and frequency boundary

Pinned source:

- `datasets/gold-prices`
- commit `95bfea9197222dcda13d8c4d9928fb631fe745aa`
- `data/monthly.csv`
- license: ODC-PDDL-1.0
- 1960-present source stated by the package: World Bank Commodity Markets ("Pink Sheet")

Eligible sample: **1960-01 through 2026-08, 800 monthly observations**.

The package's 1833-1959 rows repeat annual averages across months and are excluded entirely.

## 3. Timing rule

For an event in month M0:

- baseline = M-1 monthly average;
- event month M0 is omitted from clean outcomes because its monthly average mixes pre-event and post-event prices;
- endpoints = M+1, M+3, M+6, M+12 and M+24.

Hard QC confirms:

- FIRST_HIKE support = **10/10** frozen tightening legs;
- event-month omission violations = **0**;
- MDD identity violations = **0**;
- recovery-order violations = **0**.

Pre-1994 Fed anchors retain the v1.1 caveat: they are historical target reconstructions rather than exact modern announcement timestamps.

## 4. FIRST_HIKE long-history Gold distribution

Across 10 mechanical tightening legs:

| Metric | Median | Range |
|---|---:|---:|
| +1M endpoint | +1.55% | -11.81% to +4.36% |
| +3M endpoint | +0.51% | -15.89% to +14.64% |
| +6M endpoint | -1.90% | -16.09% to +17.50% |
| +12M endpoint | +0.24% | -19.76% to +21.99% |
| +24M endpoint | +0.58% | -36.05% to +55.21% |
| 24M maximum drawdown | 16.64% | 3.83% to 39.10% |
| MAE from pre-event baseline | -8.80% | -39.10% to 0.00% |
| MFE from pre-event baseline | +10.22% | 0.00% to +75.78% |
| event-relative minimum timing | 4.5 months | 0 to 24 months |
| 12M annualized monthly volatility | 11.06% | 5.14% to 21.31% |
| 12M downside semivolatility | 8.93% | 3.02% to 12.82% |

## 5. Main finding

### DESCRIPTIVE RESULT

The long-history sample does **not** support a simple statement that Gold reliably rises after a first Fed hike.

The clean +12M and +24M median endpoints are both close to zero, while the median 24-month drawdown is about **16.6%** and the episode range is very wide.

The information content is therefore better summarized as:

`FIRST_HIKE -> highly dispersed Gold path + meaningful drawdown risk`

rather than:

`FIRST_HIKE -> Gold up/down`.

### NOT YET VERIFIED

No claim is made yet that a particular inflation, real-rate, USD, energy or growth state explains this heterogeneity.

That requires a separately frozen predetermined/PIT state-dependence design.

## 6. Recovery — right-censoring-aware result

The frozen 60-month recovery search contains right-censoring, so observed-only recovery medians are not used as the overall population summary.

Kaplan–Meier audit passes.

### 50% recovery from the MDD trough

- risk set: 10 episodes;
- observed: 8;
- right-censored: 2;
- KM median: **8 months**;
- share not yet 50%-recovered: 60% at 6 months, 30% at 12 months, 20% at 24 months and 20% at 60 months.

### 100% recovery from the MDD trough

- risk set: 10;
- observed: 6;
- right-censored: 4;
- KM median: **19 months**;
- share not yet fully recovered: 90% at 6 months, 70% at 12 months, 50% at 24 months and 40% at 60 months.

### Interpretation

**DESCRIPTIVE RESULT:** even when Gold eventually recovers, full drawdown repair can be slow, and a material share of historical episodes remained unrecovered inside the frozen five-year search window.

These are historical recovery distributions, not forecasts for the current cycle.

## 7. Cross-frequency robustness diagnostic

Three FIRST_HIKE legs overlap with the daily `GC=F` layer:

| Cycle | World Bank monthly +12M | Monthly 24M MDD | GC=F daily +252 obs | Daily 252-obs MDD | Endpoint sign |
|---|---:|---:|---:|---:|---|
| 2004 | +12.24% | 11.70% | +7.90% | 9.52% | agrees |
| 2015 | +6.54% | 13.66% | +6.81% | 17.37% | agrees |
| 2022 | +3.07% | 14.09% | -0.35% | 17.90% | disagrees |

### DESCRIPTIVE RESULT

The 2022 endpoint sign differs across the native monthly World Bank series and daily COMEX futures proxy.

This is not treated as an error to average away.

It is evidence that endpoint conclusions can be sensitive to:

- instrument;
- frequency;
- event-month treatment;
- exact endpoint definition.

The two layers are never pooled as a homogeneous sample.

## 8. Episode heterogeneity

Illustrative FIRST_HIKE clean monthly outcomes:

- 1983: +12M -19.76%, +24M -36.05%, MDD 39.10%; full recovery not observed inside 60 months.
- 1984: +12M -18.65%, +24M -10.36%, MDD 22.54%.
- 1994: +12M -2.58%, +24M +4.65%, MDD 3.83%.
- 2004: +12M +12.24%, +24M +55.21%, MDD 11.70%.
- 2015: +12M +6.54%, +24M +16.39%, MDD 13.66%.
- 2022: +12M +3.07%, +24M +16.27%, MDD 14.09%.

These differences motivate state-dependence research; they do not justify post-hoc regime construction.

## 9. Statistical and causal status

- **DATA FACT:** all 10 frozen FIRST_HIKE legs have clean monthly Gold support.
- **DESCRIPTIVE RESULT:** endpoints are near zero on median while drawdowns are material and heterogeneous.
- **ASSOCIATIONAL EVIDENCE:** not yet tested in this module.
- **CAUSAL EVIDENCE:** none.
- **FDR:** no confirmatory p-value family is run here.
- **OOS:** not applicable; this is not a forecasting model.
- **DEPLOYMENT:** not deployable.

Realized Fed actions remain descriptive cycle markers, not identified monetary-policy shocks.

## 10. Investment-research implication

The evidence supports a measurement implication, not a trade direction:

**Gold around tightening cycles should be represented as a distribution of path risk and recovery time, not as a single endpoint-return rule.**

For PandaAI, the appropriate product primitive is therefore a historical risk map:

`cycle anchor + macro state + drawdown distribution + recovery distribution`

rather than a deterministic "hike = buy/sell Gold" signal.

## 11. Next research priority

Freeze a predetermined/PIT state-dependence layer before looking at state-conditioned Gold outcomes.

Priority states:

1. inflation level and direction;
2. growth state;
3. yield-curve state;
4. real-rate state;
5. USD state;
6. energy-shock state;
7. financial-condition state.

Market-state variables should use observations strictly available before the event.

Macro series that are revised after release require a real-time/vintage treatment or an explicit revised-data limitation; they must not be casually labeled PIT.
