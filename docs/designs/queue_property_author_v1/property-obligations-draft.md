# Queue 固定 property 义务草案

状态：`DRAFT_NO_EXECUTE`。本稿仅定义待采用的语义合同与观测需求；没有可执行 monitor、golden、证明或实际测试。作者仅为独立固定 property/monitor 规则作者；后续 golden 由另一名独立 Claude 作者制定，最终复核由独立“复核test2项目”线程承担。

唯一技术依据为 `examples/heldout_queue/docs/specification.md`，SHA256 `cf439779a935805e5717cb51c26dd3dec605c729a83154e57a17dd9c6ad2ed51`。维护恢复文件只用于权限和边界，不用于制定 queue 语义。本稿不自动进入实验 GPT prompt；实验 GPT 的产物仅为 JSON 输入动作。

## 待采用的小范围合同

研究对象是同一 queue IP 的两种 RTL 写法，各自对同一固定合同判定；两者互相一致不能替代合同正确性。以下均为草案，须与独立 golden 作者、infra 和复核者共同冻结后才能执行。

- 数据宽度采用 32 位无符号位向量；动作字段为 `reset_n/clear/enable/write/read/data`。五个控制字段仅接受整数 `0/1`，`data` 仅接受整数 `0..4294967295`；布尔、浮点、字符串、缺失值和额外字段如何处理须在 JSON schema 中固定，建议全部拒绝。
- 用抽象序列 `Q` 表示按合法动作历史得到的有效数据，`n = len(Q)`。有效元素上限 `L = 3` 是工作负载限制，**不是**从公开规格推定的物理容量或 full 阈值。初始动作必须建立低有效复位；初始化以前的观察不作有效性成功证据。
- 必须另外明确采用有效满阈值 `C_eff >= 3`、对应参数配置及 `full_o := (n == C_eff)`。公开规格未给出 `DEPTH` 与内部 full 阈值的唯一数值关系，不能令 `C_eff = 3` 或直接令其等于 `DEPTH`。若该假设不能采用，本草案保持未决，不能从 RTL 反推答案。
- 正常启用时仅纳入 idle、合法单写和合法单读：单写要求 `n < 3`；单读要求 `n > 0`。禁止第四个有效元素、空读及启用状态下同时读写。合法性由动作历史决定，不能由 DUT 的 empty/full 输出来决定。
- 复位动作要求 `clear=write=read=0`，`enable` 可为 0 或 1；复位异步生效。同步 clear 动作要求 `reset_n=1, enable=1, clear=1, write=read=0`。`clear=1, enable=0` 及 clear 与读写冲突均不纳入本合同；公开规格没有明确给出这些优先级。
- 正常 `reset_n=1, clear=0, enable=0` 时允许任意读写控制组合，包括两者同时为 1；它们不构成已接受操作，队列保持。`enable=1, clear=0, write=read=0` 也保持。
- 空队列的 `q_o` 数值不在本合同内；公开规格没有明确写出复位数值，不能默认为零。almost 标志的有效阈值、比较方向/等号及边界钳位均未唯一规定，暂不判定。仍保存这些输出和未支持原因。

公开规格描述了同时读写时占用不变及空时直接写入头部，但未唯一确定边界接受规则及其与 full 的关系。本轮默认排除启用状态下的同时读写；若以后纳入，应另立明确合同和版本，不借用旧实现、旧 checker 或旧结果消除歧义。

## 最小固定语义义务

下表中的 `Q_pre` 是由已采用合同和先前动作得到的抽象状态，完全独立于 DUT 输出；`Q_post` 是本行定义的期望后继。只比较外部可观察行为，不读取内部数组或指针。

