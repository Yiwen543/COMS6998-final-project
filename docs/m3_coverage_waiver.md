# 一条原始 RTL 覆盖豁免，以及使它失效的改动

八路 arbiter 在定向回归后还剩一个零命中的分支：`fixed_priority_arbiter.sv` 第 30 行最后一个三目表达式的 `cond_else`。这次给该点生成了可重验的豁免证书。候选豁免只增加“在此模型下不可达”的解释，原始定向分支覆盖仍为 **17/18**。改一行 RTL 后，同一计数点可以触达，旧证书被拒绝。Z3 找到的输入随后在真实 Verilator 回放中命中了该点。[源码](../examples/arbiter/rtl/fixed_priority_arbiter.sv) · [证书](../results/milestone3/coverage-waiver/waiver.json) · [实验结果](../results/milestone3/coverage-waiver/summary.json)

## 证明对象和对照方法

源过程在 `posedge clk or posedge reset` 激活。要进入该 `else`，本次激活必须满足复位无效、进入 override 路径，且从位 0 到位 7 的所有条件均为假。源位宽为 reset 1 位、req 和 override 各 8 位。QF_BV 模型允许三个端口的所有二态取值，无额外协议约束。可达性只涉及这次采样，无需假设过去输入、FIFO 状态或公平性。程序校验原 RTL 的 SHA-256，逐项匹配该行所在的复位结构、外层判别和八层三目选择，并绑定具体 Verilator `page`、层级、行列、计数类型。适用范围为该模型和该计数器。[实现](../scripts/m3_coverage_waiver.py)

| 同一个判定任务 | 原版 | 修改后 |
|---|---|---|
| 普通基线。对完整源条件直接询问 Z3 是否存在输入 | UNSAT | SAT |
| 先验证八个位的 OR 等价于 unsigned 总线非零，再用 egg 把完整 guard 中的位 OR 改成 `override_any`，对替代式询问 Z3 | UNSAT | SAT |
| Z3 给出的修改后输入，在两版上各做一次定向回放 | 目标 0 次 | 目标 1 次 |

命名规则 `override-nonzero` 的 XOR 查询在两版均为 UNSAT。两版均执行真实的 indexed egg，检查饱和、不同初始类、最终同类，再逐步核对具名改写的方向、两个端点和外围上下文。原版替代式含有 `override_any && !override_any`。普通 Z3 也能直接判定该分支不可达。egg 在这里提供可定位到具名关系的证明，本例没有测到新增的验证覆盖或求解优势。[原版完整证明](../results/milestone3/coverage-waiver/original/egg-proof.json) · [原版直接查询](../results/milestone3/coverage-waiver/original/direct.smt2)

## 改一行 RTL 后

在临时副本中，把外层的 `if (priority_override != 8'b00000000)` 改为 `if ((priority_override != 8'b00000000) || req[7])`，保留原来的位选择逻辑、测试台与激励。原证书的 RTL 哈希和完整激活条件同时失配，程序在对修改版本重新求解前拒绝复用。八个位 OR 的局部等价关系依然成立，但新替代式允许 `req[7]=1` 时总线为零。修改版本对未经约束的完整输入求解得到 `reset=0, req=0x80, priority_override=0x00`。[修改版本查询及求解器返回](../results/milestone3/coverage-waiver/edited/direct.z3)

在每版各编译一次 DUT，分别回放原有 4 步种子，以及同一组种子加这个见证，合计 4 次模拟和 18 个 checker 采样边沿。原版两次的目标命中均为 0，原始分支覆盖均为 3/18。修改版种子为 3/18、目标 0 次，加入见证后分支为 11/18、目标 1 次，同时 checker 记录 1 次功能错误。修改导致表达式计数器总数从 2 增为 5，两版均保留自身的完整原始分母。以上短回放与原项目 17/18 的完整定向回归使用不同刺激。[修改版回放日志](../results/milestone3/coverage-waiver/edited/witness.log) · [修改版原始计数](../results/milestone3/coverage-waiver/edited/witness.dat)

## 环境与复现

使用主实验的 Python、Verilator 5.050、Z3 4.16.0、Rust 和 C++ 环境。脚本仅需 Python 标准库。它从工作区读取原始 DUT，在临时目录分别构建两版，保存原始计数、日志、见证、SMT-LIB 输入、Z3 回答和 egg 证明。源 DUT 保持原样。[环境安装](milestone3.md#环境与一键复现)

```bash
CARGO_TARGET_DIR=/tmp/m3-waiver-rust cargo build --locked --release \
    --manifest-path egraph/Cargo.toml --bin guard_proofs_fast
python3 scripts/m3_coverage_waiver.py --binary /tmp/m3-waiver-rust/release/guard_proofs_fast \
    --output /tmp/m3-waiver-new
python3 scripts/m3_coverage_waiver.py --check-waiver /tmp/m3-waiver-new/waiver.json \
    --rtl examples/arbiter/rtl/fixed_priority_arbiter.sv \
    --coverage /tmp/m3-waiver-new/original/witness.dat
```

`--check-waiver` 读取受信的签发结果、同次编译的 RTL 和原始覆盖文件，核对 8 份证据的哈希、3 个完整 SMT 查询及其 UNSAT 返回、原/替代 guard 的嵌套具名改写、RTL 绑定和非负的原始命中数。单独的 Verilator `.dat` 不包含 RTL 哈希，检查时由调用者提供同次编译的 RTL 与覆盖文件；完整实验在同一临时目录内编译并采集。只要计数达到 1 次或绑定发生变化，就返回非零。需要独立重建签发依据时，运行上一条完整实验命令。对 X/Z、改动后的工具插桩或其他 DUT，应重新建立语义模型和计数器映射。
