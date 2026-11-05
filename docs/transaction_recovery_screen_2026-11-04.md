# Transaction arbitration and recovery: prospective public-IP screen — 4 November 2026

本轮实际登记、编译并分析了三个公开原版多模块 IP；没有候选通过全部离线门槛，因此**没有启动 Claude checker、B 或 C**。这不是新的 B/C 性能结果，也不支持“C 无效”的结论。

## Scope registered before screening

登记文件：[transaction_recovery_screen_v1.json](../configs/transaction_recovery_screen_v1.json)，SHA-256 `efa89c6703c8f0281355e6eae8004e05fb265dd85c0dd4ac5f077daf4ecf4393`。登记先于本轮 elaboration、原始计数、证明及模型调用。基线仓库提交为 `50d7ee83d61989017e28e981420cd58f4c5f0787`，工作区包含尚未提交的历史及本轮工作；不能把该提交声称为本轮实现的完整快照。实现与产物另存 SHA-256。

| 顺序 / 原版 IP | 固定范围 | 预登记多步事件 |
|---|---|---|
| `wbsafety` | ZipCPU Wishbone firewall + 原版 skidbuffer；AW=8、DW=32、MAX_DEPTH=8、timeout=12、自复位开启 | 下游 stall 超时后隔离/重启；已接受请求无响应后恢复；异常下游响应后隔离/恢复 |
| `wbxbar` | 原版 2-master/2-slave Wishbone crossbar + address decoder + skidbuffer；AW=8、DW=32、timeout=16、双缓冲开启 | 竞争资源等待 outstanding 清空再交接；超时中止后复用；master 中止后新 owner 获取资源 |
| `axis_ram_switch` | 原版 2×2 packet RAM switch + 仲裁器、优先编码器、stream adapter；8-bit 数据、FIFO_DEPTH=32、CMD_FIFO_DEPTH=4 | 同一输出的帧仲裁/交接；RAM/command 容量阻塞后排空再接收；坏帧/超长帧丢弃后资源释放 |

Wishbone 两项固定在 `ZipCPU/wb2axip@2e8d3bc2d26ddc33d1881022a2a2b9d3f0c16b9b`；RAM switch 固定在 `alexforencich/verilog-axis@48ff7a7e2ef782cf778d47910cf85835c64b1bce`。源文件 SHA-256、Git blob、参数、接口、时钟/复位和 ordinary 输入政策均在登记文件中。没有改 DUT、插入复制 guard 或新增 DUT 覆盖点。

两颗 Wishbone IP 共享上游及 skidbuffer，不能计为两个独立来源。RAM switch 是不同功能设计，但属于前面已使用过的 verilog-axis 家族，也不能声称为完全未见仓库。上游 verilog-axis 已标注由 Taxi 接替；本轮固定旧版以复现。上游 formal 验证的宣传不等于本项目已复现其证明。

## Unchanged gates, budget and roles

- 至少 3 组源位置不同的动态等价 guard，其中至少 2 组非平凡等价；每组至少两个映射明确、共享 seed 后为零的真实源计数。
- 普通流量 union 必须保持所有选定目标为零。普通流量包括边界长度、正常释放/重获、prompt ACK/ERR 等；不能故意把这些正常行为排除以制造“难题”。具体政策在登记文件中。
- 至少 3 类不同事件产生可区分的目标增量；独立 checker 下 384 个新物理周期内可达，且 prefix / 移除前提或恢复动作的控制不命中。一次共享 stall 不能算三类恢复事件。有限控制未命中不等于形式不可达。
- 仍是 **3 次独立重复 × 6 轮 × 每轮最多 64 个新周期**，共享 seed 为 8 周期。GPT-6.1-Sol、low reasoning、输入 32,000 / 输出 16,384 token cap、120 秒 timeout、最多 1 次重试。没有观察 C 后改目标或缩减预算。
- B 门槛仍要求至少两次重复在首轮后剩余至少两组未命中，至少两次随后取得进展，全部重复完整且输入合法。只有通过后才另行冻结正式 A/B/C/按实际 token 匹配的 placebo。
- Claude 独立依据公开规格编写 checker；GPT/Codex 负责固定 driver 和刺激。作者不拿 RTL、私有校准序列或 B/C 结果来推导 golden output。当前尚未到 commissioning checker 的门槛。

## What was implemented and verified

复用既有 Slang → typed guards → 独立 Yosys cell 编码 → Z3 → Rust `egg` → 原始源计数路径；没有重建仿真环境，也没有改旧冻结脚本。

新增 [transaction_semantics.py](../scripts/transaction_semantics.py) 解决当前真实层级设计暴露的适配问题：

