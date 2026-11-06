# trace_done 候选生成阶段：资格已通过，等待付费授权

2026-11-05。实际 Git main HEAD：`c25180848ebfe9a1f49da0aa5f579cac913e6428`。本阶段尚未生成任何真实 LLM 候选。准备工作的源码、配置、测试、回放和独立评分均有文件证据；不把 mock/replay 说成真实实验。

## 独立复核结果

Claude scope-v4 返回 **ACCEPT_SCOPE**，`adapter_changes_required=false`、`oracle_revision_required=false`。本次报告费用 $0.189521，耗时 32.892 秒。已授权的第二个复核名额因首轮接受而不使用。累计四次 CLI 调用报告费用 **$0.532023**；八次 OpenAI 输入计数接口的实际费用仍未知。没有新 oracle 作者调用。

四项低优先级建议仍保留：重复资格键的诊断、异常细节/部分产物路径、正确控制门禁抑制后的零值语义、复用计数器代表尝试而非全部验证通过。本轮固定资格清单已检查为 162 个唯一键；报告明确类别汇总以正确控制门禁为条件，失败时零值是门禁抑制，逐例标志仍保留。复用读取数按尝试解释，绑定拒绝另列为未决。不改动已经接受的评分核心，也不声称这些通用工具建议全部实现。

## 已冻结的研究条件

- DUT、规格、Claude frozen-v2 checker、固定开发/最终刺激、语义反馈、目标和资源上限均保持不变。checker SHA：`b44f32b27c11b968d23fd93ecf8b0d714e773460fc0b505d89adf23df3cd7dee`。
- B 为原始覆盖反馈；C 为 B 加已验证 E-graph 反馈。两臂共同内容完全相同，四组 C 反馈不变；没有 token placebo，结论只能归于整个反馈包。
- 各组 3 个独立 own-history 会话，每会话 6 轮，模型 gpt-6.1-sol/low。每次输入不超过 64,000 tokens、输出不超过 8,192 tokens，超时 120 秒；SDK 自动重试为 0，失败最多手工重试一次。正常 36 次生成，最多 72 次生成和 72 次随尝试输入计数。
- 所有 36 轮（包括无效/缺失/未运行）冻结后才读取隐藏评分；最终选择最后一个 compile-valid 程序，不按隐藏分数选优或修补。
- trace_done 仅在最后一个 post 可见，不增加 DUT 输入或时钟。共享评分 v4 分别报告普通 safety、未归因终点有限义务、正确控制报警、未知、无效和未达到目标。原始 12 类/144 对、N10 未暴露以及 38 个参考未知上下文全部保留。
- 形式 profile 仍为由基础设施控制确定的 cone，深度 24/z3，B/C 交错；6 个最终程序共 540 jobs，正确源每 job 10 秒、故障源 5 秒，每最终程序总体 720 秒并向物理见证工具传递剩余时间。trace_done=0 的投影不能证明 128 周期完成性，未触发 cover、超时和未知都保留。

新登记为 `test2/configs/controller_done_generation_v1.json`。资格冻结 `test2/configs/controller_done_generation_freeze_v1.json` 绑定 **900 个成员**，SHA：`3e64f64c1178973ae19be5dc52da5838f229ad2b187acbd5ff876bf8d1b7f5af`。它只表示已具备申请生成的资格，不授予 API 权限；独立生成授权文件当前不存在。

## 实际 token 和资源保护

| 组别 | 初始提示 | 原历史压力探针 | 64k 门禁 |
|---|---:|---:|---|
| B | 36,944 | 59,460 | 通过 |
| C | 40,573 | 63,089 | 通过 |

这四个实际计数的提示 SHA 与当前运行器一致，候选提示没有随评分修正而变化。911-token 的 C 压力余量不保证所有未来提示都能容纳，因此每次实际尝试都先计数，超限不生成并保留结果。失败的第一版计数没有删除。

