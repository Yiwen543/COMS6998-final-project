import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time

OWN=Path(__file__).resolve().parent
ROOT=OWN.parents[3]
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,value):
    with Path(p).open('x') as f:json.dump(value,f,ensure_ascii=False,indent=2)

packet=read(OWN/'phase-packet.json')
before=read(OWN/'input-verification-before-corrected.json')
after=read(OWN/'input-verification-after.json')
assert not before['mismatches'] and not after['mismatches']
assert before['index_sha256']==after['index_sha256']
copy_inputs=read(OWN/'review-copy-inputs.json')
assert all(sha(OWN/'review-copy'/p)==v for p,v in copy_inputs.items())
fresh=read(OWN/'fresh-suites.json')
assert [(r['tests'],r['failures'],r['errors'],r['exit_code']) for r in fresh]==[(28,0,0,0),(14,0,0,0)]
probes=read(OWN/'independent-probes/summary.json')
corrected=read(OWN/'finalization-probes-v2/summary.json')
valid_probes=[r for r in probes['rows'] if not r['name'].startswith('runner_')]
assert len(valid_probes)==29 and all(r['passed'] for r in valid_probes)
assert corrected['probes']==corrected['passed']==2
assert all(sha(OWN/'independent-probes'/r['name']/'fixture.json')==r['fixture_sha256'] and sha(OWN/'independent-probes'/r['name']/'result.json')==r['result_sha256'] for r in probes['rows'])
assert all(sha(OWN/'finalization-probes-v2'/r['name']/'fixture.json')==r['fixture_sha256'] and sha(OWN/'finalization-probes-v2'/r['name']/'result.json')==r['result_sha256'] for r in corrected['rows'])
code=OWN/'review-copy/test2/g1_v3'
tree=ast.parse((code/'runtime.py').read_text())
subprocess_calls=[(n.func.attr,n.lineno) for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='subprocess']
assert [name for name,line in subprocess_calls]==['Popen']

hallmark=dict(considered=True,read_this_round=True,source='/Users/yiwenchen/.codex/skills/hallmark/SKILL.md',source_sha256=sha('/Users/yiwenchen/.codex/skills/hallmark/SKILL.md'),version='2.0.0',read_evidence=[dict(tool='skills__read',package='e0/hallmark',contents_read_this_round=True),dict(tool='exec_command',command='cat /Users/yiwenchen/.codex/skills/hallmark/references/review-finish.md',exit_code=0)],review_finish_source='/Users/yiwenchen/.codex/skills/hallmark/references/review-finish.md',review_finish_sha256=sha('/Users/yiwenchen/.codex/skills/hallmark/references/review-finish.md'),prior_read_reference=None,applied_for=[dict(principle='Fixed-input independent critique;read actual material rather than intent',application='review.md:精确输入与实际差异;验证649/48/2382绑定及直接源码/独立探针'),dict(principle='Rank and locate real defects;do not report taste as a finding',application='review.md:P12-N1仅非阻塞scope说明;无新实质阻塞，不重开历史问题'),dict(principle='Minimal correction and preserve what must not be diluted',application='review.md:后续路由;保留旧池、累计额度、unknown及全部失败；无实施/实验扩展')],workflow_executed=False,scripts_executed=False,not_applicable_reason='网页/UI完整设计及截图/sloplint/Together流程不适用于RTL/进程/资源预检。这里只借用上述通用审阅原则。',technical_review_methods=['精确SHA与Git/index只读核验','AST/源码控制流与差异审阅','新模块42项纯mock新鲜运行','29个独立运行/门禁/祖先探针+2个修正收尾对照'],limits=['Hallmark不决定RTL正确性、OS权限或资源逻辑结论。','未执行网页/UI审计，没有Hallmark脚本、Together、API或密钥操作。'])
write(OWN/'hallmark-usage.json',hallmark)

