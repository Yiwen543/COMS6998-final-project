# 研究路线检查：收敛到 P2，再做跨 IP test2

**建议：今晚用已完成的 controller test2 原型与保存 pilot 完成 P2 离线材料；下一 IP 优先限定范围的 OpenTitan I2C READB。暂停把 G1 扩展成通用资格工程。** 本文是路线建议，不是新实验授权或新 IP 已就绪声明；未联系正在准备 R04 的 producer。

## P2 完成标准与现成证据

依据 `P2-REQUIREMENTS.md` 的用户截图原文：**Nov 9 · P2 · Prototype & pilot results**，需要最小端到端原型、一张 pilot 对照图、主要剩余风险、回应期中反馈。年份、提交格式与实际教师反馈未提供，不自行补全。

| 要求 | 当前可用材料 / 真正缺口 |
|---|---|
| 最小端到端原型 | 已有历史实跑：固定输入→B/C生成monitor→编译/开发反馈→候选冻结→隐藏评分→成本/报告。输入：`test2/tasks/axis_length_done_v1/{input-freeze,evaluation-freeze}.json`、`test2/configs/controller_done_study_v1.json`、`controller_done_generation_v2.json`；入口：`test2/scripts/controller_done_generate_v2.py`、`controller_done_live_post_v2.py`；产物：`test2/results/controller-done-live-v2/`、`controller-done-live-grade-v2/scores.json`、`controller-done-live-acceptance-v3/audit.json`、`controller-done-live-report-v4/report.md`。精确历史 argv/退出状态见 `controller-done-live-post-v2/progress.json` 和 `controller-done-live-post-recovery-v3/`。原末段审计字段适配失败已保留，只用v3恢复解析，没有为恢复上下文重跑实验；不冒称全流程刚由单条命令通过。 |
| 一张 pilot 比较图 | 直接引用已有 `../presentation_materials/COMS6998_Midterm_Nov6_2026/graphs/test2_total_tokens.png`，数据与图注见下；无需今晚重绘或重跑。 |
| 主要风险与回应 | 风险是固定故障集饱和/跨IP泛化不足，以及C提示更长带来的成本混杂。回应：换一个不同协议IP做有限simulation对照；保留负结果，暂不追求形式验证通用化。 |
| 实际 midterm feedback | **缺口**：本轮限定搜索本地docs、已读展示说明和P2要求，未找到教师/TA反馈原文；未查课程平台/邮箱/全聊天。Codex审计和用户路线偏好不能冒充教师反馈。正文先明确“原始反馈待提供，回应待核实”，保留“原文→修改→证据→局限”四栏；收到后再完成，不谎称已回应。 |

最小交付可是一份短P2说明，依次放原型流程、下图及图注、主要风险/下一IP、反馈缺口。已有证据允许标记“历史pilot已执行，今晚未复跑”；不能将尚未完成的跨IP live或G1列为P2已完成结果。

### 选定图与准确图注

图为已有 **Total API tokens, all 18 rounds / arm** 成本柱状图。本轮已看现成PNG，并核对 `../presentation_materials/COMS6998_Midterm_Nov6_2026/authoring/chart_data.json` 与 `test2/results/controller-done-live-acceptance-v3/audit.json` 的六个session：

| 组 | 三个session各6轮的actual tokens | 总计 |
|---|---|---:|
| B |247062、247753、245828|740643|
| C |272594、270449、270606|813649|

**可直接采用图注：**“历史 controller fixed-stimulus pilot；B/C各3个独立会话×6轮，共36次generation。C实际输入+输出token比B高9.8571%；六个最终monitor均检出11/11种已确认可观察fault types。原始故障数12，N10未确认可观察仍保留；未知、无效轮与全部成本不删除。缓存/推理token为子项不重复相加。图只比较生成token，不代表总编译/仿真/wall成本或实际账单；不显示统计显著性、纯语义因果、一般monitor正确性或128周期证明。”

这是同一IP的成本比较，不是三种IP或六种硬件；已有 raw CSV 为 `controller-done-live-acceptance-v3/rounds.csv`，更细成本和formal/unknown解释在v4报告。图中的“18 rounds/arm”为3×6的合计，不是每session18轮。

## Proposal 对齐与允许的偏移

已读正式两页PDF：`project_background_reading/E_Graph_Augmented_Tool_in_the_Loop_Agent_for_High_Coverage_RTL_Verification.pdf`（SHA `f92cad65c69d9c3c942ba1c04691f6c96d3c5a4224c478043b1d51f92f2c2cf0`），及 `docs/PROJECT_STATUS.md` 的“Goal and relation to proposal”。`project_proposal_cn.md` 是早期多选题草稿。

Proposal研究语义反馈是否改善verification coverage与Token ROI，比较A文本、B原始覆盖、C语义分组，并计划CVDP评估。test2的固定刺激/monitor检错是已另行授权的合理扩展，报告必须解释endpoint改变，不能自称完成官方CVDP或Pass@1评测。优先完成B/C研究对比，已有A或原stimulus结果作为背景；不为补齐三臂而今晚增加调用。

