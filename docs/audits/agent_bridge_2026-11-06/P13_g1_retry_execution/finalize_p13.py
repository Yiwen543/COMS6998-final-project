from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import subprocess
import time

OWN=Path(__file__).resolve().parent
ROOT=OWN.parents[3]
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):
    with Path(p).open('x') as f:json.dump(d,f,ensure_ascii=False,indent=2)
packet=read(OWN/'phase-packet.json');integrity=read(OWN/'input-verification.json');analysis=read(OWN/'raw-analysis.json')
audit=(ROOT/packet['producer_phase']).parent;snap=audit/'snapshot';code=snap/'test2/g1_v3'
phase=read(audit/'phase.json');resources=analysis['resources']
assert not integrity['mismatches'] and not analysis['VCD_stdout_differences']
# Confirm no producer drift during this saved-evidence review.
for row in integrity['bindings']:assert sha(row['path'])==row['expected'],row['path']
for row in read(OWN/'historical-leaf-check.json')['files']:assert sha(ROOT/row['path'])==row['expected']
index=subprocess.check_output(['git','--no-optional-locks','ls-files','--stage','-z'],cwd=ROOT)
assert hashlib.sha256(index).hexdigest()==integrity['index_sha256']

hallmark=dict(considered=True,read_this_round=True,version='2.0.0',source='/Users/yiwenchen/.codex/skills/hallmark/SKILL.md',source_sha256=sha('/Users/yiwenchen/.codex/skills/hallmark/SKILL.md'),read_evidence=[dict(tool='skills__read',package='e0/hallmark',read_this_round=True),dict(tool='exec_command',command='cat /Users/yiwenchen/.codex/skills/hallmark/references/review-finish.md',output_chunk_id='df2730',exit_code=0)],review_finish_source='/Users/yiwenchen/.codex/skills/hallmark/references/review-finish.md',review_finish_sha256=sha('/Users/yiwenchen/.codex/skills/hallmark/references/review-finish.md'),prior_read_reference=None,applied_for=[dict(principle='Fixed-input independent critique;read actual material rather than intended output',where='review.md:精确输入、实际执行与P13-R1;独立解析stdout/VCD而非依赖producer摘要'),dict(principle='Rank located material defects and propose minimal revision',where='review.md:P13-R1及额度下界;区分过去执行合规与未来完整资格阻塞'),dict(principle='Preserve what must not be diluted;do not invent a pass',where='review.md:下一路径与保留限制;不补X、不跳首行、不退款或刷新额度')],workflow_executed=False,scripts_executed=False,not_applicable_reason='无网页/UI设计任务，未运行截图/build/sloplint/Together；Hallmark不决定RTL/调度/资源正确性。',technical_review_methods=['733/48/3077+R03旧包及3历史叶子的SHA/Git/index只读核验','13实际收据与账本/plan/日志逐项比对','独立简短VCD/OBS解析与原标签比较','纯整数预算下界计算；未运行生产parser、测试或任何工具'],limits=['SHA自洽不证明用户授权真实性或完整子进程生命周期。','技术结论来自源码、真实保存输出和账本，不来自网页skill。'])
write(OWN/'hallmark-usage.json',hallmark)

