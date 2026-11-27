# FIFO 断言的三组 LLM 反馈实验

这个实验把 FIFO 的断言检查接在生成与下一轮提示之间。研究问题是反馈能否减少漏检、帮助定位实际失败，以及 egg 的具名推导是否在普通改写的基础上提供额外帮助。[原始 FIFO 规格、断言和独立回放](egg_fifo_assertions.md)

2026-11-24 已在 MacBook 上完成首次在线三组九次调用。[真实对照实验结果与独立复核](egg_fifo_llm_live_results.md)

## 三组协议

三组第一轮收到完全相同的规格和输出 schema。模型提交一至四个布尔违例式，以及对上一轮诊断样例的字段和零基采样位置。任何一个违例式为真就表示断言失败。驱动保存所选组前一轮的完整候选和短反馈，再将它们放入该组下一轮的 API 请求。三组各自维护历史，每轮轮换调用顺序。

| 组 | 发回下一轮的内容 |
| --- | --- |
| `raw` | 原版与诊断样例的 SMTBMC 日志片段、通过或失败、断言编号和失败步。 |
| `ordinary` | 同样的日志和失败步，加上失败拍的布尔观测、独立真值表结论和普通双向改写摘要。 |
| `egg` | 与 ordinary 相同的字段及格式，改写摘要来自真实 egg 和独立逐步证明检查。 |

所有候选使用同一套评分。先校验布尔语法与允许的采样字段，穷举五个布尔原子的全部 32 个赋值，再分别对原始 FIFO 和四个故障对照执行 12 状态 BMC，并独立检查原版的阻塞前件可达。即使弱断言让原始 RTL 通过，也要通过规格等价和全部故障检测才计为完整通过。若原版也失败，故障版上的失败不计为检出。诊断仅在上次诊断样例确实观测到目标字段违例且原版通过时评分。另三个故障的身份和结果都不进入提示。这些对照来自已公开的小型实验，只在会话中保留为不可见评分项。

raw 与两个结构化组比较的是整个反馈方案。ordinary 与 egg 接收相同的真值表及 RTL 证据，两组之间变化的是证明搜索和给出的具名推导。找不到证明和真值表给出不等价反例是不同的字段。原版或工具发生异常时，驱动保留记录并中断，工具异常没有 RTL 检出分数。[反馈实现](../scripts/egg_fifo_loop_feedback.py) · [统一评分](../scripts/egg_fifo_loop_rtl.py)

## 已完成的离线回归

用预先写定、三组相同的回复序列跑了三轮，共 9 条回复和 0 次 Responses API 调用。每条候选都使用真实的本地检查。累计 45 次 12 状态 BMC 和 9 次前件可达性检查。

第一轮预置漏掉 `TLAST`。实际工具显示原版与诊断样例均通过，隐藏评分显示只检出 3/4 个故障。离线驱动构造的第二轮请求保留了各组第一轮的候选。普通改写和 egg 两组的请求都包含独立真值表反例，具体是阻塞且只有 `TLAST` 变化时，原规格报告违例、候选漏检。raw 组收到有界检查的通过日志。

第二轮的预置回复补全四个字段。真实工具检出 4/4 个故障，诊断样例在第 5 步失败。第三轮请求包含这一失败，两个结构化组还收到该拍的布尔观测与等价推导摘要。普通搜索输出 3 个具名步骤，egg 输出 5 个，两份推导均通过独立复核。第三轮的预置回复给出 `TLAST` 与步骤 5。这个回归验证日志和证明确实进入各自的下一轮。预设回复只能验证反馈链路，模型改进和 token 收益需要真实在线对照。[离线汇总](../results/milestone3/fifo-llm-loop-fixture/summary.json) · [九份请求、回复与原始工具证据](../results/milestone3/fifo-llm-loop-fixture/transcript.tar.gz)

## 复现

沿用 FIFO 环境，已有固定 fixture 时可省略下载。离线模式不读取 API 密钥。以下从仓库根目录运行，输出取新路径。[环境与依赖](egg_fifo_assertions.md#环境脚本与复现)

```bash
python3 scripts/m3_controller_replay.py --fetch /tmp/egg-fifo-fixture
CARGO_TARGET_DIR=/tmp/fifo-loop-rust cargo build --locked --release --manifest-path egraph/Cargo.toml --bin egg_assertion_forms
python3 scripts/egg_fifo_loop.py --fixture --rtl /tmp/egg-fifo-fixture/public/rtl/axis_fifo.v --binary /tmp/fifo-loop-rust/release/egg_assertion_forms --output /tmp/fifo-loop-fixture
```

在线模式固定使用 OpenAI Responses API。由运行环境提供 `OPENAI_API_KEY`，并将 `FIFO_MODEL` 设置为所选模型。三组共享模型、每轮输出上限及最多三轮的预算，合计最多九次调用。程序不自动重试。每条响应保存实际模型、响应 ID 及原始 token 用量。若 API 返回失败且保留了用量回执，单独写入相应的 `provider-error.json`。开发环境没有 API 密钥；MacBook 上的实际调用结果另见上述报告。

```bash
python3 scripts/egg_fifo_loop.py --live --model "$FIFO_MODEL" --rounds 3 --max-output-tokens 1024 --rtl /tmp/egg-fifo-fixture/public/rtl/axis_fifo.v --binary /tmp/fifo-loop-rust/release/egg_assertion_forms --output /tmp/fifo-loop-live
```

如当前 API 项目支持 M2 使用的 `gpt-6.1-sol`，可指定 `--model gpt-6.1-sol --reasoning-effort low`。该设置随每个请求发送，并写入运行配置；本实验的任务和输出预算仍与 M2 不同。

`egg_fifo_loop.py` 负责编排、记录每轮实际消息和统一打分。 `egg_fifo_loop_feedback.py` 生成三组的反馈。 `egg_fifo_loop_rtl.py` 执行本地 Yosys/Z3 检查并保存原生证人和波形。 `egg_fifo_loop_provider.py` 提供真实 Responses 传输、结构化输出和用量记录。
