# P01 独立阶段复核

结论：**CHANGES_REQUIRED**。catalog适配修复和输入隔离诊断的保存证据可确认；最终形式报告仍需补充实际native/physical不一致及X→anyseq实例。没有发现当前固定轨迹主分数错误或冻结破坏。

- Manifest SHA256：`9eb5cbee8de1d2a6d4c81716b79ea9a12db63033156e207caec4b426c018bf2e`；23/23快照匹配。
- 实际HEAD：`c25180848ebfe9a1f49da0aa5f579cac913e6428`；工作区未提交，HEAD不能标识全部成果。
- 只写本轮review.json/review.md；没有新实验、重放、API、安装、删除、commit或push。精确冻结checker纯函数仅分析保存的rows。

## 核验结果

- audit_v3相对v2只改变fault source查询。12个catalog ID/hash与注册一致，540套实际DUT/候选源副本一致；v2失败日志保留。
- 540项native：361TIMEOUT/104FAIL/75PASS；104FAIL分为94BMC、7prove、3cover。无NOT_RUN_TOTAL_CAP；每final90项。10s/5s、depth24、trace_done0和720s总预算未改。
- 全94条BMC链从原始VCD、literal输入、两个物理PRE/POST日志、rows、MON位核验。20条报警物理复现，冻结参考纯函数重判其保存较早前缀全部FAIL；74条未复现且保留unresolved，均来自C（7correct、67mutant）。它们不等于参考已经判UNKNOWN，也不能叫物理候选误报。
- 核对188次保存物理执行/1246周期，94条保存MON日志/623周期；没有新的工具执行。物理前缀mutant union B={N01,N04,N09}，C={N01,N04,N05,N06,N07,N08,N11}，仍不归因到参考同样本selected alarm。
- 输入隔离：9个输入freeze成员、18个physical-freeze成员、4处composite改动匹配。4构建/4仿真/600周期；24条保存MON日志/3600周期。六final均正确控制无报警，blocked控制仅终点报警，同时保留drain_tail_short unknown。该控制是在候选冻结后登记的事后诊断，不是自然新mutant、独立LLM样本、RTLcoverage或旧分数更正。
- 36calls/144ledger事件逐条一致：36唯一response_id及prompt/context/count/usage/model/tier匹配。1475813input+78479output=1554292tokens；费率算术USD4.1022157，非账单，count实际费用未知。
- 36x162=5832计划case保留；B1round4 invalid保留162unresolved。六final correct gate通过、11类型；B2未决40，其余38。保存live/replay摘要一致。
- 四套freeze4837次成员检查与fresh acceptance2613绑定均0缺失/失配；两旧score与Claudechecker SHA不变。git diff --check exit0。

## F1–F6 状态

| 原ID | 当前状态 | P01影响 |
|---|---|---|
| F1 | 实际表示限制保留；bridge拒收正确，报告缺74/7分层和X实例 | 阻塞最终形式报告披露 |
| F2 | 历史252条漏未决；当前v4已纳入oracle unknown | 不阻塞，不是当前主分数错误 |
| F3 | 旧offline acceptance分类覆盖限制 | 历史限制，不阻塞 |
| F4 | 自动producer审计缺口未改；P01独立核验本批全部保存见证 | 当前数据获支持，自动审计能力需限定 |
| F5 | returned/calls自动绑定缺口未改；本批逐条匹配 | 当前数据不阻塞 |
| F6 | 共享冷缓存仍在；26构建共30.548166s，最慢final652.091561s且全部跑完 | 无本批总预算截断，未来注册限制 |

## P01-R1 · P1 · 最终形式报告未显式披露实际 native/physical 不一致及 X 表示实例

- 状态：`OPEN_REPORTING_CHANGE_REQUIRED`。
- 证据：全部94条保存BMC链已独立解析：20条报警物理复现，冻结参考对20条较早前缀均判FAIL；74条报警未复现且保留unresolved，均来自C（7 correct＋67 mutant）。C1/P4的字面X检查被转换成setundef-anyseq已逐文件确认。报告只混列全部formal状态，未列74/7分层及此具体前端限制。
- 影响：native FAIL及时间差异不能只解释为候选能力。报告已正确限定物理前缀union，但遗漏实际臂相关表示限制。此问题不推翻固定轨迹11/11主结果，也不否定20条真实物理前缀FAIL。
- 建议：另建报告/分析版本，显式区分native BMC FAIL、物理报警复现、未复现、参考前缀判定、correct/mutant及bmc/prove/cover。披露具体X实例；不要把所有74条都归为同一根因。保留旧报告、候选和状态。
- 验收：
  - 报告列出94 BMC FAIL＝20物理复现＋74未复现，后者含C correct7/mutant67；prove FAIL7和cover FAIL3分开。
  - 链接C1/P4 SV/SMT原始证据；选定报警与参考同样本归因仍为unresolved。
  - B3/C7 distinct physical-prefix union只作为次级诊断；固定轨迹分数不变。
  - 新版manifest绑定实际分析/报告源与不变原始证据；无需任何新DUT/formal/monitor重放或付费调用。
