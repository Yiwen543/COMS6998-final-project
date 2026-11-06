"""One grading engine for fresh/reused monitor evidence; every planned case retained."""
import argparse
import gzip
import json
from pathlib import Path
import time
from common import ROOT,BASE,dump,sha
from controller_done_data import TASK,REG as STUDY
from controller_done_loop_v2 import verify_data
from controller_done_runtime import replay
from controller_done_case_v4 import grade,unresolved,summarize
from controller_release_live import verify_release

REG=BASE/'configs/controller_done_scoring_v4.json'


def load(path):return json.loads(path.read_text())


def inventory(records):
    reg=load(STUDY);catalog={r['id'] for r in reg['fault_catalogue']};dev=sorted(reg['input_geometry_sha256']['development']);final=sorted(reg['input_geometry_sha256']['final'])
    lookup={(r['source'],r['simulator'],r.get('trace')):r for r in records};result=[]
    for source in ['correct']+sorted(catalog):
        for sim in ('iverilog','verilator'):
            for name in (dev+final if source=='correct' else final):
                label=lookup.get((source,sim,name))
                if label is None:
                    diagnostic=next((r for r in records if r['source']==source and r['simulator']==sim and not r.get('trace')),None)
                    label=dict(source=source,simulator=sim,trace=name,status='reference_case_missing',original_reference_record=diagnostic)
                result.append(label)
    return result


def assess(label,provider):
    """Providers supply evidence or a saved non-graded case, never a verdict override."""
    if label.get('status')!='complete':return unresolved(label,'reference_infrastructure_unresolved'),None
    try:
        evidence=provider()
        original=evidence.get('non_graded_case')
        if original is not None:return unresolved(label,'saved_case_unresolved',original_case=original),None
        rows_blob=evidence['rows_blob'];result=evidence['result'];raw=evidence['raw']
        case=grade(label,rows_blob,result,raw)
        case.update(evidence_provenance=evidence.get('provenance'),original_status=evidence.get('original_status','fresh'))
        return case,result
    except (OSError,ValueError,TypeError,KeyError) as error:
        return unresolved(label,'evidence_infrastructure_unresolved',error_type=type(error).__name__),None


