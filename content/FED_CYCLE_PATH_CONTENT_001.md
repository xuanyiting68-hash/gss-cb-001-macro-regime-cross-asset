# Content Card — 为什么 endpoint return 会骗你？
Content ID: FED_CYCLE_PATH_CONTENT_001
Evidence: FED-CYCLE-PATH-001 v1.1
Status: **PUBLIC-SAFE / DESCRIPTIVE ONLY / NOT A TRADING CLAIM**

## Core hook

“加息后一年股市最后涨了，不代表这一年风险很小。”

## Evidence-backed points

Under the frozen FIRST_HIKE path definition:

- S&P 500, n=10 tightening legs: 252-observation endpoint median **+4.99%**, but MDD median **11.31%**.
- Nasdaq, n=10: 252-observation endpoint median **-0.82%**, MDD median **20.67%**.
- WTI, n=8: 252-observation endpoint median **+22.04%**, MDD median **30.16%**.
- Gold daily proxy, n=3 only: 252-observation endpoint median **+6.81%**, MDD median **17.37%**.

Gold is `GC=F` continuous COMEX futures proxy, not XAUUSD spot.

## 2015 vs 2022 Gold example

Same frozen FIRST_HIKE specification:

- 2015: 252D +6.81%, MDD 17.37%.
- 2022: 252D -0.35%, MDD 17.90%.

The important difference is not simply “one rose and one fell”; their path, MAE/MFE, trough timing and recovery were different.

## Safe conclusion

**DESCRIPTIVE RESULT:** endpoint return is an incomplete description of investment risk. A risk map should include drawdown depth, adverse excursion, time-to-trough, volatility and recovery time.

## Required disclosure for publication

- Realized Fed action is a descriptive cycle marker, not an identified monetary-policy shock.
- No causal claim: do not say “Fed hikes caused” these paths.
- No confirmatory p-value/FDR family was run in this foundation module.
- OOS: not applicable; this is not a forecasting model.
- Gold FIRST_HIKE daily support is only n=3.
- Pre-1994 target dates are historical reconstructions, not exact modern announcement timestamps.
- This is not a trading signal or deployment rule.

## Forbidden headlines

Do not use:

- “加息后第 X 天必跌”
- “美联储一加息，纳指一定回撤 20%”
- “加息后黄金必涨/必跌”
- “历史证明可以靠这个择时赚钱”

## Evidence files

- `results/fed_cycle_path_v1_1/QC.json`
- `results/fed_cycle_path_v1_1/DISTRIBUTION_SUMMARY.csv`
- `results/fed_cycle_path_v1_1/GOLD_2015_2022_METRICS.csv`
- `results/fed_cycle_path_v1_1/FED_CYCLE_PATH_001_V1_1_REPORT.md`
- `research/FED_CYCLE_PATH_001_V1_1_CLOSEOUT.md`