commands=[
 dict(command='git rev-parse HEAD / git --no-optional-locks ls-files --stage -z (read-only, digest only)',exit_code=0,note='Git temp-dir confstr warning retained;no index mutation'),
 dict(command='PYTHONDONTWRITEBYTECODE=1 python3 .../P12_g1_retry_preflight/verify_inputs.py before',exit_code=1,note='Reviewer path-layout error;full result retained in input-verification-before.json,not a producer mismatch'),
 dict(command='PYTHONDONTWRITEBYTECODE=1 python3 .../P12_g1_retry_preflight/verify_inputs.py before-corrected',exit_code=0),
 dict(command='PYTHONDONTWRITEBYTECODE=1 python3 .../P12_g1_retry_preflight/prepare_review_copy.py',exit_code=0,files=51),
 dict(command='PYTHONDONTWRITEBYTECODE=1 python3 .../P12_g1_retry_preflight/run_fresh_suites.py',exit_code=0,internal_suite_exits=[0,0],tests=42),
 dict(command='PYTHONDONTWRITEBYTECODE=1 python3 .../P12_g1_retry_preflight/independent_probes.py',exit_code=1,probes=31,note='29 non-finalization probes valid;two initial finalization cases invalid due missing labels;one misleading crossing PASS excluded'),
 dict(command='PYTHONDONTWRITEBYTECODE=1 python3 .../P12_g1_retry_preflight/finalization_probes_v2.py',exit_code=0,probes=2),
 dict(command='PYTHONDONTWRITEBYTECODE=1 python3 .../P12_g1_retry_preflight/verify_inputs.py after',exit_code=0),
 dict(command='PYTHONDONTWRITEBYTECODE=1 python3 .../P12_g1_retry_preflight/finalize_review.py',exit_code=0,note='Exit confirmed by caller;checks all exact saved fixture/outcome bytes and evidence manifest')]
incidents=[dict(id='P12-HARNESS-1',product_defect=False,evidence='input-verification-before.json',description='Review checker assumed every source binding lived under snapshot/. Producer checklist is at sealed package root;initial mismatch was review mapping error.',resolution='Special-case direct sealed metadata after verifying its SHA;before-corrected and after both0 mismatches. Failed first result retained.'),dict(id='P12-HARNESS-2',product_defect=False,evidence=['independent-probes/runner_normal_final_save/result.json','independent-probes/runner_final_save_crosses_cap/result.json'],description='Reviewer empty-plan runner harness omitted labels.json. Baseline failed before reaching intended path;crossing case also had that independent error and its apparent PASS is not accepted evidence.',resolution='No edits to those fixtures/results. New finalization_probes_v2.py saves all required synthetic files before validation. Normal exit0/nohalt;crossing exit1/durablehalt with specific FINAL_PERSISTENCE_EXCEEDED_CUMULATIVE_WALL_CAP and no execution_error.' )]
write(OWN/'commands-and-incidents.json',dict(commands=commands,reviewer_incidents=incidents,read_output_limits='Some initial batched source/doc outputs were truncated. Exact requested packet and core source were separately read;conclusions tied to frozen bytes and saved probes,not truncated summary alone.'))

