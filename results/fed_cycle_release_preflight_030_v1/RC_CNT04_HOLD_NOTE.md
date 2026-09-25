# RC-CNT-04 发布 HOLD 说明

Assessment date: 2026-09-25

Status: **HOLD_REVERIFY**

内部证据/QC：PASS。

计划主发布：2026-10-01。

HOLD 原因：该包包含 CLM-CTX-B07_CTX_02，其 freshness rule 为 REVERIFY_BEFORE_CURRENT_USE。该 claim 描述的是 NBER 页面截至审计日的最新官方 business-cycle chronology，因此不能把 2026-09-25 的审计状态永久当作 2026-10-01 的当前状态。

发布前动作：
1. 重新核验 NBER Business Cycle Dating 官方页面；
2. 确认该 current-chronology claim 的表述仍准确；
3. 如状态未变，记录新的 reverify timestamp 后解除 HOLD；
4. 如官方 chronology 已变化，必须更新上游 claim/context 版本，不能只在文案层偷偷修改。

不需要重验/改写的历史事实：
- 2001 NBER recession dating 是 retrospective；
- 9/11 是 post-anchor shock；
- 2007 recession dating 是 retrospective；
- 2020 recession dating 是 retrospective；
- COVID 是 post-anchor shock。

本文件不声称 external reverify 已完成，也不授权提前发布。
