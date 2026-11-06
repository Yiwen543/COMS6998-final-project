# P11 — G1 E01 首次 setup 失败后审

**整体：CHANGES_REQUIRED（后续执行准备度）；E01失败记录完整性：PASS_WITH_LIMITS；G1资格：BLOCKED / NOT_QUALIFIED。**

E01保存的失败、成本、冻结和停止证据一致；没有把first setup ERROR冒称为16QC通过。当前源/环境组合的PID监控依赖仍阻塞后续执行。失败记录可独立作范围限定的metadata接受，但不得重写E01、补跑或重用旧pool/receipt。

## 精确输入与保全

- E01 phase SHA：6fd9815afc1d8ae58cb6764ed3f1f40ec85ca49c2320751b1b6421cad4a3cd14。
- E01 manifest SHA：61144719d65b06a3feab6fa1abb7f05b065fb136a1993b093912ca15188f1116。
- EXECUTE receipt SHA：9a6dfd949c54e1a159ff4b3e8e97999edc306c8dcac3cf3b233785a29de0dd95。
- P10B review SHA：864e76e168db17878e29bbf1d580b546620497acf269b3dcb34a144775c460dc。
- R02 manifest SHA：7c16e5020ab6212fbd66bdd57ecb272bef56e1bfc6ce4362a661960d331fb201。
- Registration SHA：85185519c5a6e2a8eaaf843b5b27c9cc312ada2fc8c44af6f915368759d98268。
- 原grant SHA：bf3da44d7cda9eadfabebf82b23271854465942a3814f36b90789f7e715575ab。
- 实际HEAD仍c25180848ebfe9a1f49da0aa5f579cac913e6428，不代表全部工作树成果。

152份E01成员、138份R02成员、43条source绑定、58条E01输入/输出绑定以及398份保护清单文件均匹配，当前E01副本无漂移。注册、flags、labels、source/profile和cap没有根据本次结果修改。HANDOFF/STATUS仅插入E01元数据，旧body保留。

另对照P01基线新鲜核验两个旧score与冻结Claude checker：
- controller-final-v1/scores.json：f13161340a46c7360002e54992be0a7aba9c1d47a70fbe6f169bba8952fe2651。
- live-final-v1/scores.json：33003b33a7172d29704f85fa84da10bdbb30aebe78b72d400a4f97b73a2ef338。
- reference/frozen-v2/checker.py：b44f32b27c11b968d23fd93ecf8b0d714e773460fc0b505d89adf23df3cd7dee。

只是哈希核验，没有重新评分、执行checker或重审整个旧cohort。完整清单见input-manifest.json。

## 原始失败与实际资源

实际启动记录时间：2026-11-06 00:12:09 America/New_York。

第一项argv为 /opt/homebrew/bin/yosys -V，receipt明确dispatch_attempted=true、process_group=44006。之后/bin/ps -ax -o pid=,ppid=,pgid=,comm=抛出：
PermissionError:[Errno 1] Operation not permitted: '/bin/ps'。

原始setup receipt SHA：40e0652ab082f08953aaf3dda69c330e501df45f7bd1e535a5e77f0ef384eb5f。

| 项目 | 已保存事实 |
|---|---|
| runner CLI | exit1 |
| setup job | ERROR，timed_out=false |
| Yosys root exit/version | null / UNKNOWN，不能补0或依据路径猜版本 |
| runner stdout/stderr | 均0字节 |
| setup stdout/stderr | 均0字节 |
| monitor_calls | 0次成功；异常路径证明至少此次失败attempt，不能解释为没有监控尝试 |
| observed_processes / inventory | [] / incomplete；不证明无子进程 |
| cleanup_group_kill | true，记录清理调用成功路径；不是全进程树独立终止证明 |
| job总账 | 1 ERROR +89 NOT_RUN |

四份emptylog SHA均为e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855。没有输出不能推断Yosys不支持SV；根本未编译任何QC。

pool已halted=true/completed=true，唯一setup reservation=1，compile/native/physical/cycles全0；关闭状态和setup成本必须保留。记录global elapsed=0.04572445806115866s，setup含cleanup=0.0056856251321733s。它们是本次局部monotonic记录，不是整轮/封存/后续诊断耗时，也不能证明一般OS时序或完整child cleanup保证。outer tool wait约0.02235s是不同观测范围，不能代替runner窗口。

unused32compile/32native/32physical/1024cycles/7setup不是重跑授权。计划18逻辑编译批次本次实际0次，不能记为已经执行18次或以剩余额度换新profile。

原始result-manifest有85成员：**81份旧regression准备证据 +3份本次setup日志/receipt +1份report**。它们不是85次新实验。没有本次native/physical VCD或rows。

## 16QC结果矩阵

独立P10数学/固定状态推导仅在source/input字节一致后复用，不是本轮新工具结果；P10/P10B接受不替代实际资格。

| QC | 预登记范围（非实测） | 本次BMC / cover / Icarus / Verilator |
|---|---|---|
| QC00 | 有限公开控制 | 全部 NOT_RUN |
| QC01 | 有限公开控制 | 全部 NOT_RUN |
| QC02 | 有限公开控制 | 全部 NOT_RUN |
| QC03 | 有限公开控制 | 全部 NOT_RUN |
| QC04 | 有限公开控制 | 全部 NOT_RUN |
| QC05 | 有限公开控制 | 全部 NOT_RUN |
| QC06 | 有限公开控制 | 全部 NOT_RUN |
| QC07 | 空泛/不可计资格 | 全部 NOT_RUN |
| QC08 | 有限公开控制 | 全部 NOT_RUN |
| QC09 | 有限公开控制 | 全部 NOT_RUN |
| QC10 | 有限公开控制 | 全部 NOT_RUN |
| QC11 | 有限公开控制 | 全部 NOT_RUN |
| QC12 | 四态等价不支持 | 全部 NOT_RUN |
| QC13 | 四态等价不支持 | 全部 NOT_RUN |
| QC14 | 仅运输 | 全部 NOT_RUN |
| QC15 | 空泛/不可计资格 | 全部 NOT_RUN |