- 精确位置和SHA：
  - `test2/results/controller-done-live-report-v3/report.md` · lines 50–63 · SHA256 `0331bb80058aab8a08736f513d7a3f65fe326b74a498ee26806f59a68c158c92` · P01 snapshot
  - `test2/scripts/controller_done_live_report_v3.py` · lines 20–23 · SHA256 `ad331d664c60aa7c8fbc3e0409ea2e649fe86c15a51bc76470692128f681d36e` · P01 snapshot
  - `test2/results/controller-done-live-v2/C2_semantic/rep1/round6/compiled/candidate.sv` · line 73 · SHA256 `7368aa0e874468b520a03da1282031b4277f7ac5147fa9b9f1db46b3fdde74be` · saved dependency hashed independently
  - `test2/results/controller-done-live-formal-v2/C2_semantic/rep1/correct/P4-bmc/work/model/design_smt2.smt2` · lines 85–89,1229 · SHA256 `6b4ad28604b4b02d605e0889438eae9f27dfbbf66d68a7d39f0a1d3d08f135af` · saved dependency hashed independently
  - `test2/results/controller-done-live-formal-v2/C2_semantic/rep1/correct/P4-bmc/physical/result.json` · status/detail · SHA256 `935a5c5723eec13bf2d90a55e5dab4d0b779263d7e65287ce5891caa13925231` · saved dependency hashed independently

## P01-R2 · P2 · 自动 live audit 仍未闭合形式物理见证原始链

- 状态：`PRODUCER_AUDIT_GAP_OPEN_CURRENT_DATA_INDEPENDENTLY_CHECKED`。
- 证据：v3只改变catalog查询。自动审计仍比较生产器witness JSON并收集日志哈希/成本；没有独立完成VCD→literal inputs→双physical PRE/POST→rows→MON选定报警→reference prefix链。P01本次已独立核验全部94链/188物理日志/94 MON日志，并对20保存前缀调用精确冻结checker纯函数，0失配。
- 影响：本批数据原始链已获P01独立支持；自动审计自身仍不能宣称具备同等闭环或未来篡改检测能力。未发现实际原始文件矛盾。
- 建议：新增只分析保存证据的versioned validator，或准确限定自动审计scope并附P01独立核验。保留失败v2及成功v3。
- 验收：
  - 完整绑定原始VCD、literal输入、两个模拟器PRE/POST/rows、选定MON位、参考前缀及冻结参考判定。
  - 缺失/截断/修改原始文件及错误slot/prefix绑定被拒绝或明确unresolved。
  - 后续授权时用离线fixture验证失败路径，无需重跑native实验。
- 精确位置和SHA：
  - `test2/scripts/controller_done_live_audit_v3.py` · lines 175–179,234–239 · SHA256 `604518ebc473d289d9bc365fe7a5e9297fae9c96eaaf2b7bf5e147c26592a604` · P01 snapshot
  - `test2/results/controller-done-live-acceptance-v3/audit.json` · formal_by_arm/formal_sessions/physical_witness_cost · SHA256 `d66e9622548d36b962a35f9dae5d05c48c669cf956ef55ce21937c898c676d8d` · P01 snapshot

## P01-R3 · P2 · 自动审计缺 returned 事件与 calls 逐项对应检查

- 状态：`PRODUCER_AUDIT_GAP_OPEN_CURRENT_DATA_INDEPENDENTLY_CHECKED`。
- 证据：独立检查36组四事件顺序、请求prompt digest/context、36唯一response_id、usage/model/tier/count逐项对应，全部匹配。生产器仍主要检查dispatch数量和calls自身usage，缺returned/calls双向唯一绑定。
- 影响：本批API账目无矛盾。未来缺失/重复/错配returned事件仍可能逃过自动验收。
- 建议：新版分析加入status-aware事件/calls绑定；失败缺用量保留unknown，不记0。
- 验收：
  - 成功returned事件唯一对应calls，context/response_id/usage/model/tier一致；计数及dispatch绑定同一prompt。
  - 失败/缺返回按实际dispatch/error记录处理，不伪造zero usage。
