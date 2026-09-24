# Changelog

## 2026-09-24 — Public companion repository initialized

- Initialized the previously empty public repository.
- Defined the repository as the PandaAI / macro-regime / cross-asset / social-media companion, separate from the unpublished academic-paper repository.
- Added a paper firewall so private staff-path, private reaction-function and unpublished paper artifacts do not leak into the public workstream.
- Added public research protocol, current-state file, evidence ledger, transfer audit and agent instructions.
- No private-paper empirical artifact was copied into the public repository.
- No trading claim was upgraded by this repository import.

## 2026-09-24 — First public-safe research import

- Added a public-safe P0-A v3 statistical re-audit protocol.
- Added P0-B/P0-C public evidence-status note.
- Added Fed-cycle drawdown / recovery preregistration.
- Added refined-product / household-inflation public closeout.
- Added Energy Reversal State Machine v2.
- Added content-layer evidence rules.
- Updated README to link imported research.
- Deliberately did not copy private S6D.3 paper data/results or raw redistribution-uncertain vendor datasets.
- Larger social-content files remain pending final claim/source audit.

## 2026-09-24 — ENERGY-PRICE-WF-001 exhaustive walk-forward

- Froze the long-history price/product walk-forward before execution.
- Added a reproducible GitHub Actions runner using public EIA/FRED monthly WTI, gasoline, heating-oil and jet-fuel series.
- Direct FRED acquisition succeeded in the QC-passed run; source bytes were hashed and raw downloads were not committed.
- Common sample: 1990-04 through 2026-08, 437 complete months.
- Identified 13 de-clustered rollover events: 6 price/product-confirmed and 7 false-relief veto.
- None of the four primary confirmed-vs-veto comparisons passed BH-FDR 10% (q≈0.224).
- Added leave-one-event-out and broad-era robustness. The descriptive separation survives leave-one-out but is not stable across pre-2008 vs later eras.
- Closed the price layer as NOT CONFIRMED / NOT DEPLOYABLE. The false-relief veto remains a promising risk-filter hypothesis.
- Froze the next release-aware EIA inventory/refinery extension before running it.

## 2026-09-24 — ENERGY-PHYSICAL-WF-001 v1.1 and FLOW-002

- Added a pre-result timing amendment after identifying that monthly-average price data cannot be treated as observable at month start.
- Built an official event-scoped EIA release registry and daily-WTI decision-date outcome convention.
- The first physical execution was quarantined after audit found a brittle archive parser had truncated release history and generated impossible timing matches for later events.
- Re-ran with explicit event-scoped official release dates and hard timing QC. Corrected physical QC passed: 12/13 strict-PIT events available, zero bad timing mappings.
- Corrected P4A_DATA_ONLY support: n=3. The frozen four-test family produced 0/4 BH-FDR survivors; q=1.00 for the family.
- Within the six completed strict-PIT price-confirmed episodes, all three P4A_DATA_ONLY events had positive WTI at both 3M and 6M. The stock-normalization-as-bearish-confirmation hypothesis is therefore not supported.
- Added a post-result mechanism diagnostic; preserved the failed v1.1 rule rather than tuning thresholds.
- Froze and executed ENERGY-FLOW-002 using EIA product supplied, refinery crude inputs, field production and crude imports.
- FLOW-002 has four complete strict-PIT price-confirmed events: FLOW_DD=0, FLOW_SN=1, FLOW_MIXED=3. It is mechanism-building only and does not establish a directional edge.
- Improved automated research workflows to rebase before push after a concurrent-write rejection exposed GitHub Actions race risk.
- Added an evidence-linked public content card: “库存增加，为什么油价不一定跌？”, with explicit n/FDR/causal-language boundaries.

## 2026-09-24 — FED-CYCLE-PATH-001 v1.1

