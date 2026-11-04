# SPI 多步事件、角色分离 checker 与下一候选 IP：2026-11-04

本次完成了一个**限定范围的离线验证检查点**：Claude 独立编写的 checker 经修正、独立控制和新会话复核后冻结；原始 SPI RTL 与 SV driver 保持不变。背压恢复、复位重启、保持配置不变的 CSID 切换都有校准证据。另发现同 CSID 的配置切换存在可信的规格/实现不一致证据。

**尚未启动新的 B 或 A/B/C/placebo。** 新事件与原始源码目标之间的关联证明仍缺失；旧的两个非平凡组合等价组仍是上一轮 B 首轮就能命中的目标。本次不是 C 优于 B 的新证据，也没有事后缩短 6×64 周期预算。

## 实际角色分工

| 角色 | 输入与职责 | 禁止的操作 |
|---|---|---|
| Codex/GPT 工程与刺激角色 | 编排工具、复用固定 SV driver、生成私有 JSON 校准序列和外部故障控制、读取真实计数 | 不编写或手改新 checker 的判分源码；不替 Claude 作出规格判决 |
| Claude checker 作者 | 固定版本的公开规格摘录、接口位宽与采样说明；修正时接收独立控制及审阅发现 | 不读 DUT 实现、旧 checker、B/C 结果；不生成实验刺激；不修改 driver、预算或计数器 |
| 新会话中的 Claude 审阅者 | 规格、候选 checker、控制结果；最终复核额外读取完整公开轨迹、固定 driver 与相关 RTL 摘录 | 不修改源码、计数或实验结果；其意见不能替代仿真与证明 |
| 后续实验刺激模型 | 计划仍为 `gpt-6.1-sol`，只提交固定 schema 的 JSON actions | 不能修改 checker、DUT、SV driver 或测量脚本 |

本次没有调用 OpenAI API 生成实验刺激。校准由本聊天的工程角色构造，不算 live B 开发结果。SV testbench 继续使用此前的 `tb_spi_host_fixed.sv`，只负责驱动、采样与完整批次执行；新的规格判定是 Claude 编写的 Python 公共引脚 scoreboard。这样可以分开刺激与判分作者，同时保留经过验证的时钟/复位驱动。

Claude 使用指定的 `claude-opus-5-5`，经 Claude Code CLI 调用，未替换模型。作者与审阅调用都是无会话继承、无工具的独立进程；`--bare` 禁止自动读取项目记忆，空工作目录与禁用工具限制其可见信息。保存了每次提示词、原始响应、源码补丁、模型标识、usage、延迟和失败记录。

冻结文件见 [`examples/heldout_spi_host_events`](../examples/heldout_spi_host_events/)。
checker SHA-256 为
`fa4d2c251fc6ef12f2da5e051206b5bc5151d6446b2450d9676934a973d63ebe`。
所有新 checker 源码均来自 Claude 的完整响应或精确文本补丁；工程角色只校验并应用补丁，没有补写判分逻辑。

## 为什么角色分开后仍要验证 checker

第一次作者调用超时，未取得可用产物；usage 和费用未知，不能计为零。第二次返回 v2：其自身 18 个控制全部通过，但独立合法参考轨迹被误报。

发现的两个关键错误是：先检查字节、后登记同周期接受的命令，导致合法的首字节被当作残留数据；以及只在新命令接受时建立切换监视器，漏掉此前已经发生的旧 CS 释放。这些是 **checker 错误，不是 DUT 缺陷**。原始版本和失败结果都保留。

Claude 的 v3 修正后，独立合法参考通过，25 个作者控制通过。但是新会话审阅发现：某些事件入口的错误发生在失败计数快照之前，导致负例虽然报错，仍被记为成功事件。v4 再由 Claude 修正，要求完整事件窗口内无错误，并同步属性表与源码。

最终验证结果：

| 检查 | 结果 |
|---|---:|
| v4 作者的正/负控制 | 38 个通过 |
| 独立合法单字节参考 | 通过，包括同周期接受命令和传输首字节 |
| 外部单故障控制 | 12 个保留，10 个在干净基线下被检测 |
| 保留但未检测的控制 | 2 个：`active` 复位值、无传输时的 `last_read` |
| 截断前缀 | 7 个均不误报已完成事件，也不因未完成而报 liveness 错误 |
| 仓库回归 | 97 项通过 |
| 最后的角色/复核包专项测试 | 5 项通过，包括新增的字段引用错误回归 |

