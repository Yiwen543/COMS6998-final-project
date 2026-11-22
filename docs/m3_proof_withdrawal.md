# Controller 单条证书撤回实验

## 固定实验方案

使用 Controller 原始的 148 个 guard、281 条已有 QF_BV 规则和 fast-v1 的全部 70 条已发表证明边。按归档顺序，每次仅撤回一条规则，下一次从完整输入重新开始。保留事件、原始事件、实例、目标 ID、六条内建布尔规则和饱和上限。每次比较全新进程运行的 v1 spanning 与 M3 indexed 的完整输出，仅排除时间字段，再独立逐步重放证明。该干预改变允许使用的等式证据；RTL 和证书所表达的布尔函数始终相同。

逐边记录旧证明原样重放、撤回引起的失效、用剩余证据可重建的证明，以及饱和后仍缺少证据的结论。普通方法可在同事件的原始 AST 完整端点等式图上沿两个方向寻找证书链。另复用 Controller 既有的结构归一化作更强对照。前者保留可追溯证书路径，后者报告能够识别的等价性。所有 281 个场景都保留，运行耗时不作为评价指标。

## 结果

70 条原证明共用到 50 个不同的专用规则名。撤回另外 231 条中的任意**一条**，这 70 条证明都可以原样通过。剩下 50 个场景各影响 1–7 条证明。影响最多的是 `qfbv-g59-g83`，原来使用它的 7 条旧证明都能用其他已认证等式重建。这些数字描述各自独立的单条撤回；多条同时撤回可能破坏同一条替代路径。[逐场景记录](../results/milestone3/proof-withdrawal/scenarios.jsonl)

| 70 条原证明 × 281 个撤回场景 | 边与场景组合数 | 含此结果的场景数 |
|---|---:|---:|
| 旧文本仍逐步通过 | 19,599 | 281 |
| 旧文本引用已撤回规则、检查失败 | 71 | 50 |
| 上述失效组合中，以剩余规则重建成功 | 57 | 36 |
| 上述失效组合中，剩余规则饱和后仍无证明 | 14 | 14 |

**一次具体的修复。** `qfbv-g18-g23` 被撤回后，原来从 `g18` 到 `g23` 的直接证明缺少前提。剩余的 `qfbv-g18-g37` 允许从 `g18` 到 `g37`，再反向使用 `qfbv-g23-g37` 即可到 `g23`。独立程序逐步检查替换位置、方向、规则名、上下文和端点。普通图搜索也找到这两条等式。相对地，撤回 `qfbv-g1-g3` 后，剩余规则无法重建旧的 `g1` 到 `g3` 证明；在全部场景评分完成后，另对 14 个缺证目标对逐对查询原始、未改动的位向量模型。每对的 XOR 反例查询都返回 UNSAT；这些补充结果没有回填进 egg 的规则库。[修复前后完整证明](../results/milestone3/proof-withdrawal/repair-example.json) · [14 对独立查询结果](../results/milestone3/proof-withdrawal/unresolved-qfbv.json) · [原始 QF_BV 逐规则记录](../results/milestone3/controller/certificate.json)

**与普通方法的差别。** 输入等式图只将同一归档事件内的完整 AST 端点连接起来，每条边保留规则名和使用方向。相同 AST 的不同目标 ID 可以引用同一顶点，同时保留各自的原始身份。它独立找到了同样 57 个失效组合的替代路径。既有结构归一化还会对六条布尔规则、子树和等价代表式做固定点简化；它在同样 57 个组合上识别出等价。该算法只输出相等的键，没有输出替代证明文本。全部场景中，v1 与 indexed 的新饱和结果逐字段一致（忽略耗时字段）；独立证明检查器重放了 19,656 条新边、19,963 个具名改写步。每个场景都检查了原来的全部 70 个目标对，原证明留下的可核查依赖可以具体定位失效文本。此工作负载里未观察到 egg 独有的修复，也没有测量 RTL 回放或求解器调用节省。[汇总](../results/milestone3/proof-withdrawal/summary.json)

**事件与实例的范围。** 每个目标保留归档 ID、规范事件、实例路径及原始全限定事件。归档的 70 条证明都在同一规范事件内讨论布尔项；其中 34 条的两个端点来自不同实例，20 条的原始事件标签也不同。这样的边可以形成项等价证据。实际 RTL 采样、覆盖归属和求解复用仍须遵守独立的实例与原始事件条件。在 36 条同实例原证明上，10,080 个组合可保留、22 个可修复、14 个在撤回后缺证。未运行新的 RTL、未注入故障，也未生成否定原有等价性的反例。[原始逐边 ID、上下文及依赖](../results/milestone3/proof-withdrawal/claims.json) · [验证工作负载的分组条件](../scripts/benchmark_m3_controller.py)

## 环境、脚本与复现

按主实验指南安装 Python 3.12、Rust/Cargo 1.90、锁定的 egg 0.11 以及 Z3 4.16；主实验的一键脚本会在两个独立目录内编译 release 二进制。这里只用 Rust 引擎、Python 检查器和 Z3 命令行，无需启动仿真器。以下从仓库根目录运行；已有固定 Controller 数据时可跳过第一条下载命令。[环境搭建](milestone3.md)

```bash
python3 scripts/m3_controller_replay.py --fetch /tmp/coms6998-ctrl-withdrawal-fixture
run=/tmp/coms6998-m3-run1
python3 scripts/m3_controller_withdrawal.py \
  --screen-dir /tmp/coms6998-ctrl-withdrawal-fixture/qualification/typed-v5/screen \
  --baseline-binary "$run/build/v1-target/release/guard_proofs_fast" \
  --binary "$run/build/m3-target/release/guard_proofs_fast" \
  --output /tmp/coms6998-ctrl-withdrawal-results
```

- `m3_controller_replay.py --fetch` 从固定提交下载 Controller 资料并校验哈希。输入中的 148 个目标与 281 条规则沿用原 ID、顺序和上下文。
- `m3_controller_withdrawal.py` 调用 `m3_controller_certificates.py`，核对输入、查询及顺序三份文件的 SHA-256，重新用 Z3 确认 281 条原始 QF_BV 规则。每次取不同的 280 条规则，分别在独立进程运行两个引擎，验证它们报告正确模式、均饱和且输出相符。遍历两种等式图时允许反向使用已验证的等式。旧证明的每一步都会在新的允许规则集合上再次检查；相同原式的目标不因归一化而丢失身份。
- `m3_proof_dependencies.py` 独立解析 flat proof，将规则逐步应用于指定子项并检查终点；另检查所报告的最终等价类及事件内证明连通性。`benchmark_m3_controller.py` 提供普通结构归一化。不存在可用证明路径时，报告会保留该目标和未决状态。[证明检查器](../scripts/m3_proof_dependencies.py) · [实验驱动](../scripts/m3_controller_withdrawal.py)
- `claims-by-withdrawal.jsonl.gz` 解压后有 281 个 JSON 行，每行有全体 70 条原结论的状态、显式规则图路径、结构方法的结果，以及修复时使用的每条新证明边和方向。`claim` 对应 `claims.json` 的索引；`repair_path` 的边编号对应同一场景的 `repair_edges`。`scenarios.jsonl` 另外记录每次新图的 SHA-256、证明边数和步数，`summary.json` 记录两套二进制哈希和总数。[逐边记录](../results/milestone3/proof-withdrawal/claims-by-withdrawal.jsonl.gz)
