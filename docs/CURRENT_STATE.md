# Current state — 2026-09-24

## Repository role

This is the public PandaAI / macro-regime / cross-asset research and social-media companion.

The unpublished academic Fed-reaction-function paper remains in a separate private repository and is not mirrored here.

## Current public evidence state

### P0-A — Gold 8-regime statistical re-audit
Status: **DESCRIPTIVELY INTERESTING / CONFIRMATORY EVIDENCE INSUFFICIENT / NOT DEPLOYABLE**

Audited summary:
- 24 regime × horizon excess-return tests: 0/24 pass BH-FDR 10%;
- weekday robustness: 0/24;
- 21 non-intercept factorial tests: 0/21;
- null block bootstrap family: 0/24.

### P0-B — Point vs trend
Status: **PRIMARY HYPOTHESES NOT SUPPORTED**

Statistical detectability is kept separate from economic significance and tradability.

### P0-C — Fed × China / A-shares
Status: **QUARANTINED / HYPOTHESIS-GENERATING**

Existing Fed-only exploratory averages are not formal evidence because realized FOMC action is not an identified monetary-policy shock, the formal China predetermined-state layer is incomplete, and the exploratory testing family does not confirm a robust effect.

### Fed-cycle risk paths
Status: **QC-PASSED DESCRIPTIVE FOUNDATION / GOLD DAILY LONG-HISTORY SUPPORT LIMITED / NOT DEPLOYABLE**

FED-CYCLE-PATH-001 v1 is quarantined after post-run readback found a timing-ontology defect: modern target effective dates were not consistently separated from FOMC decision dates, the scheduled calendar supplement stopped at 2024, and pre-1994 reconstructed target changes were being over-labeled as emergency cuts.

v1.1 corrects those defects and passes hard timing QC. The mechanical registry contains 10 qualifying tightening legs beginning in 1983, 1984, 1987, 1987, 1988, 1994, 1999, 2004, 2015 and 2022. Pre-1994 anchors remain historical target reconstructions, not exact modern announcement timestamps.

FIRST_HIKE path-risk descriptives:

- S&P 500 n=10: 252D endpoint median +4.99%, MDD median 11.31%, full-recovery median 136 valid observations.
- Nasdaq n=10: 252D endpoint median -0.82%, MDD median 20.67%; full recovery observed for 9/10, median 181 observations.
- WTI n=8: 252D endpoint median +22.04%, MDD median 30.16%; full recovery observed for 7/8.
- Gold daily layer uses `GC=F` continuous COMEX futures proxy, not XAUUSD spot. FIRST_HIKE support is only n=3; 252D endpoint median +6.81%, MDD median 17.37%, full-recovery median 150 observations.

2015 vs 2022 Gold under the same frozen FIRST_HIKE specification differs materially: 2015 252D +6.81% versus 2022 -0.35%, while both had roughly 17-18% MDD. This is descriptive evidence that endpoint return alone is an incomplete risk statistic, not evidence that Fed hikes cause a particular Gold path.

No confirmatory p-value/FDR family is run in this foundation module. OOS is not applicable because this is not a forecasting model. Emergency-cut candidates with unresolved announcement timing are registry-only and excluded from asset metrics.


#### Gold long-history native-frequency layer

Status: **QC-PASSED DESCRIPTIVE LONG-HISTORY / DIRECTIONAL RULE NOT ESTABLISHED / NOT DEPLOYABLE**

A separate monthly Gold layer uses a pinned `datasets/gold-prices` source commit, 1960-01 through 2026-08, whose 1960+ data are sourced from World Bank Commodity Markets. Pre-1960 repeated annual averages are excluded. The event month is omitted from clean endpoints to avoid mixing pre/post-event prices.

All 10 frozen FIRST_HIKE tightening legs have clean monthly support.

FIRST_HIKE Gold descriptives:
- +1M median +1.55%;
- +3M +0.51%;
- +6M -1.90%;
- +12M +0.24%;
- +24M +0.58%;
- 24M MDD median 16.64%, range 3.83% to 39.10%.

