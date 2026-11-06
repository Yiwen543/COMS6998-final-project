"""Validate non-live planning/acceptance metadata only; no experiment entrypoint."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[3];A=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads((R/'test2/configs/controller_next_qualification_draft_v1.json').read_text());c=json.loads((R/'test2/results/controller-done-audit-maintenance-closure-v1/independent-acceptance.json').read_text());text=(R/'docs/test2_next_qualification_plan_v1.md').read_text()
for key in ['live_allowed','generation_authorized','native_execution_allowed','data_generation_allowed','paid_authorization','key_needed_now','old_authorization_reuse_allowed']:assert d[key] is False,key
assert d['executable_entrypoint'] is None
assert all(d['current_stage'][key]==0 for key in ['API_requests','count_requests','native_jobs','physical_runs','monitor_replays','USD_authorized_for_new_services'])
ids=[g['id'] for g in d['gates']];assert ids==['G0','G1','G2','G3','G4','G5']
required=['current_evidence','question','minimal_artifacts','acceptance','stop_conditions','roles','proposed_resources','authorization','status']
for i,g in enumerate(d['gates']):
 assert all(g.get(k) for k in required),g['id'];assert set(g['depends_on'])<=set(ids[:i]);assert g['id'] in text
assert len(d['public_control_roster'])==16 and len(set(x['id'] for x in d['public_control_roster']))==16
assert all(x['actual_result'] is None and x['definition_and_label_status'].startswith('DRAFT') for x in d['public_control_roster'])
r=d['gates'][1]['proposed_resources'];assert r['native_jobs_max']==2*r['public_controls']==32 and r['physical_runs_max']==32 and r['physical_cycles_max']==1024;assert r['native_depth']==8 and r['status']=='PROPOSED_NOT_AUTHORIZED'
assert d['gates'][2]['proposed_resources']['USD_cap'] is None and d['gates'][4]['proposed_resources']['candidate_model'] is None
assert d['service_plan']['current_calls']==0 and d['service_plan']['current_key_access'] is False
assert len(d['role_packages'])==3 and all('forbidden_inputs' in v for v in d['role_packages'].values())
assert c['E05_plan_independent_review']=='PENDING_NOT_SELF_ACCEPTED' and c['historical_producer_audit_v3_upgraded'] is False and c['old_scientific_results_changed'] is False
assert all(v==0 for v in c['fresh_executions_in_E05'].values())
for review in c['independent_authorities'].values():
 for key in ['review','review_markdown','manifest','fixture_records']:
  x=review[key];assert sha(R/x['path'])==x['sha256']
 assert json.loads((R/review['review']['path']).read_text())['status']=='PASS_WITH_LIMITS'
for component in c['accepted_companions'].values():
 for k in ['source','tests','audit','producer_phase','producer_manifest']:
  x=component[k];assert sha(R/x['path'])==x['sha256']
assert c['P04_evidence_correction']['original_v1_exact'].startswith('REJECT') and c['P04_evidence_correction']['serialization_cause']=='UNKNOWN'
assert '原样 v1 实际 REJECT' in text and '1252' in text and 'UNKNOWN' in text
assert 'R0' in text and 'H1/H2' in text and 'P05-N1' in text
assert d['maintenance_acceptance_sidecar']['sha256']==sha(R/d['maintenance_acceptance_sidecar']['path'])
report=dict(status='PASS_PLAN_STRUCTURE_AND_AUTHORITY_BINDINGS_ONLY',gates=6,public_control_families=16,role_packages=3,execution_allowed=False,new_unit_tests=0,new_scientific_or_service_runs=0,claim='Structural documentation/metadata checks only; no qualification outcomes, tool capability or future science acceptance established.',documents_sha256={n:sha(R/n) for n in ['docs/test2_next_qualification_plan_v1.md','test2/configs/controller_next_qualification_draft_v1.json','test2/results/controller-done-audit-maintenance-closure-v1/independent-acceptance.json']})
p=A/'document-validation.json';assert not p.exists();p.write_text(json.dumps(report,indent=2)+'\n');print(report['status'],'6gates/16controlfamilies/3roleallowlists; all execution flagsfalse; current source/review/result hashes match.')
