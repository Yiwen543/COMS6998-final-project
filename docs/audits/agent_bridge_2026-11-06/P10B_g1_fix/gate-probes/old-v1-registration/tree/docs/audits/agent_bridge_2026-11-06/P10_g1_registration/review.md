# P10 — G1 执行前独立预检

**CHANGES_REQUIRED：本 R01 的 EXECUTE 路由阻塞。** 不是额外用户许可请求。公开 toy 标签经独立分析无失配，但存在两项已复现的执行/证据门禁缺陷；必须先修订封存并增量复验，不能开始实际工具 setup。

## 输入和范围

- P10 packet SHA：b3af387386847f5eaeddacf7cdf94d90d42aafebc7c0e0cb7e60a44442fcac14。
- R01 phase SHA：f01830b520c5e2f87906a0770df6c67bc59f58178a69dd18d801f50750acb749。
- R01 manifest SHA：ba96cf663df3a7aa7cef9ca43d660e80bdefe09a9482178bd8fe6a198f5c12c7。
- Registration SHA：8feb9918911177827b53bc9669d1faaad68bfb75af3380ce019df4a80ca174ba。
- 新用户授权 SHA：bf3da44d7cda9eadfabebf82b23271854465942a3814f36b90789f7e715575ab。
- 实际 HEAD：c25180848ebfe9a1f49da0aa5f579cac913e6428；不代表全部工作树成果。
- 101份封存成员、37条source-manifest绑定、73份受保护来源均匹配；当前对应文件无漂移。完整输入清单见 input-manifest.json。
- 只读R01 snapshot；仅在P10目录复制源码和执行纯Python mocks/分析。没有compiler、simulator、solver、native、monitor、版本探针、API/key或真实execution资源池操作。

## 阻塞一：P10-R1，P1，material=true

**预算检查与实际派发之间缺少截止时间复查。**

位置：budget.py:49、:72–74；runtime.py:13、:23、:26。budget SHA bd1da562b6f11d69ee1f4768aa5c9bda52d0a46b636c5fd0d94454689c5ea395；runtime SHA 294636c620b88c40e04ef5e8a7c118950e261eaa25ba77489d6063f1d1fe028c。

独立纯mock：
1. 虚拟elapsed=1194，通过1195s工作截止检查。
2. 模拟reservation持久化耗时7s，不sleep、不启动进程，时钟到1201。
3. reserve返回limit=-6；runtime仍调用mock Popen一次，派发时间1201。
4. 随后才记录JOB_WALL_CAP_EXCEEDED并halt。普通100s正例调用一次；已过期1196s负例正确零调用。

期望：不派发；保留已占用reservation并持久停止。实际：已经超过1200s仍到达派发入口。事后halt不能撤销超时工具启动。文件系统persist、目录/日志准备也可能耗尽已检查的时间。

证据：independent-probes/deadline-crossed-during-reservation/result.json。精确fixture配置在已执行 independent_probes.py，脚本/result SHA列在review.json；真实OS进程启动数为0。

最小修订：在新封存源码中，持久化后拒绝非正或不足清理余量的剩余时间；完成目录/日志准备后，在Popen前按原始绝对root/global deadline再检查。不得延长原时钟、退还reservation、重开pool或丢掉拒绝记录。

验收：纯fake-clock覆盖reserve/save及目录/日志准备跨过工作/公共deadline；Popen调用必须为0，reservation已计入、halt和NOT_RUN可审计。正常派发/timeout保持原始deadline。无需真实工具job。

## 阻塞二：P10-R2，P2，material=true

**解析器把VCD终点之前的最后状态外推到文件结束后的观测时刻。**

位置：observations.py:81、:97–109；runner.py:116、:146–151。observations SHA 8b7d95a3d94a2f39bab703d7b01086b4641dc4de73efaa71a674c4e18f633091。

独立分析生成QC00轨迹，包含全部observer phase在3/7/11/15ns的转换。完整VCD结束16ns，绑定通过。删除15ns及之后尾部，VCD结束14ns，但最后要求的post观测为15ns；绑定仍通过。程序只取tick<=row.tick的最后状态，没有检查观测位于已记录trace范围内。