- Froze a long-history Fed-cycle path-risk specification before asset-outcome execution.
- Preserved two pre-outcome market-data acquisition failures: Stooq browser verification and Yahoo `XAUUSD=X` chart 404.
- Switched the reproducible daily Gold layer to explicitly labeled `GC=F` continuous COMEX futures proxy; raw Yahoo bytes remain uncommitted.
- The first completed v1 run passed computational QC but was quarantined after readback exposed a timing-ontology bug.
- Froze a v1.1 timing amendment separating target-series effective dates from FOMC decision dates.
- Added 2025-2026 regular FOMC calendar coverage and hard assertions for the 2022-2024 modern-cycle anchors.
- Prevented pre-1994 reconstructed target changes from being labeled as modern emergency cuts.
- Kept eight timing-unresolved post-1994 emergency-cut candidates registry-only; zero enter asset-outcome metrics.
- v1.1 QC passed with 10 qualifying mechanical tightening legs, 345 asset-event metric rows, Gold FIRST_HIKE n=3 and S&P FIRST_HIKE n=10.
- FIRST_HIKE descriptive path risk shows endpoint return can coexist with materially larger intra-window MDD: S&P 500 252D median +4.99% vs MDD 11.31%; Nasdaq -0.82% vs MDD 20.67%; WTI +22.04% vs MDD 30.16%.
- Gold 2015 and 2022 differ materially under one frozen specification; this remains descriptive and non-causal.
- Added an evidence-linked content card on why endpoint return alone is an incomplete risk statistic.
- Next research priority is a native-frequency openly licensed long-history Gold layer before state-dependent Gold claims.

## 2026-09-24 — FED-CYCLE-GOLD-LONGHIST-MONTHLY-001

- Froze a native-frequency monthly Gold extension before inspecting long-history cycle outcomes.
- Pinned the public `datasets/gold-prices` source at commit `95bfea9197222dcda13d8c4d9928fb631fe745aa`; used only 1960+ monthly observations sourced by the package from World Bank Commodity Markets under ODC-PDDL-1.0.
- Excluded 1833-1959 rows because the source package states those are annual averages repeated across months.
- Omitted the event month from clean outcome measurement to avoid mixing pre-event and post-event monthly prices.
- QC passed with 800 eligible months and clean FIRST_HIKE coverage for all 10 frozen tightening legs.
- FIRST_HIKE +12M median is +0.24% and +24M median +0.58%, while 24M MDD median is 16.64% with a 3.83%-39.10% range. A stable directional Gold rule is not established.
- Cross-frequency audit agrees in endpoint sign for 2004 and 2015 but not 2022; monthly and daily/futures layers remain separate and are never pooled.
- Added a post-run recovery-statistics amendment after recognizing that observed-only recovery medians were inappropriate under right-censoring.
- Kaplan-Meier survival QC passed: FIRST_HIKE 50% recovery median 8 months (8 observed/2 censored); full recovery median 19 months (6 observed/4 censored).
- Added an evidence-linked public content card: “加息后黄金到底怎么走？长历史答案不是简单涨跌”.
- Next Fed-cycle priority is a predetermined/PIT state-dependence design; revised macro series must not be mislabeled as real-time information.

## 2026-09-24 — FED-CYCLE-STATE-001

- Froze seven state variables before conditioning the 10 FIRST_HIKE Gold outcomes.
- Separated strictly pre-event market history from release-lag-aware current-vintage macro history; current-vintage CPI/INDPRO/NFCI are not labeled ALFRED PIT.
- QC passed with zero market-timing or macro-period violations and zero unsupported contrasts promoted as supported.
- Supported n>=3/group primary contrasts exist for inflation level, inflation direction, growth and WTI direction; their +12M Gold and 24M MDD median-difference signs remain stable in computable leave-one-leg-out checks.
- Yield curve has no FIRST_HIKE cross-sectional variation (0 inverted/10 positive); the real-rate proxy is 9/1 and TIPS real-yield support is only n=3; NFCI is 2/8. No claims are made from those splits.
- The USD source bridge passes with 95.74% six-month direction-sign agreement and 5/5 event support, but the USD groups are perfectly chronologically separated: 1983-1988 falling/flat versus 1994-2022 rising. The apparent USD contrast is therefore classified as era-confounded.
- No p-values or BH-FDR are run; STATE-001 is a small-n mechanism map, not a confirmatory or forecasting model.
- Added an evidence-linked content card on why Real Yield, USD and Oil cannot yet be ranked as the dominant Gold driver.
- Next priority is a within-cycle monthly continuous-state design with cycle-aware dependence handling rather than more binary event splits.

## 2026-09-24 — FED-CYCLE-STATE-PANEL-002

