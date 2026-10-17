# CVDP 多模块集成

已接入三个官方 CVDP 数据中的原始 RTL：

| 本地模块 | CVDP 记录 | 类型 | 验证范围 |
|---|---|---|---|
| barrel_shifter | cvdp_agentic_barrel_shifter_0001 | cid016 调试输入 | 8 位逻辑左右移 |
| caesar_cipher | cvdp_agentic_caesar_cipher_0001 | cid016 调试输入 | ASCII 字母变换，其他字符保持 |
| universal_shift_register | cvdp_agentic_universal_shift_reg_0003 | cid004 增强输入 | 原接口的 hold/shift/rotate/load 与 serial_out |

来源：https://huggingface.co/datasets/nvidia/cvdp-benchmark-dataset

锁定 revision `5b807d945f6a99aa645f7e43a64a2115e281b4bf`，文件 `cvdp_v1.1.0_agentic_code_generation_no_commercial.jsonl`。每个模块保留原始问题记录、类别、原始 RTL 哈希与验证范围，未对 DUT 做修复。这不是官方 CVDP-ECov 基准复现。

## 在 VS Code 运行

“终端 → 运行任务”：

- **7. 运行 CVDP 多模块 EDA 对照**：编译并跑三个模块的初始、C/D 确定性 witness 补测和扩展集，逐条对照 Verilator/Icarus 输出，不调用 API。
- **8. 预览 CVDP Agent 请求（不调用 API）**：选择模块与组，检查实际输入字段、反馈和 JSON schema。
- **9. 单轮 CVDP Agent（调用 API）**：选择模块、组、模型，输入 API key 后执行单轮；固定 checker 不接受模型修改。

每次输出独立保存到 results/vscode，并更新 latest-cvdp 或 latest-preview 等指针。结果中 functional_errors 是独立 checker 检出的 DUT 错误；两个调试输入本就含错误，不表示运行器失败。

## 命令行复现

```sh
make cvdp
.venv/bin/python scripts/run_cvdp_agent.py --module caesar_cipher --group C --dry-run --output results/agent-preview-caesar-new
```

预览默认读取本次已验证的 `results/cvdp-suite-20261017`。若使用新一轮结果，加 `--fixture-root results/vscode/cvdp-具体时间`。预览会检查保存结果的 DUT/TB 哈希，拒绝不匹配的文件。

配置 OPENAI_API_KEY 后可以跑真正的模型对照（会产生 API 费用）：

```sh
.venv/bin/python scripts/run_cvdp_agent.py --module universal_shift_register --group C --run-id pair-01 --output results/agent-cvdp-C-pair01
.venv/bin/python scripts/run_cvdp_agent.py --module universal_shift_register --group D --run-id pair-01 --output results/agent-cvdp-D-pair01
.venv/bin/python scripts/compare_experiments.py --c results/agent-cvdp-C-pair01/summary.json --d results/agent-cvdp-D-pair01/summary.json --tokens 10000 --output results/agent-cvdp-pair01.json
```

三个模块共享同一个 Agent 控制器与预算记账。每轮重放初始 2 条刺激及全部历史刺激，所有检查都计入周期预算。Caesar 没有 branch counters，因此目标和 token ROI 的分子使用新增 line points；其余两个使用新增 branch points。summary 显式记录 coverage_objective，比较器拒绝不同目标、不同 DUT/TB/checker 的对照。跨模块汇总不能直接混合 line 与 branch 的原始数量。

每个模块输入 schema 来自审核过的端口表：字段、整数范围、target_id 都严格检查。模型只能提交输入，不能执行代码。保留原始不可达计数器，避免通过移除分母制造提升。

## 本次实测结论

完整结果见 `results/cvdp-suite-20261017/REPORT.md`。C/D 在三个模块都生成相同 witness 输入，覆盖结果相同，尚无 e-graph 额外收益证据。桶形移位器初始 branch 1/2，补测 2/2；Caesar 初始 line 3/5，补测 4/5；移位寄存器初始 branch 3/8，补测 8/8。

桶形移位与 Caesar 各扩展枚举全部 4096 个输入组合；加入两条 starter 后各检查 4098 次。移位寄存器执行 4096 个 reset/load/operation 三步试验，加入 starter 后检查 12290 次，覆盖所有先前 q、操作、方向、serial 输入。它不是所有信号笛卡尔积或任意时序的形式证明，也不验证增强题要求的新功能。同步/异步 reset 文档差异不在本次 checker 范围。

Agent 的真实 EDA 适配器另用固定离线 batch 做过检查，每个模块恰好消耗 2+3=5 个检查周期，验证了动态字段、重放预算和 line/branch 目标。固定 batch 不是 LLM 结果，不计算 token ROI。当前尚未调用真实 LLM API。

## 来源复核

完整数据文件只作为本地缓存保留在 third_party/cvdp。下载相同 revision 后可执行：

```sh
.venv/bin/python scripts/import_cvdp.py --dataset third_party/cvdp/agentic.jsonl --check
```

导入器先核对整个数据集 SHA-256，再逐字节检查选定 RTL 与问题记录；不会覆盖已修改文件。新的 DUT 版本需要重新审核 predicate/source-counter 映射，不能直接沿用当前适配器。当前映射已用 Verilator 5.052 实测，并验证每个可满足 uncovered predicate 的 witness 命中其对应源计数器。
