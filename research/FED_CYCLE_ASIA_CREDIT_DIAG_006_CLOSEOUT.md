# FED-CYCLE-ASIA-CREDIT-DIAG-006 — Closeout
Date: 2026-09-24
Status: **QC-PASSED DESCRIPTIVE / ASIA DIAGNOSTIC SUPPORT / HY CREDIT LIMITED OR INSUFFICIENT / NOT CAUSAL / NOT DEPLOYABLE**

## 1. Purpose

Extend the Fed-cycle phase map into Asia equities and high-yield credit without forcing short-history markets into the same evidence tier as the long-history U.S./Gold/WTI sample.

Frozen diagnostics:

- Hang Seng Index;
- Shanghai Composite;
- Nikkei 225;
- KOSPI;
- ICE BofA US High Yield OAS;
- post-source-audit HYG ETF price proxy.

The existing P0-C China identification quarantine remains unchanged.

## 2. QC

Main Asia/OAS module:

- QC PASS;
- 4/4 Asia Yahoo symbols acquired;
- 0 acquisition failures;
- 1,188 Asia path rows;
- 99 Asia cycle-phase rows;
- 0 anchor/timing/MDD/weight/support-label violations.

HYG proxy audit:

- QC PASS;
- Yahoo HYG history begins 2007-04-11;
- 9 cycle-phase rows;
- 0 anchor/weight/MDD/support-label violations.

## 3. Data-coverage facts

### Nikkei 225
- FIRST_HIKE / LAST_HIKE / FIRST_CUT: 10 mechanical legs / 7 broad episodes;
- PAUSE_START: 7 / 7.

### Hang Seng
- FIRST_HIKE / LAST_HIKE / FIRST_CUT: 8 / 6;
- PAUSE_START: 6 / 6.

### Shanghai Composite
Yahoo history used here begins in 1997.

- each phase: 4 / 4 broad episodes.

### KOSPI
Yahoo history begins in 1996.

- each phase: 4 / 4 broad episodes.

### ICE BofA High Yield OAS
Current FRED distribution begins 2023-09-25.

FRED currently states that beginning in April 2026 this ICE BofA series exposes only the most recent three years of observations.

Therefore:

- FIRST_CUT support = 1 / 1;
- other phase cells unavailable;
- status = **INSUFFICIENT_SUPPORT**.

This is a source-coverage limitation, not a computational failure.

### HYG price proxy

HYG is retained separately because it is a bond-price proxy, not OAS.

Support:

- FIRST_CUT: 3 / 3;
- FIRST_HIKE: 2 / 2;
- LAST_HIKE: 2 / 2;
- PAUSE_START: 2 / 2.

All HYG cells remain **LIMITED_SUPPORT**.

## 4. Asia FIRST_CUT versus PAUSE_START

Broad-episode-weighted 12M medians:

| Market | PAUSE +12M | FIRST_CUT +12M | PAUSE MDD | FIRST_CUT MDD | FIRST_CUT trough month | FIRST_CUT late-trough share |
|---|---:|---:|---:|---:|---:|---:|
| Hang Seng | -2.60% | -8.67% | 13.03% | **15.62%** | 8 | 83.33% |
| Nikkei 225 | +13.06% | +9.60% | 8.37% | **12.61%** | 8 | 90.48% |
| KOSPI | +1.23% | +4.31% | 7.67% | **16.40%** | 8 | 75.00% |
| Shanghai Composite | +19.62% | -28.73% | 6.39% | **8.59%** | 9 | 75.00% |

### DESCRIPTIVE RESULT

All four Asia indices have a higher weighted median 12M MDD after FIRST_CUT than after PAUSE_START in the available sample.

But endpoint returns are heterogeneous:

- Nikkei and KOSPI remain positive on the +12M median;
- Hang Seng and Shanghai are negative.

Therefore:

**higher historical path risk after FIRST_CUT does not imply a universal negative endpoint return.**

## 5. FIRST_HIKE Asia paths

+12M weighted medians:

- Hang Seng: -1.24%;
- Nikkei: +2.81%;
- KOSPI: +0.74%;
- Shanghai: -11.38%.

12M MDD medians:

- Hang Seng: 16.07%;
- Nikkei: 10.59%;
- KOSPI: 6.60%;
- Shanghai: 13.17%.

### DESCRIPTIVE RESULT

There is no common Asia-wide FIRST_HIKE directional response.

This further argues against treating realized Fed cycle markers as a universal Asia trading signal.

## 6. High-yield credit

### ICE BofA OAS

Current FRED coverage is too short for historical phase inference.

The one available FIRST_CUT cell is retained for provenance but is not interpreted.

Status:

**INSUFFICIENT_SUPPORT.**

### HYG price proxy

Broad-episode-weighted medians:

| Anchor | n broad episodes | +12M return | 12M MDD | MDD trough month | late-trough share |
|---|---:|---:|---:|---:|---:|
| FIRST_HIKE | 2 | -11.39% | 7.27% | 2 | 50% |
| LAST_HIKE | 2 | +4.33% | 0.82% | 3 | 0% |
| PAUSE_START | 2 | +6.75% | 0.82% | 1 | 0% |
| FIRST_CUT | 3 | -3.42% | **11.19%** | 8 | 100% |

### LIMITED-SUPPORT DIAGNOSTIC

HYG's FIRST_CUT path looks materially more stressful than PAUSE_START in these few episodes.

But:

- FIRST_CUT n=3 broad episodes;
- other phases n=2;
- HYG is a price proxy, not OAS.

No general credit-cycle rule is established.

## 7. Relation to the existing stress layer

STRESS-LAYER-005 found higher post-FIRST_CUT stress in:

- VIX;
- Baa-minus-10Y credit spread;
- copper.

ASIA-CREDIT-DIAG-006 adds:

- higher FIRST_CUT MDD than PAUSE_START across all four Asia indices;
- limited-support HYG price stress after FIRST_CUT.

Together these are consistent with:

**FIRST_CUT often occurring in a broader global stress-transition environment.**

They do not establish that the Fed cut causes the stress.

## 8. P0-C boundary

This module does **not** resolve P0-C.

Shanghai/Hang Seng results are:

- realized-Fed-cycle path descriptives;
- not Fed × China causal estimates;
- not conditional on a fully specified predetermined China state;
- not a monetary-policy shock identification design.

P0-C therefore remains:

**QUARANTINED / HYPOTHESIS-GENERATING.**

## 9. Evidence classification

### DATA FACT
- all four requested Asia indices were acquired;
- Asia timing/weight QC passed;
- ICE OAS current FRED history is truncated to recent years;
- HYG support is only 2–3 broad episodes.

### DESCRIPTIVE RESULT
- all four Asia markets have larger median 12M MDD after FIRST_CUT than PAUSE_START;
- endpoint return signs remain heterogeneous.

### LIMITED-SUPPORT DIAGNOSTIC
- HYG FIRST_CUT path appears more stressful than PAUSE_START in the few available episodes.

### CAUSAL EVIDENCE
None.

### FDR
Not applicable.

### OOS
Not applicable.

### DEPLOYMENT
Not deployable.

## 10. Product implication

PandaAI should not display:

`FIRST_CUT -> global risk resolved`

or:

`FIRST_CUT -> all Asia bearish`.

A more defensible object is:

`policy phase + region/asset + drawdown distribution + stress context + support strength`.

Support strength itself should be visible to the user.
