"""P14 report from already-saved pure evidence; final bounded preservation check."""
from pathlib import Path
import hashlib,json,subprocess
from datetime import datetime,timezone
OWN=Path(__file__).resolve().parent;ROOT=OWN.parents[3]
AUDIT=ROOT/'docs/audits/producer_test2_g1_R04_2026-11-06';SNAP=AUDIT/'snapshot'
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
    with Path(p).open('x') as f:json.dump(v,f,ensure_ascii=False,indent=2)
phase=read(AUDIT/'phase.json');manifest=read(AUDIT/'snapshot-manifest.json')
assert sha(AUDIT/'phase.json')=='8189a3e504e59b9baa3d5ef7d2f1d7e0b625be83fb0cbcc0eb4e3608b0ff7fa8'
assert sha(AUDIT/'snapshot-manifest.json')=='a61cd8744e44eb599abe331079766215a4860d64b07a3080090f8f29e9e97b0a'
for rel,h in manifest['files'].items():
    assert sha(AUDIT/rel)==h
    if rel.startswith('snapshot/'):assert sha(ROOT/rel[9:])==h
pres=read(AUDIT/'preservation-before.json')
for rel,h in pres['files'].items():assert sha(ROOT/rel)==h
reg=read(SNAP/phase['registration']);source=read(SNAP/phase['source_manifest'])['files']
index=subprocess.check_output(['git','--no-optional-locks','ls-files','--stage','-z'],cwd=ROOT)
assert hashlib.sha256(index).hexdigest()==phase['index_sha256']
assert not any((ROOT/reg[k]).exists() for k in ['pool_state','attempt_lock'])
for key,expected in [('user_physical33_authorization','91837999f0b24424ed5ca3f89a3744a6358453e669568f68ba4b68794c68d24e'),('budget_amendment','449692ff3a154f5b697a8c80f7e6795a269b488bb5efbfd0f0ab0384539ebc67'),('continuation_decision','80f69ec8d1ee0a0076dac1daa4a009b1b2e4868c5b2cd41327088a0c7fca889e')]:assert sha(SNAP/reg[key])==expected
summary=read(OWN/'fresh-r04-tests-isolated/summary.json');assert (summary['tests'],summary['failures'],summary['errors'])==(17,0,0)
for rel,h in read(OWN/'isolated-suite-inputs.json').items():assert sha(OWN/'isolated-suite-copy'/rel)==h
probes={}
for name in ['plan-allocation','reject-prior_wall_charge_seconds','reject-attempt_maximum_window_seconds','reject-prior_reserved','positive-entry']:
    r=read(OWN/name/'result.json');assert r['passed'];probes[name]=dict(fixture_sha256=sha(OWN/name/'fixture.json'),result_sha256=sha(OWN/name/'result.json'))
