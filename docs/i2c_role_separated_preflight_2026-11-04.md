# OpenTitan I2C：等价关系、独立 checker 与多步事件预检

日期：2026-11-04。结论：**限定范围的 checker/固定 driver 已通过离线检查；本候选尚不进入独立 B 开发试跑。** 9 对非平凡表达式关系证明成立，18 个相关源码计数全部精确映射，但目前可达的两对都在普通 START 流程中出现。三个多步事件可达，并不意味着找到了三个需要多步操作才能命中的等价 guard。没有运行 OpenAI、B、C、A 或 placebo，也没有调整预算。

机器可读依据：[screen.json](../results/i2c_event_candidate_20261104/screen.json)、[逐源码计数 CSV](../results/i2c_event_candidate_20261104/source-counter-comparison.csv)、[复核意见处置](../results/i2c_event_candidate_20261104/review-disposition.json)。这是一份选题及验证基础设施报告，不是 B/C 效果报告。

## 1. 固定设计与角色

原版 OpenTitan `i2c_controller_fsm` 保持不变，upstream commit 为 `0ea5236fe749e70ba18f56ba19c4be982ef46da7`，默认 `FifoDepth=64`。DUT SHA256 为 `0da13b6d8185c7bd6c3949f6c28e073292c1682fd1cc10f83457f6285fd16b1a`。规格依据为该版本公开的 `theory_of_operation.md` 与 `registers.md`；接口环境的约定单独标明，不能冒充官方规格。仓库基线 commit 为 `c71a3e580646d08fb6496c742b7b42b711179b36`，本次工作位于未提交工作区。

- Claude Opus 5.5：通过无工具、无会话持久化的 Claude Code 调用编写纯 Python 规格 checker；后续只应用 Claude 返回的修订/精确补丁。
- GPT/Codex 工程角色：固定 SystemVerilog 总线 driver、JSON schema、私有校准输入、独立手工控制轨迹、类型/源映射和计量集成。这里的私有校准不是 OpenAI live 刺激试跑。
- 新的 Claude 会话：只读复核 checker、driver、控制结果及证据边界；没有执行仿真或形式证明，不能把其意见称作独立执行验证。
- 确定性工具：Verilator/Icarus 执行全部刺激后再检查；Yosys/Z3/egg 提供组合语义证据；哈希与固定计数负责计量。

作者 v1 只看到公开规格和接口。v2 修复反馈包含旧 checker、独立复核意见及少量失败轨迹周期标签，但没有 DUT 实现、完整校准序列、guard 目标或 B/C 结果；v3 使用规格、原代码及独立控制生成器。这是角色分离，不是所有修订反馈均完全盲化。完整提示词、响应和原始 usage 均保留。

## 2. 验证 9 对关系，而不把源码覆盖合并

沿用 Slang typed AST、完整 if/case 优先级 guard、连续赋值与受限组合 SSA；新增独立 Yosys-cell 编码支持 `$add`、`$gt`、`$bmux`。动态索引只支持本固定 RTL 的 `[7:0] fmt_byte_i[bit_index]`，3 位无符号索引范围可覆盖且不会越界；不扩展为任意动态索引支持。

结果如下：

- 35 个组合定义对独立 Yosys-cell 表达式的差异查询全部 UNSAT，证明环境本身 SAT；19 个 pmux 的多选择冲突查询全部 UNSAT。
- 同上下文的 23,490 对查询：166 UNSAT、23,324 SAT、0 unknown，其中 9 对源表达式不同。
- 六条既有 Boolean 规则及九条 Z3 证明的 ground rule 输入真实 Rust `egg`；上限 20 次迭代、20,000 nodes、5 秒，保存合并前后 e-class 和解释。不是手工 union，也不是声称 egg 独自发现了关系。
- 每个跨源合并均回查 QF_BV 证明；保留 FF 当前值、posedge 时钟、低有效异步复位的上下文，不把同步/异步复位改写成相同行为。
- 268 个谓词目标中 218 个精确绑定 Verilator 源文件/行/列/类型/极性，50 个 unresolved。9 对目标的 18 个计数均映射成功。

