# FED-CYCLE-FOUR-PHASE-INVESTOR-ATLAS-032 — CLOSEOUT

Date: 2026-09-26

## Final status

**QC PASS / FOUR-PHASE INVESTOR KNOWLEDGE ATLAS / 52-ROW MASTER EVIDENCE REORGANIZED / NOT A FORECAST / NOT DEPLOYABLE**

032 converts the existing 021 evidence stack into a phase-organized investor knowledge atlas without re-estimating prices or fitting a model.

## Coverage

- 20 CORE_SUPPORTED asset x phase rows:
  - DXY
  - GOLD
  - NASDAQ
  - SP500
  - WTI
- 12 rates/cash context rows:
  - DGS2
  - DGS10
  - MECHANICAL_CASH_DFF
- 12 stress rows:
  - BAA10Y_SPREAD
  - VIX
  - COPPER
- 32 extension/diagnostic rows:
  - BTC_USD
  - TLT
  - VNQ
  - US_HOUSE_PRICE
  - HANG_SENG
  - KOSPI
  - NIKKEI_225
  - SHANGHAI_COMPOSITE
- 20 investor-question answers
- 12 myth-audit rows

## Main four-phase synthesis

### FIRST_HIKE

Historical medians can show weak short-horizon equities and positive 12-month endpoints at the same time.

- S&P 500: 3M -2.6%; 12M +8.0%
- Nasdaq: 3M -6.2%; 12M +6.5%
- 2Y / 10Y 12M yield change: +122.7bp / +55.8bp

Therefore “hiking starts = U.S. equities must be lower one year later” is not supported as a simple historical rule.

### LAST_HIKE

Market yields can already be falling while cash carry remains high.

- S&P 500 12M: +16.7%
- Nasdaq 12M: +15.6%
- 2Y / 10Y 12M yield change: -124.6bp / -59.9bp
- mechanical cash 12M carry: +5.9%

### PAUSE_START

The pause window historically combines:
- strong positive U.S.-equity median endpoints;
- materially lower 2Y/10Y yields;
- still-high cash carry;
- modestly positive Gold;
- mildly negative WTI and DXY.

This is not a single generic risk-on label.

### FIRST_CUT

The most important distinction is endpoint versus path.

- S&P 500 12M: +11.0%; MDD 14.0%; median trough M8
- Nasdaq 12M: +6.0%; MDD 17.5%; median trough M8
- WTI 12M: -16.9%; MDD 22.2%; median trough M11

Stress remains capable of developing after the anchor:
- Baa maximum widening median +38bp, peak M7
- VIX maximum increase median +8.5 points, peak M8
- copper stress median ~20.0%, peak M9

These are ex-post window statistics, not real-time bottom signals.

## Evidence-tier discipline

### LIMITED_SAMPLE
BTC / TLT / VNQ remain limited.

Examples:
- TLT FIRST_CUT 12M median +15.1%, only ~3 episodes
- VNQ PAUSE 12M median +23.5%, only 2-3 episodes
- BTC PAUSE 12M median +116.7%, only 2 episodes

Large magnitudes do not compensate for short histories.

### SUPPORTED_SLOW_MOVING
U.S. housing uses a 24-month slow-moving decline framework, not 12-month traded-asset MDD.

### DIAGNOSTIC_ONLY
Asian equity responses remain heterogeneous rather than a single Fed-beta rule.

FIRST_CUT 12M diagnostic medians:
- Hang Seng -8.7%
- KOSPI +4.3%
- Nikkei +9.6%
- Shanghai Composite -28.7%

## Important non-rules

032 explicitly rejects the following as simple universal rules:

- hiking begins -> U.S. equities must be lower one year later;
- last hike -> market yields must keep rising;
- pause -> cash carry quickly disappears;
- first cut -> risk assets have already bottomed;
- first cut -> oil must benefit;
- falling Treasury yields -> cash carry is already low;
- positive 12M endpoint -> low interim risk;
- Bitcoin / REIT short-history medians -> stable cycle law;
- Asian equities -> uniform Fed-cycle response.

## Product implication

PandaAI should surface:

`phase + core historical distributions + path risk + recovery clock + yield context + cash carry + stress context + support tier + freshness + boundary`

It should not output:
- best asset;
- best phase;
- expected return;
- bottom date;
- closest current analog;
- buy/sell instruction.

## Reproducibility

Workflow:
- `.github/workflows/fed-cycle-four-phase-investor-atlas-032-v1.yml`
- run id: `36213817369`
- source commit: `ff1faf4294e661cb8047d318b7029e886aad5b1d`
- output commit: `5f9416d3417ff2ec2c232fa1f0eebf3d132acd68`
- result: SUCCESS

## QC summary

- core rows: 20
- rates/cash rows: 12
- stress rows: 12
- extension/diagnostic rows: 32
- investor questions: 20
- myth rows: 12
- evidence tiers preserved: true
- housing metric: DECLINE_24M
- FIRST_CUT endpoint and path risk jointly reported: true
- yield changes labeled as yields, not bond returns: true
- best-asset outputs: 0
- best-phase outputs: 0
- current-analog rankings: 0
- deterministic bottom rules: 0
- expected-return forecasts: 0
- new price estimation: false
- new inference: false
- p-values: false
- private-paper inputs: false
- causal status: NONE
- OOS: NOT_A_FORECASTING_MODEL
- deployment: NOT_DEPLOYABLE

## Next research direction

The next high-value research branch should deepen mechanisms rather than add more phase-average tables.

Priority candidate:
**033 Gold Mechanism Decomposition**
- Gold vs real yields
- Gold vs DXY
- Gold vs inflation expectations
- Gold vs financial stress
- phase-dependent sign / co-movement
- historical cases and counterexamples
- no causal interpretation without separate identification design.
