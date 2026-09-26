# BTC-LIQUIDITY-RISK-REGIME-MECHANISM-039 — LOCK

Date locked: 2026-09-26

## Purpose

Build a public-safe Bitcoin mechanism map using the genuine 2014+ market history.

039 asks whether Bitcoin's contemporaneous association with:
- U.S. growth/risk equities,
- the U.S. dollar,
- real yields,
- equity volatility,
- broad financial conditions,
- the Federal Reserve balance-sheet scale,
- the U.S. M2 money stock

is stable or era-dependent.

039 does **not** backfill synthetic Bitcoin history, identify a monetary-policy shock, fit a return forecast, choose an optimal lag, or create a trading score.

## Sample

Market history begins with the public BTC-USD history available in September 2014.

Analysis uses monthly data through the last **complete** calendar month:
- 2026-08

The incomplete current month is excluded.

## Frozen market / macro inputs

### BTC_USD
- Yahoo Finance public chart history
- BTC-USD
- daily close
- transformed to calendar-month average
- BTC monthly return = monthly-average ratio - 1

### NASDAQ
- Yahoo Finance public chart history
- ^IXIC
- daily close
- calendar-month average
- monthly return

Interpretation:
`RISK_BETA_NASDAQ`

This is market co-movement, not an equity-to-Bitcoin causal shock.

### DXY
- Yahoo Finance public chart history
- DX-Y.NYB
- daily close
- calendar-month average
- monthly return

Interpretation:
`USD`

### DFII10
- 10-Year Treasury Inflation-Indexed Security, Constant Maturity
- Board of Governors via FRED
- daily percent
- calendar-month mean
- monthly change in percentage points

Interpretation:
`REAL_YIELD`

No fixed inverse-sign theory is imposed.

### VIXCLS
- CBOE Volatility Index: VIX
- daily index
- calendar-month mean
- monthly change

Interpretation:
`MARKET_STRESS_VIX`

### NFCI
- Chicago Fed National Financial Conditions Index
- weekly
- calendar-month mean
- monthly change

Positive NFCI = tighter-than-average financial conditions.

Interpretation:
`FINANCIAL_CONDITIONS_NFCI`

### WALCL
- Federal Reserve total assets
- weekly Wednesday level
- monthly mean
- 3-month percentage change

Interpretation:
`FED_BALANCE_SHEET_SCALE`

WALCL is not labeled "liquidity" without qualification and is not treated as an identified policy shock.

### M2SL
- seasonally adjusted M2
- monthly
- 3-month percentage change

Interpretation:
`M2_MONEY_STOCK`

Important:
- the 2020 H.6 / Regulation D changes altered monetary-aggregate composition;
- all M2 results spanning this period retain a structural-definition caveat;
- M2 is a contextual monetary aggregate, not a direct Bitcoin-liquidity causal variable.

## Source-snapshot rule

For every input:
- record source URL;
- retrieval UTC;
- SHA256 of raw response;
- raw bytes;
- first and last observation;
- transformation;
- raw source history not committed.

FRED downloads should be date-scoped to the actual analysis era where practical.

## Frozen monthly panel

The canonical row unit is a calendar month.

Required fields:
- month
- BTC level / return
- Nasdaq level / return
- DXY level / return
- DFII10 level / monthly change
- VIX level / monthly change
- NFCI level / monthly change
- WALCL level / 3M pct change
- M2SL level / 3M pct change
- era label

No missing monthly value may be interpolated.

## Fixed eras

These windows are frozen before results:

### ERA_1_EARLY
2014-10 through 2017-12

### ERA_2_INSTITUTIONALIZATION
2018-01 through 2021-12

### ERA_3_POST_2022
2022-01 through 2026-08

The labels are descriptive shorthand only.

No breakpoint is estimated from Bitcoin outcomes.

## Frozen mechanism variables

1. NASDAQ_RET
2. DXY_RET
3. DFII10_CHANGE_PP
4. VIX_CHANGE
5. NFCI_CHANGE
6. WALCL_3M_PCT
7. M2SL_3M_PCT

## Association analysis

For each mechanism variable, report for:
- FULL_SAMPLE
- ERA_1_EARLY
- ERA_2_INSTITUTIONALIZATION
- ERA_3_POST_2022

Metrics:
- paired month count
- Pearson correlation with BTC monthly return
- Spearman correlation
- sign of Pearson / Spearman

No p-values.

### Era stability label

For each mechanism:
- `SIGN_STABLE_ALL_ERAS` if all three eras have >=24 paired months and Pearson signs are the same;
- `ERA_DEPENDENT` if all eras have >=24 paired months and signs differ;
- `INSUFFICIENT_ERA_SUPPORT` otherwise.

Magnitude is not used to select a "dominant" driver.

## Frozen state contrasts

For every scope (FULL_SAMPLE + three fixed eras), compare BTC monthly-return distributions under the following contemporaneous states.

### NASDAQ
- NASDAQ_UP: NASDAQ_RET > 0
- NASDAQ_DOWN_OR_FLAT: <= 0

### DXY
- DXY_UP: DXY_RET > 0
- DXY_DOWN_OR_FLAT: <= 0

### REAL_YIELD
- REAL_YIELD_UP: DFII10_CHANGE_PP > 0
- REAL_YIELD_DOWN_OR_FLAT: <= 0

