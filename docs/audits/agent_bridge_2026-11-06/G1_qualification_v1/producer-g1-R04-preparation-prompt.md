继续 G1，当前为 R04 修复准备，真实执行额度不变。父线程已明确：P13指出physical累计32需至少33，正在询问用户；答复前不得扩大额度或超额运行。允许继续修复和独立预检。请不要重复询问用户，不要开始任何真实版本/编译/native/physical/探针，不要假造33批准或EXECUTE。

精确P13：docs/audits/agent_bridge_2026-11-06/P13_g1_retry_execution/review.json，SHA 2fcee5eb22542449744ba43a8967efd11adb0bcda29afda10b9f64a3fd37ab29。P13-R1 P2：QC00首拍a/b/rst/en/valid/active/ok X，stdout和VCD一致；step声明0再首轮赋0、stimulus always@*与首次激活缺口一致，具体修复未实测。失败/资源合规PASS_WITH_LIMITS，G1 BLOCKED，原件一律不改。E02 phase SHA3750f51dc2c5825ba2f386a633dd7e480f303ab06f312f7f940462c450b9c190；最终pool test2/results/g1-qualification-v3/execution-state.json SHA1bfe56363ae08fd288be7050fff2ddb05ae7af7eb537e357273222a81483c15e，保持halted/completed。

最小修订目标：新test2/g1_v4或明确独立R04空间，只修physical_tb首次刺激建立/稳定机制，尽量保持common.sv、全部native harness/输入/标签及语义材料字节不变，使新登记下可严格复用旧QC00两项native及其Yosys产物。保证首个pre1000ps/posedge2000ps/post3000ps及全部0..3行/16ns结束/4posedge合同不变；不X→0、不跳首行、不添加DUT时钟。不要简单假设另一个time0赋值必有序；考虑双sim实际支持边界(不要用不支持的#0语义伪造可移植性)。选择最小可解释启动方式，源码推理/纯Python检查不能被称为实测修复。旧首拍X原始stdout/VCD及全部111mock历史保留。

资源计划需明确：已累计setup8、compile3、native2、physical1/4cycles；剩余setup0、compile29、native30、physical31、cycles1020。若native依赖不变且新登记接受保存证据复用，可计划旧QC00 BMC+cover2(非新独立试验)、旧QC00 SMT/Yosys编译1；本次新0setup、17compile(15frontend+2新physical sharedbuild)、30native、32physical/128cycles，累计compile20/native32/physical33/cycles132/setup8。33只是待用户批准提案。若复用条件不满足，明确native会至少34累计(+2)，不得偷偷增额度或沿用旧哈希。核对实际依赖后给精确计划，不仅复制上述算术。

当前旧累计窗口实测检查点5.197697583s，累计保守charge7.151973250s；下一continuation可保守charge8秒而非实测8，剩余最多1192秒，不增加1200总帽。正式新额度决定和用户证据由协调器提供，不由你伪造。真实入口对缺失/未批physical33决定和缺失独立P14必须拒绝；不创建真实attempt lock/pool。可准备有界gate/prefix复用元数据，但不要过度重构；若审批尚未到，清楚标为提案/不可EXECUTE，并让P14可独立检验拒绝路径。

现在做：读取P13 report及budget-feasibility.json→最小R04源码/变更图→必要纯fake输入/拒绝回归(无任何真实子进程、信号、睡眠或SV工具)→给可审核的源码/差异、依赖和复用清单、资源矩阵、失败条件和哈希，供既有P14增量预检。Hallmark实际用途/读取情况照实记录，不做UI流程。审批到达前不为预检运行真实编译，也不要用纯mock宣称SV ABI/首拍实测已修复。

保护E01/E02/R03/P12/P13、原scores/Claude oracle/freezes/全部unknown和raw分母，不改任何已封存原件、Git index(10000 staged entries)/add/reset/commit/push，不做API/key/G2–G5/network/install/delete/PPT/新chat或agent。HANDOFF/STATUS仅封存时prepend简短本轮状态，保留旧body。若任务压缩，恢复本条，当前任务不是历史PPT。请在安全点完成R04准备并停于独立P14，任何新额度/依赖/权限问题先报告具体差异。
