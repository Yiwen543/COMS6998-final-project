"""Independent Yosys-cell encoding of natural-IP combinational definitions.

FF Q and memory read results are unconstrained current values. This is not a
temporal/memory correctness proof. All cuts and unsupported definitions remain
explicit; an unsupported definition cannot qualify a feedback relation.
"""
import argparse
import json
import subprocess
from pathlib import Path
from i2c_netlist_proof import I2CNetlist
from spi_semantic_v2 import BitVectors,Unsupported,stable
from hierarchy_semantics import HierarchyAdapter as NaturalAdapter,HierarchyBitVectors as NaturalBitVectors
from natural_netlist_proof import NaturalNetlist as BaseNetlist
from slang_guard_adapter import walk
from natural_semantics import comb,statement
from run_midterm_fixed import sha


class NaturalNetlist(BaseNetlist):
    def __init__(self,module):
        # Latches are state cuts, never combinational aliases. The AXI loop's
        # induction variable is intentionally not assumed initialized.
        import copy
        view=copy.deepcopy(module);latches=[]
        for name,c in list(view['cells'].items()):
            if c['type']=='$dlatch':latches.append((name,c));del view['cells'][name]
        super().__init__(view)
        for name,c in latches:
            self.primary.update(c['connections']['Q']);self.cuts.append({'cell':name,'kind':'$dlatch','bits':c['connections']['Q']})
        self.memory_bindings=[]

    def cell(self,name):
        c=self.module['cells'][name]
        if c['type']!='$shiftx':return super().cell(name)
        p=c['connections'];aw,bw,w=len(p['A']),len(p['B']),len(p['Y'])
        if int(c['parameters']['B_SIGNED'],2) or (1<<bw)-1>aw-w:raise Unsupported('shiftx out-of-range not proved absent')
        key='n_'+stable(name)
        if key not in self.macros:
            if name in self.active:raise Unsupported('Combinational cycle')
            self.active.add(name);a,b=self.word(p['A']),self.word(p['B']);expr=f'(bvlshr {a} {BitVectors.resize(b,bw,aw,False)})'
            expr=BitVectors.resize(expr,aw,w,False);self.macros[key]=f'(define-fun {key} () (_ BitVec {w}) {expr})';self.active.remove(name);self.used_cells.add(name)
        return key,w

    def symbol(self,n):
        if n['kind']!='MemoryRead':return super().symbol(n)
        src=n['source'];location=f"{src['source']}:{src['line']}.{src['column']}-{src['end_line']}.{src['end_column']}"
        found=[(key,c) for key,c in self.module['cells'].items() if c['type']=='$memrd_v2' and c['parameters']['MEMID'].lstrip('\\')==n['memory'] and c.get('attributes',{}).get('src')==location]
        if len(found)!=1:raise Unsupported('No exact memory/source binding: '+location)
        key,c=found[0]
        if int(c['parameters']['CLK_ENABLE'],2) or len(c['connections']['DATA'])!=n['type']['width'] or c['connections']['EN']!=['1']:raise Unsupported('Clocked/disabled/mismatched memory read')
        self.memory_bindings.append({'source':src,'cell':key,'address':c['connections']['ADDR'],'typed_selector':n['selector']})
        return self.word(c['connections']['DATA'])


