# AXI DMA 写通道与 Flash 编程／仲裁预检 — 2026-11-04

本轮完成范围固定、层级语义与源计数适配，并重新执行离线筛选。三个固定模块仍未达到原定静态门槛，因此没有启动 Claude checker、可达性校准或 B 开发试跑。这个结果说明当前范围缺少足量合格目标，不说明 DUT 功能错误，也不是新的 B/C 性能结论。

## 预先固定的边界

配置 [natural_write_scope.json](../configs/natural_write_scope.json) 在本轮前端运行与覆盖结果产生前写入；每个前端目录保留配置副本和 SHA-256。工作区基线提交为 `50d7ee83d61989017e28e981420cd58f4c5f0787`，本轮改动尚未提交或推送。

- AXI DMA：原版 `axi_dma_wr`，上游提交 `516bd5dadc3365b7f9e225d2af8fe0b8d804fe53`。32-bit AXI/AXIS、16-bit 地址、最大 burst 16、启用 unaligned、禁用 SG，其余参数也显式列出。保留原版同步高有效复位。
- Flash：原版 `flash_ctrl_prog` 与 `flash_ctrl_arb`，上游提交 `0ea5236fe749e70ba18f56ba19c4be982ef46da7`，**EnglishBreakfast 生成版本**及其真实子模块，保留异步低有效复位。不是完整 Earlgrey Flash controller。
- 两个 Flash 模块分别作为顶层分析，**没有虚构它们之间的连接，也不跨两个顶层合并表达式**。它们属于一个 IP 家族；本轮总计两个独立家族、三个分析单元。
- 新 [Flash 清单](../configs/flash_write_sources_manifest.json) 包含 31 个精确 Git blob，增加原版 arbiter 和 sparse FSM flop；旧 29 文件清单不变。包、宏和技术实现没有使用 stub。编译的 `SYNTHESIS` 宏关闭上游断言宏，因此不是断言通过证据。
- 延续预算：3 次 B 重复、6 轮、每轮最多 64 个新周期、8 周期 seed；模型与 token 限制也沿用前版。门槛仍为至少 3 组源位置不同的等价目标、至少 2 组非平凡关系、每组至少 2 个 seed 未覆盖的原始计数，后续还必须绑定至少 3 类合法可达多步事件。

