# CROSS-ASSET-EVIDENCE-UPGRADE-ROLLUP-038 — CLOSEOUT

Date: 2026-09-26

## Final status

**QC PASS / CANONICAL POST-032 EVIDENCE ROUTING / NO NEW ESTIMATION / NOT A FORECAST / NOT DEPLOYABLE**

038 consolidates the evidence-state changes created by 033-037.

## Canonical upgrades

### Gold
Status:
`CORE_SUPPORTED + MULTI_MECHANISM_MAP_AVAILABLE`

Gold phase evidence remains core-supported.

033 adds mechanism context across:
- inflation level/direction
- growth
- energy
- USD
- real-rate proxy / DFII10
- NFCI
- stress timing

No dominant driver is promoted.

### U.S. housing
Status:
`SUPPORTED_SLOW_MOVING + FINANCING_ACTIVITY_PRICE_TIMING_MAP`

034 adds:
- mortgage rates
- Treasury context
- permits
- starts
- new-home sales
- paired ordering diagnostics

Housing risk remains:
`DECLINE_24M`

### Long-duration Treasury

Target:
- TLT remains TARGET_ETF_LIMITED_HISTORY.

Proxy:
- VUSTX_LONG_TREASURY_PROXY = SUPPORTED_PROXY_DESCRIPTIVE.

This is the clearest evidence upgrade since 032.

### Listed REIT

VNQ:
- TARGET_ETF_LIMITED_HISTORY

VGSIX_REIT_PROXY:
- bridge-valid
- LIMITED_PROXY_DESCRIPTIVE

FRESX_REIT_ACTIVE_PROXY:
- NOT_PROMOTED_DUAL_BRIDGE_FAIL

No additional proxy search is authorized merely to obtain a passing deep-history result.

### Bitcoin

Status remains:
`LIMITED_DESCRIPTIVE`

No synthetic historical backfill.

The next step is mechanism research using genuine 2014+ history.

## Reproducibility

Workflow:
- run id: `36221488702`
- source commit: `c018892af2c09ce70243ab6abacb64848c13776e`
- output commit: `f19a6e82563a13173761dd0d71b1ee22feea014d`
- result: SUCCESS

## Next research priority

039 Bitcoin Liquidity / Risk-Regime Mechanism Map.

Key principle:
short history should be handled by richer mechanism evidence, not fabricated long history.
