# Milestone 3 · Dependency-Driven Proof Reuse：Mac 跨平台复现与研究路线

**结论：**2026-11-25 MacBook 的 `egg-dependency-20261125-225657.tar.gz` 完成了主实验与后续分流消融。Mac/Linux 全部语义判定、typed SMT 查询次数、具名证明步骤、历史路径及最终证明库一致。两轮上传证据在云端重新通过完整独立审计。首次证明的全事实枚举仍是主要查询成本（9 属性组合 399/410），另发现 Mac native 调用阶段每次约 0.2 s 的高成本。相对原 Egg 有实质改进，但普通 UNSAT-core 方法也有相近或更大的收益；暂无 Egg 独占加速或 LLM 质量改善证据。

[原实验协议和结果](egg_dependency_reuse_results.md) · [原始 Mac 归档及复核](../results/milestone3/frame-txn-dependency-reuse-mac/) · [跨平台逐工作量记录](../results/milestone3/frame-txn-dependency-reuse-mac/cross-platform.json)

## 1. 完成性与跨平台一致性

上传原文件逐字节保存，`._` AppleDouble 文件仅是归档元数据，不纳入科学统计。每轮四份证据文件均匹配 audit SHA-256。云端从锁定原始 API 档案重建输入、重新认证完整位宽事实、检查方向查询及重放历史证明/core、重建库和计数；未重新搜索 native 图。

| 项目 | Mac 和已存 Linux |
|---|---|
| 数据、23 条通用规则、顺序、分组、来源哈希 | 一致；不同平台的 binary SHA-256 不同 |
| Primary | 264 请求 / 105 组 / 6 臂，全通过 |
| Triage | 同 264 请求 / 105 组 / 4 臂（含两条重复基线），全通过 |
| 分类：等价 / 强化 / 弱化 / 不可比 / 不可行 | 233 / 9 / 15 / 6 / 1；无错误等价接受 |
| 最终证明库、具体推导及路径、查询计数、建图次数 | 两轮一致 |
| 主实验逐组记录 | 12/105 组、72 处标量差异，仅 `native.graph.enodes` 与 `native.graph.targets[].eclass` |
| 后续实验逐组记录 | 12/105 组、33 处同类差异 |
| 汇总差异 | 仅耗时及部分 `native_graph_counts.enodes_sum` |
| RTL 快照差异报告 | 一致；云端重算逐字节相同 |

因此不能声称 native 图逐字节一致。内部 ID 不携带跨平台证明语义，而实际 checked proof、端点、依赖、分类和历史库可重现。和前一轮完整云端重跑比较也得到相同的结果。6×264 + 4×264 = 2,640 次 arm-request 判定并非独立自然模型错误样本。本轮新增模型 API 调用为 0，使用历史真实 `gpt-6.1-sol/low` 公式和受控组合；上传包没有 Mac 专项测试 stdout，不能从归档确认用户是否另行执行了那 10 项测试。

## 2. 查询成本及证明质量

总 typed SMT checks 计入 guard、事实发现、实际依赖再认证、完整目标方向、typed triage，包括初始及失败成本；不把缓存命中或 abstract Boolean checks 数成 typed solver 查询。

| Workload | 原 Egg | 依赖优先 Egg | 依赖+分流 Egg | 普通 core+分流 | Direct SMT subscope | Egg 相对原查询降幅 |
|---|---:|---:|---:|---:|---:|---:|
| Matrix 224 | 581 | 583 | 516 | 505 | 57 | 11.19% |
| 真实 API 历史（6） | 181 | 181 | 153 | 153 | 10 | 15.47% |
| 多跳 ladder（10） | 288 | 214 | 139 | 139 | 19 | 51.74% |
| 1 属性组合 | 357 | 132 | 76 | 76 | 15 | 78.71% |
| 3 属性组合 | 587 | 218 | 120 | 120 | 15 | 79.56% |
| 5 属性组合 | 1897 | 718 | 376 | 376 | 15 | 80.18% |
| 9 属性组合 | 2079 | 786 | 410 | 410 | 15 | 80.28% |
| 本固定混合工作量合计 | 5970 | 2832 | **1790** | 1779 | 146 | 70.02% |