assert read(OWN/'positive-entry/result.json')['ledger']['halt_reason']=='REVIEW_STOP_NO_REAL_EXECUTION'
code=SNAP/'test2/g1_v4';reuse=read(code/'native-reuse.json')
hallmark=dict(considered=True,read_this_round=True,source='/Users/yiwenchen/.codex/skills/hallmark/SKILL.md',source_sha256=sha('/Users/yiwenchen/.codex/skills/hallmark/SKILL.md'),read_evidence=[dict(tool='skills__read',package='e0/hallmark'),dict(tool='skills__read',package='e0/hallmark',resource='skill://codex-home-skills/Users/yiwenchen/.codex/skills/hallmark/references/review-finish.md')],review_finish_sha256=sha('/Users/yiwenchen/.codex/skills/hallmark/references/review-finish.md'),applied_for=['固定精确材料独立critique：512/source/reuse/authority检查，不以producer意图或17PASS代替证据。','定位实质风险/最小范围：review.md逐项时序/复用/预算验收，不重开P2/I2C或通用validator。','保护不可稀释边界：修复合理性与SV实际有效性分开；保留旧失败、unknown与累计成本。'],prior_read_reference=None,workflow_executed=False,scripts_executed=False,not_applicable_reason='网页UI流程不适用RTL/资源预检；未执行Together、UI或脚本。技术结论来自源码、精确hash及离线探针。')
write(OWN/'hallmark-usage.json',hallmark)
identity=dict(producer_phase_sha256=sha(AUDIT/'phase.json'),producer_manifest_sha256=sha(AUDIT/'snapshot-manifest.json'),registration_sha256=sha(SNAP/phase['registration']),source_manifest_sha256=sha(SNAP/phase['source_manifest']),continuation_decision_sha256=reg['continuation_decision_sha256'],budget_amendment_sha256=reg['budget_amendment_sha256'],native_reuse_manifest_sha256=sha(code/'native-reuse.json'),user_physical33_authorization_sha256=sha(SNAP/reg['user_physical33_authorization']),predecessor_E02_pool_sha256=reg['predecessor_pool_sha256'],predecessor_E01_pool_sha256=reg['first_pool_sha256'])
incidents=[dict(id='P14-HARNESS-1',product_defect=False,command_exit=1,source='review_checks_attempt1.py',cause='Mistakenly compared current stage-entry digest with pre-publication preservation-before historical index;phase/resumption-baseline have correct current digest andstage0.',evidence='resumption-baseline.json and phase.index_sha256;old86e88... vs current9f597...',resolution='Use exact post-publication phase/resumption baseline,no Git mutation or rollback.'),dict(id='P14-HARNESS-2',product_defect=False,command_exit=1,source='review_checks.py',failed_suite='fresh-r04-tests/summary.json',counts=dict(tests=17,failures=2,errors=1),cause='Positive-entry fake pool/lock in shared reviewer copy invalidated tests14/17 empty-namespace assumptions;copy omitted old observations.py required by test2.',resolution='Preserved all first outputs;new isolated-suite-copy includes SHA-identical old observer and no fake pool. run_isolated_suite.py fresh17/0/0,exit0. No producer source edits.' )]
review=dict(phase='P14_G1_R04_STARTUP_PREFLIGHT',status='PASS_WITH_LIMITS',actual_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),observed_at_utc=datetime.now(timezone.utc).isoformat(),input_identity=identity,findings=[],execution_blockers=[],may_route_exact_R04_EXECUTE=True,autoexecution=False,qualification='NOT_QUALIFIED_SV_FIX_UNMEASURED',acceptance_scope='Exact R04 pre-execution preparation under actual physical33 amendment;not SV/ABI or general tool qualification.',integrity=dict(snapshot_bindings=512,source_bindings=len(source),protected_files=len(pres['files']),current_snapshot_drift=[],index_sha256=phase['index_sha256'],staged_changed_paths_count=0,real_pool_lock_uncreated=True),source_sha256={str(p.relative_to(code)):sha(p) for p in [code/'sources/physical_tb.sv',code/'sources/common.sv',code/'sources/QC00_formal.sv',code/'allocation.py',code/'budget.py',code/'runner.py',code/'native_reuse.py',code/'continuation_contracts.py',code/'runtime.py',code/'observations.py']},acceptance_checks=dict(startup='Positive1ps step7->0 after time-zero processes can establish a real sensitivity event;first999ps compensation keeps pre/edge/post schedule. No compiled validation.',timing_ps=dict(step_changes=[1,4000,8000,12000],pre=[1000,5000,9000,13000],posedge=[2000,6000,10000,14000],post=[3000,7000,11000,15000],end=16000),native_reuse='17native/common SV and23 semantic/reference deps unchanged;actual old SMT/argv/tool pins/logs/receipt/report/pools hash-bound. QC00 compile1/native2 REUSED_FROM_E02;old rejectedphysical not reused.',authorization='Actual user physical33/amendment/decision matched;E01+E02 terminal pools and old costs inherited.',budget='New0setup/17compile/30native/32physical128cycles; cumulative8/20/32/33/132. Prior actual5.197697583120316 vs prior charged7.151973249856383 retained; conservativecharge8/current1192/work1187<=1200.',process='runtime/parser unchanged from R03/P12+E02;owned-group mandatory guards retained,no ps/new permissions;budget differs only attempt_id from R03.',gate='Copied exact positive review_gate/main reaches Budget with real authority/reuse metadata and fake P14 receipt;only fake job dispatched then intentional halt. Duplicate copied attempt refused before another job. No production receipt created.'),validation=dict(producer_final_pure_tests=17,producer_prior16_preserved=True,reviewer_initial_suite=dict(tests=17,failures=2,errors=1,not_product_failure=True),reviewer_isolated_fresh_suite=dict(tests=17,failures=0,errors=0,summary_sha256=sha(OWN/'fresh-r04-tests-isolated/summary.json')),independent_valid_checks=6,independent_probe_bindings=probes,duplicate_attempt_refused=True,plan_allocation_complete_pure_bookkeeping=True,positive_main_scope='All hardware process execution replaced by fake execute;host binary digest checks stubbed. Does not exercise actual SV/tools/runtime ABI.',reviewer_harness_incidents=incidents),commands=[dict(command='PYTHONDONTWRITEBYTECODE=1 python3 .../P14_g1_startup_preflight/review_checks.py',attempt=1,exit_code=1,note='historical-index harness assumption'),dict(command='PYTHONDONTWRITEBYTECODE=1 python3 .../P14_g1_startup_preflight/review_checks.py',attempt=2,exit_code=1,note='independent5+duplicate checks succeeded;17suite isolation failures retained'),dict(command='PYTHONDONTWRITEBYTECODE=1 python3 .../P14_g1_startup_preflight/run_isolated_suite.py',exit_code=0),dict(command='PYTHONDONTWRITEBYTECODE=1 python3 .../P14_g1_startup_preflight/finalize_review.py',exit_code=0)],hallmark_usage='hallmark-usage.json',limits=['仅预检接受，SV首拍修复必须由下一次精确授权实际R04验证；没有以17mock或算术声称通过。','当前physical额度恰满，任何新的物理失败/重试都须保留并重新计算余量，不退款、不重置或自动增帽。','native复用仅QC00固定depth8/旧模型结果，make NOT_REPROBED/smtbmc help-only UNKNOWN保持；无新setup。','QC07/15空泛、QC12/13四态诊断、QC14运输、128/unbounded/generalDUT/oracle/B-C优劣未证明。','无完整子树普查/任意并发事务/OS硬实时保证；时间字段为保存checkpoint；必要PGID/poll/wait/kill错误仍halt。','P13旧X、E01/E02失败/unknown、全部旧score/74未复现/selectedsample/F1/H1/H2/L1/P04/P05/P06/P05-N1/billing限制保留。','用户最新优先G1后raw/B-C；本接受不授权模型API/新科学比较，不能自动扩到raw或B/C。'],actual_new_G1_tools=dict(compile=0,native=0,physical=0,ps_probe_signal=0,model_API_network_keys_install=0,real_pool_lock_created=0),evidence='evidence.json')
write(OWN/'review.json',review)
text='''# P14 — R04 首拍修复执行前独立复核

**PASS_WITH_LIMITS，无已证实执行阻塞。** 可由协调端随后交付精确R04 EXECUTE，在已批准累计caps内尝试唯一实际R04。**不是G1通过，首拍SV修复仍未实测。**

## 精确输入

phase SHA8189a3e504e59b9baa3d5ef7d2f1d7e0b625be83fb0cbcc0eb4e3608b0ff7fa8；manifest SHAa61cd8744e44eb599abe331079766215a4860d64b07a3080090f8f29e9e97b0a；registration29dcc2a0781927ac1cc624850c9fdda44625fe468544eae881f4ea86e92cfa31；source57e79f812133ec94f340009c18227b8bf773515ea571d0b172c9c59e9abd9705。

512封存binding、来源绑定及4485保护文件当前匹配，原件未改；实际HEAD2de33e981d2fffc9739d2ca049fbae1774de1aad，当前stage0。原10000-stage基线属于发布前历史；使用resumption-baseline/phase的9f597996...索引条目指纹，未回退旧HEAD或改Git。真实v4 pool/lock始终未创建。

## 核心判定

- **时序合理，但效果未实测。** physical_tb.sv:4、18–23（SHA7be66871399b32b36ce91df607e3f5d1f3c653b27cf154b43b7f377f5c49c6ca）：初始step7，正1ps后step0产生实际变化，避开time-zero敏感列表尚未等待的情形；第一轮999ps补偿。独立有理数推导pre1000/5000/9000/13000、posedge2000/6000/10000/14000、post3000/7000/11000/15000、finish16000ps。没有新增posedge、跳首拍、X补0或改标签；QC14 marker仍仅最后post。需实际双sim首拍/全部行/VCD才确认修复。
- **native复用闭合。** native_reuse.py:11–37及native-reuse.json SHA1878bd0ea59e00c67d91f2125cd72031c902283931616de52f0ecdb9a6ccc84b绑定旧E02 source/SMT/argv/tool pins/日志/receipt/report/终止pool。17份native/common SV、23材料及parser不变。QC00编译1+native2明确REUSED_FROM_E02且旧成本已继承，绝不复用旧不合格physical；新32physical仍全运行。原有深度8/有限scope不扩大。
- **实际physical33批准与累计预算。** allocation.py:54–99先核真实approval/amendment/decision、E01/E02已终止池；批准只增physical32→33。新0setup/17compile/30native/32physical128cycles，累计8/20/32/33/132，不是新32/32/33池。保留先前actual5.197697583120316s及charged7.151973249856383s，charge8是保守分配；current1192/work1187，累计1200不重置。完整纯记账探针得到准确累计数，下一physical请求拒绝并halt，之后继续请求也拒绝。
- **真实入口ABI与独占。** runner.py:33–53、70–76和新gate要求P14/精确manifest/reg/source/decision/amendment/旧E02池；独立复制入口使用真实保存批准/复用字节和明确fake P14 receipt，能进入Budget并完成一次fake reservation，随后主动halt；重复copied lock拒绝，ledger不变。硬件执行和host binary digest检查均stub，不能叫实际工具入口验证。
- **必要保护保留。** runtime.py及observations.py与R03相同；Budget逻辑只改attempt_id，绝对deadline、慢持久化/临派发检查、最后save越界halt、PGID/poll/wait/kill及未知保留逻辑未退回。E02真实收据的有限结果可复用为背景，不重跑旧套件。无ps、新权限或setup查询。

## 证据与审查者脚手架错误

生产者最终17项保存检查与封存源绑定；独立干净副本新鲜17/17 PASS，旧16项历史保留。另有6个独立检查（完整plan累计/三种坏继承拒绝/正向入口/重复启动拒绝）。源码及fixture/result SHA在evidence.json。

审查自身两类错误透明保留：第一次错用发布前index基线导致exit1；修正后共享review-copy已有fake pool使17suite中2fail，另漏复制旧observations.py导致1error。它们不是产品失败。第一次源码和日志/summary全部保留；新isolated-suite-copy包含字节相同observer且无fake pool，独立17项exit0，未改producer测试/原件。这两次不能描述成首次即全通过。

Hallmark本轮实际新读SKILL.md及review-finish：用于固定材料独立critique、实质问题定位/最小范围和不稀释失败/未知原则，具体应用为以上三类验收；来源SHA及read evidence在hallmark-usage.json。网页workflow/scripts=false，RTL时序/预算/复用判断由源码和纯离线证据完成。

## 后续边界

本review的phase=P14...、status=PASS_WITH_LIMITS及全部input_identity可供新门禁绑定；协调端还须另发精确EXECUTE。物理预算现在恰够全计划，若再失败，不自动增加或退还已花成本。真实执行后再审原始首行/双sim/状态/费用，届时才能判断公开G1有限资格；不借预检声称general correctness/128cycle/原74原因已解决。QC07/15空泛、QC12/13四态不支持、QC14仅运输与所有历史未决保持。

本轮0真实工具/仿真/API/key/network/install，不占真实pool/lock，不改producer/shared/index、不发消息/commit/push，不审P2/I2C或启动raw/B-C新研究。到此停止。
'''
with (OWN/'review.md').open('x') as f:f.write(text)
evidence={str(p.relative_to(OWN)):sha(p) for p in [OWN/'review.json',OWN/'review.md',OWN/'hallmark-usage.json',OWN/'review_checks.py',OWN/'review_checks_attempt1.py',OWN/'run_isolated_suite.py',OWN/'isolated-suite-inputs.json',OWN/'fresh-r04-tests/summary.json',OWN/'fresh-r04-tests/unittest.log',OWN/'fresh-r04-tests-isolated/summary.json',OWN/'fresh-r04-tests-isolated/unittest.log',OWN/'finalize_review.py']}
for folder in [OWN/x for x in probes]:
    for p in folder.rglob('*'):
        if p.is_file():evidence[str(p.relative_to(OWN))]=sha(p)
write(OWN/'evidence.json',dict(files=evidence,hash_cycle_policy='review references evidence path; evidence hashes review',source_bindings=source,producer_manifest_sha256=identity['producer_manifest_sha256']))
assert all(sha(OWN/r)==h for r,h in evidence.items())
print(json.dumps(dict(status=review['status'],source_bindings=len(source),real_pool_lock_uncreated=True,qualification=review['qualification'],review_sha256=sha(OWN/'review.json'),evidence_sha256=sha(OWN/'evidence.json')),ensure_ascii=False))
