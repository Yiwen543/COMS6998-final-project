import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import clean_generated


class CleanupTests(unittest.TestCase):
    def test_toolchain_and_secrets_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ('build/tools/pinned/cache', 'build/private/cache',
                         'build/replay/verilator-build', 'results/run/verilator-build',
                         'results/run/raw', 'egraph/target'):
                (root/name).mkdir(parents=True)
            with patch.object(clean_generated, 'ROOT', root):
                paths = {str(p.relative_to(root)) for p in clean_generated.candidates() if p.exists()}
            self.assertEqual(paths, {'build/replay/verilator-build', 'results/run/verilator-build'})


if __name__ == '__main__':
    unittest.main()
