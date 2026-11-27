# Milestone 3 · Proof-Carrying LLM Verification 真实 API 实验

2026-11-24 MacBook 的完整 cube 模式实验已经结束。18 个真实 Responses API 回执均完成，Raw 和 Egg 在全部三种起点上均首轮生成正确的所有五条断言；Ordinary 两种起点首轮通过，Mixed 首轮仅发生一次括号语法错误，第二轮修复。**17 份合法回复的五条监视器逐字符完全相同。** Egg 证明反馈确实已接入真实模型请求，但这组工作负载未显示相对 Raw 的候选质量或首次成功轮次收益，且实测 token 增加。

[原始真实请求和响应](../results/milestone3/frame-pc-live/transcript.tar.gz) · [独立审计](../results/milestone3/frame-pc-live/audit.json) · [预先固定协议](egg_frame_pc_protocol.md) · [此前离线证书策略对照](egg_frame_pc_results.md)

## 1. 实验设置和完成性

| 配置 | 实际值 |
|---|---|
| 请求 / 返回模型 | `gpt-6.1-sol` |
| 请求 reasoning effort | `low` |
| 回执 service tier | `default` |
| 输出上限 | 3,072 tokens |
| 起点 | historical、mixed、corner，每个起点 1 次重复 |
| 反馈组 | raw、ordinary、egg，各独立历史、固定两轮 |
| 证书策略 | `cube`（未运行 DNF 真 API 比较） |
| 完成回执 | 18/18，HTTP 200、completed、不同 response ID |
| 原始 RTL 语料 | 原版和六种固定 RTL 变异，21 条真实 Icarus 轨迹 |

三组的共同反馈包含完整位宽 Z3 判定及开发集的实际/符号反例。Ordinary 和 Egg 收到匹配候选的相同最短充分诊断，Egg 额外收到符合预算的独立可核验证书。Raw 本轮也有完整位宽反例，因此比早期只有仿真反馈的 Raw 更强。开发集只含原版和两个匿名探针（F02、F05），留出 F01/F03/F04/F06 保持仅用于物理评分。独立审计根据固定语料重建所有 18 个请求，确认 9 个非末轮回复均进入本组下一轮，没有跨组历史或留出信息出现在工具反馈中。日志包含真实 provider 用量，未在云环境发送新的模型请求。

## 2. 实际 LLM 修订质量

下表每个合法阶段写完整位宽等价属性数。解析失败的整批输出不进入语义或轨迹评分，不能算作 0/5 个语义正确。

| 初始候选 | Raw 第一轮 / 第二轮 | Ordinary 第一轮 / 第二轮 | Egg 第一轮 / 第二轮 |
|---|---:|---:|---:|
| Historical | 5/5 → 5/5 | 5/5 → 5/5 | 5/5 → 5/5 |
| Mixed | 5/5 → 5/5 | 解析失败 → 5/5 | 5/5 → 5/5 |
| Corner | 5/5 → 5/5 | 5/5 → 5/5 | 5/5 → 5/5 |
| 首轮整批合格 | 3/3 | 2/3 | 3/3 |
| 末轮整批合格 | 3/3 | 3/3 | 3/3 |
| 合格回复数（含两轮） | 6/6 | 5/6 | 6/6 |

Mixed 的 ordinary/round-01 中 `header_hold` 末尾比共同正确候选多一个 `)`，解析器返回 `header_hold: unexpected trailing tokens`。其余四个表达式与成功回复逐字符一致。该批未进入完整位宽评分；第二轮只删除这个字符。另 17 批合法输出完全相同，和之前真实 Frame 在线实验中合法模型终稿的写法也完全一致（五个表达式的规范 JSON 摘要 `79b6aa2088814e4e288069df23c2458a283e9d194ab4960a1970abc0deb66a0d`）。没有足够证据把一次可恢复语法失误归因于是否收到 egg 证明；本实验每个 profile 每臂只有一次会话。

