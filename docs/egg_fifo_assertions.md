# 用 egg 检查 FIFO 断言拆分

项目的研究重点转为 **egg 能否让同一条 RTL 规格更容易检查和诊断，同时留下独立可复核的证据**。本轮选取真实 FIFO 的跨拍行为，验证一条总断言能否安全拆成四条，并比较拆分后能否直接报告哪一个字段出错。[实验设计](egg_fifo_protocol.md)

## 验证了哪条规格

AXI-stream FIFO 上一拍在非复位状态下遇到 `TVALID=1, TREADY=0`，如果本拍仍非复位，就必须保留 `TVALID=1`，以及上一拍的 `TDATA`、`TLAST` 和 `TUSER`。两次观测都发生在相邻上升沿之前。形式模型假设第一拍复位，且输入侧在有效但未握手期间保持有效和载荷；输出侧的 `TREADY` 可逐拍变化。DUT 是固定提交中的原始 `axis_fifo.v`，深度 4、数据 8 位，启用 `TLAST` 和 `TUSER`，使用一级 RAM pipeline。[固定输入和 SHA-256](../scripts/m3_controller_replay_manifest.json) · [实际 DUT 实例、假设和监控](../examples/axis_fifo/formal/stall.sv)

总断言禁止某个触发场景下出现任一失败。脚本生成四条断言，每条保留相同的触发条件，分别禁止对应字段的失败。为了确认拆分保持规格，egg 只比较这些已经采样好的布尔条件：

```text
active ∧ (lost_valid ∨ changed_data ∨ changed_last ∨ changed_user)
= (active ∧ lost_valid) ∨ (active ∧ changed_data)
  ∨ (active ∧ changed_last) ∨ (active ∧ changed_user)
```

egg 在这一步使用经真值表确认的分配律、结合律、交换律和德摩根等规则，输出具名改写。独立检查器对照原式，核对每步的改写位置、替换方向和变量绑定。Python 把同一组条件生成 SystemVerilog，验证驱动还检查 Yosys 实际展开了预期的断言。FIFO 的跨拍正确性由 Yosys/Z3 验证。[四项拆分的完整证明](../results/milestone3/fifo-forms/split_four_fields.json) · [Yosys 使用的拆分断言](../results/milestone3/fifo-formal/assertions/split.svh)

## 公式对照

| 方法 | 证明等价的候选 | 错误接受 |
| --- | ---: | ---: |
| egg + 独立改写检查 | 5/5 | 0/5 |
| 普通结构归一化 | 1/5 | 0/5 |
| 同一批等式，普通双向树搜索，预算 64 项 | 5/5 | 0/5 |
| 同一批等式，普通双向树搜索，预算 1,024 项 | 5/5 | 0/5 |
| 独立真值表 | 5/5 | 0/5 |

egg 共输出 22 个核验通过的具名改写步骤。普通结构归一化没有分配步骤，普通双向搜索能在子项处正向和反向使用等式，因此也得到全部五份证据。egg 在本组公式上展示了可审查的推导能力，与更强的普通对照持平。表中的错误候选由独立真值表确定。egg 未证明某个候选时保留其搜索状态，公式确实不等价仍要靠反例判定。[公式、两种搜索记录和计数](../results/milestone3/fifo-forms/)

例如漏掉 `TLAST` 时，在触发有效且只有 `TLAST` 变化的赋值上，原式报告失败，误写的拆分会放过它。误用本拍 `TREADY` 有 30/1,024 个独立布尔赋值不同，可以直接由真值表复核。这里的独立赋值用于比较两个公式，实际 RTL 中的状态可达性另由时序模型和回放验证。[漏掉 TLAST 的反例](../results/milestone3/fifo-forms/omit_last.json) · [用错采样拍的反例](../results/milestone3/fifo-forms/use_current_ready.json)

## 原 RTL、故障注入和仿真

| DUT | 总断言 | 四项拆分 |
| --- | --- | --- |
| 未改动的 FIFO | 12 状态 BMC 和时间归纳通过 | 同样通过 |
| 注入丢失有效位 | 状态 5 失败 | 状态 5 报 `valid_lost` |
| 注入数据翻转 | 状态 5 失败 | 状态 5 报 `data_changed` |
| 注入 `TLAST` 翻转 | 状态 5 失败 | 状态 5 报 `last_changed` |
| 注入 `TUSER` 翻转 | 状态 5 失败 | 状态 5 报 `user_changed` |

五个 DUT 的阻塞前件均在状态 5 由独立 cover 查询确认可达。对五个 DUT 逐一单查四个字段，共 20 项对照，4 项预期失败、另外 16 项通过 12 状态 BMC。例如在 `TLAST` 翻转版上，如果漏掉 `TLAST` 检查，剩下三项在同一深度都通过。两种写法各自找到的 8 条求解器反例都原样回放到原版及对应故障版，共 **16 次 Icarus、96 个沿前观测**。每条都在第 4 个零基采样观察到阻塞，第 5 个采样只在故障版出现预期字段变化。数据翻转例中原版保持 `0x01`，故障版变成 `0x00`。[求解日志、证人与形式结果](../results/milestone3/fifo-formal/) · [Icarus 对照回放](../results/milestone3/fifo-replay/)

本轮验证了固定参数实例的输出保持性质，证明拆分前后检出相同的违例，同时使求解日志明确指出失败字段。结论适用于提供的二态模型、复位与合法输入约束。FIFO 的吞吐、顺序、无丢包及其他参数组合仍是独立的验证问题。

## 环境、脚本与复现

在 Debian 13 上用 Python 3.12、Rust/Cargo 1.90、锁定的 egg 0.11、Yosys 0.52（带 `yosys-smtbmc`）、Z3 4.16 和 Icarus 12.0（带 `vvp`）实测。沿用 Milestone 3 的环境安装步骤。从仓库根目录运行下面两行，两个目录都使用新路径。已有之前下载的固定 Controller fixture 时可以直接使用它。整个流程无需模型 API。[安装命令](milestone3.md#环境与一键复现)

```bash
python3 scripts/m3_controller_replay.py --fetch /tmp/egg-fifo-fixture
bash scripts/run_egg_fifo.sh /tmp/egg-fifo-fixture /tmp/egg-fifo-run
```

| 文件 | 职责 |
| --- | --- |
| `run_egg_fifo.sh` | 构建 Rust 引擎，运行公式核验、RTL 形式验证和 Icarus 回放，并核对形式验证用的公式和 egg 已证明的公式完全相同。 |
| `egg_assertion_forms.rs`、`egg_fifo_assertion_forms.py` | 生成候选、运行 egg、保存每个候选的等价类与具名证明，并生成与正式 RTL 检查绑定的公式清单。 |
| `m3_proof_dependencies.py`、`egg_assertion_baseline.py` | 分别检查 egg 局部证明和普通搜索路径，并提供结构归一化及独立真值表。 |
| `egg_fifo_formal.py` | 校验固定 RTL、生成断言及故障对照、运行 BMC、归纳和 cover，存档原生 Yosys 证人。 |
| `egg_fifo_replay.py` | 从证人重新解码外部输入，在未插桩的原始 RTL 和故障版上回放并核对观测。 |
