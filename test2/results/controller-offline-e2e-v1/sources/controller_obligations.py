"""Finite qualification stimuli and frozen-reference labels, never an oracle."""
import copy
import json
from pathlib import Path
from common import ROOT,dump,sha
from controller_monitor_live import TASK,replay
from controller_reference_evaluate import alignment_controls,finite_fixture,module
from controller_release_live import verify_release


def renumber(rows):
    for i,row in enumerate(rows):row['cycle']=i
    return rows


def tail128(rows):
    rows=copy.deepcopy(rows)
    rows.extend(copy.deepcopy(rows[-1]) for _ in range(96))
    return renumber(rows)


def fixtures():
    cases={}
    categories={'legal_exact':'legal','legal_pad':'legal','legal_truncate':'legal',
                'legal_both_stalled':'legal','legal_status_after_data':'legal','legal_status_before_data':'legal',
                'legal_reset_cancels_responses':'legal','wrong_payload':'payload_order','wrong_status':'status_fields',
                'extra_status':'status_justification','spurious_stalled_data_then_reset':'data_justification',
                'spurious_stalled_status_then_reset':'status_justification','pre_not_justified_by_current_input':'pre_acceptance',
                'unknown_payload':'unknown','missing_field':'invalid','source_changes_while_blocked':'invalid',
                'definite_failure_plus_unknown':'payload_order','cycle_gap':'invalid',
                'final_tail_32_not_128':'tail_sufficiency','final_tail_128':'legal'}
    for name,c in alignment_controls().items():
        c=copy.deepcopy(c)
        if name not in ('cycle_gap','final_tail_32_not_128','final_tail_128'):
            c['rows']=tail128(c['rows'])
        c.update(obligation=categories[name],min_tail=128,physically_reached=False,provenance='Existing explicit finite control extended by96 identical quiet rows; not new RTL simulation')
        cases[name]=c
    exact=finite_fixture([11,22,33,44],[11,22,33,44],(0,0,4,4))
    exact=tail128(exact)
    def add(name,obligation,rows,expect='FAIL'):
        cases[name]=dict(rows=renumber(rows),expected_verdict=expect,require_drained=True,min_tail=128,
                         obligation=obligation,physically_reached=False,provenance='Explicit finite qualification example, not a mutant/hidden model trial')
    for channel in ('data','status','both'):
        rows=copy.deepcopy(exact)
        for r in rows:
            for p in ('pre','post'):
                if channel in ('data','both'):r[p]['m_valid']=0
                if channel in ('status','both'):r[p]['h_valid']=0
        add('missing_'+channel+'_response','completion_'+channel,rows)
    # Source offers a final byte until the end, but it never becomes accepted.
    rows=copy.deepcopy(exact[:2])
    for _ in range(136):
        r=copy.deepcopy(exact[-1]);r['inputs'].update(s_valid=1,s_data=71,s_last=1)
        r['pre'].update(s_ready=0);r['post'].update(s_ready=0);rows.append(r)
    add('input_never_accepted','completion_input',rows)
    rows=copy.deepcopy(exact)
    for r in rows:
        for p in ('pre','post'):
            if r[p]['m_valid']:r[p]['m_last']=0
    add('missing_last_marker','data_last',rows)
    rows=copy.deepcopy(exact);rows[5]['post']['m_last']=1;rows[6]['pre']['m_last']=1
    add('premature_last_marker','data_last',rows)
    rows=copy.deepcopy(cases['legal_both_stalled']['rows'])
    rows[6]['post']['m_data']=77;rows[7]['pre']['m_data']=77
    add('data_changes_while_stalled','data_stall',rows)
    rows=copy.deepcopy(cases['legal_both_stalled']['rows'])
    rows[6]['post']['h_length']=7;rows[7]['pre']['h_length']=7
    add('status_changes_while_stalled','status_stall',rows)
    rows=copy.deepcopy(cases['legal_reset_cancels_responses']['rows'])
    rows[6]['post'].update(m_valid=1,m_data=11,m_last=0)
    rows[7]['pre'].update(m_valid=1,m_data=11,m_last=0)
    add('reset_does_not_clear_data','reset',rows)
    rows=copy.deepcopy(cases['legal_reset_cancels_responses']['rows'])
    header=dict(h_valid=1,h_length=4,h_original_length=4,h_pad=0,h_truncate=0)
    rows[6]['post'].update(header);rows[7]['pre'].update(header)
    add('reset_does_not_clear_status','reset',rows)
    # Keep a legal ready-low interval, then deliver exactly the saved responses.
    rows=copy.deepcopy(exact);start=6
    stalled=copy.deepcopy(rows[start]);stalled['inputs'].update(m_ready=0,h_ready=0);stalled['post']=copy.deepcopy(stalled['pre'])
    rows[start:start]=[copy.deepcopy(stalled) for _ in range(140)]
    add('legal_long_sink_stall','legal',rows,'PASS')
    rows=copy.deepcopy(exact);rows[5]['post']['h_original_length']=-1;rows[6]['pre']['h_original_length']=-1
    add('unknown_status','unknown',rows,'UNRESOLVED')
    return cases


