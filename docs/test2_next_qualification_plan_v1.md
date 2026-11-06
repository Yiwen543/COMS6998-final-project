# test2 下一阶段资格计划 v1 — 2026-11-05（America/New_York）

本文件只是一份有边界的计划，尚未登记为可执行实验。对应草案为 `test2/configs/controller_next_qualification_draft_v1.json`：`live_allowed=false`、`generation_authorized=false`、`native_execution_allowed=false`、`data_generation_allowed=false`，实验入口为 null。本阶段不需要 key，不调用服务，不生成新数据或候选，不启动 Yosys、仿真、形式工具或 monitor 回放。已关闭的 USD20 授权不能沿用。

下一项最小研究任务是：在 G0 的新接口设计门禁之后，另行授权一个小型、公开的形式表示资格包 G1。先弄清工具实际支持的位宽、四态值、采样和复位语义，再讨论新 oracle、时间义务及 B/C 对照。不要直接重跑已经饱和的旧 cohort。

## 当前证据与验收范围

P05、P06 均独立返回 PASS_WITH_LIMITS。机器可读验收记录是 `test2/results/controller-done-audit-maintenance-closure-v1/independent-acceptance.json`，绑定精确 review、manifest、源码、测试、结果及范围。

- P05 接受新增 companion validator 对**当前保存格式、精确 94 条 BMC 链**的核验能力，限定关闭 P01-R2。原 `controller_done_live_audit_v3.py` 没有修改，不因引用 companion 而自动获得通用验收能力。
- P06 接受 ledger v2 的全局 halt 修复，关闭新版的 P04-R1；P01-R3 仅限**严格串行保存格式和本批**。历史事件缺失的 request ID/context 不能补造，也不支持并发交错账本。
- P05 的 25 项定向测试、15 个独立探针，以及 P06 的 32 项定向测试、14 个独立 canonical 探针，均属于各自记录的生产／复核阶段。E05 只做哈希、元数据和文档检查，没有重跑这些测试、审计或历史实验。第四稿的 11 个拒绝控制／2 个 unknown 控制仍是第四稿证据，不改称最终稿新跑。
- 见证链仍是 94 条一致、20 条物理报警复现且较早参考前缀 FAIL、74 条未复现且未记录 oracle verdict。全部 94 条科学归因仍为 UNRESOLVED。2797 份依赖中有 1545 份匹配 P01 独立历史锚；其余 1252 份记录当前内容／身份绑定，不具有同等独立历史锚，也不证明 SMT 语义等价。

P04 证据纠正必须随结论保留：原存档 fixture 的 `snapshot.response=null`，但 calls 有 accepted parsed response。因此**原样 v1 实际 REJECT**（response/snapshot mismatch），不能再引用为“原样 PASS”。只在临时深拷贝中绑定已经记录的 accepted response 后，v1 PASS、v2 因 persistent halt REJECT；另有独立 canonical 反例确认真实代码缺陷及修复。P04 原文件和历史 CHANGES_REQUIRED 保留，序列化差异的原因仍 UNKNOWN。

科学结果没有改变：六个最终 monitor 均检出 11/11 个可观察类型；原始 12 类型／144 pairs 保留 N10。B=740643、C=813649 实际 tokens，C 多 9.8571%，没有增加最终固定轨迹检错类型。540 项 native 状态仍为 75 PASS／104 FAIL／361 TIMEOUT；94 个 BMC FAIL 分为 20 物理报警复现和 74 未复现（均 C：7 correct／67 mutant）。B3/C7 是较早物理前缀类型的合并范围，不是同样本／同类别确认或重复试验均值。该 cohort 没有 token 匹配 placebo，不能作纯语义因果结论。

## 已验收入口与未来集成边界

当前账本入口为 `test2/scripts/controller_done_ledger_audit_v2.py`，对应结果 `controller-done-ledger-audit-v3/audit.json`；不要用被 P04 指出缺陷的 v1 代替。当前见证链入口为 `test2/scripts/controller_done_witness_chain_audit_v1.py`，对应结果 `controller-done-witness-chain-audit-v5/audit.json`。

两者都是固定历史范围、拒绝覆盖输出的诊断入口。账本入口绑定旧 registration/grant/run；见证入口绑定旧 run/formal 路径、P01 锚和 checker SHA。它们不是本计划的新实验入口。未来 pipeline 必须另建版本化 schema/adapter、不可变输入与 release 锚、失败测试及独立验收；不得 patch 冻结旧 runner 或把新数据伪装成旧格式通过。

