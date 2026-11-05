"""External trace hook inspects frozen checker state; never edits its source."""
import argparse
import copy
import json
import sys
from pathlib import Path
from evaluate_spi_checker_candidate import load_candidate
from run_midterm_fixed import ROOT,sha
from wbxbar_experiment import CANDIDATE,BASE


def diagnose(packet,output):
    auth=json.loads((CANDIDATE/'authorship.json').read_text())
    source=CANDIDATE/'checker.py'
    if sha(source)!=auth['artifact_sha256']['checker.py']:raise ValueError('Checker changed')
    checker=load_candidate(source)['check_rows'];cases={}
    mapping=json.loads((packet/'private-case-map.json').read_text())
    for alias,name in mapping.items():
        path=ROOT/name;rows=json.loads((path/'trace.json').read_text());snapshots=[]
        def hook(frame,event,arg):
            if event=='call' and frame.f_code.co_filename==str(source) and frame.f_code.co_name=='fail':
                local=frame.f_locals;parent=frame.f_back.f_locals
                if local.get('cat')=='routing_payload':
                    snapshots.append({'cycle':local['c'],'diagnostic':local['d'],
                        'state':copy.deepcopy({k:parent[k] for k in ['mq','ab','sq','s','we','a','sel','d','cands','tc','amb'] if k in parent})})
            return hook
        previous=sys.gettrace()
        try:sys.settrace(hook);result=checker(copy.deepcopy(rows))
        finally:sys.settrace(previous)
        if result!=json.loads((path/'result.json').read_text())['checker']:raise ValueError('Tracing changed output')
        for snap in snapshots:
            state=snap['state'];mask=sum(255<<(8*i) for i in range(4) if state['sel']>>i&1);matches=[]
            for collection in ['mq','ab']:
                for master,entries in enumerate(state[collection]):
                    for index,entry in enumerate(entries):
                        if entry['sl']==state['s'] and entry['a']==state['a'] and entry['we']==state['we'] and entry['sel']==state['sel'] and (not state['we'] or (entry['d']&mask)==(state['d']&mask)):
                            matches.append({'collection':collection,'master':master,'index':index,**entry})
            snap['all_identity_matches']=matches
            c=snap['cycle'];snap['pin_window']=[r for r in rows if c-3<=r['cycle']<=c+1]
        cases[alias]={'trace_sha256':sha(path/'trace.json'),'checker_output_unchanged':True,'routing_snapshots':snapshots}
    if sha(source)!=auth['artifact_sha256']['checker.py']:raise ValueError('Checker drift')
    controls=json.loads((BASE/'controls-v7/private-inputs.json').read_text())
    w=controls['positive/masked_write_bytes']
    correction={'masked_write_accept_data':w[8]['pre']['i_mdata'],'masked_write_forward_data':w[10]['pre']['o_sdata'],
        'reset_note':'Reset clears mq/ab/sq and the current ambiguity flag. The accumulated unresolved list is not cleared; the review sentence saying earlier unresolved observations were cleared is imprecise.'}
    output.mkdir(parents=True,exist_ok=False)
    result={'mode':'read_only_checker_state_attribution','checker_sha256':sha(source),
        'new_model_calls':0,'new_simulations':0,'cases':cases,'review_prose_corrections':correction,
        'limits':'Identity matches in internal checker queues do not prove DUT conformance or authorize searching/reordering queues in a repaired checker. No normative rule or frozen verdict is changed.'}
    (output/'state.json').write_text(json.dumps(result,indent=2)+'\n')
    for alias,c in cases.items():print(json.dumps({'case':alias,'failures':[{'cycle':s['cycle'],'matches':s['all_identity_matches']} for s in c['routing_snapshots']]}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();diagnose(a.packet.resolve(),a.output.resolve())
