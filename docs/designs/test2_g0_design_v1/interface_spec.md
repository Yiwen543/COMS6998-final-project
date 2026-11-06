# 新接口的纸面规格

状态：DESIGN_PREPARATION_ONLY。以下是未来版本的要求，尚无运行时 schema、adapter 或解析实现。字段名是设计名称；不表示已存在该字段或已产生实际值。

## 责任和输入 → 输出边界

| 层 | 输入 | 未来 adapter 的责任 | 禁止推导或扩张 |
|---|---|---|---|
| 范围与来源 | 新合同、真实独立用户 grant、源／配置／工具／输入 manifest、版本化格式 | 检查获准范围、身份、哈希、格式支持和输入完整性 | 不能用模板、旧 USD20 或审查 PASS 代替新 grant；不访问 secret |
| 请求账本 | count/generation 的 dispatch、terminal/error、calls 与 release | 新格式按显式身份一一绑定；支持声明过的严格串行顺序；资源和全局 halt 一致性 | 不能补造旧 request ID/context、不能把 request ID 的存在当成并发支持 |
| native／物理链 | 原始 job/status/source、VCD、literal transport、双 PRE/POST、rows、HEX、MON、reference 边界 | 在授权的未来实现中解析原始表示，绑定身份／位宽／phase／slot／来源；分别报告层间关系 | 不能只比同一 producer 两份摘要；不能把 consistent 当 correctness |
| 结果／成本 | 每层原始结果、错误、unknown、资源与用量证据 | 输出独立的完整性、科学归因、成本已知性；保留 raw 分母及失败路径 | 不能把 missing/UNKNOWN 填 0、把未决改 PASS 或只保留有利 C 结果 |
| 发布 | 全轮候选／提示／反馈／输入锚、原始失败、工具成本 | 新 namespace 下不可变 release，先冻结再 hidden 评分；保留无效／NOT_RUN／NOT_REACHED | 不覆盖旧目录；不把 public 控制、参考实现或 hidden 答案送入 candidate |

候选仍是被评分对象；Claude 仍负责独立规范参考。GPT 只负责接口／基础设施。超出冻结 checker 的 phase、类别、fairness 或有限截止合同，须另由 Claude 作者与全新会话复核建立新版本；本设计不写 oracle。

## 身份、版本与顺序

类型中的 string 均为非空 UTF-8 字符串；int 为非负整数且不接受 bool。SHA256 在真实记录中须为明确算法下的 64 位十六进制摘要；这里仅定义类型，不生成值。必需字段缺失与记录明确为 unknown 是两回事。

| 字段 | 设计类型／nullability | 必需条件与绑定规则 |
|---|---|---|
| schema_name / schema_version | string，非 null | 每种 manifest/event/call/release 必需；不支持版本拒绝进入该 adapter |
| adapter_version / adapter_source_sha256 | string／SHA，非 null | 实际结果必需；本包没有 adapter 版本可使用 |
| run_id / registration_id / registration_sha256 | string／SHA，非 null | 新实际 run 必需；不能从历史路径或时间戳冒造；material 变更新版本 |
| grant_reference / grant_sha256 / authorized_scope | string／SHA／范围描述，非 null 才能执行 | 必须来自另行真实授权；不存在则不能运行；不是 credential 字段 |
| arm_id / session_id | string，非 null | 模型或候选会话记录必需；session 不跨 arm/重复试验共享 |
| round_index / attempt_index | int，非 null | 会话内索引，起始值与 retry 帽在新合同固定；attempt 唯一且不能重复接受 |
| request_id / request_kind | string／count 或 generation，非 null | 新格式每次实际 dispatch 必需；count 与 generation 为不同请求，terminal/error 引用原 request_id |
| parent_count_request_id | string 或 null | generation dispatch 必须绑定同一 attempt 的有效 precount；count 本身为 null；不借用其他 session 的计数 |
| event_id / run_event_sequence | string／int，非 null | event_id 全 run 唯一；全 run 顺序严格单调，不能以 wall timestamp 替代因果顺序 |
| context_id / context_sha256 | string／SHA，非 null | 新请求及其 terminal/call 共同绑定 run/arm/session/round/attempt/输入／prompt 版本；上下文不靠外部目录猜测 |
| prompt_artifact_sha256 / messages_sha256 / format_schema_sha256 | SHA，非 null | 分别绑定保存字节、规范化请求内容、结构化响应格式；不能混为一个 hash |
| response_id | string 或 null | 有真实返回时必需且唯一；error/NOT_RUN 无返回时为 null，不能伪造 response |
| call_record_id / terminal_event_id | string／string 或 null | 一个 attempt 的 call 绑定所有实际请求及 terminal；缺 terminal 必须标缺口，不凭空填充 |
| requested_model / requested_tier | string 或 null | dispatch 时新格式必需；无派发的 NOT_RUN 不冒称已请求 |
| returned_model / returned_tier | string 或 null | 按 provider 实际返回保存；允许的缺省值须先登记，不能把未返回当成所请求值 |
| source/config/input/toolchain manifests 的路径与 SHA | string／SHA，非 null 才可 release | 标明来源、变换、工具版本／flags、工作树／构建源、冻结输入；不可只接受 producer 自证 |
| candidate / reference / native_job / physical_run / replay IDs | string 或 null | 该层存在时必需，链接对应 source/ABI/config/raw artifact 的 SHA；不存在必须说明未执行 |
| visibility / candidate_allowlist_sha256 | 公开 dev／private final／reference-only／maintainer；SHA 或 null | 所有实际输入都分类；候选包显式 allowlist，不读取 reference/hidden/calibration/maintainer 内容 |

