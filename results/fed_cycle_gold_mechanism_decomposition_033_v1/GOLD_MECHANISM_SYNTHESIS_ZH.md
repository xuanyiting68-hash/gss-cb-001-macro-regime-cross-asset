# Gold Mechanism Decomposition — 033

## 结论先行

当前公共证据最重要的结论不是“找到了黄金唯一驱动因子”，而是相反：**黄金在Fed周期中的机制明显具有状态依赖，常见单因子叙事在这个设计里都不够稳定。**

### 1. Fed阶段本身只能做条件标签

Gold 12M历史中位数：FIRST_HIKE +3.1%、LAST_HIKE -2.8%、PAUSE +4.9%、FIRST_CUT +4.1%。四阶段没有形成一个简单的“越宽松越涨”单调序列。

### 2. “通胀对黄金”必须拆成水平和方向

FIRST_HIKE时，高通胀水平组 Gold 12M中位 -11.8%，低/中通胀组 +6.5%；但通胀RISING组 +3.1%，FALLING_OR_FLAT组 -11.8%。两组结果方向不同，说明“通胀高”和“通胀在上升”不是同一机制。

Erb & Harvey 的长期研究同样提醒：黄金在实用投资期限里并不是一个可靠的机械通胀对冲。因此，更合理的研究问题不是“CPI高不高”，而是通胀状态如何与实际利率、增长、美元和压力共同出现。

### 3. 实际利率：理论重要，但本仓库证据还不够支持单一负相关

月度 REAL_RATE_PROXY 对 Gold forward-6M 的within-cycle beta为 +0.0180/1SD，broad exact p=0.266；实际 DFII10 仅覆盖 3 个周期并被标记 INSUFFICIENT_SUPPORT。

所以当前正确表述是：**真实利率是机制候选，但在本Fed-cycle样本里没有被验证为稳定的反向Gold驱动器。** 这并不证明全市场不存在真实利率关系。Apergis等使用regime-switching模型甚至得到正向关系，进一步说明符号可能依赖状态和模型。

### 4. 美元：仓库结果与常见直觉冲突，必须保留

事件级USD诊断中，USD RISING组 Gold 12M中位 +3.6%，FALLING_OR_FLAT组 -11.8%。月度within-cycle USD beta也是正值 +0.0183/1SD，未调整 broad p=0.03125，但secondary-family FDR没有survivor。

这不能被写成“美元涨所以黄金涨”。更合理的结论是：当前Fed-cycle样本存在明显era/confounding问题，固定负相关不是可以无条件搬用的规则。外部研究经常找到Gold对弱美元的hedge属性，正因为如此，我们的反常结果更应该被当作机制异质性证据，而不是被删除。

### 5. 增长和能源状态提供了更稳定的事件级异质性

STRONG growth组 Gold 12M中位 -3.5%，WEAK组 +4.8%；energy RISING组 +3.6%，FALLING_OR_FLAT组 -2.6%。这些对比LOO方向稳定，但仍然只是事件级描述，不能被解释成独立因果贡献。

### 6. 黄金的压力时钟和美股不一样

FIRST_CUT配对中，Gold低点月中位：Baa样本M5 vs Baa压力峰值M7；VIX样本M4 vs VIX峰值M8。这意味着黄金可能在更广泛金融压力达到最大之前就完成一部分价格调整。

Baur & Lucey / Baur & McDermott 对safe haven的定义也强调：安全港是特定压力条件下的相关性属性，不等于所有压力阶段都持续单边上涨。

## 现在最适合PandaAI展示的机制框架

Gold解释卡应该同时展示：
- Fed phase
- inflation level + direction
- growth state
- real-rate evidence status
- USD evidence status
- energy state
- stress timing
- support/multiplicity/PIT caveat

并明确写：**mechanism map ≠ driver ranking ≠ expected return ≠ trading signal。**
