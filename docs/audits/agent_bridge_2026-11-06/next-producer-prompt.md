请在现有 COMS6998 项目中继续推进下一项最小的、API-free 的维护阶段。协调端发送前已核对你的线程为空闲；这不是对进行中工作的中断，也不是仅提醒潜在问题。用户最新要求继续按独立复核反馈推进，并要求在没有已确认的明显实质风险前不要打断正在工作的 Codex。

<transcript_evidence>
用户：根据独立复核的反馈和修订策略以及未来最合理的推进步骤，继续向“核对COMS6998项目状态“（推进project的chat）发送后续继续推进的步骤的prompt，但在核验的chat没有发现有明显实质性风险之前不要打断做project的codex的进度或者仅提醒潜在问题，如果需要api key可以找我隐式发送
</transcript_evidence>

先按 AGENTS.md 读紧凑 HANDOFF/PROJECT_STATUS，按需读协议/决策。仓库 /Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project。当前实际HEAD c25180848ebfe9a1f49da0aa5f579cac913e6428，dirty/untracked全部保留。上轮P02 PASS_WITH_LIMITS只关闭P01-R1报告披露；C01封存已授权USD20 cohort，不能重启。P02/review.json SHA16df57aa2858b9bbb0f331d6a660483d3c7c5b83ec4542a19a2de05ba3e45b3e。当前4套冻结4837成员新鲜核验无失配。近期6页presentation已完成；协调端正在把该固定产物交原复核线程作结论/数据一致性审查，你无需重做或等候其无实质风险的建议。

本阶段目标是把P01-R3/R2尚开放的自动审计能力补成可运行、可检验的新版维护工具，先R3后R2；不是重评旧主分数或证明monitor正确。只新增版本化分析脚本/测试/输出，不改冻结producer、DUT、规格、Claude checker、candidate、旧评分规则/结果/报告/授权或presentation。开始前列输入/输出allowlist和冻结成员检查，选未占用的新版本名，输出目录拒绝覆盖；记录使用的保存证据SHA、当前HEAD与工作树。不得把这一维护计划当作新科学比较或预算授权。

第一检查点：R3 status-aware ledger validator。从现有 calls.jsonl、api-dispatch.jsonl、prompt/snapshot、count/resource release 保存证据验证dispatch→returned/error→call一一对应、唯一身份、context/prompt digest/count、response_id、requested/returned model/tier、usage及subset/quota绑定。成功/失败/缺失返回分别处理；失败或缺用量保留UNKNOWN，不能填0，不能把actual36×4的成功格式硬编码为所有失败路径的标准。用小型离线fixtures覆盖缺失returned、重复identity、串session/context、usage/model/tier/count错配及失败缺用量，确认应拒绝或明确unresolved的情况不会接受。实际本批36calls/144events应用新版并另存结果，不改原账本。R3完成后封存独有E03a交接与精确源码/测试/输入摘要/结果快照，给出命令、退出码、解析成本及开放项。

第二检查点：R2 saved-witness-chain validator。仅重解析已保存的94条BMC链：native job身份/slot、VCD→literal transport inputs→两个模拟器原始PRE/POST→rows→MON selected sample/slot→既有reference prefix及判定。可以对保存rows调用精确冻结checker纯函数，但不能启动DUT/native/formal/monitor重放或网络。selected pre(S)与reference只到post(S-1)的范围必须保留：20物理报警复现/较早前缀FAIL不升级为同样本类别确认；74未复现继续unresolved，无参考判定不能叫oracle UNKNOWN，更不能统一归因为X转换。完整链的一致性验收与候选正确性/误报判定分开。轻量fixtures涵盖缺失/截断文件、输入/时序偏移、错slot/phase/prefix、raw MON/rows改动、checker hash错配、unknown/缺证据；只改临时fixture副本，保留拒绝证据。绑定源码、原始依赖和结果，另封存E03b。不能只对比两个来自同一producer的摘要来称独立验证。

每个检查点完成请在本会话给出精简交接路径和SHA，协调端会读取并交现有“复核 test2 项目”做独立审查。你可继续已经授权的独立维护步骤；勿自宣独立通过、勿自行创建重复review chat。共享HANDOFF/STATUS只由你更新，复核线程仅写其审查产物。普通修复/版本选择不需要再问用户；若独立复核只发现非实质/潜在问题，协调端会记录并等你空闲或明确安全点再反馈，不随意插入你的工作。

R3/R2阶段验证与独立验收后，最多再准备一份下一研究阶段的gate表/方案，不执行新科学实验。优先解决形式表示支持范围和selected-sample reference范围，再考虑独立数据/token-matched placebo等新比较；说明原轨迹检错已饱和、无纯语义因果结论。新的oracle语义必须由独立Claude新版本作者/复核完成，GPT不能改。历史H1/H2、未来L1与真实formal表示限制都保留，不能为关闭问题删旧结果或美化C。

权限/安全：本提示授权的是本地新增审计分析、必要轻量fixture测试和保存证据验证；不含新付费API/count/Claude/模型、DUT仿真、formal、monitor重放、安装、删除结果、commit/push或改变资源帽。此阶段无需API key，不要索要、读取、恢复或暴露任何key。若下一步确实需要服务，先只报告服务、用途、调用数/费用帽、为何离线不足及安全隐藏输入方式，由主聊天协调；用户愿意提供key不等于新增付费授权，不在聊天里接收secret。后台heartbeat仍未建立，不声称无人值守自动联通。
