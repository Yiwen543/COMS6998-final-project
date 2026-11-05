"""Separate registration and gated freeze; never modifies a historical experiment."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

from wbxbar_reference_experiment import (BASE, REG, FREEZE, REPLAY_FREEZE, CANDIDATE,
    ROOT, FIXED_FIELDS, read, sha, verify_original, verify_registration, verify_freeze)
from replay_wbxbar_cancel import verify_replay_freeze
from freeze_wbxbar_reference_replay import verify_registration as verify_replay_registration

NEW_SOURCES = ['wbxbar_reference_experiment', 'prepare_wbxbar_reference_bc',
               'run_wbxbar_reference_bc', 'audit_wbxbar_reference_bc',
               'report_wbxbar_reference_bc']


def write_new(path, value):
    if path.exists():
        raise ValueError('Never overwrite: ' + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def register():
    original = verify_original()
    replay, _ = verify_replay_freeze(REPLAY_FREEZE)
    verify_replay_registration(ROOT / replay['registration'])
    previous = ROOT / 'results/wbxbar_reference_replay_20261104'
    audit = read(previous / 'audit-v1/audit.json')
    validation = read(previous / 'validation.json')
    if audit.get('pass') is not True or validation.get('pass') is not True:
        raise ValueError('Saved-action replay prerequisite not passed')
    for path, digest in validation['artifact_hashes'].items():
        if sha(ROOT / path) != digest:
            raise ValueError('Replay validation evidence drift: ' + path)
    files = [p for p in previous.rglob('*') if p.is_file()]
    files += [REPLAY_FREEZE, ROOT / replay['registration']]
    value = {key: original[key] for key in FIXED_FIELDS}
    value.update(id='wbxbar_reference_bc_v1', status='registered_before_new_live_calls',
        created_utc=datetime.now(timezone.utc).isoformat(),
        user_authorization='Fresh B/C after audited replay, original budget/targets/roles, independent model sessions and all unresolved results retained.',
        classification='Exploratory known-easy reliability/feedback control; not a new difficulty-screen pass.',
        known_prior_information='Earlier WBXBAR live sessions hit all 17 targets in round 1. Revised-checker retrospective replay left all six finals unresolved. Selection is not blind to those historical outcomes; none of their stimuli/results or private controls enters prompts.',
        difficulty_waiver='User explicitly requested this same-scope B/C. Preserve the original failed ordinary/difficulty gate; no new B-before-C admission claim.',
        checker_candidate=str(CANDIDATE.relative_to(ROOT)), checker_sha256=sha(CANDIDATE / 'checker.py'),
        checker_contract_sha256=sha(CANDIDATE / 'contract.md'),
        roles={'checker': 'Previously authored/reviewed/frozen Claude contract and checker; no edits.',
               'stimulus': 'Exact gpt-6.1-sol proposes JSON cycle actions only.',
               'driver_and_measurement': 'GPT/Codex fixed infrastructure; no solver/calibration stimulus in prompts.'},
        primary_comparison='C versus B within this new run; original trials remain separate historical evidence.',
        endpoints={'raw_target': 'First fresh complete batch hitting all 17 separate counters; not reached retained.',
                   'functional_target': 'Raw target plus delivery complete and scoped_pass; unresolved never counted as passed.',
                   'costs': 'Input+output tokens, all physical replay cycles, executions, compile/simulation/preprocessing/wall time.',
                   'token_roi': 'New DUT branch points since seed per 1000 API input+output tokens; token subsets not double-counted.'},
        failure_policy='Retain failed attempts, checker alarms, unknowns and exclusions. No early stop for target attainment or unresolved verdict. Input/measurement infrastructure failures explicitly marked.',
        session_independence='Six fresh local UUIDs, stateless Responses requests with store=False, no conversation/previous_response_id. Only current arm/repetition history; no old live actions.',
        feedback_policy='Reuse original lossless RTL/semantic representation and diagnostics selection: full raw results on disk, totals and first eight per category in prompts equally for B/C; latest 64 actions and 16 trace rows.',
        evidence_hashes={str(p.relative_to(ROOT)): sha(p) for p in sorted(files)},
        git_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        working_tree_dirty=bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True)))
    write_new(REG, value)
    verify_registration()
    return {'registration': str(REG.relative_to(ROOT)), 'sha256': sha(REG)}


def prepare(output, validation=None):
    reg = verify_registration()
    original = verify_original()
    replay, _ = verify_replay_freeze(REPLAY_FREEZE)
    bound = {**original['hashes'], **replay['hashes'], str(REG.relative_to(ROOT)): sha(REG),
             str(REPLAY_FREEZE.relative_to(ROOT)): sha(REPLAY_FREEZE)}
    paths = [ROOT / f'scripts/{name}.py' for name in NEW_SOURCES]
    paths += [ROOT / 'scripts/report_wbxbar_bc.py', ROOT / 'scripts/plot_wbxbar_costs.py',
              ROOT / 'tests/test_wbxbar_reference_bc.py']
    bound.update({str(p.relative_to(ROOT)): sha(p) for p in paths})
    live = validation is not None
    if live:
        value = read(validation)
        if value.get('pass') is not True or value['registration_sha256'] != sha(REG):
            raise ValueError('Runner validation not passed')
        for path, digest in value['hashes'].items():
            if sha(ROOT / path) != digest:
                raise ValueError('Runner validation drift: ' + path)
        bound[str(validation.relative_to(ROOT))] = sha(validation)
        bound.update(value['hashes'])
    config = {**reg, 'status': 'live_frozen' if live else 'offline_prepared',
        'registration_sha256': sha(REG), 'offline_gate_pass': True,
        'live_B_allowed': live, 'live_C_allowed': live, 'hashes': bound,
        'runner_validation': str(validation.relative_to(ROOT)) if live else None,
        'review_limitations': replay['limits'], 'nonblocking_documentation_notes': replay['nonblocking_documentation_notes']}
    write_new(output, config)
    verify_freeze(output)
    return {'config': str(output.relative_to(ROOT)), 'sha256': sha(output), 'live_allowed': live}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('stage', choices=['register', 'offline', 'freeze'])
    p.add_argument('--output', type=Path)
    p.add_argument('--validation', type=Path)
    a = p.parse_args()
    if a.stage == 'register':
        result = register()
    elif a.stage == 'offline':
        result = prepare((a.output or BASE / 'offline-config.json').resolve())
    else:
        if a.validation is None:
            p.error('freeze requires --validation')
        result = prepare((a.output or FREEZE).resolve(), a.validation.resolve())
    print(json.dumps(result, indent=2))