- 完整对照：analytic-preflight/full-observer-vcd.vcd，SHA 235ef77a66cff18146ac261bde9a3abedc1fdaa253d609c984f92270c0226c0e。
- 截断反例：analytic-preflight/full-observer-vcd-truncated-before-post15.vcd，SHA 25a20fc0821203d747744f9c6dad3b762bb299c1be13baa19a926b13ece8b0da。
- 独立观测表：analytic-preflight/rows.json，SHA 5181cc4468d4334265fef0144202180b6df1fdb6aa4839e4b924bd8127e84fa0。

期望：完整对照通过，缺尾部反例UNQUALIFIED/拒绝。实际：均ACCEPT。这可能使缺失末段的输出获得EXPECTED_CONTROL_OBSERVATIONS_MATCHED，属于G1新声明的VCD绑定范围内错误接受，不是要求补建通用旧实验parser。

最小修订：每个必需观测时间都必须落在VCD已记录时间范围内；缺尾部保留明确unqualified原因并停止，不能补造延续或重采样。验收使用以上精确对照/截断文件，截断例应因时间覆盖不足拒绝；不消耗实际sim/native额度。

复现两个问题的已执行命令为：
- PYTHONDONTWRITEBYTECODE=1 python3 .../P10_g1_registration/independent_probes.py
- PYTHONDONTWRITEBYTECODE=1 python3 .../P10_g1_registration/analytic_preflight.py

保留现有目录；需要重新执行时把精确exec_tree及脚本复制到P10下新的空review-owned目录。脚本拒绝覆盖已有证据目录。所有输入、脚本及输出SHA见review.json和evidence-manifest.json。

## 标签与语义核对：仅分析性预检

独立按common.sv表达式和固定4步输入推导，再核对生产者标签；没有调用producer标签生成器。验证128条Icarus四态期望行、112条已知Verilator期望行、256组4bit加法关系及16个signed4取值，均无失配。16份formal harness除ID之外相同。

| QC | 独立有限BMC期望 | activation cover | 首个definite负例pre周期 |
|---|---|---|---|
| QC00 | PASS | PASS | — |
| QC01 | FAIL | PASS | 1 |
| QC02 | PASS | PASS | — |
| QC03 | FAIL | PASS | 1 |
| QC04 | PASS | PASS | — |
| QC05 | FAIL | PASS | 1 |
| QC06 | PASS | PASS | — |
| QC07 | PASS | NOT_REACHED | — |
| QC08 | PASS | PASS | — |
| QC09 | FAIL | PASS | 1 |
| QC10 | PASS | PASS | — |
| QC11 | FAIL | PASS | 2 |
| QC12 | DIAGNOSTIC/四态不支持 | PASS | — |
| QC13 | DIAGNOSTIC/四态不支持 | PASS | — |
| QC14 | PASS | PASS | — |
| QC15 | PASS | NOT_REACHED | — |

输入域是step0..3固定刺激，然后idle至step7，initial q=0，单posedge时钟。它不是任意a/b输入下的普遍BMC证明，也不是128/unbounded证明。

- sum4是4bit赋值截断；full5为5bit零扩展加法。15+1时low4=0、full5=16，QC02/03区别真实。
- signed4(15)=-1、signed4(8)=-8；负号与msb匹配；unsigned<0恒假，QC04/05区别真实。
- QC06完整guard含valid/en/!reset/a!=0；QC07从不激活，不得因BMC PASS获得义务信用。
- QC08/09保留直接pre和post差异，sampled寄存器与延迟native报告分开。QC09既有真实的pre q vs expected-post负例，也有明确故意错置的phase claim；其拒绝不是DUT fault或实现错误归因。
- QC10初态/同步高有效reset；QC11只故意反转reset极性，q保持0，在pre2区别可见。没有宣称已覆盖任意异步reset/CDC。
- QC12在四态源中x001==0001为X；QC13 XOR为X而case-equality检测为1。native/Verilator二态结果只作diagnostic，不能声明四态等价或解释全部74历史未复现。
- QC14的marker仅observer finalpost可见，不是DUT输入，不加边沿，只是运输控制。QC15 active=0，不给完成性credit。
- 所有actual_result/waveform仍null/pending；公开toy期望不是GPT改写FIFO DUT oracle或新Claude合同。

