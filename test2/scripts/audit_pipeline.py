#!/usr/bin/env python3
"""Fresh offline measurement/feedback/accounting audit; no API calls."""
import argparse
import json
from pathlib import Path
from common import BASE, ROOT, dump, sha
from coverage import load
from preflight import verify_inputs

def jsonl(path):return [json.loads(s) for s in path.read_text().splitlines() if s]

def audit(mock,replayed,preflight,out):
    verify_inputs();rounds=jsonl(mock/'rounds.jsonl');calls=jsonl(mock/'calls.jsonl')
    replay_calls=jsonl(replayed/'calls.jsonl')
    assert len(rounds)==len(calls)==len(replay_calls)==36
    assert len({r['session_id'] for r in calls})==6
    assert len({r['session_id'] for r in replay_calls})==6
    assert {r['session_id'] for r in calls}.isdisjoint({r['session_id'] for r in replay_calls})
    assert all(not r['generation_request_issued'] and not r['count_request_issued'] for r in calls+replay_calls)
    assert sum(r['compile_attempts'] for r in rounds)==72
    assert sum(r['monitor_replays'] for r in rounds)==108
    assert sum(r['replayed_cycles'] for r in rounds)==3456
    index=lambda data:{(r['arm'],r['repetition'],r['round']):r for r in data}
    for key,r in index(calls).items():
        t=index(replay_calls)[key]
        assert r['prompt_sha256']==t['prompt_sha256']
        assert r['parsed']==t['parsed']
    for round_no in range(1,7):
        for rep in range(1,4):
            b=json.loads((mock/'B_prime'/f'rep{rep}'/f'round{round_no}'/'prompt.json').read_text())
            c=json.loads((mock/'C_prime'/f'rep{rep}'/f'round{round_no}'/'prompt.json').read_text())
            x=json.loads(b[1]['content']);y=json.loads(c[1]['content'])
            assert y.pop('egraph_feedback')['equivalent_groups']
            assert x==y and b[0]==c[0]
            assert set(x['development'])=={'basic','boundary','wrap_reset'}
    raw_points=0
    for name in ('basic','boundary','wrap_reset'):
        d=preflight/'correct_stress/verilator'/name
        assert sha(d/'rows.json')==json.loads((d/'simulation.json').read_text())['trace_sha256']
        p=load(d/'coverage.dat','test2/public/sfifo.v',include_descendants=True)
        assert p==json.loads((d/'coverage.json').read_text())
        assert len(p)==400;raw_points+=len(p)
    for root in (mock,replayed):
        manifest=json.loads((root/'final-candidates.json').read_text())
        assert manifest['not_live_evidence'] and not manifest['final_scoring_started']
        assert len(manifest['candidates'])==6
        for c in manifest['candidates']:
            d=Path(c['candidate_dir'])
            assert c['candidate_sha256']==sha(d/'candidate.sv')
            assert c['metadata_sha256']==sha(d/'candidate.json')
    report={'status':'offline_pipeline_audit_passed','mock_rounds':36,'replay_rounds':36,
            'prompt_pairs_checked':18,'raw_counter_records_reparsed':raw_points,
            'mock_api_calls':0,'no_effectiveness_result':True,'reference_gate_still_pending':True}
    dump(out,report);return report

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for arg in ('mock','replay','preflight','output'):p.add_argument('--'+arg,required=True,type=Path)
    a=p.parse_args();print(json.dumps(audit(a.mock.resolve(),a.replay.resolve(),a.preflight.resolve(),a.output.resolve()),indent=2))
