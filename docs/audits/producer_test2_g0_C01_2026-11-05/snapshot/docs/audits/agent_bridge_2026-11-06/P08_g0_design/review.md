# P08 — D01 G0 设计独立复核

结论：**PASS_WITH_LIMITS**。未发现当前可证实的实质风险。接受范围仅为封存 D01 的纸面设计一致性；没有证明 adapter、公开控制、monitor 或 DUT 正确。

仅写本目录 review.json 和 review.md；不修改共享文档、producer 文件、D01 快照或旧结果。

## 精确输入与新鲜核验

- phase-packet.json：5ea372987d85b83adb1cbab6cab67cebff486efa12bfd32176f006a30ce833cc。
- D01 phase.json：675b772099469ad64603093569e0796aa814d24f73feeadcb24026df8b193ee2。
- D01 snapshot-manifest.json：be07ee63e34dba49cee48750a6cfe230c61994b71925f8a9a85e406829288983。
- 18/18 封存成员 SHA 匹配；9 份设计文档和两份封存共享摘要均按 snapshot 审查。
- 44 个 FM 编号及 16 个 QC 编号完整；逐类人工阅读，并独立检查 Markdown/JSON 的 208 处字段文字一致。
- 16 个 actual_result 全为 null，source/waveform/independent_label 状态全为 NOT_CREATED_OR_NOT_QUALIFIED；两个模板的权限 false、入口 null、实际 run/artifact/grant null。
- 30/30 受保护来源 SHA 匹配（包括 P05/P06/P07 身份、已接受 source/tests/audit、E05 计划与原 P04 fixture）；未重新执行这些代码或审计。
- 实际 Git HEAD 为 c25180848ebfe9a1f49da0aa5f579cac913e6428；工作树有未提交/未跟踪内容，不用 HEAD 代表全部成果。
- 首次本轮 Git status 解析：195 项（4 tracked、191 untracked）。最终封存/当前文件比较见 review.json；未读取未封存实现内容。

完整成员 SHA、当前漂移、实际核验时间和命令/退出码保存在 review.json。JSON/文本检查是文档检查，不是 fixture 或资格实验。

## 逐项结论

| 设计要求 | 本轮判断与边界 |
|---|---|
| 身份与串行 | 显式 request/event/context 等身份、prompt bytes/messages/schema 分开绑定，旧字段缺失不补造。每 run 单 outstanding，交错不支持；仅纸面接受。 |
| 全局 halt | 跨 retry/round/session 持久；flags 或孤立 dispatch 均拒绝。合法 NOT_RUN 保留；pending-halt 返回只保留原始/成本证据，未资格为 UNRESOLVED，不恢复候选信用。 |
| 资源与 unknown | 完整性、科学归因、成本已知性分开；超帽拒绝，失败缺用量 null/UNKNOWN，subset 不双计，invoice/count fees 未知不填零。 |
| 清单与不可变 release | 模板明确不可执行；独立 grant、输入封存、全轮冻结后 hidden 评分、新 namespace 与路径边界、只追加证据及 sidecar 不回写均有要求。内容哈希不冒称独立历史锚。 |
| 跨表示语义 | VCD→literal→dual raw PRE/POST→rows→HEX/MON→reference 边界要求明确。width/signedness/guard/reset/phase 保留，缩宽必须仍有 selected bit，未知位不算 definite alarm。 |
| reference 与科学范围 | selected pre(S) 与 reference post(S−1) 分开；20 较早 prefix FAIL 不确认同样本/类别，74 未复现无参考 verdict。X→anyseq 个例不外推全部74，短 depth 不证明128completion。 |
| 独立角色及可见性 | Claude 作者与 fresh reviewer 负责新 oracle 合同；GPT 仅基础设施/组包。候选显式 allowlist，禁止 reference/hidden/calibration/maintainer/其他组历史，禁止按 C 收益选 profile。 |
| 44 案例 / 16 控制 | 失败、unknown、正例和不支持/空泛类分开；每类独立确认和停止条件保留。它们是纸面要求，无 source/waveform/标签/实测结果，不认作新增 DUT fault 或 RTL coverage。 |
| 历史与权限 | P04 原件 mismatch 订正准确，P05/P06/P07 限定范围、P05-N1 backlog 和所有科学未决保留。D01 false 权限未被后续授权改写。 |

精确依据见 review.json 的 checked_requirements；所有 design 路径均指 D01 snapshot，非正在推进的 live 文档。

## 非阻塞建议 P08-N1

**P3，material=false，blocking=false。** 来源：D01 snapshot 的 interface_spec.md:74、:77，SHA feaf74795ecc8e4dddef031de8987198a832ff69dbdf3bac6683ad4662dd67cd。

状态表把“matching error／缺 terminal”合写为“RUN_OPEN 或 EVIDENCE_GAP”。正文严格串行总则和 FM06/FM07 已禁止前一请求没有绑定 terminal/error 就再 dispatch，故未证实存在错误接受路径。这里的建议是减少未来局部照表实现时的歧义，不构成本阶段实质阻塞。

最小修订：在后续新版本拆开“已绑定 error”与“缺 terminal”；后者保留 EVIDENCE_GAP 和 outstanding 屏障。若另引入取消/终止语义，须显式登记和验收，不补造 terminal。

验收标准：后续封存版本明确缺 terminal 不恢复可派发 RUN_OPEN；获准后的轻量合成测试分别覆盖 matching-error 登记 retry 和 missing-terminal 后第二 dispatch 的拒绝。P08 未构造/执行该测试，也不要求改写 D01。普通 idle/safe checkpoint 转交即可，无需打断 producer。

## 保留限制与下一交接

- P05 仅当前保存格式/精确94链；P06 仅 ledger v2 严格串行格式/本批36calls144events；旧 audit_v3 不升级为通用 gate。
- P04 原件 v1 因 response/snapshot mismatch REJECT，不能称原样 PASS。补齐已存 response 的临时副本及独立 canonical 反例才证实旧 halt 缺陷/修复；serialization cause UNKNOWN，原历史 CHANGES_REQUIRED 保留。
- P05-N1 仍为 backlog；FM39 是新设计要求，未实现加固。
- F1、selected-sample/category、128completion/general soundness、H1/H2/L1、actual invoice/count fees UNKNOWN 和 R0/R1/R2 recovery planned 均未关闭。
- 16 控制仍需具体且独立固定的 width/type/guard/reset/phase、源码、波形和标签；未运行 G1 不是本纸面包伪造通过，也不构成已通过 G1。
- 未检查未封存 adapter/fixture 实现、运行时安全性、全历史原始链、4837 冻结成员的全内容或费用可行性。仅复用 SHA 未变的先前独立结论。

用户随后单独授权的 G0 adapter 与轻量合成 fixture，属于另一阶段和 namespace；不改写 D01 历史 false 权限。**本次文档 PASS 不授权 G1/native、monitor、API/count、data/candidate generation、paid/live 或 credential 操作。** 后续只审新 manifest，不评判未封存代码。

本轮没有实现/fixture 文件、测试、旧审计重跑、科学实验、API/count、key、安装、删除、commit/push、新 agent/chat 或跨线程消息。仅产生自己的复核文档。未发现问题不等于证明完全正确。
