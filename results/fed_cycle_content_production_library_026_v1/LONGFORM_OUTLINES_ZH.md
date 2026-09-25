# 026 中文长文 / 长视频结构库

以下为证据驱动的结构，不是资产配置或市场预测模板。

## CNT-01-FIRST-CUT-NOT-THE-BOTTOM — 第一次降息之后，市场就已经见底了吗？历史数据不支持这么简单的结论

1. 误区：为什么“第一次降息=底部”过于简化
2. 五类核心资产的FIRST_CUT历史终点收益、MDD、低点月份
3. endpoint return 与 interim path risk 为什么必须分开
4. 017 recovery clock：FIRST_CUT 相对 PAUSE 并没有更快恢复
5. 019/020：为什么简单事前状态无法稳定给出底部时间
6. 2001/2007/2019/2024案例对照
7. 结论边界：历史分布不是当前预测

Claims: CLM-PHASE-DXY-FIRST_CUT|CLM-PHASE-GOLD-FIRST_CUT|CLM-PHASE-NASDAQ-FIRST_CUT|CLM-PHASE-SP500-FIRST_CUT|CLM-PHASE-WTI-FIRST_CUT|CLM-SYNTH-017-FIRSTCUT-RECOVERY|CLM-GUARD-019|CLM-GUARD-020|CLM-CASE-B04|CLM-CASE-B05|CLM-CASE-B06|CLM-CASE-B07
Figures: FIG-PHASE-DXY-FIRST_CUT|FIG-PHASE-GOLD-FIRST_CUT|FIG-PHASE-NASDAQ-FIRST_CUT|FIG-PHASE-SP500-FIRST_CUT|FIG-PHASE-WTI-FIRST_CUT|FIG-RECOVERY-FIRSTCUT-VS-PAUSE|FIG-GUARD-019|FIG-GUARD-020|FIG-CASE-B04|FIG-CASE-B05|FIG-CASE-B06|FIG-CASE-B07
Freshness: STATIC_UNLESS_UPSTREAM_REBUILT
Boundary: 历史研究/教育内容；不构成当前市场预测、资产排序、底部时间判断或投资建议。

## CNT-02-SAME-LABEL-DIFFERENT-PATHS — 同样叫“第一次降息”，为什么历史上的市场路径差这么多？

1. 问题：为什么FIRST_CUT不能作为单一市场状态
2. 1995、2001、2007、2019、2024五个案例并列
3. 股票、黄金、原油在同一案例里的分化
4. 案例内后续冲击与政策标签的区分
5. 为什么不做“最近历史类比排名”
6. 如何用状态变量而不是单一事件标签理解周期
7. 结论边界：案例不是预测模板

Claims: CLM-CASE-B03|CLM-CASE-B04|CLM-CASE-B05|CLM-CASE-B06|CLM-CASE-B07
Figures: FIG-CASE-B04|FIG-CASE-B05|FIG-CASE-B06|FIG-CASE-B07
Freshness: STATIC_UNLESS_UPSTREAM_REBUILT
Boundary: 历史研究/教育内容；不构成当前市场预测、资产排序、底部时间判断或投资建议。

## CNT-03-GOLD-VS-EQUITIES — 降息周期里，黄金和美股会一起走吗？历史上并不总是如此

1. 问题：同一Fed阶段是否意味着跨资产同方向
2. FIRST_CUT历史中位：Gold、SP500、Nasdaq
3. 路径风险：MDD与终点收益分开
4. 2001案例：黄金与科技股分化
5. 2007案例：黄金与美股分化
6. 2019/2024作为补充案例
7. 结论：跨资产比较不能变成简单排名

