# Milestone 3 · Context-Aware Semantic Regression：Mac 真实 API 结果

**结论（2026-11-25）：**本次真实在线实验成功演示了上下文限定 Egg 证明在 LLM 多轮性质维护中的完整生命周期：生成、随上下文切换阻止复用、重新生成、返回原上下文后重放旧证明。三个反馈组在三个阶段均首轮正确，逐阶段输出逐字相同。Egg 没有改善 LLM 的成功率或调用次数，反而使总 token 约为普通反馈的 2 倍、原始 SMT 反馈的 3 倍。这是**证明维护机制的正面证据、模型收益的无增益结果**，不是总体 RTL 验证加速的证据。

[冻结在线 pilot 设计](egg_regression_live_pilot.md) · [离线语义回归对照](egg_regression_results.md) · [研究定位及相关工作](egg_related_work_and_research_value.md)

## 1. 归档完整性与真实调用计数

输入为用户 Mac 上传的 `egg-regression-20261125-172728.tar.gz`。独立审计区分了以下四类数据，而没有因同一压缩包混合它们的计数：

| 目录 | 内容 | 完成情况 |
|---|---|---:|
| `main/` | 新 Egg 和三个基线的固定工作负载 | 224 请求 / 66 组 |
| `fixture/` | 人工编写的 stale-candidate 控制序列 | 12 fixture 响应、0 API |
| `live/` | 第一次失败的尝试 | 第一个 Raw 请求收到 HTTP 401；0 完成响应，无使用量回执 |
| `live-20261125-173313/` | 成功的真实在线对照 | **9 个 HTTP 200 / completed 响应，预算上限 18** |

初次 401 的请求记录为 `dispatch_attempted=true`，但没有可用的 provider response ID 或 usage；因此仅将它记为一个失败的网络派发，不添加虚构 token，也不把它算进模型语义成功率。其 config、seed、第一次 preflight 和 request 文件与成功 run 起点逐字节一致（[失败尝试核对](../results/milestone3/frame-txn-regression-live/incomplete-audit.json)）。成功 run 有九个不同 response ID，所有 usage 加法正确。独立审计重建其完整请求顺序、原始候选、当前及历史反馈、各阶段提前停止条件、证明库与 summary。这里核验的是归档的 provider 回执，不等同于另行查询 provider 的发票或服务端日志。

归档清理只去掉 172 个 AppleDouble/Finder 元数据条目，并去除外层目录包装；120 个非元数据文件（包括失败尝试）全部逐字节保留。源哈希和每文件哈希在 [provenance](../results/milestone3/frame-txn-regression-live/provenance.json) 中。新的 [真实在线逐请求审计](../results/milestone3/frame-txn-regression-live/audit.json) 核对了 49 个真实 run 文件；另审计 58 个 fixture 文件。这些审计均不调用模型或重新搜索 Egg 图。

## 2. Mac 离线复现是否成功？

独立重跑 `audit_egg_regression.py` 审计全部 224 请求和 66 组，结果与 Mac 原有审计除耗时外一致。与之前 Linux 归档比较，224 条完整非图请求记录、全部语义分类、proof store 内容、计数报告完全一致。七个组的 native 图形态/计数有差异；汇总中只 `enodes_sum` 和耗时变化，不能声称全图逐字相同或平台时间可直接比较。

| 评价 | Mac 复现结果 |
|---|---:|
| 语义分类（等价/强化/弱化/不可比） | 202 / 9 / 9 / 4 |
| 四种方法正确分类 | 均 224/224 |
| 其中原式恒等比较 | 171（不作为 Egg 增益） |
| 逐对 Egg / 共享 Egg 图次数 | 53 / 35 |
| 非恒等新 proof steps（逐对 / 共享） | 106 / 59 |
| 共享 proof store 边 / 历史路径复用次数 | 15 / 8 |
| 被阻止路径的依赖重查 | 46 次确实失效、6 次仍有效但本批无事实（52 次缺失依赖出现、27 个不同重查义务） |
| 现有 RTL 轨迹区分的非等价控制 | 18/22 |

