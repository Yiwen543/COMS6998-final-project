"""Execute only the frozen R01 profile after an exact P10/EXECUTE receipt.

No provider SDK, secret staging, old runner or old checker is imported.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import time
from budget import Budget, Refuse
from observations import (Unqualified, need, parse_rows, parse_vcd,
                          bind_physical_vcd, selected_native_alarm, eligibility, phase_binding)
from runtime import execute

ROOT = Path(__file__).resolve().parents[2]
REGISTRATION = ROOT / 'test2/configs/g1_qualification_registration_v1.json'


def digest(path):
    need(not path.is_symlink(), 'SYMLINK_NOT_ALLOWED:' + str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def review_gate(receipt):
    gate = load(receipt)
    need(gate['record_kind'] == 'G1_EXECUTE_AFTER_READONLY_P10', 'WRONG_GATE_KIND')
    need(gate['stage'] == 'EXECUTE', 'NO_EXECUTE_STAGE')
    need(gate['registration_sha256'] == digest(REGISTRATION), 'REGISTRATION_DRIFT')
    reg = load(REGISTRATION)
    manifest_path = ROOT / reg['source_manifest']
    need(gate['source_manifest_sha256'] == digest(manifest_path), 'SOURCE_MANIFEST_DRIFT')
    need(gate['user_authorization_sha256'] == digest(ROOT / reg['user_authorization']), 'GRANT_DRIFT')
    review_path = (ROOT / gate['p10_review_path']).resolve()
    allowed = ROOT / 'docs/audits/agent_bridge_2026-11-06'
    need(review_path.is_relative_to(allowed), 'P10_REVIEW_LOCATION')
    need(digest(review_path) == gate['p10_review_sha256'], 'P10_REVIEW_DRIFT')
    review = load(review_path)
    need(review['status'] in ['PASS', 'PASS_WITH_LIMITS'], 'P10_NOT_ACCEPTED')
    need(review['phase'].startswith('P10'), 'NOT_A_P10_REVIEW')
    r01_manifest = ROOT / reg['r01_snapshot_manifest']
    need(gate['r01_manifest_sha256'] == digest(r01_manifest), 'R01_MANIFEST_DRIFT')
    need(review['input_identity']['producer_manifest_sha256'] == digest(r01_manifest),
         'P10_REVIEW_WRONG_R01')
    need(review['input_identity']['registration_sha256'] == digest(REGISTRATION),
         'P10_REVIEW_WRONG_REGISTRATION')
    for path, expected in load(manifest_path)['files'].items():
        need(digest(ROOT / path) == expected, 'FROZEN_INPUT_DRIFT:' + path)
    return reg, gate


def classify_native(folder, mode):
    text = (folder / 'stdout.log').read_text() + (folder / 'stderr.log').read_text()
    matches = re.findall(r'Status:\s*(PASSED|FAILED)', text)
    need(bool(matches), 'NATIVE_STATUS_ABSENT')
    return 'PASS' if matches[-1] == 'PASSED' else ('FAIL' if mode == 'bmc' else 'NOT_REACHED')


def main(receipt):
    reg, gate = review_gate(receipt)  # metadata gate, no tools executed
    root = ROOT / reg['result_root']
    ledger_path = root / 'execution-state.json'
    budget = Budget(ledger_path, reg['caps'])  # one start, one pool; existing state refuses
    jobs = load(ROOT / reg['job_plan'])['jobs']
    results = {j['id']: {'status': 'NOT_RUN', 'reason': 'NOT_DISPATCHED'} for j in jobs}
    report = dict(profile=reg['profile'], source_manifest_sha256=gate['source_manifest_sha256'],
        registration_sha256=gate['registration_sha256'], execution_receipt_sha256=digest(receipt),
        jobs=results, controls={}, science='PUBLIC_G1_ONLY_NOT_DUT_OR_MODEL_EVALUATION',
        completion128_credit=False, independent_acceptance='PENDING_POST_REVIEW')
    env = {'PATH': '/opt/homebrew/bin:/usr/bin:/bin', 'LC_ALL': 'C', 'LANG': 'C',
        'CXX': '/usr/bin/clang++', 'CC': '/usr/bin/clang',
        'MAKE': '/usr/bin/make', 'PYTHONDONTWRITEBYTECODE': '1',
        'TMPDIR': str(root / 'tmp')}
    try:
        (root / 'tmp').mkdir(exist_ok=False)
        (root / 'jobs').mkdir(exist_ok=False)
        (root / 'build').mkdir(exist_ok=False)
        for n in range(16):
            (root / 'build' / f'QC{n:02}').mkdir()
        # Actual binary pins and versions are verified inside the shared timer.
        for name, tool in reg['tools'].items():
            need(digest(Path(tool['configured']).resolve()) == tool['resolved_sha256'],
                 'TOOL_BINARY_DRIFT:' + name)
        labels = load(ROOT / reg['controls'])['cases']
        physical = {}
        native_alarms = {}
        for original_job in jobs:
            if budget.state['halted']:
                break
            job = json.loads(json.dumps(original_job))
            folder = root / 'jobs' / job['id']
            # All paths are frozen relative paths; expansion is literal, never shell.
            job['argv'] = [arg.replace('{ROOT}', str(ROOT)).replace('{OUT}', str(root))
                           .replace('{JOB}', str(folder)) for arg in job['argv']]
            started = time.monotonic()
            process = execute(budget, job, folder, env)
            results[job['id']] = dict(process)
            if budget.state['halted']:
                break
            if job['kind'] in ['setup', 'compile']:
                need(process['exit_code'] == 0, 'SETUP_OR_COMPILATION_FAILED:' + job['id'])
                continue
            case = labels[int(job['qc'][2:])]
            if job['kind'] == 'physical':
                need(process['exit_code'] == 0, 'PHYSICAL_PROCESS_FAILED:' + job['id'])
                rows = parse_rows((folder / 'stdout.log').read_text(), case, job['simulator'])
                bind_physical_vcd(parse_vcd(folder / 'trace.vcd'), rows, case)
                physical[(case['id'], job['simulator'])] = rows
                results[job['id']]['physical_rows'] = rows
                results[job['id']]['physical_cycles_observed'] = 4
            else:
                status = classify_native(folder, job['mode'])
                need(process['exit_code'] == (0 if status == 'PASS' else 1), 'NATIVE_EXIT_STATUS_MISMATCH')
                results[job['id']]['native_status'] = status
                expected = case['native_BMC_expected'] if job['mode'] == 'bmc' else case['activation_cover_expected']
                if expected != 'DIAGNOSTIC_ONLY_ANY_RAW_STATUS':
                    need(status == expected, 'NATIVE_EXPECTATION_MISMATCH:' + case['id'] + ':' + job['mode'])
                if job['mode'] == 'bmc' and status == 'FAIL' and eligibility(case):
                    native_alarms[case['id']] = selected_native_alarm(parse_vcd(folder / 'trace.vcd'))
                    results[job['id']]['selected_registered_pre_alarm'] = native_alarms[case['id']]
            results[job['id']]['parse_and_process_seconds'] = time.monotonic() - started
            need(budget.elapsed() < reg['caps']['wall_seconds'] - 5, 'PARSE_DEADLINE')
            # Once all four jobs for a QC have returned, bind each native selected
            # registered pre sample to both physical pre rows, never post rows.
            if job['kind'] == 'physical' and job['simulator'] == 'verilator':
                cid = case['id']
                if cid in native_alarms:
                    alarm = native_alarms[cid]
                    for simulator in ['icarus', 'verilator']:
                        rows = physical[(cid, simulator)]
                        row = next(x for x in rows if x['phase'] == 'pre' and x['cycle'] == alarm['cycle'])
                        need(all(row[k] == alarm[k] for k in ['q', 'active', 'ok']),
                             'NATIVE_DELAYED_PRE_BINDING_MISMATCH:' + cid)
                observed_phase_binding = phase_binding(case)
                need(observed_phase_binding == ('REJECT' if case['phase_binding_expected'] == 'EXPECTED_REJECT'
                     else 'MATCH'), 'PHASE_REJECTION_CONTROL_MISMATCH')
                report['controls'][cid] = dict(
                    status='EXPECTED_CONTROL_OBSERVATIONS_MATCHED',
                    eligibility=case['eligibility'],
                    phase_binding_observed=observed_phase_binding,
                    qualified_real_DUT_or_oracle=False,
                    completion128_credit=False, real_DUT_oracle='UNQUALIFIED')
    except Exception as error:
        budget.halt(type(error).__name__ + ':' + str(error))
        report['execution_error'] = budget.state['halt_reason']
    finally:
        for result in results.values():
            if result['status'] == 'NOT_RUN' and budget.state['halted']:
                result['reason'] = budget.state['halt_reason']
        report['budget_snapshot_before_final_output'] = budget.state
        report['authoritative_final_budget_ledger'] = 'execution-state.json'
        report['status'] = 'HALTED_WITH_REMAINDER_NOT_RUN' if budget.state['halted'] else 'COMPLETE_PENDING_INDEPENDENT_REVIEW'
        with (root / 'report.json').open('x') as stream:
            json.dump(report, stream, indent=2)
        # Result serialization is inside the same wall deadline; recheck after write.
        if budget.elapsed() > reg['caps']['wall_seconds']:
            budget.halt('FINAL_SERIALIZATION_EXCEEDED_WALL_CAP')
        artifacts = {str(path.relative_to(root)): digest(path) for path in root.rglob('*')
                     if path.is_file() and not path.is_symlink() and '__pycache__' not in path.parts
                     and path != ledger_path}
        with (root / 'result-manifest.json').open('x') as stream:
            json.dump({'files': artifacts, 'global_elapsed_after_parse_and_serialize': budget.elapsed(),
                       'ledger_authoritative_if_late_halt': True,
                       'execution_state_excluded_because_final_end_time_is_written_after_outputs': True}, stream, indent=2)
        if budget.elapsed() > reg['caps']['wall_seconds']:
            budget.halt('RESULT_MANIFEST_WRITE_EXCEEDED_WALL_CAP')
        budget.state['elapsed_after_all_other_output_writes'] = budget.elapsed()
        budget.complete()
    return int(budget.state['halted'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute-authorization', type=Path, required=True,
                        help='Non-secret coordinator EXECUTE/P10 receipt; never an API credential')
    args = parser.parse_args()
    raise SystemExit(main(args.execute_authorization))