- Froze and ran a 165-row within-cycle monthly Gold state panel across 10 mechanical tightening legs.
- Grouped nearby early legs into 7 broad macro episode clusters for more conservative dependence-aware inference.
- Used cycle fixed effects and equal total regression weight per mechanical cycle so long cycles did not dominate.
- Primary inference enumerated exact whole-broad-episode sign flips rather than row-level IID errors.
- Frozen primary family contained 8 tests: CPI level, CPI momentum, INDPRO YoY and WTI 6M return against forward 6M Gold endpoint return and MDD.
- 0/8 primary tests survived BY-FDR 10%; 0/8 survived BH-FDR 10% diagnostic.
- This weakens the visually strong STATE-001 binary event-level splits and argues against promoting them into deterministic Gold regime rules.
- A predeclared secondary USD-return diagnostic had raw broad-cluster p=0.03125 with stable sign, but the full 12-test secondary family had 0 BH/BY FDR survivors; USD BH q=0.375 and BY q=1.00.
- USD remains hypothesis-generating only. Yield curve, nominal 10Y, simple real-rate proxy and NFCI did not provide confirmatory secondary evidence; DFII10 still has insufficient cycle support.
- Added an evidence-linked content card explaining why attractive binary macro-state patterns can disappear under a stronger within-cycle design.
- Next priority is a cross-asset event-time risk clock for trough timing, MDD accumulation and recovery hazard.

## 2026-09-24 — FED-CYCLE-CROSS-ASSET-RISK-CLOCK-003

- Froze and executed a 24-complete-month FIRST_HIKE risk clock for Gold, S&P 500, Nasdaq and WTI.
- Omitted the event month to avoid mixed pre/post-event monthly averages and gave each broad episode total aggregate weight 1.
- QC passed with 960 path rows, 40 cycle-asset rows and zero timing, MDD, recovery-order or weighting violations.
- Weighted median MDD-trough month: Nasdaq 7, S&P 500 11, Gold 12, WTI 15.
- Late-window (months 13-24) MDD-trough shares: Gold 50.0%, Nasdaq 26.2%, S&P 47.6%, WTI 61.1%.
- Broad-episode-weighted median 24M MDD: Gold 14.09%, Nasdaq 12.18%, S&P 8.47%, WTI 20.65%.
- Broad-episode-weighted full-recovery KM medians: Gold 13 months, Nasdaq 8, S&P 9, WTI 8.
- Preserved the weighting sensitivity versus the earlier equal-mechanical-leg Gold full-recovery estimate of 19 months; the two summaries use different weighting conventions.
- Added an evidence-linked content card: “第一次加息后，真正危险的是第几个月？”
- Next risk-path priority is a phase clock spanning LAST_HIKE, PAUSE_START and FIRST_CUT under the same frozen conventions.

## 2026-09-24 — FED-CYCLE-PHASE-CLOCK-004

- Froze and executed one common 12-complete-month path-risk convention across FIRST_HIKE, LAST_HIKE, PAUSE_START and FIRST_CUT.
- QC passed with 1,824 phase-path rows, 152 phase-asset-cycle rows and all 16 primary asset × phase cells supported.
- S&P 500 median 12M MDD is 4.22% after PAUSE_START versus 13.99% after FIRST_CUT; Nasdaq is 4.00% versus 17.48%.
- FIRST_CUT late-window MDD-trough shares are 90.48% for both S&P and Nasdaq.
- WTI FIRST_CUT median +12M return is -16.94%, median MDD 22.23%, median trough month 11 and late trough share 100%.
- Gold differs: FIRST_CUT +12M median +4.06%, MDD 5.43%, trough month 5.
- The phase map therefore rejects a simplistic descriptive narrative that first cut universally means risk has ended, while making no causal claim about the cut itself.
- No cross-phase significance test is run because the same cycles can enter multiple anchors and post-anchor windows can overlap.
- Added an evidence-linked content card: “第一次降息，就代表风险结束了吗？”
- Next public-safe extension is modern stress-state diagnostics such as VIX, credit spreads and copper where support permits.

## 2026-09-24 — FED-CYCLE-STRESS-LAYER-005