This longer-history layer does **not** establish a stable directional Gold rule after the first hike. The stronger descriptive finding is wide endpoint dispersion combined with material path drawdown.

Recovery is handled with right-censoring:
- 50% recovery: 8/10 observed, 2/10 censored; Kaplan-Meier median 8 months;
- 100% recovery: 6/10 observed, 4/10 censored; Kaplan-Meier median 19 months;
- at 24 months, KM survival implies 50% of episodes had not yet fully recovered.

Cross-frequency diagnostics are not pooled. For 2004 and 2015, monthly +12M and daily `GC=F` +252-observation endpoint signs agree. For 2022 they differ: monthly +3.07% versus daily -0.35%, reinforcing that instrument/frequency/endpoint definitions can change endpoint narratives.

No confirmatory p-value/FDR family is run in the monthly foundation; OOS is not applicable; there is no causal or deployment claim.


#### Fed-cycle Gold state-dependence map

Status: **QC-PASSED DESCRIPTIVE / SMALL-N MECHANISM CANDIDATES / NOT CONFIRMATORY / NOT DEPLOYABLE**

FED-CYCLE-STATE-001 freezes seven state variables before conditioning Gold outcomes and keeps information timing explicit. Yield curve and WTI use strictly pre-event market history; CPI/INDPRO/NFCI use release-lag-aware current-vintage histories and are not labeled strict ALFRED PIT.

Supported FIRST_HIKE primary contrasts (n>=3 on both sides):

- inflation level HIGH vs LOW_OR_MODERATE: n=5/5; +12M Gold medians -11.76% vs +6.54%, 24M MDD 22.54% vs 13.66%; LOO contrast sign stable;
- inflation direction RISING vs FALLING_OR_FLAT: n=7/3; +12M +3.07% vs -11.76%, MDD 14.09% vs 19.91%; LOO sign stable;
- growth STRONG vs WEAK: n=6/4; +12M -3.51% vs +4.80%, MDD 18.16% vs 15.48%; LOO sign stable;
- WTI direction RISING vs FALLING_OR_FLAT: n=5/3; +12M +3.62% vs -2.58%, MDD 16.40% vs 13.66%; LOO sign stable.

These are hypothesis-generating state contrasts, not statistical significance or causal mechanism estimates.

Unsupported/identified limitations:

- 10Y-2Y curve: 0 inverted vs 10 positive — no cross-event contrast;
- nominal-10Y-minus-CPI real-rate proxy: 9 positive vs 1 nonpositive; `DFII10` support only n=3;
- NFCI: 2 tight vs 8 loose/average;
- USD direction passes the frozen source bridge (95.74% sign agreement) and has 5/5 support, but the groups are perfectly time-separated: all falling/flat cases are 1983-1988 and all rising cases are 1994-2022. USD is therefore `ERA-CONFOUNDED DESCRIPTIVE DIAGNOSTIC`, not a Gold-driver finding.

No p-values or BH-FDR are run in STATE-001; OOS is not applicable and no state is ranked as dominant.


#### Fed-cycle within-cycle continuous-state panel

Status: **QC-PASSED / PRIMARY ASSOCIATIONS NOT CONFIRMED / USD SECONDARY CANDIDATE ONLY / NOT DEPLOYABLE**

STATE-PANEL-002 replaces the n=10 event-level binary split with 165 monthly rows inside 10 mechanical tightening legs and 7 conservative broad episode clusters. The estimator uses cycle fixed effects, equal total weight per mechanical cycle and exact whole-episode sign-flip inference for overlapping forward outcomes.

Frozen primary family:

- CPI YoY × next-6M Gold return/MDD;
- CPI momentum × next-6M return/MDD;
- INDPRO YoY × next-6M return/MDD;
- WTI 6M return × next-6M return/MDD.

Result:

- **0/8 survive BY-FDR 10%;**
- **0/8 survive BH-FDR 10% diagnostic.**

This materially weakens the visually large binary STATE-001 contrasts. Those event-level patterns should not be upgraded into robust Gold regime rules.

Secondary USD diagnostic:

