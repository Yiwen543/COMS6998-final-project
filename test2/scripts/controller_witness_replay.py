#!/usr/bin/env python3
"""All frozen original BMC FAIL witnesses, physically rechecked as a new audit."""
import argparse
from collections import Counter
import json
from pathlib import Path
import time
from common import ROOT,BASE,dump,sha
from controller_offline_pipeline import integrity,RUN
from controller_monitor_live import TASK
from controller_physical_witness import adjudicate

REG=BASE/'configs/controller_witness_replay_v1.json'


def execute(out):
    integrity();reg=json.loads(REG.read_text());scores=BASE/'results/controller-final-v1/scores.json'
    if sha(scores)!=reg['source_scores_sha256']:raise ValueError('Original scores changed')
    out.mkdir(parents=True,exist_ok=False);dump(out/'registration.json',reg)
    for name in ('controller_witness_replay.py','controller_physical_witness.py'):(out/name).write_bytes((BASE/'scripts'/name).read_bytes())
    selections=json.loads((RUN/'final-candidates.json').read_text())['candidates'];faults={f['id']:ROOT/f['source'] for f in json.loads((TASK/'private/mutant-catalog-v1.json').read_text())['faults']}
    records=[];started=time.monotonic()
    for i,w in enumerate(reg['witnesses']):
        label=dict(arm=w['arm'],repetition=w['repetition'],source=w['source'],slot=w['slot'],original_directory=w['directory'])
        # Reserve two60s builds, two15s physical runs and15s monitor replay.
        if reg['overall_wall_cap']-(time.monotonic()-started)<180:
            records.append(dict(label,status='NOT_RUN_TOTAL_CAP'));continue
        selected=next(f for f in selections if (f['arm'],f['repetition'])==(w['arm'],w['repetition']))
        d=out/w['arm']/f'rep{w["repetition"]}'/w['source']/f'P{w["slot"]}'
        result=adjudicate(BASE/'results/controller-final-v1'/w['directory'],RUN/selected['directory'],faults[w['source']],w['slot'],d,out/'physical-build-cache')
        records.append(dict(label,**result));dump(out/'progress.json',records)
        print(i+1,'of33',w['arm'],w['repetition'],w['source'],w['slot'],result['classification'],flush=True)
    integrity();assert sha(scores)==reg['source_scores_sha256']
    summary=dict(status='completed',records=records,classifications=dict(Counter(r.get('classification',r['status']) for r in records)),
                 original_labels_unchanged=True,new_model_trials=0,API_calls=0,wall_seconds=time.monotonic()-started,
                 registration_sha256=sha(REG),source_sha256=sha(__file__))
    dump(out/'summary.json',summary);print(json.dumps({k:v for k,v in summary.items() if k!='records'},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();execute(a.output.resolve())
