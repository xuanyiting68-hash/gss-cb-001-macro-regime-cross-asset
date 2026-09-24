# FED-CYCLE-CROSS-ASSET-RISK-CLOCK-003 — Closeout
Date: 2026-09-24
Status: **QC-PASSED DESCRIPTIVE RISK CLOCK / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

## 1. Question

After a mechanically defined FIRST_HIKE, when does path risk tend to materialize?

This module replaces the question:

"what is the return after one year?"

with:

"when does the drawdown deepen, when does the 24M MDD trough occur, and how long does recovery take?"

## 2. Design

Primary assets:

- Gold;
- S&P 500;
- Nasdaq Composite;
- WTI.

Broad USD is diagnostic only because it has only two supported FIRST_HIKE legs.

Timing:

- event month omitted;
- baseline = month before FIRST_HIKE month;
- risk clock = 24 complete post-event months.

Weighting:

- mechanical legs inside the same broad episode share total weight 1;
- 1983-84 and 1987-88 therefore do not receive disproportionate aggregate weight.

QC:

- 960 asset-path rows;
- 40 cycle-asset rows;
- 0 event-month violations;
- 0 negative-MDD violations;
- 0 MDD-trough timing violations;
- 0 recovery-order violations;
- 0 broad-episode weight violations.

## 3. Main MDD timing result

### Gold

Support: 10 legs / 7 broad episodes.

- weighted median MDD-trough month: **12**
- weighted 75th percentile: **23**
- months 1-6: **0%**
- months 7-12: **50%**
- months 13-24: **50%**
- weighted median 24M MDD: **14.09%**
- weighted median +12M return: **+3.07%**
- weighted median +24M return: **+4.65%**

Interpretation:

**DESCRIPTIVE RESULT:** in this broad-episode-weighted monthly history, Gold's eventual 24M maximum-drawdown trough is not concentrated in the first six complete months after FIRST_HIKE.

Half of the weighted trough mass occurs in months 7-12 and half in months 13-24.

This is not a deterministic timing rule.

### Nasdaq

Support: 10 legs / 7 broad episodes.

- median MDD-trough month: **7**
- 75th percentile: **16**
- months 1-6: **40.48%**
- months 7-12: **33.33%**
- months 13-24: **26.19%**
- weighted median 24M MDD: **12.18%**
- +12M median: **+6.50%**
- +24M median: **+16.67%**

Interpretation:

Among the four primary assets, Nasdaq's MDD trough distribution is the most front-loaded.

By month 12, the broad-episode-weighted MDD-trough CDF is about **73.8%**.

### S&P 500

Support: 10 legs / 7 broad episodes.

- median MDD-trough month: **11**
- 75th percentile: **21**
- months 1-6: **33.33%**
- months 7-12: **19.05%**
- months 13-24: **47.62%**
- weighted median 24M MDD: **8.47%**
- +12M median: **+7.98%**
- +24M median: **+16.56%**

Interpretation:

S&P path risk is not only an early-cycle phenomenon.

Nearly half of the weighted eventual 24M MDD troughs occur in months 13-24.

### WTI

Support: 8 legs / 6 broad episodes.

- median MDD-trough month: **15**
- 75th percentile: **17**
- months 1-6: **33.33%**
- months 7-12: **5.56%**
- months 13-24: **61.11%**
- weighted median 24M MDD: **20.65%**
- +12M median: **+22.45%**
- +24M median: **+27.76%**

Interpretation:

WTI has the most late-concentrated MDD-trough distribution in this sample.

A strong positive endpoint does not imply a benign path.

## 4. Risk accumulation checkpoints

Weighted share of eventual 24M MDD troughs already reached:

| Asset | By M6 | By M12 | By M18 | By M24 |
|---|---:|---:|---:|---:|
| Gold | 0.0% | 50.0% | 54.76% | 100% |
| Nasdaq | 40.48% | 73.81% | 80.95% | 100% |
| S&P 500 | 33.33% | 52.38% | 66.67% | 100% |
| WTI | 33.33% | 38.89% | 77.78% | 100% |

The 100% value at month 24 is mechanical because the trough is defined inside the frozen 24M window.

Therefore month 24 must not be presented as a natural hazard spike.

## 5. Recovery

Broad-episode-weighted Kaplan-Meier medians from the 24M-window MDD trough:

| Asset | 50% recovery | 100% recovery | Full-recovery observed / censored |
|---|---:|---:|---:|
| Gold | 8 months | 13 months | 6 / 4 |
| Nasdaq | 2 months | 8 months | 9 / 1 |
| S&P 500 | 4 months | 9 months | 9 / 1 |
| WTI | 3 months | 8 months | 7 / 1 |

### Important weighting note

The earlier Gold long-history survival module, which treated each mechanical leg equally, reported:

- 50% recovery KM median = 8 months;
- 100% recovery KM median = 19 months.

RISK-CLOCK-003 gives each broad episode equal total weight and therefore reports:

- 50% = 8 months;
- 100% = 13 months.

This is not a contradiction.

It is a weighting sensitivity:

**mechanical-leg weighting versus broad-episode weighting.**

Both estimates remain in the repository and must retain their weighting labels.

## 6. What the timing map establishes

### DATA FACT

- Gold/Nasdaq/S&P have 10 mechanical FIRST_HIKE legs and 7 broad episodes.
- WTI has 8 legs and 6 broad episodes.
- all primary assets pass the frozen support and QC gates.

### DESCRIPTIVE RESULT

- Nasdaq MDD trough timing is more front-loaded than Gold/S&P/WTI.
- S&P and especially WTI retain substantial late-window MDD-trough mass.
- Gold's weighted 24M MDD troughs are split evenly between months 7-12 and 13-24 in this sample.
- endpoint returns and drawdown timing can tell very different stories.

### CAUSAL EVIDENCE

**None.**

Realized FIRST_HIKE is a descriptive policy-cycle anchor.

### FDR

Not applicable. No p-value family is executed.

### OOS

Not applicable. This is not a forecasting model.

### DEPLOYMENT

Not deployable.

## 7. Investment-research implication

The evidence argues against one universal statement such as:

"the dangerous period after the first hike is month X."

A more defensible risk map is asset-specific:

- Nasdaq: more early/mid concentration;
- Gold: mid/late concentration;
- S&P: meaningful late tail;
- WTI: strongly late-concentrated MDD trough distribution.

For PandaAI, a useful interface is therefore a **cycle clock with empirical risk bands**, not a countdown-to-crash signal.

## 8. Social-content implication

Evidence-backed content can now answer:

- “第一次加息后，股市真正危险的是第几个月？”
- “为什么一年后上涨，不代表中间风险小？”
- “为什么 Nasdaq、S&P、Gold、WTI 的风险时钟不一样？”

Every post must state:

- sample support;
- 24M window;
- broad-episode weighting;
- descriptive/non-causal status;
- no OOS/trading claim.
