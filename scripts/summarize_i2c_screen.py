"""Keep temporal validation, raw source counts and experiment eligibility separate."""
import argparse
import csv
import json
import subprocess
from pathlib import Path
from coverage import load,summary
from preflight_spi_host import identity
from run_midterm_fixed import ROOT,sha
from run_i2c_fixed import SOURCE,DRIVER,verify_source


def summarize(base,checker):
    verify_source()
    cert=json.loads((base/'certified-guards.json').read_text())
    config=json.loads((ROOT/'configs/i2c_event_screen.json').read_text())
    ev=json.loads((checker/'controls-final/evaluation.json').read_text())
    review=json.loads((checker/'review.json').read_text())
    if ev['checker_sha256'] != sha(checker/'candidate/checker.py'):raise ValueError('Stale checker evaluation')
    for f,h in json.loads((checker/'candidate/authorship.json').read_text())['artifact_sha256'].items():
        if sha(checker/'candidate'/f)!=h:raise ValueError('Checker authorship artifact drift')
    pts={p.stem:load(p,str(SOURCE.relative_to(ROOT)),include_descendants=True) for p in (base/'driver-v2').glob('*.dat')}
    ix={n:{identity(p):p['hits'] for p in points} for n,points in pts.items()}
    if any(set(v)!=set(ix['seed']) for v in ix.values()):raise ValueError('Denominator drift')
    groups=[]
    for g in cert['groups']:
        members=[]
        for tid in g['member_ids']:
            m=cert['source_mappings'][tid]
            if m['status']!='mapped':continue
            key=identity(m['point'])
            members.append({'target_id':tid,'counter':{k:v for k,v in m['point'].items() if k!='hits'},
                            'hits':{n:v[key] for n,v in ix.items()}})
        eligible=[r for r in members if r['hits']['seed']==0 and any(r['hits'][n]>0 for n in ('stretch','nak_restart','nak_timeout'))]
        late=[r for r in eligible if r['hits']['write']==0]
        groups.append({**g,'members':members,'reachable_seed_zero_members':[r['target_id'] for r in eligible],
            'absent_in_ordinary_write_members':[r['target_id'] for r in late],
            'reachable_group':len(eligible)>=2,'late_specific_group':len(late)>=2})
    clean=lambda r:not r['failures'] and not r['assumption_violations'] and not r['unresolved']
    positive=['independent_write','reference_stretch_recovery','reference_nak_restart','reference_nak_timeout_recovery',
              'dut_seed','dut_write','dut_stretch','dut_nak_restart','dut_nak_timeout','dut_no_extension']
    predicates={
      'positive_controls_clean':all(clean(ev['cases'][n]) for n in positive),
      'selftests_pass':isinstance(ev['author_selftests'],list) and all(t['pass'] for t in ev['author_selftests']),
      'byte_and_reset_controls_detected':all(t['credited_detection'] for t in ev['negative_controls']),
      'event_fault_and_truncation_controls':all(t['credited_detection'] for t in ev['event_controls']),
      'no_extension_no_event':not any(e.get('kind')=='success' for e in ev['cases']['dut_no_extension']['events']),
      'premature_timeout_stop_rejected':not clean(ev['cases']['premature_timeout_stop']) and not ev['cases']['premature_timeout_stop']['events'],
      'missing_nak_status_not_passed':not clean(ev['cases']['missing_nak_status']) and not ev['cases']['missing_nak_status']['events'],
      'review_accepted_scoped_offline':review.get('ready_for_offline_gate') is True,
    }
    families=['stretch_recovery','nak_restart','nak_timeout_recovery']
    for fam,slug in zip(families,['stretch','nak_restart','nak_timeout']):
        predicates['event_'+fam]=all(any(e['family']==fam and e['kind']=='success' for e in ev['cases'][n]['events']) for n in ['reference_'+fam,'dut_'+slug])
    events={fam:ev['cases']['dut_'+slug]['events'] for fam,slug in zip(families,['stretch','nak_restart','nak_timeout'])}
    simulations=[]
    compiles=[]
    for folder in ['driver-v1','driver-icarus-v1','driver-v2','driver-icarus-v2','checked-smoke']:
        d=base/folder
        if not (d/'compile.json').exists():continue
        c=json.loads((d/'compile.json').read_text());compiles.append({'folder':folder,'seconds':c['seconds']})
        for p in sorted(d.glob('*.json')):
            if p.name.endswith(('.actions.json','.trace.json')) or p.name in ('compile.json','checked.json'):continue
            r=json.loads(p.read_text())
            if 'steps' in r and 'simulation_seconds' in r:
                simulations.append({'file':str(p.relative_to(ROOT)),'steps':r['steps'],'seconds':r['simulation_seconds']})
    cal={n:json.loads((base/f'driver-v2/{n}.json').read_text()) for n in pts}
    predicates['environment_valid']=all(r['environment_valid'] for r in cal.values())
    predicates['simulator_agreement']=all(json.loads((base/f'driver-v2/{n}.trace.json').read_text())==json.loads((base/f'driver-icarus-v2/{n}.trace.json').read_text()) for n in pts)
    predicates['calibration_within_budget']=all(r['steps']<=config['development_budget']['seed_cycles']+384 for r in cal.values())
    candidate_ok=all(predicates.values())
    late=[g for g in groups if g['late_specific_group']]
    calls=[]
    for p in sorted(base.glob('claude-checker-v*/**/metadata.json')):
        m=json.loads(p.read_text())
        if m.get('usage') is None and (p.parent/'stream.jsonl').exists():
            # Preserve original metadata; recover explicitly reported error usage separately.
            for line in (p.parent/'stream.jsonl').read_text().splitlines():
                try:r=json.loads(line)
                except ValueError:continue
                if r.get('type')=='result':
                    m.update(usage=r.get('usage'),total_cost_usd=r.get('total_cost_usd'))
        calls.append({'path':str(p.relative_to(ROOT)),**{k:m.get(k) for k in ['role','requested_model','status','usage','model_usage','total_cost_usd','wall_seconds']}})
    versions={}
    for name,cmd in [('verilator',['verilator','--version']),('icarus',['iverilog','-V']),('z3',['z3','--version']),
                     ('claude',['claude','--version']),('rustc',['rustc','--version']),('cargo',['cargo','--version']),
                     ('yosys',[str(ROOT/'build/tools/oss-cad-20261103/oss-cad-suite/bin/yosys'),'-V'])]:
        r=subprocess.run(cmd,text=True,capture_output=True,timeout=15)
        versions[name]=(r.stdout+r.stderr).splitlines()[0]
    result={'status':'not_qualified_for_B' # No reviewed event-to-guard binding yet
      ,
      'checker_controls_pass':candidate_ok,'checker_gates':predicates,'event_witnesses':events,
      'source_equivalence_groups':groups,'reachable_groups':sum(g['reachable_group'] for g in groups),
      'late_specific_groups':len(late),'late_nontrivial_groups':sum(g['nontrivial'] for g in late),
      'late_definition':'At least two separate mapped counters zero in shared seed AND ordinary one-byte write, positive in multistep calibration. Operational relevance check before any B/C; not an unreachability proof.',
      'decision_basis':'Requested distinct multistep targets are not provided by repeated ordinary START predicates. Do not launch B just because there are nine proved pairs or larger source code. No budget adjustment.',
      'source_event_binding_complete':False,'event_to_equivalence_group_bindings':[],
      'budget':config['development_budget'],'coverage':{n:summary(p) for n,p in pts.items()},
      'unmapped_targets':cert['unresolved_targets'],'raw_denominator':len(ix['seed']),
      'compile_attempts':compiles,'simulations':simulations,'total_executed_cycles':sum(s['steps'] for s in simulations),
      'claude_calls':calls,'known_claude_cost_usd':sum(c['total_cost_usd'] or 0 for c in calls),
      'openai_calls':0,'B_runs':0,'C_runs':0,'A_runs':0,'placebo_runs':0,
      'versions':versions,'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
      'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [SOURCE,DRIVER,ROOT/'scripts/i2c_fixture.py',ROOT/'scripts/run_i2c_fixed.py',
            ROOT/'scripts/evaluate_i2c_checker.py',ROOT/'scripts/independent_i2c_controls.py',ROOT/'scripts/i2c_netlist_proof.py',
            ROOT/'scripts/certify_i2c_guards.py',ROOT/'configs/i2c_event_screen.json',Path(__file__),checker/'candidate/checker.py',
            checker/'candidate/properties.json',checker/'candidate/contract.md',checker/'candidate/authorship.json',checker/'review.json']}}
    (base/'screen.json').write_text(json.dumps(result,indent=2)+'\n')
    with (base/'source-counter-comparison.csv').open('w') as f:
        w=csv.writer(f);names=sorted(ix);w.writerow(['pair','target','line','column','counter_type','outcome',*names])
        for num,pair in enumerate(cert['different_expression_pairs'],1):
            for m in pair['members']:
                q=m['mapping']['point'];key=identity(q)
                w.writerow([num,m['target']['id'],q['line'],q['column'],q['type'],q['outcome'],*[ix[n][key] for n in names]])
    print(json.dumps({k:result[k] for k in ['status','checker_controls_pass','reachable_groups','late_specific_groups','total_executed_cycles','known_claude_cost_usd']},indent=2))
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--checker',type=Path,required=True)
    a=p.parse_args();summarize(a.base.resolve(),a.checker.resolve())
