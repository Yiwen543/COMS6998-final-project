# Milestone 3 · egg guard 加速与 RTL 验证复现

**结论。** 当输入里有经验证的具体改写规则时，egg 可以更便宜地生成同一份证明。在 Milestone 2 的 Controller、SPI、I²C 三份原始输入上，索引匹配把引擎进程耗时分别从 61.18 降到 28.59 ms、28.21 降到 19.81 ms、9.69 降到 6.69 ms。在真正运行 RTL 的 arbiter 上，最大的提速来自**更快地找到相同的刺激向量**。使用 9 条认证规则时，保留 egg 证明的验证循环从 135.91 降到 11.49 ms。只需要复现覆盖与缺陷时，直接使用源 guard 加位并行搜索为 8.04 ms。

## 从 Milestone 2 延续了什么

开发基线是 `myzzz29/COMS6998-final-project` 的 `perf/egg-compute-fast-v1`，提交 `71e99c4cbef9768abc1b20d4d344eaee8594db59`。基线已经会按等价类复用代表式、按事件上下文提取一棵证明树、缓存完全相同的饱和结果。本次用**该提交实际编译的 spanning 二进制**作对照，两边均关闭整个结果缓存。三个历史输入取自第二个仓库固定提交 `e94172a1bd5e9b138b5fc3da01554edb3052ce52`，下载时同时校验 Git blob ID 和 SHA-256。[开发基线](https://github.com/myzzz29/COMS6998-final-project/tree/71e99c4cbef9768abc1b20d4d344eaee8594db59) · [参考仓库](https://github.com/Yiwen543/COMS6998-final-project/tree/e94172a1bd5e9b138b5fc3da01554edb3052ce52) · [三个输入的具体路径及哈希](../results/milestone3/reference-inputs/manifest.json)

M2 报告中，FIFO 的三项控制目标在两组均被命中。加入 egg 后，SMT 文本短约 29%，包含预处理与回放的耗时却从 30–32 ms 增至 235–238 ms。M3 因此分别计量引擎与完整验证循环。两仓库里可核对到三份引擎输入和旧 FIFO 材料。报告所用的 test3 FIFO 完整 runner 未取得。下面的物理回放使用开发分支原有的八路 arbiter，三个历史 IP 的新数据仅覆盖引擎阶段。历史运行的主机、测量边界与本次不同。[预先确定的实验设计及参考仓库补充](milestone3_protocol.md)

## 改了哪两处

1. **egg 的 `indexed` 模式。** 一条左侧没有模式变量的规则只匹配一个具体项。例如，八个 override 位的 OR 可改写为 `override_any`。每轮重建后，这个项至多属于一个等价类。新模式用 egg 自带的 `lookup_expr` 查找它，把匹配交给原来的改写和解释 API。含 `?a` 这类变量的规则继续用标准匹配器。两个模式采用相同规则顺序、提取代价、事件上下文、20 轮、20,000 节点和 5 秒的饱和上限。[Rust 实现](../egraph/src/bin/guard_proofs_fast.rs)
2. **精确的位并行见证搜索。** 将三个输入拼接为 17 位索引 `{reset, priority_override[7:0], req[7:0]}`，131,072 种合法赋值各占真值表的一位。布尔运算一次处理整张表，最低置位给出旧搜索顺序中的第一个合法向量，空表对应无解。`override_any` 始终由实际端口位推导。仅复用输入信号的掩码，每次实验均计入首次构建掩码的开销。`run_step1.py` 默认使用此搜索，`--witness scalar` 仍可选择旧算法。空间随输入位数指数增长，适用范围是这个固定的 17 位组合输入域。[Python 实现](../scripts/predicates.py) · [见证对照测试](../tests/test_witness_fast.py)

开发中另试过复用饱和前的表达式 ID。SPI 有 7/94 条证明选到了另一条具名改写，尽管等价类、端点与证明长度相同。完整输出对照拒绝了该版本。最终实现沿用 v1 的证明提取，新增的 3 个目标、2 条规则的回归用例可复现这次差异。下列主表使用修复后同一对 release 二进制的第一次完整运行。[回归用例](../scripts/test_guard_proofs_fast.py)

## 实验一 · 同一份证明的代价

每个输入对两个二进制各预热一次，然后交替顺序做 12 组配对。下表为新进程启动、输入传输、引擎运行和输出传回的 wall time 中位数。饱和列是内部阶段时间，已含在引擎 wall time 中。五份输入共 120 次计时，全部达到饱和，所有字段逐项一致（忽略唯一的耗时字段），包括等价类、代表式、顺序、停止原因、证明边及其完整文本。[汇总](../results/milestone3/engine/summary.json)

| 输入 | 目标 / 专用规则 / 证明边 | v1 spanning（ms） | indexed（ms） | 饱和阶段 v1 → indexed（ms） | indexed 更快的配对 |
|---|---:|---:|---:|---:|---:|
| Arbiter，相同的 alternate 表达，无专用规则 | 32 / 0 / 0 | 1.94 | 1.98 | 0.260 → 0.262 | 5/12 |
| Arbiter，同一输入加认证规则 | 32 / 9 / 16 | 4.17 | 3.23 | 1.250 → 0.301 | 12/12 |
| Controller | 148 / 281 / 70 | 61.18 | 28.59 | 34.855 → 2.374 | 11/12 |
| SPI | 283 / 302 / 94 | 28.21 | 19.81 | 8.894 → 0.806 | 11/12 |
| I²C | 268 / 9 / 9 | 9.69 | 6.69 | 3.230 → 0.363 | 11/12 |

在 arbiter 的 16 对源表达与替代表达上，仅用原有六条布尔规则时识别出 0/16 对，加入 9 条专用规则后识别出 16/16 对，v1 和 indexed 都生成相同的 16 条证明。request 路径把总线非零测试展开成逐位 OR。override 路径已要求获胜位为一，可以省去重复的非零测试。Z3 检查了 32 个表达各自与独立最低置位优先级公式的等价性，以及 9 条改写，有 41 个 `unsat` 结果。故意删除复位或优先级条件的负例产生 `sat` 并被拒绝。历史输入沿用各自归档的证明状态，本次没有重新认证其底层 RTL。[SMT-LIB 查询](../results/milestone3/arbiter-inputs/certificates.smt2) · [逐项状态](../results/milestone3/arbiter-inputs/manifest.json)

## 实验二 · 原始 RTL 验证循环

每个单元格做 6 次。每次从校验 RTL 哈希和提取目标开始，用 Verilator 运行初始刺激，解析原始覆盖率，按该组方法搜索见证，再用生成的刺激物理回放 DUT 并解析结果。六组轮转运行顺序。普通源表达配置使用原分支的 compact/expanded 两种写法。认证配置使用上面的两种设计相关写法。raw 组直接在相同的 compact 源表达上找见证。下表给出这一整段的中位数，两次仿真进程都计时。[原分支表达结果](../results/milestone3/rtl-source/summary.json) · [认证规则结果](../results/milestone3/rtl-certified/summary.json)

| 表达配置 | raw + 标量 | spanning + 标量 | indexed + 标量 | raw + 位并行 | spanning + 位并行 | indexed + 位并行 |
|---|---:|---:|---:|---:|---:|---:|
| 原分支 compact/expanded，ms | 134.99 | 137.80 | 139.39 | 7.61 | 11.28 | 11.42 |
| 9 条认证规则，ms | 139.28 | 135.91 | 135.64 | 8.04 | 12.20 | 11.49 |

在认证配置中，保持位并行搜索不变，仅替换 egg 匹配器，归一化及覆盖关联从 4.63 降到 3.53 ms，完整验证从 12.20 降到 11.49 ms（6 对中 5 对更快）。若保持 raw 不变，仅替换见证搜索，搜索及向量写入从 131.58 降到 0.39 ms。两项优化合用，相对 v1 加标量搜索的完整循环约快 11.8 倍。对于只需要刺激、覆盖和缺陷检测的任务，raw 加位并行获得同样的 RTL 结果。使用 indexed 另花约 3.45 ms 可同时取得认证配置的 16 条证明。原分支无专用规则的配置没有显示索引的稳定收益。

两份配置单独编译了 DUT，分别用时 3.82 和 4.01 秒。认证配置额外用 17.35 ms 生成并校验规则、写入文件和读取结果。一次性使用认证配置 indexed 加位并行时，可按约 4.01 s 编译、17.35 ms 认证、11.49 ms 验证循环记账。多轮共享编译和认证。Rust 构建、下载历史输入以及实验记录之间的交叉比对均在验证循环计时之外。六次重复属于同一台机器和同一个 DUT，没有独立设计样本或推断性误差条。

### 如何判定验证质量

- 两份配置共 72 次完整试验，实际启动 Verilator 回放 144 次，累计 1,872 个 checker 采样边沿。每次均从 4 个初始检查出发，覆盖引导给出相同的 14 个首见证，再加入固定的 4 个规格探针，定向回放共做 22 个检查。
- 每次初始与定向回放分别比对全部 91 个 DUT 覆盖点的身份与**命中次数**，包括零命中项。逐项结果与实时 raw 对照一致，也与归档参考一致。定向结果为 line 11/11、branch 17/18、toggle 60/60、expression 2/2。上游多位 override 功能错误和异步 reset 时序错误各复现 1 次。覆盖没有因 guard 合并而涨分，分母也没有缩减。[逐项覆盖与向量](../results/milestone3/rtl-certified/quality.json)
- 在隔离副本通过标准入口 `make step1` 加做穷举。Verilator、Icarus 各做 65,543 次检查，一致报告 63,232 次功能错误和 1 次时序错误。Yosys 完成结构检查。初始、定向和穷举三份覆盖 JSON 及定向向量与原分支归档逐字节相同。这是单独的正确性检查，不计入性能矩阵。整个实验未调用 LLM。结论适用于给定二态组合 guard、固定刺激及回放范围。[穷举记录](../results/milestone3/step1-check.json)

### 同机复跑

重新从干净的输出目录构建、下载和认证，并从基线提交提取 Step 1 的历史参考，完整复跑一次。两次构建的引擎二进制哈希一致。五组引擎输入的完整证明（去掉耗时字段），以及两种 RTL 配置的全部质量记录，分别与主试验一致。第二次 Controller、SPI、I²C 引擎中位数分别为 62.16 → 28.97、26.98 → 18.77、9.65 → 6.69 ms。认证配置中 raw、spanning 和 indexed 配合位并行搜索分别为 8.17、14.40、11.30 ms。主表仅用第一次运行的样本。复跑另行保存了 120 条引擎与 72 条 RTL 计时。[同机复跑记录](../results/milestone3/reproduction/)

## 环境与一键复现

实测为 Linux x86-64、Debian 13、4 CPU 配额，Python 3.12.14、Rust/Cargo 1.90.0、egg 0.11.0、Verilator 5.050、Z3 4.16.0、g++ 14.2。完整 Step 1 另用 Icarus 12.0、Yosys 0.52。用 release 模式和仓库的 `Cargo.lock`，C++ 编译器与 GNU make 供 Verilator 构建模拟器。[实测版本](../results/milestone3/versions.txt)

以下为 Debian 13 的搭建方式，假设已安装 rustup 和 micromamba，shell 已启用 micromamba。选择 conda-forge 的 Verilator 5.050 可重现本次使用的覆盖点定义。

```bash
sudo apt-get update
sudo apt-get install -y git build-essential iverilog yosys
micromamba create -y -n coms6998-m3 -c conda-forge python=3.12 pip 'verilator=5.050=h10c590a_0'
micromamba activate coms6998-m3
python3 -m pip install 'z3-solver==4.16.0.0'
rustup toolchain install 1.90.0 --profile minimal
export RUSTUP_TOOLCHAIN=1.90.0
cargo --version
verilator --version
z3 --version
```

在包含 M3 改动和 v1 基线提交的 Git 克隆中执行。若使用交付的补丁，先从 `perf/egg-compute-fast-v1` 建本地分支，再执行 `git am /path/to/COMS6998-milestone3.patch`。完整运行需要访问 Cargo 依赖和参考仓库的三个固定公开文件。选择尚不存在的输出目录，脚本在其中构建两套独立二进制、生成输入、跑完两组实验并保留日志。

```bash
git cat-file -e '71e99c4cbef9768abc1b20d4d344eaee8594db59^{commit}'
bash scripts/run_milestone3.sh /tmp/coms6998-m3-run1
```

运行成功后，`engine/summary.json` 的 `complete` 为 `true`，含 5 份输入，每份 `matched_runs` 为 24。`rtl-source/summary.json` 和 `rtl-certified/summary.json` 各有 36 次完成试验和 72 次物理回放。两份 `trials.jsonl` 保留逐轮、逐组耗时。`quality.json` 保留每个目标的向量、checker 原始事件和所有 DUT 计数。本仓库的证据目录另将 72 组回放的原始 `.dat`、日志与向量按配置压缩为 `replays.tar.gz`。[完整记录目录](../results/milestone3/)

### 脚本与单项复现

| 入口 | 用途和产物 |
|---|---|
| `scripts/run_milestone3.sh` | 从 Git 提取 v1 的 Rust 源码及 Step 1 参考输出，用相同工具链分别构建 v1 与 M3，并顺序运行以下数据准备与性能实验。 |
| `scripts/fetch_m3_reference.py` | 只获取固定提交的 Controller、SPI、I²C 输入，验证两个哈希后写入新目录及来源清单。 |
| `scripts/m3_guard_inputs.py` | 从已校验哈希的 RTL 派生目标与规则，用 Z3 逐条反证，生成两份 JSON、SMT-LIB 与认证清单。 |
| `scripts/benchmark_m3_engine.py` | 对任意给定输入执行 v1/候选配对比较。输出阶段耗时、配对胜负、参考输出。未饱和或证明有差异时保存差异并退出。 |
| `scripts/benchmark_m3_rtl.py` | 构建原始 DUT，运行六组真实循环，保存两次回放、检查向量及逐点计数。任一轮未完成或质量门槛未通过时返回失败。 |
| `scripts/predicates.py`、`scripts/run_step1.py` | 源 guard 提取、两种等序见证搜索，以及日常的初始、定向、穷举、跨模拟器验证。 |
| `scripts/guard_proofs_cached.py` | 现有整输入缓存也可显式选择 `--mode indexed`。计时实验直接运行二进制，避免把缓存命中计作引擎加速。 |
| `scripts/test_guard_proofs_fast.py`、`tests/test_witness_fast.py`、`tests/test_m3_guard_inputs.py` | 分别检查证明/停止条件/缓存，见证顺序与信号真值，以及错误的复位/优先级改写会被拒绝。这些测试和原分支语义控制均已运行。 |

例如，复核一个历史输入、运行本次新增的正确性控制，并重放认证查询，可在仓库根目录运行以下命令。

```bash
run=/tmp/coms6998-m3-run1
"$run/build/m3-target/release/guard_proofs_fast" indexed \
    < "$run/reference-inputs/spi.json" > /tmp/spi-indexed-proof.json
GUARD_PROOFS_FAST="$run/build/m3-target/release/guard_proofs_fast" \
    python3 scripts/test_guard_proofs_fast.py -v
python3 -m unittest discover -s tests -p 'test_witness_fast.py' -v
python3 -m unittest discover -s tests -p 'test_m3_guard_inputs.py' -v
z3 "$run/arbiter-inputs/certificates.smt2"
```

如需独立重跑完整 Step 1，使用项目原有的 `make setup`、`make test`，再执行 `.venv/bin/python scripts/run_step1.py --output /tmp/coms6998-step1`。该命令默认位并行。增加 `--witness scalar` 可使用旧搜索。首次复现选用干净克隆，单独指定 Step 1 输出目录可以保留仓库中已发表的原始覆盖数据。
