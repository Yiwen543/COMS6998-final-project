"""P09 saved-byte replay only. No test regeneration or old scientific execution."""
from pathlib import Path
import importlib.util,json,hashlib,os
P=Path(__file__).resolve().parent
B=P.parents[1]/'producer_test2_g0_I01_2026-11-05'
# P is .../agent_bridge_2026-11-06/P09_g0_implementation; producer is under audits.
B=P.parent.parent/'producer_test2_g0_I01_2026-11-05'
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
evidence=json.loads((B/'evidence-checks.json').read_text())
rows=[];mismatch=[];input_bad=[];semantic_diff=[]
def norm(v):
    if isinstance(v,dict):return {k:norm(x) for k,x in v.items() if k not in ('parse_seconds','input_bytes_read')}
    if isinstance(v,list):return [norm(x) for x in v]
    return v
for i,summary in enumerate(evidence['suite_history'],1):
    tree=P/'exec_tree' if i==6 else P/'exec_tree/drafts'/('attempt'+str(i))
    src=tree/'test2/g0_v1/adapter.py'; schema=src.with_name('schema.json')
    assert H(src)==summary['adapter_source_sha256'] and H(schema)==summary['schema_sha256']
    spec=importlib.util.spec_from_file_location('p09_saved_'+str(i),src)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    attempt=B/'snapshot'/summary['record_directory'];cases=sorted(attempt.glob('test_*'))
    for case in cases:
        binding=json.loads((case/'fixture-binding.json').read_text());saved=json.loads((case/'result.json').read_text())
        before={str(f.relative_to(case/'bundle')):H(f) for f in (case/'bundle').rglob('*') if f.is_file() and not f.is_symlink()}
        if before!=binding['input_sha256']:input_bad.append(str(case))
        result=mod.validate_bundle(case/'bundle')
        after={str(f.relative_to(case/'bundle')):H(f) for f in (case/'bundle').rglob('*') if f.is_file() and not f.is_symlink()}
        assert before==after
        row={'attempt':i,'case':case.name,'binding_sha256':H(case/'fixture-binding.json'),'saved_result_sha256':H(case/'result.json'),'expected':binding['expected'],'saved_actual':binding['actual'],'fresh_actual':result['integrity']['status'],'source_sha256':H(src),'result':result}
        rows.append(row)
        if result['integrity']['status']!=binding['actual']:mismatch.append({'attempt':i,'case':case.name,'saved':binding['actual'],'fresh':result['integrity']['status']})
        if norm(result)!=norm(saved):semantic_diff.append({'attempt':i,'case':case.name})
r={'scope':'Exact saved I01 synthetic bundles parsed once using corresponding SHA-identical copied adapter/schema;not regeneration of six suites.','cases':len(rows),'input_binding_mismatches':input_bad,'saved_status_reproduction_mismatches':mismatch,'normalized_result_differences':semantic_diff,'producer_expected_vs_actual_failures':sum(x['expected']!=x['saved_actual'] for x in rows),'rows':rows}
(P/'saved-byte-replay.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k!='rows'}))
assert len(rows)==469 and not mismatch and not input_bad

