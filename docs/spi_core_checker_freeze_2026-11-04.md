# SPI core checker v4：事件误报修正、有限冻结与 B 门槛

本报告接续 [字节序合同修订](spi_core_contract_repair_2026-11-04.md)。Claude 原作者完成 v3、v4 两次补丁，各由一个全新只读 Claude 会话审阅；GPT 没有修改生产 checker 的 expected-output 逻辑。v4 获得 `ready_for_offline_gate=true`，随后通过本地离线门槛。**这允许有限范围的独立 B 开发试跑，不等于完整 IP 认证，也不直接允许 C。**

## 修正的两个层次

v3 修好了 CPOL 空闲电平被误当 payload 边沿，以及真实 TX starvation 漏记。26 个独立正常控制全部通过。然而新增原版 DUT 反向控制发现：8 条时钟未暂停的轨迹中，晚到 TX word 和仅延迟一拍读取 RX word 各被误记一次“恢复成功”。这是两个事件计数误报，不是两个 DUT 缺陷，也不是总体误报率估计。

v4 由 Claude 定点修正：事件必须有超出配置半周期的实际 SCK 停顿证据；stall flag 本身不能建立恢复事件。事件窗口从所属 segment acceptance 开始，先前 payload 错误会使整个窗口失败。必须完成相关 segment、要求的 CS 释放和 RX 接收，才能记成功。

三个旧截断控制刚好停在预期下一边沿时刻，此时尚无“严格超过”的证据。原始轨迹保留并禁止记成功；另外增加延长一周期的三个前缀，要求出现 pending 事件且禁止成功。这个控制预期修订、原始失败及新增前缀全部交给独立 reviewer；reviewer 认为修订合理，而不是为了通过测试降低要求。

## 独立验证的实际范围

| 项目 | v4 结果 |
|---|---|
| 作者自测 | 24/24；不能代替独立控制 |
| 合格控制总数 | 88；包括真实 DUT、手工规范轨迹、输出单故障、截断及非法输入 |
| 独立正常控制 | 26/26 scoped pass，无误报 |
| 单故障控制 | 14 条基线均 scoped pass；13 条检出；missing RX word 为 inconclusive，不虚构完成期限 |
| 无 stall 的反向控制 | 8/8 不再错误报告恢复事件 |
| 只改 stall flag 的控制 | 2/2 不产生成功恢复 |
| 成功事件与错误窗口重叠、漏记应有事件 | 最终评估无此类错误 |
| 普通/模式/切换控制 | 通过限定合同；保留一个同 CSID 配置切换规范分歧 |

合法的同 CSID、CSAAT 后配置切换，在固定原版 RTL 上没有出现公开 theory 241–249 要求的 idle gap。两种仿真器一致；checker 的 35 条诊断含级联 phase 错误，不能算作 35 个独立缺陷。该结果记录为 **DUT 与固定文档的分歧，尚待上游解释**，没有改 RTL、豁免检查或向实验模型泄露该反例。最早试探控制额外维持 valid、意外提供第二条命令，属于刺激问题；修正为单次合法 offer 后重新执行，两个版本均保留。

最新 reviewer 收到 70/88 条完整无损轨迹，所有 88 条 verdict、failure、assumption、unresolved 和事件诊断均完整提供。18 条普通通过轨迹只提供诊断，没有提供全部原始 rows。最终请求 148,420 bytes；三次过大准备包在本地被拦下，没有 API 调用。Reviewer 是只读分析，没有执行程序或给出形式证明。

剩余限制明确保留：软件复位和 dummy completion 未解决；RX 仅在稳定采样窗口内判定；只检查最短时序、不证明 liveness；未有硬复位后 stale payload 的独立故障控制；未接受 offer 引发的 CPOL 调整未单独覆盖；长时间但无害的 RX hold 与自然 inter-byte gap 重合时仍有事件误分类风险。Reviewer 写的 “no FIFOs” 过宽：本次实际包含两个内部 packer FIFO，排除的是外部数据 FIFO 和 TLUL。仅二值仿真/组合证明，不声称四值等价。

## 冻结内容与离线资格

生产 checker SHA-256：`07765601452ca14f078e8a3889f6d2d21574181091eb404c717087ce2d20a540`。

[冻结配置](../configs/spi_core_b_development.json)记录完整 DUT/source、公开合同、Claude artifacts、driver、schema、解析器、runner、语义证明、校准和控制的哈希；执行前及各轮执行前重验。实际 DUT 保持 revision `0ea5236fe749e70ba18f56ba19c4be982ef46da7`、NumCS=2，core 内子模块真实连接，未补丁或绕过 ready。

本次将已审阅范围明确为：共享 seed 后 `enable=1`、`sw_reset=0`，不发 dummy command；其余原有宽度和时序参数范围不缩小。该范围在第一条实验模型生成之前冻结，未来各组完全相同。硬复位仍保留。未支持行为并没有被改判为 pass。

将双仿真器完整轨迹与 v4 实际评估输入逐行核对、检验输入合法性及原始源计数后，原预算内确认三类多步事件：TX starvation/resume、RX backpressure/resume、partial-word 后的 transaction 切换。

20 组静态候选中，**17 组**在完整、合法、scoped-pass 的私有校准中可达，其中 **8 组非平凡**；每组至少两个源位置不同、实际共享 seed 未命中的计数。选择规则是包含所有符合以上条件的组，没有看 B/C 输出选目标。其余 eclass 0、62、214 没有合格的完整可达证据，排除出此目标子集，但没有被证明不可达，其原始计数仍在分母中。

