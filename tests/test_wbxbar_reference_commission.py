"""Specification-author isolation and bounded commission, without live calls."""
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import prepare_wbxbar_reference_checker as role

PACKET = role.OUTPUT_BASE / 'spec-packet-v1'


class ReferenceCommissionTests(unittest.TestCase):
    def test_contract_is_exact_and_full_control_traces_withheld(self):
        manifest = role.verify(PACKET)
        body = json.loads((PACKET / 'packet.json').read_text())
        design = json.loads((role.BASE / 'design-patch-v2-retry2/design-location-corrected.json').read_text())
        self.assertEqual(body['reviewed_reference_contract'], {k: v for k, v in design.items() if k not in ('control_assessments', 'ready_for_independent_review')})
        self.assertEqual(set(body), {'role', 'specification', 'reviewed_reference_contract', 'design_review', 'prior_claude_artifacts', 'isolation', 'validation_boundary'})
        self.assertIs(body['design_review']['ready_for_implementation'], True)
        self.assertEqual(manifest['planned_author_calls'], 1)
        self.assertFalse(manifest['live_B_allowed'])
        self.assertEqual(manifest['original_experiment_budget'], {'repetitions': 3, 'rounds': 6, 'max_new_cycles': 64, 'seed_cycles': 8})

    def test_packet_drift_prevents_authorship(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'packet'
            shutil.copytree(PACKET, folder)
            (folder / 'prompt.txt').write_text('altered')
            with patch.object(role, 'invoke') as invoke:
                with self.assertRaisesRegex(ValueError, 'packet drift'):
                    role.run(folder, Path(tmp) / 'output')
                invoke.assert_not_called()

    def test_existing_transport_budget_and_no_automatic_live_permission(self):
        def fake_invoke(packet, output, budget, timeout):
            self.assertEqual(budget, 4)
            self.assertEqual(timeout, 600)
            self.assertNotIn('ANTHROPIC_AUTH_TOKEN', os.environ)
            self.assertNotIn('OPENAI_API_KEY', os.environ)
            output.mkdir()
            return {'status': 'candidate_generated_not_validated'}
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'ANTHROPIC_AUTH_TOKEN': 'offline-only', 'OPENAI_API_KEY': 'offline-only'}), patch.object(role, 'invoke', side_effect=fake_invoke) as invoke:
            result = role.run(PACKET, Path(tmp) / 'output')
            invoke.assert_called_once()
            self.assertTrue(result['candidate_only'])
            self.assertFalse(result['live_B_allowed'])
            self.assertEqual(os.environ['ANTHROPIC_AUTH_TOKEN'], 'offline-only')


if __name__ == '__main__':
    unittest.main()
