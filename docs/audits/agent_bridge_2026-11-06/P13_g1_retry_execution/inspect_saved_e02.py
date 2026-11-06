"""Read-only saved-evidence analysis. No project code, tool, or test is executed."""
import bisect
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import time

OWN=Path(__file__).resolve().parent
ROOT=OWN.parents[3]
PACKET=OWN/'phase-packet.json'
EXPECTED_PACKET='2161cd4803adfbdef067d5fb4af4905d6d9de79360ea59d8a8a7afc1bde9dde6'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,d):
    with Path(p).open('x') as f:json.dump(d,f,ensure_ascii=False,indent=2)

def parse_vcd(path):
    """Independent bounded VCD reader for the saved scalar/binary-vector traces."""
    scope=[];symbols={};widths={};state={};states={};tick=0;body=False
    lines=Path(path).read_text().splitlines()
    for line in lines:
        line=line.strip()
        if not body:
            parts=line.split()
            if line.startswith('$scope'):scope.append(parts[2])
            elif line.startswith('$upscope'):scope.pop()
            elif line.startswith('$var'):
                widths[parts[3]]=int(parts[2]);symbols['.'.join(scope+[parts[4]])]=parts[3]
            elif line.startswith('$enddefinitions'):body=True
            continue
        if line.startswith('#'):
            states[tick]=state.copy();tick=int(line[1:])
        elif line and line[0] in 'bB':
            bits,symbol=line[1:].split();width=widths[symbol]
            state[symbol]=bits.lower().rjust(width,bits[0].lower() if bits[0].lower() in 'xz' else '0')
        elif line and line[0].lower() in '01xz':state[line[1:]]=line[0].lower()
    states[tick]=state.copy()
    times=sorted(states)
    def at(t,name):
        assert times[0]<=t<=times[-1],('OUT_OF_RECORDED_SPAN',t)
        return states[times[bisect.bisect_right(times,t)-1]][symbols[name]]
    return times,states,symbols,at

