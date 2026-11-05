"""Retain the actual failure and complete evidence; never edit checker rules."""
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from followup_wbxbar_reference_checker import OUTPUT_BASE, verify, FILES
from prepare_wbxbar_reference_review import unpack_results, unpack_traces
from repair_wbxbar_reference_checker import apply_exact


class CompletionPacketTests(unittest.TestCase):
    def test_all17_traces_results_and_limits_roundtrip(self):
        b = OUTPUT_BASE
        m = verify(b / 'completion-packet-v1')
        body = json.loads((b / 'completion-packet-v1/packet.json').read_text())
        inputs = json.loads((b / 'followup-v1/focused-inputs.json').read_text())
        results = json.loads((b / 'followup-v1/evaluation-focused/outputs.json').read_text())
        for name, item in json.loads((b / 'followup-v1/author-test-diagnostic.json').read_text()).items():
            inputs['new_diagnostic/' + name] = {'rows': item['rows'], 'limits': {}}
            results['new_diagnostic/' + name] = item['result']
        self.assertEqual(unpack_traces(body['traces']), {n: x['rows'] for n, x in inputs.items()})
        self.assertEqual(unpack_results(body['full_results']), results)
        self.assertEqual(body['case_limits'], {n: x['limits'] for n, x in inputs.items()})
        self.assertEqual(len(inputs), 17)
        self.assertEqual(body['case_limits']['focused/tag_then_exhaustion'], {'MAX_HYP': 1})
        self.assertEqual(m['parent_candidate'], str(b / 'followup-v1/candidate'))
        self.assertFalse(m['live_B_allowed'])
        self.assertEqual(m['planned_calls'], 1)

    def test_candidate_is_exact_claude_output_and_failed_test_is_not_hidden(self):
        b = OUTPUT_BASE
        parent = {f: (b / 'repair-v1/candidate' / f).read_text() for f in FILES}
        patches = json.loads((b / 'followup-v1/patches.json').read_text())
        rebuilt = apply_exact(parent, patches)
        for f in FILES:
            self.assertEqual(rebuilt[f], (b / 'followup-v1/candidate' / f).read_text())
        body = json.loads((b / 'completion-packet-v1/packet.json').read_text())
        self.assertEqual([x['name'] for x in body['selftest_results'] if not x['pass']], ['mixed_death_keeps_prefix_tag_open'])
        self.assertEqual(sum(x['pass'] for x in body['selftest_results']), 53)


if __name__ == '__main__':
    unittest.main()