- full-sample coefficient ≈ +1.83 percentage points next-6M Gold return per within-cycle USD-return SD;
- broad-cluster exact p=0.03125;
- sign remains positive after excluding 2022 and in 1994+ restrictions;
- however the full 12-test secondary family has 0 BH/BY FDR survivors; USD BH q=0.375 and BY q=1.00.

USD therefore remains a **mechanism candidate / not multiplicity-confirmed**.

Yield curve, nominal 10Y, simple real-rate proxy and NFCI show no confirmatory secondary evidence; actual DFII10 support remains only 3 cycles.

No causal/OOS/deployment claim.


#### Cross-asset FIRST_HIKE risk clock

Status: **QC-PASSED DESCRIPTIVE RISK CLOCK / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

RISK-CLOCK-003 uses 24 complete months after the FIRST_HIKE event month, broad-episode weighting and right-censoring-aware recovery analysis.

Primary support:
- Gold: 10 mechanical legs / 7 broad episodes;
- Nasdaq: 10 / 7;
- S&P 500: 10 / 7;
- WTI: 8 / 6.

Weighted median 24M MDD-trough month:
- Nasdaq: **7**;
- S&P 500: **11**;
- Gold: **12**;
- WTI: **15**.

MDD-trough timing shares:
- Gold: 0% in months 1-6, 50% in 7-12, 50% in 13-24;
- Nasdaq: 40.48% / 33.33% / 26.19%;
- S&P 500: 33.33% / 19.05% / 47.62%;
- WTI: 33.33% / 5.56% / 61.11%.

Broad-episode-weighted median 24M MDD:
- Gold 14.09%;
- Nasdaq 12.18%;
- S&P 500 8.47%;
- WTI 20.65%.

Broad-episode-weighted full-recovery KM medians from the 24M-window MDD trough:
- Gold 13 months;
- Nasdaq 8;
- S&P 500 9;
- WTI 8.

The earlier equal-mechanical-leg Gold survival estimate was 19 months for full recovery. The 13-month estimate is a weighting sensitivity under broad-episode weighting, not a contradiction.

The main descriptive conclusion is asset-specific timing: Nasdaq is more front-loaded, S&P retains a large late tail, Gold is mid/late distributed, and WTI is the most late-concentrated. Month 24 is the frozen window boundary and must not be described as a natural hazard spike.

No p-value/FDR family is run; no causal/OOS/deployment claim.


#### Multi-anchor Fed-cycle phase clock

Status: **QC-PASSED DESCRIPTIVE PHASE MAP / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

PHASE-CLOCK-004 applies one common 12-complete-month convention to FIRST_HIKE, LAST_HIKE, PAUSE_START and FIRST_CUT across Gold, S&P 500, Nasdaq and WTI. All **16/16 primary asset × phase cells** satisfy the frozen support rule.

Selected broad-episode-weighted medians:

- Gold FIRST_HIKE / LAST_HIKE / PAUSE_START / FIRST_CUT 12M MDD: 11.58% / 9.09% / 7.57% / 5.43%;
- S&P 500: 5.86% / 4.22% / 4.22% / **13.99%**;
- Nasdaq: 12.18% / 4.00% / 4.00% / **17.48%**;
- WTI: 18.79% / 19.60% / 17.99% / **22.23%**.

FIRST_CUT late-window MDD-trough shares (months 7-12):

- Gold 50.0%;
- S&P 500 90.48%;
- Nasdaq 90.48%;
- WTI 100%.

Median +12M endpoints after FIRST_CUT:

- Gold +4.06%;
- S&P +10.98%;
- Nasdaq +6.04%;
- WTI -16.94%.

The phase map therefore does **not** support a universal "first cut = risk is over" narrative. Gold differs from equities/WTI, and positive endpoints can coexist with deep later drawdowns.

The same cycles can appear under multiple anchors and windows overlap, so no independent cross-phase p-value/FDR ranking is performed. Realized anchors remain descriptive cycle markers, not identified monetary-policy shocks.


#### Fed-cycle stress-state layer

Status: **QC-PASSED DESCRIPTIVE STRESS MAP / MECHANISM CONTEXT ONLY / NOT DEPLOYABLE**