完整逐QC四个实际状态、预期分析类别及理由见per-qc-review.json。尤其QC07/15的纸面空泛与QC12/13的四态限制，不得改写成已观察cover NOT_REACHED或已运行的UNSUPPORTED。QC14运输也没有实际执行；无128/unbounded、FIFO/DUT/oracle/monitor或B/C结论。

## P11-R1 — 已证实环境/监控依赖阻塞，P2，material=true

位置：runtime.py:18、:42–57、:61–89；runner.py:107。runtime SHA 61689aad92c17045267fcfc0871cc4eae63c1d8aaeb2044bc44834734a9876f8。

控制流是：
1. 原deadline检查后Popen返回root PID。
2. while中调用/bin/ps；PermissionError在monitor_calls增加之前发生。
3. 与实际工作共用的通用except记录ERROR；finally执行组kill/wait路径。
4. runtime持久halt，runner立即break，保留89个NOT_RUN并complete pool。

这是当前代码的fail-closed路径，不是错误放行或造假。问题在于声称best-effort的inventory成为未获环境支持时的致命依赖，当前源/环境组合无法完成G1。确切sandbox/宿主策略原因未核实；这里只能确认已保存的exec PermissionError，不能称自动审批驳回。

三个独立纯fake对照均用精确runtime/budget副本、原caps、原停止规则：
- monitor可用：假子进程正常结束，RETURNED。
- monitor拒绝且假子进程仍运行：ERROR、root receipt exit=null、组清理、halt，复现E01路径。
- monitor拒绝但假子进程在清理前已结束：仍ERROR/root receipt exit=null，说明监控错误不能证明真实root退出码或版本结论。

这些fake返回码不填入E01。实际OS进程、ps、signal和sleep调用均0。最终输入字节和SHA在validation前保存；脚本及逐例输出见permission-probes和evidence-manifest.json。

### 最小、可review的后续方案

不改E01/R02原件，不启动修复实现。可先形成新版本提案：

- 如果inventory确属可选：在单独observer边界处理PermissionError/OSError/监控timeout，记录attempt/error/time/knownness及inventory_complete=false，不冒称空列表代表完整普查。
- 原PGID、原始absolute deadline、poll、必需kill/wait、失败计数/停止与日志证据保持。不能一起禁掉budget/cleanup；进程组或cleanup不可用仍必须fatal/unresolved。
- 若inventory被定为必需，则须明确该依赖、最小执行权限范围和新资源决定；一次单PID诊断许可不能扩成全局ps或G1执行许可。
- 后续纯regression应覆盖inventory拒绝/timeout、normal child、pending child仍按原deadline kill、PGID/kill/wait失败仍halt。新源码/registration封存及独立预检后，也不能自动重用已关闭pool。

修订方案可在既有只读/维护范围内准备；真实retry需要明确的新资源/权限决定，保留本次setup=1成本和全部未知。无需API或chat key。

## 外部诊断的单独边界

permission-error-diagnostic.json SHA：5d030419c5c44627f58e74262a636afc7f0bff539403663675b6743dd2400134。

协调端另记录一次经工具审查批准的read-only require_escalated单PID查询，exit1、无输出，说明该记录PID在之后查询时不存在。它不是E01内数据，不是全部后代/PGID消失证明，不是G1重跑，也不是自动审批拒绝。未读取进程命令行/env。

本轮仅读取该记录，没有重跑ps或oskill，没有改变sandbox权限。原用户授权消息经协调端复查仍无新重跑指令；P11不再翻取全历史。

## Hallmark及其他限制

本轮read_this_round=false，引用已验证同版P10实际读取凭据；原P10 review SHA cca7589786545675331ba1daa163d4e5cc757795aa8ac57972404e7463ee73e1。当前SKILL.md SHA 25a1ff92d925b2389e8409f42fb8ad7e033fceca8b5d1f07ed4ca4c28da53dc3，review-finish SHA 9d00de59e71ee2516212140b0512d6d2e90a120d4a328eeba9cb12396ff38d64均匹配。

实际应用固定输入critique来区分原始证据与总结、资格与记录；按实质影响定位P11-R1并提出最小新版本建议；明确不得稀释关闭pool、已花setup、unknown和NOT_RUN。workflow_executed=false、scripts_executed=false，没有UI/Together/API。RTL/OS/resource结论来自专项源码/原始证据及纯fake，不来自Hallmark技术引擎。

P04 mismatch/causeUNKNOWN、P05/P06限定范围、P05-N1、F1/H1/H2/L1、selected sample/category、general soundness、历史billing UNKNOWN、R0/R1/R2 planned全部保持。398保护文件和3个关键叶子核验不等于完整4837/7450成员审计。

只写P11目录；不编辑source/shared/旧结果、不发消息或新建agent/chat。没有重跑旧suite/实验，没有实现修复、重试工具或开始新profile。完成本次失败后审后停止。

证据索引SHA256：87c094065c0624da2261aa1931ea004d62ad0ebb1efa98ca02585c98524f0861。