| 对 | 源码行 | 当前校准结果 |
| --- | --- | --- |
| 1 | 127 ↔ 673 | seed 为零，普通 START 即命中 |
| 2 | 128 ↔ 681 | seed 为零，普通 START 即命中 |
| 3 | 390 ↔ 670 | 未命中，不能据此宣称不可达 |
| 4 | 433 ↔ 714 | 未命中，总线不稳定相关 |
| 5 | 459 ↔ 754 | 未命中，总线不稳定相关 |
| 6 | 482 ↔ 793 | 未命中，读路径及不稳定相关 |
| 7 | 491 ↔ 808 | 未命中，读路径相关 |
| 8 | 518 ↔ 833 | 未命中，读 ACK 路径相关 |
| 9 | 546 ↔ 877 | 未命中，STOP 干扰路径相关 |

以上只证明**二值组合语义**。不是四态等价证明、完整顺序等价证明或可达性证明。AST 与 Yosys-cell 编码仍共享 Slang 前端，独立性不等于两个完全独立的编译器。源码不同的计数一直分别保留；相同谓词不代表每个位置都执行过。详见 [certified-guards.json](../results/i2c_event_candidate_20261104/certified-guards.json)。

## 3. 固定 JSON 总线环境与 checker 控制

[固定环境](../examples/heldout_i2c_controller/verif/tb_i2c_fixed.sv)使用开漏 wired-AND、一个输出 launch register、两级输入同步器、64 项 FMT FIFO、只观察物理 SCL/SDA 的被动 ACK target。没有读取 DUT 内部 state/tcount。JSON 只允许有界整数的入队 byte/START/STOP/NAKOK、enable/reset、FIFO flush、事件 clear、target ACK、外部 SCL 拉伸和 NACK timeout 设置。READB/RCONT 固定零，接口没有伪造 RX ready。

固定 timing 为 THIGH=4、TLOW=6、T_R=T_F=1、THD_DAT=2、START/STOP setup/hold=4（core-cycle 单位）。THIGH/TLOW 满足 TIMING0 的 >2 要求；这不是模拟电气时序或 I2C 速率等级认证。首阶段仅写模式、单控制器。读模式、仲裁、精确 timeout 延迟、THIGH 时序、总线监视器和完整寄存器 IP 未验证；对应原始覆盖计数仍保留在分母。

每个周期保存输入和 pre/post 公开观察值。FMT 的 ready 表示处理后的 pop，不能当作开始发射字节时的 accept。检查发生在完整批次仿真结束后，因此功能失败不会阻止覆盖写出。非法 flush 或 SCL-high 时开始 stretch 被记为 environment error，不能获得合格事件信用。

Claude v1 合法字节误报；v2 修好队列和 STOP 解码，但首 NACK 字节的错误会被事件窗口漏掉，且 timeout 发生顺序不严格。v3 的精确补丁解决这些问题，保留全部旧版和失败证据。

最终验证包括：12 个作者自测；独立普通写及三个多步事件正例；两个字节/reset 负例；五个事件窗口字节故障、三个截断控制；提前 timeout STOP、缺少 NACK 状态证据，以及请求 stretch 却未真正延长 SCL 的控制。提前 STOP 被拒绝，缺少状态保持 pending，截断不算完成。相同缺陷导致的重复报错不被计为新缺陷类型。控制并不穷尽全部 checker 缺陷。

最终只读复核认可限定离线用途。其要求的 checker-evaluation 哈希绑定、environment error 门槛、整条轨迹无 failure/assumption/unresolved 才计事件，均已实施。[冻结清单](../examples/heldout_i2c_controller/freeze.json)只冻结离线验证边界，`formal_B_eligible=false`；没有冻结正式 A/B/C 目标。

## 4. 可达性和原始覆盖结果

三个校准批次各为 shared seed 8 周期 + 384 周期，Verilator/Icarus 的公开轨迹完全一致。

| 多步事件 | checker 观察到的窗口（从零计周期，含 seed） | 结果 |
| --- | --- | --- |
| 实际拉伸后恢复并完成字节/STOP | 26–157 | scoped pass |
| 未预期 NACK、软件处理、repeated START 后完成 | 122–289 | scoped pass |
| NACK timeout、自动 STOP、清事件后重新完成 | 122–324 | scoped pass |

这里使用私有校准刺激提供**仿真可达性见证**，不是形式 cover 证明。参考正例由公共接口规范手工构造，未从 RTL 输出导出。

| 批次 | Line | Branch | Expression | Toggle |
| --- | ---: | ---: | ---: | ---: |
| seed | 31/132 | 20/116 | 45/209 | 76/820 |
| 普通单字节写 | 77/132 | 68/116 | 110/209 | 175/820 |
| stretch 恢复 | 79/132 | 68/116 | 111/209 | 181/820 |
| NACK restart | 80/132 | 75/116 | 120/209 | 185/820 |
| NACK timeout recovery | 79/132 | 77/116 | 119/209 | 203/820 |

