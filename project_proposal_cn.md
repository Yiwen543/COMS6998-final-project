
#### 选题一：EDA-Tool-in-the-Loop Agent for Automated RTL Verification (闭环验证智能体)

*灵感来源：CVDP 论文指出 LLM 在编写 Testbench 和 Checker 时表现极差；课程强调 Agentic AI 需要反馈闭环。*

* **I. Problem and Motivation (问题与动机)**：
* **问题**：CVDP基准测试表明，最先进的LLM在生成SystemVerilog测试平台（Testbench）和断言时错误率极高（例如经常出现语法错误或时序不匹配）。


* **动机**：验证占据了芯片设计周期的绝大部分时间。如果能利用编译器/仿真器作为反馈，提升大模型在验证代码上的生成质量，将极大加速研发。


* **研究问题**：引入带有EDA工具仿真反馈（如 Icarus Verilog）的迭代式 Agent 框架，能否显著提升 LLM 在 CVDP 验证任务（cid12, cid13）上的通过率？


* **III. Proposed Approach (研究方法)**：
* 开发一个多轮对话 Agent。
* 第一步：让大模型根据设计规范（Spec）生成初始的 Testbench 代码。


* 第二步：Agent 自动调用开源编译/仿真工具（如 Verilator 或 Icarus Verilog）运行该代码。


* 第三步：收集编译错误或波形/日志信息，将反馈重新输入给 LLM 进行代码修正。




* **IV. Evaluation Plan (评估计划)**：
* 使用 CVDP 数据集中的 `Design Verification` 类别（cid12, cid13, cid16）进行测试。


* 对比基线（Baseline）：单轮生成的 Pass@1 成功率（类似论文中的原生 GPT-4.1 或 LLaMA 3.1 表现）。


* 指标：引入闭环 Agent 后的 Pass@1 提升幅度，以及平均修复轮数。



#### 选题二：Domain-Adapted RAG System for Open-Source EDA Script Generation (基于检索增强的开源EDA脚本生成器)

*灵感来源：ChipNeMo 证明了 RAG 在 EDA 脚本生成上的有效性；我们将其拓展到开源工具链。*

* **I. Problem and Motivation (问题与动机)**：
* **问题**：商业 LLM 缺乏对特定/小众 EDA 工具（如 OpenROAD, Yosys）底层 API 和 TCL 脚本语法的理解，导致生成的综合或物理设计脚本通常无法运行。


* **动机**：工程师花费大量时间查阅工具手册来编写 TCL/Python 流程脚本。


* **研究问题**：利用领域定制的 RAG（检索增强生成）系统，能否让开源 LLM 准确生成特定 EDA 工具的操作脚本？


* **III. Proposed Approach (研究方法)**：
* 复现 ChipNeMo 中的 RAG 思路。


* 收集 Yosys 或 OpenROAD 的官方文档、API 参考和开源 GitHub 脚本，构建向量数据库。
* 设计一个基于 Llama-3 的查询系统，当用户输入自然语言指令（例如“编写一段 Yosys 脚本来读取 Verilog 并映射到特定工艺库”）时，系统先检索相关的 API 语法，再进行代码生成。


* **IV. Evaluation Plan (评估计划)**：
* 构建一个类似于 ChipNeMo 中的 EDA 脚本评估小规模数据集（包含 Easy, Medium, Hard 任务）。


* 测试生成的 TCL 脚本在实际工具中运行的通过率（Pass@5 或 Pass@1）。





#### 选题三：RL-Based Design Space Exploration for Hardware Accelerators (基于强化的硬件加速器设计空间探索)

*灵感来源：Google 的宏单元布局论文展示了 RL 处理巨大设计空间的能力；课程核心主题涉及 Accelerator 和 SoC 的优化。*

* **I. Problem and Motivation (问题与动机)**：
* **问题**：硬件加速器（如深度学习 DSA）的设计空间（如缓存大小、PE阵列维度、内存带宽）巨大，传统的周期级仿真器速度太慢，无法进行全面探索。


* **动机**：寻找帕累托最优（Pareto-optimal）的设计配置是架构师面临的最大挑战之一。


* **研究问题**：能否利用类似 Graph Placement 论文中的强化学习（RL）思路，加速 AI 硬件加速器在特定工作负载下的设计空间探索（DSE）？


* **III. Proposed Approach (研究方法)**：
* 借用 Google 论文中将问题定义为马尔可夫决策过程（MDP）的思想。


* 环境（Environment）：使用开源的加速器仿真器（如 Timeloop 或 SCALE-Sim）。


* 状态与动作：状态为当前的架构参数配置；动作为调整缓存大小或计算单元阵列维度。
* 奖励（Reward）：使用仿真器返回的延迟（Latency）和能耗（Energy）的加权反比。




* **IV. Evaluation Plan (评估计划)**：
* 选择几个典型的深度学习算子（如 ResNet 的卷积层、Transformer 的 Attention 层）作为测试负载。
* 对比基线：随机搜索（Random Search）、模拟退火（Simulated Annealing，Google 论文也以此作为对比）。


* 指标：达到目标能效（TOPS/W）所需的探索时间，以及最终配置的性能得分。



### 工程师建议

从可行性和期末出成果的角度来看，**选题一 (Tool-in-the-Loop Agent)** 是最适合计算机系统/架构方向学生的。它不仅契合这三篇文献揭示的前沿痛点（CVDP中验证的极低通过率），还能充分利用课程教授对 "Agentic AI" 的期待。你只需要编写一层 Python 脚本包装开源 EDA 工具，再结合 OpenAI/Anthropic 的 API 即可实现原型，在学期末非常容易写出有图表、有对比的数据支撑（Artifact）。