实际三种起点的独立判断与轨迹评分如下。21 条轨迹包含 6,384 个周期、6,363 个可用相邻 PRE 样本，每批五个属性共 31,815 次比较。

| 候选 | 等价属性 | 与参考报警一致 | 多报 | 漏报 | 未知比较 |
|---|---:|---:|---:|---:|---:|
| Historical seed | 0/5 | 18 | 894 | 5 | 0 |
| Mixed seed | 0/5 | 6 | 202 | 17 | 14 |
| Corner seed | 0/5 | 23 | 0 | 0 | 0 |
| 17 批合法回复中任一批 | 5/5 | 23 | 0 | 0 | 0 |

23 个参考报警仍对应 F02（4）、F04（3）、F05（16）；原版零报警，局部属性检测三种固定内部变异（3/6），完整事务 checker 检测全部六种（6/6）。没有增加局部性质的检测范围。Corner seed 虽然在这些物理观测上完全匹配，却有 5 个全位宽反例；所有三组得到的 Corner 首次反例均为符号模型。符号反例不被声称为物理可达输出。这说明完整位宽语义判断的重要性，但不能把 raw 的成功修订归功于 egg。

## 3. 真实请求中的证明携带情况

| 起点 | 初始诊断机会 | 完整私有证明（独立重放） | 实际送入首次请求的完整证书 | 预算超限未发送 |
|---|---:|---:|---:|---:|
| Historical | 5 | 5 | 4 | 1 |
| Mixed | 5 | 5 | 5 | 0 |
| Corner | 5 | 5 | 4 | 1 |
| 总计 | 15 | 15 | **13** | 2 |

15 个共同最短充分诊断都由完整位宽蕴含检查确认、15 份受限候选都得到有效 named proof。13 个公开证书有 73 步具名改写（中位 5，范围 2–10），8 个来源是物理观测、5 个是符号反例；7 个解释候选报警为真，6 个解释候选为假。Historical 和 Corner 的 `header_hold` 分别需要 56、50 步，两个完整证明超过 32 步和 6,000 字符限制而未发送；两项候选漏报仍被首轮模型正确修订。15 个不同 signed candidate 对应 14 个不同 restricted 残式，公开证书 13 个，不计重复历史为新生成。

**这个在线实验的一个重要边界：** 三组中所有语法正确的第一轮回复都已完整通过，因此没有任何新的、语法正确但语义错误的模型候选需要在第二轮重新生成证书。Egg 首轮收到 13 个来自预设 seed 的证书；第二轮的累积历史保留了同样 13 份，但第二轮的新反馈没有任何证明或诊断（普通组 Mixed 唯一未通过项得到解析错误）。所以 13 是独立发送的新证书数，若按两轮完整历史重复出现计是 26 次，不能当作 26 个不同证明。本次验证了真实 API 可消费 proof-carrying 请求及历史链路，却没有真正观察到“对 LLM 自己生成的语义错误，再生成证书帮助下一轮修复”的效果。上一轮 fixture 由于固定首轮故意留有三项错误，才有 24 次诊断机会、20 份可发送证书；实际 run 的 15 次机会与 fixture seed 子集一致。

三个实例说明证书内容确实有诊断意义：

- Historical `data_hold`，原版 backpressure 第 31 拍：`prev_m_ready=1`、`m_ready=0`、`m_data` 从 91 变 125。旧候选误用本拍 `m_ready`，造成参考为假而候选为真的多报。六文字的充分条件经 10 步具名改写证实候选报警；Egg 首轮改为 `prev_m_ready`，但是 Ordinary 与 Raw 也做出了同样修订。
- Mixed `header_hold`，Probe B backpressure 第 17 拍：上一拍 header 有效且 stalled，当前 `h_valid=0`，其它当前 header payload 不可确定，参考报警为真但候选为假。`h_valid=false` 单个已知文字足以决定候选为假，通过 4 步证书使受限的 `not(candidate)` 为真。普通组也收到相同的短诊断，Raw 得到同一反例。
- Corner `truncate_flag` 的符号反例：`h_original_length=65280`、`h_truncate=false`、`h_valid=true`、`rst=false`。候选包含多余的 `h_original_length≤255`，该条件为假足以屏蔽违例报警，经过 `and-false-left` 和 `not-false` 两步得到证书。所有合法首轮模型修订均去掉了该上限。它不是 RTL 实际输出 65280 的记录。

