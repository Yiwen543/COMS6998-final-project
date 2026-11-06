"""P15 saved-byte parsing only; no DUT, solver, simulator or tests executed."""
import ast,bisect,hashlib,json,re,subprocess
from collections import Counter
from pathlib import Path
OWN=Path(__file__).resolve().parent;ROOT=OWN.parents[3]
AUDIT=ROOT/'docs/audits/producer_test2_g1_E03_2026-11-06';SNAP=AUDIT/'snapshot'
PHASE_SHA='c7b99fd6a11a47a4204b2fb22c0f0ebb57c81bb4ca1c1ba864b57977f2601325'
MANIFEST_SHA='9511046040fb38358f1fc70bfe88742a45a5c8957a427744675c929ae1df4325'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,v):
    with Path(p).open('x') as f:json.dump(v,f,ensure_ascii=False,indent=2)
assert sha(AUDIT/'phase.json')==PHASE_SHA and sha(AUDIT/'snapshot-manifest.json')==MANIFEST_SHA
phase=read(AUDIT/'phase.json');manifest=read(AUDIT/'snapshot-manifest.json')
for rel,h in manifest['files'].items():
    assert sha(AUDIT/rel)==h,rel
    if rel.startswith('snapshot/'):assert sha(ROOT/rel[9:])==h,rel
regpath='test2/configs/g1_qualification_registration_v4.json';reg=read(SNAP/regpath)
code=SNAP/'test2/g1_v4';results=SNAP/reg['result_root'];pool=read(results/'execution-state.json');report=read(results/'report.json')
assert sha(results/'execution-state.json')=='2364e80999aaea35eb3e5da06e31d48331ee6be6b061c09bb3f92738bca8d1b8'
gatepath='docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/execute-receipt-r04.json'
assert sha(SNAP/gatepath)=='fadb3e7fd5534d63309b42c7492a8b57915025010f4832c4ca9c27a0ddcc2e7e'
gate=read(SNAP/gatepath);assert gate['p14_review_sha256']=='012373a27c68197a1baaaabf3ec67f18b1aeb16964775bfc4a6baa885cebece3'
assert sha(ROOT/gate['p14_review_path'])==gate['p14_review_sha256']
assert sha(SNAP/regpath)==gate['registration_sha256']==phase['registration_sha256']
assert sha(SNAP/reg['source_manifest'])==gate['source_manifest_sha256']
source=read(SNAP/reg['source_manifest'])['files']
for rel,h in source.items():assert sha(ROOT/rel)==h,rel
before=read(AUDIT/'before-execution.json');protected=read(ROOT/before['protected_history_manifest'])['files']
for rel,h in protected.items():assert sha(ROOT/rel)==h,rel
for rel,h in before['files'].items():assert sha(ROOT/rel)==h,rel
for rel,h in read(results/'result-manifest.json')['files'].items():assert sha(results/rel)==h,rel
assert pool['halted'] and pool['completed'] and pool['halt_reason']=='Unqualified:NATIVE_EXPECTATION_MISMATCH:QC01:cover'
plan=read(SNAP/reg['job_plan'])['jobs'];jobs={j['id']:j for j in plan}
assert [e['job_id'] for e in pool['events']]==[j['id'] for j in plan[:7]]
count=Counter();receipts=[]
for event in pool['events']:
    jid=event['job_id'];r=read(results/'jobs'/jid/'receipt.json');j=jobs[jid]
    assert all(event[k]==v for k,v in r.items())
    assert r['status']=='RETURNED' and r['exit_code']==(1 if jid in ['QC01-bmc','QC01-cover'] else 0)
    assert not r['timed_out'] and not r['mandatory_errors'] and not r['cleanup_group_kill']
    assert r['inventory']['attempts']==0 and r['inventory']['complete'] is False
    assert r['owned_group_probe']=='ABSENT_AT_OWNED_PROBE_NOT_A_CENSUS'
    assert r['root_exit_knownness']=='KNOWN_FROM_CLEANUP_WAIT'
    assert r['absolute_job_deadline']==min(event['absolute_job_start']+reg['caps'][j['kind']+'_timeout'],pool['start_monotonic']+1187)
    assert r['elapsed_seconds_including_cleanup']<reg['caps'][j['kind']+'_timeout']
    for stream in ['stdout','stderr']:assert sha(results/'jobs'/jid/(stream+'.log'))==r[stream+'_sha256']
    if j['kind']=='native':assert r['argv'][r['argv'].index('-t')+1]=='8'
    count[j['kind']]+=1;count['physical_cycles']+=j.get('cycles',0)
    receipts.append(dict(job_id=jid,kind=j['kind'],exit_code=r['exit_code'],status=r['status'],elapsed_seconds=r['elapsed_seconds_including_cleanup'],receipt_sha256=sha(results/'jobs'/jid/'receipt.json')))
