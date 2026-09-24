# Current state — 2026-09-25

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

#### Append-only prospective issuance gate

Status: **QC-PASSED FAIL-CLOSED ISSUER / WAITING CYCLE QUALIFICATION / ZERO PREDICTIONS / NOT DEPLOYABLE**

PROSPECTIVE-ISSUANCE-013 loads the immutable GCF-012 spec/model hashes and can only append a prediction after every frozen eligibility, timing and input gate passes.

First execution:
- candidate forecast month: 2026-10;
- GCF-012 spec hash: matched;
- frozen training-model hash: matched;
- BRIDGE-011 status: matched;
- current 2026 cycle: 1 hike / 25 bp;
- cycle eligibility: **False**;
- refusal reason: `WAITING_CYCLE_QUALIFICATION`;
- live Gold/RTDSM inputs were deliberately not fetched after the structural gate failed;
- model fitting: none;
- retroactive month search: none;
- predictions issued: **0**;
- registry rows after run: **0**.

The issuer therefore behaves fail-closed rather than manufacturing a forecast before the frozen 2-hike / 50 bp condition is satisfied.

Before a first real issuance, registry integrity should be strengthened with a cryptographic append-only hash chain; this is an audit-engineering amendment and does not alter the research specification.

#### Issuance registry cryptographic integrity

Status: **QC-PASSED GENESIS CHAIN / ZERO PREDICTIONS / RESEARCH SPEC UNCHANGED**

PROSPECTIVE-ISSUANCE-013 v1.1 hardens the empty prospective registry before any real prediction exists.

Current integrity state:
- prediction rows: 0;
- chain rows: 0;
- exact registry SHA256: `c8e3cfb9eeb9c748d7ae8e9f8909be6713425ccd07f6019ef24d7fb38561c971`;
- genesis/tail hash: `15c8893f10480bf408a72b705eb83015d407d9d0bb0fc23c519b3591b5656e4a`;
- prior rows immutable: PASS;
- full chain recomputation: PASS;
- research specification changed: False.

Before every later issuance, the wrapper requires the exact registry file hash, row count, chain links and tail hash to match the previously committed integrity state. After an issuance it permits growth of only 0 or 1 row and chains any new row to the previous tail hash.

This is tamper-evident provenance, not a digital signature. Git permissions/history remain separate controls.







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

#### Weekly strict-PIT energy release clock

Status: **QC-PASSED FULL RELEASE CLOCK / NO OUTCOME EVIDENCE**

ENERGY-WEEKLY-PIT-003 reconstructs the EIA weekly petroleum information clock from 2002 through 2026 using the TWIP archive through 2025-10-24 and WPSR schedule thereafter.

Final QC:
- 1,250 rows in 2002-2025;
- 1,288 total rows through 2026-09-18;
- release lag 5-10 days, median 5;
- 99.84% common physical-grid mapping coverage;
- 22/22 curated official mappings reproduced;
- 14 2025-2026 holiday exceptions parsed;
- all hard schedule anchors pass.

Weekly observations are therefore no longer treated as known on their week-ending date.

#### Weekly strict-PIT price × stock-flow engine

Status: **QC PASS / PRIMARY FAMILY INSUFFICIENT SUPPORT / CURRENT LIVE EVENT AVAILABLE / NOT DEPLOYABLE**

ENERGY-WEEKLY-STATE-004 produces 17 de-clustered strict-PIT rollover events from 1,288 release states.

Mechanism counts:
- TIGHT_OR_MIXED 11;
- DEMAND_DESTRUCTION 4;
- SUPPLY_NORMALIZATION 1;
- DATA_INCOMPLETE 1.

The frozen SUPPLY_NORMALIZATION vs TIGHT_OR_MIXED primary family cannot be estimated because SUPPLY_NORMALIZATION has only one event versus the required minimum five.

Descriptively:
- completed TIGHT_OR_MIXED 8W / 13W median WTI returns are +7.08% / +6.70%, with median short MAE +15.24% / +17.92%;
- DEMAND_DESTRUCTION 8W / 13W medians are -2.36% / -7.07%, with 75% negative at 13W;
- the single SUPPLY_NORMALIZATION event is negative at 8W and 13W with low short MAE, but n=1 prevents inference.

The 2026-09-23 selected event is currently TIGHT_OR_MIXED and has no realized 4/8/13-week outcomes in the canonical panel. It should be frozen prospectively rather than used for retrospective tuning.

#### Weekly energy post-run veto robustness

