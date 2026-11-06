from datetime import datetime,timezone
import hashlib,json,subprocess
from pathlib import Path
OWN=Path(__file__).resolve().parent;ROOT=OWN.parents[3]
AUDIT=ROOT/'docs/audits/producer_test2_g1_E03_2026-11-06';SNAP=AUDIT/'snapshot'
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,d):
    with Path(p).open('x') as f:json.dump(d,f,ensure_ascii=False,indent=2)
a=read(OWN/'saved-analysis.json');phase=read(AUDIT/'phase.json');reg=read(SNAP/'test2/configs/g1_qualification_registration_v4.json');code=SNAP/'test2/g1_v4';result=SNAP/reg['result_root']
assert sha(AUDIT/'phase.json')==a['producer_phase_sha256'] and sha(AUDIT/'snapshot-manifest.json')==a['producer_manifest_sha256']
for rel,h in read(AUDIT/'snapshot-manifest.json')['files'].items():
    assert sha(AUDIT/rel)==h
    if rel.startswith('snapshot/'):assert sha(ROOT/rel[9:])==h
index=subprocess.check_output(['git','--no-optional-locks','ls-files','--stage','-z'],cwd=ROOT);assert hashlib.sha256(index).hexdigest()==a['index_entries_sha256']
finding=dict(id='P15-R1',severity='P2',material=True,blocking=True,path='test2/g1_v4/runner.py',lines=[63,64,65,66,67,137,138,139],source_sha256=sha(code/'runner.py'),raw_log='test2/results/g1-qualification-v4/jobs/QC01-cover/stdout.log',raw_log_sha256='24b2e9a6b0def95bc74a517f150ab88ded18b7d736ddbc4baea21f9146cb2256',expected='Reachability and assertion outcome are independent fields;QC01 negative control can reach cover while its intentionally false assertion fails.',actual='Raw reached step2 +assert failed step2+Status FAILED/exit1,but classify_native converts every cover FAILED to NOT_REACHED and runner halts on expected PASS.',cause='Pinned yosys-smtbmc covermode prints reached cover,then checks assertions along that trace;found_failed_assert causes early break before assigning PASSED. The coarse caller classification incorrectly equates tool FAILED with target unreachability.',tool_source_sha256=a['pinned_tool_source_sha256'],tool_source_lines=[1869,1884,1950,1955,1956,1961,1968,1971,2184,2185],impact='Incorrect scientific reachability label plus an execution blocker;not hidden budget overrun or false overall G1 acceptance. Negative-control raw failure must not be erased.',minimal_fix='New parser/report version preserves raw exit/status, separately records cover REACHED(step2),assertion FAILED(step2),mode/property identity and explicit unknown/error. New registration clarifies abstract activation expectation from public source without changing hardware/flags or overwriting old expectations/evidence.',acceptance='Exact saved QC01 log yields raw FAILED/exit1,cover REACHED/step2,assertion FAILED/step2;never global PASS nor NOT_REACHED. Completed unreached with explicit evidence may be NOT_REACHED;missing/truncated/error/timeout stays UNKNOWN/ERROR. Known negative QC01 is judged by separately declared activation/assertion expectations,then still needs remaining physical pair and full16QC evidence. Reuse exact hashes,retain spent counters and original halt.')
hardware_reuse=dict(already_reused_E02=['compile-QC00','QC00-bmc','QC00-cover'],E03_reusable_after_explicit_binding=['compile-icarus-shared','compile-verilator-shared','QC00-icarus','QC00-verilator','compile-QC01','QC01-bmc','QC01-cover'],QC01_cover_interpretation=dict(raw_tool_status='FAILED',process_exit_code=1,cover_reachability='REACHED',cover_steps=[2],assertion='FAILED',assertion_steps=[2],overall_control='PARTIAL_PENDING_PHYSICAL',old_runner_label='NOT_REACHED_RETAINED_AS_HISTORY'),requirements=['hardware/common/formal/physicalTB/input/labels/assumptions/depth8/frontend/solver/flags/tool pins unchanged;new source/manifest explicitly documents parser/report interpretation version','Bind complete original logs/receipts/VCD/SMT and dependency/build/executable SHAs;shared executable reuse must read old artifacts and write only new result paths,not mutate old pools/builds','Mark every reused job REUSED_FROM_E02 or REUSED_FROM_E03/new_execution=false,retain all original spent compilation/native/physical/time charges;old bad E02physical never becomes valid','QC00 original native PASS+cover andnew dualphysical support that limited known-input control only;QC01 rawcover FAILED does not become a clean native PASS','New continuation includes E01/E02/E03 closed pool identities and all cumulative use,exclusive new namespace/gate;existing R04 pool/lock cannot resume/reset','No new version queries;reuse version text/knownness with runtime filepins,smtbmc help-only/make unknowns retained'])
feasibility=dict(status='CONDITIONALLY_FEASIBLE_WITHIN_EXISTING_CAPS_NOT_AUTHORIZATION',remaining=a['remaining'],new_jobs_if_exact_reuse=dict(setup=0,compile=14,native=28,physical=30,physical_cycles=120),cumulative_after=dict(setup=8,compile=20,native=32,physical=33,physical_cycles=132),physical_breakdown='QC01 two physical +QC02..QC15 fourteen dual pairs=30;QC00 actual pair reused',native_breakdown='QC02..QC15 fourteen BMC+cover pairs=28;QC00 E02 andQC01 E03 preserved/reused',conservative_time_example=dict(prior_cumulative_actual_checkpoint_seconds=a['cumulative_actual_checkpoint'],prior_cumulative_charged_checkpoint_seconds=a['cumulative_charged_checkpoint'],new_prior_charge_seconds=15,new_attempt_max_seconds=1185,new_work_cutoff_seconds=1180,original_cumulative_cap_seconds=1200,note='Example to register;charge15 conservatively covers charged14.572948...;not measured spend or fresh1200s.'),if_reuse_not_possible=dict(rebuild_both_shared_physical_binaries=dict(new_compiles=16,cumulative_compiles=22,extra_count_quota_needed=0,time_and_failures_still_charge=True),lose_one_saved_native_job='Each otherwise unnecessary native reexecution adds1 above exact28 remaining;request explicit native cap+1 per lost reusable native result if full coverage still required.',lose_QC00_E02_native_pair=dict(extra_native_cap_needed=2,cumulative_native=34),lose_QC01_E03_native_pair=dict(extra_native_cap_needed=2,cumulative_native=34),lose_QC00_physical_pair=dict(extra_physical_cap_needed=2,cumulative_physical=35),require_new_setup_query='setup8 already exhausted;any new query requires explicit additional setup allocation rather than silent re-probe'),limits='Count feasibility is not a guarantee of outcome or OS timing. Any new failures remain charged. No automatic quota/refund/retry;no extra quota presently needed if all stated reuse conditions hold.')
write(OWN/'continuation-feasibility.json',dict(reuse=hardware_reuse,budget=feasibility))
hallmark=dict(considered=True,read_this_round=True,source='/Users/yiwenchen/.codex/skills/hallmark/SKILL.md',source_sha256=sha('/Users/yiwenchen/.codex/skills/hallmark/SKILL.md'),read_evidence=[dict(tool='skills__read',package='e0/hallmark',scope='SKILL fetched this round;output abbreviated,priorP14sameversionalsoavailable'),dict(tool='skills__read',package='e0/hallmark',resource='skill://codex-home-skills/Users/yiwenchen/.codex/skills/hallmark/references/review-finish.md',scope='full finish review read this round')],review_finish_sha256=sha('/Users/yiwenchen/.codex/skills/hallmark/references/review-finish.md'),prior_read_reference='P14 same-version actual read',applied_for=['固定材料与原始证据优先：区分raw FAILED、reachability、assertion及旧derived标签。','实质排序/定位/最小修订：P15-R1分类问题，保留QC00真实有限成功，不重开无关工程。','不稀释边界：继续方案仅复用确切证据且成本不退款，不把mock/模型一致性当RTL证明。'],workflow_executed=False,scripts_executed=False,not_applicable_reason='网页/UI流程不适用；RTL/tool/ledger结论独立来自保存日志/VCD、源码和只读预算计算。')
write(OWN/'hallmark-usage.json',hallmark)
review=dict(phase='P15_G1_R04_E03_EXECUTION_REVIEW',status='CHANGES_REQUIRED',evidence_integrity='PASS_WITH_LIMITS',execution_resource_compliance='PASS_WITH_LIMITS',qualification='BLOCKED_NOT_QUALIFIED',observed_at_utc=datetime.now(timezone.utc).isoformat(),actual_HEAD=a['actual_HEAD'],input_identity=dict(producer_phase_sha256=a['producer_phase_sha256'],producer_manifest_sha256=a['producer_manifest_sha256'],registration_sha256=phase['registration_sha256'],source_manifest_sha256=sha(SNAP/reg['source_manifest']),R04_preparation_manifest_sha256=phase['R04_preparation_manifest_sha256'],P14_review_sha256=phase['P14_review_sha256'],execution_receipt_sha256=phase['EXECUTE_sha256'],final_pool_sha256=phase['final_pool_sha256'],continuation_decision_sha256=reg['continuation_decision_sha256'],budget_amendment_sha256=reg['budget_amendment_sha256']),seal_anchor_origin=a['seal_anchor_origin'],integrity=dict(sealed_members=a['sealed_members'],source_bindings=a['source_bindings'],protected_files=a['protected_files'],current_still_matches=True,index_unchanged=True),findings=[finding],QC00_result=dict(finite_control='DUAL_SIM_MATCHED_WITH_REUSED_NATIVE',startup_fix='SUPPORTED_IN_ACTUAL_QC00_RUNS_ONLY',rows_each_sim=8,known_first_row=True,phase_and_VCD_binding=True,pre_ps=[1000,5000,9000,13000],posedge_ps=[2000,6000,10000,14000],post_ps=[3000,7000,11000,15000],extra_edge=False,qualifies_other15=False,proves128_or_general_correctness=False),QC01_result=dict(BMC=a['native_QC01']['bmc'],cover=a['native_QC01']['cover'],physical='NOT_RUN',source_negative_control='common.sv ID1 deliberately ok=0;predeclared BMC FAIL,activation expected reachable',unexpected_real_RTL_defect_confirmed=False,uncertainty='NoQC01physical orQC02..15 actual result;cannot rule out future source/tool/phase problems'),results=dict(new_returned_roots=7,raw_root_exit0=5,raw_root_exit1=2,root_timeouts=0,mandatory_protection_errors=0,remaining_original_jobs_NOT_RUN=72,QC00_native_compile_reused_E02=True,new_native_trials=2,new_physical_runs=2,new_physical_cycles=8,fully_observed_public_controls=['QC00'],partial=['QC01'],not_run=['QC%02d'%n for n in range(2,16)]),resources=dict(attempt=a['attempt'],cumulative=a['cumulative'],remaining=a['remaining'],current_recorded_window_seconds=a['current_window_seconds'],cumulative_actual_checkpoint_seconds=a['cumulative_actual_checkpoint'],cumulative_charged_checkpoint_seconds=a['cumulative_charged_checkpoint'],all_observed_counters_and_single_job_deadlines_within_caps=True,setup_new=0),continuation='continuation-feasibility.json',all_hardware_jobs_may_continue_without_count_increase_if_exact_reuse=True,execution_authorized_by_this_review=False,actual_new_reviewer_jobs=dict(compile=0,native=0,physical=0,ps_signal_version_probe=0,tests_mocks=0,model_API_key_network_install=0,commit_push=0),hallmark_usage='hallmark-usage.json',commands=[dict(command='Bounded logs/RTL reads and rg/sed of pinned yosys-smtbmc Python source (not executed)',exit_code=0),dict(command='PYTHONDONTWRITEBYTECODE=1 python3 .../P15_g1_R04_execution/inspect_saved.py',exit_code=0,scope='onlysaved-byteparsing'),dict(command='Python integer budget calculation',exit_code=0),dict(command='PYTHONDONTWRITEBYTECODE=1 python3 .../P15_g1_R04_execution/finalize_p15.py',exit_code=0)],reviewer_harness_incidents=[],limits=['E03初始没有seal时仅诊断user绑定raw；phase/manifest出现后固定SHA并再次比对，未混用漂移版本。','固定模型公开负控制分类修正不代表真实DUT、monitor、128cycle/unbounded或原74未复现已解决。','R04真实QC00支持time-zero启动修复在该已测路径的效果；不据此证明所有16QC或四态转换正确。','七根job不是全部OS进程；inventory仍incomplete，未观测mandatory错误不证明完整子树或OS硬实时。','所有旧失败/unknown/timeout/score/P04/P05/P06/P05-N1/F1/H1/H2/L1/billing/selectedsample限制保留。','新metadata/解析版本必须单独封存/登记并严格继承成本，不原地更改旧报告、旧pool或QC01 raw status。','G1未通过；raw/B-C/跨IP和模型API保持暂停。'],evidence='evidence.json')
write(OWN/'review.json',review)
md='''# P15 — R04 E03 实际执行保存证据复核

**整体CHANGES_REQUIRED；证据完整性/执行资源记录PASS_WITH_LIMITS；G1资格BLOCKED / NOT_QUALIFIED。**

本轮确认一个最小分类语义缺陷；没有把native FAILED变成整体PASS，也未发现本批新的非预期RTL缺陷证据。QC01是原登记已知负控制；其物理pair及其余14控制仍未运行，不能排除后续问题。

## 精确封存与已发生执行

开始时只诊断已关闭raw pool；E03 phase/manifest出现后固定并核验：phase **c7b99fd6a11a47a4204b2fb22c0f0ebb57c81bb4ca1c1ba864b57977f2601325**，manifest **9511046040fb38358f1fc70bfe88742a45a5c8957a427744675c929ae1df4325**。571成员/96source绑定/4485保护历史文件一致，current仍匹配；HEAD实际2de33e981d2fffc9739d2ca049fbae1774de1aad，index未改。

最终pool SHA2364e80999aaea35eb3e5da06e31d48331ee6be6b061c09bb3f92738bca8d1b8；EXECUTE fadb3e7fd5534d63309b42c7492a8b57915025010f4832c4ca9c27a0ddcc2e7e；P14/R04源与登记精确相符。pool halted/completed，entry exit1，不可reset/resume。

原79个新job只运行7个：3compile、2native、2physical；5个root exit0、2个native exit1，均进程正常返回而非timeout。其余72 NOT_RUN。原QC00 compile1/native2是E02复用，不计新执行。7份实际receipt/日志/plan/ledger逐一一致，原绝对deadline与单项20/10/2秒帽保持，未见mandatory进程保护错误或ps调用；inventory仍不完整，不提供全子树或OS硬实时证明。

## QC00：首拍修复获得有限实际支持

两sim各8行均与原冻结表及各自VCD逐字段/phase/step一致：首拍a=b=0000,rst1,en0,valid0,active0,ok1；后续四周期/4posedge也一致。pre1000/5000/9000/13000，edge2000/6000/10000/14000，post3000/7000/11000/15000，结束16000ps。没有跳首行/X补0/额外上升沿。

这支持**修复在实际QC00双sim/固定输入路径有效**，加上严格绑定的E02 native前缀，形成一个有限公开控制结果；不证明其他15QC、general correctness、128周期或原74项未复现根因。

## P15-R1 — cover FAILED误分NOT_REACHED，P2/material=true

位置`test2/g1_v4/runner.py:63–67`（SHA46c29b45fd9e4afa9a342bd4ec4c99219f08596cd38826d8f06b24d734a71e1f），后续137–139触发冻结预期冲突。

QC01-cover stdout SHA24b2e9a6b0def95bc74a517f150ab88ded18b7d736ddbc4baea21f9146cb2256明确同时包含：

| 层次 | 保存事实 |
|---|---|
| process exit |1|
| raw tool status |FAILED|
| activation cover |Reached step2|
| assertion |failed step2|
| 旧derived标签 |NOT_REACHED（错误，原件保留）|

固定工具源码yosys-smtbmc（SHA0192f63913bdff347912602315504d5a6ed9e3ff8fbf0dbcdc7c33e5b66681d9）covermode在1950行报告reach，1955–1968检查trace断言并因失败跳出，然后未走到设置PASSED的分支；末尾按FAILED退出1。仅**静态读源码**，没有执行工具。独立解析native BMC/cover VCD均见sampled_cycle1、active1/ok0/q0，与原public QC01负控制一致，两VCD字节也相同，不能当两种独立缺陷。

因此是调用者taxonomy过粗：tool FAILED并不必然表示cover未达。QC01 `common.sv:36`刻意ok=0，formal源16/17行同时assert与cover，原手算期望已经是BMC FAIL且activation可达；本批不支持把它重新描述为未知真实DUT bug。

**最小修订/验收：**另建解析与报告版本，分列raw exit/status、registered cover identity/reached_steps、assertion status/steps、unknown/error。精确旧log必须得FAILED/1 +REACHED2 +assertionFAILED2，不变成overall PASS或NOT_REACHED。完整明确未达与缺日志/截断/错误/timeout要分开，后者保留UNKNOWN/ERROR。新登记明确公开负控制的activation与assertion期望：原source可直接解释其差别，不是仅把旧PASS改成NOT_REACHED迎合结果。旧labels/报告/错误原件保持历史，新增解释版本/表与独立检查；hardware/flags无需为此修改。

## 同上限内的最小继续方案

当前累计setup8/compile6/native4/physical3/cycles12；本次setup0/compile3/native2/physical2/cycles8。actual累计checkpoint11.770645541138947s、charged14.572948167100549s，本窗口6.572940208s；不退款或强行改成相同取样时刻。剩setup0/compile26/native28/physical30/cycles1012。

只改解析/报告时，可在新显式登记中复用：E02 QC00 native+编译；E03两个shared physical build、QC00双sim、QC01编译/SMT及BMC/cover原始证据。覆盖源码/输入/假设/depth8/flags/tool pin及二进制/SMT/日志/receipt/VCD的精确hash与依赖；新report标REUSED_FROM_E02/E03、new_execution=false，所有原费用仍继承。不能复用最初E02坏physical，也不能把QC01-cover的raw FAILED改成PASS。

| 后续新增 | 数量 | 完成后累计 |
|---|---:|---:|
| setup |0|8|
| compile（QC02–15）|14|20|
| native（QC02–15 BMC+cover）|28|32|
| physical（QC01两次+QC02–15双sim）|30|33|
| physical cycles |120|132|

**上述精确复用成立时，不需新增计数quota。** 可在后续continuation用累计保守charge15s覆盖既有charged14.572948...，分配至多1185s（work1180），仍累计1200s；这是待新登记的示例，不是本review的执行授权。数量可行不保证实际结果/OS时间。

如果shared physical binaries不能复用，重建2项则新增compile16/累计22，仍≤32，无需编译帽增加但时间照计。若必须重跑本可复用的native，每丢失1项复用就比剩28多1项，需明确相应native帽修订；丢QC00或QC01一对需+2（累计34），全丢四项需+4。若QC00两个physical不能复用，完整物理需累计35，需帽+2。setup无余量，任何新query须单独分配，不能自动发生。

当前R04固定gate/Allocation祖先及closed pool不能直接续跑；新版本仅为此解析修订和最小明确reuse清单，继承E01/E02/E03所有累计用量与hash，独立预检后协调EXECUTE。不要重跑已完成hardware job来修一个报告标签，不扩大为通用框架或新研究。

## 范围与交付

逐证据/资源/可复用条件见saved-analysis.json、continuation-feasibility.json、review.json及evidence.json。QC01 physical和QC02–15仍NOT_RUN；QC07/15空泛、QC12/13四态限制、QC14运输保持。旧unknown/timeout/score/P04/P05/P06/P05-N1/F1/H1/H2/L1、selected样本、billing和128限制不关闭。

Hallmark本轮实际获取SKILL并读review-finish，同版SHA/read evidence在hallmark-usage.json；实际用于固定材料独立critique、raw/derived分层、实质问题定位与最小继续范围。网页workflow/scripts=false；技术判断来自RTL/native/VCD/资源证据。

有界只读命令、inspect_saved.py和finalize_p15.py exit0；无reviewer harness错误、无旧套件或新mock。0实际compile/sim/native/version/ps/signal/API/key/network/install/commit/push，不改producer/E03/旧证据/shared/index，不发producer消息。G1尚未通过，raw/B-C/跨IP不启动。
'''
with (OWN/'review.md').open('x') as f:f.write(md)
paths=[OWN/'review.json',OWN/'review.md',OWN/'hallmark-usage.json',OWN/'saved-analysis.json',OWN/'continuation-feasibility.json',OWN/'pinned-smtbmc-cover-excerpt.txt',OWN/'inspect_saved.py',OWN/'finalize_p15.py']
files={str(p.relative_to(OWN)):sha(p) for p in paths}
write(OWN/'evidence.json',dict(files=files,original_dependencies=dict(producer_phase=a['producer_phase_sha256'],producer_manifest=a['producer_manifest_sha256'],pool=phase['final_pool_sha256'],EXECUTE=phase['EXECUTE_sha256'],P14=phase['P14_review_sha256']),hash_cycle_policy='Evidence hashes final review;review references path only'))
assert all(sha(OWN/r)==h for r,h in files.items())
print(json.dumps(dict(status=review['status'],qualification=review['qualification'],QC00='FINITE_DUAL_SIM_MATCH',issue='P15-R1_COVER_TAXONOMY',existing_caps_feasible_with_exact_reuse=True,review_sha256=sha(OWN/'review.json'),evidence_sha256=sha(OWN/'evidence.json')),ensure_ascii=False))
