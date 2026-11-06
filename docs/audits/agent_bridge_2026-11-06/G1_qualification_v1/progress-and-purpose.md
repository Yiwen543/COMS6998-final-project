# 已完成工作的意义与 G1 当前状态

截至本次新授权前，G0已完成限定的合成元数据接口实现、失败路径测试与独立复核。P09新跑93项测试、回放469保存案例、28独立探针、6CLI控制；这些计数不是独立模型试验或新科学结果。它让请求身份/上下文/哈希、全局停止、费用未知和输出不可覆盖有明确、受限的校验能力，减少后续实验“链路坏了却验收通过”的风险；不证明RTL或形式前端正确。

本项目此前已完成模型API live，不是从未到live。最新旧批次报告controller-done-live-report-v4记录36次实际generation和36次count、0retry、1554292实际tokens；B/C最终均11/11可观察类型，C tokens多9.85711%。旧实验及旧USD20任务已关闭，原始分母/负结果/未知费用与历史资格限制保留。直接重复饱和cohort不能解决任务区分度或工具表示问题，也不能强行得到C优势。

本轮新研究尚未进入新API阶段，是因为先要确定形式工具与物理表示的受支持范围，再视需要建立独立Claude规范合同、新任务/数据与公平比较注册。旧grant不能自动沿用；未来模型/调用数/token/USD/timecaps和输入隔离须另行具体确定。当前不需要API key，不处理凭据。本次G1授权只开放本地公开资格验证，不开放G2模型API、新候选生成或新B/C实验。

G1是公共的小型语言/时序/表示控制资格包：QC00–15覆盖恒真/恒假、width/truncation、signedness、完整guard/vacuity、pre/post与边沿偏移、reset/initial/clock、X/case-equality和trace_done transport/completion-credit边界。用预先固定的源码/输入和独立审核标签，对照一个工具profile的BMC/activation cover与两个physical simulator。它产出具体支持矩阵、真实状态/原始证据/成本；depth8不意味着128周期或无界证明，公共toy controls也不是真DUT faults/coverage。

新授权前已完成G1纸面定义/失败矩阵与权限规划，尚无G1实际compiler/native/physical结果。新授权已在producer idle时交付：先构造具体R01/冻结标签和预算，由既有reviewer做P10只读标签/资源预检；通过后由同一授权执行，不再向用户重复索取G1许可。执行后再做专项RTL/记录审查，并真实记录Hallmark使用。

共享资源总池：BMC+cover<=32，depth8，每项10s；physical<=32runs/1024cycles，每run<=32cycles/2s；compile<=32jobs，每项20s；runner实际设置/版本/编译/执行/解析总窗口<=1200s，不因重启/agent/新目录重置。准备和只读审阅elapsed另列；不把机器执行setup前移计时外。全部失败/timeout/unsupported/NOT_RUN成本保留。一个profile，不能根据工具输出改profile再悄悄重跑。

证据：旧报告test2/results/controller-done-live-report-v4/report.md；G0接受test2/results/g0-adapter-acceptance-p09-v1/independent-acceptance.json；本次grant user-authorization.json；刚读preservation-baseline.json确认HEAD c25180848ebfe9a1f49da0aa5f579cac913e6428，7450旧冻结/acceptance成员0差异。旧文档的未授权字样是当时历史；本次新grant另存，不回写旧freeze/draft/phase。当前进度以state.json及新R01/P10/执行记录为准。

下一次API需区分：G2若确需新独立reference，可在G1和具体public合同/服务预算授权之后先调用Claude作者与fresh reviewer；不必等GPT B/C已登记完成。新的GPT B/C candidate live才进一步依赖G3/G4。当前两类新API均未获本次G1授权，模型/费用帽也未准备。