## 4. 实际 API token 与反馈开销

| 初始候选 | 组 | 第一轮合计 | 第二轮合计 | 固定两轮 | 至首次完整合格 |
|---|---|---:|---:|---:|---:|
| Historical | raw | 2,275 | 3,341 | 5,616 | 2,275 |
| Historical | ordinary | 2,629 | 3,718 | 6,347 | 2,629 |
| Historical | egg | 4,533 | 5,612 | 10,145 | 4,533 |
| Mixed | raw | 2,286 | 3,368 | 5,654 | 2,286 |
| Mixed | ordinary | 2,625 | 3,100 | 5,725 | 5,725 |
| Mixed | egg | 5,097 | 6,176 | 11,273 | 5,097 |
| Corner | raw | 2,290 | 3,356 | 5,646 | 2,290 |
| Corner | ordinary | 2,575 | 3,648 | 6,223 | 2,575 |
| Corner | egg | 4,776 | 5,855 | 10,631 | 4,776 |

| 组 | 总输入 | 总输出 | 固定两轮总量 | 截至各会话首次合格总量 |
|---|---:|---:|---:|---:|
| raw | 15,108 | 1,808 | 16,916 | 6,851 |
| ordinary | 16,313 | 1,982 | 18,295 | 10,929 |
| egg | 30,225 | 1,824 | 32,049 | 14,406 |
| 全部 | 61,646 | 5,614 | 67,260 | 32,186 |

Egg 对 ordinary 的固定两轮 token 增加 13,754（75.18%），至首次成功增加 3,477（31.81%）。对 raw 的固定两轮增加 15,133（89.46%），至首次成功增加 7,555（110.28%）。Mixed 单独看 Egg 至首次合格比 ordinary 少 628，但普通组第一轮只是语法错误，Raw 仍更快达到合格（2,286 tokens）；不能把这一单个样本视作证明反馈的收益。历史和 Corner 两个会话均为 Egg 更高用量。

比较第一轮匹配候选、共同反例和诊断时，raw / ordinary / egg 的实报输入为 5,931 / 6,909 / 13,470，Egg 比 ordinary 增加 6,561（94.96%）。三组第一轮无 cache read；Egg 的额外初始反馈为 21,037 UTF-8 bytes。第二轮延续各自历史，其中 ordinary Mixed 只收到 58-byte 解析错误反馈，所以固定两轮差额不等同于纯粹证书 token 影响。新反馈文本累计 raw 21,737 / ordinary 22,449 / egg 46,602 bytes，包含各请求所新增的 feedback packet，不含重复历史、响应 schema 或传输包装。

两轮实报 cache reads 合计 26,283（raw 5,922、ordinary 6,900、egg 13,461），全部第二轮；cache writes 35,309 均为 30 分钟缓存。172 个 reasoning tokens 全部来自 ordinary Mixed 第二轮。缓存和 reasoning 是父 token 数的子集，不重复计入总量。没有 provider 发票、价格或端到端延迟记录，不把 token 数等同为实付费用或执行速度。

## 5. 完整 RTL Formal Verification 独立复验

根据实际模型合法回复去重，独立渲染唯一完整候选的 SystemVerilog 断言。对实际五条候选重新解全位宽 XOR，全部 UNSAT，并用 Z3 CLI 另行复核。使用固定完整 `frame_task`、原版 RTL 与原形式 harness，执行 Yosys SAT 的 24 状态有界检查，五项全部通过；两个保持属性通过 3 状态基例及时序归纳检查。另外三条长度/标志性质仍只有有界结论，不能称为整个帧事务协议已获无界证明。该轮是对真实 API 候选的后验独立 formal run，不是用历史结果替代。物理轨迹评分重用锁定的 Icarus 语料，没有重新模拟每个 API 回复。

