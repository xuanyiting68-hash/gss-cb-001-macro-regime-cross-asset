# FED-CYCLE-CROSS-ASSET-EXPANSION-014 — Closeout

Date: 2026-09-24  
Status: **QC-PASSED DESCRIPTIVE CROSS-ASSET EXTENSION / SHORT-HISTORY PROXIES LIMITED / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

## 1. Purpose

EXPANSION-014 extends the public Fed-cycle phase clock into:

- long-duration U.S. Treasury ETF proxy (TLT);
- listed U.S. REIT ETF proxy (VNQ);
- Bitcoin (BTC-USD);
- DXY;
- S&P Cotality Case-Shiller U.S. National Home Price Index;
- 2Y and 10Y Treasury yields;
- a mechanical effective-fed-funds cash-carry benchmark.

The design was frozen before outcomes were executed.

## 2. QC

QC passed:

- 10 frozen mechanical tightening cycles;
- 7 broad episodes;
- 4/4 requested market assets acquired;
- 68 liquid-market cycle × phase rows;
- 28 housing rows;
- 74 Treasury-yield rows;
- 37 cash rows;
- 0 negative-MDD/decline violations;
- 0 broad-episode weight violations;
- 0 support-label violations;
- 0 current-2026-cycle leakage;
- no raw Yahoo or Case-Shiller source history committed.

The live 2026 cycle remains excluded from completed historical outcome summaries.

## 3. Rates: the cleanest phase structure in 014

Broad-episode-weighted medians:

| Anchor | 2Y +12M change | 10Y +12M change |
|---|---:|---:|
| FIRST_HIKE | +123 bp | +56 bp |
| LAST_HIKE | -125 bp | -60 bp |
| PAUSE_START | -128 bp | -108 bp |
| FIRST_CUT | -167 bp | -20 bp |

### DESCRIPTIVE RESULT

The front end and long end generally continue upward after FIRST_HIKE in the historical phase map, while yields are generally lower after LAST_HIKE / PAUSE_START / FIRST_CUT.

The 2Y decline is especially large around FIRST_CUT in the weighted marginal median.

This is **not** a bond-return table and does not identify the causal effect of policy changes. The separate 2Y and 10Y medians also should not be subtracted and called a median curve change without a direct joint calculation.

## 4. Cash: high-rate plateau matters

Mechanical DFF-based 12M carry medians:

| Anchor | 12M mechanical cash carry |
|---|---:|
| FIRST_HIKE | 4.73% |
| LAST_HIKE | 5.94% |
| PAUSE_START | 5.88% |
| FIRST_CUT | 4.49% |

### DESCRIPTIVE RESULT

In historical tightening cycles, the highest median mechanical cash carry occurs around LAST_HIKE / PAUSE_START, when the policy level is already high but cuts have not yet removed much carry.

This helps explain why allocation decisions late in a hiking cycle face a genuine hurdle rate: risky assets must compensate for an unusually competitive cash alternative.

The benchmark ignores fees, taxes and intra-month compounding.

## 5. Long-duration Treasury proxy: duration can rally before/around easing, but episode heterogeneity is large

TLT has only 3 broad episodes, so every phase is **LIMITED_DESCRIPTIVE**.

Weighted medians:

| Anchor | +12M | 12M MDD |
|---|---:|---:|
| FIRST_HIKE | +1.10% | 14.79% |
| LAST_HIKE | +5.63% | 4.98% |
| PAUSE_START | +8.69% | 4.98% |
| FIRST_CUT | +15.13% | 3.63% |

But episode-level FIRST_HIKE +12M returns were:

- 2004: +22.27%;
- 2015: +1.10%;
- 2022: -22.51%.

FIRST_CUT +12M:

- 2007: +15.13%;
- 2019: +29.71%;
- 2024: -4.24%.

### INTERPRETATION

The duration channel is real, but “first cut = long bonds always rally” is not supported by three heterogeneous episodes. Term premium, inflation persistence, fiscal/issuance conditions and the path of long rates remain relevant.

## 6. Listed REITs are not direct housing

VNQ also has only 2-3 broad episodes.

Weighted medians:

| Anchor | +12M | 12M MDD |
|---|---:|---:|
| FIRST_HIKE | -17.76% | 11.45% |
| LAST_HIKE | +18.98% | 9.42% |
| PAUSE_START | +23.52% | 9.42% |
| FIRST_CUT | -4.65% | 18.79% |

FIRST_CUT +12M by episode:

- 2007: -4.65%;
- 2019: -7.09%;
- 2024: +3.62%.

### DESCRIPTIVE RESULT

Listed REITs do not mechanically behave like direct house prices. They combine:

- duration sensitivity;
- equity risk;
- leverage/refinancing risk;
- property fundamentals;
- credit-spread exposure.

The FIRST_CUT sample is particularly useful as a warning against equating lower policy rates with immediately safer real-estate equity.

## 7. Bitcoin: regime heterogeneity dominates a two-episode sample

BTC has only 2 broad episodes and is therefore **LIMITED_DESCRIPTIVE**.

Weighted medians:

| Anchor | +3M | +6M | +12M | 12M MDD |
|---|---:|---:|---:|---:|
| FIRST_HIKE | -40.18% | -51.42% | -38.38% | 12.36% |
| LAST_HIKE | -26.43% | +54.59% | +34.78% | 7.23% |
| PAUSE_START | +39.30% | +143.07% | +116.71% | 11.49% |
| FIRST_CUT | -10.66% | -10.90% | +1.85% | 14.92% |

