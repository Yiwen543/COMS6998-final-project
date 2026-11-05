#!/usr/bin/env python3
"""One API-free qualification path; never launches generation or edits freezes."""
import argparse
from collections import Counter
import datetime
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
from zoneinfo import ZoneInfo
from common import ROOT,BASE,clean_env,dump,run,sha
from controller_monitor_live import TASK
from controller_obligations import prepare,evaluate,fixtures
from controller_packet import identity,unpack_coverage
from controller_packet_compact import unpack
from controller_release_live import verify_release,ARMS
from controller_formal_diagnostic import REG,calibration,balanced_correct
from controller_loop_live import plumbing
from controller_reference_evaluate import module
import controller_monitor_done as done
from coverage import summary as coverage_summary

RUN=BASE/'results/controller-live-v1'


def integrity():
    reg=json.loads(REG.read_text());counts={}
    fixture_hash=hashlib.sha256(json.dumps(fixtures(),sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if fixture_hash!=reg['fixture_sha256']:raise ValueError('Registered qualification fixtures changed')
    for name,h in reg['source_freezes'].items():
        if sha(ROOT/name)!=h:raise ValueError('Parent freeze changed: '+name)
        d=json.loads((ROOT/name).read_text());members=d.get('files',d.get('artifact_sha256'))
        for path,expected in members.items():
            if sha(ROOT/path)!=expected:raise ValueError('Frozen artifact changed: '+path)
        counts[name]=len(members)
    verify_release(RUN)
    if sha(RUN/'release.json')!=reg['release']['sha256']:raise ValueError('Candidate release changed')
    return counts


def verify_formal_evidence(directory,data,balanced=False):
    selections=json.loads((RUN/'final-candidates.json').read_text())['candidates']
    for j in data['jobs']:
        if 'directory' not in j:
            if not j['status'].startswith(('NOT_RUN','INVALID')):raise ValueError('Missing formal job binding')
            continue
        d=directory/j['directory'];r=json.loads((d/'result.json').read_text())
        if r['status']!=j['status'] or sha(d/'sby.log')!=r['log_sha256']:raise ValueError('Saved formal evidence changed')
        if (d/'work/status').exists() and (d/'work/status').read_text().split()[0]!=j['status']:raise ValueError('Native formal status mismatch')
        if balanced:
            f=next(f for f in selections if (f['arm'],f['repetition'])==(j['arm'],j['repetition']))
            if sha(d/'work/src/candidate.sv')!=sha(RUN/f['directory']/'candidate.sv'):raise ValueError('Balanced source is not frozen final')
        if 'witness' in j:
            w=json.loads((d/'physical-witness/result.json').read_text())
            if w!=j['witness']:raise ValueError('Physical witness result changed')
            if w.get('status')=='adjudicated':
                oracle=json.loads((d/'physical-witness/reference.json').read_text())
                if oracle['verdict']!=w['reference_verdict']:raise ValueError('Independent witness verdict changed')
    return True


def audit(out,fresh_semantics=True):
    out.mkdir(parents=True,exist_ok=False);counts=integrity();versions={}
    for cmd in [['yosys','-V'],['sby','--version'],['z3','--version'],['iverilog','-V'],['verilator','--version'],['cargo','--version']]:
        r=subprocess.run(cmd,capture_output=True,text=True,env=clean_env(),timeout=10)
        versions[cmd[0]]=dict(returncode=r.returncode,first_line=(r.stdout+r.stderr).splitlines()[0])
    versions['python']=sys.version
    directory=TASK/'qualification/prompt-audit-v3';b=json.loads((directory/'B2_raw.json').read_text());c=json.loads((directory/'C2_semantic.json').read_text())
    semantic=c.pop('egraph_feedback')
    if b!=c:raise ValueError('B/C common information mismatch')
    raw=unpack(b['raw_coverage']);sets=[unpack_coverage(raw,i) for i in range(3)]
    hitmaps=[{identity(p):p['hits'] for p in points} for points in sets]
    identities={identity(p) for p in sets[0]};coverage={};unc=[]
    for i,name in enumerate(b['coverage_trace_order']):
        original=json.loads((TASK/'qualification/observations-v2/verilator'/name/'raw-points.json').read_text())
        if {identity(p):p['hits'] for p in sets[i]}!={identity(p):p['hits'] for p in original}:raise ValueError('Coverage codec/source mismatch')
        coverage[name]=coverage_summary(sets[i])
    if len(identities)!=3168:raise ValueError('Raw denominator changed')
    for p in sets[0]:
        key=identity(p)
        if all(h[key]==0 for h in hitmaps):unc.append({k:p[k] for k in p if k!='hits'})
    dump(out/'uncovered-source-points.json',unc)
    typed=TASK/'qualification/typed-v5';proof=json.loads((typed/'proof/proof.json').read_text());screen=json.loads((typed/'screen/screen.json').read_text())
    if proof['status']!='pass' or not proof['environment_satisfiable'] or any(c['z3']!='unsat' for c in proof['definition_checks']):raise ValueError('Typed certificate not accepted')
    if proof['unsafe_free_combinational_values']:raise ValueError('Unsafe free combinational definitions')
    semantic_run=dict(status='saved_evidence_audit_only',definition_checks_audited_not_rerun=len(proof['definition_checks']),supported=screen['typed_supported'],mapped=screen['mapped'],unresolved=screen['unresolved'],raw_targets=screen['raw_targets'])
    payload=json.loads((typed/'screen/egg-input.json').read_text());saved=json.loads((typed/'screen/egg.json').read_text())
    if fresh_semantics:
        z=run(['z3',typed/'screen/pairs.smt2'],out/'ground-rules-z3.log',30)
        if z['status']!='complete':raise ValueError('Ground-rule query replay incomplete')
        statuses=(out/'ground-rules-z3.log').read_text().splitlines();old=(typed/'screen/z3.log').read_text().splitlines()
        order=json.loads((typed/'screen/query-order.json').read_text())
        if statuses!=old or len(statuses)!=len(order):raise ValueError('QF_BV replay differs from saved evidence')
        for rule in payload['verified_rules']:
            if statuses[order.index(rule['source_ids'])]!='unsat':raise ValueError('Unproved ground rule')
        engine=ROOT/'egraph/target/debug/guard_proofs'
        if not engine.is_file():raise ValueError('Existing egg binary unavailable; no build/install attempted')
        started=time.perf_counter();p=subprocess.run([str(engine)],input=json.dumps(payload),capture_output=True,text=True,env=clean_env(),timeout=15)
        (out/'egg.json').write_text(p.stdout);(out/'egg.stderr.log').write_text(p.stderr)
        if p.returncode:raise ValueError('egg replay failed')
        graph=json.loads(p.stdout);roots={r['id']:r['eclass'] for r in graph['targets']};prior={r['id']:r['eclass'] for r in saved['targets']}
        ids=sorted(roots)
        if set(roots)!=set(prior) or any((roots[a]==roots[b])!=(prior[a]==prior[b]) for a in ids for b in ids):raise ValueError('egg equivalence partition changed')
        semantic_run.update(status='fresh_ground_rules_and_egg_replay_passed',ground_rule_queries=len(statuses),ground_rules_verified=len(payload['verified_rules']),qfbv_seconds=z['seconds'],egg_engine_sha256=sha(engine),egg_seconds=time.perf_counter()-started,egg_iterations=graph['iterations'],egg_stop_reason=graph['stop_reason'])
    selected=[m['source_point'] for g in semantic['groups'] for m in g['members']]
    if any(identity(p) not in identities for p in selected):raise ValueError('Semantic source point is not a raw DUT counter')
    semantic_run.update(C_groups=len(semantic['groups']),selected_source_points=len(selected),unhit_selected_points=sum(all(h[identity(p)]==0 for h in hitmaps) for p in selected),scope=screen['proof_scope'])
    source={str(p.relative_to(ROOT)):sha(p) for p in (TASK/'public/rtl').glob('*.v')}
    source[str((TASK/'public/task_top_v3.sv').relative_to(ROOT))]=sha(TASK/'public/task_top_v3.sv')
    calls=[json.loads(x) for x in (RUN/'calls.jsonl').read_text().splitlines()]
    adapter=dict(source='scripts/pilot_model.py',sha256=sha(ROOT/'scripts/pilot_model.py'),recorded_generation_calls=len(calls),recorded_exact_models=sorted({r['returned_model'] for r in calls}),recorded_usage_cap_match=all(r['input_token_count']==r['usage']['input_tokens']<=64000 and r['usage']['output_tokens']<=8192 for r in calls),current_API_connection_tested=False,current_API_calls=0)
    result=dict(verified_local=datetime.datetime.now(ZoneInfo('America/New_York')).isoformat(),freeze_members=counts,versions=versions,source_sha256=source,coverage=coverage,raw_denominator=3168,uncovered_in_all_development=len(unc),semantic=semantic_run,model_adapter=adapter,DUT_specification_hash=sha(TASK/'public/specification_v2.md'),reference_checker_sha256=sha(TASK/'reference/frozen-v2/checker.py'),fixed_coverage_is_not_a_monitor_effect=True)
    dump(out/'audit.json',result);return result


def marker_qualification(out):
    reg=json.loads((BASE/'configs/controller_done_abi_v1.json').read_text())
    if sha(ROOT/reg['contract']['path'])!=reg['contract']['sha256'] or reg['candidate_live_allowed']:raise ValueError('End-marker draft contract changed or live enabled')
    out.mkdir(parents=True,exist_ok=False);cases=fixtures();results={}
    for name,body,names in [('timing','assign active={6{trace_done}};assign ok=0;',['legal_exact']),('final_offer','assign active={6{trace_done}};assign ok={6{!s_valid}};',['legal_exact','input_never_accepted','missing_status_response'])]:
        candidate=plumbing(3);candidate['body']=body;d=out/name/'compiled'
        if done.compile_monitor(candidate,d)['status']!='complete' or done.build_replay(d)['status']!='complete':raise ValueError('End-marker plumbing compile failed')
        for case in names:
            r=done.replay(d,cases[case]['rows'],out/name/case,out/'row-cache');results[name+'/'+case]=r
            if not r['complete']:raise ValueError('End-marker replay incomplete')
            expected=bool(name=='timing' or case=='input_never_accepted')
            for p in r['properties']:
                if p['checks']!=1 or bool(p['failures'])!=expected or p['unknown']:raise ValueError('End-marker boundary differs from contract')
    result=dict(status='passed',plumbing_cases=len(results),API_calls=0,DUT_cycles_added=0,experimental_candidate=False,not_an_independent_oracle=True,missing_status_is_intentionally_not_checked_by_this_plumbing_predicate=True,contract_sha256=sha(TASK/'public/observer_contract_v3_draft.md'))
    dump(out/'summary.json',result);return result


def report(out,audit_data,control_dir,matrix_path,cal,balanced,marker):
    matrix=json.loads(matrix_path.read_text());labels=json.loads((control_dir/'reference-labels.json').read_text())
    finals=[r for r in matrix['records'] if r['round']==6];counters=Counter(r['verdict'] for r in labels.values())
    summary=dict(API_calls=0,new_independent_LLM_trials=0,old_scores_unchanged=True,reference_label_counts=dict(counters),synthetic_control_replays=sum(v.get('status')!='NOT_RUN_INVALID_INPUT' for r in matrix['records'] for v in r['cases'].values()),synthetic_control_cycles=matrix['cycles'],final_candidate_control_results=[],formal_profiles=[],markers=marker)
    for r in finals:
        values=r['cases'];summary['final_candidate_control_results'].append(dict(arm=r['arm'],repetition=r['repetition'],reference_accepted_alarm_cases=[n for n,v in values.items() if v['reference']=='PASS' and (v['alarm_records'] or v['unknown_records'])],missed_reference_FAIL=[n for n,v in values.items() if v['reference']=='FAIL' and not v['detected_reference_failure']],unresolved_cases=[n for n,v in values.items() if v.get('unresolved')]))
    if balanced:
        for arm in ARMS:
            for rep in (1,2,3):
                jobs=[j for j in balanced['jobs'] if (j['arm'],j['repetition'])==(arm,rep)]
                summary['formal_profiles'].append(dict(arm=arm,repetition=rep,by_mode={mode:dict(Counter(j['status'] for j in jobs if j['mode']==mode)) for mode in ('bmc','prove','cover')},correct_source_physical_witnesses=[j['witness'] for j in jobs if 'witness' in j]))
    dump(out/'summary.json',summary)
    lines=['# 自主离线资格与端到端复现','', '本轮没有API调用、新LLM重复或旧评分改写。所有旧DUT/独立Claude参考/候选/冻结保留。新控制与形式配置均另行登记。','',
           '## 可验证范围','',f'- 原DUT/规格/被动monitor回放/API适配器/原始Coverage-3/typed+egg管线已审计；原始计数分母{audit_data["raw_denominator"]}，开发三迹全部未命中{audit_data["uncovered_in_all_development"]}点，明细在audit/uncovered-source-points.json。',
           f'- 各迹实际line/branch/expr/toggle分母及命中见audit/audit.json；行为义务不是RTL覆盖率，固定刺激的覆盖不会被生成monitor提高。',
           f'- 语义复核：{audit_data["semantic"]}。168项typed定义证书本轮核对，未重跑其整个前端；新鲜QF_BV/egg状态单列。',
           '- LLM适配器代码与历史实际Responses/usage已核对，本轮未做网络连通性测试；离线资格入口不需要key。','',
           '## 规格义务控制','',f'{len(labels)}个显式合成控制，标签{dict(counters)}；{summary["synthetic_control_replays"]}次候选回放、{matrix["cycles"]}周期。invalid不执行候选，UNRESOLVED不计通过。样例由原独立checker判定；未证明所有样例在原DUT物理可达。因此“参考接受样例上报警”仅是规格一致性诊断，不自动称为原DUT误报。','',
           '| 组 | 重复 | 未检出的参考FAIL控制 | 参考接受控制上的报警/未知样例 |','|---|---:|---|---|']
    for r in summary['final_candidate_control_results']:lines.append(f'| {r["arm"]} | {r["repetition"]} | {", ".join(r["missed_reference_FAIL"]) or "无"} | {", ".join(r["reference_accepted_alarm_cases"]) or "无"} |')
    lines+=['','C重复2漏检丢失数据/状态/双响应的有限完成性，验证了旧满分指标的区分力限制；全部候选漏检一直阻塞到有限结束的输入。旧ABI没有结束标记，最后一种情况不能简单归咎于LLM。','',
            '## 形式资格与表示敏感性','', '| 诊断 | 配置 | 模式 | 原始状态 | 秒 | SMT2字节 |','|---|---|---|---|---:|---:|']
    if cal:
        for j in cal['jobs']:lines.append(f'| {j["name"]} | {j["variant"]} | {j["mode"]} | {j["status"]} | {j.get("seconds",0):.3f} | {j.get("smt2_bytes")} |')
    lines+=['','v1资格失败完整保留：它把native断言报告的末状态当成实际报警状态。v2从VCD读取active/ok失败状态，在两个模拟器逐字回放输入，比较保留的SMT输出并复现候选报警；独立参考只判定真实物理前缀，没有补造输出。恒假控制得到参考PASS（候选误报）；M02锚点得到参考FAIL（真实mutant违规）。','',
            '输出裁剪提高恒真和B复位性质的可判定性，但让C已知稳定性性质超时；不能声称更小SMT锥必然更快。下表为固定源候选、同深度/时限、交错顺序的另一形式配置，不改旧473TIMEOUT，也不是新的模型效果试验。','',
            '| 组 | 重复 | BMC24 | prove | activation cover |','|---|---:|---|---|---|']
    for r in summary['formal_profiles']:
        m=r['by_mode'];lines.append(f'| {r["arm"]} | {r["repetition"]} | {m["bmc"]} | {m["prove"]} | {m["cover"]} |')
    lines+=['','TIMEOUT/UNKNOWN/ERROR保留；归纳失败不是可达DUT反例。单槽prove仅涉及该性质、固定实现和假设；cover不证明正确性。','',
            '## 新接口的可运行离线准备','', 'observer_contract_v3_draft.md与controller_monitor_done.py新增只读trace_done，仅最终post置1，不改DUT输入、不添时钟。4个基础设施控制验证marker时序和最终未接收请求可见；它们不是实验LLM候选，也不是新的GPT参考checker。现有Claude函数/规格保持原样。将来短形式检查的trace_done=0安全性投影不能证明有限完成性。新live继续关闭。','',
            '## 复现与限制','', '复现本完整离线流程（新目录，包含新的本地形式运行）：','', '```sh', '.venv/bin/python -B test2/scripts/controller_offline_pipeline.py --output test2/results/offline-reproduction-NEW --formal all','```','',
            '本次入口可显式复用已完成的本轮formal证据；completion.json记录“新控制/回放”与“保存formal证据”分别来自哪里。所有工具版本、源哈希、未覆盖点、原始日志、失败及资源在目录中。不要把离线回放当成新模型重复，或将合成义务/等价类当RTL覆盖。','',
            '研究结论仍受一个已检查IP家族、3次生成重复、无token匹配placebo、满分语料和求解表示/墙钟敏感性限制。原模拟B/C首轮11/11、C tokens+6.919%；原短形式信号是描述性的。当前尚无整套monitor完整soundness证明，未来新增付费研究需另行具体登记与授权。']
    (out/'report.md').write_text('\n'.join(lines)+'\n');return summary


def execute(out,formal,calibration_path=None,balanced_path=None):
    out=out.resolve();out.mkdir(parents=True,exist_ok=False);started=time.perf_counter()
    dump(out/'invocation.json',dict(argv=sys.argv,registration_sha256=sha(REG),formal=formal,API_calls=0,independent_model_trials=0))
    sources={p.name:p for p in (BASE/'scripts').glob('controller_*.py') if p.name in ('controller_offline_pipeline.py','controller_obligations.py','controller_physical_witness.py','controller_formal_diagnostic.py','controller_monitor_done.py')}
    for name,p in sources.items():(out/'sources').mkdir(exist_ok=True);(out/'sources'/name).write_bytes(p.read_bytes())
    audit_data=audit(out/'audit',True)
    controls=prepare(out/'controls')
    if controls['status']!='passed':raise ValueError('Control/reference labels disagree')
    matrix=evaluate(RUN,out/'controls',out/'candidate-replay');marker=marker_qualification(out/'end-marker')
    cal=balanced=None
    if formal=='all':
        cal=calibration(RUN,out/'formal-calibration')
        if cal['status']=='passed':balanced=balanced_correct(RUN,out/'formal-calibration',out/'balanced-correct')
    elif formal=='reuse':
        if calibration_path is None or balanced_path is None:raise ValueError('Explicit completed formal paths required')
        cal=json.loads((calibration_path/'summary.json').read_text());balanced=json.loads((balanced_path/'summary.json').read_text())
        if cal['status']!='passed' or len(balanced['jobs'])!=108:raise ValueError('Saved formal qualification incomplete')
        verify_formal_evidence(calibration_path,cal);verify_formal_evidence(balanced_path,balanced,True)
        dump(out/'reused-formal-evidence.json',dict(calibration=str(calibration_path),calibration_sha256=sha(calibration_path/'summary.json'),balanced=str(balanced_path),balanced_sha256=sha(balanced_path/'summary.json'),new_formal_jobs_in_this_invocation=0))
    s=report(out,audit_data,out/'controls',matrix,cal,balanced,marker);integrity()
    dump(out/'completion.json',dict(status='completed' if balanced else 'partial_no_balanced_formal',wall_seconds=time.perf_counter()-started,API_calls=0,summary_sha256=sha(out/'summary.json'),report_sha256=sha(out/'report.md'),old_scores_unchanged=True,formal_mode=formal))
    print(json.dumps(dict(status='completed' if balanced else 'partial',wall_seconds=time.perf_counter()-started,summary=s),indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--formal',choices=['all','reuse','skip'],default='all');p.add_argument('--calibration',type=Path);p.add_argument('--balanced',type=Path);a=p.parse_args()
    execute(a.output,a.formal,a.calibration.resolve() if a.calibration else None,a.balanced.resolve() if a.balanced else None)
