# Long-Duration Treasury Proxy Bridge — 035

## Bridge result

**BRIDGE_PASS_SUPPORTED_PROXY_EXTENSION**

TLT与VUSTX在完整重叠月的月收益相关性：Pearson 0.991，Spearman 0.993；描述性beta 0.874，intercept +0.00040。

共同Fed事件的12M收益方向一致率 100%，事件12M收益相关 0.995，MDD相关 0.999。

因此可以把VUSTX作为**长期美债duration proxy**扩展1987+历史，但不能把1986–2001的VUSTX叫做TLT。

## 四阶段长历史代理

### FIRST_HIKE｜加息启动

- 12M中位：+1.0%
- 12M MDD中位：10.7%
- MDD低点月中位：M9
- 样本：8 legs / 6 broad episodes
- evidence：SUPPORTED_PROXY_DESCRIPTIVE

### LAST_HIKE｜最后一次加息

- 12M中位：+9.9%
- 12M MDD中位：3.3%
- MDD低点月中位：M11
- 样本：8 legs / 6 broad episodes
- evidence：SUPPORTED_PROXY_DESCRIPTIVE

### PAUSE_START｜暂停

- 12M中位：+15.1%
- 12M MDD中位：3.9%
- MDD低点月中位：M10
- 样本：6 legs / 6 broad episodes
- evidence：SUPPORTED_PROXY_DESCRIPTIVE

### FIRST_CUT｜第一次降息

- 12M中位：+6.0%
- 12M MDD中位：4.5%
- MDD低点月中位：M10
- 样本：8 legs / 6 broad episodes
- evidence：SUPPORTED_PROXY_DESCRIPTIVE

## 边界

这个桥接解决的是**历史测量长度**，不是预测问题。VUSTX与TLT费用、结构、久期和执行载体并不完全相同；bridge pass只允许我们研究更长的long-duration Treasury proxy分布。
