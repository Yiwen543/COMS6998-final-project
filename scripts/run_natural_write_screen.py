"""Offline reproduction of the prospectively fixed DMA/Flash write screen.

No credential access, checker generation, calibration search, or model calls.
A passing static gate would still require independent specification checkers,
legal temporal calibration and controls before any B development session.
"""
import argparse
import json
import subprocess
import time
from pathlib import Path
from probe_write_scopes import SCOPE,probe,inventory,verify
from hierarchy_netlist_proof import prove
from screen_write_hierarchy import screen
from run_midterm_fixed import ROOT,sha


def run(output):
    if output.exists():raise ValueError('Use a new output directory; evidence is not overwritten')
    config=json.loads(SCOPE.read_text())
    for c in config['candidates']:verify(c)
    output.mkdir(parents=True);rows=[];started=time.monotonic()
    for c in config['candidates']:
        top=c['top'];base=output/top;start=time.monotonic()
        probe(top,base);inventory(top,base,base/'inventory')
        proof=prove(base/'ast.json',base/('flat-kept.json' if top=='axi_dma_wr' else 'flat-simplified.json'),top,base/'proof-final')
        if proof['status']=='pass':
            screen(top,base,base/'screen-final',base/'proof-final')
            result=json.loads((base/'screen-final/screen.json').read_text())
            rows.append({'top':top,'static_count_gate_pass':result['static_count_gate_pass'],'groups':result['static_candidate_groups'],'nontrivial_groups':result['nontrivial_static_candidates'],'seconds':time.monotonic()-start})
        else:rows.append({'top':top,'static_count_gate_pass':False,'proof_status':proof['status'],'seconds':time.monotonic()-start})
    result={'scope_sha256':sha(SCOPE),'candidates':rows,'seconds':time.monotonic()-started,'API_calls':0,'B_allowed':False,'reason':'Static count gate is necessary, not sufficient. Independently authored checker and legal event calibration are still required.'}
    (output/'decision.json').write_text(json.dumps(result,indent=2)+'\n');return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();print(json.dumps(run(a.output.resolve()),indent=2))
