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