合计受较复杂受控组合主导，不是普遍 RTL/LLM 查询减少 70% 的统计。原矩阵缓存已充分，纯依赖优先反而多两次查询。真实历史纯依赖优先仍为 181；只有已确认前提失效的 typed triage 跳过两次不等价 stale carry，建图 4→2。整个 workload 建图 51→41。61 项非恒等等价请求中，原 Egg、dependency 及 triage 均有 59 项可核验路径（matrix 29/31，其余 30/30）。普通 core 路径为 60/61（允许精确 guard 内的 typed fallback 前缀）。Triage 保持 proof-route 覆盖，但完全无需全目标查询的非恒等正例从 59 降到 55，因为有的旧依赖失败而目标仍成立，需额外目标检查。

实际历史生成 20、26 步两条证明，返回 N=4 时重放 20 步旧证书。受控梯形 P→Q→R（Q=P∧N<8，R=P∧N<9）在 N=5 仅认证两个依赖，且 N<8 不在当前 P/R 的词表中；在 N=8 原路径失效但 P↔R 仍等价，找到替代证明。N=8 P↔Q 或 N=9 P↔R 才判定弱化。这证明 **proof invalidation 与 specification regression 不同**，历史证明可跨中间端点组合而不降低质量。

## 3. Mac 真实计时与新增瓶颈

| Workload | 原 Egg (s) | 依赖+分流 Egg (s) | 普通 core+分流 (s) | 直接 SMT subscope (s) | Egg 相对原耗时减少 |
|---|---:|---:|---:|---:|---:|
| Matrix | 8.609 | 7.911 | 0.864 | 0.350 | 8.11% |
| Real live | 1.095 | 0.611 | 0.202 | 0.077 | 44.22% |
| Ladder | 1.218 | 0.614 | 0.220 | 0.150 | 49.58% |
| Portfolio 1 | 0.812 | 0.301 | 0.104 | 0.108 | 62.94% |
| Portfolio 3 | 1.076 | 0.383 | 0.192 | 0.283 | 64.35% |
| Portfolio 5 | 2.448 | 0.703 | 0.514 | 0.607 | 71.27% |
| Portfolio 9 | 2.704 | 0.811 | 0.626 | 0.972 | 70.02% |
| 合计 | 17.961 | 11.334 | 2.724 | 2.546 | 36.90% |

计时是每臂各 workload 单次 wall time（包含 SMT、native invocation 和检查，不含独立 oracle、audit、build 或 API）。同机有描述性收益：9 属性组合 Egg 比直接 SMT 短约 16.6%，普通方法仍更短。普通方法在 Mac 七组均快于优化 Egg。Linux 的 3 属性组合中 Egg 与直接 SMT 的相对顺序不同；没有足够重复样本，不能声称可普遍跨平台加速或将差值归因于具体 Mac 硬件/OS。

| Mac 优化 Egg | Native 次数 | Native 调用累计 | 每次平均 | Native proof 检查累计 | Native 占该臂总时间 |
|---|---:|---:|---:|---:|---:|
| Matrix | 33 | 7.032 s | 213.1 ms | 13.1 ms | 88.9% |
| Live | 2 | 0.411 s | 205.7 ms | 2.6 ms | 67.4% |
| Ladder | 2 | 0.409 s | 204.6 ms | 1.2 ms | 66.6% |
| Portfolio 9 | 1 | 0.205 s | 205.0 ms | 1.2 ms | 25.3% |

`run_egg_regression.py:invoke` 的 native timer 包含 JSON、`subprocess.run`、Rust 处理和 stdout 解析，**不是 saturation 内部时间**。原 Matrix eager 在 Mac 35 次 native 调用累计 7.725 s（平均约 221 ms），Linux 对应 0.847 s（约 24 ms）。近似固定的每次 0.2 s 是待分解的调用成本线索，不能未经实验就断言进程启动、IPC 或 Egg 算法本身是唯一成因。

另一个确定瓶颈是 9 属性组合中 410 次总查询的 **399 次（97.3%）发生于第一次证明**；N=5/6/7 每次仅 2 次（guard + 实际依赖），N=8 失效 5 次，回到 N=4 零次。热复用已很便宜，初次完整事实发现仍不经济。

## 4. Formal verification 与真实 RTL

复用了 30 条原版/变异/额外控制轨迹、18,160 PRE/POST snapshots，复核新增 live/ladder/portfolio 共 40 请求。31 项等价均在两套采样命中 guard 且无差异/unknown；主 21 条轨迹区分全部 8 个不等价请求，另 9 条区分其中 5 个。真实 stale preflight 的主轨迹差异仍为 84、56，额外轨迹 36、24；9 属性组合 N=8 弱化漏报 69 个主采样、38 个额外采样。本次未重新运行时序 RTL BMC。

