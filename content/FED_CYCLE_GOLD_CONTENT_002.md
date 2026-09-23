# Content Card — 加息后黄金到底怎么走？长历史答案不是简单涨跌
Content ID: FED_CYCLE_GOLD_CONTENT_002
Evidence: FED-CYCLE-GOLD-LONGHIST-MONTHLY-001
Status: **PUBLIC-SAFE / DESCRIPTIVE ONLY / NOT A TRADING CLAIM**

## Hook

“第一次加息以后，黄金到底涨还是跌？”

长历史数据给出的答案更接近：

**这个问题问得太简单了。**

## Evidence

10 个机械定义的 FIRST_HIKE tightening legs，统一使用 1960+ World Bank monthly Gold，事件当月剔除：

- +1M 中位数：**+1.55%**
- +3M：**+0.51%**
- +6M：**-1.90%**
- +12M：**+0.24%**
- +24M：**+0.58%**
- 24M 最大回撤中位数：**16.64%**
- 最深单次 24M MDD：**39.10%**

也就是说，长周期 endpoint 的中位数接近零，但中间路径可能经历很深的回撤。

## Recovery

Kaplan–Meier right-censoring-aware estimates:

- 50% recovery KM median: **8 months**
- 100% recovery KM median: **19 months**
- 100% recovery: 6/10 observed, 4/10 right-censored inside the frozen 60-month search window
- at 24 months, KM estimate still has **50%** of episodes not yet fully recovered

## Why 2015 and 2022 can tell different stories

Under the same monthly convention:

- 2015 +12M: **+6.54%**, MDD **13.66%**
- 2022 +12M: **+3.07%**, MDD **14.09%**

But the separate daily COMEX futures proxy gives 2022 +252 observations **-0.35%**.

So even the sign of an endpoint can depend on instrument, frequency and endpoint definition.

## Safe conclusion

**DESCRIPTIVE RESULT:** a Fed tightening-cycle marker by itself does not produce a stable Gold direction in this long-history sample.

A better research object is:

`Gold path distribution + drawdown + recovery + predetermined macro state`.

## Mandatory disclosure

- sample: 10 FIRST_HIKE tightening legs;
- Gold source: World Bank monthly series via datasets/gold-prices, 1960+;
- event month omitted from clean outcomes;
- pre-1994 Fed dates are historical target reconstructions;
- realized Fed action is not an identified monetary-policy shock;
- no causal claim;
- no confirmatory p-value/FDR family;
- OOS not applicable;
- not a trading signal.

## Do not say

- “加息后黄金一定涨”
- “加息后黄金一定跌”
- “历史规律证明第 X 月买入”
- “美联储加息导致黄金回撤 16%”

## Evidence files

- `research/FED_CYCLE_GOLD_LONGHIST_MONTHLY_001_LOCK.md`
- `research/FED_CYCLE_GOLD_LONGHIST_MONTHLY_001_RECOVERY_AMENDMENT.md`
- `results/gold_long_history_monthly_v1/QC.json`
- `results/gold_long_history_monthly_v1/DISTRIBUTION_SUMMARY.csv`
- `results/gold_long_history_monthly_v1/RECOVERY_SURVIVAL_SUMMARY.csv`
- `results/gold_long_history_monthly_v1/CROSS_FREQUENCY_AUDIT.csv`
- `research/FED_CYCLE_GOLD_LONGHIST_MONTHLY_001_CLOSEOUT.md`
