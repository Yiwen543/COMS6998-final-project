"""Shared case binding, raw evidence parsing and conservative detection accounting."""
from collections import Counter
import hashlib
import json
import re
from controller_done_runtime import check_rows

CATEGORIES=('safety','response_completion','input_completion')


def position(p):return p[0],0 if p[1]=='pre' else 1


def base(label):
    eligible=dict(safety=bool(label.get('first_safety_failure')),response_completion=bool(label.get('end_only') and label.get('response_completion')),input_completion=bool(label.get('input_completion')))
    return dict(source=label['source'],simulator=label['simulator'],trace=label.get('trace'),reference_status=label.get('status'),
        oracle_verdict=label.get('verdict'),oracle_unknown_records=label.get('unknown_records'),eligible=eligible,
        status='not_graded',complete=False,is_unresolved=True,vacuous=None,
        alarm_samples_including_marker=None,first_alarm_including_marker=None,candidate_unknown_samples_including_marker=None,
        ordinary_alarm_samples=None,marker_alarm=None,early_safety_alarms_including_marker=None,early_finite_alarm_samples=None,
        physical_reference_PASS_alarm_including_marker=None,marker_only_safety_signal=False,
        definite_detection={k:False for k in CATEGORIES},fully_resolved_detection={k:False for k in CATEGORIES},
        category_attribution='UNATTRIBUTED_ANY_SLOT case eligibility, not slot/category proof')


def unresolved(label,status,original_case=None,error_type=None):
    row=base(label);row['status']=status
    if original_case is not None:row['carried_saved_case']=original_case
    if error_type is not None:row['error_type']=error_type
    return row


def parse_evidence(result,raw,cycles):
    if hashlib.sha256(raw).hexdigest()!=result['raw_log_sha256']:raise ValueError('raw_log_hash_mismatch')
    samples=[]
    for line in raw.decode().splitlines():
        if not line.startswith('MON '):continue
        w=line.split()
        if len(w)!=5 or w[2] not in ('pre','post') or not all(re.fullmatch('[01xz]{6}',v) for v in w[3:]):raise ValueError('malformed_raw_sample')
        samples.append((int(w[1]),w[2],w[3],w[4]))
    expected=[(i,p) for i in range(cycles) for p in ('pre','post') if i or p=='post']
    seen=[(v[0],v[1]) for v in samples]
    if seen!=expected[:len(seen)]:raise ValueError('raw_sample_order_or_range')
    if result['samples']!=len(samples) or result['cycles']!=sum(s[1]=='post' for s in samples):raise ValueError('raw_cycle_accounting')
    if result['complete'] and (seen!=expected or b'REPLAY_COMPLETE' not in raw):raise ValueError('false_complete_replay')
    if len(result['properties'])!=6:raise ValueError('missing_property_slots')
    for slot,p in enumerate(result['properties']):
        failures=[];unknown=[];checks=0;end_checks=0
        for i,phase,a,k in samples:
            active,ok=a[5-slot],k[5-slot];sample=[i,phase]
            if active not in '01' or active=='1' and ok not in '01':unknown.append(sample)
            elif active=='1':
                checks+=1;end_checks+=int(sample==[cycles-1,'post'])
                if ok=='0':failures.append(sample)
        if p['id']!=f'P{slot}' or (p['checks'],p['failures'],p['unknown'])!=(checks,failures,unknown):raise ValueError('raw_property_accounting')
        if 'end_sample_checks' in p and p['end_sample_checks']!=end_checks:raise ValueError('raw_marker_accounting')
    return samples