| ID | 完整激活条件 | 期望关系与比较点 |
|---|---|---|
| P1 复位清空 | 已按 ABI 在上升沿之外断言 `reset_n=0`，其余控制符合复位动作约束 | 在复位断言后的稳定、且尚未发生上升沿的 `reset_settle` 观察：`Q=[]`, `empty_o=1`, `full_o=0`。复位持续至上升沿后仍如此。仅有 post-edge 观察不能验证异步性。 |
| P2 同步 clear | 已初始化，`reset_n=1, enable=1, clear=1, write=read=0` | 驱动 clear 后、上升沿前仍按旧 `Q_pre` 检查；上升沿后的 `Q_post=[]`，empty=1、full=0。clear 后的读写必须按新空队列重新建立合法历史。 |
| P3 保持 | 已初始化，`reset_n=1, clear=0`，且 `enable=0` 或 `write=read=0` | `Q_post=Q_pre`；pre/post 的 empty/full 按同一占用判定。若 `n>0`，两处头部都必须是 `Q_pre[0]`。不约束空队列的 q 数值。 |
| P4 单写与 FIFO 顺序 | 已初始化，`reset_n=1, clear=0, enable=1, write=1, read=0, n<3`，且已采用 `C_eff>=3` | `Q_post=Q_pre ++ [data]`。若原来非空，post 头部不变；若原来为空，post 头部等于本次 data。后续合法读取须暴露整个已写序列的顺序。 |
| P5 单读与 fall-through | 已初始化，`reset_n=1, clear=0, enable=1, write=0, read=1, n>0` | pre 头部为被移除的 `Q_pre[0]`；`Q_post=Q_pre[1:]`。若 post 非空，稳定后的输出立即等于新头部，不额外等待另一个时钟；post 为空时 q 不比较。 |
| P6 状态与有效头部 | 已初始化且该观察对应合同内的稳定状态；复位观察使用 P1 定义的状态 | 每个 pre/post/reset 稳定点：`empty_o == (n==0)`；采用 `C_eff` 后 `full_o == (n==C_eff)`；只要 `n>0`，`q_o == Q[0]`。empty/full 不得同时为 1。不得用 DUT flags 覆盖 `n`。 |

P4/P5/P6 中的历史序列只是 property 的数学定义，不是本作者编写的可执行 golden。复位和 clear 会遗忘此前所有有效数据；不检查不可观察的物理存储位。若 `C_eff>3`，本轮不触及实际 full 状态；若 `C_eff=3`，可观察 full 的进入/退出，但仍不验证满时写入。每项只在上述完整守卫下激活。

## 待冻结的 observation ABI

至少需要 trace/实现标识、动作索引、驱动的六字段原值、时钟边沿/相位、复位断言和释放的事件顺序，以及 `q_o[31:0]`、empty/full/almost 两标志的值和逐位 knownness。不能把 X/Z 静默转为 0；不要求内部状态或 DUT 提供的有效信号。

每个正常周期需要输入稳定后的 `pre_edge` 以及该上升沿的时序更新和组合输出均稳定后的 `post_edge`；必须固定驱动、采样区域及 settle 规则。clear 在 pre 尚未生效。异步复位另需上升沿之外断言后的 `reset_settle` 观察；仅按每周期 JSON 存储 `reset_n` 而没有该相位不足以验证 P1。复位释放须在规定的安全驱动相位完成，再采样正常周期。若 ABI 尚不支持某相位，该义务标为 `UNSUPPORTED_ABI`，不得改写为较弱规则并称原义务已验证。

## 保留结果与下一步

每条输入、每个计划观察及每项义务保留激活/未激活及原因。schema 错误为 `INVALID_INPUT`；域外操作为 `UNSUPPORTED_OPERATION`；阈值未采用为 `UNRESOLVED_CONTRACT`；未初始化、缺少观察、必要位 X/Z、缺失相位分别为 `UNKNOWN_UNINITIALIZED`、`MISSING_OBSERVATION`、`UNKNOWN_OBSERVATION`、`UNSUPPORTED_ABI`。已知且激活的等式不符才是该义务的 `FAIL`；完整激活且必要位均已知并匹配才是该义务的 `PASS`。空态 q 的不比较为明确未激活，不能掩盖 flags 的失败。未知与失败可同时存在，逐项保存；不能因已知失败而删除未知，也不能把未知、未支持或无激活计为成功。所有尝试与成本记录保留，不以过滤后的集合替代原始运行数。

执行前最少还需：明确采用 `C_eff` 和参数配置；确认输入 schema/合法域；冻结 pre/post/异步复位 ABI；由独立 Claude 仅据相同公开规格、采用合同和冻结 ABI 编写 golden；另行实现固定 monitor，并交独立线程复核。两名作者不得借用对方方案来消除未决语义。

最小实现规模是一个有界三元素的动作历史、上述六组比较与结果原因记录，再加已有 infra 的动作/观察适配器；每步工作量为常数上界，抽象有效载荷最多 96 位。无需新测试框架或庞大 SVA 套件。实际运行/编译成本、golden 作者费用及验证耗时均未知，本稿不报价、不触发执行。当前仅进行了文档与 JSON 的本地静态核对，没有编译、仿真、formal、API 调用或付费实验。
