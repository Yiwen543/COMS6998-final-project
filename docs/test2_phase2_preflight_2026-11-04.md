# test2 下一阶段：评分天花板与形式瓶颈预检

日期：2026-11-04，America/New_York。用户已选择继续固定刺激的断言/monitor 研究；本阶段没有改为 agent 判决或 R0/R1/R2 研究。新工作单独登记，旧 live freeze、Claude reference、候选和评分保持原样。

## 本次重新核对的旧证据

这是保存证据的核验，不是重新运行旧实验或旧测试套件。

- `test2/configs/live_freeze_v1.json` SHA256 `7f2be65ac1b8013d614c5391b49e6cde2b821dbaca6f3e8bae609e63ed67b912`，3486 项全部匹配，运行新预检后再次匹配。
- Claude reference SHA256 `53cff0d05aa9c48a71aec72cecfba265a13fe4baa2a4d9a72b3cef4d6b201337`；六个最终候选及评分副本、release 和 report/score 哈希绑定匹配。
- B′ tokens 为 120480/120153/119960；C′ 为 127676/128393/128046。总计 744708；C′ 平均多 6.5231438214%。六次均检出 6/6 种可观察故障，正确控制无报警和未知。
- 保存的 72 个形式结果仍为 12 PASS（全部为 active cover）、29 mutant 反例、31 TIMEOUT。24 个正确控制 bmc/prove 全部超时；反例涉及 M01/M02/M03/M04/M06 五类。没有完整正确控制证明。
- Icarus M02/final_boundary 未决以及 M05 两条未激活轨迹/观察仿真器保持原样。

原始入口：`test2/results/live-final-v1/scores.json`、`test2/results/live-report-v1/formal.csv`、`report.md`。本次重新计算及具体输入哈希见各 `phase2-preflight-v*/saved-evidence-audit.json`。

## 为什么出现评分天花板

直接观察：六个最终候选都有一份完整的 16×8-bit 预期队列，保存编译状态量为 135 或 143 bit；原上限为 8192 bit。各槽普遍围绕占用量、full、empty、队首数据、范围和复位。不同槽并不自动代表不同独立检错能力；同一完整队列模型能够涵盖多个故障类别。

六种固定单故障及当前有限正确控制均已被最终候选覆盖，因此最终 distinct-kill 指标没有继续上升空间。并非证明第一轮就达到 6/6：v1 只冻结并评分最终候选，不补造逐轮隐藏分数。

语义 CSV 还显示：五个等价源点在 basic 为零，但在开发 boundary 均已有命中。固定 DUT 覆盖不会因 monitor 改善而增加。C′ 提供的是实现表达式关系，完整规格队列模型可能无需这些关系；这是解释假设，未证明模型没有使用 E-graph，也未隔离额外上下文长度的影响。

扩大同一 FIFO 的随机轨迹未必解决天花板：若完整参考队列正确实现，更多同合同的可观察故障仍可能全部检出。下一任务应有独立于 C 结果的多周期判别维度及更广合法控制，不能在看到 B/C 后削预算或选故障制造差距。

## 形式瓶颈：旧日志与新校准分别记录

旧 harness 用一个向量断言检查全部六槽；请求深度 48、每任务 60 秒、smtbmc/z3。保存日志中的最大 assertion step *started* 多为 15，B′ rep1 为 6；这不是完成深度。反例较早出现不代表正确控制易于证明。

最小可执行任务是：固定选择按 arm/repetition 排序第一的已保存候选 B′ rep1，仅用公共正确 DUT，机械拆分六槽，保留参数、时钟、初始化和合法输入假设。每槽 BMC 48 步/10 秒，候选求解器预算总计 60 秒；另有两项各 5 秒的工具控制。它是基础设施校准，不是新模型重复、正式新任务或旧超时补分。

各版本在运行前分别登记，所有失败保留：

| 预检版本 | 变更/结果 | 候选槽是否运行 |
|---|---|---|
| v1 | 工具控制也检查 48 步；恒真在 5 秒内 TIMEOUT，恒假 FAIL；停止 | 否 |
| v2 | 工具控制改为 2 步；尚未跨过首个有效断言，恒真/恒假均 bounded PASS；门失败，停止 | 否 |
| v3 | 工具控制覆盖 steps 0–2，得到预期 PASS/FAIL；六槽沿用分层 prep，全部 TIMEOUT | 是，六槽 |
| v4 | 在相同候选预算下增加 `prep -flatten`；首个工具任务完成后，JNY 遥测读取器格式错误，producer 退出 | 否 |
| v5 | 修复并测试遥测读取器，形式配置与 v4 相同；工具控制预期 PASS/FAIL；三个槽有限 PASS、三个 TIMEOUT | 是，六槽 |