| 工作类别 | 直接增量 SMT + cache/connectivity | 普通同事实 | 逐对 Egg | 共享 Egg |
|---|---:|---:|---:|---:|
| 计入共同事实发现的实际 typed SMT checks | **69** | 570 | 581 | 581 |
| Mac native Egg 进程时间（含启动） | — | — | 11.381 s | 7.464 s |
| Mac 相应操作计时项之和（不含离线 oracle/audit） | 0.475 s | 0.818 s | 12.239 s | 8.384 s |

Mac 的逐对/共享原生进程时间差约 **34.4%**，是相同实验下共享与逐对两种 Egg 方式的对照；其总体操作时间仍远高于直接增量 SMT。Linux/Mac 图节点累计分别为 90,734/91,875（逐对）、86,122/86,685（共享），图大小不是跨平台不变量。Mac 数据与 prior Linux 结论一致：在这些任务中 Egg 的主要输出价值是具名、可重放、带依赖的证明，而不是替代高效求解器。

[详细跨平台比较](../results/milestone3/frame-txn-regression-live/mac-reproduction.json) · [独立重算的 Mac 离线审计](../results/milestone3/frame-txn-regression-live/mac-offline-audit.json)

## 3. 真实模型产生了什么？

配置为 `gpt-6.1-sol`、`reasoning_effort=low`、每次最大 2048 输出 tokens。所有组从此前真实 T1 初稿中已经过完整位宽认证的 `data_last` 参考开始，而不是从自然语言规格重新合成全部 RTL 断言。固定三阶段 `(data_n=4) → (data_n=5) → (data_n=4)`，每阶段实际第一请求必须完成一个字面量重写；语义及句法同时合格立即停止。参考公式、所需字面量、当前 guard 均明确给到模型。

| 真实在线指标 | Raw | Ordinary | Egg |
|---|---:|---:|---:|
| 三个阶段最终合格 | 3/3 | 3/3 | 3/3 |
| 三个阶段第一次回复合格 | 3/3 | 3/3 | 3/3 |
| 实际 API 响应 | 3 | 3 | 3 |
| LLM 回复语法或语义失败 | 0 | 0 | 0 |
| 切换后 carry-in preflight 非等价 | 2 | 2 | 2 |

最后一行是**人为改变上下文导致上一阶段合法候选失去新上下文中的等价性**，不是模型答错两次。同一阶段三个模型输出完全相同；整个实验只出现两个不同的合格原式（A4 和 A5）。因此 9/9 仅描述三组在此次计划任务上的成功，不是九个独立任务或大样本泛化结论。

设 `N=data_n`、`I=data_index`、`D=data_done`，`C` 表示原非复位、输出有效及数据 entitlement 检查保持不变。归档实际输出的不同部分可准确概括为：

```text
参考：C ∧ (m_last XOR (I=8 ∨ (D ∧ ((N<4 ∧ I=4) ∨ (N≥4 ∧ I=N)))))
A4：  C ∧ (m_last XOR (I=8 ∨ (D ∧ I=4)))
A5：  C ∧ (m_last XOR (I=8 ∨ (D ∧ I=5)))
```

这是模型主动去掉不必要的分支并替换动态索引的**真实自然写法**，不是把 fixture 的机械一次替换伪装为模型输出。三组都产生 A4 → A5 → A4；所有输出在各自 current guard 下通过独立全位宽双向 SMT，而不是由 egg 自行判断正确。

## 4. Egg 在真实 LLM loop 中是否真的发挥了作用？

| 阶段 | Preflight：旧候选在当前 guard | 真实回复后的 Egg 结果 | 新原生图调用 |
|---|---|---|---:|
| N=4 | 原始参考恒等，但不满足字面量重写要求 | A4 的新可核验证明 P4，20 步、3 个具名依赖 | 1 |
| N=5 | A4 变成 incomparable；阻止 P4；图达到 20 轮限制、未合并 | A5 的新可核验证明 P5，26 步、3 个具名依赖 | 2 |
| N=4 | A5 变成 incomparable；阻止 P5；图达到 20 轮限制、未合并 | A4 **重放原 P4 的 20 步**，无需新图 | 1 |