These weighted medians must not be treated as stable population parameters.

The episode split is more informative:

FIRST_HIKE +12M:
- 2015: +137.35%;
- 2022: -38.38%.

FIRST_CUT +12M:
- 2019: +1.85%;
- 2024: +88.87%.

PAUSE_START +12M:
- 2019 episode: +125.67%;
- 2023 episode: +116.71%.

### INTERPRETATION

The small sample is consistent with Bitcoin behaving as a high-beta liquidity/risk asset whose path is highly state dependent, but 014 does not establish a Fed-cycle trading rule.

## 8. DXY: useful context, not a universal direction

DXY has full long-history support in this module.

Weighted +12M medians:

- FIRST_HIKE: +3.01%;
- LAST_HIKE: -1.26%;
- PAUSE_START: -1.26%;
- FIRST_CUT: -1.33%.

FIRST_HIKE 12M MDD median is about 8.24%; the other phase medians are roughly 5.18%-6.30%.

### DESCRIPTIVE RESULT

The dollar has a modest phase pattern in the aggregate medians, but not one strong enough to justify “hikes = dollar up” as a deterministic cross-asset rule.

This reinforces the existing Gold work: USD should remain a state/context variable, not a standalone causal Gold signal.

## 9. Direct housing: slow, smoothed, nominal and tail-sensitive

Case-Shiller support passes the frozen descriptive threshold.

Weighted nominal medians:

| Anchor | +12M | +24M | 24M decline |
|---|---:|---:|---:|
| FIRST_HIKE | +5.29% | +11.82% | 0.03% |
| LAST_HIKE | +3.47% | +7.34% | 0.44% |
| PAUSE_START | +3.76% | +5.55% | 0.13% |
| FIRST_CUT | +5.21% | +12.69% | 0.00% |

These medians are **not** evidence that housing is immune to tightening.

The crisis tail matters:

- PAUSE_START in the 2004 cycle (2006-08-08 anchor): +24M = -11.01%, 24M decline = 11.01%;
- FIRST_CUT in the 2004 cycle (2007-09-18 anchor): +24M = -16.98%, 24M decline = 18.71%.

### INTERPRETATION

National nominal house prices are slow and smoothed relative to liquid markets. Supply constraints, mortgage structure, leverage, credit availability and starting valuation can dominate the simple policy-phase label.

The current 014 housing result should therefore be used as a balance-sheet / slow-cycle diagnostic, not a tradable phase signal.

## 10. Cross-asset synthesis with PHASE-CLOCK-004 and STRESS-LAYER-005

The expanded evidence supports a more coherent historical cycle map:

### Early tightening / FIRST_HIKE
- 2Y and 10Y yields tend to keep rising;
- cash carry is building;
- S&P/Nasdaq historical endpoint medians can still be positive, but path risk is nontrivial;
- WTI has historically been strong on the median, consistent with some hikes beginning in firm nominal-demand/inflation states;
- Gold direction is mixed;
- TLT/VNQ/BTC show strong episode heterogeneity.

### Late tightening / LAST_HIKE and PAUSE_START
- Treasury yields tend to decline;
- cash carry remains historically high;
- S&P/Nasdaq PAUSE_START medians were strong with relatively shallow MDD in the long-history phase module;
- long-duration TLT and VNQ have positive limited-sample medians;
- this is not yet an “all clear”: stress can still migrate into later phases.

### FIRST_CUT
- 2Y yields decline strongly in the historical median;
- cash still earns positive carry, but the hurdle is falling;
- TLT has a positive limited-sample median;
- S&P/Nasdaq have positive +12M medians but much deeper MDD than after PAUSE_START;
- VIX, Baa spread and copper stress are historically worse than around PAUSE_START;
- WTI has a negative +12M median and very late drawdown concentration;
- VNQ has a negative limited-sample median;
- direct housing can remain positive in the national median while severe credit/housing episodes create large negative tails.

Therefore:

**FIRST_CUT is better interpreted as a transition in the discount-rate path occurring alongside a potentially deteriorating growth/credit state, not as a universal risk-on trigger.**

## 11. What 014 changes for PandaAI

PandaAI should separate at least four state axes:

1. **Policy phase / expected rate path**
2. **Growth and earnings / demand state**
3. **Inflation, energy and real-rate state**
4. **Credit / volatility / liquidity stress**

Then attach each asset's historical path distribution and support strength.

The product should expose:
- phase;
- asset;
- historical endpoint distribution;
- drawdown distribution;
- trough timing;
- evidence/support label;
- current stress state;
- invalidation / missing-data flags.

It should not compress those dimensions into one deterministic “Fed bullish/bearish” badge.

## 12. Evidence classification

### DATA FACT
- frozen 014 implementation and QC passed;
- all four market acquisitions succeeded;
- no current-2026 outcome leakage;
- no raw copyrighted market/housing histories committed.

### DESCRIPTIVE RESULT
- yields show the clearest phase transition;
- cash carry is highest around LAST_HIKE/PAUSE in historical medians;
- TLT/VNQ/BTC are highly episode-dependent and short-history;
- direct housing medians are slow/smoothed and can hide severe downside tails.

### CAUSAL EVIDENCE
None.

### FDR
Not applicable.

### OOS
Not applicable.

### DEPLOYMENT
Not deployable.
