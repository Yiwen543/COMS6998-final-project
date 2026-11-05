"""Complete new review evidence and preservation of prior author test cases."""
import ast
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from review_wbxbar_reference_repair import OUTPUT_BASE, verify
from prepare_wbxbar_reference_review import FILES, unpack_traces
from prepare_wbxbar_completion_review import unpack_review_results
from repair_wbxbar_reference_checker import apply_exact


def test_cases(source):
    run = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == 'run')
    tests = next(n.value for n in run.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'tests' for t in n.targets))
    return {n.elts[0].value: ast.dump(n, include_attributes=False) for n in tests.elts}


class TerminationReviewTests(unittest.TestCase):
    def test_all158_new_results_and_inputs_roundtrip(self):
        b = OUTPUT_BASE
        m = verify(b / 'termination-review-packet-v1')
        p = json.loads((b / 'termination-review-packet-v1/packet.json').read_text())
        run = b / 'termination-v1'
        rows = json.loads((b / 'controls-v1/inputs.json').read_text())
        limits = {n: {} for n in rows}
        results = json.loads((run / 'evaluation-original/cases.json').read_text())['cases']
        for n, case in json.loads((b / 'controls-v1/limit-tests.json').read_text()).items():
            rows['limit/' + n] = case['rows']
            limits['limit/' + n] = case['limits']
        results.update({'limit/' + n: x for n, x in json.loads((run / 'evaluation-original/limits.json').read_text()).items()})
        output = json.loads((run / 'evaluation-focused/outputs.json').read_text())
        for n, case in json.loads((run / 'focused-inputs.json').read_text()).items():
            kind, name = n.split('/', 1)
            target = kind + '_recheck/' + name
            rows[target] = case['rows']
            limits[target] = case['limits']
            results[target] = output[n]
        decoded = unpack_traces(p['traces'])
        decoded.update(p['raw_boundary_traces'])
        self.assertEqual(decoded, rows)
        self.assertEqual(p['case_limits'], limits)
        self.assertEqual(unpack_review_results(p['full_checker_results']), results)
        self.assertEqual(len(rows), 158)
        self.assertEqual(set(rows), {x['name'] for x in p['expectations']})
        self.assertFalse(m['replay_allowed'])
        self.assertEqual(m['planned_calls'], 1)

    def test_exact_claude_patches_preserve_all54_prior_tests(self):
        b = OUTPUT_BASE
        parent = {f: (b / 'completion-v1/candidate' / f).read_text() for f in FILES}
        rebuilt = apply_exact(parent, json.loads((b / 'termination-v1/patches.json').read_text()))
        for f in FILES:
            self.assertEqual(rebuilt[f], (b / 'termination-v1/candidate' / f).read_text())
        old, new = test_cases(parent['selftest.py']), test_cases(rebuilt['selftest.py'])
        self.assertEqual(len(old), 54)
        self.assertEqual(len(new), 58)
        self.assertEqual({k: new[k] for k in old}, old)
        summary = json.loads((b / 'termination-v1/evaluation-original/summary.json').read_text())
        self.assertEqual(len(summary['selftests']), 58)
        self.assertTrue(summary['all_control_agreements'])


if __name__ == '__main__':
    unittest.main()
