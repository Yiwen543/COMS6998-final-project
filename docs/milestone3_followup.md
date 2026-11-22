# Milestone 3 追加实验 · 规则归一化能否减少实际求解

**结论。** 在固定的 AXIS Controller、相同的 281 条认证规则和相同的最早命中任务上，普通结构改写和 indexed egg 都将 148 个目标归为 87 个求解义务，都实际少调用 Z3 61 次。egg 的增量节省为 **0 次**。两组在原始 RTL 上给出相同的 100 个有限命中及 48 个有限未命中，普通方法的验证循环中位数为 **220.10 ms**，egg 为 **246.98 ms**。这与原实验的引擎加速可以同时成立：用 egg 生成同一份证明时索引能加速，此处比较对象换成了直接利用同一批等价规则的普通方法。[逐轮数据](../results/milestone3/controller/trials.jsonl) · [原实验](milestone3.md)

## 1. 修复验收门槛并执行负例

- RTL 回放逐点比对历史 DUT 计数的完整身份、是否存在和整数命中次数，包含 Verilator 的 `page` 字段及零命中项。历史数据只改变命中次数，或只改变 `page` 而维持覆盖率，都能触发失败；同一文件仅调换记录顺序可正常通过。审查时可通过的负例是定向回放中 `grant_index[0]:0->1` 的计数从 7 改到 8。现在相同负例在第一组即返回非零，并保留失败原因。[验收实现](../scripts/benchmark_m3_rtl.py)
- 调用端核对引擎自己报告的模式。负例通过一个转发程序把请求的 `indexed` 送入真实引擎的 `spanning`，即便两种模式给出相同证明，也会被拒绝。原有两批 288 次物理回放的归档内容通过了新检查。认证配置另重新跑了 36 个正确试验，72 次回放全部成功。[可执行负例](../tests/test_m3_rtl_gates.py)

## 2. 自动见证与人工探针分别带来了什么

每组都保留原四个初始检查。Verilator 与 Icarus 对四组的 checker 事件完全一致。覆盖数据取自 Verilator 的原始 DUT 计数，16 个 guard 目标和 18 个原始分支点的分母分别保留。[逐组覆盖、向量与事件](../results/milestone3/stimulus-ablation/summary.json)

| 初始检查后追加 | 检查次数 | guard 命中 | 原始分支覆盖 | Toggle | 功能 / 时序错误 |
|---|---:|---:|---:|---:|---:|
| 无 | 4 | 2/16 | 3/18 | 9/60 | 0 / 0 |
| 14 个见证 | 18 | 16/16 | 17/18 | 58/60 | 0 / 0 |
| 4 个规格探针 | 8 | 2/16 | 3/18 | 42/60 | 1 / 1 |
| 见证和探针 | 22 | 16/16 | 17/18 | 60/60 | 1 / 1 |

14 个见证补齐了 14 个初始未命中目标。第二个规格探针输入 `req=0x80, override=0x03`，观察到 grant 为 `0x03`，规格要求 `0x01`。第三个探针在有效授权后拉高 reset，观察到输出在下一个时钟上升沿前已经清零。采用相同首见证的 raw 方法也可取得这些覆盖结果。本例的两个缺陷均由手工规格探针独立复现。[回放脚本](../scripts/m3_stimulus_ablation.py)

## 3. 普通结构改写与 egg 的 Controller 对照

**输入和问题。** 使用参考仓库固定提交的 `axis_length_fifo_v1`，包括 AXIS frame length adjuster 及 FIFO 实例。此处的 Controller 与后文生成被动监视器的 req/resp controller 是不同 DUT。原封保留 148 个目标、52 个实例限定的 atom、281 条专用规则及六条通用布尔规则。逐条将原始 QF_BV 文件的定义、目标 ID、源式、替换式、事件上下文与输入绑定，重新执行 281 个 XOR 查询，全部为 `unsat`。每组均使用每次 2,000 ms、每轮至多 148 次的相同求解预算。[固定实验设计](milestone3_controller_protocol.md) · [逐规则认证及哈希](../results/milestone3/controller/certificate.json)

