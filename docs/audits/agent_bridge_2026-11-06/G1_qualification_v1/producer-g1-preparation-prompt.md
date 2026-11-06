继续 COMS6998/test2。新用户明确授权 G1 本地公开资格验证，并要求完成后独立复核、尽量使用 Hallmark。此消息在您 idle 的安全检查点发送；无需再向用户确认这份明确额度。

<transcript_evidence>
助手：“G1 计划不需要 API key，也不调用模型 API，但会使用你电脑的计算资源：最多 32 项 BMC/cover、32 次物理仿真和 32 次编译，整体拟限制在 20 分钟内。你同意我让项目 Codex 按这个上限启动 G1，并在完成后交给独立复核吗？”
用户：“说一说目前完成的任务是什么意义，为什么到现在还没到api live test呢，G1是什么x又完成了哪些内容呢。并且我同意项目codex按这个上限启动G1并在完成后交给独立复核！记得使用hallmark”
</transcript_evidence>

先读取 AGENTS.md、HANDOFF→STATUS、test2/AGENTS.md、EXPERIMENT_PROTOCOL、相关DECISIONS；当前真实HEAD刚查为c25180848ebfe9a1f49da0aa5f579cac913e6428。电脑shell和此local聊天可达；旧四freeze+acceptance7450成员0差异，G0接受sidecar仍0a13e9a5b8b78efdc900d0e0ad7e7d215bf5700c14b7082b2237164b448fd51c。保留全部dirty工作、旧分数/未知/负结果/历史授权和已封存D01/I01/C01/P01-P09/E05；不重做PPT、不重跑旧cohort来恢复上下文。旧文档“G1未授权”是当时历史，不能据此拒绝本次新grant，也不能回改旧draft/phase。

新授权源：docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/user-authorization.json。范围是一个预先固定profile、16类公共小型SV语言/时序/表示控制QC00–QC15，不是新FIFO DUT/oracle或模型实验。G0已接受synthetic metadata，不能冒称真实G1链已被G0通用验收，勿修改G0源码来接纳新run。新代码/source/schema/runner/registration/results需全新namespace（例如test2/g1_v1、test2/configs/g1_qualification_registration_v1.json、test2/results/g1-qualification-v1，若冲突取新唯一版本不覆盖）。

总资源池（producer/reviewer共用，不按agent或重启重新给额度）：最多32项BMC+activation cover合计，depth=8，每项<=10s；最多32次physical simulator runs、每次<=32cycles且合计<=1024cycles，每次<=2s；最多32 compilation jobs，每项<=20s；本次资源执行总wall<=1200s。不能运行prove/unbounded。setup/native frontend编译/两个simulator编译/失败/timeout/重试/解析和process cleanup均显式计费，不能把Yosys prep或失败编译藏在帽外。可预先登记共享/批量编译，让16个native prep与两个physical套件共用编译在32内；不能默默降成单simulator或超compilecap。全部budget、global halt、剩余数持久化，启动前预留/记录，timeout kill整个进程组，失败/NOT_RUN/NOT_REACHED保留。Runner总deadline从本次实际setup/version/compile/native/physical执行入口开始到结果解析输出为止，不允许跨runner/新profile重置；代码/文档准备和独立只读审阅的elapsed另列，不能把机器执行setup前移到计时外。

当前先完成 G1-R01 PREPARATION_AND_REGISTRATION，并在执行任何编译/仿真/native job之前给协调端一个安全交接点：
1. 以封存D01 public_controls.md/index和E05 plan G1为需求，给16类控制具体最小源码、固定width/signedness/truncation/完整guard、clock/reset/initial、具体预登记输入序列、pre/post/selected slot和expected结果/适用范围。16类可读需求并非已经资格通过，不把占位模板转真实release。
2. 期望标签来自公开、可手算的语言/小状态机事实，不看将来的工具结果再改；由既有独立reviewer在P10执行前只读核验这些标签。GPT公共toy控制不是替代Claude FIFO独立reference；不修任何旧oracle，不调用Claude/API。任何依赖新DUT规范/真实oracle的结论保持UNQUALIFIED，留G2。
3. 固定同一个现有工具/profile、工具路径/版本验证方法、确切flags/conversion链、job顺序、source与waveform/input SHA、期望与不支持矩阵、预算accounting规则和停止条件。物理按原计划使用现有两个simulator，对每QC最多各1run，共<=32；BMC/cover各最多1，总<=32。编译计数选择须在结果前明确，复用/批量编译的source/hash和工具child过程不能隐去。不存在某工具/无法安全在帽内跑的项目如实UNSUPPORTED/NOT_RUN，不安装或下载替代工具。
4. QC07空泛guard不获资格；QC12/13 literal X/case-equality未知检测不强行称二态SMT保留四态等价；QC08/09 native delayed assert与直接pre/post样本严格分开；QC10/11 reset/initial/clock合同不能换；QC14只验final-post trace_done transport，不加clock、不改DUT，QC15 trace_done=0不得获完成性credit。全部finite depth8不外推128或unbounded；不能把本次结果解释为74历史未复现的统一根因或C的能力差异。
5. 允许构造和读源码/预登记输入、现有工具路径检查及必要轻量纯Python预算/拒绝路径mock验证（记为mock非G1资格，全部保存失败）；不能在preflight之前悄悄运行真实compile/sim/native“试试看”。工具版本实际探针纳入后续执行runner的setup记录。无API、token count/generation、key读取/配置、网络/安装、commit/push/删除。
6. 新registration/manifest/新用户grant先封存精确source/tests/expected-input/labels/config/runner/caps SHA，更新紧凑HANDOFF/STATUS当前G1新授权入口但保留旧正文。将R01 phase.json/snapshot-manifest.json路径/SHA交协调端，状态PREPARED_PENDING_P10_LABEL_AND_RESOURCE_REVIEW；本次turn在这个安全检查点停住。协调端即交既有reviewer做只读P10，接受后会在您idle时发送同一授权下的EXECUTE，不再向用户索取G1许可。这个交接是先冻结标签/计数的技术门禁，不是新的用户审批。

之后执行范围已授权，但须按冻结R01/P10 exact版本，不能依据工具outcomes换profile、修控制后重跑或开第二repair-profile。若首次结果失败/timeout/unsupported照实报告和保留，不删或自动重试；超帽或声明支持类出现实质不一致则停止该资格升级并保存剩余NOT_RUN。独立后审默认只解析新保存证据和做RTL/数学检查，不重新给一套32/32/32预算。需要额外运行或修复profile时明确剩余额度和新version/具体请求，不自行扩展。

Hallmark：后续独立审查遵循 docs/audits/agent_bridge_2026-11-06/hallmark_usage_check/future-review-policy.md；实际读/use要记录。可借鉴review-finish的独立固定输入、具体定位/最小修订和发现排序，不能把网页审查当RTL正确性，不能向candidate prompt注入skill、维护说明、oracle/hidden数据。当前阶段没有candidate/API prompt。您负责公共控制/driver/infrastructure，不宣称独立接受。

本次没有G2/G3/G4/G5、真实新DUT数据/新B/C generation的授权。旧live已完成36generation+36count、B/C最终均11/11，C多9.85711% tokens；不重复饱和数据强求正结果。未来模型API确需时先具体说明service/purpose/model/calls/token/USD/timecaps与安全凭据方案，等用户针对具体调用确认，不在聊天要key、当前不处理key。