- Froze and executed VIX, Baa-minus-10Y credit-spread and copper stress paths under the same FIRST_HIKE/LAST_HIKE/PAUSE_START/FIRST_CUT phase ontology.
- QC passed with 924 stress-path rows, 77 stress-cycle-phase rows and all 12 observable × phase cells supported.
- FIRST_CUT has the largest median maximum monthly-average VIX increase (+8.53 points) versus +4.26 after FIRST_HIKE.
- FIRST_CUT has the largest median maximum Baa-10Y widening (+38 bp) versus +16 bp after FIRST_HIKE.
- Copper median 12M MDD is 19.96% after FIRST_CUT versus 6.84% after FIRST_HIKE.
- Stress peaks are also relatively late after FIRST_CUT: median month 8 for VIX, 7 for credit widening and 9 for copper MDD.
- Combined with PHASE-CLOCK-004, this supports a mechanism-context interpretation that first cuts often occur around broader stress/deterioration transitions; it does not identify a causal effect of the cut.
- No optimized stress thresholds, p-value/FDR family, OOS forecast or deployment rule are produced.
- Added an evidence-linked content card: “为什么第一次降息时，市场反而可能更危险？”

## 2026-09-24 — FED-CYCLE-ASIA-CREDIT-DIAG-006

- Froze and executed limited-support phase diagnostics for Hang Seng, Shanghai Composite, Nikkei 225, KOSPI and U.S. high-yield credit.
- All 4 requested Asia Yahoo symbols were acquired; Asia timing, MDD, support-label and broad-episode-weight QC passed.
- Nikkei has 10/7 FIRST_HIKE/LAST_HIKE/FIRST_CUT support; Hang Seng 8/6; Shanghai and KOSPI 4/4 under the available Yahoo histories.
- All four Asia indices have higher weighted median 12M MDD after FIRST_CUT than after PAUSE_START, while +12M endpoint return signs remain mixed.
- Shanghai FIRST_CUT +12M median is -28.73% with 8.59% median MDD; Nikkei remains +9.60% with 12.61% MDD; the contrast illustrates that path risk and endpoint direction are distinct.
- Current FRED ICE BofA High Yield OAS history is restricted to recent observations, leaving only 1/1 FIRST_CUT support; this is retained as INSUFFICIENT_SUPPORT rather than backfilled from an unlicensed source.
- Froze a post-coverage-audit HYG price-proxy amendment before HYG outcomes. HYG has only 2-3 broad episodes, remains LIMITED_SUPPORT, and is explicitly not pooled with OAS.
- HYG FIRST_CUT diagnostic: +12M median -3.42%, 12M MDD 11.19%, median trough month 8; PAUSE_START has only 2 broad episodes and 0.82% MDD.
- Existing P0-C China causal/interaction quarantine remains unchanged.
- Added an evidence-linked content card: “第一次降息后，亚洲市场就安全了吗？”
- Next Fed-cycle research priority is a vintage-safe macro-state layer before stronger state-dependent claims.

## 2026-09-24 — FED-CYCLE-VINTAGE-AUDIT-007

- Froze a real-time industrial-production revision audit using official Philadelphia Fed RTDSM `IPT` monthly vintages.
- Kept the original M-2/M-14 YoY definition and frozen 2% growth threshold; selected only vintages no later than the month before each information month.
- Parsed 477,136 workbook cells across 766 vintages from 1962-11 through 2026-08; 10/10 FIRST_HIKE events and all 165 panel rows have real-time support.
- Event-level growth state flips in 1/10 cases: 2022 changes from current-revised WEAK (+1.32%) to real-time STRONG (+4.12%).
- Median absolute event-level YoY revision gap is 2.225pp; maximum 4.035pp.
- The event-level +12M Gold STRONG-minus-WEAK return contrast remains negative (-8.31pp current labels versus -9.12pp real-time), while the 24M MDD contrast disappears/reverses slightly (+2.67pp to -0.47pp).
- On the exact same 165 within-cycle rows, current-vintage INDPRO has beta -1.27pp/SD and broad exact p=0.125 for next-6M Gold return; real-time IPT has beta -1.96pp/SD and raw broad exact p=0.015625.
- All seven broad-episode real-time return score contributions are negative; this exact p-value largely reflects 7/7 sign unanimity rather than high-precision forecast evidence.
- A transparently post-run restriction audit shows the negative real-time coefficient persists after excluding 2022 (-1.49pp, p=0.03125) and after excluding early B01/B02 (-2.99pp, p=0.0625 with five broad episodes).
- The combined later/no-2022 sample has only four cycles and remains LIMITED_SUPPORT with no promoted exact p-value.
- Real-time IPT does not support a Gold MDD relation.
- Preserved CPI series-definition integrity: did not substitute seasonally adjusted Philadelphia Fed PCPI for the original not-seasonally-adjusted CPIAUCNS state.
- Added an evidence-linked content card on real-time-vintage versus revised-history bias.
- Next priority is a separately frozen time-ordered OOS test; in-sample exact p-values are not forecasting proof.

