"""Screen pinned natural write scopes, preserving physical raw counter identity."""
import argparse
import json
import subprocess
from collections import defaultdict
from pathlib import Path
from hierarchy_semantics import HierarchyAdapter,HierarchyBitVectors
from screen_spi_semantic_v2 import mapping
from preflight_spi_host import identity,resolve_clock_alias
from run_midterm_fixed import ROOT,sha
from preflight_heldout import verify_rewrites
from slang_guard_adapter import any_of,Unsupported
from probe_write_scopes import SCOPE,configuration,verify


def module_scope(target,instances):
    scope=target['instance_scope'];paths=['']+[i['path'] for i in instances]
    return max((p for p in paths if not p or scope==p or scope.startswith(p+'.')),key=len)


def join_counter(target,points,instances):
    scope=module_scope(target,instances)
    def actual(p):return '.'.join(p['hierarchy'].split('.')[p['hierarchy'].split('.').index('dut')+1:])
    selected=[p for p in points if actual(p)==scope]
    if target['outcome']=='else':
        a=target['counter_anchor']
        hits=[p for p in selected if p['source']==a['source'] and p['line']==a['line'] and p['column']==a['column'] and p['outcome']=='else' and p['type'] in ('line','branch')]
        return {'status':'mapped','point':hits[0],'basis':target['counter_anchor_basis']+'; exact original line/branch else counter'} if len(hits)==1 else {'status':'unresolved','reason':'No unique exact opposite-polarity counter','candidates':hits}
    return mapping(target,selected)


def aggregate(targets,maps):
    """Verilator shares counters across loop iterations/generate scopes.

    Such a counter's activation is the OR of *all* mapped activations. We never
    pretend a physical count measures an individual unrolled iteration.
    """
    buckets=defaultdict(list)
    for t in targets:
        mp=maps[t['id']]
        key=(identity(mp['point']),tuple(t['event_context'])) if mp['status']=='mapped' else ('unresolved',t['id'])
        buckets[key].append(t)
    result=[];joined={}
    for ts in buckets.values():
        t=dict(ts[0]);t['id']='g'+str(len(result));t['member_ids']=[x['id'] for x in ts]
        t['compact']=any_of([x['compact'] for x in ts]);t['instance_scopes']=[x['instance_scope'] for x in ts]
        locals=[x.get('local_compact') for x in ts]
        t['local_compact']=any_of(locals) if all(x is not None for x in locals) else None
        result.append(t);joined[t['id']]=maps[ts[0]['id']]
    return result,joined


def clock_context(a,net,c):
    evidence=[]
    for name,cell in net['cells'].items():
        if cell['type'] not in ('$dff','$aldff','$adff'):continue
        clock,aliases=resolve_clock_alias(cell['connections']['CLK'],net)
        row={'cell':name,'type':cell['type'],'clock_aliases':aliases,'clock_valid':clock==net['ports'][c['clock']]['bits'] and int(cell['parameters']['CLK_POLARITY'],2)==1}
        if cell['type'] in ('$aldff','$adff'):
            port,param=('ALOAD','ALOAD_POLARITY') if cell['type']=='$aldff' else ('ARST','ARST_POLARITY')
            reset,aliases=resolve_clock_alias(cell['connections'][port],net)
            row.update(reset_aliases=aliases,reset_valid=reset==net['ports'][c['reset']]['bits'] and int(cell['parameters'][param],2)==c['reset_active'])
        evidence.append(row)
    if not evidence or not all(r['clock_valid'] and r.get('reset_valid',True) for r in evidence):raise Unsupported('Clock/reset aliases not proved')
    for t in a.targets:
        original=t['event_context'];resolved=[]
        for event in original:
            if event=='combinational':resolved.append(event);continue
            edge,name=event.split(':',1)
            bits,aliases=resolve_clock_alias(net['netnames'][name]['bits'],net)
            match=[port for port in (c['clock'],c['reset']) if bits==net['ports'][port]['bits']]
            if len(match)!=1:raise Unsupported('Noncanonical edge signal')
            resolved.append(edge+':'+match[0])
        t['original_event_context']=original;t['event_context']=resolved
    return evidence