这是 Verilator 5.050 的工具定义原始 DUT counters，含初始化/reset，排除 testbench。总分母 1,277；表中分子是 hits>0 的点数，不是命中总次数。Coverage hit 值也不能直接解释成执行的 core cycles。每个批次从新进程开始，没有选择性删除未覆盖/未证明不可达的点。

36 个 source-distinct 组合等价组中，18 组在校准中达到至少两个 seed-zero 源计数；**这 18 组全部已能在普通写中命中**。其中非平凡的两组也是普通 START。相对于普通写，没有一组新增的多步事件专属等价源计数。

因此，当前缺少的是“可达、多步、源位置重复且语义真正可归并的目标交集”，而不只是更大的代码量。额外 branch 确实被 NACK 场景覆盖，但它们不自动成为成组的等价 guard。未作时间相关来源绑定的 source group 也不能用 temporal event 成功来替代。

## 5. 预算、成本和可复现性

B 预算维持原计划：3 次独立重复 × 6 轮 × 每轮最多 64 新周期；seed 8 周期，input cap 32,000、output cap 16,384、timeout 120 秒、retry 1，计划模型 `gpt-6.1-sol`。本轮未调用该模型，没有独立 B 结果，更没有 C 效果估计。

开发与控制成本单独核算：5 次 driver 编译、23 次仿真、6,136 个执行周期（包含旧版、两个模拟器、重放和最终 200 周期集成 smoke）。编译约 27.76 秒，仿真约 1.08 秒。Claude 共 7 次调用尝试：6 次完成，1 次因 prompt 过长被拒绝，错误响应明确报告零用量/零费用；CLI 报告总成本 $2.679376。Claude 调用墙钟合计约 412.55 秒。这些不是每个 B/C trial 的成本，也不包括工程思考/等待用户时间。

原始 input、cache creation、cache read、output 字段均保存；对 Anthropic 汇总输入时这些输入类别分别计入，thinking 是 output 的子集，不能再次相加。正式 Token ROI 尚不适用，因为本轮没有实验刺激模型。

复现不需要 API key：

```sh
# 重新抽取、运行全部 pair query、独立网表校验及 egg/source join；output 必须是新目录。
.venv/bin/python scripts/run_i2c_semantic_preflight.py \
  --output build/i2c-semantic-reproduce-new \
  --calibration results/i2c_event_candidate_20261104/driver-v2

# 固定 driver 执行后调用已冻结的 Claude checker；失败不隐藏 coverage。
.venv/bin/python scripts/run_i2c_checked.py \
  --actions results/i2c_event_candidate_20261104/driver-v2/write.actions.json \
  --output build/i2c-checked-replay-new

.venv/bin/python -m unittest discover -s tests -p 'test_i2c_pipeline.py' -v
.venv/bin/python -m unittest discover -s tests -p 'test_spi_semantic_v2.py' -v
```

本轮 10 个新增检查及 7 个复用语义检查通过，包括带符号/不同位宽的 128 个算术比较样本、bmux 所有选择、刻意破坏网表的负例、输入边界、旧 evaluation 拒绝、哈希冻结、两模拟器一致与复核包无损还原。独立重新跑前端/证明流水线得到同样的 9 对和 218/50 映射结果。

工具版本与每个调用/编译/仿真、DUT/checker/driver 哈希在 screen.json 和 freeze.json 中。临时 Anthropic key 已删除；没有 push 或修改上游 DUT。

## 6. 下一步应做什么

先补 READB/read-ACK 的公开规格边界、被动读 target 及 Claude 独立 checker，使 491↔808 等读路径关系能够接受合法输入下的可达性筛选；不能把当前未命中直接说成不可达。同时检查读后的 restart、连续读及状态切换是否带来多组晚触发的重复完整 guard。仲裁/异常总线跳变需要独立的对手控制器与 checker，不能任意拉线来制造“有利目标”。

如果扩展后仍只有普通读写即可达到的组，应保留 I2C 作为语义/检错能力对照，筛选另一颗自然 IP。只有“独立 checker/可达性/多步目标来源绑定”同时成立，才使用原预算做独立 B 试跑；仅在 B 也通过既定接受门槛后冻结 A/B/C/placebo。没有理由在这里为了 C 的收益缩短预算。
