# FED-CYCLE-CROSS-ASSET-EXPANSION-014 — Frozen protocol

Date: 2026-09-24  
Status: **FROZEN BEFORE OUTCOME EXECUTION / PUBLIC-SAFE / DESCRIPTIVE ONLY**

## 1. Purpose

Extend the existing timing-corrected Fed-cycle phase clock beyond Gold, U.S./Asia equities and WTI into asset classes that matter for allocation but are currently missing or under-covered:

- long-duration U.S. Treasury proxy;
- listed U.S. REIT proxy;
- Bitcoin;
- U.S. dollar index proxy;
- U.S. residential house prices;
- 2Y and 10Y Treasury-yield paths;
- cash/policy-rate carry benchmark.

This module is designed to improve cross-asset understanding, not to manufacture a trading rule.

## 2. Canonical policy-cycle anchors

Reuse the frozen timing-corrected public cycle registry from:

`results/fed_cycle_path_v1_1/FED_TIGHTENING_CYCLES.csv`

and the same broad-episode clustering logic used by PHASE-CLOCK-004.

Anchors:

- FIRST_HIKE
- LAST_HIKE
- PAUSE_START
- FIRST_CUT

No cycle boundary may be changed after viewing 014 outcomes.

The current 2026 cycle is **not** included in completed historical outcome summaries because it is still live and has not matured through the required horizons.

## 3. Asset/source layer

### Liquid / market-price diagnostics

1. **TLT**
   - source: Yahoo Finance public chart history;
   - symbol: `TLT`;
   - use adjusted close when present;
   - interpretation: long-duration Treasury ETF total-return proxy;
   - historical support expected to be limited by 2002 inception.

2. **VNQ**
   - source: Yahoo Finance public chart history;
   - symbol: `VNQ`;
   - use adjusted close when present;
   - interpretation: listed U.S. equity-REIT total-return proxy;
   - not direct private-property value.

3. **BTC_USD**
   - source: Yahoo Finance public chart history;
   - symbol: `BTC-USD`;
   - use close;
   - interpretation: Bitcoin USD price;
   - short history must remain visible in support labels.

4. **DXY**
   - source: Yahoo Finance public chart history;
   - symbol: `DX-Y.NYB`;
   - use close;
   - interpretation: U.S. Dollar Index market proxy, not the Fed broad-dollar index.
   - If acquisition fails, retain the existing USD_BROAD diagnostic from PHASE-CLOCK-004 and mark DXY unavailable; do not substitute a new definition after seeing results.

### Slow real-asset diagnostic

5. **US_HOUSE_PRICE**
   - source: S&P Cotality Case-Shiller U.S. National Home Price Index via FRED;
   - series: `CSUSHPINSA`;
   - frequency: monthly;
   - raw copyrighted source history is not committed;
   - only provenance hashes and derived event/summary metrics may be committed;
   - interpretation: national owner-occupied residential price index, not a liquid investable total-return asset.

### Rate / carry state variables

6. **DGS2** — 2Y Treasury yield via FRED.
7. **DGS10** — 10Y Treasury yield via FRED.
8. **DFF** — effective federal funds rate via FRED, used only to construct a mechanical cash-carry benchmark.

Yield changes are not labeled bond returns.

## 4. Frequency and endpoint convention

### Liquid market assets

Use monthly observations created from daily history.

For TLT/VNQ:
- monthly mean of adjusted close when available.

For BTC/DXY:
- monthly mean of close.

Common PHASE-CLOCK-004 convention:
- baseline = month before anchor month;
- anchor month omitted;
- next 12 complete months;
- report +3M, +6M, +12M endpoint return;
- 12M maximum drawdown;
- MDD trough month;
- late-trough share months 7-12.

### Housing

Housing is intentionally separated because it is slow-moving, illiquid and published with a lag.

