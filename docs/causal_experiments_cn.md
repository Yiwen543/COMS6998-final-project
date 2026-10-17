# e-graph 因果验证：已实现与运行方式

本次补充的是机制检查和实验记录设施，尚未证明覆盖率或成本收益。

## 机制

C 使用 egg 的交换、结合、幂等、常量、吸收、分配律以及原有规则；饱和受迭代、节点和时间预算限制。D 使用普通递归化简，包括交换/结合规范化、常量、幂等、吸收及双重否定。D 不做分配律搜索。这个比较只能衡量相对此明确基线的收益，不能代表优于所有传统 Boolean 优化器。

C/D 都用同一个共享表达式编码和分组接口。仅在位宽、二态语义、采样事件和 reset 上下文相同时分组。等价组仅提示可能共享刺激，不合并源代码覆盖点、不删除分母。egg 的同类是已应用规则下的证明；不同类不表示不等价。

## 离线检查

先在 VS Code 的项目终端编译现有 egraph，再运行：

```sh
cargo build --locked --offline --manifest-path egraph/Cargo.toml
.venv/bin/python scripts/audit_semantics.py --output results/agent-audit-new.json
.venv/bin/python -m unittest discover -s tests
```

审计包含两组分配律机制样例和交换/吸收对照，穷举三个变量的取值，检查输出代表式语义，并记录真实 Arbiter 的 B/C/D 反馈、哈希、字节数。字节数不是 token 数。这些人工表达式不是额外 RTL benchmark。

## 真实 C/D 对照

配置 API key 后，保持相同模型、effort、轮次、周期和 token 阈值分别运行。此步骤会调用付费 API；本次开发未执行。

```sh
.venv/bin/python scripts/run_agent.py --group C --run-id pair-01 --output results/agent-C-pair01
.venv/bin/python scripts/run_agent.py --group D --run-id pair-01 --output results/agent-D-pair01
.venv/bin/python scripts/compare_experiments.py --c results/agent-C-pair01/summary.json --d results/agent-D-pair01/summary.json --tokens 10000 --output results/agent-pair01-comparison.json
```

比较器检查 DUT/TB 哈希和全部配置一致，拒绝离线、用量缺失或失败的运行。使用共同 token 预算内最后一轮完成结果；保留越界调用实际用量。run-id 是重复标签，不是模型随机种子。初始请求相同的提示仅在新日志含哈希时有效。重复输入按 reset/req/override 三元组计数，包括 starter 和批内重复；重复 target_id 单独记录，不能直接视为语义重复。每轮保存实际请求哈希。

正式实验应轮换 C/D 执行顺序，重复独立运行，并先确定共同预算。B/A 仍可通过原入口运行。单对结果仅作描述，不计算显著性，也不支持跨设计结论。

## 仍缺的研究环节

目前支持固定 Arbiter 和三个新增 CVDP 模块，见 cvdp_modules_cn.md。已完成新增模块的真实 EDA 与确定性 witness 对照，C/D 刺激相同。下一步需继续扩展独立设计，并按设计划分开发/测试集。在这些设计上重复实验并统计成对差异和置信区间。不能拿人工分配律样例代替 RTL 上的收益证据，也不能把 C/D 语法不同本身当作收益。还应加入 BDD/SAT 或成熟 Boolean 优化器基线，以判断是否需要 e-graph 特有机制。
