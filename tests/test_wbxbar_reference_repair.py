"""Repair transport and focused trace provenance, never a functional oracle."""
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import repair_wbxbar_reference_checker as repair
from prepare_wbxbar_reference_review import unpack_results, unpack_traces
from probe_wbxbar_reference_review import build


class ReferenceRepairTests(unittest.TestCase):
    def test_packet_preserves_all_focused_inputs_outputs_and_candidate(self):
        b = repair.OUTPUT_BASE
        m = repair.verify(b / 'repair-packet-v1')
        p = json.loads((b / 'repair-packet-v1/packet.json').read_text())
        controls = build()
        self.assertEqual(controls, json.loads((b / 'review-repro-v2/inputs.json').read_text()))
        self.assertEqual(unpack_traces(p['focused_traces']), {n: x['rows'] for n, x in controls.items()})
        self.assertEqual(unpack_results(p['focused_results']), json.loads((b / 'review-repro-v2/outputs.json').read_text()))
        for f in repair.FILES:
            self.assertEqual(p['current_candidate'][f], (b / 'claude-author-v1' / f).read_text())
        self.assertEqual(m['planned_calls'], 1)
        self.assertEqual(m['cli_budget_usd'], 4)
        self.assertFalse(m['live_B_allowed'])

    def test_hr_probe_fix_is_only_forward_identity(self):
        b = repair.OUTPUT_BASE
        old = json.loads((b / 'review-repro-v1/inputs.json').read_text())
        new = build()
        n = 'hr_acceptance_and_forward_same_row'
        for name in old:
            if name != n:
                self.assertEqual(old[name], new[name])
        p = new[n]['rows'][8]['pre']
        self.assertEqual(p['o_saddr'], p['i_maddr'] & 255)
        self.assertEqual(p['o_ssel'], p['i_msel'] & 15)
        self.assertEqual(p['o_swe'], p['i_mwe'] & 1)
        self.assertEqual(p['o_sdata'], p['i_mdata'] & 0xffffffff)
        results = json.loads((b / 'review-repro-v2/outputs.json').read_text())
        self.assertFalse(results[n]['assumption_violations'])
        self.assertNotIn('K4_count_projection', [x['category'] for x in results[n]['failures']])

    def test_exact_patch_rejects_nonunique_or_missing_before(self):
        sources = {f: (repair.OUTPUT_BASE / 'claude-author-v1' / f).read_text() for f in repair.FILES}
        snapshot = copy.deepcopy(sources)
        response = {'patches': [{'file': 'checker.py', 'before': 'DEFAULT_LIMITS =',
                                'after': '# offline transport test only\nDEFAULT_LIMITS ='}], 'rationale': [], 'contract_decisions': []}
        self.assertIn('# offline transport test only', repair.apply_exact(sources, response)['checker.py'])
        self.assertEqual(sources, snapshot)
        for before in ('not a source substring', ' '):
            bad = copy.deepcopy(response)
            bad['patches'][0]['before'] = before
            with self.assertRaisesRegex(ValueError, 'exactly once'):
                repair.apply_exact(sources, bad)

    def test_failed_call_is_not_retried_and_key_is_deleted(self):
        with tempfile.TemporaryDirectory() as folder:
            key = Path(folder) / 'offline-key'
            key.write_text('test-only')
            key.chmod(0o600)
            def failed(prompt, output, env, role):
                self.assertNotIn('OPENAI_API_KEY', env)
                self.assertNotIn('ANTHROPIC_BASE_URL', env)
                raise RuntimeError('mock failure')
            with patch.object(repair, 'KEY_FILE', key), patch.object(repair, 'call', side_effect=failed) as call, patch.dict(os.environ, {'OPENAI_API_KEY': 'test', 'ANTHROPIC_BASE_URL': 'test'}):
                with self.assertRaisesRegex(RuntimeError, 'mock failure'):
                    repair.run(repair.OUTPUT_BASE / 'repair-packet-v1', Path(folder) / 'out')
                self.assertEqual(call.call_count, 1)
            self.assertFalse(key.exists())


if __name__ == '__main__':
    unittest.main()
