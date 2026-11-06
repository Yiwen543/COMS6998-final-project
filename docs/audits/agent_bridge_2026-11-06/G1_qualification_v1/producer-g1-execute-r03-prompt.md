P12独立预检PASS_WITH_LIMITS，无执行阻塞。review SHA 41c7ed9ee4af55dd6454b92e9356ddee22222c7ec4ea9de2c704de9fdebf70b2；R03 manifest SHA 169e27b1180a9e3a866559b48864b2352ec4a5715230d315e4abfc4e158e2f59。精确EXECUTE收据：docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/execute-receipt-r03.json，SHA ac8d5ef19740cf1cda86b457f3f4e2f4f30b46b53f93439e5519216b59057be0。
唯一入口命令（不要先运行其他版本/编译探针）：PYTHONDONTWRITEBYTECODE=1 .venv/bin/python test2/g1_v3/runner.py --execute-authorization docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/execute-receipt-r03.json

当前任务仍为 G1。P12 对精确 R03 的接受、EXECUTE 收据路径和 SHA 由协调器在此模板之前补充。本提示仅在该接受和收据都已核对、推进线程空闲时发送；不要恢复历史 PPT 或其他任务。

按原用户授权和已封存 continuation-decision-r03.json，执行这一次精确 R03 续行。用户已授权同任务合理重试，无需再次确认。新池和独占 attempt lock 必须尚不存在，旧 E01 halted/completed 池及其 SHA 必须保持。新代码/登记/源清单/控制/标签/工具 pins/flags 不得更改；如绑定不符立即停止，不补修后偷偷重试。

唯一实际入口是登记的 test2/g1_v3/runner.py，使用此条提供的精确 EXECUTE receipt。不要添加真实 smoke、版本查询、编译或子进程探针。特别不调用 /bin/ps、不申请完整 runner 提权；已注册 owned_process_group_only，必要 poll/PGID/kill/wait/截止时间失败仍须停下保留 UNKNOWN/UNRESOLVED。

累计原帽32编译、32 BMC+cover(depth8)、32物理运行/1024周期，单项20/10/2秒，实验执行墙钟1200秒。E01 已消耗setup1，实测0.045724458秒、保守charge2秒分别保留；本次最多新增7setup、1198秒。计划本次18逻辑编译根作业、32native、32physical/128周期，7setup；setup-make按登记未重探，不能声称已取得新版本。子编译命令和耗时仍在根作业/全局帽内。

原失败池不改写、不退额度。不要复用旧收据、清零或重启任何真实池。若发生错误/超时/权限问题，保存原始stdout/stderr、job receipts、runner退出码、所有NOT_RUN、已预留与实际执行、最终池状态，再停于证据检查点。合理后续重试仍须由协调器核对累积剩余资源和新版本，不能在本轮自行循环；不用重复用户批准替代资源核算。

完成这次入口后封存新的执行审计阶段(例如 producer_test2_g1_E02_2026-11-06，若已存在选新唯一目录，不覆盖)，连同实际命令/退出码、原始日志、资源池、每QC表、真实工具版本/已知未知、observations/VCD、解析拒绝和哈希。分别写本次计数、累计计数、当前实际窗口、历史实际窗口和保守累计charge，准备/复核经过时间另列，内存未测如实写。解释eligible/ineligible/NOT_RUN，不把mock、cover到达、QC07/15 vacuity、QC12/13四态不支持、QC14 finalpost 当成128周期或无界证明。

仅在新执行审计和结果目录写入。允许生产者在共享HANDOFF/STATUS prepend本轮准确短状态并保留全旧body；不修改封存R03、旧实验/score/Claude oracle/freeze，不触及Git index/add/reset/commit/push，不做G2–G5/API/count/generation/key/network/install/delete、新chat/agent。完成后停于既有P13保存证据独立复核，不能自认科学资格通过。


P12-N1是非阻塞来源说明：network=0只适用于受控G1准备，整turn曾偏到历史PPT/web读取和无关辅助记录，P12a证据保留；请本次执行/closure侧车如实限界，勿改R03原件或宣称整旧turn只有G1/无web。原作者部分经过1466.6785秒、P12全turn约575.6秒属于准备/复核，不是本次1198秒实验窗口，不混成0。