- 精确位置和SHA：
  - `test2/scripts/controller_done_live_audit_v3.py` · lines 53–95 · SHA256 `604518ebc473d289d9bc365fe7a5e9297fae9c96eaaf2b7bf5e147c26592a604` · P01 snapshot
  - `test2/results/controller-done-live-v2/calls.jsonl` · all36 rows · SHA256 `66a6357d255713cdb5d3ef6895fc7969328171360fa64f54b32f3ff8d51403ff` · saved dependency hashed independently
  - `test2/results/controller-done-live-v2/api-dispatch.jsonl` · all144 events · SHA256 `193d3723450ef2e7127e00313db475e02d59f8b5a5879a6dfbe387d73b7056a5` · saved dependency hashed independently

## P01-H1 · P2 · 旧控制矩阵 FAIL＋oracle unknown 漏标是历史问题

- 状态：`HISTORICAL_RETAINED_NOT_CURRENT_V4_SCORE_ERROR`。
- 证据：P01保留未变的历史producer。上轮独立审查发现252条遗漏（7controls×36rounds）；本轮不重算该历史矩阵。当前v4将oracle unknown纳入is_unresolved，本轮当前scores/diagnostic未知项均保留。
- 影响：历史控制诊断不能称为完全解决；不能将其当作当前11/11计分错误。
- 建议：保留历史结果；若重新使用其结论，另加版本化纠正overlay。
- 验收：
  - 历史纠正分别报告oracle/candidate unknown，保留全部旧冻结证据。
- 精确位置和SHA：
  - `test2/scripts/controller_obligations.py` · line132 · SHA256 `10d6df977e25683c80c76de442b9f278aa96f6c095afd3df4dd151c2679aff0b` · P01 snapshot
  - `test2/scripts/controller_done_case_v4.py` · line84 · SHA256 `e7d5d2a350bde7178ee3f260a9aac33a158645dcc58fe0a115647c1a34754ada` · P01 snapshot

## P01-H2 · P2 · 旧 offline acceptance 分类独立性限制保留

- 状态：`HISTORICAL_RETAINED_NOT_A_P01_BLOCKER`。
- 证据：历史verifier仍只验证日志hash/complete，没有独立重算matrix，也未完整绑定matrix/fixtures/reference-labels。P01重新核验2613绑定文件，但没有把其范围扩展为被遗漏的分类正确性。
- 影响：旧accepted_with_scope不能升级成完整评分正确性；当前P01数据另行检查。
- 建议：明确旧acceptance边界；今后历史纠正需要绑定全部分类输入/输出。
- 验收：
  - 不得将旧acceptance引用为全部控制矩阵分类正确性的证明。
- 精确位置和SHA：
  - `test2/scripts/controller_offline_verify.py` · lines49–56 · SHA256 `91c68038d1f7986b396eaff1f54bde766fe8febeffc6f65e2918e0b6bede5d57` · P01 snapshot

## P01-L1 · P3 · 共享冷缓存预算限制仍在，本轮无总预算截断

- 状态：`FUTURE_FAIRNESS_LIMIT_NO_CURRENT_CAP_TRUNCATION`。
- 证据：26份缓存构建元数据合计30.54816608224064s；540项全部执行，NOT_RUN_TOTAL_CAP=0；最大final elapsed652.0915609993972s，小于720s。
- 影响：本批未观察到截断影响；未来预算公平性仍受首次触发冷构建的运行顺序影响。
- 建议：未来注册统一预构建/缓存条件，单列共享预处理成本；本轮冻结日程不改。
- 验收：
  - 保留当前结果；未来试验在看结果前登记缓存条件及共享成本处理。
- 精确位置和SHA：
  - `test2/scripts/controller_done_witness_v3.py` · lines149–153 · SHA256 `b1998a59ad9e4eeff2d45b138370f6547c86f88188e8f10f1a5227f07ddc85ef` · P01 snapshot
  - `test2/scripts/controller_done_formal_v3.py` · lines85–96 · SHA256 `bfa04a22b2110e99ab4babd91c6584e1ab49e02b8509d760a1ce01282ba3bc28` · P01 snapshot
  - `test2/results/controller-done-live-formal-v2/summary.json` · elapsed_per_final/jobs[*].status · SHA256 `e67a70203b2b39c70e3c0df144b1fda4a4601b90b39098c925f9d79494c9e5d3` · P01 snapshot

## 当前版本漂移

当前20/23个工作区文件匹配P01；快照本身有效。以下当前版本stale，不纳入本次内容验收：

