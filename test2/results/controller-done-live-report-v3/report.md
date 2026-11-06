# test2 trace_done 控制器：真实 B/C 运行与最终审计 v3

本报告对应 USD20 授权的新运行，不是旧实验重评分或 mock 模型结果。当前审计 HEAD 为 `c25180848ebfe9a1f49da0aa5f579cac913e6428`；旧审计的 HEAD 不代表当前分支。具体资源和未决结果以 [audit.json](../controller-done-live-acceptance-v3/audit.json) 与原始文件为准。

## 结果与可支持的结论

固定 DUT、独立 Claude checker、固定开发/隐藏刺激下，B 为原始覆盖反馈，C 为 B 加已验证的 E-graph 反馈。各3个独立会话、每会话6轮，gpt-6.1-sol/low，Standard。六个最终候选均通过正确 DUT 控制，检出11/11个可观察故障类型；N10在固定隐藏刺激下未观察到确定故障，仍保留在12个原始类型、144个 fault/simulator/trace pair 分母中。**C 未增加最终检出类型。** 本研究比较整个反馈包；没有 token 匹配 placebo，不能归因为纯语义收益，也不能把一个 IP、每组3会话概括成一般性结论。

| 组/会话 | 最终轮 | 检出类型 | safety 确定/完全解决 | response 确定 | input 确定 | 未决 pair | API tokens | 首达11类 | 到目标tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| B2_raw/1 | 6 | 11 | 106/68 | 20 | 0 | 38 | 247062 | 2 | 81499 |
| B2_raw/2 | 6 | 11 | 106/66 | 20 | 0 | 40 | 247753 | 1 | 39526 |
| B2_raw/3 | 6 | 11 | 106/68 | 20 | 0 | 38 | 245828 | 1 | 39090 |
| C2_semantic/1 | 6 | 11 | 106/68 | 20 | 0 | 38 | 272594 | 2 | 90034 |
| C2_semantic/2 | 6 | 11 | 106/68 | 20 | 0 | 38 | 270449 | 2 | 88987 |
| C2_semantic/3 | 6 | 11 | 106/68 | 20 | 0 | 38 | 270606 | 1 | 43660 |

安全性分母106，响应完成性20，最终未接收输入10。确定检出可以同时存在明确记录的未知；“完全解决”还要求没有参考/候选未知。所有正确控制共18 pair/候选，两个模拟器不是两个独立模型试验。详细逐轮数据见 `rounds.csv` 和两条 scores.json；首次未通过控制、无效轮次及未达目标轮次都未删除。

逐轮控制失败保留：B会话1第1轮，C会话1和2各第1轮；另有B会话1第4轮格式无效。B首达11类为2/1/1轮，C为2/2/1轮，本批次没有C更早达到目标的会话。固定6轮全部执行，没有看到中途分数就提前停止或追加某一组预算。

最终输入完成性0/10不能解释为模型没有终点检查：六个最终候选在这10个 pair 上都有终点报警，但全部也有更早报警、全部重叠普通安全性、且全部带参考未知。锁定评分要求终点报警且无更早报警，因此不给该层独立 credit。这个隐藏集不能隔离输入完成性能力；不修改这次分母、规则或旧分数。另一个结构性限制是checker第290–320行：末行s_valid1必使quiet-tail为0，故当前128-tail合同必同时保留确定input FAIL和drain_tail_short UNKNOWN；不可能靠多采样几个同类末行样例得到完全解决的input判定。

B会话2在N01上有12个候选未知pair，其中10个与已有参考未知重叠，净增2个未决pair；最终安全性完全解决66/106，其余五会话68/106。该B候选P1在边界未知时主动输出X，而另一个属性已经报告无依据数据。C最终没有这类候选未知；这是局部观察，不能证明C更正确或证明E-graph导致了差异。两组均保留参考未知38pair，分布N01=10、N04=10、N11=8、N12=10；任何未知都没有改写为PASS。

## 预算为什么从35降低到20

旧35方案按最多72次、每次64k输入/8192输出、较高的12h缓存写入费率及计数预留计算，属于保守最坏预留。它未执行。新v2在生成前登记并冻结，保留全部试验、模型、输入/输出上限和失败重试次数，显式采用GPT6 implicit缓存30m。核实费率下，输入写入USD2.5/M替代普通输入费，输出USD10/M；每次最坏预留USD0.24192，72次为USD17.41824。分配生成17.5、计数2.5，总上限20。