**3,107 个 DUT counter 全部保留：line 64、branch 234、expr 349、toggle 2,460。** 原始层级实例及源位置分别计数；不能因为一个等价点命中就把其他点也记为命中。未解决的 14 个 guard 映射不被静默删除。初始化和复位活动计入，TB 排除，每次累计 replay 使用新 simulator process。

这些是静态与可达性资格，并没有证明任务足够难：普通校准已命中原 20 组中的 16 组；TX/RX 两种时间事件共享同一组合 stall group。SPI core 也仍是已探索的 OpenTitan SPI 家族，不能当作第二颗独立 held-out IP。是否值得跑 C，由原登记的 B 门槛决定。

## Runner、预算与计账

新集成 runner 复用官方 OpenAI Responses adapter、原始覆盖 parser 和固定 JSON driver；没有调用旧的 FSM-only runner 冒充 core 实验。模型只返回 JSON actions，无法编辑 checker、DUT 或计量。

- 原预算不变：3 repetitions × 6 rounds × 最多 64 新周期，共享 seed 8 周期；`gpt-6.1-sol`、low、输入 32,000 / 输出 16,384 tokens、120 s timeout、最多一次重试。
- B 反馈为原始零命中 line/branch/expr counter：按固定 source identity 排序，128 点循环分页，保留 kind、polarity、层级及原始源码行。分页不按目标或等价组排序。全部原始计数仍逐轮落盘。完整 RTL、公共合同和自己的历史动作均提供；最后 16 条 public-pin trace 与至多每类前 8 条 checker 诊断提供，诊断总数保留。无事件类别提示、校准序列、已知反例、checker 源码、solver witness 或 e-graph 附录。
- 每次生成先以 API 对确切请求计数；超出 cap 不生成、不静默换模型。原始请求/响应、usage、cached/reasoning 子项、验证失败及重试逐次保存。输入+输出才是总 token，子项不重复相加。
- 所有累计刺激在同轮完整执行后才检查。Coverage 在离线 checker 执行前已写盘，DUT failure 不会丢掉计数。超时/崩溃保留已输出 trace，实际周期和请求周期分开。
- 编译、仿真执行、累计 replay 周期、模型调用、计数请求、失败尝试和时间分别记录；诊断总条数与类别分别记录，类别也不直接等于经确认的缺陷根因。

21 项相关自动检查通过（14 项原有控制/合同检查，7 项新增边界、提示隔离、source counter、usage 和 gate 检查）。完整 mock 及其 replay 各完成 3×6 轮、1 次编译、21 次仿真和 4,200 个实际周期；18 轮 raw coverage summary、每目标计数及 checker 结果逐项一致。没有 API 调用，也不能因 mock/replay 而通过 live B 门槛。

原 B 接受条件保留：三个重复都完整且无输入 assumption violation；至少两个重复在首轮仍有至少两组未全部命中，至少两个重复在后续轮次有组目标进展。截断的 pending/inconclusive 不自动变成 DUT 失败或 pass；checker 确认的 DUT failure 不作为坏 testbench 丢弃。未通过门槛不会缩短预算重试以制造 C 优势。

## 本轮成本

| 调用 | API 输入（含缓存新建） | 输出（含 thinking） | 报告费用 | 调用时间 |
|---|---:|---:|---:|---:|
| Claude v3 作者 | 38,340 | 12,903 | $0.449756 | 121.26 s |
| Claude v3 独立复核 | 73,376 | 6,258 | $0.492036 | 68.49 s |
| Claude v4 作者 | 40,274 | 11,234 | $0.426046 | 113.40 s |
| Claude v4 独立复核 | 77,340 | 4,324 | $0.473176 | 48.60 s |
| 合计 | 229,330 | 34,719 | **$1.841014** | 351.75 s |

共 264,049 API token；22,897 thinking tokens 已含在输出，不重复加。v4 本身两次调用共 $0.899222、133,172 tokens。所有调用完成，无模型替换；暂存 Anthropic key 已删除。这是 checker 建设成本，不能混入 B/C 刺激的 Token ROI。

本轮新增反向/边界 DUT 控制为 6 次编译、32 次仿真、8,800 实际周期，含首次无效边界控制的执行；编译 39.47 s、仿真 1.21 s。另有 mock/replay 共 2 次编译、42 次仿真、8,400 周期，单独标识。手工 trace、数组故障注入和离线 checker 重放不算 DUT 仿真。以上调用/阶段时间不是端到端墙钟时间。

## 复现

```sh
.venv/bin/python -m unittest discover -s tests -p 'test_spi_core*.py' -v
.venv/bin/python scripts/evaluate_spi_core_checker.py --candidate results/real_parent_screen_20261104/claude-checker-v4/candidate --controls results/real_parent_screen_20261104/contract-repair-v4/qualified-controls --output build/reproduce_spi_core_v4/evaluation
.venv/bin/python scripts/qualify_spi_core_experiment.py --output build/reproduce_spi_core_v4/qualification.json
.venv/bin/python scripts/run_spi_core_b_development.py --mode mock --output build/reproduce_spi_core_v4/mock
.venv/bin/python scripts/run_spi_core_b_development.py --mode replay --replay build/reproduce_spi_core_v4/mock/calls.jsonl --output build/reproduce_spi_core_v4/replay
```

已冻结的配置不应重写。Live B 需隐藏暂存 OpenAI key，使用：

```sh
.venv/bin/python scripts/run_spi_core_b_development.py --mode live --output results/real_parent_screen_20261104/spi_core_b_live_v1
```

结果依据该目录的 `summary.json`/`rounds.jsonl`，不能把本文的离线资格当成 live B 已通过。后续 C 需要在 B 通过之后另行冻结对照，不自动运行。
