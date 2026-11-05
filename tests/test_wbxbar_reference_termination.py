"""Verify the targeted author packet and unchanged read-only review evidence."""
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from followup_wbxbar_reference_checker import OUTPUT_BASE, FILES, verify
from prepare_wbxbar_completion_review import unpack_review_results
from prepare_wbxbar_termination_repair import extra_controls
from run_midterm_fixed import sha


class TerminationPacketTests(unittest.TestCase):
    def test_all_nine_cases_and_results_are_exact(self):
        b = OUTPUT_BASE
        m = verify(b / 'termination-packet-v1')
        p = json.loads((b / 'termination-packet-v1/packet.json').read_text())
        cases = json.loads((b / 'completion-v1/boundary-inputs.json').read_text())
        results = json.loads((b / 'completion-v1/evaluation-boundary/outputs.json').read_text())
        name = 'new_diagnostic/valid_prefix_before_first_invalid_row'
        cases['valid_prefix'] = json.loads((b / 'completion-v1/focused-inputs.json').read_text())[name]
        results['valid_prefix'] = json.loads((b / 'completion-v1/evaluation-focused/outputs.json').read_text())[name]
        extra = json.loads((b / 'termination-controls-v1/inputs.json').read_text())
        self.assertEqual(extra, extra_controls())
        cases.update(extra)
        results.update(json.loads((b / 'termination-controls-v1/outputs.json').read_text()))
        self.assertEqual(p['complete_cases'], cases)
        self.assertEqual(unpack_review_results(p['full_results']), results)
        self.assertEqual(len(cases), 9)
        self.assertEqual(cases['undefined_after_suspension']['limits'], {'MAX_HYP': 1})
        self.assertNotIn('i_mcyc', cases['missing_input_field']['rows'][8]['pre'])
        self.assertEqual(m['planned_calls'], 1)
        self.assertEqual(m['cli_budget_usd'], 4)
        self.assertFalse(m['replay_allowed'])

    def test_rejection_and_candidate_authorship_preserved(self):
        b = OUTPUT_BASE
        p = json.loads((b / 'termination-packet-v1/packet.json').read_text())
        review = json.loads((b / 'completion-review-v1/review.json').read_text())
        self.assertEqual(p['fresh_independent_review'], review)
        self.assertFalse(review['ready_for_replay_registration'])
        self.assertEqual({f['id'] for f in review['findings']}, {'N1','N2','N3','N4','N5'})
        meta = json.loads((b / 'completion-v1/candidate/metadata.json').read_text())
        for f in FILES:
            self.assertEqual(p['current_candidate'][f], (b / 'completion-v1/candidate' / f).read_text())
            self.assertEqual(sha(b / 'completion-v1/candidate' / f), meta['artifact_sha256'][f])


if __name__ == '__main__':
    unittest.main()
