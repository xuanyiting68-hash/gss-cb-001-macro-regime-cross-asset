# Content Card — 一个模型“通过 OOS”，为什么我还是不敢说它能交易？
Content ID: FED_CYCLE_GOLD_OOS_CONTENT_010
Evidence: FED-CYCLE-GOLD-OOS-008
Status: **PUBLIC-SAFE / PRELIMINARY OOS / NOT DEPLOYABLE**

## Hook

这次 real-time growth 模型真的通过了我们事前写死的 OOS 门槛。

但我仍然不会说：

“我们找到了黄金预测神器。”

原因就在 OOS 结果的细节里。

## The frozen test

完全按时间顺序：

- 过去 episodes 训练；
- 未来 broad episode 测试；
- 不随机切分；
- 不让未来结果进入训练；
- 不调超参数。

OOS test blocks：

B04 / B05 / B06 / B07。

## It passed the preregistered gate

Real-time IPT model M3 vs Gold+cycle-age B2：

- MSE 降低 **21.27%**
- 赢 **3/4** future episodes
- OOS R² vs historical mean = **+3.38%**

所以按事前规则：

**PRELIMINARY_OOS_CANDIDATE**

## But look at the stronger benchmark

历史均值 B0：

MSE = 0.013865

M3：

MSE = 0.013397

真正改善只有：

**3.38%**

而 MAE：

- B0 = 0.0886
- M3 = 0.0910

M3 反而差约：

**2.74%**

按 episode：

- MSE 只赢历史均值 2/4
- MAE 只赢 1/4

## Why the 21% number can mislead

因为 B2 本身表现很差：

OOS R² ≈ **-22.7%**

所以：

“比一个差 benchmark 好 21%”

和

“这是一个强预测模型”

完全是两件事。

## Real-time data still matters

另一个有价值的结果：

real-time IPT M3 对 current-revised INDPRO D4：

- MSE 好约 **6.8%**
- MAE 好约 **3.5%**
- 3/4 episodes 都更好

这支持一个更稳妥的结论：

**做历史预测研究，真实 vintage 比今天修订后的历史数据更可信。**

## Calibration is still weak

M3 的预测范围：

**-14.7% 到 +12.6%**

真实 next-6M Gold：

**-14.1% 到 +41.5%**

模型明显压缩了大上涨尾部。

## Safe conclusion

OOS 不是一个“通过/失败”按钮。

真正要看的是：

- benchmark 强不强；
- 用 MSE 还是 MAE；
- 每个 episode 是否一致；
- calibration；
- 独立样本有多少。

这次结果最多说明：

**real-time growth 有 preliminary incremental information。**

还远没有到：

**tradable edge。**

## Mandatory disclosure

- only 4 independent OOS broad episodes;
- no OOS significance test;
- no causal identification;
- no model tuning after this result;
- not deployable;
- future validation must use genuinely new data.
