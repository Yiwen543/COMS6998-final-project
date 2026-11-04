#!/usr/bin/env python3
"""Audit hashes, own-trajectory prompt construction and recorded usage."""
import argparse
import json
from pathlib import Path

from minimal_c_feedback import minimal_c_messages
from run_minimal_c_ablation import ROOT, SEMANTIC, points_for, sha, usage_totals, write
from sfifo_prompt_ablation_feedback import messages_for
from token_placebo import replace_egg_with_padding


def verify(run):
    meta=json.loads((run/'metadata.json').read_text())
    for p,expected in meta['files_sha256'].items():
        if sha(ROOT/p)!=expected:
            raise AssertionError(f'Frozen file changed: {p}')
    cfg=meta['limits']; semantic=json.loads(SEMANTIC.read_text())
    calls=[json.loads(x) for x in (run/'calls.jsonl').read_text().splitlines()]
    rows=[json.loads(x) for x in (run/'rounds.jsonl').read_text().splitlines()]
    if any(not x['accepted'] for x in calls):
        raise ValueError('This full-trajectory audit requires accepted calls; failure retention is checked separately')
    prompts=0
    for arm in cfg['arms']:
        for rep in range(1,cfg['repetitions']+1):
            folder=run/arm/f'rep{rep}'
            history=[]; previous='seed'; cumulative=[]
            for call in [x for x in calls if x['arm']==arm and x['repetition']==rep]:
                prior=json.loads((folder/f'{previous}.json').read_text())
                points=points_for(folder/f'{previous}.dat')
                common=(history,prior,(folder/f'{previous}.sim.log').read_text(),points,
                        semantic,call['round'],cfg['max_new_cycles'])
                expected=messages_for('B_compact' if arm=='B_compact' else 'C_compact',*common)
                if arm in ('C_min','P_min'): expected=minimal_c_messages(expected)
                if arm=='P_min': expected=replace_egg_with_padding(expected,call['placebo']['padding_units'])
                actual=json.loads((run/call['prompt']).read_text())
                if expected!=actual: raise AssertionError('Own-trajectory prompt mismatch')
                cumulative.append(call)
                row=next(x for x in rows if (x['arm'],x['repetition'],x['round'])==(arm,rep,call['round']))
                if row['api_tokens']!=usage_totals(cumulative)['api_tokens']:
                    raise AssertionError('Usage accounting mismatch')
                history.extend(call['actions']);previous=call['simulation_prefix'];prompts+=1
    result={'status':'matched','mode':meta['mode'],'frozen_hashes_checked':len(meta['files_sha256']),
            'own_trajectory_prompts_checked':prompts,'usage_rows_checked':len(rows),
            'scope':'Saved prompt reproduction/isolation and usage arithmetic; semantic soundness and simulation replay are separate checks'}
    write(run/'prompt-accounting-validation.json',result)
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__);cli.add_argument('--run',type=Path,required=True)
    verify(cli.parse_args().run.resolve())
