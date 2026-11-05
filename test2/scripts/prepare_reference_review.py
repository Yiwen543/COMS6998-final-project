#!/usr/bin/env python3
"""Build an independent review packet with lossless finite controls, not DUT code."""
import argparse
import json
from pathlib import Path
from common import BASE, dump, sha
from feedback import pack_rows

def unpack(packed):
    rows=[]
    for values in packed['rows']:
        d=dict(zip(packed['columns'],values))
        rows.append({'cycle':d['cycle'],'action':{'reset':d['reset'],'wr':d['wr'],'rd':d['rd'],'data':d['input_data']},
                     **{p:{k:d[f'{p}_{k}'] for k in ('fill','full','empty','data')} for p in ('pre','post')}})
    return rows

def prepare(candidate,evaluation,out):
    out.mkdir(parents=True,exist_ok=False)
    report=json.loads((evaluation/'evaluations.json').read_text())
    controls=json.loads((BASE/'private/reference-controls-v1.json').read_text())
    packed={}
    for name,c in controls.items():
        # Malformed-input controls use raw rows; the compact schema cannot
        # represent an extra/missing field without accidentally repairing it.
        if c['expected_verdict']=='INVALID_INPUT':
            packed[name]={'rows':c['rows']}
        else:
            p=pack_rows(c['rows']);assert unpack(p)==c['rows'];packed[name]={'packed_rows':p}
        packed[name].update(expected_verdict=c['expected_verdict'],actual_result=report['cases']['independent/'+name])
    payload={'scope':'Independent read-only reference-checker review BEFORE any experimental candidate generation. No DUT implementation, hidden mutation sites, or model rankings supplied.',
        'specification':(BASE/'public/specification.md').read_text(),
        'interface':(BASE/'public/observer_contract.md').read_text(),
        'checker_source':(candidate/'checker.py').read_text(),'selftest_source':(candidate/'selftest.py').read_text(),
        'author_contract':(candidate/'contract.md').read_text(),'properties':json.loads((candidate/'properties.json').read_text()),
        'author_selftest_results':report['selftests'],'independent_complete_controls':packed,
        'simulation_summary':json.loads((evaluation/'summary.json').read_text()),
        'limits':['Finite controls are not a complete proof. Implementation equivalence is not specification correctness.',
                  'You have complete independent finite controls but only summaries of real-DUT and mutant traces.',
                  'Driver enforces cycle zero then consecutive steps; check_rows must not silently ignore gaps.',
                  'Initial pre phase excluded; nonempty data unknown unresolved, prior definite failures retained.',
                  'Do not strengthen the legal-input assumptions or eliminate unobserved faults to manufacture recall.']}
    prompt='''Review this reference checker independently against the supplied specification and fixed interface.
Do not rewrite code, use tools, or evaluate any B/C model arm. Return JSON only:
{"decision":"accept_with_scope" or "reject", "findings":[{"severity":"blocking" or "limitation" or "info", "issue":"...", "evidence":"..."}], "accepted_scope":"...", "required_changes":["..."]}.
Check reset timing, input-derived admission independent of DUT flags, simultaneous boundary operations,
ordering across wrap, unspecified empty data, unknown observations, validation, error precedence,
non-vacuity of the controls and whether event/acceptance claims exceed actual checks.
Differentiate blockers for the registered valid fixed-trace use from general interface hardening.
Never claim exhaustive proof or cross-model independence guarantees beyond actual role isolation.
Compact rows are exact column/value arrays; reconstruct logically using column names.
PACKET:\n'''+json.dumps(payload,separators=(',',':'),sort_keys=True)
    if len(prompt.encode())>160000:raise ValueError('Review packet exceeds local cap')
    (out/'prompt.txt').write_text(prompt)
    dump(out/'manifest.json',{'prompt_sha256':sha(out/'prompt.txt'),'prompt_bytes':len(prompt.encode()),
        'checker_sha256':sha(candidate/'checker.py'),'evaluation_sha256':sha(evaluation/'evaluations.json'),
        'complete_independent_controls':len(controls),'all_packed_controls_roundtrip_equal':True,
        'excluded':['DUT source','mutant source','held-out stimulus','experimental candidate results']})
    return {'bytes':len(prompt.encode()),'controls':len(controls)}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('candidate','evaluation','output'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();print(json.dumps(prepare(a.candidate.resolve(),a.evaluation.resolve(),a.output.resolve())))