Claims: CLM-PHASE-GOLD-FIRST_CUT|CLM-PHASE-SP500-FIRST_CUT|CLM-PHASE-NASDAQ-FIRST_CUT|CLM-CASE-B04|CLM-CASE-B05|CLM-CASE-B06|CLM-CASE-B07
Figures: FIG-PHASE-GOLD-FIRST_CUT|FIG-PHASE-SP500-FIRST_CUT|FIG-PHASE-NASDAQ-FIRST_CUT|FIG-CASE-B04|FIG-CASE-B05|FIG-CASE-B06|FIG-CASE-B07
Freshness: STATIC_UNLESS_UPSTREAM_REBUILT
Boundary: 历史研究/教育内容；不构成当前市场预测、资产排序、底部时间判断或投资建议。

## CNT-04-HINDSIGHT-TRAPS — 研究历史周期最容易犯的错：把后来才知道的事，假装成当时已经知道

1. 什么是宏观研究中的 hindsight bias
2. 2001：首降、NBER事后定年、9·11后续冲击
3. 2007：信用压力已可见 vs 衰退日期后来确认
4. 2019：当时官方理由 vs 2020 COVID后续冲击
5. NBER为什么天然具有事后定年属性
6. 如何在内容中标注 CONTEMPORANEOUS / RETROSPECTIVE / POST_ANCHOR
7. 结论：时间戳是证据的一部分

Claims: CLM-CTX-B04_CTX_02|CLM-CTX-B04_CTX_03|CLM-CTX-B05_CTX_03|CLM-CTX-B06_CTX_02|CLM-CTX-B06_CTX_03|CLM-CTX-B07_CTX_02
Figures: FIG-CASE-B04|FIG-CASE-B05|FIG-CASE-B06|FIG-CASE-B07
Freshness: REVERIFY_BEFORE_CURRENT_USE
Boundary: 历史研究/教育内容；不构成当前市场预测、资产排序、底部时间判断或投资建议。

## CNT-05-RECOVERY-CLOCK — 只看一年后涨跌还不够：真正影响持有体验的是“恢复时钟”

1. 为什么 endpoint return 不等于投资体验
2. MDD：持有过程中承受了多大回撤
3. trough month：风险什么时候发生
4. anchor-to-full-recovery：多久回到锚点水平
5. 五个支持资产的FIRST_CUT vs PAUSE比较
6. Gold/SP500/Nasdaq/WTI/DXY案例
7. 结论：三种风险对象不能合成单一收益率判断

Claims: CLM-SYNTH-017-FIRSTCUT-RECOVERY|CLM-PHASE-DXY-FIRST_CUT|CLM-PHASE-GOLD-FIRST_CUT|CLM-PHASE-NASDAQ-FIRST_CUT|CLM-PHASE-SP500-FIRST_CUT|CLM-PHASE-WTI-FIRST_CUT
Figures: FIG-RECOVERY-FIRSTCUT-VS-PAUSE|FIG-PHASE-DXY-FIRST_CUT|FIG-PHASE-GOLD-FIRST_CUT|FIG-PHASE-NASDAQ-FIRST_CUT|FIG-PHASE-SP500-FIRST_CUT|FIG-PHASE-WTI-FIRST_CUT
Freshness: STATIC_UNLESS_UPSTREAM_REBUILT
Boundary: 历史研究/教育内容；不构成当前市场预测、资产排序、底部时间判断或投资建议。

## CNT-06-1987-MULTI-LEG — 为什么1987—1989不能被压成“一次标准加息周期”？

1. B02为什么被定义为COMPOSITE_MULTI_LEG
2. T03_1987 / T04_1987 / T05_1988三个机械子周期
3. Black Monday在时间线中的位置
4. Fed流动性支持属于金融稳定语境
5. 为什么不能人为构造一条合成政策路径
6. 这种边界错误会怎样污染资产统计
7. 结论：周期定义本身就是研究结果的一部分

Claims: CLM-CASE-B02|CLM-CTX-B02_CTX_01|CLM-CTX-B02_CTX_02|CLM-CTX-B02_CTX_03
Figures: FIG-CASE-B02
Freshness: STATIC_SOURCE_AUDIT
Boundary: 历史研究/教育内容；不构成当前市场预测、资产排序、底部时间判断或投资建议。

