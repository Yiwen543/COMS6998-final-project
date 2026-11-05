# SPI core 字节序合同修订与 checker 第二轮 — 2026-11-04

本轮明确了有固定版本上游依据的 **低字节优先 core 合同**，实际完成一次 Claude 定点修正和一次独立 Claude 复核。字节序与 pending-CSID 修正通过了控制；但 CPOL=1 的边沿归属和 TX starvation 事件漏记尚未解决。因此 **checker 未冻结，B/C 均未启动**。下一轮修正包及独立控制已准备，正在等待隐藏暂存 Anthropic key。

完整机器可读账本：[contract-repair-decision.json](../results/real_parent_screen_20261104/contract-repair-decision.json)。旧 [checker 审计](spi_core_checker_audit_2026-11-04.md)、MSB 合同、失败 checker 和所有原始结果保留，没有覆盖历史。

## 合同依据与边界

上游 revision 固定为 `0ea5236fe749e70ba18f56ba19c4be982ef46da7`，实际 DUT 仍为原始 `spi_host_core`，NumCS=2。

1. 固定版本 [Data Formatting](https://github.com/lowRISC/opentitan/blob/0ea5236fe749e70ba18f56ba19c4be982ef46da7/hw/ip/spi_host/doc/theory_of_operation.md#L412-L419)、[编程指南](https://github.com/lowRISC/opentitan/blob/0ea5236fe749e70ba18f56ba19c4be982ef46da7/hw/ip/spi_host/doc/programmers_guide.md#L65-L90)和寄存器说明规定：父模块 `ByteOrder=1` 时先发送低 byte；首个 RX byte 放入低 byte，末尾不足一 word 时在高 byte 补零。byte 内部仍是 MSB-first。
2. 固定父模块 [ByteOrder/ByteSwapping 注释和连接](https://github.com/lowRISC/opentitan/blob/0ea5236fe749e70ba18f56ba19c4be982ef46da7/hw/ip/spi_host/rtl/spi_host.sv#L427-L460)明确说明 core 数据通路天然采用低字节优先；`SwapBytes=~ByteOrder` 在 core 外生效。外部 FIFO 在不交换时仅保持 byte lane 和 word 顺序。因此默认 LE 寄存器语义可经这个端口映射应用到 core pins。
3. 上游 [DV 说明](https://github.com/lowRISC/opentitan/blob/0ea5236fe749e70ba18f56ba19c4be982ef46da7/hw/ip/spi_host/dv/README.md#L48)和 scoreboard 提供旁证；scoreboard 没有交给 checker 作者，也没有被复制为 golden model。
4. 同一文件较后的内部组件描述仍写 MSB-first，与以上依据矛盾。项目将其 ordering 条款单独标记为被修订，而非默默改答案。**这是有来源、带版本的项目合同解释，不是已获上游维护者确认的勘误。** 未从浅克隆历史推断矛盾发生时间。

这些本地文件和下载的 DV 文件均核对了固定 revision 的 Git blob，合同保存 SHA-256、来源 URL 和编号原文。详细内容在 [contract.json](../results/real_parent_screen_20261104/contract-repair-v2/authority/contract.json)。期望行为来自公开接口意图及 core 外端口映射，不以 DUT 的实测 payload 作为规范。

| 输入/输出情形 | 修订后的合同 |
|---|---|
| TX word `0xA1B2C3D4`，BE=15 | 依次发送 D4、C3、B2、A1 |
| 同一个 word，BE=5 | 只发送 lane 0、2：D4、B2 |
| RX 依次收到 A5、5A、3C | word 为 `0x003C5AA5`，高 byte 补零 |
| 每个 byte 的线上 bit 顺序 | 高位先传，未改变 |

core 本身没有 ByteOrder 参数；本实验也没有增添此参数、byteswap 或 DUT 补丁。同步软件复位、异步硬复位、完整激活 guard 和原始源计数仍分别处理。

## 实际执行及发现

Claude `claude-opus-5-5` 作者只看到修订后的公开规范/接口、原 Claude 源码和逻辑问题描述，未看到 DUT、上游 scoreboard、私有校准、guard、覆盖或 B/C 结果。GPT 只准备 driver/刺激/控制及计账。只有 Claude 返回的唯一匹配补丁被应用；作者与 reviewer 均禁用工具、无会话持久化。

第二版 checker SHA-256：`31890549ab2f221984ade7fdb2133ae890b88136ff6dd0da68c33b49ddfab6c1`。

初始 47 个控制包括 9 个独立手工正常轨迹、8 个旧校准、5 个旧补充控制、14 个新增真实 DUT 模式/RX 探针，以及新增故障/截断控制。

| 检查 | 结果与解释 |
|---|---|
| 作者自测 | 14/14 通过，不能替代独立验证 |
| 9 个独立正常控制 | 9/9 无误报且 pass，含非均匀 1–4 byte 和稀疏 BE |
| 初始 10 个单故障控制 | 基线均 scoped pass；9 个有检出信用；missing RX word 保持 inconclusive，不能因缺少规范期限而强报 DUT failure |
| 非均匀 FULLCYC=1 RX | 实际两个仿真器均得到 `0x003C5AA5`，checker pass |
| 实际待接受 CSID 切换 | 原有校准 pass；旧 CS 可在新命令 acceptance 之前释放 |
| CPOL=1 模式探针 | 6 条共有 275 条级联诊断，属于同一 checker 边沿归属问题，不能算 275 种 DUT 缺陷 |
| TX starvation | 完整、截断和 dirty recovery 原先均漏记该事件；本轮仍未修好 |
| 软件复位 | unresolved，事件标作 pass_unresolved；不计作已证恢复成功 |
| 独立 reviewer | `ready_for_offline_gate=false` |

**CPOL 问题：** command acceptance 后、所有 CS 尚为高时，SCK 可以调整到新 idle level。第二版 checker 把这个变化算作 payload 的第一条边，提前取走 command，并使后面的 phase/bit 计数全部错位。公开规格要求 CPOL 在 all-CS-high 间隔生效，不能把这个结果解释为 DUT 违反 SPI。

**TX 事件问题：** 最后一个 enabled byte 已耗尽，但 word cursor 尚未跨到下一个 word；而停顿可以发生在最后一次采样之后、trailing edge 之前。只看 cursor 或完整 edge-pair 的计数会漏掉真正的 starvation。需要由 Claude 原角色继续修正，不能由 GPT 改 expected-output 实现。

## 本轮另外修复的实验基础设施

独立 reviewer 正确指出：评估器以前只检查已有成功事件的窗口，未检查“应有事件却没有出现”。现在 `required_event_family` 缺失会进入 `event_integrity_errors`，不能凭空事件列表获得完整性通过。扩展控制对第二版 checker 明确报告 5 处漏记；历史评估的空错误列表没有被回写。

进一步新增 17 个独立 hand positive，覆盖四种 CPOL/CPHA、三种宽度、非零 timing、非均匀 RX 以及采样后/尾沿前的 starvation。与旧控制合并并修复 RX 刺激后共 68 个 case；26 个独立正常控制中第二版仅 18 个无误报，8 个 CPOL=1 控制失败，进一步确认不能冻结。

另一处是控制刺激自己的问题：最初 FULLCYC=0 RX 使用了 FULLCYC=1 的时钟安排，导致输入在采样窗口内变化。它正确得到 inconclusive。已按 FULLCYC=0 自己的公开 SCK 时间安排重新生成输入并双仿真器执行，**不改 checker** 即 pass；原 case 留作 sampling-ambiguous 控制，不计成 DUT bug 或 checker false positive。

新增 6 项合同/模式/计账回归检查通过，之前 7 项 SPI 控制检查也通过。事件漏记回归使用一个刻意返回 pass 且不输出事件的 MOCK checker，端到端确认评估器会拦下；这个 mock 与生产 Claude checker 完全分开。

## 独立复核的范围和误读

本次 reviewer 获得 41/47 条完整无损轨迹。由于本地 150,000-byte 上限，6 条无失败的 CPOL=0 补充 TX 探针未提供完整轨迹，但所有 47 个 verdict、诊断总数和控制定义均提供。仅展示每 case 首条 failure、其他类别前三条，完整账本保留本地。最终请求 148,810 bytes；所有被包含轨迹逐行还原验证通过。先前超限的准备尝试在本地被拦下，未调用 API。

复核的两个表述需要纠正，原意见保留：

- F4/F7 声称除 selftest 外没有真实 pending-CSID 控制；实际上 `calibration/partial_then_csid_switch` 完整包含在包中且 pass。不能把 reviewer 的遗漏当成不存在证据。
- F5 只见首条 half-period 诊断后称没有 underflow 检出；完整故障结果同时包含 `tx_underflow`。不过这个单行 SCK 扰动确实造成两个转换，仍不能证明能检出所有满足最短周期的非法 stall pulse。

## 费用与执行量

| 调用 | API 输入（含缓存新建） | 输出（含 thinking） | 报告费用 | 时间 |
|---|---:|---:|---:|---:|
| Claude v2 作者 | 36,790 | 8,218 | $0.348306 | 72.10 s |
| Claude 独立复核 | 73,832 | 4,529 | $0.459736 | 51.79 s |
| 本轮合计 | 110,622 | 12,747 | **$0.808042** | 123.89 s |

总计 **123,369 API token**；5,494 thinking token 是输出子项，未重复相加。该成本属于 checker 基础设施，不能放进 B/C 刺激 Token ROI。两次调用均成功，无模型替换、无调用重试。暂存 key 已删除。

本轮新增 4 次编译、30 次仿真，两种仿真器合计 **5,136 个实际周期**；编译约 26.76 s、仿真约 1.11 s。手工轨迹、故障数组修改和 checker 重放不算 DUT 执行。两种仿真器逐行一致；所有 **3,107 个原始 DUT counter 身份**与之前 seed 完全相同，TB 排除，初始化/复位仍计入同一口径。未把分项时间之和称为完整端到端墙钟时间。

## 下一步及可复现入口

下一轮 [93,008-byte 修正包](../results/real_parent_screen_20261104/contract-repair-v3/packet/manifest.json)已准备，仍只允许 Claude 改 checker。先解决 CPOL 和事件完整性，再跑独立正反控制及全新只读复核；未支持的软件复位等义务保持显式 unresolved。

通过这些条件后才能登记冻结 checker 和目标，执行原预算 **3 次重复 × 6 轮 × 64 新周期**的独立 B 开发试跑。C 还须等待 B 通过原先的未立即饱和/后续进展门槛。本轮没有缩短预算，也没有依据 C 结果选题。普通流量已经命中 16/20 组、SPI 属于之前探索过的设计家族等限制仍然存在。

```sh
.venv/bin/python scripts/evaluate_spi_core_checker.py --candidate results/real_parent_screen_20261104/claude-checker-v2/candidate --controls results/real_parent_screen_20261104/contract-repair-v3/rx-window/controls --output build/reproduce_spi_contract/evaluation
.venv/bin/python -m unittest discover -s tests -p 'test_spi_core*.py' -v
.venv/bin/python scripts/summarize_spi_core_contract_repair.py
```

隐藏暂存 key 后的已准备命令（尚未运行）：

```sh
.venv/bin/python scripts/run_spi_core_checker_roles.py --packet results/real_parent_screen_20261104/contract-repair-v3/packet --prior results/real_parent_screen_20261104/claude-checker-v2/candidate --output results/real_parent_screen_20261104/claude-checker-v3
```

该 runner 在作者返回后等待集成者完成离线控制并发布复核包，再执行一次独立 review，最终删除暂存 key。作者包不含私有刺激或 DUT 源码。
