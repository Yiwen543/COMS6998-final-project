"""Exact new-stage review/billing gate. No SDK or credential imports."""
from pathlib import Path
import json
from resources import require,sha,verified_pricing

def authorize(root,reg,execute_path):
    root=Path(root);path=Path(execute_path)
    require(path.is_file() and not path.is_symlink(),'EXACT_EXECUTE_ABSENT')
    e=json.loads(path.read_text());require(e.get('record_kind')=='BC_RETEST_EXECUTE_V1' and e.get('stage')=='EXECUTE','WRONG_EXECUTE')
    require(e.get('api_ceiling_micro_usd')==20000000 and e.get('max_generations')==12 and e.get('max_counts')==16 and e.get('total_wall_seconds')==3600,'EXECUTE_RESOURCE_DRIFT')
    for field in ['pricing_path','review_path']:require(type(e.get(field)) is str,'MISSING_'+field)
    price_path=(root/e['pricing_path']).resolve();review_path=(root/e['review_path']).resolve()
    require(all(p.is_relative_to(root/'docs/audits') and p.is_file() and not p.is_symlink() for p in [price_path,review_path]),'REVIEW_PRICING_LOCATION')
    require(sha(price_path)==e.get('pricing_sha256'),'PRICING_HASH_DRIFT')
    pricing=verified_pricing(json.loads(price_path.read_text()),reg,live=True)
    identities=dict(registration_sha256=sha(root/'test2/configs/controller_done_bc_retest_v1.json'),source_manifest_sha256=sha(root/reg['source_manifest']),preparation_manifest_sha256=sha(root/reg['preparation_manifest']),pricing_sha256=sha(price_path))
    require(sha(review_path)==e.get('review_sha256'),'REVIEW_HASH_DRIFT');review=json.loads(review_path.read_text())
    require(review.get('status') in ['PASS','PASS_WITH_LIMITS'] and review.get('scope')=='BC_RETEST_V1_EXACT_PRECHECK','INDEPENDENT_PRECHECK_REQUIRED')
    for name,h in identities.items():require(e.get(name)==h and review.get('input_identity',{}).get(name)==h,'EXACT_IDENTITY_DRIFT:'+name)
    for n,h in json.loads((root/reg['source_manifest']).read_text())['files'].items():require(sha(root/n)==h,'FROZEN_SOURCE_DRIFT:'+n)
    require(json.loads((root/'docs/audits/agent_bridge_2026-11-06/G1_qualification_v1/G1-final-acceptance-p17.json').read_text())['status']=='PASS_WITH_LIMITS','G1_ACCEPTANCE_REQUIRED')
    return e,pricing