两个未检测控制属于当前 checker 明确不检查的输出范围，**仍保留在 10/12 的分母中**。不能将它们改名后当作成功检错，也不能据此宣称完整 checker 正确性。每个负例只有在未注入故障的相同基线通过时，才获得检错信用；v2 的 7 个负例全部被基线错误混淆，因此当时有效检错信用为零。

事件窗口通过与整个轨迹通过仍是两件事。例如一个恢复事件在周期 91 完成，周期 101 才注入另一个错误，前面的局部事件可以保留，但该轨迹总体仍是 `dut_violation`，不能称作干净轨迹的资格证据。固定 runner 同时保存两者。

v4 的复核包生成曾发生一次工程脚本 `KeyError`，发生在第二次 API 调用之前；checker 及其测试结果未损坏。该错误、修复与专项测试均保存，最后只补跑了缺失的独立审阅，没有重做 checker 生成。

## 多步事件校准

七组候选都使用公共接口；命令保持到 `ready` 接受。用于寻找接受时刻的私有 probe 及所有重放均计入开销，绝不进入实验提示词。最长完整候选 202 周期，小于原定总预算。Verilator 与 Icarus 的完整公开轨迹逐周期一致。

| 校准情形 | 周期 | v4 判定 | 完整事件结束周期，零起始 |
|---|---:|---|---:|
| TX 背压后恢复 | 152 | scoped_pass | 91 |
| RX 背压后恢复 | 152 | scoped_pass | 91 |
| TX/RX 背压序列 | 190 | scoped_pass；报告该段首次跟踪的 TX 恢复 | 113 |
| 软件复位中止后重启 | 125 | scoped_pass | 57 |
| 异步复位中止后重启 | 125 | scoped_pass | 57 |
| CSAAT 后改变 CSID，配置不变 | 202 | scoped_pass | 84 |
| CSAAT 后同 CSID 改变配置 | 200 | dut_violation；不计为合格切换 | 无 |

这证明了这些具体序列的离线可执行性与限定属性结果，不证明任意合法序列、完整 SPI payload、任意时序组合或完整外设正确性。`sw_reset` 与 stall 同时发生、dummy 段切换、enable 语义等仍未解决；每字节 `16/lanes` 个 SCK 边沿是明确记录的建模假设。配置变化时的加和 idle 时序，若观察不足，不能算合格事件。

## 配置切换的候选缺陷

在同一固定 RTL 上，先完成一个 `CSAAT=1`、CSID=0 的段，再提交同 CSID、改变 CPOL/CLKDIV/时序参数的命令。周期 49 的公开记录为：

| 信号 | 边沿前 | 边沿后 |
|---|---:|---:|
| command valid / ready | 1 / 1 | — |
| CSB | 2，即 CS0 有效 | 2，仍有效 |
| SCK | 0 | 1 |

公开规格要求配置在所有 CS 无效时应用，并对 CSAAT 后的配置变化规定结束旧事务。源码中，保持 CS 有效时的路径检查 CSID 变化，却没有像空闲路径那样处理 `config_changed`。固定 driver 按名字连接结构体字段，输入回显一致；两种仿真器在 50 周期触发复现及完整 200 周期复现中均一致。

最终独立审阅认可这是 **`spi_host_fsm` 边界的一类可信规格/实现不一致证据**。CS 与时钟的相关症状不算两种独立缺陷。还需要核查完整外设的命令队列/上层约束，或执行相应形式属性，才能称为上游确认的完整 IP 缺陷。没有修改原始 DUT，也没有提交外部 issue。

完整复现哈希和源码/规格依据见
[`config-switch-full-reproducer/evidence.json`](../results/spi_host_event_checker_20261104/config-switch-full-reproducer/evidence.json)。
这也补齐了最终审阅要求的周期 50–199 双仿真证据。

## 为什么仍不能运行新的 B/C

原始分母保持 **57 line、160 branch、246 expr、836 toggle**，共 1,299 个 DUT 计数点。事件记录是补充指标，没有混入这些计数，也没有把等价源码位置合并计数。

已有证明只支持组合条件相等。例如 `new_command` 与完整使能 guard 的等价，不代表“中止后成功重启”的历史序列等价。现有两个非平凡源码组在旧 B 试跑中已首轮命中；不能给它们改一个更复杂的事件名字，就声称获得了更难的原始覆盖目标。