source_hashes={p.name:sha(p) for p in code.glob('*.py')}
input_identity={key:packet[key] for key in ['producer_phase_sha256','producer_manifest_sha256','registration_sha256','source_manifest_sha256','continuation_decision_sha256','predecessor_pool_sha256']}
input_identity.update(phase_packet_sha256=sha(OWN/'phase-packet.json'),original_user_grant_sha256=allocation_sha if False else 'bf3da44d7cda9eadfabebf82b23271854465942a3814f36b90789f7e715575ab')
findings=[dict(id='P12-N1',severity='P3',material=False,blocking=False,path='docs/audits/producer_test2_g1_R03_2026-11-06/phase.json',json_key='actual_R03_resources.network / elapsed.full_turn_knownness',evidence=['docs/audits/agent_bridge_2026-11-06/P12a_coordination_check.json','docs/audits/producer_test2_g1_R03_2026-11-06/commands-and-checks.json'],evidence_sha256={'P12a':sha(ROOT/'docs/audits/agent_bridge_2026-11-06/P12a_coordination_check.json'),'phase':packet['producer_phase_sha256']},observation='R03字段network=0只能描述受控G1准备。P12a已经保存同turn历史PPT偏离、web读取及无关辅助记录写入。不得把整turn说成只有G1或完全无network。',impact='整轮来源叙述的scope需限制；没有证据表明G1工具执行/付费/封存PPT覆盖。不会改变精确runner、资源或语义输入。',minimal_revision='本review侧明确保留P12a事实；后续closure sidecar将0限定为controlled G1路径，保留whole-turn uninstrumented/unknown，不改冻结原件。',acceptance_condition='后续对外closure不声称整turn仅G1/无web，引用P12a；无须为此重跑/改功能/阻塞本轮执行预检。')]
limits=[
 '仅R03精确版本执行前、单个协调器路由的一次受限串行attempt预检；不是G1资格完成或OS生命周期证明。',
 '旧E01/P11原件保留，1 ERROR+89 NOT_RUN、16QC NOT_RUN、Yosys版本/rootexit UNKNOWN；P11历史CHANGES_REQUIRED不改写。',
 '原授权真实性来自用户/协调权限链。SHA自洽与fake gate不构成独立用户身份认证或服务来源证明。',
 'owned group不提供完整PID普查、detached/adversarial descendant containment或whole-host计费；inventory remains incomplete。',
 'fsync/调度/cleanup有阻塞和OS延迟；已观察越界必须失败，不声称硬实时。最终halt自身持久化也可能继续花时间。',
 'setup1/实际0.04572445806115866秒与保守charge2秒分别保留；新窗口至多1198秒，work1193秒，7setup。不得退还或每版本刷新32/32/32。',
 '18逻辑编译根作业包含子编译器日志和根/全局时间，不是18个OS进程；未检验真实工具ABI或子树行为。',
 '省略make版本查询仅节省setup；make版本本轮NOT_REPROBED，文件pin不等于新版本查询。',
 '固定父目录/固定namespace上独占open-x lock和pool支持此单协调串行路径的重复启动拒绝；非通用并发事务/任意多路径共享资源池。',
 '原24材料及observer/profile/labels/flags顺序未变，只复用P10/P10B有限数学/语义结论，无新RTL/native科学结果。',
 'QC07/15空泛、QC12/13四态不支持、QC14运输限制、selected sample/category、128completion/general correctness、74未复现、F1/H1/H2/L1、P04 mismatch、P05/P06 exact范围、P05-N1 backlog、billing UNKNOWN、R0/R1/R2 planned保持。',
 'P12a上下文偏移保留，不重新调查PPT；没有把当前turn的所有操作描述成纯G1。']
