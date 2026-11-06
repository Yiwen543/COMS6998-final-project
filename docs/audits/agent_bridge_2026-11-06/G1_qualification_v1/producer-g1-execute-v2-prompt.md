在当前idle安全点进入本次已获用户批准的 G1 EXECUTE。P10B独立PASS_WITH_LIMITS，精确R02的R1/R2通过，旧P10 CHANGES_REQUIRED保留。无需再次问用户同一授权或索取key。

<transcript_evidence>
助手：“G1计划不需要API key，也不调用模型API；最多32项BMC/cover、32次物理仿真和32次编译，整体限制20分钟，完成后独立复核。”
用户：“并且我同意项目codex按这个上限启动G1并在完成后交给独立复核！记得使用hallmark”
</transcript_evidence>

P10B docs/audits/agent_bridge_2026-11-06/P10B_g1_fix/review.json SHA864e76e168db17878e29bbf1d580b546620497acf269b3dcb34a144775c460dc，input_identity绑定R02manifest7c16e5020ab6212fbd66bdd57ecb272bef56e1bfc6ce4362a661960d331fb201与registration85185519c5a6e2a8eaaf843b5b27c9cc312ada2fc8c44af6f915368759d98268。协调端已核验P10B全部evidence与当前source-manifest，0差异；canonical共享pool目前不存在。独立fresh14回归、17探针、9gate探针符合预期。本接受仅是执行前资格，不是G1实测成功。

已生成非密钥执行收据 docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/execute-receipt-v2.json（SHA 9a6dfd949c54e1a159ff4b3e8e97999edc306c8dcac3cf3b233785a29de0dd95），绑定exact注册/source/preparation/usergrant/P10B。只执行：

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python test2/g1_v2/runner.py --execute-authorization docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/execute-receipt-v2.json

运行前仅核对这些身份和独占输出状态，不运行外置smoke compile/sim/version测试。任何源码/注册漂移、已存在pool或actual output/lock立即拒绝并报告，绝不删除/reset以重跑。原BF3 grant仍唯一；R01/R02都未真实执行过，此次仅final R02一个profile。setup/version/frontend/编译/native/physical/等待/解析/结果输出共享1200s窗口，32compile每项20s、32BMC+cover每项10s/depth8、32physical每项2s/合计1024cycles且每run32上限；额外setup8*2s已在注册同池计费。实际计划18logicalcompile、32native、32dualphysical/128cycles只是计划，要保存实际计数、失败与未运行。

不能timeout后换profile/修控制/加帽/重新启动/重新给pool，也不因结果不理想重跑。若supported类不符合预期、setup/compile/parser失败或预算停止，保留错误/原始log/VCD/physical PREPOST/JSON/成本/剩余NOT_RUN，按固定停止规则结束；别改source/labels以得通过。QC07/15空泛/未激活保持不资格，QC12/13未知/X/caseeq仍不获四态等价credit，QC14仅transport；depth8不是128/无界/DUT/monitor general proof，不解释旧74条未复现。双simulator真实输出不可只比producer摘要。

原user grant不授权API/count/generation/Claude/oracle/候选/新B/C/旧cohort重跑/key读取配置/network/install/commit/push/删除。不要重做PPT或访问旧秘密。旧frozenchecker/score/denominator/unresolved和所有R01/R02/P10/P10B源与快照保持不变；不要让执行产物写入这些冻结源目录。唯一pool路径保持test2/results/g1-qualification-v1/execution-state.json，真实结果按新v2root，不借版本刷新额度。

结束后无论成功/失败都封存唯一E01 execution phase.json/snapshot-manifest：receipt/P10B/R02/source/config/input/label/tool版本及命令exit/status/hash、pool ledger/时间点、原始log/VCD/观察、逐QC支持/unsupported/invalid/timeout/NOT_RUN、实际setup/compile/native/physical/cycles/墙钟及测不到的unknown。准备/审阅elapsed与本次actual execution window单列。共享HANDOFF/STATUS仅新增当前准确入口、保留旧正文。状态EXECUTED_PENDING_P11_SAVED_EVIDENCE_REVIEW，不自签独立接受。若runner报错，保存退出和原始证据/哈希，不为了报告补跑。

停在安全点交协调端路由既有reviewerP11，P11只解析保存证据和独立RTL/数学检查，0额外compiler/native/physical任务，不刷新预算。Hallmark实际使用披露保留为组织/critique方法，专项结论来自真实RTL/工具/反例证据，不跑UI脚本/API。不自动进入G2/G3/G4，未来API必须另有具体服务/模型/调用/token/USD/time和安全输入授权。