当前设计仅支持未来**严格串行**格式：每个 run 同时最多一个 outstanding 请求，terminal/error 与同一 request_id 绑定后才能有下一次 dispatch。显式 request_id 不自动开放 concurrency；并发／交错格式应标为 UNSUPPORTED_FORMAT 并拒绝该完整性验收，另行设计版本。旧保存格式仅能标记 `identity_origin=HISTORICAL_ABSENT`，真实缺少的 request/context 仍为 null；位置关联不是认证身份，不允许据此认证新 run。

## 语义、采样与跨表示字段

| 字段 | 设计类型 | 必需条件／声明边界 |
|---|---|---|
| pin_layout / width / signedness / truncation_context | 引脚描述数组，width 为正整数；符号性明确 | 比较任何值之前绑定来源、位宽、扩展／截断位置及 guard；不靠数值大小推断类型 |
| value_domain / raw_literal / knownness | 二态／四态、原始字符串、KNOWN/UNKNOWN | 原始 X/Z 必须保留；未知归一化要可追溯，不能补 0 或把 anyseq 称为四态 X 等价 |
| clock_domain / edge / reset_contract | 非 null 的合同描述 | 需包含极性、同步／异步、初态、assert/release 边沿与时序上下文；不跨上下文折叠 |
| cycle / phase / slot / slot_count | int／pre 或 post／int／正 int | 该采样存在时必需；slot 在声明向量内。形式 active/ok 可以缩宽，但所选 bit 必须真实存在，不补零 |
| native_mode / depth / tool_profile_sha256 | bmc/prove/cover／int 或明确 unbounded／SHA | 不混合 mode 的 FAIL，也不把有限深度当无界结论；profile 来自公共资格而非 C 收益 |
| VCD / literal_input / physical_log / rows / HEX / MON 的 IDs 与 SHA | 链接与 SHA，实际存在时必需 | 保留原始每层，验证数量、顺序、位宽、所选样本和传输绑定；双模拟器也不构成独立模型样本 |
| trace_done_visibility | final-post-only 或本层无此信号 | 仅观测 metadata；不改 DUT 输入、不加 clock。native trace_done=0 的短投影不能证明 128 周期完成性 |
| selected_sample | cycle/phase/slot/context 对象或 null | 指向实际选中的 active/ok；native 延迟报告时刻不能替代直接样本 |
| reference_scope / last_sample / category | 明确边界对象或 null | selected pre(S) 与仅到 post(S−1) 的 reference 必须分别保存；较早前缀 FAIL 不确认同样本／同类别 |
| checker_source_sha256 / reference_contract_version | SHA／string 或 null | 参考实际执行时必需；范围／来源失配拒绝，不能由 GPT 改 oracle 凑合 |
| scientific_eligibility / missing_evidence_reason | 分类及理由，不能省略 | 未复现且未调用 reference 时 verdict 为 null，origin=NOT_EVALUATED；不能冒称 oracle UNKNOWN 或已确认误报 |

## 三个分离的输出维度