native_model=snap/'test2/results/g1-qualification-v3/build/QC00/model.smt2'
def dep(rel):return dict(path=rel,sha256=sha(snap/rel))
qc00_reuse=[dep('test2/g1_v3/sources/common.sv'),dep('test2/g1_v3/sources/QC00_formal.sv'),dep('test2/g1_v3/inputs/stimulus.json'),dep('test2/g1_v3/inputs/controls.json'),dep('test2/g1_v3/job-plan.json'),dict(path='test2/results/g1-qualification-v3/build/QC00/model.smt2',sha256=sha(native_model))]
extra_physical=16*2-resources['remaining']['physical']
assert extra_physical==1
feasibility=dict(scope='READ_ONLY_LOWER_BOUND_NOT_AUTHORIZATION_OR_EXECUTED_PLAN',full_profile=dict(controls=16,physical_simulators_per_control=2,old_qualified_physical_runs=0,new_physical_runs_needed_at_least=32,current_physical_remaining=31,minimum_extra_physical_runs=1,minimum_cumulative_physical_cap=33,new_physical_cycles_at_four_per_run=128,cumulative_physical_cycles=132,conditional_new_native_if_reuse_QC00=30,cumulative_native=32,conditional_new_compiles=17,conditional_compile_reason='15 remaining formal builds+2changed shared physical builds',conditional_cumulative_compiles=20,additional_setup_if_exact_saved_versions_and_pins_reused=0,setup_remaining=0,cumulative_wall_cap_unchanged=1200,example_prior_total_conservative_charge_seconds=math.ceil(resources['cumulative_charged_checkpoint_seconds']),example_remaining_wall_seconds=1200-math.ceil(resources['cumulative_charged_checkpoint_seconds']),example_charge_not_a_fresh_measured_spend=True),partial_path=dict(available_without_increasing_original_counts=True,condition='新显式受限登记/累计ledger/gate，最多31新physical；保留至少1缺失合法dual-control结果及总体NOT_QUALIFIED，不放宽首行/X/双sim规则。闭合池不能直接resume。',existing_result_only='可只接受E02失败记录与QC00 native局部结果并停止，不需任何新执行。'),QC00_native_reuse=dict(possible_only_conditionally=True,already_supported_automatically=False,current_runner_limitation='R03固定job-plan/Allocation祖先为E01，attempt.lock和pool已闭合；没有REUSED job语义/跳过已完成QC00的登记。不得改旧receipt/清零/直接重开。',frozen_dependencies=qc00_reuse,requirements=['只改physical_tb，不改common.sv/QC00_formal/native stimulus/profile/assumptions/width/reset/selected pre/depth8/solver及frontend转换。若触及common或native依赖，必须重新评估复用。','绑定旧编译argv/flags、SMT内容、tool pin、stdout/stderr/receipt、BMC PASS与cover step2结果、P12/E02 identity和原累计成本。','新manifest显式标记2项native结果REUSED_FROM_E02/非新执行，保留原费用/时间/用量，并将QC00旧不合格physical永远保留为拒绝。','新版本需独立检查新physical0..3已知输入/复位/时钟/选定pre映射符合原公开标签；不把native PASS当作dual-physical已通过。','继承E01和E02两闭合池的累计计数/保守时间，显式分配余量并独立预检；旧setup版本只标复用，make仍NOT_REPROBED。']),if_reuse_disallowed=dict(new_native_full_profile=32,cumulative_native=34,additional_native_cap_at_least=2,physical_extra_cap_still=1),authority=dict(retry_permission='同任务合理retry本身无需重复确认；当前review不触发任何执行。',new_budget_decision='完整16xdual至少需明确physical累计32→33的数值修订；不能由reasonable-retry推断增帽。无增帽则仅部分路径。',new_OS_permissions='未发现新增ps/escalation/API/key需要；正常owned-group保护权限未来若失败仍halt，不能预先保证。',setup_and_time='0新setup的完整下界仅在显式复用现有版本/pin且无额外真实验证运行时成立。若需新query/额外诊断sim，也应单独计入，不能许诺无条件仅+1足够。'))
write(OWN/'budget-feasibility.json',feasibility)

