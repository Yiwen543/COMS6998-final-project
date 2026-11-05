"""Prospectively pinned transaction/recovery screen; no models or stimulus search.

New adapters/evidence are local to this scope. Old frozen scripts stay unchanged.
"""
import argparse
import json
from pathlib import Path
from run_midterm_fixed import ROOT,sha
import screen_multistep_events as previous
import real_parent_screen as parent
import screen_write_hierarchy as screen_module
from real_parent_screen import replace
import hierarchy_netlist_proof as proof_module
from transaction_semantics import TransactionAdapter,TransactionBitVectors,ObservationNetlist
from transaction_counter_mapping import CounterRegistry

SCOPE=ROOT/'configs/transaction_recovery_screen_v1.json'
CODE=[Path(__file__).resolve(),ROOT/'scripts/transaction_semantics.py',ROOT/'scripts/transaction_counter_mapping.py']

def run(top,out,array_view=False):
    adapters=[];registry=None;instances=[]
    class BoundAdapter(TransactionAdapter):
        def __init__(self,ast,top):
            super().__init__(ast,top,json.loads((out/'flat.json').read_text())['modules'][top]);adapters.append(self)
    old_prove,old_inventory,old_screen=parent.prove,parent.inventory,parent.screen
    old_join,old_aggregate=screen_module.join_counter,screen_module.aggregate
    def prove(top,base,dest):
        result=old_prove(top,base,dest)
        evidence={'range_proofs':[x for a in adapters for x in a.range_proofs.values()],
                  'array_bindings':[x for a in adapters for x in a.array_bindings.values()],
                  'instance_port_rebindings':[x for a in adapters for x in a.instance_rebinds],
                  'independent_netlist_range_proofs':ObservationNetlist.evidence}
        ep=dest/'transaction-adapter-evidence.json';ep.write_text(json.dumps(evidence,indent=2)+'\n')
        result.setdefault('hashes',{}).update({str(p):sha(p) for p in [*CODE,ep]})
        result['array_view']=array_view
        (dest/'proof.json').write_text(json.dumps(result,indent=2)+'\n')
        return result
    def inventory(top,base,dest):
        nonlocal registry
        result=old_inventory(top,base,dest)
        points=json.loads((dest/'raw-points.json').read_text())
        registry=CounterRegistry(dest/'seed.dat',dest/'verilator-build',points)
        (dest/'exact-counter-membership.json').write_text(json.dumps(registry.manifest,indent=2)+'\n')
        return result
    def join(target,points,inst):
        nonlocal instances
        instances=inst
        return registry.join(old_join,target,points,inst)
    def aggregate(targets,maps):return registry.aggregate(old_aggregate,targets,maps,instances)
    def screen(top,base,dest,proof):
        with replace(screen_module,join_counter=join,aggregate=aggregate):old_screen(top,base,dest,proof)
        p=dest/'screen.json';j=json.loads(p.read_text());mp=base/'inventory/exact-counter-membership.json'
        j['hashes'].update({str(mp):sha(mp),**{str(p):sha(p) for p in CODE}})
        p.write_text(json.dumps(j,indent=2)+'\n')
    overrides={'SCOPE':SCOPE}
    if array_view:overrides.update(EventAdapter=BoundAdapter,EventBitVectors=TransactionBitVectors)
    ObservationNetlist.evidence=[]
    with replace(previous,**overrides),replace(parent,prove=prove,inventory=inventory,screen=screen),replace(proof_module,NaturalNetlist=ObservationNetlist if array_view else proof_module.NaturalNetlist):
        previous.run(top,out,'constant_view')
    p=out/'decision.json';j=json.loads(p.read_text())
    j['hashes']={str(p):sha(p) for p in CODE};j['array_view']=array_view
    p.write_text(json.dumps(j,indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--top',required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--array-view',action='store_true')
    a=p.parse_args();run(a.top,a.output.resolve(),a.array_view)
