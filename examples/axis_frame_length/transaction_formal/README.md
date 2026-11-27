# AXI 帧调整器的事务级有界证明

在每次复位之间最多开始一帧、最多接受 12 字节的条件下，Yosys SAT 联合检查了完整 `frame_task` 上的 8 项事务安全性质。**18 个状态全部通过**。输入字节、帧尾、两个下游的 ready 信号和初始周期之后的复位均由求解器选择。六个覆盖见证都在 Icarus 上命中了求解器报告的同一周期。[结果摘要](../../../results/milestone3/frame-txn-formal/summary.json)

## 安装和复现

实验使用 Python 3.12.14、Yosys 0.52、配套的 `yosys-smtbmc`、Z3 4.16.0 和 Icarus 12.0。可在提供 Yosys 0.52 与 Icarus 12 的 Linux 发行版上安装工具，例如 Debian trixie。Yosys 需支持 `chformal -lower`。从仓库根目录运行以下命令。结果目录应使用新的路径。

```bash
sudo apt-get install yosys iverilog python3-venv
python3 -m venv /tmp/frame-txn-env
source /tmp/frame-txn-env/bin/activate
python -m pip install z3-solver==4.16.0.0
yosys -V
z3 --version
iverilog -V
python scripts/m3_controller_replay.py --fetch /tmp/frame-txn-fixture
python scripts/egg_txn_formal.py --fixture /tmp/frame-txn-fixture --output /tmp/frame-txn-reproduced
```

已配置的 Milestone 3 实验环境可以直接运行 `source /tmp/m3-tools/env.sh`，并使用已有的 `--fixture /tmp/m3-controller-rtl`。下载器校验上游提交中四份 RTL 源码和冻结事务检查器的 SHA-256。实验脚本在临时目录中编译原始 RTL 和两份受控改动，保存编译哈希、Yosys 日志、原生 `.yw` 见证，以及 Icarus 边沿前后的原始四态引脚值。[驱动脚本](../../../scripts/egg_txn_formal.py) · [源文件清单](../../../scripts/m3_controller_replay_manifest.json)

## 检查了哪些行为

记分板只读外部握手信号。输入每次被接受时累加字节数，接受 TLAST 时记录帧已结束。数据和头信息按各自实际发生的握手独立推进。检查发生在输出被呈现时，包括下游阻塞的周期。为验证全部保留字节，记分板使用一个固定、任意的三位索引，在对应输入字节被接受时记录其 8 位内容；一次联合证明覆盖该索引的全部 8 种取值。[SystemVerilog 记分板](frame_txn.sv)

| 性质 | 获取报警的条件 |
|---|---|
| `data_entitlement` | 输出字节没有已接受的输入字节或短帧所需的填充作为依据，或帧已输出完毕 |
| `data_payload` | 保留字节与输入不同，或填充字节非零 |
| `data_last` | TLAST 与预期输出帧尾不符。尚未接收输入帧尾时，第 8 个已获准呈现的字节是截断边界 |
| `header_entitlement` | 输入帧尚未结束，或对应头信息已经被消费 |
| `header_original`、`header_adjusted`、`header_flags` | 头信息与实际接受的输入长度、夹紧至 4–8 的输出长度、短帧及长帧标志不符 |
| `reset_clear` | 同步复位边沿后的状态仍显示任一输出 valid，取样点为下一拍 PRE |

输入源在阻塞期间保持 valid、data 和 last，复位可以打断尚未完成的传输。此证明的时间范围是从初始复位开始的 18 个状态。多帧游标排序、有限尾段的 `drain_complete`、无界活性和四态 X 传播由其他实验分别处理。本实验独立手写这八项规范断言；模型提交的表达式和 egg 的域内等价证据有各自的评分记录。

## 正向覆盖和变异对照

| 覆盖事件 | 首次命中步号（从 0 计） |
|---|---:|
| 呈现非零保留字节 | 6 |
| 呈现填充字节 | 7 |
| 复位冲刷尚有输出的设计，随后两路 valid 均为 0 | 7 |
| 数据阻塞时头信息握手 | 9 |
| 头信息阻塞时数据握手 | 9 |
| 呈现长度超过 8 的已完成输入帧头 | 14 |

Icarus 使用求解器给出的顶层引脚逐拍重放。独立的冻结 Python 检查器对全部六条原设计覆盖轨迹给出 PASS。F01 把填充值改为全 1，第 7 步观测到 `m_data=255`，预期为零。F06 断开头 FIFO 的复位，第 9 步呈现上一复位周期的头信息，此时新输入帧尚未完成，触发 `header_entitlement`。两条反例使用相同激励重放于原设计时均通过。归档分别保留了原设计和改动后的 Icarus 波形文本。[重放测试平台](replay_txn.sv) · [F01](../../../results/milestone3/frame-txn-formal/F01/) · [F06](../../../results/milestone3/frame-txn-formal/F06/)
