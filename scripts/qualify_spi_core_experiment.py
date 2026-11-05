"""Reconcile independent checker controls with actual source counters, then freeze.

No model calls, new simulation, target witnesses in prompts, or checker edits.
"""
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from evaluate_spi_core_checker import scoped_pass
from probe_spi_core_events import DRIVER, identity
from real_parent_screen import configuration, verify
from run_midterm_fixed import ROOT, sha
from spi_core_experiment import BASE, CANDIDATE, CONTRACT, FREEZE, validate_experimental


def qualify(out, freeze=False):
    c = configuration('spi_host_core'); verify(c)
    pre = ROOT/'configs/real_parent_screen.json'
    original = json.loads(pre.read_text())
    screen_path = BASE/'spi_host_core_v2/screen-v2/screen.json'
    screen = json.loads(screen_path.read_text())
    for p, digest in screen['hashes'].items():
        if sha(Path(p)) != digest: raise ValueError('Semantic evidence stale: '+p)
    review_path = BASE/'claude-checker-v4/review.json'
    review = json.loads(review_path.read_text())
    evaluation_path = BASE/'contract-repair-v4/qualified-evaluation/summary.json'
    ev = json.loads(evaluation_path.read_text())
    for p, digest in ev['hashes'].items():
        if sha(Path(p)) != digest:raise ValueError('Checker evaluation evidence stale: '+p)
    controls = BASE/'contract-repair-v4/qualified-controls'
    cm = json.loads((controls/'manifest.json').read_text())
    for n in ('inputs', 'controls'):
        if sha(controls/(n+'.json')) != cm[n+'_sha256']:raise ValueError('Control hash mismatch')
    rows = json.loads((controls/'inputs.json').read_text())
    if not review['ready_for_offline_gate'] or ev['worker_errors'] or ev['event_integrity_errors']:
        raise ValueError('Checker review/control gate failed')
    if not all(t['pass'] for t in ev['selftests']):raise ValueError('Selftest failed')
    if not all(x.get('scoped_pass') for x in ev['controls'] if x['kind']=='independent_positive'):
        raise ValueError('Independent positive did not pass')
    # Do not turn missing-RX inconclusive into a claimed detection.
    negative = [x for x in ev['controls'] if x['kind']=='single_fault']
    if any(not x['baseline_scoped_pass'] for x in negative):raise ValueError('Fault baseline invalid')
    if any(not x['credited_detection'] and x['verdict']!='inconclusive' for x in negative):
        raise ValueError('Fault silently passed')
    author = json.loads((CANDIDATE/'authorship.json').read_text())
    for p, digest in author['artifact_sha256'].items():
        if sha(CANDIDATE/p)!=digest:raise ValueError('Authored artifact modified')

    calibration = BASE/'spi_core_events-v3'
    obs_path = calibration/'observations.json'
    obs = json.loads(obs_path.read_text())
    seed_points = json.loads((calibration/'seed/raw-points.json').read_text())
    denominator = {identity(p) for p in seed_points}
    if len(seed_points)!=len(denominator) or len(denominator)!=screen['raw_dut_denominator']:
        raise ValueError('Raw denominator mismatch')
    seed_counts = {identity(p):p['hits'] for p in seed_points}
    witnesses, excluded_cases, input_files = [], [], []
    events = set()
    for ob in obs['cases']:
        name = ob['case']; result = ev['cases']['calibration/'+name]
        if not scoped_pass(result):
            excluded_cases.append({'case':name,'reason':'not scoped pass', 'verdict':result['verdict']})
            continue
        folder = calibration/name
        actions = json.loads((folder/'actions.json').read_text())
        validate_experimental(actions, 392, initial=True)
        if not ob['trace_agreement'] or ob['cycles_per_simulator']-8 > 384:
            raise ValueError('Original calibration budget or dual-sim gate failed')
        trace = json.loads((folder/'trace.json').read_text())
        if trace != rows['calibration/'+name]:raise ValueError('Evaluated trace differs from simulated trace')
        points = json.loads((folder/'raw-points.json').read_text())
        if {identity(p) for p in points} != denominator:raise ValueError('Calibration denominator differs')
        families = sorted({e['family'] for e in result['events'] if e['kind']=='pass'})
        events.update(families)
        witnesses.append({'case':name,'cycles_excluding_seed':len(trace)-8,'events':families,
                          'counts':{identity(p):p['hits'] for p in points}})
        input_files += [folder/n for n in ('actions.json','trace.json','raw-points.json','result.json')]
    targets, excluded_groups = [], []
    for group in screen['groups']:
        if not group['static_candidate_group']:continue
        members = [m for m in group['members'] if m['seed_zero_dynamic_candidate']]
        ids = [identity(m['mapping']['point']) for m in members]
        if any(seed_counts[i]!=0 for i in ids):raise ValueError('Target not zero in actual common seed')
        sites = {(i[0],i[1],i[2]) for i in ids}
        if len(sites)<2:raise ValueError('Not source-distinct')
        reaches = [w['case'] for w in witnesses if all(w['counts'][i]>0 for i in ids)]
        if not reaches:
            excluded_groups.append({'eclass':group['eclass'],'reason':'no complete clean in-budget calibration; not proven unreachable'})
            continue
        targets.append({'eclass':group['eclass'],'nontrivial':group['nontrivial_static_candidate'],
                        'member_ids':[m['id'] for m in members], 'counter_identities':ids,
                        'private_reachability_cases':reaches})
    gate = original['offline_acceptance']
    passed = len(targets)>=gate['min_source_distinct_groups'] and \
        sum(t['nontrivial'] for t in targets)>=gate['min_nontrivial_source_groups'] and \
        len(events)>=gate['min_distinct_reachable_event_families']
    paths = [pre,screen_path,review_path,evaluation_path,obs_path,CONTRACT,DRIVER,
             controls/'inputs.json', controls/'controls.json', controls/'prefix-audit.json',
             CANDIDATE/'authorship.json',BASE/'contract-repair-v2/authority/contract.json',
             ROOT/'configs/real_parent_dependencies.json',*input_files,
             *[CANDIDATE/n for n in author['artifact_sha256']],
             *[Path(p) for p in screen['hashes']], *[Path(p) for p in ev['hashes']],
             *[ROOT/p for p in c['source_hashes']]]
    script_names = ['spi_core_interface.py','spi_core_experiment.py','qualify_spi_core_experiment.py',
                    'run_spi_core_b_development.py','pilot_model.py','inventory_natural_coverage.py',
                    'coverage.py','evaluate_spi_checker_candidate.py','run_spi_checker_author.py',
                    'run_midterm_fixed.py','real_parent_screen.py','probe_spi_core_events.py']
    paths += [ROOT/'scripts'/n for n in script_names]
    metadata = {'created_utc':datetime.now(timezone.utc).isoformat(),
        'repository_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'status':'limited checker and B-development boundary; no formal A/B/C/P authorization',
        'dut_revision':c['revision'],'family':c['family'],'held_out_independent_ip':False,
        'offline_gate_pass':passed,'live_B_executed':False,'formal_ABCP_allowed':False,
        'development_budget':original['development_budget'],'model_limits':original['model_limits'],
        'development_acceptance':original['development_acceptance'],
        'feedback_policy':{'arm':'B','maximum_uncovered_rows':128,
            'selection':'Sort raw zero-hit line/branch/expr counters by identity; circular page offset (round-1)*128. No target/group ranking. Keep full raw evidence on disk.',
            'execution_trace':'Last 16 complete public-pin rows; history all accepted generated actions.',
            'checker_diagnostics':'Raw verdict/counts; first 8 per diagnostic category, total counts retained; no event-family feedback or checker code.'},
        'measurement_policy':'Fresh process for seed and each cumulative replay. Include init/reset. No implicit drain. Original DUT-only counters including unresolved mappings; never merge source locations.',
        'raw_denominator':len(denominator),'counter_identities':sorted(denominator),
        'targets':targets,'excluded_target_groups':excluded_groups,
        'reachable_event_families':sorted(events),'excluded_calibrations':excluded_cases,
        'private_calibration_summary':[{k:v for k,v in w.items() if k!='counts'} for w in witnesses],
        'control_counts':ev['control_counts'],'checker_sha256':sha(CANDIDATE/'checker.py'),
        'profile':'After seed enable=1, sw_reset=0, no dummy command; original widths/timing ranges retained. Fixed before first model generation, identical future arms.',
        'limits':review['limitations']+[
            'Actual integration includes two internal packer FIFOs; reviewer no-FIFOs wording applies only to the external data FIFOs.',
            'Minimum timing and stable-window RX checks, not liveness proof; pending batches remain inconclusive.',
            'All passing calibration-reachable groups selected without model outcomes. Ordinary traffic already reaches many; B may reject quickly.',
            'TX/RX recovery share a combinational group; different temporal event families are not proven equivalent.',
            'Same-CSID config-change discrepancy retained; no DUT/checker waiver and no known counterexample in prompts.'],
        'hashes':{str(p.relative_to(ROOT)):sha(p) for p in dict.fromkeys(paths)}}
    out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists():raise FileExistsError(out)
    out.write_text(json.dumps(metadata,indent=2)+'\n')
    if freeze:
        if not passed:raise ValueError('Offline qualification failed')
        if FREEZE.exists():raise FileExistsError('Freeze already exists; do not overwrite')
        FREEZE.write_bytes(out.read_bytes())
    print(json.dumps({'offline_gate_pass':passed,'targets':len(targets),
                     'nontrivial_targets':sum(t['nontrivial'] for t in targets),
                     'events':sorted(events),'frozen':freeze}))
    return metadata


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--freeze',action='store_true')
    a=p.parse_args();qualify(a.output.resolve(),a.freeze)