未来 gate 必须区分三件事：证据链一致、科学归因是否确定、费用是否已知。REJECT 不得作为有效证据放行；UNKNOWN、UNRESOLVED、缺用量和费用不得改为零或通过。`resource_halt` 一旦发生，就跨重试、轮次、会话禁止后续 count/generation 请求标志与派发；只允许无请求、无返回用量的 NOT_RUN 记录。

## 按依赖排列的门禁表

下表每行均是拟议阶段。本阶段各行的执行额度为零；完整产物、验收和停止条件见草案 JSON。G0→G1→G2→G3→G4→G5，不跳过依赖。

| 门禁 | 现有证据 | 待解决问题 | 最小产物 | 客观验收／停止条件 | 角色 | 预算／资源状态 | 新授权／服务 |
|---|---|---|---|---|---|---|---|
| G0 新 pipeline 证据门禁 | P05/P06 已接受固定历史 companion | 未来格式与锚如何绑定？ | 新 schema/adapter 设计、release 规范、失败矩阵 | 新格式独立资格；halt 后请求、孤立事件、泄露或锚失配立即拒绝。不能仅复用旧硬编码路径 | GPT 基础设施＋独立复核 | 当前 0；未来 API-free 实现另列范围 | 当前只允许写计划；新实现另行授权维护范围 |
| G1 形式表示资格 | 一例 X→anyseq 已确认；74 条不能统一归因 | 哪些运算、位宽、phase/reset 语义受支持？ | 公开控制包、支持矩阵、固定工具/profile/source manifest、成本账本 | 支持类正／负控制全部符合预先标签；不支持／未知／空泛结果不得获得正确性 credit。支持类出现未解释偏差即停 | GPT harness/transport；独立语义／控制复核；GPT 不写 DUT oracle | 拟议上限见下节；未授权、未执行 | 新的本地科学/native 资格授权；无需付费 API |
| G2 参考范围与采样合同 | 现 checker 只检查到 post(S−1)；末端输入层仍混有安全性／unknown | 如何判断 selected pre(S)、类别与有限截止？ | 新公开合同、Claude 作者包清单、全新会话复核包；必要时新 oracle/selftests/freeze | phase、输入接收边沿、截止、fairness、UNKNOWN 明确且独立接受；范围含糊或未经复核则停 | Claude 独立作者＋Claude 全新会话复核；GPT 只做接口和组包 | 当前 0 调用；拟议首作者 1 次＋复核 1 次，模型/token/费用/时间帽未定 | 新合同版本与独立验收；任何服务均需具体新 proposal/授权，当前不索 key |
| G3 新任务／数据资格 | 旧任务最终 11/11 饱和；一 IP；新 seed 不等于新 IP | 能否独立区分 safety、响应和末端输入完成性？ | 新 spec/ABI/data 版本、固定 dev、封存 hidden final、可达性与正确控制资格、分母规则 | 真 DUT 结论必须物理可达且有独立参考；合成控制另报。重叠、不可观察、unknown 不删分母；不能按 C 结果挑目标 | GPT driver/data 基础设施＋独立参考／资格复核 | 未登记种子、资源或数据生成；当前 0 | G1/G2 后另行登记并授权新科学资源；可选 B-only 难度探针也须事先登记／授权 |
| G4 公平比较与成本 | 本批只比较整个 B/C 反馈包，C tokens 更高 | 支持整体包结论还是纯语义因果？ | 新 B/C registration；若要纯语义再登记 P；完整模型/缓存/顺序/资源/token 规则 | DUT/reference/stimuli/模型/上限相同；P 实际 token 匹配容差合格；不按 C 优势选 profile/预算。帽未明确、匹配失败或 halt 后请求则停 | GPT 候选生成；独立 Claude oracle、评分与复核 | 模型、请求数、tokens、费用、profile、cache policy 全未登记；当前 0 | 通过上游 gate 后提交具体 API proposal；旧 USD20 不沿用 |
| G5 冻结、评分与复现 | 旧流程有冻结、回放、独立审计基础 | 新流程能否保留失败且可复现？ | 全轮 release、提示隔离证明、新独立评分／adapter 核验、报告及复现命令 | hidden 评分前冻结全部轮次；分别报正确控制、unknown/invalid/not-reached、raw RTL 覆盖与全部成本。泄露、失配、改分母、把 unknown 当零／通过即停 | 基础设施＋独立评分／复核；候选不自评 | 仅受未来新 registration/授权约束；当前 0 | 不构成新实验或自动重跑许可 |

## G1 的公开控制与可承受日程

