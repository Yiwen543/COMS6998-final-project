#!/usr/bin/env python3
"""Recheck the new real and controlled dependency workloads on locked native RTL traces."""
import argparse
from collections import Counter
import json
from pathlib import Path

from egg_dependency_workload import ARCHIVE, LIVE_ARCHIVE, digest, plan, require
from egg_regression_workload import load_versions
from egg_txn_observe import ROOT, either, oracle, read_corpora, snapshots
from egg_txn_terms import parse_term, sample


BASE=ROOT/'results/milestone3'
COUNTS=('snapshots','ineligible','guard_false','guard_unknown','guard_true','left_alarm','right_alarm',
        'old_only','new_only','xor_true','xor_false','xor_unknown')


def score(corpus,suites,reference):
    rows=[(name,c) for name,cases in suites.items() if name!='matrix' for c in cases]
    trees=[]
    for _,c in rows:
        left,right,guard=(parse_term(c[k]) for k in ('left','right','guard'))
        selected=c.get('selected_properties',['data_last'])
        base=parse_term(reference[selected[0]])
        for prop in selected[1:]:base=('or',base,parse_term(reference[prop]))
        trees.append((left,right,guard,('xor',left,right),('and',left,('not',right)),('and',right,('not',left)),base,selected))
    evidence=[{'counts':Counter(dict.fromkeys(COUNTS,0)),'first_difference':None} for _ in rows]
    total=0
    for (design,trace),entry in sorted(corpus.items()):
        for snap in snapshots(entry['rows']):
            total+=1;memo={};expected=oracle(snap['values'])
            def evaluate(t):
                if t not in memo:memo[t]=sample(t,snap['values'])
                return memo[t]
            for (suite,c),trees_,out in zip(rows,trees,evidence,strict=True):
                left,right,guard,xor,old_only,new_only,base,selected=trees_
                counts=out['counts'];counts['snapshots']+=1
                if not all(snap['eligible'][p] for p in selected):counts['ineligible']+=1;continue
                active=evaluate(guard)
                if active is not True:counts['guard_unknown' if active is None else 'guard_false']+=1;continue
                counts['guard_true']+=1
                require(evaluate(base) is either(*(expected[p] for p in selected)), 'archive aggregate disagrees with imperative signals')
                a,b,x,o,n=(evaluate(t) for t in (left,right,xor,old_only,new_only))
                counts['left_alarm']+=a is True;counts['right_alarm']+=b is True
                counts['xor_unknown' if x is None else 'xor_true' if x else 'xor_false']+=1
                counts['old_only']+=o is True;counts['new_only']+=n is True
                require(c['expected_relation']!='equivalent' or x is False,'expected equality differs on physical snapshot')
                require(c['expected_relation']!='weakened' or n is not True,'weakened alarm gained a physical violation')
                require(c['expected_relation']!='infeasible','infeasible context observed')
                if x is True and out['first_difference'] is None:
                    out['first_difference']={'design':design,'trace':trace,'cycle':snap['cycle'],'phase':snap['phase'],
                                             'left':a,'right':b,'values':snap['values']}
    answer={}
    for (name,c),out in zip(rows,evidence,strict=True):
        t=out['counts'];require(t['snapshots']==total and total==sum(t[k] for k in ('ineligible','guard_false','guard_unknown','guard_true')),'sample accounting failure')
        require(t['guard_true']==sum(t[k] for k in ('xor_true','xor_false','xor_unknown')),'delta accounting failure')
        answer.setdefault(name,{})[c['id']]={**out,'counts':dict(t),'guard':c['guard'],'expected_relation':c['expected_relation']}
    return {'traces':len(corpus),'snapshots':total,'workloads':answer}


def run(archive,live_archive,corpus,controls):
    suites=plan(archive,live_archive);reference=load_versions(archive)['trial-01/initial']['monitors']
    traces=read_corpora(corpus,controls)
    main={k:v for k,v in traces.items() if k[0]=='original' or k[0].startswith('F')}
    extra={k:v for k,v in traces.items() if k not in main}
    return {'complete':True,'new_api_calls':0,'archive_sha256':digest(archive),'live_archive_sha256':digest(live_archive),
            'corpus_sha256':{p.name:json.loads((p/'summary.json').read_text())['corpus_sha256'] for p in (corpus,controls)},
            'scope':'Post-hoc existing sampled RTL traces, not the source of symbolic verdicts or new DUT proof.',
            'primary':score(main,suites,reference),'additional_controls':score(extra,suites,reference)}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive',type=Path,default=ARCHIVE);p.add_argument('--live-archive',type=Path,default=LIVE_ARCHIVE)
    p.add_argument('--corpus',type=Path,default=BASE/'frame-faults');p.add_argument('--controls',type=Path,default=BASE/'frame-diagnostic-faults');p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();result=run(a.archive,a.live_archive,a.corpus,a.controls)
    with a.output.open('x',encoding='utf8') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
    print(f"Checked new real/controlled workloads on {result['primary']['snapshots']} + {result['additional_controls']['snapshots']} snapshots.")
