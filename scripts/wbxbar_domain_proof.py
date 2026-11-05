"""Independent combinational proof within the separately certified state domain.

Forked narrowly from hierarchy_netlist_proof.prove to preserve old freezes;
only the explicit domain assertions and conditional adapters differ.
"""
import json
import subprocess
from pathlib import Path
import hierarchy_netlist_proof as proof_module
from slang_guard_adapter import walk,Unsupported
from natural_semantics import comb,statement
from run_midterm_fixed import sha
from wbxbar_conditional_semantics import CERTIFICATE,LEMMA

def prove(ast,netlist,top,out):
    out.mkdir(parents=True,exist_ok=False)
    a=proof_module.NaturalAdapter(json.loads(ast.read_text()),top).extract();m=proof_module.NaturalBitVectors(a,procedural=True)
    ref=proof_module.NaturalNetlist(json.loads(netlist.read_text())['modules'][top]);checks=[];unresolved=[]
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
    domain_assertions=m.domain_assertions()
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
    header='(set-logic QF_BV)\n(set-option :timeout 10000)\n'+declarations+'\n'+'\n'.join(ref.macros.values())+'\n'+'\n'.join(bindings)+'\n'+'\n'.join(domain_assertions)+'\n'
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
        'scope':'Two-state definitions vs independent Yosys encoding under one original-transition proved conditional index lemma. Shared Slang frontend. No four-state or whole-IP correctness claim.', 'conditional_domain':LEMMA,'conditional_selects':a.conditional_selects,'domain_assertions':domain_assertions,
        'hashes':{str(p.resolve()):sha(p) for p in [ast,netlist,Path(__file__),CERTIFICATE,Path(__file__).with_name('wbxbar_conditional_semantics.py'),Path(__file__).with_name('hierarchy_semantics.py'),Path(__file__).with_name('natural_semantics.py'),Path(__file__).with_name('natural_netlist_proof.py'),
            Path(__file__).with_name('spi_semantic_v2.py'),Path(__file__).with_name('spi_netlist_proof.py'),Path(__file__).with_name('i2c_netlist_proof.py')]}}
    (out/'proof.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'definitions':len(checks),'pmux':len(ref.onehot),'unresolved':unresolved,
        'mismatches':[x for x in result['definition_checks'] if x['z3']!='unsat']}))
    return result