Status: **QC PASS / POST-RUN DESCRIPTIVE / 8W VETO ROBUST / 13W MODERN DECAY / NOT DEPLOYABLE**

ENERGY-WEEKLY-STATE-004A does not create a new p-value family and does not alter any 004 threshold.

For completed TIGHT_OR_MIXED events:
- full-sample 8W median WTI +7.08%, only 20% negative;
- 8W median remains positive in every leave-one-out run;
- excluding all 2004 events, 8W median remains +6.61%;
- 2018-present 8W median remains +6.61% with 33.3% negative;
- 2018-present 13W median falls to only +1.26% with 50% negative.

Therefore the most defensible descriptive use of TIGHT_OR_MIXED is an **8-week bearish-confirmation veto**, not a durable 13-week bullish signal.

DEMAND_DESTRUCTION remains a post-run mechanism candidate:
- n=4;
- 13W median WTI -7.07%;
- 75% negative at 13W.

Because this pattern was observed after 004, it is not promoted to confirmatory evidence.

#### Prospective weekly energy event registry

Status: **QC PASS / FIRST LIVE EVENT FROZEN / ZERO REALIZED LIVE OUTCOMES / NOT DEPLOYABLE**

ENERGY-WEEKLY-PROSPECTIVE-005 freezes selected 004 events only while all 4W/8W/13W outcomes remain blank.

First live event:
- ID `ENERGY005_2026-09-23`;
- week end 2026-09-18;
- release date 2026-09-23;
- price as of 2026-09-22;
- mechanism TIGHT_OR_MIXED;
- interpretation `ROLLOVER_WITHOUT_CLEAN_PHYSICAL_CONFIRMATION`;
- inventories improving 2/3;
- demand weak 1/3;
- throughput weak True;
- upstream supply improvement 1/2.

Historical same-class distribution was frozen at registration using 10 completed prior events:
- median WTI 8W +7.08%;
- median WTI 13W +6.70%;
- median short MAE 8W +15.24%;
- median short MAE 13W +17.92%.

The prospective registry has one row, one SHA256 chain row and **zero realized outcomes**. The event classification cannot be rewritten after outcome maturity.

#### Prospective maritime external-shock context

Status: **QC PASS / EXTERNAL SUPPLY-SHOCK CONTEXT PRESENT / CURRENT OUTCOME STILL UNREALIZED / NOT DEPLOYABLE**

ENERGY-PORTWATCH-006 adds a retrieval-time IMF PortWatch layer to the already-frozen `ENERGY005_2026-09-23` event without retroactively changing historical 004 classifications.

Snapshot:
- four official chokepoints verified;
- 2,820 daily observations per chokepoint;
- latest settled date 2026-09-20;
- maximum data lag 4 days;
- two active relevant RED PortWatch disruptions: RED SEA TENSIONS and HORMUZ-26.

Strait of Hormuz is the dominant stress state:
- 7D total / prior-90D traffic = **33.2%**;
- 7D tanker / prior-90D = **14.0%**;
- 30D total / prior-year = **4.7%**;
- 30D tanker / prior-year = **2.4%**;
- ACUTE_TRANSIT_STRESS = True;
- STRUCTURAL_TRANSIT_STRESS = True.

Suez is near recent/previous-year norms, Bab el-Mandeb remains below norms but above frozen stress thresholds, and Cape rerouting does not meet the frozen elevation gate.

Combined with the frozen current U.S. state:

`TIGHT_OR_MIXED + EXTERNAL_SUPPLY_SHOCK_CONTEXT_PRESENT`

the evidence does **not** support calling the current price rollover a clean global supply-normalization regime. This is a mechanism/risk veto, not a directional WTI forecast.

#### Current integrated energy evidence state

Status: **QC PASS / ROLLOVER NOT BEARISH-CONFIRMED / EXTERNAL SUPPLY RISK ACTIVE / CURRENT OUTCOME UNREALIZED**

ENERGY-RISK-SYNTHESIS-007 combines only already-frozen 004A, 005 and 006 evidence. It fits no model, retunes no threshold and uses no prospective WTI outcome.

Current state:

`ROLLOVER_NOT_CONFIRMED__EXTERNAL_SUPPLY_RISK_ACTIVE`

with:

`BEARISH_REVERSAL_CONFIRMATION = VETO`.

Evidence:
- current price rollover: True;
- frozen mechanism: TIGHT_OR_MIXED;
- clean supply normalization: False;
- broad demand destruction: False;
- external supply-shock context: True;
- robust descriptive 8W bearish-confirmation veto: True.

