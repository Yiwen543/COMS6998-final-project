# test2 多周期控制器资格包 — 2026-11-05

研究问题保持不变：固定刺激和匹配资源预算下，E-graph 反馈是否改善生成 monitor 的正确性、有效检错率和实际成本。当前尚无新 B/C 候选结果，不能声称 C 已获得收益。

**本阶段已完成：**具体任务/规格/接口、来源与语义映射、局部形式日程、Claude独立参考及新的隐藏评估证据已建立并冻结。最新总入口为 `test2/tasks/axis_length_fifo_v1/qualification/qualification-summary-v1.json`。独立参考接受的是明确的有限轨迹范围，不是完整oracle soundness证明；候选live仍关闭。

## 已固定的任务与保留的否定证据

选择同一锁定上游 verilog-axis revision `48ff7a7e2ef782cf778d47910cf85835c64b1bce` 的帧长调整控制器。输入帧是多周期请求，输出数据帧与状态是独立响应；合法场景含填充、截断、背压、跨帧操作和同步复位冲刷。它属于以前检查过的 IP 家族，不冒称新未见仓库或两个独立 IP。

最初直接核心被拒绝。状态 valid=1、ready=0 时，original_length 从2变1；相同9周期输入在 Icarus/Verilator 都于 cycle6 复现。见 `test2/tasks/axis_length_v1/qualification/status-witness-replay-v1/`。直接核心 BMC/prove 的 status_stall FAIL 保留，未修改原版 RTL、放宽断言或记作通过。

另行登记的选定任务是**原版 FIFO 包装控制器**，代码逐字复制上游：

- 根目录：`test2/tasks/axis_length_fifo_v1/`。
- 原始源：`public/rtl/axis_frame_length_adjust.v`、`axis_fifo.v`、`axis_frame_length_adjust_fifo.v`；公开别名 wrapper：`public/task_top_v3.sv`。
- DATA_WIDTH8、KEEP/ID/DEST/USER disabled；数据 FIFO32、header FIFO8；MIN4、MAX8；输入帧1..12字节。无独立 cancel 引脚，复位是唯一取消。
- 最新具体登记：`test2/configs/controller_task_v3.json`（v2参数/预算登记保留）；来源/参数/前端登记：`controller_qualification_v1.json` 至 v5。v1 通用提取不支持、v2 timescale 前端失败、v3 KEEP 切片未认证、v4 直接核心合同失败、v5 原版 FIFO 包装通过局部资格；原证据均保留。

这些是来源/方法版本，不是按 C 结果选择任务。没有新 B/C 模型结果参与选择。

## 静态与形式资格证据

`qualification/typed-v5/`：Slang 类型/常量展开后，168个组合定义与独立 Yosys-cell 编码 mismatch UNSAT，环境 SAT；不依赖状态不变量。19项 pmux onehot 检查通过。148个支持目标中142映射、6映射未决；3168个原始计数保留。发现9组非平凡语义关系，使用真实 egg0.11 和独立 QF_BV 规则证明。

前端/定义证明是有限支持范围的双态组合证据，不是四态、时序、DUT规格或独立参考正确性证明。所有不支持项与未决映射保留在原分母。

`qualification/formal-v2/`：正/负工具控制预期 PASS/FAIL；复位清除、数据背压保持、状态背压保持各自 bmc/prove/cover 均 PASS。共11任务，局部资格实测24.492秒。BMC请求24步，各性质/模式10秒，工具控制3步/5秒，总求解器上限100秒。prove PASS仅限该局部性质和固定假设；cover是对应触发可达，不是完整功能证明。

未来候选仍可能超时。已预定每个候选：正确源六槽×(bmc,prove,cover)×10秒=180秒，12故障×六槽×bmc×5秒=360秒，共540秒求解器上限，低于共同720秒总上限。深度24、z3、flatten；不按 arm 追加资源或事后补分。

## 固定轨迹、隐藏故障与候选隔离

`input-manifest-v1.json` 在测量前绑定源码、driver、规格和输入：3条开发轨迹48/64/64周期；6条新隐藏轨迹各198周期，含128周期尾段。源端 driver 只做保持/队列传输，不生成期望 DUT 输出。

正确实现的9轨迹×2观察仿真器共18次测量、2728周期，定义明确的公共输出一致。双仿真器一致不是规格证明。

`private/mutant-catalog-v1.json`：12个新单点故障，边界 guard、握手/复位、数据/状态各4个；没有复用旧 FIFO 的隐藏最终集。12故障×6轨迹×2观察仿真器共144次新测量、28512周期，24次构建。故障是否可评分由冻结独立 reference 决定；未激活、未知、失败、成本全部保留，不换故障凑满分。

最终reference在每种仿真器的72对中确认53对 sampled safety违反，涉及11/12种故障；另19对没有确认违反。其中一种故障在所有固定输入下均未确认可观察，不删除、不改为缺陷不存在或等价。完整144对 verdict、首个违反、未知、source/rows哈希均在 `reference/frozen-v2/fault-eligibility.json`；这些是可评分性，不是候选检出成绩。

候选输入包仅允许规格/接口、三个原始公开 RTL、固定 wrapper、三条开发观察和全部原始计数。`controller_packet.py` 用独立 bit/direction 的 RLE 压缩 toggle 存储，3168个计数的身份/逐轨迹命中逐项 roundtrip 相等，没有按 eclass 合并 hit。