STRESS-LAYER-005 adds VIX, Moody's Baa-minus-10Y spread and copper to the same four policy phases.

All **12/12 observable × phase cells** pass the frozen support rule.

FIRST_CUT versus FIRST_HIKE broad-episode-weighted median stress:

- VIX maximum 12M increase: **+8.53 points vs +4.26**;
- Baa–10Y maximum widening: **+38 bp vs +16 bp**;
- copper 12M MDD: **19.96% vs 6.84%**.

FIRST_CUT stress timing:

- VIX median maximum-stress month 8;
- Baa spread median maximum-widening month 7;
- copper median MDD-trough month 9.

Together with PHASE-CLOCK-004, this is consistent with FIRST_CUT often occurring around a broader deterioration/stress transition rather than an immediate all-clear state.

This is **mechanism context, not causal evidence**: the Fed can cut in response to worsening conditions, making endogeneity/reverse causality central. No optimized stress thresholds, p-value/FDR family, OOS forecast or deployment claim are produced.


#### Asia equity + high-yield credit diagnostics

Status: **QC-PASSED DESCRIPTIVE / ASIA DIAGNOSTIC SUPPORT / HY CREDIT LIMITED OR INSUFFICIENT / NOT CAUSAL / NOT DEPLOYABLE**

ASIA-CREDIT-DIAG-006 extends the four-phase map to Hang Seng, Shanghai Composite, Nikkei 225, KOSPI and high-yield credit context.

Asia support:
- Nikkei: FIRST_HIKE/LAST_HIKE/FIRST_CUT 10 mechanical legs / 7 broad episodes; PAUSE_START 7/7;
- Hang Seng: 8/6 for FIRST_HIKE/LAST_HIKE/FIRST_CUT and 6/6 for PAUSE_START;
- Shanghai Composite: 4/4 broad episodes per phase under the available Yahoo history;
- KOSPI: 4/4 per phase.

Across all four Asia indices, the broad-episode-weighted median 12M MDD after FIRST_CUT is higher than after PAUSE_START:

- Hang Seng: 13.03% -> **15.62%**;
- Nikkei 225: 8.37% -> **12.61%**;
- KOSPI: 7.67% -> **16.40%**;
- Shanghai Composite: 6.39% -> **8.59%**.

FIRST_CUT +12M endpoint signs remain heterogeneous:
- Hang Seng -8.67%;
- Shanghai -28.73%;
- Nikkei +9.60%;
- KOSPI +4.31%.

Thus higher path risk does not imply a universal negative endpoint.

High-yield credit:
- current FRED `BAMLH0A0HYM2` distribution exposes only recent history and yields only 1/1 FIRST_CUT support in this frozen run -> **INSUFFICIENT_SUPPORT**;
- a separately frozen HYG ETF price proxy has only 2-3 broad episodes -> **LIMITED_SUPPORT**;
- HYG is not pooled with OAS and is not treated as an OAS substitute.

The existing P0-C China identification quarantine remains unchanged. These are realized-Fed-cycle path diagnostics, not Fed-to-China causal estimates.

No p-value/FDR family, OOS forecast or deployment claim.


#### Real-time macro vintage audit

Status: **QC-PASSED REVISION AUDIT / GOLD RETURN ASSOCIATION STRENGTHENED UNDER REAL-TIME IPT / MDD NOT CONFIRMED / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

VINTAGE-AUDIT-007 replaces current-revised industrial production with Federal Reserve Bank of Philadelphia RTDSM monthly `IPT` vintages under a conservative rule: for information month M, use only a vintage no later than M-1, while keeping the original M-2/M-14 YoY definition and the frozen 2% STRONG/WEAK threshold.

Official workbook QC:
- 477,136 parsed cells;
- 766 vintages from 1962-11 through 2026-08;
- 10/10 FIRST_HIKE events supported;
- 165/165 within-cycle monthly rows supported;
- zero vintage-timing, target-period or weighting violations.

Event-level revisions:
- 1/10 growth-state labels flips;
- 2022 changes from current-revised WEAK (+1.32% YoY) to real-time STRONG (+4.12%);
- FIRST_HIKE-event median absolute YoY revision gap = 2.225pp, max = 4.035pp.