## 2026-09-24 — FED-CYCLE-GOLD-OOS-008

- Froze a single-target next-6M Gold forecast audit before execution; no random split, no hyperparameter search and no target-horizon shopping.
- Used broad-episode forward chaining: B01-B03 -> B04, then expanding through B07, producing 119 OOS monthly predictions across four future broad episodes.
- Hard leakage QC passed: every training target window ends before its test episode starts; no same/future episode enters training; Gold lag features and RTDSM vintages are strictly pre-month.
- Frozen B0/B1/B2/M3/D4 model family used weighted linear regression with broad-episode/cycle hierarchy.
- M3 (Gold history + cycle age + real-time IPT) passes the predeclared preliminary gate: 21.27% lower episode-equal MSE than B2, 3/4 B2 episode wins, OOS R² +3.38% versus historical mean.
- Benchmark sanity audit prevents overstatement: M3 only lowers MSE 3.38% versus B0, wins 2/4 B0 episodes on MSE, and has 2.74% worse aggregate MAE with only 1/4 MAE wins.
- M3 improves on current-vintage D4 by 6.80% MSE and 3.53% MAE and wins 3/4 episodes on each metric, supporting the usefulness of real-time-vintage information over revised-history input.
- Real-time IPT standardized coefficients remain negative across all four expanding training folds (-0.043 to -0.050), but episode calibration is unstable.
- M3 episode-equal signed bias is -2.84pp; the model compresses the realized positive tail, predicting at most +12.64% versus realized +41.51%.
- Final status: PRELIMINARY_OOS_CANDIDATE / WEAK AND BENCHMARK-SENSITIVE / NOT DEPLOYABLE.
- B04-B07 are now consumed OOS evidence for this specification and must not be used for further parameter tuning.
- Added an evidence-linked content card explaining why passing an OOS gate is not equivalent to a tradable model.

## 2026-09-24 — FED-CYCLE-PROSPECTIVE-SHADOW-009

- Froze an append-only prospective Gold validation architecture after OOS-008 rather than tuning the consumed B04-B07 evidence.
- Preserved the existing mechanical tightening-leg eligibility rule: at least 2 positive target changes and at least 50 bp cumulative tightening.
- The current 2026 edge run contains only the 2026-09-16 +25 bp hike, so it is a prospective candidate but **not yet an eligible B08 test episode**.
- Automated gate QC passed: 185 policy rows, zero duplicate event dates, zero ordering/sign-label violations, zero automatic prediction rows and zero retroactive-issuance permission.
- If the current/future edge run later qualifies, the existing broad-cluster rule maps it to prospective B08; no earlier month may be backfilled after qualification.
- Frozen prospective live family is B0/B1/B2/M3 only; current-revised D4 remains historical diagnostic and is excluded from the live shadow path.
- New-episode models are fit once from prior episodes only; active-episode outcomes never enter training and no within-episode refit is permitted.
- Added immutable model-spec hashing and an append-only prediction registry schema for issue timestamps, source/input provenance, predictions, realized targets and errors.
- Current registry contains 0 predictions. Evidence status is PROSPECTIVE_ARCHITECTURE_FROZEN_ARMED_NO_NEW_FORECAST_EVIDENCE / NOT_DEPLOYABLE.

## 2026-09-24 — FED-CYCLE-PROSPECTIVE-INPUT-TIMING-010

