"""Verify complete mock/replay measurements, prompt isolation and physical costs."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from wbxbar_experiment import verify_freeze,BASE


def audit(config,mock,replay,output):
    frozen=verify_freeze(config)
    m=json.loads((mock/'summary.json').read_text());r=json.loads((replay/'summary.json').read_text())
    if m['metadata']['mode']!='mock' or r['metadata']['mode']!='replay':raise ValueError('Modes')
    budget=frozen['development_budget'];sessions=2*budget['repetitions'];rounds=budget['rounds']
    expected_cycles=sessions*(8+sum(8+64*i for i in range(1,rounds+1)))
    for d in (m,r):
        meta=d['metadata']
        if meta['status']!='completed' or len(d['rows'])!=sessions*rounds:raise ValueError('Incomplete offline run')
        if meta['api_generation_calls'] or meta['api_count_requests']:raise ValueError('Offline API call')
        if meta['simulation_executions']!=sessions*(rounds+1) or meta['executed_cycles']!=expected_cycles:
            raise ValueError('Replay cycle accounting')
        if meta['compilations']!=2:raise ValueError('Compile accounting')
    for a,b in zip(m['rows'],r['rows']):
        for key in ['arm','repetition','round','status','coverage','checker','transport','groups','executed_cycles_including_replays','unique_generated_cycles']:
            if a[key]!=b[key]:raise ValueError('Replay disagreement: '+key)
        if not a['measurement_fresh'] or not b['measurement_fresh']:raise ValueError('Stale measurement')
        folder=f"rep{a['repetition']}-{a['arm']}";rnd=a['round']
        for name in ['raw-points.json','trace.json','actions.json']:
            # calls.jsonl sorts object keys; JSON object order has no meaning.
            # List order, values, source identity and every raw count must agree.
            before=json.loads((mock/folder/f'round{rnd}'/name).read_text())
            after=json.loads((replay/folder/f'round{rnd}'/name).read_text())
            if before!=after:raise ValueError('Raw replay mismatch: '+name)
    for rep in range(1,budget['repetitions']+1):
        for rnd in range(1,rounds+1):
            prompts=[json.loads((mock/f'rep{rep}-{arm}'/f'prompt-{rnd}-1.json').read_text()) for arm in ['B','C']]
            if prompts[0][0]!=prompts[1][0]:raise ValueError('Base instructions differ')
            b,c=[json.loads(p[1]['content']) for p in prompts];c.pop('semantic_relations')
            if b!=c:raise ValueError('Unequal common feedback for identical offline history')
    output.parent.mkdir(parents=True,exist_ok=True)
    if output.exists():raise ValueError('Audit exists')
    tests=output.with_suffix('.tests.log')
    command=[sys.executable,'-m','unittest','discover','-s','tests','-p','test_wbxbar*.py','-v']
    result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=120)
    tests.write_text(result.stdout+result.stderr)
    if result.returncode:raise ValueError('Focused checks failed')
    from spi_core_experiment import verify_freeze as old_spi
    from spi_core_safe_experiment import verify_freeze as safe_spi
    old_spi();safe_spi()
    paths=[config,mock/'summary.json',replay/'summary.json',mock/'calls.jsonl',replay/'calls.jsonl',tests,
        ROOT/'tests/test_wbxbar_experiment.py',ROOT/'scripts/wbxbar_experiment.py',ROOT/'scripts/run_wbxbar_bc.py',
        ROOT/'scripts/report_wbxbar_bc.py',Path(__file__)]
    for folder in (mock,replay):
        paths+=sorted(folder.glob('rep*/prompt-*.json'))
        paths+=sorted(folder.glob('rep*/round*/raw-points.json'))
    record={'pass':True,'scope':'Offline plumbing/isolation/accounting only; no live stimulus effectiveness evidence',
        'mock_rounds':len(m['rows']),'replay_rounds':len(r['rows']),
        'executions_each':sessions*(rounds+1),'physical_cycles_each':expected_cycles,
        'raw_replay_equal':True,'prompt_common_information_equal':True,'old_spi_freezes_unchanged':True,
        'focused_test_command':command,'focused_test_exit':result.returncode,
        'hashes':{str(p.relative_to(ROOT)):sha(p) for p in paths}}
    output.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k!='hashes'}))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ['config','mock','replay','output']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();audit(a.config.resolve(),a.mock.resolve(),a.replay.resolve(),a.output.resolve())
