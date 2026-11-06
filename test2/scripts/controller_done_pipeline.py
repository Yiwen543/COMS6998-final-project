"""API-free reproduction on the already frozen new physical corpus, new output only."""
import argparse
from pathlib import Path
from common import ROOT,BASE,run,dump,sha
from controller_done_loop import execute,verify_data
from controller_done_score import evaluate
from controller_done_formal import controls,finals
from controller_done_acceptance import verify


def pipeline(out):
    verify_data();out.mkdir(parents=True,exist_ok=False)
    sources=out/'sources';sources.mkdir()
    for p in (BASE/'scripts').glob('controller_done_*.py'):(sources/p.name).write_bytes(p.read_bytes())
    execute('mock',out/'mock');(out/'mock/runner-source.py').write_bytes((BASE/'scripts/controller_done_loop.py').read_bytes())
    execute('replay',out/'replay',out/'mock');(out/'replay/runner-source.py').write_bytes((BASE/'scripts/controller_done_loop.py').read_bytes())
    evaluate(out/'mock',out/'score-mock');evaluate(out/'replay',out/'score-replay')
    controls(out/'controls');finals(out/'mock',out/'controls',out/'formal')
    result=run([ROOT/'.venv/bin/python','-B','-m','unittest','discover','-s','test2/tests','-v'],out/'tests.log',120)
    dump(out/'test-command.json',result)
    if result['status']!='complete':raise ValueError('Current tests failed; results retained')
    acceptance=verify(out/'mock',out/'replay',out/'score-mock',out/'score-replay',out/'formal',out/'controls',out/'tests.log',out/'acceptance.json')
    dump(out/'completion.json',dict(status=acceptance['status'],API_calls=0,new_model_trials=0,physical_data='Reused new sealed physical corpus, not newly simulated',producer_sha256=sha(__file__)))
    return acceptance


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();print(pipeline(a.output.resolve())['status'])