partial=time.time()-(OWN/'input-verification-before.json').stat().st_mtime
review=dict(phase='P12_G1_R03_CONTINUATION_PREFLIGHT',status='PASS_WITH_LIMITS',decision='PASS_WITH_LIMITS',observed_at_utc=datetime.now(timezone.utc).isoformat(),actual_HEAD=after['actual_HEAD'],input_identity=input_identity,execution_blockers=[],findings=findings,qualification_status='NOT_QUALIFIED_R03_NOT_RUN',may_route_exact_EXECUTE=True,autoexecution=False,authorization_scope='Same original G1 grant reasonable retry allocated by exact continuation decision;no new permissions or caps. Coordinator supplies subsequent exact EXECUTE receipt.',close_scope={'P11-R1':'CLOSED_FOR_R03_PREFLIGHT_ONLY:registered default path no inventory command;mandatory group/poll/wait/kill/deadline intact;real OS behavior unqualified','R03_TEST28_FINAL_PERSISTENCE_BOUNDARY':'CLOSED_FOR_OBSERVED_FAKE_BOUNDARY:durablehalt+runnerexit1 verified independently','P10-R1':'RETAINED_AND_REVALIDATED:slow save/mkdir/log/lastcheck zero mock dispatch;charged reservation and halt retained','P10-R2':'RETAINED_AND_REVALIDATED:fresh exact-version14 regressions include full16ns ACCEPT/truncated14ns span REJECT and unknown/signal controls','cumulative_lineage':'ACCEPTED_FOR_FIXED_SERIAL_R03:exact immutable E01/grant/P11/phase/decision preconditions;duplicate paths refuse','execution_gate':'ACCEPTED:full copied runner.review_gate baseline +7 independent negatives;P12/new registration/source/manifest/decision/oldpool required'},integrity={k:after[k] for k in ['actual_HEAD','sealed_members','source_bindings','protected_files','semantic_materials','observer_unchanged','job_order_normalized_equal','only_removed_job','index_sha256','real_paths_uncreated','mismatches']},source_sha256=source_hashes,static_registered_runtime_subprocess_calls=subprocess_calls,validation=dict(producer_saved_invocations=111,producer_saved_failures=1,producer_final_source_tests=42,producer_final_source_failures=0,producer_attempt2_raw_exit_knownness='UNKNOWN;summary/log show failure;not filled with inferred1',fresh_exact_source_tests=42,fresh_exact_source_failures=0,independent_probe_invocations=33,accepted_unique_independent_probes=31,accepted_nonfinalization_probes=29,corrected_finalization_probes=2,invalid_initial_finalization_probes=2,reviewer_harness_incidents=incidents,commands='commands-and-incidents.json',fresh_suites='fresh-suites.json',independent_results='independent-probes/summary.json',corrected_results='finalization-probes-v2/summary.json'),remaining_caps=dict(setup_jobs=7,compile_jobs=32,native_BMC_cover_jobs=32,native_depth=8,native_timeout_seconds=10,physical_runs=32,physical_timeout_seconds=2,cycles_per_run_max=32,physical_cycles_total_max=1024,compile_timeout_seconds=20,attempt_wall_seconds_max=1198,attempt_work_cutoff_seconds=1193,cumulative_original_wall_seconds=1200),forbidden_actuals=dict(G1_version_queries=0,G1_compilations=0,G1_native_BMC_cover=0,G1_simulations=0,G1_process_signal_inventory_probes=0,API_count_generation=0,network=0,key_reads=0,installation=0,old_experiment_reruns=0,producer_messages=0,new_agents_chats=0,index_mutations=0,source_shared_result_edits=0),hallmark_usage='hallmark-usage.json',review_elapsed=dict(full_turn_wall_seconds=None,full_turn_knownness='NOT_INSTRUMENTED_NOT_ZERO',instrumented_partial_span_seconds=partial,partial_origin='mtime of first saved review-owned input verification,after initial reads',controlled_G1_execution_seconds=0,producer_preparation_elapsed_scope='phase.elapsed separately discloses1466.678544998169s partial authoring/recovery span;not charged G1 execution'),limits=limits,evidence_manifest='evidence-manifest.json',hash_cycle_policy='Manifest hashes final review and all reviewer files except itself;review references manifest path,not hash.')
write(OWN/'review.json',review)

