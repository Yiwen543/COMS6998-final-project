"""Evaluate independent controls and prepare a fresh review without live-pilot traces."""
import argparse
import copy
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from prepare_wbxbar_cancel_contract import BASE,OLD,REG,FILES,verify_registration,verify_packet,PRIOR
from prepare_spi_core_checker_review import vector_pack,vector_unpack,delta,apply_delta


def candidate_hashes(candidate):
    auth=json.loads((candidate/'authorship.json').read_text())
    for f in FILES:
        if sha(candidate/f)!=auth['artifact_sha256'][f]:raise ValueError('Candidate drift: '+f)
    return auth


def worker(candidate,inputs,output):
    candidate_hashes(candidate);output.mkdir(parents=True,exist_ok=False)
    inp=output/'inputs.json';inp.write_text(json.dumps(inputs,separators=(',',':'))+'\n')
    command=[sys.executable,'-I',str(ROOT/'scripts/evaluate_spi_checker_candidate.py'),'--worker',
             '--candidate',str(candidate),'--inputs',str(inp),'--output',str(output/'evaluations.json')]
    env={k:v for k,v in os.environ.items() if not any(x in k for x in ('KEY','TOKEN','SECRET','PASSWORD'))}
    with tempfile.TemporaryDirectory(prefix='wbxbar-cancel-eval-') as cwd:
        r=subprocess.run(command,cwd=cwd,env=env,capture_output=True,text=True,timeout=60)
    (output/'worker.log').write_text(r.stdout+r.stderr)
    if r.returncode:raise RuntimeError('Checker worker failed; logs retained')
    return json.loads((output/'evaluations.json').read_text())


def expected_outcome(result,expected):
    if result.get('infrastructure_error') or result.get('verdict')!=expected:return False
    if expected=='input_or_scope_invalid':return bool(result.get('assumption_violations'))
    if result.get('assumption_violations'):return False
    if expected=='dut_violation':return bool(result.get('failures'))
    if result.get('failures'):return False
    if expected=='unresolved':return bool(result.get('unresolved'))
    return expected=='scoped_pass' and not result.get('unresolved')


def evaluate(candidate,output):
    verify_registration();candidate_hashes(candidate)
    controls=BASE/'controls-v1';m=json.loads((controls/'manifest.json').read_text())
    if sha(controls/'private-inputs.json')!=m['inputs_sha256']:raise ValueError('Control drift')
    data=json.loads((controls/'private-inputs.json').read_text())
    r=worker(candidate,data,output)
    previous=json.loads((OLD/'evaluation-v8/summary.json').read_text())['cases']
    accounts=[]
    for entry in m['historical_controls']+m['new_controls']:
        name=entry['name'];new='expected' in entry
        expected=entry['expected'] if new else previous[name]['verdict']
        actual=r['cases'][name];baseline=entry.get('baseline')
        baseline_result=r['cases'].get(baseline) if baseline else None
        clean_baseline=bool(baseline_result and expected_outcome(baseline_result,'scoped_pass'))
        accounts.append({'name':name,'expected':expected,'actual':actual.get('verdict'),
            'pass':expected_outcome(actual,expected),'new':new,'baseline':baseline,
            'clean_baseline':clean_baseline,'credited_mutation_detection':expected=='dut_violation' and clean_baseline and expected_outcome(actual,'dut_violation'),
            'unresolved_baseline_detection':expected=='dut_violation' and bool(baseline_result and baseline_result.get('verdict')=='unresolved') and expected_outcome(actual,'dut_violation')})
    summary={'checker_sha256':sha(candidate/'checker.py'),'candidate':str(candidate.relative_to(ROOT)),
        'controls_sha256':sha(controls/'manifest.json'),'accounts':accounts,'selftests':r['selftests'],'worker_errors':r['errors'],
        'pass':not r['errors'] and bool(r['selftests']) and all(x['pass'] for x in r['selftests']) and all(x['pass'] for x in accounts),
        'counts':{'controls':len(accounts),'passed':sum(x['pass'] for x in accounts),
                  'new':sum(x['new'] for x in accounts),'clean_baseline_detections':sum(x['credited_mutation_detection'] for x in accounts),
                  'unresolved_baseline_detections':sum(x['unresolved_baseline_detection'] for x in accounts)},
        'limitations':'Proposed labels require source-based independent review. No actual DUT or live-pilot trace is treated as golden. No new simulation/model call.'}
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');return summary


