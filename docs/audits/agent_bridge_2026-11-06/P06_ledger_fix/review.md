# P06 持久 halt 修复独立验收

结论：**PASS_WITH_LIMITS**。P04-R1对新版v2的修复验收通过；P01-R3可在严格串行保存格式及该批次范围关闭。不能扩展为计费、监视器或formal语义正确性。

## 必须保留的 P04 证据纠正

P04关于“保存原件可原样复现PASS”的说法不准确，本轮明确纠正：

- 原始P04 fixture_records.json SHA c12eda95b03c76ef2109aab13f68f59488a3e363e505ef681c3443a4d17414d1中snapshot.response=null，却有accepted parsed response。精确旧v1执行实际REJECT：accepted response/snapshot mismatch；该文件保存result却为PASS。
- 临时深拷贝只补snapshot.response为已记录accepted parsed response，不改halt/events/usage：旧v1 PASS，新v2因API request flags after persistent resource_halt REJECT。新v2对原件也在halt guard处REJECT。
- 此差异为实质的历史证据可复现性限定（P06-E1，P2，material=true），已在本轮纠正；不改P04原文件、结论或历史状态。差异/serialization原因保持UNKNOWN，不猜测。
- 另行独立canonical fixture证明代码缺陷仍成立，不依赖P04不匹配字段或生产者测试。无halt成功基线两版PASS；绑定正确的halt后retry、跨round、跨session反例旧v1PASS、新v2特定halt原因REJECT。因此原缺陷本身有效，原样artifact复现说法需限定。

## 逐项验收

### A1 · PASS

- 精确位置：test2/scripts/controller_done_ledger_audit_v2.py:45–55,89–95,181–196。
- 判定：halted is defined outside call loop, set on resource_halt and never cleared;dispatch take guards and post-halt call/event guards reject requests across retries/rounds/sessions and orphan requests.

### A2 · PASS

- 精确位置：P06 fixture_records.json:canonical_probes。
- 判定：14 independently authored probes all meet expectations:both versions no-haltbaselinePASS;canonicalhalt oldv1PASS/v2REJECT;crossround/session same;requestflagswithout event and orphan dispatchwithout call REJECT for persistent halt;legalNOT_RUNPASS;failureusageUNRESOLVED/null.

### A3 · PASS

- 精确位置：test2/tests/test_controller_done_ledger_audit_v2.py and inherited v1 tests。
- 判定：32 exact snapshot offline tests freshly pass(exit0,0.004s),22 inherited binding checks plus10halt/evidence cases. Source/test hashes match requested versions;no native/API invoked.

### A4 · PASS_WITH_LIMITS

- 精确位置：test2/results/controller-done-ledger-audit-v3/audit.json。
- 判定：Independent pure saved audit matches every v3 function-result field;all oldv1 fields also match.36calls/144events/36responseIDs/1614dependency bindings/1554292tokens unchanged;haltfalse/events[];provider invoice/countfees null.

### A5 · PASS_WITH_LIMITS

- 精确位置：counterexample-baseline.json;P04 exact snapshot;P06 fixture_records.json。
- 判定：Evidence discrepancy independently confirmed;P04 unchanged-original reproducibility claim corrected and qualified. Root defect still holds for correctly bound evidence. Serialization cause UNKNOWN.

### A6 · PASS_STATIC_AND_SAVED_NEGATIVE_EVIDENCE

- 精确位置：main output mkdir(exist_ok=False);E04 overwrite-refused.log。
- 判定：Output refusal inspected statically and via sealed negative record;no real output write attempt. v1/E03a/P04/scientific results retained.

## 版本与证据

- P06 manifest SHA e8ea9feef15c5d8b8f66ef30c1775bc8cf65a410495d7d057a73f723b379c71b。
- E04 phase SHA501de0d809fe2933876c6ed2c850113e493a23e6187b4482120f370d7ebc949e；snapshot-manifest SHAafe21297c125850f67c3835feba18fae4ccdae4e35bffd3d84174bac32925aee。
- v2source SHA 2d27c0aac133c002f78a4fe69f505711069b67ef76778d5251fdb774abe7422f。
- v2tests SHA 0f845a547afd823071d2a65bf2a73db51ae9301f574e444f6449dc4edbaa1afe。
- 旧v1source SHA c07cdf35651c6fc90b3585d7ac11ab1041050bc7031964aa78e15ea4b91b9166。
- 真实v3audit SHA 07aedb0eb685b3b46e1e337a7b69f7804be8295f0d0e4bae8bb0a9e6c7c8dcaa。
- 26份快照、4份metadata均匹配；当前26/26匹配。实际HEAD c25180848ebfe9a1f49da0aa5f579cac913e6428；dirty/untracked保留。

## 验证证据

- 14个独立canonical探针全部符合预期。global halted跨retry/round/session持续；flags无event、无call孤立count/gen派发均REJECT，拒绝原因明确是persistent halt而非其他绑定错误。
- 合法halt后仅NOT_RUN仍可PASS consistency，actual_tokens=null；失败missing generation usage为UNRESOLVED/UNKNOWN_NOT_ZERO，known token subtotal为空而非伪造0。
- 精确snapshot32项离线unittest新鲜通过，exit0，0.004s；22项继承绑定校验和10项halt/证据差异测试。没有运行整个历史套件。
- 保存真实批次36calls/144events/36unique IDs/1614依赖，1554292tokens，与旧v1全部既有字段一致。新版新增persistent_resource_halt=false/resource_halt_events=[]，invoice/countfee仍null。
- 真实批次无halt，不受本反例和修复影响。覆盖输出拒绝只静态及保存负例核验，未尝试写真实结果。
- 本次fixture记录SHA 1326a98bee0587169de3c28eeaa13d0436bf5719b1283541568f34093dc243ac；所有固定证据精确SHA见review.json.evidence_sha256。

## 仍开放的范围

P04历史CHANGES_REQUIRED不改，P06是新版后续验收。P05既有R2限定验收不重审；P05-N1、F1/H1/H2/L1、一般monitor soundness/128completion、selectedpre/earlierprefix归因与账单真实性均不因本轮关闭。历史事件缺requestID/context，严格串行位置绑定不补造身份、不支持并发interleaving。

## 当前漂移与执行边界

最终当前26/26匹配；共享docs后续增量另作版本，不混入此验收。

仅写本轮review.md/review.json/fixture_records.json。没有改P03/P04/P05、E04或共享文件，无API/count/native/DUT/formal/monitor重放、安装、结果删除、commit/push或key操作。无需跨线程提醒；反馈按空闲/安全checkpoint转交。

## 实际命令与退出码

- 检查1：`python3 - <<'PY'`，exit 0；完整脚本见review.json.commands[0]。
- 检查2：`python3 - <<'PY'`，exit 0；完整脚本见review.json.commands[1]。
- 检查3：`python3 - <<'PY'`，exit 0；完整脚本见review.json.commands[2]。
- 检查4：`python3 -B -m unittest discover -s docs/audits/producer_test2_done_live_E04_2026-11-05/snapshot/test2/tests -p test_controller_done_ledger_audit_v2.py -v`，exit 0；完整脚本见review.json.commands[3]。

另有只读有界源码/测试读取和v1-v2 diff；diff exit1表示预期差异。相同P06 manifest已处理，后续改动用新manifest。
