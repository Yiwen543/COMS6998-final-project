"""Certify typed ground equalities, run egg, join original source counters.

No calibration or model outcomes are used. This gate is necessary, never
sufficient, for starting specification checker development or B screening.
"""
import argparse
import json
import subprocess
from collections import defaultdict
from pathlib import Path
from natural_semantics import NaturalAdapter,NaturalBitVectors
from screen_spi_semantic_v2 import mapping
from preflight_spi_host import identity,resolve_clock_alias
from run_midterm_fixed import ROOT,sha
from preflight_heldout import verify_rewrites


def screen(top,base,out):
    out.mkdir(parents=True,exist_ok=False)
    proof=json.loads((base/'netlist-proof/proof.json').read_text())
    if proof['status']!='pass' or not proof['environment_satisfiable']:raise ValueError('Independent definition proof incomplete')
    for p,h in proof['hashes'].items():
        if sha(Path(p))!=h:raise ValueError('Proof provenance drift: '+p)
    a=NaturalAdapter(json.loads((base/'ast.json').read_text()),top).extract();m=NaturalBitVectors(a,procedural=True)
    header,targets,unsupported=m.guards()
    pairs=[(x,y) for i,x in enumerate(targets) for y in targets[i+1:] if x['event_context']==y['event_context']
        and (x['source'],x['line'],x['column'])!=(y['source'],y['line'],y['column'])]
    commands=[];labels=[]
    for t in targets:
        commands += [t['id'],f'(not {t["id"]})'];labels += [(t['id'],'sat'),(t['id'],'not_sat')]
        if t.get('local_compact') is not None:
            commands += [t['local_compact'],f'(not {t["local_compact"]})'];labels += [(t['id'],'local_sat'),(t['id'],'local_not_sat')]
    for x,y in pairs:commands.append(f'(xor {x["id"]} {y["id"]})');labels.append((x['id'],y['id']))
    query=header+'\n'.join('(push)\n(assert '+q+')\n(check-sat)\n(pop)' for q in commands)+'\n'
    (out/'pairs.smt2').write_text(query)
    p=subprocess.run(['z3',str(out/'pairs.smt2')],text=True,capture_output=True,check=True,timeout=180)
    (out/'z3.log').write_text(p.stdout+p.stderr);st=p.stdout.splitlines()
    if len(st)!=len(labels) or any(s not in ('sat','unsat','unknown') for s in st):raise ValueError('Invalid Z3 status stream')
    statuses={label:s for label,s in zip(labels,st)};rules=[]
    for x,y in pairs:
        if x['compact']!=y['compact'] and statuses[(x['id'],y['id'])]=='unsat':
            rules.append({'name':'qfbv-'+x['id']+'-'+y['id'],'left':x['compact'],'right':y['compact'],
                'proof_status':'unsat','event_context':x['event_context'],'pair_proof':'pairs.smt2','source_ids':[x['id'],y['id']]})
    payload={'targets':targets,'verified_rules':rules};(out/'egg-input.json').write_text(json.dumps(payload,indent=2)+'\n')
    p=subprocess.run([str(ROOT/'egraph/target/debug/guard_proofs')],input=json.dumps(payload),text=True,capture_output=True,check=True,timeout=30)
    graph=json.loads(p.stdout);(out/'egg.json').write_text(json.dumps(graph,indent=2)+'\n')
    roots={t['id']:t for t in graph['targets']};buckets=defaultdict(list)
    points=json.loads((base/'inventory/raw-points.json').read_text())
    maps={t['id']:mapping(t,points) for t in targets}
    for t in targets:buckets[(tuple(t['event_context']),roots[t['id']]['eclass'])].append(t)
    groups=[]
    for (context,ec),members in buckets.items():
        if len({(t['source'],t['line'],t['column']) for t in members})<2:continue
        for i,x in enumerate(members):
            for y in members[i+1:]:
                if (x['source'],x['line'],x['column'])==(y['source'],y['line'],y['column']):continue
                if statuses.get((x['id'],y['id']),statuses.get((y['id'],x['id'])))!='unsat':raise ValueError('Unproved egg merge')
        rows=[]
        for t in members:
            tid=t['id'];mp=maps[tid];local=t.get('local_compact')
            parameter_only=local is not None and (statuses[(tid,'local_sat')]=='unsat' or statuses[(tid,'local_not_sat')]=='unsat')
            candidate=(mp['status']=='mapped' and mp['point']['hits']==0 and statuses[(tid,'sat')]=='sat' and not parameter_only)
            rows.append({'id':tid,'line':t['line'],'source_text':t['source_text'],'mapping':mp,
                'guard_sat':statuses[(tid,'sat')],'local_constant':parameter_only,'seed_zero_dynamic_candidate':candidate,
                'eclass_before':roots[tid]['eclass_before']})
        eligible=[r for r in rows if r['seed_zero_dynamic_candidate']]
        sites={identity(r['mapping']['point']) for r in eligible}
        groups.append({'eclass':ec,'event_context':context,'members':rows,'static_candidate_group':len(sites)>=2,
            'nontrivial_static_candidate':len(sites)>=2 and len({r['eclass_before'] for r in eligible})>1})
    net=json.loads((base/'flat.json').read_text())['modules'][top];clocks=[]
    c=json.loads((base/'probe.json').read_text())['configuration']
    for name,cell in net['cells'].items():
        if cell['type'] not in ('$dff','$aldff','$adff'):continue
        clock,aliases=resolve_clock_alias(cell['connections']['CLK'],net)
        valid=clock==net['ports'][c['clock']]['bits'] and int(cell['parameters']['CLK_POLARITY'],2)==1
        row={'cell':name,'type':cell['type'],'source':cell.get('attributes',{}).get('src'),'clock_valid':valid,'clock_aliases':aliases}
        if cell['type']=='$aldff':
            reset,aliases=resolve_clock_alias(cell['connections']['ALOAD'],net)
            row['async_reset_valid']=reset==net['ports'][c['reset']]['bits'] and int(cell['parameters']['ALOAD_POLARITY'],2)==c['reset_active']
            row['reset_aliases']=aliases
        clocks.append(row)
    if not clocks or not all(r['clock_valid'] and r.get('async_reset_valid',True) for r in clocks):raise ValueError('Clock/reset context mismatch')
    extraction={'targets':targets,'atoms':a.atoms,'unsupported':a.unsupported,'unsupported_typed_targets':unsupported,'procedure_contexts':a.procedure_notes}
    (out/'extraction.json').write_text(json.dumps(extraction,indent=2)+'\n')
    result={'top':top,'pair_counts':{s:sum(statuses[(x['id'],y['id'])]==s for x,y in pairs) for s in ('sat','unsat','unknown')},
        'different_expression_rules':len(rules),'groups':groups,'mappings':maps,'targets':len(a.targets),'typed_supported':len(targets),
        'mapped':sum(x['status']=='mapped' for x in maps.values()),'unresolved':sum(x['status']!='mapped' for x in maps.values()),
        'static_candidate_groups':sum(g['static_candidate_group'] for g in groups),
        'nontrivial_static_candidates':sum(g['nontrivial_static_candidate'] for g in groups),
        'raw_dut_denominator':len(points),'clock_reset_checks':clocks,'rewrite_validation':verify_rewrites(),
        'B_allowed':False,'checker_started':False,'reachability':'not established; SAT is not legal temporal reachability',
        'proof_scope':proof['scope'],'hierarchy':'Original child-module counters retained. Predicate extraction is top-module scoped; child guard/path equivalence not claimed.',
        'discovery':'Z3 proves typed design-dependent ground equalities; bounded egg saturation organizes them. Raw source counters never merged.',
        'hashes':{str(p):sha(p) for p in [Path(__file__),base/'ast.json',base/'netlist-proof/proof.json',base/'inventory/raw-points.json',out/'pairs.smt2',out/'egg-input.json',out/'egg.json']}}
    (out/'screen.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['top','targets','typed_supported','mapped','unresolved','pair_counts','different_expression_rules','static_candidate_groups','nontrivial_static_candidates','raw_dut_denominator']},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--top',required=True)
    for n in ['base','output']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();screen(a.top,a.base.resolve(),a.output.resolve())