Historical same-class n=10:
- median WTI 8W +7.08%;
- median short MAE 8W +15.24%.

Modern 2018+ same-class:
- median WTI 8W +6.61%;
- median WTI 13W +1.26%.

The synthesis therefore blocks an overconfident durable-bearish interpretation of the current rollover. It does not create a bullish forecast or trading instruction.

#### Prospective weekly outcome maturation

Status: **QC PASS / NO-EARLY-SETTLEMENT VERIFIED / ZERO REALIZED HORIZONS**

ENERGY-WEEKLY-OUTCOME-008 enforces the exact ENERGY-WEEKLY-STATE-004 observation-count convention on the immutable ENERGY005 registry.

First execution for `ENERGY005_2026-09-23`:
- DCOILWTICO observations strictly after release: **0**;
- newly realized horizons: **0**;
- outcome audit rows: **0**;
- event status: **UNREALIZED**;
- early-settlement violation: False.

The original 005 immutable event-chain verifies and remains unchanged. Future 4W/8W/13W outcomes can only enter through a separate append-only audit after 21/41/66 WTI observations including the execution anchor are available.

#### Post-event weekly physical confirmation

Status: **QC PASS / WAITING NEXT WPSR RELEASE / ZERO CONFIRMATION ROWS**

ENERGY-WEEKLY-CONFIRMATION-009 freezes a two-release hysteresis rule before the first post-event weekly release.

Rules:
- one DEMAND_DESTRUCTION week -> candidate only;
- two consecutive DEMAND_DESTRUCTION weeks -> confirmed;
- one SUPPLY_NORMALIZATION week -> candidate only;
- two consecutive SUPPLY_NORMALIZATION weeks -> confirmed;
- otherwise no clean confirmation.

First execution:
- fresh post-PIT common week ends: 0;
- observed releases after 2026-09-23: 0;
- registry rows: 0;
- current state: `WAITING_NEXT_WPSR_RELEASE`;
- prospective WTI outcome use: False.

The original ENERGY005 event remains permanently TIGHT_OR_MIXED; later weekly releases create a separate confirmation path rather than rewriting history.

#### External maritime shock-resolution state machine

Status: **QC PASS / CRITICAL_TRAFFIC_STRESS / CLEAN STREAK 0 / EXTERNAL CONTEXT ACTIVE**

ENERGY-PORTWATCH-RESOLUTION-010 freezes in advance how the 006 external-risk veto can be downgraded.

State hierarchy:
- traffic stress present -> `CRITICAL_TRAFFIC_STRESS`;
- traffic recovered but relevant RED alert remains -> `TRAFFIC_RECOVERED_ALERT_ACTIVE`;
- first fully clean snapshot -> `RESOLUTION_CANDIDATE`;
- two fully clean snapshots at least 7 days apart -> `RESOLVED`.

First snapshot reproduces the current 006 evidence:
- latest settled date 2026-09-20;
- 2 relevant active RED disruptions;
- petroleum traffic stress True;
- current state `CRITICAL_TRAFFIC_STRESS`;
- clean streak 0;
- external supply-shock context active True.

WTI outcomes are not loaded. One clean snapshot is explicitly insufficient to declare resolution.

#### Historical post-event mechanism-transition diagnostic

Status: **QC PASS / POST-RUN DESCRIPTIVE / CLEAN CONFIRMATION NOT A DIRECTIONAL SIGNAL**

ENERGY-WEEKLY-TRANSITION-011 applies the already-frozen 009 two-release confirmation rule descriptively to the 10 completed historical events that were TIGHT_OR_MIXED at rollover.

Within four later WPSR releases:
- 6/10 reached a clean class at least once;
- only 2/10 achieved two consecutive clean releases;
- 1 DD confirmation and 1 SN confirmation;
- none confirmed by T+2;
- both confirmed at T+3;
- 4 candidate-only;
- 4 remained mixed/incomplete.

Crucially, the two confirmed cases were **not bearish**:
- the DD-confirmed case had WTI +7.33% at 8W and +7.30% at 13W;
- the SN-confirmed case had +8.18% at 8W and +6.09% at 13W.

Candidate-only events also had positive median 8W/13W outcomes.

The remains-mixed/incomplete group had median WTI -1.12% at 8W and -7.19% at 13W, but was highly heterogeneous, ranging from large gains to large declines.

