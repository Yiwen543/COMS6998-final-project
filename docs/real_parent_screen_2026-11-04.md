# 真实多模块集成筛选 — 2026-11-04

本轮完成了事前登记、原版父模块编译、层级语义/源映射筛选，以及 SPI core 的固定 JSON driver 和双仿真器观察性校准。**SPI 达到独立 checker 建设入口，尚未达到 B 试跑入口。** AXI DMA 静态目标不足；另一 I2C 父模块仍有语义适配阻塞；完整 Flash 顶层的多时钟/复位依赖在执行前明确暂缓。本轮没有调用 OpenAI 或 Anthropic，没有生成新的 B/C 效果结论。

机器可读入口：[decision.json](../results/real_parent_screen_20261104/decision.json)。此前的[写通道/Flash 子模块报告](natural_write_scope_preflight_2026-11-04.md)和失败记录保留，不用本轮结果替换。

后续已执行的 Claude 作者/复核及未通过门槛的原因，单独记录于 [SPI core checker 审核](spi_core_checker_audit_2026-11-04.md)。以下“未调用模型”指本页的离线预检阶段。

## 事前登记和边界

[登记文件](../configs/real_parent_screen.json)在新父模块 elaboration、证明、seed 或模型输出之前写入，时间为 `2026-11-04T16:17:33.416322+00:00`，基线提交为 `50d7ee83d61989017e28e981420cd58f4c5f0787`。源码 SHA-256 和 upstream Git blob identity 均记录。父模块和原子模块未经修改；没有为了出现等价关系添加连线、复制分支或构造 wrapper DUT。

| 登记顺序 | 实际原版集成 | 固定版本/主要参数 | 本轮决定 |
|---|---|---|---|
| 1 | `axi_dma`，连接原版 read/write 通道 | verilog-axi `516bd5dadc3365b7f9e225d2af8fe0b8d804fe53`；32-bit 数据、16-bit 地址、最大 burst 16、unaligned 开启 | 0 组合格静态目标，不进入 checker/B |
| 2 | `spi_host_core`：FSM、shift register、byte merge/select、两颗参数化 packer 和 enabled flop | OpenTitan `0ea5236fe749e70ba18f56ba19c4be982ef46da7`；NumCS=2 | 进入独立规格 checker 建设，B 仍关闭 |
| 3 | `i2c_master_axil`：AXI-Lite 父模块、I2C master、command/write/read 三个 FIFO | verilog-i2c `a65be4045e898a52e791c6ee71f8f79a7cd2e129`；FIFO 深度均 32、prescale 默认 1 | 编译通过，语义适配尚未通过 |
| 执行前暂缓 | 完整 `flash_ctrl` 父模块 | 同一 OpenTitan revision，原版 English Breakfast generated top | 包含 OTP 第二时钟/复位、shadow/scan reset、TLUL、lifecycle 和 PHY/analog 依赖；当前单时钟证明不能认证 |

完整 Flash 没有通过绑定两个时钟、合并复位或删除子模块“简化成通过”。它也不计作已执行的第四个候选。SPI 是此前探索过的 IP 家族的新集成范围，**不是新增的独立 held-out IP**；目前仍未补齐两颗通过全部门槛的独立设计。

预算原样保留：3 次 B 重复、每次 6 轮、每轮最多 64 新周期、共同 8 周期 seed；`gpt-6.1-sol`、low、输入上限 32000、输出上限 16384、120 秒超时、最多一次重试。静态门槛仍是至少 3 组源位置不同的动态等价 guard，其中至少 2 组非平凡，每组至少 2 个 seed 未覆盖的原始源计数。B 接受门槛仍要求至少 2/3 次重复首轮后有两组未全命中，并且至少 2/3 次后续取得进展。未运行 B，不能声称满足这些条件。

## 适配、证明和测量

复用上一轮层级端口别名、完整 `if/case` 优先级、源位置、时钟/复位检查。新文件 [real_parent_semantics.py](../scripts/real_parent_semantics.py) 增加：

1. 真实 output port 的拼接连接，如 `{byte_en,byte_o}`；按位宽和位序拆成有方向的定义，不按名称直接合并。
2. 组合过程中对 packed vector 不同位段的阻塞赋值；保持执行顺序和最后一次写入优先级。只有全部位都显式赋值，才移除人工的未初始化初值；缺失位绝不补零。
3. proof-only `keep` 属性保留原始线网名称，使被优化掉的参数相关信号仍可与独立 netlist 逐项比对。属性只作用于证明用 JSON netlist，原始 SV 仿真不受影响。

首次 SPI 编译缺少真实 `prim_flop_en` 依赖，4 个前端均失败。随后在[依赖补充清单](../configs/real_parent_dependencies.json)登记同一 revision 的原版 primitive；没有修改最初范围、参数和预算。补齐后，三个实际执行父模块均通过 Slang、Verilator、Icarus 和 Yosys。

