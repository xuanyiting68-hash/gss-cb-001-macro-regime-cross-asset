# Housing Lag Chain — 034

## 核心框架

住房不是股票。常见机制叙事是“融资条件 → 活动量 → 价格”，但034的逐episode结果显示：**这个先后顺序不是跨阶段固定成立的。** 尤其在LAST_HIKE / PAUSE / FIRST_CUT，phase anchor可能发生在mortgage周期高点之后，所以必须看paired ordering和[-12,+24]绝对利率峰值，而不能只比较各变量的阶段中位月份。

## FIRST_HIKE｜加息启动

- 30Y mortgage 12M变化中位：+1.14pp
- 锚点后 mortgage 最大压力月份中位：M12
- [-12,+24]绝对 mortgage rate峰值月中位（post-run diagnostic）：M11
- 配对episode中，绝对mortgage峰值早于/同月activity trough的加权占比：67%
- PERMIT 12M变化 / trough：-3.9% / M13
- HOUST 12M变化 / trough：-0.1% / M15
- New-home sales 12M变化 / trough：-6.7% / M12
- Case-Shiller 12M / 24M：+5.3% / +11.8%
- 24M price decline中位：0.0%

## LAST_HIKE｜最后一次加息

- 30Y mortgage 12M变化中位：-1.01pp
- 锚点后 mortgage 最大压力月份中位：M0
- [-12,+24]绝对 mortgage rate峰值月中位（post-run diagnostic）：M0
- 配对episode中，绝对mortgage峰值早于/同月activity trough的加权占比：100%
- PERMIT 12M变化 / trough：-4.3% / M18
- HOUST 12M变化 / trough：-6.7% / M12
- New-home sales 12M变化 / trough：+5.2% / M2
- Case-Shiller 12M / 24M：+3.5% / +7.3%
- 24M price decline中位：0.4%

## PAUSE_START｜暂停

- 30Y mortgage 12M变化中位：-1.01pp
- 锚点后 mortgage 最大压力月份中位：M0
- [-12,+24]绝对 mortgage rate峰值月中位（post-run diagnostic）：M-1
- 配对episode中，绝对mortgage峰值早于/同月activity trough的加权占比：100%
- PERMIT 12M变化 / trough：-0.3% / M17
- HOUST 12M变化 / trough：-4.4% / M10
- New-home sales 12M变化 / trough：+3.6% / M1
- Case-Shiller 12M / 24M：+3.8% / +5.5%
- 24M price decline中位：0.1%

## FIRST_CUT｜第一次降息

- 30Y mortgage 12M变化中位：-0.53pp
- 锚点后 mortgage 最大压力月份中位：M11
- [-12,+24]绝对 mortgage rate峰值月中位（post-run diagnostic）：M-7
- 配对episode中，绝对mortgage峰值早于/同月activity trough的加权占比：100%
- PERMIT 12M变化 / trough：+3.9% / M11
- HOUST 12M变化 / trough：+0.6% / M10
- New-home sales 12M变化 / trough：+2.8% / M9
- Case-Shiller 12M / 24M：+5.2% / +12.7%
- 24M price decline中位：0.0%

## 为什么价格比活动慢

许可、开工和新房销售是流量/活动指标；Case-Shiller是成交房屋价格的慢变量指数。融资成本变化可以先压缩需求和建设活动，但价格还会受库存、卖方锁定效应、区域结构和交易构成影响。因此“成交冷”与“全国价格还没跌”可以同时发生。

## 两个必须单独看的案例

**B05（2004-07紧缩→住房危机）**：这是整个样本里最重要的负向住房路径之一，不能被相对温和的其他周期平均掉。

**B07（2022-23紧缩）**：融资成本冲击很大，但全国房价路径明显比B05更有韧性，说明利率只是住房结果的一部分条件。

## 投资认知边界

034提供的是历史slow-moving sequencing：融资条件、活动量和价格可能在不同月份达到压力点。它不能回答某个城市、某套房什么时候应该买，也不能把全国中位数直接搬到悉尼或其他地区。
