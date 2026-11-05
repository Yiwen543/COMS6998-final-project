# AXI DMA / Flash 读子模块：语义、映射与依赖检查

日期：2026-11-04。开发基线 commit：`50d7ee83d61989017e28e981420cd58f4c5f0787`。

本轮修复了前一版预检的主要工具缺口，但两个**固定读子模块**仍未通过动态等价目标筛选，因而没有开始 Claude checker 或 GPT 的 B 开发试跑。这个结论不等同于“B 已饱和”，也不代表完整 AXI DMA 或完整 Flash Controller 均不适合研究。

## 实际检查范围与结果

| 项目 | AXI DMA read engine | OpenTitan Flash read controller |
| --- | --- | --- |
| 固定顶层 | `axi_dma_rd` | `flash_ctrl_rd`，EnglishBreakfast 生成版本 |
| 源码版本 | `516bd5dadc3365b7f9e225d2af8fe0b8d804fe53` | `0ea5236fe749e70ba18f56ba19c4be982ef46da7` |
| 参数 | ENABLE_UNALIGNED=1，其余原默认值 | 原默认参数，真实 generic primitives |
| 原始源码前端 | Slang、Verilator、Icarus、Yosys 均通过 | Slang、Verilator、Yosys 通过；Icarus 原始 SV 仍不支持 |
| 组合定义独立交叉检查 | 68/68 通过 | 13/13 通过 |
| 并行 mux one-hot-or-zero 检查 | 13/13 通过 | 3/3 通过 |
| 支持的完整激活 guard | 68/68 | 29/29 |
| 精确原始计数映射 | 64/68 | 25/29 |
| 保留的 DUT 原始覆盖点 | 3,404 | 1,592，含真实子模块 |
| seed 未覆盖、可满足、源位置不同且排除常量条件后的等价组 | **0** | **0** |
| checker / B / C / placebo 调用 | **均未开始** | **均未开始** |

本轮沿用既有“至少三组源位置不同的动态目标，其中至少两组非平凡”的筛选原则。即使有静态候选，也仍需独立 checker、合法多步可达性和 B 开发门槛；静态 SAT 本身不是时序可达性。没有根据 C 结果挑选，也没有缩短预算制造 B 的困难。新 IP 的正式实验预算尚未冻结。

## 1. 补齐了哪些语义能力

新增 `scripts/natural_semantics.py`，没有修改旧冻结适配器：

- 对 `always @*` 建立静态组合分析，保留其原始种类；没有改写源 RTL，也不声称它与 `always_comb` 的仿真调度完全相同。
- 移位保留左操作数宽度、符号、逻辑/算术语义及自确定的移位量宽度；大移位量不能通过截断变成小移位量。
- 支持有界常量切片、非零低位索引、拼接、复制和 packed struct 字段更新。未支持的升序索引、动态索引等仍显式拒绝。
- 组合过程中的每个谓词使用**该语句位置**的 SSA 环境。例如先执行 `n=x+1` 或某个分支内的 `n=x+2`，随后 `if(n==0)` 必须使用相应版本，不能误用旧状态或过程结束时的值。
- if/else 的相反极性、外层 guard、case 的先匹配优先级、源位置、时钟边沿和复位上下文继续保留。不同分支的环境不互相污染；潜在锁存器不被假设成纯组合逻辑。

`natural_netlist_proof.py` 用另一套 Yosys cell 编码交叉检查 Slang SSA 定义。两套表达式编码不同，但**共享 Slang 前端**，因此不是完全独立的两个 RTL 解析器。FF Q 和 memory-read 结果被作为任意当前值；没有使用状态不变量、合法总线约束或复位可达性来“帮助”证明。memory read cut 不构成存储器正确性证明。

Flash 初次使用未经清理的 Yosys IR 时，冗余 mux 依赖使递归编码检测到组合环。保留此失败记录后，使用 `opt_expr; opt_clean` 消除冗余组合 mux；随后 13 个定义全部通过。原始 RTL、寄存器边沿与复位语义没有改变。这不是已发现真实 DUT 组合环的结论。

