# test2 Phase 1 — 2026-11-04

历史阶段记录：以下状态截至首次 Claude 调用之前。后续 checker 已生成并冻结；
请同时阅读 `reference-freeze-report.md`，不要把本阶段的“尚未生成”当作最新状态。

**状态：新实验已预登记，离线测量与 mock/replay 已完成；独立 Claude 参考
checker 尚未生成，未运行 live B′/C′，不存在本实验的模型效果结论。**

## 独立范围与不可变输入

原有仓库提交为 `acd220ace9c02a6b5f0d98bde15bcfaf70ae2a60`。
test2 是尚未提交的新工作，不能把上述 commit 当作包含 test2 的提交。
完整文件哈希与版本记录见 `phase1-artifact-manifest.json`。

| 项目 | 值 |
|---|---|
| 原始登记 SHA256 | `3f0b7f4ac81494849aa50368c52b1c59fd4396fbf7eee47ccb6f68e6a8e06869` |
| 输入 manifest SHA256 | `695dc87bfa8586211da2aa35b807254a2d754d05b6b93dcdaedeb1f74e208f63` |
| 实验 clean RTL SHA256 | `c46c18eb5f35489ed242d0e21fcea01e997c022356a21fae3ccb4f74a72288d0` |
| 范围 | sfifo，BW=8，深度16，同步高复位，异步 front read |
| 开发输入 | basic 9、boundary 45、wrap_reset 42 周期，共96 |
| 最终输入 | 三条隐藏序列 61、129、163 周期，共353 |
| 候选预算 | B′/C′ 各3会话×6轮，每轮6个属性槽；32k input/8192 output上限 |
| 独立控制 | 2个实现对应控制、6个预登记单点故障、20个有限 checker 控制 |

主研究对象是现有**人为构造等价冗余的 FIFO stress 变体**，不是新的自然 IP。
保持旧实验结果不变。新实验研究 monitor 生成，而非原来的 JSON 刺激优化。

模型可见源码删除了上游 FORMAL 断言块，保留其余每行及原始行号。
`source-sanitization-proof-v1/equivalence.log` 记录：未改动上游原版与 clean stress
变体在固定配置下的 **157/157 对应单元证明通过**。这是实现间对应证明，
不是 reference checker 已正确或 FIFO 全部规格已被证明。

## 实际完成的离线测量

`preflight-v2/` 保存了16次编译、96次DUT仿真、7,184个实际执行周期。
所有批次跑完，未因故障提前停止。每种实现/故障均使用相同六条输入。

- 两个正确实现的12个跨仿真器比较，在规定可观察范围内全部相同。
- 所有比较均没有两个已定义二值输出之间的矛盾。
- 19个故障/输入组合有 Icarus `X` 与 Verilator 具体二值的差异。这通常涉及
  故障导致未写存储被读出，不能隐藏成“两个仿真器完全一致”。见
  `cross-tool-audit-v1.json`。两态主评价与 Icarus 未知必须分别保留；还未
  经过 Claude oracle 确认这些组合的可评分故障资格。
- DUT 原始分母固定为400：line22、branch24、expr16、toggle338。
  含统一初始化/复位活动，排除 testbench；无等价类合并计数。

工具实际版本：Verilator5.050、Icarus12.0、Yosys0.70+post、SBY0.70、Z3 5.1.0，
egg0.11.0；Python环境的 OpenAI SDK2.54.0。Z3 使用已安装的命令行求解器。

## 语义与提示词

重新执行了现有 typed extraction、Rust egg 和独立 Z3 检查：egg5轮饱和，
30个 e-class、44个 e-node；六条重写的 Z3 XOR 均为 unsat。
五个原始 branch-if 计数仍分别映射：91/161，以及96/129/179。
另外两个 else 组未完整映射，不提供给 C′；两个不支持的抽取项明确保留。

B′/C′ 使用相同规格、clean RTL、完整开发观察及全400计数。
C′ 多两组已核验关系、完整 guard、类型和时钟上下文；没有故障见证或额外刺激。
源覆盖、复位及状态转移语义不会被等式饱和合并或证明。

