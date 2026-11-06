# P04 账本validator独立复核

结论：**CHANGES_REQUIRED**。确认一处 material=true 的错误证据接受路径；真实保存批次仍核验一致，没有发现旧科学结果或实际消费违规。**无需打断正在做R2的推进线程，待下个空闲/安全checkpoint转交即可。**

- Manifest SHA256：`647c2d23b87eb80f4af6af4535d9605926167045b73054fad5b7c3a6ad117187`。
- 实际HEAD：`c25180848ebfe9a1f49da0aa5f579cac913e6428`。
- 21份精确快照和3份metadata均匹配；当前21/21匹配。

## P04-R1 · P2 · material=true

- 精确位置：test2/scripts/controller_done_ledger_audit_v1.py:169–172;validate_ledger request-dispatch branches。
- 源SHA256：c07cdf35651c6fc90b3585d7ac11ab1041050bc7031964aa78e15ea4b91b9166。
- 证据：独立内存fixture API_requests_after_resource_halt：首attempt count=21超过input cap20，generation未派发且记录resource_halt；随后同一round attempt2重新count并generation，所有返回/用量均一致。validator返回PASS、unresolved=[]，而冻结模型halt后拒绝所有count/generate。完整输入与实际返回保存在fixture_records.json。
- 实质理由：这是已复现的错误证据接受路径，而非风格或潜在担忧：validator消费停止事件却不持久记录halt状态，能把违反已登记停止规则的后续API派发认证为一致PASS。
- 影响：影响新validator对资源/停止协议一致性的验证能力；不证明真实批次违规。当前36calls/144events没有任何resource_halt，真实账目独立重算仍PASS，旧科学结果不受该反例影响。validator只读，此缺陷本身不会发API。
- 修复：另建修订版validator/测试/输出，持久记录已发生resource_halt；之后禁止任何count/generation请求标志或派发事件。允许后续仅not_run_resource_halt且无请求/usage的保留记录。保留旧v1源、22tests证据、v1/v2结果和本反例，不改冻结生成器或重发请求。
- 验收标准：
  - 所附halt后重派发反例必须REJECT，不得PASS或仅以一般UNRESOLVED接受协议违规。
  - 增加同round重试及跨session/round在halt后派发均拒绝的轻量fixture。
  - 合法halt＋只保留NOT_RUN、无后续API事件的正例继续可表示；失败/缺用量保持null/UNKNOWN_NOT_ZERO。
  - 修订版对保存真实36calls/144events/1614依赖继续通过并绑定来源；不重跑任何科学实验。

冻结依据：controller_done_model_v2.py的halt()设置self.halted，count_input_tokens()/generate()在halt后直接拒绝；generation_v2注册runtime_halt明确停止后续API。对应精确SHA见fixture_records.json.halt_contract_sources。此次问题位于新离线审计，而非声称冻结生成器实际绕过了停止。

## 本批与fixtures

- 真实36calls/144events/36唯一responseID逐项一致；1475813input+78479output=1554292tokens。36份raw usage与缓存/推理子集独立核算符合；实际resource_halt=0。
- exact snapshot audit_saved只解析保存文件：PASS，1614依赖SHA与生产结果相同；未运行CLI或任何native/API工具。
- 20个独立fixture：19个符合预期；唯一反例为halt后重新派发错误PASS。已覆盖missing/duplicate terminal、跨session、错prompt/count、单边和双边model/tier错配、usage/subset、countquota、interleaved count、generationerror未知、依赖digest篡改及allowlist拒绝。合法halt后只有NOT_RUN的正例继续PASS。
- 真实结果及所有输入未改写。完整可复现反例和实际返回见fixture_records.json；该文件SHA为 c12eda95b03c76ef2109aab13f68f59488a3e363e505ef681c3443a4d17414d1。
- 输出覆盖拒绝依赖静态mkdir(exist_ok=False)及封存生产负例exit1/hash不变；本审查没有尝试写真实结果目录。

## 其余验收与限制

- A1 PASS · validate_ledger: calls/event state machine：Saved36calls/144events,unique response IDs,context/prompt/count/model/tier/usage/rawsubsets independently checked;actual audit_saved result and1614 dependencies match saved producer result.
- A2 PASS · validate_ledger returned/error/usage paths：Independent success baseline PASS;missing/duplicate returned,wrong context/prompt/count/model/tier conflicts rejected. Generation transport error UNRESOLVED with actual_tokens null; no missing usage converted to0.
- A3 PASS_WITH_LIMITS · validate_ledger docstring and serialized event consumption：Historical count/returned/error events lackrequestIDs/context. Validator only provides strict serialized positional binding, rejects interleaved/orphan count fixture; cannot authenticate absent fields. This limit is explicitly documented and not treated as a new defect.
- A4 PASS · Evidence.path/bind and audit_saved：1614 actual hashes verified by pure saved audit;independent digest mutation rejected without editing evidence;escape/private paths rejected.
- A5 PASS_STATIC_AND_SAVED_NEGATIVE_EVIDENCE · main output mkdir(exist_ok=False),E03a/overwrite-refused.log：Output refusal checked statically and via hash-bound producer negative log/phase;reviewer did not attempt a real output overwrite. Original result hashes remain intact.
- A6 CHANGES_REQUIRED · validate_ledger:169–172：resource_halt is consumed without persistent halt state;new count/generation accepted asPASS. Full independently authored counterexample saved.

- No actual batch resource_halt exists;not an accusation of historical cap violation or scientific-score corruption.
- Invoice/count endpoint charges remainnull/UNKNOWN even when saved ledger consistencyPASS.
- P01-R2,newR2maintenance outputs,formal representation/selected-sample scope,H1/H2,L1 are outside this review and remain as previously disclosed.
- Producer22-test suite source inspected and saved PASS noted;not rerun wholesale. Independent20fixtures do not prove allpossibleledger correctness.

历史事件缺requestID/context，严格串行位置绑定是诚实范围限制；不能凭validator补造未保存的身份。未把该已披露限制升级为新紧急问题。

## 版本与执行边界

最终检查时21/21当前文件仍匹配固定快照；后续共享docs的变化不自动纳入本结论。

只写本轮review.json/review.md/fixture_records.json。未编辑source/test/docs/results、未调用API/count/模拟/formal/monitor、未安装/删除结果/commit/push或访问key。R2工作未审查、未发跨线程消息。

## 实际命令与退出码

- 核验1：`python3 - <<'PY'`，exit 0；完整脚本见review.json.commands[0]。
- 核验2：`python3 - <<'PY'`，exit 0；完整脚本见review.json.commands[1]。
- 核验3：`python3 - <<'PY'`，exit 0；完整脚本见review.json.commands[2]。
- 核验4：`python3 - <<'PY'`，exit 0；完整脚本见review.json.commands[3]。
- 核验5：`python3 - <<'PY'`，exit 0；完整脚本见review.json.commands[4]。

其余源码/测试与E03a记录为只读有界读取。生产者22项测试不是本审查的新鲜测试结果；独立fixture已确证新缺陷，因此不能以生产PASS替代R3独立验收。后续请封存修订版新manifest再做窄范围复验。