def prepare(out):
    out.mkdir(parents=True,exist_ok=False)
    cases=fixtures();dump(out/'fixtures.json',cases)
    checker=module(TASK/'reference/frozen-v2/checker.py','qualified_claude_reference')
    labels={};mismatches=[]
    for name,c in cases.items():
        r=checker.check_rows(c['rows'],require_drained=c['require_drained'],min_tail=c['min_tail'])
        labels[name]=r
        if r['verdict']!=c['expected_verdict']:mismatches.append(dict(case=name,intended=c['expected_verdict'],actual=r['verdict']))
    dump(out/'reference-labels.json',labels)
    manifest=dict(status='passed' if not mismatches else 'reference_fixture_mismatch',mismatches=mismatches,cases=len(cases),
                  fixtures_sha256=sha(out/'fixtures.json'),labels_sha256=sha(out/'reference-labels.json'),
                  checker_sha256=sha(TASK/'reference/frozen-v2/checker.py'),producer_sha256=sha(__file__),
                  scope='Post-hoc qualification controls; no GPT grading oracle, new model evidence or RTL coverage')
    dump(out/'manifest.json',manifest)
    return manifest


def evaluate(run_root,control_dir,out):
    snapshots=verify_release(run_root);manifest=json.loads((control_dir/'manifest.json').read_text())
    if manifest['status']!='passed':raise ValueError('Fixture/reference qualification did not pass')
    if sha(control_dir/'fixtures.json')!=manifest['fixtures_sha256'] or sha(control_dir/'reference-labels.json')!=manifest['labels_sha256']:
        raise ValueError('Frozen qualification controls changed')
    out.mkdir(parents=True,exist_ok=False)
    cases=json.loads((control_dir/'fixtures.json').read_text());labels=json.loads((control_dir/'reference-labels.json').read_text())
    records=[];cycles=0
    for s in sorted(snapshots,key=lambda s:(s['arm'],s['repetition'],s['round'])):
        if s['status']!='compiled':
            records.append(dict(arm=s['arm'],repetition=s['repetition'],round=s['round'],status=s['status'],cases=None));continue
        result={}
        for name,c in cases.items():
            # Invalid inputs are recorded, not fed to a valid-interface monitor.
            if labels[name]['verdict']=='INVALID_INPUT':
                result[name]=dict(status='NOT_RUN_INVALID_INPUT',reference=labels[name]['verdict'],obligation=c['obligation']);continue
            d=out/s['arm']/f'rep{s["repetition"]}'/f'round{s["round"]}'/name
            r=replay(run_root/s['directory']/'compiled',c['rows'],d,out/'row-cache');cycles+=r['cycles']
            alarms=[f for p in r['properties'] for f in p['failures']]
            unknown=sum(len(p['unknown']) for p in r['properties'])
            verdict=labels[name]['verdict'];first=labels[name]['failures'][0] if labels[name]['failures'] else None
            onset=(first['cycle']*2+(first['phase']=='post')) if first and first['phase'] in ('pre','post') else None
            early=onset is not None and any(t*2+(phase=='post')<onset for t,phase in alarms)
            result[name]=dict(status='complete' if r['complete'] else 'incomplete',reference=verdict,obligation=c['obligation'],
                              alarm_records=len(alarms),unknown_records=unknown,first_alarm=min(alarms,key=lambda x:x[0]*2+(x[1]=='post')) if alarms else None,
                              early_before_sampled_reference_failure=early,
                              detected_reference_failure=bool(verdict=='FAIL' and r['complete'] and alarms and not early),
                              unresolved=verdict=='UNRESOLVED' or unknown>0 or not r['complete'],
                              oracle_failure_phase=first['phase'] if first else None)
        records.append(dict(arm=s['arm'],repetition=s['repetition'],round=s['round'],status=s['status'],cases=result))
        print(f'obligations {s["arm"]} rep{s["repetition"]} round{s["round"]}',flush=True)
    dump(out/'matrix.json',dict(records=records,cycles=cycles,control_manifest_sha256=sha(control_dir/'manifest.json'),
                               old_scores_unchanged=True,new_independent_model_trials=0,API_calls=0,
                               end_phase_failures_are_finite_completion_not_sampled_safety=True))
    verify_release(run_root)
    return out/'matrix.json'
