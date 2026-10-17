# 最小 LLM stimulus agent：接入与实验步骤

这份本地源码副本基于上游提交 96822c9b190fed8b4152e7b2afce6c676266f266。它新增一个 stimulus-only 单模型循环，继续使用上游固定 RTL、固定 checker 和 Verilator 覆盖率解析器。

## 1. 第一版明确做什么

每次调用模型只提交一批整数输入向量。Python 将这些向量交给固定 TB，运行仿真、读取真实覆盖率，再把该组允许看到的反馈送入下一轮。模型不能修改 DUT、checker、文件路径或执行命令。

第一版已经实现：

- Responses API 请求与 strict JSON Schema；不需要新增 Python 第三方包。
- A/B/C/D 四种反馈，以及最多轮数、每批向量数、累计仿真周期、覆盖率停滞等停止条件。
- 每轮请求、原始 API 响应、输入向量、checker 状态、覆盖率、usage 和时间记录。
- 不完整输出、拒答、非法输入的记录；这些调用的 usage 仍计入成本。
- 所有已提交向量逐轮重放，重放周期全部计入总预算。
- CSV 汇总入口。

这是提出测试输入的 agent，不是完整的自动 testbench 代码生成 agent，也不是通用 RTL 前端。Arbiter 使用原入口；另外三个 CVDP 模块使用 run_cvdp_agent.py，详见 cvdp_modules_cn.md。

## 2. 先不花 API 费用，查看实际请求

在本目录打开终端：

```sh
python3 -m unittest discover -s tests -p test_agent.py -v
python3 scripts/run_agent.py --dry-run --group C --output results/agent-preview/C
```

dry-run 从上游保存的 initial-coverage.json / egraph.json 构造请求，不运行仿真，也不访问 API。查看输出目录中的 request.json：里面是将来真正发给模型的内容。

现有源码副本已生成 A/B/C/D 四份请求预览。每次重跑请使用新的输出目录，防止覆盖已有实验。

## 3. 在有 EDA 环境的机器上准备

完整运行需要 Python、C++、Verilator（支持 --coverage-expr）、Icarus、Yosys 和 Rust/Cargo。上游 Makefile 和 Brewfile 保留。

```sh
brew bundle --file Brewfile
make setup
make doctor
make test
```

Linux 可按上游 README 准备相应工具。C 组使用 cargo --locked --offline，先执行 make setup 获取锁定依赖。准备过程不调用 LLM。

本地 VS Code 集成已安装 EDA 工具并实际完成 Verilator/egg/Icarus/Yosys 流程；新结果在 results/vscode 中。Agent 的模拟器接口也已使用明确标记的人工输入验证，未调用模型 API。真实 Agent 测量仍需要你自己的 API key。

## 4. 设置 API 后先跑一个小规模 smoke test

将你自己的 OPENAI_API_KEY 放在终端环境中，不写进 Python 源码或提交到 Git。实际模型访问权限取决于你的 API 账户。

默认主模型是 gpt-6.1-sol，推理档位 medium。先测试一轮，避免未经验证就批量发请求：

```sh
python3 scripts/run_agent.py --group C --model gpt-6.1-sol --effort medium --max-rounds 1 --batch-size 4 --run-id smoke-01 --output results/agent-runs/smoke-C
```

检查以下证据：

1. round-01/response.json 的 status 为 completed，并有实际 usage。
2. batch.json 内的输入向量合法。
3. simulation.log 有完整 RESULT，而不是中途退出。
4. summary.json 的 live_api=true、simulator=verilator，并包含初始和最终覆盖率。

smoke test 不要求一定改善覆盖率；它首先验证模型、输出解析、仿真和反馈接口接通。

## 5. 固定模型，运行四组

| 组 | 反馈内容 |
|---|---|
| A | 规格、RTL、此前向量、运行日志与 checker 结果 |
| B | A + 原始 DUT 覆盖率 + 未覆盖目标的原始完整谓词 |
| C | A + 相同原始覆盖率 + egg 代表式与共享条件因子化 |
| D | A + 相同原始覆盖率 + 普通局部 Boolean 简化与相同因子化 |

