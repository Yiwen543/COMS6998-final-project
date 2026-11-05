# SPI core 独立 checker 生成与复核 — 2026-11-04

**本轮实际完成一次 Claude 作者调用、一次独立 Claude 复核、独立控制检查和补充双仿真器实验。checker 尚不能冻结，B 保持关闭。** 暂存 Anthropic 密钥已删除，没有调用 OpenAI，也没有修改原版 DUT 或 Claude 的 checker 源码。

机器可读决定：[checker-audit-decision.json](../results/real_parent_screen_20261104/checker-audit-decision.json)。本轮接续[真实父模块预检](real_parent_screen_2026-11-04.md)，预算、原始覆盖分母和此前的负面筛选结果均未改变。

## 角色和实际执行

- Claude `claude-opus-5-5` 作者只收到冻结的公开规格节选、真实 core 接口及采样合同。它没有看到 DUT 实现、旧 checker、私有校准、guard、覆盖或 B/C 输出。
- GPT/Codex 负责固定 JSON/SV driver、独立手工正常轨迹、单故障控制和评估脚本，不改写 Claude 的 expected-output 逻辑。
- 第二个全新、无工具、无会话持久化的 Claude 会话只读审阅规格、checker、driver 和控制证据。所有 28 个输入轨迹以无损压缩格式提供；每类重复诊断只提供前 4 条并标明完整数量。
- 集成者最后对照完整日志核验 reviewer 的判断。**Claude reviewer 也可能误读，不能把它作为最终真值。**

作者产物包括 [checker.py](../results/real_parent_screen_20261104/claude-checker-v1/candidate/checker.py)、属性表、合同、自测和 SHA-256 署名清单。生成和复核均使用 Claude Code 2.1.310，requested/returned model 均为 `claude-opus-5-5`，low effort、600 秒超时、每次 CLI `$4` 预算参数，工具列表为空。

作者未被要求固定 verdict 的字符串枚举，因此评估器按其公开合同把 `pass/fail/blocked/inconclusive` 保留并解释；只有没有 failures、assumption violations 和 unresolved 的 `pass` 才能作为 scoped pass。没有为了得分修改 checker。

## 检查结果

初始评估共 28 个 case：4 个独立手工正常轨迹、8 个原有 DUT 校准轨迹、11 个单故障控制、4 个截断控制和 1 个输入协议控制。详细结果见 [summary.json](../results/real_parent_screen_20261104/spi-checker-evaluation-v1/summary.json)。

| 项目 | 结果 | 含义 |
|---|---|---|
| 作者自测 | 11/11 通过 | 不是独立有效性证明 |
| 独立手工正常控制 | 4/4 无误报且 pass | 仅覆盖 Standard、mode 0、单 segment、CLKDIV=0 的有限范围 |
| 原定 11 个单故障控制 | 8 个获得有效检出信用 | 9 个基线干净；其中 1 个 missing RX word 正确保持 inconclusive，另外 2 个故障的基线本来就失败，不给信用 |
| 截断轨迹 | 无成功恢复误计 | pending/inconclusive/fail 均保留，不改成 pass |
| 初始实际 DUT 多步事件 | 只有 RX backpressure 事件 pass | 全部 RX byte 为 FF，不能检验字节顺序和某些重排/复制问题 |
| 独立 reviewer | `ready_for_offline_gate=false` | 不能冻结 checker，更不能据此运行 B |

这里的 8 个检出不是 DUT defect 数量，也不是覆盖率。重复 payload 失败不能算成多个独立缺陷。未检出、不能判定和基线不合格都留在明细中；没有只报告成功用例。

## 阻塞一：公开规格与原版 core 字节顺序冲突

固定 revision 的 `theory_of_operation.md:699–702` 写明从 `word_i[31:24]` 开始发送；`:735–738` 写明第一个 RX byte 进入 `word_o[31:24]`，低位补零。Claude 依据这些文字建立了 MSB-first checker，独立手工控制也遵守同一公开合同。