Therefore 009 is retained strictly as a **physical-mechanism confirmation path**, not a directional price-confirmation rule.

#### Prospective historical analog benchmark

Status: **QC PASS / TOP-3 FROZEN BEFORE CURRENT OUTCOME / NOT A FORECAST**

ENERGY-WEEKLY-ANALOG-012 compares the still-unrealized `ENERGY005_2026-09-23` event with the 10 completed historical TIGHT_OR_MIXED events using 13 frozen pre-outcome price/mechanism features.

Top 3:
1. 2004-11-03 — distance 0.776;
2. 2017-09-13 — distance 1.395;
3. 2018-05-31 — distance 1.493.

Historical top-3 outcomes:
- all three positive at 8W;
- all three positive at 13W;
- frozen top-3 median WTI 8W **+8.18%**;
- frozen top-3 median WTI 13W **+14.90%**;
- 8W range +6.82% to +14.64%;
- 13W range +6.09% to +23.75%;
- median short MAE 8W +15.48%;
- median short MAE 13W +18.21%.

The closest 2004-11-03 analog exactly matches the current event's four mechanism-count fields and has a nearly identical pressure score.

This is a genuinely prospective historical reference because current ENERGY005 outcomes remain blank. It strengthens the descriptive bearish-confirmation veto but is not a validated directional forecast.

#### Prospective analog robustness

Status: **QC PASS / TOP-1 PRESERVED 13/13 / FROZEN 012 UNCHANGED**

ENERGY-WEEKLY-ANALOG-012A removes one frozen analog feature at a time while current ENERGY005 outcomes remain unrealized.

Results:
- 13 leave-one-feature-out perturbations;
- 2004-11-03 remains top-1 in 13/13;
- no feature changes top-1;
- original top-3 overlap minimum 2/3;
- mean overlap 2.85/3;
- 2004-11-03 and 2017-09-13 appear in every perturbed top-3;
- 2018-05-31 appears in 11/13.

Thus the frozen 012 benchmark is structurally stable rather than a one-feature artifact. It remains a historical similarity reference, not a forecast.











## Immediate public queue

1. Preserve the failed stock-only rule and FLOW-002 as negative/mechanism evidence; do not retune them.
2. ENERGY-WEEKLY-STATE-004 is now the weekly/daily strict-PIT engine. Do not loosen its mechanism thresholds on the consumed 17 events. Freeze the still-unrealized 2026-09-23 TIGHT_OR_MIXED event prospectively and track future selected events append-only.
3. ENERGY-WEEKLY-ANALOG-012A confirms the frozen analog structure is stable under all 13 leave-one-feature-out perturbations. Do not refit it; keep 009/010/008 as mechanism/external-risk/outcome paths.
4. PROSPECTIVE-ISSUANCE-013 v1.1 now has a QC-passed cryptographic genesis/hash chain around the still-empty registry. Keep the system armed but unchanged: no prediction until a genuinely eligible new cycle, complete pre-target GC=F/RTDSM inputs, valid issue timing and all immutable hash checks coexist.
5. Resolve official announcement timing for registry-only emergency-cut candidates before any emergency-event outcome study.
6. PRECUT-STATE-019 is a negative result: simple pre-cut growth/curve/NFCI states do not provide a robust late-trough rule. Do not fit a predictive model on six broad episodes. If continuing, freeze an exploratory continuous pre-cut stress-level 020; otherwise prioritize prospective append-only evidence maturation.
7. Keep paper-specific identification work behind the firewall.

## FED-CYCLE-CROSS-ASSET-EXPANSION-014 — duration / REIT / crypto / housing / rates / cash

Status: **QC-PASSED DESCRIPTIVE EXTENSION / SHORT-HISTORY MARKET PROXIES LIMITED / NOT DEPLOYABLE**

The protocol was frozen before outcome execution and reuses the canonical timing-corrected Fed-cycle registry and four phase anchors.

QC:
- 10 mechanical tightening cycles / 7 broad episodes;
- TLT, VNQ, BTC-USD and DXY acquisitions all succeeded;
- 68 market, 28 housing, 74 Treasury-yield and 37 cash cycle-phase rows;
- 0 current-2026 outcome leakage;
- 0 broad-episode weight or support-label violations;
- no raw Yahoo / Case-Shiller source histories committed.

### Rates and cash

Broad-episode-weighted +12M yield changes:
- FIRST_HIKE: DGS2 about **+123bp**, DGS10 about **+56bp**;
- LAST_HIKE: about **-125bp / -60bp**;
- PAUSE_START: about **-128bp / -108bp**;
- FIRST_CUT: about **-167bp / -20bp**.

