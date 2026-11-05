import json
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from phase2_preflight import (BASE, REGISTRATION, audit_saved, bounded_suite_status,
                              job_config, memory_stats, split_harness, validate_output, verify_hashes)
from monitor import formal_harness


class Phase2PreflightTests(unittest.TestCase):
    def test_split_preserves_legal_inputs_sampling_and_all_six_obligations(self):
        baseline = formal_harness()
        for slot in range(6):
            text = split_harness(baseline, slot)
            self.assertEqual(text.count('assert('), 1)
            self.assertEqual(text.count('cover('), 1)
            self.assertIn(f'assert(!active[{slot}] || ok[{slot}]);', text)
            self.assertIn(f'cover(active[{slot}]);', text)
            for line in baseline.splitlines():
                if 'assert(' not in line and 'cover(' not in line:
                    self.assertIn(line, text)

    def test_split_refuses_changed_harness_and_invalid_slot(self):
        for slot in (-1, 6, True, '0'):
            with self.assertRaises(ValueError):
                split_harness(formal_harness(), slot)
        with self.assertRaises(ValueError):
            split_harness(formal_harness().replace('assert((active & ~ok)==0);', ''), 0)

    def test_incomplete_slots_cannot_become_pass(self):
        self.assertEqual(bounded_suite_status(['PASS'] * 6), 'bounded_pass_not_proof')
        for status in ('TIMEOUT', 'UNKNOWN', 'ERROR'):
            self.assertEqual(bounded_suite_status(['PASS'] * 5 + [status]), 'incomplete')
        self.assertEqual(bounded_suite_status(['PASS'] * 5), 'incomplete')
        self.assertEqual(bounded_suite_status(['PASS'] * 5 + ['FAIL']), 'counterexample_pending_reference')

    def test_changed_evidence_rejected(self):
        with tempfile.TemporaryDirectory(dir=BASE / 'results', prefix='phase2-test-') as tmp:
            path = Path(tmp) / 'evidence.json'
            path.write_text('original')
            expected = hashlib.sha256(path.read_bytes()).hexdigest()
            verify_hashes({str(path): expected})
            path.write_text('changed')
            with self.assertRaises(ValueError):
                verify_hashes({str(path): expected})

    def test_sby_jny_telemetry_on_actual_saved_models(self):
        for name, expected in [('phase2-preflight-v3/slot0', 256),
                               ('phase2-preflight-v4/always_true', 0)]:
            path = BASE / 'results' / name / 'work/model/design.json'
            stats = memory_stats(json.loads(path.read_text()))
            self.assertEqual(stats['model_memory_bits'], expected)
        legacy = {'modules': {'top': {'cells': {'mem': {'type': '$mem_v2',
                  'parameters': {'WIDTH': '1000', 'SIZE': '10000'}}}}}}
        self.assertEqual(memory_stats(legacy), {'model_memory_cells': 1, 'model_memory_bits': 128})

    def test_old_results_and_existing_output_cannot_be_written(self):
        for path in (BASE / 'results/live-final-v1', BASE / 'results/live-v1/phase2-new',
                     BASE / 'public/phase2-new'):
            with self.assertRaises(ValueError):
                validate_output(path)
        validate_output(BASE / 'results/phase2-unique-test-no-write')
        with tempfile.TemporaryDirectory(dir=BASE / 'results', prefix='phase2-test-') as tmp:
            with self.assertRaises(FileExistsError):
                validate_output(Path(tmp))

    def test_registered_budget_and_saved_evidence(self):
        reg = json.loads(REGISTRATION.read_text())
        c = reg['calibration']
        self.assertFalse(reg['live_allowed'])
        self.assertEqual(len(c['slots']) * c['timeout_seconds_per_slot'], c['candidate_solver_budget_seconds'])
        self.assertEqual(c['candidate_solver_budget_seconds'] + 2 * c['timeout_seconds_per_control'],
                         c['total_solver_budget_seconds'])
        self.assertIn('mode bmc\ndepth 48\ntimeout 10', job_config(10, 48))
        self.assertIn('prep -top formal_top -flatten', job_config(10, 48, flatten=True))
        self.assertNotIn(' -flatten', job_config(10, 48))
        audit = audit_saved(reg)
        self.assertEqual(audit['freeze_members_checked'], 3486)
        self.assertEqual(audit['formal_statuses'], {'PASS': 12, 'FAIL': 29, 'TIMEOUT': 31})
        self.assertEqual(audit['correct_bmc_prove_statuses'], {'TIMEOUT': 24})
        self.assertAlmostEqual(audit['C_vs_B_token_percent'], 6.5231438214)
        for c in audit['candidate_sessions']:
            self.assertEqual(c['simulation']['verilator']['distinct_mutants_killed'], 6)


if __name__ == '__main__':
    unittest.main()