- `docs/HANDOFF.md`：`2dcff2e3c6904af619342a0b365c4e61c497a1368234a9a4f68872ffb4a41e51` → `1e2544f2dde08dfd08cee77156c4413fd70636474ba319218e8c17d4f879f4cf`；hunks ['@@ -2,42 +2,48 @@\n']。
- `docs/PROJECT_STATUS.md`：`cf31b2957da4b737ff1ce3366e7ebe7565e20afcb7559a969c843f94262f04c0` → `e84eb747a08b0c5f22e371ccb67659dae60253485f8bd9bc846c2794061136a7`；hunks ['@@ -2,3 +2,3 @@\n', '@@ -6,5 +6,13 @@\n', '@@ -12,5 +20,5 @@\n']。
- `test2/results/controller-done-live-post-recovery-v3/progress.json`：`4ba3e5b2963b1c3652bbca49e7c0621c4e3b8ff0fd9b69e2e3847c1efd442710` → `0aab33b828863c1e77ad94b6a8247b2f8b66223b8c0591378e75d0934dafcdcb`；hunks ['@@ -2,2 +2,3 @@\n', '@@ -60,3 +61,4 @@\n']。

两份交接文档为原线程并发更新，待下一manifest；恢复progress增量为RUNNING→COMPLETED_WITH_LIMITS，补summary_sha256及previous_progress_sha256，旧summary内容未变。

## 范围和命令

没有重跑旧实验、套件或11340条fixed-trace raw评分日志；没有作一般正确性、账单、远端验证。原始证据SHA、完整实际脚本及exit code在review.json。

辅助核验曾修正两个审查者假设：offer action实际入队并保持到接受；rounds.types为CSV文本，数值在definite_types。修正后均0错误。一次巨大摘要被截断，随后只重做轻量保存证据解析以记录SHA；一次JS语法错误没有执行shell。

- 命令1：`python3 - <<'PY'`，exit `0`；完整脚本见review.json.commands[0]。
- 命令2：`cat docs/audits/agent_bridge_2026-11-05/P01/snapshot/test2/results/controller-done-live-post-v2/raw-evidence-audit.log && diff -u docs/audits/agent_bridge_2026-11-05/P01/snapshot/test2/scripts/controller_done_live_report_v2.py docs/audits/agent_bridge_2026-11-05/P01/snapshot/test2/scripts/controller_done_live_report_v3.py`，exit `1`；完整脚本见review.json.commands[1]。
- 命令3：`cat docs/audits/agent_bridge_2026-11-05/P01/snapshot/test2/results/controller-done-live-report-v3/report.md`，exit `0`；完整脚本见review.json.commands[2]。
- 命令4：`sed -n '1,15p' docs/EXPERIMENT_PROTOCOL.md && sed -n '107,153p' docs/EXPERIMENT_PROTOCOL.md && cat docs/audits/agent_bridge_2026-11-05/P01/snapshot/test2/results/controller-done-live-post-recovery-v3/summary.json`，exit `0`；完整脚本见review.json.commands[3]。
- 命令5：`python3 - <<'PY'`，exit `0`；完整脚本见review.json.commands[4]。
- 命令6：`python3 - <<'PY'`，exit `0`；完整脚本见review.json.commands[5]。
- 命令7：`python3 - <<'PY'`，exit `0`；完整脚本见review.json.commands[6]。
- 命令8：`python3 - <<'PY'`，exit `0`；完整脚本见review.json.commands[7]。
- 命令9：`python3 - <<'PY'`，exit `0`；完整脚本见review.json.commands[8]。
- 命令10：`python3 - <<'PY'`，exit `0`；完整脚本见review.json.commands[9]。
- 命令11：`python3 - <<'PY'`，exit `0`；完整脚本见review.json.commands[10]。
- 命令12：`python3 - <<'PY'`，exit `1`；完整脚本见review.json.commands[11]。
- 命令13：`python3 - <<'PY'`，exit `0`；完整脚本见review.json.commands[12]。
- 命令14：`python3 - <<'PY'`，exit `0`；完整脚本见review.json.commands[13]。
- 命令15：`python3 - <<'PY'`，exit `0`；完整脚本见review.json.commands[14]。
- 命令16：`python3 - <<'PY'`，exit `0`；完整脚本见review.json.commands[15]。
- 命令17：`python3 - <<'PY'`，exit `0`；完整脚本见review.json.commands[16]。
- 命令18：`python3 - <<'PY'`，exit `0`；完整脚本见review.json.commands[17]。
- 命令19：`python3 - <<'PY'`，exit `0`；完整脚本见review.json.commands[18]。
- 命令20：`python3 - <<'PY'`，exit `0`；完整脚本见review.json.commands[19]。
- 命令21：`python3 - <<'PY'`，exit `0`；完整脚本见review.json.commands[20]。
- 命令22：`python3 - <<'PY'`，exit `0`；完整脚本见review.json.commands[21]。

后续仅需新的报告/分析版本及新phase manifest；不得通过重跑候选、DUT、formal或改旧分数来消除此限制。相同P01 manifest已处理。
