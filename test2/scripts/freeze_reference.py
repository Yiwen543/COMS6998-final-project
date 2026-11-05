#!/usr/bin/env python3
"""Freeze immutable Claude reference with review disposition; NOT a live release."""
import argparse
import json
from pathlib import Path
import shutil
from common import BASE,ROOT,dump,sha

def freeze(candidate,review,evaluation,out):
    author=json.loads((candidate/'metadata.json').read_text())
    reviewer=json.loads((review/'metadata.json').read_text())
    verdict=json.loads((review/'review.json').read_text())
    evidence=json.loads((evaluation/'summary.json').read_text())
    if not evidence['ready_for_read_only_review'] or evidence['selftests'].get('passed') is not True:
        raise ValueError('Reference controls did not pass')
    if verdict['decision']!='accept_with_scope' or any(f['severity']=='blocking' for f in verdict['findings']):
        raise ValueError('Independent review not accepted')
    if author['session_id']==reviewer['session_id']:raise ValueError('Review was not independent')
    for info in (author,reviewer):
        if set(info['model_usage'])!={'claude-opus-5-5'}:raise ValueError('Unexpected reference model')
    for name,h in author['artifact_sha256'].items():
        if sha(candidate/name)!=h:raise ValueError('Claude source changed')
    if evidence['checker_sha256']!=sha(candidate/'checker.py'):raise ValueError('Wrong evaluated source')
    review_packet=json.loads((BASE/'reference/review-packet-v1/manifest.json').read_text())
    if review_packet['checker_sha256']!=sha(candidate/'checker.py') or reviewer['prompt_sha256']!=review_packet['prompt_sha256']:
        raise ValueError('Review does not bind this checker')
    out.mkdir(parents=True,exist_ok=False)
    for name in author['artifact_sha256']:shutil.copyfile(candidate/name,out/name)
    disposition={'accepted_scope':verdict['accepted_scope'],
        'required_reporting_changes':{'P6':'indirect only; never independent activated property or event',
            'checks':'author_checks, unknown_comparisons, definite_comparisons separately recorded',
            'eligibility':'per simulator; M02/final_boundary is not an Icarus confirmed detection'},
        'optional_controls':'Four new independent controls all passed; fixed model inputs/mutants unchanged',
        'cycle_label_scope':'Frozen driver/parser requires zero then consecutive cycles; reference alone accepts arbitrary consecutive labels',
        'invalid_input_policy':'Retain raw partial findings for audit, exclude from authoritative scoring',
        'limitations':['Finite-trace reference validation only; no complete specification proof',
                       'Selftests share authorship; independence relies on control fixtures and separate review session',
                       'Review saw full finite controls but summaries of DUT/mutant results',
                       'No changes to Claude checker, selftests, contract or property metadata']}
    dump(out/'scope-and-disposition.json',disposition)
    eligibility=[]
    for e in evidence['fault_eligibility']:
        eligibility.append({'mutant':e['mutant'],'trace':e['trace'],
            'eligible':e['eligible_by_simulator']['verilator_two_state'],
            'eligible_by_simulator':e['eligible_by_simulator'],
            'verdict_by_simulator':{'verilator':e['two_state_reference_verdict'],'icarus':e['icarus_reference_verdict']},
            'first_reference_failure':e['first_reference_failure']})
    dump(out/'fault-eligibility.json',eligibility)
    files=[BASE/'configs/registration_v1.json',BASE/'configs/phase1_addendum_v1.json',
        BASE/'configs/input_manifest_v1.json',candidate/'metadata.json',review/'metadata.json',review/'review.json',
        evaluation/'summary.json',evaluation/'evaluations.json',BASE/'private/reference-controls-v1.json',
        BASE/'private/reference-controls-supplement-v1.json',Path(__file__),BASE/'scripts/evaluate_reference.py']
    files+=list(out.glob('*'))
    manifest={'status':'reference_frozen_for_registered_fixed_traces_only','not_live_freeze':True,
        'author_session_id':author['session_id'],'review_session_id':reviewer['session_id'],
        'reference_checker_sha256':sha(out/'checker.py'),
        'artifact_sha256':{str(p.relative_to(ROOT)):sha(p) for p in files},
        'correct_control_cases':len(evidence['correct_control_verdicts']),
        'independent_control_cases':len(evidence['independent_controls']),
        'eligible_pairs_two_state':sum(e['eligible'] for e in eligibility),
        'eligible_pairs_icarus':sum(e['eligible_by_simulator']['icarus_four_state_observations'] for e in eligibility)}
    dump(out/'freeze.json',manifest)
    return {k:manifest[k] for k in ('status','reference_checker_sha256','independent_control_cases','eligible_pairs_two_state','eligible_pairs_icarus')}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('candidate','review','evaluation','output'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();print(json.dumps(freeze(a.candidate.resolve(),a.review.resolve(),a.evaluation.resolve(),a.output.resolve()),indent=2))
