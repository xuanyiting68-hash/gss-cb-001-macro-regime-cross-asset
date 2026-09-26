# Listed REIT Proxy Bridge — 036

## Bridge result

**BRIDGE_PASS_SUPPORTED_PROXY_EXTENSION**

VNQ与VGSIX在完整重叠月的月收益相关性：Pearson 1.000，Spearman 1.000；描述性beta 1.001，intercept -0.00008。

共同Fed事件的12M收益方向一致率 100%，事件12M收益相关 1.000，MDD相关 1.000。

因此如果全部gate通过，可以把VGSIX作为**长期上市房地产/REIT proxy**扩展1996+历史，但不能把2004年以前的VGSIX叫做VNQ。

## 四阶段长历史代理

### FIRST_HIKE｜加息启动

- 12M中位：+2.5%
- 12M MDD中位：11.5%
- MDD低点月中位：M7
- 样本：4 legs / 4 broad episodes
- evidence：LIMITED_PROXY_DESCRIPTIVE

### LAST_HIKE｜最后一次加息

- 12M中位：+18.8%
- 12M MDD中位：4.3%
- MDD低点月中位：M6
- 样本：4 legs / 4 broad episodes
- evidence：LIMITED_PROXY_DESCRIPTIVE

### PAUSE_START｜暂停

- 12M中位：+21.4%
- 12M MDD中位：4.3%
- MDD低点月中位：M5
- 样本：4 legs / 4 broad episodes
- evidence：LIMITED_PROXY_DESCRIPTIVE

### FIRST_CUT｜第一次降息

- 12M中位：-4.8%
- 12M MDD中位：8.3%
- MDD低点月中位：M7
- 样本：4 legs / 4 broad episodes
- evidence：LIMITED_PROXY_DESCRIPTIVE

## 边界

这个桥接解决的是**历史测量长度**，不是预测问题。VGSIX与VNQ费用、份额结构、交易载体和历史基准实现并不完全相同；bridge pass只允许我们研究更长的上市房地产/REIT proxy分布。
