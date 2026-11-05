"""Bind independently checked reachability and fixed B/C artifacts before calls."""
import argparse
import json
import re
import subprocess
from pathlib import Path
from coverage import summary
from inventory_natural_coverage import load_all
from preflight_spi_host import identity
from run_midterm_fixed import ROOT, sha
from wbxbar_experiment import BASE, STATIC, CANDIDATE, semantic_relations, verify_scope


def prepare(output, config_path, live=False, validation=None):
    scope,candidate=verify_scope()
    review=json.loads((BASE/'claude-v3/review.json').read_text())
    if not review.get('ready_for_offline_gate'):raise ValueError('Independent review blocked')
    evaluation=json.loads((BASE/'evaluation-v8/summary.json').read_text())
    observations=json.loads((BASE/'driver-evaluation-v2/summary.json').read_text())
    driver=json.loads((BASE/'driver-v1/summary.json').read_text())
    for record in (evaluation,observations,driver):
        for path,h in record['hashes'].items():
            if sha(Path(path))!=h:raise ValueError('Evidence changed: '+path)
    if evaluation['counts']['positive_scoped_pass']!=16 or evaluation['counts']['infrastructure_errors']:
        raise ValueError('Checker positive gate')
    raw=json.loads((STATIC/'inventory/raw-points.json').read_text())
    denominator=sorted(identity(p) for p in raw)
    if len(denominator)!=len(set(denominator)):raise ValueError('Duplicate denominator')
    sources=[str(Path(candidate['root'])/n) for n in candidate['sources']]
    targets={tuple(i) for g in scope['targets'] for i in g['source_counter_identities']}
    witnesses={};union={};qualified=[]
    for row in driver['cases']:
        name=row['case'];checked=observations['cases'][name]
        points=load_all(BASE/'driver-v1'/name/'verilator/coverage.dat',sources)
        if sorted(identity(p) for p in points)!=denominator:raise ValueError('Denominator changed')
        if checked['verdict']!='scoped_pass' or not row['transport']['delivery_complete']:continue
        if checked.get('failures') or checked.get('assumption_violations') or checked.get('unresolved'):
            raise ValueError('Inconsistent checker verdict')
        qualified.append(name)
        for p in points:
            key=identity(p)
            union[key]={**p,'hits':max(p['hits'],union.get(key,{}).get('hits',0))}
            if key in targets and p['hits']>0 and key not in witnesses:
                witnesses[key]={'case':name,'hits':p['hits'],
                    'trace_sha256':sha(BASE/'driver-v1'/name/'verilator/trace.json'),
                    'coverage_sha256':sha(BASE/'driver-v1'/name/'verilator/coverage.dat')}
    if set(witnesses)!=targets:raise ValueError('Not all original targets have checker-clean reachable witnesses')
    output.mkdir(parents=True,exist_ok=False)
    # Same frontend/macros as the coverage build; preserve every active source
    # token and the tool's original line directives. Inactive FORMAL blocks and
    # comments are not part of the simulated DUT and are not model hints.
    command=['verilator','-E','--timing','--coverage-line','--coverage-toggle',
             '--coverage-expr','-Wno-fatal',*sources]
    result=subprocess.run(command,cwd=ROOT,text=True,capture_output=True,timeout=30,check=True)
    (output/'preprocessed.v').write_text(result.stdout)
    (output/'preprocess-stderr.log').write_text(result.stderr)
    files={};source=None;line=0
    for text in result.stdout.splitlines():
        directive=re.fullmatch(r'`line (\d+) "([^"]+)" \d+',text)
        if directive:line=int(directive[1]);source=directive[2];continue
        if text.strip():
            if source not in sources:raise ValueError('Unexpected preprocessor source')
            files.setdefault(source,[]).append(f'{line}:{text.strip()}')
        line+=1
    rtl_view={'format':'Original source line number: complete active RTL code. Verilator -E with the simulation macros. Comments, whitespace-only lines and inactive preprocessor branches omitted; no active logic omitted. Raw coverage source coordinates remain original.',
              'sources':{k:'\n'.join(v) for k,v in files.items()},
              'source_sha256':{k:sha(ROOT/k) for k in sources}}
    (output/'rtl-prompt-view.json').write_text(json.dumps(rtl_view,indent=2)+'\n')
    (output/'preprocess.json').write_text(json.dumps({'command':command,'preprocessed_sha256':sha(output/'preprocessed.v'),
        'view_sha256':sha(output/'rtl-prompt-view.json'),'source_lines':{k:len(v) for k,v in files.items()},
        'policy':'Common representation chosen before live calls, without changing source, targets or token budget. Inactive formal harnesses are excluded equally; full compiled RTL remains visible.'},indent=2)+'\n')
    reach={'status':'all_targets_checker_clean_reachable','targets':len(targets),'groups':len(scope['targets']),
        'checker_clean_cases':qualified,'union_coverage':summary(list(union.values())),
        'witnesses':[{'counter':list(i),**w} for i,w in sorted(witnesses.items())],
        'private_only':'Never put witness actions, traces, timings or this file in model prompts.',
        'interpretation':'Ordinary reads already reach these counters. Exploratory difficulty waiver, not a newly discriminating benchmark.'}
    (output/'reachability.json').write_text(json.dumps(reach,indent=2)+'\n')
    controls=[]
    for r in evaluation['controls']:
        if r['name']=='negative/stale_after_reset':category='exclusion_demonstration'
        elif r['name']=='negative/early_unexplained_error':category='unresolved_specification_boundary'
        elif r['kind']=='single_fault' and not r['baseline_scoped_pass']:category='identity_rejection_on_unresolved_baseline'
        else:category=r['kind']
        controls.append({**r,'report_category':category})
    (output/'control-accounting.json').write_text(json.dumps({'original_controls_retained':True,'controls':controls,
        'clean_baseline_fault_controls':sum(r['report_category']=='single_fault' for r in controls),
        'clean_baseline_detected':sum(r.get('credited_detection',False) for r in controls),
        'boundary_identity_rejections':sum(r['report_category']=='identity_rejection_on_unresolved_baseline' and r['failures']>0 for r in controls)},indent=2)+'\n')
    artifacts=[ROOT/'configs/wbxbar_exploratory_bc_v1.json',BASE/'claude-v3/review.json',
        BASE/'claude-v3/review-packet.json',BASE/'spec-packet-v1/packet.json',
        BASE/'evaluation-v8/summary.json',BASE/'controls-v7/manifest.json',BASE/'controls-v7/private-inputs.json',
        BASE/'driver-evaluation-v2/summary.json',BASE/'driver-v1/summary.json',
        BASE/'driver-v1/compiled/manifest.json',BASE/'driver-v1/compiled/tb_natural_inventory.sv',
        output/'reachability.json',output/'control-accounting.json',output/'rtl-prompt-view.json',
        output/'preprocessed.v',output/'preprocess.json']
    artifacts+=list(CANDIDATE.iterdir())
    artifacts+=[STATIC/p for p in ['netlist.json','screen/screen.json','screen/extraction.json','screen/egg.json','screen/egg-input.json','proof/proof.json','inventory/raw-points.json']]
    artifacts+=[ROOT/p for p in candidate['source_hashes']]
    for name in ['wbxbar_experiment','run_wbxbar_bc','prepare_wbxbar_experiment','wbxbar_exploratory_driver',
        'probe_wbxbar_ordinary','pilot_model','run_midterm_b_development','run_midterm_fixed','run_pilot',
        'run_spi_core_b_development','inventory_natural_coverage','preflight_spi_host','coverage',
        'evaluate_spi_checker_candidate','prepare_wbxbar_checker_role','prove_wbxbar_index','wbxbar_conditional_semantics']:
        artifacts.append(ROOT/f'scripts/{name}.py')
    if live:
        if validation is None:raise ValueError('Live freeze needs offline runner validation')
        v=json.loads(validation.read_text())
        if not v.get('pass'):raise ValueError('Offline runner validation failed')
        for p,h in v['hashes'].items():
            if sha(ROOT/p)!=h:raise ValueError('Validation artifact drift')
        artifacts.append(validation)
    frozen={**scope,'id':'wbxbar_exploratory_bc_freeze_v1','status':'live_frozen' if live else 'offline_prepared',
        'offline_gate_pass':True,'live_B_allowed':live,'live_C_allowed':live,
        'freeze_pending':[] if live else ['runner_mock_replay_validation'],
        'counter_identities':[list(i) for i in denominator], 'semantic_relations':semantic_relations(scope['targets']),
        'rtl_prompt_view':rtl_view,
        'checker_sha256':sha(CANDIDATE/'checker.py'),
        'hashes':{str(p.relative_to(ROOT)):sha(p) for p in artifacts if p.is_file()},
        'feedback_selection':'All 17 registered raw counters in both arms plus a rotating 48 uncovered line/branch/expr page. C appends frozen complete guard relations for target groups not fully hit. No private witnesses or diagnostic authorship hints.',
        'review_limitations':review['limitations']}
    if config_path.exists():raise ValueError('Never overwrite an existing freeze')
    config_path.write_text(json.dumps(frozen,indent=2)+'\n')
    print(json.dumps({'targets':len(targets),'checker_clean_cases':len(qualified),'denominator':len(denominator),'live_allowed':live}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--config',type=Path,required=True)
    p.add_argument('--live',action='store_true');p.add_argument('--validation',type=Path)
    a=p.parse_args();prepare(a.output.resolve(),a.config.resolve(),a.live,a.validation.resolve() if a.validation else None)