def screen(top,base,out,proof_dir):
    c=configuration(top);verify(c);out.mkdir(parents=True,exist_ok=False)
    if (base/'scope.json').read_bytes()!=SCOPE.read_bytes():raise ValueError('Prospective scope drift')
    proof=json.loads((proof_dir/'proof.json').read_text())
    if proof['status']!='pass' or not proof['environment_satisfiable']:raise ValueError('Independent definitions not proved')
    for p,h in proof['hashes'].items():
        if sha(Path(p))!=h:raise ValueError('Proof provenance drift: '+p)
    a=HierarchyAdapter(json.loads((base/'ast.json').read_text()),top).extract()
    net=json.loads((base/'flat.json').read_text())['modules'][top]
    clocks=clock_context(a,net,c);m=HierarchyBitVectors(a,procedural=True)
    _,targets,unsupported=m.guards();points=json.loads((base/'inventory/raw-points.json').read_text())
    raw_maps={t['id']:join_counter(t,points,a.instances) for t in targets}
    combined,maps=aggregate(targets,raw_maps);original_targets=a.targets;a.targets=combined
    header,targets,unsupported2=m.guards()
    pairs=[(x,y) for i,x in enumerate(targets) for y in targets[i+1:] if x['event_context']==y['event_context'] and (x['source'],x['line'],x['column'])!=(y['source'],y['line'],y['column'])]
    commands=[];labels=[]
    for t in targets:
        commands += [t['id'],f'(not {t["id"]})'];labels += [(t['id'],'sat'),(t['id'],'not_sat')]
        if t.get('local_compact') is not None:
            commands += [t['local_compact'],f'(not {t["local_compact"]})'];labels += [(t['id'],'local_sat'),(t['id'],'local_not_sat')]
    for x,y in pairs:commands.append(f'(xor {x["id"]} {y["id"]})');labels.append((x['id'],y['id']))
    query=header+'\n'.join('(push)\n(assert '+q+')\n(check-sat)\n(pop)' for q in commands)+'\n'
    (out/'pairs.smt2').write_text(query);(out/'query-order.json').write_text(json.dumps(labels)+'\n')
    p=subprocess.run(['z3',str(out/'pairs.smt2')],text=True,capture_output=True,check=True,timeout=300)
    (out/'z3.log').write_text(p.stdout+p.stderr);st=p.stdout.splitlines()
    if len(st)!=len(labels) or any(s not in ('sat','unsat','unknown') for s in st):raise ValueError('Invalid status stream')
    statuses=dict(zip(labels,st));rules=[]
    for x,y in pairs:
        if x['compact']!=y['compact'] and statuses[(x['id'],y['id'])]=='unsat':rules.append({'name':'qfbv-'+x['id']+'-'+y['id'],'left':x['compact'],'right':y['compact'],'proof_status':'unsat','event_context':x['event_context'],'source_ids':[x['id'],y['id']],'pair_proof':'pairs.smt2'})
    payload={'targets':targets,'verified_rules':rules};(out/'egg-input.json').write_text(json.dumps(payload,indent=2)+'\n')
    p=subprocess.run([str(ROOT/'egraph/target/debug/guard_proofs')],input=json.dumps(payload),text=True,capture_output=True,check=True,timeout=30)
    graph=json.loads(p.stdout);(out/'egg.json').write_text(json.dumps(graph,indent=2)+'\n');roots={t['id']:t for t in graph['targets']};buckets=defaultdict(list)
    for t in targets:buckets[(tuple(t['event_context']),roots[t['id']]['eclass'])].append(t)
    groups=[]
    for (context,ec),members in buckets.items():
        if len({(t['source'],t['line'],t['column']) for t in members})<2:continue
        for i,x in enumerate(members):
            for y in members[i+1:]:
                if (x['source'],x['line'],x['column'])==(y['source'],y['line'],y['column']):continue
                if statuses.get((x['id'],y['id']),statuses.get((y['id'],x['id'])))!='unsat':raise ValueError('Unproved merge')
        rows=[]
        for t in members:
            tid=t['id'];mp=maps[tid];local=t.get('local_compact');constant=local is not None and (statuses[(tid,'local_sat')]=='unsat' or statuses[(tid,'local_not_sat')]=='unsat')
            eligible=mp['status']=='mapped' and mp['point']['hits']==0 and statuses[(tid,'sat')]=='sat' and statuses[(tid,'not_sat')]=='sat' and not constant
            rows.append({'id':tid,'source':t['source'],'line':t['line'],'column':t['column'],'source_text':t['source_text'],'mapping':mp,'guard_sat':statuses[(tid,'sat')],'guard_not_sat':statuses[(tid,'not_sat')],'local_constant':constant,'seed_zero_dynamic_candidate':eligible,'eclass_before':roots[tid]['eclass_before']})
        eligible=[r for r in rows if r['seed_zero_dynamic_candidate']];sites={(r['source'],r['line'],r['column']) for r in eligible};raw={identity(r['mapping']['point']) for r in eligible}
        good=len(sites)>=2 and len(raw)>=2
        groups.append({'eclass':ec,'event_context':context,'members':rows,'static_candidate_group':good,'nontrivial_static_candidate':good and len({r['eclass_before'] for r in eligible})>1})
    extraction={'targets':targets,'raw_targets':original_targets,'atoms':a.atoms,'unsupported':a.unsupported,'unsupported_typed_targets':unsupported+unsupported2,'procedure_contexts':a.procedure_notes,'instances':a.instances,'port_aliases':a.port_aliases,'loop_unrolls':a.loop_unrolls}
    (out/'extraction.json').write_text(json.dumps(extraction,indent=2)+'\n')
    scope=json.loads(SCOPE.read_text());g=scope['offline_acceptance'];ng=sum(x['static_candidate_group'] for x in groups);nn=sum(x['nontrivial_static_candidate'] for x in groups)
    result={'top':top,'pair_counts':{s:sum(statuses[(x['id'],y['id'])]==s for x,y in pairs) for s in ('sat','unsat','unknown')},'different_expression_rules':len(rules),'groups':groups,'mappings':maps,'raw_target_mappings':raw_maps,'raw_targets':len(original_targets),'typed_supported':len(targets),'mapped':sum(x['status']=='mapped' for x in maps.values()),'unresolved':sum(x['status']!='mapped' for x in maps.values()),'static_candidate_groups':ng,'nontrivial_static_candidates':nn,'static_count_gate_pass':ng>=g['min_source_distinct_groups'] and nn>=g['min_nontrivial_source_groups'],'raw_dut_denominator':len(points),'clock_reset_checks':clocks,'rewrite_validation':verify_rewrites(),'B_allowed':False,'checker_started':False,'reachability':'not established; SAT is not legal temporal reachability','proof_scope':proof['scope'],'hierarchy':'Instance-qualified directed port aliases proved vs Yosys; original raw counters retained. Shared loop/generate source counter activation is disjunction, never individual hit transfer. Unresolved sites retained.','discovery':'Z3 typed ground equalities, bounded Rust egg; no solver stimulus','hashes':{str(p.resolve()):sha(p) for p in [Path(__file__),SCOPE,base/'ast.json',proof_dir/'proof.json',base/'inventory/raw-points.json',out/'pairs.smt2',out/'egg-input.json',out/'egg.json']}}
    (out/'screen.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['top','raw_targets','typed_supported','mapped','unresolved','static_candidate_groups','nontrivial_static_candidates','static_count_gate_pass','pair_counts']},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--top',required=True)
    for n in ['base','output','proof']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();screen(a.top,a.base.resolve(),a.output.resolve(),a.proof.resolve())
