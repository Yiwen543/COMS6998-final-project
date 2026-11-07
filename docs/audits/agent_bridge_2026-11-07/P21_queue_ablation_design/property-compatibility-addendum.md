# P21：独立 property v1 的目标兼容性补充

**静态结论：v1 的合法输入域与旧 joint 41-line / 14-branch 目标不能同时采用。** 这只是待定草案需要收敛的合同问题，不是伪造通过，不阻止向用户展示附条件预算，也不授权执行。

两份新作者文件均匹配协调端给定 SHA：property `a60d56c827fed3da19970505ac90e36b7a988073975eaa94ce956d47aa5cf77e`，role inputs `9b0ebe44ab18af24a5e935e3a878784c39813004b30db9bd1a2e13de974ef76c`。角色声明支持独立 property 作者与未来 Claude golden 作者分离；本次未另审作者完整线程访问史，不将声明扩大为已实现/已测试。

证据：property 草案第14、19行排除 enabled simultaneous read/write。原/变体 RTL 第79–105行中，data-update 的 `2'b11` 专属分支才可到达第94/96行的 line 点和第102行 if/else 两个 branch 点。独立解析两份保存的 `reference-ceiling.dat`，每版均存在这些旧 raw 目标：line94 hits2、line96 hits6，branch102 if/else 各hits1。`enable=0` 时允许 R/W=11 也不会进入这个分支。因此不能保留这些完整目标又禁止所有 enabled R/W=11。没有运行仿真，也没有宣称计算出新域的完整可达上限。

最小验收条件：

1. 先公开采用共同窄 benchmark 合同；若选 `C_eff=3`，明确它是采用假设，不能说 workload L=3 或原 spec 独立证明了容量3。所有 arm/validator/reference/property 使用同一合同和 ABI。
2. 若保留旧完整目标，合同需允许并确定 enabled simultaneous 行为：非空时 dequeue+append、有效占用不变；空时是否保留元素、当拍头部暴露的观察相位和 q 有效域必须明确。不能一处把空 simultaneous 当有效 enqueue，另一处按不变占用评分。相关 flags 也应按共同采用的状态规则解释。由原独立 property 作者只据共同合同/spec/ABI 生成 v2，Claude 另据同样输入写 golden；我不写这两者。
3. 其他优先级/排除操作逐项明示即可。本次**未发现旧完整目标必须使用 clear-disabled 的证据**；clear 分支可由 enable=1 的 clear 激活，不为保险强迫扩大这个范围。空态 q、almost 阈值未采用部分继续不评分/保留 unknown，不能补零假通过。
4. 不暗减旧 raw 分母，不改变目标迎合后验结果。若主动改用排除 simultaneous 的研究域，则必须另行事前登记与该域一致的目标/解释，并保留原始覆盖点与未达；它不再是沿用旧 joint 目标的同合同复测。此处优先建议共同合同/v2 的最小修订，而非增加证明工程。

精确输入 SHA 与8个保存 counter 见 `property-compatibility-evidence.json`。继承本 P21 已实际读取的同版 Hallmark 及 review-finish（`hallmark-usage.json`），本补充未重新读取；仅用其固定证据、定位和最小修订原则。网页流程/scripts/Together 未执行。无新 API/编译/仿真/证明、无 producer/shared 文件更改；待 producer 固定草案后一次增量收敛。