因此 [`event-screen/screen.json`](../results/spi_host_event_checker_20261104/event-screen/screen.json)
明确记录 temporal-to-source bindings 为空，live B 和正式 A/B/C 均未就绪。v4 冻结的是离线 checker 及其适用边界，**不是新的正式实验目标**。本次没有使用 C 结果选题，也没有产生新的 C 收益估计。

## 第二个自然 IP 的具体进展

从已固定的同一 OpenTitan 仓库中，预检了功能独立于 SPI_HOST 的 **I2C controller FSM**，保持默认 `FifoDepth=64`。选取原因是其公开规格自然包含多步事件，而非源码更长：

- clock stretch 解除后恢复；
- unexpected NACK 后软件处理，再 repeated START；
- NACK-handler timeout 后自动 STOP，清除事件后继续。

Slang、Yosys、Verilator lint 和 Icarus 编译检查均通过，提取到 268 个词法 guard。初步 AST/QF_BV 检查有 23,324 个 SAT、166 个 UNSAT、零 unknown，其中 9 个不同表达式对是后续假设。**这些还不是合格等价组**：尚缺独立网表交叉证明、原始计数映射、checker/driver 和可达性证据，也没有经过 egg 的正式候选认证与 B 开发试跑。

证据见 [`results/i2c_event_candidate_20261104`](../results/i2c_event_candidate_20261104/)。
I2C 后续需要真实的开漏 wired-AND 总线模型、合法时序参数、稳定的 FMT 队列入口与受控 ACK/NACK/拉伸响应，不能简单任意驱动 SCL/SDA 后宣称覆盖有效。

## 成本与复现

本次是 checker 开发开销，不与旧的刺激模型成本曲线合并。6 次 Claude CLI 调用中，5 次得到完整 usage，1 次超时 usage 未知。已返回调用的 CLI 报告成本合计 **$2.928525**，不是含未知超时调用的完整费用。

| 已知 API usage 字段 | 总计 |
|---|---:|
| input_tokens | 20 |
| cache_creation_input_tokens | 251,881 |
| cache_read_input_tokens | 0 |
| output_tokens | 83,452 |
| 其中 thinking tokens，已包含在 output 中 | 51,370 |

三个编译、30 次仿真、4,252 个实际执行周期包括：校准 probe、双仿真校准、两种长度的异常复现，以及冻结 runner 的一次 smoke replay。仓库测试中的仿真属于另列的验证开销，不混入上述账目。OpenAI 调用为零。暂存 Anthropic key 已删除。

可直接重放冻结 checker，不需要 API key：

```sh
.venv/bin/python scripts/run_spi_event_fixed.py --actions results/spi_host_event_checker_20261104/calibration/csid_switch/actions.json --output build/spi-event-replay-new
.venv/bin/python scripts/evaluate_spi_checker_candidate.py --candidate results/spi_host_event_checker_20261104/revision-v4/candidate --calibration results/spi_host_event_checker_20261104/calibration --output build/spi-event-controls-new
.venv/bin/python scripts/summarize_spi_checker_controls.py --evaluation build/spi-event-controls-new
.venv/bin/python scripts/summarize_spi_event_milestone.py --base results/spi_host_event_checker_20261104
.venv/bin/python -m unittest discover -s tests -p test_spi_role_separation.py -v
```

重新生成校准与前端证据，使用新目录：

```sh
.venv/bin/python scripts/calibrate_spi_events.py --output build/spi-events-cal-new
.venv/bin/python scripts/probe_i2c_event_candidate.py --output build/i2c-event-probe-new
```

公开源 revision 仍为 `0ea5236fe749e70ba18f56ba19c4be982ef46da7`；SPI DUT SHA
仍为 `5324b93183a0475c5e955b76a7b1e9c1c9739e810a70d213491c5657837ee47c`。
工具沿用 Verilator 5.050、Icarus 12.0、Slang 12.1.0+42710c788、Yosys 0.70+309、Z3 5.1.0；没有为本次安装或替换工具。
仓库基准 commit 仍为 `c71a3e580646d08fb6496c742b7b42b711179b36`；本次未 commit/push。

下一步应优先完成 I2C 的独立规格 checker 与固定总线 driver，再验证其候选等价组及预算内可达性；SPI 配置切换问题则进入单独的 reliability/formal 线。只有目标关联与独立 B 门槛都通过，才冻结 A/B/C/placebo。复杂事件、较大模块和更换判分模型，都不能单独作为 E-graph 有效性的证据。