### VIX
- VIX_UP: VIX_CHANGE > 0
- VIX_DOWN_OR_FLAT: <= 0

### NFCI
- NFCI_TIGHTENING: NFCI_CHANGE > 0
- NFCI_EASING_OR_FLAT: <= 0

### WALCL
- WALCL_EXPANDING_3M: WALCL_3M_PCT > 0
- WALCL_CONTRACTING_OR_FLAT_3M: <= 0

### M2
- M2_EXPANDING_3M: M2SL_3M_PCT > 0
- M2_CONTRACTING_OR_FLAT_3M: <= 0

For each contrast:
- n_a / n_b
- median BTC monthly return in each state
- BTC positive-month share in each state
- oriented median difference A minus B
- support status

Support:
- both states >=18 months: `SUPPORTED_DESCRIPTIVE`
- minimum state count 9..17: `LIMITED_DESCRIPTIVE`
- minimum state count <9: `INSUFFICIENT_VARIATION`

No inferential significance claim.

## Frozen rolling correlation diagnostic

Use a fixed trailing 36-month window.

For each mechanism:
- rolling Pearson correlation with BTC monthly return;
- no window if fewer than 36 complete paired months.

Summaries:
- number of windows
- median
- minimum
- maximum
- share positive
- latest complete-window value

Status:
`TIME_VARIATION_DIAGNOSTIC`

No best window or optimized lookback.

## Evidence statuses

Allowed:
- SUPPORTED_DESCRIPTIVE
- LIMITED_DESCRIPTIVE
- INSUFFICIENT_VARIATION
- SIGN_STABLE_ALL_ERAS
- ERA_DEPENDENT
- INSUFFICIENT_ERA_SUPPORT
- TIME_VARIATION_DIAGNOSTIC
- LITERATURE_CONTEXT

## External literature role

External literature is contextual only.

Frozen context includes:
- IMF (2022), Cryptic Connections: crypto-equity interconnectedness increased materially, especially around/post pandemic;
- Journal of International Money and Finance (2023), Monetary policy and Bitcoin: Bitcoin's response to U.S. monetary policy changed over time and became more similar to risky assets after 2020.

Literature context does not establish the repository's correlations or causality.

## Frozen research questions

1. Has Bitcoin's Nasdaq association changed across fixed eras?
2. Is Bitcoin consistently inversely associated with the U.S. dollar?
3. Is the real-yield association stable?
4. Does BTC behave differently when VIX is rising?
5. Does BTC behave differently when NFCI is tightening?
6. Are WALCL-expansion months systematically different for BTC?
7. Are M2-expansion months systematically different for BTC?
8. Which mechanism signs are stable across all three fixed eras?
9. Which are era-dependent?
10. Does the 36M rolling Nasdaq correlation rise after 2020?
11. Is "Bitcoin is always uncorrelated with stocks" supported?
12. Is "Bitcoin is digital gold" established by this design?
13. Is "Fed tightening always hurts Bitcoin" established?
14. Is "balance-sheet expansion mechanically causes BTC gains" established?
15. What should PandaAI surface without turning mechanism evidence into a trading signal?

## Frozen outputs

- SOURCE_REGISTRY.csv
- BTC_MECHANISM_MONTHLY_PANEL.csv
- BTC_FULL_SAMPLE_ASSOCIATIONS.csv
- BTC_FIXED_ERA_ASSOCIATIONS.csv
- BTC_ERA_STABILITY.csv
- BTC_STATE_CONTRASTS.csv
- BTC_ROLLING_36M_CORRELATIONS.csv
- BTC_ROLLING_CORRELATION_SUMMARY.csv
- BTC_MECHANISM_EVIDENCE_MATRIX.csv
- BTC_LITERATURE_CONTEXT.csv
- BTC_MECHANISM_MYTH_AUDIT.csv
- BTC_INVESTOR_QUESTION_REGISTRY.csv
- BTC_MECHANISM_SYNTHESIS_ZH.md
- PANDAAI_BTC_MECHANISM_SCHEMA.json
- BTC_LIQUIDITY_RISK_REGIME_MECHANISM_039_REPORT.md
- QC.json

## QC gates

PASS requires:

1. BTC history starts in the genuine 2014 era;
2. last analysis month is 2026-08 or the latest complete month fixed by this lock;
3. incomplete September 2026 excluded;
4. source SHA256 recorded for all eight inputs;
5. no missing value interpolation;
6. fixed eras exactly preserved;
7. seven mechanism variables exactly preserved;
8. all full-sample associations generated;
9. all three fixed-era association sets generated;
10. era stability uses sign only and >=24-month rule exactly;
11. state contrast cutoffs are zero exactly;
12. state-support thresholds are 18 / 9 exactly;
13. 36M rolling window is fixed and not optimized;
14. M2 structural-definition caveat retained;
15. WALCL is not called an identified liquidity shock;
16. no mechanism winner/ranking;
17. no expected BTC return forecast;
18. no optimized lag;
19. no causal monetary-policy claim;
20. no synthetic BTC history;
21. no p-values;
22. private-paper inputs = false;
23. causal status = NONE;
24. OOS status = NOT_A_FORECASTING_MODEL;
25. deployment status = NOT_DEPLOYABLE.

## Interpretation boundary

039 maps contemporaneous historical associations and their time variation.

It does not identify causal monetary-policy effects, forecast Bitcoin returns, or recommend crypto exposure.