1. 复用 Slang 子模块 AST 时，展开实例并重新绑定该实例的精确端口。保留实例限定名，不把两个子模块状态或 memory read 混为一个变量。
2. 对 Yosys 实际展开为 wire 的 unpacked array，保留声明方向、元素宽度和位偏移；真正 memory 仍保留独立 current-read cut，并检查精确 memory instance、源位置和读地址。
3. 合并完全赋值、互不重叠的连续/组合过程位片。重叠、缺失位、latch 或组合/时序混合驱动不自动补零。
4. 对动态切片，在 AST 和独立 netlist 两侧分别证明索引界限。保留符号；负的有符号索引不能当成小的无符号索引。未支持的升序 packed 动态索引明确拒绝，不猜测位序。
5. `$print` 仅在全部端口为输入、不会驱动逻辑时作为观察节点忽略；不是任意删除不支持的 cell。

这条验证路径确实拦下过数组位序、缓存实例端口以及同源不同实例 memory cut 混淆导致的错误。失败的 v1…v7 产物保留为开发记录；当前可重放结论以 `*-final` 为准。旧开发记录的代码哈希可能已不匹配当前修订代码，不能当作当前认证。

新增 [transaction_counter_mapping.py](../scripts/transaction_counter_mapping.py) 从 Verilator 生成的 C++ 插桩中恢复精确实例成员，并与 raw `.dat` 的 file/line/column/**page specialization**/outcome/span/FSM metadata 对齐。Verilator 的 `*_arb_inst` 与 `genblk*_arb_inst` 只是合并后的显示名称；本轮不按通配符猜实例归属。一个共享计数必须收集齐对应实例的 guard，再取 OR；缺失成员保持 unresolved。不会凭等价关系转移命中，也不会拆出不存在的原始计数。

`egg` 仍是实际有界等式饱和：最多 20 iterations、20,000 nodes、5 秒，使用已有六条已验证 Boolean rewrite 和本次 Z3 证明的 ground equalities。保存原始谓词、完整激活条件、source mappings、pair SMT、证明状态、导入规则及 explanation。两态语义；时钟/复位上下文保持独立。寄存器当前值和 memory read 为自由状态切点；不假设可达状态不变量。

**证明局限：** AST 与 Yosys 路径共享 Slang 前端，独立的是定义编码/等价检查，不是完全独立解析器。组合定义证明不是完整 IP 功能证明、四态证明或多步事件可达性证明。

## Actual final results

| 候选 | 定义/地址证明 | 映射后的有效项 / 未解决项 | 原始 DUT 分母 | 合格静态组 / 非平凡组 | 当前结论 |
|---|---:|---:|---:|---:|---|
| `wbsafety` | 19/19 mismatch UNSAT | 61 / 9 | 1,099 | 0 / 0 | 当前配置静态目标不足 |
| `wbxbar` | 108/108 已构造检查 UNSAT，但存在未定义组合量 `m_stall` | 未进入源计数阶段 | 未测量 | 未测量 | 语义门槛阻塞，不能宣称目标不足 |
| `axis_ram_switch` | 512/512 mismatch UNSAT | 91 / 4 | 5,044 | 2 / 0 | 当前配置静态目标不足 |

这里“有效项”是共享物理计数合并后的 guard 项，不是整个 RTL 的代码行数。RAM switch 从 198 个展开目标合并为 95 项；91 项映射成功。改进前同一设计只有 62 项映射成功，但旧版聚合项总数不同，不能把它们当成相同分母的覆盖率比较。

RAM switch 留下的两组是 `axis_ram_switch.v:1016` 与 `:1023` 的 `len_reg == 0` 及其反极性。它们是同一条件的重复使用，没有获得新的非平凡关系；正/反极性也不能被当成三个不同恢复事件。没有用单纯源码体量支持进入模型试跑。

Crossbar 的具体阻塞在 `wbxbar.v:884–894` 的 `m_stall` 定义：`request[N][mindex[N]]` 的候选状态索引不能在当前“寄存器值自由、无可达性假设”的边界内证明总是合法。Z3 对越界查询返回 SAT，所以相应定义未进入认证集。108 个已支持检查通过不代表剩余定义自动通过；当前不是已确认 DUT 缺陷。需要另行登记并证明状态约束，不能凭“正常运行应该不会发生”缩窄位宽或去掉非法索引。

有 15 个 firewall、5 个 RAM switch 的 untimed procedure 被明确排除在受支持谓词提取之外；已支持目标的 typed conversion 没有额外失败。9/4 个 unresolved source mappings 主要为不存在唯一精确反极性插桩，仍保留在原始分母。**所有普通流量筛除、多步校准和 checker 验证均未执行**：静态门槛已失败/阻塞。不能把未执行的阶段标成通过，也不能声称这批 IP 已证明普通操作难以覆盖。

共享 8 周期 reset/quiescence 的原始计数仅用于 inventory，不是 pilot 成绩：

| IP | branch | expression | line points | toggle transitions |
|---|---:|---:|---:|---:|
| wbsafety | 28/58 | 58/151 | 38/50 | 15/840 |
| axis_ram_switch | 46/116 | 68/184 | 92/112 | 56/4632 |

计数定义由 Verilator 的 `--coverage-line --coverage-toggle --coverage-expr` 决定。line 是插桩点而非所有文字行，toggle 是工具输出的位跃迁计数；TB 排除，真实子模块包含，初始化/复位活动包含，原始共享计数不拆分。