固定三条公开轨迹 basic、boundary_pressure、reset_reuse，分别有 48、64、64 个上升沿。按原观测契约去掉每条轨迹首个未初始化的 PRE 采样，合计 173 个有效采样。每个目标都问同一问题：按既定轨迹及周期顺序，原始完整 guard 首次为真在哪里？两组都在**同一份已采集轨迹**内求解。需要生成全新刺激、突破这三条轨迹的覆盖范围时，应另外做开放输入的搜索实验。这里的 48 个有限未命中不能解释为全局不可达。

普通方法用并查集合并规则的确切端点，对语法树做结构替换及布尔化简直到稳定。egg 使用相同规则做饱和，并输出其原生证明。只有完整上下文一致的目标才能共用一次求解。两组分别用相同的 Z3 求解器处理各组原始 guard，用同一个最小样本索引目标确定首个见证。额外运行的未分组对照实际发出 148 次查询，与两组逐目标答案一致。没有使用“两个目标在本次轨迹上碰巧同时为真”作为合并依据。[普通方法与 egg 驱动](../scripts/benchmark_m3_controller.py) · [Z3 有限轨迹模型](../scripts/m3_controller_solver.py)

| 每轮，六次配对试验的中位数 | 普通结构改写 | indexed egg |
|---|---:|---:|
| 实际 Z3 调用 / 相对 148 次少调用 | 87 / 61 | 87 / 61 |
| 读取输入及分组，ms | 4.12 | 30.74 |
| 建立有限域、求解及展开见证，ms | 93.53 | 93.01 |
| 三条完整原始 RTL 回放及解析，ms | 119.42 | 120.31 |
| 结果验收，ms | 4.20 | 4.02 |
| **含上述工作的总 wall time，ms** | **220.10** | **246.98** |

每个阶段和总时间各自取中位数。6 对中 egg 均用时较长，配对差值中位数 **+29.66 ms**。indexed 路线还计算并输出 70 条解释边，普通路线只需要给出分组和逐目标答案；本次衡量的是这两个实际可用的端到端实现。相同的公共准备另耗费 10.55 s 编译 DUT、60.60 ms 重验规则、120.88 ms 采集三条轨迹。轨迹的所有原始 guard 一旦已经观察到，直接扫描这些值也能给出同样答案，单次扫描观测为 **0.45 ms**。它只计扫描阶段，不能与包含仿真的整轮时间直接相比。[汇总及公共开销](../results/milestone3/controller/summary.json)

**回放与独立检查。** 六组配对共启动 36 次正式完整回放，另有 3 次公共轨迹采集。两路保存的所有目标、输出、每条轨迹的 3,168 个 DUT 计数及正确设计的 checker 结果逐项一致，三条轨迹均 PASS，没有未知事件。另用未加探针的原版 driver 与采样版逐条比较，共 531 条公开观测和每条轨迹的所有原始计数一致。[原始采样与完整计数](../results/milestone3/controller/records.json.gz) · [探针对照](../results/milestone3/controller-passivity/summary.json)

对两个实验组的实际答案又做了独立复核：从复位重新驱动每个不同的最早命中前缀，到所选周期即停止。20 个前缀共 267 个边沿，在指定 PRE 采样上逐一确认了 **100/100** 个命中。原有 148 个目标中 142 个能唯一映射至原始覆盖计数，6 个映射未决。100 个命中中有 94 个同时具备对应原始计数，另 6 个有 PRE 观测证据。各组都保留这 6 项映射状态。[逐目标答案](../results/milestone3/controller/answers.json) · [前缀回放证据](../results/milestone3/controller/prefix-replay-summary.json)

从新目录重新下载、构建并顺序执行完整追加实验，两组仍各做 87 次查询，得到相同分组、逐目标答案和原始 RTL 观测。复跑完整循环中位数分别为 219.97 ms 与 252.73 ms。见证前缀的逐条证据、无探针对照、消融、formal 与历史 usage 核对结果也与首次运行一致。[同机复跑记录](../results/milestone3/controller/reproduction/summary.json)

