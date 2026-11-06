# G0 设计准备包 v1

**DESIGN_PREPARATION_ONLY · 待既有独立复核 · 不是实现、registration、release、grant 或实验结果。**

本包只定义未来新版本接口、清单模板、失败矩阵和公开控制的纸面要求。`implementation_allowed=false`、`fixture_execution_allowed=false`；native、API、count、data、candidate generation、paid、live 权限均为 false，`entrypoint=null`。没有 adapter、解析函数、测试代码、fixture、SV、harness、波形、真实 rows 或独立标签。旧 USD20 授权已关闭，不能复用。

| 产物 | 文件 | 当前状态 |
|---|---|---|
| 接口与职责 | [interface_spec.md](interface_spec.md) | 纸面类型、身份、边界和状态表；没有运行时 schema/adapter |
| 不可变清单与生命周期 | [manifest_lifecycle.md](manifest_lifecycle.md) | 规则说明；模板不是真实记录 |
| 清单／release 模板 | [manifest.template.json](manifest.template.json)、[release.template.json](release.template.json) | TEMPLATE_ONLY_NOT_A_VALID_RELEASE；只含字段描述／占位，不可输入旧 validator |
| 失败矩阵 | [failure_matrix.md](failure_matrix.md) | 设计案例，未构造或执行任何 fixture／探针 |
| 16 类公开控制 | [public_controls.md](public_controls.md)、[public_controls.index.json](public_controls.index.json) | 纸面定义；全部 actual_result=null，源码／波形／独立标签未创建或未资格 |
| 实施待办及权限 | [implementation_permissions.md](implementation_permissions.md) | 只列未来工作；不能据此自动进入实施或 G1/G2 |

## 与既有验收的关系

P05 仅接受 companion 对当前保存格式／精确 94 条链的能力；P06 仅接受 ledger v2 的全局 halt 修复及严格串行格式／本批 36 calls、144 events。P07 仅接受 E05 文档／sidecar／non-live 计划一致性。旧 audit_v3 未改变，也不升级为通用新 run gate。此设计包本身尚未获独立接受，更没有工具或科学资格。

历史身份缺失不能补造：旧 count/returned/error 没有 request ID/context 时，只能保留受限串行位置绑定及其缺口，不能生成看似真实的新身份。未来格式应在写事件时显式提供身份；新增格式与 adapter 须新版本、单独实现／测试／验收。

P04 原件在 v1 原样执行因 response/snapshot mismatch 而 REJECT，不得再称“原样 PASS”。临时副本仅补已有 accepted response 绑定后可复现 v1 PASS／v2 persistent-halt REJECT；独立 canonical 反例也确认缺陷成立。原 P04、历史 CHANGES_REQUIRED 保留，序列化差异原因 UNKNOWN。

P05-N1 仅为 backlog，本包不修代码。F1、H1/H2、L1、selected pre(S)／reference post(S−1)、128 周期完成性、一般 monitor soundness、计数费／实际 invoice 仍未关闭。20 个物理报警复现／较早前缀 FAIL 不升级为同样本确认；74 个未复现仍无参考 verdict，不能称 oracle UNKNOWN、已确认误报或统一归因 X 转换。

## 本轮检查与交接

只允许文件边界、冻结成员**名称**检查、SHA、JSON 语法／占位／字段一致性和 Git 状态检查。文档检查成功仅表示文档结构可读，不表示 adapter、fixture、控制、DUT、native、monitor 或 128 周期正确性通过。文档封存的实际路径／SHA 是文档来源证明，与带占位符的实验清单模板性质不同。

D01 交接放在 `docs/audits/producer_test2_g0_D01_2026-11-05/`。保持本包稳定，交由协调端送既有独立复核流程；不创建新 review chat，不自行宣布独立通过。若需修订，新增设计版本；不改变执行额度，不修改 E05 计划／draft／sidecar 或封存快照。
