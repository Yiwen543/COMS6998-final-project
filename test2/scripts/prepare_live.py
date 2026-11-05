#!/usr/bin/env python3
"""Bind independent reference, fixed data, validated development/scoring code before live."""
import argparse
import json
from pathlib import Path
from common import BASE,ROOT,dump,sha
from preflight import verify_inputs
from final_score import verify_reference
from feedback import semantic_appendix
from audit_pipeline import audit
from runner import live_gate

def prepare(mock,replayed,final,output):
    if output.exists():raise ValueError('Live freeze already exists; never overwrite')
    verify_inputs();ref=verify_reference()
    for r in (mock,replayed):
        data=json.loads((r/'run.json').read_text())
        if data['runner_sha256']!=sha(BASE/'scripts/runner.py'):raise ValueError('Mock did not run current runner')
        for name,h in data['source_sha256'].items():
            if sha(ROOT/name)!=h:raise ValueError('Mock dependency changed')
    preflight=BASE/'results/preflight-v2'
    pipeline=audit(mock,replayed,preflight,BASE/'results/pre-live-pipeline-audit.json')
    cross=json.loads((BASE/'results/cross-tool-audit-v1.json').read_text())
    assert cross['exact_control_matches']==12 and cross['binary_disagreements']==0
    semantic=json.loads((preflight/'semantic.json').read_text())
    points=json.loads((preflight/'correct_stress/verilator/basic/coverage.json').read_text())
    groups=semantic_appendix(semantic,points)['equivalent_groups']
    assert len(groups)==2 and sum(len(g['members']) for g in groups)==5
    probe=json.loads((BASE/'results/formal-full-boundary-v1/summary.json').read_text())
    assert probe['formal']['status']=='FAIL' and probe['witness']['oracle_verdict']=='PASS'
    final_meta=json.loads((final/'summary.json').read_text())
    assert final_meta['not_a_model_effectiveness_result'] and final_meta['monitor_replays']==288
    assert final_meta['replayed_cycles']==33888
    scores=json.loads((final/'scores.json').read_text())
    assert len(scores)==6 and all(not s['distinct_mutants_killed'] for r in scores for s in r['simulation'].values())
    # Code/data allowlist for integrity only. This manifest is NOT a model packet.
    files={ROOT/name for name in ref['artifact_sha256']}
    for folder in ('configs','public','private','scripts','tests'):
        files.update(p for p in (BASE/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    files.add(BASE/'reference/frozen-v1/freeze.json')
    for folder in (preflight,mock,replayed,final,BASE/'results/formal-full-boundary-v1',BASE/'results/formal-witness-validation-v2'):
        files.update(p for p in folder.rglob('*') if p.is_file() and
                     not any(x in p.parts for x in ('verilator-build','work','__pycache__')) and p.suffix!='.vvp')
    for name in ('pilot_model.py','sfifo_fixture.py','coverage.py','semantic_candidate_scan.py',
                 'preflight_heldout.py','run_midterm_fixed.py'):
        files.add(ROOT/'scripts'/name)
    from preflight_heldout import ENGINE
    files.add(ENGINE)
    record={'status':'reviewed_reference_and_runner_ready',
        'gates':{k:True for k in ('reference_review','reference_controls','fault_observability','semantic_mapping','runner_accounting','feedback_isolation','formal_bridge','final_release')},
        'registration_sha256':sha(BASE/'configs/registration_v1.json'),
        'reference_checker_sha256':ref['reference_checker_sha256'],
        'budgets_unchanged':True,'scope':'test2 only; no reinterpretation of old stimulus trials',
        'known_limitations':['synthetic redundancy in one FIFO','two-state and Icarus eligibility differ',
                             'finite reference controls, not exhaustive correctness proof','no token-length placebo',
                             'formal witness decoding supports fixed Yosys SMTBMC public-pin layout only'],
        'files':{str(p.relative_to(ROOT)):sha(p) for p in sorted(files) if p!=output},
        'next_command':'.venv/bin/python test2/scripts/runner.py --mode live --preflight test2/results/preflight-v2 --output test2/results/live-v1'}
    dump(output,record);live_gate(output)
    return {'status':record['status'],'bound_files':len(record['files']),'freeze_sha256':sha(output)}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('mock','replay','final','output'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();print(json.dumps(prepare(a.mock.resolve(),a.replay.resolve(),a.final.resolve(),a.output.resolve()),indent=2))