def review_packet(candidate,evaluation,output,publish=False):
    verify_registration();verify_packet(BASE/'spec-packet-v1',PRIOR);candidate_hashes(candidate)
    summary=json.loads((evaluation/'summary.json').read_text())
    if summary['checker_sha256']!=sha(candidate/'checker.py'):raise ValueError('Evaluation checker mismatch')
    evaluated=json.loads((evaluation/'evaluations.json').read_text());inputs=json.loads((evaluation/'inputs.json').read_text())
    controls=json.loads((BASE/'controls-v1/private-inputs.json').read_text())
    if inputs!=controls:raise ValueError('Evaluation inputs differ')
    columns=[(kind,k) for kind in ('pre','post') for k in next(iter(inputs.values()))[0][kind]]
    packed={};decoded={}
    for name,rows in inputs.items():
        full=[{**r,'action':{}} for r in rows];best={'vector':vector_pack(full,columns)}
        if vector_unpack(best['vector'],columns)!=full:raise ValueError('Packing differs')
        # Choose a smaller lossless delta against an earlier trace. This changes
        # representation only; every pin, cycle and diagnostic remains available.
        for prior,base in decoded.items():
            if len(base)<len(full):continue
            d=delta(base,full);option={'base':prior,'delta':d}
            if len(json.dumps(option))<len(json.dumps(best)):
                if apply_delta(base,d)!=full:raise ValueError('Delta differs')
                best=option
        packed[name]=best;decoded[name]=full
    body={'role':'Fresh independent contract/checker reviewer; no editing or tools.',
        'task':'Audit normative contract and revision. Return ready_for_offline_gate as a boolean, findings and limitations. A false positive, weakened ordinary check, invented abort timing, invalid control, or unsupported classification is a blocker. Explicitly assess complete vs unresolved status and evidence persistence. This review cannot authorize new stimulus generation.',
        'specification':json.loads((BASE/'spec-packet-v1/packet.json').read_text())['specification'],
        'candidate':{f:(candidate/f).read_text() for f in FILES},
        'controls':json.loads((BASE/'controls-v1/manifest.json').read_text()),
        'evaluation':summary,'checker_results':{n:{k:r.get(k) for k in ('verdict','failures','assumption_violations','unresolved','infrastructure_error')} for n,r in evaluated['cases'].items()},
        'traces':{'columns':columns,'encoding':'Decode in listed order. A vector first defines a complete row; [repeat,changes] updates indexed fields repeat times, producing a row each cycle. A delta references an earlier decoded base: truncate to length, then apply pre/post field updates at each index. All unmentioned fields persist. Empty action is a placeholder. All 69 complete traces were losslessly round-trip checked; no rows or fields omitted.','values':packed},
        'questions':['Is cancellation behavior distinguished from normal live-request ordering and from reset? Are all inferred assumptions marked rather than asserted as normative rules?',
                     'Do a non-head old identity, multiple partial cancellations, same-edge acceptance/ERR, duplicate consumption and indistinguishable owners receive sound classifications? Matching old work is not evidence of correct cancellation.',
                     'Are all old known-clean positives and clean-baseline mutation controls preserved? Unresolved-baseline faults are separately counted; reject a wrong expected label rather than forcing the checker to fit.',
                     'Are contract.md and properties.json consistent with executable checks and actual unresolved exclusions? Public text does not establish exact cancellation or timeout latency.'],
        'isolation':'No executable DUT, real DUT trace, B/C prompts/trajectories, targets, semantic group, coverage or performance result. Author saw only public spec, own prior source and six synthetic examples; this reviewer sees all independent controls.'}
    prefix='Read-only independent checker/driver audit. Do not modify artifacts. Return JSON with ready_for_offline_gate, findings, limitations. Check event false positives, independent controls, spec justification and isolation. No claim of formal proof.\n'
    size=len((prefix+json.dumps(body)).encode())
    if size>150000:raise ValueError('Review byte cap: '+str(size))
    output.mkdir(parents=True,exist_ok=False)
    (output/'packet.json').write_text(json.dumps(body,indent=2)+'\n')
    (output/'manifest.json').write_text(json.dumps({'packet_sha256':sha(output/'packet.json'),'bytes':size,'roundtrips':len(inputs),'checker_sha256':sha(candidate/'checker.py'),'evaluation_sha256':sha(evaluation/'summary.json')},indent=2)+'\n')
    if publish:
        path=candidate.parent/'review-packet.json'
        if path.exists():raise ValueError('Never overwrite review packet')
        temporary=path.with_suffix('.tmp');temporary.write_text(json.dumps(body)+'\n');temporary.replace(path)
    return {'bytes':size,'roundtrips':len(inputs),'published':publish}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--candidate',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--review',type=Path);p.add_argument('--publish',action='store_true');a=p.parse_args()
    if a.review:result=review_packet(a.candidate.resolve(),a.review.resolve(),a.output.resolve(),a.publish)
    else:
        r=evaluate(a.candidate.resolve(),a.output.resolve());result={k:r[k] for k in ('pass','counts')};result['failed']=[x['name'] for x in r['accounts'] if not x['pass']]
    print(json.dumps(result,indent=2))