Event-level Gold revision impact:
- +12M STRONG-minus-WEAK median return contrast remains negative: -8.31pp current labels versus -9.12pp real-time labels;
- +24M contrast weakens from -16.07pp to -5.50pp;
- 24M MDD contrast changes from +2.67pp to -0.47pp, so the prior MDD separation is revision-fragile.

Within-cycle same 165-row Gold next-6M return:
- current-vintage INDPRO beta ≈ -1.27pp per within-cycle SD, broad exact p=0.125;
- real-time IPT beta ≈ **-1.96pp**, broad exact p=**0.015625**;
- all seven broad-episode score contributions are negative;
- excluding 2022: beta ≈ -1.49pp, raw broad exact p=0.03125;
- excluding early B01/B02: beta ≈ -2.99pp, p=0.0625 with only five broad episodes.

The small full-sample exact p largely reflects 7/7 broad-cluster sign unanimity. This is a **revision-robust associational mechanism candidate**, not a retroactive confirmatory discovery, not an OOS forecast, and not a trading signal.

Gold next-6M MDD remains unsupported under real-time IPT.

CPI boundary:
- original inflation state uses `CPIAUCNS` (not seasonally adjusted);
- Philadelphia Fed `PCPI` is seasonally adjusted and is not substituted;
- CPI is therefore not upgraded to a strict real-time-vintage object by this module.


#### Gold real-time growth OOS audit

Status: **PRELIMINARY OOS CANDIDATE / WEAK AND BENCHMARK-SENSITIVE / NOT CAUSAL / NOT DEPLOYABLE**

OOS-008 uses a frozen episode-forward design for next-6M Gold returns:

- train B01-B03 -> test B04;
- train B01-B04 -> test B05;
- train B01-B05 -> test B06;
- train B01-B06 -> test B07.

No random split, no within-test refitting, no hyperparameter search and no target-window leakage.

Frozen models:
- B0 historical mean;
- B1 lagged Gold 3M/6M returns + lagged 6M volatility;
- B2 B1 + months since FIRST_HIKE;
- M3 B2 + real-time IPT YoY;
- D4 B2 + current-revised INDPRO diagnostic.

M3 passes the predeclared preliminary gate:
- episode-equal MSE is **21.27% lower than B2**;
- M3 beats B2 in **3/4** future broad episodes;
- OOS R² versus B0 = **+3.38%**.

However the benchmark sanity audit materially limits the claim:
- versus B0, M3 MSE improves only **3.38%** and wins only 2/4 episodes;
- versus B0, M3 MAE is **2.74% worse** and wins only 1/4 episodes;
- M3 versus current-vintage D4 improves MSE 6.80% and MAE 3.53%, winning 3/4 episodes;
- episode-equal M3 signed bias is -2.84pp and calibration varies strongly by episode;
- M3 prediction range (-14.7% to +12.6%) compresses the realized upside tail (-14.1% to +41.5%).

The correct evidence label is therefore **PRELIMINARY OOS CANDIDATE / BENCHMARK-SENSITIVE**, not validated predictor or trading edge.

B04-B07 are now consumed OOS evidence for this specification and must not be reused for parameter tuning.

#### Prospective Gold shadow validation architecture

Status: **QC-PASSED PROSPECTIVE ARCHITECTURE FROZEN / ARMED / NO NEW FORECAST EVIDENCE YET / NOT DEPLOYABLE**

PROSPECTIVE-SHADOW-009 converts the consumed historical OOS experiment into an append-only future validation protocol without changing the OOS-008 specification.

Hard anti-contamination rules:
- B04-B07 remain consumed OOS evidence and cannot be used for feature, threshold, transformation, horizon or model tuning;
- B0/B1/B2/M3 definitions remain frozen;
- a new prospective broad episode is fit once using prior episodes only;
- active-episode outcomes never enter training;
- no within-episode refit;
- no retroactive prediction after cycle qualification;
- issued predictions are append-only and retain model/input provenance hashes.

