"""Failure injection tests for accounting; no simulator, model call or key use."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import run_spi_core_safe_b as runner
from run_midterm_fixed import ROOT
from spi_core_safe_runtime import BASE,SafeExecutionError

class FailureAccountingTests(unittest.TestCase):
    def run_injected(self,invalid=False):
        # The freeze check is patched in this failure-injection test. Use the
        # retained parent settings so tests do not depend on ignored build files.
        config=ROOT/'configs/spi_core_b_development.json'
        frozen=json.loads(config.read_text())
        source=BASE/'preflight-v3/calibration_seed/verilator'
        prior=json.loads((source/'result.json').read_text())
        points=json.loads((source/'raw-points.json').read_text())
        trace=json.loads((source/'trace.json').read_text())
        def execute(binary,actions,out,denominator):
            out.mkdir(parents=True)
            (out/'execution.json').write_text(json.dumps({'executed_cycles':8 if out.name=='seed' else 7,'simulation_seconds':.01}))
            if out.name!='seed':raise SafeExecutionError('transport','injected duplicate handshake')
            return prior,points,trace
        with tempfile.TemporaryDirectory() as temp,contextlib.ExitStack() as stack:
            out=Path(temp)/'run'
            stack.enter_context(patch.object(runner,'verify_freeze',return_value=frozen))
            stack.enter_context(patch.object(runner,'versions',return_value={'mode':'test'}))
            stack.enter_context(patch.object(runner,'compile_driver',return_value=(Path('unused'),['mock'],0)))
            stack.enter_context(patch.object(runner,'simulate',side_effect=execute))
            if invalid:stack.enter_context(patch.object(runner,'validate_experimental',side_effect=ValueError('invalid test actions')))
            with contextlib.redirect_stdout(io.StringIO()):
                runner.run(Namespace(config=config,output=out,mode='mock',replay=None))
            result=json.loads((out/'summary.json').read_text())
            failures=[json.loads(x) for x in (out/'failures.jsonl').read_text().splitlines()] if (out/'failures.jsonl').exists() else []
        return result,failures

    def test_simulation_fault_counts_partial_cycles_and_marks_stale_measurement(self):
        result,failures=self.run_injected()
        self.assertFalse(result['gate']['pass'])
        self.assertEqual(len(result['rows']),3)
        self.assertEqual(result['metadata']['simulation_executions'],6)
        self.assertEqual(result['metadata']['executed_cycles'],45)
        self.assertEqual(result['metadata']['requested_cycles'],240)
        self.assertEqual(result['metadata']['api_generation_calls'],0)
        for row in result['rows']:
            self.assertEqual(row['status'],'simulation_failed')
            self.assertFalse(row['measurement_fresh']);self.assertEqual(row['measurement_round'],0)
            self.assertIn('last successful',row['measurement_note'])
        self.assertEqual(len(failures),3)
        self.assertTrue(all(f['stage']=='transport' and 'duplicate' in f['detail'] for f in failures))

    def test_invalid_actions_keep_attempts_but_do_not_count_nonexistent_simulations(self):
        result,failures=self.run_injected(invalid=True)
        self.assertFalse(result['gate']['pass']);self.assertEqual(failures,[])
        self.assertEqual(len(result['rows']),18)
        self.assertEqual(result['metadata']['simulation_executions'],3)
        self.assertEqual(result['metadata']['executed_cycles'],24)
        for row in result['rows']:
            self.assertEqual(row['status'],'no_valid_actions')
            self.assertFalse(row['measurement_fresh']);self.assertEqual(row['measurement_round'],0)
            self.assertEqual(row['failed_attempts'],2*row['round'])

if __name__=='__main__':unittest.main()
