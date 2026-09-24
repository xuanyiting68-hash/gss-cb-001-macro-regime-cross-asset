# FED-CYCLE-RECOVERY-EXTENSION-015 — New-Asset Drawdown Recovery Lock
Date: 2026-09-24
Status: **FROZEN BEFORE EXECUTION / DESCRIPTIVE / PUBLIC-SAFE**

## 1. Purpose

Extend the already-established PHASE-CLOCK-004 drawdown/recovery framework to the new asset classes introduced in CROSS-ASSET-EXPANSION-014.

Do not re-estimate or replace the existing 004 recovery results for Gold, S&P 500, Nasdaq, WTI or USD_BROAD.

New liquid assets:
- TLT;
- VNQ;
- BTC_USD;
- DXY.

Slow real asset:
- US_HOUSE_PRICE.

## 2. Historical cycle universe

Use the same canonical historical cycle registry as 014:
- 10 mechanical cycles;
- 7 broad episodes;
- current 2026 live cycle excluded.

Anchors:
- FIRST_HIKE;
- LAST_HIKE;
- PAUSE_START;
- FIRST_CUT.

## 3. Liquid-asset drawdown definition

For TLT/VNQ/BTC/DXY reuse PHASE-CLOCK-004 exactly:

- baseline = month before anchor month;
- omit anchor month;
- next 12 complete months form the drawdown-identification window;
- running peak includes baseline;
- MDD = maximum peak-to-trough decline inside baseline + 12M path;
- MDD trough month = month of maximum drawdown.

If MDD <= numerical tolerance, no recovery clock is opened.

## 4. Liquid-asset recovery definition

For episodes with positive MDD:

1. identify the running peak that generated the 12M maximum drawdown;
2. identify the corresponding trough;
3. 50% recovery threshold = trough + 0.5 × (peak - trough);
4. 100% recovery threshold = prior peak;
5. search from trough month through at most 60 months after trough.

Record:
- recovery50_months;
- recovery100_months;
- observed flags;
- right-censor month.

This must match the 004 implementation.

## 5. Housing drawdown definition

Housing remains separate.

For US_HOUSE_PRICE:
- baseline = month before anchor month;
- omit anchor month;
- next 24 complete months form the housing drawdown-identification window;
- running peak includes baseline;
- decline_24m = maximum peak-to-trough decline within baseline + 24M path;
- identify the peak and trough generating that decline.

Housing recovery:
- same 50% and 100% prior-peak recovery thresholds;
- search up to 60 months after the housing trough;
- right-censor when the threshold is not reached.

Do not compare housing months mechanically with liquid-market liquidity.

## 6. Weighting

Reuse 014 broad-episode weights exactly:
- each broad episode total weight = 1 within asset × anchor;
- multiple mechanical cycles inside one broad episode split that unit weight.

## 7. Survival summary

Use weighted Kaplan-Meier-style recovery curves as in PHASE-CLOCK-004.

For every asset × anchor × recovery level report:
- n mechanical legs;
- n broad episodes;
- positive-drawdown episodes;
- observed recoveries;
- right-censored recoveries;
- weighted KM median recovery months when survival_not_recovered reaches <= 0.5.

If no weighted median is reached within observed/censored support, keep it missing.

## 8. Support labels

Reuse 014 support labels:
- SUPPORTED_DESCRIPTIVE: >=5 mechanical legs and >=4 broad episodes;
- LIMITED_DESCRIPTIVE: >=2 broad episodes but below supported threshold;
- INSUFFICIENT_SUPPORT: <2 broad episodes.

Support labels must remain visible beside recovery results.

## 9. Cross-module consistency QC

For liquid assets:
- 12M MDD and trough month must reproduce 014 MARKET_PHASE_METRICS to numerical tolerance.

For housing:
- 24M decline and trough month must reproduce 014 HOUSING_PHASE_METRICS.

Also require:
- recovery100_months >= recovery50_months whenever both observed;
- no current-2026 cycle;
- no negative drawdowns;
- raw Yahoo / Case-Shiller histories not committed.

## 10. Frozen questions

Q1. Does duration recovery accelerate after LAST_HIKE / PAUSE compared with FIRST_HIKE?

Q2. Does listed REIT recovery differ from direct national housing recovery?

Q3. How much right-censoring remains in BTC because its cycle history is short?

Q4. Does DXY generally recover prior peaks quickly enough for its phase effect to remain mostly contextual rather than persistent?

These are descriptive questions only.

## 11. Evidence boundary

**DESCRIPTIVE DRAWDOWN/RECOVERY EXTENSION / RIGHT-CENSORING PRESERVED / NOT CAUSAL / NOT A FORECAST / NOT DEPLOYABLE**
