# SPI core：协议安全 offer driver 的独立登记与验证

本轮为原版 OpenTitan SPI core 建立了一个**单独登记的新刺激接口版本**，修复的是
LLM 请求到 DUT 引脚的握手保持机制。它不修改 DUT、Claude v4 checker、原实验结果、
17 组目标或 3×6×64 周期预算，也不构成 C 优于 B 的证据。

离线门槛、故障控制及 mock/replay 已通过。Claude 第二次只读审阅接受了限定范围冻结；
新的独立 live B 已按原预算完成，见[结果报告](spi_core_safe_b_development_2026-11-04.md)：
三组均无输入违规，但首轮只剩一组、第二轮全目标命中，未通过原区分度门槛；C 不启动。
最终 checker 为 pass/fail/fail，失败轨迹和待归因状态全部保留。

## 为什么另行登记

[旧 B 报告](spi_core_b_development_2026-11-04.md)中，前两次重复合法地在第 4/3 轮
命中全部目标；第三次在 cycle 173 的 `valid=1, ready=0` 后，于 cycle 174 撤回了
请求。第三次最终原始覆盖仍被保留，但不满足合法输入门槛。这表明当时有刺激传输
可靠性问题，不能据此判断 e-graph 是否有效。

新的 [预登记文件](../configs/spi_core_safe_driver_prereg_v1.json)在新 driver 实现和
仿真之前生成。旧的直接引脚版本保持原状；历史失败刺激只用于标明的私有回归控制，
不修补旧 B 分数，不进入新模型提示词。

## 实现方法

1. JSON 的 `valid/tx_valid` 改成 `cmd_offer/tx_offer`。每个 `1` 都表示一次入队，
   连续两个 `1` 是两次请求，即使 payload 相同。其余字段宽度及硬件含义不变。
2. 命令和 TX word 分别使用容量 392 的 FIFO。时钟低电平时入队并驱动队首；上升沿前
   采样 ready，只有 `valid && ready` 才出队一次。未握手时 valid 和整个 payload 保持。
   不读取内部 RTL 状态，不根据覆盖自动选择输入。
3. 每条 JSON action 仍恰好消耗一个物理周期，最多 8 个 seed 加 384 个新周期。
   等待握手需要模型提供空 offer 周期；EOF 不 drain，不额外推进时钟。下一轮从固定
   seed 重放全部累计 action，重建 pending 队列后再执行新 action。
4. 硬件复位取消未接受请求并记录 ID；已接受事务仍由原 checker 按规范判断。
   每个通道验证 `offered = accepted + reset_cancelled + pending`，防止丢失和重复。
5. 独立的 Python transport oracle 核对请求、实际引脚和队列日志；原 Claude checker
   仅接收实际 DUT 引脚。两者职责不同。oracle 和 SV driver 都由 GPT/Codex 实现，
   因此不能宣称作者独立；Claude 的只读审阅和故障控制提供额外检查。
6. simulator、transport、coverage、checker worker 错误分开记录。失败轮若展示上一轮
   覆盖，会显式标注 `measurement_fresh=false` 及测量轮次。DUT checker 拒绝设计仍是
   功能失败证据，不归为 driver 错误。pending 时即使原 checker 返回 pass，整体完成标志
   仍为 false。

新接口见 [公开 offer 合同](../examples/spi_core_integration/docs/safe_offer_contract.md)，
实现见 [SV driver](../examples/spi_core_integration/verif/tb_spi_core_safe.sv)、
[接口与 oracle](../scripts/spi_core_safe_interface.py)、[runner](../scripts/run_spi_core_safe_b.py)。

## 离线证据与审阅处置

最终 [preflight-v3](../results/spi_core_safe_20261104/preflight-v3/summary.json)包含 13 个
控制，每个分别运行 Verilator/Icarus：普通写、三种 speed、full-cycle 读、TX 饥饿恢复、
RX 背压恢复、部分字节与 CSID 切换、相同 payload 的不同 offer、硬件复位取消与重启、
EOF pending、跨轮 pending 前缀以及明确标注的历史失败意图回归。实际引脚轨迹和队列
日志双仿真器一致，checker/完成状态也一致。完整 result 文件因工具、路径、耗时以及
仅 Verilator 采集 coverage 而不同；这不等于语义不一致。