def execute(run_root,out,source_scores=None,original_run=None):
    snapshots=verify_release(run_root);verify_data()
    originals=verify_release(original_run) if source_scores is not None else None
    saved=load(source_scores/'scores.json') if source_scores is not None else None
    if saved is not None and saved.get('release_sha256')!=sha(original_run/'release.json'):raise ValueError('Source replay scores are not bound to the original release')
    out.mkdir(parents=True,exist_ok=False);started=time.perf_counter();labels=inventory(load(TASK/'measurements-v1/summary.json')['records']);rounds=[]
    costs=dict(new_monitor_replays=0,new_replayed_cycles=0,reused_monitor_replays=0,new_DUT_simulations=0,new_formal_jobs=0,API_calls=0)
    for snap in sorted(snapshots,key=lambda r:(r['round'],r['repetition'],r['arm'])):
        key=(snap['arm'],snap['repetition'],snap['round']);cases=[];source_round=None;can_reuse=True
        if saved is not None:
            source_round=next((r for r in saved['rounds'] if (r['arm'],r['repetition'],r['round'])==key),None)
            old=next((r for r in originals if (r['arm'],r['repetition'],r['round'])==key),None)
            can_reuse=bool(old and snap['status']=='compiled' and old['status']=='compiled' and sha(run_root/snap['directory']/'compiled/candidate.sv')==sha(original_run/old['directory']/'compiled/candidate.sv'))
        for label in labels:
            if snap['status']!='compiled':cases.append(unresolved(label,'candidate_unavailable'));continue
            if saved is not None and not can_reuse:cases.append(unresolved(label,'candidate_reuse_binding_unresolved'));continue
            def provider():
                rows_path=(ROOT/label['directory']/'rows.json').resolve()
                if not rows_path.is_relative_to((TASK/'measurements-v1').resolve()):raise ValueError('rows_outside_frozen_task')
                if saved is not None:
                    oldcase=next((r for r in (source_round or {}).get('cases',[]) if (r['source'],r['simulator'],r.get('trace'))==(label['source'],label['simulator'],label['trace'])),None)
                    if oldcase is None:return dict(non_graded_case=dict(status='saved_case_missing'))
                    if oldcase.get('status')!='graded':return dict(non_graded_case=oldcase)
                    p=(source_scores/oldcase['result_path']).resolve()
                    if not p.is_relative_to(source_scores.resolve()) or sha(p)!=oldcase['result_sha256']:raise ValueError('saved_result_binding')
                    result=load(p);raw=gzip.decompress((p.parent/'replay.log.gz').read_bytes())
                    if sha(p.parent/'replay.log.gz')!=result['compressed_log_sha256']:raise ValueError('gzip_hash_mismatch')
                    costs['reused_monitor_replays']+=1
                    return dict(rows_blob=rows_path.read_bytes(),result=result,raw=raw,original_status=oldcase['status'],provenance=dict(result_path=str(p.relative_to(ROOT)),result_sha256=sha(p)))
                rows_blob=rows_path.read_bytes();rows=json.loads(rows_blob)
                p=out/snap['arm']/f"rep{snap['repetition']}"/f"round{snap['round']}"/label['source']/label['simulator']/label['trace']
                result=replay(run_root/snap['directory']/'compiled',rows,p,out/'row-cache');costs['new_monitor_replays']+=1;costs['new_replayed_cycles']+=result['cycles']
                return dict(rows_blob=rows_blob,result=result,raw=gzip.decompress((p/'replay.log.gz').read_bytes()),provenance=dict(result_path=str((p/'result.json').relative_to(ROOT)),result_sha256=sha(p/'result.json')))
            case,_=assess(label,provider);cases.append(case)
        summary=summarize(cases);rounds.append(dict(arm=key[0],repetition=key[1],round=key[2],candidate_status=snap['status'],**summary,cases=cases))
        dump(out/'progress.json',dict(rounds=rounds));print('grade-v4',*key,summary['unresolved_pairs'],flush=True)
    selected=load(run_root/'final-candidates.json')['candidates'];endpoints=[{k:v for k,v in r.items() if k!='cases'} for r in rounds if any((r['arm'],r['repetition'],r['round'])==(s['arm'],s['repetition'],s['selected_round']) for s in selected)]
    calls=[json.loads(s) for s in (run_root/'calls.jsonl').read_text().splitlines() if s.strip()];actual=[r for r in calls if r.get('generation_request_issued')];known=[r['usage'] for r in actual if isinstance(r.get('usage'),dict) and type(r['usage'].get('input_tokens'))==int and type(r['usage'].get('output_tokens'))==int]
    costs.update(generation_requests=len(actual),count_requests=sum(bool(r.get('count_request_issued')) for r in calls),unknown_generation_usage_requests=len(actual)-len(known),actual_generation_tokens=sum(u['input_tokens']+u['output_tokens'] for u in known) if actual and len(known)==len(actual) else None,wall_seconds=time.perf_counter()-started)
    result=dict(status='COMPLETE_WITH_UNRESOLVED_RETAINED',mode='reuse' if saved is not None else 'fresh',rounds=rounds,selected_endpoints=endpoints,costs=costs,
        inventory_cases=len(labels),oracle_unknown_by_type=summarize([unresolved(r,'inventory_only') for r in labels])['oracle_unknown_by_type'],
        registration_sha256=sha(REG),release_sha256=sha(run_root/'release.json'),source_scores_sha256=sha(source_scores/'scores.json') if source_scores is not None else None,
        field_semantics='Names including_marker include finalpost; ordinary excludes it. Union detections split into ordinary_safety and end_marker_finite_UNATTRIBUTED.',not_new_LLM_evidence=load(run_root/'run.json')['mode']!='live',old_scores_overwritten=False,producer_sha256=sha(__file__))
    dump(out/'scores.json',result);verify_release(run_root);return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--reuse-scores',type=Path);p.add_argument('--original-run',type=Path);a=p.parse_args()
    if bool(a.reuse_scores)!=bool(a.original_run):p.error('Reuse requires both scores and original run')
    x=execute(a.run.resolve(),a.output.resolve(),a.reuse_scores.resolve() if a.reuse_scores else None,a.original_run.resolve() if a.original_run else None);print(x['status'])
