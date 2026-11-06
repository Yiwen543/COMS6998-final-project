# P13 — G1 R03 E02 执行后独立复核

**证据完整性 PASS_WITH_LIMITS；执行资源合规 PASS_WITH_LIMITS；公开资格 BLOCKED / NOT_QUALIFIED。整体 CHANGES_REQUIRED，针对后续完整资格准备。**

E02不是完整89jobs通过：13根作业返回0，首个QC00-Icarus行合同拒绝后halt，76job保留NOT_RUN，0个控制完成双sim资格。旧错误/成本/unknown均保留。本轮只有保存证据解析，0版本/编译/native/仿真/测试/API/ps。

## 精确输入与保全

HEAD实际读取为c25180848ebfe9a1f49da0aa5f579cac913e6428，不等于全部dirty成果。packet SHA2161cd4803adfbdef067d5fb4af4905d6d9de79360ea59d8a8a7afc1bde9dde6；E02 manifest cb207fe73f2911df992c03591374e4911bd9bffdf8839ba883911a438ffbfd49。

733封存成员、48源绑定及3077个E02 pre-entry保护文件0失配；旧R03 manifest及649成员完整，P12/EXECUTE/grant/continuation/E01终止池精确相符。前后再次确认current匹配，index指纹未变。另只读核验2旧score+1冻结Claude checker叶子SHA不变，不声称重审全部freeze或重新评分。所有依赖SHA见input-verification.json及historical-leaf-check.json。

## 实际运行、费用与停止

| 指标 | E02本次 | 含E01累计 | 剩余 |
|---|---:|---:|---:|
| setup |7|8|0|
| 逻辑编译根作业 |3|3|29|
| BMC+cover |2|2|30|
| 物理仿真运行 |1|1|31|
| 物理周期 |4|4|1020|

本次7setup+3compile+2native+1physical=13个returned0；不是总OS进程数。Icarus预处理/编译和Verilator的c++/make等子命令保存在原始build日志，完整子进程计数UNKNOWN。

本次记录窗口5.151964417193085s；E01实际0.04572445806115866s与保守charge2s分列。最终累计实际checkpoint5.197697583120316s、累计保守checkpoint7.151973249856383s；分别取样有微秒差，未强行修成同一时间值。当前1198s/累计1200s没有重分配；所有13收据的setup2s/compile20s/native10s/physical2s单项记录均在帽内。BMC/cover argv均depth8。本次8行、4posedge，0accepted rows；内存未测。

当前pool/lock已halted/completed，不能reset/resume。runner exit1，halt_reason=Unqualified:PHYSICAL_EXPECTED_MISMATCH:a。stdout/stderr根入口为空，详细日志在各job；没有把空入口日志当未执行。各job原始receipt和stdout/stderr与账本/plan逐项一致。

## 真实进程保护与版本

13收据均owned_process_group_only，inventory attempts0/complete=false，root exit0由CLEANUP_WAIT记录，owned-group probe均ABSENT_AT_OWNED_PROBE_NOT_A_CENSUS；无mandatory保护错误/timeout/SIGKILL记录。实际未走timeout-kill分支，不能称真实kill故障路径已全面通过；完整child生命周期及脱离组后代也未证明。

精确runtime仍是P12接受版本，无ps扫描；argv/源/收据相符。组探测与poll/wait保持，deadline来自同一个起点及原job帽。本轮不调用ps、signal或重查PID。

7setup原始日志保留Yosys/Z3/Icarus/vvp/Verilator/clang版本文字。smtbmc只输出help，版本UNKNOWN；make没有重新query，不能填成新验证版本。此前PPT/web偏移已在E02 sidecar按P12-N1披露，本轮不重查/不改写该历史。

## P13-R1 — 首拍刺激未建立已知值，P2，material=true

位置：test2/g1_v3/sources/physical_tb.sv:4、19–24；common.sv:3、5–14。TB SHA8582031db7abc155aeccfc09f8935e0cdc6e3c41ea31b7c8b1001c296ab28bdd；common SHAf5e448f2e32ef2c26322e198ca7dff72618818572a4a02ce85728b5377dd2c12。

原始QC00-Icarus stdout SHA309593fafed18238b0ee6576ec9d0cf4075c2f6bba4d5ecf9154040add7f4bff，VCD SHAf81b528090d499897c07f03d0e163cfbdbb1d239fbf8cb19267822d7a1a55e11。独立OBS/VCD解析：

- cycle0 pre1000/post3000：a/b=xxxx，rst/en/valid/active/ok=x；期望a=b=0000/rst1/en0/valid0/active0/ok1，共14字段不一致。
- cycle1–3全部六行与原表一致。VCD与8行stdout逐字段0冲突，phase/step也一致；记录跨度0..16000，4posedge为2000/6000/10000/14000。
- step在time0已经000，首轮再赋000，直到4000才变001；输入至4000才已知。stimulus为always@*。若该块在第一拍前有效求值，常量默认/step0分支会给出已知输入；保存现象与time-zero未触发有效初次求值一致。

