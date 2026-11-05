"""Separate provisional/mock and independently reviewed live freeze."""
import argparse
import copy
import json
import re
from datetime import datetime,timezone
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from spi_core_experiment import verify_freeze as parent_freeze
from spi_core_safe_runtime import PREREG,DRIVER
from spi_core_safe_experiment import CONTRACT
from probe_spi_core_events import identity
from evaluate_spi_core_checker import scoped_pass

def freeze(preflight,out,review=None,faults=None):
    parent=parent_freeze();f=copy.deepcopy(parent)
    p=json.loads((preflight/'summary.json').read_text());reg=json.loads(PREREG.read_text())
    capacity=int(re.search(r'Capacity=(\d+)',DRIVER.read_text()).group(1))
    required=reg['development_budget']['seed_cycles']+reg['development_budget']['rounds']*reg['development_budget']['max_new_cycles']
    if capacity!=required or capacity!=reg['design']['command_queue_depth'] or capacity!=reg['design']['tx_queue_depth']:
        raise ValueError('Physical driver cap differs from registered budget/queues')
    if p['status']!='pass' or p['failures']:raise ValueError('Offline control gate failed')
    if p['checker_sha256']!=parent['checker_sha256']:raise ValueError('Checker changed')
    for name,h in p['hashes'].items():
        if sha(ROOT/name)!=h:raise ValueError('Preflight source drift: '+name)
    for k in ('development_budget','model_limits','development_acceptance','targets','counter_identities'):
        if reg[k]!=parent[k]:raise ValueError('Original budget/targets changed: '+k)
    expected={g['eclass'] for g in parent['targets']}
    if set(p['unchanged_targets_reachable'])!=expected:raise ValueError('Targets not all reachable')
    points=json.loads((preflight/'calibration_seed/verilator/raw-points.json').read_text())
    counts={identity(p):p['hits'] for p in points}
    for g in parent['targets']:
        if any(counts[tuple(k)]!=0 for k in g['counter_identities']):raise ValueError('Target already covered by new seed')
    families={e['family'] for name,c in p['cases'].items() if name.startswith('calibration_') and scoped_pass(c['checker']) and c['delivery_complete']
              for e in c['checker']['events'] if e['kind']=='pass'}
    if len(families)<3:raise ValueError('Multistep calibration incomplete')
    if not all(c['dual_simulator_agreement'] for c in p['cases'].values()):raise ValueError('Dual simulation mismatch')
    if not all(n['checker_assumption_detected'] and n['transport_oracle_rejected'] for n in p['transport_negative_controls']):
        raise ValueError('Negative controls failed')
    if faults is None:raise ValueError('Actual faulty-SV transport control evidence required')
    fs=json.loads((faults/'summary.json').read_text())
    if fs['status']!='pass' or fs['production_driver_sha256']!=sha(DRIVER):raise ValueError('Fault evidence not valid')
    if {x['name'] for x in fs['faults']}!={'dropped_offer','duplicate_acceptance','reordered_head','post_edge_acceptance'}:
        raise ValueError('Missing required faulty-SV controls')
    if not all(x['rejection']['stage']=='transport' for x in fs['faults']):raise ValueError('Fault stage wrong')
    if not all(x['equal'] for x in fs['pending_prefix_replay'].values()):raise ValueError('Pending replay differs')
    paths=[PREREG,DRIVER,CONTRACT,preflight/'summary.json',preflight/'case-definition.json',faults/'summary.json']
    for name in p['cases']:
        for tool in ('verilator','iverilog'):
            paths += [preflight/name/tool/n for n in ('requests.json','trace.json','transport.json','result.json')]
        paths.append(preflight/name/'verilator/raw-points.json')
    scripts=['spi_core_safe_interface.py','spi_core_safe_runtime.py','spi_core_safe_experiment.py',
             'run_spi_core_safe_b.py','create_spi_core_safe_driver.py','preflight_spi_core_safe_driver.py',
             'review_spi_core_safe_driver.py','freeze_spi_core_safe_experiment.py',
             'test_spi_core_safe_faults.py',
             'run_midterm_b_development.py','run_pilot.py']
    paths += [ROOT/'scripts'/n for n in scripts]
    if review:
        judged=json.loads((review/'review.json').read_text())
        if judged.get('ready_to_freeze') is not True:raise ValueError('Independent review not ready')
        manifest=json.loads((review/'packet-manifest.json').read_text())
        if manifest['preflight_sha256']!=sha(preflight/'summary.json'):raise ValueError('Reviewed different offline evidence')
        for name,h in manifest['source_hashes'].items():
            if sha(ROOT/name)!=h:raise ValueError('Reviewed source drift: '+name)
        paths += [review/'review.json',review/'metadata.json',review/'packet-manifest.json']
    f.update(created_utc=datetime.now(timezone.utc).isoformat(),experiment_id=reg['experiment_id'],
        status='protocol-safe driver separate development version',live_B_allowed=review is not None,
        offline_gate_pass=True,formal_ABCP_allowed=False,
        original_preregistration_sha256=sha(PREREG),
        profile=reg['design'],transport_preflight=str(preflight.relative_to(ROOT)),
        reachable_event_families=sorted(families),independent_review=str(review.relative_to(ROOT)) if review else None,
        limits=parent['limits']+['Per-cycle offers enter bounded producer queues; empty queues hold previous payload. This changes stimulus representation and cannot be pooled with old direct-pin B.',
            'Checker pass does not imply delivery complete: pending producer requests tracked independently.',
            'Only one fresh development run preregistered; no selectively replaced repetitions.'])
    f['hashes'].update({str(q.relative_to(ROOT)):sha(q) for q in paths})
    out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists():raise FileExistsError(out)
    out.write_text(json.dumps(f,indent=2)+'\n')
    print(json.dumps({'offline_gate_pass':True,'live_B_allowed':review is not None,'targets':len(f['targets']),'sha256':sha(out)}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--preflight',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--review',type=Path)
    p.add_argument('--faults',type=Path,required=True)
    a=p.parse_args();freeze(a.preflight.resolve(),a.output.resolve(),a.review.resolve() if a.review else None,a.faults.resolve())
