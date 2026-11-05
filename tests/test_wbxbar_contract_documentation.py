"""A documentation-only role must never modify checker artifacts."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import clarify_wbxbar_contract as role


class DocumentationRoleTests(unittest.TestCase):
    def exercise(self, invalid):
        with tempfile.TemporaryDirectory() as folder:
            key = Path(folder) / 'key'
            key.write_text('offline-only')
            key.chmod(0o600)
            parent = role.OUTPUT_BASE / 'termination-v1/candidate'
            first = (parent / 'contract.md').read_text().splitlines()[0]
            responses = [
                {'patches': [{'file': 'checker.py' if invalid else 'contract.md', 'before': first,
                              'after': first + '\nOffline documentation test.'}], 'rationale': [], 'contract_decisions': []},
                {'ready_for_contract_addendum': True, 'findings': [], 'limitations': []}]
            def fake(prompt, output, env, job):
                output.mkdir()
                return responses.pop(0)
            out = Path(folder) / 'output'
            with patch.object(role, 'KEY_FILE', key), patch.object(role, 'call', side_effect=fake) as call:
                if invalid:
                    with self.assertRaisesRegex(ValueError, 'only contract.md'):
                        role.run(out)
                    self.assertFalse((out / 'candidate').exists())
                else:
                    result = role.run(out)
                    self.assertTrue(result['model_readiness'])
                    self.assertFalse(result['replay_allowed'])
                    self.assertFalse(result['live_B_allowed'])
                    for f in ('checker.py', 'selftest.py', 'properties.json'):
                        self.assertEqual((out / 'candidate' / f).read_bytes(), (parent / f).read_bytes())
                self.assertEqual(call.call_count, 1 if invalid else 2)
            self.assertTrue(key.exists())

    def test_document_only_patch_and_review_keep_functional_files(self):
        self.exercise(False)

    def test_forbidden_functional_patch_stops_before_review(self):
        self.exercise(True)


if __name__ == '__main__':
    unittest.main()
