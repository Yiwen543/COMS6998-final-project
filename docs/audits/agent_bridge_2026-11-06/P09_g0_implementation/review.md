# P09 — I01 G0 实现独立复核

**PASS_WITH_LIMITS。未发现当前可证实的实质风险或可复现的范围内错误接受。** 只接受本次精确 I01 版本的严格串行、显式身份、合成 JSON/text 元数据验证能力。不等于 DUT/oracle/monitor 正确、128 周期完成性、真实实验准入或未来执行授权。

没有实质 blocker，也没有需立即转交的建议；不需要中断 producer。没有发现问题不等于证明完全正确。

## 精确版本和保全

| 对象 | SHA256 |
|---|---|
| P09 phase-packet.json | 9646b4277b7ef942979e332b28e5d19c5fc6986b77d9e9b73b0399f932223eaf |
| I01 phase.json | 0b6b49b4ca1ae4ea55d172d08e6d8d5f3b90eb26b5ff44ca24a023c4ff5a5bbe |
| I01 snapshot-manifest.json | c49c8c409757322fe49c28142f77cad133fdf9407256e3dcb96ac3ffa2869eb6 |
| adapter.py | b19d188e3692e77b7c1dd9513b6d3e83778df5b86533563610eba33dfe279918 |
| schema.json | fe8d736e6aff38fb200fc6f38c0bb3ad67f2a667d3c3be66bc88e5ac42cbf1cc |
| test_g0_adapter_v1.py | 42a4b0987913d30d2a863711c29093fd5baf63f167910fd9d9a830fb6ad62f71 |

审查以 I01 snapshot 为准。实际 HEAD：c25180848ebfe9a1f49da0aa5f579cac913e6428；不以 HEAD 代替工作树成果。执行前后核验 8695 份封存文件、6 个 symlink 文本，均匹配；当前对应副本无漂移，41 份受保护来源不变。执行副本三份源 SHA 与 packet 一致，未生成 __pycache__。本次只写 P09 目录；P08/P08a、共享文档和 producer 文件不变。

所有输入与复核证据均由 review.json 和 evidence-manifest.json 绑定。

## 执行证据与计数

| 证据类别 | 本轮核验 | 结果 |
|---|---|---|
| Producer 历史自测 | 6轮共469例；最终93例 | 保留为 producer 证据，不直接代替独立验收 |
| Reviewer 新鲜最终套件 | 在 SHA 一致的 review-owned 副本执行93项 | 93通过，0失败/错误，约1.031秒，exit0 |
| 保存字节复现 | 各自 SHA 一致源码/格式逐例解析469个已存 I01 bundle；不重建六轮套件 | 469状态全部复现，输入绑定0失配；首轮8个预期/实际失败完整保留 |
| 独立新探针 | 独立改写/绑定，先复制再扰动，保存实际执行字节 | 28项均符合预期，无错误接受 |
| CLI/输出保全 | 新副本和 review-owned 输出、sentinel | 6控制符合预期；PASS0、UNRESOLVED2、REJECT1，覆盖/direct symlink/ancestor escape均拒绝且旧字节不变 |
| D01 映射 | 44项及94条 result/fixture-binding SHA链接 | 26元数据测试、12部分元数据、6范围外，标签与源码范围一致 |

保存结果复现仅有六处缺文件错误中的绝对路径变成 snapshot 路径；移除本地计时字段并显式规范化该路径后无其他差异。不是结果状态漂移。完整结果在 saved-byte-replay.json。

关键命令（均仅新 G0 合成范围，运行时设置 PYTHONDONTWRITEBYTECODE=1）：

- python3 .../P09_g0_implementation/exec_tree/test2/tests/test_g0_adapter_v1.py --record .../P09_g0_implementation/fresh-suite，exit0。
- python3 .../P09_g0_implementation/replay_saved.py，exit0。
- python3 .../P09_g0_implementation/independent_probes.py，exit0。
- python3 .../P09_g0_implementation/cli_controls.py，exit0。

完整真实路径、argv、退出码见 review.json/commands 与 cli-controls.json。新套件和独立探针的结果、fixture-binding、输入逐文件 SHA 均保留。每项独立探针的精确 fixture SHA 可查 independent-probes/summary.json；全部文件/脚本/执行源码/输出另由 evidence-manifest.json 冻结。已有 record 目录不能直接覆盖重跑；可使用新的 review-owned 目录，或用已复制 adapter CLI 的 --bundle 指向保存 bundle、--out 指向其 test2/results 下未占用的 g0-名称。

一次只读映射检查误用了不存在的 status/id 键，退出1；修正为 coverage_status/case_id 后44/94检查exit0。这是 reviewer 检查脚本错误，未改输入，不是产品失败。失败命令保留在命令记录中。

## 关键判断

