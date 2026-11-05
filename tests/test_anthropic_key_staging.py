"""Credential input validation using fake keys only; no network calls."""
import contextlib
import io
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import stage_anthropic_crosscheck_key as stage


class AnthropicStagingTests(unittest.TestCase):
    def test_invalid_input_never_written_or_echoed(self):
        samples = ('', 'WBXBAR ERR 边界密钥已就绪', 'sk-ant-abc中文',
                   'sk-proj-test', '"sk-ant-test"', 'export ANTHROPIC_API_KEY=test',
                   'sk-ant-test\nsecondline', 'sk-ant-', 'sk-ant-test value')
        for value in samples:
            with self.subTest(value_kind='invalid'), tempfile.TemporaryDirectory() as tmp:
                dest = Path(tmp) / 'private/key'
                output = io.StringIO()
                with patch.object(stage, 'DEST', dest), patch.object(stage.getpass, 'getpass', return_value=value), contextlib.redirect_stdout(output):
                    with self.assertRaises(SystemExit) as error:
                        stage.main()
                self.assertFalse(dest.exists())
                self.assertEqual(output.getvalue(), '')
                if value and value != 'sk-ant-':  # The documented public prefix is not a secret.
                    self.assertNotIn(value, str(error.exception))

    def test_format_only_success_has_private_permissions_and_no_echo(self):
        value = 'sk-ant-test'
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'private/key'
            output = io.StringIO()
            with patch.object(stage, 'DEST', dest), patch.object(stage.getpass, 'getpass', return_value=value), contextlib.redirect_stdout(output):
                stage.main()
            self.assertEqual(dest.read_text(), value)
            self.assertEqual(stat.S_IMODE(dest.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(dest.parent.stat().st_mode), 0o700)
            self.assertNotIn(value, output.getvalue())
            self.assertIn('API authentication not tested', output.getvalue())

    def test_existing_credential_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'key'
            dest.write_text('existing fixture')
            with patch.object(stage, 'DEST', dest), patch.object(stage.getpass, 'getpass') as hidden_input:
                with self.assertRaisesRegex(SystemExit, 'already staged'):
                    stage.main()
                hidden_input.assert_not_called()
            self.assertEqual(dest.read_text(), 'existing fixture')


if __name__ == '__main__':
    unittest.main()
