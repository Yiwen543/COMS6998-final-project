# 实施待办／权限清单（一页摘要）

当前仅 DESIGN_PREPARATION_ONLY；所有执行权限 false，entrypoint=null。表中是待办，不是下一条要执行的命令。

| 待办 | 已有依据 | 尚缺最小产物 | 客观验收／停止 | 角色 | 权限／资源状态 |
|---|---|---|---|---|---|
| 本文档独立复核 | P05/P06 的限定能力、P07 的 non-live 计划接受 | 既有复核流程对 D01 的纸面结论 | 只接受文档一致性；发现歧义只修新文档版本，不开额度 | 协调端＋既有独立复核 | 当前允许文档封存／检查；不得自行宣布独立通过 |
| G0 纯本地 schema/adapter | 本接口、清单、44 个纸面案例 | 明确实现范围、全新版本、代码／失败测试设计与输入锚 | 串行身份、持续 halt、unknown/成本分层可检验；不借旧硬编码路径或 P01 锚认证新 run | GPT 基础设施＋独立复核 | **需新的明确维护范围**；当前 implementation_allowed=false |
| G0 fixture 构造／执行 | 纸面失败矩阵和 16 类控制意图 | 获准后的非敏感合成 fixture、可复现拒绝／未决／正例证据 | 不写真实实验文件；不把合成控制当 DUT fault／RTL coverage；未知不填零 | GPT 基础设施＋独立复核 | **需明确 fixture 范围与执行许可**；当前 fixture_execution_allowed=false |
| G1 公共 native 资格 | E05 的资源帽仅提案；本轮只有控制定义 | 源／波形／独立标签、固定工具/profile/support matrix、真实结果与成本 | 支持类控制符合预定标签；不支持／空泛留范围，depth8 不外推 128；偏差即停 | 基础设施＋独立语义资格复核 | **需具体新的本地资源授权**；当前无 SV/harness/native/仿真/formal/monitor 许可 |
| G2 独立 Claude 合同 | 现 checker 只到较早前缀；GPT 不可扩 oracle | 公开合同、独立作者与全新会话复核包、新 oracle 版本及范围 | phase/category/finite deadline/fairness 明确；不得展示 hidden finals 或 GPT 候选答案 | Claude 作者＋Claude fresh reviewer；GPT 仅组包 | **NOT_READY**：模型/token/USD/时间帽未定；需具体新服务授权，当前不索 key |
| 新 data／B/C/P／release | 旧 11/11 饱和；B/C 只限整体反馈包 | 新登记任务／可达性／参考资格、固定 dev/hidden、模型与全资源帽；纯语义需另登记 token-matched P | 不按 C 结果调目标/profile；全部失败/unknown/分母/成本保留，评分前全轮冻结 | 基础设施、独立 Claude 参考、GPT 候选、独立评分 | **未授权**；旧 USD20 不沿用；无 data/count/generation/paid/live 入口 |

P05-N1 留 backlog；本轮不加固 helper。F1、H1/H2/L1、selected sample、128 completion 和 invoice/count fees 限制保留。真实服务需要时，应先形成精确请求数、模型、tokens/费用/时间帽和通过门禁的方案，由主聊天协调授权；愿意提供 key 不等于授权。当前不读取、恢复或处理 key，不创建后台任务、不创建新 review chat。
