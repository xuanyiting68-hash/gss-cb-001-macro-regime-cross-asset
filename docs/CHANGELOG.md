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
