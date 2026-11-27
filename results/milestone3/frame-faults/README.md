# AXI 帧长度调整器的变异对照

本实验在临时目录中编译完整的帧长度调整器、其 AXIS 输出 FIFO 和状态 FIFO。六项改动在首次运行变体前固定，每次只改动一处 RTL。端口数据宽度为 8 位，最短输出帧 4 字节，最长 8 字节。三个场景覆盖 1–12 字节输入、独立数据/状态背压，以及有未完成事务时复位。全部设计使用相同的入队指令、消费端 ready 和复位时序；驱动在各自 DUT 真正接收后才取出下一个输入字节，所以受到背压的设计可能在不同时刻看到后续字节。[计划、精确代码改动及哈希](plan.json)

| 设计 | 行为改动 | 长度扫描 | 独立背压 | 中途复位 |
|---|---|---|---|---|
| original | 原始 RTL | PASS | PASS | PASS |
| F01 | 填充字节改为全一 | FAIL | FAIL | FAIL |
| F02 | 正好达到长度上限也设置截断标志 | FAIL | FAIL | FAIL |
| F03 | 截断帧缺少最后一拍的 TLAST | FAIL | FAIL | FAIL |
| F04 | 输入有效但未被接收时仍增加长度计数 | PASS | FAIL | PASS |
| F05 | 用数据通道 ready 消费状态 FIFO | PASS | FAIL | FAIL |
| F06 | 状态 FIFO 不再响应同步复位 | PASS | PASS | FAIL |

共 21 次原生 Icarus 回放、6,384 个 PRE/POST 周期记录。原版三次均通过；在 18 个变异与场景组合中，冻结的独立 checker 检出 13 个，5 个通过。六项变异都至少在一个场景中有确定的失败。F04 仅在背压场景暴露，F06 仅在中途复位场景暴露。F03 的三个场景、F05 的背压场景和 F06 的复位场景共五份报告，既有确定失败，也有 `completion_unresolved`；后者没有计为额外检出。重复采样同一错误可能产生多条失败事件，事件条数不能作为不同故障数。[逐场景结果](cases.json) · [汇总](summary.json)

## 复现与数据读取

使用 Python 3.12、Icarus Verilog/vvp 12.0，以仓库根目录为工作目录。已有固定版本 Controller 数据时可跳过下载。新建输出目录后，脚本会先记录变异与开发/评估拆分，再在隔离目录分别编译并重放原始驱动，复核每一份公开信号记录及参考 checker 结果。每个原始文件和改动后的 RTL 均有 SHA-256。[构建记录](builds.json)

```bash
python3 scripts/m3_controller_replay.py --fetch /tmp/frame-fixture
python3 scripts/egg_frame_faults.py --fixture /tmp/frame-fixture --output /tmp/frame-faults-run1
```

- `scripts/m3_controller_replay.py --fetch` 下载固定提交的完整 Controller 数据，并核对哈希。
- `scripts/egg_frame_replay.py` 构建原始测试顶层，生成原生输入指令，解析 PRE/POST 观测并执行冻结的独立 checker。
- `scripts/egg_frame_faults.py` 校验每条变异的源文件、行号及原语句，对每个变体使用同一套刺激。保存每个设计/场景的判定、明确失败、未知以及完整公开采样。开发可见的设计为原版及匿名探针 A/B，对应 F02/F05。其余四项保留为评估数据。
- `observations.jsonl.gz` 中的每个 JSON 行包含设计、场景、公开的周期输入与 PRE/POST 采样，以及参考判定。端口采样使用整数，`-1` 表示 X/Z。`native-replays.tar.gz` 中保存全部 21 份原生驱动日志和三份共用刺激。可从任一公开采样重新运行独立 checker；再次编译和回放复现了相同的 21 份原生日志、采样和判定。[原始日志与刺激](native-replays.tar.gz)

下例供离线评分程序使用；给生成器的开发视图只选择约定的匿名探针和允许的公开反馈，参考标签和留出变体另行保管。

```python
from pathlib import Path
import sys

sys.path.insert(0, "scripts")
from egg_frame_faults import load_corpus

cases = load_corpus(Path("results/milestone3/frame-faults"))
rows = cases["F05", "backpressure"]["rows"]
reference = cases["F05", "backpressure"]["checker"]
```
