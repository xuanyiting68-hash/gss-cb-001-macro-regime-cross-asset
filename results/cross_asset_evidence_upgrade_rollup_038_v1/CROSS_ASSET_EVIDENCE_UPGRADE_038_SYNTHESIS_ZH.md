# Cross-Asset Evidence Upgrade Rollup — 038

032之后，证据层发生了四个重要变化：

1. **长期美债：真正升级。** TLT本身仍是短历史ETF，但035把VUSTX验证成高质量long-duration Treasury proxy，扩展到6个broad episodes并达到SUPPORTED_PROXY_DESCRIPTIVE。
2. **REIT：测量桥接成功，但证据仍有限。** VGSIX几乎完美复刻VNQ的重叠历史，但只有4个broad episodes，所以仍是LIMITED_PROXY_DESCRIPTIVE；FRESX虽然长期相关很高，却因预注册双桥的一项方向gate失败而不允许升级1987+历史。
3. **住房：从‘房价结果’升级为‘融资→活动→价格’慢时钟。** mortgage peak通常早于activity trough，但activity trough并不总在price trough之前，因此不能写成固定机械传导链。
4. **黄金：从‘阶段表现’升级为‘多机制地图’。** 通胀水平/方向、增长、能源、美元、实际利率、压力时钟彼此并不支持一个稳定单因子故事。

因此当前跨资产内容的证据等级已经更清楚：

- CORE_SUPPORTED：Gold / S&P 500 / Nasdaq / DXY / WTI
- SUPPORTED_PROXY_DESCRIPTIVE：long-duration Treasury via VUSTX
- SUPPORTED_SLOW_MOVING：U.S. national housing
- LIMITED_PROXY_DESCRIPTIVE：listed REIT via VGSIX
- LIMITED_DESCRIPTIVE：Bitcoin and target ETF short-history layers
- DIAGNOSTIC_ONLY：Asia regional equity extensions
- NOT_PROMOTED：FRESX deep-history REIT candidate

下一步最合理的新增研究不是继续找REIT代理，而是转向Bitcoin的真实2014+机制：美元、实际利率、Nasdaq/risk beta、VIX/NFCI、Fed liquidity / balance-sheet proxies，以及这些关系是否随regime变化。