Mechanical DFF-based 12M cash-carry medians:
- FIRST_HIKE: **4.73%**;
- LAST_HIKE: **5.94%**;
- PAUSE_START: **5.88%**;
- FIRST_CUT: **4.49%**.

This supports treating the late-tightening plateau as a high cash-hurdle-rate phase rather than assuming all risk assets should immediately dominate cash.

### TLT / VNQ / BTC

All three remain **LIMITED_DESCRIPTIVE** because only 2-3 broad episodes are available.

TLT +12M weighted medians:
- FIRST_HIKE +1.10%;
- LAST_HIKE +5.63%;
- PAUSE_START +8.69%;
- FIRST_CUT +15.13%.

Episode heterogeneity is large: TLT FIRST_HIKE +12M is +22.27% in 2004 but -22.51% in 2022; FIRST_CUT is +29.71% in 2019 but -4.24% in 2024.

VNQ +12M medians:
- FIRST_HIKE -17.76%;
- LAST_HIKE +18.98%;
- PAUSE_START +23.52%;
- FIRST_CUT -4.65%, with FIRST_CUT 12M MDD median 18.79%.

BTC has only two broad episodes. FIRST_HIKE +12M is +137.35% in 2015 versus -38.38% in 2022. PAUSE_START +12M is positive in both available episodes but is not promoted into a stable rule.

### DXY

DXY has supported long-history cells. +12M medians are approximately:
- FIRST_HIKE +3.01%;
- LAST_HIKE -1.26%;
- PAUSE_START -1.26%;
- FIRST_CUT -1.33%.

This is contextual phase evidence, not a deterministic USD rule or causal Gold signal.

### Direct housing

Case-Shiller national nominal house prices pass the frozen descriptive support threshold and remain slow/smoothed:
- +12M weighted medians are positive across the four phase labels;
- +24M medians range roughly +5.5% to +12.7%.

But the median hides severe episode tails:
- 2006 PAUSE_START in the 2004 cycle: +24M about -11.0%;
- 2007 FIRST_CUT: +24M about -17.0%, 24M decline about 18.7%.

Therefore direct housing must remain separated from listed REITs and evaluated with credit, leverage, mortgage structure, supply and starting valuation.

### Integrated interpretation

The public evidence now supports a four-axis cycle representation for PandaAI:

1. policy phase / expected rate path;
2. growth and earnings / commodity-demand state;
3. inflation / energy / real-rate state;
4. credit / volatility / liquidity stress.

Asset output should remain:
`phase + asset + historical endpoint/drawdown/trough distribution + support strength + current state`.

It should not be reduced to deterministic labels such as “hikes bearish” or “first cut bullish.”

## FED-CYCLE-RECOVERY-EXTENSION-015 — new-asset recovery clock

Status: **QC PASS / RISK-SET SUPPORT CORRECTED / DESCRIPTIVE / NOT DEPLOYABLE**

015 extends the 004 prior-peak drawdown recovery clock to TLT, VNQ, BTC, DXY and national house prices, with up to 60 months of post-trough recovery follow-up.

v1.1 separates full phase-cell support from the narrower positive-drawdown recovery risk set.

Supported recovery evidence:
- DXY in all four phases;
- US_HOUSE_PRICE at LAST_HIKE only.

DXY full-recovery KM medians:
- FIRST_HIKE 11m;
- LAST_HIKE 12m;
- PAUSE_START 8m;
- FIRST_CUT 6m.

Limited-descriptive but economically notable:
- TLT full recovery: FIRST_HIKE 30m vs LAST_HIKE 3m / PAUSE_START 2m;
- VNQ: FIRST_HIKE 21m vs LAST_HIKE/PAUSE_START 2m;
- housing FIRST_CUT: 28m full recovery, but only 3 positive-drawdown broad episodes;
- BTC: 2-4m full recovery in only two broad episodes despite very large drawdowns.

Recovery speed must therefore be interpreted jointly with drawdown depth, censoring and support strength.

## FED-CYCLE-SUPPORTED-RECOVERY-MAP-016 — support-filtered recovery synthesis

Status: **QC PASS / FIRST_CUT NOT UNIVERSALLY FASTER / DESCRIPTIVE**

Only recovery-supported cells enter the main four-phase comparison.

Fully supported four-phase assets:
- DXY;
- GOLD;
- NASDAQ;
- SP500;
- WTI.