## 资源、工具与生命周期

8setup +18逻辑编译根任务 +32native +32physical =90个固定根任务。编译为16Yosys前端、1共享Icarus和1共享Verilator；native为16BMC+16activation cover；双sim各16次、4周期/run，共128预留周期。

**P10-N1，P3，material=false：** 可接受“逻辑编译批次”作为此预登记的job计数，不能称18个OS编译进程。内部ivl/make/C++编译必须属于对应根任务的20s及公共1200s；不能额外免费、不能拿剩余额度开新profile。此项不阻塞，但R1未修不能执行。

源码检查了固定source/flags/order、binary SHA运行时验证、独占execution-state、预留先于派发、失败不退款、重复/重启拒绝、全局halt和NOT_RUN余项。公共timer在工具hash/version/build前建立；JSON/源的只读执行前gate不是工具setup。

runtime使用process group和超时kill，发现已知linger/cleanup失败即halt；PID采样明确best-effort、不穷尽。本轮没有实际OS生命周期证据，不能把空PID列表当无子进程证明，也不能宣称完整清理/供应链认证。后续实际执行仍须保留所有失败、cleanup未知、内部build日志及耗时。

本次无真实pool；实际result根仅含两轮mock。不存在第二个32-job许可，post-review只能读保存证据。G2/oracle/API/data/candidate/paid/key均未授权。

## 测试、时间与保全

- Producer保存初轮12和最终14项mock，均0失败；本轮核验对应5/6源码SHA。初轮源码由编辑记录重建、不是当时归档，该限制诚实保留；未重跑初轮。
- Reviewer在SHA一致review-owned副本新跑最终14项，0失败/错误，exit0，约0.0201s；只是Python预算/拒绝mock。
- 独立7次探针求值：3种虚拟timer场景、两对合成VCD绑定。第二对补足全部observer phase时序，确认同一尾部缺陷。全部真实OS/tool调用为0。
- 一个只读标签打印helper误遍历QC12的Verilator=None而退出1；已按unsupported处理并用独立推导核对。失败命令保留，不是产品工具失败。
- 本轮整体只读审查耗时未从turn入口计时，为null/NOT_INSTRUMENTED，不填0。producer记录的约973.327s authoring区间与执行timer分开；本轮未启动1200s执行钟。
- 101封存/37绑定/73保护hash未变，无current漂移；未重审全部旧4837/7450成员内容。原P04 mismatch/causeUNKNOWN、P05/P06限定范围、P05-N1、F1/H1/H2/L1、selected-sample、general soundness、billing UNKNOWN及recovery planned保持。

## Hallmark 实际使用披露

本轮新读SKILL.md v2.0.0（SHA 25a1ff92d925b2389e8409f42fb8ad7e033fceca8b5d1f07ed4ca4c28da53dc3），并新读references/review-finish.md（SHA 9d00de59e71ee2516212140b0512d6d2e90a120d4a328eeba9cb12396ff38d64）。

实际应用其适用原则：
- 固定输入独立critique：input_identity/input-manifest及独立数学/探针，不以producer意图替代证据。
- 精确定位、按影响排序而非个人偏好：R1/R2给source行、SHA、反例和实际输出；N1明确非阻塞。
- 最小修订且reviewer不改源码：每条修订/验收仅针对已证实缺陷，保留已固定标签与历史。
- 明确修订中不可稀释的内容：原公共控制、唯一profile/资源池、科学未决和权限边界。

considered=true，read_this_round=true；applicable_generic_principles_executed=true。**workflow_executed=false，scripts_executed=false**：没有网页/UI目标，不执行截图、sloplint、Together/API，也不声称Hallmark决定RTL正确性。专项结论来自单列的源码、数学及纯mock方法。

## 下一步

停止本R01的EXECUTE路由。在同一个尚未消耗的用户grant内，只修两个门禁、保留R01和全部失败，新增精确封存包并作有界增量验收。不换控制/标签/toolchain来迎合结果，不创建、刷新或扩张资源池。无需向用户再要相同范围许可；本结论本身不启动任何工具。

证据索引 SHA256：0bc7925ce58d31d2d341a4349cdbb41a47fd16ef59dfc99173a5fdabf8a5eb5f。