def prove(ast,netlist,top,out):
    out.mkdir(parents=True,exist_ok=False)
    a=NaturalAdapter(json.loads(ast.read_text()),top).extract();m=NaturalBitVectors(a,procedural=True)
    ref=NaturalNetlist(json.loads(netlist.read_text())['modules'][top]);checks=[];unresolved=[]
    for key,d in m.definition_sources.items():
        try:
            expected=m.term(d['rhs']);actual=ref.symbol(d['lhs'])
            checks.append({'symbol':d['lhs']['symbol'],'definition':key,'mismatch':f'(not (= {expected} {actual}))'})
        except Unsupported as e:
            unresolved.append({'symbol':d['lhs']['symbol'],'reason':str(e)})
    if unresolved:
        result={'status':'unsupported_definition','environment_satisfiable':False,
            'definition_checks':[],'unresolved_definitions':unresolved,'ssa_unsupported':m.unresolved,
            'scope':'No certification: at least one independent definition encoding was unsupported.'}
        (out/'proof.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result));return result
    # Include every predicate atom in the independent binding audit, even if
    # its free-state value appears in no output definition.
    m.guards()
    for n in list(m.variables.values()):
        if n['kind']=='MemoryRead':m.term(n['selector'])
    bindings=[f'(assert (= {k} {ref.symbol(n)}))' for k,n in list(m.variables.items())]
    for r in ref.memory_bindings:
        expected=m.term(r['typed_selector']);actual=ref.word(r['address'])
        checks.append({'symbol':r['cell']+':ADDR','definition':'exact memory source/address','mismatch':f'(not (= {expected} {actual}))'})
    written={n['symbol'].split(' ',1)[1] for p in a.body['members'] if p.get('kind')=='ProceduralBlock' and comb(p) for x in walk(statement(p)) if x.get('kind')=='Assignment' for n in walk(x['left']) if n.get('kind')=='NamedValue'}
    unsafe=[n['symbol'] for key,n in m.variables.items() if n['kind']=='NamedValue' and n['symbol'] in written and key not in m.definitions]

    declarations='\n'.join(f'(declare-fun b{b} () (_ BitVec 1))' for b in sorted(ref.primary) if isinstance(b,int))
    declarations+='\n'+'\n'.join(f'(declare-fun {n} () (_ BitVec 1))' for n in ref.unknown_bits)
    declarations+='\n'+'\n'.join(f'(declare-fun {k} () (_ BitVec {v["type"]["width"]}))' for k,v in m.variables.items())
    header='(set-logic QF_BV)\n(set-option :timeout 10000)\n'+declarations+'\n'+'\n'.join(ref.macros.values())+'\n'+'\n'.join(bindings)+'\n'
    query='(check-sat)\n'+'\n'.join('(push)\n(assert '+q+')\n(check-sat)\n(pop)' for q in [*[r['violation'] for r in ref.onehot],*[r['mismatch'] for r in checks]])
    (out/'proof.smt2').write_text(header+query+'\n')
    p=subprocess.run(['z3',str(out/'proof.smt2')],text=True,capture_output=True,timeout=180,check=True)
    (out/'z3.log').write_text(p.stdout+p.stderr);statuses=p.stdout.splitlines()
    if len(statuses)!=1+len(ref.onehot)+len(checks) or statuses[0]!='sat':raise ValueError('Invalid/inconsistent proof environment')
    for row,s in zip(ref.onehot+checks,statuses[1:]):row['z3']=s
    result={'status':'pass' if not unresolved and not unsafe and all(x=='unsat' for x in statuses[1:]) else 'unresolved_or_mismatch',
        'environment_satisfiable':True,'definition_checks':[{k:v for k,v in r.items() if k!='mismatch'} for r in checks],
        'pmux_onehot_checks':ref.onehot,'unresolved_definitions':unresolved,'ssa_unsupported':m.unresolved,
        'unsafe_free_combinational_values':unsafe,'port_aliases':a.port_aliases,'instances':a.instances,'type_parameter_resolution':a.type_alias_repairs,'loop_unrolls':a.loop_unrolls,'memory_bindings':ref.memory_bindings,'state_cuts':ref.cuts,'used_netlist_cells':sorted(ref.used_cells),'synthesis_dont_care_bits':len(ref.unknown_bits),
        'scope':'Two-state static definitions vs Yosys cells, shared Slang frontend. FF Q and memory read cuts free; no memory/state invariants, reachability, four-state or sequential equivalence.',
        'hashes':{str(p.resolve()):sha(p) for p in [ast,netlist,Path(__file__),Path(__file__).with_name('hierarchy_semantics.py'),Path(__file__).with_name('natural_semantics.py'),Path(__file__).with_name('natural_netlist_proof.py'),
            Path(__file__).with_name('spi_semantic_v2.py'),Path(__file__).with_name('spi_netlist_proof.py'),Path(__file__).with_name('i2c_netlist_proof.py')]}}
    (out/'proof.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'definitions':len(checks),'pmux':len(ref.onehot),'unresolved':unresolved,
        'mismatches':[x for x in result['definition_checks'] if x['z3']!='unsat']}))
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ['ast','netlist','output']:p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--top',required=True);a=p.parse_args();prove(a.ast,a.netlist,a.top,a.output)