## 4. 跨周期性质与历史模型用量

**跨周期验证。** 对原始 arbiter 的同步复位要求建立了实际 DUT 的半周期模型。Yosys/Z3 的 cover 在状态 4 达到触发条件，BMC 在状态 4 找到反例。Icarus 回放相同输入，看到低电平期间的输出从 `01/1/0` 提前变为 `00/0/0`。仅修正复位敏感列表的控制版本可以到达同一场景，8 个半周期的有界检查及时间归纳均通过。该证明仅针对所写的复位保持性质和列明的时钟/输入假设。[性质、边界与复现](m3_formal.md)

**历史 token。** 逐条核对 M2 六次实际模型响应与账本，B 共 123,663 tokens，C 共 133,915，多 10,252（8.2903%）。两组最终都检测到 11/12 类历史故障。本轮新 provider 请求为 0；保留了新在线实验的真实调用入口和预算配置说明。当前用量不能用于计算 indexed 相对普通改写的 token 收益。[离线用量、实验配置与未来入口](m3_online.md)

## 复现命令与脚本职责

在含 v1 提交的 Git 克隆中配置[原实验环境](milestone3.md)。本轮需要 bash、C++/make、Rust 1.90、Python 3.12、Verilator 5.050、Icarus 12、Yosys 0.52 和附带的 yosys-smtbmc。Z3 的 CLI 和 Python 模块来自同一 `z3-solver==4.16.0.0`。以下第二条会从 GitHub 下载固定提交的 14 个公开文件，每个都校验 SHA-256。输入、构建和回放保存在全新的运行目录。默认复核随仓库保存的历史用量，不访问模型 API。

```bash
bash scripts/run_milestone3.sh /tmp/coms-m3-base
bash scripts/run_milestone3_followup.sh /tmp/coms-m3-base /tmp/coms-m3-followup
```

| 入口 | 作用、输入与产物 |
|---|---|
| `scripts/run_milestone3_followup.sh` | 复用上一轮编译好的 arbiter 和 egg release 二进制，按顺序执行验收负例、消融、Controller 实验、前缀与无探针对照、时序 formal 和历史用量核对。 |
| `tests/test_m3_rtl_gates.py` | 在原始覆盖数据上改变一次命中次数或身份，并用真实二进制转发到错误模式，检查新门槛能拒绝全部负例。 |
| `scripts/m3_stimulus_ablation.py` | 从带哈希的原 arbiter 运行提取 14 个见证，分别启用见证、探针或两者，用 Verilator 和 Icarus 核对 checker。 |
| `scripts/m3_controller_replay.py` | 下载并校验清单中的 DUT、driver、轨迹、checker 和证书，编译原始 RTL；采集 PRE guard、公开输出及原始覆盖。另提供 `--check-passivity` 对比原版与加探针 driver。 |
| `scripts/m3_controller_certificates.py` | 对固定 `screen/` 文件重新执行附带的 281 个位向量反例查询，验证上下文并写出逐规则状态。 |
| `scripts/m3_controller_solver.py` | 将原始 atom 的观测序列编码为采样索引上的谓词，用 Z3 Optimize 求有限域内的最早命中。超时、未知或没有证实最优值的查询使运行失败。 |
| `scripts/benchmark_m3_controller.py` | 用两种分组方法、同一个求解器和预算对固定目标做配对计时，逐轮记录求解次数、时间、证明和原始 RTL 回放校验。 |
| `scripts/check_m3_controller_witnesses.py` | 无分组重做 148 次求解并逐目标比较，再从复位回放求解器选出的每个不同前缀。|
| `scripts/check_m3_formal.py` | 对真实 arbiter 和单项修正控制运行 BMC、cover、控制版本的归纳证明及 Icarus 反例回放。 |
| `scripts/audit_m3_online_usage.py` | 校验历史真实回包、逐次账本和汇总，缓存及 reasoning token 仅作为已包含的子项。直接付费调用入口另见在线实验说明。 |
