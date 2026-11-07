# Queue 固定 property 义务草案 v2

状态：`DRAFT_NO_EXECUTE`。仅更新独立 property/monitor 的语义义务；没有可执行 monitor、golden、证明或实际测试。v1 保留不动。唯一角色仍为固定 property/monitor 规则作者，独立于未来 Claude golden 作者、实验刺激生成者和最终复核者。

## 输入与采用边界

技术输入仅为公开规格 `examples/heldout_queue/docs/specification.md`（SHA256 `cf439779a935805e5717cb51c26dd3dec605c729a83154e57a17dd9c6ad2ed51`）和共同合同 `docs/designs/queue_efficiency_contract_v1.json`（SHA256 `229ab3b3d99c597bba92a367e7697ef39bc1c039098b395382773cff9b94cc64`）。共同合同文件仍标为 `PROPOSED_COMMON_BENCHMARK_CONTRACT_NO_EXECUTE`；本稿按任务明确采用其中语义来写基准草案，不把它视作执行授权。

共同基准采用 `DEPTH=4, DBITS=32, C_eff=3`，有效元素工作负载上限也是 3。工作负载限制与有效 full 阈值是两个不同合同项；数值相同不构成从公开规格证明物理容量的证据。`C_eff=3` 以及下述空态同时读写解释均为显式基准假设，不是 DUT 推定的完整原规格真值。两种 RTL 写法属于同一 IP，分别对相同合同检查；互相一致不能替代合同正确性。

动作必须恰有 `reset_n/clear/enable/write/read/data` 六字段。控制值严格为整数 0 或 1；data 严格为整数 `0..4294967295`，按 32 位无符号位向量解释；拒绝布尔、浮点、字符串、缺失或额外字段。实验 GPT 只输出 JSON 动作，不生成 oracle 或 grader。用动作历史独立得到的有序抽象序列 `Q` 和 `n=len(Q)` 定义合法性与期望值，始终保持 `0<=n<=3`，不得用 DUT flags 更新历史。

初始必须先建立低有效异步复位；此前观察为未初始化未知。复位域为 `reset_n=0, clear=write=read=0, enable∈{0,1}`。同步 clear 域为 `reset_n=1, enable=1, clear=1, write=read=0`。正常状态为 `reset_n=1, clear=0`：禁用时允许任意二进制读写组合且均不接受操作；启用 idle 保持；单写仅在 `n<3` 合法，单读仅在 `n>0` 合法；启用同时读写在 `n=0..3` 均为合同内操作。

空态单读、满态单写、禁用时 clear、clear 与读写冲突、reset 与 clear/读写冲突均排除。保留 `INVALID_OR_UNSUPPORTED`，不丢弃、不自动改写动作，也不因 DUT flags 错误而把合同内动作排除。空队列的物理 `q_o` 不评分；almost 两标志只记录值及 knownness，阈值和比较关系没有采用，不能给功能验证信用。

## 七组固定语义义务

除 P1 的复位建立过程外，下表每项都要求已初始化、schema 合法、动作在上述域内。`pre` 是该动作上升沿前的稳定观察，`post` 是上升沿时序更新及组合输出稳定后的观察。每项完整守卫决定激活；禁用读写不能激活 P4/P5/P6。