| 指标 | AXI DMA parent | SPI core |
|---|---:|---:|
| 独立 Yosys 定义/地址检查，全部 UNSAT mismatch | 236（229 定义 + 7 地址） | 215 |
| 并行 mux one-hot-or-zero 检查 | 32 | 6 |
| 原始提取 guard | 195 | 289 |
| 支持的聚合 activation target | 189 | 283 |
| 精确映射 / 未映射 | 180 / 9 | 269 / 14 |
| pair query SAT / UNSAT / unknown | 12713 / 193 / 0 | 22747 / 780 / 0 |
| seed-zero 动态源组 / 非平凡组 | 0 / 0 | 20 / 9 |
| 原始 DUT 分母 | 8598 | 3107 |

SPI 的实际 `egg 0.11.0` 运行使用 6 个已验证 Boolean rewrite 加 302 个 Z3 证明的 ground rules；5 次迭代饱和，493 e-nodes、316 e-classes，约 0.083 秒。证明文件、query 顺序和 rewrite explanations 均保存。**关系的发现/证明来自 typed SSA + Z3；egg 对已认证关系做等式饱和和分组。** 本轮不是“egg 单独发现全部关系”的实验。

范围仍是二值组合关系。状态寄存器、memory read 是自由当前值；不假定可达状态不变量，不证明完整时序功能或四态等价。AST 与 netlist 使用不同 IR 编码，但共享 Slang 前端。AXI 未完整赋值的循环临时变量仍显式记录，不用它认证目标。相同源码的多个实例不算两个不同源码位置；共享 loop/generate 计数的 activation 是所有相关路径的 OR。原始位置、层级和 hits 从不因表达式等价而转移或合并。

SPI 原始分母为 line 64、branch 234、expr 349、toggle 2460；AXI 为 line 148、branch 156、expr 194、toggle 8100。未证明不可达、未映射和未覆盖的点均留在分母中。这里的 line/branch/expr 是 Verilator 发出的计数类型，不是语句行数或 e-class 数量。

I2C 的[阻塞清单](../results/real_parent_screen_20261104/i2c_master_axil/adapter-gate.json)保留 13 项 extraction 和 33 项 definition unsupported 记录：包括 unpacked pipeline register、参数化 indexed slice、循环索引分析，以及 `addr_reg[bit_count_reg-2]` 在所有自由二值状态下可能越界。不能根据“正常运行应该不会越界”擅自添加状态不变量。编译成功不等于语义集成成功。

## 固定 driver 与私有校准

[固定 SV driver](../examples/spi_core_integration/verif/tb_spi_core.sv)只驱动原版 core 的公开命令、TX word/byte-enable、RX readiness 和 serial input。没有直接操纵 FSM 的 `sr_*_ready` 或内部状态，也没有 expected-output/checker 逻辑。[JSON 接口](../scripts/spi_core_interface.py)验证字段、整数类型、位宽、速度/方向约束、reset 和长度。每一行恰好一个核心时钟周期；输入先稳定，pre 在时钟上升沿前采样，post 在上升沿后采样。handshake 只使用 pre。

两种仿真器分别重新启动并执行相同完整序列。以下均是**未经过规格 checker 的观察结果**，不等于已证明合法恢复。

| 私有序列 | 周期，含 seed | 完全命中的源组 / 20 | 相对全部 ordinary controls 新增的组 |
|---|---:|---:|---|
| seed | 8 | 0 | 无 |
| 普通单字节 Standard write | 64 | 10 | 无 |
| 普通 Standard/Dual/Quad write | 184 | 14 | 无 |
| 普通 full-cycle read | 120 | 10 | 无 |
| TX 缺数据后补入第二个 word | 264 | 11 | stall 组 315 |
| RX word 背压后排空 | 392 | 10 | 同一个 stall 组 315 |
| partial read 后 CSID 切换 | 184 | 9 | 无 |
| 软件复位中止后重新发命令 | 184 | 10 | software-reset 组 0 |

三个 ordinary controls 合计已命中 16/20 组。TX/RX 两类物理事件不能因名称不同就把同一个 stall guard 算两次。reset 组只表示复位谓词被执行，不能证明事务被正确中止和重新启动。CSID 切换在修正版中接受了两条命令，但没有新增独立语义组。因此目前仅有**checker 建设入口**，缺少规格正确性、事件到源目标的区分力证据和独立 B 接受结果；不宣布目标冻结，也不启动 A/B/C/P。

最终 8 个 case 的完整公开 pre/post trace 在两种仿真器间一致，输入侧 valid/payload 保持检查通过。观察性 runner 为 [probe_spi_core_events.py](../scripts/probe_spi_core_events.py)，结果为 [spi_core_events-v3](../results/real_parent_screen_20261104/spi_core_events-v3/observations.json)。这些序列、计数、结果不进入 checker-author 或实验模型提示词。

## 保留的失败、初始化差异和成本