**固定刺激下换monitor不会改变DUT原覆盖。** 覆盖只作固定输入充分性、可观测性和反馈来源背景；主收益用有效可观察缺陷种类、误报、unknown和实际成本衡量。原stimulus的普通操作排除/B难度gate不自动约束新test2；既有失败状态保持，只为新monitor任务登记适用条件。C结果好坏都接受，不为制造收益换标签或无限追加。

## 三个不同IP候选：资产存在，但都没有现成 test2 接口

以下路径本轮已做有限存在/文档核对，不是重新资格测试。I2C与SPI来自同一OpenTitan仓库，是不同协议IP，不能当作独立上游来源；WBXBAR来自另一设计家族。它们均非FIFO语法变体，也尚不是全新完成的test2比较。

**1. 推荐 I2C READB controller：现成独立参考最多、额外准备较少，协议顺序/计数与FIFO有实际区别。**

- DUT/spec存在：`third_party/opentitan_candidate/hw/ip/i2c/rtl/{i2c_pkg,i2c_controller_fsm}.sv`、`hw/ip/i2c/doc/{theory_of_operation,registers}.md`；pin/provenance在 `examples/heldout_i2c_controller/provenance.json`。
- Claude参考存在：`examples/heldout_i2c_read/{checker.py,authorship.json,contract.md,freeze.json}`；本轮checker SHA与作者记录相符。它是原stimulus轨道的有限wire/队列合同参考，**还不是直接合格的test2 oracle**。可复用须保持READB/ACKing-target/profile、字段含义、push-before-pre及pre/post时序，并由独立scope review确认评分需求没有扩大。读不完为pending；额外STOP有invalid归因限制，stretch/recovery与256-byte完成性不纳入确定检错credit。GPT不得补其expected逻辑。
- 输入/observer资产存在：`scripts/run_i2c_read_fixed.py`、`scripts/i2c_read_fixture.py::OBS/parse`、`examples/heldout_i2c_read/verif/tb_i2c_read_fixed.sv`、`results/i2c_read_candidate_20261104/driver-v2/`和`icarus-v2/`。这些是旧校准/观察，不能冒充新hidden集。**缺** test2 passive SV observer ABI、冻结dev/hidden集与可独立归因的DUT单点mutant集；旧trace-corruption controls不是现成的多种RTL缺陷。
- E-graph资产存在：`results/i2c_event_candidate_20261104/{certified-guards.json,egg.json}`、`results/i2c_read_candidate_20261104/source-screen.json`。旧报告有25个reached group/3非平凡组，218/268精确映射、50未决；都不能改写成已证明时序性质。新任务只用与所选monitor义务有关的已证关系/完整guard，不开发新通用frontend。
- 历史：`docs/i2c_read_preflight_2026-11-04.md`。原刺激选择gate失败、无I2C B/C live；不因此禁止新monitor pilot，也不称旧scope已适用所有新义务。

**2. 备选 SPI_HOST core：资产丰富，但已知合同归因问题使当前准备成本更高。**

- DUT/spec：`third_party/opentitan_candidate/hw/ip/spi_host/rtl/spi_host_core.sv`及真实依赖，规格在同IP `doc/`；`configs/spi_core_safe_b_development_v1.json`绑定closure。
- Claude v4参考：`results/real_parent_screen_20261104/claude-checker-v4/candidate/{checker.py,authorship.json,contract.md}`。不能将仅FSM的 `examples/heldout_spi_host/contract.md` 当整个core合同。现有safe-offer driver/TB在 `examples/spi_core_integration/`，旧inputs/traces在 `results/spi_core_safe_20261104/`；test2 ABI、隐藏集/物理mutants均需新做。
- E-graph：`results/real_parent_screen_20261104/spi_host_core_v2/screen-v2/egg.json`，原映射/合同绑定见上述config。旧B试验不是test2比较。
- `docs/spi_failure_attribution_2026-11-04.md`明确same-CS配置切换分歧和checker级联诊断；不能算23个独立bug。如使用该义务，须Claude作者新版本+fresh review；若只用原已审固定配置scope，先scope review，不追同CS扩展。

**3. 备选 WBXBAR：结构差异大，当前公开引脚归因未知多，排第三。**

- DUT：`third_party/wb2axip_candidate/rtl/{wbxbar,skidbuffer,addrdecode}.v`；本地规格来源为该checkout `README.md`与冻结合同，并非不存在的`doc/spec.pdf`。
- Claude参考：`results/wbxbar_reference_replay_20261104/frozen-checker/{checker.py,authorship.json,contract.md}`；固定driver `scripts/wbxbar_exploratory_driver.py`，原输入/观察在 `results/wbxbar_reference_bc_20261104/live-v1/`。test2 ABI/新hidden/单点mutants未建立。
- 既有语义组/完整guards在 `configs/wbxbar_reference_bc_v1.json::semantic_relations`；重复源计数仍分开。旧鲜活B/C全部17/17早达，但全部功能unresolved，不能把零报警当pass（`docs/wbxbar_reference_bc_2026-11-04.md`）。旧oracle复用须保留ACK/ERR/取消歧义、容量与排除项；不为试验再造隐藏所有权裁判。

