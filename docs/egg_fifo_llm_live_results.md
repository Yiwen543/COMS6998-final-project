# FIFO LLM 反馈闭环 · 首次真实 API 实验

2026-11-24 的 MacBook 实测完成了 raw、ordinary、egg 三组各三轮的 Responses API 调用。**三组第一轮就生成了完全相同、满足规格的四条断言，并且后两轮均正确报告了同一诊断。egg 增加了反馈用量，但在本任务上没有观察到额外的验证质量收益。** [原始评分与逐调用复核](../results/milestone3/fifo-llm-loop-live/audit.json)

## 实验对照

| 配置 | 值 |
| --- | --- |
| 请求与返回模型 | `gpt-6.1-sol` |
| 请求 reasoning effort | `low` |
| 返回 service tier | `default` |
| 每次输出上限 | 1,024 tokens |
| 三组反馈策略 | SMTBMC 日志；日志加普通改写和结构化语义反馈；日志加 egg 和同样的结构化语义反馈 |
| 对照规模 | 每组 1 个会话，固定 3 轮 |
| RTL | 固定提交的 4 深度、8 位 AXI-stream FIFO，原版及 4 个单字段故障对照 |

九份回执均记录 HTTP 200、completed、独立的响应 ID 及实际用量。第一轮的三份请求逐字节相同；后六份请求均可由各组自己的先前候选、实际存档反馈和固定提示重建。未发现其他组的对话或三个不可见故障的身份和评分泄漏。归档中的配置记录 `low`，API 用量回执没有独立回传该参数。九次均报告 0 reasoning tokens 和 0 cached/input cache-write tokens。这里依据的是客户端保存的请求和用量回执，没有另外核对 API 账户发票。[实验协议](egg_fifo_llm_loop.md) · [归档核对](../results/milestone3/fifo-llm-loop-live/audit.json)

## 验证效果

| 三轮指标 | raw | ordinary | egg |
| --- | ---: | ---: | ---: |
| 首次生成完全通过评分的断言 | 第 1 轮 | 第 1 轮 | 第 1 轮 |
| 通过规格等价检查的候选 | 3/3 | 3/3 | 3/3 |
| 原版 FIFO 的 12 状态 BMC 通过 | 3/3 | 3/3 | 3/3 |
| 末轮注入故障检出 | 4/4 | 4/4 | 4/4 |
| 错误断言通过原版的轮数 | 0 | 0 | 0 |
| 有诊断评分的两轮 | 2/2 | 2/2 | 2/2 |
| API 调用次数 | 3 | 3 | 3 |

三组九份响应总共只生成了 **1 种有序断言集合**，即 `active && valid_lost`、`active && data_changed`、`active && last_changed`、`active && user_changed` 四项违例式。所有 32 行布尔赋值核对通过。第一轮各组报告 `none/-1`，第二、三轮均报告 `TLAST/5`。

45 次 BMC 的归档日志包含 9 次原版通过和 36 次故障失败，9 次独立 cover 均在状态 5 到达阻塞前件。36 份反例实际是 4 份不同的原生见证各重复九次。重新解码 YW 的外部输入并比对 VCD 的顶层引脚和相邻沿前观测，共核验 216 个状态，均与违例表达式求值一致。另用固定 RTL 在本地 Yosys 0.52、Z3 4.16.0 对这唯一的断言集合重新执行五个 BMC 和一个 cover，复现了相同状态、失败字段/编号和布尔观测。用户的原始 Mac 归档没有记录精确的 Yosys 或 Z3 版本。[真实运行汇总](../results/milestone3/fifo-llm-loop-live/summary.json) · [逐轮复核](../results/milestone3/fifo-llm-loop-live/audit.json)

还用上传的 4 份不同原生见证分别驱动原版和对应故障版 RTL。8 次实际 Icarus 仿真共得到 48 个沿前样本。全部在第 4 步观察到阻塞，在第 5 步仅故障版违反对应字段。数据翻转样例中原版保持 `TDATA=0x01`，故障版从 `0x01` 变为 `0x00`。TLAST 样例中原版保持 0，故障版从 0 变为 1。[针对真实在线候选的物理回放](../results/milestone3/fifo-llm-loop-live/physical-recheck/summary.json)

诊断器向 raw 报告 `check_2` 在状态 5 失败。因为模型自己生成的第三项本来就是 `last_changed`，只读这条原始日志即可定位 TLAST。ordinary 和 egg 还收到布尔采样向量，但最终响应完全相同。这里的 2/2 诊断分针对一个可见诊断样例的重复观察，四种注入故障是断言的评分对照。

## 证明反馈究竟提供了什么

