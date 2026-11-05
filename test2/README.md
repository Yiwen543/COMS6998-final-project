# test2 — 固定刺激下的 FIFO 监视器生成实验

本目录是新的独立登记，不替换此前的刺激生成实验或其负结果。
研究问题是：**相同输入序列和资源上限下，经过验证的 E-graph 反馈能否
提高 LLM 生成断言／监视器的正确性、有效检错率及成本效率？**

当前阶段：正式 B′/C′、隐藏仿真评分、72 个形式任务和只读审计均已完成。
完整结果见 [中文报告](results/live-report-v1/report.md)，独立参考验证见
[参考冻结记录](results/reference-freeze-report.md)。

36 次真实生成无重试，模型均为 `gpt-6.1-sol`。B′、C′ 每组三次最终候选都检出
6/6 种可观察注入故障，正确控制无报警/未知；平均 tokens 为120,197.67/128,038.33，
C′ 高6.523%，本轮未见仿真检错收益。形式反例检出次数为B′14、C′15，去重后两组
均涉及M01/M02/M03/M04/M06五种故障；差异来自B′第一次的M02超时。
12个PASS均为激活cover；正确控制的24个bmc/prove任务及7个故障bmc任务超时，
不能据此宣称候选已被完整形式证明。样本和六故障集有限，不能推广为E-graph普遍无效。

[比较图](results/live-report-v1/comparison.png)、[逐次数据](results/live-report-v1/endpoints.csv)、
[形式状态](results/live-report-v1/formal.csv)、[审计](results/live-report-v1/audit.json)
均可追溯至原始日志。两把暂存密钥已删除；本轮未commit/push。

## 产物与角色

| 目录 | 内容 | 是否交给候选模型 |
|---|---|---|
| `configs/` | 预登记、输入文件哈希；后续另建 live freeze | 仅公共限额 |
| `public/` | 规格、去除上游 FORMAL 的 RTL、固定 driver、开发输入、观察接口 | 显式白名单 |
| `private/` | 最终输入、单点故障源文件、独立 checker 控制 | 否 |
| `reference/` | Claude 作者包、之后的参考 checker 与独立复核 | 否 |
| `scripts/` | GPT/Codex 实现的测量、隔离、评分基础设施 | 不自动注入 |
| `results/` | 原始轨迹、覆盖、证明、提示词预览与阶段报告 | 仅指定开发证据 |
| `tests/` | 边界、隔离、无效输入和评分反向控制 | 否 |

`private` 表示候选 API 的访问边界，不表示加密或不保存。为了重现，文件留在
本地仓库，但候选模型没有仓库工具，只接收显式渲染的消息。提示词不会递归
读取目录。真实密钥仍使用仓库已有、Git 忽略的 `build/private/`，不放在 test2。

Claude 只根据规格与观察接口编写 Python **参考 checker**，再由全新 Claude
会话只读审查。GPT 实验会话生成单独的 SystemVerilog **候选 monitor**。
GPT/Codex 编写 driver、输入、故障控制和评估编排，但不代写或暗改 Claude oracle。
候选的内部期望值只是被测试的假设，不能作为裁判。

## 预登记方法

1. 固定深度 16、8 位、同步高电平复位、异步 front read 的 FIFO 合同。
   使用现有 ZipCPU sfifo 的**合成等价冗余 stress 变体**；它不是一颗新的自然 IP。
   上游原版作为实现对应控制。原版与变体的 Yosys 等价不等于规格正确性证明。
2. 清除模型可见 RTL 的上游 FORMAL 验证段，逐行留空保留源码位置；其他行不改。
3. 开发输入固定为 9/45/42 周期，最终输入固定为 61/129/163 周期；均含两个
   已计数的 idle 尾周期。六个单点故障版本预先生成，不能按候选结果挑选。
4. 先验证 Claude 参考 checker：独立有限规格控制、自测、正确实现轨迹、单故障
   轨迹与独立只读复核。逐对登记固定输入能否使故障产生可观察的规格违反。
   无法激活、X 敏感、不可判定的样本保留。差异检测本身不是规范判决。
5. 参考 checker、输入、故障目录、语义、driver、评分和 runner 均通过审查后，
   **另建 live freeze**。B′/C′ 各 3 次独立会话，每次 6 轮，每轮固定 6 个属性槽。
   上限均为 32,000 input tokens、8,192 output tokens、120 秒、最多 1 次重试。
   这些是新任务的预算，不通过缩短原刺激实验预算来制造优势。
6. B′ 使用规格、RTL、完整固定开发观察、400 个原始 DUT 计数及同策略开发反馈。
   C′ 仅多一份 egg/Z3 验证的关系与完整 guard。两组调用/输出/属性/工具上限相同。
   原始计数用可无损还原的字典编码，不能按等价类合并。相同 token 上限不等于
   实际提示词等长；本轮没有 placebo，不能把效果自动归因于纯语义。
