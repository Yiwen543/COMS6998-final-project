"""Pure Python budget/refusal mocks only. Never imports runner/runtime or tools."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import time
import unittest
from budget import Budget, Refuse
from observations import Unqualified, parse_rows, signal, eligibility, phase_binding

HERE = Path(__file__).resolve().parent
CAPS = dict(compile_jobs=32, native_jobs=32, physical_jobs=32, setup_jobs=8,
    physical_cycles=1024, cycles_per_run=32, wall_seconds=1200,
    compile_timeout=20, native_timeout=10, physical_timeout=2, setup_timeout=2)
RECORD = None


class Mocks(unittest.TestCase):
    def setUp(self):
        self.folder = RECORD / self._testMethodName
        self.folder.mkdir()
        self.clock = [0]
        (self.folder / 'origin.json').write_text(json.dumps({
            'origin': 'PURE_PYTHON_MOCK_NOT_G1_QUALIFICATION',
            'actual_native_compile_physical_calls': 0}))

    def budget(self, caps=None):
        return Budget(self.folder / 'synthetic-budget.json', caps or CAPS,
                      clock=lambda: self.clock[0])

    def test_01_all_native_slots_reserved_before_dispatch(self):
        b = self.budget()
        for i in range(32):
            b.reserve('native', str(i))
            b.terminal(str(i), {'status': 'MOCK_RETURNED', 'exit_code': 0})
        with self.assertRaises(Refuse):
            b.reserve('native', 'over')
        self.assertEqual(b.state['reserved']['native'], 32)
        self.assertTrue(b.state['halted'])

    def test_02_halt_persists_across_job_kinds(self):
        b = self.budget(); b.halt('MOCK_HALT')
        for kind in ['compile', 'native', 'physical', 'setup']:
            with self.assertRaises(Refuse): b.reserve(kind, kind)

    def test_03_existing_pool_cannot_restart(self):
        self.budget()
        with self.assertRaises(FileExistsError): self.budget()

    def test_04_deadline_cannot_reset(self):
        b = self.budget(); self.clock[0] = 1196
        with self.assertRaises(Refuse): b.reserve('compile', 'late')
        self.assertTrue(b.state['halted'])

    def test_05_physical_cycle_limit(self):
        b = self.budget()
        with self.assertRaises(Refuse): b.reserve('physical', 'too-long', 33)
        self.assertEqual(b.state['reserved']['physical'], 0)

    def test_06_duplicate_no_retry(self):
        b = self.budget(); b.reserve('compile', 'one')
        with self.assertRaises(Refuse): b.reserve('compile', 'one')
        self.assertEqual(b.state['reserved']['compile'], 1)

    def test_07_exact_integer_caps_and_cycles(self):
        caps = CAPS.copy(); caps['native_jobs'] = True
        with self.assertRaises(Refuse): self.budget(caps)
        b = self.budget()
        with self.assertRaises(Refuse): b.reserve('physical', 'bool', True)

    def test_08_completed_pool_cannot_dispatch(self):
        b = self.budget(); b.complete()
        with self.assertRaises(Refuse): b.reserve('native', 'after')

    def test_09_preregistered_counts_no_prove(self):
        jobs = json.loads((HERE / 'job-plan.json').read_text())['jobs']
        self.assertEqual(sum(j['kind'] == 'compile' for j in jobs), 18)
        self.assertEqual(sum(j['kind'] == 'native' for j in jobs), 32)
        self.assertEqual(sum(j['kind'] == 'physical' for j in jobs), 32)
        self.assertEqual(sum(j.get('cycles', 0) for j in jobs), 128)
        self.assertEqual(set(j['mode'] for j in jobs if j['kind'] == 'native'), {'bmc', 'cover'})

    def test_10_phase_negative_is_rejected_not_resampled(self):
        cases = json.loads((HERE / 'inputs/controls.json').read_text())['cases']
        self.assertEqual(phase_binding(cases[8]), 'MATCH')
        self.assertEqual(phase_binding(cases[9]), 'REJECT')
        broken = copy.deepcopy(cases[8]); broken['selected_phase'] = 'later'
        with self.assertRaises(Unqualified): phase_binding(broken)

    def test_11_unknown_is_not_zero_and_width_is_exact(self):
        vcd = {'wires': {'top.x': ('!', 4)}}
        self.assertEqual(signal(vcd, {'!': 'x'}, 'top.x', 4), 'xxxx')
        with self.assertRaises(Unqualified): signal(vcd, {'!': '0'}, 'top.x', 1)

    def test_12_vacuous_fourstate_exclusions(self):
        cases = json.loads((HERE / 'inputs/controls.json').read_text())['cases']
        for n in [7, 12, 13, 15]: self.assertFalse(eligibility(cases[n]))
        self.assertEqual(cases[14]['eligibility'], 'TRANSPORT_ONLY')
        self.assertTrue(all(not c['completion128_credit'] for c in cases))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--record', type=Path, required=True)
    args = parser.parse_args(); RECORD = args.record; RECORD.mkdir(exist_ok=False)
    started = time.monotonic()
    with (RECORD / 'unittest.log').open('x') as log:
        result = unittest.TextTestRunner(stream=log, verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Mocks))
    summary = dict(scope='PURE_PYTHON_BUDGET_REFUSAL_MOCK_NOT_G1_QUALIFICATION',
        tests=result.testsRun, failures=len(result.failures), errors=len(result.errors),
        seconds=time.monotonic()-started, passed=result.wasSuccessful(),
        actual_setup_compile_native_physical_calls=0,
        source_sha256={str(p.name): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in HERE.glob('*.py')})
    (RECORD / 'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary)); raise SystemExit(int(not result.wasSuccessful()))