下列只是预先提出的公开控制族，不是已生成／执行的 fixtures、真实 DUT 故障、RTL 覆盖点、已证明重写或 GPT 编写的 DUT oracle。执行前必须冻结具体源码、位型、波形、独立期望标签、工具版本与转换命令；不依据任何未来 B/C 结果选控制或 profile。

| ID | 控制族 | 拟议标签与验收重点 |
|---|---|---|
| QC00 | 激活的恒真断言 | 正控制；受支持边界内无报警，且激活证据存在 |
| QC01 | 复位后的故意恒假断言 | 负控制；已知可达报警及选定物理样本可核对 |
| QC02 | 显式位宽、赋值截断边界 | 正控制；位宽和上下文不丢失，期望关系先独立审核 |
| QC03 | QC02 的单 bit／截断边界扰动 | 负控制；区别可检出，不静默扩宽或转移 counter 命中 |
| QC04 | 显式 signedness/cast 边界 | 正控制；仅限已声明支持子集，类型与上下文完整 |
| QC05 | 故意混淆 signed／unsigned | 负控制；保留区别，或明确拒绝不支持的运算 |
| QC06 | 完整 activation guard＋组合关系 | 正控制；guard、关系、clock/reset/phase 一起绑定 |
| QC07 | 永不激活／空泛 guard | 不合资格；native PASS 不能算语义或完成性证明 |
| QC08 | 明确 pre/post 的公开波形 | 正控制；native 选样与物理 phase 一致 |
| QC09 | QC08 的一边沿／phase 偏移 | 负控制；拒绝偏移，不改到更有利的样本 |
| QC10 | 复位断言／释放与初态上下文 | 正控制；前端、物理日志、monitor 的合同一致 |
| QC11 | 故意错置 reset／初态／clock | 负控制；拒绝或声明不支持，不跨上下文重写 |
| QC12 | literal X 转成二态 anyseq | UNKNOWN／不支持；不能称保留四态 X 语义 |
| QC13 | case equality／未知检测 | UNKNOWN／不支持；native 与物理观察分开，不静默补成等价 |
| QC14 | 仅 final-post 的 trace_done | 只验 transport；不改 DUT 输入、不加 clock，不代表完成性证明 |
| QC15 | trace_done=0 下的完成性义务 | 不得获得完成性 credit；短 safety projection 不能证明 128 周期合同 |

第一轮资格的拟议上限为：16 个公开控制、1 个预先声明的基础设施 profile；每控制最多一次 BMC 和一次 activation cover，共 32 native jobs，depth=8、每项最多 10 秒；两个物理模拟器共 32 次运行，每次最多 32 周期，最多 1024 物理周期；最多 32 次编译、每次 20 秒，物理运行每次 2 秒，整体 wall cap=1200 秒。**这些只是待授权的资源帽，不是实际成本或已许可执行。** 第二个修复 profile 不在此帽内，须新版本与资源决定。保留未运行、超时、失败、setup、编译和解析成本；depth=8 不能外推为 128 周期或无界证明。

支持矩阵必须逐项记录二态／已知值范围、位宽、signedness、截断、完整 guard、clock/reset、选定 phase 与转换链。已确认的一例 X→anyseq 是一个具体表示限制，不能推广成 74 条未复现的共同根因，也不能挑能让 C 多得分的转换来通过资格。

## G2 角色包清单与 allowlist

现有 Claude checker 只能在冻结接口、假设和较早前缀范围复用。给 monitor 增加 final-post marker 不会自动扩展 oracle。若要 selected pre(S)／类别确认或独立的末端输入义务，先明确新的规范合同，再由 Claude 写新版本；GPT 不静默改旧 oracle。

**Claude 作者包（尚未渲染为 API prompt）**只允许：新的公开 specification/interface、位宽/reset/phase、pending input 与 accepted edge 语义、有限截止/fairness/offer cutoff 决定、明确标为背景的冻结 Claude checker、公开手工正／负／unknown 例子及来源哈希。排除 GPT 候选／答案／历史、隐藏 mutants/final traces、私有 calibration、benchmark expected answers 和 B/C 结果。作者交付新 reference/selftests/范围与不支持项。

**Claude 全新会话复核包**只允许：冻结作者产物与 SHA、公开合同、公开资格与负／unknown 控制证据、scope delta 和验收表。排除作者会话、GPT candidate context、hidden finals 和调参答案。必须返回有哈希约束的独立范围结论。对于迟到 offer、永久 backpressure、接收边沿与最终 pending，不能擅自施加 DUT 未承诺的完成义务；合同含糊则先停。