Full-recovery KM medians (FIRST_HIKE / LAST_HIKE / PAUSE_START / FIRST_CUT):
- DXY: 11 / 12 / 8 / 6 months;
- GOLD: 19 / 6 / 5 / 12;
- NASDAQ: 8 / 3 / 3 / 3;
- SP500: 4 / 1 / 3 / 5;
- WTI: 3 / 19 / 8 / 9.

Frozen synthesis result:
- PAUSE_START is faster than FIRST_HIKE for 4/5 supported assets;
- FIRST_CUT is slower than PAUSE_START for 3/5, equal for 1/5 and faster for 1/5.

Therefore **FIRST_CUT does not universally accelerate recovery**. Recovery must remain asset-specific and phase-conditioned.

## FED-CYCLE-TOTAL-RISK-CLOCK-017 — anchor-to-trough-to-recovery

Status: **QC PASS / FIRST_CUT NEVER FASTER THAN PAUSE IN SUPPORTED SET / DESCRIPTIVE**

017 computes total time event-by-event from each policy anchor to the maximum-drawdown trough and then to 50%/100% prior-peak recovery. It does not add separately calculated medians.

Fully supported four-phase assets remain:
- DXY;
- GOLD;
- NASDAQ;
- SP500;
- WTI.

Anchor→full-recovery KM medians (FIRST_HIKE / LAST_HIKE / PAUSE_START / FIRST_CUT):
- DXY: **17 / 15 / 13 / 13m**;
- GOLD: **30 / 11 / 15 / 22m**;
- NASDAQ: **14 / 11 / 10 / 15m**;
- SP500: **12 / 12 / 14 / 14m**;
- WTI: **12 / 29 / 17 / 20m**.

FIRST_CUT versus PAUSE_START:
- slower: **3/5**;
- equal: **2/5**;
- faster: **0/5**.

A major reason is delayed trough risk. FIRST_CUT median troughs occur around:
- DXY month 8;
- Gold month 5;
- Nasdaq month 8;
- S&P month 8;
- WTI month 11.

Thus many “recovery after cuts” narratives miss the fact that the eventual maximum drawdown can occur well after the first cut.

Supported housing LAST_HIKE risk is even slower:
- median trough 17m;
- anchor→full recovery 20m.

This remains descriptive phase evidence, not a causal effect of policy easing.

## FED-CYCLE-STRESS-TROUGH-ALIGNMENT-018 — FIRST_CUT stress/trough timing

Status: **QC PASS / EQUITY & WTI STRESS ALIGNMENT / GOLD EXCEPTION / NOT A REAL-TIME SIGNAL**

018 aligns FIRST_CUT asset MDD trough months with the already-frozen VIX, Baa–10Y and copper stress-peak months.

All 12 asset × stress pairs pass descriptive support.

Most striking result:
- Nasdaq × VIX: trough month 8, VIX stress month 8, same-month share **100%** across 5 modern broad episodes;
- S&P × VIX: the same **100% same-month** alignment;
- both equity/VIX pairs are within ±2 months in 100% of weighted support.

Equity stress also aligns with:
- Baa spread: median absolute gap 1m, ~71% within ±2m;
- copper: median absolute gap 1m, 80% within ±2m.

WTI troughs are similarly close to VIX/copper/credit stress, usually 0-1 month after the broad stress maximum.

Gold is the exception:
- Gold × VIX median lead -4m;
- Gold × Baa spread -3m;
- Gold often troughs before the later financial-stress maximum.

Therefore the delayed FIRST_CUT equity/WTI troughs in 017 are consistent with a broader stress transition, while Gold follows a different timing channel. Because both stress peaks and troughs are future-window statistics, this is explanatory evidence only.

## FED-CYCLE-PRECUT-STATE-019 — predetermined pre-cut state diagnostic

Status: **QC PASS / SIMPLE STATE RULE NOT SUPPORTED / NEGATIVE DESCRIPTIVE RESULT**

019 uses only pre-FIRST_CUT information:
- real-time RTDSM industrial-production growth;
- pre-cut 10Y–2Y curve;
- pre-cut NFCI.

Outcome:
- supported FIRST_CUT SP500/NASDAQ/WTI trough timing and late-trough breadth.

v1.1 corrects binary support to the independent broad-episode level.

