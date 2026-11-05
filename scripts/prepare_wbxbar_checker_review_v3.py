"""Fresh repair/driver review; scoped RTL excerpts are attribution-only."""
import argparse
import json
from pathlib import Path
from prepare_spi_core_checker_review import vector_pack,vector_unpack,delta,apply_delta
from prepare_wbxbar_checker_role import verify_packet
from run_midterm_fixed import ROOT,sha

BASE=ROOT/'results/wbxbar_exploratory_bc_20261104'


def prepare(output,publish=False):
    role=BASE/'claude-v3';candidate=role/'candidate';packet=BASE/'spec-packet-v1'
    verify_packet(packet)
    auth=json.loads((candidate/'authorship.json').read_text())
    for name,digest in auth['artifact_sha256'].items():
        if sha(candidate/name)!=digest:raise ValueError('Checker hash changed')
    evaluation=json.loads((BASE/'evaluation-v8/summary.json').read_text())
    driver_eval=json.loads((BASE/'driver-evaluation-v2/summary.json').read_text())
    driver_summary=json.loads((BASE/'driver-v1/summary.json').read_text())
    for record in (evaluation,driver_eval,driver_summary):
        for path,digest in record['hashes'].items():
            if sha(Path(path))!=digest:raise ValueError('Evidence drift: '+path)
    traces=json.loads((BASE/'controls-v7/private-inputs.json').read_text())
    chosen=['pending_prefix','contended_burst','error_burst_restart','reset_pending_restart',
            'isolated_m0_d2_w0','burst_m1_d1_n7']
    for name in chosen:traces['driver/'+name]=json.loads((BASE/'driver-v1'/name/'verilator/trace.json').read_text())
    first=next(iter(traces.values()))[0];columns=[(kind,name) for kind in ('pre','post') for name in first[kind]]
    packed={};changes={}
    metadata={c['name']:c for c in json.loads((BASE/'controls-v7/manifest.json').read_text())['controls']}
    for name,rows in traces.items():
        if metadata.get(name,{}).get('baseline'):continue
        padded=[{**r,'action':{}} for r in rows]
        packed[name]=vector_pack(padded,columns)
        if vector_unpack(packed[name],columns)!=padded:raise ValueError('Trace packing changed data')
    for name,rows in traces.items():
        parent=metadata.get(name,{}).get('baseline')
        if not parent:continue
        baseline=vector_unpack(packed[parent],columns)
        padded=[{**r,'action':{}} for r in rows]
        d=delta(baseline,padded)
        if apply_delta(baseline,d)!=padded:raise ValueError('Delta changed data')
        changes[name]={'base':parent,**d}
    def brief(record):
        return {name:{'verdict':r.get('verdict'),'failures':r.get('failures',[])[:3],
             'failure_total':len(r.get('failures',[])),'assumption_violations':r.get('assumption_violations',[])[:3],
             'assumption_total':len(r.get('assumption_violations',[])),'unresolved':r.get('unresolved',[])[:3],
             'unresolved_total':len(r.get('unresolved',[])),'infrastructure_error':r.get('infrastructure_error')}
             for name,r in record['cases'].items()}
    body={'role':'Fresh independent read-only reviewer; no artifact modifications.',
        'task':'Assess repaired checker and fixed offer-driver evidence. Return ready_for_offline_gate, findings, limitations. A detected genuine DUT violation does not imply a bad checker/testbench; separate specification violation, checker false positive, driver error and unresolved attribution. Do not authorize B/C automatically; final reachability/prompt/hash freeze is separate.',
        'specification':json.loads((packet/'packet.json').read_text()),
        'previous_findings':[{k:r[k] for k in ('id','severity','topic')} for r in json.loads((BASE/'claude-v2/review.json').read_text())['findings']],
        'candidate':{name:(candidate/name).read_text() for name in auth['artifact_sha256']},
        'checker_controls':json.loads((BASE/'controls-v7/manifest.json').read_text())['controls'],
        'control_accounting':evaluation['controls'],'selftests':evaluation['selftests'],
        'checker_evaluations':brief(evaluation),'driver_evaluations':brief(driver_eval),
        'driver':{'source':(ROOT/'scripts/wbxbar_exploratory_driver.py').read_text().split('def compile_driver(')[0],
                  'source_scope':'Exact generator and Python transport parser. Build and case-generation helpers omitted; standalone compiled SV and evidence are supplied.',
                  'compiled_sv':(BASE/'driver-v1/compiled/tb_natural_inventory.sv').read_text(),
                  'boundary':'Same original public ports/parameters/denominator. One action is one physical cycle. Per-master offer queues; hold STB/payload until sampled acceptance. CYC persists for outstanding work. On sampled ERR discard remaining accepted work and keep unaccepted offers, with one counted low-CYC gap. Reset discards pending/queued work. No hidden drains. Cumulative-prefix replay preserves pins.',
                  'preflight':{k:driver_summary[k] for k in ('status','executions','executed_cycles','raw_denominator')},
                  'transport_cases':[r for r in driver_summary['cases'] if r['case'] in chosen],
                  'unit_checks':'Six tests pass: pending prefix remains incomplete, aborted/reset requests not counted as responses, counted CYC gap, mutated abort input rejected, reset+offer rejected, exact prefix pin replay.'},
        'traces':{'columns':columns,'encoding':'first is complete vector; each [repeat, [[index,value],...]] applies updates repeat times, one new cycle each time. Other values persist. For deltas, decode base then truncate to length, apply listed pre/post field updates at index. Empty action is packing-only. Every vector/delta roundtrip checked.',
                  'values':packed,'deltas':changes,'disclosure':'All 46 independent hand controls and 6 selected driver traces included losslessly. Diagnostics supplied for all 44 old and all 48 new DUT observations; unshown traces are not independently reread by this reviewer.'},
        'prior_attribution': 'Previous independent review classified the matching buffered forward after master abort as unresolved public abort-propagation timing. This review supplies exact public-pin traces; no executable DUT or additional timing assumption is needed to audit identity conservation. Original DUT remains unchanged.',
        'questions':[
            'Independently audit v3 abort identity repair: only unique oldest matching aborted-unforwarded identity may justify later forwarding as unresolved. Consume identity once. No arbitrary grace period, payload/address relaxation or completion credit.',
            'Review four new boundary controls: duplicate old forwarding must fail, reset must erase old identity, earlier unresolved observation must persist across reset, and competing live/aborted identities must remain unresolved. Hand control timing is a fixture, not a DUT latency rule. Negatives whose baseline is unresolved are not credited in ordinary mutation sensitivity; report their raw detection separately.',
            'Confirm F1 unexplained mapped ERR and F6 SEL masking fixes remain valid. All 16 hand positives and 44 ordinary DUT observations are clean. Actual error_burst_restart is now unresolved post_abort_forward at14, not DUT violation or scoped_pass; pending_prefix remains unresolved. Validate from source and supplied traces, not from this summary alone.',
            'Review driver protocol and accounting, including pending prefix, error/reset discard, pre-edge sampling and no free drains. Exact template/generator hashes will be frozen. No slave-stall coverage is claimed.',
            'If a blocker remains, identify the concrete property and control. Otherwise state limited readiness and residual exclusions; full IP correctness and experiment readiness are separate.'],
        'isolation':'Reviewer receives checker/driver implementation and public-pin observations; no executable DUT is supplied in this repair review. Original checker author/patch role received no executable DUT or DUT traces. Neither role receives equivalence groups, source coverage targets, LLM stimulus or B/C outcomes.'}
    prefix='Read-only independent checker/driver audit. Do not modify artifacts. Return JSON with ready_for_offline_gate, findings, limitations. Check event false positives, independent controls, spec justification and isolation. No claim of formal proof.\n'
    size=len((prefix+json.dumps(body)).encode())
    if size>150000:raise ValueError('Review byte cap: '+str(size))
    output.mkdir(parents=True,exist_ok=False)
    (output/'packet.json').write_text(json.dumps(body,indent=2)+'\n')
    (output/'manifest.json').write_text(json.dumps({'bytes':size,'roundtrips':len(traces),
        'packet_sha256':sha(output/'packet.json'),'script_sha256':sha(Path(__file__))},indent=2)+'\n')
    if publish:
        target=role/'review-packet.json'
        if target.exists():raise ValueError('Review already published')
        tmp=role/'review-packet.pending';tmp.write_text(json.dumps(body,separators=(',',':'))+'\n');tmp.rename(target)
    print(json.dumps({'bytes':size,'roundtrips':len(traces),'published':publish}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--publish',action='store_true');a=p.parse_args()
    prepare(a.output.resolve(),a.publish)
