"""Classify existing cross-tool observations; never mask definite disagreements."""
import argparse
import json
from common import BASE,dump

def compare(a,b):
    binary=[];unknown=[]
    if len(a)!=len(b): raise ValueError('Trace length mismatch')
    for x,y in zip(a,b):
        if x['cycle']!=y['cycle'] or x['action']!=y['action']: raise ValueError('Stimulus mismatch')
        for phase in ('pre','post'):
            if x['cycle']==0 and phase=='pre': continue
            for key in ('fill','full','empty','data'):
                if key=='data' and x[phase]['empty']==y[phase]['empty']==1: continue
                u,v=x[phase][key],y[phase][key]
                if u!=v:
                    target=unknown if -1 in (u,v) else binary
                    target.append(dict(cycle=x['cycle'],phase=phase,signal=key,icarus=u,verilator=v))
    return dict(binary_disagreements=binary,unknown_differences=unknown)

def audit(source,out):
    results=[]
    for control in ('correct_stress','correct_original','M01','M02','M03','M04','M05','M06'):
        for case in ('basic','boundary','wrap_reset','final_boundary','final_wrap_reset','final_mixed'):
            a=json.loads((source/control/'iverilog'/case/'rows.json').read_text())
            b=json.loads((source/control/'verilator'/case/'rows.json').read_text())
            results.append(dict(control=control,trace=case,**compare(a,b)))
    result={'comparisons':results,'control_pairs':12,'exact_control_matches':sum(
        not r['binary_disagreements'] and not r['unknown_differences'] for r in results if r['control'].startswith('correct')),
        'binary_disagreements':sum(len(r['binary_disagreements']) for r in results),
        'pairs_with_unknown_differences':sum(bool(r['unknown_differences']) for r in results),
        'policy':'No changed vectors/mutants; Icarus X remains unknown. Verilator concretization never proves a four-state fault. Determine two-state eligibility with independent oracle; report X-sensitive pairs separately.'}
    dump(out,result)
    if result['exact_control_matches']!=12 or result['binary_disagreements']:
        raise RuntimeError('Unexpected defined behavior disagreement')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--preflight',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();from pathlib import Path
    r=audit(Path(a.preflight).resolve(),Path(a.output).resolve())
    print(json.dumps({k:v for k,v in r.items() if k!='comparisons'},indent=2))
