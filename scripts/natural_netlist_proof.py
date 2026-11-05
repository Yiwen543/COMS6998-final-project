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
from natural_semantics import NaturalAdapter,NaturalBitVectors
from run_midterm_fixed import sha


class NaturalNetlist(I2CNetlist):
    def __init__(self,module):
        self.module=module
        self.primary={b for p in module['ports'].values() if p['direction']=='input' for b in p['bits']}
        self.drivers={};self.macros={};self.active=set();self.onehot=[];self.used_cells=set();self.unknown_bits=[]
        self.cuts=[]
        for name,c in module['cells'].items():
            k=c['type'];ports=c['connections']
            if k in ('$dff','$adff','$aldff'):
                self.primary.update(ports['Q']);self.cuts.append({'cell':name,'kind':k,'port':'Q','bits':ports['Q']});continue
            if k=='$memwr_v2':continue
            if k=='$memrd_v2':
                self.primary.update(ports['DATA']);self.cuts.append({'cell':name,'kind':k,'port':'DATA','bits':ports['DATA']});continue
            outputs=[p for p,d in c['port_directions'].items() if d=='output']
            if outputs!=['Y']:raise Unsupported('Unsupported cell output '+k)
            for i,b in enumerate(ports['Y']):
                if b in self.drivers:raise Unsupported('Multiple drivers')
                self.drivers[b]=(name,i)

    def cell(self,name):
        n=self.module['cells'][name];kind=n['type']
        if kind not in ('$ge','$le','$lt','$mul','$xor','$reduce_xor','$reduce_xnor','$shr','$shl','$sshr','$sshl'):
            return super().cell(name)
        c,p=n['connections'],n['parameters'];w=len(c['Y']);key='n_'+stable(name)
        if key in self.macros:return key,w
        if name in self.active:raise Unsupported('Combinational cycle')
        self.active.add(name);self.used_cells.add(name)
        aw=len(c['A']);a=self.word(c['A'])
        if kind in ('$reduce_xor','$reduce_xnor'):
            parts=[self.bit(x) for x in c['A']];s=parts[0]
            for x in parts[1:]:s=f'(bvxor {s} {x})'
            if kind=='$reduce_xnor':s=f'(bvnot {s})'
            expr=BitVectors.resize(s,1,w,False)
        else:
            bw=len(c['B']);b=self.word(c['B']);signed=bool(int(p['A_SIGNED'],2) and int(p['B_SIGNED'],2))
            if kind in ('$shr','$shl','$sshr','$sshl'):
                signed=kind=='$sshr' and bool(int(p['A_SIGNED'],2))
                # Assignment context first widens A (including signed logical
                # shifts). A wider count must not truncate or change that
                # value's logical-shift semantics.
                semantic_width=max(w,aw);size=max(semantic_width,bw)
                a=BitVectors.resize(a,aw,semantic_width,bool(int(p['A_SIGNED'],2)))
                a=BitVectors.resize(a,semantic_width,size,signed);b=BitVectors.resize(b,bw,size,False)
                op='bvashr' if signed else ('bvshl' if kind in ('$shl','$sshl') else 'bvlshr')
                expr=BitVectors.resize(f'({op} {a} {b})',size,w,False)
            elif kind in ('$ge','$le','$lt'):
                size=max(aw,bw);a=BitVectors.resize(a,aw,size,signed);b=BitVectors.resize(b,bw,size,signed)
                suffix={'$ge':'ge','$le':'le','$lt':'lt'}[kind]
                expr=BitVectors.resize(BitVectors.bit(f'(bv{"s" if signed else "u"}{suffix} {a} {b})'),1,w,False)
            else:
                op={'$mul':'bvmul','$xor':'bvxor'}[kind]
                expr=f'({op} {BitVectors.resize(a,aw,w,signed)} {BitVectors.resize(b,bw,w,signed)})'
        self.active.remove(name);self.macros[key]=f'(define-fun {key} () (_ BitVec {w}) {expr})'
        return key,w


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
    bindings=[f'(assert (= {k} {ref.symbol(n)}))' for k,n in m.variables.items()]
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
    result={'status':'pass' if not unresolved and not m.unresolved and all(x=='unsat' for x in statuses[1:]) else 'unresolved_or_mismatch',
        'environment_satisfiable':True,'definition_checks':[{k:v for k,v in r.items() if k!='mismatch'} for r in checks],
        'pmux_onehot_checks':ref.onehot,'unresolved_definitions':unresolved,'ssa_unsupported':m.unresolved,
        'state_cuts':ref.cuts,'used_netlist_cells':sorted(ref.used_cells),'synthesis_dont_care_bits':len(ref.unknown_bits),
        'scope':'Two-state static definitions vs Yosys cells, shared Slang frontend. FF Q and memory read cuts free; no memory/state invariants, reachability, four-state or sequential equivalence.',
        'hashes':{str(p.resolve()):sha(p) for p in [ast,netlist,Path(__file__),Path(__file__).with_name('natural_semantics.py'),
            Path(__file__).with_name('spi_semantic_v2.py'),Path(__file__).with_name('spi_netlist_proof.py'),Path(__file__).with_name('i2c_netlist_proof.py')]}}
    (out/'proof.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'definitions':len(checks),'pmux':len(ref.onehot),'unresolved':unresolved,
        'mismatches':[x for x in result['definition_checks'] if x['z3']!='unsat']}))
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ['ast','netlist','output']:p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--top',required=True);a=p.parse_args();prove(a.ast,a.netlist,a.top,a.output)