ordinary 对每一轮相同的候选均找到了 3 个具名分配律步骤（访问 43 个表达式）。egg 找到 5 个具名步骤（3 次分配、2 次交换，包括一次逆向使用）；全链均可独立重放。两者提供了同样的等价判定及同样的失败采样值。ordinary 的下一轮提示附了完整 3 步摘要，egg 附了前 4 步和总步数 5，完整证明留在存档。反馈文本分别为 354、852 和 893 个 UTF-8 字节（不含结尾换行及共同提示）。最后一轮的反馈只保留在档案中，未参与第四次调用。三组返回内容没有变化，无法判断模型是否阅读或利用了具体改写步骤。[九次实际请求、回执与全证明](../results/milestone3/fifo-llm-loop-live/transcript.tar.gz)

## API Token

全部 9 次模型调用累计 **5,619 tokens**，其中输入 5,106 和输出 513。三组逐轮数据如下。每个单元格为本次调用的输入、输出与总数。

| 组 | 第 1 轮 | 第 2 轮 | 第 3 轮 | 累计输入 | 累计输出 | 累计总 token |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| raw | 326/57/383 | 481/57/538 | 637/57/694 | 1,444 | 171 | 1,615 |
| ordinary | 326/57/383 | 602/57/659 | 879/57/936 | 1,807 | 171 | 1,978 |
| egg | 326/57/383 | 618/57/675 | 911/57/968 | 1,855 | 171 | 2,026 |

- ordinary 相对 raw 增加 363 个 token（22.48%）。
- egg 相对 raw 增加 411 个 token（25.45%）。
- egg 相对 ordinary 增加 48 个 token（2.43%），分轮增量为 0、16、32。

差异全部来自输入。三组都在还没有反馈的首轮以 383 tokens 生成了正确断言，后两轮继续按预注册的三轮预算调用。若只计算达到首次合格候选的用量，三组均为 383。报告采用实报 token，不把它直接转换为实际扣费。[来源为九份 API 使用量回执](../results/milestone3/fifo-llm-loop-live/audit.json)

## 结论与下一项研究

本轮任务的抽象层已经为模型定义了阻塞前件和四个失败字段，规格与断言一一对应。raw 在首轮达到满分，ordinary 和 egg 没有留下可以提高的质量空间。所有组都只有一次会话，三轮是在同一任务上的连续迭代，不能当作独立样本。实验支持可复核的断言证明与 LLM 反馈链路实际工作；验证效果、诊断和 token 三个指标均未给出 egg 相对强普通对照的优势。

下一项实验可转向现有 AXI 帧长调整器的自然语言规格，提供原始接口、跨拍条件和事务观测，考察多条真正需要推理的监视器。例如输入计数应在 valid 与 ready 同时成立时增加，长度边界 4/8 的等号归属，数据与状态两条通道的独立阻塞，以及复位后的计数清除。先固定任务及正确对照，另可在三组都从同一错误监视器出发时测量 LLM 依据反馈纠正验证断言的能力。普通组和 egg 组共享等式、独立等价检查、反例和同一模型调用预算，时间、采样与位宽始终作为语义边界。主要评价规定预算内的合格断言数、新增误报及故障漏检、诊断与每个合格结果的 token。该设计需要独立约束和新的对照，当前未运行。

## 环境与复核命令

沿用 [FIFO 的环境设置](egg_fifo_assertions.md#环境脚本与复现)。本次上传文件 `fifo-live-20261124-173053.tar.gz` 的 SHA-256 已登记。归档保留 236 份实验文件的原始内容，去掉 Mac 压缩包自动附加的 303 个 AppleDouble 元数据条目及 tar 文件头。对原上传包和整理后的证据包运行审计，结果逐字节相同。审计需要 Python 标准库及固定的原 RTL 文件；重新执行物理回放还需要 Icarus。`make test` 的 62 项测试和旧引擎的 7 项测试也已复核。四个额外的审计负例分别篡改用量、会话历史、普通证明和解码输入，均被拒绝。[来源清单](../results/milestone3/fifo-llm-loop-live/provenance.json)

```bash
python3 scripts/m3_controller_replay.py --fetch /tmp/live-audit-fixture
python3 scripts/audit_egg_fifo_live.py --archive results/milestone3/fifo-llm-loop-live/transcript.tar.gz \
  --rtl /tmp/live-audit-fixture/public/rtl/axis_fifo.v --output /tmp/fifo-live-audit.json
cmp /tmp/fifo-live-audit.json results/milestone3/fifo-llm-loop-live/audit.json

unpacked=$(mktemp -d)
tar -xzf results/milestone3/fifo-llm-loop-live/transcript.tar.gz -C "$unpacked"
python3 scripts/egg_fifo_replay.py --rtl /tmp/live-audit-fixture/public/rtl/axis_fifo.v \
  --candidate-grade "$unpacked/fifo-live-20261124-173053/raw/round-01/rtl" \
  --output /tmp/fifo-live-physical
```

`audit_egg_fifo_live.py` 从归档重建各组历史，逐轮核对 API 账本和候选、证明路径、源文件哈希、真实 RTL 检查日志、反例输入与波形、反馈及最终评分。复核已归档的完成运行，不发起 API 请求。固定 RTL 和规则沿用旧实验；这一验证检查归档内部一致性和独立可重放证据，API 的实际账单需使用提供方的用量记录。