- v1 在时间零同时初始化/断言 reset，首周期 pre 观察在两种仿真器间不同。v2 起先让 inactive reset 稳定 1 ns，再断言 reset；没有新增时钟边沿或周期。
- 因此相对最初 reset inventory，8 个层级 reset 下降沿 toggle 从未覆盖变为覆盖。全部 3107 个原始计数身份/分母不变，20 组合格 guard 仍全部 seed-zero。此差异属于初始化测量政策，不记作模型贡献。今后各组必须使用同一修正 driver/seed。
- v2 的 CSID 切换只发单周期 valid，在 ready=0 时撤回，属于刺激接口错误。v3 保持到接受；未将 v2 记作成功事务切换或 DUT 缺陷。
- 最终校准：2 次编译、16 次仿真、两种仿真器合计 2800 周期；编译约 13.32 秒、仿真约 0.46 秒。包括失败和中间版本：6 次编译、34 次仿真、5616 周期。计数由实际日志重新汇总；静态 frontend/proof/inventory 的命令和时间另存各目录，不冒充这组校准成本。
- 10 个新检查与 35 个相关回归检查全部通过：拼接位序突变能被证明器拒绝；packed 最后写优先级、未初始化位拒绝、冻结预算、JSON/握手、作者包隔离、只使用 mock 的调用包装测试和原始计数身份均有检查。
- 本轮 live model calls=0，API tokens=0。没有 Token ROI 或 B/C 效率曲线可据此报告。

## 下一道门槛与角色

38,022-byte 的[最终作者包](../results/real_parent_screen_20261104/spi-core-spec-packet-v2/manifest.json)已准备。它只含原版公开规格节选、接口、采样和输入协议；Claude 不看到 RTL、旧 checker、校准向量、guard、覆盖或 B/C 结果。首次准备包被后续隔离检查替代，从未发送。

下一步由 Claude 独立写 payload/packing、stall/recovery、reset/restart 与事务切换属性及 checker。GPT/Codex 只集成固定 driver、执行独立正常/单故障控制，不改写 Claude 的 expected-output/checker 逻辑；问题返回原作者修正。再用新会话只读复核。运输复用现有隔离 Claude runner，包装器为 [run_spi_core_checker_roles.py](../scripts/run_spi_core_checker_roles.py)，计划最多一次生成和一次复核，每次 CLI 设置 `$4` 预算。

checker 的有效性、完整事件窗口无错误、事件对应的源目标、预算内可达性和不同事件的重复计数风险必须先检查。如果仍没有值得测的目标，保留淘汰结论，继续 I2C 适配或登记新自然 IP。不能仅因已经花费 checker 成本就启动 B，不能为了 C 缩短预算。之后若进入 B，仍应用事前登记的 3×6×64 开发门槛；A/B/C/P 需另行冻结目标和长度匹配规则。

## 复现

工具版本见 [tool-versions.json](../results/real_parent_screen_20261104/tool-versions.json)：Python 3.13.9、Verilator 5.050、Icarus 12.0、Slang 12.1.0+42710c788、Yosys 0.70+309、Z3 5.1.0、Rust 1.99.0。保留原版 pinned checkout 和已安装工具。从仓库根目录选择全新输出路径，不覆盖历史结果：

```sh
TASK_OUT=build/reproduce_real_parent/spi_host_core
.venv/bin/python scripts/real_parent_screen.py probe --top spi_host_core --output "$TASK_OUT"
.venv/bin/python scripts/real_parent_screen.py preserve --top spi_host_core --base "$TASK_OUT" --output "$TASK_OUT"
.venv/bin/python scripts/real_parent_screen.py inventory --top spi_host_core --base "$TASK_OUT" --output "$TASK_OUT/inventory"
.venv/bin/python scripts/real_parent_screen.py proof --top spi_host_core --base "$TASK_OUT" --output "$TASK_OUT/proof"
.venv/bin/python scripts/real_parent_screen.py screen --top spi_host_core --base "$TASK_OUT" --proof "$TASK_OUT/proof" --output "$TASK_OUT/screen"
.venv/bin/python scripts/probe_spi_core_events.py --screen "$TASK_OUT/screen/screen.json" --output "$TASK_OUT/events"
.venv/bin/python -m unittest discover -s tests -p 'test_real_parent_screen.py' -v
```

核对已完成的规范证据：

另在全新 build 目录实际重跑了 frontend、保留原始名称、inventory、proof 和 screen；上述计数以及所有 seed 原始计数身份和 hits 完全一致，见 [fresh-reproduction.json](../results/real_parent_screen_20261104/fresh-reproduction.json)。该额外静态/inventory 复现单独记账，不加入校准刺激或模型周期。

```sh
.venv/bin/python scripts/summarize_real_parent_screen.py --base results/real_parent_screen_20261104
```

暂存密钥后才执行作者/审阅调用；尚未执行以下命令：

```sh
.venv/bin/python scripts/run_spi_core_checker_roles.py --packet results/real_parent_screen_20261104/spi-core-spec-packet-v2 --output results/real_parent_screen_20261104/claude-checker-v1
```

作者输出后，runner 等待集成者运行独立控制并准备 `review-packet.json`，再调用新 reviewer；作者输出不会被直接冻结为可信 checker。调用结束/失败后清理 Git 忽略且权限为 0600 的暂存密钥。没有修改主分支远端，本轮也未执行 push。