本轮 formal verification 是**自由类型化二态快照、指定 guard 下的监控器等价/强化/弱化/不可比**。真实轨迹交叉检查与完整位宽符号证明彼此补充。原始 [full-wrapper 有界事务验证](egg_frame_txn_results.md) 的 8 项安全属性、18 状态、单帧环境假设不变；不能把 monitor 等价直接视为任意多帧或无界 DUT 正确性。将来复用 temporal verification verdict 时必须绑定 DUT 版本、时序性质与环境约束，独立认证变化后仍满足旧证明的适用条件。

## 5. Milestone 3 的累计成果

| 阶段 | 实际成果 | 结论 |
|---|---|---|
| 基础 guard 和 witness 优化 | 索引匹配保持 Controller/SPI/I²C 原证明，arbiter 认证循环从 135.91→11.49 ms；直接位并行 8.04 ms；普通与 Egg Controller 对照都 148→87 调用 | 大部分完整循环收益来自 witness 搜索，Egg 未额外省 Controller 求解；见 [M3](milestone3.md)、[追加实验](milestone3_followup.md) |
| 证明工程 | 可查 waiver、规则撤回、依赖和真实 RTL 编辑证据；Controller 的 70 条历史证明只引用 50 条规则，71 个受影响的撤回组合中 Egg/普通均恢复 57 个 | 可以定位何处失效、复核剩余结论，但普通方法也能完成部分任务；见 [证明应用](milestone3_proof_applications.md) |
| RTL 属性与在线 LLM | FIFO、Frame 真 API；九项跨周期事务规范检测六种内部变异从 3/6 到 6/6；真实 full-wrapper 八项安全性质有界 8/8、6 cover、2 变异反例 | 验证质量来自独立规格和可信 ghost tracker。三个真实九属性无辅助初稿都是 9/9，18 次后续修订原文不变；见 [事务](egg_frame_txn_results.md)、[在线](egg_frame_txn_live_results.md) |
| Proof-Carrying / Context-Aware | 检查 proof 进入后续真实 API prompt；4→5→4 的生成、阻止、再生成、重放；224 次语义回归共享 53→35 张图、全部判定正确 | 证据生命周期成立，但实际三组输出相同、raw/ordinary/egg token 3292/4936/9859；见 [语义回归](egg_regression_results.md)、[真实反馈](egg_regression_live_results.md) |
| Dependency-Driven | 264 请求、只复核实际依赖、跨中间原子、安全失效分流、Mac/Linux 证书和计数复现 | 建立可核验的验证证据维护机制；还未胜过普通依赖或直接 SMT 在真实 workload 的效率 |

推荐研究定位为 **Context-Aware Equality Saturation for Semantic Regression and Proof Reuse in LLM-Driven RTL Verification**：持续维护随 LLM 和规格修订变化的正式语义证据。此前 [相关工作](egg_related_work_and_research_value.md) 已涵盖 SMART、Versioned E-Graphs 等；不能将条件 E-Graph、断言等价去重或证明复用本身宣称为首次提出。Egg 的具名改写路径是可进一步利用的结构信息，但尚未验证这比普通 UNSAT-core 更有用。

## 6. 下一阶段路线

### 第一优先：Demand-Driven Proof Construction（按需构建可认证的条件证明）

利用 399/410 冷启动证据，将“先枚举事实→再找证明”改成“先找候选证明→只认证实际需要的 typed obligations”。

1. 用同一无条件规则从端点建立 E-Graph，相关条件等式只作为待认证 obligation；将候选路径规划与已认证证明状态隔离，不因未认证的合并接受等价。
2. 抽取候选推导，按预计新增前提成本选择候选，只对实际使用的前提做完整位宽检查。`UNSAT` 才授权具名等式、独立逐步 replay。`SAT` 排除该路径错误前提而不是直接宣布目标不等价，尝试替代证明。
3. 未知或预算用完，安全回退完整 typed SMT。记录失败尝试、额外 native 图及全部成本；不只统计成功路径的少数前提。
4. 冻结原七组 workload，分别报告冷启动、有效 guard 迁移、失败及返回旧 guard；再扩充新真实设计/性质级留出样本，避免将受控属性拼接视为新独立 DUT 或自然模型错误。

### 配套工程消融：native cost breakdown

对相同输入比较一请求一进程与常驻 Rust worker。先分别记录启动、IPC/JSON、建图与 saturation、提取、独立检查及 SMT 时间，worker 每请求独立重建图与上下文，避免混淆 transport 和图增量复用。保留旧入口与 checker；Mac/Linux 各自至少五轮交错运行，报告 median/IQR，不得排除首次成本或改变求解预算。这个优化是消除平台测量干扰，而非独立研究贡献。

