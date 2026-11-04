"""Fixed environment/scope gate around the independently authored checker.

This is integration policy, not a replacement golden model. Never drop checker
failures. A clean verdict also requires valid driver execution and no observed
out-of-scope event in either sampling phase.
"""
ERR_KEYS=('nak','nak_timeout','arbitration','scl_interference','stretch_timeout','sda_unstable')


def gate_result(simulation, rows, checked):
    unsupported=[{'cycle':r['cycle'],'phase':phase,'event':key}
        for r in rows if r['action']['rst_n'] for phase in ('pre','post') for key in ERR_KEYS
        if r[phase][key]]
    passed=(simulation['environment_valid'] and checked.get('verdict')=='pass'
            and not checked['failures'] and not checked['assumption_violations']
            and not checked['unresolved'] and not unsupported)
    # Preserve raw checker events, but never promote stretch observations to a
    # proof of data-bit recovery; the independent reviewer limited that meaning.
    events=[e for e in checked['events'] if e.get('family')!='read_stretch_recovery'] if passed else []
    return {'scoped_pass':bool(passed),'unsupported_observations':unsupported,
            'credited_events':events,'raw_checker':checked,
            'stretch_event_policy':'Observation while READB current only; excluded from qualified event targets.',
            'formal_B_eligible':False}
