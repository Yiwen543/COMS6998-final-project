#!/usr/bin/env python3
"""Saved-evidence audit and opt-in, bounded slot calibration. No API client/oracle."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import shutil
import statistics

from common import BASE, ROOT, dump, run, sha

REGISTRATION = BASE / 'configs/phase2_preflight_v1.json'


def load(path):
    return json.loads(Path(path).read_text())


def verify_hashes(files):
    for name, expected in files.items():
        path = ROOT / name
        if not path.resolve().is_relative_to(ROOT) or not path.is_file() or sha(path) != expected:
            raise ValueError('Missing or changed evidence: ' + name)


def split_harness(text, slot):
    if type(slot) is not int or slot not in range(6):
        raise ValueError('Slot must be 0..5')
    assertion = 'assert((active & ~ok)==0);'
    covers = ''.join(f'cover(active[{i}]);' for i in range(6))
    if text.count(assertion) != 1 or re.sub(r'\s+', '', text).count(covers) != 1:
        raise ValueError('Unexpected frozen harness')
    text = text.replace(assertion, f'assert(!active[{slot}] || ok[{slot}]);')
    return re.sub(r'cover\(active\[[0-5]\]\);',
                  lambda m: m[0] if m[0] == f'cover(active[{slot}]);' else '', text)


def bounded_suite_status(statuses):
    if len(statuses) != 6:
        return 'incomplete'
    if 'FAIL' in statuses:
        return 'counterexample_pending_reference'
    return 'bounded_pass_not_proof' if all(s == 'PASS' for s in statuses) else 'incomplete'


def audit_saved(reg):
    verify_hashes(reg['historical_evidence'])
    freeze = load(BASE / 'configs/live_freeze_v1.json')
    verify_hashes(freeze['files'])
    manifest = load(BASE / 'results/live-v1/final-candidates.json')
    candidates = sorted(manifest['candidates'], key=lambda c: (c['arm'], c['repetition']))
    if len(candidates) != 6 or {(c['arm'], c['repetition']) for c in candidates} != {
            (a, r) for a in ('B_prime', 'C_prime') for r in (1, 2, 3)}:
        raise ValueError('Expected all six frozen candidates')
    scores = load(BASE / 'results/live-final-v1/scores.json')
    report_audit = load(BASE / 'results/live-report-v1/audit.json')
    release = load(BASE / 'results/live-final-v1/release.json')
    if (report_audit['final_source_sha256'] != sha(BASE / 'results/live-final-v1/scores.json')
            or release['final_candidates_sha256'] != sha(BASE / 'results/live-v1/final-candidates.json')
            or release['reference_freeze_sha256'] != sha(BASE / 'reference/frozen-v1/freeze.json')):
        raise ValueError('Report/release binding mismatch')
    evidence = dict(reg['historical_evidence'])
    candidate_rows = []
    for c in candidates:
        directory = Path(c['candidate_dir']).resolve()
        if not directory.is_relative_to(BASE / 'results/live-v1'):
            raise ValueError('Candidate outside saved run')
        for filename, field in [('candidate.sv', 'candidate_sha256'), ('candidate.json', 'metadata_sha256')]:
            for parent in [directory, BASE / 'results/live-final-v1' / c['arm'] / f'rep{c["repetition"]}' / 'compiled']:
                name = str((parent / filename).relative_to(ROOT))
                verify_hashes({name: c[field]})
                evidence[name] = c[field]
        matching = [s for s in scores if (s['arm'], s['repetition']) == (c['arm'], c['repetition'])]
        if len(matching) != 1 or matching[0]['candidate_sha256'] != c['candidate_sha256']:
            raise ValueError('Candidate/score binding mismatch')
        s = matching[0]
        compile_path = directory / 'compile.json'
        evidence[str(compile_path.relative_to(ROOT))] = sha(compile_path)
        candidate_rows.append({
            'arm': c['arm'], 'repetition': c['repetition'], 'api_tokens': s['api_known_tokens'],
            'saved_compile_state_bits': load(compile_path)['state_bits'],
            'simulation': {sim: {k: (len(v) if isinstance(v, list) else v) for k, v in m.items()
                                if k in ('correct_control_alarm_records', 'correct_control_unknown_records',
                                         'distinct_mutants_killed', 'eligible_mutant_trace_count', 'valid_mutant_trace_kills')}
                           for sim, m in s['simulation'].items()}})
    formal = [f for s in scores for f in s['formal']]
    means = {a: statistics.mean(s['api_known_tokens'] for s in scores if s['arm'] == a)
             for a in ('B_prime', 'C_prime')}
    calibration = reg['calibration']
    if ((candidates[0]['arm'], candidates[0]['repetition'], candidates[0]['candidate_sha256'])
            != (calibration['candidate_arm'], calibration['candidate_repetition'], calibration['candidate_sha256'])):
        raise ValueError('Predeclared first-candidate selection changed')
    return {'scope': 'saved evidence rechecked; no historical test, simulation or formal job rerun',
            'freeze_members_checked': len(freeze['files']), 'candidate_sessions': candidate_rows,
            'api_tokens_total': sum(s['api_known_tokens'] for s in scores), 'mean_api_tokens': means,
            'C_vs_B_token_percent': (means['C_prime'] / means['B_prime'] - 1) * 100,
            'formal_statuses': dict(Counter(f['status'] for f in formal)),
            'correct_bmc_prove_statuses': dict(Counter(f['status'] for f in formal
                if f['control'].startswith('correct') and f['mode'] in ('bmc', 'prove'))),
            'formal_seconds_saved': sum(f['seconds'] for f in formal),
            'counterexample_fault_types': sorted({f['control'] for f in formal if f['status'] == 'FAIL'}),
            'artifact_sha256': evidence}


def job_config(timeout, depth):
    return f'''[options]
mode bmc
depth {depth}
timeout {timeout}
[engines]
smtbmc z3
[script]
read -formal -sv dut.v candidate.sv harness.sv
prep -top formal_top
[files]
dut.v
candidate.sv
harness.sv
'''


def run_job(out, source, harness, settings, timeout, depth=None):
    depth = settings['depth'] if depth is None else depth
    out.mkdir()
    shutil.copyfile(ROOT / settings['dut'], out / 'dut.v')
    (out / 'candidate.sv').write_text(source)
    (out / 'harness.sv').write_text(harness)
    (out / 'job.sby').write_text(job_config(timeout, depth))
    result = run(['sby', '-d', 'work', 'job.sby'], out / 'sby.log',
                 timeout + settings['process_grace_seconds'], cwd=out)
    status_path = out / 'work/status'
    status = status_path.read_text().split()[0] if status_path.exists() else (
        'TIMEOUT' if result['status'] == 'timeout' else 'ERROR')
    if status == 'PASS' and result['returncode'] != 0:
        status = 'ERROR'
    result.update(status=status, mode='bmc', requested_depth=depth,
                  unbounded_proof=False, independent_specification_verdict=False)
    dump(out / 'result.json', result)
    return result


def calibrate(reg, out):
    from monitor import HEADER
    settings = reg['calibration']
    baseline = (ROOT / settings['baseline_harness']).read_text()
    controls = []
    for name, ok in [('always_true', "6'b111111"), ('always_false', "6'b000000")]:
        source = HEADER + f"assign active=6'b111111; assign ok={ok};\nendmodule\n"
        result = run_job(out / name, source, split_harness(baseline, 0), settings,
                         settings['timeout_seconds_per_control'],
                         settings.get('control_depth', settings['depth']))
        controls.append(dict(control=name, **result))
    controls_ok = [r['status'] for r in controls] == ['PASS', 'FAIL']
    slots = []
    if controls_ok:
        manifest = load(BASE / 'results/live-v1/final-candidates.json')
        candidate = sorted(manifest['candidates'], key=lambda c: (c['arm'], c['repetition']))[0]
        source = (Path(candidate['candidate_dir']) / 'candidate.sv').read_text()
        for slot in settings['slots']:
            result = run_job(out / f'slot{slot}', source, split_harness(baseline, slot), settings,
                             settings['timeout_seconds_per_slot'])
            slots.append(dict(slot=slot, **result))
    return {'scope': 'new infrastructure calibration on one saved candidate; not new B/C data',
            'plumbing_controls_passed': controls_ok, 'controls': controls, 'slots': slots,
            'suite_status': bounded_suite_status([r['status'] for r in slots]),
            'formal_jobs': len(controls) + len(slots),
            'seconds': sum(r['seconds'] for r in controls + slots),
            'api_calls': 0, 'new_dut_simulations': 0, 'historical_results_modified': False,
            'live_ready': False}


def report(audit, calibration):
    rows = ['# test2 phase2 offline preflight', '',
            'Saved v1 evidence was read again; old experiments/tests were not rerun.', '',
            f"- Frozen members matched: {audit['freeze_members_checked']}",
            f"- Saved formal statuses: {audit['formal_statuses']}",
            f"- Saved correct-control bmc/prove: {audit['correct_bmc_prove_statuses']}",
            f"- Saved C/B token difference: {audit['C_vs_B_token_percent']:.6f}%", '',
            '## New slot calibration', '']
    if calibration is None:
        rows.append('Not executed. This audit alone is not a formal result.')
    else:
        rows += ['One predeclared saved candidate, public correct DUT, no new candidate generation.',
                 'BMC PASS is bounded only; FAIL needs independent reference adjudication.', '',
                 '| Job | Status | Seconds |', '|---|---|---:|']
        for r in calibration['controls'] + calibration['slots']:
            rows.append(f"| {r.get('control', 'slot'+str(r.get('slot')))} | {r['status']} | {r['seconds']:.3f} |")
        rows += ['', f"Suite status: {calibration['suite_status']}",
                 f"New formal jobs: {calibration['formal_jobs']}; measured seconds: {calibration['seconds']:.3f}"]
    rows += ['', '## Boundary', '',
             'No API calls or new DUT simulations. No old source/reference/freeze/result changes.',
             'Not a new effectiveness trial, not proof of monitor soundness, and not a live gate.',
             'See docs/test2_phase2_preflight_2026-11-04.md for interpretation and remaining gates.', '']
    return '\n'.join(rows)


def validate_output(out):
    if out.parent != BASE / 'results' or not out.name.startswith('phase2-'):
        raise ValueError('Use a new direct test2/results/phase2-* directory')
    if out.exists():
        raise FileExistsError('Refusing to overwrite existing output')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--registration', type=Path, default=REGISTRATION)
    parser.add_argument('--run-slot-calibration', action='store_true')
    args = parser.parse_args()
    out = args.output.resolve()
    validate_output(out)
    reg = load(args.registration)
    if reg['live_allowed'] or reg['api_calls_allowed'] != 0:
        raise ValueError('This command only accepts an offline registration')
    audit = audit_saved(reg)
    if args.run_slot_calibration:
        for tool in ('sby', 'yosys', 'z3'):
            if shutil.which(tool) is None:
                raise RuntimeError('Required installed tool unavailable: ' + tool)
    out.mkdir()
    dump(out / 'registration.json', reg)
    shutil.copyfile(Path(__file__), out / 'producer.py')
    dump(out / 'run.json', {'registration_sha256': sha(args.registration), 'script_sha256': sha(Path(__file__)),
                          'mode': 'offline_calibration' if args.run_slot_calibration else 'saved_evidence_audit',
                          'api_calls': 0, 'live_allowed': False})
    dump(out / 'saved-evidence-audit.json', audit)
    calibration = calibrate(reg, out) if args.run_slot_calibration else None
    if calibration is not None:
        dump(out / 'formal-calibration.json', calibration)
    verify_hashes(load(BASE / 'configs/live_freeze_v1.json')['files'])
    verify_hashes(audit['artifact_sha256'])
    (out / 'report.md').write_text(report(audit, calibration))
    print(json.dumps({'output': str(out), 'v1_integrity_verified_before_and_after': True,
                      'calibration': calibration['suite_status'] if calibration else 'not_run',
                      'live_ready': False, 'api_calls': 0}, indent=2))
    if calibration is not None and not calibration['plumbing_controls_passed']:
        raise SystemExit('Plumbing controls failed; candidate jobs were not run')


if __name__ == '__main__':
    main()
