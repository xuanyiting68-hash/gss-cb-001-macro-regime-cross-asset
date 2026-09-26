# Bitcoin Liquidity / Risk-Regime Mechanism Map — 039

## 结论框架

Bitcoin只有真实的2014+公开历史，所以039不再假装补更多Fed周期，而是问：它与风险资产、美元、实际利率、市场压力、金融条件和货币/资产负债表变量的关系，是否会随时代变化。

所有结果都是**同月历史关联**，不是因果冲击，也不是下一月预测。

## 1. Bitcoin × Nasdaq：风险资产属性是否强化？

固定时代 Pearson：2014-11–2017-12 +0.211；2018–2021 +0.388；2022–2026-08 +0.555。Era status：SIGN_STABLE_ALL_ERAS。

36个月滚动相关范围 +0.120 到 +0.578，最新窗口 +0.479。

这可以和IMF关于疫情前后crypto-equity interconnectedness上升的文献背景对照，但仓库结果仍以本项目数据为准。

## 2. Bitcoin × 美元

BTC-DXY时代相关：-0.154 / -0.050 / -0.117；状态 SIGN_STABLE_ALL_ERAS。

因此不能先验把“美元涨=BTC跌”当作固定恒等式；是否稳定必须由三个固定时代的符号与状态对比共同判断。

## 3. Bitcoin × 10Y实际利率

BTC与DFII10月变化相关：+0.132 / -0.117 / -0.231；状态 ERA_DEPENDENT。

这只是市场实际利率共变，不是identified monetary-policy shock。JIMF 2023 的因果研究使用更严格的货币政策识别，并发现Bitcoin的政策反应本身也随时间改变。

## 4. VIX / NFCI：压力与金融条件

VIX时代相关：-0.070 / -0.339 / -0.335；NFCI时代相关：-0.333 / -0.329 / -0.359。

全样本状态对比中，VIX_UP minus VIX_DOWN_OR_FLAT 的BTC月收益中位差为 -5.5%；NFCI_TIGHTENING minus EASING_OR_FLAT 为 -6.3%。

## 5. WALCL / M2：不能直接叫“流动性因果”

WALCL 3M变化的时代相关：-0.240 / +0.106 / -0.352；M2 3M变化：-0.308 / +0.166 / -0.044。

WALCL只是Fed资产负债表规模代理；M2是广义货币存量，而且2020年H.6/Regulation D变化带来定义/构成 caveat。相关关系不能直接翻译成“印钱导致BTC上涨”。

状态样本的跨时代可比性：WALCL = PARTIAL_STATE_COMPARABILITY；M2 = WEAK_STATE_COMPARABILITY。特别是M2在前两个固定时代没有任何3个月收缩/持平状态，因此全样本+4.2%的状态差不能写成跨时代规律。

## 6. Era stability

- 三个时代Pearson符号一致：NASDAQ_RET, DXY_RET, VIX_CHANGE, NFCI_CHANGE
- 三个时代符号发生变化：DFII10_CHANGE_PP, WALCL_3M_PCT, M2SL_3M_PCT

符号稳定也不等于因果稳定，更不等于可预测；符号变化则直接反对把该机制写成跨时代固定规律。

## PandaAI 应该怎样用

展示：当前机制变量、历史同月关联、固定时代差异、36M滚动相关、状态对比、样本支持、数据更新时间和证据边界。

禁止：dominant liquidity score、expected BTC return、Fed-causes-BTC叙事、最佳regime、买卖指令。
