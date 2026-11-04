"""Reuse unchanged RTL proofs; bind every original counter in the read profile."""
import csv
import json
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from run_i2c_fixed import SOURCE,verify_source
from coverage import load,summary
from preflight_spi_host import identity
from screen_spi_semantic_v2 import mapping


def screen():
    verify_source()
    old=ROOT/'results/i2c_event_candidate_20261104'
    base=ROOT/'results/i2c_read_candidate_20261104'
    cert=json.loads((old/'certified-guards.json').read_text())
    for file,h in cert['hashes'].items():
        if sha(ROOT/file)!=h:raise ValueError('Proof artifact changed: '+file)
    audit=json.loads((old/'qfbv-hypotheses/audit.json').read_text())
    targets={t['id']:t for t in audit['supported_targets']}
    pts={p.stem:load(p,str(SOURCE.relative_to(ROOT)),include_descendants=True) for p in (base/'driver-v2').glob('*.dat')}
    ix={n:{identity(p):p['hits'] for p in rows} for n,rows in pts.items()}
    assert all(set(x)==set(ix['seed']) for x in ix.values())
    maps={tid:mapping(t,pts['seed']) for tid,t in targets.items()}
    rows=[];groups=[]
    for g in cert['groups']:
        members=[]
        for tid in g['member_ids']:
            m=maps[tid];record={'id':tid,'mapping':m}
            if m['status']=='mapped':record['hits']={n:x[identity(m['point'])] for n,x in ix.items()}
            members.append(record)
        supported=[r for r in members if 'hits' in r and r['hits']['seed']==0]
        multi=('multi_read','multi_read_varied','rcont_chain','read_restart','read_stretch')
        reached=[r for r in supported if any(r['hits'][n] for n in multi)]
        late=[r for r in reached if not r['hits']['ordinary_write'] and not r['hits']['ordinary_read']]
        groups.append({**g,'members':members,'reachable_group':len(reached)>=2,'beyond_ordinary_read_group':len(late)>=2})
    with (base/'nine-pairs-counters.csv').open('w') as f:
        w=csv.writer(f);names=sorted(ix);w.writerow(['pair','target','source_line','type','outcome',*names])
        for i,pair in enumerate(cert['different_expression_pairs'],1):
            for mem in pair['members']:
                tid=mem['target']['id'];m=maps[tid];p=m['point'];k=identity(p)
                w.writerow([i,tid,p['line'],p['type'],p['outcome'],*[ix[n][k] for n in names]])
    result={'status':'source_relevance_gate_failed' if not any(g['beyond_ordinary_read_group'] for g in groups) else 'requires_checker_and_event_bindings',
      'reason':'No raw source-distinct equivalent group adds two seed-zero points beyond ordinary one-byte READB. Multistep event completion is separate evidence, not a substitute for guard provenance.',
      'groups':groups,'source_mappings':maps,'reached_groups':sum(g['reachable_group'] for g in groups),
      'reached_nontrivial_groups':sum(g['reachable_group'] and g['nontrivial'] for g in groups),
      'groups_beyond_ordinary_read':sum(g['beyond_ordinary_read_group'] for g in groups),
      'mapped':sum(m['status']=='mapped' for m in maps.values()),'unresolved':sum(m['status']!='mapped' for m in maps.values()),
      'coverage':{n:summary(p) for n,p in pts.items()},'raw_denominator':len(ix['seed']),
      'proofs_reused':str((old/'certified-guards.json').relative_to(ROOT)),'proof_sha256':sha(old/'certified-guards.json'),
      'timing_or_reachability_proof':False,'B_allowed':False,'checker_status':'independently gated; not assumed from source results',
      'config_sha256':sha(ROOT/'configs/i2c_read_screen.json'),'source_sha256':sha(SOURCE),
      'raw_files_sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted((base/'driver-v2').glob('*.dat'))}}
    (base/'source-screen.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','reached_groups','reached_nontrivial_groups','groups_beyond_ordinary_read','mapped','unresolved','raw_denominator']},indent=2))


if __name__=='__main__':screen()