v4 的异常见 `test2/results/phase2-preflight-v4/producer-failure.json`；其单项求解器记录保留，但精确 Python 墙钟缺失，不能当作零成本。每次 producer 的实际源码均保存在对应 `producer.py` 并与 `run.json` 的 SHA256 绑定。

v3 的 slot0 生成模型保留两份 `$mem_v2`，共 256 bit；分槽本身并未移除模块中无关的数据存储。v5 flatten 后：

| B′ rep1 槽 | 该候选的槽说明（不是独立真值） | BMC 48/10s | 模型 memory bits |
|---|---|---|---:|
| P0 | 预期占用量 | PASS | 0 |
| P1 | full 与预期占用量一致 | TIMEOUT | 0 |
| P2 | empty 与预期占用量一致 | TIMEOUT | 0 |
| P3 | 队首数据顺序 | TIMEOUT | 256 |
| P4 | fill 范围 | PASS | 0 |
| P5 | 复位状态 | PASS | 0 |

v5 8 项任务实测合计 38.683 秒，含工具控制及启动开销；它不是求解器上限的替代计量。详细时间见 `test2/results/phase2-preflight-v5/formal-calibration.json`。

可支持的结论：消除无关状态让部分局部性质完成了有限检查；仅拆分还不够，且消除 memory 也未解决 full/empty。因此不能把所有超时单因归于 RAM，也没有解决整组 soundness。后续需要性质级归纳/状态关系或更小受检任务的独立可行性验证。所有新 PASS 都是有限 BMC；没有新 prove、cover、DUT 仿真或模型调用。新校准不改变旧 31 个 TIMEOUT。

## 下一项最小任务及新研究登记

建议下一项是**一个多周期协议控制器的单任务离线资格包**：先固定请求/响应、背压下保持、取消/复位跨事务的明确合同；只处理一个可复现配置。选择依据是规格明确、语义关系与 monitor 义务相关、分解形式检查可承受，不根据新 B/C 结果筛选。具体 DUT 尚未选择，不能宣布新任务已经合格。

`test2/configs/registration_v2_draft.json` 已把共同预算、角色、指标、固定输入、隐藏评分、每轮快照和准入门写为机器可读草案。`live_allowed=false`，source/spec/interface/formal schedule 尚未绑定，所有 live gate 均为 false。它不是可执行 live freeze。

最小资格包的验收内容：

1. 固定 DUT/规格/公共观察接口及可支持的双态/复位边界；保留所有不支持项。
2. 证明至少一个非平凡 E-graph 关系的完整类型、guard 与独立源点映射，并说明其与待检查行为的关系。test2 不要求沿用旧刺激任务的 ordinary-unhit/B-before-C gate，也不将组合等价当作时序正确性。
3. 冻结相同的开发观察；规划新隐藏最终故障及轨迹、合法正确控制和独立 observability。旧 final 仅供校准，不冒称新的盲测。
4. 为局部控制和数据义务分开制定形式日程，按每候选总预算控制；保留超时，不对某个 arm 追加资源。先验证该日程有区分力，再冻结正式任务。
5. Claude 独立参考作者与新会话审阅；GPT monitor 是被评估对象。候选提示词用 allowlist，排除 reference、故障、最终轨迹、求解器见证、维护技能与评估结果。
6. 所有轮次的候选源码/元数据先快照冻结，全部生成结束后才做隐藏评估。第一轮达标、cost-to-quality 等端点如需使用，必须在调用前定义，不能事后挑最好轮次。

草案匹配原有模型/轮次/token 请求上限，并给每候选 720 秒总形式求解器上限；具体性质/案例日程待任务绑定。相同 cap 不代表实际 prompt token 相同。未另行登记 token 匹配 placebo 前，只评价整个 C 反馈包，不声称隔离了纯语义因果效应。固定覆盖率仍是输入证据，主指标是正确控制有效性、独立可观察故障检出、未决率及实际成本。

本次没有创建新的独立 reference 或隐藏最终数据，也没有可启动的 live 阶段。后续需要 API 时，继续使用既有终端隐藏暂存流程；不从聊天读取或复用密钥。

## 命令与验证范围

本次新测试（7 项，不是旧 25 项测试重跑）：

```sh
.venv/bin/python -B -m unittest discover -s test2/tests -p test_phase2_preflight.py -v
```

以下是已执行的最新**新校准**命令；复现需全新 `phase2-*` 目录，不能覆盖已有结果。它会启动 8 个新 SBY 任务，不能为恢复上下文自动重跑：

```sh
.venv/bin/python -B test2/scripts/phase2_preflight.py --registration test2/configs/phase2_preflight_v5.json --output test2/results/phase2-preflight-v5 --run-slot-calibration
```

省略 `--run-slot-calibration` 只核验保存文件和哈希，不调用模型、编译器、仿真器或形式工具。新脚本拒绝覆盖已有输出，且仅允许直接写入 `test2/results/phase2-*`。未安装工具、提交、推送或 fetch。
