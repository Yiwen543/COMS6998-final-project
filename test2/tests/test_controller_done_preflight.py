import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import controller_done_preflight as preflight
from controller_done_loop import authorization,live_gate


class PreflightTests(unittest.TestCase):
    def test_approved_scope_excludes_generation_and_author(self):
        a=preflight.verify('token_count');self.assertEqual(a['approved_usd'],9)
        self.assertEqual(preflight.verify('reference_review')['claude_max_requests'],1)
        for scope in ('generation','author'):
            with self.assertRaises(ValueError):authorization(scope)
        with self.assertRaises(ValueError):live_gate()

    def test_durable_claim_prevents_repeat_paid_review(self):
        with tempfile.TemporaryDirectory() as t,patch.object(preflight,'OUT',Path(t)),patch.object(preflight,'key_present'),patch.object(preflight,'invoke',return_value=dict(status='fake')) as call:
            self.assertEqual(preflight.review(),'returned_requires_independent_audit')
            with self.assertRaises(FileExistsError):preflight.review()
            self.assertEqual(call.call_count,1)

    def test_failure_is_recorded_without_retry_and_claim_stays(self):
        with tempfile.TemporaryDirectory() as t,patch.object(preflight,'OUT',Path(t)),patch.object(preflight,'key_present'),patch.object(preflight,'invoke',side_effect=RuntimeError('synthetic failure')) as call:
            self.assertEqual(preflight.review(),'failed_no_retry')
            with self.assertRaises(FileExistsError):preflight.review()
            record=json.loads((Path(t)/'review-phase.json').read_text());self.assertEqual(record['result']['error_type'],'RuntimeError');self.assertEqual(call.call_count,1)

    def test_missing_credentials_do_not_consume_claim(self):
        with tempfile.TemporaryDirectory() as t,patch.object(preflight,'OUT',Path(t)),patch.object(preflight,'key_present',side_effect=ValueError('missing key')):
            with self.assertRaises(ValueError):preflight.counts()
            self.assertFalse((Path(t)/'count-request-claim.json').exists())


if __name__=='__main__':unittest.main()
