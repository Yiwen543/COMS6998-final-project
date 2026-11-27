# AXI Frame Length Adjuster · Egg 的规则覆盖与可证明报警诊断

本轮把研究重点从验证耗时转到两个具体环节：**如何稳定获得等价证明，以及如何让 egg 自己生成带证明的报警解释。** 五条实际规格产生了 18 个诊断子句、67 个经过独立核验的具名改写步骤。它们在完整原版 RTL 上通过新的形式验证，并在原有故障及附加灵敏度对照的 45,450 次性质采样中保持原始报警不变。但普通 DNF 基线也能产生同样完整且最短的报警解释，本轮没有观察到额外的诊断质量收益。

[固定实验协议](egg_frame_diagnostic_protocol.md) · [真实 API 上一轮结果](egg_frame_live_results.md) · [原始规格与验证边界](egg_frame_results.md)

## 1. 规则覆盖：为什么不能只看 egg 是否饱和？

在实际在线生成公式、五条错误 seed、冻结的 18 个合成结构变体和六个唯一的预设修订对上，共重新运行 34 个唯一公式对、102 个通用 egg 任务。每对公式均独立进行完整位宽 Z3 等价判定。三个 egg 配置和强普通基线共用相同的抽象、同一组已证实的原子等价/互补替换，之后在命题层比较。输入中的包含关系、括号、交换次序、德摩根和可用的分配位置均事前固定；合成式不算新增真实模型样本。

| 输入组 | 独立 oracle 等价数 | 普通结构 + 命题 XOR | 旧 6 条 | + and/or 结合律 | + 交换律、and/or 分配律 |
|---|---:|---:|---:|---:|---:|
| 真实模型最终公式 | 5/5 | 5/5 | 3/5 | **5/5** | 5/5 |
| 在线实验使用的预设错误 seed | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 |
| 合成等价结构变体 | 18/18 | 18/18 | 5/18 | 10/18 | 18/18 |
| 预设修订对 | 6/6 | 6/6 | 6/6 | 6/6 | 6/6 |
| 等价总数 | 29 | 29 | 14 | 21 | 29 |

上述计数是结构恒等或具名改写证书能够独立核验的数目，不等同于全图饱和。旧六条和八条配置的全部 34 项任务均饱和；最宽的十二条配置全部到达限制（31 次节点限制、3 次轮次限制），严格按旧的仅饱和接受规则算，最宽配置为 **0/29**。在已找到的同域等价证书全部独立复核后，仍可以认定这 29 对已证明等价，却不能认定图已饱和或没有找到证明的两式不等价。没有一种配置对五个已知错误 seed 产生错误证书。普通方法独立证明了全部 29 对。

真实最终公式的三个旧成功是结构恒等；新增两项由合取结合律产生 10 个已核对的步骤。宽规则扩大了等价搜索空间，存在反复扩张，不能简单将规则越多等同于验证质量越好。历史在线 indexed 引擎的 3/5 仍然保留；新的通用引擎是在认证原子商集上的离线比较，并不是对历史 LLM 调用重跑。

[各组结果](../results/milestone3/frame-proof-coverage/summary.json) · [具体输入、规则与预算](../results/milestone3/frame-proof-coverage/protocol.json) · [完整独立证据](../results/milestone3/frame-proof-coverage/cases.jsonl.gz)

## 2. 主动生成可证明的诊断断言

此前 egg 收到两个式子，仅判断已给出的写法是否等价。这次新 Rust 引擎只接收**一个已有规格**以及冻结规则，目标分解没有预先插入图内。它在真实 egg 饱和图的等价类中搜索析取范式（DNF），按子句数、文字出现次数、抽象 AST 节点数顺序提取。每个子句表示一个足以触发原始报警的条件；多个子句可以同时成立。常量、字面量和子句的语法在引擎与独立检查器分别核对。

所有生成式均独立回放具名改写，将比较原子还原成原始位宽引脚和运算。Z3 验证完整式 XOR 不可满足；18 个子句均独立验证为充分报警条件，归一化后的子句析取也经 Z3 验证与原始提取式一致。没有把图合并本身作为最终规格判定。