Convention:
- baseline = month before anchor month;
- anchor month omitted;
- evaluate +6M, +12M and +24M;
- 24M peak-to-trough decline from the post-anchor path;
- trough month inside the 24M window.

Do not compare housing MDD mechanically with daily-traded asset MDD as if liquidity were equivalent.

### Rates

For DGS2 and DGS10:
- monthly mean yield;
- report change at +3M/+6M/+12M in basis points;
- maximum increase and maximum decrease over the 12M window;
- no return label.

### Cash carry

Construct a mechanical monthly cash return using the monthly average DFF:

`r_m = (DFF_m / 100) / 12`

Compound over complete post-anchor months.

Report +3M/+6M/+12M cumulative carry.

This ignores fees, taxes and intra-month compounding and is only a benchmark.

## 5. Broad-episode weighting

As in PHASE-CLOCK-004:

- mechanical legs inside the same broad episode share one unit of total weight;
- weights are recalculated inside each asset × anchor cell according to available support.

## 6. Support labels

For each asset × anchor cell:

- **SUPPORTED_DESCRIPTIVE**: >=5 mechanical legs and >=4 broad episodes;
- **LIMITED_DESCRIPTIVE**: >=2 broad episodes but below the supported threshold;
- **INSUFFICIENT_SUPPORT**: <2 broad episodes.

Short-history assets must not be promoted because their point estimates look large.

## 7. Frozen questions

### Q1 — Duration / bond proxy
How does long-duration Treasury total-return proxy path risk differ across FIRST_HIKE, LAST_HIKE, PAUSE_START and FIRST_CUT?

### Q2 — Listed real estate
Does listed REIT path risk resemble equities, bonds or direct housing across policy phases?

### Q3 — Crypto
Does Bitcoin behave more like a high-beta risk asset than a monetary hedge in the limited historical Fed-cycle sample?

No strong inference is permitted from fewer than two broad episodes.

### Q4 — Direct housing
How slowly do national house prices react around Fed-cycle anchors, and does any weakness concentrate later than listed-market drawdowns?

### Q5 — Dollar
How does DXY path behavior differ across phases, and does it add context to Gold without being treated as a causal Gold driver?

### Q6 — Rates and cash
What happens to 2Y/10Y yields and mechanical cash carry across the same phase clock?

## 8. No hypothesis fishing

The following are frozen before execution:

- assets;
- sources;
- anchors;
- horizon definitions;
- support thresholds;
- broad-episode weighting;
- no p-value family.

Do not:
- add/remove an asset because its sign is inconvenient;
- change 12M to another liquid-asset horizon after seeing outcomes;
- change 24M housing horizon after seeing outcomes;
- substitute price close for adjusted close in TLT/VNQ merely to improve the story;
- treat the live 2026 cycle as a completed historical episode.

## 9. Evidence class

Primary evidence class:

**DESCRIPTIVE**

There is no structural monetary-policy shock identification in this module.

Therefore:
- causal status: NONE;
- FDR: NOT APPLICABLE;
- OOS: NOT A FORECASTING MODEL;
- deployment: NOT DEPLOYABLE.

## 10. Product use boundary

PandaAI may use QC-passed 014 outputs as:

`policy phase + asset class + historical path-risk distribution + support strength + current-state context`

It may not translate 014 into deterministic commands such as:
- hikes -> buy cash / short bonds;
- cuts -> buy equities;
- tightening -> short Bitcoin;
- rate cuts -> housing always rises.

## 11. Current-cycle boundary

As of 2026-09-24, the public prospective infrastructure records the current cycle as one 25 bp hike beginning 2026-09-16.

014 must not use future or incomplete 2026 outcomes to tune historical summaries.

## 12. Raw-data policy

Do not commit raw Yahoo or copyrighted Case-Shiller histories.

Commit only:
- provenance/source registry;
- derived cycle metrics;
- derived aggregate summaries;
- QC;
- report/figures that do not reproduce raw source histories.