- Froze and ran a strict live-input timing audit before any prospective Gold prediction.
- Reconstructed recent first-seen availability from the public `datasets/gold-prices` monthly-file commit history.
- All 6/6 recent uncensored monthly Gold observations arrived after the following target month had already begun.
- Release lag is 51.7-107.7 hours after next-month start, so the exact OOS-008 World-Bank-monthly Gold feature contract cannot satisfy strict pre-target issuance.
- Current RTDSM probe for a hypothetical 2026-10 forecast also remains incomplete: last vintage is 2026-08 and the frozen August IPT YoY input is not yet available under the same-vintage rule.
- QC passes because the audit successfully identifies a negative transport result; no prediction or forecast-performance test is created.
- OOS-008 and SHADOW-009 remain unchanged; B04-B07 remain consumed.
- Exact same-definition daily Gold replacement is nontrivial because FRED removed IBA/LBMA Gold Price data in 2022 and benchmark use/licensing constraints remain.
- Next task: pre-freeze a Gold live-source feature-equivalence bridge before any prospective B08 issuance.

## 2026-09-24 — FED-CYCLE-GOLD-LIVE-BRIDGE-011

- Froze a feature-only transport audit for GC=F before examining bridge results.
- Candidate is continuous COMEX Gold futures daily close from Yahoo public chart history, aggregated to monthly mean; raw JSON is not committed.
- Reference remains the pinned World Bank Gold monthly series used by OOS-008.
- No calibration/regression bridge, forecast target, M3 forecast error or outcome-based tuning is used.
- Feature-complete overlap is 306 months from 2001-03 through 2026-08; minimum accepted proxy month has 16 daily observations.
- All 17/17 frozen engineering gates pass.
- Monthly level median absolute gap is 0.13% and p95 is 0.71%.
- 3M return correlation is 0.99839, median absolute difference 0.19pp and sign agreement 99.02%.
- 6M return correlation is 0.99939, median absolute difference 0.17pp and sign agreement 99.02%.
- 6M volatility correlation is 0.99280 with median absolute difference 0.000855.
- 3M/6M sign agreement remains at least 98.11% in each frozen era.
- Bridge status: PROXY_FEATURE_BRIDGE_CANDIDATE; this is measurement transport evidence only and does not revalidate or inherit OOS-008 performance.
- First workflow attempt failed before research execution because beautifulsoup4 was absent; dependency was added and the exact frozen specification reran successfully without changing any research threshold.
- Next task: freeze a separately versioned prospective measurement amendment that uses the bridge only for live Gold features while preserving outcome isolation and no-backfill rules.

## 2026-09-24 — FED-CYCLE-PROSPECTIVE-GCF-012

- Froze a separately versioned prospective Gold measurement specification after BRIDGE-011 passed all engineering-equivalence gates.
- Historical fitting remains on the original OOS-008 World Bank Gold feature panel; GC=F is used only as the future live measurement contract.
- Final historical training contains 165 rows across B01-B07, with latest realized target end 2025-01 and zero overlap with the current 2026 candidate.
- Hierarchical broad-episode weights pass to numerical tolerance.
- Froze immutable prospective spec SHA256 `f3d3eff3020af41665da93151962d0a488b14f642bf3e7e68dcf16cb156787b4`.
- Froze training-model SHA256 `96520e9316a0cbcc18085f0dfa2d7432fab9892d715e7893fcf5ad2b172ba50d`.
- Serialized B0/B1/B2/M3 coefficients, training weighted means and standard deviations.
- Current 2026 edge run remains 1 hike / 25 bp, so it does not satisfy the frozen 2-hike / 50 bp activation rule.
- Prediction registry remains empty and zero predictions are created.
- OOS-008 performance is explicitly not inherited by the measurement-amended model.
- Next step is a separate append-only issuance engine with hard duplicate, timing, input-readiness and no-backfill gates.

## 2026-09-24 — FED-CYCLE-PROSPECTIVE-ISSUANCE-013

- Froze and executed a fail-closed append-only forecast issuer for GCF-012.
- Issuer requires exact frozen GCF-012 spec/model hashes and the BRIDGE-011 approved status.
- First run evaluated candidate forecast month 2026-10.
- Current 2026 edge run remains 1 hike / 25 bp, so the 2-hike / 50 bp activation gate fails.
- Correct refusal state is WAITING_CYCLE_QUALIFICATION.
- Because the structural gate failed, the issuer did not fetch live Gold/RTDSM inputs, did not fit a model and did not search backward for missed months.
- Zero predictions were issued and the canonical prediction registry remains empty.
- Append-only row-count identity passes.
- Identified one remaining pre-issuance audit hardening task: add a cryptographic registry hash chain so any future external/manual rewrite of an already committed prediction row is detectable.