| 性质 | egg 子句数 | 普通 DNF 子句数 | 两种方法的文字总出现数 | egg 已核验步骤 | egg 最终节点数 |
|---|---:|---:|---:|---:|---:|
| data_hold | 4 | 4 | 26 | 19 | 103 |
| header_hold | 7 | 7 | 46 | 36 | 225 |
| pad_flag | 2 | 2 | 8 | 3 | 22 |
| truncate_flag | 2 | 2 | 8 | 3 | 22 |
| clamped_length | 3 | 3 | 13 | 6 | 41 |
| **合计** | **18** | **18** | **101** | **67** | — |

五个图均正常饱和；上述提取目标是在有限搜索图内的最优语法成本，而不是所有逻辑公式全局最优性的承诺。强普通基线直接 NNF 分配与吸收，独立穷举真值表对五条源式共 5,152 个布尔赋值验证其 DNF 正确。区别在于 egg 的改写步骤是可以审阅、逐步重放的证书，而普通算法本身也可进行可靠的整体等价检查。

[生成输入、输出、逐步证明和 Z3 查询](../results/milestone3/frame-diagnostic/generated.json)

## 3. 真正 RTL 的报警诊断

原有 21 条真实 Icarus 轨迹只触发三种局部性质，因此新增三个**端口灵敏度对照**，不是发现三个新 RTL 缺陷：D01 阻塞时使可见数据变化，D02 在原长恰好 4 时让 pad 标志反转，D03 原长大于 8 时将报告长度改为 7。三项均在原先固定顶层包装的临时副本注入，内部三个 RTL 模块保持固定。重新编译了原版及三个对照，共 12 次新回放；原版与旧轨迹完全相同并在合并时去重。第二轮独立重放也成功复现。

| 真正轨迹样例 | 原有参考局部报警次数 | egg 解释成功 | 普通解释成功 |
|---|---:|---:|---:|
| 原版 | 0 | 0 | 0 |
| F01、F03、F06 | 0 | 0 | 0 |
| F02 | 4 | 4 | 4 |
| F04 | 3 | 3 | 3 |
| F05 | 16 | 16 | 16 |
| D01 | 126 | 126 | 126 |
| D02 | 23 | 23 | 23 |
| D03 | 48 | 48 | 48 |
| **总计** | **220** | **220** | **220** |

30 条不重复轨迹、9,120 个周期记录，扣除每条初始 PRE 后为 9,090 个相邻采样，五条性质共 **45,450** 次采样比较。对完整提取式，包括有未知引脚时的可能二态补全，两个方法均完全匹配原始完整位宽谓词、零不一致、零无法判定的性质。共有 247 个已知为真的子句（同一采样可触发多个子句），220 个报警分别都能选择一个最短充分子句：78 个需要 4 个已知文字，142 个需要 6 个。四个带未知抽象原子的 F05 报警仍有已知充分子句。最短由另一个独立穷举算法确认：在每条源式至多 12 个抽象原子的独立 Boolean 取值空间内，对所有符合观测的补全检查充分性。这个域不利用原子间位宽依赖，因此不能声称对所有可能的位宽诊断表达式取得全局最优。

例如 F05 的背压轨迹第 16 个周期，前一拍 header 有效且 `h_ready=0`，两拍都未 reset，`h_original_length` 从 3 变成 4，同时 `h_pad` 从 1 变成 0。抽取的子句明确指出两个保持条件遭到破坏。D03 的背压第 43 周期，`h_original_length=9`、`h_length=7`、`h_valid=1`、`rst=0`，足以解释较长帧应截到 8、却报告 7 的报警。它们解释的是**哪条规格条件失败**，不是自动定位导致失败的 RTL 源码。

以前六个真实内部变异的局部检测能力仍是 3/6，独立事务 checker 仍为 6/6；197 个附加端口报警不能拿来提高这个检出比例。诊断分解没有增加原五项的语义覆盖，也不能替代检查完整帧数据、结束标志和复位完成条件的事务验证。

[端口对照计划、原生结果和复现](../results/milestone3/frame-diagnostic-faults/README.md) · [全部逐性质诊断分数和实例](../results/milestone3/frame-diagnostic/physical-score.json)

## 4. Formal verification 不是只证明 guard

