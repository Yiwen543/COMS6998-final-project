"""P01-R1: saved-evidence disclosure only; no native tools, replay or API calls."""
import argparse
from collections import Counter
import json
from pathlib import Path
from common import ROOT, BASE, dump, sha


def load(p):return json.loads(p.read_text())


def analyze(out):
    formal=BASE/'results/controller-done-live-formal-v2/summary.json'
    review=ROOT/'docs/audits/agent_bridge_2026-11-05/P01'
    paths={
        'review_md':(review/'review.md','fd45bfcd842b42bf3d28d0c8b41709a89706f6dc699a24270e70a62cd33308e2'),
        'review_json':(review/'review.json','79d5bdb4f86bb82fa94c273afb7ec07cec695f05077a6e05621ac11df7bf1cbf'),
        'review_manifest':(review/'manifest.json','9eb5cbee8de1d2a6d4c81716b79ea9a12db63033156e207caec4b426c018bf2e'),
        'candidate':(BASE/'results/controller-done-live-v2/C2_semantic/rep1/round6/compiled/candidate.sv','7368aa0e874468b520a03da1282031b4277f7ac5147fa9b9f1db46b3fdde74be'),
        'smt':(BASE/'results/controller-done-live-formal-v2/C2_semantic/rep1/correct/P4-bmc/work/model/design_smt2.smt2','6b4ad28604b4b02d605e0889438eae9f27dfbbf66d68a7d39f0a1d3d08f135af'),
        'physical':(BASE/'results/controller-done-live-formal-v2/C2_semantic/rep1/correct/P4-bmc/physical/result.json','935a5c5723eec13bf2d90a55e5dab4d0b779263d7e65287ce5891caa13925231')}
    for p,h in paths.values():
        if sha(p)!=h:raise ValueError('P01 evidence changed: '+str(p))
    jobs=load(formal)['jobs'];states=dict(Counter(j['status'] for j in jobs))
    fails=dict(Counter(j['mode'] for j in jobs if j['status']=='FAIL'))
    bmc=[j for j in jobs if j['status']=='FAIL' and j['mode']=='bmc']
    reproduced=[j for j in bmc if j.get('witness',{}).get('status')=='physically_reproduced_prefix_checked' and j['witness'].get('formal_alarm_reproduced')]
    unresolved=[j for j in bmc if j.get('witness',{}).get('status')=='unresolved']
    assert len(jobs)==540 and states=={'PASS':75,'FAIL':104,'TIMEOUT':361}
    assert fails=={'bmc':94,'prove':7,'cover':3} and len(reproduced)==20 and len(unresolved)==74
    assert all(j['witness']['reference_verdict']=='FAIL' for j in reproduced)
    assert all(j['arm']=='C2_semantic' and 'reference_verdict' not in j['witness'] for j in unresolved)
    assert sum(j['source']=='correct' for j in unresolved)==7
    table=[]
    for arm in ('B2_raw','C2_semantic'):
        for kind in ('correct','mutant'):
            selected=[j for j in bmc if j['arm']==arm and (j['source']=='correct')==(kind=='correct')]
            good=[j for j in selected if j in reproduced];bad=[j for j in selected if j in unresolved]
            table.append(dict(arm=arm,DUT_kind=kind,native_BMC_FAIL=len(selected),physical_alarm_reproduced=len(good),not_reproduced=len(bad),reference_prefix_FAIL=len(good),reference_verdict_not_recorded=len(bad),same_sample_category_reference_confirmation=0))
    source=paths['candidate'][0].read_text().splitlines();smt=paths['smt'][0].read_text().splitlines()
    prep=paths['smt'][0].parent/'design_prep.ys';prep_lines=prep.read_text().splitlines()
    assert "(^s_data===1'bx)" in source[72]
    assert 'yosys-smt2-anyseq formal_top#16' in smt[84] and 'auto$setundef' in smt[84]
    assert 'formal_top#405' in smt[1228] and 'formal_top#16' in smt[1228] and '$eqx$candidate.sv:73' in smt[1228]
    assert any('setundef -undriven -anyseq' in line for line in prep_lines)
    x=dict(candidate_line_73=source[72],smt_lines_85_89=smt[84:89],smt_line_1229=smt[1228],
           preparation_commands=[line for line in prep_lines if 'setundef' in line],
           observed_physical_result=load(paths['physical'][0]),
           interpretation='Confirmed one representation example: the literal X used by the four-state SV unknown-data test is represented as formal anyseq#16 in this saved SMT comparison. This does not establish a common root cause for all74 unreproduced alarms; their old unresolved statuses remain.',
           selected_alarm_reference_attribution='UNRESOLVED; the reference only checks an earlier physical prefix, not the selected pre-sample/category')
    extra=[formal,prep,BASE/'results/controller-done-live-acceptance-v3/audit.json',BASE/'results/controller-done-live-grade-v2/scores.json',BASE/'results/controller-done-live-replay-grade-v2/scores.json',BASE/'results/controller-done-live-report-v3/report.md',BASE/'results/controller-done-live-report-v3/manifest.json',BASE/'results/controller-done-live-v2/calls.jsonl',BASE/'results/controller-done-live-v2/api-dispatch.jsonl']
    inputs={str(p.relative_to(ROOT)):sha(p) for p,h in paths.values()}
    inputs.update({str(p.relative_to(ROOT)):sha(p) for p in extra})
    result=dict(status='P01_R1_REPORTING_ANALYSIS_READY_FOR_P02',native_jobs=len(jobs),native_statuses=states,native_FAIL_by_mode=fails,
        BMC_chain_summary=table,BMC_FAIL_total=94,physical_alarm_reproduced=20,not_reproduced=74,
        not_reproduced_scope=dict(arm='C2_semantic',correct=7,mutant=67),reference_prefix_verdicts=dict(FAIL=20,not_evaluated_or_recorded_after_bridge_rejection=74),
        x_representation_example=x,automatic_audit_limits=dict(R2='v3 does not independently close the full VCD-to-physical-to-MON-to-reference chain; P01 independently checked this batch',R3='v3 lacks complete returned-event/calls bijection; P01 checked36calls/144events for this batch; automatic gap remains open'),
        cache_limit=dict(shared_builds=26,shared_build_seconds=30.54816608224064,max_final_seconds=652.0915609993972,overall_seconds_per_final=720,NOT_RUN_TOTAL_CAP=0,future_order_effect_not_excluded=True),
        input_sha256=inputs,producer_sha256=sha(__file__),old_scores_changed=False,new_API_calls=0,new_DUT_simulations=0,new_monitor_replays=0,new_formal_jobs=0,
        independent_review='P01_CHANGES_REQUIRED; reporting fix awaits P02, not self-accepted')
    out.mkdir(parents=True,exist_ok=False);dump(out/'analysis.json',result)
    dump(out/'manifest.json',dict(analysis_sha256=sha(out/'analysis.json'),producer_sha256=sha(__file__),input_sha256=inputs))
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=analyze(a.output.resolve())
    print(r['status'],r['native_FAIL_by_mode'],r['BMC_chain_summary'])
