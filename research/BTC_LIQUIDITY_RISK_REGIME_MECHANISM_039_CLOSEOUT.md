# BTC-LIQUIDITY-RISK-REGIME-MECHANISM-039 — CLOSEOUT

Date: 2026-09-26

## Final status

**QC PASS / GENUINE-2014+ BITCOIN MECHANISM MAP / ERA-DEPENDENT / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**

039 replaces the temptation to synthetically backfill Bitcoin history with a richer mechanism analysis over the genuine public BTC-USD sample.

## Sample and data discipline

- BTC source history begins: 2014-09-17
- first complete BTC price month: 2014-10
- first complete month-over-month analysis return: 2014-11
- last analysis month: 2026-08
- analysis months: 142
- incomplete September 2026 excluded
- no interpolation
- eight source histories frozen with SHA256

Mechanism variables:
- NASDAQ_RET
- DXY_RET
- DFII10_CHANGE_PP
- VIX_CHANGE
- NFCI_CHANGE
- WALCL_3M_PCT
- M2SL_3M_PCT

Fixed eras:
- ERA_1_EARLY: 2014-11 to 2017-12, n=38
- ERA_2_INSTITUTIONALIZATION: 2018-01 to 2021-12, n=48
- ERA_3_POST_2022: 2022-01 to 2026-08, n=56

## 1. Bitcoin increasingly co-moves with Nasdaq in the fixed-era descriptive map

BTC-Nasdaq Pearson:
- ERA_1: +0.211
- ERA_2: +0.388
- ERA_3: +0.555

Full sample:
- Pearson +0.354
- Spearman +0.408

36M rolling Pearson:
- minimum +0.120
- maximum +0.578
- latest +0.479
- positive-window share 100%

Full-sample state contrast:
- NASDAQ_UP months: n=98, median BTC +5.19%, BTC positive share 74.5%
- NASDAQ_DOWN_OR_FLAT: n=44, median BTC -4.65%, positive share 27.3%
- median difference: +9.84pp

However, cross-era state comparability is WEAK:
- ERA_1 downside state only n=7
- ERA_2 downside state n=14
- ERA_3 downside state n=23

Therefore the stable positive correlation evidence is stronger than a claim that the state-contrast magnitude is stable across all eras.

This direction is consistent with the IMF literature context documenting stronger crypto-equity interconnectedness over time, but 039 remains repository-specific descriptive evidence.

## 2. The dollar relation is negative in all three fixed Pearson eras, but weak and time-varying in magnitude

BTC-DXY Pearson:
- ERA_1 -0.154
- ERA_2 -0.050
- ERA_3 -0.117

Full sample:
- Pearson -0.092
- Spearman -0.067

Full state contrast:
- DXY_UP BTC median +0.97%
- DXY_DOWN_OR_FLAT +2.10%
- difference -1.13pp
- state comparability ROBUST across the three eras

But 36M rolling correlation:
- range -0.315 to +0.165
- latest +0.077
- positive in ~21.5% of windows

Therefore the fixed-era Pearson sign is consistently negative, but “stronger dollar always means Bitcoin falls” is too strong.

## 3. Real-yield association changes sign by era

BTC vs DFII10 monthly change Pearson:
- ERA_1 +0.132
- ERA_2 -0.117
- ERA_3 -0.231

Status:
`ERA_DEPENDENT`

Full sample:
- Pearson -0.100
- Spearman -0.105

State contrast:
- REAL_YIELD_UP median BTC +0.72%
- REAL_YIELD_DOWN_OR_FLAT +3.42%
- difference -2.70pp
- robust state sample comparability across eras

36M rolling:
- range -0.435 to +0.171
- latest +0.068

Thus the project does not support a fixed universal real-yield sign for Bitcoin.

This is descriptive market co-movement, not a monetary-policy shock estimate.

## 4. VIX and NFCI are the most sign-stable stress associations in this design, without being promoted into a driver ranking

### VIX_CHANGE

Pearson:
- ERA_1 -0.070
- ERA_2 -0.339
- ERA_3 -0.335

Full:
- Pearson -0.254
- Spearman -0.274

State contrast:
- VIX_UP median BTC -0.51%
- VIX_DOWN_OR_FLAT +4.94%
- difference -5.45pp

36M rolling:
- range -0.427 to -0.032
- positive-window share 0%
- latest -0.390

State comparability:
`PARTIAL_STATE_COMPARABILITY`
because ERA_1 has only 17 VIX_UP months versus the supported threshold of 18.

### NFCI_CHANGE

Pearson:
- ERA_1 -0.333
- ERA_2 -0.329
- ERA_3 -0.359

Full:
- Pearson -0.286
- Spearman -0.369

State contrast:
- NFCI_TIGHTENING median BTC -1.10%
- NFCI_EASING_OR_FLAT +5.19%
- difference -6.29pp

36M rolling:
- range -0.422 to -0.167
- positive-window share 0%
- latest -0.422

State comparability:
`PARTIAL_STATE_COMPARABILITY`
because ERA_1 has 17 tightening months.

