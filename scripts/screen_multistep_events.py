"""Reuse original-parent integration for a prospectively registered new scope.

No keys/models/checker logic. A successful static screen never authorizes B.
Old frozen adapters are not edited. Unsupported bindings remain explicit.
"""
import argparse
import json
import time
from pathlib import Path
from run_midterm_fixed import ROOT,sha
import real_parent_screen as parent
from real_parent_semantics import ParentAdapter,ParentBitVectors
from event_scope_semantics import EventAdapter,EventBitVectors
from probe_write_scopes import verify

SCOPE=ROOT/'configs/multistep_event_screen_v1.json'
def configuration(top):
    c=next(c for c in json.loads(SCOPE.read_text())['candidates'] if c['top']==top)
    c.setdefault('proof_keep',[])  # no extra manual naming hints in this scope
    return c

def run(top,out,adapter='original'):
    start=time.perf_counter();c=configuration(top);verify(c)
    decisions={'top':top,'scope_sha256':sha(SCOPE),'B_allowed':False,'C_allowed':False,'model_calls':0,
        'scope':'Static dependency/definition/mapping gate only. No event reachability, checker validity or B difficulty claim.'}
    A,M=(EventAdapter,EventBitVectors) if adapter=='constant_view' else (ParentAdapter,ParentBitVectors)
    decisions['adapter']=adapter
    with parent.replace(parent,SCOPE=SCOPE,configuration=configuration,ParentAdapter=A,ParentBitVectors=M):
        stage='probe'
        try:
            parent.probe(top,out)
            # Legacy helper copies its SPI overlay as metadata. It is not used
            # by this configuration; replace that misleading copy explicitly.
            (out/'dependency-overlay.json').write_text(json.dumps({'scope_sha256':sha(SCOPE),'additions':{},
                'policy':'No dependency overlay; exact source closure in registered scope.'},indent=2)+'\n')
            p=json.loads((out/'probe.json').read_text())
            if any(x['returncode'] for x in p['runs']):raise ValueError('Frontend failed; see probe logs')
            stage='typed_adapter'
            a=A(json.loads((out/'ast.json').read_text()),top).extract();m=M(a,procedural=True)
            _,targets,unsupported=m.guards()
            (out/'adapter-gate.json').write_text(json.dumps({'supported_guards':len(targets),'definitions':len(m.definition_sources),
                'extraction_unsupported':a.unsupported,'definitions_unsupported':m.unresolved,'typed_unsupported':unsupported,
                'constant_branch_elaboration':getattr(a,'constant_branch_elaboration',[])},indent=2)+'\n')
            stage='preserve';parent.preserve(top,out)
            stage='independent_definition_proof';proof=parent.prove(top,out,out/'proof')
            if 'hashes' in proof:
                proof['hashes'].update({str((ROOT/'scripts'/n).resolve()):sha(ROOT/'scripts'/n) for n in ('event_scope_semantics.py','screen_multistep_events.py')})
                (out/'proof/proof.json').write_text(json.dumps(proof,indent=2)+'\n')
            if proof['status']!='pass':raise ValueError('Independent definitions not certified: '+proof['status'])
            stage='source_inventory';parent.inventory(top,out,out/'inventory')
            stage='semantic_source_screen';parent.screen(top,out,out/'screen',out/'proof')
            s=json.loads((out/'screen/screen.json').read_text())
            decisions.update(status='static_gate_pass' if s['static_count_gate_pass'] else 'static_group_gate_rejected',
                static_groups=s['static_candidate_groups'],nontrivial_groups=s['nontrivial_static_candidates'],raw_denominator=s['raw_dut_denominator'])
        except Exception as e:
            out.mkdir(parents=True,exist_ok=True)
            decisions.update(status='blocked_before_event_qualification',failed_stage=stage,error_type=type(e).__name__,detail=str(e)[:2000])
        finally:
            decisions['elapsed_seconds']=time.perf_counter()-start
            decisions['runner_sha256']=sha(Path(__file__))
            (out/'decision.json').write_text(json.dumps(decisions,indent=2)+'\n')
    print(json.dumps(decisions,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--top',required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--adapter',choices=['original','constant_view'],default='original')
    a=p.parse_args();run(a.top,a.output.resolve(),a.adapter)