1. **完整性**：拟议 `PASS_WITH_SCOPE`、`REJECT`、`UNRESOLVED`，并列 adapter/format/scope、错误、缺口及已绑定原始 artifact。PASS_WITH_SCOPE 只说明声明范围内记录一致。成功记录却缺失应有 terminal/usage、身份矛盾、非法派发、哈希失配等不能通过；有可信失败记录但用量或返回缺失，可保留为 UNRESOLVED。
2. **科学归因**：拟议 `NOT_EVALUATED`、`UNRESOLVED`、`SCOPED_OBSERVATION`，另存原 native/physical/reference verdict 和范围。不提供无边界的 monitor/DUT correctness PASS。一个整体完整性通过可以同时有科学 UNRESOLVED；参考缺失不是参考已经给出 UNKNOWN。
3. **成本已知性**：每项为 KNOWN、UNKNOWN 或有完整未派发证据的 NOT_INCURRED；值与证据来源分开。NOT_INCURRED 的请求数可以确认为未派发，但不能推出整个实验或 provider 账单为零。token、count、call、compile、physical simulation、monitor replay、formal 的成本分别记录；cached/reasoning 为子集，不重复相加。

用量 core tokens 在真实返回且可测量时为非负整数；subset 不能超过 total；实际 input 应匹配同请求 precount，model/tier/上限按新 registration 绑定。失败缺 usage/未知费用为 null＋UNKNOWN，不填 0。数值已证明超帽或协议冲突为 REJECT；UNKNOWN 是诚实缺口，不是自动通过，也不自动等于每一种记录都被拒绝。invoice 与 count 费用没有账单来源时持续 null／UNKNOWN。

## 严格串行账本的状态转换表（非可执行算法）

| 全局状态／前提 | 事件／记录 | 下一状态 | 纸面规则与保留内容 |
|---|---|---|---|
| RUN_OPEN、真实授权存在 | count dispatch | COUNT_PENDING | 新 request_id/event_id；相同 attempt/prompt/schema/context，先记录请求，再等待结果 |
| COUNT_PENDING | matching count returned | COUNT_READY | 保存实际计数、来源和 terminal；数值无效或上限冲突不能放行 generation |
| COUNT_PENDING | matching count error／缺 terminal | RUN_OPEN 或 EVIDENCE_GAP | 错误／缺口及费用 UNKNOWN 保留；只有新合同明确允许的失败 retry 才能继续，不能伪造 returned |
| COUNT_READY | generation dispatch | GENERATION_PENDING | 必须绑定本 attempt 的 count request、实际 count、prompt/schema/context 和资源帽 |
| GENERATION_PENDING | matching returned | RUN_OPEN 或 EVIDENCE_GAP | 唯一 response，实际 model/tier/usage；成功且字段齐备才可接受候选，失败／缺用量按事实保留 |
| GENERATION_PENDING | matching generation error／缺 terminal | RUN_OPEN 或 EVIDENCE_GAP | 不生成虚假的 usage 或 response；retry 只在已登记规则内，缺口不改写为通过 |
| 任一非 HALTED 状态 | resource_halt | HALTED | 记录原因、事件、当时已知 dispatch/cost；halt 全 run 持久，不能在 attempt/round/session 边界清除 |
| HALTED | 无请求标志、无返回／usage 的 NOT_RUN | HALTED | 保留原计划位置和未执行理由；不是模型失败样本，也不是免费成功 |
| HALTED | count/generation 标志或 dispatch，包括孤立派发 | HALTED，完整性 REJECT | 同轮 retry、跨轮、跨 session 均禁止；不能仅降为一般 UNRESOLVED 后继续 |
| 任一状态 | 重复／孤立／错身份 terminal、交错请求 | EVIDENCE_GAP 或 REJECT | 可解释的缺返回保留缺口；成功认证矛盾、重复身份和未支持并发不能通过 |
| 所有状态 | release 请求 | 不改变历史状态 | 只有新合同规定的完整性、冻结和授权条件都满足，才可在新目录发布；未决仍明示。本文没有 release 执行入口 |

任何状态都不能删除原错误、用量或 UNKNOWN。停止新请求不否定 halt 前已派发请求的消费事实；若 halt 时尚有一个未结请求，随后绑定返回只能作为该请求的迟到原始／成本证据保留，不得恢复 run、派发新请求或认证新的成功候选。pending-halt 合同尚未资格时，完整性保留 UNRESOLVED；已知用量仍照实记录，多请求并发仍是不支持格式。不能补造合法请求流。本表并不是 adapter 实现或 fixture 数据。
