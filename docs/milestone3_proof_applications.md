# Milestone 3 · 用 egg 审阅和维护验证证据

**最直接的用途是回答“这个零命中分支凭什么可以豁免，今天改过的 RTL 还能用昨天的证明吗？”** egg 能导出一条逐步可查的等价推导，说明如何把完整的源 guard 改写成便于判定的表达式。Z3 负责检查推导所依赖的设计等式、判定可达性；仿真器负责核实可达输入是否真的命中对应的 DUT 计数器。项目已有的端到端对照仍然成立，同一 Controller 求解任务中普通结构改写更快。这里衡量的是证明能否检查、定位、保留和修复。[原性能对照](milestone3_followup.md) · [实验范围与对照设计](m3_proof_use_protocol.md)

## 一条可以交给验证工程师的覆盖豁免

八路 arbiter 第 30 行有一个零命中分支。进入它需要外层判断 override 非零，同时在内层逐位检查中发现八位全为零。egg 的证明指出在完整激活条件的哪个子项应用了具名规则 `override-nonzero`。独立程序逐步重放这次替换，Z3 对替代式的可达性查询返回 UNSAT，对未经改写的完整条件直接查询也返回 UNSAT。证书绑定 DUT 哈希、事件、位宽、模型假设及具体 Verilator 计数器。归档定向覆盖维持 **17/18**，同时给最后一个分支附上了可复核的解释。[豁免证书](../results/milestone3/coverage-waiver/waiver.json) · [实际步骤与模型](m3_coverage_waiver.md)

在 RTL 临时副本中给外层判断加入 `|| req[7]`，旧证书因源文件和分支条件改变而失效。重新求解给出 `reset=0, req=0x80, priority_override=0x00`。同一组四个种子加这个输入，在原版上目标计数为 0，在修改版上为 1，修改版的功能 checker 也报告一次错误。在这个设计上，普通 Z3 同样能得到结论；egg 额外提供了从 RTL 条件到替代式的具名改写记录。[原始覆盖数据、两个模型和回放日志](../results/milestone3/coverage-waiver/)

## 旧证明依赖哪些规则，规则撤回后怎么办

AXIS Controller 有 148 个 guard 目标和 281 条已通过 QF_BV 检查的设计规则。同事可以用一个规则名查出哪些旧证明需要审核。下例返回 7 条原证明及其源位置和改写步骤。单独撤回该规则并重建时，这 7 对均取得了替代证明。另一个容易手查的例子是撤回连接 `g18` 和 `g23` 的直接规则后，依次正向使用 `g18 = g37` 和反向使用 `g23 = g37`，恢复原结论。[完整修复例](../results/milestone3/proof-withdrawal/repair-example.json)

```bash
python3 scripts/m3_proof_dependencies.py \
  --input "$FIXTURE/qualification/typed-v5/screen/egg-input.json" \
  --graph results/milestone3/engine/profile-2/reference.json --using-rule qfbv-g59-g83
```

| Controller 的审阅问题 | 实测结果 |
| --- | --- |
| 每次撤回一条规则，依次测完 281 条，原有的 70 条证明有多少还能读通？ | 19,670 个“原证明 × 撤回规则”组合中，19,599 个仍可按原文检查，71 个引用了已撤回规则。 |
| 能否修复这 71 个组合？ | egg 和普通等式图均修复 57 个。另 14 个缺少剩余规则支持；对原目标重新做独立 XOR 查询，14 个均为 UNSAT。 |
| 在相同输入上，下一轮只复核哪几条证书，就能保留原文？ | 70 条旧证明共引用 50 个不同的设计规则名。仅复核这 50 条、重新运行 egg，70/70 条具名证明逐字相同。 |
| 如果只要求验证结果一致，需要多少规则？ | 普通结构算法找到 44 条，保留全部 148 个代表表达式及 87 个同作用域分组；有 9 条证明换了推导。44 是已验证的上界。 |

两种缩减在全部 148 个“原 guard XOR 新代表式”查询中均获 UNSAT。原 RTL 的三条开发轨迹给出每组 25,604 个逐目标布尔观测，全部一致。跨实例的 guard 即使有代数等价证明，也不能凭此分享覆盖计数或跨时钟结论；物理复用要额外匹配实例和原始采样事件。[撤回实验与全部记录](m3_proof_withdrawal.md) · [子集选择、对照、原 RTL 核验](../results/milestone3/proof-basis/README.md)

## 对真实 RTL 编辑定位哪些等价结论要重验

