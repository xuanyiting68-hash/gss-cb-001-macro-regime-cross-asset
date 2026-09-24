# Content Card — 你回看历史数据时，可能看到了“当时根本不存在的数据”
Content ID: FED_CYCLE_VINTAGE_CONTENT_009
Evidence: FED-CYCLE-VINTAGE-AUDIT-007
Status: **PUBLIC-SAFE / REAL-TIME REVISION AUDIT / NOT A TRADING SIGNAL**

## Hook

很多宏观回测有一个隐蔽问题：

**你今天下载到的历史数据，不一定是当时市场真正看到的数据。**

这叫 data revision / real-time vintage problem。

## We tested it on industrial production

使用 Philadelphia Fed RTDSM 的真实历史 vintage：

- 10 个 FIRST_HIKE events 全覆盖；
- 165 个 monthly panel rows 全覆盖；
- 每个月只允许使用前一个月或更早的 vintage；
- growth threshold 仍然固定在 2%，没有调参。

## One event actually changes state

2022 第一次加息前：

今天修订后的 INDPRO YoY：

**+1.32% -> WEAK**

当时可获得的 real-time IPT：

**+4.12% -> STRONG**

也就是说：

**用今天的历史数据回看 2022，你甚至可能把当时的 growth regime 分类错。**

## Revisions are not tiny

10 个 FIRST_HIKE events：

- median absolute YoY revision gap ≈ **2.22 percentage points**
- max ≈ **4.04 pp**

165个月面板：

- current vs real-time correlation ≈ **0.90**
- median absolute gap ≈ **1.03 pp**
- P90 ≈ **2.74 pp**

高相关不代表 revision 可以忽略。

## What happened to the Gold relationship?

Same 165 rows, same estimator:

Current-vintage growth:

- Gold next-6M beta ≈ **-1.27pp per growth SD**
- broad exact p = **0.125**

Real-time growth:

- beta ≈ **-1.96pp**
- broad exact p = **0.015625**

而且 7 个 broad episodes 的 score 全部同号为负。

删掉 2022 后：

- beta 仍约 **-1.49pp**
- raw broad p = **0.03125**

## But do not overclaim

这不等于：

“工业生产可以预测黄金。”

原因：

- 这里只有 7 个 broad episodes；
- p=0.015625 很大程度来自 7/7 cluster sign unanimity；
- robustness restrictions 是看到 full-sample 结果以后做的；
- 没有 time-ordered OOS；
- 没有因果识别。

## Another important finding

事件层的 +12M Gold return 强弱增长差异方向仍保留：

- current labels: STRONG-WEAK ≈ **-8.31pp**
- real-time labels: ≈ **-9.12pp**

但 24M MDD 差异：

- current: **+2.67pp**
- real-time: **-0.47pp**

所以 endpoint relation 比 drawdown relation 更 revision-robust。

## Safe conclusion

做真正严谨的历史宏观研究，必须区分：

`CURRENT REVISED HISTORY`

和

`WHAT THE MARKET KNEW THEN`

PandaAI 后续的 historical replay 也应该保留这个 distinction。

## Mandatory disclosure

- association, not causation;
- no new confirmatory family;
- no OOS forecast;
- no trading rule;
- CPIAUCNS was not replaced by seasonally adjusted PCPI.