Current 2026 eligibility gate:
- candidate FIRST_HIKE: 2026-09-16;
- observed hikes in the current edge run: **1**;
- cumulative tightening: **25 bp**;
- frozen mechanical-cycle qualification requires **at least 2 hikes and at least 50 bp**;
- current candidate therefore **does not qualify**;
- if a later continuation satisfies the frozen rule, the next broad episode would be **B08** under the existing >18-month clustering rule;
- current prospective prediction registry rows: **0**.

QC passes with zero duplicate policy dates, zero sorting/sign-label violations, zero automatic prediction rows and explicit prohibition of retroactive predictions and historical-OOS specification tuning.

Model specification SHA256:
`fcaebf36a65ccd12dd7aa1cbb83450589e37ea852b638ad0cb60f43f2d16558b`.

This milestone is forecasting infrastructure, not new positive forecast evidence. No B08 forecast is issued yet.

#### Prospective input timing audit

Status: **QC-PASSED SOURCE-TIMING AUDIT / EXACT OOS-008 LIVE TRANSPORT FAILS / REPAIR REQUIRED / NOT DEPLOYABLE**

INPUT-TIMING-010 tests whether the exact historical OOS-008 input contract can be used in SHADOW-009 before any part of the forecast target month is observed.

Gold source audit:
- 6 recent uncensored monthly introductions reconstructed from `datasets/gold-prices` commit history;
- **6/6** first appear only after the following month has already begun;
- release lag versus next-month start ranges from **51.7 to 107.7 hours**;
- exact pre-target Gold input availability therefore fails.

Current RTDSM probe:
- next-month probe 2026-10;
- required IPT observation 2026-08;
- last workbook vintage 2026-08;
- frozen RT-IPT YoY not yet computable for that probe;
- classified as current source refresh pending, not yet a permanent RTDSM structural failure.

Result:

**SOURCE_TIMING_REPAIR_REQUIRED.**

No forecast is issued, no forecast performance is evaluated, OOS-008 is unchanged and B04-B07 remain consumed. The next research task is a separately frozen Gold live-source bridge audit; any proxy specification starts without inherited prospective validation evidence.

#### Gold live-source feature bridge

Status: **QC-PASSED PROXY FEATURE BRIDGE CANDIDATE / NO FORECAST PERFORMANCE EVIDENCE / NOT DEPLOYABLE**

GOLD-LIVE-BRIDGE-011 tests whether a same-month observable `GC=F` continuous COMEX Gold futures proxy can reproduce the Gold input features used by OOS-008 closely enough for a separately versioned prospective measurement specification.

Frozen construction:
- daily `GC=F` closes;
- calendar-month arithmetic mean;
- minimum 10 daily observations;
- no scaling/calibration/regression mapping;
- no forecast targets or M3 errors loaded.

Feature-complete overlap: **306 months, 2001-03 to 2026-08**.

Key source-equivalence diagnostics:
- monthly level median absolute gap **0.13%**, p95 **0.71%**;
- 3M return correlation **0.99839**, median absolute difference **0.19pp**, sign agreement **99.02%**;
- 6M return correlation **0.99939**, median absolute difference **0.17pp**, sign agreement **99.02%**;
- 6M volatility correlation **0.99280**, median absolute difference **0.000855**;
- era-specific 3M/6M sign agreement is at least **98.11%** in every frozen era.

All **17/17** predeclared engineering gates pass.

Result:

**PROXY_FEATURE_BRIDGE_CANDIDATE.**

This does not revalidate OOS-008 with futures data and does not transfer its historical OOS label automatically. It only supports building a separately versioned prospective measurement amendment. Yahoo/raw market-data licensing is also not treated as resolved for production deployment.

#### Proxy-measurement prospective Gold model

Status: **QC-PASSED MODEL FREEZE / PROXY-MEASUREMENT SHADOW READY / NO PROSPECTIVE EVIDENCE YET / NOT DEPLOYABLE**

PROSPECTIVE-GCF-012 converts the successful BRIDGE-011 measurement result into a separately versioned future model without changing OOS-008.

Frozen training:
- 165 historical rows;
- B01-B07;
- latest realized training target end 2025-01;
- zero target overlap with the 2026 candidate;
- hierarchical broad-episode weighting passes.

