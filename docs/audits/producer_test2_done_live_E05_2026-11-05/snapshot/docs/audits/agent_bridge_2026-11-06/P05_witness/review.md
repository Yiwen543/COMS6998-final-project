# P05 保存见证链 validator 独立验收

结论：**PASS_WITH_LIMITS**。P01-R2可在当前保存格式与精确94条固定批次范围内由新增companion validator关闭；不等于修复formal语义、证明监视器正确或关闭R3。**未发现需要提前打断推进线程的明确实质风险。**

- Manifest SHA256：`e17a5952c588c24014e6b44f34165f79f43fa0204d45bd2b55dc0bb2e5b63536`。
- E03b phase SHA1f4dc7a88f66e1b75e709ce4e81de3d9e751f92950486542f78d8a290650f8ea；snapshot-manifest SHAed8d5121acd9cced18c361c29b5cb7856aef53f1664e7e4f890abc79cef5db39。
- 最终source SHA f1b1124be9f9e088f92d61f682223056f96c6f4ba1ce2accb610b9429bf2f82d；tests SHA23d6e6b907cc2887daf3bcbbee5fb46fca1a873a3abddbb4dcf5f179c3b63fdb。
- v5结果SHA e12e02ca6721637247bf013eeb0340a9c8198ad3f6c1cfd21bb86aec0833640c。
- 精确快照27/27与metadata3份均匹配；当前25/27匹配。HEAD c25180848ebfe9a1f49da0aa5f579cac913e6428，dirty/untracked保留。

## 逐项验收

### A1 · PASS

- 精确位置：test2/scripts/controller_done_witness_chain_audit_v1.py:220–279。
- 证据与判定：native summary/job/status/log/source copies/harness slot and expected mutant source,physical compile/binary paths,candidate replay binary and snapshot artifacts are checked;real94-chain execution matches savedv5 all fields.

### A2 · PASS

- 精确位置：decode_vcd:46–91。
- 证据与判定：Declared top pin widths and selected bit existence bound. Does not assume6-bit formal active/ok. Independent3-bit active/ok withslot2/alarm1 passes; declaration excludingselectedslot4 rejects;no synthetic padding of missing slot.

### A3 · PASS

- 精确位置：inspect_chain:169–197。
- 证据与判定：VCD→formal-inputs→literalinputs→dual orderedPRE/POST→rows→retainedVCDoutputs→HEX→MON scopes/digests/properties checked. Independent correlatedfresh-hash mutations reject at semantic binding, not merely fileSHA.

### A4 · PASS_WITH_LIMITS

- 精确位置：inspect_chain:198–218。
- 证据与判定：20reproducedalarms re-evaluate exactfrozen purechecker on earlierprefix only. All94scientific_adjudication remainsUNRESOLVED;20referenceprefixFAIL,74no referenceverdict,allC7correct/67mutant. Unknown selected MON bit remains noalarm/UNRESOLVED;phase/slot/prefix/same-sample upgrade negativesreject.

### A5 · PASS_WITH_LIMITS

- 精确位置：Saved:31–43;audit_saved:240–282。
- 证据与判定：2797contentdependencies,1545P01anchor matches,1252additionalhashedwithoutindependent historicalanchor explicitlyreported. No claim ofSMTequivalence or immutable independenthistoryfor everydependency.

### A6 · PASS

- 精确位置：load_checker:161–166;25targeted final tests。
- 证据与判定：ExactcheckerSHAb44f… before in-memorycompile;no importcache write. Freshsnapshot-only25unit tests exit0 in0.082s;noEDA/API/monitor execution.

### A7 · PASS_WITH_LIMITS

- 精确位置：E03bdrafts/v1..v5/fixture-controls.json。
- 证据与判定：v1REJECT91/94 retained withfirstsourceSHA;v2..v4 sourcebindings retained. Fourth→final AST differences onlyload_checker;old11negative/2unknown controls remain fourthsource evidence,not calledfreshfinaltests. Final25tests plus independent15probes are separately recorded.

### A8 · PASS_STATIC_AND_SAVED_NEGATIVE_EVIDENCE

- 精确位置：main:286–294;E03b/overwrite-refused.log。
- 证据与判定：exist_ok=False precedes audit;producer refusalexit1/hashunchanged preserved. Reviewer did not attempt a real resultoverwrite.

## 主要核验结果

