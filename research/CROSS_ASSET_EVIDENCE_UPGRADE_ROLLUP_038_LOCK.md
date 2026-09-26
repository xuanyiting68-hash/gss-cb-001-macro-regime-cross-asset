# CROSS-ASSET-EVIDENCE-UPGRADE-ROLLUP-038 — LOCK

Date locked: 2026-09-26

## Purpose

Create a canonical post-032 evidence-status rollup incorporating completed modules 033-037.

038 is synthesis only.

No new price estimation, regression, p-value, forecast, ranking or trading rule is allowed.

## Required upstream PASS

- 032 Four-Phase Investor Knowledge Atlas
- 033 Gold Mechanism Decomposition
- 034 Housing Lag Chain
- 035 Long-Duration Treasury Proxy Bridge
- 036 Listed REIT Proxy Bridge
- 037 REIT Deep-History Dual Bridge

## Frozen evidence-state rules

### Gold
- retain CORE_SUPPORTED phase evidence;
- add MULTI_MECHANISM_MAP_AVAILABLE;
- do not create a dominant-driver ranking.

### Housing
- retain SUPPORTED_SLOW_MOVING;
- add FINANCING_ACTIVITY_PRICE_TIMING_MAP;
- risk metric remains DECLINE_24M;
- no city-level extrapolation.

### Long-duration Treasury
- TLT remains the target ETF with LIMITED original history;
- VUSTX_LONG_TREASURY_PROXY becomes SUPPORTED_PROXY_DESCRIPTIVE after 035 bridge pass;
- proxy history must never be relabeled TLT.

### Listed REIT
- VNQ remains LIMITED_DESCRIPTIVE;
- VGSIX_REIT_PROXY is bridge-valid but LIMITED_PROXY_DESCRIPTIVE;
- FRESX_REIT_ACTIVE_PROXY remains NOT_PROMOTED_DUAL_BRIDGE_FAIL;
- no proxy shopping after 037.

### Bitcoin
- remains LIMITED_DESCRIPTIVE in the phase atlas;
- no synthetic historical backfill.

## Frozen outputs

- ASSET_EVIDENCE_STATUS_V2.csv
- FOUR_PHASE_EXTENSION_STATUS_V2.csv
- CANONICAL_CLAIM_UPGRADE_REGISTRY.csv
- PANDAAI_EVIDENCE_ROUTING_V2.json
- CROSS_ASSET_EVIDENCE_UPGRADE_038_SYNTHESIS_ZH.md
- CROSS_ASSET_EVIDENCE_UPGRADE_ROLLUP_038_REPORT.md
- QC.json

## QC

PASS requires:
- 035 bridge pass preserved;
- 036 bridge pass + limited support preserved;
- 037 dual-bridge fail preserved;
- no FRESX promotion;
- no VUSTX history relabeled TLT;
- housing metric remains DECLINE_24M;
- Gold mechanism map remains non-ranked;
- Bitcoin remains limited;
- no best asset / best phase / expected return / trade instruction;
- private-paper inputs false;
- causal status NONE;
- OOS NOT_A_FORECASTING_MODEL;
- deployment NOT_DEPLOYABLE.