这定位了启动/组合刺激建立缺口，**没有内部事件队列或修订运行证据，不断言Icarus bug或某修复已验证**。原生cover VCD的初始输入是已知reset表，后来激活；它与坏首拍物理轨迹不能组成合格对照。

影响：QC00物理合同不合格，不能因为进程exit0、后六行正确或native PASS而给资格。observations.py:15–34按冻结表拒绝是正确fail-closed，没有把X转0、跳首行或伪造通过。

最小修订：只在新版本保证首观察/时钟前合法刺激已初始化并稳定；尽量仅修physical TB启动，保留原0..3输入/复位/4posedge/phase/marker/标签。具体改法留给producer，不能就地补旧source。验收需新封存预检及计入额度的双sim真实0..3行/VCD一致；不能用纯mock声称SV调度已经修复。

## 16QC状态

| QC | 实际native | 实际Icarus / Verilator | 预登记限制 |
|---|---|---|---|
|00|BMC depth8 PASS，cover step2 reached|首拍合同拒绝 / NOT_RUN|有限公开控制，未完成资格|
|01–06|全部NOT_RUN|全部NOT_RUN|未观察，不补预期结果|
|07|NOT_RUN|NOT_RUN|空泛不可计正确性|
|08–11|全部NOT_RUN|全部NOT_RUN|pre/post/reset/initial映射仅纸面支持|
|12–13|NOT_RUN|NOT_RUN|四态等价不支持是声明边界，非实测结论|
|14|NOT_RUN|NOT_RUN|仅finalpost marker运输，无额外DUT时钟/输入|
|15|NOT_RUN|NOT_RUN|trace_done0无完成性credit|

完整逐QC JSON在per-qc-review.json。原手算材料/源码与P12/P10一致，复用既有有限分析，不重做实验。QC00的两个native PASS只表示当前depth8模型及激活cover，不是128周期/无界/真实DUT证明。

## 后续额度下界与可复用范围

完整16QC×2sim仍需至少32次合格物理运行：已运行的QC00-Icarus不合格，不能抵扣。剩31，因此**原累计physical32帽至少差1，完整下界需累计33**；新增128周期、累计132，周期帽1024无需因此增加。该结论不授权增帽；不得仅以同任务retry自行扩大。

若只改physical TB，common/QC00 formal/输入/SMT/profile/depth/tool pin/原生argv均不变，旧QC00 BMC+cover有条件复用为局部真实证据。新登记必须绑定旧SMT与源、日志/receipt/P12/E02身份和费用，显式标REUSED_FROM_E02，不伪装成新执行；新physical输入/phase仍需符合原合同。

该路径新增15formal compile+2shared physical compile=17，累计compile20≤32；新增native30，累计32≤32；setup新0，累计8，版本明确复用而非重探。若拒绝复用而全跑32native，累计34，另需native帽+2。上述是无额外失败/诊断下的最小下界，不保证任意修复都只花这些资源。

当前R03 runner/gate没有reuse或E02后续分配机制，旧pool/lock已闭合，不能只改路径接着跑。必须新显式登记/累计分配/门禁，继承E01+E02；setup已无余量，新版本query不能偷偷发生。可选择保守累计charge8s（覆盖现有7.151973250s checkpoint）后至多1192s，维持累计1200；这是待登记示例，不是新执行额度或实测耗时。

不增帽时，可接受当前失败/部分证据并停止；或另登记最多31新physical的受限部分方案，明确至少缺一个合法pair、未完成dual控制、总体NOT_QUALIFIED，不降低验收或按结果挑有利控制。完整覆盖需要具体physical32→33决定；合理retry本身无需再问同一个许可。未发现新增ps/escalation/API/key权限需求；未来必需PGID权限失败仍须halt。

## 方法、Hallmark与边界

Hallmark本轮新读SKILL.md及review-finish，SHA/证据/实际应用在hallmark-usage.json：固定输入独立critique、原始观测优先、定位排序与最小修订。网页/UI workflow/scripts=false；没有Together/UI工具。技术结论来自真实保存日志、RTL与独立解析/整数计算。

实际命令inspect_saved_e02.py exit0；历史3叶子SHA/预算整数计算exit0；finalize_p13.py最终保全/报告核对exit0。Git只读confstr临时目录warning不影响exit0。无reviewer harness失败，无旧测试、mock或生产parser回放。输入/输出和命令源SHA在evidence-manifest.json。

旧分数、Claude checker、所有unknown/timeouts/74未复现/selected样本归因/128completion、P04/P05/P06/P05-N1/F1/H1/H2/L1/billing及R0/R1/R2计划均保留。只写P13，不改source/共享文档/原结果/index，不联系producer，不新agent/chat；到此停止。