**类型、身份与资源。** adapter.py:28、:41、:89、:123、:145、:185。检查了 closed-shapes、bool/int、null/必需字段、版本/占位符、重复JSON键/显式NaN、request/event/call/response身份与orphan、context/跨arm、prompt/messages/schema/source绑定、count→generation、model/tier、quota/retry/reserve、usage算术/subset。独立重算外层 SHA 后的 source/raw usage/cross-session parent-count 扰动仍被拒绝，说明测试覆盖的语义绑定不是仅比较外层摘要。未穷举所有输入或证明认证真实性。

**P08-N1 已获本版本独立行为证据。** adapter.py:160、:162、:180。12个组合覆盖 count/generation × retry/round/session × 缺terminal/匹配error：
- 缺terminal后第二请求6例，均 REJECT，原因 REQUEST_AFTER_MISSING_TERMINAL。
- 匹配error后合法继续6例，均保留原失败和费用缺口，完整性 UNRESOLVED；不会把 retry 的成功抹掉前面的未知成本。
- dedicated组合测试原先没有保存，producer已诚实披露；本轮新证据补足此行为验收，不回写冻结D01。

**持久 halt 与迟到用量。** adapter.py:166、:175、:223。新鲜套件覆盖 retry/round/session、flags及孤立dispatch；独立 late-usage-after-halt 保留已声明12tokens，仍 halted/UNRESOLVED/无候选信用。late-return-cannot-be-accepted 因 ACCEPTED_WITH_HALT 拒绝；halted-next-session 因 REQUEST_FLAGS_AFTER_GLOBAL_HALT 拒绝。没有因迟到返回恢复许可。

**unknown/费用。** adapter.py:117、:209、:261。失败或返回缺usage保持 null；cached/reasoning subsets 也保持 null，不能补零。已知subtotal与完整总成本分开；缺raw usage只得到 UNRESOLVED，invoice/count fee保持UNKNOWN/null。合法NOT_RUN保留无请求与null tokens。这里的tokens、model和reserve都是合成声明，不是provider事实。

**输出与输入保全。** adapter.py:65、:110、:267。新鲜套件与CLI负例核对inventory/hash/目录占用/路径/符号链接。REJECT报告保留，覆盖尝试不改变既有报告，两个symlink逃逸控制不改变sentinel。限定稳定本地文件系统，不宣称抵抗恶意并发竞态。

**科学范围没有升级。** adapter.py:238、:264。观测仅核验合成source/width/slot/reset/phase/reference-prefix声明。raw parsers、独立标签、reference执行均未提供且明确范围外；science固定NOT_EVALUATED。selected UNKNOWN 可以完整性范围内一致，但不获得definite alarm、同样本确认或正确性credit。G0接受不意味着完整实现D01科学链。

## 首轮失败与最终修复

首轮60例中8个失败的字节、result、fixture-binding和源码保留；用对应旧源码解析保存字节全部复现，没有为对齐审计而修原件。

- 可空ref：最终 adapter.py:45 在 ref 分派前处理null，独立新鲜套件和保存字节复现确认合法NOT_RUN/缺usage路径已纠正。
- test50：首稿 SHA=None 扰动被默认seal重算修复，保存实际是PASS，未被偷偷重标。最终 test_g0_adapter_v1.py:226 用 reseal=False，确实保留坏SHA且REJECT。
- 最终源码接受只绑定 attempt6 的93例及本轮证据；早期66/78/83/89通过不冒称都是最终三份源的新鲜测试。

## 保留的限制及权限

- 只支持 SYNTHETIC_FIXTURE/显式身份/严格串行/有限closed-shapes。真实或历史run、并发、原始科学链、opaque prompt隔离和真实own-history renderer不在本版验收范围。
- 哈希自洽不认证用户grant、provider、独立历史执行或invoice；offline grant记录不是live授权。
- P05仅当前保存格式/精确94链，P06仅当前严格串行36calls/144events；旧audit_v3未升级通用gate。P05-N1仍backlog。
- P04原件v1仍因response/snapshot mismatch REJECT，不能称原样PASS；补齐临时副本/canonical证据与其区分，serialization cause UNKNOWN。本轮不重跑P04。
- F1、selected pre(S)/reference post(S−1)及类别归因、20较早prefix FAIL/74未复现、128completion/general soundness、H1/H2/L1、实际invoice/count fees UNKNOWN、R0/R1/R2 recovery planned均未关闭。
- 未新鲜重哈希全部4837旧freeze成员内容；仅复用旧独立结论与核对本次41受保护来源/四个freeze manifest身份与成员名。
- 未调用原始checker、DUT/native/formal/simulator/monitor、模型/API/count/generation、网络或key；未安装、删除旧结果、commit/push、新建agent/chat、修改共享文件或联系producer。
- **本次接受不授权G1或任何未来native/科学/API/paid/live阶段。** 下一阶段须单独形成精确范围、授权和资格证据。

本轮有界G0审查结束；协调端可记录范围限定的接受，无需因潜在建议重开代码工程。

证据索引 SHA256：01df254c3b1ea5bee0fe56251777a34e5d25583dfd2d698f27ee4e2055df1f4e。