Frozen hashes:
- prospective spec: `f3d3eff3020af41665da93151962d0a488b14f642bf3e7e68dcf16cb156787b4`;
- training model: `96520e9316a0cbcc18085f0dfa2d7432fab9892d715e7893fcf5ad2b172ba50d`.

Historical fitting still uses the original World Bank Gold features. Only future live Gold inputs are allowed to use the BRIDGE-011 GC=F monthly-mean measurement contract.

The current 2026 edge run is still 1 hike / 25 bp, below the frozen 2-hike / 50 bp rule. Therefore prediction registry rows remain **0**.

012 does not inherit OOS-008's preliminary OOS label. Its evidence status is **PROXY_MEASUREMENT_SHADOW_READY_NO_PROSPECTIVE_EVIDENCE**.





### Household inflation / energy
Status: **MECHANISM CANDIDATE / NOT A TRADING SIGNAL**

The public work distinguishes crude shocks from downstream refined-product amplification. Refined-product pressure is useful as a household-energy pressure monitor but is not yet a validated next-month cross-asset predictor.

### Commodity reversal / physical energy
Status: **RISK-STATE RESEARCH USEFUL / DIRECTIONAL EDGE NOT ESTABLISHED / NOT DEPLOYABLE**

#### Price/product layer

The exhaustive public-source monthly walk-forward covers 1990-04 to 2026-08.

QC:
- 437 complete common months;
- 13 de-clustered rollover events;
- 6 price/product-confirmed events;
- 7 false-relief veto events.

Primary result: **0/4 pass BH-FDR 10%**; adjusted q≈0.224.

The strongest descriptive use remains asymmetric: the price/product filter looks more promising as a **false-relief / no-short risk veto** than as a positive short signal.

#### Release-aware physical-stock layer

The first release parser was found to be invalid because it truncated the historical registry and produced impossible 2017→2026 mappings for some later events. That execution is quarantined.

The corrected event-scoped EIA release registry preserves:
- 13 frozen price events;
- 12 strict-PIT physical events;
- zero bad timing mappings.

Corrected P4A_DATA_ONLY support:
- 3 P4A events;
- 9 physical-veto events;
- 1 strict-PIT unavailable event.

Frozen four-test family: **0/4 pass BH-FDR 10%; q=1.00**.

Within the six completed strict-PIT PRICE_PRODUCT_CONFIRMED episodes, all three P4A_DATA_ONLY episodes had positive WTI returns at both 3M and 6M. This falsifies the narrow idea that the current inventory-normalization rule is a reliable falling-WTI confirmation. It does not establish the opposite rule because n is only 3.

#### Stock-flow mechanism map

FLOW-002 adds product supplied, refinery crude inputs, field production and crude imports.

Among strict-PIT price-confirmed episodes:
- complete flow support: 4;
- FLOW_DD: 0;
- FLOW_SN: 1;
- FLOW_MIXED: 3.

The single FLOW_SN episode was not bearish. 2008 was still FLOW_MIXED at the release-aware decision date before its large later collapse; 2022 and 2023 show that weaker product-supplied components can coexist with different subsequent WTI directions.

Current conclusion:

**stocks and flows improve mechanism understanding, but do not yet provide a validated directional timing signal.**

## Immediate public queue

1. Preserve the failed stock-only rule and FLOW-002 as negative/mechanism evidence; do not retune them.
2. Design a genuinely weekly/daily PIT commodity event engine to remove monthly-average timing limitations and increase event support.
3. Freeze an independent geopolitical/physical shock registry before any full P4A claim.
4. PROSPECTIVE-GCF-012 is now frozen and QC-passed with immutable spec/model hashes, but the 2026 edge run remains 1 hike / 25 bp and ineligible. Build the append-only issuance engine next; it must refuse duplicate, retroactive, late or input-incomplete forecasts and must create zero predictions until every frozen gate passes.
5. Resolve official announcement timing for registry-only emergency-cut candidates before any emergency-event outcome study.
6. Continue provenance-safe charts/content cards tied to the evidence ledger.
7. Keep paper-specific identification work behind the firewall.
