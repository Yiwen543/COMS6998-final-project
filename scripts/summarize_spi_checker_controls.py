#!/usr/bin/env python3
"""Require a clean baseline before crediting checker negative-control detection."""
import argparse
import json
from pathlib import Path


def summarize(evaluation):
    data=json.loads((evaluation/'summary.json').read_text())
    controls=[]
    for control in data['controls']:
        name=control['name']
        if control['status']!='applied':
            controls.append({'name':name,'result':'inapplicable'});continue
        positive=data['cases']['calibration/'+control['source_case']]
        negative=data['cases']['negative/'+name]
        baseline_good=(positive['verdict']=='scoped_pass' and positive['failure_count']==0 and positive['assumption_count']==0)
        detected=negative['verdict']=='dut_violation' and negative['failure_count']>0
        controls.append({'name':name,'baseline_clean':baseline_good,
            'result':('confounded_by_baseline_failure' if not baseline_good else 'detected' if detected else 'not_detected'),
            'negative_categories':negative['categories'], 'negative_verdict':negative['verdict']})
    reference=data['cases']['independent_reference/one_byte_write']
    truncated={n:v for n,v in data['cases'].items() if n.startswith('truncated/')}
    result={'controls':controls,'detected_with_clean_baseline':sum(c['result']=='detected' for c in controls),
        'applied_controls':sum(c['result']!='inapplicable' for c in controls),
        'confounded_controls':sum(c['result']=='confounded_by_baseline_failure' for c in controls),
        'independent_legal_reference_passed':reference['verdict']=='scoped_pass' and reference['failure_count']==0,
        'author_selftests_passed':all(t.get('pass') for t in data['selftests'] or []),
        'author_selftest_count':len(data['selftests'] or []),
        'truncated_prefixes':{n:{'false_completed_events':len(v['events']), 'failures':v['failure_count'],
            'verdict':v['verdict']} for n,v in truncated.items()},
        'interpretation':'Undetected controls stay in the denominator and require scope review. This is finite fault-detection evidence, not a checker proof.'}
    (evaluation/'control-accounting.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__);cli.add_argument('--evaluation',type=Path,required=True)
    args=cli.parse_args();result=summarize(args.evaluation.resolve())
    print(json.dumps({k:v for k,v in result.items() if k not in ('controls','truncated_prefixes')},indent=2))