**未来 GPT candidate 包**只允许新的 public spec/DUT/ABI、固定 dev observations/实际 raw coverage、自己的 previous candidate 和共同 dev feedback；C 可加已验证语义组；P 仅在另登记后加非语义 token filler。排除 reference 实现、hidden faults/final traces/labels、其他组候选内容、solver/calibration witnesses、maintainer AGENTS/skills。

本阶段只有清单，没有新 oracle、API caller 或真实模型 prompt。拟议的首作者和全新复核各最多 1 次，尚未指定模型、token、费用或时间帽，因此不是可申请／可执行的 API 阶段；修复循环也没有自动额度。未来需要服务时，由主聊天提交精确请求数、模型、token/费用/时间帽、通过的门禁与“离线为何不足”。独立 Claude 作者／复核角色和 provider 实际计数／新候选响应不能由保存回放冒充。获得新授权后才走既有终端隐藏暂存流程；不在聊天收 key，当前不读取、恢复或改变 key 权限。

## G3–G5 的比较与计量约束

G1/G2 通过后，才另登记新 spec/DUT/ABI/data 合同。先固定 dev 并封存 hidden final faults/trajectories，再生成候选。记录种子选择规则、数值、来源、工具版本和 SHA；本阶段没有生成任何种子或数据。仍是一个 IP 就如实写一个 IP；新 seed 不等于新 IP。真 DUT 结论须物理可达且有独立 reference 标签，合成语言／义务控制独立报告。

分开报告呈现 valid 时的 safety、延迟／丢失响应、合资格最终未接收输入的有限完成性，以及正确控制报警、参考／候选 unknown、invalid/missing、not reached。保留所有 raw faults/pairs、未观察类型和类别重叠，不回改旧 0/10 或 11/11。离线 plumbing 可以区分义务，不等于已证明 LLM 难度未饱和；任何 B-only 难度探针均须事先登记阈值／预算并另行授权，不从 C 结果反向选题。

未来 B=raw coverage＋共同反馈，C=B＋已验证 E-graph guard/context。固定 DUT/spec/reference/stimuli/ABI/model/tier/资源帽。若只做 B/C，结论只限整个反馈包；若检验纯语义收益，另登记非语义 token-matched placebo P、实际 provider token 匹配方法与容差、own history、计数开销和失败停止条件。不得跨组传候选内容或 hidden answers；byte matching／相同 caps 不等于实际 token 匹配。C 无收益是允许结果。

新的 cache/read/write/tier、轮次/顺序与计算资源必须在 outcomes 前统一登记，并用公共 cold/warm 基础设施控制及平衡顺序支持。相同 seed 不宣称 provider 确定性配对；formal profile 和 solver/wall caps 不按 C 优势选择。分别记录 calls、counts、tokens、编译、物理仿真、monitor replay、native mode/时间与复现成本；cached/reasoning 是子集，缺用量／计数费／账单是 UNKNOWN，不填零。cost-to-target 保留 NOT_REACHED 及失败成本。

hidden 评分前冻结全轮 prompt/response/candidate/feedback/snapshot。独立评分与新 adapter 门禁必须有精确来源和复现命令，保留超时、unknown 和负结果。实际 RTL line/branch/expr/toggle 须报告工具分母和未命中项；行为组不是 RTL coverage。固定刺激的 passive monitor 变化不能算 DUT 覆盖率增长。

## Backlog 与本阶段停止点

P05-N1 仅记为非阻塞 P3 backlog：无锚的隔离 helper 可忽略未复现记录中额外的 `reference_confirmed_selected_alarm=true`，但输出仍 false／无 verdict／科学 UNRESOLVED。当前 74 份带 P01 锚的记录没有这个字段。未来若另版本加固，应补明确 REJECT 控制；本轮不修改已验收 helper，不扩大工程范围。

F1 表示限制、selected pre／earlier prefix 归因、一般 monitor soundness／128 周期完成性、历史 H1/H2、未来 L1 cache/order 公平性及实际计数费／账单仍开放。R0 无新增 checkpoint、R1 全重启、R2 选择回滚的受控比较仍属计划，不能以冻结哈希或维护成功充当实验。展示材料本轮不改。

本阶段只交付维护验收元数据、这一份非 live 计划及角色／allowlist 清单，E05 收尾／方案仍待有界独立复核。它不授权 G0 实现、G1 native、G2 服务、新数据、precount/generation、安装或科学重跑。没有后台 heartbeat 或无人值守自动联通声明。