从本轮实际 egg 提取出的五条完整 DNF 重新生成 SV 断言（独立类型解析和渲染），在原版 `frame_task` 的固定完整 RTL、固定形式环境/复位/四个输入假设上重新执行 Yosys SAT 的 24 状态有界检查，五项全部通过；`data_hold` 和 `header_hold` 两项另外通过 Z3 的 3 状态基例及时序归纳。其他三项仍只报告有界结论。形式验证用的是实际生成式，不是用历史原始规格的结果替代。

[新断言与工具结果](../results/milestone3/frame-diagnostic/formal/summary.json) · [实际生成的 SV](../results/milestone3/frame-diagnostic/formal/frame_assertions.svh) · [24 状态 SAT 日志](../results/milestone3/frame-diagnostic/formal/candidate-sat.log.gz) · [两项归纳日志](../results/milestone3/frame-diagnostic/formal/candidate-holds.log)

## 5. 追加：目标证明成功即停止

由于初次宽规则实验实际观察到全图爆炸，增加一个独立对照：同一宽规则、同一 34 个公式对、同一二进制与资源预算，只改变 `--stop-on-merge` 开关。新模式只接受两个目标、明确相同的事件域；合并后结束搜索并输出真实的 `TargetsMerged` 停止原因。仍由 Python 独立重放证明。旧默认模式和实时 indexed 引擎保持原行为。

| 宽规则配置 | 默认继续饱和 | 目标合并后停止 |
|---|---:|---:|
| 等价目标有有效证书 | 29/29 | 29/29 |
| 不等价目标的错误证书 | 0/5 | 0/5 |
| 明确完成目标证明而停止 | 0 | 29 |
| 达到节点或迭代限制 | 34 | 5 |
| 等价组进程壁钟时间中位数 | 42.95 ms | 1.93 ms |
| 等价组最终 e-node 数中位数 | 26,864 | 44 |

29 个正例中 28 个进程实测更快；以上每对只观测一次，包含短进程启动和 proof JSON 输出，不包括共享的位宽认证、Python 检查、RTL 仿真和 LLM 调用，不能外推为完整验证速度或统计显著收益。五个负例仍到达限制，由独立位宽 oracle 证明不等价；egg 的未找到证明不能当作反例。该追加对照的主要作用是让只关心一个等价性问题的验证环节在证书完成时明确退出，而不受无关的全图饱和目标限制。

[完整规则实验和专项命令](egg_frame_proof_coverage.md) · [目标停止逐组结果](../results/milestone3/frame-proof-goal-stop/summary.json) · [实际两模式证明](../results/milestone3/frame-proof-goal-stop/cases.jsonl.gz)

## 6. 环境、脚本、复现

实际运行环境：Linux，Python 3.12.14，Rust/Cargo 1.90.0，锁定 egg 0.11.0，Python Z3 与 CLI Z3 4.16.0，Icarus 12.0，Yosys 0.52。以下步骤可在之前成功运行真实 API 的 MacBook 原仓库中执行。沿用已加载 OSS CAD Suite 的终端（`yosys`、`yosys-smtbmc`、`z3`、`iverilog`、`vvp` 可用）及 Homebrew Python；Linux 使用相同版本或等价可用工具。此次全部离线，不需 API key。输出目录用新的路径，避免覆盖已归档结果。