count['setup']=0;assert dict(count)==pool['attempt_reserved']
assert {k:pool['prior_reserved'][k]+count[k] for k in pool['reserved']}==pool['reserved']
assert pool['reserved']=={'setup':8,'compile':6,'native':4,'physical':3,'physical_cycles':12}
assert Counter(r['status'] for r in report['jobs'].values())=={'RETURNED':7,'NOT_RUN':72}
assert pool['cumulative_charged_window_seconds']<1200
# Reuse only the independent read-only VCD helper definition from this reviewer's P13.
helper=ROOT/'docs/audits/agent_bridge_2026-11-06/P13_g1_retry_execution/inspect_saved_e02.py'
tree=ast.parse(helper.read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='parse_vcd')
namespace={'Path':Path,'bisect':bisect};exec(compile(ast.Module(body=[fn],type_ignores=[]),str(helper), 'exec'),namespace)
parse_vcd=namespace['parse_vcd'];labels=read(SNAP/reg['controls'])['cases'];physical={}
for sim in ['icarus','verilator']:
    folder=results/'jobs'/('QC00-'+sim);text=(folder/'stdout.log').read_text();rows=[]
    for line in text.splitlines():
        if line.startswith('OBS '):
            row=dict(x.split('=',1) for x in line.split()[1:])
            for k in ['cycle','tick','qc']:row[k]=int(row[k])
            rows.append(row)
    expected=labels[0]['physical_rows_expected_icarus']
    assert len(rows)==8 and all(all(row[k]==v for k,v in exp.items()) for row,exp in zip(rows,expected))
    times,states,symbols,at=parse_vcd(folder/'trace.vcd')
    assert times[0]==0 and times[-1]==16000
    for row in rows:
        for field in ['a','b','rst','en','valid','marker']:
            assert at(row['tick'],'physical_tb.'+field)==row[field]
        for field in ['q','active','ok']:assert at(row['tick'],'physical_tb.units[0].u.'+field)==row[field]
        assert at(row['tick'],'physical_tb.obs_phase')==('0' if row['phase']=='pre' else '1')
        assert int(at(row['tick'],'physical_tb.step'),2)==row['cycle']
    previous=None;edges=[]
    for t in times:
        value=at(t,'physical_tb.clk')
        if previous=='0' and value=='1':edges.append(t)
        previous=value
    assert edges==[2000,6000,10000,14000]
    physical[sim]=dict(rows=rows,posedges=edges,stdout_sha256=sha(folder/'stdout.log'),VCD_sha256=sha(folder/'trace.vcd'))
assert physical['icarus']['rows']==physical['verilator']['rows']
native={}
for mode in ['bmc','cover']:
    folder=results/'jobs'/('QC01-'+mode);log=(folder/'stdout.log').read_text()+(folder/'stderr.log').read_text()
    raw=re.findall(r'Status:\s*(PASSED|FAILED)',log);reached=[int(x) for x in re.findall(r'Reached cover statement in step (\d+)',log)]
    assert raw==['FAILED'] and 'Assert failed' in log
    times,states,symbols,at=parse_vcd(folder/'trace.vcd')
    failing=[dict(tick=t,cycle=at(t,'formal_top.sampled_cycle'),q=at(t,'formal_top.sampled_q'),active=at(t,'formal_top.sampled_active'),ok=at(t,'formal_top.sampled_ok')) for t in times if at(t,'formal_top.sampled_active')=='1' and at(t,'formal_top.sampled_ok')=='0']
    assert failing
    native[mode]=dict(raw_tool_status='FAILED',process_exit_code=1,cover_reached_steps=reached,assertion_failed=True,sampled_failures=failing,stdout_sha256=sha(folder/'stdout.log'),VCD_sha256=sha(folder/'trace.vcd'))
assert native['cover']['cover_reached_steps']==[2]
assert labels[1]['native_BMC_expected']=='FAIL' and labels[1]['activation_cover_expected']=='PASS'
native['cover']['old_runner_label']=report['jobs']['QC01-cover']['native_status'];assert native['cover']['old_runner_label']=='NOT_REACHED'
tool=Path(reg['tools']['smtbmc']['configured']);assert sha(tool)==reg['tools']['smtbmc']['resolved_sha256']
lines=tool.read_text().splitlines();excerpt='\n'.join(f'{i+1}: {lines[i]}' for i in range(1868,1981))+'\n'+'\n'.join(f'{i+1}: {lines[i]}' for i in range(2180,2185))
(OWN/'pinned-smtbmc-cover-excerpt.txt').write_text(excerpt+'\n')
index=subprocess.check_output(['git','--no-optional-locks','ls-files','--stage','-z'],cwd=ROOT);assert hashlib.sha256(index).hexdigest()==before['index_entries_sha256']
write(OWN/'saved-analysis.json',dict(seal_anchor_origin='First completed local E03 seal observed during authorized review;raw pool/EXECUTE independently match supplied hashes.',producer_phase_sha256=PHASE_SHA,producer_manifest_sha256=MANIFEST_SHA,sealed_members=len(manifest['files']),source_bindings=len(source),protected_files=len(protected),actual_HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),index_entries_sha256=hashlib.sha256(index).hexdigest(),receipts=receipts,attempt=dict(count),cumulative=pool['reserved'],remaining=pool['remaining'],current_window_seconds=pool['total_elapsed_seconds'],cumulative_actual_checkpoint=pool['cumulative_actual_window_seconds'],cumulative_charged_checkpoint=pool['cumulative_charged_window_seconds'],physical_QC00=physical,native_QC01=native,pinned_tool_source_sha256=sha(tool),pinned_tool_excerpt_sha256=sha(OWN/'pinned-smtbmc-cover-excerpt.txt'),independent_VCD_reader_sha256=sha(helper),SV_common_sha256=sha(code/'sources/common.sv'),physical_TB_sha256=sha(code/'sources/physical_tb.sv'),runner_sha256=sha(code/'runner.py'),native_reuse=report['native_prefix_reuse']['status'],real_new_jobs=0))
print(json.dumps(dict(status='PASS_SAVED_CHECKS_CLASSIFICATION_DEFECT_CONFIRMED',E03_phase=PHASE_SHA,E03_manifest=MANIFEST_SHA,sealed=len(manifest['files']),QC00_both_sim_rows_match=8,QC01_cover_reached=2,QC01_raw_status='FAILED',old_label='NOT_REACHED',new_real_jobs=0)))