## 2. Flash 的真实依赖已经闭合

通过官方 GitHub 连接取得缺失文件，并把 **29 个文件逐个与固定 Git tree 的 blob ID 和 SHA-256 核对**。保留原始 `prim_count`、`prim_flop`、`tlul_data_integ_enc`、SECDED 编码器以及所需 package；没有替换成常量或简化 stub。

EnglishBreakfast 的 `top_pkg.core` 明确依赖 Earlgrey 的 `top_pkg`，所以这项 package 复用来自上游构建规则，而非我们猜测。其余关键闭合包括 Flash register package、CSRNG/entropy/EDN、TLUL、JTAG、MuBi、计数器 package 和 assertion/flop 宏。

公开[Flash 规格](https://opentitan.org/book/hw/top_earlgrey/ip_autogen/flash_ctrl/doc/theory_of_operation.html)描述了 FIFO 流控、错误处理及请求仲裁；但本轮仅编译和提取固定 EnglishBreakfast **read 子模块**，没有宣称验证整个规格或完整控制器。

Icarus 12.0 仍拒绝上游 package 中的 `inside` 等 SystemVerilog 语法。这是工具兼容性问题，不是 DUT 错误。另做了一项明确标注的有限补充：Yosys 输出 lowered Verilog 后交给 Icarus，和原始 SV 的 Verilator 结果比较。8 个复位/空闲周期的全部顶层公共端口一致。它不是原始 SV 的 Icarus 编译通过，也不是完整顺序等价证明。覆盖分母始终来自原始 RTL 的 Verilator，未混入 lowered 源码的覆盖。

`scripts/fetch_flash_closure.py` 提供无 API key 的可重复下载/校验入口；若本地文件与固定 hash 不同，会拒绝覆盖。

## 3. 原始覆盖和映射没有合并

两个新 harness 只执行 8 周期复位/空闲种子，用于建立原始计数清单。它们**不是规格 checker、完整 JSON 事务 driver，也不是多步功能校准**。

| DUT 原始计数类型 | AXI DMA | Flash，包括子模块 |
| --- | ---: | ---: |
| Line | 67 | 17 |
| Branch | 60 | 40 |
| Expression | 67 | 119 |
| Toggle | 3,210 | 1,416 |
| 合计 | 3,404 | 1,592 |

保留每个点的文件、行、列、计数种类、分支极性、实例层级和 hits。TB 不计入，初始化和复位活动计入。Line 指 Verilator instrumentation point，不等于物理源码行数。子模块计数全部保留，但本轮 **guard 提取仍只覆盖顶层模块**；没有把子模块计数当成已证明的层级 guard。

AXI DMA 的四个未映射项是两个参数三元表达式极性及两个 else-if 补极性；Flash 的四个未映射项位于 else-if 链。当前没有可唯一对应的原始计数，因此保留 unresolved。没有用相邻行、整条 if 的计数或多个计数之和替代。详见各候选的 `mapping-disposition.json` 和 `source-map.csv`。这些位置的语义表达式已支持，但“有语义 guard”不保证模拟器为其提供独立计数。

## 4. 为什么没有继续花 API 预算

AXI DMA：1,666 次同上下文 pair 查询得到 65 个 UNSAT、1,601 个 SAT、0 unknown。57 对不同形式的完整表达式进入经证明的 ground rules，再由真正的 Rust `egg` 有界饱和组织等价组。多数关系来自固定参数开关或不可满足分支；其余重复复位条件已由种子覆盖。例如 descriptor 握手与其内部 `ENABLE_UNALIGNED` 分支在此参数下等价，但后者是常量开关，不是额外的动态事件。

Flash read：203 次 pair 查询得到 6 个 UNSAT、197 个 SAT、0 unknown。等价项主要是重复的复位极性；没有不同形式的非平凡 ground rule。不能把正常读取、错误填充、暂停恢复等**不同事件**因为名字相关就放进同一 E-class。

因此两个范围的合格静态动态组均为零，尚未满足开始多步可达性和 B 筛选的必要条件。没有为其编写新 Claude checker，也没有调用 GPT 生成刺激。这个否定结果是候选筛选证据，不能转换成 C/B 性能结果。

下一次有意义的范围扩展应预先记录，例如原始 `axi_dma_wr`、Flash `prog/arb` 或包含真实父子模块连接的协议范围；它们仍分别属于现有两个 IP 家族，不能另算独立 IP。必须先实现并验证层级端口别名和路径 guard，再观察是否有三类不同的多步事件各自对应重复动态谓词。增加文件数量、参数常量点或复位重复点不满足门槛。只有通过后，才让 Claude 按公开规格建立 checker，GPT 负责固定 driver/刺激，并冻结预算后跑独立 B。

## 验证、成本与限制

- 新增 7 项测试通过，包括 450 个移位/位宽/符号的 Z3 检查，SSA 语句位置与兄弟分支隔离、packed 字段、非零索引、锁存器拒绝、错误 netlist 的负控制及精确映射拒绝回退。
- 原有 20 项 I2C 回归检查通过，旧冻结 hash 未改变。
- 两次原始覆盖 inventory + 两次 Flash 翻译交叉仿真，共 4 次实际仿真、32 周期。这是集成工作量，不是 LLM Token ROI。
- 12 次前端调用保留了 5 次失败：第一次 Flash 缺宏 include 的四个前端失败，以及闭合后的 Icarus 兼容性失败。成功编译不能抹掉这些失败尝试。
- 本轮模型/API 调用为零、API 费用为零，没有请求或使用暂存密钥。
- 工具：Slang 12.1.0+42710c788、Yosys 0.70+309/bd3168b1a、Z3 5.1.0、Verilator 5.050、Icarus 12.0、Rust 1.99.0、egg 0.11.0。
- 所有等价证明限二值组合语义；没有四态、全 IP 规范、存储器功能或多周期行为的完整证明。

## 可重复执行

在仓库根目录使用新的输出目录；以下命令不调用 LLM：

```sh
.venv/bin/python scripts/fetch_flash_closure.py
.venv/bin/python -m unittest discover -s tests -p 'test_natural_ip_integration.py' -v
.venv/bin/python -m unittest discover -s tests -p 'test_i2c*.py' -v

.venv/bin/python scripts/probe_natural_frontends.py --candidate axi_dma_rd --output build/axi-next
.venv/bin/python scripts/natural_netlist_proof.py --ast build/axi-next/ast.json --netlist build/axi-next/flat.json --top axi_dma_rd --output build/axi-next/netlist-proof
.venv/bin/python scripts/inventory_natural_coverage.py --candidate axi_dma_rd --frontend build/axi-next --output build/axi-next/inventory
.venv/bin/python scripts/screen_natural_semantics.py --top axi_dma_rd --base build/axi-next --output build/axi-next/screen

.venv/bin/python scripts/probe_natural_frontends.py --candidate flash_ctrl_rd --output build/flash-next
.venv/bin/python scripts/natural_netlist_proof.py --ast build/flash-next/ast.json --netlist build/flash-next/flat-simplified.json --top flash_ctrl_rd --output build/flash-next/netlist-proof
.venv/bin/python scripts/inventory_natural_coverage.py --candidate flash_ctrl_rd --frontend build/flash-next --output build/flash-next/inventory
.venv/bin/python scripts/screen_natural_semantics.py --top flash_ctrl_rd --base build/flash-next --output build/flash-next/screen
.venv/bin/python scripts/check_flash_lowered_sim.py --base build/flash-next --output build/flash-lowered-check
```

复现 Flash 前端时，仍应看到原始 Icarus 不支持的记录，不能把它预期为全部成功。最终证据位于 `results/natural_ip_integration_20261104/`：`decision.json`、`validation.json`、`flash-sources.json`，以及两个候选的 `netlist-proof/`、`screen/`、`inventory/`。部分失败编译生成的大型不完整 AST 已记录 hash 后删除；失败日志、输入与最终有效 AST 保留。