共 4 次 native graph（2 次成功合并、2 次达到迭代上限）；2 个不同的非恒等 proof store 记录、46 步新证明、1 次 20 步历史重放。原始 P4 与 P5 分别为 `proof-c7157570…`、`proof-f3c09328…`。独立审计从空证明库按阶段重建内容 ID，核对图请求、每个具名改写及证书依赖，最后得到完全相同的 store。不因为证明引用缺失或图未合并就宣称非等价；方向 SAT 才说明真实 typed difference。

### 失效依赖是真错误还是仅仅缺失证书？

| 原始局部事实 | 旧 guard | 新 guard | 独立重查 |
|---|---|---|---|
| `(eq 4 data_index) = (eq data_index data_n)` | N=4 | N=5 | 两方向 SAT，确实不等价 |
| `(eq data_index data_n) = (eq 5 data_index)` | N=5 | N=4 | 两方向 SAT，确实不等价 |

两条正好是各自已归档 proof 实际使用的依赖，而不是只因 context ID 变化就否决。另两条公共事实 `N<4=false`、`N≥4=true` 在从 4 切换到 5（或反之）时仍成立。系统明确定位失效层级并保留旧上下文的证书。

例如 stage 2 的 exact typed witness 在 `N=5,I=4,D=true,m_valid=true,rst=false,data_count=0,input_count=1` 时：参考要求 I=4 尚不是帧末，而 stale A4 要求 I=4 已是帧末。所以 `m_last=true` 时旧候选漏报参考违规，`m_last=false` 时旧候选额外报警。它们是自由二态赋值的语义见证，真实轨迹相关性见下一节。

### 证明是否实际进入模型请求？

已逐字重建并核对九次保存的 `request.json`：

- Egg 第 1 阶段的 preflight 只有恒等检查，没有非平凡历史证书。
- 第 2 阶段真实请求包含历史 P4 的 ID、作用域、已核验的 20 步中前 8 步（明确标记不完整）、当前 guard 的 blocked dependency ID 和 typed SAT witness。
- 第 3 阶段真实请求包含历史 P5 的 ID、26 步中前 8 步和新的失效诊断。
- 第 3 阶段**得到回复后**才端到端复用 P4；没有第 4 阶段，因此这次复用的结果未进入后续模型请求。不能说重用 P4 导致模型第 3 阶段成功。

这证实 proof feedback 确实被序列化到真实模型请求中，但不是将完整 20/26 步机器证书全部传入模型；完整证书只在本地归档与独立检查器中。Raw 和 Ordinary 同样得到了当前 guard 的 typed 反例及权威参考，因此都能一次修订成功。三个 arm 的归档方向义务一致，不过 stage 2 Ordinary 的 `old_only` SAT 见证选择 I=5，Raw/Egg 选择 I=4；均有效，说明共同 SMT 信息在逻辑上相同而非保证每个具体见证字节完全一致。更严格的因果反馈比较应共享同一候选和同一固定见证。

在本 pilot 中，所有组每个 preflight/reply 都重新进行完整 typed grading（每组 6 次 assessment，每次 1 feasibility + 2 directional obligation），且 Ordinary/Egg 的共同 primitive fact discovery 都是 175 次 miss、256 次 cache hit。实际 proof reuse 避免一次 native search，但**没有跳过这一轮的完整 SMT grading**。这些计数不包含独立核对器重复查询，不把 graph-skip 说成求解器-skip。

## 5. Token：实际更贵，原因在哪里？

| 阶段 | Raw total | Ordinary total | Egg total |
|---|---:|---:|---:|
| N=4 | 941 | 1,324 | 1,655 |
| N=5 | 1,172 | 1,757 | 3,723 |
| 恢复 N=4 | 1,179 | 1,855 | 4,481 |
| **全部** | **3,292** | **4,936** | **9,859** |

| 用量 | Raw | Ordinary | Egg | 总计 |
|---|---:|---:|---:|---:|
| Input tokens | 2,995 | 4,639 | 9,562 | 17,196 |
| Output tokens | 297 | 297 | 297 | 891 |
| Total tokens | 3,292 | 4,936 | 9,859 | **18,087** |
| Reasoning tokens（provider 明细） | 0 | 0 | 0 | 0 |
| Cache read tokens | 0 | 0 | 0 | 0 |
| Cache write tokens（input 明细，不额外相加） | 2,147 | 4,630 | 9,553 | 16,330 |