提示词采用无损共享列字典，18对 mock 提示词逐一确认公共部分相同，区别
只有语义附录。初轮 JSON 序列化字节数 B′34,999/C′39,108；**字节不是token**，
尚未调用 provider token count。初版重复路径预览约121/125KB已留档，未调用模型。

## 监视器隔离和评分

候选 SV 只能观察公共输入输出并维护有界私有状态，通过6组 active/ok输出
报警。编译检查限制系统调用、层级访问、输入驱动、时钟变化与额外假设。
实际候选仿真使用独立 trace replay，不连接DUT，原始DUT计数不受候选影响。
时钟驱动/采样相位已用专门的有状态观察控制核对。

评分函数使用单独冻结的 oracle eligibility，而不是候选输出作为真值。
正确控制上的误报/未知会使 suite 失去主要有效检错分；无触发的故障留在报告。
原始报警、晚于规范违反的有效报警、不同 mutant 数、空检查和ROI分别记录。
所有最终候选哈希冻结之后才能进行隐藏最终评分。

19项自动检查通过，覆盖文件完整性、提示词隔离、数据集分离、单点变异、
禁止改写输入/系统调用、采样相位、误报/未知/空检查、ROI及缺失live freeze拒绝。
20个参考 checker 控制目前只是预先登记和结构核对，**还未由 Claude checker执行**。

## 实际 mock 与形式集成

`mock-v2` 与 `mock-replay-v2` 每次均完整运行36轮、72次编译工具调用、108次
监视器重放、3,456周期；每次新DUT仿真0、API调用0。mock故意使用恒假、
不激活和恒真监视器，不能当成LLM质量数据。`pipeline-audit-v1.json`核对了
逐轮提示词/响应、6个独立会话、最终候选哈希，并重新解析1,200条开发原始计数。

`formal-smoke-v1/` 中，恒真控制的 bmc/prove/cover分别PASS，恒假控制的bmc为FAIL，
符合预期。这些是**工具接线测试**，不是任何FIFO规格属性的完整证明。
正式评价仍需保留任务状态、深度、假设、反例和超时。SBY的有限深度检查与无界
证明是不同任务。[官方模式说明](https://symbiyosys.readthedocs.io/en/latest/reference.html)

## 失败尝试与限制

1. preflight-v1在完成等价检查后因缺少`flatten`关键字参数中止，无模型调用。
2. preflight-v2完成全部仿真后，原先“所有故障输出必须逐字段相同”的过严门槛
   因X差异中止；原证据保留。后续独立重分类未更改输入、故障或轨迹，明确记录
   X差异与真实二值矛盾。更新后的脚本未来输出此分类，不需要重跑已有96批次。
3. 初次单元测试发现schema字面量缺括号，已修复并完整重跑。
4. mock-v1/replay-v1是早期离线版本；v2补充分项成本和实际完成周期计数后重跑。
   这些开发成本不应计入后续live候选预算，也不能隐藏成只运行了一个mock。
5. 没有参考checker、独立复核、完整fault eligibility或live freeze；当前不能将
   输出差异直接记为规范缺陷，也不能开展最终候选评分。live SDK接口未在test2实测。
6. 一个合成冗余IP、六种人工故障和少量模型重复只能提供限定范围的探索性结论。
   无placebo，不能从B′/C′差异单独分离提示词长度与语义因素。

## 下一步

隐藏暂存Anthropic key后，Claude一次规格checker生成→独立有限控制和固定
正确/故障轨迹评估→全新Claude只读复核。作者不看RTL、隐藏输入、故障位置。
若不通过，保留失败版本并由Claude修订，不由GPT替换oracle。

通过后才冻结参考checker与可观察故障表，补齐并审计最终评分release编排，
绑定runner与所有证据哈希，最后请求OpenAI key运行新B′/C′。此阶段不会改动旧结果。
