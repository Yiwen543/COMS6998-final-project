请在现有项目中完成 G0 的设计准备包，并在准备完成后交由既有独立复核流程检查。发送前协调端已核对你为空闲；本任务遵守用户不要打断推进中工作的要求。仓库 /Users/yiwenchen/Desktop/COMS6998/ai_for_chip_design_project/COMS6998-final-project。当前实际HEAD仍为c25180848ebfe9a1f49da0aa5f579cac913e6428，dirty/untracked及全部历史证据保留。

本轮权限严格限定：G0接口设计、清单模板、失败矩阵、公开控制的纸面定义和文档封存。现有controller_next_qualification_draft_v1.json实施额度仍0；本提示不授权adapter实现、测试代码、fixture构造/执行、G1/native/Yosys/simulation/formal/monitor、API/count/候选生成、新数据、付费、安装、key操作、删除结果、commit/push。用户确认之前不要进入这些操作。只允许Markdown/非执行JSON模板及必要的读取、SHA/JSON语法/字段一致性等文档检查；不要创建或运行.py验证器、.sv/.v控制源码、harness、波形、真实rows或可运行fixture。不要运行旧companion审计或unit suite来验证文档。

先按AGENTS读紧凑HANDOFF/STATUS，按需读现有非live资格计划与P05/P06/P07审查摘要，先摘要后有界源码。P07只接受文档范围、P05仅当前保存格式94链、P06仅严格串行保存格式/本批；旧audit_v3不升级为通用新run gate。P04原件response绑定差异与P06限定保持、原因UNKNOWN；P05-N1只backlog，F1/H1/H2/L1/selected sample/128completion/invoice等开放限制不关闭。

选未占用的新文档目录，例如 docs/designs/test2_g0_design_v1/，不要改已冻结/已验收source/tests/audit、旧E05计划/draft/sidecar或snapshot。交付一份README/范围说明，写明DESIGN_PREPARATION_ONLY、implementation_allowed=false、fixture_execution_allowed=false、native/API/data/generation权限false、entrypoint=null；所有模板字段明确是占位，不是新registration/release、用户grant或实际运行结果。新设计不要冒用旧USD20许可；仅你负责更新共享HANDOFF/STATUS一条当前文档准备状态，历史内容保留。

产物1：接口规格（纸面）。定义新版本schema/adapter的职责和输入→输出边界，列run/session/round/attempt/request/event/context身份、顺序、版本、source/config/input/release hashes、时钟/reset/phase/width等必要字段、类型/nullability/必需条件。区分新格式应具备的身份与历史串行格式缺少的身份，不能补造旧requestID/context或用旧hardcoded路径/历史P01锚认证新run。分别定义完整性结果、科学归因、成本已知性；缺usage/费用仍UNKNOWN/null，不填0。用状态转换表（非可执行算法）定义dispatch/returned/error、全局persistent resource_halt、halt后禁止任何retry/round/session请求flags或dispatch，合法无请求/usage的NOT_RUN保留。不要实现任何adapter/解析函数。

产物2：不可变清单/release模板（非执行）。用明确的占位符给出manifest/release、源/工具/输入/产物绑定、记录失败/unknown/invalid/NOT_REACHED与成本的字段模板和生命周期/拒绝覆盖规范。必须显眼标TEMPLATE_ONLY_NOT_A_VALID_RELEASE；没有真实新run_id、实际artifact路径/摘要或可使用的grant，必需尚未生成的值写占位/待定。不得把证据一致或模板结构合法写成native/monitor/128周期正确性通过，不包含任何secret字段或候选私有答案。

产物3：失败矩阵（Markdown表，不创建fixture数据）。逐项描述前提、纸面扰动、需绑定的字段/来源、预期REJECT或UNRESOLVED规则、科学判定仍未知的范围、成本/原始失败证据保留及验收依据。至少覆盖缺失/重复/孤立/交错事件、跨session/context/prompt/response错配、halt后请求（retry/round/session/孤立dispatch）、usage/model/tier/count/quota/sha错配、覆盖输出、VCD/input/PRE-POST/rows/MON跨表示错误、错slot/phase/prefix/width/未知位、checker/source失配、无锚新增metadata的声明边界。区分支持的strict serial与尚未支持的并发格式；不是所有unknown都拒绝，更不能都当PASS。仅列设计案例，不生成可供validator运行的记录或执行探针。

产物4：16类公开控制的纸面定义（QC00..QC15，沿用G1草案作概念对照）。每类写目的、语言/位宽/signedness/guard/clock-reset/pre-post前提、正/负/unknown/不合资格的拟议类别、人工预期与需要独立标签确认之处、拟议验收/停止条件和不支持范围。可以用自然语言/数学记号描述，不写SV、时钟波形、逐周期输入/输出或可运行测试。全部actual_result=null、source/waveform/independent_label_status=NOT_CREATED_OR_NOT_QUALIFIED。X→anyseq/四态unknown不能被声明为等价；trace_done运输不等于完成性证明；depth8不外推128周期。不得根据本轮C outcomes选有利控制/profile或把这些纸面控制当新DUTfault/RTLcoverage。此次独立审查只能检查纸面一致性，不认定控制已资格通过。

再交一页实施待办/权限清单：G0未来纯本地adapter/fixtures实施需要明确维护范围；G1公共native资格仍需具体资源授权；G2如需新独立Claude合同，模型/token/费用/时间帽还未定、NOT_READY，当前不索key。说明每项已有依据、尚缺产物、客观验收/停止条件和角色；不要开始下一任务或为完成文档安装软件。

完成后只做文档级检查：文件边界、JSON模板可读性/占位状态、身份与scope一致性、hash、Git状态和新路径非freeze成员检查。不要以JSON能解析等同于adapter/fixture/native通过。封存独有D01/E06或未占用phase文档快照、manifest、输入来源SHA、实际文档检查命令/退出码，记录0implementation/0fixture execution/0API/native/keyaccess。报告精确路径/SHA，保持文件稳定等待协调端送到现有“复核 test2 项目”chat。不要创建新项目/review chat，不自行宣布独立通过。若有问题，修订仅限新文档版本，不改变执行额度；普通文档选择无需再问用户确认。