Egg total 是 Raw 的 **2.995×（+6,567 tokens，+199.5%）**、Ordinary 的 **1.997×（+4,923 tokens，+99.7%）**，而且各组输出 99 tokens/次，没有修订轮次或输出质量的节省。因为没有发票和 provider latency 记录，只比较实报 token 数，不估算精确美元成本或 API 端到端运行时间。

归档当前消息的紧凑 JSON UTF-8 bytes（不是 token）分别是 Raw 11,271、Ordinary 15,866、Egg 28,258。Egg stage 2、3 当前整个请求为 10,712/12,347 bytes；历史阶段 Egg 单个子对象（含 8 步前缀的重复抽象表达式）自身已占 3,511/4,862 bytes，另有当前 blocked 诊断、atom 对照和公共事实。尽管原生证明在阶段 3 成功复用，长历史反馈仍被发送。这正是后续应检验的 feedback compression/按 ID 引用的成本问题，而不是模型输出更复杂。

## 6. 独立检查真实 A4/A5 在原始 RTL 上的作用域边界

前一轮物理复核针对固定控制修改；本轮额外使用真实 API 返回的两个简化原式，逐个独立求解在 N=4、N=5 和不限制 N 时的语义，再在同一锁定的 21 条原版与功能变异轨迹（12,712 PRE/POST 快照）及 9 条额外对照（5,448 快照）上复核。独立 imperative `data_last` oracle 与原 T1 参考无差异；比较双方使用相同 X/Z completion。本实验的所有计数都是性质×观测快照，不是 bug 数量，也不把局部和全域重复采样相加为不同故障。

| 实际模型表达式 | 比较作用域 | 完整位宽语义 | 主轨迹作用域样本 | 主轨迹差异 | 额外对照差异 |
|---|---|---|---:|---:|---:|
| A4 | N=4（实际合格域） | equivalent | 853 | **0** | 0（363 样本） |
| A4 | N=5（错误复用） | incomparable | 316 | 84（2 漏报、82 新增） | 36（132 样本） |
| A4 | 不限 N | incomparable | 12,712 | **612** | **270** |
| A5 | N=4（错误复用） | incomparable | 853 | 56（4 漏报、52 新增） | 24（363 样本） |
| A5 | N=5（实际合格域） | equivalent | 316 | **0** | 0（132 样本） |
| A5 | 不限 N | incomparable | 12,712 | **922** | **420** |

所有上述比较均无未知差异。在指定 guard 内，真实候选与原参考报警完全相同：N=4 主语料 4 次、N=5 主语料 2 次。若错误地去掉作用域，甚至在未修改的正确 RTL 原版上，A4/A5 也会分别产生 **90/140 次额外报警**；错误跨用到 N=5/N=4 则分别产生 12/8 次原版报警。这比仅观察 solver 的 SAT 更直观地展示必须保留证书的 guard。仅可在已认证的上下文替代原公式；不应把局部语义合格的结果无条件部署为全域性质。

[实际输出的完整物理及 typed 对照](../results/milestone3/frame-txn-regression-live/live-physical.json)

**Formal Verification 的边界：**当前报告独立使用 QF_BV solver 检查所有声明位宽的二态快照在给定 guard 下的双向语义等价性，并实际重放 Egg equational proofs；另有真实 RTL 语料复核。不是用 Egg 对 DUT 本身执行无界 temporal model checking。本次没有新运行序列 RTL BMC；既有 [事务级 RTL formal](egg_frame_txn_results.md) 的原有 harness、深度及环境假设依旧成立，不将 scoped monitor 的正确性自动扩大成整个设计的时序证明。

## 7. 对当前研究方向的实际含义

**支持的成果：**已在真实 API 路径上核验上下文依赖证明的生成→阻止错误复用→新证据→恢复旧证据；实际返回的公式在错 scope 的确造成可观测误报、漏报；Mac 与 Linux 大矩阵的分类和可复用证据一致。项目可以诚实地展示 context-aware proof maintenance 框架和经过独立检查的真实用例。