### 第二研究假设：Dependency-Aware Explanation Selection

同一目标有多条合法证明时，探索选择依赖更少/适用 guard 更广的证明，而不只取最短步骤。在 C05 中，P→Q→R 含 N<8 导致 N=8 失效，而只依赖 N<9 的 P→R 证明仍成立。比较依赖成本和可迁移性选择、最短证明、普通 UNSAT-core minimization；不根据未来 guard 或 grading oracle 选择历史路径。测量后续失效、重证明次数与依赖大小。若相对 ordinary 没有收益，仍可如实报告可核验结构化证据的能力。

### 对照与接受条件

| 比较组 | 目的 |
|---|---|
| Direct SMT exact/subscope（另测只需等价时的直接 XOR） | 强非 Egg 基线 |
| Ordinary core dependency+triage | 已得到相近收益的非 Egg 证书基线 |
| Ordinary lazy discovery/core | 同候选信息/预算，隔离按需认证的通用收益 |
| 当前 Egg dependency+triage | 对照冷启动及失效成本 |
| Demand-driven Egg | 新实验组 |
| Demand-driven + explanation selection | 单独冻结的后续消融 |

报告正确分类、零错误等价接受、有证路径覆盖、冷/热 typed solver queries/时间、native/IPC/重放时间、失败路径、重试与 fallback、实际依赖/路径大小、后继复用和失效；unknown 单独报告，不算正确。新真实模块应保留独立规格、真实修订和受控错误来源；先固定数据和预算再测。只有与强 ordinary 公平对照后才可宣称 Egg 特异收益。

之后才把精简 proof ID、实际依赖、具体失效及 typed 差异接入已有 Proof-Carrying LLM loop，比较同信息和 token 预算的普通反馈 vs Egg 结构化反馈，测量真实非平凡修订的成功率、轮数、token 和 RTL/形式规格质量。此前在线 ceiling 和 token 增加说明不适宜重复易例。应预注册全部首次生成样本、不因初稿已经通过而删除 trial，并区分真实修订与受控场景。上述研究是下一阶段建议，不是本次已完成实验。

## 7. 保存与复现

依赖工具环境见 [原复现说明](egg_dependency_reuse_results.md#6-环境脚本与从-mac-复现)：Python 3.12、Z3 4.16.0、锁定 Rust/egg 0.11.0；云端重新审计使用原 Linux 环境，无需 Mac binary 或新 API。新增脚本 `compare_egg_dependency_platforms.py` 核对原审计绑定、同冻结协议、证书/逐组差异类型、计数和单次时间；不把合法的不同证明当成算法失败。既有 `audit_egg_dependencies.py` 重做 typed 和 proof 审计、`summarize_egg_dependencies.py` 重算对照、`check_egg_dependency_physical.py` 重算真实轨迹计数，均已在本次执行。

```bash
FPY="$HOME/rtl-tools/frame-venv/bin/python"
REF=results/milestone3/frame-txn-dependency-reuse
DATA=results/milestone3/frame-txn-dependency-reuse-mac
VERIFY=$(mktemp -d /tmp/egg-dependency-mac.XXXXXXXX)
tar -xzf "$DATA/transcript.tar.gz" -C "$VERIFY"
MAC="$VERIFY/egg-dependency-20261125-225657"
"$FPY" scripts/audit_egg_dependencies.py --run-dir "$MAC/primary" --output "$VERIFY/primary-audit.json"
"$FPY" scripts/audit_egg_dependencies.py --triage --run-dir "$MAC/triage" --output "$VERIFY/triage-audit.json"
"$FPY" scripts/summarize_egg_dependencies.py --primary "$MAC/primary" --triage "$MAC/triage" --output "$VERIFY/comparison.json"
"$FPY" scripts/check_egg_dependency_physical.py --output "$VERIFY/physical.json"
"$FPY" scripts/compare_egg_dependency_platforms.py --reference "$REF" --candidate "$MAC" --output "$VERIFY/cross-platform.json"
cmp "$VERIFY/comparison.json" "$MAC/comparison.json"
cmp "$VERIFY/physical.json" "$MAC/physical.json"
cmp "$VERIFY/cross-platform.json" "$DATA/cross-platform.json"
```

保存原始 `transcript.tar.gz`、`provenance.json`（源与载荷哈希）、两份 `*-cloud-audit.json`、`cloud-physical.json` 及 `cross-platform.json`。没有修改原依赖实验、RTL、LLM loop，也没有新增 API 调用。