原始 3,107 个 DUT counter identity 全部保留：64 line、234 branch、349 expression、
2,460 toggle。新 seed 下原 17 组目标仍全未覆盖，校准仍可达全部目标及三个多步事件。
这里可达不表示每一组都是多步事件特有的目标。原有限范围 checker 的限制继续有效。

一个明确的保持例子：cycle 88 入队命令，88/89 两周期 ready 为 0；89 的 offer 已为 0，
实际 valid 仍为 1、payload 保持；90 握手后才撤下。共 89 个周期、结束于 cycle 88 的
短轨迹与完整累计轨迹的同长度前缀逐字段一致，pending ID 88 在 cycle 90 恰好接受一次。

[实际故障 SV 控制](../results/spi_core_safe_20261104/transport-faults-v1/summary.json)
分别编译执行了四个故意损坏的 driver，每个都保留原 DUT：

| 故障 | 独立 transport 拒绝点 | 额外证据 |
| --- | --- | --- |
| 丢失一次 offer | cycle 8，引脚意图不符 | JSON 中有请求，实际未驱动 |
| 重复接受 | cycle 8，接受/守恒不符 | 后续 ID 8 确实再次被接受 |
| 队首乱序 | cycle 10，引脚 payload 不符 | 待处理请求顺序被改变 |
| 使用边沿后的 ready | cycle 8，接受/守恒不符 | pre/post ready 不同的周期被保留 |

另四个 trace-level 控制覆盖 valid 撤回及 payload 改变，原 Claude checker 的输入假设
检查和 transport oracle 均拒绝。以上是 driver 检错控制，不应计为发现四种 DUT bug。

10 个新测试通过，包含无 ready 不得自动前进、相同 offer 不得去重、独立通道复位守恒、
字段/宽度拒绝，以及失败轮部分周期、重试、陈旧测量标识的计账。修订版完整 mock 与
replay 各 21 次仿真、4,200 个实际周期、零 API 调用。21 个累计批次的实际 trace、队列
及原始计数文件逐字节一致；请求和 checker 结果按 JSON 值一致，重放请求的键顺序可不同。

Claude [首轮审阅](../results/spi_core_safe_20261104/claude-review-v1/review.json)未批准冻结。
它认可核心队列顺序，但要求实际渲染提示词、四种额外故障控制、pending 前缀重放和
更清楚的失败分类。上述证据及容量/预算断言已补齐。其“旧 system prompt 可能要求
手动保持 valid”的猜测不符合实际原文；149,414-byte 补充包提供 runner 实际提示词
以便直接核验。补充包同时提供原 17 组源计数、之前未提供的脚本和已审阅代码的精确
差异；省略的旧控制/代码用哈希明确绑定，不声称重新审阅这些省略内容。

[第二次 Claude 审阅](../results/spi_core_safe_20261104/claude-review-v2/review.json)返回
`ready_to_freeze=true`，仅接受 B 开发范围。仍保留：四种实际 faulty-SV 仅覆盖命令通道、
跨边界 pending 的专用控制仅覆盖命令、尚无未来 C/P 公共字段一致性验证。TX 已有保持、
变化、相同 offer、守恒、取消及 EOF 控制，但不能把它们说成完整 TX mutation suite。

[审阅意见处置](../results/spi_core_safe_20261104/review-disposition.json)逐项记录证据。
关于 compile 返回值的意见不成立：底层返回二元组，runner 使用的包装函数返回三元组，
单测及真实 mock/replay 均符合。未经 review 的 provisional 配置已实测在访问 key/API
之前被拒绝。覆盖分母异常仍会终止该重复并使完整性门槛失败，但不立即中止其他重复；
simulator 失败有 execution/log/runner failures.jsonl，未统一另写 per-round failure.json。
这两个有限的错误处理限制保留，不修改已审阅代码，也不将失败结果纳入合法达标。

最终 [新冻结配置](../configs/spi_core_safe_b_development_v1.json) SHA-256 为
`7ea4c6e6e6ef12582640f52679ecba0488855dffe22efc8f4f7801db153d10e4`。

## 成本与复现