实际36次生成、36次随调用计数、0次重试。输入1475813、输出78479、合计1554292tokens；推理5165包含在输出中、缓存读155022包含在输入中，不能再相加。最大输入43871、最大输出3087，每次实际输入等于调用前计数。B总tokens=740643，C=813649，C多9.85711%。各会话实际tokens与首次目标成本均保留；完整预算终点ROI及成本到目标见审计 sessions，不把保存响应回放当成免费独立模型试验。

按已核实费率与实际缓存写/读明细估算，生成费用约 **USD4.102216**（若完整），**不是实际账单**。计数接口费用、最终账单仍未知，不宣称免费；2.5只是预留。36次调用的保守生成预留8.70912，加计数预留为11.20912，低于20。所有调用均有返回用量，没有把失败或缺失用量当0。官方费率依据：[模型](https://developers.openai.com/api/docs/models/gpt-6.1-sol)、[价格](https://developers.openai.com/api/docs/pricing)、[缓存](https://developers.openai.com/api/docs/guides/prompt-caching)（登记核实日2026-11-05）。

## 实验如何实现

1. 复用冻结的4份DUT源、规格和Claude checker。GPT没有修补oracle；独立全新会话复核已ACCEPT_SCOPE，第二个条件复核名额未使用。本阶段没有新增Claude调用。
2. 新固定开发集3条/230周期，隐藏集6条/每条214周期，种子分别6998201..3和6999301..6。输入及评价冻结在候选前完成；此前资格包含26构建、162物理仿真、33844周期，不冒充本阶段重跑。12个新单行fault源与旧fault哈希不同，但仍是同一IP。
3. 公共提示包只允许完整RTL、规格、真实源计数、开发观察；C另含4组已有组合语义证书。共同无损codec可恢复全部3168计数与230开发周期。提示不含隐藏fault、轨迹、参考实现或结果。每个会话只看自己的上轮候选和公共开发反馈。
4. GPT返回被动SV body和P0..P5。Yosys做语法/状态/边界资格，Icarus构建回放；不驱动DUT。`trace_done`只在最后post为1，所有pre/其余post为0，不增加DUT输入或时钟。开发反馈仅来自三条固定开发观察。
5. 每轮冻结prompt、response、SV、编译和开发反馈；36轮全部释放后才读取隐藏结果。最终候选按最后编译有效轮选择，不能挑隐藏高分。B会话1第4轮P5描述401>400字符而无效，原样保留；第5轮依正常反馈恢复。
6. 两次全新离线评分分别处理live候选与保存响应回放。每个计划轮固定162项，包含18正确控制和144faultpair；无效候选的162项全部保留为未决。独立grader与候选代码分开，不用候选给自己评分。重新解析原始MON位、实测HEX输入及行/周期哈希；仅规范化Icarus `$finish` 中已知运行根路径，保留原始哈希。
7. 原始RTL计数固定为line110（未命中7）、branch176（77）、expr248（160）、toggle2634（1726），共3168/未命中1970。候选是被动monitor，修改它不会提高这些覆盖率。故障检出、行为类别与语义等价类均未冒充RTL覆盖率。

接口说明限制：描述400字符上限存在于静态validator，但当前SYSTEM、公共接口文本和JSON schema没有明确表达这个上限。因此这一次401字符格式失败不能被解释为C的语义或验证能力优势。未来应先登记新提示/schema版本，对两组共同明示约束；本次不修剪产物、不更改无效判定。该无效轮次晚于该会话首次达到目标的第2轮，首次目标成本仍按全部实际调用计算。

## 固定形式日程与限制

形式profile由基础设施控制预先确定，未根据C结果挑选。每个最终候选正确DUT的6slot×bmc/prove/cover（各10s），12mutant×6slot bmc（各5s），共90项/候选、540项；深度24/z3/cone，每最终候选整体720s并向物理见证传递剩余截止时间，B/C交错执行。所有TIMEOUT、UNKNOWN、ERROR、未达到cover与未运行都保留。

| 组/会话 | 全部状态 | correct prove PASS slots | 早期物理前缀 FAIL 的 mutant IDs |
|---|---|---|---|
| B2_raw/1 | {"FAIL": 3, "PASS": 11, "TIMEOUT": 76} | [] | N01,N04,N09 |
| B2_raw/2 | {"PASS": 6, "TIMEOUT": 84} | [] | 无 |
| B2_raw/3 | {"FAIL": 4, "PASS": 23, "TIMEOUT": 63} | [5] | N01,N04,N09 |
| C2_semantic/1 | {"FAIL": 43, "PASS": 21, "TIMEOUT": 26} | [5] | N01,N04,N05,N06,N07,N08,N11 |
| C2_semantic/2 | {"FAIL": 54, "PASS": 8, "TIMEOUT": 28} | [] | N01,N04,N05,N06,N07,N08 |
| C2_semantic/3 | {"PASS": 6, "TIMEOUT": 84} | [] | 无 |

物理复现且较早独立参考前缀FAIL的mutant类型，三会话合并后B为 `['N01', 'N04', 'N09']`，C为 `['N01', 'N04', 'N05', 'N06', 'N07', 'N08', 'N11']`；仅C出现的类型为 `['N05', 'N06', 'N07', 'N08', 'N11']`，仅B为 `['N09']`。逐会话分布保留在表和审计中，合并集合不是三个重复实验的平均效果。它衡量物理前缀反例发现范围，不能改称为参考逐样本确认的选定断言报警，也不回写固定轨迹分数。若某组有局部范围优势，结论只限这项次级诊断；不能从原生FAIL数量或该集合直接推出总体monitor正确性、纯语义因果或128周期完成性收益。

trace_done恒0的短深度形式投影**不能证明128周期有限完成性**。BMC/cover/induction不混为证明。物理见证采用原始输入双模拟器回放并复现所选slot报警；独立参考只检查到前一周期post的物理前缀，所以前缀FAIL不等于该选定pre报警已被参考逐样本确认，前缀PASS也不自动证明候选误报。对应报警/类别一致性继续UNRESOLVED，不把它们补造成通过。

还必须联读每slot的prove、cover与实际义务guard：依赖trace_done的slot在本投影中可能不激活，或保持active但ok恒真，相应prove PASS可能是空泛结果。即使active cover PASS也不说明完成性义务被检查，不能称为有效完成性或总体monitor正确性证明。全部原生状态与模式都保留，未达到cover只表示该有界/投影检查未达到目标。实际monitor状态位数另见rounds.csv；相同8192上限不意味着状态规模或求解难度相同。

## 成本、审计与文件

- Live开发：35次Yosys和35次Icarus，105次monitor回放/8050周期，0新物理DUT仿真。原运行器71“编译调用”包含静态校验尝试，实际native70，二者均保留。
- 两条全新评分各5670次回放/1184540周期；累计审计11340条原始日志/2369080周期，148种实际物理观察向量。回放不是新LLM样本。
- 形式540项，墙钟2967.483s。物理见证188次仿真、已知1246周期，另有0次周期未知；构建26次。详见审计，不把monitor replay算成DUT执行。
- 新资格冻结900个成员、旧3486/212/239成员与两份旧score哈希均核对；HEAD从实际Git读取。没有提交、推送、安装工具或修改旧冻结运行器。11项当前API保护测试是本阶段离线证据；历史76项套件、语义证明与旧实验没有为恢复上下文重跑。
- 独立Claude checker SHA为 `b44f32b27c11b968d23fd93ecf8b0d714e773460fc0b505d89adf23df3cd7dee`；旧controller score SHA为 `f13161340a46c7360002e54992be0a7aba9c1d47a70fbe6f169bba8952fe2651`。当前生成配置/900成员freeze/授权/所有release和scores的完整SHA见audit evidence_sha256；旧冻结清单的完整SHA和成员数见old_freezes。
- 新增分析审计脚本的一次括号语法错误在调用前被发现并修复，检查记录位于live-analysis-preparation-v2/syntax-check.json；这没有更改候选、评分或形式生产器。

| 文件 | 用途 |
|---|---|
| configs/controller_done_study_v1.json / scoring_v4.json | 科学协议、固定原始分母、共享评分定义 |
| tasks/axis_length_done_v1/input-freeze.json / evaluation-freeze.json | 刺激、物理观察、独立标签、fault来源和哈希 |
| configs/controller_done_generation_v2.json / generation_freeze_v2.json | 生成配置、20美元资源门禁和900成员资格冻结；不是付费许可本身 |
| configs/controller_done_generation_authorization_v2.json | 用户这一次付费授权及绑定哈希；不授权额外研究调用 |
| results/controller-done-live-v2/run.json | 六个会话ID、模式、源与数据绑定 |
| 各round/prompt.json、response.json、snapshot.json | 精确请求、模型产物及该轮全文件哈希 |
| 各round/development-feedback.json、development-cost.json | 只含公共开发反馈与原始资源记录 |
| calls.jsonl / api-dispatch.jsonl | 实际调用、重试、响应、token、缓存、服务层级与保守资源预留 |
| release.json / final-candidates.json / resource-release.json | 全轮冻结、按编译选择终点、调用账本绑定 |
| live-grade-v2及live-replay-grade-v2/scores.json | 每轮162项、各层确定/完全解决/未知、正确控制门禁 |
| live-formal-v2/summary.json及各job原始文件 |540项原生状态、日志、物理见证、剩余时间与未决结果 |
| live-acceptance-v3/audit.json / rounds.csv | 原始位和向量核对、旧冻结审计、所有轮与会话成本、未达目标 |
| 本目录manifest.json | 本报告、审计、分析代码哈希；分析代码不属于候选提示或评分oracle |

## 复现与下一项最小任务

实际执行命令、各阶段退出状态和耗时保存在 `controller-done-live-post-v2/progress.json` 及分阶段日志。原编排在新审计的catalog字段适配处失败，日志与v2脚本完整保留；此前模型/回放/评分/形式阶段均已完成。只用新audit_v3读取已冻结的实际mutant catalog并重新审计，未重跑模型或物理/形式实验；恢复记录在 `controller-done-live-post-recovery-v3/`。`controller_done_live_post_v2.py`编排保存响应回放、两个fresh grade、固定形式日程和原始证据审计，默认拒绝覆盖任何输出。不要重启已完成的付费生成来恢复上下文。需要新复现时，对已冻结响应使用新的输出目录；新独立模型样本必须另登记、另授权。提供的复现命令不等于已经额外重跑。

下一最小研究主线是隔离“最终未接收输入，但此前没有安全性错误”的义务；审计物理可达性及尾段/未知约束，保留本轮0/10和全部重叠样例。不直接重跑这套饱和故障集。另行登记的物理合成义务控制若已执行，结果列在下节；它不能替代新的自然故障隐藏集或独立LLM样本。新的类别敏感评分可先在固定合成义务控制上检查，但不能把它称为RTL覆盖或真实DUT误报；需要真实DUT结论时必须提供物理见证。若纯语义因果是目标，另登记token匹配placebo和固定资源；当前B/C仅支持整包比较。若超出现有oracle的有限轨迹范围，先准备Claude作者/全新复核包，不由GPT修补。条件性独立作者与全新复核说明已准备，尚未调用或授权。任何下一付费阶段都需具体调用数、模型、token/费用上限和离线门禁后单独授权。

## 追加的物理输入义务控制（独立登记、事后诊断）

状态：`PHYSICAL_INPUT_OBLIGATION_CONTROL_QUALIFIED`。这在原候选全部冻结后另行登记，使用seed6999401、150周期和4处明确标注的合成RTL改动；不是自然新故障，不是新的独立B/C实验，不加入原12故障/144pair分母。为了避免影响既定形式超时，物理工具等待该形式日程结束后才运行。候选和原始分数均未修改。

资格门禁：`{"correct": true, "dual_physical_agreement": true, "isolated_input": true, "unavoidable_unknown_retained": true}`。新物理构建4次、仿真尝试4次、完整周期600，另有0次周期未知；候选回放24次/3600周期；新增API/LLM样本0。参考仍为原Claude checker，确定终点FAIL与short-tail UNKNOWN均原样保留，不能把这项诊断宣称为完全解决的128周期完成性证明。

| 会话 | 两条正确控制通过 | 隔离输入终点报警且无更早报警 pair | 未决 pair |
|---|---|---:|---:|
| B2_raw/1 | True | 2 | 2 |
| B2_raw/2 | True | 2 | 2 |
| B2_raw/3 | True | 2 | 2 |
| C2_semantic/1 | True | 2 | 2 |
| C2_semantic/2 | True | 2 | 2 |
| C2_semantic/3 | True | 2 | 2 |

详细原始物理输入、输出、双模拟器比较、参考标签及候选MON位保存在 `test2/results/controller-done-input-isolation-v1`。资格与候选观测是两件事：控制资格通过不意味着每个候选都检出；未决pair继续未决。其用途是检验原输入层0/10是否受前置安全性重叠影响，并为下次独立研究定义可区分的义务，不能制造本次C优势。
