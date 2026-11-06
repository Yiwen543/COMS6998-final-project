"""R02 exact policy/costbasis/source/review gate;no HTTP or credential access."""
from pathlib import Path
import json
from resources import require,sha,financial_policy

def authorize(root,reg,execute_path):
    root=Path(root);path=Path(execute_path)
    require(path.is_file() and not path.is_symlink(),'EXACT_EXECUTE_ABSENT')
    e=json.loads(path.read_text());require(e.get('record_kind')=='BC_RETEST_EXECUTE_V2' and e.get('stage')=='EXECUTE','WRONG_EXECUTE')
    require(e.get('api_ceiling_micro_usd')==20000000 and e.get('max_generations')==12 and e.get('max_counts')==0 and e.get('total_wall_seconds')==3600,'EXECUTE_RESOURCE_DRIFT')
    basis=financial_policy(root,reg);review_path=(root/e['review_path']).resolve()
    require(review_path.is_relative_to(root/'docs/audits') and review_path.is_file() and not review_path.is_symlink(),'REVIEW_LOCATION')
    ids=dict(registration_sha256=sha(root/'test2/configs/controller_done_bc_retest_v2.json'),source_manifest_sha256=sha(root/reg['source_manifest']),preparation_manifest_sha256=sha(root/reg['preparation_manifest']),financial_policy_sha256=reg['financial_policy_sha256'],cost_basis_sha256=reg['cost_basis_sha256'],method_addendum_sha256=reg['method_addendum_sha256'],user_zero_count_confirmation_sha256=reg['user_zero_count_confirmation_sha256'])
    require(sha(review_path)==e.get('review_sha256'),'REVIEW_HASH_DRIFT');review=json.loads(review_path.read_text())
    require(review.get('status') in ['PASS','PASS_WITH_LIMITS'] and review.get('scope')=='BC_RETEST_V2_EXACT_PRECHECK','INDEPENDENT_PRECHECK_REQUIRED')
    for n,h in ids.items():require(e.get(n)==h and review.get('input_identity',{}).get(n)==h,'EXACT_IDENTITY_DRIFT:'+n)
    for n,h in json.loads((root/reg['source_manifest']).read_text())['files'].items():require(sha(root/n)==h,'FROZEN_SOURCE_DRIFT:'+n)
    return e,basis