def grade(label,rows_blob,result,raw):
    """Every backend uses this function; mismatched input is a retained unresolved case."""
    if label.get('status')!='complete':return unresolved(label,'reference_infrastructure_unresolved')
    try:
        if hashlib.sha256(rows_blob).hexdigest()!=label['rows_sha256']:raise ValueError('qualified_rows_file_mismatch')
        rows=json.loads(rows_blob);check_rows(rows);n=len(rows)
        if type(label.get('unknown_records'))!=int or label['unknown_records']<0 or label.get('verdict') not in ('PASS','FAIL','UNRESOLVED','INVALID_INPUT'):raise ValueError('invalid_reference_label')
        if any(base(label)['eligible'].values()) and label['verdict']!='FAIL':raise ValueError('inconsistent_reference_failure_label')
        if type(label['cycles'])!=int or type(result['attempted_cycles'])!=int or not label['cycles']==result['attempted_cycles']==n:raise ValueError('label_replay_cycle_mismatch')
        canonical=json.dumps(rows,separators=(',',':'),sort_keys=True).encode()
        if hashlib.sha256(canonical).hexdigest()!=result['rows_sha256']:raise ValueError('canonical_rows_hash_mismatch')
        if result['trace_done_sample']!=[n-1,'post'] or result.get('safety_projection'):raise ValueError('marker_scope_mismatch')
        first=label.get('first_safety_failure')
        if first and (type(first['cycle'])!=int or first['phase'] not in ('pre','post') or not 0<=first['cycle']<n or (first['cycle']==0 and first['phase']=='pre')):raise ValueError('invalid_reference_onset')
        parse_evidence(result,raw,n)
    except (ValueError,TypeError,KeyError,UnicodeError) as error:return unresolved(label,'replay_binding_unresolved',error_type=type(error).__name__+':'+str(error))
    row=base(label);end=(n-1,'post');alarms=sorted({tuple(x) for p in result['properties'] for x in p['failures']},key=position)
    unknown=sorted({tuple(x) for p in result['properties'] for x in p['unknown']},key=position)
    ordinary=[p for p in alarms if p!=end];early_end=[p for p in alarms if position(p)<position(end)];early_safety=[]
    if first:
        onset=(first['cycle'],first['phase']);early_safety=[p for p in alarms if position(p)<position(onset)]
        row['definite_detection']['safety']=result['complete'] and not early_safety and any(position(p)>=position(onset) for p in ordinary)
    for category in ('response_completion','input_completion'):
        row['definite_detection'][category]=bool(row['eligible'][category] and result['complete'] and end in alarms and not early_end)
    is_unresolved=not result['complete'] or bool(unknown) or bool(label.get('unknown_records')) or label.get('verdict') not in ('PASS','FAIL')
    row.update(status='graded' if result['complete'] else 'replay_infrastructure_unresolved',complete=result['complete'],is_unresolved=is_unresolved,
        vacuous=not any(p['checks'] for p in result['properties']),alarm_samples_including_marker=len(alarms),
        first_alarm_including_marker=list(alarms[0]) if alarms else None,candidate_unknown_samples_including_marker=len(unknown),
        ordinary_alarm_samples=len(ordinary),marker_alarm=end in alarms,early_finite_alarm_samples=len(early_end),
        early_safety_alarms_including_marker=len(early_safety),physical_reference_PASS_alarm_including_marker=label.get('verdict')=='PASS' and bool(alarms),
        marker_only_safety_signal=bool(first and result['complete'] and end in alarms and not ordinary),
        fully_resolved_detection={k:bool(v and not is_unresolved) for k,v in row['definite_detection'].items()})
    return row


def oracle_by_type(labels):
    result={}
    for source in sorted({r['source'] for r in labels if r['source']!='correct'}):
        values=[r for r in labels if r['source']==source]
        result[source]=dict(raw_pairs=len(values),verdicts=dict(Counter(r.get('oracle_verdict') or 'UNKNOWN' for r in values)),
            oracle_unknown_pairs=sum(bool(r.get('oracle_unknown_records')) for r in values),
            FAIL_with_oracle_unknown_pairs=sum(r.get('oracle_verdict')=='FAIL' and bool(r.get('oracle_unknown_records')) for r in values),
            FAIL_without_oracle_unknown_pairs=sum(r.get('oracle_verdict')=='FAIL' and not r.get('oracle_unknown_records') for r in values))
    return result


def summarize(cases):
    correct=[r for r in cases if r['source']=='correct'];gate=len(correct)==18 and all(r['status']=='graded' and r['oracle_verdict']=='PASS' and not r['is_unresolved'] and r['alarm_samples_including_marker']==0 for r in correct)
    categories={}
    for category in CATEGORIES:
        eligible=[r for r in cases if r['source']!='correct' and r['eligible'][category]]
        detected=[r for r in eligible if gate and r['definite_detection'][category]];resolved=[r for r in eligible if gate and r['fully_resolved_detection'][category]]
        categories[category]=dict(eligible_pairs=len(eligible),definite_pairs=len(detected),fully_resolved_pairs=len(resolved),definite_types=sorted({r['source'] for r in detected}),fully_resolved_types=sorted({r['source'] for r in resolved}))
    paths=dict(ordinary_safety=categories['safety']['definite_types'],end_marker_finite_UNATTRIBUTED=sorted(set(categories['response_completion']['definite_types'])|set(categories['input_completion']['definite_types'])))
    return dict(correct_control_gate=gate,raw_fault_pairs=sum(r['source']!='correct' for r in cases),raw_fault_types=len({r['source'] for r in cases if r['source']!='correct'}),categories=categories,
        status_counts=dict(Counter(r['status'] for r in cases)),oracle_unknown_pairs=sum(bool(r.get('oracle_unknown_records')) for r in cases),
        candidate_unknown_pairs=sum(bool(r.get('candidate_unknown_samples_including_marker')) for r in cases),unresolved_pairs=sum(r['is_unresolved'] for r in cases),
        marker_only_safety_signal_pairs=sum(r['marker_only_safety_signal'] for r in cases),
        oracle_FAIL_any_unknown_context_types=sorted({r['source'] for r in cases if r['source']!='correct' and r['oracle_verdict']=='FAIL'}),
        detection_types_by_credit_path=paths,union_definite_types_UNATTRIBUTED=sorted(set(paths['ordinary_safety'])|set(paths['end_marker_finite_UNATTRIBUTED'])),
        oracle_unknown_by_type=oracle_by_type(cases),union_scope='Union includes unattributed end-marker case detections, not category-specific monitor proofs')