md='''# P12 — R03 G1 受限续行执行前复核

**PASS_WITH_LIMITS；当前未发现可证实的执行阻塞。** 仅接受精确R03准备版本。协调端可随后在原授权剩余额度内交付精确EXECUTE；本复核不自动执行、不新建额度、不代表G1资格通过。

## 精确输入与实际差异

实际HEAD：`c25180848ebfe9a1f49da0aa5f579cac913e6428`，不代表全部dirty工作树成果。packet、phase、manifest、registration/source/decision绑定均独立核验；649封存成员、48来源绑定、2382保护文件前后均0失配，current与snapshot一致，Git index指纹未变。51份review-owned复制输入前后不变，真实R03 pool/attempt.lock均未创建。

输入身份完整SHA见review.json.input_identity；manifest为169e27b1180a9e3a866559b48864b2352ec4a5715230d315e4abfc4e158e2f59。旧E01终止池、P11原件及原grant/decision均绑定。24语义/参考材料及observations.py与R02一致；job argv/order只做路径规范化，唯一删除setup-make。caps/tool pins不变。复用P10/P10B有限语义推导，无旧实验重跑。

## 逐项验收

| 项目 | 判定与证据 |
|---|---|
| P11-R1权限依赖 | R03预检范围关闭。runtime.py:36–49、60–78、90–132：注册入口inventory_probe=None，无ps/run扫描；AST仅见Popen。optional PermissionError/OSError/timeout分别记录unavailable/incomplete，正常root exit由poll/wait确定。 |
| 必需保护 | runtime.py:65–78、90–132：自身PGID探测/kill/wait/poll失败保留PROTECTION_UNRESOLVED并halt；独立探针随后再次请求均无新Popen，预留不退款。pending timeout仍使用原deadline。无完整子树或硬实时保证。 |
| P10-R1 | budget.py:77–91、107–142及runtime.py:52–61：慢save/mkdir/log/最近precheck跨界均0 mock Popen；保留CHARGED_NOT_DISPATCHED/NOT_RUN与持久halt。未重置clock。 |
| P10-R2 | observations.py字节未变；新鲜14项包括完整16ns观察接受、14ns尾段按VCD_TIME_COVERAGE_MISSING拒绝、缺头/未知/缺信号/未来native候选拒绝。无波形回放。 |
| 累计预算 | allocation.py:59–102、budget.py:14–53：执行前核对不可变旧pool/grant/phase/P11/decision及终止状态，setup1/实测0.04572445806115866s与charge2分列；最多7setup/1198s，work1193s。假旧用量0、扩大窗口/祖先漂移均拒绝。 |
| 最后持久化越界 | budget.py:152–178、runner.py:188–202：修复后的独立完整main收尾对照，正常exit0；末次save推进1199s时，磁盘completed=true/halted=true/charged1201，特定halt原因FINAL_PERSISTENCE_EXCEEDED_CUMULATIVE_WALL_CAP，runner exit1。未以别的异常掩盖。 |
| 新门禁与独占 | runner.py:32–72、83–88及continuation_contracts.py:39–54：新P12身份+新manifest/reg/source+continuation+旧pool；完整review_gate独立baseline接受、7个旧/错误身份负例拒绝。固定lock/pool独占创建，不支持任意多路径/并发资源池泛化。 |

源码SHA：runtime d34cc3a9c01ae55fdf3fd97c55116f0287e74ef8d8ad94e851e9607e2cdd7d7f；budget 257dc9da8130c0b5a5ca1f09096524004a422193bb120a8b73c59b8072f107ab；runner 73f0aee7ad26cc761d894a97d52f7f7981f766c7a77483d75ac86dafef2c4485；其他逐源SHA见review.json/evidence-manifest.json。

## 验证数量、命令与审查者错误

- Producer保存111次pure case invocation含1失败，最终源28+14=42通过；旧attempt2原tool退出码UNKNOWN，保存summary/log确定失败，不补造exit1。
- Reviewer复制后新鲜运行同两小模块42项，均exit0/0fail；未运行旧R01/R02/G0套件。命令入口run_fresh_suites.py及两个内部suite exit均保存。
- 独立探针初次31次，其中29个非收尾探针有效；2个初版收尾夹具漏放标签文件而提前FileNotFound。正常基线失败，越界夹具虽“匹配失败”但原因错误，**两者均排除验收证据**。原文件/输出/exit1全部保留。
- 新finalization_probes_v2.py仅重验修正的2个对照，均符合预期。因此独立共33次调用、31个有效独立检查；不是33个首次即成功。最终越界fixture SHA6b2b3783ac52aba5f0c5c57d8955757cc1487919b862d80223a30525b9f60c56；正常fixture SHAe24a9309c84b8adb7dd83b4be4bbe74056c3575014ac0585b2484849a9b2ce4c。逐fixture/result SHA在各summary和证据manifest。
- 首次输入检查另有reviewer封存路径映射错误：checklist实际在包根，不在递归snapshot；修正映射后两次0失配，初次exit1/result保留。不是源输入缺失。

完整命令和退出码见commands-and-incidents.json。全部Python以PYTHONDONTWRITEBYTECODE=1执行，真实G1工具/version/compile/BMC/sim/ps/signal/API/network/key/安装均0；运行器中的进程与sleep全mock。实际OS保障不由fake结果扩大。

## P12-N1 — 非阻塞来源范围说明

severity=P3，material=false。phase.json的actual_R03_resources.network=0及commands-and-checks中的0仅按**受控G1准备路径**解释。P12a已记录同turn转向旧PPT、网页读取和辅助记录写入；42PPT当时无漂移。不能将整turn描述成仅G1/完全无network。该事件已于idle恢复，不重审或推断PPT覆盖/API调用。建议后续closure sidecar引用P12a并明确上述scope；不改封存原件、不为此阻塞代码预检。完整full-turn耗时未测，不填0；producer partial authoring/recovery span与G1执行耗时分列。

## Hallmark、路由与保留限制

本轮实际新读Hallmark SKILL.md与review-finish.md，SHA与此前版本一致；用于固定材料独立critique、事实/意图区分、定位/排序与最小修订，本报告上述三处有对应应用。workflow/scripts=false，未运行网页/UI/Together。技术结论来自源码、SHA和独立纯fake，详见hallmark-usage.json。

接受后仅可路由G1_EXECUTE_CONTINUATION_AFTER_P12精确收据，绑定本review SHA及R03 manifest/reg/source/decision/predecessor。不再询问同任务重试许可；不把评审本身当EXECUTE，不修改/重开E01池、不退款。累计原32compile/32BMC+cover(depth8/10s)/32physical(2s、≤32cycles/run、1024total)/1200s仍有效，当前至多7setup、1198s。18逻辑编译根作业不等于18OS进程；make版本NOT_REPROBED。

G1仍NOT_QUALIFIED：R03无真实控制结果；E01/P11失败与未知不改。无完整PID清点/任意脱离进程组后代约束、OS绝对实时或通用多进程并发事务保证。QC07/15空泛、QC12/13四态限制、QC14运输、128completion/general correctness、74未复现、selected样本/类别、F1/H1/H2/L1、P04证据订正、P05/P06限定范围、P05-N1、billing UNKNOWN和R0/R1/R2 planned均保留。未扩大到G2/API/数据/候选/付费。

只写P12自有目录，未联系producer/创建agent或chat，未改source/shared/results/index。完整保全和命令见JSON；本轮到此停止。
'''
with (OWN/'review.md').open('x') as f:f.write(md)
validation=dict(status='PASS',review_status=review['status'],input_checks='before-corrected and after zero mismatches',source_copy_unchanged=True,fresh_suite_tests=42,accepted_independent_checks=31,reviewer_errors_retained=True,source_and_original_hashes_not_rewritten=True,real_pool_lock_uncreated=after['real_paths_uncreated'])
write(OWN/'final-validation.json',validation)
files={str(p.relative_to(OWN)):sha(p) for p in OWN.rglob('*') if p.is_file() and p.name!='evidence-manifest.json'}
manifest=dict(scope='P12 reviewer-owned exact inputs/code/fixtures/results/report;external dependencies individually listed in input-verification files',files=files,file_count=len(files),excluded=['evidence-manifest.json'],source_hashes=source_hashes)
write(OWN/'evidence-manifest.json',manifest)
assert all(sha(OWN/rel)==expected for rel,expected in files.items())
print(json.dumps(dict(status=review['status'],qualification=review['qualification_status'],execution_blockers=0,review_sha256=sha(OWN/'review.json'),evidence_manifest_sha256=sha(OWN/'evidence-manifest.json'),evidence_files=len(files)),ensure_ascii=False))