```bash
# 在仓库根目录。已有 Python 环境可直接复用 FPY。
"$(brew --prefix python@3.12)/bin/python3.12" -m venv "$HOME/rtl-tools/frame-venv"
FPY="$HOME/rtl-tools/frame-venv/bin/python"
"$FPY" -m pip install 'z3-solver==4.16.0.0'
FBUILD="$HOME/rtl-tools/frame-rust"
RUSTUP_TOOLCHAIN=1.90.0 CARGO_TARGET_DIR="$FBUILD" cargo build --locked --release --manifest-path egraph/Cargo.toml --bin guard_proofs_fast --bin egg_assertion_forms --bin egg_diagnostic_forms
OUT="$HOME/rtl-tools/frame-diagnostic-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT"

# 规则覆盖与目标证明停止对照：使用归档真实公式，不调用 API。
"$FPY" scripts/egg_frame_proof_coverage.py --binary "$FBUILD/release/egg_assertion_forms" --output "$OUT/proof-coverage"
"$FPY" scripts/egg_frame_proof_coverage.py --binary "$FBUILD/release/egg_assertion_forms" --compare-early-stop --output "$OUT/proof-goal-stop"

# 单源生成 + 已归档真实曲线评分
"$FPY" scripts/egg_frame_diagnostic.py --binary "$FBUILD/release/egg_diagnostic_forms" --output "$OUT/generated.json"
"$FPY" scripts/egg_frame_diagnostic_score.py --generated "$OUT/generated.json" --output "$OUT/physical-score.json"

# 如果需要重新采集真实 RTL 对照并执行 formal，获取固定 upstream 文件；已有可复用。
"$FPY" scripts/m3_controller_replay.py --fetch "$OUT/fixture"
"$FPY" scripts/egg_frame_diagnostic_faults.py --fixture "$OUT/fixture" --output "$OUT/controls"
"$FPY" scripts/egg_frame_diagnostic_score.py --generated "$OUT/generated.json" --controls "$OUT/controls" --output "$OUT/physical-recheck.json"
"$FPY" scripts/check_frame_diagnostic_formal.py --generated "$OUT/generated.json" --fixture "$OUT/fixture" --output "$OUT/formal"
```

| 脚本 / 引擎 | 职责 |
|---|---|
| `scripts/egg_frame_proof_coverage.py` | 固定和去重公式对，独立完整位宽判定、认证原子替换、三配置比较及目标提前停止对照 |
| `egraph/src/bin/egg_assertion_forms.rs` | 原有通用规则引擎，加选用的目标证明停止开关；默认不变 |
| `egraph/src/bin/egg_diagnostic_forms.rs` | 实际单源 equality saturation 和 DNF 语法提取，输出具名解释 |
| `scripts/egg_frame_diagnostic.py` | 冻结生成规则，独立逐步检查和完整位宽/各子句等价充分性认证 |
| `scripts/egg_frame_diagnostic_baseline.py` | 普通 NNF/DNF 基线、精确最小充分已知文字搜索（至多 12 个抽象原子） |
| `scripts/egg_frame_diagnostic_faults.py` | 固定端口灵敏度对照、真实 Icarus 编译回放、独立 checker、PRE/POST 输出差异核验 |
| `scripts/egg_frame_diagnostic_score.py` | 重新核验证书与归档绑定，在真实轨迹上评分，包含 X/Z 的二态完成 |
| `scripts/check_frame_diagnostic_formal.py` | 独立解析生成式，重新渲染 SV、运行完整原版 RTL 的有界及归纳验证 |

最终回归：在隔离仓库副本内用已构建的两个通用引擎、indexed 原引擎、Python Z3 及固定 FIFO fixture 运行全量 `make test`，96 项均通过；indexed 专项 7 项通过；新的 Rust 单源生成器 3 项通过。测试覆盖拒绝伪造证明、无证明改写、错误端点、未饱和提取、目标停止范围和独立最小充分文字的控制。共 106 项测试无失败。

## 7. 结论与在线研究方向

最扎实的本轮结果是，把 egg 用于生成和审计验证证据：它不只是清理 guard，还能从一个复杂性质主动产生等价诊断分解、提供可追踪的具名改写；在等价性查询中也有明确的、证书导向的搜索停止方式。对简单 Boolean DNF，普通基线已经达到同样效果。不能据此声称 egg 增加了 RTL 检出率、优于命题求解器或增加在线模型准确率。

后续可以把已核验的短诊断子句和具体物理采样作为下一轮 LLM 反馈的可选实验因素。需要注意：本次生成源是冻结参考规格，直接把全部参考 DNF 暴露给模型将泄漏答案，不应作为公平的在线修订实验。应在保持各组同样可见波形/反例的前提下，比较候选自身的分解、普通短诊断和 egg 具名证明，使用多个独立会话和更困难的规格；把 held-out 事务故障与模型可见开发样本保持隔离，测量实际 token、首次合格轮次和新属性/真实轨迹质量。本轮没有发送新 API 调用，也没有更改原在线实验记录。