B/C/D 的目标 ID、源位置、位宽、时钟/reset 上下文一致；完整谓词都含外层 guard。C 没有额外获得满足输入或手写 probes。C/D 使用同一个共享条件编码器，减少格式差异。

早期六规则版本的 C/D 预览相同。扩展规则后预览可以不同，但新的三个 CVDP 模块中，C/D 确定性 witness 仍相同，尚未证明 e-graph 独有收益。不要为制造增益而弱化 D；先跑通一组真实 smoke test，然后扩展表达式/电路样例，再投入四组批量实验。相同请求下的随机响应差异也不能解释为机制增益。

```sh
python3 scripts/run_agent.py --group A --run-id trial-01 --output results/agent-runs/trial-01/A
python3 scripts/run_agent.py --group B --run-id trial-01 --output results/agent-runs/trial-01/B
python3 scripts/run_agent.py --group C --run-id trial-01 --output results/agent-runs/trial-01/C
python3 scripts/run_agent.py --group D --run-id trial-01 --output results/agent-runs/trial-01/D
python3 scripts/summarize_agent.py results/agent-runs/trial-01 --output results/agent-runs/trial-01/summary.csv
```

默认各组相同限制：5 次模型调用、每批最多 16 个向量、累计最多 512 个 checked cycles、每次最多 4096 个输出 tokens；连续两轮 branch coverage 没有改善则停止。格式无效的响应仍消耗一轮调用。已有预算不能绕过的仿真失败会终止该次运行并保存错误。

默认 stop-after-tokens=50000 是每次调用后检查的累计 usage 停止阈值，不是严格账单上限；最后一次请求可能超过阈值。每次输出 cap 包含 reasoning tokens。输入、输出、缓存和 reasoning 细分以 API 实际回执为准；reasoning 不重复累加到 output_tokens。网络错误不自动重试，缺失回执时不能声称成本完整。

使用标准 API 的实际 tokens 与成本作结果曲线；对于严格相同 token 预算的比较，应在每组已记录的轨迹上选不超过该预算的最后一个完成轮次。粗粒度预算检查允许的 overshoot 需保留在原始记录中。

## 6. 如何解读结果

先在开发样例上确认接口，再换新的 run-id 重复独立运行。run-id 只是实验标签，不会被当成 API seed 参数。记录服务返回的 model 字段；有可用固定快照时优先锁定，并保存完整请求。

主表比较：最终 raw branch coverage、新增 branch points、实际 tokens、总仿真周期、总耗时和失败比例。覆盖率图的横轴可用累计实际 tokens 或周期，纵轴用覆盖点数。总耗时包含本次编译与语义预处理，不能只比较最后一次仿真时间。

checker 失败可能是在发现原始 DUT 缺陷，应与格式错误、工具失败分开。不要修改 checker 以提高覆盖率或让已知错误通过。默认保留不可达分支在原始分母里；没有归零计数就不能说 100%。

单个 Arbiter 上的模型结果只能证明局部流程。只有 C 在多个设计与重复运行中超过 B，而且与 D 的差异也有证据，才支持 e-graph 特有贡献。下一阶段再扩展到更多条件结构和 FIFO，不必先开发完整 SystemVerilog 前端。

## 7. 主要新增文件

- scripts/agent_core.py：反馈表示、普通简化对照、JSON 输出检查与 API 客户端。
- scripts/run_agent.py：多轮控制、预算、Verilator 执行与实验记录。
- scripts/summarize_agent.py：结果汇总。
- tests/test_agent.py：不需要模型密钥或 EDA 工具的离线测试。

离线测试中的 Simulator/Provider 是明确标记的测试替身；没有把它们的合成覆盖率当作新 RTL 实验结果。

API 依据：

- https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses
- https://developers.openai.com/api/docs/models/gpt-6.1-sol
- https://developers.openai.com/api/docs/guides/latest-model