finding=dict(id='P13-R1',severity='P2',material=True,blocking=True,blocking_scope='完整G1资格/未修版本重跑；不否定E02失败记录完整性或过去资源合规',path='test2/g1_v3/sources/physical_tb.sv',lines=[4,19,20,21,24],related_path='test2/g1_v3/sources/common.sv',related_lines=[3,5,6,7,8,9],evidence_sha256={'physical_tb':sha(code/'sources/physical_tb.sv'),'common':sha(code/'sources/common.sv'),'physical_stdout':sha(snap/'test2/results/g1-qualification-v3/jobs/QC00-icarus/stdout.log'),'physical_VCD':sha(snap/'test2/results/g1-qualification-v3/jobs/QC00-icarus/trace.vcd'),'labels':sha(code/'inputs/controls.json')},expected='cycle0 pre/post: a=b=0000,rst=1,en=valid=0,active=0,ok=1',actual='cycle0 tick1000/3000: a/b=xxxx,rst/en/valid/active/ok=x;cycle1–3 known。14field mismatches,8raw rows,0accepted。',direct_observation='独立VCD与stdout8行全部一致；step在0保持000，至tick4000才变001；stimulus输入直到4000才已知。4posedge在2000/6000/10000/14000。',source_based_cause='step declaration0和首轮再赋0未建立显式初次变化，stimulus采用always@*。若该块在首观测前有效求值，常量默认/step0分支应产生已知输入；保存轨迹显示未建立这些值。与time-zero事件激活缺口一致。',cause_limit='未读取模拟器事件队列，未编译/执行修订，因此不宣称已实验证明内部调度根因、Icarus缺陷或任一具体修复有效。',impact='物理输入与冻结已知输入合同不同；native已知二态控制结果不能与此首拍X轨迹组成合格双sim比较。',minimal_revision='另建版本，保证首个观察/时钟前组合刺激被显式初始化并稳定；尽量仅修TB启动机制，保留4cycles/原输入/首行/时钟/phase和原标签。不改旧结果，不X→0，不跳首拍，不加额外DUT时钟来取巧。',acceptance_condition='新独立预检+可计费执行中，两sim都保存并验证cycle0 pre/post已知预期输入和全部0..3行/相位/跨度/4posedge；未知控制仍未知。修复之前无完整G1PASS；所有新尝试受显式累计资源上限约束。')
max_by_kind={kind:max(r['elapsed_seconds'] for r in analysis['receipts'] if r['kind']==kind) for kind in ['setup','compile','native','physical']}
review=dict(phase='P13_G1_R03_EXECUTION_POST_REVIEW',status='CHANGES_REQUIRED',evidence_integrity='PASS_WITH_LIMITS',execution_resource_compliance='PASS_WITH_LIMITS',public_qualification='BLOCKED_NOT_QUALIFIED',actual_HEAD=integrity['actual_HEAD'],observed_at_utc=datetime.now(timezone.utc).isoformat(),input_identity={k:packet[k] for k in ['producer_phase_sha256','producer_manifest_sha256','registration_sha256','source_manifest_sha256','R03_manifest_sha256','P12_review_sha256','execution_receipt_sha256','continuation_decision_sha256','original_grant_sha256','predecessor_pool_sha256','current_pool_sha256']},phase_packet_sha256=sha(OWN/'phase-packet.json'),findings=[finding],integrity=dict(sealed_members=733,source_bindings=48,E02_preentry_protected_files=3077,R03_frozen_members=649,critical_old_score_checker_leaves=3,current_vs_snapshot_mismatches=0,index_sha256=integrity['index_sha256'],index_unchanged=True,current_still_matches=True),results=dict(total_registered_jobs=89,root_returned0=13,remaining_NOT_RUN=76,setup=7,logical_compilation_roots=3,native_BMC=1,activation_cover=1,physical_runs=1,physical_cycles=4,physical_raw_rows=8,physical_accepted_rows=0,QC00_native_BMC='PASS_DEPTH8',QC00_activation_cover='REACHED_STEP2',QC00_physical='REJECTED_CYCLE0_EXPECTATION_MISMATCH',QC00_verilator='NOT_RUN',fully_qualified_controls=0,other_controls_NOT_RUN=15,root_process_error_or_timeout=0,parser_error='PHYSICAL_EXPECTED_MISMATCH:a',runner_exit_code=1,memory_bytes=None,memory_knownness='NOT_MEASURED'),resources=dict(resources,max_observed_root_elapsed_by_kind_seconds=max_by_kind,all_observed_root_elapsed_below_individual_cap=True,job_timeout_caps=dict(setup=2,compile=20,native=10,physical=2),native_depth=8,current_window_cap=1198,original_cumulative_wall_cap=1200,all_recorded_counters_within_caps=True),process_evidence=dict(mode='owned_process_group_only',saved_root_receipts=13,optional_inventory_attempts=0,inventory_complete=False,all_root_exit0_known_from_cleanup_wait=True,all_owned_group_probes='ABSENT_AT_OWNED_PROBE_NOT_A_CENSUS',required_protection_errors=0,timeout_roots=0,recorded_SIGKILL_attempts=0,deadlines_bound_to_original_monotonic_origin=True,complete_child_lifecycle_proven=False,total_internal_OS_child_count=None,ps_real_call_in_saved_registered_path=0,claim_scope='精确P12 source+13实际receipt一致；无外部ps记录，不扩为整个宿主无其他进程或完全子树普查。'),budget_feasibility='budget-feasibility.json',minimum_full_profile_extra_physical_runs=1,full_profile_under_current_remaining_caps_possible=False,conditional_native_reuse='Requires explicit new registration/dependency/reuse provenance;not automatic',Hallmark='hallmark-usage.json',commands=[dict(command='Bounded sed/nl/rg and Python JSON/SHA/log reads',exit_code=0),dict(command='PYTHONDONTWRITEBYTECODE=1 python3 docs/audits/agent_bridge_2026-11-06/P13_g1_retry_execution/inspect_saved_e02.py',exit_code=0,scope='saved evidence parsing only,not a test suite/native run'),dict(command='Python3 critical historical leaf hashes and integer budget lower bound',exit_code=0),dict(command='PYTHONDONTWRITEBYTECODE=1 python3 docs/audits/agent_bridge_2026-11-06/P13_g1_retry_execution/finalize_p13.py',exit_code=0,scope='final rehash/index/report checks')],reviewer_harness_errors=[],reviewer_actual_new_tools=dict(version_queries=0,compile=0,BMC_cover=0,physical_runs=0,tests_mocks=0,project_parser_replay=0,ps_signal_process_probes=0,API_network_keys=0),elapsed=dict(full_turn_seconds=None,knownness='NOT_INSTRUMENTED_NOT_ZERO',partial_saved_analysis_to_report_seconds=time.time()-(OWN/'input-verification.json').stat().st_mtime,controlled_G1_execution_seconds=0),limits=['记录完整性通过不等于G1通过；P12仅预检，E02在首个physical解析时停止。','native QC00仅固定模型depth8/activation reachability；没有128/无界/真实DUT/Claude oracle或B/C优劣结论。','QC07/15空泛、QC12/13四态限制、QC14finalpost transport仅预登记边界，其本次实际任务均NOT_RUN。','无全子进程生命周期/脱离PGID后代/OS硬实时/未测内存证明；13根作业不是13个总OS进程。','工具smtbmc仅help，版本UNKNOWN；make未新探；所有实际版本文字来自保存7setup日志，无本轮新query。','本次单项和累计记录未超限；微秒级不同monotonic checkpoint不强行改成同一数值。','旧E01/P11、P12a偏移/P12-N1披露、P04证据订正、P05/P06限定范围、P05-N1、F1/H1/H2/L1、74未复现/selected-sample、billing UNKNOWN、R0/R1/R2planned保持。','不修改旧pool/lock/source/shared/docs/results/index，不发消息，不新agent/chat；本轮不修代码或开始下一执行。'],evidence_manifest='evidence-manifest.json',hash_cycle_policy='evidence manifest hashes final review and all reviewer files except itself;review stores path only')
write(OWN/'review.json',review)

md='''# P13 — G1 R03 E02 执行后独立复核

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
'''
with (OWN/'review.md').open('x') as f:f.write(md)
write(OWN/'final-validation.json',dict(status='PASS',evidence_integrity=review['evidence_integrity'],resource_compliance=review['execution_resource_compliance'],qualification=review['public_qualification'],overall=review['status'],binding_recheck_count=len(integrity['bindings']),index_unchanged=True,new_execution_calls=0))
files={str(p.relative_to(OWN)):sha(p) for p in OWN.rglob('*') if p.is_file() and p!=OWN/'evidence-manifest.json'}
write(OWN/'evidence-manifest.json',dict(files=files,file_count=len(files),excluded=['evidence-manifest.json'],external_bindings='input-verification.json',scope='Only reviewer-owned analysis/report/inputs;no experiment'))
assert all(sha(OWN/rel)==expected for rel,expected in files.items())
print(json.dumps(dict(overall=review['status'],evidence=review['evidence_integrity'],resources=review['execution_resource_compliance'],qualification=review['public_qualification'],minimum_extra_physical=1,review_sha256=sha(OWN/'review.json'),evidence_manifest_sha256=sha(OWN/'evidence-manifest.json')),ensure_ascii=False))