## Validation and accounting

[机器可读审计](../results/transaction_recovery_screen_20261104/validation.json) 记录最终证据、各轮失败/修订尝试、版本和命令。92 项当前产物/生成代码哈希检查通过，原 SPI checker/driver/目标/分母冻结验证通过。**31 个自动检查通过**：13 个新适配/映射测试，8 个原有 event-screen 测试，8 个 safe-driver 测试，2 个 accounting 测试。

新负向检查包括：修改输出位绑定必须产生 SAT mismatch；两个同源 memory instance 不得合并；索引越界和有符号负数必须拒绝；重叠 wildcard 不得导致错误归属；缺失共享计数成员不得生成完整 OR guard；原始 identity 冲突必须阻断映射。

全部 18 次候选筛选尝试均保留：72 次 frontend lint/elaboration 调用，0 次 frontend 失败；7 次覆盖 inventory 编译、7 次仿真、共 56 个 reset/quiescence 周期。inventory 编译累计 27.90 秒，仿真累计 1.39 秒；筛选过程记录的 elapsed 累加为 74.68 秒。部分过程并行，后者不是研究工作的端到端 wall time。单元 fixture 的编译/证明属于回归检查，不计为 DUT pilot。**模型调用 0、API token 0、API 费用 $0**。

版本：Python 3.13.9；Verilator 5.050；Icarus 12.0；Yosys 0.70+309 (`bd3168b1a`)；Slang 12.1.0+42710c788；Z3 5.1.0；Rust/Cargo 1.99.0；egg 0.11.0。精确版本字符串和 egg 二进制哈希见审计 JSON。

## Reproduce

在仓库根目录，先确认第三方 checkout 处于上述固定 revision。依赖源哈希和 Git blobs 不符时 runner 会停止。使用新的输出目录，防止覆写历史证据：

```sh
.venv/bin/python scripts/screen_transaction_recovery.py --top wbsafety --output build/reproduce-transaction/wbsafety
.venv/bin/python scripts/screen_transaction_recovery.py --array-view --top wbxbar --output build/reproduce-transaction/wbxbar
.venv/bin/python scripts/screen_transaction_recovery.py --array-view --top axis_ram_switch --output build/reproduce-transaction/axis_ram_switch
.venv/bin/python -m unittest discover -s tests -p 'test_transaction*.py' -v
.venv/bin/python scripts/audit_transaction_screen.py
```

最后一条审计检查保存的 `results/.../*-final`，不是上面新复现目录。完整 frontend/proof/simulation 命令在各产物中。生成 C++ 属于 Git 忽略的 build cache；跨机器复现应先重跑 runner 再核对新的哈希，不能期待不同绝对路径的生成物字节哈希相同。

## Next decision

1. 优先针对 `wbxbar` 单独登记状态索引的有效域/guard 条件，使用原 RTL 的 reset 和转移关系做 base/inductive 检查。明确是否需要合法 Wishbone 假设及其来源。若不能证明，就保留 unresolved；不能把源码断言或随机仿真未见越界当作证明，也不能静默把当前无状态假设实验改成有状态假设实验。
2. 只有该独立证明让受支持范围扩大，才重新做等价源组筛选。普通操作 union 先行；如果只剩 ACK/empty/一般仲裁进入等共享条件，继续拒绝，不据此购买 checker 或模型调用。
3. 通过静态和普通操作门槛之后，再准备规格/接口专用包给 Claude 建立 checker。GPT 编写持有 valid/payload 至握手的固定 driver；用独立正负控制及前缀/移除前提控制验证事件。保持 384 新周期可达性上限和原 B 预算。只有此时才请求隐藏暂存 API key。
4. 若最终仍无合格组，登记新的事务协议族再筛选，保留本轮负结果。扩大表达式支持与跨 IP 样本是研究进展；“所有复杂 IP 必然产生 C 优势”不是实验前提。

## Public sources

[ZipCPU wb2axip pinned README / protocol capabilities](https://github.com/ZipCPU/wb2axip/blob/2e8d3bc2d26ddc33d1881022a2a2b9d3f0c16b9b/README.md)

[Original Wishbone firewall](https://github.com/ZipCPU/wb2axip/blob/2e8d3bc2d26ddc33d1881022a2a2b9d3f0c16b9b/rtl/wbsafety.v)

[Original Wishbone crossbar](https://github.com/ZipCPU/wb2axip/blob/2e8d3bc2d26ddc33d1881022a2a2b9d3f0c16b9b/rtl/wbxbar.v)

[verilog-axis pinned README / frame-aware RAM switch](https://github.com/alexforencich/verilog-axis/blob/48ff7a7e2ef782cf778d47910cf85835c64b1bce/README.md)

[Original AXI Stream RAM switch](https://github.com/alexforencich/verilog-axis/blob/48ff7a7e2ef782cf778d47910cf85835c64b1bce/rtl/axis_ram_switch.v)
