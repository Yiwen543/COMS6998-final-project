# AXI 帧长度调整器的验证结果

在固定的 `frame_task` 上，独立事务检查器检出了全部 **6/6 种注入故障**。五条局部断言在同一批真实 RTL 观测中触发了 **3/6 种**。普通方法与 egg 都能证明五条修订后的断言等价于参考规格。对于其中三个涉及长度边界的断言，egg 还给出了可逐步复核的具名改写。本次离线修订使用预设回复，无法估计模型从 egg 反馈中获得的增益。[预先固定的实验设计](egg_frame_protocol.md)

后续真实 API 三组实验已在 MacBook 上完成，另见[在线实测、token 与合取结合律的事后对照](egg_frame_live_results.md)。

## 原始硬件和规格

使用固定提交 `e94172a1bd5e9b138b5fc3da01554edb3052ce52` 的原始 wrapper、帧长度调整器、数据和头部 FIFO。数据宽 8 位，两条 FIFO 深度分别为 32 和 8。输出不足 4 字节的帧应补齐，超过 8 字节的帧应截断。事务检查器从输入握手重建每一帧，检查输出数据、结束标记和头部。五条局部断言分别检查数据通道阻塞时保持、头部通道阻塞时保持，以及头部有效时的补齐标志、截断标志和夹紧后长度。长度字段为 16 位无符号数。局部断言以头部报告的原长为输入，原长本身与实际入队字节数的一致性由事务检查器覆盖。[RTL 与检查器哈希](../results/milestone3/frame-replay/summary.json) · [实际参与形式验证的五条断言](../results/milestone3/frame-formal/frame_assertions.svh)

**形式验证。** 在两态模型中，第一拍复位，复位时输入无效。源在未握手期间保持有效和载荷，每帧至多接受 12 个字节。消费端可独立阻塞。Yosys SAT 对完整 wrapper 的五条断言联合展开 **24 个状态，通过**。独立的 SMTBMC/Z3 路径完成状态 0–17，进入状态 18 后达到 15 秒求解时限，因此其 24 状态结论为 **INCONCLUSIVE**。单独检查的两条保持性质通过 3 状态基例与时间归纳，在上述模型及假设内成立。其余三条头部性质保留 24 状态有界结论。[形式结果及运行版本](../results/milestone3/frame-formal/summary.json) · [Z3 超时日志](../results/milestone3/frame-formal/safety-z3.log) · [归纳日志](../results/milestone3/frame-formal/holds-induction.log)

六个 cover 分别在零基状态 7、10、9、14、9、13 达到数据阻塞、头部阻塞、补齐帧、截断帧、恰好 4 字节和恰好 8 字节。每个原生 witness 都在 Icarus 上回放，同一状态再次观察到相应条件。这一检查说明保持性质和长度边界确实可以被激活。[cover 日志与回放](../results/milestone3/frame-formal/)

## 三个真实场景与六种故障

| 原始 DUT 的场景 | 周期 | 在端口观察到的行为 | 事务检查 |
|---|---:|---|---|
| 长度扫描 | 250 | 输入帧 1–12 字节各一帧，收到 12 个输出帧及 12 个头部 | PASS |
| 数据与头部独立背压 | 423 | 24 帧。两个输出同时受阻 42 周期。对端受阻时分别发生 59 次数据握手、13 次头部握手 | PASS |
| 有未完成事务时复位 | 239 | 第 29 个采样复位时已有 3 个完整输入帧和下一帧的 3 个字节。复位后完成 5 帧及对应头部 | PASS |

三次回放的参考检查均无确定失败或未知。另把原版和 6 种单点变异分别编译，在相同的三个场景下做 **21 次 Icarus 回放、6,384 个周期**。18 个变异与场景组合中，独立检查器给出 13 个失败、5 个通过。5 份已有确定失败的报告还记录了未决的完成性检查，故障类型计数仅采用确定失败。[原版场景记录](../results/milestone3/frame-replay/summary.json) · [逐变异原始记录](../results/milestone3/frame-faults/cases.json)

三个原始场景合计接受 44 帧完整输入、交付 41 帧完整输出及头部。其余 3 帧及一帧已接收的 3 个字节属于复位前被撤销的事务。每个场景有至少 128 拍完成阶段，所有未撤销的帧均完成交付。

