# P17 — G1 R05B 完成结果独立后审

**PASS_WITH_LIMITS。未发现当前可证实的实质风险。** 证据完整性、累计资源合规、本注册公开有限控制验收均有条件接受；本次 G1 有限资格门槛可以关闭。不是16个科学正确性证明，也没有创建后续 raw/B/C/API/跨IP 的执行许可。

E04精确phase `cc5b0539…f5b22e2`、manifest `43d9e3cd…4e219152` 已固定。独立校验568封存成员、215源/依赖及结果manifest全部成员；当前副本漂移见review.json。真实HEAD `2de33e981d2fffc9739d2ca049fbae1774de1aad`，index不变。五套旧freeze/acceptance的7450成员引用（含重复）再次纯哈希核验0失配；旧scores、Claudechecker、closed pools、坏首拍X原件保留。

72个新根作业均RETURNED（60exit0/12exit1），另有10个精确复用job，不是新trial。独立读取receipt、argv、log、deadline与持久ledger，未见timeout、mandatory error、NOT_RUN或native未知被接受。native合计18PASSED/14FAILED；BMC10PASS/6FAIL；activation14REACHED/2UNREACHED。故意负例的rawFAILED/exit1、coverREACHED、assertFAILED分别保留，旧QC01 NOT_REACHED仍留原记录。没有将FAILED改写为工具PASSED。

采用独立Python数学计算和独立VCD/文本解析，没有导入生产者解析器。由common.sv的4bit截断、signedcast、完整guard、q初值/同步reset及故意反向reset，复算16QC固定输入下预期值，逐项对应原表及实际256行。32有效运行=QC00旧双sim+本次15对，4cycle/8行各自核对；VCD/stdout及观察相位无冲突。每条轨迹posedge仅2000/6000/10000/14000ps，pre1/5/9/13ns，post3/7/11/15ns，end16ns。采样输入a/b/rst/en/valid全部已知，首拍问题在该固定路径实测消除；Icarus QC12的8行ok=x仍完整保留，不能说所有四态未知都解决。

已核对所有可用native反例的registered sampled pre；五类有资格的故意负例与两模拟器对应pre的q/active/ok匹配，未拿延迟assert报告时刻的live值冒充所选样本。QC09错误post声称被拒绝；QC07/15不激活仍排除，QC12/13四态等价不支持，QC14只有final-post传输marker，无额外时钟/输入或128completion信用。总分母仍16=11有限公开+2空泛+2四态不支持+1传输。

资源新0setup/14compile/28native/30physical/120cycles；累计8/20/32/33/132，保留全部旧失败。32条有效物理运行128cycles之外，旧E02无效运行1次/4cycles继续计入累计33/132。current total约3.494314s；最新累计actual checkpoint15.264969499s与保守charged18.494324125s分开，继承charge15/window1185/work1180而非刷新1200。root收据有已知退出、ownedPGID/poll/wait/deadline/absent-at-owned-probe；清点attempt0且不完整。它不证明全子树生命周期、内存或OS硬实时/未触发kill路径。

本轮真实工具/实验/API/ps均0，只读保存证据。一次元数据查看误读不存在的可选summary.json（exit1）已记录；使用实际phase/per-qc/resources等继续完成独立分析（exit0），不是生产者缺证据。具体命令、原始SHA、逐QC矩阵、计数及限制见review.json/evidence.json/independent-analysis.json，未编辑生产者、共享docs、原结果或索引。

Hallmark主文件与review-finish本轮实际读取，用于固定材料独立批评、事实/结论边界与实质问题优先级；无UI流程/脚本/Together，技术结论来自RTL、原始log/VCD及资源记录。旧F1/H1/H2/L1/P05-N1、74未复现、同样本归因、128/unbounded/realDUT/oracle/monitorgeneral soundness、C因果、账单unknown和recovery planned均不因本次接受而关闭。