新 API 适配器显式设置 `service_tier=default`、`prompt_cache_retention=in_memory`、`store=false`、官方 endpoint、无工具和独立消息；不依赖项目默认服务层级。服务层级含义来自[官方 Responses 参考](https://developers.openai.com/api/reference/python/resources/responses/methods/create)。本地 SDK 为 2.54.0。

持久 dispatch 账本限制最多 72 次计数/72 次生成。实际返回的模型、服务层级、输入/输出/总 token 和缓存/推理子集受检查；返回用量缺失、超过上限或与实际预计数不一致时停止后续 API 请求，剩余轮次仍冻结为 NOT_RUN/未决。连接失败、不完整或 JSON 失败的已发请求及未知成本不当作零成本，按登记的一次失败重试处理。

## 实际离线验证

十项生成端测试通过，含离线注入 SDK 故障：一次计数/用量错配后，后续请求停止，仍形成完整 36 轮冻结，调用数没有因本地拒绝而虚增。最早的九项测试也通过；十项版初次运行因测试没有提供模拟授权/冻结文件失败，修正测试夹具后通过，失败日志保留。这里的注入请求不是真实 API 调用。

当前运行器新执行了 36 轮 mock 和 36 轮 saved-response replay，各有 72 次编译工具调用、108 次开发 monitor 回放、8,280 个周期。全部提示、源码和开发反馈逐轮一致，也与先前已资格的 mock 一致。

当前 mock 使用已验证的相同程序与旧的平面回放记录做独立评分复用：5,832 份日志，0 次新评分回放。全部 36 轮/5,832 个样例分类与已接受的共享评分结果一致。复用输入明确为旧平面 `result_path/result_sha256` 格式；v4 的嵌套 `evidence_provenance` 输出不是该旧输入格式。真实阶段的 saved-response replay 可以重新回放评分，不把复用或 replay 计为独立 LLM 样本。

最终人工 mock 仍为普通 safety 0/106、另有 10 个 marker-only 信号、响应完成性 20/20、输入完成性 10/10 明确检出但 0 完全已决检出。所有会话未达到全部 11 类目标。这不是 C 收益或无收益的真实模型结论。

实际 RTL 开发覆盖计数固定如下；monitor 编辑不改变它们，行为义务或等价类不是 RTL 覆盖率：

| 实际计数类型 | 分母 | 开发并集未覆盖 |
|---|---:|---:|
| line | 110 | 7 |
| branch | 176 | 77 |
| expr | 248 | 160 |
| toggle | 2,634 | 1,726 |
| 合计 | 3,168 | 1,970 |

最后的只读审计核对了新冻结全部成员、实际计数 payload、当前 mock/replay、评分绑定、原 3486/212/239 个冻结成员和两份旧分数。没有为恢复上下文重跑旧实验，没有安装、提交或推送；历史测试不能称为本轮重跑。

## 新阶段费用申请

具体方案：`test2/tasks/axis_length_done_v1/qualification/candidate-generation-v1/proposal.json`。这是原 $9 预检之外的新生成阶段，**当前未授权**。

申请上限 **$35**：生成预留 $30，最多 72 次随调用计数的费用预留 $5。按[官方模型计价](https://developers.openai.com/api/docs/models/gpt-6.1-sol)及[计价页](https://developers.openai.com/api/docs/pricing)，当前标准输入 $2/M、输出 $10/M；本地生成保护保守按输入 $5/M、输出 $10/M 预留，每次最多 $0.40192，72 次合计 $28.93824。这个数是基于请求和 token 上限的本地预留，不是已知账单；计数接口费用及未返回的费用保持未知。缺失 token 用量不参与“免费高效率”结论。

批准后复用现有暂存 OpenAI key，执行生成→全轮冻结→saved-response replay→独立评分→固定形式日程→分层分析及审计，不在普通阶段停下来索取下一条 prompt。仅真实新增付费/权限/方向阻塞才再询问。当前不调用生成，不额外调用 Claude，不使用第二个复核名额，不再次索取 key。

复现/恢复入口：只读审计 `controller_done_generation_audit.py --output <新文件>`；生成命令 `controller_done_generate_v1.py --mode live --output test2/results/controller-done-live-v1` 需要新授权且在获准网络中运行；之后按新输出路径调用同运行器 replay、`controller_done_grade_v4.py` 与 `controller_done_formal_v3.py`。不要在授权前试运行 live，也不要为上下文恢复重跑已有 mock/实验。