- 本审查执行精确snapshot纯audit_saved，结果全部函数字段与封存v5一致：94链consistent，20physical alarm reproduced且20earlier reference prefixFAIL，74unreproduced unresolved；same-sample/categoryconfirmed=0，所有scientific_adjudication为UNRESOLVED。原540状态75PASS/104FAIL/361TIMEOUT未改。
- 2797依赖中1545匹配P01独立SHA锚；1252是新增当前内容与身份绑定，不能称每份都有独立历史锚或已证明SMT语义等价。
- 独立overlay不写真实文件，并故意同步更新physical log/rows/execution hash、MON gzip/raw/property hash。physical input错配、双模拟器相关改动但VCD未改、MON非法phase、selectedslot/phase、referenceprefix长度、同样本确认升级、未复现伪造oracleverdict均拒绝。未知selectedMON位可consistent但无物理报警、scientificUNRESOLVED。
- 独立3-bit active/ok、slot2正确定位可通过；声明不含slot4立即拒绝。没有补零伪造缺失slot。nativeassert延迟报告不替代直接观察active/ok选定pre样本。
- 精确snapshot最终25项纯离线unittest新鲜通过（exit0，0.082s），覆盖缺失/截断/错hash/nativeidentity/破gzip/unknown/cache等。不是只引用生产者PASS。
- 保存11negative/2unknown controls属于第四稿，不冒充最终稿新鲜测试。AST对比第四稿→最终只改load_checker，旧分支定义等价；最终独立测试和实际解析另计。v1的91reject及v1..v5/source绑定均保留。
- 覆盖输出拒绝仅静态检查exist_ok=False及保存producer负例；没有尝试写真实结果。

## 非阻塞建议 P05-N1 · P3 · material=false

位置：inspect_chain第200及213–216行。无锚的isolated helper probe额外注入未复现source metadata reference_confirmed_selected_alarm=true时，函数忽略该多余字段并返回consistent；但receipt仍强制false、reference_verdict=null、scientificUNRESOLVED。严格REJECT的探索预期未满足，完整记录不隐去。
当前74份未复现格式没有这个true字段且P01 independently anchored，实际文件篡改会被顶层Saved.raw先拒绝。因此未证明当前批次科学确认错误，不能当作新的实质紧急风险。
建议未来安全checkpoint将不得true的metadata检查移至分支外；若实施，加固probe应REJECT，真实94链与candidateunknown保持不变。此建议不阻塞当前格式/批次验收，也不要求打断R3修复。

## 剩余范围

- Only current saved format/cohort R2 capability accepted; historicalaudit_v3 itself remains unchanged.
- P04CHANGES_REQUIRED and newR3repair requireseparateP06;not inspectedhere.
- F1representationlimitations/selectedpre-vs-earlierprefix attribution/wholemonitorcorrectness/128completion remainunresolved.
- H1/H2history andL1cache/order fairness are notclosed.
- 1252dependencies are currently content/identitybound but lack P01independenthistorical anchors;no semantic equivalence or proof of execution beyond saved evidence.

## 版本漂移与边界

- STALE当前文件：docs/PROJECT_STATUS.md，snapshot=3e0fa965f7e338f27b2c66833911b96f18661a2a86501e0f65a765a37b793550，current=0ee06988ae2f3caff67c0533bc367262871b97f685cc94850958eaf0462a66ea；本次只验固定快照。
- STALE当前文件：docs/HANDOFF.md，snapshot=4872a8c1ad0c1a2229043644d0649c1f20bcdbd2de1b3e2160fc44a8253e515c，current=d9d976133c3f01de4169c18fc47c0e38022cd7bb6db4c2ac74cdd17c416ba6b9；本次只验固定快照。

只写review.json/review.md/fixture_records.json。轻量unittest在临时隔离目录写其合成fixtures；没有编辑真实source/test/docs/results或oracle、没有native/model/count/monitor工具、安装、删除结果、commit/push或key操作。P04历史CHANGES_REQUIRED不变；新R3修订等待P06，不混审。

## 实际命令与退出码

- 检查1：`python3 - <<'PY'`，exit 0；完整脚本见review.json.commands[0]。
- 检查2：`python3 - <<'PY'`，exit 0；完整脚本见review.json.commands[1]。
- 检查3：`python3 - <<'PY'`，exit 0；完整脚本见review.json.commands[2]。
- 检查4：`python3 - <<'PY'`，exit 0；完整脚本见review.json.commands[3]。
- 检查5：`python3 -B -m unittest discover -s docs/audits/producer_test2_done_live_E03b_2026-11-05/snapshot/test2/tests -p test_controller_done_witness_chain_audit_v1.py -v`，exit 0；完整脚本见review.json.commands[4]。
- 检查6：`python3 - <<'PY'`，exit 0；完整脚本见review.json.commands[5]。

另有有界source/test读取与第四稿diff（exit1表示存在预期改动）。一次probe名称过强已纠正，并添加真正声明缺slot和3-bit正例；不是项目失败。15个独立probe中14个满足预期，1个探索性metadata严格性差异按上述非实质理由保留。

后续按新manifest单独验R3，不扩展本轮。无跨线程消息或提前打断建议。