原版 SV 的两个仿真器却一致观察到：

- TX 接受 `0xA1B2C3D4`、byte-enable=15 后，单字节写在线上发出 **D4**，公开合同要求 A1。8-byte TX 校准的前四个 byte 为 D4/C3/B2/A1。
- 三个 FF byte 的 RX partial word 是 **0x00FFFFFF**，公开合同要求 `0xFFFFFF00`。

随后只读检查原版 RTL 确认：byte-select 把低 byte 放在 packer 的低位，unpacker 从 ptr=0 开始；byte-merge 从 depth=0 开始向低位插入。driver 直接连接真实 word 端口，没有隐藏 byteswap。[诊断证据](../results/real_parent_screen_20261104/spi-byte-order-diagnosis.json)保留源码、文档、driver 和 trace 的哈希。

因此可以确认**提供给实验的固定 core 文档与固定 core 行为不一致**。这不足以断言整个 OpenTitan 顶层有生产缺陷，也不能判定一定是 RTL 错而不是文档过时或边界解释错误。不得把 checker 默默改成跟随 RTL，再宣称“规格验证通过”。本轮保留原始矛盾，等待明确的上游规范依据或单独登记的合同修订。

## 阻塞二：checker 本身和事件记录的问题

1. **CSAAT/CSID 判据过强。** 实际切换在 cycle 89 看到 valid 的新 CSID 后释放旧 CS；新命令 cycle 90 才 ready&valid。checker 只看已经接受的队列，在 cycle 89 报错。公开规格的“检测到 CSID 改变”没有要求先完成 acceptance；应由原 Claude 作者修正 pending-offer 追踪或明确标为 unresolved。
2. **漏记 TX starvation 事件。** 原轨迹确实有 55 个 pre-stall 周期，但 checker 没有输出成功、失败或 pending 的该类事件。它在恢复后的采样边沿才判断等待时长，漏掉了之前的停顿。这会把失败/未识别事件从统计中隐去，不能接受。
3. **软件复位和更广模式尚未充分验证。** 软件 reset 的未解决义务、CS 行为检查范围、CPHA/CPOL/FULLCYC、非零 timing 参数及非均匀 RX payload 都需要继续补控制。不能因为几个手工 case 通过就宣称完整 core checker 正确。

上述问题需要 Claude 原作者修正；GPT 没有对其源码打补丁。

## reviewer 的错误也单独核对

[原始复核意见](../results/real_parent_screen_20261104/claude-checker-v1/review.json)的 F3 提到可能存在 TX underflow 和 stall 中 SCK tick。完整日志不支持这两点：

- 8 条 TX 失败全部是 byte-order payload mismatch，**没有 `tx_underflow`**。
- cycle 73 是第 4 个 byte 的最后采样；pre-stall 从 74 到 128，共 55 个周期，SCK 始终保持高。
- 新 word 在 128 接受，129 是恢复后的 trailing edge，130 才是下一次 leading sample。

因此保留 F3 的“事件漏记”发现，撤回其潜在 DUT clock-under-stall 判断。完整行证据和 checker 条件分析记在 [review_corrections_and_followups](../results/real_parent_screen_20261104/checker-audit-decision.json)。原始 reviewer 输出不修改。这个例子说明交叉模型审阅能提供线索，但仍必须对原始测量负责。

## 复核后补齐的两个控制缺口

这部分是**复核后新增的离线证据**，没有追加 API 调用，也没有声称被第一轮 reviewer 看过。继续使用原版 DUT、固定 driver 和未修改的 Claude checker，三条实际序列均在 Verilator/Icarus 中一致，详见 [补充评估](../results/real_parent_screen_20261104/spi-checker-postreview-v1/evaluation/summary.json)。

