# CVDP 多模块本地 EDA 实测

原始 RTL 不变；真实 Verilator 覆盖 + Icarus 输出交叉检查；没有调用 LLM API。

| 模块 | 初始检查/错误 | C 补测检查/错误 | D 补测检查/错误 | 扩展检查/错误 | C/D 刺激相同 |
|---|---:|---:|---:|---:|---|
| barrel_shifter | 2/1 | 3/1 | 3/1 | 4098/3562 | True |
| caesar_cipher | 2/0 | 3/0 | 3/0 | 4098/3015 | True |
| universal_shift_register | 2/0 | 8/0 | 8/0 | 12290/0 | True |

## 原始覆盖点统计

| 模块 | 阶段 | line | branch | toggle | expr |
|---|---|---:|---:|---:|---:|
| barrel_shifter | initial | 1/1 | 1/2 | 4/40 | 无此类计数器 |
| barrel_shifter | C-refined | 1/1 | 2/2 | 9/40 | 无此类计数器 |
| barrel_shifter | D-refined | 1/1 | 2/2 | 9/40 | 无此类计数器 |
| barrel_shifter | expanded | 1/1 | 2/2 | 25/40 | 无此类计数器 |
| caesar_cipher | initial | 3/5 | 无此类计数器 | 4/40 | 3/6 |
| caesar_cipher | C-refined | 4/5 | 无此类计数器 | 12/40 | 4/6 |
| caesar_cipher | D-refined | 4/5 | 无此类计数器 | 12/40 | 4/6 |
| caesar_cipher | expanded | 4/5 | 无此类计数器 | 37/40 | 4/6 |
| universal_shift_register | initial | 2/6 | 3/8 | 4/46 | 1/2 |
| universal_shift_register | C-refined | 5/6 | 8/8 | 10/46 | 2/2 |
| universal_shift_register | D-refined | 5/6 | 8/8 | 10/46 | 2/2 |
| universal_shift_register | expanded | 5/6 | 8/8 | 46/46 | 2/2 |

## 反馈机制诊断

| 模块 | C/D 反馈相同 | B/C/D 预览字节数 | egg 停止原因 |
|---|---|---|---|
| barrel_shifter | True | 8223/8223/8223 | Some(Saturated) |
| caesar_cipher | False | 10003/10003/10003 | Some(IterationLimit(20)) |
| universal_shift_register | False | 19939/19939/19956 | Some(Saturated) |

字节数不是 token 数。IterationLimit 表示有界搜索未完全饱和，不代表已发现全部等价关系。

## 解释范围

- 原始 CVDP 中 barrel/caesar 是 cid016 调试题输入，预期 checker 能发现错误；shift-register 是 cid004 增强题的原始输入，仅验证其现有端口功能，不测试尚未实现的增强要求。
- C/D 各自从 uncovered predicate 找有限具体输入域中的第一个 witness；相同候选顺序和补测预算，未手工加入仅供 C 使用的刺激。
- Caesar lower_path 在所有 8 位字符上不可达；2 位 mode 的 default 在二态输入上不可达。保留其原始覆盖分母。
- 桶形移位和 Caesar 扩展集枚举全部输入组合。移位寄存器枚举全部 256 个先前状态、4 种模式、2 个方向、2 个串行输入，每次先 reset/load；parallel_in 在 load 测试中遍历 256 个值，但并未穷举所有信号的笛卡尔积，也不是任意时间序列证明。
- 移位寄存器 checker 只检验稳定后时钟沿输出，不裁定同步/异步 reset 的文档差异。
- 计数器 raw hits 是工具事件数，不能作为测试向量数。没有 branch 计数器的模块按 line/expr 单独报告。
- 所有组原始覆盖身份不变。不能把 e-class 同类视为覆盖点已命中。
- 这些结果仅检验多模块工具链与反馈机制；不支持 e-graph 的 LLM 覆盖率、token ROI 或统计显著性结论。
