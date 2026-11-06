from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import controller_done_review_v3 as review


class ReviewV3Tests(unittest.TestCase):
    def test_review_is_fresh_tool_free_and_has_lower_hard_budget(self):
        cmd=review.command()
        self.assertEqual(cmd[cmd.index('--max-budget-usd')+1],'3.8')
        self.assertEqual(cmd[cmd.index('--tools')+1],'')
        self.assertIn('--no-session-persistence',cmd);self.assertIn('--bare',cmd)
        self.assertEqual(cmd[cmd.index('--model')+1],'claude-opus-5-5')

    def test_no_new_authorization_blocks_before_key_or_cli(self):
        with patch.object(review.subprocess,'run',side_effect=AssertionError('must not call CLI')):
            with self.assertRaises(ValueError):review.invoke()


if __name__=='__main__':unittest.main()
