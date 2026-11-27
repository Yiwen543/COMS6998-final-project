# AXI Frame Length Adjuster · 真实 API 反馈实验结果

2026-11-24 的 MacBook 运行共完成 6 次真实 Responses API 调用。**raw 与 egg 都在首轮把五条错误的初始监视器修订到满足规格；ordinary 在第二轮通过，原因是首轮多写了一个右括号。最终三组的候选完全相同。实时 egg 引擎只独立证明了其中三条，另两条的等价性由完整位宽 Z3 验证。** 两条未证明的具体原因已定位为现有规则缺少合取结合律。[原始实测和审计](../results/milestone3/frame-monitor-loop-live/audit.json)

## 实验设置与公平性

| 配置 | 实测值 |
| --- | --- |
| 请求及返回模型 | `gpt-6.1-sol` |
| 请求 reasoning effort | `low` |
| 返回 service tier | `default` |
| 单次输出上限 | 3,072 tokens |
| 预算 | 每组 1 个会话，各 2 轮 |
| 评分数据 | 21 条实际 Icarus RTL 轨迹，包含原版与 6 种已固定故障 |
| 可见数据 | 原版、F02、F05，两个故障在提示中使用 Probe A/B |

六个回执均记录 HTTP 200、completed 和不同的响应 ID。三组共享五条已知错误的初始监视器和相同规格。第一轮之前即收到不同反馈策略，因此与之前 FIFO 首轮提示完全相同的设计不同。重建了所有 6 份请求，确认后续历史只包含本组候选和反馈。ordinary 与 egg 对匹配候选收到完全相同的完整位宽反例及认证原子关系，仅证明摘要不同；原版和两个开发故障的可见 RTL 反馈也一致。记录中没有留出故障的名称或判定泄漏。[协议](egg_frame_protocol.md) · [所有实际请求和回执](../results/milestone3/frame-monitor-loop-live/transcript.tar.gz)

## 真实模型修订结果

| 指标 | raw | ordinary | egg |
| --- | ---: | ---: | ---: |
| 初始合格断言 | 0/5 | 0/5 | 0/5 |
| 首轮完整合格断言 | 5/5 | 解析失败，未评分 | 5/5 |
| 末轮完整合格断言 | 5/5 | 5/5 | 5/5 |
| 首次通过轮次 | 1 | 2 | 1 |
| 末轮独立抽象方法证明数 | 无此方法 | 5/5 | 3/5 |
| 末轮额外报警 | 0 | 0 | 0 |
| 末轮漏报 | 0 | 0 | 0 |
| 末轮与局部参考吻合的故障种类 | 3/6 | 3/6 | 3/6 |

ordinary 第一轮的结构化 JSON 有效，但 `header_hold` 含一个额外的闭括号（17 个左括号、18 个右括号）。解析器正确返回 `header_hold: unexpected trailing tokens`，整批没有进入语义或轨迹评分。第二轮只删除了该字符。另五份合法回复的五条监视器逐字符相同，raw 和 egg 均在首轮生成同一正确结果，且第二轮没有修改。这样的一次会话不足以把多出的一轮解析修订归因于证明反馈。所有合法输出都通过独立完整位宽查询。[逐轮评分](../results/milestone3/frame-monitor-loop-live/summary.json)

在原始完整 wrapper 和六个故障的 6,384 个周期记录上，每个候选有 31,815 个可判定的“性质 × PRE 采样”比较。独立复算了三份 seed 记录及五份合法回复的全量评分，逐项一致。

| 固定候选 | 参考报警 | 与参考一致的报警 | 多报 | 漏报 |
| --- | ---: | ---: | ---: | ---: |
| 初始错误监视器 | 23 | 18 | 894 | 5 |
| 五份合法模型回复中的任一份 | 23 | 23 | 0 | 0 |

23 次报警分别对应 F02（4 次）、F04（3 次）和 F05（16 次）。四个留出故障中仅 F04 会触发这组局部性质。初始候选已命中 F04 两次，修订后为三次，留出故障种类检出仍为 1。其余三种故障由完整事务检查器检测，参见 [真实 RTL 对照](egg_frame_results.md)。在线候选评分在已归档的真实波形上执行，模型各轮未重新启动 DUT 仿真。

另外在事后复核中，按五份合法回复中的唯一一组表达式独立生成 SystemVerilog 断言。直接在原版完整 wrapper 上运行 Yosys SAT，全部五项均通过 24 状态检查；对 indexed egg 未证明的两项保持性质又分别通过 3 状态基例和时间归纳。RTL 源哈希、时钟、复位及输入约束均沿用此前固定模型。三个头部算术性质保留有界结论，头部报告原始帧长是否与真实输入匹配仍由事务检查器处理。[实际模型候选的独立形式复核](../results/milestone3/frame-monitor-loop-live/candidate-formal/summary.json)

## Egg 3/5 的具体原因

| 性质 | 独立完整位宽 Z3 | 普通抽象判定 | 实时 indexed egg |
| --- | :---: | :---: | :---: |
| `data_hold` | 等价 | 已证明 | 饱和后无证明 |
| `header_hold` | 等价 | 已证明 | 饱和后无证明 |
| `pad_flag` | 等价 | 已证明 | 同一表达式 |
| `truncate_flag` | 等价 | 已证明 | 同一表达式 |
| `clamped_length` | 等价 | 已证明 | 同一表达式 |

