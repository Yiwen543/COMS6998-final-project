请在既有“复核 test2 项目”聊天进行 P12 增量独立复核。对象是 R03 的精确封存版本；不得修改推进代码或共享 HANDOFF/STATUS，不发送任何消息给活跃推进线程。输出到新目录 docs/audits/agent_bridge_2026-11-06/P12_g1_retry_preflight/。

身份：实际 HEAD 应重新读取，旧审计 HEAD 不作当前值。R03 phase、manifest、registration、source manifest 及各 SHA 将由协调器在此模板之后补齐。先验证这些绑定、旧 E01 终止池和 P11 原件。引用 P10/P10B 已接受的未变语义，勿重做旧实验。

授权：用户原 G1 授权已包含同一任务的合理重试，不因重试再问确认。continuation-decision-r03.json 只是从原授权分配剩余额度，不扩大权限或资源。旧失败池不可修改、清零或重启。原上限累计为 compile32、BMC+cover32(depth8、10秒/项)、physical32(2秒/项、每项32周期、总1024周期)、实验执行墙钟1200秒。E01 已计 setup1、实测0.045724458秒，续行保守 charge2秒，当前尝试至多1198秒和7个 setup。准备和只读复核经过时间另行披露。执行前必须使全部历史用量、旧池身份和终止状态成为机器检查的前置条件。

本轮关键：
1. 验证真实路径已注册 owned_process_group_only，完全不调用已知被拒的 /bin/ps；没有提升权限或绕过访问限制。PID/PGID、poll、原绝对截止时间、进程组 kill/wait 仍必须执行，不能因为可选清点缺失而略过；必要保护失败须停止并保留未知。inventory_complete=false/不可用/未测子进程应如实记录，不能将未观察当作无人存活。静态确认即可；不得运行真实 ps 或新工具探针。
2. 独立纯 Python 假时钟/假进程测试覆盖 PermissionError/OSError/可选监控超时、已退出/仍运行、清理与必要权限失败。确认失败后没有继续派发或退还已预留用量。重验 P10-R1 的慢持久化/mkdir/log 临派发截止检查及 P10-R2 的 VCD EOF 覆盖拒绝，纯假输入即可。
3. 累计账本：新池须绑定不可变旧池 SHA、原授权和续行决定，继承 setup1 及时间 charge2，最多再7setup/1198秒。不允许把新版本当作新32/32/32额度；不得伪造旧用量零、重启或接受旧执行收据。新池重复创建、祖先/额度/版本/输入哈希漂移应拒绝。解释是否需要跨进程并发支持，勿超出受限单进程已登记路径泛化。
4. 版本变更应只涉及权限修复、续行预算及必要门禁/路径。18SV、手算标签和输入/观察相位、native/physical flags/order语义保持。仅省略非语义 setup-make --version 以维持累计8setup；记录 make 版本本轮未重探，不能声称刚验证过。18 logical compilation batches不等于18OS进程；孩子仍计入根作业和全局预算。
5. 新 EXECUTE 门禁应绑定本轮 P12 接受结果、R03 manifest/registration/source 和 continuation，不依赖过期硬编码 P10。评审接受不自动执行，协调器随后交付精确 EXECUTE。若发现实质风险，给可定位证据、影响、最小修复及验收条件；仅重大风险才建议打断生产者。

Hallmark：按用户要求尽量使用，真实记录本轮是否新读，或引用已核对同版本的先前读取；说明实际用于固定材料独立批评、证据组织与问题优先级的具体位置。其网页/UI流程、脚本不适用于RTL和资源门禁，不能替代技术专项复核，也不能编造已运行。可 fresh read SKILL.md 与 review-finish；记录 SHA 和适用性。核心结论来自源代码、预算逻辑和独立假输入。

本轮额度为只读代码/保存数据和轻量纯 Python 假输入检查；真实版本查询、编译、BMC/cover、仿真、API、网络、安装、凭据、旧实验重跑均0。禁止 git add/reset/commit/push，保留其他工作和索引。

交付 review.json、简短 review.md、hallmark-usage.json 和必要测试证据，status=PASS_WITH_LIMITS 或 CHANGES_REQUIRED，绑定 input_identity.producer_manifest_sha256、registration_sha256、source_manifest_sha256、continuation_decision_sha256；分别报告修复关闭范围、剩余限制、是否可在剩余额度内安全重试。只做比例适当的验证，不为补记录再跑完整套历史测试。