上游：[AXI 写通道](https://github.com/alexforencich/verilog-axi/blob/516bd5dadc3365b7f9e225d2af8fe0b8d804fe53/rtl/axi_dma_wr.v)、[Flash 编程](https://github.com/lowRISC/opentitan/blob/0ea5236fe749e70ba18f56ba19c4be982ef46da7/hw/top_englishbreakfast/ip_autogen/flash_ctrl/rtl/flash_ctrl_prog.sv)、[Flash 仲裁](https://github.com/lowRISC/opentitan/blob/0ea5236fe749e70ba18f56ba19c4be982ef46da7/hw/top_englishbreakfast/ip_autogen/flash_ctrl/rtl/flash_ctrl_arb.sv)。Flash 清单还固定了该生成版本的规格文档；尚未把规格转为独立 checker。

## 实现与证明

[hierarchy_semantics.py](../scripts/hierarchy_semantics.py) 为实例内信号加入完整路径，展开 Slang 缓存的重复实例，处理 elaborated generate 范围。输入／输出连接转成保留方向和位宽的定义，支持结构体、完整且不重叠的 packed 切片；不按信号同名直接 union。

支持的 guard 保留 statement-position SSA、外层 if 的真／假路径、case 所有先前匹配排除、原始源位置及边沿上下文。固定次数循环有 64 次展开上限，保留每次迭代进入条件；实际 DMA 循环是 3、2、1、0。纯单 return 函数按类型展开。动态 packed 索引仅在二值选择器的整个域都合法时支持；越界情形不假定为零。

[hierarchy_netlist_proof.py](../scripts/hierarchy_netlist_proof.py) 用独立 Yosys 单元编码核对以上定义。DMA 内存读保留每个源表达式的任意当前读值，并核对精确 memory/source/address 对应；没有假定两个读口内容一致、FIFO 内容正确或某状态可达。FF Q 是自由当前状态；未在全部路径赋值的循环变量 `i` 显式记录，不作为有效组合别名。所有被使用的组合值都有定义，`i` 不进入这些 guard。

AXI 的三个原始内部信号会被 `opt_clean` 删除，故仅为证明保留其名字：`cycle_size`、`tr_word_count_next`、`input_last_cycle_next`。这不修改仿真的 RTL、参数或预算。此前缺失信号及未简化网表的失败证明保留为诊断记录。

Z3 证明二值、同上下文的具体表达式对后，导入真实 Rust `egg`：20 iterations、20,000 nodes、5 秒上限，输出重写解释；每个跨源合并再次核对 UNSAT。不是手写语义摘要或 AST 去重，也不是四值或时序等价证明。Slang AST 与 Yosys `read_slang` 共享前端，这仍是独立性的限制。

[screen_write_hierarchy.py](../scripts/screen_write_hierarchy.py) 按真实模块层级、文件、行、列、极性和计数类型精确关联。增加 packed select 的 `[`、replication 内层 `{` token，以及工具实际提供的 `line/else` 计数。没有独立计数的 else-if 补集仍 unresolved，不从相邻计数相减推断。

Verilator 对部分循环／generate 位置共享一个原始计数。对此先合并**该计数的完整激活条件并集**，再比较等价性；不能声称某次迭代已执行。不同原始位置始终分别保留。重复实例的同一源码位置也不能充当两个源位置，覆盖分母不删减。

## 实际结果

权威证据：[decision.json](../results/natural_write_screen_20261104/decision.json)、[summary.csv](../results/natural_write_screen_20261104/summary.csv)，各模块的 `proof-final/`、`screen-final/`、`source-map.csv` 和 `mapping-disposition.json`。早期 `netlist-proof*`、`proof-v2`、`screen` 是诊断历史。

| 固定范围 | 原始 guard / 按计数聚合后的激活条件 | 精确映射 / unresolved | 组合定义与地址检查 | 未覆盖动态等价组 / 非平凡组 |
| --- | ---: | ---: | ---: | ---: |
| AXI DMA write | 127 / 121 | 115 / 6 | 80 定义 + 7 读地址 | 0 / 0 |
| Flash program | 64 / 48 | 44 / 4 | 65 定义 | 1 / 1 |
| Flash arbiter | 28 / 28 | 26 / 2 | 30 定义 | 0 / 0 |

所有上述定义／地址检查均 UNSAT；额外 pmux 选择互斥检查分别为 19、3、13 项，均通过。候选对查询分别是 5,142 SAT / 40 UNSAT、555 SAT / 34 UNSAT、315 SAT / 2 UNSAT，均无 unknown。导入 egg 的不同表达式 ground rules 分别为 36、28、2 条。证明存在不代表符合实验筛选门槛。

- **DMA**：剩余重复多来自固定 `ENABLE_UNALIGNED`、`AXIS_KEEP_ENABLE` 等参数判断或 reset。参数判断本身恒定时，即使外层完整 guard 动态，也按预定筛选政策排除该成员；不能用重复的参数门控凑组数。
- **Flash program**：唯一候选组是 `prim_count.sv` 第 103、104 行。双计数器的 increment/decrement 端口关系经过层级展开，工具共享计数对应的两个 guard 确实等价。它只体现同一个计数更新事件，**尚未校准可达，也不能代表三类独立复杂事件**。
- **Flash arbiter**：`StHw` 与 `HwSel`、`SwSel` 与对应输出选择确实等价，但 8 周期 reset/quiescence inventory 已覆盖这些位置。

| 模块 | line covered/total | branch | expr | toggle | 原始总分母 |
| --- | ---: | ---: | ---: | ---: | ---: |
| AXI DMA write | 65/81 | 11/96 | 17/129 | 27/3932 | 4238 |
| Flash program | 11/16 | 18/36 | 35/112 | 137/1140 | 1304 |
| Flash arbiter | 14/19 | 6/14 | 6/12 | 153/858 | 903 |

这是 **8 周期 reset inventory**，包含初始化／复位活动、排除 testbench，保留真实子模块计数。它不是合法协议校准、JSON 实验 driver 或功能通过率；例如空闲时的高 line 百分比不代表完成过 DMA 事务。Flash seed 的全零输入也不替代后续合法枚举／MuBi 输入约束。

三个范围均通过 Slang、Verilator、Yosys。DMA 原版 Icarus 编译通过，两个 Flash 原版 Icarus 编译仍因包／SystemVerilog 支持失败，不能归为 DUT 错误。本轮没有声称其双仿真器功能一致。

## 检查与复现

[validation.json](../results/natural_write_screen_20261104/validation.json) 记录 **35/35** 测试通过：8 项新增层级／guard／映射控制、7 项原 natural integration、20 项 I2C 回归。负向控制包括接错子模块端口、错配内存读地址、时钟反相、越界选择域及错位源锚点。

从头重跑的一键命令完成于 21.09 秒；三个模块的**每个原始计数身份和 hits、分母、等价查询状态及筛选结果全部一致**。主预检是 3 次编译、3 次仿真、24 周期；独立复跑额外同样各 3 次和 24 周期，总计 6 次候选仿真、48 周期。所有模型调用与 API 费用均为 0。测试夹具单独保存在测试日志，未混作候选试跑。首次交互式证明没有完整 wall-time 记录；复跑日志提供端到端计时。

工具实测：Python 3.13.9、Verilator 5.050、Icarus 12.0、Slang 12.1.0+42710c788、Yosys 0.70+309 bd3168b1a、Z3 5.1.0、Rust 1.99.0、egg 0.11.0。DUT、driver、配置、证明输入和脚本哈希见 JSON 证据。

在仓库根目录运行；必须使用新的输出目录，避免覆盖证据：

```sh
.venv/bin/python scripts/fetch_flash_closure.py --manifest configs/flash_write_sources_manifest.json
.venv/bin/python scripts/run_natural_write_screen.py --output build/natural_write_reproduce_new
.venv/bin/python -m unittest discover -s tests -p 'test_write_hierarchy.py' -v
```

AXI 源文件必须先位于 `third_party/verilog_axi_candidate/rtl/axi_dma_wr.v`，版本和 SHA-256 由配置校验；Flash fetcher 校验每个 Git blob 和 SHA-256，拒绝覆盖不同内容。现有 OSS CAD Suite、Verilator、Icarus、Z3 和 `egraph/target/debug/guard_proofs` 是复现依赖。

## 后续决策

本轮只完成必要的静态筛选，三个范围均不进入下一阶段；无需申请 API key。不能为了通过门槛，把 Flash 一个计数更新事件拆成三类事件、拼接没有真实连接的顶层，或缩短 B 预算。

下一次应先单独登记**真实多模块集成范围**或其他自然 IP，复用本次实例别名适配，仍在任何 B/C 结果之前筛选。必须先有足量不同源 guard 组，再由 Claude 仅依据固定规格／接口编写 checker，GPT/Codex 建立固定 JSON driver 和私有校准。通过正负控制、合法多步可达性和仿真器依赖门槛后，才使用原预算进行独立 B 试跑；C 结果不参与选题。
