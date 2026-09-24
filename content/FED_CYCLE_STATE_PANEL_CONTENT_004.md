# Content Card — 为什么“宏观状态看起来很准”，换个设计就失效？
Content ID: FED_CYCLE_STATE_PANEL_CONTENT_004
Evidence: FED-CYCLE-STATE-PANEL-002
Status: **PUBLIC-SAFE / ASSOCIATIONAL / NULL PRIMARY RESULT**

## Hook

“高通胀、强增长、油价上涨，看起来都能把加息后的黄金分成两类。那是不是已经找到 Gold regime 了？”

不是。

## Step 1 — event-level binary split looked strong

在 10 个 FIRST_HIKE legs 上：

- HIGH inflation 的 Gold +12M 中位数明显弱于 LOW/MODERATE；
- STRONG growth 也更弱；
- WTI rising / falling 也有差异。

但这主要是**不同周期之间**的比较。

## Step 2 — stronger within-cycle design

新设计使用：

- 165 个 monthly rows；
- cycle fixed effects；
- 每个 cycle 等权；
- 7 个 broad episode clusters；
- overlapping outcomes 不当 IID；
- exact broad-cluster sign-flip；
- 8 个 frozen primary tests；
- BY-FDR 10%。

结果：

**0/8 survive BY-FDR 10%.**

甚至更宽松的 BH-FDR 10%：

**0/8.**

## What this means

这不能证明宏观状态“没用”。

它说明：

**之前漂亮的二元分组，不足以成为稳定的 Gold regime rule。**

它们可能混合了：

- 年代差异；
- 周期间结构差异；
- 阈值切分；
- 小样本。

## USD is interesting but still not confirmed

USD 6M return 的 secondary diagnostic：

- beta ≈ +1.83pp Gold 6M return / within-cycle SD；
- raw broad-cluster p≈0.0313；
- LOO sign stable。

但把 12 个 secondary diagnostics 一起校正：

- BH survivors = 0；
- BY survivors = 0；
- USD BH q = 0.375。

所以最多只能叫：

**mechanism candidate**。

## Safe conclusion

真正可靠的研究纪律是：

“漂亮分组 ≠ 稳定关系”

“within-cycle association ≠ causal driver”

“raw p-value ≠ FDR-confirmed evidence”

## Mandatory disclosure

- primary family 0/8 FDR survivors;
- no causal identification;
- no OOS forecasting test;
- current-vintage CPI/INDPRO/NFCI are not strict PIT vintages;
- USD is secondary and not multiplicity-confirmed;
- not a trading signal.
