#!/usr/bin/env python3
"""Post-hoc audit of missing proof dependencies: false in new scope vs absent from fact forest.

This is an explanatory ablation and not an operational fallback or a new proof
reuse result. Every missing typed relation is queried only after the frozen run.
"""
import argparse
from collections import Counter
import gzip
import json
from pathlib import Path

from egg_regression_smt import fresh_compare, verify_result


def run(directory):
    directory=Path(directory)
    entries=json.loads((directory/'proof_store.json').read_text())
    output=[]; unique={}
    with gzip.open(directory/'groups.jsonl.gz','rt',encoding='utf8') as stream:
        for line in stream:
            group=json.loads(line)
            for row in group['requests']:
                case=row['case']; reuse=row['arms']['shared_egg']['reuse']
                if reuse['status']!='blocked':
                    continue
                item={'request_id':case['id'],'control':case['control'],'cohort':case['cohort'],
                      'guard':case['guard'],'case_relation':row['oracle']['relation'],'missing':[]}
                for reason in reuse['reasons']:
                    record=entries[reason['entry_id']]
                    if reason['old_guard']!=record['guard'] or reason['new_guard']!=case['guard']:
                        raise ValueError('blocked proof scope mismatch')
                    deps={d['rule']['name']:d['receipt'] for d in record['dependencies']}
                    for name in reason['missing_current_dependencies']:
                        receipt=deps[name]; left,right=receipt['typed_left'],receipt['typed_right']
                        key=(case['guard'],left,right)
                        if key not in unique:
                            check=fresh_compare(left,right,case['guard'])
                            verify_result(left,right,case['guard'],check)
                            unique[key]=check
                        check=unique[key]
                        status={'equivalent':'still_valid_but_absent','strengthened':'invalid_in_current_scope',
                                'weakened':'invalid_in_current_scope','incomparable':'invalid_in_current_scope'}.get(check['relation'],'unknown')
                        item['missing'].append({'entry_id':reason['entry_id'],'fact_name':name,'old_guard':record['guard'],
                                                'left':left,'right':right,'status':status,'typed_check':check})
                if not item['missing']:
                    raise ValueError('blocked path without missing dependency')
                output.append(item)
    classifications=Counter(d['status'] for row in output for d in row['missing'])
    direct_scope=[d for r in output if r['control']=='scope-edit-four-to-five' for d in r['missing']
                  if d['old_guard']=='(eq data_n 4)' and 'data_index' in d['left'] and 'data_index' in d['right']]
    if not direct_scope or any(d['status']!='invalid_in_current_scope' for d in direct_scope):
        raise ValueError('fixed four-to-five dependency did not fail independent typed recheck')
    return {'complete':True,'new_api_calls':0,'blocked_requests':len(output),'unique_rechecks':len(unique),
            'missing_dependency_occurrences':dict(classifications),'scope_edit_exact_dependency_examples':direct_scope,
            'requests':output,'scope':'post-hoc checks, not used by operational paths or query counts'}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--run-dir',type=Path,required=True); p.add_argument('--output',type=Path,required=True); a=p.parse_args()
    result=run(a.run_dir)
    with a.output.open('x',encoding='utf8') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