Results:
- REALTIME_GROWTH_CONTRACTION: 0 True / 6 False broad episodes -> insufficient variation;
- CURVE_INVERTED: 3 True / 3 False -> balanced support, but median risk-3 trough month is 8 in both groups and median late-trough share is 1 in both;
- FINANCIAL_CONDITIONS_TIGHT: 1 True / 5 False -> insufficient variation.

The naive composite PRE_CUT_STRESS_COUNT has negative broad-episode rank correlations:
- trough month rho about -0.636;
- late-trough share rho about -0.707.

But component sensitivity shows the negative relation is largely driven by the single NFCI-tight broad episode:
- drop NFCI -> trough rho about -0.127 and late-share rho +0.141;
- NFCI-only -> -0.674 / -1.000.

Therefore the composite is not a robust state rule and must not be promoted into a PandaAI timing score.

Next work should either:
1. test continuous pre-anchor stress levels under an explicitly exploratory 020 lock; or
2. stop this small-sample explanatory branch and wait for prospective append-only evidence.






#### Continuous pre-cut stress-level diagnostic

Status: **QC PASS / CONTINUOUS PRE-CUT LEVEL RULE NOT SUPPORTED / BRANCH STOP**

FED-CYCLE-PRECUT-STRESS-LEVEL-020 freezes four predetermined continuous pre-FIRST_CUT inputs after the negative 019 binary-state result: Baa–10Y spread level, VIX level, curve stress and real-time RTDSM IPT growth stress.

Support:
- 8 mechanical cycles / 6 broad episodes;
- VIX available for 5 broad episodes.

Median SP500/Nasdaq/WTI trough-month Spearman rho:
- Baa +0.075;
- VIX -0.211;
- curve stress +0.029;
- real-time growth stress -0.177.

Every full-sample relation fails the frozen composition-robustness requirement because LOO signs change.

The late-trough-share outcome is nearly degenerate: B02 = 0.556 and B03-B07 = 1.000. The VIX common sample therefore has no late-share variation.

A stronger B03-B07 curve-stress relation (rho about -0.738) disappears when B02 is restored (full-sample rho about +0.029), so it is sample-composition sensitive and is not promoted.

Canonical conclusion: **continuous pre-cut levels do not rescue 019. Stop the small-sample FIRST_CUT timing-rule branch.**

Do not add predictors, optimize transformations or fit a multivariate score on these six broad episodes.

Next priority is prospective append-only evidence maturation and evidence-linked PandaAI integration. B04-B07 remain consumed OOS evidence for OOS-008 M3 and must not be reused for tuning.

## Cross-asset master synthesis — 021

Status: **QC-PASSED CANONICAL DESCRIPTIVE EVIDENCE MAP / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

FED-CYCLE-CROSS-ASSET-MASTER-SYNTHESIS-021 now provides the public canonical integration layer over the Fed-cycle research chain without new price estimation or inference.

Coverage:
- 52 price-asset x phase rows across 13 assets;
- 20 core-supported asset x phase rows;
- five fully supported four-phase core assets: DXY, GOLD, NASDAQ, SP500 and WTI;
- 12 separate policy/rate/cash context rows;
- 12 separate VIX/Baa/copper stress-context rows.

FIRST_CUT core historical medians:
- DXY: +12M -1.33%, 12M MDD 5.18%, trough month 8, anchor-to-full-recovery 13m;
- GOLD: +12M +4.06%, MDD 5.43%, trough month 5, total full recovery 22m;
- NASDAQ: +12M +6.04%, MDD 17.48%, trough month 8, total full recovery 15m;
- SP500: +12M +10.98%, MDD 13.99%, trough month 8, total full recovery 14m;
- WTI: +12M -16.94%, MDD 22.23%, trough month 11, total full recovery 20m.

Canonical interpretation: endpoint return and path risk are different objects. A positive 12-month endpoint does not imply that drawdown risk ended at the first cut.

PandaAI is allowed to consume 021 as: `policy phase + historical asset-specific path-risk distribution + recovery clock + support + evidence class + uncertainty`. It must not turn the map into a deterministic bottom date, causal Fed claim, best/worst ranking or trading recommendation.

The 019/020 branch remains closed: simple predetermined FIRST_CUT bottom-timing rules are not supported in the available small sample.

Next research/content priority: build **022 Historical Fed Cycle Casebook** from representative episodes and explicitly separate what was knowable in real time from ex-post stress peaks/troughs. Prospective Fed/energy registries remain append-only and should mature only under their frozen gates.

## Historical Fed Cycle Casebook — 022

Status: **QC-PASSED SIX-EPISODE HISTORICAL CASEBOOK / EVIDENCE-LINKED / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