实时 egg 的三项成功均为输入表达式直接相同，具名改写数为零。五条 seed 的错误公式也没有生成等价改写。对两项保持性质，参考与实际 LLM 输出具有相同的六个有序合取子项，差别在于括号如何结合。当前 `guard_proofs_fast indexed` 使用的六条布尔规则没有合取结合律。普通方法在认证原子上采用结构归一化和命题 XOR，能够处理这种写法。

独立的事后实验保留这两个实时未证明的公式，使用仓库已有的通用 `egg_assertion_forms` 引擎，只装载以下一条规则：

```text
(and (and ?a ?b) ?c) = (and ?a (and ?b ?c))
```

真值表独立检查该规则的 8 个赋值。实际 egg 对两个保持公式均生成 5 个具名步骤，全部通过逐步核验。这定位了当前实时配置的规则缺口。这个新配置是事后控制，实时报告和模型收到的反馈保持原有 3/5 结果。[两项事后证明与输入](../results/milestone3/frame-monitor-loop-live/associativity-control.json)

## Token 使用量

| 组 | 首轮 tokens | 第二轮 tokens | 总输入 | 总输出 | 总量 | 至首次通过 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| raw | 1,704 | 2,661 | 3,757 | 608 | 4,365 | 1,704 |
| ordinary | 2,285 | 2,721 | 4,263 | 743 | 5,006 | 5,006 |
| egg | 2,300 | 3,574 | 5,266 | 608 | 5,874 | 2,300 |

六次实报累计 **15,245 tokens**，其中输入 13,286，输出 1,959。缓存读取 5,344、缓存写入 7,924 和 reasoning 133 均为输入/输出细项，未重复计入总量。全部 133 个推理 tokens 来自 ordinary 第二轮；配置记录的是 low，不从推理计数字段推断模型内部处理。

- egg 对比 raw，总量增加 1,509（34.57%），输出量相同。两组都首轮合格，至首次合格 raw 1,704、egg 2,300。
- egg 对比 ordinary，总量增加 868（17.34%）。ordinary 第二轮只收到短的解析错误反馈，egg 第二轮收到完整语义/RTL 反馈，因此两轮累计差异不能全部归因于证明文本。
- 首轮 ordinary 与 egg 的共同证据一致，输入分别为 1,973 与 1,988。egg 首轮多 15 tokens。至首次合格 egg 的累计量低于 ordinary，差异主要来自 ordinary 的单字符语法失败。

这些是归档的请求和 provider 使用量回执，未包含独立核对的实际发票或现金费用。

## 结论与复核

该实验证明更复杂的实际 RTL 规格与修订反馈闭环能够运行，三个组都生成了满足五条规格的相同候选。raw 首轮已完成修订，egg 没有表现出额外的候选质量收益。实时 egg 证明覆盖低于强普通基线；事后对照进一步表明缺少结合律会使简单的结构差异无法合并。后续应把这种规则覆盖作为可测试指标，在固定真实公式和负例上评价证明质量，再进行多次独立在线会话。

审计读取 48 份实验文件并核对原生输入语料的 SHA-256。移除了 Mac 压缩包自动添加的 61 个 AppleDouble 元数据条目，保留实验文件原文。对原上传版和整理后的证据包得到逐字节相同的审计结果。复核 40 份完整位宽查询（15 SAT、25 UNSAT）、228 份原子关系查询（218 SAT、10 UNSAT）、10 份普通抽象查询和 15 份 indexed egg 图，重解查询并校验其与原公式的绑定，重放全部归档反例。评阅中没有发送新的 API 请求。[来源清单](../results/milestone3/frame-monitor-loop-live/provenance.json) · [独立审计](../results/milestone3/frame-monitor-loop-live/audit.json)

以下从仓库根目录运行。沿用 [Frame 的 Python/Z3 和 Rust 环境](egg_frame_results.md#环境脚本与复现)。两种 egg 二进制按仓库锁定依赖构建。

```bash
CARGO_TARGET_DIR=/tmp/frame-live-audit-rust cargo build --locked --release --manifest-path egraph/Cargo.toml --bin guard_proofs_fast --bin egg_assertion_forms
python3 scripts/audit_egg_frame_live.py --archive results/milestone3/frame-monitor-loop-live/transcript.tar.gz --corpus results/milestone3/frame-faults --binary /tmp/frame-live-audit-rust/release/guard_proofs_fast --output /tmp/frame-live-audit.json
cmp /tmp/frame-live-audit.json results/milestone3/frame-monitor-loop-live/audit.json
python3 scripts/check_frame_live_associativity.py --archive results/milestone3/frame-monitor-loop-live/transcript.tar.gz --binary /tmp/frame-live-audit-rust/release/egg_assertion_forms --output /tmp/frame-live-assoc.json

# 若之前已下载固定 RTL 文件，可复用其目录
python3 scripts/m3_controller_replay.py --fetch /tmp/frame-live-formal-fixture
python3 scripts/check_frame_live_candidate_formal.py --archive results/milestone3/frame-monitor-loop-live/transcript.tar.gz --fixture /tmp/frame-live-formal-fixture --output /tmp/frame-live-candidate-check
```

`audit_egg_frame_live.py` 负责重新评分、验证保存的 SMT 查询与证明、按实际输出重建隔离会话及核对 token。 `check_frame_live_associativity.py` 单独运行新引擎的合取结合律控制实验。`check_frame_live_candidate_formal.py` 独立渲染实际模型候选并在固定 RTL 上重新执行有界与归纳检查。这些脚本均在本地执行。