7. 迭代只反馈编译结果、正确开发轨迹上的候选报警/未知/激活；不反馈任何隐藏
   故障或最终轨迹评分。每会话选最后一轮成功验证的候选，若没有则计 invalid；
   此选择规则在 live freeze 中明确核对。全部最终候选哈希冻结后才评分。
8. 仿真与形式结果分表。SBY `bmc` 检查有限深度，`prove` 尝试无界安全证明，
   `cover` 检查属性激活可达性。固定初始复位、禁止 reset 同时读写，不允许候选
   自加假设。48 深度/每任务 60 秒；UNKNOWN、TIMEOUT、ERROR 都保留。
   形式通过只涉及固定 DUT/假设，不能替代独立规格；覆盖激活也不能证明属性有用。
   [SBY 官方模式说明](https://symbiyosys.readthedocs.io/en/latest/reference.html)

候选模块只有只读公共输入和六组 `active/ok` 输出，可有有界内部状态。固定
wrapper 记录报警、继续跑完所有周期；形式 wrapper 添加 immediate assertions。
候选仿真在独立进程中重放已保存的观察，不接入 DUT，所以不能改变 DUT 覆盖。
这限定了本实验为受限 SV monitor 生成，不是任意 UVM/SVA 环境生成。

## 评价

- 先看正确控制上的误报和未知。存在误报/未知的 suite 不获得主要“有效检错”分数。
- 只在独立 oracle 确认可观察的 mutant/trace 对上计算检出率；同时报告全部未激活
  和未决样本，不能从报告中删除。
- 记录原始报警与合格报警。有效报警不能早于该轨迹的独立规范违反；重复报警
  不等于多个缺陷，同一 mutant 在多轨迹命中也只算一个独立 mutant。
- Token ROI = 合格的不同 mutant 检出数 / API input-plus-output tokens × 1,000。
  cached/reasoning token 是子项，不重复加总；mock 没有 API token ROI。
- 同时报属性激活、空检查、编译成功、未决、每条轨迹结果、仿真/重放/形式调用
  和时间。3 次重复仅作描述性比较，不声称显著性。

## 已运行与复现

离线阶段历史证据见 `results/phase1-report.md`，最新 mock 为 v5，最终评分 mock 为 v2。
以下路径均相对仓库根目录：

```sh
.venv/bin/python -m unittest discover -s test2/tests -v
.venv/bin/python test2/scripts/audit_observations.py --preflight test2/results/preflight-v2 --output test2/results/cross-tool-audit-recheck.json
.venv/bin/python test2/scripts/audit_pipeline.py --mock test2/results/mock-v5 --replay test2/results/mock-replay-v5 --preflight test2/results/preflight-v2 --output test2/results/pipeline-audit-recheck.json
```

全量重建输出必须用新目录，不能覆盖旧证据：

```sh
.venv/bin/python test2/scripts/preflight.py --output test2/results/preflight-reproduction
.venv/bin/python test2/scripts/formal_smoke.py --output test2/results/formal-smoke-reproduction
.venv/bin/python test2/scripts/runner.py --mode mock --preflight test2/results/preflight-v2 --output test2/results/mock-reproduction
.venv/bin/python test2/scripts/runner.py --mode replay --preflight test2/results/preflight-v2 --replay-source test2/results/mock-reproduction --output test2/results/mock-replay-reproduction
```

`prepare.py` 与 `reference_controls.py` 只用于首次创建，已有登记会拒绝覆盖。
依赖复用主仓库 `.venv`、typed extraction、egg 二进制、Z3 和 Coverage-3 parser。
实际工具版本与命令在 `results/preflight-v2/versions.json` 及各目录日志。

以下为已执行阶段的历史作者调用与离线评估命令；旧输出保留，勿覆盖或直接复跑：

```sh
.venv/bin/python test2/scripts/reference_role.py --role author --packet test2/reference/author-v1 --output test2/reference/candidate-v1
.venv/bin/python test2/scripts/evaluate_reference.py --candidate test2/reference/candidate-v1 --preflight test2/results/preflight-v2 --output test2/reference/evaluation-v1
```

作者成功后仅保留 key 供本轮已授权的一次独立复核；任一调用失败或复核结束即删除。
作者失败产物、控制失败和拒绝意见一律保留，GPT 不修 oracle。独立复核包需根据
真实作者输出/控制结果生成，不能提前伪造；live B′/C′ runner 的最终审计和冻结
也必须等参考合同确认后完成。

`runner.py` 已有 mock/replay/live 接口；live 依赖已建立的独立审阅及完整哈希绑定
`configs/live_freeze_v1.json`。SDK 连接复用主仓库的 `pilot_model.py`，不会悄悄换模型。
`final_score.py` 在全部最终候选哈希冻结后做隐藏评分；按仿真器分别使用16/18和15/18
可评分故障/轨迹组合。live 最终评分必须启用 `--formal`，不能省略登记的形式检查。
形式 FAIL 的可解码反例另交给冻结的参考 checker；未支持的格式保留 unresolved。
官方接口参考：[Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses)、
[GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol)。
