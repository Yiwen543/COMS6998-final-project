请在既有复核线程进行 P13：独立审核精确封存的 G1 R03 重试实际输出。协调器会补充本次执行阶段、manifest、源/登记、P12、EXECUTE 收据及资源池的路径和 SHA。只读保存证据；不得再运行版本查询、编译、BMC/cover、仿真、API 或旧实验。输出仅新 P13_g1_retry_execution 目录，不改原始证据、共享 handoff 或索引。

检查链：实际 HEAD、P12 对象与当前执行代码精确相符；旧 E01 halted/completed 池 SHA 与原授权不变；当前池确实继承 setup1、保守 charge2。分别报告本次和累计 setup/compile/native/physical/cycles、实际运行/保留/NOT_RUN/失败、实际窗口和累计保守计费窗口，不能把1198秒重分配成新1200秒额度，也不能把逻辑编译批次数当成 OS 进程数。核对 setup累计≤8、compile/native/physical各≤32、周期≤1024、depth8、单项20/10/2秒和累计1200秒；保留超限、未知和清理异常。

核对16QC的原手算标签、native BMC与activation cover、双物理仿真及VCD/行/相位绑定，分别报告支持/不支持/不一致/未运行。QC07 vacuity、QC12/13四态限制、QC14 finalpost marker、QC15未完成不得被算成128周期或无界证明。来源不一致或原始状态冲突须定位；不将没有发现问题等同于全面正确。公开玩具控制资格与真实 DUT/模型科学结论分开。

本轮重点核查 owned_process_group_only 的真实收据：无 ps 真实调用、inventory不完整如实标记、根退出状态单独已知/未知、进程组/原截止时间/kill/wait 必要保护证据及任何失败。记录有限证据不能证明完整子进程生命周期或未测内存；不得用纯mock替代实际执行观测。

E02实际已在首个QC00-Icarus物理行接收处halt(PHYSICAL_EXPECTED_MISMATCH:a)，不是完整89jobs完成。请基于原始stdout/VCD及physical_tb.sv/common.sv，定位cycle0的a/b/rst/en/valid为何为X、后续cycle1–3才已知；核查是否time-zero组合驱动未激活，区分直接观测与未执行的修复假设。不允许把X替成预期0或跳过第一行来让旧结果通过。原错误和费用保留，source不就地修补。

请另做只读预算可行性判断：累计setup8、compile3、native2、physical1/4cycles后，剩余setup0、compile29、native30、physical31、cycles1020。若要覆盖16QC×双物理仿真，已有QC00-Icarus合同不合格，是否至少还需32物理运行，从而比原32累计帽多1？若只改physical TB而native源码/输入/SMT不变，精确旧QC00 native2项能否在新的显式登记下复用，需哪些绑定/条件，不能自动假设当前门禁支持？请分别给：保留全部未决的受限部分结果路径、完整G1所需最小具体额外额度(如有)、任何真正新增权限需求；不要仅因再一次retry要求用户重复确认，也不得扩大累计帽或放宽验收。修复准备/纯mock可由后续生产者受限任务完成，不在本轮改代码。

按用户要求如实记录 Hallmark 本轮新读或已核对同版先前读取，以及实际适用的固定输入独立批评/证据组织/问题优先级；网页UI流程和脚本不适用，技术结论来自RTL/原始日志/账本。输出 review.json/md、hallmark-usage.json 和必要精简核验记录；给出证据完整性、执行资源合规、公开资格结果三个分别的结论，必要时明确最小实质问题、影响、验收条件。无需为补记录重跑历史测试。