## 下一IP最小计划：离线先准备，明天再决定在线

1. 先为I2C写一个短任务卡：选已审read byte/count/order/ACK/复位范围；固定同版本DUT/spec/参考、2条dev及3条新hidden输入、最多4–6种单点可观察故障。仅使用当前支持的语义组。共享公共引脚/观察字段明确allowlist，排除reference内部状态、私有校准/标签/故障源码/最终分数；先准备文件和映射，不运行仿真或模型。
2. 旧参考**先不改字节**；准备最小scope-review包，指出observer transport和评分用途变更。若新义务超出合同，独立Claude作者修订再fresh review；已知extra-STOP invalid等限制继续保留。旧手工/校准反例只作控制，不拿来宣称新独立DUT缺陷。
3. 新登记先用simulation-only。B/C同模型/推理档、共同包、资源帽、每组2个独立session×3轮；C只多已证语义关系和guard。全部12轮冻结后才hidden评分，按同一预定规则选最终monitor，不看hidden挑轮次。相同模板/feedback/失败处理；没有长度placebo则只声称整包比较。若需要控制长度，先在登记中规定，不事后剪C。
4. 指标：distinct **valid observable defect types**（重复报警/两sim不重复计种类）、正常控制false alarm、invalid/unknown/not-reached及原始分母、actual input+output tokens；compile次数/时长、DUT sim与monitor replay分列、实际cycles/wall、失败重试成本。raw DUT覆盖保持背景。先完成有限pilot再按预定饱和/精度/预算标准决定更多重复，对两组对称，不能只在C占优时追加。

**明天才讨论的具体在线/资源项，均未获本报告授权：**优先1次Claude独立scope review（拟≤USD4）；如确需新参考，另1次作者+1次fresh review（各拟≤USD4，Claude总拟≤USD12）。B/C pilot正常12generation、最多24含失败重试，最多24count；单次拟64k输入/8192输出，总生成拟≤USD8、count预留≤USD2。获准模型/费率和最坏预留必须在启动前核清，不引用历史费率当当前报价；不足则不派发。最多新local64编译、64DUT runs（每条≤392周期）、640monitor replays、总≤300k周期/20min作为待细化上限，按具体任务清单冻结，不能借G1余量执行。今晚不generation/count/Claude/API/network、不索钥匙。

安全可做的后续离线准备只有：P2正文/图注、真实反馈占位、I2C任务卡/公开ABI映射/allowlists、旧参考scope包和有限输入/故障计划。可逆scaffolding若后续明确实施，也仅为这个接口，不能扩为验证平台工程。本轮没有实现上述代码或新数据。

## G1/R04 最小止损边界

physical累计32→33已被用户明确批准，授权文件 `G1_qualification_v1/user-authorization-physical33.json` SHA本轮核对为91837999f0b24424ed5ca3f89a3744a6358453e669568f68ba4b68794c68d24e；其他帽不变。R04仍纯准备，本文不给EXECUTE。P13首拍X/失败池、费用和全部未决保持。

R04需要保留的最小成果：新版本修正time-zero刺激建立；不改原标签/跳首拍/X补0；基本正/负/unknown与首行/相位/记录完整性检查；旧池/累计预算/必要owned-group清理保持；如复用旧native必须显式绑定。若以后真正使用该路径，需要原始首拍正确及基本真实正负控制，纯mock不能替代。

可以停止并列限制：全16QC的一般formal资格、所有历史74未复现根因、SMT/四态通用等价、完整child census、任意并发事务、128/unbounded/recovery证明。**不使用native formal的跨IP有限simulation pilot，无需先完成整个G1**；只验证它实际使用的driver/observer/reference路径。若不用G1的坏TB，则坏TB不阻塞独立已检查的simulation路径；若继续用它，首拍X仍是实质问题。P2不需要今晚新G1或新跨IP live。

## 本轮方法与限制

Hallmark本轮未新读：核对当前SKILL SHA25a1ff92d925b2389e8409f42fb8ad7e033fceca8b5d1f07ed4ca4c28da53dc3，与P13 `hallmark-usage.json`的新读凭据同版；借用review-finish的固定材料优先、准确区分事实/意图、按实质影响排序及最小修订，实际用于上述P2矩阵、资产缺口与G1止损。完整网页workflow/scripts=false；技术/研究判断不由Hallmark担保。

只读PDF文本、已有报告/配置/少量源代码与现成图；未做新实验或复审整个旧oracle。PDF用已安装pdftotext读取：pypdf缺失后采用只读回退，未安装依赖；workspace dependency工具不支持本调用环境，未因此扩展任务。若干推测性旧路径不存在，最终只列已核对资产；搜索范围有限，反馈缺失是“本轮未找到”，不是证明不存在。只新增本文件，不改producer、P01–P13、源/结果/共享handoff/index，不发消息/新agent或chat，不建新门禁/长manifest。