| 固定故障 | 完整事务检查器至少一次确定失败 | 五项局部参考断言在三条轨迹中的报警次数 |
|---|:---:|---:|
| F01 · 补齐字节值错误 | 是 | 0 |
| F02 · 长度恰好为 8 也报告截断 | 是 | 4 |
| F03 · 截断后缺失 TLAST | 是 | 0 |
| F04 · 输入未握手时仍累加长度 | 是 | 3 |
| F05 · 错用数据通道 ready 消费头部 | 是 | 16 |
| F06 · 头部 FIFO 未响应复位 | 是 | 0 |

表中次数按“断言 × 采样”计数。F01 的数据内容、F03 的帧边界和 F06 的跨复位残留说明为什么仍需保留事务级检查。例如，错的补齐字节也可以在阻塞期间保持稳定。F04 只在背压场景被事务检查器检出，F06 只在复位场景被检出。[故障注入语句、检测矩阵和原生日志](../results/milestone3/frame-faults/README.md)

## 从错误监视器开始修订

固定初始候选有五处错误，分别为数据保持误用本拍 ready、头部保持漏查原始长度、补齐/截断在恰好 4/8 时误报警，以及未正确计算夹紧长度。对每条完整公式，用包含实际位宽的 Z3 XOR 查询判定是否等价。再在上述真实轨迹上逐字段比较候选与局部参考的报警。每条轨迹的第一个 PRE 采样没有前一拍，剩余 6,363 个采样共形成 31,815 个“断言 × 采样”对照。[类型与公式定义](../scripts/egg_frame_terms.py) · [轨迹评分](../scripts/egg_frame_observe.py)

| 冻结候选 | 与规格等价 | 多报 | 漏报 | 比较结果未知 |
|---|---:|---:|---:|---:|
| 初始错误候选 | 0/5 | 894 | 5 | 0 |
| 各组首轮预设修订 | 5/5 | 0 | 0 | 0 |
| 各组第二轮预设修订 | 5/5 | 0 | 0 | 0 |

894 次额外报警中，127 次发生在通过完整事务检查的原版上。局部参考共报警 23 次，初始候选匹配 18 次。四种留出变体中仅 F04 会触发这组局部监视器，修订增加了对 F04 的一次参考报警的匹配。因此修订没有增加留出故障种类的检出数。部分未有效的输出引脚仍含 X/Z，评分器对这些值的所有二态补全求值，只认可可确定的违例。本批比较均可确定；综合合格状态要求无未知比较。

三组各运行两轮，使用内容相同的预设候选和各自独立的历史。raw 查看真实 RTL 的局部结果。ordinary 和 egg 额外接收同一份完整位宽等价反例，以及各自的证明结果。开发视图只含原版和两个匿名探针 F02/F05，统一评分还包括 F01/F03/F04/F06。第二轮将夹紧长度的区间再写成越界条件的否定，重新核验后仍为 5/5。总计 6 个预设回复、0 次模型 API 调用。该实验检验反馈隔离、证明内容和评分链路，未测得真实模型的修订能力或 token 成本。[分轮结果](../results/milestone3/frame-monitor-loop-fixture/summary.json)

第一次流程审查发现，即使两个公式完全相同，重复运行 Z3 也可能选到不同的反例，对模型构成不同提示。最终版本在三个组之间为相同的参考式和候选式共用一次完整位宽的独立查询。驱动同时检查匹配候选的 common 反例、可见反馈和认证原子规则库存一致，只允许普通组和 egg 组的证明字段不同。两次最终离线复跑均通过，50 份请求、判定及证据文件在排除计时字段后完全相同。这次尚未实际花费模型额度。

ordinary 与 egg 使用相同的、经 Z3 认证的原子比较关系。ordinary 合并等价或互补的比较，进行结构归一化，并检查命题 XOR。修订后的五项都可获得相同的归一化形式。egg 也证出 5/5 项。两条保持公式与参考相同，无需改写。首轮另外三项各有两步已核对的具名改写，例如 16 位无符号数的 `length < 4` 与 `length <= 3` 等价，`length > 8` 与 `length >= 9` 等价。第二轮的夹紧长度产生六步证明，包含两个有类型的互补关系、双重否定和德摩根变换。普通对照仍可归一化并证明。原来的五条错误公式在两种方法中均未取得证明。此次没有观察到 egg 相对普通对照额外修复或证明的断言。[普通方法的首轮证明](../results/milestone3/frame-monitor-loop-fixture/ordinary/round-01/semantic.json) · [egg 首轮逐步证明](../results/milestone3/frame-monitor-loop-fixture/egg/round-01/semantic.json)