固定 arbiter 的 16 对源 guard 与替代表达式，各自在原始 RTL 上成立。在 10 个隔离编辑中，8 个分别从 override 非零检测器漏掉一位，另外两个分别改用等价语法和故意改错 grant 输出。Yosys 从实际编辑过的 DUT 读取检测器，逐一求值全部 256 个 override 输入，再对发生变化的检测器用 Z3 复核规则。每个漏位编辑都使 2 条前提和 9 对 guard 失效。跨 10 个编辑合计 160 项结论，88 项由仍有效的旧证明支撑，72 项重验发现反例。改错 grant 数据的版本仍保留 16 个 guard 等价结论，但 Icarus 读到错误的 grant 值，说明这批性质能覆盖到哪一层。[逐编辑判定](../results/milestone3/eco-impact/cases.json) · [真实输出与路径采样](../results/milestone3/eco-replay/)

对照使用同一检测器和语义变化判定。普通语法树改写也记录所用规则名，标出了完全相同的待复核目标。计入前提重验后，egg 和普通方法各需 144 次 Z3 查询；同样跳过语义未变检测器、直接检查全部目标需要 128 次。若每个编辑无条件重查全部目标则需 160 次。计数排除首次认证、检测器真值表生成及实验审计。每例的独立真值表覆盖全部 131,072 个二态端口组合，发现的不等价性各取一个见证，再用 Icarus 在 11 版 RTL 中各回放 75 个输入。此处没有测量耗时或人工审查成本。[查询计数](../results/milestone3/eco-impact/summary.json) · [独立枚举及回放记录](../results/milestone3/eco-replay/summary.json)

## 环境、运行与脚本

使用 Debian 13、Python 3.12、Rust/Cargo 1.90、egg 0.11、Yosys 0.52、Icarus 12、Verilator 5.050、Z3 4.16（CLI 和 Python 包）、C++ 编译器和 GNU make。按主指南中的 Debian 命令安装环境。在包含基线提交 `71e99c4` 的 Git 工作区运行下面的命令，每个输出位置取新目录。如果已跑过 Milestone 3 或下载过固定的 Controller fixture，可直接使用相应目录。完整实验不调用模型 API。[环境安装命令](milestone3.md#环境与一键复现)

```bash
BASE_RUN=/tmp/coms6998-m3-base
FIXTURE=/tmp/coms6998-controller
OUT=/tmp/coms6998-proof-applications
bash scripts/run_milestone3.sh "$BASE_RUN"
python3 scripts/m3_controller_replay.py --fetch "$FIXTURE"
bash scripts/run_m3_proof_applications.sh "$BASE_RUN" "$FIXTURE" "$OUT"
```

| 脚本 | 可重现的工作 |
| --- | --- |
| `run_m3_proof_applications.sh` | 运行 Controller 撤回、四组缩减、两种已发布子集的独立复核、按名查询、10 项 RTL 编辑及覆盖豁免签发与复核。 |
| `m3_proof_dependencies.py` | 解析 egg 的具名证明，逐步检查改写位置、方向、变量绑定和端点。可用 `--using-rule NAME` 查依赖，或用 `--edge TARGET_A TARGET_B` 查看已存证据。 |
| `m3_controller_withdrawal.py` | 独立撤回每条规则并重新饱和，对比两版 egg、普通等式图和结构归一化，保留逐边证据及缺证目标的独立形式查询。 |
| `m3_controller_basis.py`、`m3_controller_certificates.py` | 选择复核子集，重跑所选位向量义务，核对代表式、具名证明和 RTL 回放。带 `--qualify` 的入口输出可重新使用的 egg 输入。 |
| `m3_eco_formal.py` | 从审阅过的 arbiter 源码结构提取实际选择条件，调用 Yosys 穷举选择器，按名称提交 Z3 规则或等价性查询。 |
| `m3_eco_replay.py` | 生成受控编辑，独立枚举二态输入，编译未插桩 DUT 与记录路径的副本，回放具体输入并核对输出和路径。 |
| `m3_eco_impact.py` | 在 10 个编辑上用 egg 证明或普通规则记录选择复核范围，与直接判定、独立枚举及 RTL 回放结果核对。 |
| `m3_coverage_waiver.py` | 签发绑定具体 RTL 和计数器的覆盖豁免，导出两版的 SMT 查询和原始计数，可单独用 `--check-waiver` 复核。 |

完整流程已在两个新目录重跑。两次得到相同的逐项撤回结果、子集复核结果、RTL 编辑判定及覆盖豁免。另在隔离副本执行 `make test` 的 35 项测试和 `python3 scripts/test_guard_proofs_fast.py -v` 的 7 项引擎测试，均通过。其中负例覆盖重算哈希后仍然错误的 SMT 查询、篡改证明、负命中数以及与独立枚举相矛盾的编辑判定。Verilator 原生 `.dat` 不附 RTL 摘要，单独消费证书时需要能追溯到同次编译的 RTL 和计数文件；完整实验在同一驱动内完成编译与采集。

这里的证明限于列明的二态组合条件和采样事件。跨周期复位性质另有直接在 DUT 上运行的有界模型检查、归纳和反例回放。两类证据分别回答“这个 guard 能否在该输入下激活”和“这个状态随时钟变化时是否满足性质”。[跨周期性质与实测反例](m3_formal.md)
