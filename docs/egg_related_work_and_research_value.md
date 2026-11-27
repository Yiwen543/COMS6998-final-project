# Milestone 3 · Egg 研究定位、相关工作与实际价值

调研日期：2026-11-25。本文是针对当前研究方向的定向文献调研及证据评估，不是穷尽式系统综述，也不是新实验结果。区分已有算法、当前已实现机制、仍待检验的研究假设；不把未发现完全相同的工作当成首创证明。

## 1. 已有工作与重合程度

| 研究 | 已有贡献 | 对本项目的影响 |
|---|---|---|
| [egg: Fast and Extensible Equality Saturation, POPL 2021](https://arxiv.org/abs/2004.03082) | 通用 equality saturation、e-class analysis、跨表达式共享 | 使用 egg、同图放入多个表达式不是原创算法。 |
| [Small Proofs from Congruence Closure, FMCAD 2022](https://arxiv.org/abs/2209.03398) | Egg 等价证明生成和精简 | 具名 rewrite 证明及 proof extraction 本身不是新贡献。 |
| [Datapath Verification via Word-Level E-Graph Rewriting, FMCAD 2023](https://arxiv.org/html/2308.00431) | 位宽感知 RTL 改写，将两个组合 datapath 的等价性证明分解成多个由可信工业工具检查的局部证明 | Egg 辅助 RTL 形式验证及独立检查已经存在；本项目对象不同，是 LLM 生成的监控谓词而非两份 datapath 实现。 |
| [Colored E-Graph: Equality Reasoning with Conditions, 2023 preprint](https://arxiv.org/abs/2305.19203)、[Easter Egg, FMCAD 2024](https://repositum.tuwien.at/handle/20.500.12708/200780) | 多假设下的等价关系共享；明确讨论为不同假设复制图的基础方法 | 当前每个 guard 独立图是较简单的已知做法。与本项目 scoped rewrite 证书直接相关。 |
| [Automating Datapath Verification and Bug Correction via Equality Saturation, DVCon 2025](https://dvcon-proceedings.org/wp-content/uploads/1008-2.pdf) | RTL 证明分解与等式饱和辅助功能错误修正 | 不能宣称首次将 egg 用于硬件诊断或修正。 |
| **[Unlocking Hardware Verification with Oracle Guided Synthesis (SMART), FMCAD 2025](https://repositum.tuwien.at/bitstream/20.500.12708/219560/1/Ye%20Leiqi%20-%202025%20-%20Unlocking%20Hardware%20Verification%20with%20Oracle%20Guided%20Synthesis.pdf)** | Section VII-D/E：用 egg 近似检查同一基准的 assertion set 中的等价冗余，105 条 bitvector 和 10 条 Boolean 规则；报告各场景中去冗余比例低于 3% | **最直接的先行工作**。硬件断言等价去重不是本项目首创。SMART 的生成器是 oracle-guided synthesis；其所述 egg 用法是后验冗余评估，并非面向 LLM 修订的具名 scoped proof feedback。 |
| [Contextual Equality Saturation, SAS 2025（2026 proceedings）](https://doi.org/10.1007/978-3-032-07106-4_3) | 条件分支中的局部假设改写，带上下文注解的循环 e-graphs | 上下文敏感等式饱和已是独立研究主题。 |
| [Versioned E-Graphs, PLDI 2026](https://doi.org/10.1145/3808249)（[author PDF](https://programming-group.com/assets/pdf/papers/2026_Versioned-EGraphs.pdf)） | 单一数据结构共享多个条件等价集合；作者报告相对所测基线减少内存并加速 | 跨上下文共享不构成新颖性；未来可用其思想，而非重复发明通用版本图。 |
| [Incremental Equality Saturation, EGRAPHS 2025 workshop](https://pldi25.sigplan.org/details/egraphs-2025-papers/4/Incremental-Equality-Saturation)（[paper](https://rupanshusoi.github.io/pdfs/egraphs-25.pdf)） | 复用同一张图，处理陆续到达的表达式 | 增量加入表达式已有研究；但加入新表达式不同于旧假设变化后的安全撤销。 |
| [Proof Primitives for Equality Saturation-based Automated Provers, VeriLang 2026](https://programming-group.com/assets/pdf/papers/2026_Proof-Primitives-for-Equality-Saturation-Based-Automated-Provers.pdf)；[Checking Equality-Saturation Merge and Extraction Certificates, Isabelle AFP 2026](https://isa-afp.org/entries/Equality_Saturation_Checker.html) | 前者针对 versioned graph 提取含 case split 等步骤的 proof；后者提供经过形式化验证的证书检查框架 | 不能声称首次提取条件证明或首次独立检查 egg 的证明。 |
| [Incremental Formal Verification of Hardware, FMCAD 2011](https://www.cs.utexas.edu/~hunt/FMCAD/fmcad11/papers/8.pdf) | 利用 IC3 在相关硬件版本或性质间复用验证信息 | 硬件增量验证已有历史。 |
| [Shrinking Mission-time LTL Runtime Monitors with Equality Saturation, FMCAD 2026](https://repositum.tuwien.at/handle/20.500.12708/230490) | 针对 MLTL 监控器使用 EggLog 和代价提取，SMT 检查改写等价；作者报告在 1,177 个基准上有 61% 的公式降低内存 | 时序验证监控器的等式饱和优化也已有直接研究；不能仅凭扩展至 temporal monitors 宣称新颖性。 |

### LLM 驱动验证及相邻工具

| 研究 | 已有贡献 | 对本项目的影响 |
|---|---|---|
| [AssertLLM, 2024 preprint](https://arxiv.org/abs/2402.00386)、[FVEval, 2024 preprint](https://arxiv.org/html/2410.23299) | 从规格生成验证断言；FVEval 使用形式化方法比较生成与参考性质的语义等价及蕴含 | LLM 生成断言、等价性评估本身已有研究。 |
| [ASPEN, MLCAD 2025](https://www.csl.cornell.edu/~zhiruz/pdfs/aspen-mlcad2025.pdf) | LLM 引导 E-Graph RTL 改写，使用实际 EDA PPA 反馈优化 datapath | 三者组合不新；它的目标是设计优化而非验证性质管理。 |
| [LGuess: Equality Saturation Guided by Large Language Models, EGRAPHS 2025](https://arxiv.org/abs/2511.00403) | LLM 给出高层改写检查点，e-graph 找可靠的底层改写链；实验为多项式因式分解 | LLM + e-graph + 可检查改写已有先行工作。 |
| [ProofLoop, 2026](https://arxiv.org/html/2604.23100v1)、[Closing the Loop on LLM-Generated RTL Assertions with Quality-Aware Formal Verification, SBCCI 2026](https://arxiv.org/abs/2606.21451) | 求解器驱动迭代修订；后者还包括非空洞/功能检测质量、求解器选择、反例解释 | 单纯把诊断放入下一轮 prompt 或使用 mutation-based quality gate 并不新。 |
| [CircuitProver, July 2026 preprint](https://arxiv.org/abs/2607.27259) | LLM 通过 Lean 4 反馈构造可检查的 RTL 相关证明，并将证明和定理积累为可复用库；作者在 63 个任务中报告证明轮数和时间收益 | 证明携带反馈及跨硬件任务的证明复用这一广义思路已存在。不同点可能是本项目更轻量的有限位宽监控谓词和作用域签名。该论文是预印本，不能与本项目的数字作直接对比。 |
| **[SVApshot, November 2026 preprint / DAC WIP](https://arxiv.org/html/2611.12712v1)** | 将 LLM 断言生成、CNF+相同延迟去重、验证反馈修订、只出现重复断言时停止扩展以及 RTL 回归快照纳入闭环 | 与当前项目的 LLM 多轮性质去重及早停最相关。其 Section 2.1 所述去重范围不同于我们在类型化条件域上构造可重放 proof；尚不能据此断定后者有更好的实际效果。 |
| [AssertLLM2, May 2026 preprint](https://arxiv.org/abs/2605.27472) | 83 个实际设计、13 个功能类别；提供结构化规格、正确 RTL、功能变异，评价形式可证明性、覆盖率等 | 可作更具代表性的外部验证任务来源。 |
| [HierSVA, NeurIPS 2026, November 21 camera-ready](https://arxiv.org/abs/2606.13706v2) | BaseJump STL 342 个模块；作者报告在可评估运行中 82.1% 的断言非空洞地证明通过，但相应断言集合仅检出 70.2% 的符合条件的功能故障，formal core coverage 为 36.2% | 独立证据表明仅追求 pass rate 不能代表验证质量，多轮反馈也存在平台期；为语义回归研究提供较真实的任务来源。 |

## 2. 当前结果究竟说明什么

依据 [上下文证明报告](egg_txn_context_results.md) 与 [真实事务级 LLM 在线实验](egg_frame_txn_live_results.md)：

| 固定的 29 对公式 | 无上下文 egg | 上下文 egg | 同 facts 的普通对照 | 直接 full-width SMT oracle |
|---|---:|---:|---:|---:|
| 12 个真实 LLM 非同形等价对 | 10/12 | 12/12 | 12/12 | 12/12 |
| 16 个等价正例（含四个构造边界正例） | 10/16 | 16/16 | 16/16 | 16/16 |
| 13 个不等价负例的错误接受数 | 0/13 | 0/13 | 0/13 | 0/13 |

- 原子事实发现查询由 1,268 增至 1,628，且未计入全部其他检查开销。不能称为加速结果。
- 这是正确证明的覆盖率，不是 RTL bug 检出率、LLM 准确率或完整 SVA 的一致性。等价对来自同一设计的三个真实初稿；样本小且相关。16 个正例中的四个专门用于边界控制。
- 在两个四字节边界分支撤掉条件事实后，egg 与普通抽象基线均不能证成，而完整位宽目标仍然等价。结论是条件事实对这一抽象表示必要，而非 egg 独有收益。
- Egg 构造了 33 份可重放局部推导（含全域不等价对中的局部等价分支）。106 份输入事实去重得 58 份；实际使用按图去重为 57 次、32 种事实。这是待验证的共享机会，不是已测的节省。
- 三次事务级真实 LLM 初稿均 9/9，18 次追加回复无实质修改且消耗 86,418 tokens。证书反馈机会为零，不能宣称反馈改善 LLM 的准确率或成本。既有独立 formal harness 对有限深度和单帧输入约束作 BMC，未直接证明所有模型生成式渲染后的时序 SVA，更不是无界全 DUT 正确性证明。
- [实际边界轨迹](egg_txn_context_physical.md) 支持 `data_n=4` 有真实行为意义，但不证明每个 SMT 自由赋值均为 RTL 可达状态。

## 3. 可辩护的研究问题

**Research question:** Can context-scoped, independently replayable e-graph explanations improve the semantic maintenance of evolving LLM-generated RTL verification properties over equivalently informed SMT and normalization baselines, without losing verification quality?

与 SMART 的主要区别不应只是“断言来自 LLM”，而是跨 LLM 轮次/规格变更时处理证明依赖、分支限定等价和剩余待验证义务。与 SVApshot 的区别不应只是换了去重数据结构，而是检查类型、时序和上下文并为可复用结论提供证据。与 CircuitProver 的区别应落在轻量、有限位宽形式验证管线，不能宣称证明复用是原创概念。

示例：令 `N=data_n, I=data_index`。在 guard `N=4` 下，`I=4` 和 `I=N` 可合并；guard 改为 `N=5` 后，不允许把旧合并当作新域上的等价。若仅表达式写法或保留原上下文的有效等价事实发生无语义改变的编辑，可研究是否无需重新搜索该 proof；独立证据不足时必须重新验证或报告 unknown。对 D、环境模型 A、性质 P 的关系，要明确区分自由位宽的 `P ≡ Q`、`A ⊨ (P ↔ Q)` 和 DUT 上的 `D,A ⊨ P`。只有前提和时序语义保持且原始性质证明适用时，才能转移其验证结论。

性质修订不只有等价/不等价两类：在相同语义与假设下，对「成立谓词」可以用双向蕴含区分等价、新性质强化、新性质弱化、不可比和 unknown；若原表达式编码的是违规报警，必须先统一极性。Egg 的等价类适合管理等价关系；单向蕴含不是等价，不能直接合并 e-class，需要使用 SMT 等独立方法判断。非等价时应报告差异上下文和可核验的剩余义务，而不是将所有语义变化视作错误。

## 4. 建议的后续实验（尚未执行）

1. 首先利用现有归档，固定多个真实候选和预声明的语义保持/改变的性质版本；加入新的、互不重复的 RTL 模块（可依据 FVEval、AssertLLM2 的数据和支持的子语言选定）。不将人工改变当作真实模型错误。明确 clock、reset、采样时刻、位宽、符号性、环境假设、ghost tracker 和 RTL 版本。
2. 同一数据、规则、事实、资源预算比较：(a) 规范化/CNF；(b) 普通共享命题事实；(c) 完整位宽增量 SMT（共享上下文、允许缓存及证据复用）；(d) 现有逐对 scoped egg；(e) multi-target scoped egg 加共享证书依赖。若衡量 proof 体积或人/LLM 可用性，非 egg 组也要提供相应的结构化上下文、SMT 证据或反例，不能只给一个 pass/fail。
3. 设计版本更新：相同语义改写、边界修改、位宽改变、时钟/复位或环境假设变化；旧 equality 只有在新作用域有效时才复用。记录真正可复用与真正失效的证据、误复用/漏复用、未知率、独立检查通过率，分离 SMT 判定、图构建、证明提取、检查成本。对照使用相同缓存键与失效规则，避免将 caching 的收益归因于 egg。任何不等价或未验证的结果不自动合并。
4. 选择具有实际区分度的非天花板 LLM 任务；先固定初始候选，再按反馈类型配对：普通反例、同信息量 SMT/结构化诊断、egg replayable proof。正确初稿早停，不能重抽直到找到错例。评价首次合格的修订数/tokens、独立性质正确性、覆盖率、非空洞与功能检测质量，并统计全部真实任务和困难子集及失败。避免仅在当前模型已熟练的九个谓词上反复调用。

**Decision rule:** 即使不加速 RTL formal，若能够在多候选和多版本条件下产生更小/可复用的检查证据，降低重复人工/LLM 推理，或可靠精确识别失效证明，且不增加误接受、不降低性质质量，则有实际价值。优于弱基线不足以证明 egg 的独特优势。若强 SMT/普通方法在质量、证据复用和总成本上均持平或胜出，就报告适用边界的负结果，不继续为引入 egg 而引入 egg。

## 5. 建议报告写法

> Prior work has established equality-saturation-based datapath verification, assertion redundancy checking, contextual e-graphs, proof extraction, and solver-guided LLM assertion generation. We investigate their intersection in a typed, context-scoped evidence workflow for evolving LLM-generated RTL verification properties. On our initial workload, contextual reasoning improves proof coverage, but an equally informed non-e-graph baseline matches that coverage. We therefore treat the incremental, independently checkable explanations and their effect on verification maintenance and model feedback as hypotheses requiring controlled evaluation rather than claiming an established end-to-end speedup or a new equality-saturation algorithm.

本次仅增加文献与研究定位文档；未修改 RTL、验证代码或已有结果，也没有新增 API 调用。