这些是工程验证成本，不能并入尚未运行的新 B/C 性能结果。早期版本和失败的本地
复核包构建尝试保留，不能只报告最终成功版本。

| 阶段 | 编译 | 仿真 | 实际周期 | API |
| --- | ---: | ---: | ---: | ---: |
| preflight-v1 / v2 / v3 | 2 / 2 / 2 | 24 / 26 / 26 | 3554 / 3922 / 3922 | 0 |
| 四种实际 faulty-SV | 4 | 4 | 672 | 0 |
| mock-v1 / mock-v2 / replay-v2 | 1 / 1 / 1 | 21 / 21 / 21 | 4200 / 4200 / 4200 | 0 |
| Claude 首轮只读审阅 | 0 | 0 | 0 | 1 |
| Claude 第二轮只读审阅 | 0 | 0 | 0 | 1 |

首轮 Claude 审阅用时 57.90 s，API 报价 $0.467176；输入 72,480、输出 5,239 token，
其中 thinking 1,858 已包含在输出，不重复相加。输入含 72,476 cache-creation token。
第二次 40.76 s，$0.442816，输入 72,332、输出 4,058 token。两次合计 $0.909992、
154,109 token；thinking/cache 子明细不重复计入。两次暂存 Anthropic key 均已删除。

环境：Python 3.13.9、Verilator 5.050、Icarus 12.0、Yosys 0.70+post、OpenAI SDK 2.54.0。
工作树基于 commit `50d7ee83d61989017e28e981420cd58f4c5f0787`，本轮文件尚未提交或 push。
DUT 固定于 OpenTitan `0ea5236fe749e70ba18f56ba19c4be982ef46da7`。
checker SHA-256 `07765601452ca14f078e8a3889f6d2d21574181091eb404c717087ce2d20a540`；
新 SV driver SHA-256 `66bbc3fdbe3ecc45b0821833492c99463a4d97fa10a10c63b089006fc2411bbc`。

从仓库根目录复现（输出目录须不存在，避免覆盖历史证据）：

```sh
.venv/bin/python scripts/preflight_spi_core_safe_driver.py --output results/spi_core_safe_reproduce/preflight
.venv/bin/python scripts/test_spi_core_safe_faults.py --preflight results/spi_core_safe_reproduce/preflight --output results/spi_core_safe_reproduce/faults
.venv/bin/python -m unittest discover -s tests -p 'test_spi_core_safe*.py' -v
.venv/bin/python scripts/freeze_spi_core_safe_experiment.py --preflight results/spi_core_safe_reproduce/preflight --faults results/spi_core_safe_reproduce/faults --output build/spi_core_safe_reproduce.json
.venv/bin/python scripts/run_spi_core_safe_b.py --mode mock --config build/spi_core_safe_reproduce.json --output results/spi_core_safe_reproduce/mock
.venv/bin/python scripts/run_spi_core_safe_b.py --mode replay --config build/spi_core_safe_reproduce.json --replay results/spi_core_safe_reproduce/mock/calls.jsonl --output results/spi_core_safe_reproduce/replay
```

上述无 review 的 freeze 仅允许 mock/replay，不能直接运行 live B。原版 checker 不重新生成。

## 后续门槛

独立只读复核接受后，冻结新接口并运行**一次新的三重复 B 开发实验**。仍用
`gpt-6.1-sol`、low、输入上限 32,000、输出上限 16,384、120 s timeout、最多一次重试，
正常共 18 次生成。三重复均须完整、输入合法；至少两次首轮仍有至少两组目标未全命中，
且至少两次后续取得目标组进展。不得换预算、删失败或选择性重跑。

```sh
.venv/bin/python scripts/run_spi_core_safe_b.py --mode live --output results/spi_core_safe_20261104/b-live-v1
```

该输出目录已用于本次运行，复现应使用新目录。live 命令读取隐藏暂存密钥，不在命令行写入 key。

仅 B 通过后才准备新的正式对照；开发 B 不能混作正式控制组。C/P 在运行前还需验证
所有公共 transport 字段一致，C 只添加已证明的语义关系，P 按自身轨迹的 shadow-C
实际输入 token 匹配。当前阶段没有测量 C 收益，也没有把 driver 改进当作 e-graph 收益。
