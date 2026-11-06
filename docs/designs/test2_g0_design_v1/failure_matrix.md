# 纸面失败矩阵

DESIGN_PREPARATION_ONLY。下列 FM 编号只是设计案例，不是故障样本、fixture、运行记录或探针。没有构造输入、执行 validator、跑测试或验证预期。所有“预期”均为未来设计规则，待独立纸面复核及另行获准实现后验证。

完整性 REJECT、完整性 UNRESOLVED、范围内记录一致但科学归因 UNRESOLVED 必须区分。每行均保存原始输入／错误／缺口与实际已知成本；缺失用量／费用一律 null＋UNKNOWN，不能丢分母或补 0。表中“保留”只规定未来记录要求，不表示本轮生成了证据。

| 案例 | 前提与纸面扰动 | 必须绑定的字段／来源 | 拟议完整性规则 | 科学判断仍未知的范围 | 成本／原始失败保留 | 验收依据 |
|---|---|---|---|---|---|---|
| FM01 | 声称成功却缺 returned | request/terminal/call/response ID、原始事件 | REJECT 成功认证 | 不推断候选或 DUT 正确性 | 已派发及缺口保留，usage/fee UNKNOWN | 接口身份与 terminal 条件 |
| FM02 | 有可信 transport error，但 terminal/usage 不完整 | 同一请求、error、dispatch、上下文 | UNRESOLVED，不补返回 | 无新成功样本；不是科学 PASS | null＋UNKNOWN；已耗请求不删除 | 失败／成本分离 |
| FM03 | 重复 event/request/response identity | 全 run 唯一键及原始字节 | REJECT | 不把重复返回算独立试验 | 两份记录均保留，成本不擅自去重为零 | 唯一身份 |
| FM04 | 无 dispatch 的孤立 terminal | request ID、event sequence、calls | REJECT 认证，保存孤立证据 | 来源／执行未认证 | 费用缺证据保持 UNKNOWN | 一一对应 |
| FM05 | 无 call 的孤立 dispatch | dispatch、planned attempt、call inventory | REJECT 完整发布 | 不能补一个成功 call | 未知返回与可能成本保留 | 全计划 inventory |
| FM06 | strict serial 中第二请求先于前一 terminal | global sequence、request IDs、schema | REJECT 为未支持格式 | 不把交错解释成有效新运行 | 全流保留，任何真实用量不删除 | 串行范围 |
| FM07 | 有 ID 的并发格式企图进入串行 adapter | format/version、ordering contract | UNSUPPORTED_FORMAT／REJECT，不自动开启并发 | 不认证并发因果关系 | 原始格式和成本留档 | 新版本／独立资格 |
| FM08 | call/dispatch 跨 session 或 arm | run/arm/session/round/attempt/context | REJECT | 不归因于某一组能力 | 错配双方和成本均保留 | 会话隔离 |
| FM09 | 同 session 却串 round/attempt 或 context | context ID/hash、索引、own history | REJECT | 不当作合法 retry 或独立样本 | 原请求、prompt 和缺口保留 | context 绑定 |
| FM10 | prompt 字节或 normalized messages/schema digest 错配 | 三种不同 hash、实际保存 prompt、schema 来源 | REJECT | 不推测使用了哪个真实 prompt | count/generation 及缺口均保留 | prompt/count/schema 绑定 |
| FM11 | response ID/parsed response 与 snapshot 不符 | response/terminal/call/snapshot | REJECT；不修原件 | 不能宣称原样可复现成功 | 原返回和归档差异保留 | P04/P06 纠正所示边界 |
| FM12 | halt 后同 round retry 请求 | 全局 halt event、request flags、sequence | REJECT，不能只降为普通 UNRESOLVED | 不认证新候选 | halt 前成本与非法请求证据都保留 | persistent halt |
| FM13 | halt 后跨 round 请求 | 全 run halt、round、dispatch | REJECT | round 切换不恢复许可 | 同上，未执行计划行仍保留 | persistent halt |
| FM14 | halt 后跨 session/arm 请求 | 全局状态、session/arm、dispatch | REJECT | session 切换不恢复许可 | 同上，不能把失败删除 | persistent halt |
| FM15 | halt 后 flags 声称请求，但无事件 | flags、halt、call、event inventory | REJECT 协议矛盾 | 不补 dispatch／usage | flags 原件及缺口保留 | halt／发行声明一致 |
| FM16 | halt 后孤立 count/generation dispatch，无 call 或 flags=false | 原始全局流及 halt sequence | REJECT | 不用“缺 call”淡化非法派发 | 孤立事件及未知费用保留 | halt／孤立派发规则 |
| FM17 | halt 后仅无请求、无返回／usage 的 NOT_RUN | planned position、halt、空请求标志 | 可保持范围内一致；不是候选成功 | NOT_EVALUATED／无新模型样本 | actual tokens 不伪造；不推出整体 bill 为零 | 合法停止正例的纸面条件 |
| FM18 | halt 时仍有未结请求，随后到达绑定返回 | halt 前 dispatch ID、terminal、顺序 | 保存迟到证据；未经明确支持的 pending-halt 合同为 UNRESOLVED，不新派发或恢复 run | 不从迟到返回认证新候选／科学信用 | 已知用量照存，未知仍 null，不抹除消费 | 明确停止与缺口范围 |
| FM19 | 失败缺 usage，被写成全零 | raw usage/缺失来源、cost knownness | REJECT 零值伪造；诚实缺口应 UNRESOLVED | 不把请求变免费成功 | 原缺口、error 和 UNKNOWN 保留 | null/UNKNOWN 规则 |
| FM20 | 成功 core usage 算术、subset、raw/normalized 不符 | provider raw、输入／输出／total、cached/reasoning | REJECT | 不认证预算或效率结论 | 原值均存，不重复相加或事后挑值 | 用量绑定 |
| FM21 | requested/returned model 或 tier 不符 | 请求、terminal、call、真实注册范围 | REJECT；缺返回字段不可冒填匹配值 | 不混合不同模型／层级的比较 | 全用量／失败／未知费用保留 | 固定模型／资源合同 |
| FM22 | precount 与 input 不符，或借其他请求 count | count request ID/context/prompt/schema、actual usage | REJECT | 不宣称实际 tokens 已匹配 | 两次观测与计数费 UNKNOWN 保留 | 同请求 count 绑定 |
| FM23 | quota/token/retry/reserve 确认超帽，或旧 grant 被复用 | 新 grant、限额、全局 issuance、实际值 | REJECT；没有 grant 不执行 | 不是通过／免费重试 | 违规前后原始成本不删 | 资源与授权边界 |
| FM24 | artifact SHA/source/config/input/release 错配 | 原始字节、算法、manifest、版本与锚 | REJECT | 不认证执行来源或 correctness | 失配双方和已知资源保留 | 不可变来源 |
| FM25 | 覆盖既有目录、拼接 run 或路径越界 | 新 namespace、路径规范化、输入输出 allowlist | REJECT／不写入，不删除旧结果 | 无新可发布结果 | 既有证据原封保留；记录拒绝意图 | 拒绝覆盖／路径范围 |
| FM26 | 只有同一 producer 的两份摘要一致 | 原始 VCD/transport/logs/MON/reference 与锚 | 原始链不足则 UNRESOLVED，不称独立核验 | 不证明执行／科学归因 | 保留摘要和缺证据清单 | 原始链优先 |
| FM27 | VCD 缺失／截断／输入声明或 step 不完整 | raw VCD、声明宽度、连续状态、native identity | REJECT 完整链；不可恢复部分记录缺口 | 不推断所选报警或 DUT fault | 截断原件、native 原状态及成本留存 | VCD→literal 链 |
| FM28 | literal transport 与 VCD 输入／顺序不同 | VCD、formal-input 记录、transport、源 layout | REJECT | 不是同一物理见证 | 原始输入和执行成本不抹除 | 传输绑定 |
| FM29 | 双物理模拟器 PRE/POST／rows 被一致改动，但 VCD 未变 | raw PRE/POST、源／build identity、VCD retained outputs | REJECT，不能只因双 simulator 相同通过 | 两个 simulator 不是两个独立模型试验 | 两份 raw、rows 和实际运行成本保留 | 跨表示语义绑定 |
| FM30 | raw log 与 rows 不符／重复／缺 phase／cycle 偏移 | 原始 PRE/POST、cycle/phase、rows | REJECT | 不把错位归为 DUT 行为 | 原件、截断／重复与成本保留 | 时序与解析边界 |
| FM31 | HEX/MON input rows 与物理 rows 不同 | rows canonical digest、HEX 路径／字节、执行绑定 | REJECT | 不认证 candidate 使用了同一观察 | 原 transport／MON 与 replay 成本保留 | MON 输入来源 |
| FM32 | MON 位／property 被改，并同步更新 hash | raw MON、phase/slot、property 摘要、rows | REJECT 语义不一致，不只看 hash | 不补造检错能力 | 改动前后声明、原日志与 unknown 保留 | 原始样本对属性 |
| FM33 | slot/phase 错位或缺所选 bit | native harness/source、declared vector width、selected sample | REJECT；缩宽向量若仍含所选 bit 不因缩宽本身拒绝 | 不补零模拟所选报警 | 实际声明／样本／成本留存 | 精确 slot 与宽度 |
| FM34 | 所选 active/ok 是未知位 | raw four-state literal、位宽与 knownness | 完整记录可范围内一致；科学 UNRESOLVED，不算 definite alarm | 不是 confirmed fault，也不是 false alarm | 未知位原样保留，成本不归零 | unknown 与完整性分离 |
| FM35 | reference prefix 长度／最后 phase 或类别被换 | selected pre(S)、reference last sample／contract | REJECT 错绑；正确的较早 prefix 也只能给受限观察 | post(S−1) FAIL 仍不确认 pre(S)／类别 | 所有 reference/physical 原结果保留 | 参考范围 |
| FM36 | 未复现且未调用 reference，却填 oracle UNKNOWN/FAIL | 调用存在性、reference artifact、status origin | REJECT 伪造 verdict；合法未调用为 null/NOT_EVALUATED | 原 74 条不升级为 oracle 判定或已确认误报 | 未复现和未评估理由保留 | 评价来源可区分 |
| FM37 | checker source/contract 或 candidate/native source 错配 | 精确 source/ABI/config SHA、独立参考版本 | REJECT；不由 GPT 补 oracle | 不认证任何新判定 | 原代码身份和所有成本保留 | 来源与角色边界 |
| FM38 | 新增无历史锚 metadata 声称“独立历史确认” | metadata provenance、已有锚覆盖范围 | 对无依据声明 REJECT；仅诚实记录当前内容可保留受限／UNRESOLVED | 不提升执行真实性／科学确认 | 当前内容、来源缺口留存 | 锚与声明范围 |
| FM39 | 无锚 helper 的未复现记录额外置 confirmed=true | source metadata、receipt、允许字段／锚 | 未来新 schema 拟拒绝矛盾确认；不是本轮已实现能力 | 科学仍 UNRESOLVED，不确认报警 | 原声明及 receipt 保留；P05-N1 backlog 不隐藏 | 新设计要求；当前 helper 不改 |
| FM40 | 把 literal X→anyseq 或 case equality 当已证明等价 | 原值域、转换、位宽、工具支持矩阵 | 不支持／未证明则 UNRESOLVED；若认证为等价则 REJECT 声明 | 不证明四态语义／所有未复现共同根因 | native／physical 原状态、unknown 与成本保留 | F1 支持范围 |
| FM41 | 空泛 prove／cover 未达／短 depth 被写成 128 completion PASS | mode/depth/activation/trace_done/reference 合同 | REJECT 越界结论；原状态本身保留 | 完成性／一般 soundness 未知 | PASS/FAIL/TIMEOUT/未达与原成本不删 | 模式、激活和范围分离 |
| FM42 | hidden/reference/其他组历史进入 candidate prompt，或评分先于全轮 freeze | 可见性、prompt allowlist、release 时间／内容锚 | REJECT 发布／比较 | 不支持公平 B/C 或纯语义归因 | 泄露／未冻结证据和已耗成本保留 | 提示隔离与冻结 |
| FM43 | 删除 invalid/unknown/NOT_REACHED／未观察类型或改 raw 分母 | 预登记 inventory、全部结果、覆盖源 counter | REJECT 汇总认证 | 不把行为组／合成控制当 RTL coverage 或新 DUT fault | 全部分母、失败和成本保留 | 公平计量 |
| FM44 | 把模板 JSON 可读／设计审查 PASS 当执行 grant | 模板标记、真实 grant、权限、entrypoint | REJECT 执行／结果声明；文档检查仅文档检查 | 没有 adapter/fixture/native 资格 | 保存文档状态，不生成虚假运行成本 | 本轮设计边界 |

本矩阵不证明任何分支已经可被实现正确处理。尤其是并发、pending-halt 的迟到返回、无历史锚 metadata 的发布条件，须在未来新格式中明确支持范围并获得实施及资格许可；不能借历史 v2/v1 的限定验收自动认证这些未来能力。
