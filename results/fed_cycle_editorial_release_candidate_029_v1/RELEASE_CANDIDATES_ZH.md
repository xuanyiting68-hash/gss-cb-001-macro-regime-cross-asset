# 029 Editorial Release Candidates — RC1

## RC-CNT-01-FIRST-CUT-NOT-THE-BOTTOM

**主标题：** 第一次降息之后，市场就已经见底了吗？历史数据不支持这么简单的结论

**Hook A（RC1）：** 第一次降息 = 市场见底？把历史路径拆开看，结论没有这么简单。

**Hook B：** 首降后标普500历史+12个月中位数是+11.0%，但同期最大回撤中位数仍有14.0%。

**Hook C：** 降息是一个政策阶段标签，不是市场底部的时间戳。

**Figures：** FIG-PHASE-DXY-FIRST_CUT|FIG-PHASE-GOLD-FIRST_CUT|FIG-PHASE-NASDAQ-FIRST_CUT|FIG-PHASE-SP500-FIRST_CUT|FIG-PHASE-WTI-FIRST_CUT|FIG-RECOVERY-FIRSTCUT-VS-PAUSE|FIG-GUARD-019|FIG-GUARD-020|FIG-CASE-B04|FIG-CASE-B05|FIG-CASE-B06|FIG-CASE-B07

**Freshness：** STATIC_UNLESS_UPSTREAM_REBUILT

**Release gate：** PREFLIGHT_REQUIRED

**Immutable evidence SHA256：** 0e1c9b5111a635e9a11b4248bbb29165b8ae579e4b76cb20e09f2b710880278f

**边界：** 历史研究/教育内容；不构成当前市场预测、资产排序、底部时间判断或投资建议。

## RC-CNT-02-SAME-LABEL-DIFFERENT-PATHS

**主标题：** 同样叫“第一次降息”，为什么历史上的市场路径差这么多？

**Hook A（RC1）：** 同一个FIRST_CUT标签，2001、2007、2019、2024走出了完全不同的资产路径。

**Hook B：** 2001首降后，纳指+12个月是-25.6%；2024案例里则是+28.5%。

**Hook C：** 真正值得研究的不是“降息”两个字，而是降息发生在什么宏观和金融环境里。

**Figures：** FIG-CASE-B04|FIG-CASE-B05|FIG-CASE-B06|FIG-CASE-B07|FIG-CASE-B03

**Freshness：** STATIC_UNLESS_UPSTREAM_REBUILT

**Release gate：** PREFLIGHT_REQUIRED

**Immutable evidence SHA256：** 48a659bb900be19707165bf8f6802e5ce31c514b59a9eb2ee050ccd89868a191

**边界：** 历史研究/教育内容；不构成当前市场预测、资产排序、底部时间判断或投资建议。

## RC-CNT-03-GOLD-VS-EQUITIES

**主标题：** 降息周期里，黄金和美股会一起走吗？历史上并不总是如此

**Hook A（RC1）：** 首降后，黄金历史+12个月中位数+4.1%，标普500是+11.0%，但它们的路径风险完全不同。

**Hook B：** 2001案例：黄金+4.1%，纳指却是-25.6%。

**Hook C：** 同一个Fed阶段，并不会自动给所有资产排出统一顺序。

**Figures：** FIG-PHASE-GOLD-FIRST_CUT|FIG-PHASE-SP500-FIRST_CUT|FIG-PHASE-NASDAQ-FIRST_CUT|FIG-CASE-B04|FIG-CASE-B05|FIG-CASE-B06|FIG-CASE-B07

**Freshness：** STATIC_UNLESS_UPSTREAM_REBUILT

**Release gate：** PREFLIGHT_REQUIRED

**Immutable evidence SHA256：** df1257d58a95001910673822cbc250b952f6af9d41d85553bfc0965b90ca988c

**边界：** 历史研究/教育内容；不构成当前市场预测、资产排序、底部时间判断或投资建议。

## RC-CNT-04-HINDSIGHT-TRAPS

**主标题：** 研究历史周期最容易犯的错：把后来才知道的事，假装成当时已经知道

**Hook A（RC1）：** 2001年1月第一次降息时，后来被NBER认定的衰退起点还没有发生，更没有被官方确认。

**Hook B：** 9·11不能被倒灌进2001年1月的政策理由，COVID也不能被倒灌进2019年7月。

**Hook C：** 做周期研究，最重要的不只是数据，而是时间戳：当时到底知道什么？

**Figures：** FIG-CASE-B04|FIG-CASE-B05|FIG-CASE-B06|FIG-CASE-B07|FIG-CTX-B04_CTX_02|FIG-CTX-B04_CTX_03|FIG-CTX-B05_CTX_03|FIG-CTX-B06_CTX_02|FIG-CTX-B06_CTX_03

**Freshness：** REVERIFY_BEFORE_CURRENT_USE

**Release gate：** REVERIFY_REQUIRED_BEFORE_RELEASE

**Immutable evidence SHA256：** b34f4d4cf21884207252a93890765c998192bbc46d44c3dd79bad5a4273663a8

**边界：** 历史研究/教育内容；不构成当前市场预测、资产排序、底部时间判断或投资建议。

## RC-CNT-05-RECOVERY-CLOCK

**主标题：** 只看一年后涨跌还不够：真正影响持有体验的是“恢复时钟”

**Hook A（RC1）：** 一年后是正收益，不代表中间没有经历很深的回撤。

**Hook B：** 首降之后，五个完整支持资产的完全恢复速度，相对暂停阶段没有一个更快。

**Hook C：** 黄金首降后的+12个月中位数是+4.1%，但从锚点到完全恢复的历史中位时间是22个月。

**Figures：** FIG-RECOVERY-FIRSTCUT-VS-PAUSE|FIG-PHASE-DXY-FIRST_CUT|FIG-PHASE-GOLD-FIRST_CUT|FIG-PHASE-NASDAQ-FIRST_CUT|FIG-PHASE-SP500-FIRST_CUT|FIG-PHASE-WTI-FIRST_CUT

**Freshness：** STATIC_UNLESS_UPSTREAM_REBUILT

**Release gate：** PREFLIGHT_REQUIRED

**Immutable evidence SHA256：** 2e020286b2f1b599b2958aa8868d3e074d912aa7e514b97e93bd3f5692657b43

**边界：** 历史研究/教育内容；不构成当前市场预测、资产排序、底部时间判断或投资建议。

## RC-CNT-06-1987-MULTI-LEG

**主标题：** 为什么1987—1989不能被压成“一次标准加息周期”？

**Hook A（RC1）：** 1987—1989不是一条干净的“加息—暂停—降息”直线，而是三个机械子周期。

**Hook B：** 如果把1987股灾前后全部压成一个周期，你会直接破坏政策时间线。

**Hook C：** 历史周期研究的第一步，有时不是算收益，而是先把周期边界划对。

**Figures：** FIG-CASE-B02

**Freshness：** STATIC_SOURCE_AUDIT

**Release gate：** PREFLIGHT_REQUIRED

**Immutable evidence SHA256：** 60c9c9ad35eb0858096412ff852c44442400bbbf754fc97104f5c9d0d4183ad9

**边界：** 历史研究/教育内容；不构成当前市场预测、资产排序、底部时间判断或投资建议。