[独立形式结果、源哈希与调用来源](../results/milestone3/frame-pc-live/formal/summary.json) · [24 状态 SAT 日志](../results/milestone3/frame-pc-live/formal/79b6aa2088814e4e288069df23c2458a283e9d194ab4960a1970abc0deb66a0d/candidate-sat.log.gz) · [两项时序归纳](../results/milestone3/frame-pc-live/formal/79b6aa2088814e4e288069df23c2458a283e9d194ab4960a1970abc0deb66a0d/candidate-holds.log)

## 6. 结论、局限与下一研究任务

- 工程上成功：真实 LLM 请求可以携带可重放的候选局部证明，13/15 公开证书全部复核通过；达到限制的证明不发送残缺版本。该性质可用于验证证据审计，与模型是否正确修订是两个指标。
- 实验上未观察到额外修订质量或语义收敛收益：强 Raw 首轮已 3/3，Egg 消耗最高。前一次 Frame 真 API 实验也产生逐字符相同的合法终稿，表明当前五项显式规格与强反例反馈对模型较容易。不能仅为争取正向结论重复运行同一简单修订实验或将语法失败算作语义错误。
- 建议转向更有判别力的真实事务级规格，如按输入 TLAST 重建的完整帧/状态对应、数据字节保持顺序及正确 padding、复位跨 epoch 的完成约束。先让 LLM 在同一任务上自主生成尚未经修订的断言，以同一候选作为所有反馈组的起点；只在真实生成的语义错误处比较证明反馈。需在观察模型修订结果之前冻结新规格、独立事务 oracle、可达性约束、训练/留出样本、固定重复数及预算；语法解析错误独立记录。对于更复杂时序规格，不能把本研究的两拍布尔等价证明直接外推为全事务形式验证。

## 7. 复现与证据归档

本次 Mac 上传文件 `frame-pc-live-20261124-212714.tar.gz` 已保存为整理版：只移除 239 个 AppleDouble/Finder 元数据成员，保留 196 个实验文件原始字节。来源与整理后哈希、独立审计、配置、全量用量及形式结果均单独保存。原始上传和整理后的两份审计结果逐字节一致。复核环境为 Linux Python 3.12.14、z3py / CLI 4.16.0、Yosys 0.52；无需 API key，不需重新调用模型。[归档来源](../results/milestone3/frame-pc-live/provenance.json)

在原项目仓库根目录可执行：

```bash
python3 scripts/audit_egg_frame_pc.py \
  --archive results/milestone3/frame-pc-live/transcript.tar.gz \
  --output /tmp/frame-pc-live-audit.json
cmp /tmp/frame-pc-live-audit.json results/milestone3/frame-pc-live/audit.json

# 再做后验 formal；已下载的 fixture 可直接复用。
python3 scripts/m3_controller_replay.py --fetch /tmp/frame-pc-live-fixture
mkdir -p /tmp/frame-pc-live-extract
tar -C /tmp/frame-pc-live-extract -xzf results/milestone3/frame-pc-live/transcript.tar.gz
python3 scripts/check_frame_pc_candidate_formal.py \
  --run-dir /tmp/frame-pc-live-extract/frame-pc-live-20261124-212714 \
  --fixture /tmp/frame-pc-live-fixture --output /tmp/frame-pc-live-formal
```

`audit_egg_frame_pc.py` 重建完整物理评分、共同反例、最短诊断及证书、隔离会话、真实 usage 和首次合格用量；`check_frame_pc_candidate_formal.py` 在冻结 RTL 上重新对去重后的真实合格候选运行完整位宽和原版 RTL formal 检查。本次只新增真实结果和复核报告，原实验程序与协议不变。