## 环境、脚本与复现

使用 Linux、Python 3.12、Z3 4.16.0（Python 模块和 CLI）、Yosys 0.52（含 `yosys-smtbmc`）、Icarus/vvp 12.0、Rust/Cargo 1.90 与锁定的 egg 0.11。下例在仓库根目录执行，输出目录均需为新路径。安装完整工具链的步骤见主文档。[环境安装](milestone3.md#环境与一键复现)

```bash
python3 scripts/m3_controller_replay.py --fetch /tmp/frame-fixture
CARGO_TARGET_DIR=/tmp/frame-rust cargo build --locked --release \
    --manifest-path egraph/Cargo.toml --bin guard_proofs_fast
python3 scripts/egg_frame_formal.py --fixture /tmp/frame-fixture --output /tmp/frame-formal
python3 scripts/egg_frame_replay.py --fixture /tmp/frame-fixture --output /tmp/frame-replay
python3 scripts/egg_frame_faults.py --fixture /tmp/frame-fixture --output /tmp/frame-faults
python3 scripts/egg_frame_llm.py --fixture --corpus /tmp/frame-faults \
    --binary /tmp/frame-rust/release/guard_proofs_fast --rounds 2 --output /tmp/frame-monitor-loop
```

`egg_frame_formal.py` 构建形式模型、运行 SAT/SMTBMC、保存并回放 cover 证人。`egg_frame_replay.py` 构建原始 wrapper，生成三种激励并用冻结的事务检查器评分。`egg_frame_faults.py` 逐一核验并应用六处注入，保存完整端口观测和参考判定。`egg_frame_llm.py` 隔离各组历史，调用 `egg_frame_terms.py` 的类型化表达式、`egg_frame_proof.py` 的等价与证明检查、`egg_frame_observe.py` 的真实轨迹评分。替换参数、放宽输入帧长上限或增加新的事务正确性要求时，需要重新验证相应结论。

## 下一轮真实 Responses API

在 MacBook 上沿用已跑通的 OSS CAD Suite 和 Cargo 环境，在现有仓库根目录应用新增文件。新增的 Python 类型化等价检查需要 `z3-solver`。下面使用此前安装的 Python 3.12 建立隔离环境。已归档的 `frame-faults` 可直接用于候选评分，也可用上述命令重新模拟获取自己的真实 corpus。每轮评分基于全量固定 PRE 观测和独立类型化 Z3 查询，模型只收到预设开发子集。

```bash
"$(brew --prefix python@3.12)/bin/python3.12" -m venv "$HOME/rtl-tools/frame-venv"
FPY="$HOME/rtl-tools/frame-venv/bin/python"
"$FPY" -m pip install 'z3-solver==4.16.0.0'
FBUILD="$HOME/rtl-tools/frame-rust"
RUSTUP_TOOLCHAIN=1.90.0 CARGO_TARGET_DIR="$FBUILD" cargo build --locked --release --manifest-path egraph/Cargo.toml --bin guard_proofs_fast
FBIN="$FBUILD/release/guard_proofs_fast"
CORPUS="$PWD/results/milestone3/frame-faults"
"$FPY" scripts/egg_frame_llm.py --fixture --binary "$FBIN" --corpus "$CORPUS" --rounds 2 --output "$HOME/rtl-tools/frame-check-$(date +%Y%m%d-%H%M%S)"
```

预检成功后用下面的指令运行三组真实 API。固定 `gpt-6.1-sol/low` 及最多两轮，每轮最多 3,072 输出 tokens，合计最多 6 次 API 调用。模型输出候选的真实内容、请求、语义判定、物理轨迹评分、反馈和用量统一保存。

```bash
OUT="$HOME/rtl-tools/frame-live-$(date +%Y%m%d-%H%M%S)"
(
  printf 'OpenAI API key: '
  IFS= read -rs OPENAI_API_KEY
  printf '\n'
  export OPENAI_API_KEY
  "$FPY" scripts/egg_frame_llm.py --live --model gpt-6.1-sol --reasoning-effort low --rounds 2 --max-output-tokens 3072 --binary "$FBIN" --corpus "$CORPUS" --output "$OUT"
)
cat "$OUT/summary.json"
```