| ID | 完整激活条件 | 期望关系与外部观察 |
|---|---|---|
| P1 异步复位 | `reset_n=0, clear=write=read=0, enable∈{0,1}`，且 ABI 记录实际断言事件 | 上升沿之外断言复位后的 `reset_settle` 即为 `Q=[]`、empty=1、full=0；保持复位期间及上升沿后仍如此。断言前的有效数据被遗忘。不比较空态 q 的数值；仅有 post-edge 观察不能验证异步性。 |
| P2 同步 clear | `reset_n=1, enable=1, clear=1, write=read=0` | clear 驱动稳定后、上升沿前仍按旧 `Q_pre` 检查；post 为 `Q_post=[]`、empty=1、full=0。清除后未来操作按新的空历史判断。 |
| P3 保持 | `reset_n=1, clear=0`，且 `enable=0` 或 `write=read=0` | `Q_post=Q_pre`。状态标志不变；若 `n>0`，pre/post 头部均为 `Q_pre[0]`。禁用且 write=read=1 也适用本项，不能被当作一次同时操作。 |
| P4 合法单写 | `reset_n=1, clear=0, enable=1, write=1, read=0, n<3` | `Q_post=Q_pre ++ [data]`。原非空则头部不变，原为空则 post 头部等于 data。`n=2` 写后 n=3，full=1；写入顺序由后续所有合法观察约束。 |
| P5 合法单读 | `reset_n=1, clear=0, enable=1, write=0, read=1, n>0` | pre 头部为被移除的 `Q_pre[0]`；`Q_post=Q_pre[1:]`。若 post 非空，稳定输出立即为新头部，不再等待另一个时钟；若 post 为空，q 不比较。`n=3` 读后 full=0。 |
| P6 合同内同时读写 | `reset_n=1, clear=0, enable=1, write=read=1, 0<=n<=3` | 若 `n>0`：pre 头部为 `Q_pre[0]`，`Q_post=Q_pre[1:] ++ [data]`，占用不变。n=1 时 post 头部为 data；n=2 或 3 时为旧第二元素，追加的数据保持在尾部；n=3 也合法且 full 保持 1。若 `n=0`：采用 `Q_post=[]`，empty=1、full=0；本次 data 不加入逻辑历史，空态物理 q 不评分，也不得在以后作为有效元素出现。 |
| P7 状态与有效头部 | 每个已初始化且处于合同内状态的 pre/post/reset 稳定点；复位使用 P1 的空状态 | `empty_o==(n==0)`、`full_o==(n==3)`；两者不能同时为 1。只要 `n>0`，q 必须为已知 32 位值且等于 `Q[0]`；空态不比较 q。标志比较所用 n 始终来自历史，不能由 DUT 自报。 |

P4/P5/P6 的序列等式是 property 的数学定义，不是本作者实现的 golden。它们共同约束有效前端数据、FIFO 顺序、fall-through 和满空转换；不要求读取内部指针或存储。P6 空态行为是共同合同明确采用的解释：公开规格的“直接写入 index 0”可以涉及未评分的物理空头部，本稿不据此推定一个有效元素。未发现共同合同在上述抽象域内的文本矛盾；这不证明实现或原规格一致。

## ABI 与结果保留

ABI 仍未冻结。至少记录实现/trace 标识、动作索引和六字段原值、驱动与边沿事件顺序、`pre_edge`、`post_edge`、上升沿之外复位断言后的 `reset_settle`，以及 `q_o[31:0]`、`empty_o`、`full_o`、`almost_empty_o`、`almost_full_o` 的值和逐位 knownness。驱动相位、采样区域、settle 规则及复位安全释放相位必须具体冻结，不能以只在时钟边沿采样冒充异步检查，也不能把 X/Z 转成 0。

逐动作、逐计划观察、逐义务保留激活与原因。schema 错误或排除域保留 `INVALID_OR_UNSUPPORTED`；未初始化、缺失观察、必要输出 X/Z、缺少规定采样相位分别保留 `UNKNOWN_UNINITIALIZED`、`MISSING_OBSERVATION`、`UNKNOWN_OBSERVATION`、`UNSUPPORTED_ABI`。已知且激活的关系不符为 FAIL；全部必要位已知且匹配才为该激活义务的 PASS。未激活、未支持或未知不算成功；FAIL 与 UNKNOWN 可以并存，不能互相覆盖。空态 q 的未激活不能掩盖 flags 的失败；almost 没有功能信用。所有尝试、失败和成本记录保留，不用过滤后的运行数替代原始分母。

## 最小剩余工作

下一步仅需具体冻结 ABI 与公共合同版本，再由另一名独立 Claude 作者仅据相同公开规格、共同合同及冻结 ABI 编写 golden；该作者不看本 property 源码。本规则后续另行实现为固定 monitor，并由独立“复核test2项目”线程复核。实验 GPT 继续仅生成 JSON 刺激。

实现规模仍为最多三个 32 位有效元素的历史、七组比较和结果原因记录，加动作/观察适配；无需新框架或庞大 SVA 套件。运行、编译及外部作者费用仍未知。本阶段只做文档/JSON/哈希静态核对，无 monitor 实现、测试、编译、仿真、formal、API 或付费调用。