**尚未证明：**Egg 能提高 LLM 的生成准确性、降低修订次数或整体成本。只有一个 monitor、固定三个 guard、权威原式和所需字面量均直接给出，任务很容易；三组输出完全相同且都首轮合格，没有可区分的模型修订失败。没有跨设计泛化、独立复杂 temporal SVA、统计显著性或新 DUT 无界验证证据。更强的直接 SMT/普通事实基线结果仍然成立。本研究的应用与实验结果不能宣称为 E-Graph、proof reuse 或 LLM feedback 等通用技术的首创。

最值得下一阶段检验两个具体假设，而不是重复当前 4→5→4 简单 task：

1. **Dependency-driven re-certification / compressed proof feedback。** 优先使用此前 proof 的实际依赖而非全面 primitive-pair 枚举；在下一轮仅传递 guard、已核验的必要等价事实、proof ID、具体失效前提与反例，允许按需返回局部改写证据。离线检查精简证据可重放、安全且不漏报，再在固定共同候选/见证下比较 Raw、同信息普通诊断、Egg 简明证据的 token、修订成功率和覆盖质量。当前 token 和缺失依赖结果为该问题提供实测动机，但未声称已获得该优化。
2. **更有区分度的真实任务。** 如跨多个事务性质的规格/采样条件改变、同时保留不受影响的性质和验证责任，或受限 ghost 状态更新合成。事先冻结任务、独立参考、保留/改变的验证义务与观测，使用真实初稿，保留所有失败或成功，不人为重抽直到出现错误。比较强增量 SMT 和普通结构证据，除合格率外报告误报、漏报、非空洞性、实际功能覆盖以及人工可审计性。不要再次把已正确的单属性字面量替换作为模型收益的主实验。

## 8. 复现环境、脚本及证据

离线复核使用之前锁定的 Python 3.12.14、Z3/z3py 4.16.0 环境，以及原 Icarus 语料。不需要 API key 或再次调用模型，也不需要重新编译 Egg 来审计已保存的 native proofs。原 Mac 原生图的 binary hash 和 exact configuration 已在归档中保留。

| 新脚本 | 用途 |
|---|---|
| `scripts/audit_egg_regression_live.py` | 独立解决各方向、重新认证 common facts、核对 archived native proof 与 prefix store、逐字重建发送给模型的 prompt、重算预算及 usage |
| `scripts/check_egg_regression_live_physical.py` | 先审计真实回执，再去重真实合格公式并作 guard 交叉及全域 typed/physical 检查 |
| `tests/test_audit_egg_regression_live.py` | 真实及 fixture 审计、遗漏历史证据、过期证书复用、虚假 usage 的拒绝测试 |

从项目根目录运行：

```bash
AUDIT_TMP=$(mktemp -d)
tar -xzf results/milestone3/frame-txn-regression-live/transcript.tar.gz -C "$AUDIT_TMP"
python3 scripts/audit_egg_regression.py --run-dir "$AUDIT_TMP/main" --output "$AUDIT_TMP/main-rechecked.json"
python3 scripts/audit_egg_regression_live.py --run-dir "$AUDIT_TMP/live-20261125-173313" --output "$AUDIT_TMP/live-rechecked.json"
python3 scripts/audit_egg_regression_live.py --run-dir "$AUDIT_TMP/fixture" --output "$AUDIT_TMP/fixture-rechecked.json"
python3 scripts/check_egg_regression_live_physical.py --run-dir "$AUDIT_TMP/live-20261125-173313" --output "$AUDIT_TMP/live-physical-rechecked.json"
python3 -m unittest discover -s tests -p 'test_audit_egg_regression_live.py' -v
```

五项新增审计测试均通过；隔离 Linux 副本完整回归为 228 项 Python、7 项旧 indexed engine、19 项 Rust，共 **254 项通过，无跳过项**。原 Mac 离线证明依赖及物理报告重新计算后 JSON 与原归档、Linux 报告完全一致。已将原始线上记录、失败尝试、复现实验、独立审计、实际公式物理复核及来源哈希保存于 [frame-txn-regression-live](../results/milestone3/frame-txn-regression-live/)。本轮分析未发起新的 API 调用，未修改原始在线实验脚本或 RTL。