These findings support a stable descriptive association between worsening market/financial conditions and weaker same-month Bitcoin outcomes, but not a causal or predictive score.

## 5. WALCL does not support a stable “Fed balance sheet up = Bitcoin up” rule

BTC vs WALCL 3M change Pearson:
- ERA_1 -0.240
- ERA_2 +0.106
- ERA_3 -0.352

Status:
`ERA_DEPENDENT`

Full:
- Pearson +0.040
- Spearman +0.007

Full-sample state contrast:
- WALCL expanding median BTC +4.02%
- contracting/flat +0.96%
- difference +3.06pp

But:
- ERA_1 state support limited
- ERA_3 state support limited
- cross-era state comparability PARTIAL
- 36M rolling correlation ranges -0.436 to +0.455
- latest -0.360

WALCL is therefore retained as a balance-sheet-scale context variable, not an identified liquidity shock.

## 6. M2 is especially unsuitable as a clean universal Bitcoin-liquidity rule

BTC vs M2 3M change Pearson:
- ERA_1 -0.308
- ERA_2 +0.166
- ERA_3 -0.044

Status:
`ERA_DEPENDENT`

Full:
- Pearson +0.086
- Spearman +0.138

Full-sample state contrast:
- M2 expanding median BTC +1.95%
- contracting/flat -2.24%
- difference +4.19pp
- full-sample support reaches the frozen threshold: 124 vs 18 months

But the post-run state-support audit shows:
- ERA_1: 38 expanding / 0 contracting-or-flat
- ERA_2: 48 / 0
- ERA_3: 38 / 18

Cross-era state comparability:
`WEAK_STATE_COMPARABILITY`

Additionally, M2 retains the 2020 H.6 / Regulation D definition-composition caveat.

Therefore the full-sample +4.2pp contrast must not be called a stable cross-era liquidity mechanism.

## 7. What is stable versus era-dependent

Pearson sign stable across all three fixed eras:
- NASDAQ_RET: positive
- DXY_RET: negative
- VIX_CHANGE: negative
- NFCI_CHANGE: negative

Era-dependent:
- DFII10_CHANGE_PP
- WALCL_3M_PCT
- M2SL_3M_PCT

Sign stability is not causal stability and is not predictive validity.

## Myth audit

039 does not support the following shortcuts as universal causal rules:

- Bitcoin is always uncorrelated with stocks;
- stronger dollar always guarantees lower Bitcoin;
- higher real yields always hurt Bitcoin;
- Fed balance-sheet expansion mechanically causes Bitcoin gains;
- M2 growth is a clean Bitcoin liquidity signal;
- Fed tightening always hurts Bitcoin.

“Bitcoin is digital gold” is **not tested directly** by 039 because Gold is not included in this mechanism design.

## Literature context

IMF (2022) documents rising crypto-equity interconnectedness, especially around/post the pandemic.

Journal of International Money and Finance (2023), *Monetary policy and Bitcoin*, reports that Bitcoin's response to U.S. monetary policy changed over time and became more similar to risky assets after 2020.

These sources motivate time variation; they do not substitute for this repository's measurements and do not make 039 causal.

## Product implication

PandaAI may expose:

`current mechanism values + fixed-era association + rolling-36M association + state contrast + sample-support audit + source freshness + caveats`

It must not output:
- dominant liquidity score;
- expected BTC return;
- optimized lag;
- identified Fed-liquidity shock;
- best Bitcoin regime;
- buy/sell instruction.

## Reproducibility

Final authoritative workflow:
- run id: `36222161781`
- source commit: `e3b567cb3692837cd96073c948e7f7179fb09ffb`
- output commit: `d7a5c12c43bfec3a446a8ba15f08ba7318ca3843`
- result: SUCCESS

Earlier successful run:
- `36222034094`

It is superseded for interpretation by the state-support amendment. Core associations were unchanged.

## QC

- analysis months: 142
- fixed eras: 38 / 48 / 56
- source hashes: 8/8 complete
- partial Sep 2026: excluded
- inception-partial Sep 2014: not used as return month
- interpolation: false
- mechanisms: 7 exactly
- full associations: 7
- fixed-era associations: 21
- state contrasts: 28
- state-support audit: 7
- rolling window: 36M fixed, not optimized
- p-values: false
- mechanism ranking: false
- optimized lag: false
- forecast: false
- synthetic Bitcoin history: false
- causal monetary-policy claim: false
- private-paper inputs: false
- causal status: NONE
- OOS: NOT_A_FORECASTING_MODEL
- deployment: NOT_DEPLOYABLE

## Next research direction

039 resolves the major Bitcoin mechanism gap enough for public research synthesis.

The next high-value question is **not** another short-history Bitcoin factor.

Priority:
**040 Cash Hurdle / Inflation-Adjusted Cross-Asset Opportunity Map**

This should answer, phase by phase:
- what nominal asset returns looked like relative to the mechanical cash carry already available;
- what inflation-adjusted real outcomes looked like;
- how path risk changes the apparent opportunity;
- whether a positive nominal endpoint actually beat cash / inflation;
- with no best-asset ranking or allocation prescription.