def main():
    started=time.monotonic();assert sha(PACKET)==EXPECTED_PACKET
    packet=read(PACKET);audit=(ROOT/packet['producer_phase']).parent;snap=audit/'snapshot'
    mismatches=[];bindings=[]
    def check(p,expected,kind):
        actual=sha(p) if Path(p).is_file() else None
        row=dict(path=str(p),expected=expected,actual=actual,kind=kind);bindings.append(row)
        if actual!=expected:mismatches.append(row)
    for k in ['producer_phase','producer_manifest','execution_receipt','current_pool']:
        check(ROOT/packet[k],packet[k+'_sha256'],k)
    manifest=read(ROOT/packet['producer_manifest'])
    for rel,expected in manifest['files'].items():
        check(audit/rel,expected,'sealed_member')
        if rel.startswith('snapshot/'):check(ROOT/rel[len('snapshot/'):],expected,'current_vs_snapshot')
    regpath='test2/configs/g1_qualification_registration_v3.json'
    reg=read(snap/regpath)
    check(snap/regpath,packet['registration_sha256'],'registration')
    check(snap/reg['source_manifest'],packet['source_manifest_sha256'],'source_manifest')
    sources=read(snap/reg['source_manifest'])['files']
    for rel,expected in sources.items():
        sealed=snap/rel
        if not sealed.exists():sealed=ROOT/rel # R03 checklist is sealed in its original package root.
        check(sealed,expected,'sealed_source');check(ROOT/rel,expected,'current_source')
    pre=read(audit/'pre-entry.json')
    for rel,expected in pre['protected_files'].items():check(ROOT/rel,expected,'protected')
    oldaudit=ROOT/'docs/audits/producer_test2_g1_R03_2026-11-06'
    check(oldaudit/'snapshot-manifest.json',packet['R03_manifest_sha256'],'R03_manifest')
    for rel,expected in read(oldaudit/'snapshot-manifest.json')['files'].items():check(oldaudit/rel,expected,'R03_member')
    gate=read(snap/packet['execution_receipt']);review=read(snap/gate['p12_review_path'])
    check(snap/gate['p12_review_path'],packet['P12_review_sha256'],'P12_review')
    assert review['status']=='PASS_WITH_LIMITS' and review['phase'].startswith('P12')
    assert review['input_identity']['producer_manifest_sha256']==gate['preparation_manifest_sha256']==packet['R03_manifest_sha256']
    for k in ['registration_sha256','source_manifest_sha256','continuation_decision_sha256']:
        assert packet[k]==gate[k]==review['input_identity'][k]
    assert gate['predecessor_pool_sha256']==packet['predecessor_pool_sha256']
    assert gate['user_authorization_sha256']==packet['original_grant_sha256']
    for key in ['predecessor_pool','user_authorization','continuation_decision']:
        check(snap/reg[key],reg[key+'_sha256'],'lineage')
    old=read(snap/reg['predecessor_pool']);assert old['halted'] and old['completed']
    result=snap/reg['result_root'];pool=read(result/'execution-state.json');report=read(result/'report.json')
    assert pool['halted'] and pool['completed'] and pool['halt_reason']=='Unqualified:PHYSICAL_EXPECTED_MISMATCH:a'
    assert pool['prior_reserved']==old['reserved'] and pool['prior_conservative_charge_seconds']==2 and pool['current_attempt_window_seconds']==1198
    for rel,expected in read(result/'result-manifest.json')['files'].items():check(result/rel,expected,'raw_result_member')
    plan=read(snap/reg['job_plan'])['jobs'];by_id={j['id']:j for j in plan};receipts=[]
    assert len(plan)==89 and Counter(x['status'] for x in report['jobs'].values())=={'RETURNED':13,'NOT_RUN':76}
    assert [e['job_id'] for e in pool['events']]==[j['id'] for j in plan[:13]]
    recomputed=Counter();workdeadline=pool['start_monotonic']+1193
    for event in pool['events']:
        jid=event['job_id'];folder=result/'jobs'/jid;receipt=read(folder/'receipt.json');job=by_id[jid]
        for k,v in receipt.items():assert event[k]==v,('RECEIPT_EVENT_MISMATCH',jid,k)
        assert receipt['status']=='RETURNED' and receipt['exit_code']==0 and receipt['root_exit_knownness']=='KNOWN_FROM_CLEANUP_WAIT'
        assert not receipt['timed_out'] and not receipt['mandatory_errors'] and not receipt['cleanup_group_kill']
        assert receipt['owned_group_probe']=='ABSENT_AT_OWNED_PROBE_NOT_A_CENSUS'
        assert receipt['process_group']>0 and receipt['dispatch_attempted']
        inv=receipt['inventory'];assert inv['mode']=='owned_process_group_only' and inv['attempts']==0 and inv['complete'] is False and receipt['child_pid_inventory_complete'] is False
        assert inv['predecessor_pool_sha256']==packet['predecessor_pool_sha256']
        assert receipt['absolute_job_deadline']==min(event['absolute_job_start']+reg['caps'][job['kind']+'_timeout'],workdeadline)
        assert 0<receipt['elapsed_seconds_including_cleanup']<reg['caps'][job['kind']+'_timeout']
        assert receipt['remaining_at_last_dispatch_check']>.25
        expanded=[x.replace('{ROOT}',str(ROOT)).replace('{OUT}',str(ROOT/reg['result_root'])).replace('{JOB}',str(ROOT/reg['result_root']/'jobs'/jid)) for x in job['argv']]
        assert receipt['argv']==expanded
        assert not any(x=='/bin/ps' for x in receipt['argv'])
        for stream in ['stdout','stderr']:check(folder/(stream+'.log'),receipt[stream+'_sha256'],'raw_log')
        recomputed[job['kind']]+=1;recomputed['physical_cycles']+=job.get('cycles',0)
        receipts.append(dict(job_id=jid,kind=job['kind'],argv=receipt['argv'],exit_code=0,status=receipt['status'],root_exit_knownness=receipt['root_exit_knownness'],elapsed_seconds=receipt['elapsed_seconds_including_cleanup'],deadline=receipt['absolute_job_deadline'],process_group=receipt['process_group'],inventory_complete=False,owned_group_probe=receipt['owned_group_probe'],receipt_sha256=sha(folder/'receipt.json')))
    assert dict(recomputed)==pool['attempt_reserved']
    assert {k:pool['prior_reserved'][k]+recomputed[k] for k in pool['reserved']}==pool['reserved']
    assert pool['reserved']==packet['cumulative_reserved']
    for k in ['compile','native','physical','setup']:
        assert pool['reserved'][k]<=reg['caps'][k+'_jobs']
        assert pool['remaining'][k]==reg['caps'][k+'_jobs']-pool['reserved'][k]
    assert pool['reserved']['physical_cycles']==4 and pool['remaining']['physical_cycles']==1020
    assert pool['total_elapsed_seconds']<1198 and pool['cumulative_charged_window_seconds']<1200
    for jid in ['QC00-bmc','QC00-cover']:
        args=by_id[jid]['argv'];assert args[args.index('-t')+1]=='8'
        text=(result/'jobs'/jid/'stdout.log').read_text()+(result/'jobs'/jid/'stderr.log').read_text()
        assert re.findall(r'Status:\s*(PASSED|FAILED)',text)==['PASSED']
    assert 'Reached cover statement in step 2' in (result/'jobs/QC00-cover/stdout.log').read_text()
    assert '-c' in by_id['QC00-cover']['argv'] and '-c' not in by_id['QC00-bmc']['argv']
    text=(result/'jobs/QC00-icarus/stdout.log').read_text();rows=[]
    for line in text.splitlines():
        if line.startswith('OBS '):
            row=dict(x.split('=',1) for x in line.split()[1:])
            for k in ['qc','cycle','tick']:row[k]=int(row[k])
            rows.append(row)
    assert len(rows)==8 and 'END qc=0 cycles=4 posedges=4' in text
    labels=read(snap/reg['controls'])['cases'];expected=labels[0]['physical_rows_expected_icarus']
    assert labels[0]['native_BMC_expected']==labels[0]['activation_cover_expected']=='PASS'
    mismatched_values=[]
    for i,(row,exp) in enumerate(zip(rows,expected)):
        for k,v in exp.items():
            if row[k]!=v:mismatched_values.append(dict(row=i,cycle=row['cycle'],phase=row['phase'],field=k,expected=v,observed=row[k]))
    assert len(mismatched_values)==14 and {m['cycle'] for m in mismatched_values}=={0}
    times,states,symbols,at=parse_vcd(result/'jobs/QC00-icarus/trace.vcd')
    assert (times[0],times[-1])==(0,16000)
    fields={k:'physical_tb.'+k for k in ['a','b','rst','en','valid','marker']}
    fields.update({k:'physical_tb.units[0].u.'+k for k in ['q','active','ok']})
    waveform_differences=[]
    for i,row in enumerate(rows):
        for k,symbol in fields.items():
            if at(row['tick'],symbol)!=row[k]:waveform_differences.append(dict(row=i,field=k,vcd=at(row['tick'],symbol),stdout=row[k]))
        assert at(row['tick'],'physical_tb.obs_phase')==('0' if row['phase']=='pre' else '1')
        assert int(at(row['tick'],'physical_tb.step'),2)==row['cycle']
    assert not waveform_differences
    clock_id=symbols['physical_tb.clk'];prior=None;posedges=[]
    for t in times:
        value=states[t].get(clock_id)
        if prior=='0' and value=='1':posedges.append(t)
        if value is not None:prior=value
    assert posedges==[2000,6000,10000,14000]
    changes=[];prior=None
    for t in times:
        value=states[t].get(symbols['physical_tb.step'])
        if value!=prior:changes.append(dict(tick=t,step=value));prior=value
    assert changes==[dict(tick=0,step='000'),dict(tick=4000,step='001'),dict(tick=8000,step='010'),dict(tick=12000,step='011')]
    assert at(0,'physical_tb.a')=='xxxx' and at(3999,'physical_tb.a')=='xxxx' and at(4000,'physical_tb.a')=='1111'
    cv_times,cv_states,cv_symbols,cv_at=parse_vcd(result/'jobs/QC00-cover/trace.vcd')
    cover_samples=[dict(tick=t,**{k:cv_at(t,'formal_top.'+k) for k in ['a','b','rst','en','valid','q','active','ok','cycle','sampled_cycle','sampled_active','sampled_ok']}) for t in cv_times if t%10==0]
    assert cover_samples[0]['a']=='0000' and cover_samples[0]['rst']=='1'
    assert any(x['sampled_active']=='1' and x['sampled_ok']=='1' for x in cover_samples)
    matrix=[]
    for n,case in enumerate(labels):
        matrix.append(dict(qc=case['id'],declared_eligibility=case['eligibility'],paper_exclusion_not_observed=n in [7,12,13,14,15],BMC='PASS_DEPTH8' if n==0 else 'NOT_RUN',cover='REACHED_STEP2' if n==0 else 'NOT_RUN',icarus='REJECTED_CYCLE0_UNKNOWN_INPUTS' if n==0 else 'NOT_RUN',verilator='NOT_RUN',accepted_rows=0,full_qualification=False,completion128_credit=False))
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    index=subprocess.check_output(['git','--no-optional-locks','ls-files','--stage','-z'],cwd=ROOT)
    index_sha=hashlib.sha256(index).hexdigest();assert index_sha==pre['index_entries_sha256']
    assert not mismatches
    write(OWN/'input-verification.json',dict(actual_HEAD=head,packet_sha256=sha(PACKET),sealed_members=len(manifest['files']),source_bindings=len(sources),protected_files=len(pre['protected_files']),R03_members=len(read(oldaudit/'snapshot-manifest.json')['files']),index_sha256=index_sha,bindings=bindings,mismatches=mismatches,elapsed_seconds=time.monotonic()-started))
    write(OWN/'raw-analysis.json',dict(resources=dict(attempt=dict(recomputed),cumulative=pool['reserved'],remaining=pool['remaining'],current_recorded_window_seconds=pool['total_elapsed_seconds'],prior_actual_seconds=pool['prior_actual_window_seconds'],prior_charge_seconds=2,cumulative_actual_checkpoint_seconds=pool['cumulative_actual_window_seconds'],cumulative_charged_checkpoint_seconds=pool['cumulative_charged_window_seconds'],attempt_checkpoint_seconds=pool['attempt_elapsed_checkpoint_seconds'],sum_root_elapsed_seconds=sum(r['elapsed_seconds'] for r in receipts)),receipts=receipts,rows=rows,label_mismatches=mismatched_values,VCD_stdout_differences=waveform_differences,VCD_span=[times[0],times[-1]],posedges=posedges,step_changes=changes,native_cover_samples=cover_samples,root_statuses=dict(Counter(x['status'] for x in report['jobs'].values())),run_report_controls=report['controls'],code_sha256={name:sha(snap/'test2/g1_v3'/name) for name in ['runtime.py','budget.py','runner.py','sources/common.sv','sources/physical_tb.sv','sources/QC00_formal.sv']},read_only_saved_evidence=True))
    write(OWN/'per-qc-review.json',dict(controls=matrix,qualified_controls=0,qualification='NOT_QUALIFIED'))
    print(json.dumps(dict(status='SAVED_EVIDENCE_CHECKS_PASS',HEAD=head,sealed=len(manifest['files']),sources=len(sources),protected=len(pre['protected_files']),root_statuses=dict(Counter(x['status'] for x in report['jobs'].values())),label_mismatches=len(mismatched_values),raw_rows=len(rows),VCD_stdout_mismatches=len(waveform_differences),actual_new_G1_tools=0)))

if __name__=='__main__':main()
