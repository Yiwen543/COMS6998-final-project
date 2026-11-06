# P16 — R05B 执行前独立复核

**PASS_WITH_LIMITS。未发现当前可证实的实质风险。** 可以由协调端签发唯一、精确绑定的 `G1_EXECUTE_R05B_AFTER_P16`；本报告本身不是 EXECUTE，也没有启动真实任务。G1 仍为 **BLOCKED/NOT_QUALIFIED**，须等待实际结果及后审。

P15-R1 在本批次、单 cover 包装器支持范围关闭。重新解析实际 QC01 保存证据得到：工具 `FAILED`、exit1、activation `REACHED`、assertion `FAILED`，旧 `NOT_REACHED` 原件保留；不会计作 clean tool PASS。`native_results.py:47` 在期望判断之前拒绝不完整证据，四态诊断也不能绕过该条件。runner 实际调用该判断；不是只有独立 parser 可用。

复核277个封存成员、215个当前来源/依赖绑定，全匹配。10个 E02/E03 job 明确 `new_execution=false`；SMT、receipt/log/VCD、编译模型/二进制、工具及21组硬件/输入对应均核验。无效 E02 物理运行不复用。剩余72根作业及顺序/flags逐项等于旧计划未运行部分；QC01两物理项与QC02–15均没有被跳过。runtime 与v4逐字节相同，budget仅 attempt_id 文本改变。

预算继承 setup8/compile6/native4/physical3/12cycles，旧实测11.770645541秒与旧计费14.572948167秒不混用。新保守charge15、window1185、work1180；新0/14/28/30/120cycles，计划累计8/20/32/33/132，仍在原physical33修订上限内，无新增额度或权限。native与physical无重试余量；失败继续计费并停止。

验证分开记录：生产者11项保存自测通过，本轮未重跑；前段10项独立parser探针复用哈希不变证据。新增7组独立接入检查及40个预先保存输入的门禁/UNKNOWN谓词检查，均符合预期；两者有重叠，不能相加成独立科学试验。最小caller假执行只走QC01双物理项和刻意失败的下一编译，实际持久halt、剩余69个NOT_RUN、累计reservation保留。其行/VCD解析被明确stub，是控制流检查，不是模拟证据。没有跑完整72项mock，也没有完整正向执行门禁/main实物运行。

最终EXECUTE必须绑定本review路径/SHA、R05B manifest/reg/source、实际R05decision、reuse及physical33 amendment，另含原grant与closed E03 pool。缺review、六种identity漂移均拒绝；重复claim拒绝。真实pool/lock仍不存在。Git HEAD实际为 `2de33e981d2fffc9739d2ca049fbae1774de1aad`，index指纹前后一致。原4485文件保全为生产者保存记录，本次没有重新全历史逐项扫描。

Hallmark主文件及review-finish本轮实际读取，SHA和工具证据见 `hallmark-usage.json`；用于固定材料、事实/计划分离、只列实质问题和最小修订。完整UI流程与脚本未执行，RTL/资源结论来自源码、保存证据、哈希和独立纯Python检查。verification-before-completion用于报告前校验；context-compression用于保留本审查边界与交接。

保留限制：支持精确串行路径而非通用SV解析器/全OS资源保证；inventory不完整、内存未知。QC07/15空泛、QC12/13四态限制、QC14仅transport、depth8/4cycle非128或无界证明；不授权raw/B/C/API/跨IP。F1/H1/H2/L1/P05-N1、同样本归因、74未复现见证、账单/计数费、recovery planned均未关闭。没有发现问题不等于证明全面正确。

可复现命令/退出码见 `commands.json`，确切输入、执行源、探针、输出SHA见 `evidence-manifest.json` 与 `review.json`。本轮只写P16审查目录，无真实工具、实验、API、key、安装、Git写入或跨线程消息。
