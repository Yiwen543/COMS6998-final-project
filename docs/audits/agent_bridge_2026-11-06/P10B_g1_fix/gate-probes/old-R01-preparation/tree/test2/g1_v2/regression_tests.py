"""Only new R02 deadline/horizon regressions. All process/sleep/signal calls mocked."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
from types import SimpleNamespace
import time
import unittest
from unittest.mock import patch
from budget import Budget, Refuse
from runtime import execute
from observations import (Unqualified, parse_vcd, bind_physical_vcd,
                          state_at, signal, selected_native_alarm)

HERE = Path(__file__).resolve().parent
CAPS = dict(compile_jobs=32, native_jobs=32, physical_jobs=32, setup_jobs=8,
    physical_cycles=1024, cycles_per_run=32, wall_seconds=1200,
    compile_timeout=20, native_timeout=10, physical_timeout=2, setup_timeout=2)
RECORD = None


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Clock:
    value = 0.0

    def now(self):
        return self.value

    def advance(self, seconds):
        self.value += seconds


class FakeProcess:
    pid = 987654321

    def __init__(self, pending=False):
        self.returncode = None if pending else 0

    def poll(self):
        return self.returncode

    def wait(self, timeout=None):
        return self.returncode


class Regressions(unittest.TestCase):
    def setUp(self):
        self.folder = RECORD / self._testMethodName
        self.folder.mkdir()
        self.inputs = self.folder / 'inputs'
        self.inputs.mkdir()
        self.result = {'origin': 'PURE_PYTHON_R02_REGRESSION_NOT_G1_QUALIFICATION',
                       'real_process_tool_sleep_signal_calls': 0}

    def tearDown(self):
        bindings = {str(p.relative_to(self.inputs)): sha(p)
                    for p in self.inputs.rglob('*') if p.is_file()}
        (self.folder / 'input-bindings.json').write_text(json.dumps(bindings, indent=2)+'\n')
        (self.folder / 'result.json').write_text(json.dumps(self.result, indent=2)+'\n')

    def run_deadline(self, elapsed=1194, stage=None, delay=0, pending=False):
        clock = Clock()
        budget = Budget(self.folder / 'synthetic-pool.json', CAPS, clock=clock.now)
        clock.value = elapsed
        job = dict(id='mock-only-root', kind='compile', argv=['MOCK_NO_EXECUTABLE'])
        job_folder = self.folder / 'mock-job'
        config = dict(initial_elapsed=elapsed, delayed_stage=stage,
            delay_seconds=delay, pending_process=pending, argv=job['argv'],
            clock_origin=0, work_deadline=1195, global_deadline=1200)
        (self.inputs / 'fake-clock.json').write_text(json.dumps(config, indent=2)+'\n')
        original_save = budget.save
        original_mkdir, original_open = Path.mkdir, Path.open
        delayed = [False]
        proc = FakeProcess(pending)

        def maybe_delay(where):
            if stage == where and not delayed[0]:
                delayed[0] = True
                clock.advance(delay)

        def save():
            original_save()
            maybe_delay('save')

        def mkdir(path, *args, **kwargs):
            answer = original_mkdir(path, *args, **kwargs)
            if path == job_folder:
                maybe_delay('mkdir')
            return answer

        def open_file(path, *args, **kwargs):
            answer = original_open(path, *args, **kwargs)
            if path == job_folder / 'stdout.log':
                maybe_delay('log_open')
            return answer

        def killpg(pid, signum):
            self.assertEqual(pid, proc.pid)
            if proc.returncode is not None:
                raise ProcessLookupError()
            if signum:
                proc.returncode = -9

        budget.save = save
        with patch('runtime.time.monotonic', clock.now), \
             patch('runtime.time.sleep', clock.advance), \
             patch('runtime.subprocess.Popen', return_value=proc) as popen, \
             patch('runtime.subprocess.run', return_value=SimpleNamespace(stdout='', returncode=0)) as ps, \
             patch('runtime.os.killpg', side_effect=killpg), \
             patch.object(Path, 'mkdir', mkdir), patch.object(Path, 'open', open_file):
            receipt = execute(budget, job, job_folder, {})
            process_calls, monitor_calls = popen.call_count, ps.call_count
        self.result.update(runtime_receipt=receipt, mocked_Popen_calls=process_calls,
            mocked_monitor_calls=monitor_calls, final_clock=clock.value,
            budget=copy.deepcopy(budget.state), original_clock_start=budget.start)
        return budget, receipt, process_calls

    def assert_no_dispatch(self, stage):
        budget, receipt, calls = self.run_deadline(stage=stage, delay=7)
        self.assertEqual(calls, 0)
        self.assertFalse(receipt['dispatch_attempted'])
        self.assertEqual(receipt['status'], 'NOT_RUN')
        self.assertEqual(budget.state['reserved']['compile'], 1)
        self.assertTrue(budget.state['halted'])
        self.assertEqual(budget.event('mock-only-root')['dispatch_state'], 'CHARGED_NOT_DISPATCHED')
        self.assertEqual(budget.event('mock-only-root')['absolute_job_deadline'], 1195)
        self.assertEqual(budget.start, 0)

    def test_01_save_crosses_work_and_global_deadline(self):
        self.assert_no_dispatch('save')

    def test_02_mkdir_crosses_work_and_global_deadline(self):
        self.assert_no_dispatch('mkdir')

    def test_03_log_open_crosses_work_and_global_deadline(self):
        self.assert_no_dispatch('log_open')

    def test_04_already_expired_has_no_reservation_or_process(self):
        budget, receipt, calls = self.run_deadline(elapsed=1196)
        self.assertEqual(calls, 0)
        self.assertEqual(budget.state['reserved']['compile'], 0)
        self.assertEqual(receipt['status'], 'NOT_RUN')
        self.assertEqual(budget.event('mock-only-root')['dispatch_state'], 'UNRESERVED_NOT_DISPATCHED')

    def test_05_insufficient_cleanup_window_refuses(self):
        budget, receipt, calls = self.run_deadline(elapsed=1194.9)
        self.assertEqual(calls, 0)
        self.assertEqual(budget.state['reserved']['compile'], 1)
        self.assertIn('INSUFFICIENT_DEADLINE', receipt['refusal_reason'])

    def test_06_normal_baseline_dispatch_once(self):
        budget, receipt, calls = self.run_deadline(elapsed=100)
        self.assertEqual(calls, 1)
        self.assertEqual(receipt['status'], 'RETURNED')
        self.assertEqual(receipt['absolute_job_deadline'], 120)
        self.assertFalse(budget.state['halted'])

    def test_07_timeout_keeps_original_deadline_after_save_delay(self):
        budget, receipt, calls = self.run_deadline(elapsed=0, stage='save', delay=2, pending=True)
        self.assertEqual(calls, 1)
        self.assertEqual(receipt['absolute_job_deadline'], 20)
        self.assertEqual(receipt['status'], 'TIMEOUT')
        self.assertTrue(receipt['timed_out'])
        self.assertLessEqual(self.result['final_clock'], 20)
        self.assertTrue(budget.state['halted'])

    def test_08_charged_refusal_does_not_refund_or_allow_new_pool(self):
        budget, _, calls = self.run_deadline(stage='save', delay=7)
        self.assertEqual(calls, 0)
        with self.assertRaises(Refuse): budget.reserve('native', 'next')
        with self.assertRaises(FileExistsError):
            Budget(self.folder / 'synthetic-pool.json', CAPS)
        self.assertEqual(budget.state['reserved']['compile'], 1)

    def fixture(self, name, mutation=None):
        source = HERE / 'inputs/p10-regressions' / name
        path = self.inputs / name
        shutil.copy2(source, path)
        before = sha(path)
        if mutation:
            path.write_text(mutation(path.read_text()))
        self.result['fixture'] = dict(source=str(source), source_sha256=sha(source),
            copied_initial_sha256=before, final_mutated_sha256=sha(path))
        rows_source = HERE / 'inputs/p10-regressions/rows.json'
        shutil.copy2(rows_source, self.inputs / 'rows.json')
        rows = json.loads((self.inputs / 'rows.json').read_text())['QC00']
        return path, rows, {'id': 'QC00'}

    def test_09_exact_complete_P10_fixture_accepts(self):
        path, rows, case = self.fixture('full-observer-vcd.vcd')
        before = sha(path); vcd = parse_vcd(path)
        bind_physical_vcd(vcd, rows, case)
        self.assertEqual(vcd['recorded_last_tick'], 16000)
        self.assertEqual(sha(path), before)
        self.result.update(outcome='ACCEPT_COMPLETE_ANALYTIC_FIXTURE', input_unchanged=True)

    def test_10_exact_truncated_P10_fixture_rejects_for_horizon(self):
        path, rows, case = self.fixture('full-observer-vcd-truncated-before-post15.vcd')
        before = sha(path); vcd = parse_vcd(path)
        with self.assertRaisesRegex(Unqualified, 'VCD_TIME_COVERAGE_MISSING') as caught:
            bind_physical_vcd(vcd, rows, case)
        self.assertEqual(vcd['recorded_last_tick'], 14000)
        self.assertEqual(sha(path), before)
        self.result.update(outcome='REJECT', reason=str(caught.exception), input_unchanged=True)

    def test_11_query_before_recorded_span_rejects(self):
        path, _, _ = self.fixture('full-observer-vcd.vcd')
        with self.assertRaisesRegex(Unqualified, 'VCD_TIME_COVERAGE_MISSING') as caught:
            state_at(parse_vcd(path), -1)
        self.result.update(outcome='REJECT', reason=str(caught.exception))

    def test_12_unknown_is_preserved_and_not_accepted_as_zero(self):
        path, rows, case = self.fixture('full-observer-vcd.vcd',
            lambda text: text.replace('b0000 (', 'bxxxx (', 1))
        vcd = parse_vcd(path)
        self.assertEqual(signal(vcd, state_at(vcd, 1000), 'physical_tb.units[0].u.q', 4), 'xxxx')
        with self.assertRaisesRegex(Unqualified, 'VCD_ROW_OUTPUT:q') as caught:
            bind_physical_vcd(vcd, rows, case)
        self.result.update(outcome='REJECT', reason=str(caught.exception), observed_q='xxxx')

    def test_13_missing_signal_still_rejects(self):
        path, rows, case = self.fixture('full-observer-vcd.vcd',
            lambda text: text.replace('$var wire 4 ! a $end\n', '', 1))
        with self.assertRaisesRegex(Unqualified, 'VCD_SIGNAL_AMBIGUOUS_OR_ABSENT') as caught:
            bind_physical_vcd(parse_vcd(path), rows, case)
        self.result.update(outcome='REJECT', reason=str(caught.exception))

    def test_14_native_selected_candidate_cannot_extend_horizon(self):
        path = self.inputs / 'analytic-native.txt'
        path.write_text('$timescale 1 ns $end\n$scope module formal_top $end\n'
            '$var wire 1 ! sampled_active $end\n$var wire 1 " sampled_ok $end\n'
            '$var wire 3 # sampled_cycle $end\n$var wire 4 $ sampled_q $end\n'
            '$upscope $end\n$enddefinitions $end\n#0\n1!\n0"\nb001 #\nb0000 $\n#10\n')
        vcd = parse_vcd(path)
        self.assertEqual(selected_native_alarm(vcd)['native_tick'], 10)
        vcd['samples'].append((11, vcd['samples'][-1][1].copy()))
        (self.inputs / 'deliberate-future-candidate.json').write_text(json.dumps(vcd, indent=2)+'\n')
        with self.assertRaisesRegex(Unqualified, 'VCD_TIME_COVERAGE_MISSING') as caught:
            selected_native_alarm(vcd)
        self.result.update(outcome='REJECT_FUTURE_SELECTED_CANDIDATE', reason=str(caught.exception))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--record', type=Path, required=True)
    args = parser.parse_args(); RECORD = args.record; RECORD.mkdir(exist_ok=False)
    source_copy = RECORD / 'executed-source'; source_copy.mkdir()
    for source in HERE.glob('*.py'): shutil.copy2(source, source_copy / source.name)
    started = time.monotonic()
    with (RECORD / 'unittest.log').open('x') as log:
        result = unittest.TextTestRunner(stream=log, verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Regressions))
    summary = dict(scope='R02_ONLY_NEW_PYTHON_DEADLINE_HORIZON_REGRESSIONS',
        tests=result.testsRun, failures=len(result.failures), errors=len(result.errors),
        seconds=time.monotonic()-started, passed=result.wasSuccessful(),
        actual_native_compile_physical_version_sleep_process_calls=0,
        source_sha256={p.name: sha(p) for p in source_copy.iterdir()})
    (RECORD / 'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary)); raise SystemExit(int(not result.wasSuccessful()))