022 turns the canonical Fed-cycle evidence into six primary broad-episode cases: B02 1987-89, B03 1994-95, B04 1999-2001, B05 2004-07, B06 2015-19 and B07 2022-24. B02 remains a three-sub-cycle composite and is not collapsed into a fictitious single policy sequence.

Evidence-time separation is now explicit:
- REALTIME_KNOWABLE: 8 timing-audited pre-FIRST_CUT context rows from 019;
- DESCRIPTIVE_PATH: 120 Gold/S&P/Nasdaq/WTI phase-path rows plus 90 rate/cash rows;
- EXPOST_ONLY: 72 stress-peak versus asset-trough timing pairs from 018.

Content-ready case contrasts include:
- 2001 FIRST_CUT: Nasdaq +12M about -25.6%, 12M MDD about 40.8%, trough month 8;
- 2007 FIRST_CUT: S&P 500 +12M about -16.3%, MDD about 21.0%, trough month 12;
- 2019 FIRST_CUT: S&P 500 +12M about +11.0% while MDD was about 19.1%, trough month 8;
- 2024 FIRST_CUT: S&P 500 +12M about +20.2%, MDD about 11.1%, trough month 7.

These are descriptive historical paths. They do not establish Fed causality or identify a current-cycle analog. The 019/020 timing-rule branch remains closed.

Next priority: **022A Historical Context Registry** using independently sourced public historical macro/event context with source-level provenance. After 022A, combine 021 + 022/022A into the claim registry, figure registry and reusable content production library.

## Historical Context Registry — 022A

Status: **QC-PASSED OFFICIAL-SOURCE CONTEXT REGISTRY / ANTI-HINDSIGHT LAYER / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

022A adds 18 source-audited context claims across the six 022 cases using 21 normalized official-source links. It does not alter the canonical policy chronology or market outcomes.

Claim-time classes:
- CONTEMPORANEOUS_POLICY_CONTEXT = 6;
- RETROSPECTIVE_DATING = 6;
- RETROSPECTIVE_EVENT_CONTEXT = 4;
- POST_ANCHOR_SHOCK = 2.

Binding anti-hindsight rules:
- the March 2001 recession peak was later NBER dating and was not officially known at the January 2001 first cut;
- the December 2007 recession peak was later NBER dating and was not officially known at the September 2007 first cut;
- September 11 is a later shock inside the 2001 post-cut path;
- COVID is a later shock inside the 2019 post-cut path and must not be inserted into the July 2019 policy rationale;
- B07 NBER chronology is only an as-of-2026-09-25 official-source audit, not a forecast.

The combined content-ready evidence object is now: `policy chronology -> what was known then -> asset path -> stress/trough path -> later official dating -> later shock context -> evidence boundary`.

Next priority: **022B Content Claim Registry**, then **023 Real-Time Regime Dashboard**. The claim registry should be the single source of truth for reusable script/article/image-card claims. Prospective Fed/energy registries remain append-only under their frozen gates.

## Content Claim Registry — 022B

Status: **QC-PASSED 47-CLAIM CANONICAL CONTENT CONTROL LAYER / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

022B is now the single-source-of-truth claim layer for reuse in videos, long articles, image cards and PandaAI.

Inventory:
- 20 core asset x phase claims for DXY/GOLD/NASDAQ/SP500/WTI across FIRST_HIKE/LAST_HIKE/PAUSE_START/FIRST_CUT;
- 6 historical case claims B02-B07;
- 18 official-source context claims mapped 1:1 from 022A;
- 2 timing-rule guardrails preserving the negative 019/020 results;
- 1 supported FIRST_CUT-vs-PAUSE recovery-clock synthesis.

Every claim carries canonical wording, sample/support, evidence class/time, sources, allowed/prohibited wording, freshness, figure key and content routing tags.

Six content packs now exist: FIRST_CUT_NOT_THE_BOTTOM, SAME_LABEL_DIFFERENT_PATHS, GOLD_VS_EQUITIES, HINDSIGHT_TRAPS, RECOVERY_CLOCK and 1987_MULTI_LEG.

No claim can be interpreted as causal, an asset ranking, a current analog selection, a deterministic bottom date or a trading recommendation.

Next priority: **023 Real-Time Regime Dashboard**, using release-aware current observables and linking current-state descriptions back to 022B CLAIM_IDs and 021 historical distributions. 023 must not select a single historical analog. After 023, build the Figure Registry and visual/content production library.