| 补充 case | 实际结果 |
|---|---|
| 干净的重复-byte write 基线 | pass；仅用来避免 byte-order 矛盾干扰输入协议控制，不作为新的字节顺序证据 |
| ready=0 时 offer 命令，随后撤回；重新仿真实际输出 | cycle 29 只有 `cmd_transport` 假设违规，verdict=blocked；不计 DUT 缺陷 |
| 运行中硬复位，释放后新 TX 完成 | reset/restart 事件 48..125 pass |
| 在同一干净 reset 基线注入错误 CS | cycle 48 被检出，事件变为 fail |
| reset 中截断，尚未发起新命令 | inconclusive，事件 pending，没有恢复成功计数 |

这修复了原输入控制“只改输入却沿用旧输出”的因果问题，并补上 hardware-reset 的有限正反控制。原来的无效控制仍留档且不计信用。它们没有解决字节顺序、软件复位或 TX 事件统计阻塞，不能据此推翻 `B_allowed=false`。

## 成本、失败记录和复现

| 调用 | 普通输入 | 缓存新建输入 | 输出（含 thinking） | 报告费用 | 调用耗时 |
|---|---:|---:|---:|---:|---:|
| Claude 作者 | 4 | 14,869 | 52,062 | $1.115601 | 478.41 s |
| Claude 独立 reviewer | 4 | 69,377 | 5,887 | $0.464641 | 72.81 s |
| 合计 | 8 | 84,246 | 57,949 | **$1.580242** | 551.22 s |

总输入为 84,254，总输入加输出为 **142,203 token**。41,201 thinking token 已包含在输出中，没有再次相加；缓存子项、iterations 和 modelUsage 的重复汇总也不再累加。这些是基础设施作者/审阅成本，不是 B/C 刺激 Token ROI。

首版复核包为 173,367 bytes，被本地 150,000-byte 门槛拦下，没有发 API。改为可逆的列索引/RLE 后为 142,986 bytes，全部 28 条轨迹逐行还原验证通过，第二次模型调用才开始。作者和 reviewer 调用均成功，没有超时或额外重试。

初始 28 个 case 重放已有 trace，不新增仿真。复核后补测新增 2 次编译、6 次仿真，两种仿真器合计 **912 周期**，编译约 13.50 秒、仿真约 0.34 秒。故障 trace 变体和截断数组没有被算成额外 DUT 执行周期。新增 7 项控制/计账/无损压缩检查通过。

从仓库根目录重放 immutable checker 评估，使用新输出目录：

```sh
.venv/bin/python scripts/evaluate_spi_core_checker.py --candidate results/real_parent_screen_20261104/claude-checker-v1/candidate --controls results/real_parent_screen_20261104/spi-checker-controls-v2 --output build/reproduce_spi_core_checker/evaluation
.venv/bin/python scripts/evaluate_spi_core_checker.py --candidate results/real_parent_screen_20261104/claude-checker-v1/candidate --controls results/real_parent_screen_20261104/spi-checker-postreview-v1/controls-v2 --output build/reproduce_spi_core_checker/followup
.venv/bin/python scripts/summarize_spi_core_checker_audit.py --base results/real_parent_screen_20261104
.venv/bin/python -m unittest discover -s tests -p test_spi_core_checker_controls.py -v
```

补充双仿真器实验也可独立重跑，不需要 API key：

```sh
.venv/bin/python scripts/probe_spi_core_checker_followup.py --screen results/real_parent_screen_20261104/spi_host_core_v2/screen-v2/screen.json --output build/reproduce_spi_core_checker/simulation-followup
```

下一步应先确定有权威依据的 core 字节序合同，再由 Claude 修正 pending-offer、事件完整性与未支持属性，补非均匀数据和模式控制。原始不一致版本必须保留；若建立修订合同或 RTL，另行登记版本。之后还要证明多步事件对应的等价源目标确有区分力——普通流量已覆盖 16/20 组的问题仍在。只有这些门槛和原定 B 开发门槛通过，才能冻结正式 A/B/C/P；本轮没有 C 相对 B 的效果结论。
