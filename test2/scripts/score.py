"""Metrics over independently labeled final cases. Never infer truth from candidate."""
def sample_time(item):
    cycle,phase=item
    return cycle*2+(phase=='post')

def score(correct_results, fault_results, eligibility, tokens):
    """fault_results keyed by (mutant,trace); eligibility is frozen oracle evidence.

    Returns raw outcomes even when suite fails soundness. No unknown is a pass.
    Caller must verify final candidate/reference/evaluation hashes before calling.
    """
    correct_alarms=sum(len(p['failures']) for r in correct_results for p in r['properties'])
    correct_unknown=sum(len(p['unknown']) for r in correct_results for p in r['properties'])
    sound=bool(correct_results) and all(r['complete'] for r in correct_results) and correct_alarms==correct_unknown==0
    activation=[sum(r['properties'][j]['checks'] for r in correct_results) for j in range(6)]
    details=[]
    for e in eligibility:
        key=(e['mutant'],e['trace']);r=fault_results.get(key)
        eligible=e['eligible']
        first=e.get('first_reference_failure')
        onset=sample_time((first['cycle'],first['phase'])) if first else None
        unknown=r is None or not r['complete'] or any(p['unknown'] for p in r['properties'])
        raw_alarm_count=sum(len(p['failures']) for p in r['properties']) if r else None
        raw_alarm=False
        if r and eligible and onset is not None:
            raw_alarm=any(sample_time(f)>=onset for p in r['properties'] for f in p['failures'])
        # Unknown values do not erase an already definite detection. Record both.
        valid_kill=sound and raw_alarm and r is not None and r['complete']
        details.append(dict(mutant=e['mutant'],trace=e['trace'],eligible=eligible,
                            raw_alarm_records=raw_alarm_count,raw_post_violation_alarm=raw_alarm,
                            valid_kill=valid_kill,unresolved=unknown))
    eligible_mutants={x['mutant'] for x in details if x['eligible']}
    killed={x['mutant'] for x in details if x['valid_kill']}
    denominator=sum(x['eligible'] for x in details)
    kills=sum(x['valid_kill'] for x in details)
    return {'suite_sound_on_fixed_controls':sound,'correct_control_alarm_records':correct_alarms,
            'correct_control_alarms_by_property':[sum(len(r['properties'][j]['failures']) for r in correct_results) for j in range(6)],
            'correct_control_unknown_records':correct_unknown,'property_activations':activation,
            'vacuous_slots':[i for i,n in enumerate(activation) if n==0],
            'eligible_mutants':sorted(eligible_mutants),'distinct_mutants_killed':sorted(killed),
            'observable_mutant_recall':len(killed)/len(eligible_mutants) if eligible_mutants else None,
            'eligible_mutant_trace_count':denominator,'valid_mutant_trace_kills':kills,
            'eligible_pair_detection_rate':kills/denominator if denominator else None,
            'api_input_plus_output_tokens':tokens,
            'distinct_mutant_kills_per_1000_tokens':len(killed)*1000/tokens if tokens else None,
            'details':details}
