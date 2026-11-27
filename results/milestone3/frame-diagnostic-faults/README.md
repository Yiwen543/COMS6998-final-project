# 帧监视器的端口灵敏度对照

这些附加样例用于在实际端口波形上检查三个违例监视器能否报警。先固定输出改动，再使用原始帧长度调整器、帧 FIFO、状态 FIFO 和已有的三份输入指令运行 Icarus。每次仅在顶层包装模块的临时副本中改动一个输出，后端 RTL 保持原版。所有样例均在先前的模型生成之后构造，不用于统计原始 RTL 缺陷或先前六项变异的检出率。[精确 Verilog 改动及哈希](plan.json)

| 设计与测试信号 | 改动 | 长度扫描 | 独立背压 | 中途复位 | 总报警采样数 |
|---|---|---:|---:|---:|---:|
| 原版，全部五个监视器 | 原始输出 | 0 | 0 | 0 | 0 |
| D01，`data_hold` | 上一拍数据有效但接收端未准备好时翻转掩码，用掩码异或公开数据的最低位 | 0 | 94 | 32 | 126 |
| D02，`pad_flag` | 有效头部的原长恰好为 4 时翻转填充标志 | 1 | 2 | 20 | 23 |
| D03，`clamped_length` | 有效头部的原长大于 8 时，将公开调整后长度报告为 7 | 4 | 37 | 7 | 48 |

每个表格数字是违例成立的 PRE 采样次数。持续呈现的同一头部能触发多次报警。三项改动均仅激活预先指定的参考监视器。冻结的独立事务 checker 在 9 个改动与场景组合中判定 8 个 FAIL，D01 在全程 ready 的长度扫描中判定 PASS。原版三个场景均 PASS。12 次回放产生 3,648 个 PRE/POST 周期记录、3,636 个相邻 PRE 采样对；五项参考监视器均无无法判定的采样。[逐场景事务判定与各项报警](cases.json) · [汇总](summary.json)

每次运行核对源文件和输入指令的哈希，并用原版波形独立重建每个变体的全部 PRE/POST 输出。未被改动的引脚和每拍驱动输入均须与原版逐项相同。新采的原版波形、参考 checker 的完整结果与原实验归档一致。另作一轮全新编译和回放，12 份原生日志、波形及判定均重现。[各设计的编译输入](builds.json) · [三份输入和十二份原生日志](native-replays.tar.gz)

## 运行与读取

使用项目已有的 Python 3.12、Icarus/vvp 12.0 及 Python 的 z3-solver 环境。安装和获取固定版本的完整 Controller 数据见原实验。已有数据时可直接运行第二条命令，输出目录需尚不存在。[原实验环境说明](../frame-faults/README.md)

```bash
python3 scripts/m3_controller_replay.py --fetch /tmp/frame-fixture
python3 scripts/egg_frame_diagnostic_faults.py --fixture /tmp/frame-fixture --output /tmp/frame-diagnostic-faults
```

`egg_frame_diagnostic_faults.py` 构造端口控制、验证波形并整理语料；`egg_frame_replay.py` 编译和驱动原生设计，运行冻结事务 checker；`egg_frame_observe.py` 依据 `egg_frame_terms.py` 定义的五项局部违例，对连续两个 PRE 采样求值。事务 checker 还检查逐字节内容、帧边界和完成条件，因此其 FAIL 类别与局部监视器分别保存。[驱动脚本](../../../scripts/egg_frame_diagnostic_faults.py)

```python
from pathlib import Path
import sys

sys.path.insert(0, "scripts")
from egg_frame_diagnostic_faults import load_corpus

case = load_corpus(Path("results/milestone3/frame-diagnostic-faults"))["D02", "reset_epoch"]
rows, transaction_verdict = case["rows"], case["checker"]["verdict"]
```