`qualification/prompt-audit-v2/` 中 B/C 共享内容完全一致，C仅追加4组事先按行为选择的 transfer cutoff/padding exit关系及完整 guard/类型/源映射。压缩 JSON B/C 为226209/238844 bytes；这不是 API token计数。provider token-count gate尚未执行。共同新 input cap64k，在任何候选调用前登记；相同 cap 不意味着实际 prompt 等长。

## Claude 独立参考：过程与尚未自动接受的事项

- 作者包只含规格和观察接口；无 RTL、故障位置、隐藏轨迹、E-graph witness、候选或维护技能。
- `reference/author-v1/`：作者返回 checker，但辅助 selftest 使用禁用 `__setitem__`，调用状态保留 failed，费用$0.743996。
- `reference/author-repair-v1/`：Claude只修复 selftest，checker逐字未变。作者自测34项、独立有限控制15项、正确实现18条轨迹得到预期结果；费用$0.357046。没有 GPT checker 修补。
- 原合成正控制曾因延长 header 背压而仅剩30周期 quiet tail，被正确判 UNRESOLVED。保留原 fixture/diagnostic，仅给该独立控制追加2个idle周期，不改实际开发/隐藏输入或 checker。
- `reference/review-v1/`：全新会话给出 accept_with_scope，但指出未接收的无依据 valid可能漏报、final128周期未强制、pre/post同边沿因果和 INVALID_INPUT分类等范围限制。费用$0.817401。该限定接受没有被改成完整合同通过。
- `public/specification_v2.md`、`observer_contract_v2.md` 及 `reference/alignment-stage-v2.json` 固定原合同检查强度：pre仅由先前边沿已接受数据支撑，post包含当前接受；无依据 presented valid即使阻塞/后续reset也失败；新增显式 min_tail参数，final128/development32；非法源协议归 INVALID_INPUT。加强版 checker和自测必须仍由Claude作者生成，之后再全新会话复核。
- `reference/author-strengthen-v1/`：Claude完成原合同强度对齐，自测50项；独立控制扩为20项，正确实现18条轨迹仍PASS。作者调用费用$0.643801。
- `reference/review-v2/`：新会话无blocking finding，accept_with_scope；费用$1.152376。仍保留未知后状态保守丢失、首次失败后诊断不完整、reset pre样本及post/pre连续性等范围限制。不得外推为全规格证明。复核文字把182 evaluations泛称control cases；实际只有20独立合成控制、18正确轨迹、144mutant轨迹，已在scope-notes纠正且原review不改。
- 正式参考：`reference/frozen-v2/`。checker SHA256 `b44f32b27c11b968d23fd93ecf8b0d714e773460fc0b505d89adf23df3cd7dee`；freeze SHA256 `bbac094bcf82eecb44e57fd85a3dbdabb27dd07af00559300617753103ed7c67`。全部5次CLI角色调用含失败的报告费用合计$3.714620；不存在缺失费用项，不推算OpenAI美元成本。

用户2026-11-05明确授权：修订与复核之间保留主暂存key，参考任务完成后清理。`controller_credentials.py` 仅为旧不可修改调用器提供每次0600工作副本；主key不进日志、prompt或Git。不能照旧交接在每次修订之间要求用户重复暂存。

该参考任务现已完成，主暂存key及临时工作副本已清理。早期失败/有限接受均保留，新的限定范围接受没有回写升级任何旧结果。

## 在什么情况下 C 可能有额外收益

这是假设和预定分层，不是已观察到的正结果。

1. **guard组织成本高而语义已认证**：transfer中剩余长度条件的不同写法，以及PAD退出条件的正/反极性，在完整激活条件下等价。C可能减少遗漏合法激活条件或写出过宽 active 的错误，表现为更少正确控制误报、更早得到有效监视器，而不是增加固定 DUT覆盖。
2. **联合场景超出开发轨迹的具体组合**：独立数据/状态背压、跨帧边界和复位冲刷需要把规格义务与实现 guard 联系起来。C可能帮助泛化；但不能把组合等价当作时序/规格正确性，也不能假定隐藏场景已被这些关系解释。
3. **规格模型已经足够或缺陷主要是数据/时序问题时，增益可能很小**：完整规格模型可能使B和C再次饱和，C增加的token反而降低ROI。因此数据/状态类作为对照分层，与guard类一起报告；不能只挑C占优的类别。

所选4组的8个源点在开发 boundary_pressure 已全部命中，不能声称它们整体未覆盖。反馈是否减少推理成本/错误只能由后续模型试验回答。无长度placebo时只比较整个反馈包，不能证明纯语义因果效应。

## Live 边界与下一步

候选 live 仍关闭。参考完整复核、隐藏eligibility冻结之后，还需新接口候选边界/回放与逐轮快照release测试、总成本审计、实际provider token计数和新的live freeze；不能使用旧FIFO runner自动启动。

本阶段新增测试位于 `test2/tests/test_controller_task.py`（13项），覆盖隔离/计数roundtrip、单点故障、否定证据保留、参考freeze和用户授权的跨调用key生命周期。本次新13项及前阶段7项静态回归均实际通过（共20项）；旧25测试及旧实验没有重跑。最终审计核对旧freeze3486项、旧参考、旧评分和原未提交工作；没有提交、推送、安装工具或新的B/C生成。

Git补充：会话开始HEAD为acd220a；最终为00e0dd974d3a910b37de3c029f61e7beeb7953fd，中途出现test2_phase1/test2_phase2两个提交。本轮agent未执行提交/推送/fetch，不推断这些提交的操作者或远端实时状态。保留新基线和剩余未提交/未跟踪完成文件；不回滚，也不冒称全部新冻结材料已在HEAD内。
